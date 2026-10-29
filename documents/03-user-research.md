# 3. User Research

**Project:** Building Maintenance Coordinator · **Sprint:** 1 · **Revision:** 2026-10-22
**Status:** synthesis prepared for independent review; acceptance and integration evidence in [DISC-01-03](backlog/tasks/DISC-01-03-synthesise-findings.md#completion-record).

## 1. Research objectives

| # | Question | Related assumption (deliverable 1) |
|---|---|---|
| Q1 | How are maintenance issues currently managed, from first report to resolution? | P1, P3 |
| Q2 | How much time and effort does each issue cost the administrator? | P1 |
| Q3 | How often are reports duplicated or contradictory? | P2 |
| Q4 | How is urgency determined, and who decides? | P3 |
| Q5 | How are contractors chosen (criteria, sources, approvals, cost limits)? | P6 |
| Q6 | What tools are used today, and what is missing? | Deliverable 2 |
| Q7 | Would administrators accept AI-assisted recommendations subject to approval? Under what conditions? | P7 |
| Q8 | What prompts residents to report, or not report, an issue? | P5 |
| Q9 | What does a contractor need to know about a request, and how do they manage scheduling? | P6 |

## 2. Method and evidence coverage

Sprint 1 uses eight written simulated interviews and the historical public-source review. The reported lecturer clarification permits real or simulated interviews; its date and meeting record were not supplied. This exercise analyses fictional scenarios, not empirical validation.

| Material | Actual coverage | Canonical record |
|---|---|---|
| Simulated answers | Two fictional profiles per segment: professional administrators, volunteer administrators, residents and contractors; 78 written answers | [Inventory, creation dates and provenance](research/answers/README.md) |
| Public sources | Nine sources, accessed 2026-10-14; no new source visits for this synthesis | [Source register](#31-public-sources-reviewed) |
| Real collection | Zero participants, sessions, survey responses, observations or prototype tests recorded; no documented recruitment attempts | Unexecuted [collection procedure and guides](templates/research-collection.md) |

Consent, interviewer and session date/duration do not apply to fictional profiles. Preparation, collection checks and synthesis acceptance are recorded in [DISC-01-01](backlog/tasks/DISC-01-01-prepare-research.md#completion-record), [DISC-01-02](backlog/tasks/DISC-01-02-conduct-research.md#completion-record) and [DISC-01-03](backlog/tasks/DISC-01-03-synthesise-findings.md#completion-record), respectively.

<!-- Preserve the former findings anchor used by the eight unchanged SIM-* source records. -->
<a id="7-findings"></a>

## 3. Findings

### 3.1 Public sources reviewed

| Code | Source type and publisher | Publication/access date | Scope and evidence reviewed | Limitations |
|---|---|---|---|---|
| S1 | Government guidance, GOV.UK | Accessed 2026-10-14 | [Private renting: repairs](https://www.gov.uk/private-renting/repairs): residents should report faults promptly; landlords have specified repair responsibilities; landlords should indicate when repairs are expected; unresolved problems can be escalated to the local council or relevant housing body. | England-focused private-renting guidance; not evidence about condominium administration, local practice, frequency or effort. |
| S2 | Vendor product article, Buildium | Published 2025-11-22; accessed 2026-10-14 | [The role of property maintenance management systems](https://www.buildium.com/blog/property-maintenance-management-systems/): describes centralized repair records, work orders, tenant communication/status updates, vendor history, scheduling and cost reporting as capabilities or claimed benefits. | Supplier marketing content; claims are not independent outcome measurements and do not prove user demand or effectiveness. |
| S3 | Ombudsman casework report, Housing Ombudsman Service | Published 2019-03; accessed 2026-10-14 | [Spotlight report on complaints about repairs](https://www.housing-ombudsman.org.uk/reports/spotlight-on-complaints-about-repairs/): dissatisfaction with repairs accounts for over a third of complaints in the report's context; recurring complaint causes include responsibility, time taken and record-keeping. | UK social-housing ombudsman casework; not a prevalence estimate for this project or for private/condominium buildings. |
| S4 | Ombudsman casework report, Housing Ombudsman Service | Published 2025-05; accessed 2026-10-14 | [Spotlight report on repairs and maintenance](https://www.housing-ombudsman.org.uk/reports/spotlight-reports/repairing-trust/): reports 6,380 repair-and-maintenance findings in 2024–25 and highlights trust, communication, complaint handling, contractor relationships, costs and skills shortages; recommends transparency, stronger relationships and more proactive maintenance. | Casework findings and recommendations, not a controlled study; its 2024–25 count is not a general incident rate. |
| S5 | Ombudsman information-management report, Housing Ombudsman Service | Published 2023-05; accessed 2026-10-14 | [Spotlight report on Knowledge and Information Management](https://www.housing-ombudsman.org.uk/reports/spotlight-on-knowledge-and-information-management/): states that weak information management can turn a service request into a protracted complaint and can prevent risk identification, evidence-based practice and consistent service. | Social-housing governance context; the page summarises a report and does not quantify the effect for this product's target segment. |
| S6 | Vendor product documentation, Buildium | Accessed 2026-10-14 | [Property management maintenance software](https://www.buildium.com/features/maintenance-request-management/): presents resident request capture, task ownership, due dates, recurring work, time-stamped updates, work-order visibility and an AI maintenance agent as product capabilities. | Supplier claims and feature descriptions; no independent usability, adoption, accuracy or outcome evidence. |
| S7 | Vendor product documentation, Property Meld | Last modified 2025-03-26; accessed 2026-10-14 | [Scheduling](https://propertymeld.com/scheduling-efficiency/): positions scheduling as a major coordinator workload and describes tracking speed to schedule, speed to assign, vendor/technician cycle times and bottlenecks. | Supplier marketing content; workload and performance claims are not independently measured here. |
| S8 | Vendor product documentation, Property Meld | Last modified 2025-06-13; accessed 2026-10-14 | [Maintenance communication](https://propertymeld.com/maintenance-communication/): describes resident responses, missing work-order information, vendor follow-up, investor approvals and tracking communication volume/response speed. | Supplier marketing content; does not establish that these problems occur in the project's local target segment. |
| S9 | Vendor product documentation, Property Meld | Last modified 2025-10-02; accessed 2026-10-14 | [Oversight and data](https://propertymeld.com/maintenance-data/): presents metrics for technician performance, vendor efficiency, coordinator effectiveness, communication, scheduling, staffing and profitability. | Supplier marketing content; benchmark availability and metric definitions require independent verification. |

### 3.2 Public-source findings

| ID | Public-source finding | Implication / limit | Sources |
|---|---|---|---|
| PS-01 | Public repair guidance makes reporting, expected timing and escalation visible parts of the process. | Supports investigating status visibility and escalation as workflow requirements; does not validate local need or frequency. | S1 |
| PS-02 | A commercial maintenance platform positions centralized records, work orders, vendor coordination and resident updates as a product baseline. | Supports treating traceable history, dispatch and status communication as competitor capabilities to compare; does not prove differentiation or value. | S2 |
| PS-03 | Public ombudsman casework identifies responsibility, elapsed time and record-keeping as recurring repair-complaint themes. | Supports making ownership, due dates, status history and escalation explicit workflow concepts; does not establish local complaint frequency. | S3 |
| PS-04 | Recent ombudsman casework links repair outcomes with trust, communication, complaint handling and contractor relationships, and recommends more proactive maintenance. | Supports evaluating resident-facing updates, contractor coordination and preventive follow-up as separate workflow concerns; does not validate the proposed AI approach. | S4 |
| PS-05 | Ombudsman information-management guidance treats data creation, storage, sharing and use as service controls, not just record retention. | Supports an auditable issue history with controlled visibility and usable information for decisions; supports DEC-07 concerns without confirming the final policy. | S5 |
| PS-06 | Competitor documentation commonly exposes request intake, ownership, due dates, timestamps, recurring work and status visibility. | Establishes a baseline feature set that the product must compare against; does not show which capabilities users value or use. | S6 |
| PS-07 | Property Meld frames scheduling and assignment cycle time, vendor performance and bottleneck visibility as core maintenance-management concerns. | Supports measuring time-to-assign, time-to-schedule, completion and handoff bottlenecks if primary data becomes available; no local baseline exists. | S7, S9 |
| PS-08 | Competitor documentation treats communication gaps, missing request information, follow-up and approval visibility as operational problems. | Supports testing minimum request information, approval states and communication history in later usability work; vendor claims do not validate severity. | S8 |

### 3.3 Scenario synthesis (DISC-01-03)

Compare answers by effort, duplication, urgency, adoption, access, dispatch and AI trust, retaining contrasts within each segment. Counts below describe fictional documents, not supporting participants; question numbers refer to each record's guide, not Q1–Q9. Public findings provide context, not independent corroboration of a scenario.


| ID / topic | Recorded scenario content and exact references | Interpretation and counterexample | Context from public findings |
|---|---|---|---|
| SF-01 / effort | [SIM-ADM-P-01](research/answers/SIM-ADM-P-01.md), questions 3/11: fragmented contacts; [SIM-ADM-P-02](research/answers/SIM-ADM-P-02.md), 3/11: an existing structured tool; [SIM-ADM-V-01](research/answers/SIM-ADM-V-01.md), 3/11: several contacts and access coordination; [SIM-ADM-V-02](research/answers/SIM-ADM-V-02.md), 3/11: low-volume direct coordination. Four fictional records; constructed times are extracted once in section 3.5. | Coordination effort may depend on process maturity and contact volume, not role alone. Focus the experiment on fragmented coordination; low-effort cases challenge a universal value claim. Waiting for a contractor is not active administration. | PS-03 and PS-07 motivate examining handoffs; they supply no local effort baseline. |
| SF-02 / duplicates | All four administrator records, question 6: P-01 describes six repeated communications out of 20 and two apparently similar but distinct faults; P-02 one out of 15; V-01 two repeated messages out of five; V-02 none out of three. [SIM-MOR-01](research/answers/SIM-MOR-01.md) and [SIM-MOR-02](research/answers/SIM-MOR-02.md), question 3, describe not reporting when someone else may have done so. | Duplicate volume is not uniformly high even within fiction. Different denominators and invented periods prohibit pooling rates. Preserve separate reports and human review of links; silence does not show lack of impact. | PS-06 concerns feature availability, not proof of duplicate frequency. |
| SF-03 / urgency | Four administrator records, question 5: P-01/V-01/V-02 seek technical input when uncertain; P-02 describes triage that worked. | Missing context and uncertainty deserve explicit handling, but poor current triage is not established. Retain manual judgement and independent critical-signal rules; do not promise diagnosis or safety. | PS-03/04 concern repair outcomes, not AI classification accuracy. |
| SF-04 / administrator adoption | Four administrator records, questions 9/12/14: P-01 considers a limited pilot without migration; P-02 requires demonstrated integration; V-01 wants simplicity and collective cost approval; V-02 sees little reason to add a paid tool. | Conditional interest is not adoption. Keep professionals as the primary experiment segment, but compare process maturity within it; volunteers cannot validate business purchasing. Integration is a barrier to test, not a commitment to build integrations now. | PS-02/06 show existing alternatives; supplier feature claims do not establish switching demand. |
| SF-05 / resident access and privacy | Two resident records, questions 4-6: MOR-01 wants receipt/status with a short mobile flow and private, optional impact confirmation; MOR-02 prefers telephone/help and rejects mandatory digital participation. | A simple page alone may not include everyone. Retain private reports, administrator-published summaries and optional impact confirmation; evaluate an assisted reporting route before claiming accessibility. These are two fictional perspectives, not a usability test. | PS-01/05 support investigating communication and controlled information sharing in other contexts. |
| SF-06 / dispatch and closure | [SIM-PRE-01](research/answers/SIM-PRE-01.md) and [SIM-PRE-02](research/answers/SIM-PRE-02.md), questions 1-5, distinguish scope approval, acceptance, availability, access and completion. PRE-01 accepts a simple request but keeps its own calendar; PRE-02 rejects another mandatory app and automatic penalties. Administrator records, questions 7-8, provide four additional fictional process perspectives. | Retain distinct approval, response, booking, completion and closure steps. A calendar event cannot prove contractor availability. Preserve refusal, rescheduling and a manual coordination option; no assumed contractor adoption. | PS-07/08 motivate scheduling and approval visibility, without validating this local workflow. |
| SF-07 / AI value and trust | Four administrator records, question 10: P-01/V-01 ask for reasons, correction and a manual route; P-02 sees limited need for routine classification; V-02 would not adopt for AI. | Explainability and review are design conditions, not demonstrated trust or usefulness. Keep assisted classification as the academic experiment, compare it with rules/manual triage, and allow suggestions to be ignored. | None of PS-01 to PS-08 evaluates the proposed AI or proves its benefit. |

### 3.4 Hypothesis disposition and next tests

All P1-P7 remain **empirically unresolved**. Support or contradiction below applies only to the constructed scenarios; no hypothesis is marked confirmed or refuted about the target population.

| Hypothesis | Scenario disposition / finding | Next evidence that could change the decision |
|---|---|---|
| P1 | Mixed: high-contact cases support investigating effort; low-effort cases challenge universal significance (SF-01). | Compare equivalent current-process and BMC tasks by active time, errors and assistance, including a structured-process counterexample; validate operational relevance separately. |
| P2 | Mixed: duplication exists in some scenarios and is absent/rare in others (SF-02). | Real anonymised reports with common period/denominator for frequency; separately annotated same-fault versus different-fault pairs for duplicate-link evaluation. |
| P3 | Mixed: uncertain cases coexist with working triage (SF-03). | Expert-reviewed cases, reasons for priority and errors under manual/rules/AI conditions; no safety guarantee from a small dataset. |
| P4 | Conditional interest and resistance, not buying intent (SF-04). | Professional administrators complete a trial task and explain actual purchasing/integration constraints; distinguish stated interest from continued use. |
| P5 | Digital willingness in one profile and telephone preference in another (SF-05). | Task-based reporting with people of differing digital access, recording completion, errors, assistance and privacy comprehension. |
| P6 | Conditional request acceptance with calendar/app resistance (SF-06). | Test accept/refuse/reschedule and change-of-scope tasks with contractors; check actual willingness to maintain the proposed channel. |
| P7 | Correction/explanation requested, but some profiles see little AI value (SF-07). | Compare task outcomes with rules/manual and AI suggestions, including wrong and unavailable suggestions; record corrections and harmful reliance. |

### 3.5 Coordination-effort baseline

**No empirical baseline estimate is available.** SF-01 contains invented case times of 45, 10, about 60 and 15 active minutes. The corresponding question-11 ranges are 30-60, 10-15, 40-70 and 15-20 minutes within those fictional profiles. Do not average these into a user baseline, use them to calibrate a reduction target, or interpret elapsed repair time as effort saved.

The answers describe different per-occurrence activities and do not isolate the receipt-to-approved-request window in the [vision's measurement protocol](04-product-vision.md#51-primary-success-criterion-dec-08). No conversion to that window can be inferred. DEC-08 and LIM-04 remain open.


## 4. Resulting product decisions

The [decision register](planning/decisions-and-feedback.md#disc-01-03-synthesis-proposals) is canonical for proposal wording, rationale, review status and affected product artefacts. The mapping below connects findings to those proposals without maintaining a second decision record.

| Findings | Proposal | Consequence |
|---|---|---|
| SF-01/04 | SP-01 / DEC-02 | Qualify the opportunity by process fragmentation and contact volume |
| SF-02/05 | SP-02 / DEC-07 | Retain controlled sharing and optional participation |
| SF-03/07 | SP-03 / DEC-05 | Retain reviewed AI as an experiment with a manual/rules alternative |
| SF-06 | SP-04 / DEC-10 | Keep approval, acceptance, booking and closure distinct |
| SF-01/07 | SP-05 / DEC-08 | Evaluate equivalent tasks without using fictional times as a baseline |

## 5. Limitations

- The scenarios contain constructed incidents, counts and effort values. They may reflect the product already imagined by their authors; adding fictional counterexamples does not remove that design bias. They cannot establish real frequency, adoption, trust or savings. All P1–P7 remain empirically unresolved.
- The nine public sources provide contextual guidance, casework and supplier claims. This is not a systematic literature review, representative market study or independent competitor audit; source-specific limits remain in section 3.1.
- Original simulation generation tooling/process and the record of the lecturer clarification are unavailable. See the [inventory provenance](research/answers/README.md#método-e-proveniência). The absence of recruitment records is not evidence that recruitment failed.

The [hypothesis table](#34-hypothesis-disposition-and-next-tests) identifies next evidence needed; future collection risks and procedures belong in the [reusable preparation](templates/research-collection.md#5-analysis-and-later-prototype-tests).
