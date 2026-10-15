# LABDSOF_GX — agent instructions

**BMC — Building Maintenance Coordinator** (ISEP LABDSOF 26/27): platform to coordinate condominium faults. Repo `Phenriquerafael/LABDSOF_GX`, default branch `main`. Current stage: **Sprint 1 — discovery/validation/design**; there is no application code, tests, CI or deployment yet (walking skeleton excluded by DEC-11). These rules apply to every agent (opencode, Codex, Claude Code, T3 Code) working in this repository.

## Skills

Skills live in `.agents/skills/` (open standard), mirrored in `.claude/skills/` and `.opencode/skills/`; keep all copies in sync.

- `labdsof-workflow` — full team workflow: commits, branches, PRs, reviews, issues, epics, sub-issues, DoR/DoD, commands. Load it before doing commit, PR, review or issue work.
- `grilling` — relentless design-tree interview in rounds, to stress-test a plan or decision; triggers on "grill me" phrasing.
- `grill-me` — user-invoked entry point that starts a `grilling` session.

## Non-negotiables

- Never invent sources, results or evidence; cite exact URLs with access dates and separate supplier claims / observed behaviour / unknown.
- Never commit secrets, tokens, recordings or identifiable participant data.
- Do not mark remote configuration (protections, board, labels) as active without evidence; documentation status is not execution.
- Do not force-push shared branches or rewrite published history; recover with a revert PR.
- Use `Closes #N` only when the PR completes a real GitHub issue; otherwise reference with `Refs #N`.
- Authors never approve their own changes.

## Git and pull requests

- Short-lived branch from `main`: `feature/US-01-reporting`, `fix/BUG-12-state`, `docs/DISC-02-competitors`.
- Commits: `<ID>: <imperative summary>` (e.g. `US-01: validate building membership`). Small, purposeful commits.
- Follow `.github/pull_request_template.md` (Problem and outcome / Traceability / Change / Verification / Checklist / Deployment). Cite the local backlog ID (e.g. `DISC-02-01`). Docs-only PRs: review content, sources and links; do not claim code tests ran.
- Squash merges preferred; delete the merged branch when safe.

## Issues and tracking

- Hierarchy: epic (`EP-XX`) → parent task (`DISC-0x`, `EN-01`, `AI-01`) → delivery task (`DISC-02-01`); native GitHub sub-issues both ways; stable local IDs kept in titles as `[DISC-02-01] …`.
- Flow: Backlog → Refinement → Ready → In progress → In review → Done. DoR gates Ready; DoD gates Done (`documents/governance/definition-of-ready.md`, `definition-of-done.md`).
- Issue drafts live in `documents/backlog/{epics,tasks}/`; publishing steps in `documents/backlog/README.md`. After publication, GitHub Issues/Projects own live status.
- Labels on GitHub: `Epic`, `Task`, `Sub-Task`, `product`, `backend`, `ai`, `devops`, `security`, `frontend`, `documentation`, `bug`. Milestones: `Sprint A` (due 2026-11-01), `Sprint B` (2026-12-06), `Sprint C` (2027-01-03). The `type:*`/`area:*` scheme in `documents/governance/issue-management.md` is proposed, not fully applied remotely — check actual labels before creating issues.
- Board: `https://github.com/users/Phenriquerafael/projects/9`.

## Where to find what

- Overview and status: `README.md`; assignment: `LABDSOF-26-27-Assignment.md`.
- Git/branch/PR/review rules: `documents/governance/git-workflow.md`.
- Open decisions (DEC-XX), feedback, limitations: `documents/planning/decisions-and-feedback.md`.
- Sprint phases: `documents/planning/sprint-1-plan.md`; board and metrics: `documents/planning/project-monitoring.md`.
- Product backlog: `documents/06-product-backlog.md`.
- Team roles (P1–P5): `documents/governance/team-working-agreement.md` — Pedro PM, Ricardo Tech Lead, Afonso BA/PO, Sandro AI, Martim DevOps/QA/security.

## Verification and automation

- No build/test/lint commands exist yet (no code). Documentation changes are verified by content, source, consistency and link review.
- Commits named `update metrics` are automation (`.github/workflows/metrics.yml`, daily 00:00 UTC) appending `workflow-scripts/data/`. Do not hand-edit `history.json`; when changing the collector or charts, run `node --test workflow-scripts/tests/metrics.test.cjs`.
- In T3 Code sessions, register any PR you open for the thread with the `link_pull_request` tool.
