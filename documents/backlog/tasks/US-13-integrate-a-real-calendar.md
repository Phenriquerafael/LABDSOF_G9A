# [US-13] Integrate a real calendar

## Planning

- Epic: [EP-03 — Intervention and closure](../epics/EP-03-intervention-and-closure.md).
- Priority: Could; select only if useful provider access and sprint capacity are available.
- Estimate: 8 story points — one provider adapter, credentials/permissions, contract mapping and integration/failure tests.
- Sprint: S3, if selected.
- Dependencies: [US-08](US-08-confirm-booking-and-handle-failures.md), DEC-06 provider/access decision and an authorised test calendar.

## Story

As an **administrator**, I want to **use an operational calendar through the existing adapter**, so that **confirmed interventions can be recorded in that calendar**.

## Scope

Add one real provider behind US-08's calendar contract and verify its behaviour against the simulator. Use a dedicated test account/calendar and document configuration and recovery.

This story does not cover account provisioning, multiple providers, two-way editing or a new rescheduling workflow. The simulator remains the initial and reproducible integration.

## Acceptance criteria

- [ ] Record why the real integration is selected, the provider and the authorised test calendar. Map its create, query and cancellation operations to US-08's contract and document any limitations before enabling it.
- [ ] Keep credentials outside Git and logs. Document the minimum permissions, secure configuration, renewal/revocation and removal of test access.
- [ ] Create a booking only for an approved and accepted intervention. Save and validate the provider reference and window, and send only the necessary context without private report text or resident identifiers.
- [ ] Preserve US-08's pending, manual, uncertain and failure behaviour for expired/revoked access, rate limits, unavailable service, timeouts, conflicts and invalid replies. Manual confirmation must never appear as provider synchronisation.
- [ ] Reconcile uncertain creation/cancellation outcomes before sending again. Use a stable external correlation/idempotency mechanism; if the provider cannot safely establish the outcome, keep it uncertain for review rather than risking a duplicate.
- [ ] Test repeated requests, a timeout after creation, late confirmation, manual action and cancellation. Reuse US-08's contract scenarios and provide provider-specific evidence without duplicating the core workflow implementation.
- [ ] Check backend permissions and configuration access. A user cannot choose another building's calendar or use the adapter to read unrelated events.
- [ ] Keep the simulator available for repeatable tests. Document how to disable the provider safely, retaining existing booking references and reconciliation needs; switching configuration must not recreate bookings. If access or capacity is insufficient, record deferral without claiming real synchronisation.

## Verification and risks

Run the shared contract checks with the simulator and an authorised provider test calendar. Record which failures were exercised against the provider and which required controlled simulation. Remove test bookings and revoke temporary access after verification.

The main risks are credential exposure, limited provider permissions and duplicate or orphaned events. Document provider-specific gaps instead of treating simulator results as proof of live behaviour.

References: RF-08, P6, J2–J3 and NFR-01/02/04/06/09/11. Assignment: 6.5–6.8.

## Ready / Done

Before starting, select the extension explicitly and confirm DEC-06, provider permissions/access, contract mapping, data handling, rate limits, timeout/retry settings, reconciliation and test cleanup. Agree how to disable the adapter without losing track of existing bookings.

- [ ] Ready: estimate recorded, blocking decisions resolved and [DoR](../../governance/definition-of-ready.md) reviewed by the team.
- [ ] Done: acceptance criteria met, changes reviewed, PR and contract/provider checks.
