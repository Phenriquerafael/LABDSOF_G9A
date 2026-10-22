# 1. Problem and Opportunity Report

**Project:** Building Maintenance Coordinator
**Sprint:** 1 · **Status:** synthesis revision; independent review pending · **Revision:** 2026-10-22

> Assumptions and benefits not yet demonstrated are hypotheses. Public-source findings and explicitly simulated scenario interpretations belong in [User Research](03-user-research.md); competitor sources belong in [document 02](02-market-and-competitor-analysis.md). This report links that evidence to the problem without duplicating the findings.

---

## 1. Target community

Residential building communities in Portugal, managed by:

- **Condominium management companies** (primary segment: managing multiple buildings), or
- **Resident administrators** (volunteer or elected administrators managing a single building).

The community includes residents and property owners, as well as maintenance contractors working in the building.

## 2. Problem

> **[Hypothesis]** In some residential buildings, reports scattered across calls, messages and emails increase the effort required for triage, contractor contact and follow-up. The opportunity is conditional on fragmented coordination: an already structured process or low request volume may offer little benefit from another tool (SF-01/04). Duplicate frequency, triage quality and local process limitations remain empirically unresolved.

### Connection to the project theme (community resilience)

Failures involving water, electricity, lifts or plumbing are **disruptions to a community's everyday life**. The time between the first report and resolution affects the impact on residents and the cost of damage.

### Outcome the product aims to improve

Reduce administrators' active effort when triaging and preparing an intervention. Also measure time to request submission, acceptance and resolution, distinguishing external factors. Metrics are defined in the [vision](04-product-vision.md); targets depend on the baseline (DEC-08).

## 3. Current practices (existing alternatives)

**[Hypothesis]** Reports may arrive through calls, messages or neighbourhood groups; administrators and contractors coordinate through existing contacts and records in software, spreadsheets or paper. We need to observe where this process helps and where it requires additional effort. Advantages, limitations and products are compared in the [alternatives analysis](02-market-and-competitor-analysis.md#2-selected-alternatives).

## 4. Stakeholders

| Stakeholder | Interest | Power / influence | Main pain point [Hypothesis] |
|---|---|---|---|
| Administrator (management company) | Resolve issues quickly, control costs, avoid complaints | Potentially high; purchasing/spending authority to verify | Contact volume, manual coordination, lack of traceability |
| Resident administrator (volunteer) | Resolve issues without spending too much time | Medium | Limited time and technical knowledge |
| Resident / property owner | Know the problem was received and its current status | Medium (puts pressure on the administrator) | Lack of feedback, multiple channels |
| Contractor | Clear requests, conflict-free schedule, timely payment | Medium | Incomplete information, wasted visits |
| Caretaker / building attendant (where applicable) | Report and follow up | Low | Overload as an intermediary |
| Owners' assembly | Approve expenditure and review accounts | High for major expenses | Lack of cost transparency |
| Insurers | Documented incidents | Low (indirect) | Missing damage records |

## 5. Problem evidence

**Synthesis dated 2026-10-22:** eight fictional interview records and nine previously registered public sources; zero real participants. The simulated method is permitted by the clarification recorded in the research plan. It supports academic scenario analysis, not claims of market prevalence, actual adoption or measured savings. No new external-source review was performed; public-source access dates remain 2026-10-14.

| ID | Evidence type / reference | Implication for the problem | Assumptions |
|---|---|---|---|
| E1 | Historical public findings [PS-03/04/05](03-user-research.md#72-findings), based on S3-S5 | Repair coordination, communication and records warrant investigation; UK housing casework does not establish prevalence in Portuguese condominiums. | P1/P3 |
| E2 | Vendor descriptions [PS-02/06/07/08](03-user-research.md#72-findings), S2/S6-S9 | Existing tools already address coordination; availability and marketing claims do not demonstrate local switching demand or differentiation. | P1/P4/P6 |
| E3 | Scenario interpretations [SF-01/04](03-user-research.md#721-scenario-synthesis-disc-01-03), four administrator documents, zero participants | Focus on fragmented processes; structured professional and low-volume volunteer cases challenge universal need. | P1/P4 |
| E4 | Scenario interpretations SF-02/05, four administrator and two resident documents, zero participants | Duplicates and non-reporting require different responses; preserve separate reporting and voluntary participation. | P2/P5 |
| E5 | Scenario interpretations SF-03/07, four administrator documents, zero participants | Uncertainty is not proof of poor triage; explainable suggestions are not proof of AI value or trust. | P3/P7 |
| E6 | Scenario interpretation SF-06, two contractor and four administrator documents, zero participants | Approval, acceptance, booking and closure must not be conflated; contractor adoption remains uncertain. | P6 |

SF references resolve to the [source-linked synthesis table](03-user-research.md#721-scenario-synthesis-disc-01-03); counts overlap between findings and must not be summed as independent support. Government guidance PS-01 is contextual, not Portuguese condominium law. No legal rule or spending limit is asserted here.

### Stakeholder implications

- **Professional administrators:** compare fragmented and already organised processes within the segment. Purchase authority, integration and migration barriers may outweigh a feature benefit (SF-01/04).
- **Volunteers:** simplicity and low volume can make existing tools sufficient. Their scenarios do not validate professional buying behaviour (SF-01/04).
- **Residents:** receipt/status and privacy need evaluation alongside telephone/assisted participation; non-reporting is not absence of need (SF-02/05).
- **Contractors:** request clarity must coexist with refusal, own calendars, rescheduling and separate approval of changed scope (SF-06).
- **Caretakers, assemblies and insurers:** no dedicated scenario or participant record exists; their table entries remain untested stakeholder hypotheses. Do not infer their authority or needs from contractor answers.

### Effort baseline and decision consequence

No empirical baseline is available. The fictional per-occurrence times neither measure real effort nor isolate the product metric's receipt-to-approved-request window. See the [canonical effort extraction and limitations](03-user-research.md#723-coordination-effort-baseline); the evaluation protocol remains in vision section 5.1.

The [SP-01 to SP-05 proposals](planning/decisions-and-feedback.md#disc-01-03-synthesis-proposals) narrow the framing and retain the bounded MVP with explicit reasons; no new integration, marketplace or autonomous decision is committed.

## 6. Consequences of leaving the problem unresolved

- Urgent failures (leaks, electrical faults) worsen because of delayed triage. **[Hypothesis]**
- Higher costs from emergency interventions and avoidable damage. **[Hypothesis]**
- Conflict between residents and administrators due to lack of transparency. **[Hypothesis]**
- Administrator overload and decisions without data or cost history. **[Hypothesis]**

## 7. Assumptions and risks

| # | Assumption | Risk if false |
|---|---|---|
| P1 | Administrators spend significant time coordinating maintenance issues | No meaningful pain point, no product opportunity |
| P2 | Duplicate reports occur in significant numbers | Duplicate detection loses value |
| P3 | Urgency is poorly triaged today | AI classification loses value |
| P4 | Administrators are willing to adopt a new platform | Low adoption |
| P5 | Residents will report through an app/web page if it is simple | Insufficient input |
| P6 | Contractors will accept requests and scheduling through the platform | Dispatch remains manual |
| P7 | Administrators trust AI-assisted recommendations if they are explainable and subject to approval | AI is underused or rejected |

The [P1-P7 disposition table](03-user-research.md#722-hypothesis-disposition-and-next-tests) records each hypothesis as empirically unresolved, identifies scenario support/counterexamples and specifies the next test. No hypothesis is confirmed merely because a fictional profile expresses it.

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Limited access to professional administrators | High | High | Also involve volunteers; document the limitation |
| Excessive scope (contractor marketplace) | High | High | Small synthetic catalogue, rule-based ranking |
| Personal data and interior photographs (GDPR) | Medium | High | Synthetic data, minimisation, defined retention |
| AI error in a critical situation | Medium | High | Independent rules, human review and false-negative evaluation; no guarantee of perfect detection |
| Existing competitors cover the essentials | Medium | Medium | Investigate the flow's specific value and revise scope based on evidence; see deliverable 2 |

## 8. Opportunity

For buildings where coordination is fragmented and repeated handoffs create material effort, test a traceable chain: **report → triage → dispatch → resolution → history**, with urgency as a central concern and AI as support, never the final decision-maker. P1 is central to the opportunity. P2 and P3 determine the value of duplicate detection and assisted triage; negative findings should change those capabilities. Adoption (P4–P6), AI usefulness (P7) and differentiation require their own evaluation.

## 9. Investor question (Sprint 1)

*Is this a valuable problem, and is the cycle “report, review triage, approve a request, obtain a response, schedule and close” the smallest credible experiment?*

## 10. Traceability and domain research

- Interview guides and findings: [03 User Research](03-user-research.md).
- Derived requirements: [requirements](requirements.md), still subject to validation.
- IoT and target segment: DEC-01 and DEC-02 in the [register](planning/decisions-and-feedback.md).
- Investigate responsibility for shared/private areas, recurring interventions, contractor availability, approvals and digital exclusion. These are research questions, not legal or market conclusions.
- Residents may be tenants; building membership and authority to approve expenses are different concepts. Confirm terminology during interviews.
