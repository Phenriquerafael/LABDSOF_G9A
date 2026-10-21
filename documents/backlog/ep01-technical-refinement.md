# EP-01 technical refinement register

**Scope:** follow-ups identified by [PLAN-01](tasks/PLAN-01-prepare-reporting-and-tracking-stories.md) for [US-01](tasks/US-01-record-and-view-report.md), [US-02](tasks/US-02-triage-manually-and-track-states.md), [US-04](tasks/US-04-publish-shared-issue-and-confirm-impact.md) and [US-10](tasks/US-10-notify-changes.md).

**Status:** open technical refinement; stack and architecture are not selected by these drafts. These entries track existing EN-01 design work, not additional implementation tasks or estimates. PLAN-01 may deliver reviewed drafts while these entries remain open; a story becomes Ready only after its applicable entries and other DoR conditions are satisfied.

Sandro Dias maintains drafting traceability. EN-01's allocated owner coordinates the relevant design work, with product/security input as appropriate; implementation owners and independent reviewers are assigned in planning. No role proposal below claims a meeting or accepted decision.

## R01 — Stack and component boundaries

- Applies to: all four stories.
- Design work: [EN-01-01](tasks/EN-01-01-select-stack-and-boundaries.md), [EN-01-03](tasks/EN-01-03-consolidate-architecture-views.md); DEC-04/06.
- Resolve: client/backend/persistence/transport stack, Issue/Dispatch ownership, notification worker placement, independently deployable boundaries or an accepted alternative, and relevant service-to-service communication.
- Closure evidence: accepted ADRs and updated component/deployment view, linked from the affected stories. Do not treat the conceptual Issue/Dispatch proposal as accepted architecture.
- Closure record: open; add actual decision/reviewer/date references when resolved.

## R02 — Reports, persistence and API contracts

- Applies to: US-01, US-02, US-04.
- Design work: [EN-01-02](tasks/EN-01-02-define-domain-and-contracts.md); DEC-04/07.
- Resolve: request/query schemas, field limits, building/area relationship, report/issue identity, summary/impact/subscription data, errors, idempotency identity scope/lifetime and mismatched-content behaviour, persistence atomicity and restart behaviour.
- Closure evidence: reviewed representative requests/responses/error examples and data-ownership/lifecycle model. Map user-visible receipt to durable storage; record the handoff to asynchronous consumers without losing saved reports.
- Closure record: open; add actual contract/reviewer/date references when resolved.

## R03 — Identity, authorisation and safe projections

- Applies to: all four stories.
- Design work: [EN-01-02](tasks/EN-01-02-define-domain-and-contracts.md), [EN-01-04](tasks/EN-01-04-review-security-and-privacy.md); DEC-07.
- Resolve: real or permitted mocked identity, trustworthy membership context, resource/field checks for own reports versus shared summaries, administrator scope, contributor privacy and recipient/read-time checks after access changes.
- Closure evidence: reviewed access/projection matrix and negative scenarios for unauthenticated, same-building non-author, other-building, administrator and contractor callers. Mock identity must not allow callers to choose arbitrary permissions.
- Closure record: open; add actual security/contract/reviewer/date references when resolved.

## R04 — States, history and concurrent changes

- Applies to: US-02 and US-10; report creation in US-01 supplies the initial received state.
- Design work: [EN-01-02](tasks/EN-01-02-define-domain-and-contracts.md); DEC-07/10.
- Resolve: allowed category/urgency values and manual transitions, audit fields/public projection, version/conflict contract, intervention status projection and late AI-result handling. Preserve distinct request approval, contractor acceptance and booking confirmation.
- Closure evidence: reviewed transition/visibility examples, valid/invalid action table and stale-version scenario. Link EP-02's human-decision protection and EP-03 source-event contracts without cross-writing owned data.
- Closure record: open; add actual model/contract/reviewer/date references when resolved.

## R05 — Events, notifications and optional preferences

- Applies to: US-10 and US-04; US-02 supplies state-change events.
- Design work: [EN-01-01](tasks/EN-01-01-select-stack-and-boundaries.md), [EN-01-02](tasks/EN-01-02-define-domain-and-contracts.md), [EN-01-03](tasks/EN-01-03-consolidate-architecture-views.md); DEC-04/06/07.
- Resolve: selected notification channel, event schemas/versions/identities/correlation, recipient rules, optional versus required updates, preference changes, state/event handoff, bounded retry/final failure policy and event/recipient deduplication across restarts.
- Cross-epic contract: agree EP-03 US-07 event examples and permitted data with the [intervention epic](epics/EP-03-intervention-and-closure.md). Fixtures can support early development; final story completion includes the actual producer integration. No dependency on the whole EP-03 epic or on delivery succeeding before the source transaction commits.
- Closure evidence: reviewed event examples, subscriber/recipient matrix and failure/replay/restart scenarios. Link agreed contracts and their producers/consumers from US-10.
- Closure record: open; add actual event/channel/reviewer/date references when resolved.

## R06 — Test environment, delivery and measurable evidence

- Applies to: all four stories.
- Design work: [EN-01-03](tasks/EN-01-03-consolidate-architecture-views.md), [EN-01-04](tasks/EN-01-04-review-security-and-privacy.md); EN-02/03/04 in the [product backlog](../06-product-backlog.md#3-discovery-and-engineering); DEC-08.
- Resolve: synthetic users/buildings/issues, API/contract/E2E environment, restart/AI-disabled/notification-failure scenarios, container/CI setup, sanitised observability evidence and agreed performance/accessibility scenarios. Framework/tool choices follow R01.
- Closure evidence: linked verification plan and reproducible environment instructions, with numerical thresholds reviewed before measuring. Actual execution evidence belongs to story implementation, not this drafting task; final usability/performance evaluation remains EN-04.
- Closure record: open; add actual plan/environment/reviewer/date references when resolved.

## Closure procedure

For each applicable entry, record the accepted decision/contract, affected stories, reviewer/date and any remaining limitation; update the source design/ADR before marking a story Ready. Use the [decision register](../planning/decisions-and-feedback.md) for decision rationale. A reference to a still-open decision does not close an entry. Apply the [DoR](../governance/definition-of-ready.md) and avoid counting this register as six extra delivery tasks.
