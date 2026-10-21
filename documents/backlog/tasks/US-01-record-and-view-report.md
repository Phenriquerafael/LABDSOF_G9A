# [US-01] Record and view a report

## Identification

- Local ID / epic: US-01 / [EP-01 — Reporting and tracking](../epics/EP-01-reporting-and-tracking.md) (direct child).
- Requirement(s), hypothesis/finding and journey: RF-01; P1/P5; J1; NFR-01/02/03/04/05/07/09; [requirements](../../requirements.md), [vision](../../04-product-vision.md), [assignment](../../../LABDSOF-26-27-Assignment.md).
- Proposed MoSCoW priority / reason: Must — establishes the persistent reporting journey required by the MVP.
- Official milestone: proposed S2 initial delivery and S3 refinement/evaluation; No Sprint 1 implementation commitment.
- Blocking decisions/dependencies: DEC-04 and DEC-07 in the [decision register](../../planning/decisions-and-feedback.md). Close applicable EN-01 refinements before implementation readiness.

[EN-01 design](EN-01-technical-design.md) and EN-02 implementation foundations (see the [product backlog](../../06-product-backlog.md#3-discovery-and-engineering)). The minimal report/query path can form part of EN-02; count its implementation once. AI classification is not a prerequisite.

The [technical design](../../08-technical-design.md) and [access matrix](../../09-security-privacy.md#2-proposed-access-matrix) are conceptual inputs, not accepted stack/contracts. These criteria describe behaviour without selecting a framework, database, broker or provider.

Draft status: Backlog; technical refinement required before Ready. No GitHub story URL recorded. Sandro Dias under [PLAN-01](PLAN-01-prepare-reporting-and-tracking-stories.md). Implementation allocation: see the [backlog index](../README.md#ep-01-story-drafts-and-planning-allocation).

## Story

As a **resident**, I want to **report a fault in my building and retrieve its receipt**, so that **management can track the issue and I know it was received**.

## Scope

Included: Text report, authorised building/area selection, immediate receipt, own-report retrieval and persistence. Include server-side access checks and safe handling of a retried submission.

Excluded: AI inference, duplicate matching/merging, photographs, shared publication (US-04), notification delivery (US-10), intervention actions and unrestricted access to another resident's private text.

## Acceptance criteria

- [ ] **Receipt:** Given a resident who belongs to the selected building and valid text/area, when they submit, then one report/issue is persisted and an ID with a “received” status is returned without waiting for AI.
- [ ] **Own-report retrieval:** Given the author and the returned ID, when they query the report after a backend restart, then the saved report and authorised status are available.
- [ ] **Invalid input:** Given blank or invalid text, an invalid area or an area belonging to another building, when submitted, then a clear validation error is returned and no partial report is created. Final field limits belong to R02.
- [ ] **Denied access:** Given an unauthenticated caller or a user without the required building/resource permission, when they submit, list, query or modify a report through the API, then access is denied without exposing private data. Same-building membership alone does not grant access to another resident's raw text.
- [ ] **Retry:** Given a successful submission whose response was lost, when the same operation is retried with the same idempotency identity, including concurrent retries, then one logical report exists and the caller can obtain its original receipt. Reusing that identity with different content must not silently replace the original report; refine the exact conflict contract under R02.
- [ ] **Unavailable dependency:** Given AI is disabled or unavailable, then valid reporting and own-report retrieval still work. If persistence itself fails, show a failure/retry outcome and do not claim the report was received unless it was durably saved.
- [ ] **Usable and private interface:** The form supports keyboard use, labels and understandable errors. Render submitted text safely and keep private text/identities out of logs and unrelated views.

## Verification and risks

Use synthetic residents in buildings A/B, an administrator and a contractor. Verify successful submission/query after restart, invalid fields/area, direct API denial for other users/buildings, duplicate concurrent retries, persistence failure and AI disabled. Include a form→receipt→query end-to-end path and keyboard/error checks. Capture environment, IDs/counts and sanitised logs; use the agreed NFR-05 scenario after thresholds are frozen.

Principal risks: A successful-looking receipt without persistence, cross-building leakage, duplicate reports from network retries and confusing server denial with client-only button hiding.

This is a story draft: these are planned implementation checks, not executed tests. PLAN-01 validates document content, traceability, consistency and links only.

## Ready / Done

Technical refinement: R01 — stack/component boundaries; R02 — report/API/data/idempotency contract; R03 — identity/access; R06 — environment and evidence.

Close the applicable rows of the [EP-01 refinement register](../ep01-technical-refinement.md) using EN-01 decision/contract evidence; record any justified non-applicability. Do not invent concrete endpoints, queue names, database schemas or retry thresholds before those decisions.

- Implementation owner / independent reviewer / estimate / capacity / sprint:
- Refinement closure references and remaining limitations:
- [ ] DoR reviewed by the team; date/author:
- [ ] DoD verified with links to PR, tests and demonstration:

See [definition-of-ready.md](../../governance/definition-of-ready.md) and [definition-of-done.md](../../governance/definition-of-done.md). Do not mark Ready without estimates/capacity, agreed owner/reviewer and resolved dependencies. Record actual implementation/test/demo evidence before checking Done.
