# [US-09] Complete, close and reopen

## Planning

- Epic: [EP-03 — Intervention and closure](../epics/EP-03-intervention-and-closure.md).
- Priority: Must.
- Sprint: S2, refined in S3.
- Dependencies: [US-07](US-07-approve-request-and-obtain-response.md) and [US-08](US-08-confirm-booking-and-handle-failures.md) for the intervention cycle; US-02 in the [product backlog](../../05-product-backlog.md#4-stories-and-criteria) for authorised issue transitions/history.

## Story

As an **administrator**, I want to **review completed work and close or reopen the issue**, so that **the recorded outcome matches what happened**.

## Scope

Let the assigned contractor report completion, let the administrator validate it or request rework, and support justified manual closure and reopening. Preserve the intervention and issue history.

Cost recording belongs to [US-11](US-11-record-a-basic-cost.md). This story does not cover payments, invoices or automatic closure.

## Acceptance criteria

- [ ] Let the assigned contractor report completed work for a booked or in-progress intervention, with a work summary and completion time. An administrator may record completion on their behalf with a reason. Missing optional cost must not prevent submission.
- [ ] Save the completion report and move the issue to awaiting validation through the agreed event contract. Reporting completion must not close the issue or imply administrator approval.
- [ ] Let only the building administrator validate and close an issue awaiting validation, or return the work for execution with a reason. Rework keeps the earlier completion report in history.
- [ ] Let the administrator close an open issue manually with a justification. If an intervention or booking is still active or uncertain, start its cancellation through the agreed contract and show any pending cancellation.
- [ ] Let the administrator reopen a resolved issue with a reason and preserved history. Follow the current design: return it to triage, retain earlier closed interventions and require a new intervention for further work. Reject reopening a cancelled issue.
- [ ] Reject completion from an invalid state, missing required explanations and closure before the completion report reaches the issue. Return a clear error and leave existing records unchanged.
- [ ] Enforce permissions in the backend. Contractors cannot close/reopen issues or submit work for another contractor; residents and users from another building cannot perform administrator actions. Residents see only authorised public status/history.
- [ ] Repeated completion, closure, reopening and events must have no duplicate effects. Check versions on concurrent updates; late events from an earlier intervention must not reopen a closed issue or overwrite the current intervention.
- [ ] Keep actors, reasons, timestamps, versions and event history after restart. Provide authorised state changes to US-02 and events to US-10; notification failures do not undo closure. Unknown cost never blocks completion, validation, closure or reopening.

## Verification and risks

Demonstrate booking, completion, validation, closure and reopening, plus rework and manual closure while booking is pending. Test stale updates, repeated events, invalid transitions and contractor/other-building access.

The main risks are treating a completion report as closure, losing the audit trail and changing a resolved issue through a late event. Check Issue/Dispatch recovery without direct writes to the other service's data.

References: RF-09, P1, J2–J3 and NFR-01/02/04/06/09/11. Assignment: 6.6–6.8.

## Ready / Done

Before starting, confirm DEC-10's completion, rework, manual closure and reopening rules. Agree required fields, service/data ownership, version checks, cancellation and state/event contracts with EN-01 and US-02/10 using the [technical design](../../07-technical-design.md).

- [ ] Ready: owner, reviewer, estimate and sprint capacity agreed; [DoR](../../governance/definition-of-ready.md) reviewed by the team. Date/author:
- [ ] Done: acceptance criteria met, changes reviewed, and PR, tests and demonstration linked according to the [DoD](../../governance/definition-of-done.md).
