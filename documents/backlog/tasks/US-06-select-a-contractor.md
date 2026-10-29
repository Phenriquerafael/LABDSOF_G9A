# [US-06] Select a contractor

## Planning

- Epic: [EP-03 — Intervention and closure](../epics/EP-03-intervention-and-closure.md).
- Priority: Must.
- Sprint: S2.
- Dependencies: US-02 in the [product backlog](../../05-product-backlog.md#4-stories-and-criteria) for manual triage and authorised issue access.

## Story

As an **administrator**, I want to **select an eligible contractor for a triaged issue**, so that **I can prepare an intervention request**.

## Scope

Use a small synthetic contractor catalogue, filter by specialisation and coverage, and show a simple, explained order. The administrator chooses the contractor and prepares a draft request.

Sending the request belongs to [US-07](US-07-approve-request-and-obtain-response.md). Price/distance ranking belongs to [US-12](US-12-refine-ranking.md). This story does not cover a marketplace, automatic selection or confirmed availability.

## Acceptance criteria

- [ ] Show the catalogue to an administrator of the issue's building. Each contractor has an identifier, specialisation and coverage, with synthetic data identified as such.
- [ ] Filter out contractors who do not meet the issue's agreed eligibility rules. Explain why a candidate is eligible; missing data must not be treated as proof of eligibility.
- [ ] Apply a documented, repeatable order with a clear tie-breaker. Show the criteria used and label unknown information without inventing prices or availability.
- [ ] Let the administrator select or replace a contractor in a draft request. Save the issue, contractor and necessary work description, and check eligibility again when saving.
- [ ] Reject a missing or invalid contractor, an issue that is not ready for intervention, or a second active intervention for the same issue. Leave the existing data unchanged.
- [ ] When no contractor is eligible, explain the result and leave the issue available for manual coordination. Do not create or send a request automatically.
- [ ] Enforce building permissions in the backend. Residents and contractors cannot select a contractor; changing identifiers must not expose another building's reports.
- [ ] Repeating the same save must not create two drafts. Reject outdated or conflicting changes and let the administrator reload the current version. Selection alone sends nothing and confirms neither acceptance nor a booking.

## Verification and risks

Use synthetic catalogue entries and triaged issues to test eligibility, missing data, ties, no candidates, changed selection, repeated saves and concurrent updates. Check backend permissions and persistence after restart.

The main risks are unsuitable recommendations, treating catalogue data as confirmed availability and exposing private report text. Send contractors only the context needed for their assigned request.

References: RF-06, P1/P6, J2 and NFR-01/02/09. Assignment: 6.2–6.3.

## Ready / Done

Before starting, agree the catalogue fields and fixtures, eligibility rules, initial ordering, draft ownership and save/version contract with EN-01. Confirm the relevant DEC-07/10 rules in the [technical design](../../07-technical-design.md).

- [ ] Ready: owner, reviewer, estimate and sprint capacity agreed; [DoR](../../governance/definition-of-ready.md) reviewed by the team. Date/author:
- [ ] Done: acceptance criteria met, changes reviewed, and PR, tests and demonstration linked according to the [DoD](../../governance/definition-of-done.md).
