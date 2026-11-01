# Definition of Ready (DoR)

**Status:** proposal v0.4 · ratification pending (DEC-09)

An item is Ready when the team has enough information to start developing it. Keep its ID, title, epic and relevant requirement/source identified.

## Checklist

- [ ] The story explains who needs the feature, what they want and why.
- [ ] Scope and acceptance criteria are clear, including success, errors and denied access where applicable.
- [ ] Relevant dependencies are identified and no unresolved decision prevents work from starting.
- [ ] An estimate in story points and a short reason are recorded.
- [ ] The team knows how to verify the result, has the data/access needed to start, and understands the relevant permissions, failure and quality risks.
- [ ] Owner and independent reviewer are agreed during planning, before Ready.
- [ ] The team understands the item and records the date and author of the DoR check.

For a technical or documentation task, state the intended outcome instead of a user story.

## Additional criteria when applicable

| Type | Information needed before Ready |
|---|---|
| Integration | Contract, authentication, timeout and handling of invalid or duplicate data |
| AI | Example inputs/outputs, baseline/fallback, evaluation criteria and planned model/prompt version |
| Research | Question, method, sources/participants, access and data handling |
| Spike | Question, effort limit and expected result |
| Documentation | Audience, purpose and sources |

Only the details needed to start must be settled. Later implementation work, completed evaluations and final results are not prerequisites for Ready.

## Planning and review

Estimate stories before Ready using story points (1, 2, 3, 5, 8, 13). Include the story's UI/API work, persistence, permissions, integration and applicable tests/review. Points express relative effort, complexity and uncertainty, not hours.

Review initial estimates when scope or technical assumptions change. Count shared foundations once.

Priority, sprint and capacity are agreed during planning, before committing the item to a sprint. Owner and reviewer agreement is required before Ready, consistently with the repository workflow.

Agree the owner and independent reviewer during refinement/planning before Ready, and request the agreed review when opening the PR. Independent review is required before Done according to the [DoD](definition-of-done.md).

Items with questions that prevent development remain in Refinement; a bounded investigation can be planned separately.
