# [DISC-01-01] Prepare research and participant data handling

- Publication: Local task record; no remote issue URL recorded.
- Delivery: Research preparation documented; integration and independent review through PR.
- Milestone: S1 — Discover, Validate and Design; preparation revision: 2026-10-15; planning allowance: 6 person-hours (4 preparation, 1 setup/checks, 1 review), excluding collection.
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

- [Research plan](../../03-user-research.md) — update the relevant sections and link the change/review evidence.
- [Research record template](../../templates/research-record.md) — update the relevant sections and link the change/review evidence.
- [Security/privacy assessment](../../09-security-privacy.md) — update the relevant sections and link the change/review evidence.

## Verification

Reviewer checks the guides and data-handling arrangements against the research questions before participant collection.

Use the documentation/research checks appropriate to this task; implementation tests are not required for a design-only outcome.

## Completion record

- Preparation revised 2026-10-15: P1–P7 coverage, sample/segment rationale, recruitment routes, consent text, notes-only collection and named responsibilities defined. At the user's direction, retain only anonymous answers in Git; remove the separate personal-data archive and fixed-deletion design.
- Evidence: [guide coverage](../../03-user-research.md#guide-review-against-p1p7-disc-01-01), [collection arrangements](../../03-user-research.md#32-collection-arrangements), [interview templates](../../templates/interviews/README.md), [record template](../../templates/research-record.md), [research safeguards](../../09-security-privacy.md#41-research-data-handling-disc-01-01). Branch: `docs/DISC-01-01-research-data-handling`.
- Decision: [DEC-07 research arrangements](../../planning/decisions-and-feedback.md#dec-07-research-preparation-disc-01-01) select anonymous answer records in Git, Sandro as record owner, Pedro/Ricardo as interview pair, Afonso/Sandro as replacements and Martim as reviewer. Anonymous responses remain with academic project/history; no identity lookup or complete-erasure promise. DEC-02 remains a product hypothesis.
- Planning: owner Sandro, reviewer Martim, 6 person-hours allowance. Scope and verification are documentation/research preparation only; research collection remains DISC-01-02 and synthesis DISC-01-03. These are current planning choices, not a retrospective claim of a team DoR meeting.
- Delivery process: commit and open a PR referencing DISC-01-01; Martim reviews, comments are resolved, applicable checks pass and the change is merged. Record actual PR/review evidence and mark acceptance/DoD boxes only against that evidence. No remote publication, independent approval or merge is asserted here.
- Execution boundary: blank templates and eight completed simulated interview records are included. There are no real participants or consent records; formal findings synthesis and independent approval remain separate. Repository visibility and survey settings must be checked if real participant collection is later undertaken.
- Documentation/privacy review (2026-10-22): all eight simulated records were read; no participant names, contacts, exact addresses, companies, signatures or consent attachments were found. The team contact in the plan identifies the project owner, not a participant. Consent is not applicable to fictional profiles; Git-history retention and the controls for any future real collection remain documented. This author-side content review is not independent approval.
- [ ] Independent review and applicable [DoD](../../governance/definition-of-done.md) evidenced through PR.
