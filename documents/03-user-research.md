# 3. User Research

**Project:** Building Maintenance Coordinator
**Sprint:** 1 · **Status:** research plan and eight simulated answer records; no real participant collection. · **Revision:** 2026-10-22

> **Research method:** interviews may be real or simulated, as clarified by the lecturer. Identify simulated responses as such and distinguish them from real participant evidence.

---

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

### Guide review against P1–P7 (DISC-01-01)

Reviewed against the [problem hypotheses](01-problem-and-opportunity-report.md#7-assumptions-and-risks). References below identify questions in sections 4 and 5, not collected evidence.

| Hypothesis | Existing coverage and preparation change | Evidence sought / limit |
|---|---|---|
| P1 — administrative effort | Administrator 3, 11; add a breakdown of active work versus waiting | One recent case, steps and approximate effort; recollections are estimates, not measured baselines |
| P2 — duplicates | Administrator 6; add frequency, period and an example of reports that were distinct | Estimate duplicates relative to total reports in the same period; do not presume duplication is common |
| P3 — urgency | Administrator 5; add what worked and what failed | Concrete priority decision, decision-maker and consequences; no presumption that current triage is poor |
| P4 — administrator adoption | Administrator 9, 12, 14; add switching barriers | Existing tools, purchase authority, training and migration constraints; interest is not adoption or a purchase |
| P5 — resident reporting | Resident 1–6 and survey 1–8; add ability to use the proposed channel | Past reporting/non-reporting and accessibility barriers; stated willingness does not validate actual use |
| P6 — contractor adoption | Administrator 7–8 and contractor 1–5; add a recent request and refusal conditions | Information needs, acceptance, availability and rescheduling; administrators cannot prove contractor willingness |
| P7 — trust in assisted recommendations | Administrator 10; add correction, disagreement and unavailability probes | Exploratory trust conditions now; task-based prototype evaluation later, without claiming trust is validated |

Q6 provides context about alternatives rather than proving a product hypothesis. Seek counterexamples for each hypothesis and record which questions were actually asked. A skipped question supplies no evidence.

## 2. Methods

| Method | Purpose | Participants | Effort |
|---|---|---|---|
| Semi-structured interviews (30–40 min) | Q1–Q7, Q9 | Administrators, contractors | Primary method |
| Short online survey | Q8, validate problem frequency | Residents | Low |
| Review of documented experiences (articles, forums, app reviews) | Q1, Q6 | Public sources | Low |
| Public competitor documentation / demos | Q6 | n/a | Low |
| Prototype testing (late Sprint 1 or Sprint 2) | Q7, usability | Administrators, residents | Medium |

### Target sample

| Group | Target | Note |
|---|---|---|
| Professional administrators | 2 | Personal introductions and public business contact channels |
| Resident / volunteer administrators | 3 | Relatives, neighbours or acquaintances |
| Residents | 8 (survey) | Forwarded invitation through personal networks |
| Contractors | 2 | Electricians, plumbers or maintenance companies |

These figures are **targets**, not results. Record the actual numbers obtained.

This is a purposive convenience sample chosen for access and contrasting roles, not statistical representation. Start with one administrator and one contractor interview to check guide clarity, then adjust effort with the team. Do not claim saturation from the target counts.

Keep professional administrators (paid work, potentially multiple buildings and company purchasing processes) separate from resident/volunteer administrators (elected or unpaid work, typically a single building). Ask about actual role and remuneration rather than inferring the segment from a title. Record mixed roles explicitly. Volunteers offer useful contrasts but do not replace evidence about the primary professional segment in DEC-02. Report counts, effort estimates and adoption constraints by segment; insufficient professional access leaves DEC-02 unvalidated. Residents and contractors provide complementary perspectives, not substitutes for administrator evidence.

## 3. Recruitment and ethics

The repository contains reusable blank templates and eight simulated answer records. The recruitment, consent and participant-data procedures below apply to future real interviews; no real participants, sessions or permissions are claimed for the simulations.

Do not collect names, contact lists, signatures, exact addresses, unit numbers, company names, photographs, recordings or identity mappings. Record broad role segments and anonymous document IDs only. An ID identifies an answer record, not a participant identity; do not create a lookup table. Remove identifying combinations of incident details, dates, location and role, even when no name is given. If the research team can still reasonably identify someone from an answer record, generalise or omit that material before saving it in Git.

### Consent text (template)

> We are students developing the academic project Building Maintenance Coordinator, which explores maintenance coordination in residential buildings. Participation is voluntary, and you may skip any question or end the conversation at any time. We retain only anonymous answers, without names, contact details, addresses or information identifying the building or company. We do not make recordings. Answers will be reviewed to remove identifying details and stored in the project's Git repository for analysis and academic assessment. Anyone with access to the repository will be able to read them; if the repository is public or becomes public, anyone will be able to read them. Git retains historical versions, and copies may exist: we cannot promise to delete all versions after publication. You may withdraw or correct an answer during the session, before your final confirmation; once the answers are anonymised, we do not keep a record linking them to your identity. Do you agree to participate and allow your answers to be used under these conditions?

Obtain an affirmative verbal answer before an interview, or an affirmative opt-in before survey questions. Record only `participation and anonymous Git storage authorised: yes/no`, without a name, signature or consent attachment. If declined, stop and do not retain answers. Use paraphrases by default; a direct quotation needs separate permission and must pass the same anonymity check. Sandro is the research-record owner; project contact: 1201244@isep.ipp.pt.

### 3.1 Recruitment and session procedure

| Segment | Recruitment route | Selection and safeguards |
|---|---|---|
| Professional administrators | Personal introductions or public business contact channels | Seek people involved in actual maintenance coordination; no contact database |
| Volunteer administrators | Relatives, neighbours or acquaintances forward an invitation | Voluntary participation; distinguish paid and unpaid roles |
| Residents | Forwarded invitation or in-person approach | Adult volunteers; no resident lists, names, units or addresses |
| Contractors | Personal introductions or public business contact channels | People receiving/scheduling maintenance work; no customer records |

Pedro coordinates invitations through existing contact channels, without copying contacts, messages or identity-linked schedules into research records. Use at most one reminder after five working days; close an unanswered invitation after ten working days. Invitations are not participant commitments. Record only aggregate recruitment counts and limitations.

### 3.2 Access failures and withdrawal

- If professional access fails after the ten-working-day invitation window, record the limitation. Volunteers and public sources do not prove professional adoption or purchasing behaviour.
- If a group is unavailable, leave its hypotheses unresolved. Record source/date for public-source review and do not call it participant research.
- If someone declines or cancels, do not retain their identity or claim a completed session. Reschedule only with their agreement.
- If no interview pair is available, use the replacements or reschedule; no solo sessions.
- If Git is unavailable, prepare only anonymous Markdown locally and perform the same check before its first commit. Do not switch to recordings or identifiable notes.
- Accept corrections/removal during the session before final confirmation. After anonymisation, do not claim that a participant can be located by identity. Remove problematic published content from the current version if discovered, and assess repository history/copy exposure separately; a deletion commit alone does not erase it.

## 4. Interview guides

The interview questions are maintained only in the interview template folder. The templates remain blank; completed simulated records are stored separately. Question numbers in the P1–P7 coverage table refer to those templates.

### 4.1 Administrator (professional or volunteer)

Use the [administrator template](templates/interviews/administrador.md), including the neutral probes on effort, duplicates, urgency, adoption and AI trust.

### 4.2 Resident

Use the [resident template](templates/interviews/morador.md), including reporting barriers, privacy, digital access and alternative channels.

### 4.3 Contractor

Use the [maintenance contractor template](templates/interviews/prestador-manutencao.md), including request acceptance, missing information, scheduling and completion.

### 4.4. Optional exploratory questions

Photographs and IoT are outside the interview core and are not presented as MVP commitments. Do not request real photographs or device/customer records.

### 4.5. Prototype testing

Task-based prototype testing is separate from this preparation. During later testing, record completion, errors, time and assistance, and compare an equivalent current-process task. Stated interest alone does not validate benefit or adoption.

## 5. Short resident survey (template)

The resident survey is a collection activity under DISC-01-02. Use the resident interview template to explore P5 in depth.

Pedro implements the survey in Microsoft Forms using the consent and settings defined in section 3.2. No survey is launched by this preparation. Open answers must not request names, contacts, exact addresses or third-party details; review them privately before synthesis.

1. Do you live in a building with condominium administration? (Yes/No)
2. Have you reported a maintenance issue in the last 12 months? (Yes/No)
3. If so, through which channel? (call, WhatsApp, email, caretaker, other)
4. Did you receive status feedback? (Always / Sometimes / Never)
5. How long did resolution take? (<1 day / 1–3 days / 4–7 days / >1 week / still unresolved)
6. What difficulty did you experience? (Open answer)
7. Would you use an app or web page to report? (Yes/Maybe/No, and why)
8. What information would you like to see? (status, expected date, contractor, other)

## 6. Analysis

- Transcribe or summarise each interview in **structured notes** immediately after the session.
- Code by theme (urgency, duplicates, costs, channels, trust in AI…).
- Record **quotes** only with permission and without identifying details.
- Each finding must state **how many participants** support it, e.g. “4 of 6 administrators”.
- Clearly distinguish **what was said** from **the team's interpretation**.

## 7. Findings

### 7.1 Actual participants

| Answer record ID | Broad segment | Month (if non-identifying) | Mode | Approximate duration | Anonymous evidence reference |
|---|---|---|---|---|---|
| | | | | | |

### 7.2 Findings

| ID | Finding | Number of supporting participants | Assumption confirmed, refuted or adjusted | Evidence (codes) |
|---|---|---|---|---|
| F1 | | | | |

### 7.3 Resulting product decisions

| Finding | Decision taken | Where reflected (backlog, vision, ADR) |
|---|---|---|
| | | |

## 8. Limitations (review after collection)

Expected limitations, to confirm or adjust:

- **Small convenience sample**, not representative.
- Limited access to **professional administrators**; probable bias towards volunteers.
- Risk of **confirmation bias**: interviewers know the proposed solution. Mitigate with open questions about past experiences before showing the idea.
- Participants may know the students (politeness, social desirability bias).
- Stated willingness to pay or adopt does not always translate into behaviour.
- No access to real incident data; AI evaluation will use synthetic data.

## 9. Activity sequence

| When | Activity |
|---|---|
| DISC-01-01 | Define the plan, consent, roles, storage rules and blank templates |
| Before DISC-01-02 recruitment | Check anonymous templates, Git readership/visibility and survey settings; |
| DISC-01-02 (deferred) | Recruit and schedule participants; conduct interviews and resident survey |
| DISC-01-03 | Analyse actual evidence, document limitations and resulting decisions |
| Later task-based testing | Evaluate usability/adoption against concrete tasks |

## 10. Records and decisions

Use the [recording template](templates/research-record.md). Findings remain in section 7; requirements and the problem report reference their IDs. Section 7.3 links to the [decision register](planning/decisions-and-feedback.md), which stores rationale, participants and decision status without duplicating meeting notes.

Apply the ownership, access and retention defined in DEC-07 and section 3.2. Pedro schedules collection under DISC-01-02; no sessions are scheduled by this preparation. Findings inform [requirements](requirements.md) and [backlog](06-product-backlog.md) prioritisation.

Store only reviewed anonymous answers in `documents/research/answers/`; no identity maps, contact lists or consent attachments. Link anonymous record IDs to findings without creating a participant lookup. Preparation evidence is tracked in [DISC-01-01](backlog/tasks/DISC-01-01-prepare-research.md#completion-record); collection and synthesis remain DISC-01-02/03.
