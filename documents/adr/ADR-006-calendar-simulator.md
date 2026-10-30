# ADR-006 — External calendar simulator as a separate process, and reconciliation

**Status:** Proposed
**Date:** 2026-10-27
**Participants:** Ricardo (P2, Tech Lead) — proposer; Afonso (P3, BA/PO, intervention backend) to confirm; team review pending
**Related decision:** DEC-06
**Supersedes / superseded by:** — (the 2026-10-15 version was revised in place; see Record)

## Context

§6.5 requires integration with an external system or a realistic simulator, with handling of unavailable, delayed, incomplete or invalid data (E01). §6.8 requires one degraded-mode scenario that can be demonstrated. The [design §6](../07-technical-design.md#6-external-integration-and-degraded-mode) lists the scenarios (success, timeout, unavailability, delay, incomplete/invalid response, scheduling conflict) and the rule that a timeout may happen after creation, so Dispatch must query and reconcile before retrying. The [contract outline](../07-technical-design.md#45-calendarsimulator-contract-outline) fixes the operations, the idempotency key and the `discrepancy` state; this ADR does not change that behaviour, only where the simulator runs and how it is built.

Dispatch is the only caller. It reaches the calendar through a provider-neutral `CalendarPort` ([ADR-009](ADR-009-service-internal-architecture.md)), so a real calendar (US-13, Could) can replace the simulator behind the same port.

## Why a separate process

The Tech Lead asked for this choice to be justified explicitly. Three reasons, one per requirement:

| Reason | Argument |
|---|---|
| §6.5 — real failures | Unavailable and delayed data are network phenomena. With a separate process Dispatch sees a real `connection refused`, a real read timeout and a real late answer, so its HTTP client, timeout and retry configuration are exercised rather than assumed. In an in-process fake each failure becomes an `if` statement that returns a prepared exception; the code under test never meets the failure it claims to handle. |
| §6.8 — degraded-mode demo | The demo needs the “external system” to disappear while the product stays up. A separate container can be stopped, delayed or restarted on its own (`docker compose stop calendar-sim`) while Dispatch keeps running, shows pending/manual bookings and reconciles after the simulator returns. An in-process fake cannot be stopped without stopping Dispatch. A restart also gives the “external system lost data” scenario for free, because state is in memory. |
| §6.2 / [ADR-001](ADR-001-backend-boundaries.md) — not a business component | The business components counted for §6.2 are the ones in ADR-001. The simulator is outside that count: it owns no business data, has no database and is not on the public route. A separate directory (`tools/calendar-sim`), image and container make that visible to a reviewer; code inside Dispatch would blur it. |

The in-process fake is not discarded. It stays as the test double behind `CalendarPort` for fast unit and slice tests of Dispatch (no container needed). It does not replace the simulator for the integration tests and the demo, because it cannot produce the network failures above.

## Alternatives

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Separate small Spring Boot app (`tools/calendar-sim`)** | Real network failures; stoppable on its own; every scenario triggerable on demand; same Java tooling as the other services; no OAuth or quota | One more JVM in the stack (memory to be measured in the spike); must model only the external system | E01 §6.5 and §6.8; E04 |
| B. In-process fake inside Dispatch | No extra container; fast | Failures are `if` statements; the “external system” cannot be stopped without stopping Dispatch; blurs §6.2; kept only as a `CalendarPort` test double | E01 |
| C. The 2026-10-15 Elysia-on-Bun simulator | Same behaviour; already described | Rejected only because the stack changed ([ADR-002](ADR-002-technology-stack.md)): a Bun container would be the only TypeScript backend and the team's Java experience would not apply to it | E03 |
| D. Google Calendar API | Real external system | OAuth setup and secrets; quotas; failures cannot be forced on demand; account needed for the demo | — |
| E. Self-hosted CalDAV server | Real protocol | Weak scenario control; extra server to run; idempotency key and `requestId` lookup are not CalDAV concepts | — |
| F. WireMock | Scripted responses and fault injection (delay, connection reset) with little code | Stateful, idempotent bookings and reconciliation after a restart are awkward to express as stubs; the logic would live in mapping files | — |
| G. No integration | — | Fails §6.5 | E01 |

Options D, E and F are assessed from their general properties, not from sources read for this ADR; no evidence IDs are claimed for them.

## Proposed decision

**A**, proposed, not accepted:

- A small Spring Boot application in `tools/calendar-sim` (Java 25, same Boot line as the services), packaged as its own image and Compose service on the internal network. It exposes booking creation with an idempotency key and a stable external reference, booking query by `requestId`, and cancellation, as in the [contract outline](../07-technical-design.md#45-calendarsimulator-contract-outline), documented with OpenAPI.
- A scenario control endpoint (internal network only, never routed by Traefik) selects the behaviour per request or globally: success, timeout after creation, unavailable, delay, invalid/incomplete response, conflict.
- State is **in memory**, loaded from a fixed seed so it starts the same way every time. A restart is a documented “external system lost data” scenario that Dispatch reconciliation must surface as `discrepancy`; the simulator has no database.
- Dispatch uses `CalendarPort` with an HTTP adapter (`adapters.out`) and an in-process fake for tests. Contract behaviour is unchanged: `Idempotency-Key` = booking ID, validity check of a `2xx` answer, `uncertain` → reconcile before any re-send, `discrepancy` never silently recreated. Calendar values stay as in [design §4.6](../07-technical-design.md#46-retry-timeout-and-lease-values-proposal) (5 s timeout, 5 attempts, backoff 5 s doubling to 2 min).
- Manual confirmation stays distinct from external synchronisation and suspends automatic re-creation until reconciliation.

## Consequences

- Integration failure tests (NFR-11) are reproducible in CI and demos, and use real network behaviour.
- One more JVM in the Compose stack. Its memory cost is not measured; the spike measures the full stack ([ADR-004](ADR-004-deployment-contract.md)).
- The simulator must not become a business component: no business data, no domain code shared with the services, no route through Traefik.
- Dispatch keeps working while the simulator is down (bookings stay `requested`/`uncertain`, the administrator can confirm manually); this is the §6.8 scenario candidate, together with the AI fallback ([ADR-008](ADR-008-ai-triage-service.md)).
- A real calendar would add OAuth secret handling and a new security review.

## Verification and review

Sprint B evidence to produce (none exists yet): success; timeout-after-create with reconciliation; duplicate request (one booking); conflict; invalid/incomplete response; simulator stopped and restarted (`discrepancy`); Dispatch started while the simulator is down. The tests run against the simulator container, with the in-process fake used only for unit tests. EN-01-01 consolidates the integration view. Review if the lecturer requires a real provider or if the simulator's memory cost is a problem on the demonstration host (EN01-U3).

## Record

2026-10-15 — first proposed by Ricardo (Tech Lead) after a structured design interview for EN-01-01: a separate Elysia-on-Bun container (`apps/calendar-sim`) with an in-memory state, scenario control endpoint and a provider-neutral adapter; drafting AI-assisted.

2026-10-27 — revised by Ricardo (Tech Lead) after a structured design interview; drafting and source checks AI-assisted. Reason: the stack changed to Java and Spring ([ADR-002](ADR-002-technology-stack.md)), so the simulator becomes a small Spring Boot app; the reasons for a separate process were made explicit (§6.5, §6.8, §6.2) and the in-process fake was limited to a test double; contract behaviour unchanged. Evidence: [evidence register](README.md#evidence-register-en-01-01) E01, E03, E04. Affected documents: [technical design §4.5, §6](../07-technical-design.md#45-calendarsimulator-contract-outline), DEC-06. Final decision, date and participants: pending team review. Issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15).
