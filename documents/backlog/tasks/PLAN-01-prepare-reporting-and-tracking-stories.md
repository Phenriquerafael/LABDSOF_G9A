# [PLAN-01] Prepare Sprint 2/3 user stories for reporting and tracking

- Publication: Local task record for PLAN-01; no remote issue URL recorded here.
- Workflow: Backlog; type: task;
- Parent / epic: [EP-01 — Reporting and tracking](../epics/EP-01-reporting-and-tracking.md) (direct task).
- Horizon: Sprint 1 backlog preparation for implementation in Sprints 2/3;
- Priority: Must candidate for backlog preparation; confirm during prioritisation.
- Source: [Assignment](../../../LABDSOF-26-27-Assignment.md) §7.1.2 item 5; §5.5; §6.1, §6.3–§6.4, §6.6–§6.8.
- Dependencies / related decision: use the existing epic, [product backlog](../../06-product-backlog.md) and [requirements](../../requirements.md); DEC-04, DEC-06, DEC-07 and DEC-10 in the [decision register](../../planning/decisions-and-feedback.md). Initial drafts can be prepared before architecture selection; technical completion and implementation readiness require the relevant EN-01 design decisions.

## Objective and scope

Prepare individual, traceable user-story drafts for reporting and tracking, translating EP-01 and the existing product backlog into work that can be refined for Sprints 2/3.

Included: US-01 — Record and view a report; US-02 — Triage manually and track states; US-04 — Publish a shared issue and confirm impact; US-10 — Notify changes.

Excluded: application implementation, selecting the stack/architecture, remote issue publication and claiming that the implementation stories are Ready.

This is a documentation task, not a spike. Estimate the drafting/review effort during planning. It may finish with reviewed draft stories and explicit technical-refinement follow-ups; it does not require resolving the architecture itself.

## Acceptance criteria

- [ ] Create an individual Markdown draft for each included story in `documents/backlog/tasks/`, preserving its existing ID, scope and proposed priority.
- [ ] Include role, intended benefit, included/excluded scope, proposed sprint, requirement/NFR references, dependencies, verification approach and observable acceptance criteria in each draft.
- [ ] Cover valid and invalid reporting, building-level permissions, persistence across restart, manual triage, state/history visibility and repeated or concurrent actions where applicable.
- [ ] Cover administrator-published shared summaries, impact confirmation/withdrawal and notification content/recipients without exposing private report text or resident identities.
- [ ] Specify that reporting and manual triage remain available without AI, and status queries remain available when notification delivery fails.
- [ ] Identify story-level dependencies on EP-02/EP-03, including intervention events consumed by US-10, without requiring either whole epic to finish first.
- [ ] Link the drafts from EP-01 and update `documents/backlog/README.md` and `documents/06-product-backlog.md` without creating duplicate work items.
- [ ] Record technical-refinement follow-ups linked to EN-01: API/event contracts, data ownership, identity/authorisation integration, notification mechanism, persistence and test environment. Complete these after stack and architecture selection, before implementation readiness.
- [ ] Link the reviewed PR and document the remaining refinements; do not mark child implementation work completed or Ready merely because its draft exists.

## Deliverables and evidence

- Story drafts in `documents/backlog/tasks/` — preserve existing story IDs and add new IDs only where needed.
- [EP-01 epic](../epics/EP-01-reporting-and-tracking.md) — link the future implementation stories directly to this epic, alongside PLAN-01, rather than making them children of this planning task.
- [Backlog index](../README.md) — update story references and record Sandro Dias as the owner of PLAN-01.
- [Product backlog](../../06-product-backlog.md) — keep scope, priorities and dependencies consistent.
- Reviewed PR and technical-refinement follow-ups — provide actual references in the completion record.

## Verification

Review each draft against EP-01, RF-01/02/04/10 and NFR-01/02/04/05/06/07/09. Another team member checks scope, dependencies, failure cases and links. Verify Markdown/link consistency; implementation tests do not apply to this documentation task.

Use the documentation portions of the [DoR](../../governance/definition-of-ready.md) and [DoD](../../governance/definition-of-done.md). Check for existing story drafts/issues before duplicating IDs or publishing child issues.

## Completion record

- Preparation performed: four individual story drafts created under EP-01, preserving US-01/02/04/10, existing Must priorities and S2 initial delivery/S3 refinement horizons.
- Drafts: [US-01](US-01-record-and-view-report.md), [US-02](US-02-triage-manually-and-track-states.md), [US-04](US-04-publish-shared-issue-and-confirm-impact.md), [US-10](US-10-notify-changes.md).
- Evidence: reciprocal epic/index/product-backlog links and the [technical-refinement register](../ep01-technical-refinement.md). Entries R01–R06 map to existing EN-01 design work; no stack, architecture or provider is selected here.
- Source/requirement impact: existing RF-01/02/04/10 scope expanded into verifiable scenarios; no research finding, product validation or accepted technical decision is claimed.
- Preparation branch: `docs/PLAN-01-reporting-and-tracking-stories`. PR/independent review evidence is added when performed; no remote issue publication or merge is claimed.
- Independent review and resolved comments:
- Local verification (2026-10-18): `git diff --check` passed for tracked edits; content checks on all nine affected documents passed for trailing whitespace, 203 relative Markdown targets/anchors, 29 unique issue IDs and the four story templates' required sections/unchecked acceptance criteria. These are documentation checks, not implementation tests or independent approval.
- Remaining work: close each story's applicable R01–R06 refinements after EN-01 decisions; agree implementation owner/reviewer/estimate/capacity before Ready.
- [ ] DoR reviewed with date, estimate, owner and reviewer confirmed.
- [ ] Acceptance criteria and applicable DoD verified with independent review and PR evidence.
