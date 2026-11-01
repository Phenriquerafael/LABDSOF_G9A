# ADR-006 — External calendar: Google Calendar behind CalendarPort, with a simulator for tests and failure modes

**Status:** Proposed
**Date:** 2026-11-01
**Participants:** Ricardo (P2, Tech Lead) — proposer; Afonso (P3, BA/PO, intervention backend) to confirm; team review pending
**Related decision:** DEC-06
**Supersedes / superseded by:** — (the 2026-10-15 version was revised in place; see Record)

## Context

§6.5 requires integration with an external system or a realistic simulator, with handling of unavailable, delayed, incomplete or invalid data (E01). §6.8 requires one degraded-mode scenario that can be demonstrated. The [design §6](../07-technical-design.md#6-external-integration-and-degraded-mode) lists the scenarios (success, timeout, unavailability, delay, incomplete/invalid response, scheduling conflict) and the rule that a timeout may happen after creation, so Dispatch must query and reconcile before retrying. The [contract outline](../07-technical-design.md#45-calendarsimulator-contract-outline) fixes the operations, the idempotency key and the `discrepancy` state; this ADR does not change that behaviour; it decides which external system Dispatch talks to, and where the simulator runs and how it is built.

Dispatch is the only caller. It reaches the calendar through a provider-neutral `CalendarPort` ([ADR-009](ADR-009-service-internal-architecture.md)). Until 2026-10-31 this ADR used only the simulator and rejected Google Calendar (option D); after Martim's review of [PR #45](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/45) the Tech Lead revised it on 2026-11-01: Google Calendar is the external system of the live system, and the simulator stays for tests, offline work and failure demos. A real calendar was backlog story US-13 (Could); its priority is for the backlog owners to revisit.

## Why a separate process

The Tech Lead asked for this choice to be justified explicitly. The reasons below were written when the simulator was the only external system; they now justify keeping a separate simulator next to the Google Calendar adapter, because Google's failures cannot be forced on demand. Three reasons, one per requirement:

| Reason | Argument |
|---|---|
| §6.5 — real failures | Unavailable and delayed data are network phenomena. With a separate process Dispatch sees a real `connection refused`, a real read timeout and a real late answer, so its HTTP client, timeout and retry configuration are exercised rather than assumed. In an in-process fake each failure becomes an `if` statement that returns a prepared exception; the code under test never meets the failure it claims to handle. |
| §6.8 — degraded-mode demo | The demo needs the “external system” to disappear while the product stays up. A separate container can be stopped, delayed or restarted on its own (`docker compose stop calendar-sim`) while Dispatch keeps running, shows pending/manual bookings and reconciles after the simulator returns. An in-process fake cannot be stopped without stopping Dispatch. A restart also gives the “external system lost data” scenario for free, because state is in memory. |
| §6.2 / [ADR-001](ADR-001-backend-boundaries.md) — not a business component | The business components counted for §6.2 are the ones in ADR-001. The simulator is outside that count: it owns no business data, has no database and is not on the public route. A separate directory (`tools/calendar-sim`), image and container make that visible to a reviewer; code inside Dispatch would blur it. |

The in-process fake is not discarded. It stays as the test double behind `CalendarPort` for fast unit and slice tests of Dispatch (no container needed). It does not replace the simulator for the integration tests and the demo, because it cannot produce the network failures above.

## Alternatives

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A + D. Google Calendar adapter for the live system + the existing separate simulator for tests, offline work and failure demos** (chosen) | A real external system in the live system (D) and every failure scenario triggerable on demand (A), behind one `CalendarPort` with two adapters selected by configuration | The costs of both rows below; two adapters to keep on the same outcome classification | E01 §6.5 and §6.8; E04; E87 |
| A. Separate small Spring Boot app (`tools/calendar-sim`) only (the 2026-10-27 choice) | Real network failures; stoppable on its own; every scenario triggerable on demand; same Java tooling as the other services; no OAuth or quota | No real external system; one more JVM in the stack (memory to be measured in the spike); must model only the external system. Kept inside the chosen option | E01 §6.5 and §6.8; E04 |
| B. In-process fake inside Dispatch | No extra container; fast | Failures are `if` statements; the “external system” cannot be stopped without stopping Dispatch; blurs §6.2; kept only as a `CalendarPort` test double | E01 |
| C. The 2026-10-15 Elysia-on-Bun simulator | Same behaviour; already described | Rejected only because the stack changed ([ADR-002](ADR-002-technology-stack.md)): a Bun container would be the only TypeScript backend and the team's Java experience would not apply to it | E03 |
| D. Google Calendar API v3 over HTTPS through a Google Calendar adapter (the live integration in the chosen option; rejected in the 2026-10-27 version) | Real external system; the client may set the event ID, so the booking ID becomes the event ID (E87) | OAuth client or service-account credentials, a secret in the host environment; API quota; a Google account and calendar for the demo; failures cannot be forced on demand, so the simulator covers them; ID collisions are not guaranteed to be detected at event creation (E87); Dispatch needs internet access | E87 |
| E. Self-hosted CalDAV server | Real protocol | Weak scenario control; extra server to run; idempotency key and `requestId` lookup are not CalDAV concepts | — |
| F. WireMock | Scripted responses and fault injection (delay, connection reset) with little code | Stateful, idempotent bookings and reconciliation after a restart are awkward to express as stubs; the logic would live in mapping files | — |
| G. No integration | — | Fails §6.5 | E01 |

For option D only the event-ID facts are sourced (E87); its credential, quota and account costs, and options E and F, are assessed from general properties, not from sources read for this ADR.

## Proposed decision

**A + D**, proposed, not accepted:

- **Google Calendar is the external system.** Dispatch reaches it through `CalendarPort` with a Google Calendar adapter (`adapters.out`; Google Calendar API v3 over HTTPS). Dispatch therefore joins the `egress` network ([ADR-004](ADR-004-deployment-contract.md)). Whether the adapter uses a service account or an OAuth client is a spike item; the secret lives in the host environment, never in Git.
- **Event ID = booking ID.** Dispatch sets its booking ID as the Google event ID: a UUID in lowercase hex without hyphens fits the base32hex alphabet (a–v, 0–9) and the 5–1024 length, and Google recommends an RFC 4122 UUID (E87). Google does not guarantee that ID collisions are detected at event creation (E87), so a create cannot be trusted to fail on a repeat; the reconcile-before-retry rule stays: after a timeout or an uncertain answer Dispatch queries the event by ID before any re-send. A create that timed out may still complete after that lookup finds nothing, so duplicate prevention with Google is best effort until the adapter spike; the simulator keeps the strict at-most-one-booking behaviour. How Google's answers map to the outcomes in [design §4.5](../07-technical-design.md#45-calendarsimulator-contract-outline) is a spike item.
- **The simulator stays**, selected by configuration instead of the Google adapter, for integration tests, offline work and the §6.5/§6.8 failure-mode demos, because Google's failures cannot be forced on demand. A small Spring Boot application in `tools/calendar-sim` (Java 25, same Boot line as the services), packaged as its own image and Compose service on the internal network. It exposes booking creation with an idempotency key and a stable external reference, booking query by `requestId`, and cancellation, as in the [contract outline](../07-technical-design.md#45-calendarsimulator-contract-outline), documented with OpenAPI.
- A scenario control endpoint (internal network only, never routed by Traefik) selects the behaviour per request or globally: success, timeout after creation, unavailable, delay, invalid/incomplete response, conflict.
- State is **in memory**, loaded from a fixed seed so it starts the same way every time. A restart is a documented “external system lost data” scenario that Dispatch reconciliation must surface as `discrepancy`; the simulator has no database.
- Dispatch uses `CalendarPort` with two adapters in `adapters.out` (Google Calendar and the simulator's HTTP API, selected by configuration) and an in-process fake for tests. Contract behaviour is unchanged: `Idempotency-Key` (simulator) or event ID (Google) = booking ID, validity check of a `2xx` answer, `uncertain` → reconcile before any re-send, `discrepancy` never silently recreated. Calendar values stay as in [design §4.6](../07-technical-design.md#46-retry-timeout-and-lease-values-proposal) (5 s timeout, 5 attempts, backoff 5 s doubling to 2 min).
- Manual confirmation stays distinct from external synchronisation and suspends automatic re-creation until reconciliation. Degraded behaviour is the same with either adapter: bookings stay `requested`/`uncertain` and the administrator can confirm manually.

## Consequences

- Integration failure tests (NFR-11) are reproducible in CI and demos, and use real network behaviour.
- NFR-11's "repetition does not duplicate bookings" holds strictly with the simulator; with Google Calendar it is best effort until the adapter spike: Google does not guarantee that ID collisions are detected (E87), and a timed-out create may still complete after the lookup.
- One more JVM in the Compose stack. Its memory cost is not measured; the spike measures the full stack ([ADR-004](ADR-004-deployment-contract.md)).
- The simulator must not become a business component: no business data, no domain code shared with the services, no route through Traefik.
- Dispatch keeps working while the calendar is down (bookings stay `requested`/`uncertain`, the administrator can confirm manually); stopping the simulator is the §6.8 scenario candidate, together with the AI fallback ([ADR-008](ADR-008-ai-triage-service.md)).
- The Google adapter adds a credentials secret, internet access for Dispatch (`egress`, no allow-list in the MVP) and API quota; it needs the EN-01-04 security review. A Google account and calendar are needed for the demo.
- Two adapters must keep the same outcome classification; the contract tests run against the simulator, and the Google adapter is checked against the same cases where Google allows it.

## Verification and review

Sprint B evidence to produce (none exists yet): success; timeout-after-create with reconciliation; duplicate request (one booking); conflict; invalid/incomplete response; simulator stopped and restarted (`discrepancy`); Dispatch started while the simulator is down. The tests run against the simulator container, with the in-process fake used only for unit tests. Against Google, with test credentials (spike item): create with the booking ID as event ID, query by ID, cancel, and a forced client timeout followed by reconciliation by ID leaves one event. EN-01-01 consolidates the integration view. Review if Google credentials or quota fail the spike, or if the simulator's memory cost is a problem on the demonstration host (EN01-U3).

## Record

2026-10-15 — first proposed by Ricardo (Tech Lead) after a structured design interview for EN-01-01: a separate Elysia-on-Bun container (`apps/calendar-sim`) with an in-memory state, scenario control endpoint and a provider-neutral adapter; drafting AI-assisted.

2026-10-27 — revised by Ricardo (Tech Lead) after a structured design interview; drafting and source checks AI-assisted. Reason: the stack changed to Java and Spring ([ADR-002](ADR-002-technology-stack.md)), so the simulator becomes a small Spring Boot app; the reasons for a separate process were made explicit (§6.5, §6.8, §6.2) and the in-process fake was limited to a test double; contract behaviour unchanged. Evidence: [evidence register](README.md#evidence-register-en-01-01) E01, E03, E04. Affected documents: [technical design §4.5, §6](../07-technical-design.md#45-calendarsimulator-contract-outline), DEC-06. Final decision, date and participants: pending team review. Issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15).

2026-11-01 — revised by Ricardo (Tech Lead) after Martim's review of [PR #45](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/45) (2026-10-31) and the Copilot review of 2026-10-31; drafting AI-assisted. Reason: Google Calendar becomes the external system behind `CalendarPort` (option D, rejected on 2026-10-27, is now the live integration); the simulator stays for tests, offline work and failure demos because Google's failures cannot be forced; booking ID used as the Google event ID, with reconcile-before-retry kept because collisions are not guaranteed to be detected at creation; Dispatch joins the `egress` network. Contract behaviour unchanged, except that duplicate prevention with Google is best effort until the adapter spike (NFR-11). Evidence: E01, E04, E87; [review decisions](../planning/decisions-and-feedback.md#review-decisions--en-01-01-2026-11-01). Affected documents: [technical design §1, §4.5, §6](../07-technical-design.md#45-calendarsimulator-contract-outline), [ADR-004](ADR-004-deployment-contract.md), [backlog](../05-product-backlog.md) (US-13 note), DEC-06. Still Proposed; final decision pending team review.
