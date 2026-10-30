# ADR-005 — Keycloak identity, Backend-for-Frontend session and membership-based authorisation

**Status:** Proposed
**Date:** 2026-10-27
**Participants:** Ricardo (P2, Tech Lead) — proposer; team review pending; EN-01-04 security review required
**Related decision:** DEC-04; DEC-07 (visibility and data lifecycle)
**Supersedes / superseded by:** — (revised in place; the 2026-10-15 version proposed an own login and is in the Git history)

## Context

- §6.6 requires appropriate identity and access controls; its footnote allows mocked authentication for the MVP (E01). A mock stays legitimate, but it would show less of what the assignment asks for.
- NFR-01 requires the author/administrator/contractor/other-building matrix to be enforced and tested in the backend. The [access matrix](../09-security-privacy.md#2-proposed-access-matrix) defines the policy.
- EN-01-02 decisions that this ADR keeps: building memberships are owned by the Issue service and resolved server-side, tokens carry the user identity (`sub`) and never building roles, and every service authorises its own operations.
- The DISC-03-06 [workflows](../workflows/bmc-workflows.md) need self-service sign-up for administrators, residents (after an e-invite) and contractors (workflows 1, 2 and 9), email delivery of invitations, and validation of contractors by the project team. The 2026-10-15 own-login proposal excluded self-service sign-up and email-based recovery, so it covered neither.
- Browser-based applications that handle personal data should use a Backend-for-Frontend (BFF) rather than keep tokens in the browser; RFC 10017 (BCP 212) states this and requires PKCE for public browser clients (E30). Reports, locations and costs are personal or sensitive data in this product.
- Keycloak runs only on MySQL 8.4 or 8.0 (E27); 8.0 reached end of life on 2026-04-30 (E44), so the platform database is MySQL 8.4 LTS ([ADR-002](ADR-002-technology-stack.md)).

## Alternatives

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Keycloak + BFF at the edge: Traefik ForwardAuth → oauth2-proxy (confidential client `bmc-edge`), services as resource servers** | Maintained identity provider owns credentials, verification email and sign-up; no token in the browser (httpOnly cookie session); no authentication code in the services except JWT validation; documented Traefik integration | Two more containers; Keycloak base memory about 1250 MB (E28); a security-critical edge component the team configures but does not write; cookie size and `SameSite` behaviour to confirm in the spike | E16, E26–E32, E35 |
| B. Keycloak + SPA as a public PKCE client with `react-oidc-context` (tokens held by the SPA) | Better developer experience; no oauth2-proxy; works without ForwardAuth | Tokens live in browser memory or storage and are reachable by script injection (T-05); RFC 10017 recommends a BFF for applications handling personal data. **Recorded fallback** if the oauth2-proxy spike item fails | E30, E33 |
| C. Keycloak + `keycloak-js` in the SPA | Official Keycloak adapter | Same browser-token exposure as B; the React wrapper `@react-keycloak/web` was last published 2020-10-21 | E30, E33 |
| D. Spring Cloud Gateway as the BFF | Java, same stack as the services; session logic in code the team controls | Another JVM and another service to build and secure; Traefik already provides the edge and ForwardAuth | E18, E32 |
| E. Own login in the Issue service (argon2id, JWT in httpOnly cookies; the 2026-10-15 proposal) | No identity container; full control of claims | The team writes and maintains security-sensitive code; no sign-up, verification email or recovery; the workflows need all three | E03 |
| F. Mocked authentication (seeded users, no passwords) | Least effort; allowed by the §6.6 footnote | Weaker demonstration of §6.6; authorisation must still be real | E01 |
| G. Zitadel | Modern OIDC server | AGPL-3.0 licence; a second identity technology to learn without an advantage recorded here | E61 |

## Proposed or accepted decision

**A**, proposed, not accepted. B is the recorded fallback.

### What Keycloak owns and what the services own

| Concern | Owner |
|---|---|
| Accounts, credentials, login, sign-up, email address and its verification, password reset, coarse realm roles (`user`; `platform_staff` validates contractor registrations) | Keycloak (realm `bmc`) |
| User profile keyed by Keycloak `sub` (display name; no credentials), organisations, buildings, memberships (user × building × role), invitations | Issue |
| Contractors, contractor registrations, contractor-to-account link | Dispatch |
| Notification inbox, preferences, delivery log | Notification ([ADR-007](ADR-007-notification-service.md)) |

Tokens carry `sub`, issuer, audience and expiry; building roles never travel in a token and a client-supplied role or building is never authority. A global account grants no access by itself: a new `user` with no membership sees nothing.

### Browser session (BFF at the edge)

- The browser holds only an encrypted session cookie issued by oauth2-proxy (`keycloak-oidc` provider, confidential client `bmc-edge`, encrypted cookie session storage by default, Redis optional; E31). Cookie flags: `HttpOnly`, `Secure`, `SameSite=Strict`; the cookie secret comes from the environment.
- Traefik runs a ForwardAuth middleware against oauth2-proxy for `/api/*`. On success oauth2-proxy passes `Authorization: Bearer <access token>` upstream (E32); the service receives a normal bearer request. Traefik Proxy has no JWT middleware (that one is Traefik Hub only, E35), so Traefik does not validate the token itself.
- Single origin: Traefik routes `/` to the client's nginx, `/api/issue/*`, `/api/dispatch/*` and `/api/notifications/*` to the services, `/auth/*` to Keycloak and `/oauth2/*` to oauth2-proxy. Internal endpoints are never routed. There is no CORS.
- API routes use the no-auto-redirect behaviour, so an unauthenticated call returns `401` (E32). The SPA's session provider loads the session from `GET /api/issue/me`; on `401` it navigates to `/oauth2/start?rd=<path>`, which starts the authorisation-code flow with Keycloak and returns to the requested path.
- Logout, token lifetimes, refresh behaviour and cookie-secret rotation are open details (EN01-U6, EN-01-04).

### CSRF

`SameSite=Strict` on the session cookie, plus a required custom request header on every state-changing request (the client sets it; ForwardAuth or the service rejects the request without it). The header name and where it is enforced are an EN-01-04 detail. A cross-origin page cannot add a custom header without a CORS pre-flight, and there is no CORS.

### Resource servers

Every Spring service is an OAuth2 resource server (E16): it validates the JWT signature, issuer, audience and expiry, then authorises each operation itself against its own data — memberships in Issue, contractor assignment and the administrator projection in Dispatch, inbox ownership in Notification. The gateway is not the security control and hiding UI elements is never the control. Resources outside the caller's scope answer `404`, not `403`. Which audience value(s) the services require is open (a single API audience added by an audience mapper, or one per service); the `bmc-edge` audience mapper is needed anyway for oauth2-proxy (E31).

### Service accounts and broker credentials

- Notification → Keycloak Admin API with the client-credentials grant (E17): service account `notification-service` with the `view-users` role, only to look up an email address by `sub` at send time.
- Issue → Keycloak: no service account is planned; one is created only if the invitation flow proves to need it, with minimal rights.
- RabbitMQ: a separate user per service on the shared vhost, with least-privilege permissions on exchanges and queues ([ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)). No shared superuser credential anywhere; secrets come from the host or CI environment, never from Git.
- The old Issue↔Dispatch service JWTs and internal endpoints no longer exist: services talk only through RabbitMQ.

### Onboarding flows

Keycloak self-registration and email verification are enabled. Domain onboarding stays in the services (steps in the [setup guide](../guides/keycloak-setup.md#8-onboarding-flows-step-by-step)):

| Flow | Keycloak | Service |
|---|---|---|
| Condominium registration (workflow 1) | The user registers, verifies the email address and logs in | Issue: an authenticated call (endpoint to define in the EN-01-01 views) creates the organisation, building and administrator membership for the authenticated `sub` |
| Resident e-invite (workflow 2) | The invitee registers or logs in | Issue: administrator creates an invitation (hashed single-use token, 7 days, bound to a unit); a `NotificationRequested` email carries the link; the link carries the token in the URL fragment, and `POST /api/issue/invitations/acceptance` with the token in the body binds the membership to the `sub`, only if the token's verified `email` matches the invitee address (a forwarded link is refused with `403`) |
| Contractor registration (workflow 9) | The contractor registers and logs in | Dispatch: `POST /api/dispatch/contractor-registrations` creates a `pending` registration; a `platform_staff` user validates it |

**Rejected: Issue creating Keycloak users through the Admin API and sending `execute-actions-email`.** Creating a user through the API sends no email by itself; `execute-actions-email` does (E29, community source). The approach would give Issue realm-management rights, couple its invitation flow to Keycloak's mail templates, and bypass the notification facade, so invitations would be the one email the platform could not retry, log or switch off in one place.

These flows are DISC-03-06 scope additions that still need DEC entries and stories (EN01-U11).

### Realm as code

`infra/keycloak/bmc-realm.json` is imported with `--import-realm` (E29), which skips a realm that already exists. The file holds no secrets: client secrets, the admin password and SMTP settings come from the environment. Synthetic demo users exist only in the dev/demo profile. Keycloak sends verification email through SMTP to Mailpit in dev and demo (E52).

## Consequences

- **Memory:** Keycloak adds about 1250 MB of base memory per instance, and the heap defaults to 70% of the container limit, so a memory limit is mandatory (E28). The total footprint of the Compose stack must be measured in the spike ([ADR-004](ADR-004-deployment-contract.md), EN01-U3); this is the cost the 2026-10-15 version rejected Keycloak for.
- **Database:** Keycloak ties the platform to MySQL 8.4 (E27, E44). `sql_generate_invisible_primary_key` must be `OFF` and `binlog_format` must not be `STATEMENT`; MySQL 9.x is unsupported.
- **Revocation delay:** a user disabled in Keycloak keeps a valid access token until it expires (lifetime to set in EN-01-04). A membership revoked in Issue takes effect at once for Issue, but Dispatch authorises administrator commands from a projection fed by `MembershipRevoked`, so the delay equals event propagation (normally seconds; unbounded while Dispatch's consumer or the broker is down). This is inherited from the projection decision in [ADR-001](ADR-001-backend-boundaries.md) and [ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md) and is recorded as an EN-01-04 risk. Mitigations proposed there: projection freshness metric and "membership data as of …" in the UI.
- **Edge dependency:** if oauth2-proxy or Keycloak is down, no API call succeeds for a browser session (fail closed). Services that already hold a valid token are unaffected for validation, because the JWT is checked locally against the signing keys.
- **Security-sensitive configuration, not code:** cookie flags, redirect URIs, audience mapping and realm roles replace argon2id, token signing and rotation code. They need an EN-01-04 review and negative tests all the same.
- **Operations:** realm changes are made in `bmc-realm.json`; a changed file is not re-imported into an existing database (E29), so the dev procedure is a documented reset.
- **Swap path:** because the services are plain resource servers, another OIDC provider that issues the same claims replaces Keycloak without changing authorisation logic; option B replaces only the edge.

## Verification and review

- EN-01-04 reviews cookie flags, the CSRF header, token and session lifetimes, cookie-secret rotation, RabbitMQ per-service permissions, the revocation delay of the Dispatch projection (EN01-U6).
- Tests, written with the implementation: the full access matrix in each service; expired, forged and unsigned tokens; wrong issuer; wrong audience; missing custom CSRF header on a state-changing request; `401` (not a redirect) on an API call without a session; `404` for resources outside the caller's scope; invitation token reuse, expiry, wrong unit and address mismatch; contractor registration not usable before validation.
- Spike items (EN01-U2 in the [decision register](../planning/decisions-and-feedback.md)): **1** Keycloak 26.8 on MySQL 8.4 with realm import; **3** Traefik ForwardAuth → oauth2-proxy returns `401` to API calls and passes the bearer token. Also confirmed there: cookie size with the Keycloak tokens, `SameSite=Strict` through the login redirects, audience configuration. If item 3 fails, option B is adopted and this ADR and the setup guide are revised.
- Revisit before any real-user pilot.

## Record

- 2026-10-15 — first proposed by Ricardo (Tech Lead) after a structured design interview for EN-01-01: own login in the Issue service, argon2id password hashing, short-lived JWTs in httpOnly cookies, opaque rotating refresh tokens, service JWTs between Issue and Dispatch, membership-based authorisation; mocked authentication, Keycloak and Zitadel were the rejected alternatives.
- 2026-10-27 — revised by Ricardo (Tech Lead) after a structured design interview; drafting and source checks AI-assisted. Reason: the workflows need sign-up, email verification and invitation email, which the own-login proposal excluded; the stack moved to Java services (a Tech Lead proposal, not lecturer feedback), where a maintained identity provider and the Spring resource-server support are preferred to hand-written security code; the Keycloak memory cost is accepted pending measurement. Evidence: [evidence register](README.md#evidence-register-en-01-01) E01, E03, E16, E17, E26–E33, E35, E44, E52, E61; issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15). Affected documents: [security](../09-security-privacy.md), [technical design](../07-technical-design.md), [Keycloak setup guide](../guides/keycloak-setup.md), [workflows](../workflows/bmc-workflows.md), DEC-04. Final decision, date and participants: pending team review.
