# 4. Product Vision

**Status:** proposal v0.4 (DISC-03-03) · **Sprint:** 1 · **Reviewed:** 2026-10-19

This is the **source of the proposed functional scope**; changes must be reflected in the [backlog](05-product-backlog.md), [requirements](requirements.md) and [decisions](planning/decisions-and-feedback.md).

**Evidence basis (2026-10-22; synthesis pending review):** [PS-01–PS-08](03-user-research.md#32-public-source-findings) provide public context, [SF-01–SF-07](03-user-research.md#33-scenario-synthesis-disc-01-03) interpret fictional scenarios, and [S01–S28](02-market-and-competitor-analysis.md#5-source-and-findings-register) identify competitor sources (supplier claims unless marked otherwise). This competitor namespace is separate from the research register's S1–S9. Personas, journeys and targets remain proposals; [SP-01–SP-05](planning/decisions-and-feedback.md#disc-01-03-synthesis-proposals) explain their qualification and retained scope. Choices marked **[BA/PO proposal]** originate in the [2026-10-19 scope proposals](planning/decisions-and-feedback.md#product-scope-proposals--disc-03-03) and await team agreement.

## 1. Vision and value proposition

> Help residential communities recover from everyday faults through traceable coordination, less administrative effort and information appropriate to each participant.

**Value proposition [Hypothesis].** For condominium administrators who receive fault reports through scattered channels, BMC turns each report into a reviewed, traceable intervention: a triage suggestion the administrator confirms or corrects, an approved request to a chosen contractor, a booking shown as confirmed only when it is, and a validated closure with history. Residents see the status and expected date without repeated contact; contractors see only what the assigned request needs.

| Compared with | What BMC proposes to do differently | Evidence status |
|---|---|---|
| Informal channels (calls, messages, groups, spreadsheets) | Structured status, ownership and history for each issue | Hypothesis; current tools are interview question Q6. PS-03 and PS-05 show responsibility, elapsed time and record-keeping as recurring concerns in UK social-housing casework, not in the target segment |
| Portuguese condominium suites (SolidSoft GC, Gecond, Unitify) | Focus on coordination with external contractors, keeping approval, acceptance, booking confirmation and closure as separate recorded steps (§4.3) | Suites claim reporting (S01, S02, S09). Unitify claims AI classification, urgency scoring and automatic assignment (S05); SolidSoft GC claims AI incident descriptions from photographs and quote suggestions (S17), not triage or assignment. The external acceptance → booking chain is **unconfirmed, not absent** in the sources opened ([02 §6](02-market-and-competitor-analysis.md#6-differentiation-hypothesis)) |
| Comparable maintenance products (Fixflo, Infraspeak) | Small residential buildings in Portugal | Fixflo Block targets the UK with a 50-property minimum (S11, S22); Infraspeak's listed sectors exclude residential condominiums (S13). Supplier claims |
| Service marketplace (Zaask) | Coordination and history after a contractor is chosen, not contractor discovery | Zaask covers quotes and selection (S15); tracking after hiring is unconfirmed |

**What BMC does not claim:** exclusivity in reporting, AI triage, human approval of AI output, traceability or scheduling. Competitors already claim AI urgency scoring (S05), human approval of AI decisions (S20), reporter-side editing of AI summaries (S24) and AI incident descriptions (S17). The proposition stands or falls on the measured reduction in administrative effort (§5.1); simplicity or focus alone is not a defensible advantage.

## 2. Provisional personas

No participant supports these personas yet. "Secondary support" lists only what the public sources make plausible; "To validate" lists the research questions ([03 §1](03-user-research.md#1-research-objectives)) and assumptions ([01 §7](01-problem-and-opportunity-report.md#7-assumptions-and-risks)) that must confirm or refute each one.

| Persona | Context [Hypothesis] | Expected benefit | Difficulty / condition for trust | Secondary support | To validate |
|---|---|---|---|---|---|
| Marta, professional administrator (proposed primary segment, DEC-02) | Manages several buildings | Less active effort per issue; control over decisions and costs | Scattered contacts; needs to understand suggestions and approve before committing resources | PS-03 (responsibility, time and record-keeping as complaint themes); PS-07 and PS-08 (scheduling, follow-up and approval visibility framed by a vendor as coordinator workload) | Q1, Q2, Q5–Q7; P1, P3, P4, P7 |
| Rui, resident (owner or tenant) | Uses a mobile phone and reports occasionally | Report once and know the status and expected date | Lack of feedback; concern about exposing location and private details | PS-01 (expected timing and escalation are visible parts of repair guidance); PS-04 (communication and trust in casework) | Q8; P5; resident survey and question 6 on identification |
| Carlos, contractor | Small maintenance company | Complete requests and an organised schedule, avoiding wasted trips | Vague descriptions, late changes and uncertainty about payment terms | PS-08 (missing request information treated as an operational problem by a vendor); marketplace contractors pay to bid (S16) | Q9; P6 |

**Secondary persona — volunteer administrator** of a single building: simpler coordination with limited time. A single-condominium plan already exists (S17, Home Edition at €200/year excluding VAT), so this segment is served by at least one suite. Volunteers are relevant participants but cannot by themselves validate adoption by companies (DEC-02).

Timely payment is a need to investigate, not a promise of payment functionality. Usability targets belong in the [NFRs](requirements.md#non-functional-requirements--constraints). Building membership and authority to approve expenses are different concepts; residents may be tenants.

## 3. Journeys and responsibilities

Step names in bold are defined in §4.3. Each journey lists its secondary support and the hypotheses it still depends on.

### J1 — Report and track

1. An authenticated resident selects a building they belong to, an area and a text description.
2. The system persists the report and acknowledges receipt without waiting for AI.
3. When implemented, suggestions of similar issues show only authorised information; linking is not automatic and does not delete the report.
4. The resident tracks the status and expected date, and can make an **impact confirmation** (“This affects me too”) on published shared issues (§6).
5. They receive updates through the defined channel and manage their subscription.

*Support:* PS-01, PS-04. *Remaining hypotheses:* residents will report through a web page or app (P5); reporting frequency and preferred channels (Q8).

### J2 — Triage and coordinate (main journey)

1. The administrator sees the queue for buildings they manage, including unclassified items or items using fallback.
2. They review the suggested category, urgency and rationale, then make a **triage decision**: confirm or correct, with the decision recorded.
3. They review duplicate suggestions, if available, and publish a summary without private data when appropriate.
4. They select an eligible contractor from a small catalogue; rule-based ranking explains the available criteria.
5. They give **approval** to the proposal and send the request. If no contractor is eligible, the issue remains visibly pending manual action.
6. After the contractor's **acceptance**, they track calendar synchronisation. Without a **booking confirmation**, the status remains “scheduling pending”; they can confirm manually and record the source.
7. After the contractor's **completion report**, they review it, record the cost when known and perform **closure**. They can reopen with a reason.

Steps 1–5 are the window measured by the primary success criterion (§5.1).

*Support:* PS-03, PS-05, PS-07, PS-08. *Remaining hypotheses:* administrators spend significant time coordinating (P1); urgency is poorly triaged today (P3); explainable, approvable suggestions are trusted (P7); how contractors are chosen and approved (Q5).

### J3 — Respond and carry out the work

1. The contractor sees only assigned requests and necessary data.
2. They give **acceptance**, decline or propose another date. Changes to terms return to the administrator for a new **approval**.
3. They submit a **completion report** with the cost, if known. This does not close the issue.

*Support:* PS-08; suites already offer technician apps (S03, S10). *Remaining hypotheses:* contractors will respond through the platform (P6); what a request must contain and how dates are confirmed (Q9).

### J4 — Analyse costs (post-MVP)

The administrator views aggregates and trends; figures are calculated from records. AI summaries depend on a demonstrated need and a separate evaluation.

## 4. MVP boundary

### 4.1 Smallest credible experiment

In one building community with synthetic data, a resident's text report becomes an administrator-confirmed triage (AI suggestion, independent rules and manual fallback), a contractor selected by rules from a small catalogue, an approved request, a contractor response, a confirmed — or explicitly pending — booking through the calendar simulator and a validated closure, with states, history, one notification channel and authorisation enforced in the backend. Alongside this chain, the administrator can publish a shared summary on which other residents of the same building make impact confirmations (§6).

The experiment tests one claim: **the coordination chain reduces the administrator's active effort compared with the current process** (§5.1). The shared summary and impact confirmation are also mandatory, because the assignment requires an engagement mechanism (§5.5), but they are not part of the measured claim. The baseline column below lists exactly these elements; everything else is conditional or post-MVP. This is the team's answer to the Sprint 1 investor question (assignment §7.1.3), pending review.

| Baseline (Must) | Conditional candidates (§4.4) | Outside the MVP / post-MVP |
|---|---|---|
| Text reports, states and history | Duplicate suggestions (rules first, embeddings after evaluation) | Photo upload/analysis |
| Assisted classification, review, rules and fallback | Price/distance ranking if reliable data is available | Cost charts and summaries |
| Impact confirmation on shared issues | Real calendar instead of the simulator | Marketplace, payments, condominium fees and assemblies |
| Catalogue, rule-based selection and approval | Additional notification channel | IoT, monitoring and fault prediction (§4.2) |
| Contractor response and calendar/simulator booking confirmation | Basic cost recording | Automatic expense approval |
| Notifications through one channel, closure and enforced authorisation | | Native apps and subscription management |

Basic cost may remain “not provided” and never blocks closure. The [backlog](05-product-backlog.md) distinguishes Must/Should/Could/Won't; priorities await the MoSCoW session (DISC-03-04).

### 4.2 IoT decision (DEC-01)

**[BA/PO proposal]** **IoT is excluded from the MVP; the academic release is coordination-only.** Reasons:

1. The assignment asks for coordination of information, decisions, people or resources (§3); sensing is not a common requirement.
2. No [research finding](03-user-research.md#3-findings) identifies a decision that sensor data would improve.
3. A suite marketed in Portugal already bundles meters and building hardware (S04), so an IoT feature would not test BMC's own proposition.
4. A device simulator and ingestion path would compete with the Must cycle for three-sprint capacity.

Reopen only through a scope review if research identifies a concrete decision that needs sensor data. In that case a sensor event would enter as a report through J1 and follow the same triage and approval; it would not bypass them. The IoT tools in `NOTAS.md` remain background notes, not backlog items.

### 4.3 Distinct steps (DEC-10)

The workflow keeps these steps separate in states, history and UI wording. They match the issue and intervention states in [07 §3](07-technical-design.md#3-states-and-business-rules). Validation with administrators and contractors is still pending (Q5, Q9; administrator question 8).

| Step | Who | What it records | What it does not mean | Story |
|---|---|---|---|---|
| Triage decision | Administrator | Category and urgency confirmed or corrected, with actor, time and reason | Not a dispatch; an AI suggestion stays labelled as unverified until then | US-02, US-03 |
| Approval | Administrator of the building | Authorises one version of the request (contractor, scope, terms) to be sent | The contractor has not agreed and no date exists | US-07 |
| Acceptance | Assigned contractor | Agrees to the approved version; a counterproposal creates a new version that needs new approval | No booking is confirmed yet | US-07 |
| Booking confirmation | Calendar/simulator, or administrator manually | External reference stored, or manual confirmation with date and source | Without it, the status stays “scheduling pending”; manual confirmation is never shown as synchronised | US-08 |
| Completion report | Assigned contractor | Work reported done, with cost if known; the issue moves to “awaiting validation” | The issue is not closed | US-09 |
| Closure | Administrator | Validates completion and closes, returns the work with a reason, or closes manually with justification; reopening needs a reason | Not automatic after a completion report; unknown cost does not block it | US-09 |
| Impact confirmation | Resident of the same building | “This affects me too” on a published summary (§6) | Unrelated to booking confirmation; does not change urgency | US-04 |

Documents and UI use the qualified terms “booking confirmation” and “impact confirmation”, never “confirmation” alone.

### 4.4 Conditions for optional features

| Candidate | Enters the release only if | Backlog |
|---|---|---|
| Duplicate suggestions | Research shows duplicates are frequent enough to matter (P2, Q3) and capacity remains after the Must cycle; rules are evaluated before embeddings (DEC-05) | US-05, Should |
| Basic cost recording | Kept optional; never blocks closure; residents get no access by default | US-11, Should |
| Price/distance ranking | Price, distance and availability data have a documented source and freshness; missing data never means zero price or confirmed availability | US-12, Should |
| Real calendar provider | The simulator contract and failure scenarios are demonstrated first; credentials stay outside Git | US-13, Could |
| Additional notification channel | The in-app channel works end to end and the channel detail in DEC-06 is resolved | Not yet a story |

## 5. Metrics and success

### 5.1 Primary success criterion (DEC-08)

**[BA/PO proposal]** The primary metric is **active administrative time**.

**Definition.** The time an administrator spends actively working to take a new fault report from receipt to an approved request sent to an eligible contractor (J2 steps 1–5): reading, classifying, checking related reports, choosing a contractor and sending the request. Waiting time, such as waiting for a contractor's reply, is excluded and measured separately (§5.2).

**Answer key (recorded before any test session).** For each scripted scenario, the protocol records the expected category and urgency, whether the scenario is critical, the eligible contractor(s), the minimum content of a correct request and a time cap (proposal: 15 minutes). The key is versioned with the protocol and is not changed after the first session.

**Task outcome (same rules in both conditions).**

- *Observation:* one participant performing one scripted scenario in one condition. Practice tasks and the AI-disabled BMC run are excluded from the threshold and reported separately.
- *Complete:* within the time cap and without facilitator help beyond the scripted instructions, a request matching the answer key is sent to an eligible contractor with the expected urgency or a higher one.
- *Incomplete:* the cap is reached, the request is wrong or sent to an ineligible contractor, the urgency is lower than the key, or the facilitator had to help. An incomplete task is **recorded at the time cap** in the timing comparison; it is never dropped.

**Calculation.**

1. For each participant and condition, take the median time of that participant's observations (the participant median).
2. For each condition, take the median of the participant medians: *M*<sub>current</sub> and *M*<sub>BMC</sub>. Each participant therefore weighs the same, whatever the number of scenarios.
3. reduction = (*M*<sub>current</sub> − *M*<sub>BMC</sub>) / *M*<sub>current</sub>.

**Success threshold.** The criterion is met only if all three conditions hold:

- reduction ≥ 0.30;
- *completion guard:* the BMC completion rate (complete observations ÷ all observations, pooled across participants) is not lower than the current-process completion rate;
- *critical guard:* every BMC observation of a critical scenario ends with the issue triaged at the key's urgency or higher, consistent with the critical-set criterion in the [AI assessment](06-responsible-ai-assessment.md#4-provisional-criteria). A single violation fails the criterion.

*Illustrative example, not data:* participant medians of 10, 8 and 12 minutes (current) and 6, 7 and 5 minutes (BMC) give *M*<sub>current</sub> = 10, *M*<sub>BMC</sub> = 6 and a reduction of 0.40, which passes if both guards hold. Pooled medians and per-participant reductions are reported for transparency but do not decide the result.

**Measurement conditions** (to freeze before the evaluation in EN-04):

| Element | Proposal |
|---|---|
| Participants | Target: at least three administrators; professional administrators preferred, with volunteers reported separately. If no administrator is available, team members acting as administrators make a pilot run that is reported as such, not as evidence of user benefit |
| Tasks | At least three scripted scenarios with synthetic data: an ordinary fault, an urgent fault with critical signals and two reports of the same fault needing one intervention. Equivalent variants in each condition to limit recall |
| Current-process condition | The participant's usual tools (phone, messages, email or spreadsheet) with simulated contacts; if not reproducible, a documented paper or spreadsheet equivalent |
| BMC condition | The Sprint 2/3 increment with AI enabled, plus a rules/manual run with AI disabled to separate the AI contribution |
| Design | Within-subject, counterbalanced order, one practice task per condition, observer timing with the start and stop events defined above; contractor replies simulated instantly |
| Reporting | Raw time and outcome per observation, participant medians, the calculation above, completion rates, errors and assistance needed; answer-key version, sample, environment and limitations. No generalisation to production |

**Rationale for 30% (team judgement, not a sourced benchmark).** With three to five participants, order, learning and individual differences can produce sizeable differences in timed tasks; a threshold well above small differences makes a positive result less likely to come from noise alone, although it does not make it statistically significant. Adopting a new tool has training and migration costs (P4), so a marginal reduction is unlikely to justify leaving free informal channels or a suite already in use. A 20% threshold was rejected as hard to distinguish from noise in this sample; 50% was rejected as likely to fail on factors outside the product, such as scenario design and participant familiarity. The threshold is fixed before measurement; any change after observing results must be documented and the evaluation repeated.

**Baseline limitations.**

- No measured baseline exists. Interview time estimates (administrator questions 3 and 11), once collected, are self-reports, not measurements.
- The current-process condition is simulated; real effort includes interruptions, unavailable contractors and follow-up over several days that the test does not capture.
- Synthetic scenarios, a small convenience sample, facilitation by the team that built BMC and novelty effects all bias the comparison.
- A positive result shows an effect in controlled tasks only; it does not show shorter resolution times, less damage or adoption.

If the threshold is not met, record the result, analyse where time was spent and review scope under §7; do not redefine the metric afterwards.

### 5.2 Secondary and diagnostic metrics

| Metric | How to measure | Proposed criterion / limitation |
|---|---|---|
| Time until request sent | Receipt to dispatch to the contractor | Separate waiting from active time |
| Time until acceptance | Dispatch to contractor response | Do not confuse dispatch with confirmation |
| Time until resolution | Receipt to closure | Exploratory; simulation does not prove real impact |
| Triage quality | Model, rules and combined system | Protocol and targets in the [AI Assessment](06-responsible-ai-assessment.md) |
| Duplicate detection quality | Precision and recall on labelled pairs, if implemented | Criteria centralised in the [AI Assessment](06-responsible-ai-assessment.md#4-provisional-criteria) |
| Acceptance without editing | Percentage and correctness audit | Does not independently equate to trust |
| Impact-confirmation use | Confirmations, withdrawals and separate repeat reports on published issues, in prototype tests | Diagnostic for §6; no target until research exists |
| Continuity | AI disabled and calendar unavailable | Reporting and triage continue; pending/manual scheduling is explicit |

Interviews provide estimates, not instrumented measurements. In tests, vary the order of methods where possible and disclose the sample and limitations.

## 6. Ethical participation and visibility

**Mechanism:** “This affects me too” (impact confirmation), on shared issue summaries published by the administrator for the same building. Proposal awaiting validation in DEC-07; implemented by US-04. Reviewed on 2026-10-19 against the five questions in assignment §5.5:

| §5.5 question | Design | Residual risk and check |
|---|---|---|
| 1. Behaviour encouraged | Confirming impact on a known, published problem instead of filing another report or calling the administrator | — |
| 2. Benefit | Residents: less effort and optional updates. Administrator: one issue with an indication of extent. Community: fewer repeated contacts | Hypothesis (P2, P5); PS-04 supports communication as a trust factor, not this mechanism. Observe use in prototype tests (§5.2) |
| 3. Misuse prevention | One confirmation per user and issue; members of the same building only; rate limits; only the administrator publishes summaries, so residents create no public content; no free text in a confirmation; the counter never changes urgency or priority, so inflating it cannot move an issue up the queue | Coordinated confirmations can still exaggerate apparent extent, so the administrator treats the count as context only. Limits and authorisation need backend tests (NFR-01) |
| 4. Exclusion, exposure, discouragement | *Exclusion:* residents without digital access cannot confirm, so the count understates impact; it is labelled “confirmations in BMC”, never “affected residents”. *Exposure:* identities are never shown to other residents; summaries contain no private text, unit or names; the administrator sees the count, not a list ([access matrix](09-security-privacy.md#2-proposed-access-matrix)); the link between user and confirmation is kept only for one-per-user, withdrawal and subscription. *Discouragement:* no rankings, badges, streaks, penalties or reminders to confirm | Assisted access remains an open question ([requirements](requirements.md#open-decisions)). In a very small building a low count may let neighbours infer who confirmed; whether to show residents an exact count is an open DEC-07 option |
| 5. Control and opt-out | Withdraw at any time, which removes the contribution; optional updates can be disabled separately; a separate report is always possible; confirming is never required to see the status of one's own reports | Retention of confirmations after closure is decided in DEC-07 |

The mechanism must respect the separation between the private report and the published summary.

## 7. Risks

| Risk | Proposed response |
|---|---|
| Segment shows no interest | Investigate specific episodes, current tools and willingness to test |
| No primary research before scope is frozen | Personas and scope stay marked as hypotheses; DISC-01 findings can change the baseline and are recorded as decisions |
| Competitors already claim AI classification, urgency scoring and assignment (S05), other AI assistance such as incident descriptions (S17) and human approval of AI decisions (S20) | Claim no exclusivity; justify BMC by the measured effort reduction (§5.1) |
| Baseline cannot be measured in real conditions | Simulated equivalent tasks with frozen protocol and disclosed limitations (§5.1) |
| AI adds no value | Compare the baseline and review the task; retain the required meaningful workflow |
| Critical urgency goes unrecognised | Independent rules and review; no guarantee of perfect detection |
| Impact count read as severity or exposes participants | Count never changes urgency; neutral wording; identities hidden (§6) |
| Excessive scope | Complete cycle first; extras only under the conditions in §4.4 |
| A competitor covers the workflow | Review value against evidence; no automatic repositioning towards costs |
| External failure | Visible pending state, limited retries, idempotency and audited manual action |

DEC-01 to DEC-11 are in the [register](planning/decisions-and-feedback.md). These proposals are not yet stakeholder-approved decisions.

## 8. Business model

**[Hypothesis]** SaaS per building or unit, with terms suitable for property management companies. Buyer, willingness to pay and adoption costs need validation in DEC-02 and the [administrator interview guide](templates/interviews/administrador.md). Competitor price points are references, not a BMC price: SolidSoft GC from €200/year for one condominium to €1,990/year (S17), Unitify €0.50–€1.50 per apartment per month (S19), and Fixflo Block £75/month plus a quoted price with a 50-property minimum (S22). Contractor commissions/partnerships are only a future hypothesis and do not expand the MVP.

## 9. Expected community benefit

The aim is to make it easier to respond to water, lighting and lift faults, reduce coordination effort and provide visibility of progress. Shorter delays may reduce impact and damage, but this benefit still needs evidence. Transparency respects permissions; it does not mean publishing costs or private details to the whole building.

## 10. Change record

| Version | Change | Basis |
|---|---|---|
| v0.4, 2026-10-19 (DISC-03-03) | Value proposition compared with each alternative and stated without exclusivity claims; each AI capability attributed to its own source | 02 §2–§6; S05, S17, S20, S24 |
| | Personas and J1–J3 linked to secondary findings and to the hypotheses still open | 03 §3.2 (PS-01–PS-08); 01 §7 |
| | Smallest credible experiment stated; IoT excluded from the MVP; conditions for optional features | DEC-01 [BA/PO proposal]; assignment §3, §7.1.3 |
| | Approval, acceptance, booking confirmation, completion report, closure and impact confirmation defined as distinct steps | DEC-10; 07 §3 |
| | Primary metric defined with a 30% threshold, an answer key, a reproducible calculation, guards, measurement conditions and baseline limitations | DEC-08 [BA/PO proposal]; review of PR #40 |
| | Impact-confirmation mechanism reviewed against the five §5.5 questions | DEC-07; access matrix |
