# EP-01 technical refinement

The working choices for [PLAN-01](tasks/PLAN-01-prepare-reporting-and-tracking-stories.md) are now in the stories and existing design documents. This file is a reference index, not an additional approval checklist.

| Topic | Development basis |
|---|---|
| Stack and boundaries | React, Spring Boot Issue/Dispatch/Notification, Flask AI, MySQL, RabbitMQ and Keycloak; [technical design §1](../07-technical-design.md#1-context-and-boundaries) |
| Fields, persistence and API | [Contract examples §1](../07a-contract-examples.md#1-principal-journey) and [field limits](../07a-contract-examples.md#41-shared-fields-and-access); service-owned data and transactional outbox |
| Identity and access | Keycloak plus server-owned memberships/assignments; [access projection](../07-technical-design.md#43-how-dispatch-obtains-trustworthy-authorisation-context) and negative scenarios |
| States, history and concurrency | [State table](../07-technical-design.md#3-states-and-business-rules), ETag/version checks and late-result protection |
| Notifications | Separate Notification service, in-app channel, [messages](../07a-contract-examples.md#42-service-contracts-and-messaging) and [recipient rules](../07a-contract-examples.md#44-notifications-and-optional-features) |
| Verification inputs | Contract examples, planned synthetic data/fake adapters and [test-tool choices](../07a-contract-examples.md#45-calendar-adapters-and-test-access) |

EN-02/03 implement the shared environment, identity configuration, executable schemas and CI. Story implementation supplies its own tests and integration evidence. These are delivery tasks, not requirements to invent completed checks before development.

Formal ADR review, sprint capacity and independent PR review retain their normal workflow. The selected proposal is a working development base, not evidence of accepted ADRs, deployed services or passed application tests.
