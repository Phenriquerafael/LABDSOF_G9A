# [US-04] Publish a shared issue and confirm impact

## Identification

- Local ID / epic: US-04 / [EP-01 — Reporting and tracking](../epics/EP-01-reporting-and-tracking.md) (direct child).
- Requirement(s), hypothesis/finding and journey: RF-04; P2/P5; J1–J2; assignment §5.5; NFR-01/02/04/07/09; [requirements](../../requirements.md), [vision](../../04-product-vision.md), [assignment](../../../LABDSOF-26-27-Assignment.md).
- Proposed MoSCoW priority / reason: Must — enables privacy-preserving shared impact and constructive, optional participation.
- Official milestone: proposed S2 initial delivery and S3 refinement/evaluation; No Sprint 1 implementation commitment.
- Blocking decisions/dependencies: DEC-04 and DEC-07 in the [decision register](../../planning/decisions-and-feedback.md). Close applicable EN-01 refinements before implementation readiness.

[US-01](US-01-record-and-view-report.md) for reports and [US-02](US-02-triage-manually-and-track-states.md) for administrator review/status. [US-10](US-10-notify-changes.md) consumes the resulting events/preferences, but its delivery is not required to publish or confirm impact.

The [technical design](../../08-technical-design.md) and [access matrix](../../09-security-privacy.md#2-proposed-access-matrix) are conceptual inputs, not accepted stack/contracts. These criteria describe behaviour without selecting a framework, database, broker or provider.

Draft status: Backlog; technical refinement required before Ready. No GitHub story URL recorded. Sandro Dias under [PLAN-01](PLAN-01-prepare-reporting-and-tracking-stories.md). Implementation allocation: see the [backlog index](../README.md#ep-01-story-drafts-and-planning-allocation).

## Story

As a **resident**, I want to **view an administrator-published shared issue and confirm that it affects me**, so that **I can contribute useful impact information without repeating the report**.

## Scope

Included: Explicit administrator publication of a safe shared summary, same-building visibility, one impact contribution per user/issue, withdrawal and optional subscription control.

Excluded: Publishing raw reports, AI summary generation, automatic duplicate merging, automatic urgency changes, public contributor identities, leaderboards and notification transport.

## Acceptance criteria

- [ ] **Explicit publication:** Given an issue in a managed building, when its administrator reviews and publishes a shared summary, then same-building residents can view that summary and authorised status. Before publication, raw report text is not made shared by default.
- [ ] **Publication authority:** Only the authorised building administrator can publish/change the summary. Reject invalid publication content or unauthorised/cross-building publication without exposing private fields.
- [ ] **Safe shared view:** The shared listing, detail and API expose only the reviewed summary and permitted fields, never the original private text, contributor identities, internal notes or private costs.
- [ ] **Unique contribution:** Given an authorised same-building resident, when they confirm impact, then one contribution is recorded. Repeated or concurrent confirmations by that user for the same issue do not increase the count twice.
- [ ] **Withdrawal:** Given an existing own contribution, when withdrawn, then it no longer contributes to the count. Repeated withdrawal remains safe, and a user cannot remove another user's contribution.
- [ ] **Denied cross-building access:** Residents of another building, unauthenticated callers and contractors cannot read restricted shared information or confirm impact through direct API/list/detail operations.
- [ ] **Human control:** Changes to the impact count do not automatically alter category/urgency or approve an intervention. An administrator still decides, and creating a separate report remains possible.
- [ ] **Optional participation:** Impact confirmation and notification subscription are distinct choices; users can decline/withdraw optional participation or disable their optional subscription without losing authorised status access. US-10 respects those preferences.
- [ ] **Persistence and feedback:** After reload/restart, the user's own contribution/subscription state and permitted total remain consistent. Keyboard controls and text feedback explain confirmation, withdrawal and errors without relying on colour alone.

## Verification and risks

Use two residents in building A, one in B, an administrator and contractor. Verify unpublished/published projections via API and UI, role/building denial, duplicate/concurrent confirmations, own withdrawal, unchanged urgency, preference separation and persistence. Inspect returned JSON, history and logs for identities/private fields. Demonstrate optional opt-out without blocking report creation or status queries; notification transport is verified in US-10.

Principal risks: Indirect identification through summaries, inflated impact counts, manipulative mandatory participation and accidentally coupling subscriptions or counts to operational urgency.

This is a story draft: these are planned implementation checks, not executed tests. PLAN-01 validates document content, traceability, consistency and links only.

## Ready / Done

Technical refinement: R01 — component placement; R02 — summary/impact persistence and API; R03 — field-level visibility and membership; R05 — preferences/events; R06 — environment/evidence.

Close the applicable rows of the [EP-01 refinement register](../ep01-technical-refinement.md) using EN-01 decision/contract evidence; record any justified non-applicability. Do not invent concrete endpoints, queue names, database schemas or retry thresholds before those decisions.

- Implementation owner / independent reviewer / estimate / capacity / sprint:
- Refinement closure references and remaining limitations:
- [ ] DoR reviewed by the team; date/author:
- [ ] DoD verified with links to PR, tests and demonstration:

See [definition-of-ready.md](../../governance/definition-of-ready.md) and [definition-of-done.md](../../governance/definition-of-done.md). Do not mark Ready without estimates/capacity, agreed owner/reviewer and resolved dependencies. Record actual implementation/test/demo evidence before checking Done.
