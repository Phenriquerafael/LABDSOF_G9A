# Security and Privacy Assessment

**Status:** proposed initial assessment · Sprint 1, deliverable 9 · boundaries and controls revised on 2026-10-27 for the EN-01-01 proposal (ADR-001–010, team review pending) · controls not implemented/verified

## 1. Context and assets

Assets: identity/membership, browser sessions, private text, report photos, published summary, location, proposals, schedules, costs, invitation tokens and invitee addresses, credentials and secrets (Keycloak admin and clients, oauth2-proxy cookie secret, broker, database, object storage, SMTP), events in the broker and its dead-letter queues, and history.

Boundaries ([ADR-001](adr/ADR-001-backend-boundaries.md), [ADR-004](adr/ADR-004-deployment-contract.md), [ADR-005](adr/ADR-005-authentication-authorisation.md)): browser → Traefik, the only exposed container; Traefik → oauth2-proxy (ForwardAuth, browser session) → services with the bearer token; browser → Keycloak for sign-in and registration; service → RabbitMQ, the only path between services ([ADR-003](adr/ADR-003-asynchronous-messaging-rabbitmq.md)); service → its own database; Issue → object storage (Garage, [ADR-010](adr/ADR-010-object-storage.md)); Notification → Keycloak Admin API and SMTP; AI triage service → AI provider; Dispatch → calendar simulator; research repository. The broker, databases, object storage, internal endpoints and the simulator's scenario control are on internal networks and never routed.

The MVP uses synthetic demonstration data. Real interviews still require a purpose, participation permission and their own data management. This proposal does not claim legal compliance; legal issues and institutional policies need appropriate review before a real pilot.

## 2. Proposed access matrix

| Operation/data | Resident | Administrator | Contractor | Enforced in |
|---|---|---|---|---|
| Create report | Buildings they belong to | Managed buildings, with source recorded | Outside baseline | Issue |
| Raw report text | Own | Managed buildings | Only necessary extract in the assigned request | Issue; Dispatch stores only the administrator-written extract |
| Published shared summary | Same building | Managed buildings | Context needed for the request | Issue |
| Confirmed category/urgency | Authorised viewing | Confirms/corrects | Views assigned request | Issue; Dispatch for the contractor's view |
| Confirm impact | Same building; own contribution | Views counter | No | Issue |
| Proposal/approval | No | Managed buildings, one version at a time | Responds only to assigned request | Dispatch, with its projection of Issue's memberships and issue state |
| Counterproposal | No | Approves or replaces it | Proposes on the assigned request only | Dispatch |
| Booking/completion | Authorised public status | Coordinates/validates | Assigned request | Dispatch |
| Manual booking confirmation | No | Managed buildings, with source and reason | No | Dispatch, with its projection |
| Rework / cancel intervention | No | Managed buildings, with reason | No | Dispatch, with its projection |
| Cost | No access by default | Managed buildings | Proposes/views cost of own work | Dispatch |
| Close/cancel/reopen issue | No | With reason according to transition | Reports completion, without closing | Issue |
| Report photos (US-14 proposal) | Uploads to and views own report | Managed buildings | No; sharing into the extract is open and post-MVP | Issue; never served directly by object storage |
| Register a condominium | — | Any authenticated user may register one and becomes its administrator (DEC entry pending) | — | Issue |
| Invitations | Accepts an invitation addressed to them (holding the link) | Creates for managed buildings | No | Issue |
| Contractor registration | No | No | Submits own registration; validated only by the `platform_staff` realm role (project team) | Dispatch |
| Notifications and preferences | Own | Own | Own | Notification service |
| Data from another building/request | No | Only if explicitly authorised | No | All services |
| Internal endpoints and the broker | No | No | No | Never routed by Traefik; one broker credential per service |

Each service enforces the rows it owns. Dispatch takes only the user identity from the token: contractor assignment is checked against Dispatch's own records, and administrator rights over an issue's building are checked for every command against Dispatch's projection of Issue's membership and issue events. A missing projection row denies; a revocation takes effect once `MembershipRevoked` has been applied, so it is delayed by event propagation (T-12; [design §4.3](07-technical-design.md#43-how-dispatch-obtains-trustworthy-authorisation-context)). Resources outside the caller's scope answer `404`, not `403`, to avoid enumeration.

Check in the backend for each operation; hiding buttons is insufficient. The proposed identity is Keycloak with a Backend-for-Frontend session at the edge ([ADR-005](adr/ADR-005-authentication-authorisation.md)): oauth2-proxy, behind Traefik ForwardAuth, keeps the session in an encrypted httpOnly, Secure, SameSite=Strict cookie and passes the access token upstream; the browser never holds tokens. Every service is an OAuth2 resource server that validates the token (issuer, audience, expiry) and authorises each operation itself; the edge is not the security control. Tokens carry `sub` and coarse realm roles (`user`, `platform_staff`), never building roles; memberships are resolved server-side. Keycloak self-registration with email verification is enabled; invited residents and contractors register there. A mocked authentication would be allowed by §6.6 but is no longer the baseline; the 2026-10-15 own login is a rejected alternative. Services that call platform components use client-credentials service accounts with minimal rights (Notification: `view-users`), and each service has its own broker and database credentials; there is no shared superuser credential.

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
| T-11 | Forged or stale authorisation context in Dispatch (client-supplied building or role) | Authority only from the token's `sub` and Dispatch's projections of Issue's events; no client-supplied authority; a missing projection row denies; Issue validates every Dispatch event against its own records | Negative cases W5–W7 in the [contract annex](07a-contract-examples.md#3-review-walkthrough) |
| T-12 | Revocation delay: a revoked administrator keeps acting on Dispatch until `MembershipRevoked` is applied (normally seconds; unbounded while the broker or Dispatch's consumer is down) | Projection freshness metric and alert; “membership data as of …” in the UI; Issue rejects inconsistent Dispatch events; `IssueResolved`/`IssueCancelled` cancel interventions; a revocation-delay target and any staleness limit decided in EN-01-04 (EN01-U6) | W6 with the broker and with Dispatch's consumer stopped; measured delay against the target |
| T-13 | Session cookie theft or cross-site request forgery | Encrypted httpOnly, Secure, SameSite=Strict cookie; TLS at Traefik; required custom header on state-changing requests; cookie secret from the environment, with rotation and token lifetimes decided in EN01-U6 | Cookie flag inspection; cross-site and header-less requests rejected |
| T-14 | Private report text exposed through `TriageRequested` or its DLQ | Point-to-point binding to the AI triage service only; DLQ messages expire after 7 days; payloads never logged; management UI internal and restricted; synthetic data until the provider terms are checked (DEC-05, DEC-07) | Binding and DLQ configuration inspection; log inspection after a failed triage |
| T-15 | Invitation token exposed or reused (message, DLQ, logs, delivery log) | Only the token hash stored; single use; 7-day expiry; link only inside `NotificationRequested`; delivery log keeps neither address nor link; DLQ TTL 7 days; payloads never logged | Reuse and expiry tests; database and log inspection |
| T-16 | Photo metadata (EXIF/GPS) reveals a location, or a disguised file is uploaded (US-14 proposal) | Type verified by content; EXIF/GPS stripped before storage; count and size limits; random object keys; download only through Issue under the access matrix; storage never routed | Upload of a geotagged photo and of a disguised file; direct storage access denied |
| T-17 | Broker credential misuse (one service reads another's queue or publishes as another producer) | One credential per service with least-privilege permissions on `bmc.events` and its own queue; no shared superuser; management UI not exposed | Permission tests with each service credential |
| T-18 | Keycloak administration exposed or over-privileged | Admin password, client secrets and SMTP settings from the environment, not in the realm JSON; service accounts with minimal roles; admin console not reachable through the public route (configuration to confirm in the spike) | Route inspection; realm export review; service-account role review |

Assess likelihood and impact with the team after defining deployment; do not assign a residual risk rating without validating controls.

## 4. Data lifecycle and minimisation

| Data | Proposed collection/access | Retention/deletion |
|---|---|---|
| Demo fixtures | Synthetic, without real people/addresses | Reproducible reset; retain only necessary fixtures |
| Reports/interventions | Minimal text and area reference; restricted private details | Period and rules to be finalised in DEC-07 before a pilot |
| Logs/audit | Necessary metadata, without full text/secrets | Period, access and deletion to be defined with the environment |
| Interviews | Anonymous answers only; no recordings, identity links or identifying metadata | Reviewed Markdown in Git; retained with academic project/history |
| Participant identities | Not collected in research records; no code-to-identity mapping | No participant database or identity archive |
| Accounts | Email, credentials and verification in Keycloak only; services keep `sub` and profile data; Notification looks up addresses at send time and does not store them | Account deletion and its effect on profiles to be defined in DEC-07 |
| Invitations | Invitee email and token hash in Issue; the link only inside the invitation message | Retention of used and expired invitations to be defined in DEC-07 |
| Report photos (US-14 proposal) | EXIF/GPS stripped; same visibility as the private report text | Follow the report's retention (DEC-07); deletion must also remove the object |
| Messages in the broker | Transient; IDs and states only, except `TriageRequested` (report text) and invitation `NotificationRequested` (address and link) | DLQ messages expire after 7 days |
| Data sent to a provider | Only what is necessary; the report text reaches the AI provider through the AI triage service; synthetic during development | Review provider terms, configuration and retention before use (for Gemini, unpaid data may be used to improve products, but in the EEA/Switzerland/UK the paid-service data terms apply to unpaid quota, and users must be 18+: E63 in the [evidence register](adr/README.md#evidence-register-en-01-01)) |
| Backups | Restricted access and restore test; MySQL dumps copied to object storage | Define rotation and the effect of deletion requests |

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
- EN01-U6 (Martim with Ricardo, EN-01-04): oauth2-proxy cookie secret rotation, token lifetimes, the CSRF header, per-service RabbitMQ credentials, the revocation delay of Dispatch's projection, `TriageRequested` carrying private text and the invitation token in messages.
- Before collecting data: check Git visibility/readership, anonymous collection and participation permission; Martim records the review.
- Before S2: isolation tests and approval workflow review.
- In S3: review threats/implemented controls, dependencies, results and residual risk; record limitations.
- Before a real pilot: review applicable obligations and policies; synthetic data does not prove suitability for real operation.

Traceability: [NFR-01/02/04/09](requirements.md), [backlog](05-product-backlog.md), [research](03-user-research.md).
