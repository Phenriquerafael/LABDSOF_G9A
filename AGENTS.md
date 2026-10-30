# LABDSOF_G9A — agent instructions

**BMC — Building Maintenance Coordinator** (ISEP LABDSOF 26/27): platform to coordinate condominium faults. Repo `Phenriquerafael/LABDSOF_G9A`, default branch `main`. Current stage: **Sprint 1 — discovery/validation/design**; there is no application code, tests, CI or deployment yet (walking skeleton excluded by DEC-11). These rules apply to every agent (opencode, Codex, Claude Code, T3 Code) working in this repository.

This file holds only the always-on rules. Details (where to find what, commits, branches, PRs, reviews, issues, labels, milestones, DoR/DoD, commands, pitfalls) live in the `labdsof-workflow` skill — load it before any commit, PR, review or issue work, and edit details there, not here.

## Skills

Canonical copies live in `.agents/skills/` (open standard), mirrored byte-for-byte in `.claude/skills/` and `.opencode/skills/`. Edit the canonical copy, copy it over both mirrors, then run `scripts/check-skill-mirrors.sh`.

- `labdsof-workflow` — full team workflow and repository map.
- `grilling` — relentless design-tree interview in rounds, to stress-test a plan or decision; triggers on "grill me" phrasing.
- `grill-me` — user-invoked entry point that starts a `grilling` session.
- `takeover` — take over an existing PR, branch or agent thread, preserving the original contributors' credit.

`grilling` and `grill-me` are vendored from `mattpocock/skills` (MIT) and `takeover` from `rmotafreitas/dotfiles` (MIT); keep their `LICENSE` files and pinned `source`, plus the `SOURCE.md` where one exists.

## Non-negotiables

- Never invent sources, results or evidence; cite exact URLs with access dates and separate supplier claims / observed behaviour / unknown.
- Never commit secrets, tokens, recordings or identifiable participant data.
- Do not mark remote configuration (protections, board, labels) as active without evidence; documentation status is not execution.
- Do not force-push shared branches or rewrite published history; recover with a revert PR.
- Use `Closes #N` only when the PR completes a real GitHub issue; otherwise reference with `Refs #N`.
- Authors never approve their own changes.
- Before creating an issue, query GitHub for the `[ID]` — never assume which drafts are published.

## Quick reference

- Branch from `main` (`docs/DISC-02-competitors`); commit as `<ID>: <imperative summary>`; follow `.github/pull_request_template.md`; squash-merge.
- Documentation-only changes are verified by content, source, consistency and link review; do not claim code tests ran.
- Commits named `update metrics` are automation; do not hand-edit `workflow-scripts/data/history.json`.
- In T3 Code sessions, register any PR you open for the thread with the `link_pull_request` tool.
