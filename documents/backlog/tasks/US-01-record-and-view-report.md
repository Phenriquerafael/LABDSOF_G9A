# [US-01] Record and view a report

## Planning

- Epic: [EP-01 — Reporting and tracking](../epics/EP-01-reporting-and-tracking.md).
- Priority: Must.
- Estimate: 5 story points — report form/API, persistence, building permissions, safe retries and tests.
- Sprint: implement in S2 and refine/evaluate in S3.
- Dependencies: [EN-01](EN-01-technical-design.md) for design and access rules, and EN-02 in the [product backlog](../../06-product-backlog.md#3-discovery-and-engineering) for implementation foundations. Count a shared report/query implementation once. AI is not a prerequisite.

## Story

As a **resident**, I want to **report a fault in my building and view its receipt**, so that **I know management has received it**.

## Scope

Submit a text report, select an authorised building/area, receive an ID and view the saved report and status. Handle retried submissions safely.

This story does not cover AI, duplicate matching, photographs, shared publication, notification delivery or intervention actions.

## Acceptance criteria

- [ ] Save a valid report from a resident of the selected building and return its ID and “received” status without waiting for AI.
- [ ] Let the author retrieve the saved report and authorised status using its ID, including after a backend restart.
- [ ] Reject blank or invalid text, invalid areas and areas from another building with a clear error. Do not create a partial report.
- [ ] Check permissions in the backend for submission, listing, reading and modification. Unauthenticated or unauthorised users cannot access private data; belonging to the same building does not allow someone to read another resident's raw text.
- [ ] If the response is lost, repeating the submission with the same idempotency key must return the original receipt without creating another report, including concurrent retries. Reject reuse of the key with different content without changing the original.
- [ ] Keep reporting and retrieval available when AI is disabled or unavailable. If storage fails, show a failure/retry message and do not claim the report was received unless it was durably saved.
- [ ] Support keyboard use, labels and understandable validation errors. Display submitted text safely and keep private text and identities out of logs and unrelated views.

## Verification and risks

Use synthetic residents from two buildings, an administrator and a contractor. Test submission, retrieval after restart, invalid fields, denied API access, concurrent retries, storage failure and unavailable AI. Include the form-to-receipt journey, keyboard checks and the agreed NFR-05 performance scenario.

The main risks are false receipts, duplicate reports and private data reaching other users. Keep the environment, record counts and sanitised logs as evidence.

References: RF-01, P1/P5, J1 and NFR-01/02/03/04/05/07/09 in the [requirements](../../requirements.md).

## Ready / Done

Before starting, agree the report fields/limits, building/area rules, API responses, storage ownership, idempotency scope/lifetime and conflict behaviour, identity/access rules and test environment. Confirm DEC-04/07 through EN-01 and the [technical design](../../08-technical-design.md).

- [ ] Ready: estimate recorded, blocking decisions resolved and [DoR](../../governance/definition-of-ready.md) reviewed by the team.
- [ ] Done: acceptance criteria met, changes reviewed, PR and tests.
