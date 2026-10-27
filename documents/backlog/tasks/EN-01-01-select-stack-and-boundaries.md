# [EN-01-01] Select the stack and accept architecture decisions

- Publication: Published as [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15) (checked 2026-10-27; GitHub milestone `Sprint A`); GitHub owns live status.
- Workflow: Backlog; proposed milestone: S1 — Discover, Validate and Design; dates/estimate: to be agreed.
- Type: task; suggested labels: `type:task`, `area:backend`, `phase:3`, `priority:must`.
- Parent: [EN-01](EN-01-technical-design.md); epic: [EP-04](../epics/EP-04-engineering-and-quality.md).
- Allocation: see the [backlog README](../README.md).
- Source: [Assignment](../../../LABDSOF-26-27-Assignment.md) §6.2–§6.5; §7.1.2 items 7 and 8.
- Dependencies for completion: No blocking predecessor task; use current proposals as inputs.
- Related decisions: DEC-04, DEC-06, in the [register](../../planning/decisions-and-feedback.md).

## Objective and scope

Choose a feasible technical direction using the current scope and actual team skills/capacity.

Existing drafts are inputs to review and improve; do not recreate work already supported by evidence. Preparation may overlap predecessor work; confirm dependent conclusions only after the needed findings/decisions exist.

Excluded: Building services, benchmarking invented results and selecting technologies solely to fill document fields.

## Acceptance criteria

- [ ] Compare credible alternatives for client/backend stack, persistence, asynchronous transport and deployment, recording evidence and operational/learning costs.
- [ ] Decide Issue/Dispatch boundaries and ownership, worker placement and integration approach; record consequences of shared infrastructure.
- [ ] Accept or revise ADR-001 and create additional ADRs only for significant choices, with decision-makers, dates, rationale and trade-offs.
- [ ] If proposing a modular alternative, record lecturer acceptance or keep the exception explicitly unresolved; do not assume permission.
- [ ] Update DEC-04/06 and list unresolved details with owners and impact on later implementation.

## Deliverables and evidence

- [Technical design](../../07-technical-design.md) — update the relevant sections and link the change/review evidence.
- [Backend ADR](../../adr/ADR-001-backend-boundaries.md) — update the relevant sections and link the change/review evidence.
- [ADR index](../../adr/README.md) — update the relevant sections and link the change/review evidence.
- [ADR template](../../templates/adr.md) — update the relevant sections and link the change/review evidence.
- [Decision register](../../planning/decisions-and-feedback.md) — update the relevant sections and link the change/review evidence.

## Verification

Reviewer checks that accepted decisions have actual decision evidence and that the proposed deployment fits team capacity.

Use the documentation/research checks appropriate to this task; implementation tests are not required for a design-only outcome.

## Completion record

- Result/findings and limitations: proposal revised 2026-10-27 by Ricardo (Tech Lead): ADR-001–006 revised in place and ADR-007–012 added ([ADR index](../../adr/README.md), evidence register E01–E83; ADR-011 client and ADR-012 health and status page added the same day); technical design, contract annex, security, requirements, backlog (US-14 proposal) and register aligned. Limitations: nothing is accepted; team review (EN01-U1) and the two-day spike (EN01-U2) are pending; no value or memory figure has been measured; nothing has been built or tested.
- Evidence/PR/review links: the pull request for the `docs/EN-01-01-select-stack` branch (to be opened); independent review pending. Document presence alone is not completion evidence.
- Decision/requirement changes: DEC-04/06 revised and DEC-07 production notes added in the [register](../../planning/decisions-and-feedback.md#stack-revision--en-01-01-2026-10-27); NFR-01/04/06/07 reworded; EN-01-02 §4.3 changed to projection-based authorisation (pending Afonso's review); unresolved details EN01-U1–U15 in [register §5](../../planning/decisions-and-feedback.md#5-en-01-01-unresolved-details).
- [ ] DoR reviewed with date, estimate, owner and reviewer confirmed.
- [ ] Acceptance criteria and applicable [DoD](../../governance/definition-of-done.md) verified with evidence.
