# [US-02] Triage manually and track states

## Planning

- Epic: [EP-01 — Reporting and tracking](../epics/EP-01-reporting-and-tracking.md).
- Priority: Must.
- Estimate: 8 story points — manual triage, state/history views, permissions, concurrent edits and tests.
- Sprint: implement in S2 and refine/evaluate in S3.
- Dependencies: [US-01](US-01-record-and-view-report.md) for saved reports and [EN-01](EN-01-technical-design.md) for permissions, states and contracts. Manual triage does not require AI or the whole intervention epic.

## Story

As an **administrator**, I want to **review issues, set their category and urgency, and view their history**, so that **I can decide the next step without depending on AI**.

## Scope

List issues from managed buildings, record manual triage and permitted state changes, and show history according to the user's permissions.

This story does not cover AI generation, shared publication, intervention approval/booking/closure or notification delivery.

## Acceptance criteria

- [ ] Show administrators only issues from buildings they manage. Display an undecided category or urgency as pending rather than inventing a decision.
- [ ] Save a valid manual category/urgency decision with its actor, timestamp, reason and version. Keep the decision and history after reload or restart.
- [ ] Allow only the agreed manual state changes. Reject invalid values, transitions or missing required reasons without a partial update. Intervention approval, booking and closure remain in EP-03.
- [ ] Reject a save based on an outdated version when another edit has already been accepted. Explain the conflict without overwriting the newer decision or history.
- [ ] Let residents authorised through US-01 or US-04 view only permitted public status/history. Exclude internal notes, private costs and other residents' raw text or identities.
- [ ] Check permissions in the backend. Residents, contractors and administrators of another building cannot change triage/state or read restricted history, including by changing resource IDs.
- [ ] Keep manual triage and queries available with AI disabled. A late AI result must not overwrite a newer human decision; coordinate this contract with EP-02.
- [ ] Clearly distinguish confirmed human decisions from pending or unverified suggestions. Support keyboard navigation and understandable validation/conflict messages. Keep request approval, contractor acceptance and booking confirmation distinct in the displayed status.

## Verification and risks

Use synthetic users from managed and unmanaged buildings. Test saved decisions/history, invalid transitions, missing reasons, concurrent edits, denied access, resident views and unavailable AI. Include a manual-triage journey and a late-result fixture; verify the actual AI integration when available.

The main risks are private history leaks, lost updates and late suggestions replacing human decisions.

References: RF-02, P1/P3, J1–J2 and NFR-01/02/03/06/07/09 in the [requirements](../../requirements.md).

## Ready / Done

Before starting, agree allowed labels/transitions, required reasons, audit fields, public history, version conflicts, permissions, late AI handling and intervention status events. Confirm DEC-04/07/10, component/data ownership and the test environment with EN-01 using the [technical design](../../08-technical-design.md).

- [ ] Ready: estimate recorded, blocking decisions resolved and [DoR](../../governance/definition-of-ready.md) reviewed by the team.
- [ ] Done: acceptance criteria met, changes reviewed, PR and tests.
