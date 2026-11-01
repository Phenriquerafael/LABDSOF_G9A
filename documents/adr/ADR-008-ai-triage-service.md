# ADR-008 — AI triage service in Flask

**Status:** Proposed
**Date:** 2026-11-01
**Participants:** Ricardo (P2, Tech Lead) — proposer; Sandro (P4, AI) to confirm; team review pending
**Related decision:** DEC-05 (provider and evaluation stay open there), DEC-04, DEC-07
**Supersedes / superseded by:** — (new ADR; replaces the triage worker of the 2026-10-15 proposal, see Context and Record)

## Context

§6.3 asks for at least one meaningful asynchronous workflow; classifying a report and enriching it with AI is one of the examples (E01). NFR-03 requires that reporting works with AI disabled, with a 10 s timeout per attempt, a visible fallback or pending state and manual correction ([requirements](../requirements.md#non-functional-requirements--constraints)). The [responsible AI assessment](../06-responsible-ai-assessment.md) defines the baseline (versioned rules), the fallback and the controls.

AI-01 and DEC-05 own the provider, model, vocabulary, prompt, dataset and evaluation. This ADR decides only the **shape of the service**: how it runs, how it communicates, how a provider is plugged in, and what happens on failure. No accepted provider decision or measured result is claimed. The story refinements propose Gemini with an unverified model identifier, `gemini-3.5-flash-lite`, working prompt/schema names `triage-v1` / `triage-output-v1` and a zero-EUR budget cap. Prompt/schema content, model availability and formal DEC-05/AI-01 review remain open.

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

**Deployment.** The AI is one service, `ai-triage`, at the same level as Issue, Dispatch and Notification. It is one image running two processes, the Flask web process and the pika consumer process; whether they run as one container or as two Compose services from the same image is spike item 7. `ai-triage` sits on the `internal` network (RabbitMQ) and on the `egress` network, which is the only way out to the internet and the provider ([ADR-004](ADR-004-deployment-contract.md)). An egress proxy with an allow-list is not adopted for the MVP; it stays open for EN-01-04.

**Messages** (contract in [ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md) and `contracts/proto/`):

| Direction | Event | Payload |
|---|---|---|
| In | `TriageRequested` (routing key `issue.TriageRequested`, bound only to `ai-triage.requests`) | `issueId`, `issueVersion`, `buildingId`, `areaKind`, report text needed for classification |
| Out | `TriageSuggested` | `issueId`, `issueVersion`, category, urgency, rationale, `needsReview`, origin (`ai`, `rules` or `fallback`), `modelVersion`, `promptVersion`, `rulesVersion`, `outputSchemaVersion`; `failureCode` for fallback |

**Structure** (instance of [ADR-009](ADR-009-service-internal-architecture.md)). A triage facade, `TriageService.classify(request)`, depends on two ports: `AiProvider` and `RulesBaseline`. Provider adapters (adapter pattern) implement `AiProvider`; Gemini Flash on the free tier is the **candidate** adapter (E63), and the actual provider and model remain DEC-05/AI-01 (Sandro). A disabled-AI configuration uses rules only. The composition root is `create_app()` and a matching consumer factory: plain Python wiring, no DI library.

**Ownership.** Issue owns persisted criticalSignals, criticalRulesVersion=critical-alerts-v1 and criticalCheckStatus. Flask owns the category/urgency RulesBaseline, rulesVersion=rules-v1, used for provider-disabled/fallback results and baseline evaluation. Stopping Flask leaves reporting, manual triage and Issue's independent safeguards available; it does not pretend the classification baseline ran. A failed local critical detector leaves a durable report with a visible pending/manual check. Evaluate both rule systems separately. Provider failure is returned as TriageSuggested origin=fallback, not a new TriageFailed wire contract. Model/prompt versions are null when no provider was called. `outputSchemaVersion` identifies the model-output validation schema used (null if no provider output was validated); it is distinct from the integer event-envelope `schemaVersion`. Its JSON schema, allowed values and fallback-code vocabulary still require AI-01/US-03 review before Ready.

**Behaviour.**

1. Issue independently records critical-alerts-v1 signals when storing the report; this does not wait for the provider, broker or Flask. The Flask facade runs its separate rules-v1 classification baseline first; call the provider with a 10 s timeout per attempt, at most 2 attempts (design §4.6, to calibrate in the spike).
2. Validate the provider output against the schema and the allowed vocabulary. Missing fields, out-of-vocabulary values or malformed output count as a failed attempt.
3. On invalid output or quota exhaustion, fall back immediately; after the permitted transient-failure attempts, publish the rules result with `origin = fallback`; with AI disabled, `origin = rules`. A successful answer has `origin = ai`. An AI result never removes Issue's critical alert. The event carries a suggestion, not authority to change the persisted safeguard.
4. Publish `TriageSuggested` with the versions of model, prompt and rules, persistent and `mandatory`; wait for a positive publisher confirm with no returned message (E84), then acknowledge `TriageRequested`. If the publish fails, is returned or is not confirmed, `TriageRequested` is not acknowledged (nack with requeue), so it is redelivered. The service keeps no state: a redelivered request is classified again and produces an equivalent message for the same `issueVersion`, and Issue applies it idempotently by `issueVersion`.
5. If nothing arrives within 2 min, Issue shows “triage pending — classify manually”; manual triage is always possible ([design §4.6](../07-technical-design.md#46-retry-timeout-and-lease-values-proposal)).

**Metrics** (`/metrics`): fallback rate, provider latency, provider errors by type, requests consumed and published, consumer redeliveries, DLQ depth (from the broker). No request text in metrics or logs.

**Privacy.** `TriageRequested` is the only message that carries private report text. It is point-to-point, never fanned out; messages that reach the DLQ expire after 7 days (`x-message-ttl` on the DLQ only), while retention in `ai-triage.requests` (if the consumer stays stopped) and in Issue's outbox is not specified yet (EN01-U6); payloads are never logged. The text leaves the system for the provider, so DEC-07 and [security §4](../09-security-privacy.md#4-data-lifecycle-and-minimisation) apply: development and demonstration use synthetic data only. For Gemini (E63), unpaid data may be used to improve products unless the EEA/Switzerland/UK paid-service terms apply, and users must be 18+; both points need Sandro's and the team's confirmation before any non-synthetic text is sent.

## Consequences

- AI failure never blocks reporting: the report is stored, the event is published through the outbox, and triage is either a suggestion or manual.
- A second runtime (Python) adds an image, a lock file and a CI job; the team's Java premise does not cover it (EN01-U1).
- The Python messaging module is a small counterpart of the Java starter ([ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)); it must follow the same CloudEvents mapping, `mandatory` publishing with confirms and returns, and the queues declared by the deployment.
- Replacing the provider changes one adapter and its configuration, not the contract.
- The [AI assessment](../06-responsible-ai-assessment.md#1-need-and-workflow) records the working provider proposal and budget. Prompt/schema content, model availability, actual Free-tier access/quotas and decision review remain open under AI-01/US-03 and EN01-U5/DEC-05; no live access is claimed.

## Verification and review

Tests to write, none exists yet (spike item 7 covers a pika consumer in the Flask image):

- AI provider stopped or unreachable → `TriageSuggested` with `origin = fallback` and the rules result.
- Provider timeout (stub that sleeps beyond 10 s) → second attempt, then fallback.
- Malformed or out-of-vocabulary provider output → fallback.
- Flask service stopped → Issue still records critical safeguards, report/query/manual triage work, and no-result processing becomes pending after two minutes.
- Issue critical detector fails → durable report, visible pending/manual check; no false claim of a completed safeguard.
- AI disabled by configuration → `origin = rules`, reporting unaffected.
- Duplicate `TriageRequested` → equivalent result; Issue applies once by `issueVersion`.
- `TriageSuggested` returned, not confirmed, or the consumer killed before the confirm → `TriageRequested` not acknowledged and redelivered; no request lost.
- Late result after a human triage decision → ignored by Issue ([design §3.3](../07-technical-design.md#33-invalid-and-concurrent-transitions)).
- Poison message (unsupported `schemaversion`) → DLQ without retry; no payload in logs.
- Injection text from the [adversarial set](../06-responsible-ai-assessment.md#3-proposed-dataset-and-protocol) → no action outside the output schema.

Review the working provider configuration in DEC-05/AI-01, after the evaluation, and if the 2-attempt/10 s values prove wrong in the spike.

## Record

2026-10-27 — proposed by Ricardo (Tech Lead) after a structured design interview; drafting and source checks AI-assisted (new ADR; the 2026-10-15 proposal had a Bun triage worker claiming jobs over HTTP, with a job table and `SKIP LOCKED` claiming). Reason: RabbitMQ replaces the job table and claim endpoints; the AI part becomes its own Flask service with a facade and provider adapters. Evidence: [evidence register](README.md#evidence-register-en-01-01) E01, E03, E20–E25, E62, E63. Affected documents: [technical design §1, §4.4, §4.6, §5](../07-technical-design.md#5-asynchronous-workflow-and-consistency), [responsible AI assessment](../06-responsible-ai-assessment.md), DEC-05. Final decision, date and participants: pending team review. Issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15).

2026-10-27 — fixed health path removed; liveness and readiness endpoint names per DEVOPS-02 (#42), checks in [ADR-012](ADR-012-health-and-status-page.md).

2026-11-01 — revised by Ricardo (Tech Lead) after Martim's review of PR #45 (2026-10-31) and the Copilot review of 2026-10-31; drafting AI-assisted. Reason: the stateless consumer acknowledged the request without waiting for its reply, so `TriageSuggested` is now published persistent and `mandatory` and the request is acknowledged only after a positive confirm with no return; the AI is one service `ai-triage` (web and consumer processes from one image, container split in spike item 7) on `internal` and the new `egress` network, with an egress allow-list proxy left open for EN-01-04; the 7-day TTL is stated as DLQ-only. Evidence: [evidence register](README.md#evidence-register-en-01-01) E84. Affected documents: [technical design §5](../07-technical-design.md#5-asynchronous-workflow-and-consistency), [ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md), [ADR-004](ADR-004-deployment-contract.md), [security](../09-security-privacy.md). Final decision, date and participants: pending team review.

2026-11-01 — PLAN-01/02/03 review correction, AI-assisted: align the assessment and technical design with the proposed Issue/Flask ownership split; distinguish `outputSchemaVersion` from the event-envelope version and retain missing prompt/schema specifications as open refinements. No team acceptance is recorded.
