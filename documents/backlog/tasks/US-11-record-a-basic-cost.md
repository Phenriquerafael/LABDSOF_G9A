# [US-11] Record a basic cost

## Planning

- Epic: [EP-03 — Intervention and closure](../epics/EP-03-intervention-and-closure.md).
- Priority: Should; include only if evidence and capacity justify it.
- Sprint: S3 candidate; may start in S2 if selected without displacing the core cycle.
- Dependencies: [US-09](US-09-complete-close-and-reopen.md) for the intervention history and closure flow.

## Story

As an **administrator**, I want to **record a known intervention cost and its source**, so that **the work history includes this information**.

## Scope

Record an optional basic cost, allow the assigned contractor to propose it, and let the administrator confirm or correct it with a history.

This story does not cover payments, invoices, financial approval, totals, charts or AI summaries. Selection is conditional; the core cycle works without it.

## Acceptance criteria

- [ ] Allow the cost to remain unknown. Distinguish an empty value from a confirmed zero; missing cost must not block completion, validation, closure or reopening.
- [ ] For a recorded cost, require a non-negative amount, currency and source. Reject invalid numbers, unsupported currency or missing required fields without saving a partial record.
- [ ] Let the assigned contractor propose the cost of their own work. Mark it as proposed until the building administrator confirms or corrects it; contractor input must not approve an expense.
- [ ] Record who proposed, confirmed or corrected the value, when and why. Preserve earlier values and distinguish confirmed from unconfirmed information.
- [ ] Enforce permissions in the backend. Contractors cannot change another contractor's cost or confirm it; residents have no cost access by default, and other buildings cannot read or change it.
- [ ] Repeating a save must not duplicate the record or its effects. Reject concurrent changes based on an old version and preserve the latest accepted value.
- [ ] Keep the cost and audit history after restart without changing the issue's lifecycle state. Record selection or deferral during planning; deferral must not block US-09 or be marked as completed implementation.

## Verification and risks

Use synthetic interventions to test empty, zero, positive, negative and invalid costs, contractor proposals, administrator corrections, denied access and concurrent saves. Demonstrate closure with no cost.

The main risks are exposing commercial information and presenting an estimate or unconfirmed proposal as a final amount.

References: RF-11, P1, J2–J3 and NFR-01/02/09. Assignment: 6.6–6.8.

## Ready / Done

Before starting, select this extension explicitly and agree supported currencies, amount precision/limits, source fields, visibility, correction rules and data/API ownership with EN-01 and DEC-07/10.

- [ ] Ready: owner, reviewer, estimate and sprint capacity agreed; [DoR](../../governance/definition-of-ready.md) reviewed by the team. Date/author:
- [ ] Done: acceptance criteria met, changes reviewed, and PR, tests and demonstration linked according to the [DoD](../../governance/definition-of-done.md).
