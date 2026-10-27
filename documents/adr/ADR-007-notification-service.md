# ADR-007 — Notification service: facade and channel adapters

**Status:** Proposed
**Date:** 2026-10-27
**Participants:** Ricardo (P2, Tech Lead) — proposer; team review pending
**Related decision:** DEC-06, DEC-07
**Supersedes / superseded by:** — (the 2026-10-15 proposal placed in-app notifications in a module of the Issue service, [ADR-001](ADR-001-backend-boundaries.md))

## Context

- §6.3 lists notifications as an example of asynchronous work, and §6.8 lists "a notification provider" among the dependencies a degraded-mode scenario may use (E01). A notification that fails must neither lose the business change nor disappear silently.
- The DEC-06 baseline was one in-app channel. The DISC-03-06 [workflows](../workflows/bmc-workflows.md) already need email for e-invites to people who have no account yet, and describe a resident opt-out; the [technical design](../07-technical-design.md#8-gaps-and-validation) lists email and opt-out as not yet covered, because email adds contact data (DEC-07).
- Business services decide that something must be notified; they should not know how it is delivered. The assignment does not prescribe a channel, so channels will be added or swapped (Mailpit now, a real SMTP account later).
- Keycloak owns email addresses ([ADR-005](ADR-005-authentication-authorisation.md)); services hold `sub` only. Services communicate only through RabbitMQ ([ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)).

## Alternatives

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Separate Notification service with a `NotificationFacade` and `NotificationChannel` adapters; recipients decided by the producing service** | One place for templates, preferences, idempotency, delivery log and retries; a new channel is one adapter; SMTP failure is isolated from the business services; no duplicated memberships | A third Spring deployable (more memory, more configuration); needs a Keycloak service account | E01, E16, E17, E52, E53 |
| B. Notification module inside the Issue service (2026-10-15 proposal) | No extra deployable | Dispatch events would reach residents only through Issue; email and SMTP retries mixed into the issue domain; harder to show notification failure as an independent degraded mode | E03 |
| C. Notification computes recipients from its own projection of memberships | Producers only say "this happened" | Duplicates memberships a third time; revocation lag grows with another projection; recipient rules (who counts as affected) are domain knowledge that belongs to the owners | — |
| D. Send email from Keycloak, or from each service directly | No new service | Keycloak sends only its own account emails; direct sending duplicates templates, preferences, retries and SMTP credentials in every service, and there is no single delivery log | E29 |

Keycloak's own emails (verification, password reset) stay with Keycloak and go to the same SMTP server; they are outside this ADR.

## Proposed or accepted decision

**A**, proposed, not accepted. The Notification service is a Spring Boot 4.1.2 deployable ([ADR-002](ADR-002-technology-stack.md)) with its own database `notification` ([ADR-001](ADR-001-backend-boundaries.md)).

### Structure

A hexagonal service ([ADR-009](ADR-009-service-internal-architecture.md)). The sketch below shows the intended shape of the ports; names and signatures are illustrative, not code that exists.

```text
application
  NotificationFacade
    notify(NotificationRequest request)
      for each recipient in request.recipients
        for each channel in channels
          if preferences.allow(recipient, request.templateKey, channel)
             -> record delivery (pending), channel.deliver(...)
          else
             -> record delivery (skipped_by_preference)

  port NotificationChannel
    ChannelId id()
    DeliveryResult deliver(Notification notification)

  port PreferenceRepository, DeliveryLogRepository, AddressDirectory
  port TemplateRenderer

adapters.out
  InAppChannelAdapter      implements NotificationChannel   (writes an inbox row)
  EmailChannelAdapter      implements NotificationChannel   (SMTP via Spring Mail)
  KeycloakAddressDirectory implements AddressDirectory      (lookup by sub, service account view-users)

adapters.in
  NotificationRequestedListener   (RabbitMQ, queue notification.inbox)
  NotificationsController         (GET /notifications, GET/PUT /preferences; reached at the edge as /api/notifications/…)
```

`NotificationFacade.notify(request)` resolves the recipient's preferences, and for each enabled channel calls that channel's `NotificationChannel` implementation. Adding a channel means adding one adapter and its configuration; the facade, the producers and the event do not change. This is the adapter pattern, one of the instances of the port style in ADR-009.

### Recipients are decided by the producer

Issue and Dispatch publish `NotificationRequested` to the `bmc.events` exchange ([ADR-003](ADR-003-asynchronous-messaging-rabbitmq.md)); it is routed to `notification.inbox`. The payload is `notificationId` (idempotency key), `sourceEventId`, `recipientUserIds`, `templateKey`, `params` (no private text) and `priority`.

- Issue decides recipients for issue-side events, and for Dispatch-driven events it projects (it owns memberships).
- Dispatch decides recipients for contractor-addressed events (from its own data) and for administrator-addressed events from its projection of building administrators.
- Notification never reads memberships and never interprets domain events.

**Invitation exception.** An e-invite goes to someone with no account, so `NotificationRequested` carries `recipientAddress` and the invite link instead of `recipientUserIds`. This is the only message type with an address and a secret link. The DLQ message TTL of 7 days applies, the delivery log stores neither address nor link, and payloads are never logged. Whether Notification keeps a rendered body is an EN-01-04 point.

### Addresses, templates and preferences

- Address lookup happens at send time: Notification asks Keycloak for the user's email by `sub` through its service account (`view-users`, client-credentials grant; E17). Addresses are not stored in messages (except invitations) and not persisted by Notification.
- Templates are rendered server-side from `templateKey` and `params`; the client never supplies message text.
- Preferences are per user, per event type and per channel. Opt-out applies to **email only**, per event type: the in-app notification is always created, because it is the status record a resident can always look up. This is how the workflows' “the resident can turn notifications off” is read. Which email notifications cannot be switched off (for example invitations, which have no account, and security-relevant ones) is an open item (EN01-U8).

### Idempotency, delivery log and retries

- Unique (`notificationId`, `recipientUserId`, `channel`) in the delivery log. A redelivered `NotificationRequested` therefore creates no second inbox row and no second email. For an invitation the key is `notificationId` and the channel.
- The listener writes the delivery rows in one transaction and acknowledges after commit. The in-app adapter completes its row in that transaction; the email adapter sends after the commit, so a slow SMTP server never holds the message.
- Delivery states: `pending`, `sent`, `failed`, `skipped_by_preference`.
- An SMTP failure is retried with backoff and then marked `failed`; the number of attempts and delays are proposals to calibrate in the spike (EN01-U7), not measured values. `failed` deliveries are counted in a metric and visible to operators ([ADR-004](ADR-004-deployment-contract.md) dashboard: notification failures).
- If the process dies between an accepted SMTP send and the state update, the retry can send the email twice. Delivery by email is at-least-once; the in-app inbox is exactly one row per key.

### Channels

- **In-app** (always on): the inbox, served at the edge path `/api/notifications/notifications` (service-relative `GET /notifications`) to the authenticated user's own notifications only; the Notification service is a resource server like the others ([ADR-005](ADR-005-authentication-authorisation.md)).
- **Email**, SMTP through Spring Mail: **Mailpit** in dev and demo, which captures mail and shows it in a web UI (E52). A later adapter for a Gmail account would use an App Password, which requires 2-Step Verification, is not available for work or school accounts and is revoked when the account password changes (E53); the secret stays outside Git. Using a personal Gmail account for a university project is not decided here.

### Degraded mode

When SMTP is unavailable, the in-app notification is still created, the email delivery is retried and then `failed`, and the failure is visible in metrics. The UI can show "notification provider unavailable", which gives §6.8 a degraded-mode scenario that does not stop any business function. When Keycloak is unavailable for the address lookup, the email delivery stays `pending` and is retried.

### Mapping to the workflow notification table

The [notification table](../workflows/bmc-workflows.md#notification-table) maps to templates. Which service requests each one is a proposal for EN-01-03:

| Workflow event | Notified | Requested by |
|---|---|---|
| Invite sent | Resident (email, invitation exception) | Issue |
| Report received | Resident | Issue |
| Proposal ready | Administrator | Dispatch (matching is in Dispatch) |
| Request sent | Contractor | Dispatch |
| Contractor accepts; counterproposes; booking not recorded | Administrator | Dispatch |
| Booking confirmed; booking cancelled | Administrator, contractor (cancelled only) | Dispatch |
| Booking confirmed; booking cancelled | Resident | Issue, after applying the projected Dispatch event |
| Summary published | Residents of the building | Issue |
| Work completed | Administrator | Dispatch |
| Issue closed or reopened | Resident | Issue |

The DEC-06 baseline changes from "one in-app channel" to "in-app plus email (Mailpit in dev/demo)". The workflows' own wording ("one channel in the MVP") must be updated with it.

## Consequences

- A third Spring JVM and one more database (`notification`) to run; the memory is part of the spike measurement (EN01-U3).
- Producers stay unaware of channels; adding a channel (for example web push) touches only Notification.
- Residents get email only if Keycloak holds a verified address; they can switch it off per event type. Email adds contact data, which DEC-07 must cover (EN01-U11).
- A Keycloak service account with `view-users` can read every user in the realm; it is confined to Notification and its secret to the environment.
- The 2026-10-15 design placed the `Notification` entity in Issue; [technical design](../07-technical-design.md#21-issue-service) §2.1, §4.2 (`GET /notifications`) and §4.4 (consumers "Notification module") must follow.
- Private report text never enters `NotificationRequested`; `params` carry identifiers and labels only.

## Verification and review

Tests with the implementation, using real RabbitMQ and MySQL containers where possible and an SMTP test server (Mailpit):

- A duplicate `NotificationRequested` produces one delivery per channel (one inbox row, one email).
- SMTP down: the in-app notification is created, the email delivery is retried and ends `failed`, and the failure appears in the metric.
- Preference off for email: the delivery is recorded `skipped_by_preference`, no email is sent, the in-app row is still created.
- Keycloak address lookup unavailable: the email delivery stays `pending` and is retried; the in-app row exists.
- An invitation message appears in no log and the DLQ copy expires after 7 days.
- `GET /api/notifications` returns only the caller's own rows.

Review after the spike (EN01-U2: Keycloak service account) and at EN-01-03, where Afonso details templates and preferences (EN01-U8); EN-01-04 reviews the invitation exception.

## Record

2026-10-27 — proposed by Ricardo (Tech Lead) after a structured design interview for EN-01-01; drafting and source checks AI-assisted. Reason: the workflows need email and opt-out beyond the DEC-06 baseline, and notification delivery is a natural isolated failure for the §6.8 scenario. Evidence: [evidence register](README.md#evidence-register-en-01-01) E01, E03, E16, E17, E29, E52, E53; issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15). Affected documents: [technical design](../07-technical-design.md), [workflows](../workflows/bmc-workflows.md), [security](../09-security-privacy.md), DEC-06, DEC-07. Final decision, date and participants: pending team review.
