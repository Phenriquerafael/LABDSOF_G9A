# [US-07] Approve a request and obtain a response

## Planning

- Epic: [EP-03 — Intervention and closure](../epics/EP-03-intervention-and-closure.md).
- Priority: Must.
- Estimate: 8 story points — versioned proposals, approval and contractor responses, events and permission/concurrency tests.
- Sprint: S2.
- Dependencies: [US-06](US-06-select-a-contractor.md) for the selected contractor and draft request; US-02 in the [product backlog](../../05-product-backlog.md#4-stories-and-criteria) for authorised status/history.

## Story

As an **administrator**, I want to **approve an intervention request and see the contractor's response**, so that **we agree on the work before arranging the booking**.

## Scope

Approve a specific proposal version and let the assigned contractor accept, reject or counterpropose. Keep the work description, time window, terms and approval history.

Booking belongs to [US-08](US-08-confirm-booking-and-handle-failures.md). Notification delivery belongs to US-10 in EP-01. This story does not cover payments, automatic approval or confirmation of a calendar booking.

## Acceptance criteria

- [ ] Let only the building administrator approve the current proposal version. Save its contractor, work description, proposed window and terms, with the approver and timestamp.
- [ ] Send only the approved version to the assigned contractor. Show approval, contractor response and booking status separately; approval must not appear as acceptance or a confirmed booking.
- [ ] Let only the assigned contractor accept, reject or counterpropose on the current approved version. Reject an invalid response or a response to an outdated version without changing the request.
- [ ] When the contractor accepts, record the agreed version and make it available to US-08. When they reject, record the response and show that another contractor or manual coordination is needed; do not book.
- [ ] Changed terms create a new proposal version and invalidate the earlier approval. A contractor's counterproposal needs administrator approval. Under the current design proposal, that approval records agreement by both parties without requiring the contractor to accept their own terms again.
- [ ] Check permissions in the backend and limit the contractor's view to their assigned request and necessary context. If administrator authorisation cannot be checked, do not approve or change the request.
- [ ] Repeated approvals, responses or delivered events must not send duplicate requests or start two bookings. Concurrent approval, changed terms, acceptance and cancellation must use version checks; a losing update cannot overwrite the winning decision.
- [ ] Keep actor, version, response and timestamps in history. Publish the agreed intervention events for US-02 and US-10; delayed notifications must not undo a saved decision. A request with no response stays visibly awaiting a response.

## Verification and risks

Test approval followed by acceptance, rejection and counterproposal, including changed terms and a contractor replying to an old version. Test repeated commands, competing updates, denied access and failure after saving but before event delivery.

The main risks are stale approvals, duplicate requests, unnecessary disclosure and confusing approval with acceptance or booking. Review the state/event examples with the owners of US-02, US-08 and US-10.

References: RF-07, P6, PS-08, J2–J3 and NFR-01/02/04/06/09. Assignment: 6.3–6.4.

## Ready / Done

Before starting, confirm DEC-10's version, counterproposal and cancellation rules. Agree request/response fields, service ownership, permissions, event contracts and retry limits with EN-01 using the [technical design](../../07-technical-design.md) and [contract examples](../../07a-contract-examples.md). Decide whether a response deadline is included; silence must never count as acceptance.

- [ ] Ready: estimate recorded, blocking decisions resolved and [DoR](../../governance/definition-of-ready.md) reviewed by the team.
- [ ] Done: acceptance criteria met, changes reviewed, PR and tests.
