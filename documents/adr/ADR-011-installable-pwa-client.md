# ADR-011 — Client: installable PWA, photos, online-only operation and status banner

**Status:** Proposed
**Date:** 2026-10-27
**Participants:** Ricardo (P2, Tech Lead) — proposer; Pedro (P1, frontend/UX) to confirm; team review pending
**Related decision:** DEC-04, DEC-06
**Supersedes / superseded by:** —

## Context

- §6.1 lets the team choose a web application or a Progressive Web App among other client options (E01). Residents report faults from their phones, often with photos; administrators work mostly on a desktop; contractors answer requests from either. NFR-07 asks for keyboard journeys, visible focus and status not conveyed by colour alone ([requirements](../requirements.md)).
- The client is React 19 + Vite 8 + Tailwind 4 + shadcn/ui, built to static files served by nginx ([ADR-002](ADR-002-technology-stack.md)); its internal structure is in [ADR-009](ADR-009-service-internal-architecture.md) and its session in [ADR-005](ADR-005-authentication-authorisation.md).
- Report photos are a post-MVP design candidate (no backlog story; pending a DEC entry, see the [decision register](../planning/decisions-and-feedback.md#stack-revision--en-01-01-2026-10-27)), stored through the Issue service ([ADR-010](ADR-010-object-storage.md)).
- Degraded modes ([technical design §6](../07-technical-design.md#6-external-integration-and-degraded-mode)) must be communicated to users (§6.8, E01); the health and status mechanism is [ADR-012](ADR-012-health-and-status-page.md), this ADR owns the client side.

## Alternatives

**Delivery**

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Installable PWA (vite-plugin-pwa), online only** | One codebase for phone and desktop; installable where the browser supports it; Vite 8 is within the plugin's peer range | Install experience differs by browser; no offline use | E54, E64, E72 |
| B. Responsive web, no install | Least work | No home-screen icon or standalone window; weaker phone experience | — |
| C. Native or cross-platform apps | Store presence, native push | A second codebase, store accounts and review, outside the team's web skills; no assignment need | — |
| D. PWA with offline drafts and queued send | Reporting without connectivity | **Rejected by the Tech Lead: effort exceeds value.** Background Sync exists only in Chromium browsers; Safari storage is best-effort and can be evicted; conflict and duplicate handling would add a second sync path | E70 |

**Update strategy**

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. `registerType: 'prompt'`** | The user chooses when to reload; no lost form content | One toast to build | E72 |
| B. `autoUpdate` | No prompt | Reloads open tabs; “the user can lose data” in forms | E72 |

**Photo pipeline**

| Option | Benefits | Costs/risks | Evidence |
|---|---|---|---|
| **A. Client re-encodes to JPEG** | Smaller uploads; iPhone HEIC converted (Chrome and Android Chrome cannot decode HEIC); one format to test | Canvas work on the phone; `toBlob` may fall back to PNG, so `blob.type` is checked | E68, E69 |
| B. Upload originals | No client code | HEIC and multi-MB files reach the 5 MB limit and the server | E68 |
| C. Re-encode to WebP | Smaller files | Encoding support in Safari not verified | E69 |

## Proposed decision

**A / A / A**, proposed, not accepted.

### Manifest and service worker

- Web app manifest: `name`, `short_name`, 192 px and 512 px icons (including maskable), `start_url`, `display: standalone`, theme colours, optional `description` and `screenshots` for a richer install dialog. Served over HTTPS through Traefik ([ADR-004](ADR-004-deployment-contract.md)). These fields match Chrome's install criteria (E64).
- vite-plugin-pwa 2.0 with Workbox. The service worker **precaches the app shell and static assets only**. **API responses are never cached**: private data must not linger in a cache and users must not see stale states. Update flow: “New version available — Reload” toast; never a silent reload.

### Online-only behaviour

No offline drafts, no queued sends, no Background Sync. When offline the installed app still opens and shows “No connection — BMC needs internet to load and send data”; submit buttons are disabled with that reason visible next to them.

### Install UX

**One-click install is Chromium-only.** The install event is non-standard (E65); other browsers need a manual step, so the app guides rather than promises.

| Platform | Behaviour |
|---|---|
| Chrome, Edge, Samsung Internet (desktop, Android) | “Install app” button: capture `beforeinstallprompt`, `preventDefault()`, call `prompt()` on click (E65) |
| iPhone/iPad Safari, not installed | Short guided sheet “Share → Add to Home Screen” with an illustration, shown once and reachable from the menu; since Safari 26 a Home Screen site opens as a web app by default (E66) |
| macOS Safari | Hint “File > Add to Dock” (E66) |
| Firefox desktop | No install; the app works in the tab |
| Already installed (`display-mode: standalone`) | Nothing shown |

### Works everywhere

Not “mobile-first” overall. Resident and contractor journeys must be usable at 360 CSS px with no horizontal scrolling; touch targets at least 24×24 CSS px (WCAG 2.2 SC 2.5.8, E83) and larger on phones by design. Administrator screens are desktop-oriented but responsive. Anyone may install on desktop or phone.

### Photos

Design for the report-photos candidate; it applies only if the team accepts that scope change (DEC entry pending, [ADR-010](ADR-010-object-storage.md#candidate-acceptance-criteria-not-a-backlog-story)).

- Two controls: **Take photo** (`<input type="file" accept="image/*" capture="environment">`) and **Choose from gallery** (same input without `capture`). On iOS Safari `capture` does not force the camera but offers it (E67); desktop shows a file picker.
- Every photo is re-encoded with `createImageBitmap` and canvas/`OffscreenCanvas` to JPEG, checking `blob.type` because an unsupported type falls back to PNG (E69). This also converts HEIC (E68). Proposed starting values, not sourced, to tune in the spike (item 13): long edge about 2048 px, quality about 0.8. Preview and remove before sending.
- Client processing is a convenience, not a control: the server verifies type by content, enforces ≤ 5 photos × 5 MB and strips EXIF/GPS ([ADR-010](ADR-010-object-storage.md)).

### Web Push (next adapter, not built)

`WebPushChannelAdapter` behind the facade of [ADR-007](ADR-007-notification-service.md), plus a subscription table. Not in the MVP: iOS/iPadOS web push needs a Home Screen install and permission from a user gesture, the Java library's last release is 5.1.2 on 2025-02-17, and a VAPID key would need managing (E71).

### Status banner

Reads the public `/status/api` ([ADR-012](ADR-012-health-and-status-page.md)) on start, about every 60 s while open (proposal), and after an API call fails.

| Rule | Decision |
|---|---|
| Trigger | A capability relevant to the user's role is Unavailable after **two consecutive failed checks** (team proposal, not a sourced convention), or planned maintenance |
| Role filtering (proposal) | Resident: Report a fault, Sign-in, Photo upload, Notifications. Contractor: Schedule interventions, Sign-in, Notifications, Photo upload. Administrator: all. Exact sets to confirm with Pedro |
| Count | One banner at a time, combining all affected capabilities |
| Placement | Below the top bar, above the page heading (E82) |
| Content | Icon + affected capability + what still works + “See status”, for example “Photo upload is unavailable. You can still report faults without photos. See status.” |
| Dismissal | Dismissible for the session; reappears when the set of affected capabilities changes. **Not dismissible** while Sign-in or Report a fault is Unavailable. Sources do not agree on dismissal (E82); this is a team decision |
| Accessibility | `role="status"`, not `alert` (WCAG 4.1.3, E83); shadcn/ui `Alert` with the role set explicitly, as the component documents none (E82); never colour alone (E83); controls ≥ 24×24 CSS px |

## Consequences

- One codebase and one build; install quality varies by browser, and the docs say so.
- Offline reporting is not offered: a resident without connectivity cannot report. Accepted by the Tech Lead for effort reasons; revisit only with evidence of need.
- Photo re-encoding adds client code and phone-dependent behaviour (HEIC, memory on large images), tested on real devices.
- The banner needs a role on the client; signed-out visitors (and Sign-in outage, when no role can be loaded) see Sign-in and Report a fault only — open item for Pedro.
- Web Push later costs one adapter, a subscription table and key management.
- Update prompts depend on users reloading; an old client may call a changed API, so API compatibility follows the contract rules in [ADR-002](ADR-002-technology-stack.md).

## Verification and review

Planned, nothing exists yet:

- **Spike item 13:** photo pipeline on a real iPhone and a real Android device — HEIC→JPEG conversion, resulting size, `blob.type`, camera/gallery behaviour.
- Lighthouse and browser installability check of the manifest once client code exists; install flow on Chrome, Edge, iOS Safari and macOS Safari by hand.
- Offline check: the shell opens, API responses are absent from Cache Storage, submit is disabled with a visible reason.
- Banner accessibility: screen-reader announcement without focus move, keyboard dismissal, contrast and icon+text in both states, 360 px layout, 24×24 px targets.
- Banner logic tests with fake `StatusApi` providers ([ADR-009](ADR-009-service-internal-architecture.md)): two-failure threshold, role filtering, dismissal reset, non-dismissible cases.

Review after the spike item and when Pedro confirms components (EN01-U4).

## Record

2026-10-27 — proposed by Ricardo (Tech Lead) after a structured design interview; drafting and source checks AI-assisted (new ADR). Reason: reporting with photos from phones while the app works on every screen size, installability without a second codebase, and visible degraded modes; offline reporting rejected by the Tech Lead. Evidence: [evidence register](README.md#evidence-register-en-01-01) E01, E54, E64–E72, E82, E83; issue [#15](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/15). Affected documents: [technical design §1, §6](../07-technical-design.md#6-external-integration-and-degraded-mode), [requirements](../requirements.md) (NFR-07), ADR-002, ADR-009, [register §5](../planning/decisions-and-feedback.md#5-en-01-01-unresolved-details). Final decision, date and participants: pending team review.
