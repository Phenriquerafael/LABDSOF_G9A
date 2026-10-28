# [US-15] Evaluate AI triage against the non-AI baseline

## Planning

- Epic: [EP-02 — Assisted triage and reviewed links](../epics/EP-02-assisted-triage.md).
- Priority: Must.
- Sprint: prepare the data in S2 and complete the evaluation in S3.
- Dependencies: [US-03](US-03-classify-with-ai.md) and [US-14](US-14-continue-triage-without-ai.md) for the final comparison. Data preparation can start earlier.

## Story

As a **product owner**, I want to **compare AI triage with the rules-based baseline**, so that **I can decide whether AI adds value to the product**.

## Scope

Prepare synthetic cases and compare rules alone, AI alone and the full workflow with human review. Write a report on quality, response time, cost and limitations. EN-04 will use this report.

This story does not cover model training, US-03/14 implementation, real participant data or the other EN-04 evaluations.

## Acceptance criteria

- [ ] Prepare a versioned dataset with synthetic reports, expected answers and cases that require human review. Document how the cases were created, the authors/tools used, the labels and the number of cases in each category.
- [ ] Include ordinary reports, incomplete descriptions, spelling errors, negation, critical and non-critical cases, prompt injection and attempts to access another building's data. Two team members review the critical-case labels and record how disagreements were resolved.
- [ ] Keep development cases separate from the final test cases, including closely reworded examples. Agree and record the dataset version, test method and acceptance targets before the final run. Explain any later changes and repeat affected checks.
- [ ] Run the baseline, AI and full workflow on the same cases. Report accuracy, precision, recall and F1 by class, a confusion matrix and critical false positives/negatives. Include failed cases in the totals and distinguish model suggestions, validated outputs and human corrections.
- [ ] Measure response times (p50/p95), timeouts, failures, calls, tokens, retries and cost per run/report. Record the price date and configuration, and keep runs within the agreed budget.
- [ ] Test unavailable AI and invalid output. Reporting and manual triage must still work through US-14. AI results must not remove critical alerts or overwrite newer human decisions.
- [ ] Check that injected instructions and unauthorised requests cannot expose another building's data or approve actions such as expenses or bookings. Use synthetic data and remove sensitive content from saved outputs and logs.
- [ ] If administrative effort is measured, follow the controlled-task method in the [vision](../../04-product-vision.md#51-primary-success-criterion-dec-08). Record completion, errors and corrections. Times invented for interview simulations cannot be used as a measured baseline.
- [ ] If US-05 is selected, add a versioned set of duplicate/non-duplicate pairs, including similar reports about different problems. Report precision, recall and the impact of wrong links, and check that links need human approval and can be undone. Otherwise, record this part as not selected.
- [ ] Produce a report with the dataset, model, prompt and rule versions, environment, run instructions, results, error examples and limitations. Compare results with the agreed targets and recommend keeping or revising the AI feature. Link the report from the [AI assessment](../../06-responsible-ai-assessment.md) and EN-04 without repeating the same evaluation work.

## Verification and risks

Another team member checks the test cases, calculations, failures and costs. Keep the configuration and results so the evaluation can be repeated.

Avoid using the final test cases to tune the system, changing targets after seeing results or leaving failed calls out of the totals. Synthetic tests do not prove real-world savings or adoption.

## Ready / Done

Before starting, agree the example inputs and expected answers, baseline, model/prompt versions, targets, budget and access.

- [ ] Ready: owner, reviewer, estimate and sprint capacity agreed; [DoR](../../governance/definition-of-ready.md) reviewed by the team. Date/author:
- [ ] Done: acceptance criteria met, report reviewed, and PR, results and demonstration linked according to the [DoD](../../governance/definition-of-done.md).
