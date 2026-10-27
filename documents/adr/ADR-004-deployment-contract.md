# ADR-004 — Deployment contract, environments and pipeline

**Status:** Proposed
**Date:** 2026-10-27
**Participants:** Ricardo (P2, Tech Lead) — proposer; Martim (P5, DevOps) to confirm; team review pending
**Related decision:** DEC-04
**Supersedes / superseded by:** revises in place the 2026-10-15 version (nginx edge, about six to eight containers); see [Record](#record)

## Context

The topology grows to about sixteen containers (listed below): Traefik edge, identity, three Spring services, the AI service in two containers, simulator, MySQL, RabbitMQ, object storage, mail capture, metrics and the client. The design excludes a Kubernetes commitment. The demonstration host is not yet known (college servers are expected; EN01-U3, Martim); the system should run on any Docker host. NFR-08 requires reproducible builds, containers, CI and configuration without secrets in Git; NFR-09 an exercised backup and restore. Docker's documentation calls a single server the easiest way to deploy with Compose (E59). Assignment §6.7 asks for logs, health, metrics, correlation, error reporting and a dashboard (E01).

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

Internal endpoints (Actuator beyond health where exposed, `/metrics`, the AI service's `/classify`, the simulator's control endpoint, RabbitMQ management, Garage, Mailpit) are never routed. There is no JWT middleware in Traefik Proxy (Traefik Hub only, E35); each Spring service validates the JWT itself ([ADR-005](ADR-005-authentication-authorisation.md)). Which Keycloak paths must stay unrouted (admin console), how Grafana is reached in demo, and the TLS certificate source are open items to settle with Martim.

**Containers.** Traefik, oauth2-proxy 7.15, Keycloak 26.8, RabbitMQ 4.x (pin a minor at the spike), MySQL 8.4, Garage 2.5 ([ADR-010](ADR-010-object-storage.md)), Mailpit 1.32 ([ADR-007](ADR-007-notification-service.md)), Prometheus 3.x, Grafana 13, client nginx, Issue, Dispatch, Notification, AI triage (web container and a consumer container from one image, to confirm in spike item 7; [ADR-008](ADR-008-ai-triage-service.md)), calendar simulator ([ADR-006](ADR-006-calendar-simulator.md)). Only the AI service needs outbound access to its provider; whether other containers can be denied egress is to confirm.

**Networks.** An `edge` network holds Traefik and the services it routes to; an `internal` network holds MySQL, RabbitMQ, Garage, Mailpit, Prometheus, Grafana and the simulator, and every service attaches to it as needed. No published ports except Traefik's.

**Images and Compose.** Images for each app in GitHub Container Registry for linux/amd64 and linux/arm64. One `compose.yaml` with profiles (names proposed): `core`; `observability` (Prometheus and Grafana: standard in demo and release, optional on a laptop); `demo` (Mailpit and synthetic realm users, [ADR-005](ADR-005-authentication-authorisation.md)). `.env.example`; secrets only in the host or CI environment, never in Git. Multi-arch availability is recorded for Traefik, RabbitMQ, MySQL, Mailpit, Temurin and python images (E08, E23, E34, E37, E44, E52); it is not checked for Keycloak, oauth2-proxy, Garage, Prometheus, Grafana or nginx, so spike item 8 covers both architectures.

**Pipeline (outline; no CI exists yet).** Aligned with PR #40 (E02, proposed, open, not merged): `feature/* → dev → main`, release by protected `v*` tag, build once and promote the same image. Proposed stages: lint → unit tests → `buf lint` and `buf breaking` → boundary tests ([ADR-009](ADR-009-service-internal-architecture.md)) → integration tests with real MySQL 8.4 and RabbitMQ containers → multi-arch build and push to GHCR. Deployment is `docker compose pull && docker compose up -d`. Required checks are configured only when the pipeline exists; arm64 build method (emulation or native runners) is open (EN01-U9).

**Observability.** Health: Spring Actuator `/actuator/health` (liveness and readiness) and Flask `/health`. Prometheus scrapes Actuator/Micrometer, Flask `prometheus_client`, Traefik, RabbitMQ and oauth2-proxy (E36, E39, E58). The Grafana dashboard shows outbox lag, DLQ depth, consumer retries, AI fallback rate, pending bookings, error rate, notification failures and projection freshness. Correlation uses W3C `traceparent` and `correlationId` (CloudEvents extensions and HTTP headers). Traefik writes JSON access logs but has no built-in request-ID generator (E36), so the first Spring service generates a missing correlation ID (to confirm in the spike). Loki and Tempo are left to DEVOPS-02 (Martim, EN01-U12).

**Runbook.** Start/stop, logs, migrations, rollback to the previous image tag, **DLQ replay** (management-UI shovel back to the source queue; [ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)), **projection rebuild** (Issue's snapshot job republishing memberships and issue states for Dispatch; [design §4.3](../07-technical-design.md#43-how-dispatch-obtains-trustworthy-authorisation-context)), and **backup and restore**: MySQL dumps of each database to object storage (Garage, and an off-host copy such as R2, E49, because single-node Garage has no redundancy, E46), restore exercised with counts and integrity checks (NFR-09).

**Host.** College servers are expected, not confirmed (EN01-U3, Martim); the contract does not depend on the choice.

## Consequences

- No provider lock-in; a reviewer can run the system from a clone.
- **Memory is the main risk.** Three Spring JVMs, the simulator JVM, Keycloak (about 1250 MB base, E28), RabbitMQ (high watermark 0.6 of RAM, E39), MySQL, Prometheus and Grafana together are likely several GB. This is not measured; it is measured in the spike on the real host and architectures, and may force profile or sizing changes.
- One host, one MySQL and one RabbitMQ node are single points of failure, stated as limits of the academic release ([ADR-001](ADR-001-backend-boundaries.md)).
- Multi-arch builds lengthen CI; this proposal takes that cost to keep the host choice open.
- More secrets to manage (Keycloak client secrets, cookie secret, per-service database and broker credentials); rotation is EN01-U6.

## Verification and review

Spike item 8 (measured memory of the full stack on amd64 and arm64) and items 1, 3 and 5 (Keycloak, ForwardAuth, dead-lettering) feed this ADR. Before release: fresh clone → `docker compose up` → guided journey works; backup/restore exercise recorded; a DLQ replay rehearsed; stopping the simulator, then a service, then the broker shows the degraded modes expected by §6.8. Review when the host is chosen and at Sprint B planning (EN01-U10 version re-check).

## Record

- 2026-10-15 — first proposed: Compose on any Docker host, multi-arch images in GHCR, nginx as the only exposed container, GitHub Actions with a MySQL 9.7 service container (E03).
- 2026-10-27 — revised by Ricardo (Tech Lead) after a structured design interview; drafting and source checks AI-assisted. Reason: Traefik with ForwardAuth replaces nginx as edge; platform containers added (Keycloak, RabbitMQ, object storage, mail capture, metrics); pipeline aligned with PR #40. Evidence: [evidence register](README.md#evidence-register-en-01-01) E01, E02, E28, E34–E39, E44, E46, E49, E52, E58–E60; issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15). Affected documents: [technical design §7](../07-technical-design.md#7-proposed-deployment-and-operations), DEVOPS-01 (PR #40), DEC-04. Final decision, date and participants: pending team review.
