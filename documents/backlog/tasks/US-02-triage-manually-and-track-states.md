# [US-02] Triage manually and track states

## Identification

- Local ID / epic: US-02 / [EP-01 — Reporting and tracking](../epics/EP-01-reporting-and-tracking.md) (direct child).
- Requirement(s), hypothesis/finding and journey: RF-02; P1/P3; J1–J2; NFR-01/02/03/06/07/09; [requirements](../../requirements.md), [vision](../../04-product-vision.md), [assignment](../../../LABDSOF-26-27-Assignment.md).
- Proposed MoSCoW priority / reason: Must — provides administrator decisions and auditable progress, including when AI is unavailable.
- Official milestone: proposed S2 initial delivery and S3 refinement/evaluation; No Sprint 1 implementation commitment.
- Blocking decisions/dependencies: DEC-04, DEC-07 and DEC-10 in the [decision register](../../planning/decisions-and-feedback.md). Close applicable EN-01 refinements before implementation readiness.

[US-01](US-01-record-and-view-report.md) for persisted reports; [EN-01 design](EN-01-technical-design.md) for permissions, state rules and contracts. AI suggestions and EP-03 intervention updates integrate later; manual triage does not require either whole epic to be completed.

The [technical design](../../08-technical-design.md) and [access matrix](../../09-security-privacy.md#2-proposed-access-matrix) are conceptual inputs, not accepted stack/contracts. These criteria describe behaviour without selecting a framework, database, broker or provider.

Draft status: Backlog; technical refinement required before Ready. No GitHub story URL recorded. Sandro Dias under [PLAN-01](PLAN-01-prepare-reporting-and-tracking-stories.md). Implementation allocation: see the [backlog index](../README.md#ep-01-story-drafts-and-planning-allocation).

## Story

As a **administrator**, I want to **review issues, set category and urgency manually, and inspect their history**, so that **I can decide the next step and explain the decisions without depending on AI**.

## Scope

Included: Authorised administrator queue/detail, explicit pending triage, manual category/urgency decisions, permitted state changes, audit history and resident-safe status/history projections.

Excluded: AI generation/provider integration, publishing shared summaries, contractor approval/booking/completion/closure actions (EP-03), notification delivery and finalising the stack.

## Acceptance criteria

- [ ] **Managed queue:** Given an administrator, when listing or opening issues, then only managed-building resources are returned; category/urgency not yet decided are explicitly shown as pending, without inventing a decision.
- [ ] **Manual decision:** Given an authorised administrator and valid category/urgency with a reason, when saved, then the human decision and history record contain actor, timestamp, reason and resulting version, and remain available after reload/restart.
- [ ] **State rules:** Given a permitted manual action in the reviewed state model, then the resulting state/history is persisted; an invalid transition, missing required reason or invalid triage value is rejected without a partial change. Approval, booking and closure actions remain in EP-03.
- [ ] **Concurrent editing:** Given two editors using the same version, when one saves and the other submits the stale version, then the second receives an understandable conflict and cannot silently overwrite the first decision or its audit trail.
- [ ] **Resident projection:** Given a resident authorised to view the issue under US-01 or the shared-summary rules of US-04, when querying status/history, then only permitted public fields/history are returned, without internal notes, private costs or other residents' raw text/identities.
- [ ] **Denied access:** Residents, contractors and administrators of another building cannot alter triage/state or inspect restricted history via the API, including by changing resource IDs.
- [ ] **AI independence:** With AI disabled, manual triage and queries remain usable. If a late AI result arrives after a human edit, it must not overwrite the human decision; coordinate this integration contract with EP-02.
- [ ] **Clear status:** Render confirmed human decisions separately from pending/unverified AI suggestions; support keyboard navigation and understandable validation/conflict errors.

## Verification and risks

Use synthetic managed/unmanaged buildings, administrator/resident/contractor identities and two concurrent edits. Verify decision/audit persistence, invalid transitions and reasons, stale conflicts, cross-building/role denials, resident-safe projections and manual operation with AI disabled. Later integrate a stale AI-result test under EP-02; a representative stub can test the contract before real inference exists. State/history API integration and principal triage E2E evidence are required for implementation.

Principal risks: Private history leaking into resident views, lost updates, late suggestions replacing human decisions and accidentally treating a request approval as booking confirmation.

This is a story draft: these are planned implementation checks, not executed tests. PLAN-01 validates document content, traceability, consistency and links only.

## Ready / Done

Technical refinement: R01 — stack/component boundaries; R02 — query/persistence contracts; R03 — authorisation; R04 — states, audit and versions; R06 — environment/evidence.

Close the applicable rows of the [EP-01 refinement register](../ep01-technical-refinement.md) using EN-01 decision/contract evidence; record any justified non-applicability. Do not invent concrete endpoints, queue names, database schemas or retry thresholds before those decisions.

- Implementation owner / independent reviewer / estimate / capacity / sprint:
- Refinement closure references and remaining limitations:
- [ ] DoR reviewed by the team; date/author:
- [ ] DoD verified with links to PR, tests and demonstration:

See [definition-of-ready.md](../../governance/definition-of-ready.md) and [definition-of-done.md](../../governance/definition-of-done.md). Do not mark Ready without estimates/capacity, agreed owner/reviewer and resolved dependencies. Record actual implementation/test/demo evidence before checking Done.
