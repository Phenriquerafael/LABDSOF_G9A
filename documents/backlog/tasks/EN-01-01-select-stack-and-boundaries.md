# [EN-01-01] Select the stack, accept architecture decisions and consolidate the views

- Publication: Published as [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15) (checked 2026-10-27; GitHub milestone `Sprint A`); GitHub owns live status. On 2026-10-30 [EN-01-03](EN-01-03-consolidate-architecture-views.md) ([#13](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/13), now closed) was merged into this task, because the views draw the decisions made here; its scope is the second group of criteria below.
- Workflow: Backlog; proposed milestone: S1 — Discover, Validate and Design; dates/estimate: to be agreed.
- Type: task; suggested labels: `type:task`, `area:backend`, `phase:3`, `priority:must`.
- Parent: [EN-01](EN-01-technical-design.md); epic: [EP-04](../epics/EP-04-engineering-and-quality.md).
- Allocation: see the [backlog README](../README.md).
- Source: [Assignment](../../../LABDSOF-26-27-Assignment.md) §6.2–§6.8; §7.1.2 items 7 and 8.
- Dependencies for completion: none for the stack choice; the views also draw on [EN-01-02](EN-01-02-define-domain-and-contracts.md) ([#14](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/14), merged in PR #44).
- Related decisions: DEC-04, DEC-06, in the [register](../../planning/decisions-and-feedback.md).

## Objective and scope

Choose a feasible technical direction using the current scope and actual team skills/capacity, and make the system boundaries, communication and proposed runtime understandable to the whole team.

Existing drafts are inputs to review and improve; do not recreate work already supported by evidence. Preparation may overlap predecessor work; confirm dependent conclusions only after the needed findings/decisions exist.

Excluded: Building services, benchmarking invented results, selecting technologies solely to fill document fields, container builds, live dashboards, deployment or a walking skeleton.

## Acceptance criteria

Stack and decisions:

- [ ] Compare credible alternatives for client/backend stack, persistence, asynchronous transport and deployment, recording evidence and operational/learning costs.
- [ ] Decide Issue/Dispatch boundaries and ownership, worker placement and integration approach; record consequences of shared infrastructure.
- [ ] Accept or revise ADR-001 and create additional ADRs only for significant choices, with decision-makers, dates, rationale and trade-offs.
- [ ] If proposing a modular alternative, record lecturer acceptance or keep the exception explicitly unresolved; do not assume permission.
- [ ] Update DEC-04/06 and list unresolved details with owners and impact on later implementation.

Architecture and deployment views (from EN-01-03):

- [ ] Provide consistent system-context, component/container and deployment views, using diagrams or clear structured tables.
- [ ] Identify independently deployable backend units, worker ownership, data stores, broker, external simulator/provider and trust boundaries.
- [ ] Trace report persistence, event publication, triage suggestion and intervention updates, including retries, duplicates and stale messages.
- [ ] Document proposed configuration/secrets, service identity, health/logs/metrics and recovery responsibilities with a feasible environment.
- [ ] Walk through AI, broker and calendar failure behaviour and clearly distinguish planned design from a tested deployment.

## Deliverables and evidence

- [Technical design](../../07-technical-design.md) — update the relevant sections and link the change/review evidence.
- [Backend ADR](../../adr/ADR-001-backend-boundaries.md) — update the relevant sections and link the change/review evidence.
- [ADR index](../../adr/README.md) — update the relevant sections and link the change/review evidence.
- [ADR template](../../templates/adr.md) — update the relevant sections and link the change/review evidence.
- [Decision register](../../planning/decisions-and-feedback.md) — update the relevant sections and link the change/review evidence.
- [Physical views](../../07b-physical-views.md) — the deployment views and their sources.
- [Requirements/NFRs](../../requirements.md) — update the relevant sections and link the change/review evidence.

## Verification

Reviewer checks that accepted decisions have actual decision evidence and that the proposed deployment fits team capacity, checks the views against the ADRs, and asks another team member to explain the principal flow.

Use the documentation/research checks appropriate to this task; implementation tests are not required for a design-only outcome.

## Completion record

- Result/findings and limitations: proposal revised 2026-10-27 by Ricardo (Tech Lead): ADR-001–006 revised in place and ADR-007–012 added ([ADR index](../../adr/README.md), evidence register E01–E83; ADR-011 client and ADR-012 health and status page added the same day); technical design, contract annex, security, requirements, backlog and register aligned (report photos moved from a backlog story to a register candidate after review). Limitations: nothing is accepted; team review (EN01-U1) and the two-day spike (EN01-U2) are pending; no value or memory figure has been measured; nothing has been built or tested.
- Views: 2026-10-29 — Afonso drafted the physical (deployment) views P1–P7 in [07b — Physical views](../../07b-physical-views.md) from this proposal, with open items P-01 to P-07; 2026-10-30 — Ricardo redrew them as UML deployment diagrams in the Visual Paradigm style, generated by a Python script in [`diagrams/physical-views/`](../../diagrams/physical-views/README.md). Still to do for the view criteria: the system-context and component views, the flow traces, the failure walkthroughs and the Figure 1 redraw.
- Evidence/PR/review links: [PR #45](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/45) (`docs/EN-01-01-select-stack`), which since 2026-10-30 also carries the views of PR #49 (merged into its branch); three read-only AI review rounds are recorded in the PR body; Afonso's comment review of 2026-10-27 (BA/PO and EN-01-02 owner; findings 1–10) addressed in a follow-up commit, his re-check pending; independent team review (Martim, allocated reviewer) pending. Document presence alone is not completion evidence.
- Decision/requirement changes: DEC-04/06 revised and DEC-07 production notes added in the [register](../../planning/decisions-and-feedback.md#stack-revision--en-01-01-2026-10-27); NFR-01/04/06/07 reworded; EN-01-02 §4.3 changed to projection-based authorisation (acknowledged by Afonso on condition that membership events are versioned; addressed, his confirmation pending); unresolved details EN01-U1–U15 in [register §5](../../planning/decisions-and-feedback.md#5-en-01-01-unresolved-details).
- [ ] DoR reviewed with date, estimate, owner and reviewer confirmed.
- [ ] Acceptance criteria and applicable [DoD](../../governance/definition-of-done.md) verified with evidence.
