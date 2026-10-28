# Epic, planning task and user story specifications

**Status:** local issue specifications and allocation index, originally drafted in October 2026. Research issues #21-23 are published; their task records link to publication/integration evidence. GitHub owns live status, assignees and estimates. Functional roles do not override the task allocation below.

This folder contains **5 epic specifications, 4 parent-task specifications, 15 original Sprint 1 delivery-task specifications, 1 PLAN-02 preparation task and 4 EP-02 story drafts**. Published and draft records retain their individual publication state; these counts do not imply completion. The [product backlog](../05-product-backlog.md) remains the scope and priority overview. Existing product documents hold the deliverables; these files specify the work and its completion evidence.

The walking skeleton (EN-02) is excluded from Sprint 1 under DEC-11. EP-01/EP-03 now have epic drafts for later implementation; their US stories are defined in the product backlog but do not yet have separate issue draft files here. EP-02 now has individual US-03/05/14/15 drafts for later delivery, prepared under PLAN-02. EP-02/EP-04 span later sprints; neither AI-01 nor PLAN-02 completes implementation or final evaluation. Drafting or publishing a future epic does not commit implementation to Sprint 1.

## Hierarchy and issue index

Use epic → parent task → delivery task for broad discovery/engineering items. AI-01 is a direct task under EP-02. Stable IDs are local identifiers, not GitHub issue numbers.

For implementation, use epic → user story → implementation subtask when needed. Keep dependency links separate from parent/child relationships. This package currently has 29 issue specification/draft files in `epics/` and `tasks/`, excluding this README; reconcile with existing remote issues by stable ID before publishing to avoid duplicates.

| Epic draft | Parent/direct item | Purpose |
|---|---|---|
| [EP-00](epics/EP-00-discovery-and-planning.md) | [DISC-01](tasks/DISC-01-user-research.md) | Gather user evidence and document the problem |
| [EP-00](epics/EP-00-discovery-and-planning.md) | [DISC-02](tasks/DISC-02-market-comparison.md) | Complete the market and competitor comparison |
| [EP-00](epics/EP-00-discovery-and-planning.md) | [DISC-03](tasks/DISC-03-organisation-and-product-planning.md) | Agree organisation, product scope and priorities |
| [EP-01](epics/EP-01-reporting-and-tracking.md) | [US-01/02/04/10](../05-product-backlog.md#4-stories-and-criteria), story drafts pending | Reporting, manual triage, shared impact and notifications; S2 implementation |
| [EP-02](epics/EP-02-assisted-triage.md) | [AI-01](tasks/AI-01-assess-ai-opportunity.md), [PLAN-02](tasks/PLAN-02-prepare-ai-and-fallback-stories.md); [US-03](tasks/US-03-classify-with-ai.md), [US-05](tasks/US-05-review-duplicate-suggestions.md), [US-14](tasks/US-14-continue-triage-without-ai.md), [US-15](tasks/US-15-evaluate-ai-against-baseline.md) | AI design/preparation; classification, provider-free fallback, optional links and comparative evaluation |
| [EP-03](epics/EP-03-intervention-and-closure.md) | [US-06–09/11–13](../05-product-backlog.md#4-stories-and-criteria), story drafts pending | Contractor selection through closure; S2 core, conditional extensions |
| [EP-04](epics/EP-04-engineering-and-quality.md) | [EN-01](tasks/EN-01-technical-design.md) | Consolidate technical design, ADRs and security |

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

## EP-02 story drafts and planning allocation

| Item | Drafting owner | Independent review / implementation planning |
|---|---|---|
| [PLAN-02](tasks/PLAN-02-prepare-ai-and-fallback-stories.md) | Sandro Dias (user-assigned) | Another team member reviews preparation; estimate/review evidence recorded in planning/PR |
| [US-03](tasks/US-03-classify-with-ai.md) | Sandro Dias under PLAN-02 | Implementation owner/reviewer/estimate/capacity before Ready; S2 initial delivery |
| [US-14](tasks/US-14-continue-triage-without-ai.md) | Sandro Dias under PLAN-02 | Provider-free rules/manual continuity; S2, hardened in S3 |
| [US-05](tasks/US-05-review-duplicate-suggestions.md) | Sandro Dias under PLAN-02 | Should; select/defer explicitly after evidence and capacity review |
| [US-15](tasks/US-15-evaluate-ai-against-baseline.md) | Sandro Dias under PLAN-02 | Dataset/protocol preparation in S2; formal results in S3; EN-04 consumes the report |
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
