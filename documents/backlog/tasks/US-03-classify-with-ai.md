# [US-03] Suggest category and urgency with AI

## Planning

- Epic: [EP-02 — Assisted triage and reviewed links](../epics/EP-02-assisted-triage.md).
- Priority: Must.
- Sprint: implement in S2 and evaluate/refine in S3.
- Dependencies: US-01/02 in the [product backlog](../../05-product-backlog.md#4-stories-and-criteria) for reporting and manual triage, and [US-14](US-14-continue-triage-without-ai.md) for rules and fallback.

## Story

As an **administrator**, I want to **receive a category and urgency suggestion for a reported issue**, so that **I can review it and decide how to proceed**.

## Scope

Process saved reports asynchronously, validate the AI response and show the suggestion with a short explanation. The administrator confirms or corrects it through US-02.

Rules and fallback belong to US-14. The final evaluation belongs to [US-15](US-15-evaluate-ai-against-baseline.md).

This story does not cover provider/model selection, duplicate detection, automatic diagnosis, contractor selection, expense approval or booking.

## Acceptance criteria

- [ ] Process a saved report in the background without delaying its receipt. Send only the text and context needed for triage.
- [ ] Check the response against the agreed fields and allowed category/urgency values. Reject missing, invalid or oversized output and use US-14. A confidence value supplied by the model must not be shown as a reliable probability.
- [ ] Mark the suggestion as unconfirmed. Save the explanation, provider/model, prompt/schema version, original issue version and processing status.
- [ ] Let the administrator confirm or correct the suggestion using US-02's permissions, history and version checks. AI output cannot execute code/tools, approve expenses, send intervention requests or confirm bookings.
- [ ] Keep critical alerts from US-14 visible even if AI suggests a lower urgency or disagrees. The administrator must review them.
- [ ] Repeated jobs/events must not create duplicate suggestions or effects. Late results must not overwrite a newer human decision; retain them in history only as allowed by the agreed contract.
- [ ] If AI is disabled, unavailable, times out, returns invalid output or reaches the agreed retry/budget limit, keep fallback available and show the processing failure. Retries must have a limit.
- [ ] Reject unauthorised access or result submissions, including forged building/job identifiers. Treat instructions inside a report as data, not as permission to access other buildings or perform actions.
- [ ] Record job/correlation IDs, response times, usage, retries, failures and cost for troubleshooting and evaluation. Do not include private text or credentials in logs.

## Verification and risks

Test valid and invalid responses, unavailable AI, timeouts and injected instructions. Check duplicate jobs, denied access, late results and the suggestion-to-human-correction flow. Use synthetic cases to compare an initial result with the rules baseline; US-15 covers the final evaluation.

The main risks are incorrect suggestions, private-data leaks, overwritten decisions, duplicate processing and excessive calls or cost.

References: RF-03, P3/P7, J2 and NFR-01/02/03/04/06/10. Assignment: 5.6 and 6.3.

## Ready / Done

Before starting, agree the example inputs/expected outputs, provider/model, prompt version, allowed labels, response format, timeout, retry limits, budget and access.

- [ ] Ready: owner, reviewer, estimate and sprint capacity agreed; [DoR](../../governance/definition-of-ready.md) reviewed by the team. Date/author:
- [ ] Done: acceptance criteria met, changes reviewed, and PR, tests and demonstration linked according to the [DoD](../../governance/definition-of-done.md).
