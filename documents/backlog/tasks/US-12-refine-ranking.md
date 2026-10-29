# [US-12] Refine ranking

## Planning

- Epic: [EP-03 — Intervention and closure](../epics/EP-03-intervention-and-closure.md).
- Priority: Should; include only with useful, available data and sprint capacity.
- Sprint: S3 candidate.
- Dependencies: [US-06](US-06-select-a-contractor.md), evidence that additional criteria help selection, and documented data sources.

## Story

As an **administrator**, I want to **compare eligible contractors using additional criteria**, so that **I can make a better-informed selection**.

## Scope

Extend US-06's simple ordering with justified criteria such as price, distance or indicative availability. Explain the ranking and keep the administrator's choice.

This story does not cover automatic assignment, AI ranking, collecting real personal addresses, a marketplace or guaranteed contractor availability. It remains a conditional extension.

## Acceptance criteria

- [ ] Select criteria based on evidence of usefulness and available data. Document each source, unit, update time and limitation; identify synthetic fixtures clearly.
- [ ] Apply US-06's eligibility filters before ranking. An ineligible contractor must not become selectable because of a high score.
- [ ] Document the scoring method, weights and tie-breaker. The same inputs and configuration produce the same order, and the administrator can see the main reasons for it.
- [ ] Show missing or stale data explicitly. Do not treat unknown price as zero, unknown distance as nearby or an availability indication as contractor acceptance or booking confirmation.
- [ ] Reject invalid values or configuration without silently replacing the existing ranking. Use US-06's simple ordering when the extra data cannot support a useful comparison and explain the fallback.
- [ ] Keep selection and approval with the administrator. Ranking alone must not send requests, reserve a slot or bypass US-07/08.
- [ ] Enforce administrator/building permissions in the backend. Use only authorised catalogue and issue context; do not expose resident identities or private addresses to explain a score.
- [ ] Compare the refined order with US-06 on documented synthetic examples, including ties, missing/stale data and conflicting criteria. Record limitations and whether to keep, revise or defer the refinement; deferral does not block the core cycle.

## Verification and risks

Test filtering, scoring, tie-breaking and invalid or unavailable data with fixed examples. Review the explanation and compare the results with US-06's simple order. Check that repeated requests do not change ordering or create intervention effects.

The main risks are misleading scores, invented data quality and assumptions about availability. A better-looking ranking does not by itself demonstrate a better business outcome.

References: RF-06, P6, J2 and NFR-01/02. Assignment: 6.2–6.3; [optional-feature conditions](../../04-product-vision.md#44-conditions-for-optional-features).

## Ready / Done

Before starting, select the extension explicitly and agree data sources/freshness, criteria, weights, units, missing-data handling, fallback and comparison cases. Confirm catalogue ownership and the ranking contract with EN-01.

- [ ] Ready: owner, reviewer, estimate and sprint capacity agreed; [DoR](../../governance/definition-of-ready.md) reviewed by the team. Date/author:
- [ ] Done: acceptance criteria met, changes reviewed, and PR, tests, comparison results and demonstration linked according to the [DoD](../../governance/definition-of-done.md).
