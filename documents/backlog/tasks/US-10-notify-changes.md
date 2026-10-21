# [US-10] Notify changes

## Identification

- Local ID / epic: US-10 / [EP-01 — Reporting and tracking](../epics/EP-01-reporting-and-tracking.md) (direct child).
- Requirement(s), hypothesis/finding and journey: RF-10; P5; J1–J3; NFR-01/02/04/06/09; [requirements](../../requirements.md), [vision](../../04-product-vision.md), [assignment](../../../LABDSOF-26-27-Assignment.md).
- Proposed MoSCoW priority / reason: Must — keeps authorised participants informed without making delivery a dependency of issue state.
- Official milestone: proposed S2 initial delivery and S3 refinement/evaluation; No Sprint 1 implementation commitment.
- Blocking decisions/dependencies: DEC-04, DEC-06 and DEC-07 in the [decision register](../../planning/decisions-and-feedback.md). Close applicable EN-01 refinements before implementation readiness.

[US-02](US-02-triage-manually-and-track-states.md) and [US-04](US-04-publish-shared-issue-and-confirm-impact.md) for authorised changes/preferences; EP-03's US-07 for intervention events (see the [EP-03 epic](../epics/EP-03-intervention-and-closure.md)). Start with agreed event fixtures/contracts; final integration evidence includes the actual producer. This does not require completion of either whole epic.

The [technical design](../../08-technical-design.md) and [access matrix](../../09-security-privacy.md#2-proposed-access-matrix) are conceptual inputs, not accepted stack/contracts. These criteria describe behaviour without selecting a framework, database, broker or provider.

Draft status: Backlog; technical refinement required before Ready. No GitHub story URL recorded. Sandro Dias under [PLAN-01](PLAN-01-prepare-reporting-and-tracking-stories.md). Implementation allocation: see the [backlog index](../README.md#ep-01-story-drafts-and-planning-allocation).

## Story

As a **participant**, I want to **receive authorised updates about an issue**, so that **I can track progress without repeatedly asking for status**.

## Scope

Included: One proposed in-app notification channel, asynchronous state-event consumption, authorised recipient/content selection, optional preferences, idempotent delivery and observable failure.

Excluded: Extra push/email/SMS channels, changing issue/intervention states, retrying bookings, implementing EP-03 producers, automatic subscriptions tied to impact confirmation and selecting transport technology.

## Acceptance criteria

- [ ] **Authorised update:** Given a committed eligible state event, when processed, then the intended participant can view one notification containing only the permitted issue/status context and a reference they are authorised to open.
- [ ] **Visibility:** Recipient selection and rendered content respect building/resource permissions and current publication visibility; an event is not permission to publish private report text, internal notes or costs.
- [ ] **Preferences:** Optional subscriptions can be disabled independently of impact confirmation; notification processing respects those preferences. Final mandatory/optional event rules are resolved under R05, without treating opt-out as loss of status-query access.
- [ ] **Duplicate delivery:** Repeated or concurrent processing of the same event/recipient does not create multiple visible notifications. Distinct valid changes are not incorrectly collapsed into one event.
- [ ] **Bounded failure:** For temporary processing failure, retry within the configured policy. Exhausted attempts and invalid events are visible in operational logs/metrics with event/correlation identifiers, without private payloads, unlimited retry loops or corrupt notifications.
- [ ] **Independent source state:** Notification failure does not roll back the committed issue/intervention state and does not prevent reporting, manual triage or status queries.
- [ ] **Safe retrieval:** Only an authorised recipient can query their notifications or follow a protected resource link; changing a recipient/resource ID does not expose another user's notifications. A loss of authorisation must not reveal stale private content on retrieval.
- [ ] **Persistence/restart:** Notifications and delivery/deduplication state survive the relevant component restart so replaying an already-processed event does not produce a duplicate visible notification.
- [ ] **Integration evidence:** Demonstrate at least one Issue-originated change and the agreed US-07 intervention event path. Test adverse fixtures before producer integration, then verify against the actual EP-03 producer; do not call stub-only evidence a completed integration.

## Verification and risks

Use synthetic recipients with different roles/buildings, optional opt-in/out and changed membership. Exercise event→delivery→authorised read, repeated/concurrent event replay, invalid events, exhausted retries, restart and unavailable notification processing while status queries work. Inspect sanitised logs, correlation and metrics for failed deliveries. Combine contract tests with an E2E update path and later actual US-07 producer evidence.

Principal risks: Private data in notifications, stale permissions, duplicate delivery, lost state-to-event handoff and circular dependencies between notification delivery and the producer's business transaction.

This is a story draft: these are planned implementation checks, not executed tests. PLAN-01 validates document content, traceability, consistency and links only.

## Ready / Done

Technical refinement: R01 — worker/transport placement; R03 — recipient and read-time authorisation; R04 — source-state/version semantics; R05 — schemas, recipients, preference rules, retry/deduplication; R06 — environment/evidence.

Close the applicable rows of the [EP-01 refinement register](../ep01-technical-refinement.md) using EN-01 decision/contract evidence; record any justified non-applicability. Do not invent concrete endpoints, queue names, database schemas or retry thresholds before those decisions.

- Implementation owner / independent reviewer / estimate / capacity / sprint:
- Refinement closure references and remaining limitations:
- [ ] DoR reviewed by the team; date/author:
- [ ] DoD verified with links to PR, tests and demonstration:

See [definition-of-ready.md](../../governance/definition-of-ready.md) and [definition-of-done.md](../../governance/definition-of-done.md). Do not mark Ready without estimates/capacity, agreed owner/reviewer and resolved dependencies. Record actual implementation/test/demo evidence before checking Done.
