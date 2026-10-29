# Observability and degraded operation

**Issue:** [#42 — DEVOPS-02: Observability and DR](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/42)
**Status:** proposal. Nothing in this document is deployed, configured or demonstrated yet. Every statement about running services is a plan.

Companion documents: [CI/CD strategy](CICD.md) and [disaster recovery](DR.md).

---

## 1. Requirements coverage

| Assignment item | Where it is answered | Status |
|---|---|---|
| §6.6 Audit records | [section 7](#7-audit-events) | Proposed format; authentication may be mocked for the MVP |
| §6.7 Structured application logs | [section 3](#3-application-contract) | Proposed |
| §6.7 Health checks | [section 3.2](#32-health-endpoints) | Proposed |
| §6.7 Relevant metrics | [section 3.3](#33-metrics) | Proposed |
| §6.7 Correlation or trace identifiers | [section 3.1](#31-logs-and-correlation) | Proposed |
| §6.7 Error reporting | [section 5](#5-error-reporting) | Option not chosen |
| §6.7 Small operational dashboard | [section 4](#4-service-level-indicators-and-dashboard) | Proposed |
| §6.7 Service-level indicators | [section 4](#4-service-level-indicators-and-dashboard) | Example targets, to agree |
| §6.8 Degraded-mode scenario | [section 6](#6-degraded-mode-scenario) | One scenario proposed; others listed |

---

## 2. Architecture view

The components follow the [technical design](../07-technical-design.md): Issue, Dispatch, workers, broker, database and simulator. The stack, broker and database are still undecided, so the names below are placeholders.

```text
Services (Issue, Dispatch, workers)
   │  JSON logs (stdout)            /metrics            /healthz /readyz /status
   ▼                                   ▼                         ▼
Log collector (optional)          Prometheus  ──────►  Grafana dashboard
   │                                   │
   ▼                                   ▼
Log store (optional, e.g. Loki)   Alert rules  ──►  notification channel (to choose)

Errors ──► error-reporting tool (open decision, section 5)
```

Diagram status: textual sketch only. No rendered diagram is committed for this document.

---

## 3. Application contract

Every service follows the same contract so that the dashboard and runbooks work across components.

### 3.1 Logs and correlation

- One JSON object per line on stdout. No log file inside the container.
- Required fields: `timestamp` (UTC, ISO 8601), `level`, `service`, `message`, `request_id`, `event`.
- Optional fields: `issue_id`, `building_id`, `error.kind`, `duration_ms`, `dependency`.
- `request_id` comes from the incoming `X-Request-ID` header. If the header is missing, the service generates one. It is returned in the response and passed to every downstream call and event.
- Logs must not contain passwords, tokens, full personal data or free-text report content beyond what the operator needs (NFR-02). Identifiers are preferred to names.

### 3.2 Health endpoints

| Endpoint | Meaning | Checks |
|---|---|---|
| `GET /healthz` | The process is running (liveness) | None beyond the process itself |
| `GET /readyz` | The service can accept traffic (readiness) | Database reachable; broker reachable where the service needs it |
| `GET /status` | Human-readable state for the operator | Each dependency with `ok`, `degraded` or `down`, and the last check time |

`/readyz` returns `503` when a required dependency is down. `/status` returns `200` with degraded entries, so operators can see partial failure without the orchestrator restarting the service.

### 3.3 Metrics

Prefix: `bmc_`. Labels stay low-cardinality (no issue IDs as labels).

| Metric | Type | Purpose |
|---|---|---|
| `bmc_http_requests_total{route,status}` | counter | Traffic and errors per route |
| `bmc_http_request_duration_seconds{route}` | histogram | Latency; basis for the p95 SLI |
| `bmc_dependency_up{dependency}` | gauge | 1 when the dependency check passes |
| `bmc_outbox_pending` | gauge | Events persisted but not yet published (NFR-04) |
| `bmc_outbox_oldest_age_seconds` | gauge | Age of the oldest pending event |
| `bmc_ai_requests_total{result}` | counter | AI calls by `ok`, `timeout`, `error`, `skipped` (NFR-03) |

---

## 4. Service-level indicators and dashboard

Example SLIs and targets. They are starting points for the team to agree, not measured values.

| SLI | Measured as | Example target (proposal) |
|---|---|---|
| Availability of reporting | Share of successful `GET`/`POST` responses on reporting routes | ≥ 99% per month, excluding planned maintenance |
| Latency of viewing and reporting | p95 `bmc_http_request_duration_seconds` | ≤ 2 s, matching NFR-05 |
| Notification freshness | `bmc_outbox_oldest_age_seconds` | Below an agreed number of minutes |
| AI availability | `bmc_ai_requests_total` with `result="ok"` over all attempts | Informational; reporting must work with AI disabled (NFR-03) |

Dashboard panels (one page): service health and `/status` summary; request rate, error rate and p95 latency; dependency up/down; outbox backlog; AI result breakdown; recent error count from logs.

Alerts (proposal): a dependency down for more than an agreed period; error rate above an agreed threshold; outbox backlog growing for an agreed period. Notification channel is not chosen.

---

## 5. Error reporting

Open decision. Options under consideration:

- **Hosted error tracker** (for example Sentry, free tier). Pricing and limits must be checked on the vendor's page before adoption; this document does not state them.
- **Log-based only.** Errors are logged with `level=error` and `error.kind`; the dashboard counts them. No extra service.

Recommendation for discussion: start log-based, since it adds no external processor of personal data. Revisit when a hosted tracker's data-processing terms have been reviewed.

---

## 6. Degraded-mode scenario

Each team must demonstrate at least one degraded mode (§6.8). Proposed scenario: **the AI service is unavailable.** The product already requires this (NFR-03, and the [technical design](../07-technical-design.md)).

| Element | Definition |
|---|---|
| Dependency | AI triage service |
| Detection | Call timeout (proposed 10 s per attempt) or error; `bmc_ai_requests_total{result="timeout"}` rises; `/status` shows `degraded` |
| Behaviour | Reporting continues. The issue is stored with a pending-triage state. Rules-based suggestion or manual triage is offered. No retry storm: bounded attempts, then pending |
| User message | Visible notice that automatic triage is unavailable and the report is saved for manual review |
| Recovery | When `/status` returns `ok`, pending issues are re-queued for triage. Manual corrections are never overwritten |
| Evidence to produce | Demo script that disables the AI dependency, submits a report, shows the pending state, restores the dependency and shows the queue draining. Log lines and a dashboard screenshot |

Other scenarios to define later, with the same table: external data provider, network connection, database, notification provider, backend component. The team picks which ones it will demonstrate; the assignment requires at least one.

---

## 7. Audit events

Proposed event format for access-related and state-changing actions (§6.6):

```json
{
  "event": "issue.status_changed",
  "occurred_at": "2026-11-01T10:15:00Z",
  "actor_id": "usr_123",
  "actor_role": "administrator",
  "action": "status_change",
  "resource": "issue/iss_456",
  "outcome": "allowed",
  "request_id": "req_789"
}
```

Rules: record denied attempts as well as allowed ones; never include report free text or personal contact data; keep audit events separate from debug logs; retention is an open decision (see [DR](DR.md) for backup of audit data).

---

## 8. Resources and security

- Dashboards and `/metrics` are internal. They are not exposed on the public listener, and `/status` shows no secrets.
- Credentials for the monitoring stack follow the rules in [CI/CD section 9](CICD.md#9-secrets-and-variables).
- Monitoring containers run with the same non-root and read-only rules as the application images, once the golden-image approach is adopted.

---

## 9. Limitations and open decisions

- No example configuration has been run. Metric and endpoint names are design proposals.
- Prometheus, Grafana and a log store are proposals from the issue. The hosting target is undecided, so resource sizing is not known.
- The degraded-mode scenario and the alert thresholds have not been tested.
- Error-reporting tool and its free-tier terms are unverified.
- Whether Loki is included is open.
