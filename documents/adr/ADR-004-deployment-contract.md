# ADR-004 — Deployment contract, environments and pipeline

**Status:** Proposed
**Date:** 2026-11-01
**Participants:** Ricardo (P2, Tech Lead) — proposer; Martim (P5, DevOps) to confirm; team review pending
**Related decision:** DEC-04
**Supersedes / superseded by:** revises in place the 2026-10-15 version (nginx edge, about six to eight containers); see [Record](#record)

## Context

The topology has fifteen services (listed below): traefik, oauth2-proxy, client, issue, dispatch, notification, keycloak, ai-triage, calendar-sim, rabbitmq, mysql, garage, mailpit, prometheus and grafana; sixteen containers if ai-triage's consumer runs as its own Compose service (spike item 7). The design excludes a Kubernetes commitment. The demonstration host is not yet known (college servers are expected; EN01-U3, Martim); the system should run on any Docker host. NFR-08 requires reproducible builds, containers, CI and configuration without secrets in Git; NFR-09 an exercised backup and restore. Docker's documentation calls a single server the easiest way to deploy with Compose (E59). Assignment §6.7 asks for logs, health, metrics, correlation, error reporting and a dashboard (E01).

## Alternatives

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Host-agnostic contract: multi-arch images in GHCR + one Compose file on any Docker host** (chosen) | Same definition on laptops, a college server, a VPS or an arm64 VM; failure injection is easy; no provider lock-in | Single host is a single point of failure; patching and backups are self-managed; memory unknown until measured | E59 |
| B. Render free tier | Managed, free | Free services spin down after 15 minutes idle | E60 |
| C. Fly.io | Managed containers | Trial only | E60 |
| D. Railway | Managed | One-time USD 5 trial | E60 |
| E. Kubernetes | Standard orchestration | Not committed in the design; operational burden | [design §7](../07-technical-design.md#7-proposed-deployment-and-operations) |

B–D are rejected on the free-tier terms recorded in E60 (idle spin-down, trials only); in addition the stack contains Keycloak (about 1250 MB base memory, E28), RabbitMQ and MySQL, and its fit on those plans was not tested. Oracle Always Free (Ampere A1, arm64, 2 OCPUs / 12 GB, E60) remains a possible host under A, not a separate option.

## Proposed decision (not accepted)

**A**, proposed, not accepted.

**Edge.** Traefik 3.7 (v3.7.16, E34) is the only exposed container (80/443). Routes and middlewares:

| Route | Upstream | Middlewares |
|---|---|---|
| `/` | client nginx (static files) | Headers |
| `/api/issue/*`, `/api/dispatch/*`, `/api/notifications/*` | the matching Spring service, which serves service-relative paths | ForwardAuth (oauth2-proxy), StripPrefix (`/api/<service>`), RateLimit, Headers |
| `/oauth2/*` | oauth2-proxy | RateLimit, Headers |
| `/auth/*` | Keycloak | RateLimit, Headers |

The public `/status` page and the `/status/api` route proposed on 2026-10-27 were fed by Gatus; they are deferred past the MVP with the status page ([ADR-012](ADR-012-health-and-status-page.md)). Never route the Traefik API (E74). Internal endpoints (liveness and readiness endpoints, other Actuator endpoints, `/metrics`, the AI service's `/classify`, the simulator's control endpoint, RabbitMQ management, Garage, Mailpit) are never routed. Mailpit stays internal only; in the demo the presenter shows its inbox through an SSH tunnel (demo only). There is no JWT middleware in Traefik Proxy (Traefik Hub only, E35); each Spring service validates the JWT itself ([ADR-005](ADR-005-authentication-authorisation.md)). Which Keycloak paths must stay unrouted (admin console), how Grafana is reached in demo, and the TLS certificate source are open items to settle with Martim.

**Containers.** Traefik, oauth2-proxy 7.15, Keycloak 26.8, RabbitMQ 4.x (pin a minor at the spike), MySQL 8.4, Garage 2.5 ([ADR-010](ADR-010-object-storage.md)), Mailpit 1.32 ([ADR-007](ADR-007-notification-service.md)), Prometheus 3.x, Grafana 13, client nginx, Issue, Dispatch, Notification, `ai-triage` and the calendar simulator `calendar-sim` ([ADR-006](ADR-006-calendar-simulator.md)). `ai-triage` is one service at the same level as Issue, Dispatch and Notification: one image running two processes, the Flask web process and the pika consumer process; whether they run as one container or as two Compose services from the same image is spike item 7 ([ADR-008](ADR-008-ai-triage-service.md)). Gatus is not in the MVP ([ADR-012](ADR-012-health-and-status-page.md)). Only `ai-triage` (its AI provider) and Dispatch (the Google Calendar API, [ADR-006](ADR-006-calendar-simulator.md)) need outbound access; they get it through the `egress` network below. An egress proxy with an allow-list is not adopted for the MVP; it stays open for EN-01-04 (security review).

**Database.** One MySQL 8.4 instance with one database per service (`issue`, `dispatch`, `notification`, `keycloak`), each with its own user. Scaling a service adds replicas of that service, never another database; the instance scales vertically (a bigger machine). A separate database host is not adopted for the MVP: MySQL stays on the demonstration host.

**Networks.** Three networks; no published ports except Traefik's.

| Network | Members | Purpose |
|---|---|---|
| `edge` | Traefik, oauth2-proxy, client, Issue, Dispatch, Notification, Keycloak | Traefik and the containers it routes to (Keycloak for `/auth/*`) |
| `internal` | Issue, Dispatch, Notification, Keycloak, ai-triage, calendar-sim, RabbitMQ, MySQL, Garage, Mailpit, Prometheus, Grafana | Broker, databases (Keycloak joins for its MySQL database), storage, mail capture, metrics and the simulator |
| `egress` | ai-triage, Dispatch | The only way out to the internet: the AI provider and the Google Calendar API |

How `edge` and `internal` are kept from reaching the internet in Compose is confirmed at the spike with Martim.

**Images and Compose.** Images for each app in GitHub Container Registry for linux/amd64 and linux/arm64. One `compose.yaml` with profiles (names proposed): `core` (nine containers, below); `observability` (Prometheus and Grafana: standard in demo and release, optional on a laptop); `storage` (Garage); `demo` (synthetic realm users only, [ADR-005](ADR-005-authentication-authorisation.md)). ai-triage, Notification and calendar-sim are added when the slice needs them. `.env.example`; secrets only in the host or CI environment, never in Git. Multi-arch availability is recorded for Traefik, RabbitMQ, MySQL, Mailpit, Temurin and python images (E08, E23, E34, E37, E44, E52); it is not checked for Keycloak, oauth2-proxy, Garage, Prometheus, Grafana or nginx, so spike item 8 covers both architectures.

**Minimal profile for the first vertical slice (proposal, to decide at the team review, EN01-U1).** The Sprint 2 slice is not yet defined in the repository; this proposal assumes a resident reports a fault through the client and an administrator sees and handles it through Issue and Dispatch (two independent backend components, [walking skeleton](../10-walking-skeleton.md)). The team can start from a smaller set and add containers as stories need them; the design of the later ones stays as written above. Reviewers can change the assumption and the split.

| When | Containers | Reason |
|---|---|---|
| First (`core`, nine containers) | Traefik, oauth2-proxy, Keycloak, MySQL, RabbitMQ, Issue, Dispatch, client nginx, Mailpit | Sign-in and the Backend-for-Frontend session ([ADR-005](ADR-005-authentication-authorisation.md)) are needed by every journey; Issue and Dispatch exchange events through the broker (membership and issue-state projections, [ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)). Keycloak's verification emails need SMTP from the first journey, so Mailpit is in `core` (internal only, never routed) |
| When the slice includes the step | ai-triage; Notification service; calendar simulator | Reporting works with AI disabled and manual triage is always possible (NFR-03, [ADR-008](ADR-008-ai-triage-service.md)), so triage can follow. The Notification service also hosts the in-app channel ([ADR-007](ADR-007-notification-service.md)), so it is needed as soon as US-10 notifications are in the slice, even without email. The simulator is needed when Dispatch books a visit in tests or failure demos ([ADR-006](ADR-006-calendar-simulator.md)) |
| Later | Prometheus and Grafana; Garage | Prometheus and Grafana are the `observability` profile. Garage serves the report-photos candidate (post-MVP, pending a DEC entry) and the backup bucket `bmc-backups`; the runbook below writes backups to it, so it is needed before the backup and restore exercise (NFR-09) ([ADR-010](ADR-010-object-storage.md)) |

Later containers would join through further profiles (`observability`, `storage`; the `status` profile proposed earlier disappears with Gatus) so that `docker compose up` on a laptop starts only the set the slice uses. Memory of the minimal profile, as of the full stack, is not measured (EN01-U3); spike item 8 should record both.

**Pipeline (outline; no CI exists yet).** Aligned with PR #40 (E02, proposed, open, not merged): `feature/* → dev → main`, release by protected `v*` tag, build once and promote the same image. Proposed stages: lint → unit tests → `buf lint` and `buf breaking` → boundary tests ([ADR-009](ADR-009-service-internal-architecture.md)) → integration tests with real MySQL 8.4 and RabbitMQ containers → multi-arch build and push to GHCR. Deployment is `docker compose pull && docker compose up -d`. Required checks are configured only when the pipeline exists; arm64 build method (emulation or native runners) is open (EN01-U9).

**Health checks and startup order.** Every BMC service exposes liveness and readiness endpoints, names per [DEVOPS-02 (#42)](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/42); they are internal and never routed publicly. Container health checks, Traefik `loadBalancer.healthcheck` on readiness, startup order with `depends_on: condition: service_healthy` and the Prometheus `up` alerts are specified in [ADR-012](ADR-012-health-and-status-page.md) (E73, E74, E77–E79); this ADR does not repeat them.

**Observability.** Prometheus scrapes each service's metrics endpoint (Actuator/Micrometer, Flask `prometheus_client`), RabbitMQ, Traefik and oauth2-proxy (E36, E39, E58); the per-target `up` series and alerts on it cover a service that has gone; blackbox_exporter is added only if readiness endpoints must be probed directly ([ADR-012](ADR-012-health-and-status-page.md)). Grafana remains the operator dashboard and the §6.7 dashboard; Gatus and the public status page are deferred past the MVP ([ADR-012](ADR-012-health-and-status-page.md)). The Grafana dashboard shows outbox lag, DLQ depth, consumer retries, AI fallback rate, pending bookings, error rate, notification failures and projection freshness. Correlation uses W3C `traceparent` and `correlationId` (CloudEvents extensions and HTTP headers). Traefik writes JSON access logs but has no built-in request-ID generator (E36), so the first Spring service generates a missing correlation ID (to confirm in the spike). Loki and Tempo are left to DEVOPS-02 (Martim, EN01-U12).

**Runbook.** Start/stop, logs, migrations, rollback to the previous image tag, **DLQ replay** (management-UI shovel back to the source queue; [ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)), **projection rebuild** (Issue's snapshot job republishing memberships and issue states for Dispatch; [design §4.3](../07-technical-design.md#43-how-dispatch-obtains-trustworthy-authorisation-context)), and **backup and restore**, kept simple for the academic release: a cron job on the Docker host (not a container) runs a nightly `mysqldump` of each database into the Garage bucket `bmc-backups` ([ADR-010](ADR-010-object-storage.md)), using a read-only MySQL backup user and the `bmc-backups` key, both in the host environment; restore is exercised once with counts and integrity checks (NFR-09). No snapshot scheme and no off-site VPS. Single-node Garage has no redundancy (E46) and sits on the same host, so losing the host loses the backups too; an off-host copy to Cloudflare R2 (E49) stays optional and is not part of the academic release.

**Host.** College servers are expected, not confirmed (EN01-U3, Martim); the contract does not depend on the choice.

## Consequences

- No provider lock-in; a reviewer can run the system from a clone.
- **Memory is the main risk.** Three Spring JVMs, the simulator JVM, Keycloak (about 1250 MB base, E28), RabbitMQ (high watermark 0.6 of RAM, E39), MySQL, Prometheus and Grafana together are likely several GB. This is not measured; it is measured in the spike on the real host and architectures, and may force profile or sizing changes (the minimal profile above is the first lever).
- One host, one MySQL and one RabbitMQ node are single points of failure, stated as limits of the academic release ([ADR-001](ADR-001-backend-boundaries.md)).
- Multi-arch builds lengthen CI; this proposal takes that cost to keep the host choice open.
- More secrets to manage (Keycloak client secrets, cookie secret, per-service database and broker credentials, the Google Calendar credentials, the backup user and the `bmc-backups` key); rotation is EN01-U6.
- Dispatch and ai-triage reach the internet through `egress` without an allow-list; whether to add an egress proxy is an EN-01-04 item.

## Verification and review

Spike item 8 (measured memory of the full stack on amd64 and arm64), items 1, 3 and 5 (Keycloak, ForwardAuth, dead-lettering) feed this ADR; items 11 and 12 (Gatus) are deferred with the status page ([ADR-012](ADR-012-health-and-status-page.md)). Before release: fresh clone → `docker compose up` → guided journey works; backup/restore exercise recorded; a DLQ replay rehearsed; stopping the simulator, then a service, then the broker shows the degraded modes expected by §6.8, in context in the client (booking pending or calendar unavailable, “triage pending — classify manually”, delayed email) and in Grafana. Review when the host is chosen and at Sprint B planning (EN01-U10 version re-check).

## Record

- 2026-10-15 — first proposed: Compose on any Docker host, multi-arch images in GHCR, nginx as the only exposed container, GitHub Actions with a MySQL 9.7 service container (E03).
- 2026-10-27 — revised by Ricardo (Tech Lead) after a structured design interview; drafting and source checks AI-assisted. Reason: Traefik with ForwardAuth replaces nginx as edge; platform containers added (Keycloak, RabbitMQ, object storage, mail capture, metrics); pipeline aligned with PR #40. Evidence: [evidence register](README.md#evidence-register-en-01-01) E01, E02, E28, E34–E39, E44, E46, E49, E52, E58–E60; issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15). Affected documents: [technical design §7](../07-technical-design.md#7-proposed-deployment-and-operations), DEVOPS-01 (PR #40), DEC-04. Final decision, date and participants: pending team review.
- 2026-10-27 — Gatus container, `/status` and `/status/api` routes and a pointer to [ADR-012](ADR-012-health-and-status-page.md) for health checks and startup order added; fixed health paths removed, endpoint names left to [DEVOPS-02 (#42)](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/42). Evidence: E73–E79.
- 2026-10-29 — minimal profile for the first vertical slice proposed in response to review (Afonso, BA/PO): what is needed first and what can be added later; to decide at the team review (EN01-U1).
- 2026-11-01 — revised by Ricardo (Tech Lead) after Martim's review of [PR #45](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/45) (2026-10-31) and the Copilot review of 2026-10-31; drafting AI-assisted. Reason: one MySQL instance that scales vertically and stays on the demonstration host; backups by a host cron job to `bmc-backups`, R2 optional and outside the academic release (settles P-03 of the physical views); `ai-triage` as one service; an `egress` network for ai-triage and Dispatch, which now calls Google Calendar (settles P-02); Keycloak on `edge` and `internal`; Gatus, `/status` and `/status/api` removed (status page deferred); Mailpit in `core` (nine containers) because Keycloak needs SMTP (Copilot finding on the minimal profile); the `status` profile dropped. Evidence: E46, E49, E59, E87; [review decisions](../planning/decisions-and-feedback.md#review-decisions--en-01-01-2026-11-01). Affected documents: [ADR-006](ADR-006-calendar-simulator.md), [ADR-010](ADR-010-object-storage.md), [ADR-012](ADR-012-health-and-status-page.md), [technical design §7](../07-technical-design.md#7-proposed-deployment-and-operations), [physical views](../07b-physical-views.md), DEC-04. Still Proposed; final decision pending team review.
