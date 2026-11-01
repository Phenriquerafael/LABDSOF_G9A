# [US-08] Confirm calendar booking and handle failures

## Planning

- Epic: [EP-03 — Intervention and closure](../epics/EP-03-intervention-and-closure.md).
- Priority: Must.
- Estimate: 8 story points — calendar simulator/adapter, reconciliation, manual confirmation/cancellation and failure/recovery tests.
- Sprint: S2, with recovery checks refined in S3.
- Dependencies: [US-07](US-07-approve-request-and-obtain-response.md) for agreed terms and contractor acceptance. Coordinate status/history and notification events with US-02/10 in the [product backlog](../../05-product-backlog.md#4-stories-and-criteria).

## Story

As an **administrator**, I want to **know whether an intervention booking was confirmed**, so that **I do not communicate a date that has not been secured**.

## Scope

Integrate a realistic calendar simulator through an adapter. Handle booking creation, confirmation, uncertain outcomes, reconciliation and justified manual confirmation.

A real provider belongs to [US-13](US-13-integrate-a-real-calendar.md). This story does not cover provider/account setup or a separate rescheduling feature.

## Acceptance criteria

- [ ] Request a booking only after administrator approval and contractor acceptance of the same proposal version. Save the requested window and a stable booking/request identifier before calling the simulator.
- [ ] Confirm only a valid response for that request, contractor and agreed window, with an external reference. Save the result and show whether confirmation came from the calendar or a manual action.
- [ ] For conflicts, unavailability, delays, invalid/incomplete responses or exhausted retries, show the reason and the appropriate pending, uncertain, rejected or failed booking status. Never display an external booking as confirmed without evidence.
- [ ] A timeout may happen after the booking was created. Query by the stable request identifier before sending again; if a booking exists, reuse it. If the result cannot be checked, keep the outcome uncertain.
- [ ] Limit retries and make final failures visible to the administrator. Repeated events, worker restarts and retries must reuse the same booking key and create at most one booking for the request.
- [ ] Let only an authorised administrator manually confirm a pending booking with its window, source and reason. Label it as manual, stop automatic creation attempts and reconcile any outstanding request. If an external booking is later found, show the discrepancy for review without presenting two confirmed bookings.
- [ ] Handle cancellation when a booking exists or may exist. Keep cancellation pending until the external outcome is checked. Reject stale or incompatible confirmation/cancellation actions; late responses must not revive a cancelled intervention.
- [ ] Detect when a previously confirmed external booking is missing during reconciliation and show the discrepancy. Do not silently recreate it. In the current design, moving a confirmed booking requires cancellation and a new intervention.
- [ ] Check backend permissions and send only the necessary booking context. Persist booking history, correlation identifiers, attempts and outcomes without private report text or credentials. Publish status events for US-02/10; failed notification delivery must not change the booking outcome.

## Verification and risks

Use a controllable simulator for success, slot conflict, unavailability, delay, invalid replies, timeout after creation and a missing confirmed booking. Test repeated calls, restart recovery, cancellation, manual confirmation and a late automatic response.

The main risks are duplicate bookings, false confirmations and an unresolved external booking after cancellation. The simulator must exercise these failures; an always-successful stub is insufficient.

References: RF-08, P6, PS-07, J2–J3 and NFR-01/02/04/06/09/11. Assignment: 6.5–6.8.

## Ready / Done

Before starting, agree the adapter and simulator contract, authentication, data ownership, states, time-zone handling, timeout/retry limits, idempotency, reconciliation triggers and test scenarios. Confirm DEC-06/10 and EN-01's [calendar contract](../../07-technical-design.md#45-calendarsimulator-contract-outline), including cancellation and manual-action races.

- [ ] Ready: estimate recorded, blocking decisions resolved and [DoR](../../governance/definition-of-ready.md) reviewed by the team.
- [ ] Done: acceptance criteria met, changes reviewed, PR and failure/recovery tests.
