# Research collection procedure

**Status:** reusable preparation from DISC-01-01; real interviews, resident survey and prototype tests remain unexecuted. These are options for separately planned validation. The simulated exercise follows the reported lecturer clarification; no dated minutes or independent acceptance are recorded.

Relocation recorded 2026-10-25 in PR #39: preparation guidance formerly in research report sections 2–6 and 9–10 is maintained here; this is not evidence that the planned activities occurred.

The [research report](../03-user-research.md) records the method actually used and its findings. The [security policy](../09-security-privacy.md#41-research-data-handling-disc-01-01) governs storage, access, anonymity, review and retention; [DEC-07](../planning/decisions-and-feedback.md#dec-07-research-preparation-disc-01-01) records the rationale. Use the [answer-record template](research-record.md) for collection metadata and evidence.

## 1. Guides and hypothesis coverage

| Segment | Reusable guide | Focus |
|---|---|---|
| Professional or volunteer administrator | [Administrator](interviews/administrador.md) | Process, effort, duplicates, urgency, adoption and AI trust |
| Resident | [Resident](interviews/morador.md) | Reporting, privacy, digital access and alternative channels |
| Contractor | [Maintenance contractor](interviews/prestador-manutencao.md) | Request acceptance, missing information, scheduling and completion |

Preparation mapping for [P1–P7](../01-problem-and-opportunity-report.md#7-assumptions-and-risks); references identify guide questions, not collected evidence.

| Hypothesis | Guide questions and probes | Evidence sought / limit |
|---|---|---|
| P1 — administrative effort | Administrator 3, 11; a breakdown of active work versus waiting | One recent case, steps and approximate effort; recollections are estimates, not measured baselines |
| P2 — duplicates | Administrator 6; frequency, period and an example of reports that were distinct | Estimate duplicates relative to total reports in the same period; do not presume duplication is common |
| P3 — urgency | Administrator 5; what worked and what failed | Concrete priority decision, decision-maker and consequences; no presumption that current triage is poor |
| P4 — administrator adoption | Administrator 9, 12, 14; switching barriers | Existing tools, purchase authority, training and migration constraints; interest is not adoption or a purchase |
| P5 — resident reporting | Resident 1–6 and resident survey 1–8; ability to use the proposed channel | Past reporting/non-reporting and accessibility barriers; stated willingness does not validate actual use |
| P6 — contractor adoption | Administrator 7–8 and contractor 1–5; a recent request and refusal conditions | Information needs, acceptance, availability and rescheduling; administrators cannot prove contractor willingness |
| P7 — trust in assisted recommendations | Administrator 10; correction, disagreement and unavailability probes | Exploratory trust conditions now; task-based prototype evaluation later, without claiming trust is validated |

Photographs and IoT are optional exploratory topics outside the interview core, not MVP commitments. Do not request real photographs or device/customer records.

Q6 provides context about alternatives. Seek counterexamples, record omitted questions and never treat a skipped question as negative evidence.

## 2. Future sample and access

The method options below preserve the DISC-01-01 plan. They are not executed participant research or a commitment to new collection; Q1–Q9 refer to the [research objectives](../03-user-research.md#1-research-objectives). Public-source review already has a separate historical register.

| Method | Purpose | Participants | Effort |
|---|---|---|---|
| Semi-structured interviews (30–40 min) | Q1–Q7, Q9 | Administrators, contractors | Primary method |
| Short online survey | Q8, explore reported frequency (non-representative) | Residents | Low |
| Review of documented experiences (articles, forums, app reviews) | Q1, Q6 | Public sources | Low |
| Public competitor documentation / demos | Q6 | n/a | Low |
| Prototype testing (separately planned) | Q7, usability | Administrators, residents | Medium |

Use semi-structured administrator/contractor interviews (30–40 minutes) and the optional resident survey below. Recruitment targets from preparation:

| Group | Target | Note |
|---|---|---|
| Professional administrators | 2 | Personal introductions and public business contact channels |
| Resident / volunteer administrators | 3 | Relatives, neighbours or acquaintances |
| Residents | 8 (survey) | Forwarded invitation through personal networks |
| Contractors | 2 | Electricians, plumbers or maintenance companies |

This is a purposive convenience sample chosen for access and contrasting roles, not statistical representation. Start with one administrator and one contractor interview to check guide clarity, then adjust effort with the team. Do not claim saturation from the target counts.

Keep professional administrators (paid work, potentially multiple buildings and company purchasing processes) separate from resident/volunteer administrators (elected or unpaid work, typically a single building). Ask about actual role and remuneration rather than inferring the segment from a title. Record mixed roles explicitly. Volunteers offer useful contrasts but do not replace evidence about the primary professional segment in DEC-02. Report counts, effort estimates and adoption constraints by segment; insufficient professional access leaves DEC-02 unvalidated. Residents and contractors provide complementary perspectives, not substitutes for administrator evidence.

| Segment | Recruitment route | Selection and safeguards |
|---|---|---|
| Professional administrators | Personal introductions or public business contact channels | Seek people involved in actual maintenance coordination; no contact database |
| Volunteer administrators | Relatives, neighbours or acquaintances forward an invitation | Voluntary participation; distinguish paid and unpaid roles |
| Residents | Forwarded invitation or in-person approach | Adult volunteers; no resident lists, names, units or addresses |
| Contractors | Personal introductions or public business contact channels | People receiving/scheduling maintenance work; no customer records |

Pedro coordinates invitations through existing contact channels, without copying contacts, messages or identity-linked schedules into research records. Use at most one reminder after five working days; close an unanswered invitation after ten working days. Record aggregate recruitment counts and limitations; invitations are not commitments.

Pedro conducts interviews and Ricardo takes notes; Afonso and Sandro are their respective replacements. Sandro owns research records (project contact: 1201244@isep.ipp.pt); Martim reviews anonymity before merge. Task ownership and synthesis review remain in the [backlog allocation](../backlog/README.md).

### Access failures and withdrawal

- If professional access fails after the ten-working-day invitation window, record the limitation. Volunteers and public sources do not prove professional adoption or purchasing behaviour.
- If a group is unavailable, leave its hypotheses unresolved. Record source/date for public-source review and do not call it participant research.
- If someone declines or cancels, do not retain their identity or claim a completed session. Reschedule only with their agreement.
- If no interview pair is available, use the replacements or reschedule; no solo sessions.
- If Git is unavailable, prepare only anonymous Markdown locally and perform the same check before its first commit. Do not switch to recordings or identifiable notes.
- Accept corrections/removal during the session before final confirmation. After anonymisation, do not claim that a participant can be located by identity. Remove problematic published content from the current version if discovered, and assess repository history/copy exposure separately; a deletion commit alone does not erase it.

## 3. Consent and session procedure

Before collecting real answers, check repository visibility/readership and the [data-handling controls](../09-security-privacy.md#41-research-data-handling-disc-01-01). Collect notes only: no audio/video, automatic transcription, real photographs or device/customer records. Apply the same anonymity check to incidental details and combinations that could identify someone.

### Consent text (template)

> We are students developing the academic project Building Maintenance Coordinator, which explores maintenance coordination in residential buildings. Participation is voluntary, and you may skip any question or end the conversation at any time. We retain only anonymous answers, without names, contact details, addresses or information identifying the building or company. We do not make recordings. Answers will be reviewed to remove identifying details and stored in the project's Git repository for analysis and academic assessment. Anyone with access to the repository will be able to read them; if the repository is public or becomes public, anyone will be able to read them. Git retains historical versions, and copies may exist: we cannot promise to delete all versions after publication. You may withdraw or correct an answer during the session, before your final confirmation; once the answers are anonymised, we do not keep a record linking them to your identity. Do you agree to participate and allow your answers to be used under these conditions?

Obtain an affirmative verbal answer before an interview, or an affirmative opt-in before survey questions. Record only **participation and anonymous Git storage authorised: yes/no**, without a name, signature or consent attachment. If declined, stop and do not retain answers. Use paraphrases by default; a direct quotation needs separate permission and the same anonymity check. Read answers back for corrections/removal before final confirmation.

## 4. Short resident survey (template)

Unexecuted option for P5. Pedro prepares Microsoft Forms and checks its settings against the security policy before launch: no identifying questions, login, account metadata or uploads. Obtain consent before questions; review open answers privately before synthesis. The policy specifies export checks and deletion of working exports/tool responses.

1. Do you live in a building with condominium administration? (Yes/No)
2. Have you reported a maintenance issue in the last 12 months? (Yes/No)
3. If so, through which channel? (call, WhatsApp, email, caretaker, other)
4. Did you receive status feedback? (Always / Sometimes / Never)
5. How long did resolution take? (<1 day / 1–3 days / 4–7 days / >1 week / still unresolved)
6. What difficulty did you experience? (Open answer)
7. Would you use an app or web page to report? (Yes/Maybe/No, and why)
8. What information would you like to see? (status, expected date, contractor, other)

## 5. Analysis and later prototype tests

- Summarise interviews in structured notes immediately after each session; code by theme and retain counterexamples.
- Separate answers/observations from interpretation. Empirical findings cite actual participant/source counts; scenario interpretations cite fictional record IDs and question numbers, never participant counts.
- Record quotations only with permission and after the anonymity check.
- Plan prototype testing separately. Record completion, errors, time and assistance on equivalent current-process and BMC tasks, following the [vision's measurement protocol](../04-product-vision.md#51-primary-success-criterion-dec-08). Stated interest alone does not establish benefit or adoption.

Risks to revisit when planning real collection:

- **Small convenience sample**, not representative.
- Limited access to **professional administrators**; probable bias towards volunteers.
- Risk of **confirmation bias**: interviewers know the proposed solution. Mitigate with open questions about past experiences before showing the idea.
- Participants may know the students (politeness, social desirability bias).
- Stated willingness to pay or adopt does not always translate into behaviour.
- Check access to incident data separately; synthetic AI evaluation cannot establish real-world performance.

## 6. Activity sequence

| When | Activity |
|---|---|
| DISC-01-01 | Define the plan, consent, roles, storage rules and blank templates |
| Before any real recruitment/collection | Check anonymous templates, Git readership/visibility and survey settings |
| DISC-01-02 (2026-10-22 check) | Inventory and verify the eight existing simulated interviews; real collection and survey remain unexecuted; independent acceptance unevidenced |
| DISC-01-03 | Synthesise public evidence and fictional scenarios separately; document limitations and proposed decisions; PR #39 awaits re-review |
| Later task-based testing | Plan and evaluate usability/adoption against concrete tasks |

## 7. Records and decisions

Use the [record template](research-record.md) for each actual interview, survey administration, observation, prototype test or public source; label simulated records explicitly and never invent consent or session metadata. The [research findings](../03-user-research.md#3-findings) retain finding IDs; requirements and the problem report cite them. The [decision register](../planning/decisions-and-feedback.md) retains rationale, authors, dates and decision status without duplicating meeting notes.

The collection inventory and author-side checks do not establish independent acceptance of DISC-01-02. No real collection or empirical validation of adoption, problem frequency or AI value is claimed. Pedro coordinates any future collection under the DEC-07 arrangements above; this procedure schedules no sessions. Findings inform [requirements](../requirements.md) and [backlog](../05-product-backlog.md) prioritisation.

Store only reviewed anonymous answers in `documents/research/answers/`; no identity maps, contact lists or consent attachments. Link anonymous document IDs to findings without creating a participant lookup. Preparation evidence remains in [DISC-01-01](../backlog/tasks/DISC-01-01-prepare-research.md#completion-record), collection evidence in [DISC-01-02](../backlog/tasks/DISC-01-02-conduct-research.md#completion-record), and synthesis evidence in [DISC-01-03](../backlog/tasks/DISC-01-03-synthesise-findings.md#completion-record).
