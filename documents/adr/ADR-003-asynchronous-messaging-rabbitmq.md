# ADR-003 — Asynchronous messaging: transactional outbox and RabbitMQ

**Status:** Proposed
**Date:** 2026-10-27
**Participants:** Ricardo (P2, Tech Lead) — proposer; Martim (P5) to confirm the DLQ runbook ownership; Sandro (P4) to confirm the AI message contracts; team review pending
**Related decision:** DEC-04; supports DEC-06 (notifications); DEC-07 note on `TriageRequested` below
**Supersedes / superseded by:** revises in place the 2026-10-15 version ("Asynchronous workflow without a broker"; file renamed); see [Record](#record)

## Context

§6.3 requires at least one meaningful asynchronous workflow with retries, duplicates, failures and eventual consistency; it does not require a broker (E01). NFR-04 requires that redelivery does not duplicate effects, that retries are limited with an observable final failure, and that a crash between persistence and publication is tested. The 2026-10-15 outbox with an HTTP relay already met §6.3 (E03). This revision proposes RabbitMQ because [ADR-001](ADR-001-backend-boundaries.md) now has four deployables that must talk only through messages, with fan-out to several consumers; broker redelivery, dead-lettering and a management UI replace code the team would otherwise write. This is a Tech Lead proposal of 2026-10-27, not lecturer feedback. The envelope and consistency rules of [design §5](../07-technical-design.md#5-asynchronous-workflow-and-consistency) are kept.

## Alternatives

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Hand-rolled outbox in a shared starter + RabbitMQ 4 quorum queues** (chosen) | Small code under our control; broker gives redelivery, dead-lettering, fan-out and a management UI; Spring AMQP supports publisher confirms | One more container and AMQP concepts; the starter is shared by all Spring services; outbox still needed | E12, E13, E37–E39 |
| B. 2026-10-15: outbox + HTTP relay, no broker | No extra infrastructure; works | Team owns retry and dead-letter code; receivers must be up; no fan-out; polling | E03 |
| C. Spring Modulith event externalisation | Native publication registry; `@Externalized` to AMQP | Its own docs say it lacks critical outbox features | E14 |
| D. Namastack Outbox | JPA and RabbitMQ modules, MySQL example, Apache-2.0 | Young project (v1.11.0, about 400 stars); recorded alternative if the hand-rolled starter proves costly | E15 |
| E. Dapr | Outbox pattern in the platform | Outbox covers only Dapr state-API writes, not our JPA tables; a sidecar per service plus extra services in Compose | E40 |
| F. Spring Cloud Stream | Binder abstraction | Java only (the AI service is Python); no outbox | E18 |
| G. Kafka | Replayable log | Disproportionate for the project; more operations | — |
| H. gRPC or RPC for internal calls | Typed calls | Synchronous coupling, against [ADR-001](ADR-001-backend-boundaries.md); Spring gRPC 1.1 pairing with Boot 4.1 not stated; a saga orchestrator is not needed (choreography and the EN-01-02 state machines suffice) | E19 |

## Proposed decision (not accepted)

**A**, proposed, not accepted.

1. **Outbox.** Each Spring service writes its domain change and an `outbox` row in one database transaction. A publisher polls every 1 s and sends with publisher confirms (`ConfirmType.CORRELATED`), marking the row sent only after the broker confirms. Code lives in `platform/bmc-messaging-spring-boot-starter` (outbox table and publisher, idempotent consumer with `processed_events` written in the same transaction as the effect, CloudEvents mapping, queue and DLQ declaration, metrics); no domain types. The AI service has a small Python counterpart.
2. **Topology.** One durable topic exchange `bmc.events`; routing key `<producer>.<eventType>` (for example `issue.IssueResolved`, `dispatch.BookingConfirmed`). One quorum queue per consumer: `issue.inbox`, `dispatch.inbox`, `notification.inbox`, `ai-triage.requests`, each bound only to the keys it needs. `x-delivery-limit` 5 (the 4.x default is 20). Dead-letter exchange `bmc.dlx` → `<queue>.dlq`, with `dead-letter-strategy=at-least-once` (requires `overflow=reject-publish`), because at-most-once is the default. Manual acknowledgement after the transaction commits; modest prefetch (configuration). Per-service broker credentials and vhost permissions: [ADR-005](ADR-005-authentication-authorisation.md).
3. **Wire format.** CloudEvents 1.0 structured JSON; `data` is the Protobuf payload in proto3 JSON mapping. `id` = eventId, `type` = eventType, `source` = producer, `subject` = aggregateId, `time` = occurredAt; extensions `schemaversion`, `aggregateversion`, `buildingid`, `correlationid`, `traceparent`. This maps the EN-01-02 envelope one-to-one.
4. **Schemas.** `.proto` files in `contracts/proto/` are the single source; Buf provides `buf lint`, `buf breaking` in CI and Java/Python generation; an AsyncAPI 3 document in `contracts/asyncapi/` describes channels with Protobuf `schemaFormat`. A consumer rejects an unsupported major `schemaversion` to the DLQ without retry.
5. **Idempotent consumers.** Duplicates are acknowledged without repeating the effect; processed event IDs are kept at least 7 days. "Exactly once" is not promised.
6. **Out-of-order events.** Unchanged from [design §3.3](../07-technical-design.md#33-invalid-and-concurrent-transitions): apply by `aggregateVersion`, ignore or reject stale ones; late triage results never override a human decision.
7. **Failure policy.** *Broker down:* outbox rows stay `pending`; the publisher retries with backoff (2 s doubling, cap 5 min) without limit; metric "outbox lag" and an alert; the user request already succeeded. *Consumer failure:* up to 5 deliveries, then `<queue>.dlq`; DLQ depth metric and alert. *Replay:* a runbook step (management-UI shovel back to the source queue), owned by Martim and safe because consumers are idempotent ([ADR-004](ADR-004-deployment-contract.md)).
8. **Event changes.** All EN-01-02 events stay ([design §4.4](../07-technical-design.md#44-event-contracts)); additions and changes:

| Event | Flow | Payload and rules |
|---|---|---|
| `TriageRequested` | Issue → AI, point-to-point (`issue.TriageRequested` bound only to `ai-triage.requests`) | `issueId`, `issueVersion`, `buildingId`, `areaKind`, the report text needed for classification. The only message type that carries private report text (DEC-07 note); never fanned out; DLQ messages expire after 7 days (`x-message-ttl` on the DLQ); payloads never logged |
| `TriageSuggested` | AI → Issue | `issueId`, `issueVersion`, category, urgency, rationale, origin (`ai`, `rules`, `fallback`), model/prompt/rules versions. Applied by version. No suggestion within 2 min: Issue shows "triage pending — classify manually"; no state change |
| `IssueStateChanged` | Issue → Dispatch projection | `issueId`, `buildingId`, state, version, dispatchable flag, category, urgency, area label, published-summary reference; never raw text |
| `MembershipGranted`, `MembershipRevoked` | Issue → Dispatch projection | `userId`, `buildingId`, role |
| `NotificationRequested` | Issue or Dispatch → Notification | `notificationId` (idempotency), `sourceEventId`, `recipientUserIds`, `templateKey`, params without private text, priority. Invitation exception: carries `recipientAddress` and the invite link because the invitee has no account; the DLQ TTL applies |

9. **Removed.** `POST /internal/triage-jobs/claim|complete`, `GET /internal/issues/{id}/dispatch-context`, `GET /internal/users/{id}/memberships` and `POST /internal/events`; the triage job table and `SKIP LOCKED` claiming (RabbitMQ is the queue).
10. **Values (proposals, to calibrate in the spike; not measured).**

| Mechanism | Value |
|---|---|
| Outbox publisher | Poll 1 s; backoff 2 s doubling to 5 min; unlimited while the broker is down |
| Consumer | Delivery limit 5, then DLQ; DLQ TTL 7 days |
| AI | 10 s per attempt (NFR-03), 2 attempts, then rules fallback; "triage pending" notice after 2 min |
| Calendar call | Unchanged: 5 s timeout; 5 attempts; backoff 5 s doubling to 2 min |
| Retention | Idempotency keys 24 h; processed event IDs at least 7 days |

## Consequences

- One more critical component: RabbitMQ is a single node and a single point of failure ([ADR-001](ADR-001-backend-boundaries.md)). Memory high watermark defaults to 0.6 of RAM (E39), which matters on a shared host.
- Reporting stays available when the broker or a consumer is down; effects arrive later (visible timestamps, "triage pending").
- At-least-once dead-lettering keeps messages until the target confirms and may duplicate them (E38); consumers are idempotent anyway.
- Immediate redelivery can exhaust the limit of 5 during a short database outage and send healthy messages to the DLQ; redelivery pacing (for example a bounded in-listener retry with backoff) is an open item for the spike (EN01-U7).
- Private text exists in `TriageRequested` messages in the queue and, on failure, in the DLQ for up to 7 days; the invitation address and link likewise. Security details are EN01-U6 (EN-01-04).
- A defect in the shared starter affects every Spring service; Namastack Outbox (option D) is the fallback.
- Which events have no bound consumer (and are therefore dropped by the exchange) is an open item; see [ADR-001](ADR-001-backend-boundaries.md).

## Verification and review

NFR-04 tests when the first asynchronous slice is built: crash after commit and before publish (event still delivered); duplicate delivery (single effect); out-of-order events (stale ones ignored); exhausted deliveries (message in the DLQ, metric raised, replay works); broker down then up (outbox drains); consumer down then up (queue drains). Spike items: 4 outbox publisher with confirms survives a kill between commit and publish; 5 quorum queue dead-letters at-least-once to the DLQ (including the `reject-publish` requirement); 6 proto3 JSON round-trip; 7 pika consumer in the Flask image. Pin the RabbitMQ minor at the spike (4.4.0 is the latest, E37). Review after the spike and at Sprint B planning.

## Record

- 2026-10-15 — first proposed: transactional outbox, triage job table with `SKIP LOCKED` claiming and HTTP relay between services, no broker (E03).
- 2026-10-27 — revised by Ricardo (Tech Lead) after a structured design interview; drafting and source checks AI-assisted. Reason: four deployables communicating only through messages, with fan-out, broker-managed redelivery and dead-lettering. Evidence: [evidence register](README.md#evidence-register-en-01-01) E01, E03, E12–E15, E18, E19, E37–E43; issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15). Affected documents: [technical design](../07-technical-design.md) §2.1, §4.2–§4.4, §4.6, §5, §7, EN-01-02 §4.3, requirements NFR-04, DEC-04/06. Final decision, date and participants: pending team review.
