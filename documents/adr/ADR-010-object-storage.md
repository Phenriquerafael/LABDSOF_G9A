# ADR-010 — S3-compatible object storage for attachments and backups

**Status:** Proposed
**Date:** 2026-10-27
**Participants:** Ricardo (P2, Tech Lead) — proposer; Martim (P5, DevOps/QA/security) to confirm; team review pending
**Related decision:** DEC-04; DEC-07 (photos are personal data); DEC-06 baseline unaffected
**Supersedes / superseded by:** —

## Context

Report photos were classed as post-MVP in the 2026-10-07 editorial harmonisation. This ADR proposes a scope addition, not a settled one: a new **Should** story, US-14 “Attach photos to a report”, which needs a DEC entry and backlog work (EN01-U11) before it exists. Must stories do not depend on it.

A second need is independent of photos: DEVOPS-02 needs an off-host target for database backups, so that losing the host does not lose the data (T-09, [security](../09-security-privacy.md#3-threats-and-checks)). Backups are exercised in the runbook ([ADR-004](ADR-004-deployment-contract.md)).

§6.4 asks to avoid multiple database technologies unless justified (E01). Object storage is proposed as a justified exception: it is a blob store for opaque files, not a second database technology; all structured data stays in MySQL ([ADR-002](ADR-002-technology-stack.md)).

## Alternatives

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Garage 2.5, single node** | S3 API on port 3900; presigned URLs, multipart and CORS implemented; about 1 GB RAM; started with one command and default credentials from the environment | AGPL-3.0 (run unmodified, as a separate service); single node “provides no redundancy”; no object versioning | E46 |
| B. SeaweedFS | Apache-2.0; presigned URLs, multipart, CORS and versioning supported; 4.51 current | Larger system; recorded as the fallback if Garage fails the spike | E47 |
| C. RustFS | Apache-2.0; multi-arch images | First 1.0 line in October 2026; features labelled Available or Preview; rejected as too young | E48 |
| D. MinIO | Well known | Repository archived, “no longer maintained”, community edition distributed as source only; rejected | E45 |
| E. Cloudflare R2 | Free tier per month: 10 GB-month storage, 1 million Class A and 10 million Class B operations, no egress charge | Hosted third party: an account, and data leaves the host (DEC-07); no bucket versioning; partial checksum support. Kept as an **optional hosted target** of the same adapter, not as an alternative | E49 |
| F. BLOBs in MySQL | Nothing new to run | Larger backups; memory pressure on the shared MySQL instance; no path to direct upload | — |

Garage is chosen on the facts recorded above (maintained, S3 subset sufficient, small footprint per its own documentation), not on a measured comparison; no benchmark was run. Its AGPL-3.0 licence matters only if the team modified or redistributed it; none is planned.

## Proposed decision

**A**, proposed, not accepted. Garage 2.5 single node (`dxflrs/garage:v2.5.0`, E46) in dev, on the college servers and in the demo; R2 (E49) optional as a hosted target; SeaweedFS (B) is the recorded fallback.

**Portable subset.** Only operations common to Garage and R2: Put, Get, Delete, Head, presigned GET/PUT, optional multipart. No versioning, bucket policies or object lock.

**Adapter.** An `ObjectStoragePort` in `application` ([ADR-009](ADR-009-service-internal-architecture.md)) with an S3 adapter on the AWS SDK for Java v2 (E51). Configuration: endpoint override, path-style access, configurable region (`auto` for R2), `requestChecksumCalculation` and `responseChecksumValidation` = `WHEN_REQUIRED` because the SDK default since December 2024 sends CRC checksums, which broke third-party S3 providers in another SDK (E50, community source), and `chunkedEncodingEnabled(false)` for R2 (E49). Credentials come from the environment, one key per service and bucket; no secret in Git.

**Uses.**

| Use | Bucket | Rules |
|---|---|---|
| (a) Report photos | `bmc-attachments` | Before upload the client re-encodes each photo to JPEG, long edge about 2048 px, which also converts iPhone HEIC that Chrome and Android cannot decode ([ADR-011](ADR-011-installable-pwa-client.md); E68, E69). Server checks are unchanged and do not trust the client: through Issue: `POST /reports/{id}/attachments` (multipart), at most 5 photos × 5 MB, JPEG/PNG/WebP verified by content and not by the declared type, EXIF and GPS data stripped before storage, random object key, `Attachment` metadata row in the `issue` database |
| (a) Download | same | `GET /attachments/{id}` through Issue, authorised by the access matrix: same visibility as the private report text (author and administrators of the building). Not in the contractor extract unless an administrator shares it; sharing is open and post-MVP. Unauthorised access answers `404` |
| (c) Backups | `bmc-backups` | Scheduled MySQL dumps written by the backup job to the bucket (and optionally to R2); DEVOPS-02 owns schedule, rotation and restore exercise |

Client re-encoding is a convenience (smaller uploads, one format), not a control; a request that bypasses the client still meets the server checks. Its exact values are tuned in spike item 13 on a real iPhone and Android device. Contractor completion photos are a later topic. The storage endpoint is never routed by Traefik and is reachable only on the internal network. Presigned direct upload from the browser is recorded as the scaling path if proxying through Issue becomes a bottleneck; it would need CORS and a revised access check.

## Consequences

- Single-node Garage has no redundancy (E46). A disk failure loses attachments, and backups of the database depend on the same node unless they are copied elsewhere (R2 or another host). The bucket itself needs a backup or an off-host copy; this is Martim's runbook item (DEVOPS-02).
- AGPL-3.0: run the upstream image unmodified as a separate service; do not embed or patch it.
- Privacy (DEC-07): photos can show people and the inside of dwellings. EXIF/GPS stripping, random keys, the access matrix and synthetic data only in dev/demo reduce exposure; they do not make photos non-personal. Retention and deletion rules are open under DEC-07. R2 as a hosted target sends the data to a third party and needs a decision before real data.
- One more container (~1 GB RAM per E46, to be measured in the spike) in an already heavy stack ([ADR-004](ADR-004-deployment-contract.md)).
- If storage is down, reporting must not fail (below); the status page and banner show Photo upload as Unavailable ([ADR-012](ADR-012-health-and-status-page.md)).

## Verification and review

Spike item 9: the same adapter against Garage and R2, including checksum and path-style settings. Spike item 13: the client photo pipeline (HEIC to JPEG, resulting size) on a real iPhone and Android device. Tests to write (none exists yet):

- Oversized (> 5 MB) or sixth photo → rejected with a problem response.
- Wrong content (for example an executable renamed `.jpg`) → rejected.
- A stored photo has no EXIF/GPS data.
- Unauthorised user (another building, or a contractor not given access) → `404`.
- Storage stopped → the report is saved without the photo and the user sees a clear message that the photo was not stored; this is a §6.8 degraded-mode scenario (E01).
- Backup written to `bmc-backups` and restored in the restore exercise.

Review if Garage fails the spike, if photos become Must, or if the demonstration host cannot run it.

## Record

2026-10-27 — proposed by Ricardo (Tech Lead) after a structured design interview; drafting and source checks AI-assisted (new ADR). Reason: a Should-priority photo attachment story and an off-host backup target need storage that is not MySQL; MinIO is archived. Evidence: [evidence register](README.md#evidence-register-en-01-01) E01, E45–E51. Affected documents: [security §2, §4](../09-security-privacy.md#4-data-lifecycle-and-minimisation), backlog (US-14, to be created), DEVOPS-02. Final decision, date and participants: pending team review. Issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15).

2026-10-27 — client-side JPEG re-encoding before upload added (incl. HEIC; [ADR-011](ADR-011-installable-pwa-client.md), E68, E69); server checks unchanged.
