# Pending decisions and feedback

**Status:** decision register and team updates · **Updated:** 2026-10-25

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
| DEC-07 | Visibility and data lifecycle | Research: anonymous answers in Git, no participant identities/maps, permission for repository retention; production: private reports and shared summary | Sandro (research records), Pedro (collection), Martim (review), Afonso (method/synthesis) | Anonymous collection and pre-commit check; production design under EN-01-04 | User-selected Git storage; production policies separate |
| DEC-08 | Baselines and targets | Administrative effort as primary metric; provisional technical targets | QA, BA/PO, AI | Before formal evaluation | To be calibrated |
| DEC-09 | Methodology, board and Git | Adapted Scrum, GitHub Projects or Jira, short-lived branches and reviewed PRs | Team | Phase 1 | To be ratified/configured |
| DEC-10 | Approval and confirmation | Administrator approves request; contractor accepts; calendar/manual booking confirmation; contractor reports completion; administrator closes ([vision §4.3](../04-product-vision.md#43-distinct-steps-dec-10)) | BA/PO, administrators and contractors | Before US-07–US-09 | Step definitions proposed on 2026-10-19; transition, cancellation and concurrency rules proposed in EN-01-02 on 2026-10-19; validation with administrators and contractors pending |

### DEC-07 research preparation (DISC-01-01)

Historical record restored 2026-10-25 in PR #39; the preparation link is relocated, with original roles, rationale and execution boundary preserved.

- **Source:** the user specified that only answers, without participant data, are to be retained in Git. This supersedes the earlier OneDrive/storage and fixed-deletion choices.
- **Decision:** anonymous Markdown answers in `documents/research/answers/`; no participant identities, contact database, identity mapping, recordings or consent attachments. Keep blank guides in the interview template folder. An answer ID identifies a document, not a known person.
- **Roles:** Sandro owns research records; Pedro interviews/recruits, Ricardo takes notes; Afonso replaces Pedro and Sandro replaces Ricardo. Afonso owns method/synthesis; Martim reviews anonymity and handling.
- **Consent/retention:** explain repository readers/potential public visibility, Git history and copies before participation. Record only affirmative anonymous permission for participation/Git storage; quotations separately. Permit corrections/removal during the session before final confirmation; keep no identity lookup afterwards. Anonymous answers remain with the academic project; no fixed deletion date or promise of complete history/clone erasure.
- **Review:** record answers without identifiers from the start. Interviewer/note-taker check before first commit; Martim reviews before merge. Generalise distinctive role/location/date/incident combinations and omit any response that remains identifiable. Survey exports exclude timestamps/account metadata and are not committed as-is; delete working exports after checks and survey-tool responses within seven days of checked export.
- **Sample/recruitment:** two professional administrators, three volunteers, eight residents and two contractors; invitations via existing introductions/public business channels, without copying contacts into research records. One reminder after five working days, close after ten without response. Counts are targets, not commitments or findings.
- **Reason/alternatives:** anonymous answer records support traceability without a separate personal-data archive. Identifiable or merely pseudonymous records are excluded from this Git workflow. Professional evidence gaps still leave DEC-02 unvalidated.
- **Traceability:** [plan](../templates/research-collection.md#3-consent-and-session-procedure), [interview templates](../templates/interviews/README.md), [answer-record template](../templates/research-record.md), [security](../09-security-privacy.md#41-research-data-handling-disc-01-01), [task](../backlog/tasks/DISC-01-01-prepare-research.md#completion-record).
- **Execution boundary:** real interviews remain deferred and templates blank; eight separately labelled simulated records are inventoried under DISC-01-02 below. No real participant permissions, access checks or peer approvals are claimed. Production permissions/retention belong to the technical design/security tasks.

### DISC-01-02 simulated research record

Historical record restored 2026-10-25 in PR #39; no new acceptance or lecturer approval is asserted.

- **Recorded:** 2026-10-22, during execution of [#22](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/22). This documents the method already stated in the research plan; it is not a new lecturer approval or team ratification.
- **Basis:** the [research report](../03-user-research.md) records the reported lecturer clarification permitting real or simulated interviews. The clarification date, lecturer identity and meeting reference were not supplied. The assignment remains unchanged; fictional records must never be presented as real user evidence.
- **Execution:** reuse and check eight explicitly simulated records created on 2026-10-21, covering two professional administrators, two volunteers, two residents and two contractors. The [inventory](../research/answers/README.md) records 78 written answers, provenance limits, question-level coverage, counterexamples and the author-side check. No real interviews or recruitment attempts are recorded.
- **Handling:** consent, real session dates, interviewers and duration are not applicable to fiction. Existing DEC-07 safeguards still apply before any future real collection. Ownership remains in the backlog allocation.
- **Consequence:** DISC-01-02 has a simulated collection package for independent review; DISC-01-03 must distinguish scenario interpretations from public-source findings and actual observations. DEC-02/08/10 are not validated by simulation; LIM-01 and LIM-04 remain open. No new product decision, baseline or confirmed participant commitment results from this inventory.

### Confirmed Sprint 1 scope decision — DEC-11

- **Recorded:** 2026-10-10, from the team's update in the project conversation.
- **Clarification:** the evaluator confirmed that the walking skeleton is optional for Sprint 1.
- **Team decision:** do not develop the walking skeleton this sprint. Its absence is not a Sprint 1 completion blocker; it is not marked as implemented.
- **Change:** the earlier plan treated §7.1.2 item 10 as required in Sprint 1. The revised plan excludes that implementation and retains EN-02 as a candidate foundation for later implementation planning.
- **Scope:** other Sprint 1 discovery/design deliverables and later technical delivery requirements remain applicable. The original assignment is retained unchanged.
- **Traceability:** README, strategy, roadmap, backlog, Sprint 1/Sprint B plans, walking skeleton plan, team agreement and milestone conventions updated. Evaluator name, clarification date and meeting link were not supplied.

### Product scope proposals — DISC-03-03

- **Recorded:** 2026-10-19 by Afonso (BA/PO) for [#31](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/31). Team agreement is sought through the pull-request review (proposed reviewer: Martim); until then these are proposals, not stakeholder or lecturer approval, and not evidence for §5.7.
- **Evidence used:** secondary findings PS-01–PS-08 ([Public-source findings](../03-user-research.md#32-public-source-findings)) and competitor sources S01–S28 ([02 §5](../02-market-and-competitor-analysis.md#5-source-and-findings-register)). No primary research exists; DISC-01-03 is open, so personas and journeys keep their remaining hypotheses explicit.
- **DEC-01:** exclude IoT from the MVP. Reasons: not required by the assignment; no finding identifies a decision that sensor data would improve; a suite marketed in Portugal already bundles hardware (S04); capacity. Alternative considered: one simulated sensor scenario as Could — rejected because it would not test BMC's proposition.
- **DEC-08:** primary threshold of a ≥ 30% reduction in active administrative time on equivalent scripted tasks, computed as the median of participant medians against a pre-recorded answer key, with incomplete tasks recorded at the time cap and completion and critical-case guards. Alternatives: 20% (hard to separate from noise in a three-to-five-person sample) and 50% (likely to fail on factors outside the product). The rationale is team judgement, not a sourced benchmark; baseline limitations are disclosed in the vision.
- **DEC-10:** triage decision, approval, acceptance, booking confirmation, completion report, closure and impact confirmation defined as distinct steps, consistent with [07 §3](../07-technical-design.md#3-states-and-business-rules).
- **DEC-07 input:** the impact-confirmation review adds neutral count wording, no confirmation list for administrators and an open option on exact counts in very small buildings; the policy itself stays with DEC-07.
- **Affected documents:** [vision](../04-product-vision.md), [strategy](../building-maintenance-coordinator-strategy.md), [requirements](../requirements.md), [backlog §5](../05-product-backlog.md#5-wont-in-this-baseline--alternatives), [README](../../README.md). The IoT row of the former roadmap is carried by backlog §5 since the roadmap was removed in #16. US-04 criteria are unchanged; the counter wording is a refinement for the US-04 owner to consider.

### DEVOPS-01 proposals — CI/CD (Martim)

Recorded 2026-10-29 as proposals. Nothing below is applied to the repository or to GitHub settings.

- Build once and release by tag; promotion retags the tested image, no rebuild. Proposed, not configured.
- GHCR images with a cosign signature and SBOM. Proposed, not configured.
- CodeQL for SAST. Proposed, not configured.
### Domain and contract proposals — EN-01-02

- **Recorded:** 2026-10-19 by Afonso (BA/PO) for [#14](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/14). Proposed reviewer: Ricardo. These are design proposals, not accepted decisions and not stakeholder validation.
- **Inputs:** vision J1–J3 and §4.3; backlog US-01–US-11; the boundaries, asynchronous mechanism, identity and simulator proposed in EN-01-01 ([#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15); [`docs/EN-01-01-select-stack`](https://github.com/Phenriquerafael/LABDSOF_G9A/tree/docs/EN-01-01-select-stack) branch, not merged at the time of writing). If those ADRs change, the affected sections of the design must be reviewed again.
- **DEC-10:** issue and intervention state machines with allow-listed transitions, optimistic versions and idempotency keys ([07 §3](../07-technical-design.md#3-states-and-business-rules)). Proposed rules to validate: approving a contractor's counterproposal counts as that contractor's acceptance; a cancelled issue is not reopened (a new report is made instead); a confirmed booking is moved only by cancelling the intervention and creating a new one (manual booking confirmation applies only to a pending booking); contractors cannot cancel after acceptance through the platform.
- **DEC-04 input:** Dispatch takes only the user identity from the token, checks contractor assignment from its own data and fetches administrator context from Issue for each command, failing closed ([07 §4.3](../07-technical-design.md#43-how-dispatch-obtains-trustworthy-authorisation-context)). Alternatives (token claims, read-only database access, membership projection) and their trade-offs are recorded there; projection versus per-request calls stays open for EN-01-03.
- **DEC-06 input:** calendar/simulator contract outline with outcome classification, reconciliation by request ID and a `discrepancy` state ([07 §4.5](../07-technical-design.md#45-calendarsimulator-contract-outline)).
- **DEC-07 input:** an “Enforced in” column and new rows in the [access matrix](../09-security-privacy.md#2-proposed-access-matrix); threat T-11. Whether contractor accounts are scoped to an organisation stays open.
- **EN01-U7 (from #15):** starting retry, lease and retention values proposed in [07 §4.6](../07-technical-design.md#46-retry-timeout-and-lease-values-proposal), to calibrate in the EN01-U2 spike.
- **Reconciliation with the DISC-03-06 workflows ([BMC workflows](../workflows/bmc-workflows.md), merged in [#41](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/41) on 2026-10-25):** the workflow proposals differ from this design on five points. They are recorded as open DEC-10 items; this design keeps its rules until the team decides.
  - (a) Contractor cancellation: #41 lets the contractor cancel up to 24 h before; here only the administrator cancels after acceptance, and the contractor asks the administrator.
  - (b) Rejected work: #41 returns the issue to “to be scheduled”; here it is rework on the same intervention (`completion_reported → in_progress`).
  - (c) Resident cancellation request: #41 lets the resident request a cancellation that the administrator decides. Contract gap: a resident request operation in Issue that notifies the administrator; the cancellation itself stays administrator-only.
  - (d) Response deadline: #41 alerts the administrator when the contractor does not answer in time. Contract gap: a deadline on `sent` that raises an alert and leaves the intervention in `sent`; the value is to be agreed.
  - (e) Counterproposal: #41 has no counterproposal branch; here a counterproposal is a new version, and approving it counts as acceptance (US-07).
- **Affected documents:** [technical design](../07-technical-design.md), [contract annex](../07a-contract-examples.md), [requirements](../requirements.md), [security](../09-security-privacy.md), [README](../../README.md).

### DISC-01-03 synthesis proposals

**Recorded 2026-10-22 for [#21](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/21).** Proposed by Pedro (agent-assisted); independent/team approval pending. Allocation remains in the backlog README. This is research synthesis, not lecturer feedback or evidence of meeting the separate feedback obligation.

Evidence: [scenario interpretations SF-01 to SF-07](../03-user-research.md#33-scenario-synthesis-disc-01-03) and [public findings PS-01 to PS-08](../03-user-research.md#32-public-source-findings).

| Proposal / existing decision | Before and proposed outcome | Rationale / alternative considered | Affected artefacts |
|---|---|---|---|
| SP-01 / DEC-02 | Broad coordination opportunity → explicitly conditional on fragmentation/contact volume; retain professionals as primary | SF-01/04 show contrasting structured/low-volume scenarios. Reject extrapolating volunteer interest to business demand; do not commit new integrations. | [Problem sections 2/4/5/8](../01-problem-and-opportunity-report.md), [vision personas/J2](../04-product-vision.md), [US-02/06](../05-product-backlog.md#4-stories-and-criteria) |
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
