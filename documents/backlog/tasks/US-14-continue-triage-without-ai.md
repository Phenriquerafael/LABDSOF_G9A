# [US-14] Continue triage without AI

## Planning

- Epic: [EP-02 — Assisted triage and reviewed links](../epics/EP-02-assisted-triage.md).
- Priority: Must.
- Sprint: implement in S2 and refine in S3.
- Dependencies: US-01/02 in the [product backlog](../../05-product-backlog.md#4-stories-and-criteria) and the agreed rules. No AI provider, credentials or successful US-03 call are required.

## Story

As an **administrator**, I want to **continue triage with rules and manual review when AI is unavailable**, so that **reported issues can still be handled**.

## Scope

Provide versioned rules, independent critical alerts and a clear fallback status. Use US-02 for manual decisions and integrate the AI path when US-03 is available.

This story does not cover model calls/training, a second manual-triage implementation, notifications or the final evaluation in [US-15](US-15-evaluate-ai-against-baseline.md). The rules do not guarantee that every emergency will be detected.

## Acceptance criteria

- [ ] With AI disabled or no provider configured, users can submit and view reports, and administrators can triage them without a model call.
- [ ] Save the rule version and reason for each rules-based suggestion. Leave unclear or unmatched cases for manual review instead of assuming low urgency.
- [ ] Show critical alerts independently of AI. An AI response or retry must not remove or lower an alert; it remains subject to human review.
- [ ] Use fallback when AI times out, is unavailable, returns invalid data or reaches the agreed retry/budget limit. Show that AI is unavailable and keep available rules and manual triage usable. Retries must have a limit.
- [ ] If the rules or worker fail, saved reports must remain viewable and manually triageable with a pending/manual status. Do not show a rules result that was never computed or delay the original receipt until processing recovers.
- [ ] When AI recovers or a late result arrives, it must not overwrite a newer human decision or remove a critical alert. Keep its source separate if the result is retained.
- [ ] Repeated events, restarted jobs or repeated fallback attempts must not duplicate rule results, alerts or business actions. Reuse the existing job/idempotency mechanism.
- [ ] Only authorised administrators can change triage through the API. Reject other roles and users from other buildings. Clearly distinguish rules, unavailable AI and human decisions in the interface, using text as well as colour.
- [ ] Demonstrate disabled AI, timeout, provider error, invalid output, rules failure and worker unavailability. Reporting, viewing and manual triage must still work, and processing failures must be visible in logs without private data.

## Verification and risks

Test the rules with ambiguous text, negation, spelling errors and critical/non-critical cases. Run reporting and manual triage without provider credentials. Check permissions, repeated jobs, failures and late recovery using synthetic data. Keep these initial cases separate from US-15's final test set.

The main risks are misleading rule results, duplicate alerts, repeated retries and recovered AI overwriting human decisions.

References: RF-02/03, P3/P7, J1–J2 and NFR-01/02/03/04/06. Assignment: 5.6.2 and 6.8.

## Ready / Done

Before starting, agree the rule inputs/expected outputs, versions, critical alerts, manual/fallback states, permissions and retry limits.

- [ ] Ready: owner, reviewer, estimate and sprint capacity agreed; [DoR](../../governance/definition-of-ready.md) reviewed by the team. Date/author:
- [ ] Done: acceptance criteria met, changes reviewed, and PR, tests and demonstration linked according to the [DoD](../../governance/definition-of-done.md).
