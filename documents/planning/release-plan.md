# Product roadmap

**Updated:** 2026-11-01 · DISC-03-04 / [#19](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/19).

This roadmap brings together the project's achievements, planned releases and their contents. Priorities follow the [MoSCoW evaluation](../05-product-backlog.md#1-moscow-evaluation). Completed work below concerns discovery, planning and design; MVP and MVI are planned software deliveries.

## Project history and main achievements

Dates refer to recorded decisions or merged documentation, not software deployment. PR evidence checked on 2026-11-01.

| Date | Achievement | Evidence |
|---|---|---|
| 10 October 2026 | Established the Sprint 1 discovery/design boundary: the team excluded the optional walking skeleton and retained implementation foundations for later delivery. | [DEC-11](decisions-and-feedback.md#confirmed-sprint-1-scope-decision--dec-11), recorded team decision |
| 22 October 2026 | Documented research data handling and a collection of eight explicitly simulated interview records. | [PR #35](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/35), [PR #37](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/37); simulations are not real-user validation |
| 25–26 October 2026 | Documented end-to-end business workflows, synthesised research findings, and consolidated the domain model and API/event contract outlines. | [PR #41](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/41), [PR #39](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/39), [PR #44](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/44) |
| 29 October 2026 | Linked local backlog records to published GitHub issues, improving work-item traceability. | [PR #47](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/47) |
| 1 November 2026 | Prepared 15 detailed stories covering reporting, AI/fallback, intervention, closure and evaluation, with initial estimates and acceptance criteria. | PLAN-01/02/03: [PR #46](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/46), [PR #50](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/50), [PR #51](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/51) |
| 1 November 2026 | Consolidated the proposed stack, ADRs and physical views, together with CI/CD, observability and backup/recovery documentation. | [PR #45](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/45), [PR #40](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/40), [PR #54](https://github.com/Phenriquerafael/LABDSOF_G9A/pull/54); design evidence, not deployed infrastructure |

## Current release plan

**Evidence-supported** identifies assignment or documented journey requirements. **Team decision** identifies product-scope choices; it does not record a meeting or vote.

| Delivery | Target | Contents | Expected outcome and basis |
|---|---|---|---|
| **MVP — Sprint B** | **6 December 2026** | US-01/02: reporting and manual triage; US-03/14: AI and fallback; US-04: shared summaries and impact confirmation; US-06–09: contractor selection, approval/response, booking and closure; US-10: notifications. EN-02/03: foundations, access controls, persistence, tests, CI/CD and initial observability. Start US-15 data preparation. | Operational report-to-closure journey. Evidence-supported: assignment §7.2 and J1–J3. Team decision: retain proactive notifications. |
| **MVI — Sprint C** | **3 January 2027** | Complete US-15 AI evaluation; EN-04 product/quality evaluation; EN-03 hardening and improvements from feedback. Include usability/accessibility, security/performance evidence, resilience, dashboard and final demonstration. | Evaluated and refined MVP. Evidence-supported: assignment §7.3. |
| **Optional backlog** | No fixed delivery date | US-05: duplicate suggestions; US-11: basic costs; US-12: richer ranking (Should); US-13: real calendar (Could). | Team decision: select after core delivery and evaluation fit capacity. These may enter Sprint C without displacing its required outcomes. |
| **Outside this release** | Not scheduled | Payments, marketplace, photographs, native apps, IoT/prediction and the other [Won't exclusions](../05-product-backlog.md#5-wont-in-this-baseline--alternatives). | Team decision: preserve the coordination MVP boundary. |

Milestone descriptions and dates were checked on 2026-11-01: [Sprint B](https://github.com/Phenriquerafael/LABDSOF_G9A/milestone/2) is “Minimal Viable Product”; [Sprint C](https://github.com/Phenriquerafael/LABDSOF_G9A/milestone/3) is “Minimal Viable Incrementation”. Release contents above are planned scope, not completed functionality. Actual software releases are identified by a tag and release notes with included stories, verification and limitations.

## Delivery sequence and estimates

1. Deliver EN-02 foundations and US-01/02: persistent reporting and authorised manual triage.
2. Build US-14 → US-03 and US-06 → US-07 → US-08 → US-09 alongside each other where dependencies allow. Integrate US-04/10 during the MVP; EN-03 quality work accompanies each increment.
3. Prepare US-15's dataset/protocol during the MVP; complete its comparison and EN-04 evaluation in MVI. Select optional extensions after required outcomes.

Existing estimates total **68 SP for the MVP core**, **8 SP for US-15 across both deliveries**, and **24 SP for optional stories**. Shared engineering, additional hardening/evaluation and carry-over are estimated separately. Count US-15 once and reuse its report in EN-04; these totals do not establish sprint capacity.

Sources: [assignment §§7.2–7.3](../../LABDSOF-26-27-Assignment.md), [product vision](../04-product-vision.md) and [story estimates](../05-product-backlog.md).
