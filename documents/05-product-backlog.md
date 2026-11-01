# Product Backlog

**Status:** MoSCoW evaluation and release planning · updated 2026-11-01 · DISC-03-04

Corresponds to deliverable 5 in §7.1.2. This document defines the product backlog items. No remote issues, estimates, assignments or implementations are assumed.

## 1. MoSCoW evaluation

Priorities apply to the academic release. **Evidence-supported** means the rationale traces to the assignment, requirements or documented principal journey. **Team decision** identifies a product-scope choice rather than an assessment obligation; it does not assert that a meeting or vote occurred. Research simulations are scenario evidence, not validated demand.

Must = essential to the core journey or assessment; Should = valuable with a workable alternative; Could = optional enhancement; Won't = outside this release. Delivery timing is recorded in the [release plan](planning/release-plan.md).

| Stories / work | Priority | Basis | Rationale |
|---|---|---|---|
| US-01/02 — reporting and manual triage | Must | Evidence-supported | RF-01/02 and J1/J2: the journey needs durable reports, authorised review and human decisions. |
| US-03/14 — AI classification and fallback | Must | Evidence-supported | RF-03, NFR-03 and assignment §§5.6/7.2: initial meaningful AI with correction and non-AI continuity. |
| US-04 — shared summary and impact confirmation | Must | Evidence-supported | RF-04 and assignment §5.5: the selected ethical-participation mechanism, including privacy and opt-out. |
| US-06–09 — intervention through closure | Must | Evidence-supported | RF-06–09 and J2/J3: selection, approval, contractor response, booking and validated closure complete the business cycle. US-08 also covers assignment §6.5 integration. |
| US-10 — notifications | Must | Team decision | Retain proactive updates in the MVP (RF-10/P5). Status queries remain available if delivery fails; notifications are not the sole way to satisfy asynchronous processing. |
| US-15 — AI evaluation | Must | Evidence-supported | NFR-10 and assignment §§5.6.1/7.3: reproducible quality, latency, cost and baseline comparison. |
| EN-02/03/04 — foundations, quality and evaluation | Must | Evidence-supported | Assignment §§6–8 requires executable delivery, access controls, testing, operations and evaluation beyond functional stories. |
| US-05 — duplicate suggestions | Should | Team decision | Useful coordination support; manual review is a workaround and duplicate frequency/value is not established. |
| US-11 — basic cost | Should | Team decision | Adds historical information; missing cost must not block completion or closure. |
| US-12 — advanced ranking | Should | Team decision | Extra criteria may improve selection; US-06's simple eligibility/order remains sufficient. |
| US-13 — real calendar | Could | Team decision | A realistic simulator satisfies assignment §6.5; a real provider is an optional extension. |
| Payments, marketplace, photographs, native apps, IoT/prediction and other section 5 exclusions | Won't this release | Team decision | Keep the release focused on maintenance coordination and its evaluation. |

Evidence: [assignment](../LABDSOF-26-27-Assignment.md), [vision and journeys](04-product-vision.md), [requirements](requirements.md), [research findings](03-user-research.md) and [scope/decision record](planning/decisions-and-feedback.md). This evaluation retains the existing story priorities and acceptance scope.

## 2. Epics

| ID | Outcome / boundary | Items | Source |
|---|---|---|---|
| [EP-00](backlog/epics/EP-00-discovery-and-planning.md) | Justifiable discovery and planning | DISC-01–03 | §5.1–5.5, §5.7 |
| [EP-01](backlog/epics/EP-01-reporting-and-tracking.md) | Residents report and track issues with appropriate visibility | US-01/02/04/10 | J1, P1/P5 |
| [EP-02](backlog/epics/EP-02-assisted-triage.md) | Assisted triage and reviewed links | AI-01 (S1 assessment), PLAN-02 (preparation), US-03/05/14/15 | §5.6; J2, P2/P3/P7 |
| [EP-03](backlog/epics/EP-03-intervention-and-closure.md) | Intervention from request to closure | PLAN-03 (preparation), US-06–09/11–13 | J2–J3, P6 |
| [EP-04](backlog/epics/EP-04-engineering-and-quality.md) | Deliverable, secure, observable and evaluable system | EN-01–04 | §6–§8 |

## 3. Discovery and engineering

Detailed issue bodies and child tasks for [DISC-01](backlog/tasks/DISC-01-user-research.md), [DISC-02](backlog/tasks/DISC-02-market-comparison.md), [DISC-03](backlog/tasks/DISC-03-organisation-and-product-planning.md) and [EN-01](backlog/tasks/EN-01-technical-design.md) are indexed in the [draft package](backlog/README.md). Count delivery tasks once; do not add their parent/epic totals. AI-01 makes the Sprint 1 assessment explicit without completing US-03 implementation.

| ID / priority | Outcome and acceptance criteria | Dependencies | Horizon |
|---|---|---|---|
| DISC-01 / Must | Gather evidence: actual method/participants recorded; findings linked to P1–P7; explicit limitations and decisions. If access fails, document attempts and alternative evidence without claiming validation | Research plan, access/retention | S1 |
| DISC-02 / Must | Complete comparison: exact, dated sources; §5.2 criteria; include an informal alternative and a comparable maintenance/helpdesk product; conclusion separates evidence from inference | Selection of comparables | S1 |
| DISC-03 / Must | Ratify organisation and review scope/priorities: roles/board/DoR/DoD; DEC-01/03/09 and DEC-10 discussion; actual feedback recorded. Document at least one decision revised following lecturer feedback during the project | Team and stakeholder availability | S1, follow-up S2/S3 |
| [PLAN-01](backlog/tasks/PLAN-01-prepare-reporting-and-tracking-stories.md) / Must candidate | Prepare detailed US-01/02/04/10 drafts under EP-01; preserve IDs/priorities, link dependencies and identify technical refinements. Sandro Dias owns preparation; independent review/PR evidence completes the task, not the stories | Existing scope/requirements; working choices indexed in the [EP-01 reference](backlog/ep01-technical-refinement.md) | S1 drafting for S2/S3; no implementation commitment |
| [AI-01](backlog/tasks/AI-01-assess-ai-opportunity.md) / Must | Review the AI opportunity: user-need evidence/limitations, workflow, representative/adverse examples, evaluation criteria and dataset plan, baseline/fallback, human control and cost assumptions; DEC-05/08 updated. Design assessment only; no executed evaluation required | DISC-01 synthesis, reviewed vision; supports US-03 | S1 |
| [PLAN-02](backlog/README.md#ep-02-story-drafts-and-planning-allocation) / Must candidate | Prepare US-03/05/14/15 drafts, separate classification/fallback/evaluation, and record technical refinements; owner Sandro Dias. Drafting does not implement or validate AI | Existing scope/AI-01; confirm applicable EN-01/DEC-05/08 decisions listed in the stories before Ready | S1 drafting for S2/S3 |
| PLAN-03 / Must candidate | Prepare US-06–09/11–13 drafts and record decisions needed before development; owner Sandro Dias. Core delivery is separate from conditional extensions | Existing EP-03 scope; confirm applicable EN-01/DEC-06/07/10 decisions listed in the stories before Ready | S1 drafting for S2/S3 |
| EN-01 / Must | Consolidate design: context, components, model, API/events, data ownership, deployment and threats; ADRs record alternatives and actual decisions | DEC-04/07, vision | S1 |
| EN-02 / Must for later implementation foundations; optional in S1 | Walking skeleton: client→backend→persistence→query after restart; automated build, initial test and containers with reproducible instructions; linked evidence. Not selected for Sprint 1 (DEC-11) | EN-01 | S2 planning candidate; no Sprint 1 commitment |
| EN-03 / Must | Delivery/quality: independent components or accepted exception; CI/CD, authorisation/contract/journey tests, logs/health/metrics/correlation, queue/AI/calendar failures and backup/restore; evidence for applicable NFRs | EN-01/02; accompanies stories | S2, strengthened in S3 |
| EN-04 / Must | Final evaluation: consumes the AI-specific US-15 report once, alongside usability, accessibility, security, performance, dashboard, architecture evolution, limitations, roadmap and contributions; reproducible results and environment | Operational increment, DEC-08 | S3 |

### EP-03 contribution to Sprint 2

Complete the intervention steps of [main journey J2](04-product-vision.md#j2--triage-and-coordinate-main-journey) and the contractor's J3, supporting the [assignment's end-to-end Sprint 2 objective](../LABDSOF-26-27-Assignment.md#72-sprint-2-build-and-operate-the-vertical-slice).

| Story | Initial estimate | Horizon |
|---|---|---|
| US-06 — Select an eligible contractor | 5 SP | Required in S2 |
| US-07 — Approve terms and obtain a contractor response | 8 SP | Required in S2 |
| US-08 — Confirm booking and handle failures | 8 SP | Required in S2, using a realistic simulator |
| US-09 — Complete, validate, close and reopen | 8 SP | Required in S2 |
| US-11 — Record an optional basic cost | 3 SP | S3 if selected; may start in S2 if there is capacity |
| US-12 — Refine ranking | 5 SP | S3 if selected |
| US-13 — Add a real calendar provider | 8 SP | S3 if selected and provider access is available |

The required cycle totals **29 SP**; the optional extensions add **16 SP**. These are initial story estimates, not a sprint capacity commitment. The [index](backlog/README.md#ep-03-story-drafts-and-planning-allocation) records their assumptions. Count shared reporting, identity, jobs, persistence and delivery foundations once.

Implement US-06 → US-07 → US-08 → US-09 after the necessary US-01/02 reporting/manual-triage slice. Integrate response, booking and completion events with US-02/10 without making notification delivery a condition for saving business decisions. US-03/14 add the S2 AI/fallback path; EN-02/03 provide deployment, contracts, authentication/authorisation, tests, CI/CD and observability.

The four core stories cover EP-03's part of S2; no additional intervention story is needed for the current scope. Keep the failure/reconciliation cases in US-08, human approval and validation, and closure without cost in the S2 increment. Advanced ranking and a real provider are optional, while the simulator must exercise realistic external failures.

Working eligibility, state rules, ownership and retry limits are proposed in the stories, [journey examples](07a-contract-examples.md#1-principal-journey) and [calendar contract outline](07-technical-design.md#45-calendarsimulator-contract-outline). Remaining contract refinements must be reviewed before the affected stories become Ready. EN-02/03 supply the shared environment; US-13 still needs provider-specific mappings and test access for its optional live integration.
### EP-02 contribution to Sprint 2

The [main journey J2](04-product-vision.md#j2--triage-and-coordinate-main-journey) needs a first working AI capability and non-AI continuity in S2, as required by [assignment 7.2](../LABDSOF-26-27-Assignment.md#72-sprint-2-build-and-operate-the-vertical-slice).

| Work | Scope / initial estimate | Horizon |
|---|---|---|
| US-14 | Versioned rules, independent alerts and manual continuity; 5 SP | Required in S2; no provider dependency |
| US-03 | Asynchronous validated AI suggestions and human correction; 8 SP | Required in S2, integrated with US-01/02/14 |
| US-15 | Synthetic dataset/protocol and comparative report; 8 SP total | Prepare data in S2; complete the formal evaluation in S3 |
| US-05 | Reviewed, reversible duplicate links; 8 SP | Conditional S3 candidate; does not block the main journey |

The required classification/fallback implementation totals **13 SP**. Dataset preparation belongs to US-15's single 8-SP estimate, not another 8-SP Sprint 2 commitment. Its report is consumed once by EN-04. Select any US-05 pair evaluation explicitly and review the evaluation estimate when its scope is agreed.

The existing stories cover EP-02's part of S2; no additional AI story is needed for the currently defined journey. US-01/02 provide reporting, manual decisions and authorised status; US-06–09 provide contractor coordination, booking and closure; US-10 provides updates. Shared deployment, authentication/authorisation, persistence, contracts, jobs, tests, CI/CD and observability remain EN-02/03 work and must not be counted twice.

AI development proposes Gemini and a 0 EUR budget in the [AI assessment](06-responsible-ai-assessment.md#1-need-and-workflow). The model identifier and live access remain unverified; prompt/schema names are placeholders for specifications still to be completed and reviewed under AI-01/US-03/US-14 before Ready. Fake-provider preparation does not close these refinements. Initial implementation checks belong to US-03/14; US-15’s full comparison follows in S3.

### Sprint 2 journey coverage

Deliver J2, the [main journey](04-product-vision.md#j2--triage-and-coordinate-main-journey), from a resident's report through triage, contractor coordination and booking to completion/closure, with authorised status updates. This supports the [assignment's Sprint 2 objective and deliverables](../LABDSOF-26-27-Assignment.md#72-sprint-2-build-and-operate-the-vertical-slice).

| Journey step | Stories / work |
|---|---|
| Report and retrieve the receipt | US-01 |
| Review triage, including initial AI and non-AI continuity | US-02; US-03 and separate fallback to review under PLAN-02 |
| Publish a safe summary and confirm impact | US-04; the ethical-participation mechanism in assignment 5.5 |
| Select contractor, approve terms and receive a response | US-06/07, to review under PLAN-03 |
| Confirm a booking or expose pending/manual/failure status | US-08, to review under PLAN-03 |
| Report completion, validate, close and reopen | US-09, to review under PLAN-03 |
| Follow authorised status/history and receive updates | US-01/02/10; include response, booking and completion/closure events |

PLAN-01 covers the four EP-01 stories needed by this baseline: **5 + 8 + 5 + 8 = 26 SP**. Estimates and short reasons are in each story; the [index](backlog/README.md#ep-01-story-drafts-and-planning-allocation) explains their assumptions. This is not the whole Sprint 2 estimate.

EN-02/03 must also cover the client/backend foundations, authentication (mocked if agreed, with real authorisation checks), persistence, API contracts, two backend components or an approved alternative, asynchronous delivery, CI/CD, tests, logs/health/metrics and a demonstrated failure. AI and calendar integration come from PLAN-02/03; simulator support remains the initial calendar approach. Estimate shared engineering work separately, without counting story-level work twice.

US-05/11/12/13 remain conditional extensions. The full AI comparison belongs to Sprint 3; Sprint 2 still needs initial AI behaviour and a non-AI baseline or fallback. No extra EP-01 story is needed for the currently agreed scope. Use the concrete development details and representative examples for DoR review; confirm sprint capacity before selecting implementation work.

## 4. Stories and criteria

The criteria below apply the needs to each delivery. Detailed definitions are maintained in the [AI assessment](06-responsible-ai-assessment.md#4-provisional-criteria), [domain states](07-technical-design.md#3-states-and-business-rules), [access matrix](09-security-privacy.md#2-proposed-access-matrix) and [NFRs](requirements.md#non-functional-requirements--constraints). Changes to those definitions require a review of the affected stories.

PLAN-01 expands EP-01's existing stories into individual drafts linked below. This section retains the scope/priority overview; detailed scenarios live in the story files. The [EP-01 reference](backlog/ep01-technical-refinement.md) links the concrete working decisions and verification inputs. S2 delivery and S3 refinement refer to the same stories and are not duplicate estimates or work items.

### US-01 — Record and view a report · Must · EP-01

**Detailed draft:** [US-01](backlog/tasks/US-01-record-and-view-report.md). **Initial estimate:** 5 SP.

As a resident, I want to report a fault in my building so that management can track it.

- With valid membership, text and area, save the report/issue and return an ID and “received” status without waiting for AI.
- Invalid input produces an understandable error without creating a partial record.
- Another building cannot read or modify the report, even through direct API calls.
- Repeating the same request with the same key does not create two issues.
- Querying after a restart returns the persisted record.

**Source:** RF-01; NFR-01/02/05/07/09. **Dependencies:** EN-01/02, DEC-07. **Horizon:** S2, minimal slice in the skeleton.

### US-02 — Triage manually and track states · Must · EP-01

**Detailed draft:** [US-02](backlog/tasks/US-02-triage-manually-and-track-states.md). **Initial estimate:** 8 SP.

As an administrator, I want to review issues and their history to decide the next step.

- List only managed buildings, with pending category/urgency explicit.
- Manually changing category/urgency records the actor, timestamp and reason.
- Reject invalid transitions and concurrent changes based on an outdated version.
- Residents see authorised status and public history, without internal notes.

**Source:** RF-02; NFR-01/06. **Dependencies:** US-01, DEC-07/10. **Horizon:** S2.

### US-03 — Suggest category and urgency with AI · Must · EP-02

**Detailed draft:** [US-03](backlog/tasks/US-03-classify-with-ai.md). **Initial estimate:** 8 SP.

As an administrator, I want a category and urgency suggestion to reduce triage effort while retaining the final decision.

- Process persisted reports asynchronously; validate output and display rationale, uncertainty and source/model/prompt/schema/issue versions.
- Administrator confirmation/correction uses US-02; model text cannot authorise consequential actions.
- Preserve independent critical alerts and newer human decisions when results arrive late or disagree.
- Deduplicate redelivery/effects, bound retries/calls and expose sanitised latency/usage/failure evidence.
- Hand disabled/unavailable/invalid AI outcomes to US-14. Rules and provider-free continuity belong there; formal comparative evaluation belongs to US-15.

**Source:** RF-03; NFR-01/02/03/04/06/10. **Dependencies:** US-01/02, US-14, AI-01, applicable EN-01/DEC-05/08 refinements. **Horizon:** S2, refined/evaluated in S3.

### US-04 — Publish a shared issue and confirm impact · Must · EP-01

**Detailed draft:** [US-04](backlog/tasks/US-04-publish-shared-issue-and-confirm-impact.md). **Initial estimate:** 5 SP.

As a resident, I want to confirm that a shared problem affects me to provide useful information without repeating the report.

- Only a summary explicitly published by the administrator is visible to the same building.
- Confirming twice retains one contribution; withdrawing removes it.
- Identity and private text are not shown to other residents; another building cannot confirm.
- The counter does not automatically change urgency; optional subscriptions can be disabled.
- Creating a separate report remains possible.

**Source:** RF-04 / §5.5; NFR-01/02/07. **Dependencies:** US-01/02, DEC-07. **Horizon:** S2.

### US-05 — Review duplicate suggestions · Should · EP-02

**Detailed draft:** [US-05](backlog/tasks/US-05-review-duplicate-suggestions.md). **Initial estimate:** 8 SP. Selection and evaluation remain conditional; if selected, US-15 supplies its pair-evaluation report without duplicate effort.

As an administrator, I want to identify reports of the same fault to coordinate a single response.

- Candidates respect building, area and time window; they explain why they were suggested.
- Linking requires confirmation, preserves originals and can be undone with an audit trail.
- Do not expose private text in resident searches or mix buildings.
- Measure precision/recall on annotated pairs; choose rules or embeddings after evaluation.

**Source:** RF-05; NFR-01/10. **Dependencies:** US-01/02, P2, DEC-05. **Horizon:** S3 candidate; S2 only if selected without displacing the core journey.

### US-06 — Select a contractor · Must · EP-03

**Detailed draft:** [US-06](backlog/tasks/US-06-select-a-contractor.md). **Initial estimate:** 5 SP.

As an administrator, I want to select an eligible contractor to prepare the intervention.

- The synthetic catalogue provides specialisation and coverage; filters eliminate incompatible candidates.
- Simple, deterministic ordering explains available criteria; unknown data is not invented.
- The administrator can change the selection; when none are eligible, they see a pending state and a manual coordination option.
- Selection does not send a request or confirm actual availability.

**Source:** RF-06; NFR-01. **Dependencies:** US-02, DEC-10. **Horizon:** S2.

### US-07 — Approve a request and obtain a response · Must · EP-03

**Detailed draft:** [US-07](backlog/tasks/US-07-approve-request-and-obtain-response.md). **Initial estimate:** 8 SP.

As an administrator, I want to authorise a request and know the contractor's response to coordinate the intervention.

- Only the building administrator can approve; record the proposal, terms and version.
- Repeated approval does not send two requests.
- Only the assigned contractor can accept, decline or counterpropose; a counterproposal requires new approval.
- Request approval does not show the booking as confirmed.
- Changed terms invalidate approval of the previous version. Under the current DEC-10 proposal, approving contractor-authored terms also records their acceptance; use this rule for initial development.

**Source:** RF-07; NFR-01/04. **Dependencies:** US-06, DEC-10. **Horizon:** S2.

### US-08 — Confirm calendar booking and handle failures · Must · EP-03

**Detailed draft:** [US-08](backlog/tasks/US-08-confirm-booking-and-handle-failures.md). **Initial estimate:** 8 SP.

As an administrator, I want to know whether the booking was actually recorded to avoid communicating a false date.

- Only an approved and accepted request is sent to the calendar/simulator.
- A valid response stores the external reference and confirms; timeout/invalid data leaves an explicit pending state.
- A retry/duplicate event does not create a second booking; uncertain external outcomes are reconciled.
- Manual confirmation requires an administrator, date and reason/source; do not present it as synchronised.
- Retrying after manual action does not create a duplicate booking. Cancellation and late responses are reconciled, and a missing external booking is shown as a discrepancy.

**Source:** RF-08; NFR-04/11. **Dependencies:** US-07, DEC-06/10. **Horizon:** S2.

### US-09 — Complete, close and reopen · Must · EP-03

**Detailed draft:** [US-09](backlog/tasks/US-09-complete-close-and-reopen.md). **Initial estimate:** 8 SP.

As an administrator, I want to verify completion to close the issue with a history.

- The assigned contractor reports completion; the issue becomes “awaiting validation”.
- The administrator closes it or returns it for execution with a reason; they can also close it manually with justification.
- Reopening records a reason and preserves history; invalid transitions are rejected. Under the current DEC-10 proposal, a resolved issue returns to triage with a new intervention, while cancelled issues cannot be reopened.
- Unknown cost does not prevent closure; no financial conclusion is invented.

**Source:** RF-09; NFR-01/09. **Dependencies:** US-02/07/08, DEC-10. **Horizon:** S2, refined in S3.

### US-10 — Notify changes · Must · EP-01

**Detailed draft:** [US-10](backlog/tasks/US-10-notify-changes.md). **Initial estimate:** 8 SP.

As a participant, I want to receive authorised updates to track the issue.

- One proposed in-app channel; state events generate notifications with unique IDs. EN-01-01 proposes email as a second channel on 2026-10-27 ([ADR-007](adr/ADR-007-notification-service.md), DEC-06, pending team review); these criteria are unchanged until that is agreed.
- Recipients and content respect visibility and optional preferences.
- Retries do not duplicate notifications; failure is observable without rolling back issue state.
- Status queries work even if notifications fail.

**Source:** RF-10; NFR-01/04/06. **Dependencies:** US-02/04/07/08/09, DEC-06. **Horizon:** S2.

### US-11 — Record a basic cost · Should · EP-03

**Detailed draft:** [US-11](backlog/tasks/US-11-record-a-basic-cost.md). **Initial estimate:** 3 SP. Select or defer explicitly based on evidence and capacity.

As an administrator, I want to record known costs to maintain intervention history.

- Non-negative amount, currency and source; the field may be empty.
- The contractor can propose the cost of their work; administrator confirmation/correction is audited.
- Residents do not receive costs/private data by default.
- Does not include payments, aggregations or AI summaries.

**Source:** RF-11; NFR-01/02. **Dependencies:** US-09, DEC-07/10. **Horizon:** S3 if selected; may start in S2 if there is capacity.

### US-12 — Refine ranking · Should · EP-03

**Detailed draft:** [US-12](backlog/tasks/US-12-refine-ranking.md). **Initial estimate:** 5 SP. Select or defer explicitly based on evidence and capacity.

As an administrator, I want to compare additional criteria to select among eligible contractors.

- Documented weights; justify the source/freshness of price, distance and availability.
- Missing data does not mean zero price or confirmed availability.
- Tests demonstrate ordering and tie-breaking; approval remains human.

**Source:** P6 / RF-06. **Dependencies:** US-06, evidence of usefulness and data. **Horizon:** S3 if capacity allows.

### US-13 — Integrate a real calendar · Could · EP-03

**Detailed draft:** [US-13](backlog/tasks/US-13-integrate-a-real-calendar.md). **Initial estimate:** 8 SP. Select or defer explicitly based on evidence and capacity.

As an administrator, I want to synchronise with the calendar used in operations.

- The Google Calendar adapter is checked against the simulator contract, including explicit provider limitations; no simulator or live checks are claimed yet.
- Credentials stay outside Git; permissions and revocation are documented.
- Test availability and failure without compromising reproducible evaluation.

**Source:** RF-08. **Dependencies:** US-08, DEC-06, provider access. **Horizon:** S3 if selected and capacity allows.

*Note (2026-11-01, EN-01-01):* [ADR-006](adr/ADR-006-calendar-simulator.md) now proposes a Google Calendar adapter behind `CalendarPort` for the live system, with the simulator kept for tests and failure demos (pending team review). The priority above is unchanged; revisiting it is for the backlog owners.

### US-14 — Continue triage without AI · Must · EP-02

**Detailed draft:** [US-14](backlog/tasks/US-14-continue-triage-without-ai.md). **Initial estimate:** 5 SP.

As an administrator, I want independent rules and manual review when AI cannot provide a usable suggestion so that issues remain actionable.

- Implement versioned deterministic rules and independent critical-signal alerts without a provider/account or successful AI call.
- For disabled AI, timeout, provider/schema errors or exhausted budget/attempts, show degraded/manual status and preserve reporting/query/US-02 manual triage.
- If rules/worker processing itself fails, keep saved reports/manual action available; do not pretend new rules were computed.
- Replays do not duplicate alerts/effects; recovery or late AI cannot overwrite newer human decisions or remove alerts.
- Integrate with shared job/idempotency infrastructure rather than reimplementing the same mechanisms twice.

**Source:** RF-02/03; NFR-01/02/03/04/06; §5.6.2/§6.8. **Dependencies:** US-01/02 and applicable EN-01/rules contracts; no dependency on US-03 or provider selection. **Horizon:** S2, hardened in S3.

### US-15 — Evaluate AI-assisted triage against the non-AI baseline · Must · EP-02

**Detailed draft:** [US-15](backlog/tasks/US-15-evaluate-ai-against-baseline.md). **Initial estimate:** 8 SP.

As a product owner, I want reproducible comparison evidence so that AI usefulness, operating cost and limitations can be assessed.

- Implement a versioned synthetic dataset/protocol, annotation/disagreement review and development/held-out separation without leakage.
- Freeze quality/value/latency/cost criteria before formal evaluation; compare baseline, AI and combined workflow on documented inputs with failures retained in denominators.
- Report per-class metrics, critical false positives/negatives, cost/calls, latency, adverse cases, limitations and reproducible versions.
- Controlled-task value evidence follows the reviewed vision protocol; simulated interview times are not an empirical baseline.
- Include duplicate-pair evaluation only if US-05 is selected. EN-04 consumes this AI-specific report/run once; broader system evaluation stays there.

**Source:** RF-03, conditional RF-05; NFR-03/10; §5.6.1/§7.3.2. **Dependencies:** AI-01/DEC-05/08 for protocol; US-03/14 for comparative completion, not initial dataset preparation. **Horizon:** S2 preparation/initial run; S3 formal results.

## 5. Won't in this baseline / alternatives

Photos and visual analysis, cost charts/summaries, payments, marketplace, native apps, automatic approval and subscriptions. Report photos without visual analysis are a design candidate recorded in the [decision register](planning/decisions-and-feedback.md#stack-revision--en-01-01-2026-10-27), pending a DEC entry and the team review; no story exists, and this baseline still excludes them. IoT, monitoring and prediction are **excluded from the MVP** (DEC-01, BA/PO proposal of 2026-10-19 in [vision §4.2](04-product-vision.md#42-iot-decision-dec-01), team agreement pending); reopening requires a scope review.

## 6. Release plan

See the [release plan](planning/release-plan.md) for MVP, MVI and backlog scope, estimates and delivery order. GitHub remains the source of live issue status and assignments.
