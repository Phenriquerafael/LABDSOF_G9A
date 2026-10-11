# Project monitoring

**Status:** collector and chart paths configured; live project access, workflow execution and real measurements remain to be verified.

## 1. Assignment requirements and chosen evidence

The [assignment](../../LABDSOF-26-27-Assignment.md) requires the evidence below. The recording formats are our choices; it does **not** mandate a burndown, burnup or cumulative-flow chart. Optional capacity analysis, blocker-age indicators and retrospective actions are not part of this required evidence list.

| Assignment requirement | Reference | Chosen evidence and location |
|---|---|---|
| Prioritised backlog and acceptance criteria | §7.1.2, §8.2 | [Product backlog](../06-product-backlog.md), linked to board items with priority and acceptance criteria |
| Sprint planning, goals and initial release plan | §7.1.2, §8.2 | Sprint dates, selected items and goal in the [sprint plan](sprint-1-plan.md) / sprint backlog; release milestones in the [roadmap](../05-product-roadmap.md) |
| Assign and track work; monitor progress | §8.2 | Owners and current statuses on the board; sprint goal outcome and a dated progress chart in the sprint review. Section 4 explains the chart choices |
| Record decisions and stakeholder feedback | §8.2 | [Decisions and feedback](decisions-and-feedback.md), with source, date, rationale and affected items |
| Revise at least one product or technical decision following lecturer/investor feedback | §5.7 | Actual previous → revised decision and rationale, using the [review template](../templates/investor-review.md); a scheduled meeting is not evidence |
| Define product risks and measurable success criteria | §5.4 | [Product vision](../04-product-vision.md), supported by research and evaluation evidence |
| Demonstrate collaborative engineering and quality | §8.1, §8.3, §8.5 | Linked PRs, reviews, tests and CI results; acceptance evidence organised using the [DoD](../governance/definition-of-done.md) |
| Demonstrate individual contributions | §7.3.2, §10, §12 | Individual contribution statements linked to implementation, reviews, research, decisions and documentation. Explain impact; raw commit counts are insufficient |

The operational dashboard required by §6.7 and §7.3.2 monitors the running application. It is separate from these project-management charts.

## 2. Common measurement rules

- Use the board for operational status, following [issue conventions](../governance/issue-management.md). Update the documentation at reviews.
- Record the sprint dates, selected issue IDs and starting scope before measuring progress. Record dated scope additions/removals and reopenings.
- Count delivery items once: do not count both an epic and its children. Use item counts initially; the snapshot script does not capture estimates.
- Done means the acceptance criteria and DoD are met. Missing data does not mean Done. Counts indicate progress, not equal effort or individual productivity.
- Use one reporting timezone, retain UTC source timestamps and show missing snapshots as gaps.
- Save the selected chart, source data, sprint goal outcome and evidence links in `documents/planning/sprint-N-review.md` for each official sprint. These review records are to be created when evidence exists.

## 3. Data collection and configuration

Files: [snapshot.js](../../workflow-scripts/snapshot.js), [metrics.yml](../../.github/workflows/metrics.yml), [chart.html](../../workflow-scripts/chart.html) and [burndown.html](../../workflow-scripts/burndown.html).

### Implemented configuration

- Repository: `Phenriquerafael/LABDSOF_GX`; project number: `9`. These values are constants at the top of `snapshot.js`, not placeholders. The collector queries personal project `9` directly under user `Phenriquerafael`; a repository link is not required. The token must have access to the project. Confirm the owner and number in the project URL (`https://github.com/users/Phenriquerafael/projects/9`). In the supplied URL ending `/projects/9/views/3`, `9` is the project number and `3` is a view ID; the collector reads the project without applying view-specific filters.
- The collector runs as CommonJS on Node 20 without requiring a root `package.json`. Run it from the repository root with `node workflow-scripts/snapshot.js`, with `GITHUB_TOKEN` supplied through the environment.
- All output paths are resolved relative to the script: `workflow-scripts/data/history.json` holds timestamped issue/status snapshots; `workflow-scripts/data/raw/` holds one consolidated export per successful collection, matching `example.json`: `data.repository.projectsV2.nodes[]` contains project metadata and `items.nodes[]`, with issue `content.number`, `content.title`, `sprint` and `fieldValues.nodes[]` containing the Status and assigned Sprint values with their field names. Each issue in `history.json` has `{ id, status, sprint }`; `sprint` preserves the board label or is `null` when unassigned. All item pages are combined; only issues from the configured repository are included. These are normalized exports, not verbatim API responses; unrelated fields and empty field objects are omitted. Each new raw export includes a top-level `date` in ISO 8601 UTC, identical to its history entry. Its filename uses the same timestamp with colons replaced by hyphens, followed by the process ID: `2026-10-10T14-30-00.123Z-2358.json`. Older raw files retain their original format. Existing history is appended, not reset.
- The project is resolved directly by owner and number; its items are paginated. Status and Sprint are retrieved directly by field name rather than from a limited field list, using [GitHub's project field API](https://docs.github.com/en/graphql/reference/projects).
- Only issues from the configured repository are counted; PRs, draft items and issues from other repositories are excluded. The collector queries active project items: preserve review evidence before archiving/removing items. It collects the whole project, including each issue?s Sprint assignment, so the page can filter without recollecting data. The `sprintFieldName` constant defaults to `Sprint`; single-select, iteration and text fields are supported. A missing field or unassigned value is saved as `null` and logged. Configure the board field and assign values before collecting sprint measurements. Old snapshots are not backfilled from current assignments.
- HTTP/GraphQL errors, inaccessible items, missing Status values, invalid pagination and empty collections stop the run without appending to history. Invalid existing history is not overwritten. History is replaced only after the complete snapshot has been written to a temporary file.
- Both HTML pages use `./data/history.json`. `chart.html` renders stacked status counts; `burndown.html` defaults to all issues and filters by predefined sprint, plots remaining/ideal/scope lines, shows an issue list and daily table, supports local JSON selection and exports daily CSV data. Filters refresh automatically; no manual issue-number list is required.
- The workflow runs daily at `00:00 UTC` or manually, checks out `main`, runs the collector and commits `workflow-scripts/data/` back to `main`. Concurrent workflow runs are serialised. A rebase incorporates intervening commits before pushing; commit/push failures remain visible.

### Checks still required before automated collection

1. Configure the Actions secret `MY_PAT` with access to read the repository/project and push snapshot commits. It is passed to the collector as `GITHUB_TOKEN`; do not add tokens to tracked files.
2. Confirm the project URL identifies personal project `9` under `Phenriquerafael`, the token has `read:project` access, its single-select field is named `Status`, and each tracked issue has a value. If the URL uses `/orgs/` instead of `/users/`, the lookup must use an organisation owner rather than the current user query. Also configure the `Sprint` field with `A`/`Sprint A`, `B`/`Sprint B` and `C`/`Sprint C` assignments. The completed-status dropdown defaults to `Done`, includes predefined options and adds statuses found in the loaded history.
3. Confirm `main` is the intended destination and branch rules permit this workflow to push. Ensure the workflow is available on the repository's default branch for scheduled execution.
4. If earlier history exists at an old path, preserve and migrate it into `workflow-scripts/data/history.json` before the first run; do not silently start a new series or concatenate overlapping histories.
5. Run the workflow manually and inspect the saved history, consolidated raw export and resulting commit. Then verify scheduled collection. Live token permissions and project visibility have not been verified locally. The collector logs active item counts, item types and issue repositories. If no issues match, use that summary to distinguish an empty board, draft-only cards or issues belonging to another repository. Draft cards must be converted to repository issues (or existing issues added to the project) for the current issue-number-based charts; transferring a project does not transfer its issues.
6. Serve `workflow-scripts/` through HTTP and open either chart. Alternatively, open `burndown.html` directly and select a local history file. Select a sprint and completed status; review the issue list and missing-data messages.

The collector, workflow paths and chart defaults are aligned. Configuration is implemented; successful local checks do not constitute evidence of live collection or completed project work.

## 4. Charts and flow measures

These are ways to satisfy progress monitoring, not additional assignment requirements. Use burndown as the main sprint chart; use the others only where they help explain progress.

### 4.1 Burndown — remaining sprint work

**Calculation and interpretation**

For each UTC reporting day, use the latest snapshot and count issues assigned to the selected sprint. Remaining work is that scope minus issues in the selected completed status (case-insensitive). **All sprints** counts all repository issues, including unassigned issues. Assignments are taken from each historical snapshot, so additions, removals and sprint transfers change the recorded scope. The separate scope line helps distinguish these changes from completion; a drop in remaining work alone is not evidence of completion.

The ideal line uses the first non-empty, complete observed scope within the selected period: `reference scope ? (1 ? elapsed weekdays / remaining weekdays)`. It begins on that observation date and reaches zero at the period end, decreasing on Monday?Friday only (public holidays are not excluded). If collection began late, this is a late reference, not the original sprint commitment. There is no ideal line before that observation or if no working days remain after it. Later scope changes do not rebase the ideal line.

Missing daily snapshots, duplicate IDs or unknown selected statuses produce gaps. For a sprint filter, snapshots missing the `sprint` attribute on any issue also produce gaps because membership is unknown. Explicit `sprint: null` means unassigned and is excluded from a specific sprint; it is included under **All sprints**. Historical assignments are never inferred from collection dates. A complete snapshot with zero matching issues records zero scope. Archived/removed issues disappear from scope; this is not recorded as completion.

**Data source and implementation ? custom API snapshots and chart**

Open [burndown.html](../../workflow-scripts/burndown.html):

1. Serve the page through HTTP to load the default history automatically, or select a local `history.json` file. Local files are read in the browser without uploading. The expandable data-source section allows a different URL; use **Reload history** to refresh it.
2. Choose **All sprints** (default) or a predefined sprint. Dates are inclusive and in UTC:

   | Sprint | Start | End |
   |---|---|---|
   | A | 10 October 2026 | 31 October 2026 |
   | B | 1 November 2026 | 5 December 2026 |
   | C | 6 December 2026 | 3 January 2027 |

3. Choose the **Completed status**, default `Done`. Sprint and status changes update automatically. The issue list shows assignments from the latest snapshot on or before the selected period end, including planned work if the sprint has not started; its source timestamp is displayed. The chart only uses snapshots within the selected dates.
4. Review the issue list, daily values and gaps. **Download daily CSV** preserves `sprint,completed_status,date_utc,total_scope,done,remaining,ideal,data_quality` with the review.

Sprint labels `A` and `Sprint A` (likewise B/C) match case-insensitively. Other labels remain visible in **All sprints** but do not match the predefined filters. All-sprints dates span 10 October 2026?3 January 2027. The date presets are in `SPRINTS` in the HTML. The years are based on the current 2026/27 assignment period.

The page includes labelled controls, visible keyboard focus, a live status message, scrollable tables and distinct line styles. If Chart.js cannot load, the issue list, daily table and CSV remain available. Older history without sprint attributes works in **All sprints**, but cannot establish historical sprint membership. Run the updated collector to start recording it; no earlier progress is inferred.

Run the local regression checks with `node --test workflow-scripts/tests/metrics.test.cjs`. These use mocked API responses and the page?s calculation code; they do not verify live GitHub access.

### 4.2 Current status distribution — where work stands

**Calculation and interpretation**

Count selected items in each workflow status. The distribution shows how much work is waiting, active, under review or Done. It is a current snapshot, not evidence of how long items have spent there.

**Data source and implementation — GitHub Projects native Insights**

Create a current chart, filter to the sprint and group item counts by Status. Save its configuration and a dated capture for the review. Native Insights provides current charts and filtering; no custom API collector is needed for this view. [GitHub documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/viewing-insights-from-your-project/about-insights-for-projects)

### 4.3 Cumulative flow — status distribution over time

**Calculation and interpretation**

For each daily snapshot, count sprint items by Status and plot stacked areas in workflow order. A widening In review band indicates an increasing review queue; it does not establish the cause. Scope changes and reopened work can change the bands. Daily snapshots do not provide exact transition times or cycle times.

**Data source and implementation — custom API snapshots and existing HTML**

Use `snapshot.js` history with `chart.html`, which already renders stacked status counts. Apply the section 3 setup, sprint filtering, consistent workflow ordering and daily snapshot selection. Label it as status history with scope changes, rather than assuming all movement is forward.

### 4.4 Burnup — completed work and scope

**Calculation and interpretation**

Plot completed items and total scope over time. This helps distinguish delivery progress from growth in scope. State whether completion means board Status = Done or issue closure; these definitions are not automatically equivalent.

**Data source and implementation — native Insights or custom snapshots**

GitHub Projects offers a native historical Burn up chart based on issue/PR states. Use it if those states match the team's completion policy. For the exact sprint-scope and board-Status definition above, calculate Done and total scope from the snapshot table and add a custom chart. Native Insights excludes archived/deleted items, so preserve review evidence before removing them. [GitHub documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/viewing-insights-from-your-project/about-insights-for-projects)
