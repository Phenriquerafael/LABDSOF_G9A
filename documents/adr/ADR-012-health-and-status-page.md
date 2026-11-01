# ADR-012 — Health checks and monitoring; public status page deferred

**Status:** Proposed
**Date:** 2026-11-01
**Participants:** Ricardo (P2, Tech Lead) — proposer; Martim (P5, DevOps/QA/security) to confirm; team review pending
**Related decision:** DEC-04; DEVOPS-02 ([#42](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/42))
**Supersedes / superseded by:** — (revised in place on 2026-11-01; see Record)

## Context

- §6.7 asks for health checks, metrics and a dashboard, and §6.8 for a degraded-mode scenario in which the degraded state is communicated to users (E01). Grafana ([ADR-004](ADR-004-deployment-contract.md)) serves operators; users need a plain-language view. In the MVP that view is the in-context messages of the client ([ADR-011](ADR-011-installable-pwa-client.md), [technical design §6](../07-technical-design.md#6-external-integration-and-degraded-mode)).
- Tech Lead requirement of 2026-10-27: every service exposes health, and the gateway serves a `/status` page with overall and per-component health. On 2026-11-01, after Martim's review of [PR #45](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/45), the Tech Lead dropped Gatus for the MVP and deferred the public status page; health on every service stays.
- DEVOPS-02 ([#42](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/42)) already plans `/healthz`, `/readyz` and `/status`. The endpoint names are Martim's decision; this ADR does not fix them and says “liveness and readiness endpoints, names per DEVOPS-02”.
- Services never call each other ([ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)), so any aggregator must live outside the business services. Only Traefik is exposed ([ADR-004](ADR-004-deployment-contract.md)).

## Alternatives

**MVP monitoring (2026-11-01)**

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **M1. Health endpoints, container health checks, Traefik load-balancer health checks, Prometheus `up` series and alerts, Grafana; no public status page** (chosen) | No extra container: Prometheus and Grafana are already in the stack; a service that has gone is visible per target; readiness enforced where routing and startup order need it | No public plain-language status view; users meet degraded states only in context; blackbox_exporter needed if readiness endpoints must be probed directly | E36, E39, E58, E73, E74, E77–E79 |
| M2. M1 + Gatus and the public status page (the 2026-10-27 proposal, option A below) | Per-capability public view, role-filtered banner, uptime history | One more container, extra client work, JSON sanitisation (spike item 11) and storage (item 12) before the MVP | E75 |

**Public status page (assessed on 2026-10-27; deferred past the MVP, Gatus remains the candidate)**

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Gatus (internal) + a public React `/status` page reading Gatus's JSON through Traefik** (candidate if the page returns) | Checks in YAML (reviewable in Git); Apache-2.0; about 26 MB image, amd64/arm64; per-endpoint `hide-*` options; announcements, maintenance windows, Prometheus metrics; page matches the app and the banner ([ADR-011](ADR-011-installable-pwa-client.md)) | One more container; the React page is extra client work; relies on `hide-*` also covering the JSON API (spike item 11) | E75 |
| B. Gatus UI on a subdomain | No client work | UI “does not support path-based routing”; needs a subdomain, DNS and TLS on college servers | E75 |
| C. Uptime Kuma | Rich UI | Configured through its web UI, not Git; “does not support a subdirectory”; about 617 MB image | E76 |
| D. Statping-ng | Status page built in | GPL-3.0; maintenance status not verified | E76 |
| E. Expose the Traefik API/dashboard | Nothing new | Exposes all routing configuration; not recommended in production | E74 |
| F. Custom aggregator service | Exact fit | More code and another deployable to maintain | — |
| G. No status page; banner only from failed API calls | Least work | Cannot tell users which capability is down or what still works; no §6.7 per-component view | E01 |

## Proposed decision

**M1** for the MVP, proposed, not accepted. The public status page is deferred past the MVP; if it returns, option A (Gatus) remains the candidate and the [deferred design](#deferred-design-gatus-and-the-public-status-page) below applies.

### Health endpoints

Each Spring service exposes Actuator liveness and readiness groups (E73); the Flask service its own equivalent routes; names per DEVOPS-02. Readiness includes the dependencies a service needs (`db`, `rabbit`, `mail` indicators exist, E73); a `DOWN` maps to HTTP 503. Health endpoints are internal and never routed publicly; `show-details` stays `never` on anything reachable from outside (E73).

### Traefik

`ping` enabled for Traefik's own liveness; it says nothing about the services (E74). Per-service `loadBalancer.healthcheck` on the readiness path (path, interval, timeout, settable through labels) so Traefik stops routing to an unready service (E74). The Traefik API and dashboard are never public (E74).

### Monitoring

Prometheus scrapes each service's metrics endpoint (Actuator/Micrometer, Flask `prometheus_client`), RabbitMQ and Traefik (E36, E39, E58). It would also scrape `mysqld_exporter` (MySQL metrics) and Garage's metrics on the database host over the private link ([ADR-004](ADR-004-deployment-contract.md)); that path is not yet specified and Garage's metrics endpoint is not verified, so neither is claimed here and both stay open (P-08 of the [physical views](../07b-physical-views.md), Martim with Ricardo). Until then MySQL and Garage have no `up` series. The per-target `up` series and alerts on it cover “service gone”; readiness stays in the container health checks (below) and in Traefik's load-balancer health check. blackbox_exporter is added only if readiness endpoints must be probed directly. Grafana is the §6.7 dashboard ([ADR-004](ADR-004-deployment-contract.md)).

### How degraded states reach users in the MVP

In context, where the user meets them, not on a separate page: booking pending or calendar unavailable, “triage pending — classify manually”, a delayed-email notice, the photo-upload error and the explicit error of a failed request ([technical design §6](../07-technical-design.md#6-external-integration-and-degraded-mode), [ADR-011](ADR-011-installable-pwa-client.md)). Operators see the same states in Grafana. Public text never shows versions, hostnames, container names, error messages or stack traces.

### Container health checks (Compose)

| Container | Check | Note |
|---|---|---|
| Spring services | Actuator readiness | Paths per DEVOPS-02 |
| ai-triage (web process) | Flask health route | The consumer process's check depends on spike item 7 (one container or two) |
| Keycloak | `/health/ready` on management port 9000 with `KC_HEALTH_ENABLED` | Via Bash `/dev/tcp`: curl was removed from the image (E77) |
| RabbitMQ | `rabbitmq-diagnostics -q ping`, at most every 30 s | The CLI has a performance cost (E77) |
| MySQL (database host) | `mysqladmin ping` | Exits 0 even on “Access denied” (E77), so it does not prove credentials work; a query-level check is a spike detail |
| Garage (database host and backup host) | admin `GET /health` | 200 with quorum, else 503 (E78) |
| `mysqld_exporter` (database host) | Not stated | A spike detail (P-08) |
| Mailpit | `readyz` | E78 |
| Prometheus | `/-/ready` | E78 |
| Grafana | `/api/health` | E78 |
| Traefik | `ping` | E74 |

Gatus is not in the MVP, so it has no row; nor does oauth2-proxy, which the second revision of 2026-11-01 removed (the OIDC plugin runs inside Traefik, [ADR-005](ADR-005-authentication-authorisation.md)). Startup order uses `depends_on` with `condition: service_healthy` (long syntax; the short syntax does not wait, E79). MySQL and Garage run on the database host, outside the application host's Compose project, so `depends_on` there cannot wait for them; how the services wait for the database at startup is a spike detail. Whether each image contains curl or wget for HTTP checks is a spike detail.

## Deferred design: Gatus and the public status page

**Deferred past the MVP (2026-11-01); Gatus remains the candidate.** Kept as proposed on 2026-10-27 so it can be resumed; none of it is in the MVP, and the `/status` and `/status/api` routes and the `status` profile are removed from [ADR-004](ADR-004-deployment-contract.md).

#### Gatus

Not publicly exposed, with these principles (E75). Gatus would sit on the `internal` network and also join `edge` only so that Traefik can route `/status/api` to its JSON API; its UI is never routed:

- Polls each service's readiness endpoint directly on the internal network, not through Traefik, and the platform checks below.
- Plain public names per capability and a `group`; `ui.hide-hostname`, `hide-url`, `hide-port`, `hide-conditions` and `hide-errors` on every endpoint.
- Storage on a volume so 30 days of results exist (default keeps 100 results per endpoint); the storage type is a spike item.
- `/metrics` scraped by Prometheus, with an alert if the series disappears; the image is built `FROM scratch`, so there is no in-container health check.
- Announcements and maintenance windows are the operator's tools for incident notes and planned work.

#### Routing and public content

- `/status` is a **public page of the React app** (no login; also “Service status” in the app menu). It must bypass the OIDC middleware so it works when Sign-in is down.
- Traefik routes **only** Gatus's read-only JSON under `/status/api`, rewritten to `/api/v1/endpoints/statuses` and the uptime-data endpoints. The longer prefix must win over the SPA route (rule priority to confirm in the spike).
- **Spike item 11:** confirm that the `hide-*` settings also strip the JSON output. If not, the raw API is never routed publicly and the fallback is decided at the spike (for example a filtering step); the page is not built on an unsanitised API.
- Public content: one overall sentence and a capability list. No versions, hostnames, container names, error messages or stack traces; full detail only on the internal network and in Grafana.

#### Vocabulary

| Level | Values |
|---|---|
| Overall | All systems working · Some features are affected · Service disruption (when Sign-in or Report a fault is Unavailable) · Planned maintenance |
| Capability | **Working** · **Unavailable** · **Planned maintenance**, each with icon + text, never colour alone (WCAG 1.4.1, E83) |

There are no “degraded/partial” levels because Gatus checks are up or down. The five-level Statuspage scheme (Operational, Degraded performance, Partial outage, Major outage, Under maintenance; E81) is the reference, deliberately reduced.

#### Capability → check mapping

Capability names: Report a fault · Schedule interventions · Notifications · Suggestions · Calendar sync · Sign-in · Photo upload. Infrastructure (MySQL, RabbitMQ, Keycloak, Garage, Mailpit…) rolls up into the capability it breaks and is never listed by name. Service readiness covers the service's own database, not the broker, which the outbox absorbs (ADR-003).

| Capability | Check |
|---|---|
| Report a fault | Issue readiness (its own database only; the broker is excluded because reports are accepted while it is down and events wait in the outbox, [design §5](../07-technical-design.md#5-asynchronous-workflow-and-consistency)) |
| Schedule interventions | Dispatch readiness |
| Notifications | Notification readiness + Mailpit/SMTP + RabbitMQ (with the broker down nothing is delivered until it recovers) |
| Suggestions | AI triage service health + RabbitMQ (with the broker down no `TriageRequested` is delivered; manual triage still works) |
| Calendar sync | The configured calendar (Google Calendar or the simulator, [ADR-006](ADR-006-calendar-simulator.md)) |
| Sign-in | Keycloak ready (the OIDC plugin runs inside Traefik) |
| Photo upload | Garage health |

MySQL would get a query-level check here, because `mysqladmin ping` exits 0 even on “Access denied” (E77).

#### Status page layout

- Overall sentence and last check time; capability list (one column on phones, table on desktop) with the time each was last checked.
- **30-day uptime bars** with a percentage and a text alternative per day. Not 90 days: Gatus uptime data goes to 30 days (E75); 90-day bars are the convention on GitHub and Vercel (E80).
- **Incident notes** written by an operator as Gatus announcements, using Investigating → Identified → Monitoring → Resolved plus one sentence (E81); “No incidents reported” on quiet days (E80).
- Maintenance section when a window is configured (E75).

If resumed, it costs one more container and Gatus storage to back up or accept as losable; it reveals capability-level availability to anyone (capability names and states only); and banner and page share one data source, so a capability name change touches Gatus config, the page and the banner ([ADR-011](ADR-011-installable-pwa-client.md)).

## Consequences

- No extra container for monitoring in the MVP: Prometheus and Grafana are already in the stack ([ADR-004](ADR-004-deployment-contract.md)).
- No public view of availability. Users learn of degraded states only in context, and only operators see overall health in Grafana. Accepted for the MVP.
- If Traefik, nginx or the client is down, users see a browser error; Prometheus alerts and Grafana cover operators.
- Ownership: Martim owns health checks, alert rules and the dashboard. Endpoint names are EN01-U13. Gatus checks and sanitisation (EN01-U14) and incident notes and maintenance windows (EN01-U15) are deferred with the status page.
- Service health endpoint names follow DEVOPS-02 once Martim chooses them; ADR-004, ADR-008 and the [technical design](../07-technical-design.md#7-proposed-deployment-and-operations) already defer to it.

## Verification and review

Planned, nothing exists yet:

- Spike items 11 and 12 (Gatus JSON sanitisation, persistent storage) are deferred with the status page.
- Compose starts cleanly in dependency order from a fresh clone; Traefik stops routing to an unready service.
- Stopping a service sets its `up` series to 0, fires the alert and shows in Grafana.
- **§6.8 demo outline:** with the calendar simulator configured, stop it → new bookings stay pending and administrators see “booking pending — calendar unavailable” in context, with manual confirmation offered; Grafana shows pending bookings ([technical design §6](../07-technical-design.md#6-external-integration-and-degraded-mode)); restart it → the booking reconciles. Repeat with ai-triage stopped as a second case: after 2 min the administrator sees “triage pending — classify manually”.
- Public-output review: no hostname, version or error text in any user-facing message.

Review after the spike and when DEVOPS-02 fixes the endpoint names.

## Record

2026-10-27 — proposed by Ricardo (Tech Lead) after a structured design interview; drafting and source checks AI-assisted (new ADR). Reason: §6.7/§6.8 need health and a user-visible degraded state; Gatus is small, Git-configured and internal. Evidence: [evidence register](README.md#evidence-register-en-01-01) E01, E73–E83; DEVOPS-02 [#42](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/42); issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15). Affected documents: ADR-004, [technical design §6, §7](../07-technical-design.md#6-external-integration-and-degraded-mode), [register §5](../planning/decisions-and-feedback.md#5-en-01-01-unresolved-details). Final decision, date and participants: pending team review.

2026-11-01 — revised by Ricardo (Tech Lead) after Martim's review of [PR #45](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/45) (2026-10-31) and the Copilot review of 2026-10-31; drafting AI-assisted. Reason: Gatus is dropped for the MVP; monitoring is health endpoints, container and Traefik health checks, Prometheus `up` and alerts (blackbox_exporter only if needed) and Grafana; the public `/status` page, `/status/api` and the banner, fed by Gatus, are deferred past the MVP with Gatus as the candidate; degraded states are shown in context; EN01-U14 and EN01-U15 deferred. Evidence: E36, E39, E58, E73–E79; [review decisions](../planning/decisions-and-feedback.md#review-decisions--en-01-01-2026-11-01). Affected documents: [ADR-004](ADR-004-deployment-contract.md), [ADR-011](ADR-011-installable-pwa-client.md), [ADR-010](ADR-010-object-storage.md), [technical design §1, §4, §6, §7](../07-technical-design.md#6-external-integration-and-degraded-mode), [requirements](../requirements.md) (NFR-06), [register §5](../planning/decisions-and-feedback.md#5-en-01-01-unresolved-details). Still Proposed; final decision pending team review.

2026-11-01 (second revision) — revised by Ricardo (Tech Lead) after Martim's [PR #52](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/52); drafting AI-assisted. Reason: oauth2-proxy is removed ([ADR-005](ADR-005-authentication-authorisation.md)), so its health check, scrape target and Sign-in check go; MySQL and Garage move to the database host and a second Garage to the backup host; `mysqld_exporter` added; the scrape path to the database host and Garage's metrics endpoint are recorded as open, not claimed (P-08, Martim with Ricardo). Evidence: E77–E79, E88; [second revision](../planning/decisions-and-feedback.md#second-revision--en-01-01-2026-11-01). Affected documents: [ADR-004](ADR-004-deployment-contract.md), [technical design §7](../07-technical-design.md#7-proposed-deployment-and-operations). Still Proposed; final decision pending team review.
