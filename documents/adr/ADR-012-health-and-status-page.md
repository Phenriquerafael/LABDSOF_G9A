# ADR-012 — Health checks and the public status page

**Status:** Proposed
**Date:** 2026-10-27
**Participants:** Ricardo (P2, Tech Lead) — proposer; Martim (P5, DevOps/QA/security) to confirm; team review pending
**Related decision:** DEC-04; DEVOPS-02 ([#42](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/42))
**Supersedes / superseded by:** —

## Context

- §6.7 asks for health checks, metrics and a dashboard, and §6.8 for a degraded-mode scenario in which the degraded state is communicated to users (E01). Grafana ([ADR-004](ADR-004-deployment-contract.md)) serves operators; users need a plain-language view.
- Tech Lead requirement: every service exposes health, and the gateway serves a `/status` page with overall and per-component health.
- DEVOPS-02 ([#42](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/42)) already plans `/healthz`, `/readyz` and `/status`. The endpoint names are Martim's decision; this ADR does not fix them and says “liveness and readiness endpoints, names per DEVOPS-02”. [ADR-004](ADR-004-deployment-contract.md) and the [technical design](../07-technical-design.md#7-proposed-deployment-and-operations) mention `/actuator/health` and Flask `/health` as the current sketch.
- Services never call each other ([ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)), so an aggregator must live outside the business services. Only Traefik is exposed ([ADR-004](ADR-004-deployment-contract.md)).

## Alternatives

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Gatus (internal) + a public React `/status` page reading Gatus's JSON through Traefik** | Checks in YAML (reviewable in Git); Apache-2.0; about 26 MB image, amd64/arm64; per-endpoint `hide-*` options; announcements, maintenance windows, Prometheus metrics; page matches the app and the banner ([ADR-011](ADR-011-installable-pwa-client.md)) | One more container; the React page is extra client work; relies on `hide-*` also covering the JSON API (spike item 11) | E75 |
| B. Gatus UI on a subdomain | No client work | UI “does not support path-based routing”; needs a subdomain, DNS and TLS on college servers | E75 |
| C. Uptime Kuma | Rich UI | Configured through its web UI, not Git; “does not support a subdirectory”; about 617 MB image | E76 |
| D. Statping-ng | Status page built in | GPL-3.0; maintenance status not verified | E76 |
| E. Expose the Traefik API/dashboard | Nothing new | Exposes all routing configuration; not recommended in production | E74 |
| F. Custom aggregator service | Exact fit | More code and another deployable to maintain | — |
| G. No status page; banner only from failed API calls | Least work | Cannot tell users which capability is down or what still works; no §6.7 per-component view | E01 |

## Proposed decision

**A**, proposed, not accepted.

### Health endpoints

Each Spring service exposes Actuator liveness and readiness groups (E73); the Flask service its own equivalent routes; names per DEVOPS-02. Readiness includes the dependencies a service needs (`db`, `rabbit`, `mail` indicators exist, E73); a `DOWN` maps to HTTP 503. Health endpoints are internal and never routed publicly; `show-details` stays `never` on anything reachable from outside (E73).

### Traefik

`ping` enabled for Traefik's own liveness; it says nothing about the services (E74). Per-service `loadBalancer.healthcheck` on the readiness path (path, interval, timeout, settable through labels) so Traefik stops routing to an unready service (E74). The Traefik API and dashboard are never public (E74).

### Gatus

Not publicly exposed, with these principles (E75). Gatus sits on the `internal` network and also joins `edge` only so that Traefik can route `/status/api` to its JSON API ([ADR-004](ADR-004-deployment-contract.md)); its UI is never routed:

- Polls each service's readiness endpoint directly on the internal network, not through Traefik, and the platform checks below.
- Plain public names per capability and a `group`; `ui.hide-hostname`, `hide-url`, `hide-port`, `hide-conditions` and `hide-errors` on every endpoint.
- Storage on a volume so 30 days of results exist (default keeps 100 results per endpoint); the storage type is a spike item.
- `/metrics` scraped by Prometheus, with an alert if the series disappears; the image is built `FROM scratch`, so there is no in-container health check.
- Announcements and maintenance windows are the operator's tools for incident notes and planned work.

### Routing and public content

- `/status` is a **public page of the React app** (no login; also “Service status” in the app menu). It must bypass ForwardAuth so it works when Sign-in is down.
- Traefik routes **only** Gatus's read-only JSON under `/status/api`, rewritten to `/api/v1/endpoints/statuses` and the uptime-data endpoints. The longer prefix must win over the SPA route (rule priority to confirm in the spike).
- **Spike item 11:** confirm that the `hide-*` settings also strip the JSON output. If not, the raw API is never routed publicly and the fallback is decided at the spike (for example a filtering step); the page is not built on an unsanitised API.
- Public content: one overall sentence and a capability list. No versions, hostnames, container names, error messages or stack traces; full detail only on the internal network and in Grafana.

### Vocabulary

| Level | Values |
|---|---|
| Overall | All systems working · Some features are affected · Service disruption (when Sign-in or Report a fault is Unavailable) · Planned maintenance |
| Capability | **Working** · **Unavailable** · **Planned maintenance**, each with icon + text, never colour alone (WCAG 1.4.1, E83) |

There are no “degraded/partial” levels because Gatus checks are up or down. The five-level Statuspage scheme (Operational, Degraded performance, Partial outage, Major outage, Under maintenance; E81) is the reference, deliberately reduced.

### Capability → check mapping (proposal, to refine in EN-01-03)

Capability names: Report a fault · Schedule interventions · Notifications · Suggestions · Calendar sync · Sign-in · Photo upload. Infrastructure (MySQL, RabbitMQ, Keycloak, Garage, Mailpit…) rolls up into the capability it breaks and is never listed by name.

| Capability | Check |
|---|---|
| Report a fault | Issue readiness (database, broker) |
| Schedule interventions | Dispatch readiness |
| Notifications | Notification readiness + Mailpit/SMTP |
| Suggestions | AI triage service health |
| Calendar sync | Calendar simulator |
| Sign-in | Keycloak ready + oauth2-proxy ready |
| Photo upload | Garage health |

### Status page layout

- Overall sentence and last check time; capability list (one column on phones, table on desktop) with the time each was last checked.
- **30-day uptime bars** with a percentage and a text alternative per day. Not 90 days: Gatus uptime data goes to 30 days (E75); 90-day bars are the convention on GitHub and Vercel (E80).
- **Incident notes** written by an operator as Gatus announcements, using Investigating → Identified → Monitoring → Resolved plus one sentence (E81); “No incidents reported” on quiet days (E80).
- Maintenance section when a window is configured (E75).

### Container health checks (Compose)

| Container | Check | Note |
|---|---|---|
| Spring services | Actuator readiness | Paths per DEVOPS-02 |
| AI triage (web) | Flask health route | |
| Keycloak | `/health/ready` on management port 9000 with `KC_HEALTH_ENABLED` | Via Bash `/dev/tcp`: curl was removed from the image (E77) |
| RabbitMQ | `rabbitmq-diagnostics -q ping`, at most every 30 s | The CLI has a performance cost (E77) |
| MySQL | `mysqladmin ping` | Exits 0 even on “Access denied”, so Gatus adds a query-level check (E77) |
| Garage | admin `GET /health` | 200 with quorum, else 503 (E78) |
| oauth2-proxy | `/ready` | E78 |
| Mailpit | `readyz` | E78 |
| Prometheus | `/-/ready` | E78 |
| Grafana | `/api/health` | E78 |
| Traefik | `ping` | E74 |
| Gatus | none in the container | `FROM scratch` (E75); Prometheus alert instead |

Startup order uses `depends_on` with `condition: service_healthy` (long syntax; the short syntax does not wait, E79). Whether each image contains curl or wget for HTTP checks is a spike detail.

## Consequences

- One more container, and Gatus storage to back up or accept as losable (history only).
- The status page reveals capability-level availability to anyone. Accepted: no internals are shown.
- If Traefik, nginx or the client is down, the page itself is unreachable; Grafana and Prometheus alerts cover that case.
- Banner and page share one data source, so their wording stays consistent; changing a capability name touches Gatus config, the page and the banner.
- Ownership: Martim owns checks, Gatus configuration, incident notes and maintenance windows (procedure open, EN01-U15). Endpoint names and the relation of `/status` to DEVOPS-02 are EN01-U13.
- The 2026-10-27 [technical design](../07-technical-design.md#7-proposed-deployment-and-operations) and ADR-004 name `/actuator/health` and `/health`; they must follow DEVOPS-02's names once chosen.

## Verification and review

Planned, nothing exists yet:

- **Spike item 11:** the `hide-*` options also strip the JSON API; routing exposes nothing else.
- **Spike item 12:** Gatus persistent storage and 30-day uptime data survive a restart.
- Compose starts cleanly in dependency order from a fresh clone; Traefik stops routing to an unready service.
- **§6.8 demo outline:** stop the calendar simulator → after two failed checks administrators see the banner “Calendar sync is unavailable…”, the status page shows Calendar sync Unavailable, new bookings stay pending ([technical design §6](../07-technical-design.md#6-external-integration-and-degraded-mode)); restart it → the banner clears, the booking reconciles. Repeat with object storage (“Photo upload”) as a second case.
- Public-output review: no hostname, version or error text in page, JSON or banner.

Review after the spike and when DEVOPS-02 fixes the endpoint names.

## Record

2026-10-27 — proposed by Ricardo (Tech Lead) after a structured design interview; drafting and source checks AI-assisted (new ADR). Reason: §6.7/§6.8 need health and a user-visible degraded state; Gatus is small, Git-configured and internal. Evidence: [evidence register](README.md#evidence-register-en-01-01) E01, E73–E83; DEVOPS-02 [#42](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/42); issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15). Affected documents: ADR-004, [technical design §6, §7](../07-technical-design.md#6-external-integration-and-degraded-mode), [register §5](../planning/decisions-and-feedback.md#5-en-01-01-unresolved-details). Final decision, date and participants: pending team review.
