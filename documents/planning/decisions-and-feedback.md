# Pending decisions and feedback

**Status:** decision register and team updates · **Updated:** 2026-10-22

A provisional baseline enables consistent documents; it does not mean approval. Named role holders are recorded in the [team agreement](../governance/team-working-agreement.md); item owners and deadlines still require assignment. When deciding, record evidence, author, date and affected documents. The recording dates below do not imply that the meetings occurred on those dates.

## 1. Open decisions

| ID | Question | Provisional baseline / alternatives | Participants (roles mapped in team agreement) | Timing | Status |
|---|---|---|---|---|---|
| DEC-01 | Coordination or IoT? | Coordination only; IoT, monitoring and prediction excluded from the MVP; reopen only through a scope review ([vision §4.2](../04-product-vision.md#42-iot-decision-dec-01)) | Team, BA/PO, lecturers | Before finalising the MVP | Proposed by BA/PO on 2026-10-19 (DISC-03-03); team agreement pending |
| DEC-02 | Segment and commercial model | Property management companies; volunteers secondary; SaaS is a hypothesis | BA/PO, administrators | After initial research | To be validated |
| DEC-03 | Team, schedule, capacity and Sprint B | Five named members and responsibilities agreed; P1 = PM, P3 = BA/PO. Three official sprints; phases 1–3 within Sprint 1; do not assume B = Sprint 2 | Pedro (PM), team, lecturers | Before committing to Sprint B | Assignments confirmed; schedule, capacity and Sprint B unresolved |
| DEC-04 | Stack, boundaries and infrastructure | Independent Issue + Dispatch; worker/queue; modular alternative subject to acceptance | Tech Lead, DevOps, team | Sprint 1 design; before implementation | Proposed ADR-001 |
| DEC-05 | AI workflow, provider and evaluation | Text classification, baseline/fallback, one provider; optional embeddings | AI, QA, BA/PO | Before the AI story meets DoR | Undecided |
| DEC-06 | Integration and notifications | Realistic simulated calendar; real optional; one proposed in-app channel | Tech Lead, BA/PO | Before integration | Undecided |
| DEC-07 | Visibility and data lifecycle | Research: anonymous answers in Git, no participant identities/maps, permission for repository retention; production: private reports and shared summary | Sandro (research records), Pedro (collection), Martim (review), BA/PO methodological input; task allocation in backlog | Anonymous collection and pre-commit check; production design under EN-01-04 | User-selected Git storage; production policies separate |
| DEC-08 | Baselines and targets | Administrative effort as primary metric; provisional technical targets | QA, BA/PO, AI | Before formal evaluation | To be calibrated |
| DEC-09 | Methodology, board and Git | Adapted Scrum, GitHub Projects or Jira, short-lived branches and reviewed PRs | Team | Phase 1 | To be ratified/configured |
| DEC-10 | Approval and confirmation | Administrator approves request; contractor accepts; calendar/manual booking confirmation; contractor reports completion; administrator closes ([vision §4.3](../04-product-vision.md#43-distinct-steps-dec-10)) | BA/PO, administrators and contractors | Before US-07–US-09 | Step definitions proposed on 2026-10-19; validation with administrators and contractors pending |

### DEC-07 research preparation (DISC-01-01)

- **Source and choice:** the user selected anonymous Markdown answers in Git, superseding the earlier separate personal-data archive and fixed-deletion design.
- **Rationale:** answer records support research traceability without retaining identities or an identity lookup. Identifiable or merely pseudonymous records are excluded; repository readers and Git history/copies constrain retention promises.
- **Implementation:** the [security policy](../09-security-privacy.md#41-research-data-handling-disc-01-01) owns handling controls; the [collection procedure](../templates/research-collection.md) owns consent, recruitment and session arrangements. [DISC-01-01](../backlog/tasks/DISC-01-01-prepare-research.md#completion-record) records preparation and review evidence. Production permissions/retention remain separate design decisions.

### DISC-01-02 simulated research record

**Recorded 2026-10-22:** use the simulated-interview option from the reported lecturer clarification. This permits scenario exploration for Sprint 1; it does not validate DEC-02/08/10. The [research method](../03-user-research.md#2-method-and-evidence-coverage) records actual coverage and clarification limits; the [inventory](../research/answers/README.md) records provenance. Collection verification and integration belong to [DISC-01-02](../backlog/tasks/DISC-01-02-conduct-research.md#completion-record).

### Confirmed Sprint 1 scope decision — DEC-11

- **Recorded:** 2026-10-10, from the team's update in the project conversation.
- **Clarification:** the evaluator confirmed that the walking skeleton is optional for Sprint 1.
- **Team decision:** do not develop the walking skeleton this sprint. Its absence is not a Sprint 1 completion blocker; it is not marked as implemented.
- **Change:** the earlier plan treated §7.1.2 item 10 as required in Sprint 1. The revised plan excludes that implementation and retains EN-02 as a candidate foundation for later implementation planning.
- **Scope:** other Sprint 1 discovery/design deliverables and later technical delivery requirements remain applicable. The original assignment is retained unchanged.
- **Traceability:** README, strategy, roadmap, backlog, Sprint 1/Sprint B plans, walking skeleton plan, team agreement and milestone conventions updated. Evaluator name, clarification date and meeting link were not supplied.

### Product scope proposals — DISC-03-03

- **Recorded:** 2026-10-19 by Afonso (BA/PO) for [#14](https://github.com/Phenriquerafael/LABDSOF_GX/issues/14). Team agreement is sought through the pull-request review (proposed reviewer: Martim); until then these are proposals, not stakeholder or lecturer approval, and not evidence for §5.7.
- **Evidence used:** secondary findings PS-01–PS-08 ([Public-source findings](../03-user-research.md#32-public-source-findings)) and competitor sources S01–S28 ([02 §5](../02-market-and-competitor-analysis.md#5-source-and-findings-register)). No primary research exists; DISC-01-03 is open, so personas and journeys keep their remaining hypotheses explicit.
- **DEC-01:** exclude IoT from the MVP. Reasons: not required by the assignment; no finding identifies a decision that sensor data would improve; a suite marketed in Portugal already bundles hardware (S04); capacity. Alternative considered: one simulated sensor scenario as Could — rejected because it would not test BMC's proposition.
- **DEC-08:** propose a 30% active-time reduction threshold; the [vision](../04-product-vision.md#51-primary-success-criterion-dec-08) owns the calculation, guards and baseline limitations. Alternatives considered: 20% (judged hard to separate from noise in a three-to-five-person sample) and 50% (judged likely to fail on factors outside the product). This rationale is team judgement, not a sourced benchmark.
- **DEC-10:** triage decision, approval, acceptance, booking confirmation, completion report, closure and impact confirmation defined as distinct steps, consistent with [07 §3](../07-technical-design.md#3-states-and-business-rules).
- **DEC-07 input:** the impact-confirmation review adds neutral count wording, no confirmation list for administrators and an open option on exact counts in very small buildings; the policy itself stays with DEC-07.
- **Affected documents:** [vision](../04-product-vision.md), [strategy](../building-maintenance-coordinator-strategy.md), [requirements](../requirements.md), [backlog §5](../05-product-backlog.md#5-wont-in-this-baseline--alternatives), [README](../../README.md). The IoT row of the former roadmap is carried by backlog §5 since the roadmap was removed in #16. US-04 criteria are unchanged; the counter wording is a refinement for the US-04 owner to consider.

### DISC-01-03 synthesis proposals

**Recorded 2026-10-22 for [#21](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/21).** Proposed by the agent during implementation; independent/team approval pending. Allocation remains in the backlog README. This is research synthesis, not lecturer feedback or evidence of meeting the separate feedback obligation.

Evidence: [scenario interpretations SF-01 to SF-07](../03-user-research.md#33-scenario-synthesis-disc-01-03) and [public findings PS-01 to PS-08](../03-user-research.md#32-public-source-findings).

| Proposal / existing decision | Before and proposed outcome | Rationale / alternative considered | Affected artefacts |
|---|---|---|---|
| SP-01 / DEC-02 | Broad coordination opportunity -> explicitly conditional on fragmentation/contact volume; retain professionals as primary | SF-01/04 show contrasting structured/low-volume scenarios. Reject extrapolating volunteer interest to business demand; do not commit new integrations. | [Problem sections 2/4/5/8](../01-problem-and-opportunity-report.md), [vision personas/J2](../04-product-vision.md), [US-02/06](../05-product-backlog.md#4-stories-and-criteria) |
| SP-02 / DEC-07 | Retain controlled shared status and optional participation; US-05 remains Should | SF-02/05 include low duplication, distinct faults and telephone preference. Automatic merging and mandatory digital participation are not justified. Assisted reporting needs design/testing before implementation commitment. | [RF-01/04/05](../requirements.md#functional-requirements), US-01/04/05/10, vision J1/participation |
| SP-03 / DEC-05 | Retain correctable AI with rules/manual fallback as an experiment | SF-03/07 do not establish poor current triage or trust. Reject autonomous diagnosis; compare against the existing manual/rules baseline before claiming benefit. | RF-02/03, NFR-03/10, US-02/03, AI-01, vision J2 |
| SP-04 / DEC-10 | Retain separate approval, acceptance, booking confirmation, completion and closure | SF-06 challenges automatic availability and compulsory extra apps. Retain manual coordination and refusal/rescheduling; no new contractor-app requirement. | RF-07/08/09, NFR-11, US-07/08/09, [vision section 4.3](../04-product-vision.md#43-distinct-steps-dec-10) |
| SP-05 / DEC-08 | Retain provisional controlled-task protocol/threshold; no empirical baseline supplied | SF-01 times are fictional; SF-07 requires wrong/unavailable-suggestion cases. Reject averaging invented times or claiming operational savings. Include low-effort process counterexamples. | [Vision section 5.1](../04-product-vision.md#51-primary-success-criterion-dec-08), EN-04, AI-01, LIM-04 |

Requirement and story IDs refer to [requirements](../requirements.md) and the [product backlog](../05-product-backlog.md). Existing priorities and MVP boundaries are retained; this synthesis changes the problem's qualification and evidence traceability, not the implementation scope. Independent review should assess source-to-interpretation links and the scope rationale.

## 2. Editorial harmonisation

These are neither investor feedback nor user-validated choices.

| Conflict | Treatment on 2026-10-07 |
|---|---|
| 05 treated as backlog | Roadmap retained; 06-product-backlog created |
| MVP ended at notification | Completion, closure and history made explicit |
| Approval confused with scheduling | Approval, acceptance and confirmation separated |
| Photos/costs/summaries in Sprint 3 and after the course | Post-MVP, without Sprint 3 commitment |
| Automatic vs human approval | Automatic approval outside baseline |
| 100% of critical cases as a guarantee | Criterion restricted to the test set |
| Not found = nonexistent | Comparison marked preliminary/unconfirmed |
| IoT in notes vs vision scope | Preserved for DEC-01 |
| Git protections and board as facts | Proposed configurations without remote evidence |

## 3. Stakeholder/investor feedback

The evaluator clarification below was reported by the team. No separate investor review session or revision of a product/technical decision has been recorded; the scope clarification alone is not treated as proof of meeting §5.7.

| ID | Date/participants | Feedback and evidence | Previous → revised decision | Reason | Documents/issues | Owner/status |
|---|---|---|---|---|---|---|
| FB-01 | Recorded 2026-10-10; team reports evaluator clarification; session date/name not supplied | Walking skeleton optional in Sprint 1; source: team update in project conversation | Required Sprint 1 skeleton → no skeleton development this sprint | Team chose not to implement the optional deliverable | DEC-11; EN-02; Sprint 1 plan | Team decision confirmed; Pedro coordinates planning updates |

Use the [template](../templates/investor-review.md). At least one decision must actually be revised in response to lecturers (§5.7). Minutes without a change do not meet that requirement.

## 4. Limitations and technical debt

| ID | Limitation | Impact | Next action | Owner |
|---|---|---|---|---|
| LIM-01 | No real participant research; eight simulated records inventoried on 2026-10-22 | Scenarios do not validate value, frequency or adoption | DISC-01-03 records SF-01 to SF-07 and P1-P7 dispositions; empirical validation remains future work | See DISC-01 allocation |
| LIM-02 | Incomplete competitor sources | Differentiation not demonstrated | DISC-02 | To be assigned |
| LIM-03 | No application code, CI or deployment in this baseline | Later technical requirements not yet demonstrated; optional skeleton excluded from Sprint 1 by DEC-11 | EN-01 design; EN-02 considered in later implementation planning | To be assigned |
| LIM-04 | No measured baseline for the primary metric; the current-process condition will be simulated | An effort reduction can be shown only in controlled tasks, not in real operation | DISC-01-02 scenario times are fictional, not a baseline; obtain empirical estimates or controlled task measurements and freeze the protocol/threshold before EN-04 | Afonso (BA/PO) |

Add implementation debt when it exists; future features are not automatically technical debt.
