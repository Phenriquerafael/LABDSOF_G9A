# [DISC-01-01] Prepare research and participant data handling

- Publication: [#23](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/23).
- Evidence and review snapshot: [completion record](#completion-record).
- Milestone: Sprint A (verified on the linked issue on 2026-10-25); planning horizon: Sprint 1; preparation revision: 2026-10-15; planning allowance: 6 person-hours (4 preparation, 1 setup/checks, 1 review), excluding collection.
- Type: task; suggested labels: `type:task`, `area:product`, `phase:2`, `priority:must`.
- Parent: [DISC-01](DISC-01-user-research.md); epic: [EP-00](../epics/EP-00-discovery-and-planning.md).
- Allocation: see the [backlog README](../README.md).
- Source: [Assignment](../../../LABDSOF-26-27-Assignment.md) §5.1, §5.3, §11; §7.1.2 items 1 and 3.
- Dependencies for completion: No blocking predecessor task; use current proposals as inputs.
- Related decisions: DEC-02, DEC-07, in the [register](../../planning/decisions-and-feedback.md).

## Objective and scope

Prepare a feasible study of actual maintenance coordination practices before collecting participant data.

Existing drafts are inputs to review and improve; do not recreate work already supported by evidence. Preparation may overlap predecessor work; confirm dependent conclusions only after the needed findings/decisions exist.

Excluded: Executing interviews, claiming findings, and final production data policies.

## Acceptance criteria

- [ ] Review the existing administrator, resident and contractor guides against hypotheses P1–P7; explain the intended sample and professional/volunteer distinction.
- [ ] Record recruitment routes, anonymous participation/storage permission, notes-only choices, record owner, repository readership and retention limits; no participant identities, contact lists, identity maps or consent attachments collected. User-selected anonymous Git retention replaces the separate-storage/deletion-date design.
- [ ] Agree who conducts and records each session and what to do if access fails; do not invent participant commitments.
- [ ] Have the reviewer approve the collection arrangements and update DEC-07 to the level needed for research.

## Deliverables and evidence

- [Collection procedure and guide coverage](../../templates/research-collection.md).
- [Research record template](../../templates/research-record.md) — update the relevant sections and link the change/review evidence.
- [Security/privacy assessment](../../09-security-privacy.md) — update the relevant sections and link the change/review evidence.

## Verification

Reviewer checks the guides and data-handling arrangements against the research questions before participant collection.

## Completion record

Record revised 2026-10-25 in PR #39: preparation guidance and deliverable links relocated to the collection procedure; original evidence and historical verification results unchanged. This revision does not certify the closed issue's acceptance criteria.

Preparation revised 2026-10-15; integration and review snapshot checked on 2026-10-22.

| Acceptance criterion | Evidence | Review / completion state |
|---|---|---|
| Guides, sample and segment distinction | [P1–P7 coverage](../../templates/research-collection.md#1-guides-and-hypothesis-coverage) and [future sample](../../templates/research-collection.md#2-future-sample-and-access) | Preparation supplied; targets are not recruited participants |
| Consent, storage and retention | [Session procedure](../../templates/research-collection.md#3-consent-and-session-procedure), [record template](../../templates/research-record.md), [security policy](../../09-security-privacy.md#41-research-data-handling-disc-01-01) | Anonymous Git storage reflects the user's choice |
| Session arrangements and access failures | [Interview pair, replacements and fallback](../../templates/research-collection.md#2-future-sample-and-access) | Arrangements documented; check repository visibility and survey settings before real collection |
| Reviewer approval and DEC-07 | [Decision rationale](../../planning/decisions-and-feedback.md#dec-07-research-preparation-disc-01-01); [PR #35](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/35) | PR merged; no GitHub review entries found in the dated check, so approval criterion remains unevidenced |

The author-side privacy/content check of the eight simulated records is recorded once in [DISC-01-02](DISC-01-02-conduct-research.md#completion-record). Independent review is still required by the [DoD](../../governance/definition-of-done.md).
