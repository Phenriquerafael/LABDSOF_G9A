# Security and Privacy Assessment

**Status:** proposed initial assessment · Sprint 1, deliverable 9 · controls not implemented/verified

## 1. Context and assets

Assets: identity/membership, private text, published summary, location, proposals, schedules, costs, credentials, events and history. Boundaries: client→API, service→service, broker, database, AI/calendar provider and research repository.

The MVP uses synthetic demonstration data. Real interviews still require a purpose, participation permission and their own data management. This proposal does not claim legal compliance; legal issues and institutional policies need appropriate review before a real pilot.

## 2. Proposed access matrix

| Operation/data | Resident | Administrator | Contractor | Enforced in |
|---|---|---|---|---|
| Create report | Buildings they belong to | Managed buildings, with source recorded | Outside baseline | Issue |
| Raw report text | Own | Managed buildings | Only necessary extract in the assigned request | Issue; Dispatch stores only the administrator-written extract |
| Published shared summary | Same building | Managed buildings | Context needed for the request | Issue |
| Confirmed category/urgency | Authorised viewing | Confirms/corrects | Views assigned request | Issue; Dispatch for the contractor's view |
| Confirm impact | Same building; own contribution | Views counter | No | Issue |
| Proposal/approval | No | Managed buildings, one version at a time | Responds only to assigned request | Dispatch, with Issue context |
| Counterproposal | No | Approves or replaces it | Proposes on the assigned request only | Dispatch |
| Booking/completion | Authorised public status | Coordinates/validates | Assigned request | Dispatch |
| Manual booking confirmation | No | Managed buildings, with source and reason | No | Dispatch, with Issue context |
| Rework / cancel intervention | No | Managed buildings, with reason | No | Dispatch, with Issue context |
| Cost | No access by default | Managed buildings | Proposes/views cost of own work | Dispatch |
| Close/cancel/reopen issue | No | With reason according to transition | Reports completion, without closing | Issue |
| Data from another building/request | No | Only if explicitly authorised | No | Both |
| Internal endpoints | No | No | No | Service tokens with the right audience |

Each service enforces the rows it owns. Dispatch takes only the user identity from the token: contractor assignment is checked against Dispatch's own records, and administrator rights over an issue's building are fetched from Issue for every command. If Issue cannot answer, the command fails closed ([design §4.3](07-technical-design.md#43-how-dispatch-obtains-trustworthy-authorisation-context)). Resources outside the caller's scope answer `404`, not `403`, to avoid enumeration.

Check in the backend for each operation; hiding buttons is insufficient. Mock authentication identifies predefined test users, but does not allow the client to choose arbitrary privileges. Internal services are also authenticated/authorised.

## 3. Threats and checks

| ID | Threat / impact | Proposed control | Required evidence |
|---|---|---|---|
| T-01 | Change ID to read another building | Membership/resource authorisation and data projection | Negative API/list/search tests |
| T-02 | Contractor approves expenses or reads another request | Permissions and assignment checked on the server | Matrix tests |
| T-03 | Text induces AI to act/disclose | Apply [AI controls](06-responsible-ai-assessment.md#5-controls-and-communication) | [Adversarial cases and protocol](06-responsible-ai-assessment.md#3-proposed-dataset-and-protocol) |
| T-04 | Retry duplicates request/booking | Idempotency, versioning and reconciliation ([design §3.3](07-technical-design.md#33-invalid-and-concurrent-transitions), [§4.5](07-technical-design.md#45-calendarsimulator-contract-outline)) | Failures after external effects and repeated events |
| T-05 | Malicious text in UI | Safe rendering, input validation | Non-executable content tests |
| T-06 | Logs/payloads expose data | Minimisation, sanitisation and restricted access | Log and payload inspection |
| T-07 | Tokens/secrets in Git | Environment injection, review/secret checks | CI and review evidence |
| T-08 | Spam or excessive AI calls | Per-user/input limits, budget and limited retries | Limit and cost tests |
| T-09 | Data loss / component failure | Persistence, backup/restore, degraded states | Recovery exercise |
| T-10 | Changes without accountability | Minimal audit with actor, version and timestamp | Trace an intervention and correction |
| T-11 | Forged or stale authorisation context in Dispatch (client-supplied building or role, membership revoked after a check) | Context from Issue's internal API for each administrator command; no client-supplied authority; read-only cache of at most 30 s; fail closed | Negative cases W5–W7 in the [contract annex](07a-contract-examples.md#3-review-walkthrough) |

Assess likelihood and impact with the team after defining deployment; do not assign a residual risk rating without validating controls.

## 4. Data lifecycle and minimisation

| Data | Proposed collection/access | Retention/deletion |
|---|---|---|
| Demo fixtures | Synthetic, without real people/addresses | Reproducible reset; retain only necessary fixtures |
| Reports/interventions | Minimal text and area reference; restricted private details | Period and rules to be finalised in DEC-07 before a pilot |
| Logs/audit | Necessary metadata, without full text/secrets | Period, access and deletion to be defined with the environment |
| Interviews | Anonymous answers only; no recordings, identity links or identifying metadata | Reviewed Markdown in Git; retained with academic project/history |
| Participant identities | Not collected in research records; no code-to-identity mapping | No participant database or identity archive |
| Data sent to a provider | Only what is necessary; synthetic during development | Review provider terms, configuration and retention before use |
| Backups | Restricted access and restore test | Define rotation and the effect of deletion requests |

A code alone does not anonymise an answer if its content still identifies someone. Git stores only anonymous answers after a check before the first commit; contacts, recordings, identifiable notes and consent attachments are excluded. Research controls are specified below; [DEC-07](planning/decisions-and-feedback.md#dec-07-research-preparation-disc-01-01) records the storage decision and alternatives.

### 4.1 Research data handling (DISC-01-01)

**Policy:** retain only anonymous answers in Git. The [collection procedure](templates/research-collection.md#3-consent-and-session-procedure) provides consent text and session steps; no participant database or identity mapping is used.

| Data | Collection and storage | Retention/access |
|---|---|---|
| Interview answers | Anonymous Markdown in `documents/research/answers/`; broad segment and record ID, no identity lookup | Retained with academic project/Git history; visible to repository readers, potentially public |
| Participation permission | Anonymous yes/no field for participation and Git storage; separate quotation permission | Same record, no signed consent forms or attachments |
| Names, contacts, addresses, companies, recordings | Not collected in research records | Never committed; distinctive contextual details omitted/generalised |
| Survey answers | No identifying questions, login, name/email collection or uploads; reviewed Markdown export only | Strip timestamps/metadata; delete working exports after checking and tool responses within seven days of checked export |
| Synthesis | Counts, limitations and decisions linked to anonymous answer IDs | Retained in Git; avoid combinations that identify a person/building |

Sandro owns research-record quality, Afonso owns method/synthesis under DEC-07, and Martim reviews anonymity. Session arrangements belong to the [collection procedure](templates/research-collection.md#2-future-sample-and-access); task ownership and synthesis review follow the [backlog allocation](backlog/README.md). Everyone with repository read access can read the answers; do not describe Git as restricted raw-data storage. Check repository visibility and communicate potential public access before participation. No fixed deletion deadline applies to retained anonymous answers: Git history, forks and clones prevent a promise of complete erasure.

| Risk | Control | Verification |
|---|---|---|
| Answers reveal identity without a name | Omit exact locations, companies, distinctive incidents and role/date combinations | Interviewer/note-taker check before first commit; Martim reviews before merge |
| Permission does not cover Git publication | Explain retention, readers/public visibility and history before questions | Affirmative anonymous participation/storage permission; no answer retained if refused |
| Survey export contains identifying metadata | No identifier collection; no unreviewed CSV/attachments | Synthetic settings test; strip timestamps, identifiers and incidental personal details |
| A code is mistaken for anonymisation | Document ID has no identity map; omit identifying context | Review content as well as fields; omit an answer if it remains identifiable |
| Deletion promise conflicts with Git history | Permit in-session corrections before confirmation; explain anonymous retention and copy limits | Consent and templates contain no identity-based post-publication withdrawal promise |

If identifying content is discovered, stop publication, remove it from working copies and inform Sandro/Martim. If already committed, assess history/copies and coordinate appropriate cleanup rather than treating a deletion commit as erasure. This policy does not authorise identifiable notes in Git.

## 5. Open questions and review plan

No actual interviews, participant permissions or independent approval of collection arrangements are evidenced by this documentation edit. The independent synthesis review of PR #39 requested changes; it does not establish collection approval.

- DEC-07: shared/private area boundary, summary publication, retention, deletion and participant access.
- DEC-04/05/06: identity, secrets and provider configuration.
- Before collecting data: check Git visibility/readership, anonymous collection and participation permission; Martim records the review.
- Before S2: isolation tests and approval workflow review.
- In S3: review threats/implemented controls, dependencies, results and residual risk; record limitations.
- Before a real pilot: review applicable obligations and policies; synthetic data does not prove suitability for real operation.

Traceability: [NFR-01/02/04/09](requirements.md), [backlog](05-product-backlog.md), [research](03-user-research.md).
