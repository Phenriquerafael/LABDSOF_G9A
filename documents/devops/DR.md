# Disaster recovery and backup

**Issue:** [#42 — DEVOPS-02: Observability and DR](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/42)
**Status:** proposal. **No backup has been created and no restore has been performed.** Every recovery claim below is planned, not demonstrated.

Companion documents: [observability](OBSERVABILITY.md) and [CI/CD strategy](CICD.md) (rollback of application versions).

---

## 1. Scope

In scope: the issue data (reports, triage state, assignments, audit records) stored in the database. Recovery of the application itself is handled by redeploying a previous image tag (see [CI/CD section 7](CICD.md#7-releasing-to-production-by-tag)).

Out of scope: multi-region or multi-site disaster recovery, and any production compliance claim.

The database engine, hosting option and whether schemas are shared are still open in the [technical design](../07-technical-design.md). This document therefore gives a general approach that works for most relational engines and is revised once the choice is made.

---

## 2. Recovery targets (proposal)

| Target | Proposed value | Meaning |
|---|---|---|
| RPO (recovery point) | ≤ 24 h | Up to one day of issue data may be lost in the worst case |
| RTO (recovery time) | ≤ 4 h | Service is restored within four hours of a decision to recover |

These values are starting points for the team to agree. They must be revisited once the hosting option, backup frequency cost and the real size of the data are known (NFR-09).

---

## 3. Backup layers

| Layer | What it protects against | Frequency (proposal) | Notes |
|---|---|---|---|
| Logical dump of the database | Accidental deletion, bad migration, corruption of one table | Daily | Engine-native dump tool, once the engine is chosen |
| Disk or volume snapshot of the database host | Loss of the instance or its disk | Daily, with the logical dump as a second copy | Snapshot tooling depends on the hosting option |
| Migration history and schema version | Restoring to a compatible schema | With each release | Kept in the repository; see migration rules below |
| Audit log export (optional) | Loss of audit records | Daily | Retention is an open decision |

Storage rules (proposal):

- Backups are stored outside the database host, in a location with separate credentials.
- Backups are encrypted at rest. Encryption keys are not stored next to the backups.
- Access to backups is limited to the DevOps owner and one named backup reviewer.
- Retention: keep daily copies for an agreed number of days and a monthly copy for an agreed number of months. Values are open.
- Backups never contain secrets from the application environment. Credentials are restored from the secrets store, not from a dump.

Migration rule: schema migrations must be forward-compatible with the previous application version, so that an application rollback does not require a database rollback.

---

## 4. Integrity checks

Each backup run records:

- Completion status and size.
- A checksum of the dump or snapshot identifier.
- Row counts for the main tables (reports, issues, assignments, audit records) compared with the source at the time of the dump.

A restore is accepted only if the restored copy passes a smoke query on each main table and the row counts match the recorded values, allowing for changes made after the backup point.

---

## 5. Restore runbook (outline)

1. Declare the incident and record the time. Freeze writes to the affected service by taking it to a degraded or maintenance state (see [observability section 6](OBSERVABILITY.md#6-degraded-mode-scenario)).
2. Choose the recovery point: the latest backup that passes its integrity check, and record which one.
3. Provision a new database instance. Do not restore over a damaged instance until the damage is understood.
4. Restore the chosen backup into the new instance. Apply compatible migrations for the deployed version.
5. Run the integrity checks from section 4.
6. Point the application to the new instance using environment configuration. Credentials come from the secrets store.
7. Check `/readyz` and `/status`, then re-enable writes.
8. Record the data gap between the recovery point and the incident, and inform the affected users if issues were lost.
9. Write a short post-incident note with the time taken against the RTO target.

---

## 6. Failure scenarios

| Scenario | Likely impact | First response | Recovery path |
|---|---|---|---|
| Accidental deletion of rows by a user or operator | Lost issues or history | Stop writes to the affected table if needed; identify the time | Restore from logical dump into a scratch instance and copy the missing rows back, or restore fully within RPO |
| Bad migration | Errors or wrong data | Roll back the application image; stop further migrations | Restore from the snapshot taken before the migration |
| Database instance or disk failure | Full outage of persistence | Mark database `down` in `/status`; show explicit error, no false acknowledgement | Provision new instance; restore from snapshot or dump |
| Data corruption detected by checks | Unknown extent | Freeze writes; keep the damaged copy for analysis | Restore the last good backup that passes checks |
| Backup job fails silently | RPO is no longer true | Alert on missing or failed backup (see [observability](OBSERVABILITY.md)) | Fix the job; run a manual backup; record the gap |
| Backup storage credential leak | Backups exposed | Revoke the credential; review access logs | Rotate keys; re-encrypt newer backups; assess personal-data impact |
| Hosting region or provider loss | Full outage | Out of scope for the MVP | Documented as a limitation |

---

## 7. Restore-test plan

Planned, not yet executed.

- **Frequency:** once per sprint during the project, and before each release that changes the schema.
- **Method:** restore the most recent backup into a scratch instance, run the integrity checks, start the application against it and run the smoke journey (report an issue, view it).
- **Pass criteria:** restore completes within the RTO target; row counts and smoke queries match; the application starts with `/readyz` returning `ok`.
- **Evidence to keep:** date, backup identifier, restore duration, row counts, pass or fail, and the person who ran it. No personal data in the evidence; use counts and identifiers only.
- **Failure:** a failed test is recorded as an issue and fixed before the next release.

---

## 8. Limitations and open decisions

- No backup or restore exists yet. The RPO and RTO values are proposals.
- Database engine, hosting option, snapshot tooling and backup cost are undecided. Provider pricing and free-tier claims are not stated here and must be verified against vendor pages with access dates before a decision.
- Retention periods for backups and audit records are open.
- Multi-region recovery is out of scope.
- The restore runbook has not been tested against a real environment.
