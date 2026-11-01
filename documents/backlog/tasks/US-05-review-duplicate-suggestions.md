# [US-05] Review duplicate suggestions

## Planning

- Epic: [EP-02 — Assisted triage and reviewed links](../epics/EP-02-assisted-triage.md).
- Priority: Should.
- Estimate: 8 story points — candidate matching, permissions, reversible links, concurrency and matching tests.
- Sprint: S3 candidate; include in S2 only if selected without displacing the core journey.
- Dependencies: US-01/02 in the [product backlog](../../05-product-backlog.md#4-stories-and-criteria) and the duplicate-matching approach in DEC-05. This feature does not depend on successful AI classification.

## Story

As an **administrator**, I want to **review reports that may refer to the same fault**, so that **I can coordinate the response without losing the original reports**.

## Scope

Suggest possible duplicates within the same building and explain each suggestion. The administrator can confirm or reject a link and undo it later.

The initial estimate assumes simple rules. Optional embeddings need an agreed approach and an estimate review. [US-15](US-15-evaluate-ai-against-baseline.md) will include duplicate evaluation only if this feature is selected.

This story does not cover automatic merging, closing or reprioritising reports, matching across buildings or sending interventions.

## Acceptance criteria

- [ ] Show candidates only from the administrator's buildings and the agreed area/time range. Explain why each report was suggested.
- [ ] Keep candidates as suggestions until the administrator confirms a link. Rules or AI must not merge, close or reprioritise reports, or send an intervention.
- [ ] Save confirmed links with an audit record and preserve both original reports and their history. Undoing a link removes the association, not the reports.
- [ ] Allow rejection of similar reports that describe different problems. Missing information, an unclear match or no candidates must not block reporting or manual triage.
- [ ] Reject unauthorised queries and link changes. Identical text in different buildings must not produce a shared candidate or expose private report text.
- [ ] Repeated confirmations or undo requests must not create duplicate effects. Reject outdated versions when someone else has changed the records.
- [ ] If an optional model fails or returns invalid data, use safe rule-based candidates or show no suggestion. Manual coordination must remain available. Identify the source of a suggestion; a similarity score is not proof of duplication.
- [ ] Before selecting this feature, document the evidence and limitations behind P2 and compare possible matching approaches. Plan positive, negative, similar-but-different and cross-building test pairs with US-15. If deferred, record that decision rather than marking the feature Done.

## Verification and risks

Test duplicate and non-duplicate pairs, missing information and identical reports from different buildings. Check permissions, repeated/stale requests and the confirm/undo flow. Use US-15's evaluation report for precision, recall and examples of wrong links.

The main risks are linking different faults, exposing private text, losing original records and spending time on an optional feature before the core MVP is complete.

References: RF-05, P2, J2 and NFR-01/02/04/10.

## Ready / Done

Before starting, confirm that the feature is selected. Agree the matching method, input/output examples, filters, permissions, version checks and evaluation targets.

- [ ] Ready: estimate recorded, blocking decisions resolved and [DoR](../../governance/definition-of-ready.md) reviewed by the team.
- [ ] Done: acceptance criteria met, changes reviewed, PR and tests.
