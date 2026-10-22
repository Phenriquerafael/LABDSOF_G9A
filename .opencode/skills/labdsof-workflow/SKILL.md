---
name: labdsof-workflow
description: Use when working in the LABDSOF_GX repository (Building Maintenance Coordinator, ISEP LABDSOF 26/27): making commits, branches, pull requests, code reviews, GitHub issues, epics, tasks, sub-issues, labels, milestones, DoR/DoD checks, or consulting the team's backlog, governance and workflow conventions.
---

# LABDSOF_GX — team workflow

Mirrored for every agent harness: canonical `.agents/skills/labdsof-workflow/SKILL.md` (open standard, read by Codex and T3 Code sessions), copies in `.claude/skills/` (Claude Code) and `.opencode/skills/` (opencode). Edit the canonical copy, copy it over both mirrors, then run `scripts/check-skill-mirrors.sh` (fails on any drift). The repository root `AGENTS.md` is loaded every session and holds only the always-on rules plus a pointer here; this skill is the single source for the details.

## Project snapshot

- **BMC — Building Maintenance Coordinator**: platform to coordinate condominium faults (report → triage → intervention → closure), with AI-assisted triage.
- Repo: `github.com/Phenriquerafael/LABDSOF_GX`, default branch `main`. Stage: **Sprint 1 — discovery/validation/design**. There is **no application code, tests, CI or deployment yet**; the walking skeleton is excluded from Sprint 1 by DEC-11.
- Team (P1–P5): Pedro (PM, frontend/UX), Ricardo (Tech Lead, issue backend), Afonso (BA/PO, intervention backend), Sandro (AI), Martim (DevOps/QA/security).
- Authors **never approve their own changes**. At least one other member reviews.

## Where to find what

| Topic | File |
|---|---|
| Overview, status table, "start here" | `README.md`; assignment: `LABDSOF-26-27-Assignment.md` |
| Branch, commit, PR, review rules | `documents/governance/git-workflow.md` |
| Backlog workflow, proposed labels/milestones | `documents/governance/issue-management.md` |
| Ready/Done gates | `documents/governance/definition-of-ready.md`, `definition-of-done.md` |
| Roles, working agreement | `documents/governance/team-working-agreement.md` |
| Decisions DEC-XX, feedback FB-XX, limitations LIM-XX | `documents/planning/decisions-and-feedback.md` |
| Sprint phases/deliverables | `documents/planning/sprint-1-plan.md` |
| Board, metrics collector, charts | `documents/planning/project-monitoring.md` |
| Product backlog (epics, stories, MoSCoW) | `documents/06-product-backlog.md` |
| Issue drafts + ownership + publishing steps | `documents/backlog/README.md` (+ `epics/`, `tasks/`) |
| Issue/PR templates | `.github/ISSUE_TEMPLATE/{user-story,epic,task,bug}.md`, `.github/pull_request_template.md` |
| Product docs 01–10, requirements, ADRs | `documents/*.md`, `documents/adr/` |

## Commits and branches

- Short-lived branch from `main`: `feature/US-01-reporting`, `fix/BUG-12-state`, `docs/DISC-02-competitors`.
- Commits: `<ID>: <imperative summary>` — e.g. `US-01: validate building membership`; real example: `DISC-02-01: verify competitor and alternative sources`. Small, purposeful commits.
- No secrets, tokens, env files, recordings or identifiable participant data in commits.
- Do not force-push shared branches or rewrite published history. Docs accompany scope/contract changes in the same PR.

## Pull requests and reviews

- Follow the PR template: Problem and outcome / Traceability / Change / Verification / Checklist / Deployment and recovery.
- `Closes #N` **only** when a real GitHub issue exists and the PR completes it; otherwise reference with `Refs #N`. Also cite the local backlog ID.
- Request review from another member; resolve comments before merge. Squash merges preferred, preserving item reference and authorship. Delete merged branches when safe.
- Documentation-only PRs: review content, sources and links; **do not claim code tests were run**. Never mark external configuration as active without evidence.
- Recover merged mistakes by a revert PR (not by rewriting history).

## Issues, epics and sub-issues

- Hierarchy: **epic (`EP-XX`) → parent task (`DISC-0x`, `EN-01`, `AI-01`) → delivery task (`DISC-02-01`)**. AI-01 is a direct task under EP-02. Use native GitHub sub-issues in both directions. IDs are stable local identifiers kept in titles: `[DISC-02-01] Verify competitor and alternative sources`.
- Status flow: Backlog → Refinement → Ready → In progress → In review → Done. `Blocked` is a flag with reason/dependency/next action. DoR gates Ready; DoD gates Done. Do not select items that fail the DoR as commitments.
- Drafts live in `documents/backlog/{epics,tasks}/` with a publication field. Publishing steps (README §"Publishing to GitHub"): confirm scope/owner/reviewer/estimate with the team → create epic issues first, then parent tasks, then delivery tasks → convert relative links to repo/commit permalinks → add two-way parent/child links → record the issue URL and mark Published. After publication, GitHub Issues/Projects own live status.
- Never assume which drafts are already published: query GitHub (`gh issue list --repo Phenriquerafael/LABDSOF_GX --state all --limit 200`) and match the `[ID]` in titles before creating an issue, to avoid duplicates. Board: personal project 9, `https://github.com/users/Phenriquerafael/projects/9`.
- Labels on GitHub: `Epic`, `Task`, `Sub-Task`, `product`, `backend`, `ai`, `devops`, `security`, `frontend`, `documentation`, `bug`. Milestones: `Sprint A` (due 2026-11-01), `Sprint B` (2026-12-06), `Sprint C` (2027-01-03); windows: A = 10–31 Oct 2026, B = 1 Nov–5 Dec 2026, C = 6 Dec–3 Jan 2027. The `type:*`/`area:*`/`priority:*` scheme in `issue-management.md` is proposed, not fully applied remotely — check actual labels before creating issues.
- Issue reality rules: docs status ≠ execution; leave acceptance boxes unchecked until evidence is reviewed; attach existing commits/PRs as evidence instead of fabricating prior planning.

## DoR / DoD essentials

- **DoR**: stable ID and epic link, explicit scope with observable acceptance criteria, dependencies resolved, verification strategy, team estimate, agreed owner + reviewer, DoR check recorded with date/author. Extra criteria by type (story/integration/AI/research/spike/documentation) in the file.
- **DoD common**: acceptance criteria met with evidence linked; independent review done and comments resolved; merged via PR referencing the issue ID; docs/decisions/board consistent; no secrets or invented results; limitations explicit.
- Documentation/research work requires content, source, consistency and link review — **not** code tests or container images. Code work adds build/tests/static analysis/CI per the DoD.

## Useful commands

```bash
gh issue list --repo Phenriquerafael/LABDSOF_GX --state all --limit 200   # live list of published issues
gh issue create --repo Phenriquerafael/LABDSOF_GX --title "[DISC-02-03] ..." --body-file draft.md --label Task --milestone "Sprint A"
gh pr create --repo Phenriquerafael/LABDSOF_GX --title "DISC-02-01: ..."   # PR template auto-fills body
gh pr review <n> --comment|--approve|--request-changes   # never on your own PR
# Link a sub-issue (child's numeric database id):
gh api repos/Phenriquerafael/LABDSOF_GX/issues/<child> --jq .id
gh api repos/Phenriquerafael/LABDSOF_GX/issues/<parent>/sub_issues -f sub_issue_id=<id>
```

If `gh issue view`, `gh pr view` or `gh pr edit` fails with `GraphQL: Projects (classic) is being deprecated … (repository.issue.projectCards)` (seen with some `gh` versions), update `gh` or fall back to REST: `gh api repos/Phenriquerafael/LABDSOF_GX/issues/<n>`, `gh api -X PATCH repos/Phenriquerafael/LABDSOF_GX/pulls/<n> -F body=@body.md`.

## Automation and pitfalls

- Commits named `update metrics` are automation (`.github/workflows/metrics.yml`, daily 00:00 UTC) appending `workflow-scripts/data/`. Do not hand-edit `history.json`; when changing the collector or charts, run `node --test workflow-scripts/tests/metrics.test.cjs`.
- `grilling` and `grill-me` are vendored verbatim from `mattpocock/skills` (MIT): keep the `LICENSE` file in each skill folder, and when updating from upstream, re-pin `metadata.source` to the new commit SHA and re-check that the body still matches upstream.
- `P1–P5` = team members; `P1–P7` = research hypotheses — different namespaces. `Sprint A/B/C` (milestones) vs `Sprint 1/2/3` (narrative) vs `Sprint B` (planning concept, DEC-03 open): do not assume B = Sprint 2.
- Never invent sources, results or evidence. Cite exact URLs with access dates (S01–Sxx) and separate supplier claims / observed behaviour / unknown capabilities. Record unavailable sources as limitations, not current facts.
- DEC register: record decisions with evidence, author, date and affected documents. At least one product/technical decision must actually be revised from lecturer feedback (§5.7) — a scheduled meeting or minutes without a change is not enough.
- In T3 Code sessions, register any PR you open for this thread with `link_pull_request`.
