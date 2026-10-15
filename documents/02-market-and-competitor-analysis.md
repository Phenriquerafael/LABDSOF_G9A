# 2. Market and Competitor Analysis

**Status:** source verification v0.5 (DISC-02-01) — comparison and differentiation conclusions pending DISC-02-02 · **Sprint:** 1 · **Revision:** 2026-10-15

## 1. Evidence quality

Public sources were opened on **2026-10-13** (S01–S16) and **2026-10-15** (S17–S27, plus re-checks of S09 and S14) and recorded in the [register](#5-source-and-findings-register). They replace the undated leads of v0.3. **No demo, trial or hands-on test was performed**; no cell in this document is “observed in testing”.

- **SC** = supplier claim (vendor page, help article or app-store listing written by the vendor). **AD** = advertising or promotional editorial. **UR** = public user reviews. **PD** = platform documentation (e.g. how an app store produces its labels). None of these proves quality, security or compliance.
- **UC** = unconfirmed: the sources opened do not describe the capability. This is insufficient evidence, **not absence** of the capability.
- Short quotes from S01–S16 have not yet been re-checked word for word against the live pages. The reviewer must open the URLs and check a sample of claims (DISC-02-01 verification) before any cell is treated as reviewed.
- App-store listings show day and month of the last update but not the year; versions are recorded instead.
- Prices are recorded with their source date. Prices older than the access date are **historical** and must not guide budgeting.
- Differentiation can only be supported after comparing alternatives relevant to users (DISC-02-02) and cross-checking with [user research](03-user-research.md).

## 2. Selected alternatives

The set is bounded to what a Portuguese condominium administrator could plausibly use today for fault coordination. It is not a market census.

| Group | Alternative | Why it is relevant to the proposed segment | Role in this analysis |
|---|---|---|---|
| Informal practice | Calls, SMS, WhatsApp/neighbourhood groups, email, spreadsheets and paper | Hypothesised current process for residents, administrators and contractors | Compared; evidence must come from interviews (DISC-01) |
| Condominium suite, Portugal | [SolidSoft GC](https://pplware.sapo.pt/software/solidsoft-gc-o-software-para-gestao-de-condominios-a-sua-medida/) · [Owner app](https://apps.apple.com/us/app/-/id6473123549) | A Portuguese condominium-management platform with dedicated apps for owners and technicians, allowing residents to report issues and technicians to manage and track their work. | Compared |
| Condominium suite, Portugal | [Gecond (Improxy)](https://apps.apple.com/pt/app/gecond-o-meu-condom%C3%ADnio/id1541353491) | Portuguese condominium-management software with an owner app for reporting faults and tracking their resolution | Compared |
| Condominium suite + smart building | [Unitify](https://unitify.com/smart-building/portugal) | Targets the Portuguese market with a platform that combines building management services with resident requests. According to its latest product update, it uses AI to classify requests, assess their urgency and assign them accordingly. | Compared |
| Comparable maintenance product | [Fixflo (Block)](https://www.fixflo.com/solutions/block-management) | A UK-focused platform that helps property managers handle repair requests and coordinate contractors for apartment buildings. | Compared |
| Comparable maintenance product | [Infraspeak](https://www.infraspeak.com/pt-pt) | Portuguese-origin maintenance and facilities-management platform, relevant to work orders, suppliers and preventive maintenance | Compared |
| Generic helpdesk | [Freshdesk](https://www.freshworks.com/freshdesk/) | General-purpose helpdesk that could be adapted to condominium maintenance; useful for comparing ticketing and business model rather than domain-specific workflows | Compared on business model and ticketing only |
| Service marketplace, Portugal | [Zaask](https://www.zaask.pt/como-funciona) | Gives an administrator without an established contractor a way to request and compare service quotes | Compared |

Secondary references from Brazil (CondoBOM, Manu, In Motion CONDOS; S06–S08) have similar workflows but no evidence of availability or support for Portugal. They are kept in section 2.2 and in the register for context only and are outside the matrix.

### 2.1. Informal practices [Hypotheses to validate]

| Alternative | Users | Potential advantage | Limitation to investigate |
|---|---|---|---|
| Calls, SMS, WhatsApp and email | Residents, administrators and contractors | Familiarity and low initial adoption effort | Message history may not structure statuses, responsibilities and decisions |
| Neighbourhood groups | Residents | Fast communication and local knowledge | Noise, repetition and information exposure |
| Spreadsheets, paper and incident logs | Administrators and caretakers | Flexibility and simple record-keeping | Effort required to update, consult and share |
| Established contractor contacts | Administrators | Trust and knowledge of the building | Dependence on individuals and availability; comparisons may be manual |

No public source was verified for this group: actual usage, cost and difficulties are interview questions (Q1 and Q6 in [03](03-user-research.md)). Better to not assume that everyone uses the same channels or that the current process is always inferior.

### 2.2. Products — what the sources say

IDs refer to the [register](#5-source-and-findings-register). Everything below is a supplier claim or advertising unless marked UR.

| Product | Market / users stated | Capabilities stated | Not described in the sources opened |
|---|---|---|---|
| SolidSoft GC | Portugal; “domestic or professional” use; owners, administration and maintenance technicians (S01) | Owners report faults with a photo, saved offline (S01, S02). Technician app: daily routes by building, QR/NFC check-in, products used, respond to pending interventions (S01, S03). Documents, assemblies and voting, balances, MB WAY/Multibanco/Payshop (S01, S02). RGPD compliance claim (S01, S18). Professional plan €1590/year or €159/month, 14-day trial (S17) | Urgency triage, duplicates, status visible to the reporting owner, AI |
| Gecond (Improxy) | Portugal; administrations using Gecond; owners by invitation only (S09) | Owners report faults and track their resolution; assemblies and advance voting (S09). Field occurrence management with technicians; supplier invoices read by QR code (S10) | Triage, duplicates, contractor dispatch/acceptance, pricing, AI |
| Unitify | Management companies, developers and residents; Portugal page (S04) | Resident app with requests; access control, intercoms, meters; quotas with Multibanco, MB WAY and card (S04). Requests typed, tagged and urgency-scored by AI, auto-assigned to the technician for that issue type; AI drafts replies; technician calendar and Kanban (S05). AI-drafted maintenance plans (S04). Homepage states AI decisions require human approval (S20). Free, Base and Pro plans priced per apartment (S19) | How review and correction work for each triage step, duplicates, external contractors and their acceptance, cost recording, GDPR statement on the Portugal pages |
| Fixflo (Block) | UK block and property managers, leaseholders, residents and contractors (S11) | Multilingual picture-based reporting with photo/video and self-help pop-ups; automatic progress updates; time-stamped audit trail; automated contractor instruction and multiple quote requests; contractor app and marketplace; planned maintenance; AI assistant for repairs (S11, S12, S23); tenants review and confirm or edit an AI-generated report summary before submitting (S24) | Duplicate detection, explicit triage rules, contractor acceptance flow, Portuguese market support |
| Infraspeak | Facility management providers and in-house teams; residential condominiums not mentioned (S13) | Work orders, schedules and approvals; preventive maintenance; supplier management and network; procurement; AI to “predict and prevent” failures; mobile apps (S13) | How requesters report faults, prices, free trial |
| Freshdesk | General customer support teams (S14) | Ticketing, automations and role-based access on all listed plans; AI agent sessions included (S14) | Any building, contractor or maintenance concept; duplicate handling was not checked in a primary source |
| Zaask | Portugal; individuals requesting services and professionals bidding (S15, S16) | Free request; up to five quotes; customer compares profiles and reviews and chooses; optional payment held until the customer confirms completion; reviews (S15) | Job status tracking after hiring, multi-party visibility, history per building |
| CondoBOM (Brazil) | Managers, doormen and residents; Portuguese-language app (S06) | Occurrence log, maintenance schedules, reservations, visitors, packages, polls, documents, billing, supplier tenders (S06) | Dispatch, availability for Portugal |
| Manu (Brazil) | Condominium managers (S07) | Asset mapping, preventive routines, supplier links, maintenance history, account manager (S07) | Handling of unplanned faults reported by residents |
| In Motion CONDOS (Brazil) | Managers, caretakers, technicians, residents (S08) | Residents open corrective requests by QR code with photos; routing to the responsible provider; mobile work orders; preventive plans; history (S08) | Current status of a 2020 product description |

## 3. Comparison matrix

Each cell is “**Claimed** (source ID)” or **UC**. “Claimed” means the vendor or an advertising text states it; nothing was tested. “Not described” in a cited source is still UC, not absence. The BMC column describes **plans**, not implemented capabilities; scope and priorities are in [04 Vision](04-product-vision.md) and [06 Backlog](06-product-backlog.md). Interpretation of this matrix belongs to DISC-02-02.

| Criterion | SolidSoft GC | Gecond | Unitify | Fixflo (Block) | Infraspeak | Freshdesk | Zaask | Proposed BMC |
|---|---|---|---|---|---|---|---|---|
| Reporting and follow-up | Claimed: reporting (S01, S02); follow-up for the owner UC | Claimed: report and track resolution (S09) | Claimed: requests become scored, tagged tickets (S04, S05) | Claimed: reporting and automatic progress updates (S11) | Claimed: work orders (S13); requester reporting UC | Claimed: ticketing (S14) | Claimed: quote request (S15); follow-up after hiring UC | Text, statuses and history |
| Photographs | Claimed (S01, S02) | Photos listed in privacy label (S09); one UR reports upload failing (S09) | UC | Claimed: photo and video (S11) | UC | UC | UC | Post-MVP |
| Urgency triage | UC | UC | Claimed: AI type, tags and urgency score (S05); human approval claimed (S20), review/correction per step UC | UC; AI repairs assistant claimed (S23), tenant confirms or edits AI summary (S24); urgency scoring UC | UC; predictive AI claimed for assets (S13) | UC; AI agent claimed without detail (S14) | UC | Assisted AI, rules and review |
| Duplicates | UC | UC | UC | UC | UC | UC | UC | Should; reviewed association |
| Contractors and dispatch | Claimed: technicians notified, routes, QR/NFC, pending interventions (S01, S03) | Claimed: field occurrences with technicians (S10) | Claimed: auto-assignment to internal technician by issue type (S05); external contractors UC | Claimed: automated instruction, multiple quotes, contractor app, marketplace (S11, S12) | Claimed: supplier management and network (S13) | UC | Claimed: up to five quotes, customer chooses (S15) | Small catalogue; approval and response |
| External calendar | UC | UC | UC; technician-app calendar only (S05) | UC; scheduling of planned events (S11) | UC | UC | UC | Realistic simulator; real provider optional |
| Cost recording | Claimed: products used by technicians (S01, S03) | Claimed: supplier invoices by QR (S10) | UC | Claimed: quotes and invoices (S12) | Claimed: procurement, accounting integrations (S13) | UC | Claimed: optional held payment (S15) | Basic, optional |
| Financial analysis / summaries | Claimed: condominium accounts (S01) | UC | UC | Claimed: dashboards and KPIs (S12) | UC | UC | UC | Post-MVP |
| Preventive maintenance | Claimed: maintenance routes (S01, S03) | UC | Claimed: AI-drafted maintenance plans (S04) | Claimed (S11, S12) | Claimed (S13) | UC | UC | Outside the current baseline scope |
| Fees, assemblies and payments | Claimed (S01, S02) | Claimed: assemblies and voting (S09) | Claimed: quotas and payments (S04) | UC | UC | UC | UC | Outside the current baseline scope |
| Hardware / meters | UC | UC | Claimed (S04) | UC | UC | UC | UC | IoT pending DEC-01 |

Also evaluate the informal process in section 2.1 using equivalent tasks; do not assign absolute capability gaps merely because it lacks specialised structure.

## 4. Business models, usability and trust

| Dimension | What the sources state | Verification still needed |
|---|---|---|
| Business models | SolidSoft GC: the **€120/year** Home Edition price was reported in a **2023 promotional article** ([S01](https://pplware.sapo.pt/software/solidsoft-gc-o-software-para-gestao-de-condominios-a-sua-medida/)); it is historical, not the current price. The current [official pricing page](https://www.gcsoftware.pt/en/pricing/) (S17) lists Professional Plan at **€1590/year** and **€159/month**; it also advertises a 14-day free trial. The [owner app](https://apps.apple.com/us/app/gc-cond%C3%B3minos-condom%C3%ADnios/id6473123549) (S02) and [technician app](https://apps.apple.com/pt/app/gc-t%C3%A9cnicos-condom%C3%ADnios/id6477870167) (S03) are listed as free downloads; access to the owner app requires a building managed with GC. Unitify: the [current pricing page](https://unitify.com/pricing) (S19) lists Free, Base (**US$0.50/apartment/month**) and Pro (**US$1.50/apartment/month**) plans, plus a 30-day trial for paid plans. The [Portugal page](https://unitify.com/portugal) (S21) says its white-label branding is a paid option. Fixflo Block: [price on request, plus a £75/month software fee](https://www.fixflo.com/pricing/block-management) (S22); the same page states a minimum of 50 properties and says prices exclude VAT, setup fees and integration costs. Infraspeak: its [official pricing page](https://infraspeak.com/en/pricing) (S25) does not publish plan prices and invites prospective customers to find a suitable plan; it does not establish whether a free trial is available. Freshdesk: the [official pricing page](https://www.freshworks.com/freshdesk/pricing/) (S14) lists **US$19 / US$55 / US$89 per agent/month, billed annually**, and a 14-day trial. It also advertises a Free Program for up to two agents for six months. Zaask: customer use is free, while professionals use purchased credits to bid; see [customer information](https://zaask.zendesk.com/hc/pt/articles/360029628111-Como-posso-ter-uma-no%C3%A7%C3%A3o-de-quanto-custa-um-servi%C3%A7o) (S26) and the [professional credit system](https://www.zaask.pt/sistema-de-creditos) (S16). | Confirm current offers, billing units, taxes and availability for Portugal, especially for Gecond and the Brazil-focused products. Validate who would buy and pay, and include adoption and migration costs (DEC-02). A free app download is not evidence that the related service is free. |
| UX | No equivalent task or hands-on product test was performed for this analysis. On the [Portuguese App Store listing](https://apps.apple.com/pt/app/gecond-o-meu-condom%C3%ADnio/id1541353491) (S09), Gecond’s owner app showed **1.9/5 from 37 ratings** when checked on **2026-10-15**. Some visible reviews report login problems, missing features or difficulty uploading photos; these are user reviews, not usability-test results. The [GC owner app](https://apps.apple.com/us/app/gc-cond%C3%B3minos-condom%C3%ADnios/id6473123549) and [GC technician app](https://apps.apple.com/pt/app/gc-t%C3%A9cnicos-condom%C3%ADnios/id6477870167) did not have enough ratings to display an overview on the listings reviewed. | Run equivalent tasks in each product and record completion time, errors and assistance. Ratings and self-selected reviews are not representative usability studies; record the date of any rating snapshot. |
| Privacy | SolidSoft GC’s [privacy policy](https://www.gcsoftware.pt/en/privacy-policy/) (S18) says it aims to comply with applicable data-protection law, including the GDPR. The [GC owner-app listing](https://apps.apple.com/us/app/gc-cond%C3%B3minos-condom%C3%ADnios/id6473123549) (S02) displays the developer’s “Data Not Collected” privacy disclosure. Gecond’s [App Store listing](https://apps.apple.com/pt/app/gecond-o-meu-condom%C3%ADnio/id1541353491) (S09) says the developer indicates that contact information and user content may be collected and linked to the user. CondoBOM’s [App Store listing](https://apps.apple.com/il/app/condobom/id6449686523) (S06) displays developer-provided privacy information, including location, contact information and photos/videos. Apple explains that app privacy information is supplied by developers on its [privacy-label information page](https://www.apple.com/privacy/labels/) (S27). Unitify’s [Portugal page](https://unitify.com/portugal) (S21) links to a privacy policy; the page itself is not evidence of an independent GDPR-compliance assessment. | Verify actual data flows, role-based visibility, retention, deletion, processors and demonstrable security controls. Vendor statements and app-store privacy disclosures are not compliance audits. |
| Trust in AI | Unitify’s [July 2026 product update](https://unitify.com/blog/whats-new-in-unitify) (S05) claims AI classification, tags, urgency scoring, reply drafting and automatic assignment. Its [homepage](https://unitify.com/) (S20) says AI decisions require human approval, but the pages do not clearly explain exactly how review and correction work for each request-triage step. Fixflo describes its Aidenn repairs assistant on its [official product page](https://www.fixflo.com/solutions/aidenn-ai-repairs-maintenance) (S23); its [AI reporting help article](https://help.fixflo.com/support/solutions/articles/61000319589-fixflo-ai-reporting-what-tenants-see-when-they-report-an-issue) (S24) says tenants can review and confirm or edit a report summary before submitting it. Infraspeak describes intelligent suggestions, predictions and alerts on its [platform page](https://infraspeak.com/pt-pt) (S13), but the source does not specify review and approval controls for each AI feature. Freshdesk lists Freddy AI Agent features and included sessions on its [official pricing page](https://www.freshworks.com/freshdesk/pricing/) (S14); that page is not a detailed account of human review for every AI response. | Compare what each AI feature decides or generates, what users can inspect or correct, and when a person takes over. **BMC must not claim exclusivity in AI triage.** |

BMC's commercial model is a [product hypothesis](04-product-vision.md#8-business-model), to validate in DEC-02. Its access policy is defined in the [security assessment](09-security-privacy.md#2-proposed-access-matrix), not by automatically copying a competitor.

## 5. Source and findings register

S01–S16 accessed on 2026-10-13; S17–S27 accessed on 2026-10-15, when S09 and S14 were also re-checked. Evidence types are defined in section 1.

| ID | Product and plan/version | Exact URL | Source date | Observed capability or limitation | Evidence type | Consequence for BMC |
|---|---|---|---|---|---|---|
| S01 | SolidSoft GC; domestic and enterprise editions | https://pplware.sapo.pt/software/solidsoft-gc-o-software-para-gestao-de-condominios-a-sua-medida/ | 2023-06-14 | Fault reporting with photo, “grava offline”; technician QR check-in and routes; documents, assemblies, payments; RGPD claim; “a partir de 120€/ano para o plano doméstico” | AD — promotional editorial, not labelled as sponsored | A Portuguese suite already claims report-to-technician flow; price is historical |
| S02 | GC Condóminos, iOS v7.5.7, free | https://apps.apple.com/us/app/-/id6473123549 | Updated 29 May, year not shown | Owners: account, receipts, meetings and voting, issue reporting with photos; requires a building managed with GC; “Data Not Collected” label | SC | Reporting is bundled in a suite the administration must already use |
| S03 | GC - Técnicos, iOS v5.5.8, free | https://apps.apple.com/us/app/-/id6477870167 | Updated 30 May, year not shown | Daily routes, QR/NFC visit confirmation, products used, report issues with photos, respond to pending interventions; access activated by the managing company | SC | Technician execution is covered; triage and approval steps are not described |
| S04 | Unitify, Portugal offering; plan not stated | https://unitify.com/smart-building/portugal | Undated; footer © 2026 | Resident app with “requests”; access control, intercoms, meters; quotas via Multibanco, MB WAY, card; “AI-drafted maintenance plans”; no prices on this page (see S19), no GDPR statement | SC | Broad suite with hardware; request workflow not detailed on this page |
| S05 | Unitify product update | https://unitify.com/blog/whats-new-in-unitify | 2026-07-09 | “Requests are prioritized by urgency score and automatically assigned to the technician responsible for that issue type”; AI identifies type, adds tags, drafts reply; technician calendar and Kanban. Human review, duplicates, external contractors and costs not mentioned | SC | AI-assisted triage is claimed by a competitor marketed in Portugal |
| S06 | CondoBOM, iOS v6.12.1, free (Winplex) | https://apps.apple.com/il/app/condobom/id6449686523 | Updated 3 July, year not shown | Occurrence log, maintenance schedules, reservations, visitors, billing, supplier tenders; Portuguese-language; privacy label: location, name, photos/videos | SC | Secondary reference; Portugal availability unknown |
| S07 | Manu; Digital and Essencial plans | https://www.sindiconet.com.br/informese/manutencao-do-condominio-na-palma-da-mao-mercado-coluna-de-olho-no-mercado | 2022-03-09 | Asset mapping, preventive routines, supplier links, history; “R$ 59,90 por mês” and “R$ 89,90 mensais” | AD — column declared as “informes publicitários” | Preventive focus; prices historical |
| S08 | In Motion CONDOS (Byte in Motion) | https://www.sindiconet.com.br/informese/gestao-da-manutencao-do-condominio-coloque-a-casa-em-ordem-mercado-coluna-de-olho-no-mercado | 2020-06-15 | Residents open corrective requests by QR code with photos; routing to provider; work orders; “R$ 6,00 por unidade” per month and “R$ 2.000” setup | AD — column declared as “informes publicitários” | New lead found during verification; old, secondary reference |
| S09 | Gecond, o meu condomínio, iOS v4.9.5, free (Improxy) | https://apps.apple.com/pt/app/gecond-o-meu-condom%C3%ADnio/id1541353491 | Updated 9 September, year not shown | Report faults and track resolution; assemblies and voting; “apenas disponível aos condóminos por convite”; 1.8/5 from 38 ratings on 2026-10-13 and 1.9/5 from 37 ratings on 2026-10-15; reviews (2021, 2022 and undated) on login, lost features, photo upload | SC + UR | A second Portuguese suite covers report and follow-up; public reviews suggest usability problems to investigate |
| S10 | PRO Gecond, iOS v4.7.5, free (Improxy) | https://apps.apple.com/us/app/id1574891458 | Updated 29 July, year not shown | “Gestão de ocorrências no terreno” with field staff and technicians; supplier invoices read by QR code; restricted to Gecond users | SC | Field handling and supplier costs are claimed |
| S11 | Fixflo Block; tiers Basic, Essentials, Professional, Manager | https://www.fixflo.com/solutions/block-management | Undated | Multilingual picture-based reporting, photo/video, self-help pop-ups, automatic progress updates, audit trail, automated contractor instruction, multiple quotes, planned maintenance, AI assistant; UK regulation context | SC | Closest functional comparable for report → instruct contractor; not targeted at Portugal |
| S12 | Fixflo, lettings pricing | https://www.fixflo.com/pricing/lettings | Undated | Price on request “+ a £75 software fee/month”; minimum 50 properties; contractor marketplace “From £0.30 per unit per month”; quotes and invoices; contractor app | SC | Per-unit pricing with a floor suggests small buildings are not the target; block pricing is S22 |
| S13 | Infraspeak, platform homepage (pt-PT) | https://www.infraspeak.com/pt-pt | Undated | Work orders, preventive maintenance, supplier management and network, procurement, AI “Prever e prevenir avarias”; sectors listed exclude residential condominiums; demo only | SC | Maintenance depth exists in Portugal for facility management; resident reporting not described |
| S14 | Freshdesk; Growth, Pro, Enterprise | https://www.freshworks.com/freshdesk/pricing/ | Undated | $19, $55, $89 per agent per month billed annually; 14-day trial; ticketing, automations, role-based access; AI agent sessions included; on 2026-10-15 also a Free Program for up to two agents for six months | SC | A generic helpdesk is cheap per agent but has no domain concepts in the page opened; adaptation effort unknown |
| S15 | Zaask, customer flow | https://www.zaask.pt/como-funciona | Undated | Free request, up to five quotes, customer chooses, optional payment held until completion is confirmed, reviews; Zaask gives no guarantee on services | SC | Covers contractor discovery, not coordination or history |
| S16 | Zaask, credit system for professionals | https://www.zaask.pt/sistema-de-creditos | Undated | Professionals spend credits to bid; cost varies by category and request quality; maximum five bidders | SC | Contractors bear the acquisition cost; relevant to P6 and the catalogue-versus-marketplace hypothesis |
| S17 | SolidSoft GC, pricing (Professional plan) | https://www.gcsoftware.pt/en/pricing/ | Undated | Professional plan €1590/year or €159/month; 14-day free trial | SC | Current price replaces the historical S01 figure for budgeting comparisons |
| S18 | SolidSoft GC, privacy policy | https://www.gcsoftware.pt/en/privacy-policy/ | Undated | States it aims to comply with applicable data-protection law, including the GDPR | SC | A compliance statement, not an audit |
| S19 | Unitify, pricing | https://unitify.com/pricing | Undated | Free, Base (US$0.50/apartment/month) and Pro (US$1.50/apartment/month) plans; 30-day trial for paid plans | SC | Per-apartment pricing is a reference point for DEC-02 |
| S20 | Unitify, homepage | https://unitify.com/ | Undated | States that AI decisions require human approval; review and correction per triage step not explained | SC | Human-in-the-loop AI is also claimed by a competitor |
| S21 | Unitify, Portugal page | https://unitify.com/portugal | Undated | White-label branding offered as a paid option; links to a privacy policy | SC | Not evidence of an independent GDPR assessment |
| S22 | Fixflo, block-management pricing | https://www.fixflo.com/pricing/block-management | Undated | Price on request plus £75/month software fee; minimum 50 properties; prices exclude VAT, setup fees and integration costs | SC | Floor of 50 properties suggests small administrators are not the target |
| S23 | Fixflo, Aidenn AI repairs assistant | https://www.fixflo.com/solutions/aidenn-ai-repairs-maintenance | Undated | AI assistant for repairs and maintenance reporting | SC | AI-assisted reporting exists in the closest comparable |
| S24 | Fixflo help centre, AI reporting | https://help.fixflo.com/support/solutions/articles/61000319589-fixflo-ai-reporting-what-tenants-see-when-they-report-an-issue | Undated | Tenants review and confirm or edit an AI-generated report summary before submitting | SC | Reporter-side correction of AI output is claimed; urgency triage still UC |
| S25 | Infraspeak, pricing | https://infraspeak.com/en/pricing | Undated | No plan prices published; prospective customers are invited to find a suitable plan; free trial not stated | SC | Pricing remains unknown |
| S26 | Zaask help centre, service cost for customers | https://zaask.zendesk.com/hc/pt/articles/360029628111-Como-posso-ter-uma-no%C3%A7%C3%A3o-de-quanto-custa-um-servi%C3%A7o | Undated | Customer use is free; service cost depends on the quotes received | SC | Confirms S15: the customer does not pay Zaask |
| S27 | Apple, app privacy labels | https://www.apple.com/privacy/labels/ | Undated | App privacy information is supplied by developers | PD | App-store privacy labels (S02, S06, S09) are self-declared |

### Unavailable sources and access limits

| Item | What happened | Treatment |
|---|---|---|
| GC Companies app listing (`apps.apple.com/app/id6449394940`) | HTTP 404 on 2026-10-13 | Plan limits seen only in a search snippet are **not** recorded as evidence |
| Gecond vendor product page | Not located; a guessed address on improxy.pt returned 404 | Gecond is supported only by app-store listings; pricing unknown |
| Gecond pricing on software directories | Seen only as a search snippet, page not opened | Not recorded as evidence |
| WhatsApp help page on communities (`faq.whatsapp.com/495856382464992`) | Only the title was retrieved | No product source for the informal channel; rely on interviews |
| Freshdesk duplicate/merge handling | Only third-party blogs found | Left UC |
| Demos and trials (all products) | Not requested; paid trials are excluded by DISC-02-01; GC and Gecond apps need an account issued by an administration | No observed behaviour; a demo request is a possible follow-up |
| Android listings and non-Portuguese App Store storefronts | iOS listings only; S02, S03, S06 and S10 opened on non-PT storefronts | Availability and ratings in Portugal not confirmed for those apps |

Record new evidence here and reference its ID in the matrix. Do not create entries from memory of pages or from unverified content.

## 6. Differentiation hypothesis

The [value proposition](04-product-vision.md#1-vision-and-value-proposition) depends on demonstrating lower administrative effort, without assuming exclusivity in AI, traceability or scheduling.

Hypotheses to test:

- Simplicity may reduce contacts and active time.
- Explanations and correction may support decisions.
- Companies may prefer integration with existing software over replacement.
- An established catalogue may be more useful than a marketplace.
- A suite may already cover the workflow or add it; focus and speed alone do not demonstrate a defensible advantage.

If competitors cover the essentials, revisit positioning using evidence; do not automatically switch to cost analysis without investigating that need.

### Observations from source verification (input to DISC-02-02, not conclusions)

- Two Portuguese suites claim resident fault reporting (S01, S02, S09), and one claims follow-up of resolution (S09). Reporting alone is unlikely to differentiate BMC.
- Unitify claims AI classification, urgency scoring and auto-assignment (S05) and states that AI decisions require human approval (S20), without explaining how review and correction work per step. Fixflo lets tenants confirm or edit an AI summary (S24). Reviewed, explainable triage remains a hypothesis to compare, not an exclusive capability.
- No source opened describes duplicate-report handling, or a request → contractor acceptance → booking confirmation chain with an external contractor. This is **unconfirmed, not absent**; a demo would be needed before claiming a gap.
- Fault reporting in the Portuguese suites is tied to the administration already using that suite (S02, S09). This supports testing the “integrate rather than replace” hypothesis in DEC-02.
- Public reviews of one owner app point to usability problems (S09). The sample is small and self-selected.

## 7. Next actions

1. Reviewer opens the register URLs and checks a sample of cells against them (DISC-02-01 verification).
2. DISC-02-02: interpret the matrix, complete strengths/weaknesses and UX per §5.2, and state differentiation as supported conclusions or remaining hypotheses.
3. Decide whether to request demos of SolidSoft GC, Gecond or Unitify; document observed tasks and access limits.
4. Cross-check with [user research](03-user-research.md) which tools participants actually use (Q6).
5. Revise vision and priorities; record decisions under [DEC-02](planning/decisions-and-feedback.md) and work under DISC-02 in the [backlog](06-product-backlog.md).
