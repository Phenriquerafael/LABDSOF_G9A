# ADR-008 — AI triage service in Flask

**Status:** Proposed
**Date:** 2026-10-27
**Participants:** Ricardo (P2, Tech Lead) — proposer; Sandro (P4, AI) to confirm; team review pending
**Related decision:** DEC-05 (provider and evaluation stay open there), DEC-04, DEC-07
**Supersedes / superseded by:** — (new ADR; replaces the triage worker of the 2026-10-15 proposal, see Context and Record)

## Context

§6.3 asks for at least one meaningful asynchronous workflow; classifying a report and enriching it with AI is one of the examples (E01). NFR-03 requires that reporting works with AI disabled, with a 10 s timeout per attempt, a visible fallback or pending state and manual correction ([requirements](../requirements.md#non-functional-requirements--constraints)). The [responsible AI assessment](../06-responsible-ai-assessment.md) defines the baseline (versioned rules), the fallback and the controls.

AI-01 and DEC-05 own the provider, model, vocabulary, prompt, dataset and evaluation. This ADR decides only the **shape of the service**: how it runs, how it communicates, how a provider is plugged in, and what happens on failure. Nothing here claims a provider was chosen or any result measured.

The 2026-10-15 proposal had a Bun triage worker that claimed jobs from Issue over internal HTTP endpoints; that design is replaced here. The AI service is stateless and owns no database. It communicates only through RabbitMQ ([ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)); there is no synchronous call between Issue and the AI service.

## Alternatives

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Flask behind Gunicorn (HTTP) + separate pika consumer process, same image** | Small Python service where AI libraries live; HTTP gives health, `/metrics` and an evaluation endpoint; consumer isolated from the WSGI workers | Two process types in one image; Python is a second backend language | E20, E24, E25 |
| B. FastAPI | Async, built-in OpenAPI | The consumer would still need its own process or thread model; no need for async here; Flask was the Tech Lead's choice | E62 (usage only, not a technical argument) |
| C. Triage inside the Issue service (Java) | One fewer deployable | AI client and fallback in the Issue process; harder to disable or scale separately; weakens the visible asynchronous workflow | — |
| D. The 2026-10-15 Bun triage worker claiming jobs over HTTP | Already described | Depends on the removed internal claim endpoints and job table; Bun is no longer in the stack ([ADR-002](ADR-002-technology-stack.md)) | E03 |
| E. Synchronous classification during report submission | Simplest flow | Rejected: a slow or failing provider would delay or fail reporting, against NFR-03 and §6.3 | E01 |

Why not use the Flask development server or one process for both: the Flask documentation says not to use the development server in production and lists Gunicorn among the WSGI servers (E20). pika connections are not thread-safe and must stay on the thread that created them (E24), so the consumer runs as its own process with one connection and channel, not inside a Gunicorn worker thread.

## Proposed decision

**A**, proposed, not accepted.

**Runtime.** Python 3.14, Flask 3.1.3, Gunicorn 26.x, pika 1.4.x, prometheus-client (E20–E25; versions pinned in the lock file). One image, two entry points: `gunicorn` serves the liveness and readiness endpoints (names per [DEVOPS-02 (#42)](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/42); [ADR-012](ADR-012-health-and-status-page.md)), `/metrics` and the internal `POST /classify`; `python -m triage.consumer` consumes `ai-triage.requests`. Health, `/classify` and `/metrics` are internal and never routed by Traefik. `POST /classify` exists for the AI-01 evaluation harness: it runs the same triage facade on a text and returns the result without touching the queue.

**Messages** (contract in [ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md) and `contracts/proto/`):

| Direction | Event | Payload |
|---|---|---|
| In | `TriageRequested` (routing key `issue.TriageRequested`, bound only to `ai-triage.requests`) | `issueId`, `issueVersion`, `buildingId`, `areaKind`, report text needed for classification |
| Out | `TriageSuggested` | `issueId`, `issueVersion`, category, urgency, rationale, `origin` (`ai`, `rules` or `fallback`), `modelVersion`, `promptVersion`, `rulesVersion` |

**Structure** (instance of [ADR-009](ADR-009-service-internal-architecture.md)). A triage facade, `TriageService.classify(request)`, depends on two ports: `AiProvider` and `RulesBaseline`. Provider adapters (adapter pattern) implement `AiProvider`; Gemini Flash on the free tier is the **candidate** adapter (E63), and the actual provider and model remain DEC-05/AI-01 (Sandro). A disabled-AI configuration uses rules only. The composition root is `create_app()` and a matching consumer factory: plain Python wiring, no DI library.

**Behaviour.**

1. Run the rules baseline first so a critical signal is never lost; call the provider with a 10 s timeout per attempt, at most 2 attempts (design §4.6, to calibrate in the spike).
2. Validate the provider output against the schema and the allowed vocabulary. Missing fields, out-of-vocabulary values or malformed output count as a failed attempt.
3. After the attempts, publish the rules result with `origin = fallback`; with AI disabled, `origin = rules`. A successful answer has `origin = ai`. An AI result never removes a rules alert.
4. Publish `TriageSuggested` with the versions of model, prompt and rules, then acknowledge `TriageRequested`. The service keeps no state: a redelivered request is classified again and produces an equivalent message for the same `issueVersion`, and Issue applies it idempotently by `issueVersion`.
5. If nothing arrives within 2 min, Issue shows “triage pending — classify manually”; manual triage is always possible ([design §4.6](../07-technical-design.md#46-retry-timeout-and-lease-values-proposal)).

**Metrics** (`/metrics`): fallback rate, provider latency, provider errors by type, requests consumed and published, consumer redeliveries, DLQ depth (from the broker). No request text in metrics or logs.

**Privacy.** `TriageRequested` is the only message that carries private report text. It is point-to-point, never fanned out; the DLQ `x-message-ttl` is 7 days; payloads are never logged. The text leaves the system for the provider, so DEC-07 and [security §4](../09-security-privacy.md#4-data-lifecycle-and-minimisation) apply: development and demonstration use synthetic data only. For Gemini (E63), unpaid data may be used to improve products unless the EEA/Switzerland/UK paid-service terms apply, and users must be 18+; both points need Sandro's and the team's confirmation before any non-synthetic text is sent.

## Consequences

- AI failure never blocks reporting: the report is stored, the event is published through the outbox, and triage is either a suggestion or manual.
- A second runtime (Python) adds an image, a lock file and a CI job; the team's Java premise does not cover it (EN01-U1).
- The Python messaging module is a small counterpart of the Java starter ([ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)); it must follow the same CloudEvents mapping and queue declarations.
- Replacing the provider changes one adapter and its configuration, not the contract.
- Open (EN01-U5): provider, model, tier and budget; the free-tier limits are not recorded in the register.

## Verification and review

Tests to write, none exists yet (spike item 7 covers a pika consumer in the Flask image):

- AI provider stopped or unreachable → `TriageSuggested` with `origin = fallback` and the rules result.
- Provider timeout (stub that sleeps beyond 10 s) → second attempt, then fallback.
- Malformed or out-of-vocabulary provider output → fallback.
- AI disabled by configuration → `origin = rules`, reporting unaffected.
- Duplicate `TriageRequested` → equivalent result; Issue applies once by `issueVersion`.
- Late result after a human triage decision → ignored by Issue ([design §3.3](../07-technical-design.md#33-invalid-and-concurrent-transitions)).
- Poison message (unsupported `schemaversion`) → DLQ without retry; no payload in logs.
- Injection text from the [adversarial set](../06-responsible-ai-assessment.md#3-proposed-dataset-and-protocol) → no action outside the output schema.

Review when AI-01 chooses a provider, after the evaluation, and if the 2-attempt/10 s values prove wrong in the spike.

## Record

2026-10-27 — proposed by Ricardo (Tech Lead) after a structured design interview; drafting and source checks AI-assisted (new ADR; the 2026-10-15 proposal had a Bun triage worker claiming jobs over HTTP, with a job table and `SKIP LOCKED` claiming). Reason: RabbitMQ replaces the job table and claim endpoints; the AI part becomes its own Flask service with a facade and provider adapters. Evidence: [evidence register](README.md#evidence-register-en-01-01) E01, E03, E20–E25, E62, E63. Affected documents: [technical design §1, §4.4, §4.6, §5](../07-technical-design.md#5-asynchronous-workflow-and-consistency), [responsible AI assessment](../06-responsible-ai-assessment.md), DEC-05. Final decision, date and participants: pending team review. Issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15).

2026-10-27 — fixed health path removed; liveness and readiness endpoint names per DEVOPS-02 (#42), checks in [ADR-012](ADR-012-health-and-status-page.md).
