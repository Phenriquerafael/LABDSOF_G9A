# Epic, planning task and user story specifications

**Status:** local issue specifications and allocation index, originally drafted in October 2026. The original 24 drafts have published issue mappings checked on 2026-10-29. PLAN-01 and the four reporting/tracking stories also map to existing issues, checked on 2026-11-01; this package now contains 29 draft/record files. GitHub owns live status, assignees and estimates. Functional roles do not override the task allocation below.

This folder contains **5 epic drafts, 4 parent-task drafts, 16 delivery/planning-task records and 4 user-story drafts**: all product epics and the detailed Sprint 1 research, planning and design tasks. The [product backlog](../05-product-backlog.md) remains the scope and priority overview. Existing product documents hold the deliverables; these files specify the work and its completion evidence.

The walking skeleton (EN-02) is excluded from Sprint 1 under DEC-11. EP-01 now has separate US-01/02/04/10 drafts for S2 delivery and S3 refinement/evaluation; their technical details are completed after stack/architecture decisions. EP-02/EP-03 implementation stories remain in the product backlog without individual files in this package. EP-02/EP-04 also span later sprints; their Sprint 1 tasks do not complete the entire epic. Drafting or publishing a future story does not commit implementation to Sprint 1.

## Hierarchy and issue index

Use epic → parent task → delivery task for broad discovery/engineering items. AI-01 is a direct task under EP-02. Stable IDs are local identifiers, not GitHub issue numbers.

For implementation, use epic → user story → implementation subtask when needed. Keep dependency links separate from parent/child relationships. PLAN-01 is a direct preparation task under EP-01, alongside the stories it prepares. This package currently has 29 issue draft/record files in `epics/` and `tasks/`; reconcile with existing remote issues by stable ID before publishing to avoid duplicates. The technical-refinement register is supporting documentation, not an additional issue or six extra tasks.

| Epic draft | Parent/direct item | Purpose |
|---|---|---|
| [EP-00](epics/EP-00-discovery-and-planning.md) | [DISC-01](tasks/DISC-01-user-research.md) | Gather user evidence and document the problem |
| [EP-00](epics/EP-00-discovery-and-planning.md) | [DISC-02](tasks/DISC-02-market-comparison.md) | Complete the market and competitor comparison |
| [EP-00](epics/EP-00-discovery-and-planning.md) | [DISC-03](tasks/DISC-03-organisation-and-product-planning.md) | Agree organisation, product scope and priorities |
| [EP-01](epics/EP-01-reporting-and-tracking.md) | [US-01/02/04/10](../05-product-backlog.md#4-stories-and-criteria), story drafts pending | Reporting, manual triage, shared impact and notifications; S2 implementation |
| [EP-02](epics/EP-02-assisted-triage.md) | [AI-01](tasks/AI-01-assess-ai-opportunity.md), [PLAN-02](#ep-02-story-drafts-and-planning-allocation); [US-03](tasks/US-03-classify-with-ai.md), [US-05](tasks/US-05-review-duplicate-suggestions.md), [US-14](tasks/US-14-continue-triage-without-ai.md), [US-15](tasks/US-15-evaluate-ai-against-baseline.md) | AI design/preparation; classification, provider-free fallback, optional links and comparative evaluation |
| [EP-03](epics/EP-03-intervention-and-closure.md) | [US-06–09/11–13](../05-product-backlog.md#4-stories-and-criteria), story drafts pending | Contractor selection through closure; S2 core, conditional extensions |
| [EP-04](epics/EP-04-engineering-and-quality.md) | [EN-01](tasks/EN-01-technical-design.md) | Consolidate technical design, ADRs and security |

### Published issue mapping

Checked on 2026-10-29 with `gh issue list --repo Phenriquerafael/LABDSOF_G9A --state all --limit 200`, matching the `[ID]` prefix of each issue title; creation dates come from the issue API. This records that the issues exist; it does not show that the board, labels, milestones or sub-issue links are configured. GitHub owns live state.

| Draft ID | GitHub issue |
|---|---|
| EP-00 | [#29](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/29) |
| EP-01 | [#10](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/10) |
| EP-02 | [#28](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/28) |
| EP-03 | [#9](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/9) |
| EP-04 | [#27](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/27) |
| DISC-01 | [#26](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/26) |
| DISC-02 | [#25](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/25) |
| DISC-03 | [#24](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/24) |
| EN-01 | [#16](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/16) |
| AI-01 | [#17](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/17) |
| DISC-01-01 | [#23](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/23) |
| DISC-01-02 | [#22](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/22) |
| DISC-01-03 | [#21](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/21) |
| DISC-02-01 | [#34](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/34) |
| DISC-02-02 | [#33](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/33) |
| DISC-03-01 | [#32](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/32) |
| DISC-03-02 | [#20](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/20) |
| DISC-03-03 | [#31](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/31) |
| DISC-03-04 | [#19](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/19) |
| DISC-03-05 | [#18](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/18) |
| EN-01-01 | [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15) |
| EN-01-02 | [#14](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/14) |
| EN-01-03 | [#13](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/13) |
| EN-01-04 | [#12](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/12) |
| PLAN-01 | [#8](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/8) |
| US-01 | [#5](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/5) |
| US-02 | [#4](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/4) |
| US-04 | [#3](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/3) |
| US-10 | [#2](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/2) |

PLAN-01 and US-01/02/04/10 map to existing issues (verified by stable ID on 2026-11-01); these drafts do not create new work items. Other remote issues without a draft here (PLAN-02/03, DEVOPS-01/02, AGENT-01/02, DISC-03-06) are outside this 29-record package.

| Delivery task | Proposed owner | Proposed reviewer | Predecessors for completion |
|---|---|---|---|
| [DISC-01-01 — Prepare research and participant data handling](tasks/DISC-01-01-prepare-research.md) | Sandro | Martim | None |
| [DISC-01-02 — Conduct research and record source evidence](tasks/DISC-01-02-conduct-research.md) | Pedro | Afonso | DISC-01-01 |
| [DISC-01-03 — Synthesise research and update the problem report](tasks/DISC-01-03-synthesise-findings.md) | Ricardo | Sandro | DISC-01-02 |
| [DISC-02-01 — Verify competitor and alternative sources](tasks/DISC-02-01-verify-competitor-sources.md) | Afonso | Ricardo | None |
| [DISC-02-02 — Compare alternatives and assess differentiation](tasks/DISC-02-02-compare-alternatives.md) | Martim | Pedro | DISC-02-01 |
| [DISC-03-01 — Agree working practices, dates and capacity](tasks/DISC-03-01-agree-working-practices.md) | Ricardo | Pedro | None |
| [DISC-03-02 — Configure and verify project tracking](tasks/DISC-03-02-configure-project-tracking.md) | Sandro | Afonso | DISC-03-01 |
| [DISC-03-03 — Refine vision, journeys and success criteria](tasks/DISC-03-03-refine-product-vision.md) | Afonso | Martim | DISC-01-03, DISC-02-02 |
| [DISC-03-04 — Prioritise backlog and prepare the release plan](tasks/DISC-03-04-prioritise-and-plan-backlog.md) | Pedro | Sandro | DISC-03-01, DISC-03-03, EN-01-01 |
| [DISC-03-05 — Prepare Sprint 1 review and record stakeholder feedback](tasks/DISC-03-05-record-sprint-review.md) | Martim | Ricardo | DISC-03-04, EN-01, AI-01 |
| [EN-01-01 — Select the stack and accept architecture decisions](tasks/EN-01-01-select-stack-and-boundaries.md) | Ricardo | Martim | None |
| [EN-01-02 — Consolidate the domain model and contract outlines](tasks/EN-01-02-define-domain-and-contracts.md) | Afonso | Ricardo | DISC-03-03, EN-01-01 |
| [EN-01-03 — Consolidate architecture and deployment views](tasks/EN-01-03-consolidate-architecture-views.md) | Ricardo | Sandro | EN-01-01, EN-01-02 |
| [EN-01-04 — Review the initial security and privacy assessment](tasks/EN-01-04-review-security-and-privacy.md) | Martim | Ricardo | EN-01-01, EN-01-02 |
| [AI-01 — Assess the AI opportunity and define evaluation](tasks/AI-01-assess-ai-opportunity.md) | Sandro | Afonso | DISC-01-03, DISC-03-03 |

The owner coordinates the outcome; others can contribute. Team P1–P5 identifiers and contact details are in the [team agreement](../governance/team-working-agreement.md). Research hypotheses P1–P7 are unrelated identifiers. GitHub usernames must be verified separately; emails and school numbers are not usernames.

This README is the single local source for task ownership and review allocation. Task Markdown files link here rather than repeating assignments.

| Newly drafted epic | Coordinator | Reviewer |
|---|---|---|
| [EP-01](epics/EP-01-reporting-and-tracking.md) | To be agreed during planning | To be agreed during planning |
| [EP-03](epics/EP-03-intervention-and-closure.md) | To be agreed during planning | To be agreed during planning |

| Parent task | Proposed coordinator | Proposed reviewer |
|---|---|---|
| [DISC-01](tasks/DISC-01-user-research.md) | Ricardo | Sandro |
| [DISC-02](tasks/DISC-02-market-comparison.md) | Martim | Afonso |
| [DISC-03](tasks/DISC-03-organisation-and-product-planning.md) | Pedro | Martim |
| [EN-01](tasks/EN-01-technical-design.md) | Ricardo | Martim |

For AI-01, Ricardo supports review of interface assumptions and Martim supports review of data handling as needed; Afonso remains the proposed primary reviewer.

## EP-01 story drafts and planning allocation

| Item | Estimate | Preparation owner | Independent reviewer | Implementation allocation |
|---|---|---|---|---|
| [PLAN-01](tasks/PLAN-01-prepare-reporting-and-tracking-stories.md) | Separate preparation task | Sandro | Pedro | Documentation only; no implementation assignment |
| [US-01](tasks/US-01-record-and-view-report.md) | 5 SP | Select during story refinement | Agree before Ready | Owner before Ready; sprint/capacity during planning |
| [US-02](tasks/US-02-triage-manually-and-track-states.md) | 8 SP | Select during story refinement | Agree before Ready | Owner before Ready; sprint/capacity during planning |
| [US-04](tasks/US-04-publish-shared-issue-and-confirm-impact.md) | 5 SP | Select during story refinement | Agree before Ready | Owner before Ready; sprint/capacity during planning |
| [US-10](tasks/US-10-notify-changes.md) | 8 SP | Select during story refinement | Agree before Ready | Owner before Ready; sprint/capacity during planning |

Initial estimates recorded on 2026-10-30: **26 SP** for US-01/02/04/10. These are planning estimates, not a recorded team estimation session or a capacity commitment. They include each story's UI/API work, persistence, authorisation, tests and review, assuming shared EN-02/03 foundations. Estimate those foundations separately and count shared work once; points are not hours.

These stories preserve their existing local IDs and Must priorities; none is Ready or implemented. Use the [EP-01 technical-refinement register](ep01-technical-refinement.md) for open EN-01 decisions and closure evidence. It covers stack/boundaries, data/API contracts, identity/access, state/audit/concurrency, event/notification semantics and the verification environment. Close applicable entries before implementation readiness; do not invent a selected stack to complete a draft.

S2 is the proposed initial delivery horizon, with S3 refinement/evaluation. Confirm the configured milestone during planning without assuming that narrative sprint names and remote milestone names are interchangeable. A drafting assignment to Sandro does not automatically assign all implementation to him. Keep the authored preparation record separate from independent review, actual PR/merge and implementation evidence.
## EP-02 story drafts and planning allocation

| Item | Estimate | Drafting owner | Independent review / implementation planning |
|---|---|---|---|
| [PLAN-02](#ep-02-story-drafts-and-planning-allocation) | Separate preparation task | Sandro Dias (user-assigned) | Another team member reviews preparation; estimate/review evidence recorded in planning/PR |
| [US-03](tasks/US-03-classify-with-ai.md) | 8 SP | Sandro Dias under PLAN-02 | Estimate and blocking decisions reviewed before Ready; S2 initial delivery |
| [US-14](tasks/US-14-continue-triage-without-ai.md) | 5 SP | Sandro Dias under PLAN-02 | Provider-free rules/manual continuity; S2, hardened in S3 |
| [US-05](tasks/US-05-review-duplicate-suggestions.md) | 8 SP | Sandro Dias under PLAN-02 | Should; select/defer explicitly after evidence and capacity review |
| [US-15](tasks/US-15-evaluate-ai-against-baseline.md) | 8 SP | Sandro Dias under PLAN-02 | Dataset/protocol preparation in S2; formal results in S3; EN-04 consumes the report |

## Sprint 1 deliverable coverage

| Assignment §7.1.2 | Deliverable | Draft coverage | Primary output |
|---|---|---|---|
| 1 | Problem and opportunity | DISC-01-02/03 | [Problem report](../01-problem-and-opportunity-report.md) |
| 2 | Market and competitor analysis | DISC-02-01/02 | [Competitor analysis](../02-market-and-competitor-analysis.md) |
| 3 | User research | DISC-01-01/02/03 | [Method, findings and limitations](../03-user-research.md); [collection procedure](../templates/research-collection.md) |
| 4 | Product vision | DISC-03-03 | [Vision](../04-product-vision.md) |
| 5 | Product backlog | DISC-03-01/02/04 | [Backlog](../05-product-backlog.md) and [Sprint 1 plan](../planning/sprint-1-plan.md) |
| 6 | Responsible AI opportunity assessment | AI-01 | [AI assessment](../06-responsible-ai-assessment.md) |
| 7 | Technical design | EN-01-01/02/03 | [Design](../07-technical-design.md) |
| 8 | Architecture decision records | EN-01-01; reviewed across design tasks | [ADRs](../08-architecture-decision-records.md) |
| 9 | Security and privacy assessment | EN-01-04; research safeguards in DISC-01-01 | [Security/privacy](../09-security-privacy.md) |
| 10 | Walking skeleton | Not selected for Sprint 1 (DEC-11) | [Retained plan](../10-walking-skeleton.md) |

DISC-03-05 covers the Sprint 1 investor review (§7.1.3), feedback and contribution evidence. DISC-03 stays open if the project-level decision revision required by §5.7 has not happened; the Sprint 1 review task can finish with an explicit tracked follow-up.

## Planning and dependencies

- Start with working-practice/capacity confirmation, research preparation, competitor source verification and architecture alternatives. Assign separate estimates and reviewers before selecting work.
- Participant collection depends on the safeguards in DISC-01-01, not the entire later security-design review.
- Synthesis and comparison feed the vision; the agreed vision and architecture feed contracts, security and AI assessment.
- Backlog refinement and stakeholder discussion can begin with proposals and continue as findings arrive. Completion dependencies describe evidence needed to finish, not a ban on early collaboration.
- Choose only work that fits capacity. Use bounded spikes if a technology question needs an experiment, with its effort limit agreed before execution; no working prototype is required by these drafts.
- The 15 delivery tasks are candidates for the official Sprint 1 milestone; EP-01/EP-03 implementation stories belong to later planning. Clarify “Sprint B” separately; do not copy its later implementation candidates into Sprint 1.
- Attach existing commits/reviews where they demonstrate completed work. Retrospective issue creation must record the real work dates and must not fabricate prior planning.

## Publishing to GitHub

1. Review each draft with the team: confirm scope, acceptance criteria, owner/reviewer, estimate, milestone and readiness using the [DoR](../governance/definition-of-ready.md).
2. Verify repository, GitHub usernames and available labels/milestones. Suggested labels are proposals; these files do not configure GitHub.
3. When issue publication is authorised, reconcile existing issues by stable ID, then create missing epic issues first, parent tasks second and delivery tasks third (AI-01 directly under EP-02). Later implementation stories go directly under their epic, with subtasks beneath each story. Use the first heading as the issue title and the remaining content as its body.
4. Replace relative Markdown links with repository file URLs, preferably commit permalinks for evidence. Relative file links resolve in this folder but should not be pasted unchanged into issue bodies.
5. Add actual parent/child issue links in both directions; use supported sub-issue relationships where available, otherwise explicit linked checklists. Also link dependency issues. Preserve local IDs in titles.
6. Change the local publication field to Published and record its actual issue URL; update the product backlog/index links. Local workflow fields are the initial draft snapshot.
7. After publication, GitHub Issues/Projects own live status, assignees, estimates and discussion. Keep local files as published draft records; do not maintain a competing live board here. Update product documents and the overview at reviews.

Do not infer publication from file presence. Consult each item's publication link and GitHub for current state; drafts and published specifications coexist in this folder.

## Evidence and completion

Trace assignment requirement → epic → parent/task → document/source evidence → reviewed PR → decision/requirement change.

A task may be Done while its parent remains open. Completing an interview guide does not complete research; completing AI-01 does not complete US-03. Use the documentation/research portions of the [DoD](../governance/definition-of-done.md); code tests are not required for design-only work.

For progress charts, count selected delivery tasks once. Exclude epic/parent roll-ups from those totals. Parent coordination is not extra delivery unless separately scoped and estimated.

Leave acceptance boxes unchecked until evidence is reviewed. Link publishable summaries and secure evidence references as appropriate; never copy participant identities, consent forms, raw recordings or secrets into an issue.
