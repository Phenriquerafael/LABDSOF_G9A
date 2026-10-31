# [US-04] Publish a shared issue and confirm impact

## Planning

- Epic: [EP-01 — Reporting and tracking](../epics/EP-01-reporting-and-tracking.md).
- Priority: Must.
- Estimate: 5 story points — shared summary, impact confirmation, preferences, privacy and concurrent-action tests.
- Sprint: implement in S2 and refine/evaluate in S3.
- Dependencies: [US-01](US-01-record-and-view-report.md) and [US-02](US-02-triage-manually-and-track-states.md). [US-10](US-10-notify-changes.md) uses the events/preferences, but notification delivery is not needed to publish or confirm impact.

## Story

As a **resident**, I want to **view a shared issue and confirm that it affects me**, so that **I can contribute without repeating the report**.

## Scope

Let the administrator publish a reviewed summary for the building. Let residents confirm or withdraw their own impact contribution and manage an optional subscription.

This story does not cover sharing raw reports, AI summaries, duplicate merging, automatic urgency changes, contributor lists, leaderboards or notification delivery.

## Acceptance criteria

- [ ] Let the building administrator review and publish a shared summary. Only then can residents of that building view the summary and authorised status; raw report text remains private.
- [ ] Allow only the authorised administrator to publish or change the summary. Reject invalid content and unauthorised changes without exposing private fields.
- [ ] Return only the reviewed summary and permitted fields in shared listings, details and API responses. Exclude raw report text, contributor identities, internal notes and private costs.
- [ ] Record at most one impact contribution per resident and issue. Repeated or concurrent confirmations must not increase the count twice.
- [ ] Let a resident withdraw their own contribution and update the count. Repeated withdrawal is safe; users cannot remove another person's contribution.
- [ ] Enforce backend permissions. Unauthenticated users, contractors and residents of another building cannot read the restricted shared information or confirm impact through the API.
- [ ] Keep category/urgency and intervention approval under administrator control. A change in the impact count must not change them automatically, and residents can still create a separate report.
- [ ] Keep impact confirmation and notification subscription as separate, optional choices. Declining or withdrawing participation, or disabling a subscription, must not remove authorised status access. US-10 respects these preferences.
- [ ] Preserve the user's contribution/subscription and permitted total after reload or restart. Provide keyboard controls and clear confirmation, withdrawal and error messages without relying on colour alone.

## Verification and risks

Use two residents in one building, a resident from another building, an administrator and a contractor. Test publication, safe API/UI views, denied access, concurrent confirmations, withdrawal, unchanged urgency, separate preferences and persistence. Inspect responses and logs for private fields and identities.

The main risks are identifiable summaries, inflated counts and participation becoming mandatory. Demonstrate opt-out while reporting and authorised status queries remain available.

References: RF-04, P2/P5, J1–J2, assignment 5.5 and NFR-01/02/04/07/09 in the [requirements](../../requirements.md).

## Ready / Done

Before starting, agree summary fields/limits, field visibility, membership checks, contribution/subscription storage, API responses, events/preferences and test cases with EN-01. Confirm DEC-04/07 and data ownership using the [technical design](../../08-technical-design.md) and [access matrix](../../09-security-privacy.md#2-proposed-access-matrix).

- [ ] Ready: estimate recorded, blocking decisions resolved and [DoR](../../governance/definition-of-ready.md) reviewed by the team.
- [ ] Done: acceptance criteria met, changes reviewed, PR and tests.
