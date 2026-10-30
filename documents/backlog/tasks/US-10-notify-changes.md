# [US-10] Notify changes

## Planning

- Epic: [EP-01 — Reporting and tracking](../epics/EP-01-reporting-and-tracking.md).
- Priority: Must.
- Sprint: implement in S2 and refine/evaluate in S3.
- Dependencies: [US-02](US-02-triage-manually-and-track-states.md) and [US-04](US-04-publish-shared-issue-and-confirm-impact.md), plus US-07 events from [EP-03](../epics/EP-03-intervention-and-closure.md). Start with agreed fixtures; final integration needs the actual producer, without waiting for the whole epic.

## Story

As a **participant**, I want to **receive authorised updates about an issue**, so that **I can follow its progress without repeatedly asking for status**.

## Scope

Deliver state updates through one proposed in-app channel. Select authorised recipients/content, respect optional preferences and handle repeated events and failures.

This story does not cover email/SMS/push, changing issue states, retrying bookings, implementing EP-03 event producers or automatically subscribing impact contributors.

## Acceptance criteria

- [ ] Process a committed eligible state event and show the intended recipient one notification with permitted status/context and a link they are authorised to open.
- [ ] Check building/resource permissions and current publication visibility when choosing recipients and content. Events must not expose private report text, internal notes or costs.
- [ ] Respect optional subscriptions independently of impact confirmation. Users can disable them without losing authorised status access; apply the agreed rules for required and optional updates.
- [ ] Repeated or concurrent processing of the same event for the same recipient must not create duplicate notifications. Keep distinct valid changes separate.
- [ ] Limit retries for temporary failures. Record invalid events and exhausted attempts with event/correlation IDs in logs/metrics, without private payloads, unlimited retries or malformed notifications.
- [ ] A notification failure must not undo a saved issue/intervention change or prevent reporting, manual triage or status queries.
- [ ] Let only the authorised recipient retrieve their notifications or open the protected resource. Changing identifiers or losing access must not expose another user's notifications or old private content.
- [ ] Preserve notifications and delivery/deduplication records after restart. Replaying a processed event must not create another visible notification.
- [ ] Demonstrate an Issue-originated update and the agreed US-07 intervention event path. Use failure fixtures early, then verify the actual EP-03 producer before claiming the integration is complete.

## Verification and risks

Use synthetic recipients with different roles/buildings, preferences and changed membership. Test event-to-notification delivery, authorised reading, concurrent replay, invalid events, retry exhaustion and restart. Show that status queries work while notifications are unavailable and retain sanitised logs/metrics.

The main risks are private-data leaks, stale permissions, duplicate notifications and losing the event after the source state was saved.

References: RF-10, P5, J1–J3 and NFR-01/02/04/06/09 in the [requirements](../../requirements.md).

## Ready / Done

Before starting, agree the channel, worker/transport ownership, event schemas/versions, recipients, required/optional updates, read-time permissions, state/event handoff, retry limits, deduplication and test environment. Confirm DEC-04/06/07 and EN-01 contracts with US-02/04 and US-07's owner.

- [ ] Ready: owner, reviewer, estimate and sprint capacity agreed; [DoR](../../governance/definition-of-ready.md) reviewed by the team. Date/author:
- [ ] Done: acceptance criteria met, changes reviewed, and PR, tests and demonstration linked according to the [DoD](../../governance/definition-of-done.md).
