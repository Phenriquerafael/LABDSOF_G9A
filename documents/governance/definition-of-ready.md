# Definition of Ready (DoR)

**Status:** proposal v0.3 · ratification pending (DEC-09)

An item is Ready when the team has enough information to start developing it. Keep its ID, title, epic and relevant requirement/source identified.

## Checklist

- [ ] The story explains who needs the feature, what they want and why.
- [ ] Scope and acceptance criteria are clear, including success, errors and denied access where applicable.
- [ ] Relevant dependencies are identified and no unresolved decision prevents work from starting.
- [ ] An estimate in story points and a short reason are recorded.
- [ ] The team knows how to verify the result, has the data/access needed to start, and understands the relevant permissions, failure and quality risks.
- [ ] The team understands the item and considers it clear enough to develop.

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

Priority, sprint and capacity are agreed during planning, before committing the item to a sprint. Owner and reviewer assignment are not prerequisites for Ready.

Assign the owner during planning or before work starts. Choose the reviewer when opening the PR; independent review is required before Done according to the [DoD](definition-of-done.md).

Items with questions that prevent development remain in Refinement; a bounded investigation can be planned separately.
