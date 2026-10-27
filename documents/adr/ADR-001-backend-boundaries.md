# ADR-001 — Backend boundaries, data ownership and communication

**Status:** Proposed
**Date:** 2026-10-27
**Participants:** Ricardo (P2, Tech Lead) — proposer; Afonso (P3) to confirm the authorisation-context change in the Dispatch section below; team review pending
**Related decision:** DEC-04 (also DEC-06 for notifications)
**Supersedes / superseded by:** revises in place the 2026-10-15 version of this ADR (nothing had been accepted or merged); see [Record](#record)

## Context

§6.2 requires at least two independently deployable backend components; a modular alternative needs a justified, accepted exception (E01). BMC separates issue and triage handling from intervention preparation and execution, and the design adds notification delivery and AI classification as separate concerns. EN-01-01 ([#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15)) must decide boundaries, data ownership, communication and the consequences of shared infrastructure. Evidence is in the [evidence register](README.md#evidence-register-en-01-01); the domain model and states are in the [technical design](../07-technical-design.md#2-domain-model-and-data-ownership) (EN-01-02, merged).

The 2026-10-15 proposal (Issue + Dispatch + triage worker, notifications inside Issue, HTTP relay) already met §6.2 and §6.3. This revision moves notifications and AI triage into their own deployables and replaces synchronous service calls with messages (Tech Lead proposal of 2026-10-27; not lecturer feedback).

## Alternatives

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Issue + Dispatch + Notification + AI triage service** (chosen) | One deployable per bounded context or supporting concern; notification and AI failures cannot take Issue or Dispatch down; AI runtime (Python) isolated from the Java services; each service testable alone | Four business deployables plus platform containers; eventual consistency; contracts and message topology to maintain; more memory (to be measured, [ADR-004](ADR-004-deployment-contract.md)) | E01 §6.2; [ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md) |
| B. 2026-10-15 proposal: Issue + Dispatch + triage worker; notifications as an Issue module; HTTP outbox relay | Fewest containers; no broker | Worker depends on Issue's internal API; Dispatch calls Issue per administrator command, so Dispatch stops when Issue is down; email adapter and SMTP failures live inside Issue | E03 |
| C. A + notifications as a module inside Issue | One JVM fewer; no `NotificationRequested` hop for issue-side events | Channel adapters, preferences and delivery log mixed into the heaviest service; SMTP failure handling in Issue's process; Dispatch-driven notifications still need Issue | — |
| D. Modular monolith | Lowest operational and transaction cost | Exception to §6.2 needs evidence and lecturer acceptance; boundaries only as strong as the build and tests | E01 §6.2 |
| E. Service per role (resident, administrator, contractor) | Extensive separation | Roles are views over the same issues and interventions; no demonstrated need; duplicated data | — |

## Proposed decision (not accepted)

**A.** No modular-monolith exception is requested, so no lecturer acceptance is needed or claimed. Each unit is one deployable per bounded context; CQRS is used only as internal command and query packages, with no separate read store ([ADR-009](ADR-009-service-internal-architecture.md)).

| Unit | Owns | Database |
|---|---|---|
| Issue service | Organisations, buildings, areas, user profiles keyed by Keycloak `sub` (no credentials, [ADR-005](ADR-005-authentication-authorisation.md)), memberships, invitations, reports, attachment metadata ([ADR-010](ADR-010-object-storage.md)), issues, triage suggestions and decisions, summaries, impact confirmations, issue history, audit; decides notification recipients for issue-side events and for the Dispatch events it projects | `issue` |
| Dispatch service | Contractors and registrations, interventions, proposal versions, responses, bookings, completion reports, costs, audit, calendar adapter, contractor matching rules (rules, not AI); read projections of building administrators and of issue dispatchability | `dispatch` |
| Notification service | Inbox notifications, per-user preferences, delivery log; facade and channel adapters ([ADR-007](ADR-007-notification-service.md)) | `notification` |
| AI triage service | Stateless: consumes `TriageRequested`, publishes `TriageSuggested` ([ADR-008](ADR-008-ai-triage-service.md)) | none |
| Calendar simulator | Simulated external bookings, in memory ([ADR-006](ADR-006-calendar-simulator.md)); not one of the business components counted for §6.2 | none |

**Rules**

1. **Single writer.** Each service is the only writer of its database, with its own database user and migrations; no cross-database queries or writes. Cross-service references are IDs.
2. **No synchronous calls between services.** Services communicate only through RabbitMQ using the transactional outbox ([ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)). The client reaches services through REST routes at the edge ([ADR-004](ADR-004-deployment-contract.md)); internal endpoints (health, metrics, the AI service's `POST /classify` for AI-01 evaluation) are never routed. Calls from services to platform components (Keycloak, object storage, SMTP) are not service-to-service calls.
3. **Projections instead of lookups.** Dispatch keeps read projections fed by events: building administrators (from `MembershipGranted` / `MembershipRevoked`) and issue dispatchability (from `IssueStateChanged`). Issue's state reflects Dispatch only through events that Issue validates and applies by version.
4. **AI is a replaceable adapter.** The provider stays behind the triage facade; Gemini Flash free tier is the candidate, and provider, model and evaluation remain DEC-05/AI-01.

**Change to EN-01-02 §4.3 (authorisation context).** The merged design has Dispatch call Issue for `dispatch-context` and memberships on each administrator command. That is replaced: Dispatch authorises administrator commands against its projection (administrator membership for the issue's building, and a dispatchable issue state at a projection version) and still verifies the token's `sub` locally. This revises a proposal made by Afonso in EN-01-02; the record does not imply that he agreed.

| Aspect | Effect |
|---|---|
| Benefit | Dispatch keeps working when Issue is down, which the §6.8 degraded-mode demo needs |
| Cost | Revocation delay equals event propagation: normally seconds, unbounded while Dispatch's consumer or the broker is down. A revoked administrator could still issue commands in that window. Recorded as an EN-01-04 risk |
| Mitigation | Projection freshness metric; Dispatch shows "membership data as of …"; Issue rejects Dispatch events whose `issueId`/`buildingId` do not match its records (→ failed handling, DLQ); `IssueResolved` and `IssueCancelled` cancel interventions; contractor commands are already authorised from Dispatch's own data |

## Consequences

- Each service has its own build, image, configuration, health checks and migrations; deployment order is not coupled because contracts are versioned ([ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)).
- **Shared infrastructure** — single points of failure, stated as limits of the academic release: one MySQL 8.4 instance (a database and user per service, plus `keycloak`), one RabbitMQ node, one host. Mitigations: separate users and grants; broker-down behaviour that leaves business data intact (outbox rows stay pending); health and readiness checks; restart policies; DLQ and outbox-lag alerts; backup and restore exercise ([ADR-004](ADR-004-deployment-contract.md)). A node or host loss is not mitigated in the MVP.
- Eventual consistency is visible to users (history may show Dispatch events late; "triage pending"; "membership data as of …").
- Tests must cover consumer unavailability, redelivery, out-of-order events, stale projections and delayed updates (NFR-04).
- Effort is higher than options B–D; accepted to meet §6.2 without an exception. Re-estimate at Sprint B planning.

## Verification and review

Evidence once built: each service starts and passes its own tests with the others stopped; stopping Issue leaves contractor and administrator Dispatch commands working; stopping Dispatch's consumer shows projection staleness on the freshness metric; no service has credentials for another's database. Boundary tests per service are in [ADR-009](ADR-009-service-internal-architecture.md). Review at the team review of ADR-001–010 and at Sprint B planning.

Open items: which Dispatch-driven events Dispatch notifies directly and which Issue notifies after projecting them (to settle with EN-01-03); whether Issue's own events with no consumer (`ReportSubmitted`, `IssueTriaged`, `IssueSummaryPublished`) are still published; revocation-delay bound (EN-01-04); the service count's effect on measured memory (EN01-U3).

## Record

- 2026-10-07 — first proposal: Issue and Dispatch services with a triage worker.
- 2026-10-15 — first proposed in EN-01-01 by Ricardo (Tech Lead), revising the 2026-10-07 draft: Issue + Dispatch + triage worker, notifications as an Issue module, synchronous HTTP for immediate answers, HTTP relay, no broker (E03).
- 2026-10-27 — revised by Ricardo (Tech Lead) after a structured design interview; drafting and source checks AI-assisted. Reason: notifications and AI triage become separate deployables; all service-to-service communication moves to RabbitMQ; EN-01-02 §4.3 replaced by a Dispatch projection. Evidence: [evidence register](README.md#evidence-register-en-01-01) E01, E03, E27, E38; issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15). Affected documents: [technical design](../07-technical-design.md) §1, §2.1, §4.2–§4.4, [ADR index](README.md), DEC-04/06. Final decision, date and participants: pending team review.
