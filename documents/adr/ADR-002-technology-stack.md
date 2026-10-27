# ADR-002 — Technology stack

**Status:** Proposed
**Date:** 2026-10-27
**Participants:** Ricardo (P2, Tech Lead) — proposer; all team members to confirm the Java premise (EN01-U1); Pedro (P1) to confirm the client components (EN01-U4); Martim (P5) to confirm test tooling (EN01-U9); team review pending
**Related decision:** DEC-04
**Supersedes / superseded by:** revises in place the 2026-10-15 version (Elysia on Bun, Prisma, MySQL 9.7); see [Record](#record)

## Context

No application code exists yet. Five students deliver over three sprints; implementation starts after Sprint 1 (DEC-11). The stack must support separate services ([ADR-001](ADR-001-backend-boundaries.md)), asynchronous messaging ([ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)), one database technology (E01 §6.4), identity through Keycloak ([ADR-005](ADR-005-authentication-authorisation.md)), container deployment without Kubernetes ([ADR-004](ADR-004-deployment-contract.md)) and an accessible client (NFR-07).

**Team premise.** The Tech Lead states that all members are ISEP students who have used Java ("comfortable with Java"). No skills survey is recorded; this is the Tech Lead's statement, to be confirmed at team review (EN01-U1). The 2026-10-15 proposal assumed TypeScript instead. The change of stack is a Tech Lead proposal of 2026-10-27, not lecturer feedback.

## Alternatives

### Backend language and framework (Issue, Dispatch, Notification, simulator)

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Java 25 LTS + Spring Boot 4.1** (chosen) | Team's Java experience (premise); one framework covers JPA, AMQP with publisher confirms, resource-server security, Actuator/Micrometer; Boot 4.1 supports Java 17 to 27; Temurin 25 supported to 2031-09-30; OSS support for 4.1 to 2027-07-31, beyond Sprint C (ends 2027-01-03) | JVM memory and startup per service; several Spring projects to learn; Boot 4.0 ends 2026-12-31, so 4.1 only | E04–E07, E09, E12, E16 |
| B. Elysia on Bun (the 2026-10-15 proposal) | One language with the client; typed client from the API | Rejected: team's Java experience, Spring's mature AMQP, security and JPA integration, and smaller ecosystem and single-maintainer risk recorded on 2026-10-15; TypeScript stays on the client only | E03 |
| C. NestJS | Modules and DI; ecosystem; was the 2026-10-15 recorded fallback | Decorator-heavy; no recorded team depth; would keep two runtimes | E03, E62 |
| D. ASP.NET Core | Mature tooling | Third language; no recorded team depth | E03, E62 |
| E. FastAPI or Flask for the domain services | Same language as the AI service | Fewer conventions for transactional domain services with outbox and security; no recorded team depth | E62 |

### AI service runtime

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Python 3.14 + Flask 3.1 behind Gunicorn, pika consumer in the same image** (chosen) | Python for the AI provider SDKs and evaluation; small HTTP surface (`/health`, `/metrics`, `POST /classify`); Flask documents production WSGI servers, Gunicorn 26.2 | Second language and runtime; pika connections are not thread-safe, so the consumer is its own process; no DI library (manual composition root) | E20–E25, [ADR-008](ADR-008-ai-triage-service.md) |
| B. FastAPI | Async and typed models; popular (14.8% in the 2025 survey) | The service's HTTP surface is tiny and its work is queue-driven; async adds nothing the consumer needs | E62 |
| C. Spring Boot (Java) | One language | Provider SDK and evaluation tooling would be written on the JVM; one more JVM | E04 |

### Database

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. MySQL 8.4 LTS** (chosen) | The only MySQL line Keycloak 26.8 supports and tests with; support to 2029-04-30; `mysql:8.4` multi-arch; team preference for MySQL | 8.4 not in Flyway's verified list (spike item 2); `sql_generate_invisible_primary_key=OFF` and non-STATEMENT binlog required by Keycloak | E11, E27, E44 |
| B. MySQL 9.7 LTS (the 2026-10-15 choice) | Newer LTS | Rejected: Keycloak does not support MySQL 9.x; a second database technology for Keycloak would break §6.4 | E27, E44 |
| C. PostgreSQL | Richer types; supported by Keycloak | Not the team's choice; no requirement that MySQL fails; no schema-level reason | E27 |
| D. MySQL + SQLite for tests | Fast local start | Two database technologies; tests would not prove MySQL behaviour | E01 §6.4 |

### Data access and migrations

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Spring Data JPA / Hibernate 7.4 + Flyway** (chosen) | Boot-managed versions; versioned SQL migrations owned per service; optimistic-lock `version` column maps to the design's aggregate versions | Flyway 12.4 lists MySQL 8.0 and 9.4 as verified, not 8.4 → spike; JPA learning curve | E09–E11 |
| B. Prisma (the 2026-10-15 choice) | Typed client | Rejected with the TypeScript backend | E03 |

### Contracts

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Protobuf in `contracts/proto/` + Buf + AsyncAPI 3 for events; OpenAPI 3 from the Spring services for REST** (chosen) | Single schema source with Java and Python code generation; `buf breaking` in CI; AsyncAPI documents channels with Protobuf `schemaFormat` | Toolchain to set up; proto3 JSON mapping must round-trip between Java and Python (spike item 6) | E41, E42, E43 |
| B. JSON Schema only | Simple | No generated types or breaking-change check across Java and Python | — |
| C. Shared Java domain library | No schema files | Couples services; excluded: no shared domain library between services | [ADR-001](ADR-001-backend-boundaries.md) |

### Client

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. React 19 + Vite 8 + Tailwind 4 + shadcn/ui, TanStack Router and Query, generated OpenAPI client, PWA install shell** (chosen) | Static build served by nginx; shadcn/ui components are Radix-based, which addresses the keyboard/ARIA gap of plain Tailwind (proposed; Pedro to confirm); typed client from OpenAPI; MIT packages | Several libraries to pin; PWA limited to install and cached shell (reporting needs a connection) | E54 |
| B. Next.js | Full-stack framework | Server runtime and SSR not needed for an authenticated tool | — |
| C. Native mobile app | App-store presence | Second UI codebase; administrator workflows are desktop-first | E01 §6.1 |

## Proposed decision (not accepted)

| Layer | Choice | Pin (exact versions in lockfiles and BOMs) |
|---|---|---|
| Java services | Java 25 LTS (Temurin), Spring Boot, Maven; Spring Data JPA/Hibernate, Flyway, Spring AMQP, Spring Security resource server, Actuator/Micrometer | Boot 4.1.2; Hibernate 7.4; Flyway 12.4 (Boot-managed) |
| AI service | Python, Flask behind Gunicorn, pika, prometheus-client | Python 3.14; Flask 3.1.3; Gunicorn 26.x; pika 1.4.x |
| Database | MySQL, databases `issue`, `dispatch`, `notification`, `keycloak`, one user each | `mysql:8.4` |
| Contracts | Protobuf, Buf, AsyncAPI 3, OpenAPI 3 | Buf 1.75 |
| Client | React, Vite, Tailwind, shadcn/ui, TanStack Router and Query, openapi-typescript + openapi-fetch, vite-plugin-pwa; nginx serves the build | versions as E54 |
| Tests | JUnit 5 with integration tests against real MySQL 8.4 and RabbitMQ containers; pytest; Vitest; no SQLite | Container tooling (for example Testcontainers) to be confirmed by Martim at setup; not in the register |
| Monorepo | `services/issue`, `services/dispatch`, `services/notification`, `services/ai-triage`, `apps/client`, `tools/calendar-sim`, `platform/bmc-messaging-spring-boot-starter`, `contracts/proto`, `contracts/asyncapi`, `infra/` | No shared domain library; the starter holds infrastructure only |

Platform container versions (Traefik, Keycloak, RabbitMQ, Garage and others) are in [ADR-004](ADR-004-deployment-contract.md).

## Consequences

- Two backend languages (Java and Python) plus TypeScript on the client; the Python service is small and isolated behind messages, and TypeScript is limited to the client build.
- Higher memory use than a Bun stack: three Spring JVMs plus the simulator; measured in the spike, not assumed ([ADR-004](ADR-004-deployment-contract.md)).
- Keycloak's database support fixes MySQL at 8.4; a later MySQL 9.x move depends on Keycloak.
- The shared messaging starter is a platform dependency of every Spring service, so a defect affects all; it contains no domain types ([ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)).
- Versions in the register were current on 2026-10-27; re-check at Sprint B planning (EN01-U10).

## Verification and review

A two-day spike (Ricardo and Afonso; Martim for infrastructure) before the first implementation stories are Ready. Items relevant here: 1 Keycloak 26.8 on MySQL 8.4 with realm import; 2 Flyway migrations against MySQL 8.4; 6 Buf-generated Java and Python code round-trips proto3 JSON; 7 a pika consumer runs in the Flask image; 8 measured memory of the full stack on amd64 and arm64; 10 ArchUnit works on Java 25. Failure of an item reopens the ADR that depends on it. Open items: Java premise (EN01-U1), accessible components (EN01-U4), test tooling and CI layout (EN01-U9).

## Record

- 2026-10-15 — first proposed: Elysia on Bun, Prisma 7.10, MySQL 9.7, React + Vite PWA, outbox without a broker (E03).
- 2026-10-27 — revised by Ricardo (Tech Lead) after a structured design interview; drafting and source checks AI-assisted. Reason: Java team premise (to confirm), Spring's AMQP/security/JPA integration, Keycloak not supporting MySQL 9.x. Evidence: [evidence register](README.md#evidence-register-en-01-01) E01, E03–E12, E16, E20–E25, E27, E41–E44, E54, E62; issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15). Affected documents: [technical design](../07-technical-design.md) §1, §7, [ADR index](README.md), DEC-04. Final decision, date and participants: pending team review.
