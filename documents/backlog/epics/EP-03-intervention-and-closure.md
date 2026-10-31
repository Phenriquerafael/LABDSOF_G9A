# [EP-03] Intervention from request to closure

- Publication: Draft — not published by this change; GitHub issue URL: pending. Prepared on 2026-10-15.
- Workflow: Backlog; type: epic; suggested labels: `type:epic`, `area:backend`.
- Allocation: see the [backlog README](../README.md); confirm coordinator and reviewer during planning.
- Horizon: S1 discovery/design inputs; first operational cycle in S2, refinement and conditional extensions in S3. No Sprint 1 implementation commitment.
- Source: [Assignment](../../../LABDSOF-26-27-Assignment.md) §6.2–§6.8; [vision](../../04-product-vision.md) J2–J3 and hypothesis P6.
- Priority: Must core outcome for the academic release, proposed; Should/Could children remain conditional. Validate at prioritisation and do not add epic estimates to child estimates.

## Problem and outcome

Administrators need to turn a triaged issue into an authorised, accepted and scheduled intervention, then verify completion. Contractors need clear requests, appropriate context and a way to respond. Deliver the traceable cycle from contractor selection to closure without confusing request approval, contractor acceptance and booking confirmation.

The intended benefit is reduced active coordination effort. Track dispatch, acceptance and resolution separately; a simulated calendar demonstration does not establish real-world impact or contractor adoption.

## Boundary

Included in the core:

- A small synthetic contractor catalogue with eligibility filtering, deterministic ordering and administrator selection.
- Versioned proposals, administrator approval and assigned-contractor acceptance, rejection or counterproposal. Changed terms require new approval.
- A realistic external calendar simulator, with actual confirmation distinguished from pending or explicitly recorded manual confirmation.
- Idempotency and reconciliation for retries, uncertain external outcomes and manual action; visible failure/degraded states.
- Contractor completion reporting, administrator validation, closure/reopening with reasons and preserved history.

Conditional extensions: basic cost recording (US-11), richer ranking using justified data (US-12), and a real calendar provider (US-13). Unknown cost does not prevent closure; the simulator satisfies the initial integration approach.

Excluded: marketplace, payments, subscriptions, automatic expense approval, cost analytics/narrative summaries, photos and unrestricted access to resident reports. Notification delivery remains US-10 in [EP-01](EP-01-reporting-and-tracking.md); this epic provides the relevant intervention events and permitted context. AI-assisted triage belongs to [EP-02](EP-02-assisted-triage.md).

## Child stories

Detailed drafts are linked below; the [product backlog](../../05-product-backlog.md#4-stories-and-criteria) remains the scope and priority overview. PLAN-03 prepares these drafts in Sprint 1; it does not implement the stories. Each story is a direct child of EP-03, alongside PLAN-03.

Core cycle:

- [ ] [US-06 — Select a contractor](../tasks/US-06-select-a-contractor.md) · Must · S2 · RF-06.
- [ ] [US-07 — Approve a request and obtain a response](../tasks/US-07-approve-request-and-obtain-response.md) · Must · S2 · RF-07.
- [ ] [US-08 — Confirm calendar booking and handle failures](../tasks/US-08-confirm-booking-and-handle-failures.md) · Must · S2 · RF-08.
- [ ] [US-09 — Complete, close and reopen](../tasks/US-09-complete-close-and-reopen.md) · Must · S2, refined in S3 · RF-09.

Conditional scope, subject to evidence and capacity:

- [ ] [US-11 — Record a basic cost](../tasks/US-11-record-a-basic-cost.md) · Should · S3 if selected · RF-11.
- [ ] [US-12 — Refine ranking](../tasks/US-12-refine-ranking.md) · Should · S3 · RF-06 / P6.
- [ ] [US-13 — Integrate a real calendar](../tasks/US-13-integrate-a-real-calendar.md) · Could · S3 if selected · RF-08.

Once published, attach each story as a sub-issue of this epic and link its actual issue URL. Put implementation subtasks beneath their story. Optional stories are not automatic release commitments: record selection or deferral explicitly; never mark deferred work Done. Keep unfinished selected children visible, and reparent deferred extensions to future scope if needed before closing the released epic.

## Sprint 2 coverage and estimates

US-06 (5 SP), US-07 (8 SP), US-08 (8 SP) and US-09 (8 SP) form the required S2 intervention cycle: **29 SP**. Use the small synthetic catalogue, administrator control and realistic calendar simulator, including uncertain outcomes and recovery. Completion/closure stays in S2; later refinement does not defer the core journey.

US-11 (3 SP), US-12 (5 SP) and US-13 (8 SP) add **16 SP of conditional extensions**, planned for S3 if selected. Missing costs, advanced ranking or a real calendar must not block the core cycle. The full 45-SP total is not a Sprint 2 commitment.

Each estimate includes story-specific verification and assumes shared EN-02/03 foundations. Resolve the decisions in each story and review the DoR before Ready; assign owners before starting and reviewers when opening PRs. Revisit estimates if contracts, architecture or provider assumptions change.

## Completion criteria

- [ ] Core stories US-06–09 meet their acceptance criteria and applicable [DoD](../../governance/definition-of-done.md), with reviewed PR and verification evidence.
- [ ] Demonstrate an authorised administrator selecting a contractor and approving a request, the assigned contractor responding, and a booking reaching a correctly labelled confirmed or pending/manual state.
- [ ] Demonstrate contractor-reported completion followed by administrator closure and justified reopening, retaining the history. Missing optional cost does not block closure.
- [ ] Verify backend permissions, version checks and the distinction between approval, acceptance and scheduling. A contractor cannot approve expenses or close an issue as administrator.
- [ ] Demonstrate unavailable/delayed/invalid calendar responses and uncertain outcomes; retries and manual confirmation must not create duplicate bookings or false confirmations.
- [ ] Demonstrate a rejection or counterproposal requiring review and, for changed terms, new approval; absence of an eligible contractor leaves a visible manual-coordination path.
- [ ] Link authorised history/status projections and notification-event integration evidence with EP-01, without exposing unnecessary private report details to contractors.
- [ ] Record the disposition of US-11/12/13 and satisfy any selected extension's criteria. Provide quality evidence and known limitations; design completion alone does not close the epic.

## Dependencies and risks

- US-06 depends on EP-01's US-02. Implement the core in order US-06 → US-07 → US-08 → US-09, with US-09 also depending on US-02/07. US-11 follows US-09, US-12 follows US-06 and US-13 follows US-08.
- Coordinate US-07/08/09 response, booking and completion events with EP-01's US-02/10; do not turn this story-level integration into a requirement that either whole epic must finish first.
- Decisions needed before development are listed in each story's Ready / Done section. Confirm service/data ownership, API/event contracts, calendar adapter/authentication, idempotency, version checks, reconciliation and the test environment with EN-01. The current DEC-10 state rules are proposals; drafting does not approve them.
- EP-00 research must investigate contractor participation and approval/scheduling rules. Resolve DEC-06/07/10, and use EN-01 design/ADRs plus EN-02/03 foundations and delivery checks. See the [decision register](../../planning/decisions-and-feedback.md).
- Apply [NFR-01/02/04/06/09/11](../../requirements.md), the [security/access assessment](../../09-security-privacy.md) and [technical ownership/state rules](../../07-technical-design.md). Dispatch controls interventions/bookings; issue closure is performed through the Issue-owned interface, not cross-writing its tables.
- Principal risks: contractor non-adoption, scope growth into a marketplace, invented price/availability data, double bookings, stale approvals and inconsistent cancellation/status projections. A calendar slot alone does not prove contractor availability.

## Publication and review record

- Priority discussion / participants / date: pending.
- Selected/deferred optional stories and rationale: pending.
- GitHub child issue links: pending; replace the local story references after publication.
- Completion evidence / reviewer / date: pending. Checkboxes remain unchecked until verified.
