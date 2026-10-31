# [EP-01] Residents report and track issues with appropriate visibility

- Publication: Draft — not published by this change; GitHub issue URL: pending. Prepared on 2026-10-15.
- Workflow: Backlog; type: epic; suggested labels: `type:epic`, `area:product`.
- Allocation: see the [backlog README](../README.md); confirm coordinator and reviewer during planning.
- Horizon: S1 discovery/design inputs; implementation in S2, refinement and evaluation in S3. No Sprint 1 implementation commitment.
- Source: [Assignment](../../../LABDSOF-26-27-Assignment.md) §5.5, §6.1, §6.3, §6.4, §6.6–§6.8; [vision](../../04-product-vision.md) J1–J2 and hypotheses P1/P5.
- Priority: Must outcome for the academic release, proposed; validate at prioritisation. Do not add epic estimates to child estimates.

## Problem and outcome

Residents need to know that a fault was received and how it is progressing. Administrators need a persistent queue, manual triage and an auditable history. Provide a usable reporting and tracking journey with building-level access control, understandable states and updates that respect private information.

The proposed benefit is fewer repeated contacts and less coordination effort. Evaluate it through the agreed product metrics; implementation alone does not prove that benefit.

## Boundary

Included:

- Text reports with an authorised building/area, persistent identifier and immediate receipt independent of AI.
- Administrator manual triage and controlled state changes with actor, reason, timestamp and version checks.
- Resident access to their own reports and authorised status/history; sanitised shared summaries published explicitly by administrators.
- Optional impact confirmation on shared issues, one contribution per user/issue, withdrawal and subscription controls.
- One proposed in-app notification channel, with authorised recipients/content, idempotent delivery and observable failures.

Excluded:

- AI classification and duplicate suggestions, which belong to [EP-02](EP-02-assisted-triage.md).
- Contractor selection, approvals, booking and completion/closure actions, which belong to [EP-03](EP-03-intervention-and-closure.md). This epic displays their authorised status/history and delivers relevant notifications.
- Photos, native apps, extra notification channels, payments and public access to private text or costs.

Reporting, viewing and manual triage remain usable when AI is unavailable. Notification failure must not prevent status queries or roll back the issue state.

## Child stories

These are existing [product backlog stories](../../06-product-backlog.md#4-stories-and-criteria), expanded into individual drafts by PLAN-01 without creating additional copies of implementation work. The product backlog retains their scope/priority overview; the files below contain the detailed scenarios. No remote story issue URLs are recorded here.

- [ ] [US-01 — Record and view a report](../tasks/US-01-record-and-view-report.md) · Must · S2 · RF-01.
- [ ] [US-02 — Triage manually and track states](../tasks/US-02-triage-manually-and-track-states.md) · Must · S2 · RF-02.
- [ ] [US-04 — Publish a shared issue and confirm impact](../tasks/US-04-publish-shared-issue-and-confirm-impact.md) · Must · S2 · RF-04 / §5.5.
- [ ] [US-10 — Notify changes](../tasks/US-10-notify-changes.md) · Must · S2 · RF-10.

Preparation task: [PLAN-01 — Prepare Sprint 2/3 user stories for reporting and tracking](../tasks/PLAN-01-prepare-reporting-and-tracking-stories.md), owned by Sandro Dias. PLAN-01 and the implementation stories are direct children of EP-01; the stories are not children of PLAN-01. Drafting completion does not complete the stories or this epic.

Before implementation readiness, close the applicable entries in the [technical-refinement register](../ep01-technical-refinement.md) using EN-01 decisions/contracts. Initial delivery remains S2; S3 refines/evaluates the same stories without duplicating them.

Once published, attach each story as a sub-issue of this epic and link its actual issue URL. Record any implementation subtasks beneath the relevant story. Count selected delivery work once, excluding parent roll-ups.

## Completion criteria

- [ ] US-01/02/04/10 meet their acceptance criteria and applicable [DoD](../../governance/definition-of-done.md), with reviewed PR and verification evidence.
- [ ] Demonstrate a resident submitting a report, querying it after restart and viewing permitted updates while an administrator reviews it and records changes.
- [ ] Demonstrate direct API denial of unauthorised/cross-building access, invalid transitions and stale updates; UI restrictions alone are insufficient.
- [ ] Shared summaries and impact confirmation preserve private text and participant identities, allow withdrawal and do not automatically determine urgency.
- [ ] Repeated submissions/notification events do not duplicate effects. Show notification failure with status queries still available and AI unavailability with manual triage available.
- [ ] Confirm the notification path for relevant intervention events with EP-03, including authorised recipient selection and content.
- [ ] Record applicable quality checks, environment, known limitations and follow-up work. Documentation or design completion does not close this epic.

## Dependencies and risks

- EP-00 research and scope decisions inform requirements; EN-01/02 provide design and implementation foundations, and EN-03 accompanies delivery. EN-02 is excluded from Sprint 1 under DEC-11.
- Build US-01 before US-02/04. US-10 depends on US-02/04 and EP-03's US-07/08/09 response, booking and completion events; this does not block starting the reporting slice while intervention work is unfinished.
- Resolve DEC-06 (notification channel), DEC-07 (visibility/data) and DEC-10 (state rules) to the level needed by each story. Use the [decision register](../../planning/decisions-and-feedback.md).
- Apply [NFR-01/02/04/05/06/07/09](../../requirements.md) and the [access matrix](../../09-security-privacy.md#2-proposed-access-matrix); reporting must not require AI availability.
- Review risks of private-data leakage through lists/history/notifications, duplicate delivery and misleading status projections. Keep Issue-owned state and Dispatch-originated updates consistent with the [technical design](../../08-technical-design.md).

## Publication and review record

- Priority discussion / participants / date: pending.
- GitHub child issue links: pending; replace the local story references after publication.
- Completion evidence / reviewer / date: pending. Checkboxes remain unchecked until verified.
