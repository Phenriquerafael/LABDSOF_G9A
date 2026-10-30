# Definition of Done (DoD)

**Status:** proposal v0.2 · ratification pending (DEC-09)

An item is Done when its agreed result has been delivered, verified and reviewed.

## Checklist

- [ ] Acceptance criteria are met, with evidence in the issue/PR.
- [ ] Applicable tests and checks pass.
- [ ] Another member reviewed the changes, comments are resolved and the PR is merged.
- [ ] Necessary documentation and affected decisions are updated.
- [ ] No secrets or unnecessary personal data are included; relevant limitations are recorded.

The reviewer verifies the acceptance criteria.

## Additional checks when applicable

### Code and configuration

Test affected rules, persistence/contracts and critical journeys, including permissions and failures. Run relevant build, static analysis and dependency checks.

Build/run changed components, including containers when affected. Update APIs, logs/metrics, architecture, configuration and migration/recovery instructions where needed.

### AI

Test relevant normal/adverse cases, fallback and protection of human decisions. Distinguish suggestions from confirmed decisions; AI output cannot authorise consequential actions.

Record model/prompt/data versions and relevant quality, latency and cost results. US-15 covers the full baseline comparison. Repeat checks affected by a change; small changes do not automatically require the entire evaluation.

### Research and documentation

Check content, sources, consistency and links. Separate facts, hypotheses and simulated examples; report only work actually performed and link findings to affected decisions.

Documentation-only work uses documentation checks rather than code tests or container builds.

## Evidence

Keep checks, results and demonstration links in the issue/PR and reference them elsewhere.

Record limitations, keep backlog status consistent and leave unmet acceptance criteria open.
