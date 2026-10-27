# ADR-009 — Internal architecture: hexagonal layers, dependency injection and enforcement

**Status:** Proposed
**Date:** 2026-10-27
**Participants:** Ricardo (P2, Tech Lead) — proposer; team review pending
**Related decision:** DEC-04
**Supersedes / superseded by:** —

## Context

[ADR-001](ADR-001-backend-boundaries.md) splits the system into deployable units by bounded context; this ADR decides how each unit is organised inside. The EN-01-02 [domain model](../07-technical-design.md#2-domain-model-and-data-ownership) and [state machines](../07-technical-design.md#3-states-and-business-rules) must stay free of framework code so they can be tested without a database or broker, and so the same pattern repeats in three runtimes (Java, Python, TypeScript). Several decisions already rely on it: the notification facade and channel adapters ([ADR-007](ADR-007-notification-service.md)), the triage facade and provider adapters ([ADR-008](ADR-008-ai-triage-service.md)), the calendar port ([ADR-006](ADR-006-calendar-simulator.md)) and the object storage port ([ADR-010](ADR-010-object-storage.md)).

The rule is only worth having if it is checked. Conventions without a failing build erode, so each runtime gets a test that fails when a dependency points the wrong way.

## Alternatives

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Hexagonal / onion layers with test-enforced rules** | Domain testable alone; adapters replaceable (provider, channel, calendar, storage); the boundaries are executable | Some boilerplate (ports, mappers); team must learn the layering | E56, E57 |
| B. Layered MVC by convention | Familiar; least code | Nothing prevents controllers or JPA entities leaking into the domain; no check | — |
| C. InversifyJS in the client | Container-style DI | Needs `reflect-metadata` with `emitDecoratorMetadata`, which esbuild (used by Vite) does not support; the React binding was last published 2024-12-27 | E55 |
| D. `dependency-injector` in Flask | Declarative containers | More concepts than a small service needs; manual wiring in one function is enough | E57 |
| E. Spring Modulith module verification alone | Checks module boundaries inside one application | Our services are already separate deployables; it does not check the layering inside a module. It could still be adopted later within a large service. Its verification feature was not read for this ADR | — (E14 covers Modulith events only) |

## Proposed decision

**A**, proposed, not accepted, with the rules below in every service.

**Layers.**

| Layer | Contains | May depend on |
|---|---|---|
| `domain` | Entities, aggregates, value objects, state machines from EN-01-02, domain events, domain errors | Nothing but the language standard library |
| `application` | Use cases (commands and queries), ports (interfaces): repositories, event publisher/outbox, notification channel, calendar, AI provider, object storage, clock | `domain` |
| `adapters.in` | REST controllers, RabbitMQ listeners, Flask routes, scheduled jobs | `application`, `domain` (through DTO mapping) |
| `adapters.out` | JPA repositories, outbox writer, SMTP/in-app channels, calendar HTTP client, AI provider client, S3 client | `application`, `domain` |
| composition root | Wiring of ports to adapters; configuration | Everything |

**Dependency rule.** Dependencies point inwards only: `adapters` → `application` → `domain`. `domain` has no framework imports (no Spring, JPA or Jackson annotations, no Flask, no pika). `adapters.in` and `adapters.out` do not depend on each other. Adapters map between transport/persistence models and domain objects; JPA entities are adapter classes, not the domain aggregates.

**Composition root per runtime.**

| Runtime | Composition root |
|---|---|
| Java (Spring Boot) | Spring dependency injection: constructor injection, `@Configuration` classes wire ports to adapters; use cases are plain classes registered as beans |
| Flask | Manual composition root in `create_app()` (and a matching consumer factory): build adapters, build the facade, pass them in. No DI library |
| React client | React Context composition root: `<ServicesProvider>` and `useServices()` |

**Client ports.** TypeScript interfaces `IssueApi`, `DispatchApi`, `NotificationApi`, `AuthSession` and `Clock`, implemented over the generated OpenAPI fetch client. TanStack Query hooks call ports obtained from `useServices()`; tests provide fake implementations. A custom `AuthProvider` loads the session from `GET /api/issue/me` and redirects to `/oauth2/start` on `401` ([ADR-005](ADR-005-authentication-authorisation.md)). Hiding UI is never the authorisation control.

**Mapping of EN-01-02 to `domain`.** The aggregates of [design §2](../07-technical-design.md#2-domain-model-and-data-ownership) become domain packages: in Issue — `Report`, `Issue`, `TriageSuggestion`, `ImpactConfirmation`, `Membership`; in Dispatch — `Intervention`, `ProposalVersion`, `Booking`, `Contractor`. `Invitation` and `Attachment` (Issue) and the projections (Dispatch) are additions of this proposal and not yet in EN-01-02. The transition allow-lists of [design §3](../07-technical-design.md#3-states-and-business-rules) are domain methods that reject anything not listed, without side effects. Versions (`If-Match`) and event-version rules are enforced in `application`.

**Ports per service** (names indicative).

| Service | Output ports |
|---|---|
| Issue | `IssueRepository`, `ReportRepository`, `MembershipRepository`, `InvitationRepository`, `AttachmentRepository`, `EventOutbox`, `ObjectStoragePort`, `Clock` |
| Dispatch | `InterventionRepository`, `BookingRepository`, `ContractorRepository`, `CalendarPort`, `AdminProjectionRepository`, `EventOutbox`, `Clock` |
| Notification | `NotificationRepository`, `PreferenceRepository`, `DeliveryLogRepository`, `NotificationChannel` (`InAppChannelAdapter`, `EmailChannelAdapter`), `UserDirectory` (Keycloak address lookup), `Clock` |
| AI triage | `AiProvider`, `RulesBaseline`, `EventPublisher`, `Clock` |

The shared infrastructure starter `platform/bmc-messaging-spring-boot-starter` ([ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)) provides the outbox and consumer plumbing as an `adapters`-level library with no domain types; services do not share a domain library.

**Layout sketches.**

```text
services/issue/src/main/java/.../issue/
  domain/          report/ issue/ membership/ triage/ attachment/
  application/     command/ query/ port/in/ port/out/
  adapters/in/     rest/ messaging/
  adapters/out/    persistence/ outbox/ storage/
  config/          composition root (Spring @Configuration)

services/ai-triage/src/triage/
  domain/ application/ adapters/in/ (http, consumer) adapters/out/ (providers, rules, publisher)
  app.py           create_app() and consumer factory

apps/client/src/
  domain/ (types)  ports/ (IssueApi, ...)  adapters/ (openapi clients)
  features/ (screens + TanStack Query hooks)  app/ (ServicesProvider, routes)
```

**CQRS** is used only as separate `command` and `query` packages inside `application`: commands go through the aggregates and the outbox, queries read projections for a role. There is no separate read store and no event sourcing.

**Enforcement** (run in CI once CI exists; EN01-U9):

| Runtime | Tool | Check |
|---|---|---|
| Java | ArchUnit 1.5.1 `onionArchitecture()` (E56) | Domain, application and adapter layers in one test per service; plus a rule that `domain` imports no `org.springframework`, `jakarta.persistence` or `com.fasterxml` packages. Java 25 support to confirm in the spike (item 10) |
| Python | import-linter 2.15 `layers` and `independence` contracts (E57) | `adapters` → `application` → `domain`; `adapters.in` independent of `adapters.out` |
| Client | eslint-plugin-boundaries 7.3.0 (E57) | Features depend on ports, not on adapters; `domain` imports nothing |

## Consequences

- More files per feature (port, adapter, mapper) in exchange for testable domain and replaceable adapters; the cost is real for a team that has not used the pattern, and the Java premise is still to be confirmed (EN01-U1).
- Fakes for ports make unit tests fast; integration tests still run against real MySQL and RabbitMQ containers ([ADR-002](ADR-002-technology-stack.md)).
- A failing architecture test blocks a merge once CI runs; until CI exists the rule rests on review.
- Each service repeats the structure; no shared domain library keeps services independently deployable.

## Verification and review

Spike item 10: ArchUnit `onionArchitecture()` runs on Java 25 and fails on a deliberately wrong dependency. Equivalent negative checks for import-linter and eslint-plugin-boundaries when the first Python and client code exist. Review after the first implementation slice: if the layering costs more than it protects, relax the rules by a new ADR, not silently.

## Record

2026-10-27 — proposed by Ricardo (Tech Lead) after a structured design interview; drafting and source checks AI-assisted (new ADR). Reason: one architectural pattern across Java, Python and TypeScript with executable boundary checks. Evidence: [evidence register](README.md#evidence-register-en-01-01) E14, E55–E57. Affected documents: [technical design §1](../07-technical-design.md#1-context-and-boundaries). Final decision, date and participants: pending team review. Issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15).
