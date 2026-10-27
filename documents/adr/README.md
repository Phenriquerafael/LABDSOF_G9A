# Architecture Decision Records

**Status:** ADR-001–006 first proposed in EN-01-01 on 2026-10-15 and revised on 2026-10-27; ADR-007–012 proposed on 2026-10-27; team review pending, no ADR accepted

ADRs document context, alternatives, choice, consequences and evidence. “Proposed” does not justify claiming that a technology was selected or that a monolith exception was accepted.

| ADR | Topic | Status |
|---|---|---|
| [ADR-001](ADR-001-backend-boundaries.md) | Backend boundaries, data ownership and communication | Proposed (revised 2026-10-27) |
| [ADR-002](ADR-002-technology-stack.md) | Technology stack: Spring Boot services, Flask AI service, React client, MySQL, contracts | Proposed (revised 2026-10-27) |
| [ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md) | Asynchronous messaging: transactional outbox, RabbitMQ, idempotent consumers | Proposed (revised 2026-10-27) |
| [ADR-004](ADR-004-deployment-contract.md) | Deployment contract: Traefik edge, Compose, images, pipeline and observability | Proposed (revised 2026-10-27) |
| [ADR-005](ADR-005-authentication-authorisation.md) | Keycloak identity, Backend-for-Frontend session and membership-based authorisation | Proposed (revised 2026-10-27) |
| [ADR-006](ADR-006-calendar-simulator.md) | External calendar simulator as a separate process, and reconciliation | Proposed (revised 2026-10-27) |
| [ADR-007](ADR-007-notification-service.md) | Notification service: facade and channel adapters | Proposed |
| [ADR-008](ADR-008-ai-triage-service.md) | AI triage service in Flask | Proposed |
| [ADR-009](ADR-009-service-internal-architecture.md) | Internal architecture: hexagonal layers, dependency injection and enforcement | Proposed |
| [ADR-010](ADR-010-object-storage.md) | S3-compatible object storage for attachments and backups | Proposed |
| [ADR-011](ADR-011-installable-pwa-client.md) | Client: installable PWA, photos, online-only operation and status banner | Proposed |
| [ADR-012](ADR-012-health-and-status-page.md) | Health checks and the public status page | Proposed |
| To be created after comparison | AI provider/model and evaluation | Undecided in DEC-05 |

Use the [template](../templates/adr.md). States: Proposed → Accepted or Rejected; an accepted decision may be Superseded by a new ADR, preserving history. Record participants/date and links to evidence or feedback.

ADR-001–012 are proposals prepared by the Tech Lead in EN-01-01 ([#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15)). They become Accepted only after a team review records participants and date, and an independent PR review. Product and process decisions belong in the [register](../planning/decisions-and-feedback.md). A practical companion for the identity setup is the [Keycloak setup guide](../guides/keycloak-setup.md).

ADR-001–006 were revised in place on 2026-10-27 rather than superseded, because none had been accepted or merged. The 2026-10-15 versions (Elysia on Bun, Prisma, MySQL 9.7, outbox relay without a broker, own login) remain in the Git history of this branch (commits `d0bb844` and `a66f896`), with their evidence register.

## Evidence register (EN-01-01)

Unless a row says otherwise, sources were accessed on 2026-10-27. Versions and terms change; re-check them before relying on a number after that date. Type: **O** = official documentation, release data or registry metadata; **C** = community or secondary source (for example endoflife.date, Docker Hub listings, news articles); **A** = assignment or project document. None of these sources is a benchmark run by the team. Most rows come from AI-assisted research passes that read pages through a summarising tool. In the Tech Lead's AI-assisted session, the load-bearing facts were then re-fetched directly from the source page (E04, E11, E27, E30, E32, E35, E40, E45, E46, E49, E53, E55), and release and registry data was queried directly from the GitHub, npm, PyPI, Docker Hub and endoflife.date APIs (E25, E26, E31, E34, E37, E44, E52, E54, E58). Other rows were not re-checked individually; quote a figure verbatim only after opening the URL. Rows E64–E83 were added on 2026-10-27 for the client (ADR-011) and health/status (ADR-012) decisions; caniuse rows were read from the caniuse data repository on GitHub, not the rendered site.

### Assignment and project

| ID | Source | URL | Recorded fact |
|---|---|---|---|
| E01 | Assignment §6 | [LABDSOF-26-27-Assignment.md](../../LABDSOF-26-27-Assignment.md) (PDF copy: [LABDSOF-26-27-Assignment.pdf](../../LABDSOF-26-27-Assignment.pdf)) | A — §6.2 at least two independently deployable backend components; §6.3 at least one meaningful asynchronous workflow with retries, duplicates, failures and eventual consistency (no broker required); §6.4 avoid multiple database technologies unless justified; §6.5 external system or realistic simulator, handling unavailable/delayed/incomplete/invalid data; §6.6 footnote allows mocked authentication; §6.7 logs, health, metrics, correlation, error reporting, dashboard; §6.8 one degraded-mode scenario |
| E02 | DEVOPS-01 pull request | https://github.com/Phenriquerafael/LABDSOF_G9A/pull/40 | A — proposed, open, not merged: `feature/* → dev → main`, release by protected `v*` tag, build once and promote the same image, GHCR |
| E03 | 2026-10-15 proposal and register | Branch history, commits `d0bb844` and `a66f896` | A — Elysia/Bun, Prisma, MySQL 9.7, outbox relay without a broker and own login, with sources accessed 2026-10-15 |

### Java services

| ID | Source | URL | Recorded fact |
|---|---|---|---|
| E04 | Spring Boot system requirements | https://docs.spring.io/spring-boot/system-requirements.html | O — Spring Boot 4.1.2 is current; “requires at least Java 17 and is compatible with versions up to and including Java 27”; Maven 3.6.3+ |
| E05 | Spring Initializr metadata | https://start.spring.io/metadata/client | O — default `bootVersion` 4.1.2; Java 17, 21, 25 and 27 offered |
| E06 | Spring Boot lifecycle | https://endoflife.date/api/spring-boot.json | C — 4.1 released 2026-06-30, end of OSS support 2027-07-31; 4.0 ends 2026-12-31 |
| E07 | Java LTS lifecycle | https://endoflife.date/api/oracle-jdk.json · https://endoflife.date/api/eclipse-temurin.json | C — LTS releases 17, 21 and 25; Temurin 25 supported to 2031-09-30; 26 and 27 are not LTS |
| E08 | eclipse-temurin images | https://hub.docker.com/_/eclipse-temurin | C — JRE images for 25 published for amd64 and arm64 (Alpine and UBI variants checked; Ubuntu variants not checked) |
| E09 | Spring Boot 4.1 release notes | https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.1-Release-Notes | O — managed versions include Hibernate 7.4, Flyway 12.4.0, Spring AMQP 4.1.0 and Spring Security 7.1.0 |
| E10 | Hibernate ORM releases | https://hibernate.org/orm/releases/ | O — 7.4.14.Final latest stable (2026-10-25) |
| E11 | Flyway MySQL driver reference | https://documentation.red-gate.com/flyway/reference/database-driver-reference/mysql | O — “Verified Versions: 5.7, 8.0, 9.4”; MySQL 8.4 not listed; open-source artifact `org.flywaydb:flyway-mysql` |
| E12 | Spring Boot AMQP reference | https://docs.spring.io/spring-boot/reference/messaging/amqp.html | O — `spring-boot-starter-amqp`; listener retries off by default; a throwing listener is redelivered indefinitely unless requeue is disabled; after retries are exhausted the message is rejected and dropped or dead-lettered according to broker configuration |
| E13 | Spring AMQP publisher confirms | https://docs.spring.io/spring-amqp/reference/amqp/template.html | O — confirms via `ConfirmType.CORRELATED` with `CorrelationData`; returns need `mandatory` and `publisherReturns` |
| E14 | Spring Modulith events | https://docs.spring.io/spring-modulith/reference/events.html | O — event publication registry written in the business transaction; externalisation to AMQP with `@Externalized`; the docs state the native approach “lacks critical features developers might expect from actual outbox pattern implementations” and point to dedicated libraries |
| E15 | Namastack Outbox | https://github.com/namastack/namastack-outbox | O/C — v1.11.0 (2026-10-19), Apache-2.0, JPA and RabbitMQ modules, MySQL example; about 400 stars |
| E16 | Spring Security resource server | https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html | O — `spring.security.oauth2.resourceserver.jwt.issuer-uri` / `jwk-set-uri`; Boot auto-configures the `JwtDecoder` |
| E17 | Spring Security client credentials | https://docs.spring.io/spring-security/reference/servlet/oauth2/client/authorization-grants.html | O — `client_credentials` registration with an `OAuth2AuthorizedClientManager` |
| E18 | Spring Cloud | https://spring.io/projects/spring-cloud · https://github.com/spring-cloud/spring-cloud-stream/releases · https://github.com/spring-cloud/spring-cloud-gateway/releases | O — train 2025.1.x supports Boot 4.1.x from 2025.1.2; Spring Cloud Stream and Spring Cloud Gateway 5.0.4 (2026-10-23) |
| E19 | Spring gRPC | https://github.com/spring-projects/spring-grpc/releases · https://docs.spring.io/spring-grpc/reference/getting-started.html | O — 1.1.2 (2026-10-26); the docs say “Spring gRPC 1.0.x supports Spring Boot 4.1.x”; a 1.1.x pairing is not stated |

### Python AI service

| ID | Source | URL | Recorded fact |
|---|---|---|---|
| E20 | Flask changelog and deployment | https://flask.palletsprojects.com/en/stable/changes/ · https://flask.palletsprojects.com/en/stable/deploying/ | O — 3.1.3 (2026-02-18); “Do not use the development server when deploying to production”; Gunicorn among the listed WSGI servers |
| E21 | Gunicorn on PyPI | https://pypi.org/pypi/gunicorn/json | C — 26.2.0, requires Python ≥ 3.10 |
| E22 | Python versions | https://devguide.python.org/versions/ | O — 3.14 and 3.15 in bugfix (3.15 first released 2026-10-09); 3.14 end of life 2030-10 |
| E23 | python images | https://hub.docker.com/_/python | C — 3.14 and 3.15 slim images for amd64 and arm64 |
| E24 | pika | https://pika.github.io/pika/latest/faq/ · https://pypi.org/pypi/pika/json | O — connections are not thread-safe and must stay on the thread that created them; 1.4.4 stable (2026-08-06) |
| E25 | prometheus-client on PyPI | https://pypi.org/pypi/prometheus-client/json | C — 0.26.0 |

### Identity and edge

| ID | Source | URL | Recorded fact |
|---|---|---|---|
| E26 | Keycloak release | https://github.com/keycloak/keycloak/releases | O — 26.8.1 published 2026-10-13 |
| E27 | Keycloak databases | https://www.keycloak.org/server/db | O — MySQL tested 8.4, supported 8.4 (LTS) and 8.0 (LTS), “configurations outside these versions are not supported”; set `sql_generate_invisible_primary_key=OFF` before install or upgrade; `binlog_format=STATEMENT` not allowed |
| E28 | Keycloak sizing and containers | https://www.keycloak.org/high-availability/single-cluster/concepts-memory-and-cpu-sizing · https://www.keycloak.org/server/containers | O — base memory 1250 MB per instance; heap 70% of the container limit by default; always set a memory limit |
| E29 | Keycloak realm import; Admin API emails | https://www.keycloak.org/server/importExport · https://forum.keycloak.org/t/does-creating-a-new-user-via-api-send-a-confirmation-email/20646 | O/C — `--import-realm` reads `/opt/keycloak/data/import/*.json` and skips existing realms; (C) creating a user sends no email, `execute-actions-email` does |
| E30 | RFC 10017 | https://www.rfc-editor.org/info/rfc10017 · https://datatracker.ietf.org/doc/draft-ietf-oauth-browser-based-apps/ | O — *OAuth 2.0 for Browser-Based Applications*, BCP 212, published 2026; public browser clients must use PKCE; a Backend-for-Frontend is strongly recommended for business applications and applications handling personal data |
| E31 | oauth2-proxy | https://github.com/oauth2-proxy/oauth2-proxy/releases · https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/keycloak_oidc · https://oauth2-proxy.github.io/oauth2-proxy/configuration/session_storage | O — v7.15.5 (2026-10-01); `keycloak-oidc` provider (audience mapper needed); encrypted cookie session storage by default, Redis optional |
| E32 | oauth2-proxy with Traefik | https://oauth2-proxy.github.io/oauth2-proxy/configuration/integrations/traefik | O — documented ForwardAuth integration; `authResponseHeaders` pass `Authorization` and `X-Auth-Request-Access-Token` upstream; `--reverse-proxy=true`; a no-auto-redirect route returns `401` for an unauthenticated session |
| E33 | SPA OIDC libraries | https://registry.npmjs.org/keycloak-js · https://registry.npmjs.org/@react-keycloak/web · https://registry.npmjs.org/react-oidc-context · https://registry.npmjs.org/oidc-client-ts | O — keycloak-js 26.2.4 (2026-04-22); `@react-keycloak/web` last published 2020-10-21; react-oidc-context 3.3.1 and oidc-client-ts 3.5.0 (2026-03-13) |
| E34 | Traefik release and image | https://github.com/traefik/traefik/releases · https://hub.docker.com/_/traefik | O — v3.7.16 (2026-10-20); images for amd64, arm64 and others |
| E35 | Traefik middlewares | https://doc.traefik.io/traefik/reference/routing-configuration/http/middlewares/overview/ | O — JWT, OIDC, Token Introspection and API key middlewares are Traefik Hub only; ForwardAuth, RateLimit, Retry, CircuitBreaker, Headers and InFlightReq are in Traefik Proxy |
| E36 | Traefik observability | https://doc.traefik.io/traefik/reference/install-configuration/observability/logs-and-accesslogs/ · https://doc.traefik.io/traefik/reference/install-configuration/observability/metrics/ | O — JSON access logs with selected headers; Prometheus metrics; no built-in request-ID generator found |

### Messaging and contracts

| ID | Source | URL | Recorded fact |
|---|---|---|---|
| E37 | RabbitMQ release and image | https://github.com/rabbitmq/rabbitmq-server/releases · https://hub.docker.com/_/rabbitmq | O/C — 4.4.0 published 2026-10-19; 4.3.7 on the previous line; `4.4-management-alpine` for amd64 and arm64 |
| E38 | RabbitMQ quorum queues | https://www.rabbitmq.com/docs/quorum-queues | O — “Starting with RabbitMQ 4.0, the delivery limit for quorum queues defaults to 20”; dead-lettering through DLX; at-most-once is the default dead-letter strategy, at-least-once keeps messages until the target confirms (more resources, possible duplicates); classic mirroring removed in 4.0 |
| E39 | RabbitMQ confirms, memory, management | https://www.rabbitmq.com/docs/confirms · https://www.rabbitmq.com/docs/memory · https://www.rabbitmq.com/docs/management | O — use publisher confirms to guarantee persistence; consumers must be prepared to handle redeliveries; automatic ack is unsafe; memory high watermark defaults to 0.6 of RAM; management UI on port 15672 |
| E40 | Dapr | https://github.com/dapr/dapr/releases · https://docs.dapr.io/developing-applications/building-blocks/state-management/howto-outbox/ · https://docs.dapr.io/operations/hosting/self-hosted/self-hosted-with-docker/ | O — v1.19.0 (2026-10-22); the outbox notifies subscribers of state written through Dapr's transactional state API; one sidecar container per application plus placement and scheduler services in Compose |
| E41 | Buf | https://github.com/bufbuild/buf/releases · https://buf.build/docs/breaking/ | O — v1.75.0 (2026-10-22); `buf breaking` compares against a previous version (Git and others); lint and generation for many languages |
| E42 | AsyncAPI | https://www.asyncapi.com/docs/reference/specification/v3.0.0 · https://github.com/asyncapi/spec/releases | O — `schemaFormat` lists Protocol Buffers; v3.1.0 (2026-01-31) |
| E43 | CloudEvents | https://github.com/cloudevents/spec · https://github.com/cloudevents/sdk-java/releases · https://pypi.org/pypi/cloudevents/json | O — spec v1.0.2 with Protobuf format and AMQP protocol binding; Java SDK 5.1.0 (2026-10-13); Python SDK 2.2.0 |

### Data, storage and notifications

| ID | Source | URL | Recorded fact |
|---|---|---|---|
| E44 | MySQL lifecycle and image | https://endoflife.date/api/mysql.json · https://hub.docker.com/_/mysql | C — 8.4 LTS: latest 8.4.13 (2026-09-30), support to 2029-04-30, end of life 2032-04-30; 8.0 end of life 2026-04-30; 9.7 LTS exists but is not supported by Keycloak (E27); `mysql:8.4` for amd64 and arm64 |
| E45 | MinIO repository | https://github.com/minio/minio | O — “THIS REPOSITORY IS NO LONGER MAINTAINED”; “The MinIO community edition is now distributed as source code only”; archived on 2026-04-25 |
| E46 | Garage | https://garagehq.deuxfleurs.fr/documentation/quick-start/ · https://garagehq.deuxfleurs.fr/documentation/reference-manual/s3-compatibility/ · https://garagehq.deuxfleurs.fr/ · https://github.com/deuxfleurs-org/garage | O — `dxflrs/garage:v2.5.0`; `garage server --single-node --default-bucket` with default credentials from environment variables; S3 API on port 3900; single-node “should not be used in production, as it provides no redundancy”; presigned URLs, multipart and CORS implemented; no object versioning; about 1 GB RAM; AGPL-3.0 (mirror repository) |
| E47 | SeaweedFS | https://github.com/seaweedfs/seaweedfs · https://github.com/seaweedfs/seaweedfs/wiki/Amazon-S3-API | O — 4.51 (2026-10-25), Apache-2.0; presigned URLs, multipart, CORS and versioning supported |
| E48 | RustFS | https://github.com/rustfs/rustfs | O — Apache-2.0; 1.0.4 (2026-10-25), first 1.0 line in October 2026; features labelled Available or Preview; images for amd64 and arm64 |
| E49 | Cloudflare R2 | https://developers.cloudflare.com/r2/pricing/ · https://developers.cloudflare.com/r2/api/s3/api/ · https://developers.cloudflare.com/r2/examples/aws/aws-sdk-java/ | O — free tier per month: 10 GB-month storage, 1 million Class A and 10 million Class B operations, no egress charge; bucket versioning not implemented; partial checksum support; Java example uses `endpointOverride`, region `auto`, path-style access and `chunkedEncodingEnabled(false)` |
| E50 | AWS SDK data integrity | https://docs.aws.amazon.com/sdkref/latest/guide/feature-dataintegrity.html · https://docs.aws.amazon.com/boto3/latest/guide/configuration.html · https://gitlab.com/gitlab-org/gitlab-runner/-/merge_requests/6691 | O/C — SDKs since December 2024 send CRC checksums by default (`WHEN_SUPPORTED`); `request_checksum_calculation=WHEN_REQUIRED` / `AWS_REQUEST_CHECKSUM_CALCULATION` disables this; (C) the new default broke third-party S3 providers in another SDK |
| E51 | S3 SDK versions | https://repo1.maven.org/maven2/software/amazon/awssdk/s3/maven-metadata.xml · https://pypi.org/pypi/boto3/json | O — AWS SDK for Java v2 `s3` 2.57.4; boto3 1.43.119 |
| E52 | Mailpit | https://github.com/axllent/mailpit/releases · https://mailpit.axllent.org/docs/ | O — v1.32.0 (2026-10-22); SMTP server that captures mail and shows it in a web UI with an API; multi-arch images `axllent/mailpit` |
| E53 | Gmail App Passwords | https://support.google.com/accounts/answer/185833 | O — “App passwords can only be used with accounts that have 2-Step Verification turned on”; not available for work/school accounts or with Advanced Protection; revoked when the account password changes |

### Client, architecture tooling and observability

| ID | Source | URL | Recorded fact |
|---|---|---|---|
| E54 | Client packages (npm registry) | https://registry.npmjs.org/ (`react`, `vite`, `tailwindcss`, `vite-plugin-pwa`, `shadcn`, `@tanstack/react-router`, `@tanstack/react-query`, `openapi-typescript`, `openapi-fetch`) | O — react 19.3.1 (2026-10-14), vite 8.3.5 (2026-10-21), tailwindcss 4.3.3, vite-plugin-pwa 2.0.0, shadcn CLI 4.22.1 (2026-10-18), @tanstack/react-router 1.170.46 (2026-10-22), @tanstack/react-query 5.105.0 (2026-10-26), openapi-typescript 7.13.0 and openapi-fetch 0.17.0; all MIT |
| E55 | InversifyJS and esbuild | https://inversify.io/docs/introduction/getting-started/ · https://esbuild.github.io/content-types/ · https://registry.npmjs.org/inversify-react | O — Inversify 8.2.3 needs `reflect-metadata` with `experimentalDecorators` and `emitDecoratorMetadata`; esbuild: “The `emitDecoratorMetadata` TypeScript configuration option is not supported”; inversify-react last published 2024-12-27 |
| E56 | ArchUnit | https://www.archunit.org/userguide/html/000_Index.html · https://repo1.maven.org/maven2/com/tngtech/archunit/archunit/maven-metadata.xml | O — 1.5.1; `onionArchitecture()` with domain models, domain services, application services and adapters that may not depend on each other |
| E57 | Python and frontend boundary tools | https://import-linter.readthedocs.io/en/stable/contract_types/ · https://pypi.org/pypi/dependency-injector/json · https://registry.npmjs.org/eslint-plugin-boundaries · https://registry.npmjs.org/dependency-cruiser | O — import-linter 2.15 with `layers` and `independence` contracts (Python 3.14 classifier); dependency-injector 4.49.1; eslint-plugin-boundaries 7.3.0; dependency-cruiser 18.7.0 |
| E58 | Prometheus and Grafana | https://github.com/prometheus/prometheus/releases · https://github.com/grafana/grafana/releases | O — Prometheus v3.15.1 (2026-10-21); Grafana v13.2.4 (2026-10-13) |

### Hosting and other (accessed 2026-10-15, carried over)

| ID | Source | URL | Recorded fact |
|---|---|---|---|
| E59 | Docker Compose in production | https://docs.docker.com/compose/how-tos/production/ | O — “The easiest way to deploy an application is to run it on a single server” |
| E60 | Managed free tiers | https://render.com/docs/free · https://docs.fly.io/about/pricing · https://docs.railway.com/reference/pricing/plans · https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm | O — Render free services spin down after 15 minutes idle; Fly.io trial only; Railway one-time USD 5 trial; Oracle Always Free Ampere A1 (arm64) 2 OCPUs / 12 GB |
| E61 | Zitadel licence | https://github.com/zitadel/zitadel | O — AGPL-3.0 |
| E62 | Stack Overflow Developer Survey 2025 | https://survey.stackoverflow.co/2025/technology | O — web frameworks: Spring Boot 14.7%, ASP.NET Core 19.7%, FastAPI 14.8%, NestJS 6.7% |
| E63 | Gemini API terms and models | https://ai.google.dev/gemini-api/terms · https://ai.google.dev/gemini-api/docs/models | O — unpaid data may be used to improve products, but in the EEA/Switzerland/UK paid-service data terms apply to unpaid quota; users must be 18+; stable Flash models listed (model choice remains DEC-05) |

### Client: installable PWA and photos

| ID | Source | URL | Recorded fact |
|---|---|---|---|
| E64 | Chrome install criteria | https://web.dev/articles/install-criteria | O — Chrome installs over HTTPS for an engaged user when the manifest has `name` or `short_name`, 192 px and 512 px `icons`, `start_url` and a `display` of `standalone` (or fullscreen, minimal-ui, window-controls-overlay); no service worker requirement is listed (page updated 2024-09-19) |
| E65 | `beforeinstallprompt` | https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeinstallprompt_event · https://raw.githubusercontent.com/Fyrd/caniuse/main/features-json/web-app-manifest.json | O/C — non-standard (WICG incubation), “limited availability”; pattern: `preventDefault()`, keep the event, call `prompt()` from an install button; (C) install supported in Chrome, Edge, Samsung Internet and Android Chrome, not in desktop Firefox, partial in Safari |
| E66 | Safari web apps | https://webkit.org/blog/16993/news-from-wwdc25-web-technology-coming-in-safari-26-beta/ · https://webkit.org/blog/14445/webkit-features-in-safari-17-0/ | O — Safari 26: “every website added to the Home Screen opens as a web app” by default; no programmatic install prompt is described; macOS Safari 17 “File > Add to Dock” |
| E67 | Camera capture | https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/capture · https://raw.githubusercontent.com/Fyrd/caniuse/main/features-json/html-media-capture.json | O/C — `capture="environment"` on `<input type="file">` works on mobile; desktop shows a file picker; (C) iOS Safari does not force the camera with `capture` but offers it |
| E68 | HEIC | https://raw.githubusercontent.com/Fyrd/caniuse/main/features-json/heif.json · https://bugs.webkit.org/show_bug.cgi?id=303803 | C — HEIC decodes in Safari only (not Chrome, Firefox or Android Chrome); Safari's transcoding of HEIC in file inputs is documented only in bug reports |
| E69 | Client-side image processing | https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob · https://raw.githubusercontent.com/Fyrd/caniuse/main/features-json/createimagebitmap.json | O/C — `toBlob` falls back to PNG for an unsupported type, so `blob.type` must be checked; JPEG and WebP are common but not required; (C) `createImageBitmap` and `OffscreenCanvas` supported in current Chrome, Safari, iOS Safari and Firefox |
| E70 | Offline support limits | https://raw.githubusercontent.com/Fyrd/caniuse/main/features-json/background-sync.json · https://webkit.org/blog/14403/updates-to-storage-policy/ · https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/ | O/C — (C) Background Sync only in Chromium browsers, not Safari or iOS Safari; Safari storage is best-effort, and script-writable storage can be deleted after seven days of Safari use without interaction (Home Screen web apps keep their own counter) |
| E71 | Web Push | https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/ · https://raw.githubusercontent.com/Fyrd/caniuse/main/features-json/push-api.json · https://repo1.maven.org/maven2/nl/martijndwars/web-push/maven-metadata.xml | O/C — iOS/iPadOS 16.4+ only for web apps added to the Home Screen, permission from a user gesture; (C) Push API in Chrome, Edge, Firefox, macOS Safari and Samsung; Java library `nl.martijndwars:web-push` last released 5.1.2 on 2025-02-17 |
| E72 | vite-plugin-pwa and Workbox | https://registry.npmjs.org/vite-plugin-pwa · https://vite-pwa-org.netlify.app/guide/auto-update.html · https://registry.npmjs.org/workbox-window | O — vite-plugin-pwa 2.0.0 (2026-10-03) with Vite `^8.0.0` in its peer range; `autoUpdate` reloads open tabs and “the user can lose data” in forms, `prompt` leaves the update to the user; workbox-window 7.4.1 |

### Health checks and status page

| ID | Source | URL | Recorded fact |
|---|---|---|---|
| E73 | Spring Boot Actuator | https://docs.spring.io/spring-boot/reference/actuator/endpoints.html · https://docs.spring.io/spring-boot/reference/actuator/monitoring.html | O — 4.1.2 docs: liveness and readiness groups enabled automatically, optionally also on the main port (`/livez`, `/readyz`); health groups with `include`/`exclude` and additional paths; built-in `db`, `rabbit` and `mail` indicators; `DOWN` maps to HTTP 503; `show-details` defaults to `never`; base path and path mapping configurable |
| E74 | Traefik health | https://doc.traefik.io/traefik/reference/install-configuration/observability/healthcheck/ · https://doc.traefik.io/traefik/reference/routing-configuration/http/load-balancing/service/ · https://doc.traefik.io/traefik/reference/install-configuration/api-dashboard/ | O — `/ping` reports Traefik's own liveness only; `loadBalancer.healthcheck` (path, interval, timeout) per service, settable through Docker labels; enabling the API/dashboard in production “is not recommended” because it exposes all configuration |
| E75 | Gatus | https://github.com/TwiN/gatus · https://raw.githubusercontent.com/TwiN/gatus/master/README.md · https://hub.docker.com/r/twinproduction/gatus | O — v5.37.0 (2026-09-24), Apache-2.0; YAML-configured checks with conditions; read-only JSON API (`/api/v1/endpoints/statuses`); Prometheus metrics; per-endpoint `ui.hide-hostname`, `hide-url`, `hide-port`, `hide-conditions`, `hide-errors`; announcements and maintenance windows; uptime data up to 30 days; storage keeps 100 results per endpoint by default; its UI “does not support path-based routing”; image built `FROM scratch` (no shell), amd64/arm64/armv7, about 26 MB |
| E76 | Uptime Kuma and Statping-ng | https://github.com/louislam/uptime-kuma · https://github.com/louislam/uptime-kuma/wiki/Reverse-Proxy · https://github.com/statping-ng/statping-ng | O/C — Uptime Kuma 2.5.8 (2026-10-26), MIT, configured through its web UI, “does not support a subdirectory”, image about 617 MB; Statping-ng GPL-3.0, maintenance status not verified |
| E77 | Platform health checks | https://www.keycloak.org/observability/health · https://www.rabbitmq.com/docs/monitoring · https://dev.mysql.com/doc/refman/8.4/en/mysqladmin.html | O/C — Keycloak `/health/ready` on management port 9000 with `KC_HEALTH_ENABLED`; curl removed from the image, the docs' check uses Bash `/dev/tcp`; RabbitMQ staged checks starting with `rabbitmq-diagnostics -q ping`, whose CLI has a performance cost; `mysqladmin ping` exits 0 even on “Access denied” |
| E78 | Other health endpoints | https://garagehq.deuxfleurs.fr/documentation/reference-manual/admin-api/ · https://oauth2-proxy.github.io/oauth2-proxy/features/endpoints · https://raw.githubusercontent.com/axllent/mailpit/develop/server/server.go · https://prometheus.io/docs/prometheus/latest/management_api/ · https://grafana.com/docs/grafana/latest/developers/http_api/other/ | O/C — Garage admin `GET /health` (200 with quorum, else 503); oauth2-proxy `/ping` and `/ready`; Mailpit `livez`/`readyz` routes; Prometheus `/-/healthy` and `/-/ready`; Grafana `/api/health` |
| E79 | Compose health | https://docs.docker.com/reference/compose-file/services/#healthcheck | O — `healthcheck` (`test`, `interval`, `timeout`, `retries`, `start_period`); `depends_on` long syntax with `condition: service_healthy` waits for health, the short syntax does not |
| E80 | Status page examples | https://www.githubstatus.com · https://status.openai.com · https://www.cloudflarestatus.com · https://status.atlassian.com · https://vercel-status.com/ · https://slack-status.com | E — observed (text extraction, not rendered): one overall sentence (“All Systems Operational”) then components named by user-visible function; 90-day daily uptime bars on GitHub and Vercel; uptime percentages on OpenAI and Slack; timestamped incident updates; “No incidents reported” on quiet days |
| E81 | Statuspage conventions | https://support.atlassian.com/statuspage/docs/show-service-status-with-components/ · https://support.atlassian.com/statuspage/docs/create-an-incident/ | O — component statuses Operational, Degraded performance, Partial outage, Major outage, Under maintenance; two-level component groups; incident states Investigating, Identified, Monitoring, Resolved with a brief message per update |
| E82 | Banner and message guidance | https://design-system.service.gov.uk/components/notification-banner/ · https://www.nngroup.com/articles/visibility-system-status/ · https://www.nngroup.com/articles/error-message-guidelines/ · https://ui.shadcn.com/docs/components/alert | O — GOV.UK: banners for service-wide problems, used sparingly, one per page, before the `h1`, no dismissal guidance; NN/g: keep users informed, never colour alone, offer remedies; shadcn/ui Alert: icon, title, description, action, no documented ARIA role |
| E83 | WCAG 2.2 | https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html · https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html · https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html | O — 4.1.3 status messages via `role=status` without moving focus; `role=alert` only for important, time-sensitive content; 1.4.1 a visible alternative to colour; 2.5.8 targets at least 24×24 CSS px (with exceptions) |

Checked and not used as evidence: npm weekly download counts (the registry API returned a June–July 2026 window), a blog's claim about the date MinIO stopped publishing images, and RustFS's separate S3 compatibility matrix (not read).
