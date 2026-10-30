"""The seven BMC physical views, drawn with vpdraw.

Each function places its shapes by hand from the text of
documents/07b-physical-views.md and the ADRs it cites; change the text there
first, then the coordinates here, then re-render (see README.md).

    python3 views.py            # writes p1..p7 .svg
    python3 views.py --png      # also writes the .png files (needs Chromium)
"""

import os
import subprocess
import sys
from pathlib import Path

from vpdraw import ELEMENT, OUTSIDE, Diagram

HERE = Path(__file__).resolve().parent


def p1():
    d = Diagram("p1-deployment-overview", "P1 Deployment overview", 1900, 1090)
    d.pool(20, 20, 1860, "Outside\nthe host", [("", 130)])
    d.box("device", 130, 42, 220, 84, ["User device", "browser or installed PWA", "online only"],
          icon="device", fill=OUTSIDE)
    d.box("ghcr", 1250, 42, 260, 84, ["GitHub Container Registry", "one multi-arch image per app",
                                      "linux/amd64 and linux/arm64"], icon="cloud", fill=OUTSIDE)

    d.pool(20, 180, 1860, "Demonstration host\nDocker Engine + Compose",
           [("edge network only", 180), ("edge + internal networks", 200), ("internal network only", 330)])
    d.box("traefik", 130, 240, 220, 84, ["traefik", "Traefik 3.7", "publishes 80 and 443"])
    d.box("client", 560, 240, 220, 84, ["client", "nginx", "React + Vite build"])
    d.box("o2p", 890, 240, 220, 84, ["oauth2-proxy", "oauth2-proxy 7.15", "browser session (BFF)"])

    row = [("issue", ["issue", "Spring Boot 4.1.2", "Java 25"], "/api/issue/*"),
           ("dispatch", ["dispatch", "Spring Boot 4.1.2", "Java 25"], "/api/dispatch/*"),
           ("notification", ["notification", "Spring Boot 4.1.2", "Java 25"], "/api/notifications/*"),
           ("keycloak", ["keycloak", "Keycloak 26.8", "sign-in and accounts"], "/auth/*"),
           ("gatus", ["gatus", "Gatus 5.37", "capability checks"], "/status/api")]
    for i, (key, lines, route) in enumerate(row):
        x = 130 + 300 * i
        d.box(key, x, 440, 220, 84, lines)
        cx = x + 110
        d.edge([(240, 324), (240, 400), (cx, 400), (cx, 440)] if i else [(240, 324), (240, 440)],
               route, at=(cx + 8, 420))

    internal = [("aiweb", 130, 600, ["ai-triage-web", "Python 3.14 · Flask", "Gunicorn"], "node"),
                ("sim", 430, 600, ["calendar-sim", "Spring Boot · Java 25", "in memory, fixed seed"], "node"),
                ("mailpit", 730, 600, ["mailpit", "Mailpit 1.32", "SMTP capture"], "node"),
                ("grafana", 1030, 600, ["grafana", "Grafana 13"], "node"),
                ("prom", 1330, 600, ["prometheus", "Prometheus 3.x"], "node"),
                ("aicon", 130, 765, ["ai-triage-consumer", "same image", "consumer process"], "node"),
                ("rabbitmq", 430, 765, ["rabbitmq", "RabbitMQ 4.x", "quorum queues and DLQs"], "queue"),
                ("mysql", 730, 765, ["mysql", "MySQL 8.4 LTS", "four databases"], "db"),
                ("garage", 1030, 765, ["garage", "Garage 2.5 · single node", "two buckets"], "bucket")]
    for key, x, y, lines, icon in internal:
        d.box(key, x, y, 220, 84, lines, icon=icon)

    d.pool(20, 920, 1860, "Outside\nthe host", [("", 150)])
    d.box("ai", 130, 955, 220, 84, ["AI provider API", "candidate: Gemini Flash", "choice open (DEC-05)"],
          icon="cloud", fill=OUTSIDE)
    d.box("r2", 1030, 955, 220, 84, ["Off-host backup copy", "Cloudflare R2", "optional"],
          icon="cloud", fill=OUTSIDE, dashed=True)

    d.edge([(240, 126), (240, 240)], "HTTPS 443", at=(250, 205))
    d.edge([(350, 282), (560, 282)], "/  and  /status", at=(455, 268), anchor="middle")
    d.edge([(320, 240), (320, 205), (1000, 205), (1000, 240)], "/oauth2/*", at=(660, 205), anchor="middle")
    d.edge([(1380, 126), (1380, 180)], "image pull, every app container", at=(1390, 140))
    d.edge([(240, 849), (240, 955)], "HTTPS · the only egress the design needs", at=(250, 872))
    d.edge([(1140, 849), (1140, 955)], "backup copy", at=(1150, 872), dashed=True)

    d.note(1200, 222, ["This document's reading, not ADR text:", "keycloak joins internal because its",
                       "database is in MySQL."], attach=d.p("keycloak", "n", 0.85))
    d.note(1610, 598, ["Open (P-01): prometheus is on internal",
                       "only, yet ADR-004 has it scrape traefik",
                       "and oauth2-proxy, which are on edge only."], attach=d.p("prom", "e"))
    d.note(430, 960, ["Open (P-02): if internal is declared internal: true, the AI",
                      "containers cannot reach the provider, and a later real",
                      "SMTP server is unreachable for notification and keycloak."], attach=d.p("ai", "e"))
    d.note(1330, 768, ["The connections from the services to the broker,",
                       "the databases, storage, mail and the calendar",
                       "are drawn in P3 and P4."])
    return d


def p2():
    d = Diagram("p2-edge-and-trust", "P2 Edge routing and trust boundaries", 1860, 780)
    d.pool(20, 20, 1820, "Edge request path · routes of ADR-004, authorisation of ADR-005",
           [("Internet", 150), ("traefik container\ntrust boundary 1", 200),
            ("Public upstreams\nno ForwardAuth", 190), ("API services\ntrust boundary 2", 200)])

    d.event("start", 205, 80, "Browser or installed PWA\none origin, no CORS", at=(28, 0))
    d.box("router", 120, 230, 170, 80, ["Router", "TLS terminates here"], icon="gear")
    d.diamond("rule", 430, 270, "Which rule?", at=(-62, -26))
    d.event("never", 430, 80, "", end=True)
    d.note(480, 26, ["Not routed: no Traefik rule (ADR-004)", "Gatus UI · Traefik API and dashboard",
                     "liveness, readiness, Actuator, /metrics", "AI /classify · simulator control",
                     "RabbitMQ management, Garage, Mailpit", "open: Keycloak paths kept unrouted,",
                     "and how Grafana is reached in demo"], attach=(450, 80))
    d.box("fa", 940, 230, 240, 80, ["ForwardAuth", "asks oauth2-proxy for the session",
                                    "passes Authorization: Bearer"], icon="gear")
    d.diamond("valid", 1270, 270, "Session valid?", at=(0, 46))
    d.event("deny", 1270, 75, "401, no redirect for API calls", end=True, at=(30, 0))
    d.box("strip", 1370, 230, 200, 80, ["StripPrefix", "removes /api/<service>", "then RateLimit, Headers"],
          icon="gear")

    d.edge([(205, 100), (205, 230)], "HTTPS 443", at=(213, 200))
    d.edge([(290, 270), (401, 270)])
    d.edge([(430, 241), (430, 100)], "no matching rule", at=(438, 205))
    d.edge([(459, 270), (940, 270)], "/api/<service>/*", at=(700, 258), anchor="middle")
    d.edge([(1180, 270), (1241, 270)])
    d.edge([(1270, 241), (1270, 95)], "no session", at=(1278, 205))
    d.edge([(1299, 270), (1370, 270)], "yes", at=(1334, 258), anchor="middle")

    public = [("client", 110, ["client", "nginx static files"], "/  and  /status"),
              ("gatus", 310, ["gatus", "read-only JSON API"], "/status/api"),
              ("keycloak", 510, ["keycloak", "sign-in pages"], "/auth/*"),
              ("o2p", 740, ["oauth2-proxy", "session, OIDC client"], "/oauth2/*")]
    for key, x, lines, route in public:
        w = 200 if key == "o2p" else 170
        d.box(key, x, 440, w, 84, lines)
        cx = x + 60 if key == "o2p" else x + w / 2
        d.edge([(430, 299), (430, 410), (cx, 410), (cx, 440)], route, at=(cx + 8, 427))
    d.edge([(1000, 310), (1000, 482), (940, 482)], "session check", at=(1008, 400))

    for i, (key, check) in enumerate((("issue", "membership check"), ("dispatch", "assignment check"),
                                      ("notification", "inbox owner check"))):
        x = 1145 + 220 * i
        d.box(key, x, 640, 210, 84, [key, "validates the JWT", check])
        cx = x + 105
        route = f"/api/{'notifications' if key == 'notification' else key}/*"
        path = [(1470, 310), (1470, 640)] if cx == 1470 else [(1470, 310), (1470, 605), (cx, 605), (cx, 640)]
        d.edge(path, route, at=(cx + 8, 624))

    d.note(420, 585, ["/status/api exists only if spike item 11 shows that",
                      "Gatus strips hosts, URLs and errors from its JSON;",
                      "it must win over /status, rule priority to confirm",
                      "in the spike (ADR-004, ADR-012)."], attach=d.p("gatus", "s"))
    d.note(800, 585, ["Traefik Proxy has no JWT middleware: each",
                      "Spring service is an OAuth2 resource server,",
                      "authorises against its own data and answers",
                      "404 outside the caller's scope (ADR-005)."], attach=d.p("issue", "w"))
    return d


def p3():
    d = Diagram("p3-messaging", "P3 Messaging through RabbitMQ", 1880, 790)
    d.pool(20, 20, 1840, "Messaging through RabbitMQ · topology of ADR-003",
           [("Publishers", 170), ("rabbitmq\none node · one user per service", 380),
            ("Consumers\nmanual acknowledgement", 200)])

    cols = [260, 550, 840, 1130]
    d.box("pa", 140, 55, 240, 100, ["ai-triage-consumer", "TriageSuggested", "publishes, then acknowledges"])
    d.box("pi", 430, 55, 240, 100, ["issue", "TriageRequested", "IssueStateChanged · Membership*",
                                    "outbox · publisher confirms"])
    d.box("pd", 720, 55, 240, 100, ["dispatch", "intervention and booking events", "NotificationRequested",
                                    "outbox · publisher confirms"])
    d.note(1020, 62, ["Outbox rows wait as pending while the broker is",
                      "down; the publisher retries with backoff (2 s",
                      "doubling, cap 5 min) without limit."], attach=d.p("pd", "e"))

    d.diamond("ex", 550, 250)
    d.text(590, 300, ["bmc.events · durable topic exchange", "routing key <producer>.<eventType>"])
    d.edge([(260, 155), (260, 250), (521, 250)], "publish", at=(268, 215))
    d.edge([(550, 155), (550, 221)], "publish", at=(558, 200))
    d.edge([(840, 155), (840, 250), (579, 250)], "publish", at=(848, 215))

    queues = [("qi", ["issue.inbox", "quorum · delivery limit 5"], "TriageSuggested, dispatch events"),
              ("qd", ["dispatch.inbox", "quorum · delivery limit 5"], "IssueStateChanged, Membership*"),
              ("qn", ["notification.inbox", "quorum · delivery limit 5"], "NotificationRequested"),
              ("qa", ["ai-triage.requests", "point to point · private text", "quorum · delivery limit 5"],
               "issue.TriageRequested only")]
    for cx, (key, lines, binding) in zip(cols, queues):
        d.box(key, cx - 130, 375, 260, 90, lines, icon="queue")
        d.edge([(550, 279), (550, 335), (cx, 335), (cx, 375)] if cx != 550 else [(550, 279), (550, 375)],
               binding, at=(cx + 8, 356))
        d.edge([(cx + 80, 465), (cx + 80, 515), (1400, 515), (1400, 449)], dashed=True)
    d.text(1320, 503, ["after 5 deliveries"], anchor="middle")

    d.diamond("dlx", 1400, 420)
    d.text(1400, 372, ["bmc.dlx · dead-letter exchange", "at-least-once"], anchor="middle")
    d.box("dlq", 1510, 375, 260, 90, ["<queue>.dlq", "one per queue · TTL 7 days", "replay by runbook (shovel)"],
          icon="queue")
    d.edge([(1429, 420), (1510, 420)], dashed=True)

    consumers = [("ci", ["issue", "TriageSuggested by issueVersion", "dispatch events by aggregateVersion",
                         "→ history and issue state"], "ack after commit"),
                 ("cd", ["dispatch", "IssueStateChanged, Membership*", "by aggregateVersion",
                         "→ local projections"], "ack after commit"),
                 ("cn", ["notification", "NotificationRequested", "→ in-app inbox and email"], "ack after commit"),
                 ("ca", ["ai-triage-consumer", "TriageRequested → rules, provider", "stateless: a duplicate",
                         "is classified again"], "ack after publishing")]
    for cx, (key, lines, ack) in zip(cols, consumers):
        d.box(key, cx - 130, 610, 260, 110, lines)
        d.edge([(cx, 465), (cx, 610)], ack, at=(cx + 8, 590))

    d.note(1430, 600, ["TriageRequested is the only message with",
                       "private report text: bound only to",
                       "ai-triage.requests, never logged; its DLQ",
                       "copy expires after 7 days (ADR-003, 008)."], attach=(1240, 465))
    d.note(1430, 700, ["The Spring consumers keep processed event IDs,", "so a duplicate is acknowledged without", "repeating the effect (ADR-003)."])
    return d


def p4():
    d = Diagram("p4-data-and-platform", "P4 Data stores and platform connections", 1880, 640)
    d.pool(20, 20, 1840, "Data stores and platform connections · arrows from client to server",
           [("Platform\ncomponents", 170), ("Services\nown database only", 180), ("Data stores", 250)])

    d.box("sim", 140, 55, 220, 90, ["calendar-sim", "HTTP · Idempotency-Key", "in memory"])
    d.box("mailpit", 380, 55, 220, 90, ["mailpit", "SMTP capture", "demo only"])
    d.box("keycloak", 680, 55, 220, 90, ["keycloak", "accounts and credentials", "sends account email"])

    d.box("dispatch", 140, 230, 220, 96, ["dispatch", "interventions · bookings", "contractors"])
    d.box("notification", 380, 230, 220, 96, ["notification", "inbox · preferences", "delivery log"])
    d.box("issue", 960, 230, 320, 96, ["issue", "reports · issues · memberships", "attachments"])
    d.box("backup", 1370, 230, 220, 96, ["backup job", "container and schedule", "not placed (P-03)"],
          icon="gear", dashed=True)

    d.group(120, 400, 980, 170, "mysql · MySQL 8.4 LTS · one instance")
    for x, owner in ((150, "dispatch"), (390, "notification"), (630, "keycloak"), (870, "issue")):
        d.box("db-" + owner, x, 460, 200, 90, [owner, "database", "owner: " + owner], icon="db")
    d.group(1130, 400, 480, 170, "garage · Garage 2.5 · S3 subset")
    d.box("ba", 1140, 460, 220, 90, ["bmc-attachments", "report photos", "candidate, post-MVP"], icon="bucket")
    d.box("bb", 1380, 460, 220, 90, ["bmc-backups", "MySQL dumps"], icon="bucket")

    d.edge([(250, 230), (250, 145)], "HTTP", at=(258, 170))
    d.edge([(490, 230), (490, 145)], "SMTP", at=(498, 170))
    d.edge([(680, 100), (600, 100)], "SMTP", at=(640, 88), anchor="middle")
    d.edge([(600, 280), (800, 280), (800, 145)], "Admin API · view-users", at=(700, 268),
           anchor="middle", dashed=True)
    d.edge([(860, 145), (860, 430), (730, 430), (730, 460)], "JDBC", at=(868, 380))
    d.edge([(250, 326), (250, 460)], "JDBC", at=(258, 390))
    d.edge([(490, 326), (490, 460)], "JDBC", at=(498, 390))
    d.edge([(990, 326), (990, 460)], "JDBC", at=(998, 390))
    d.edge([(1240, 326), (1240, 460)], "S3", at=(1248, 390))
    d.edge([(1480, 326), (1480, 460)], "write dumps", at=(1488, 390), dashed=True)
    d.edge([(1590, 280), (1700, 280), (1700, 596), (610, 596), (610, 570)], "dump · placement open",
           at=(1150, 596), anchor="middle", dashed=True)

    d.note(1000, 52, ["Every Spring service also needs Keycloak's signing keys;",
                      "that connection is not drawn and its route is open (P-05).",
                      "Calls to a platform component or to the calendar are not",
                      "service-to-service calls (ADR-001)."], attach=d.p("keycloak", "e", 0.4))
    return d


def p5():
    d = Diagram("p5-health-and-metrics", "P5 Health, metrics and logs", 1700, 680)
    d.pool(20, 20, 1660, "Health, metrics and the public status page · ADR-004, ADR-012",
           [("Readers", 150), ("Edge and\nobservability", 200), ("Checked\ntargets", 290)])

    d.box("public", 140, 45, 220, 84, ["Public /status page", "and role-filtered banner", "client page, no login"],
          icon="device")
    d.box("operator", 1190, 45, 220, 84, ["Operator", "reads the dashboard"], icon="person")
    d.note(470, 40, ["Public capabilities: Report a fault, Schedule interventions,",
                     "Notifications, Suggestions, Calendar sync, Sign-in, Photo",
                     "upload; infrastructure is never listed by name (ADR-012)."],
           attach=(600, 230))

    d.box("traefik", 140, 230, 220, 84, ["traefik", "health check", "before routing"])
    d.box("gatus", 490, 230, 220, 84, ["gatus", "capability checks", "results kept 30 days"])
    d.box("prom", 840, 230, 220, 84, ["prometheus", "scrapes /metrics", "alerts"])
    d.box("grafana", 1190, 230, 220, 84, ["grafana", "operator dashboard"])

    d.box("bmc", 140, 420, 440, 116, ["BMC services · readiness covers own database",
                                      "issue, dispatch, notification: Actuator",
                                      "readiness, Micrometer /metrics",
                                      "ai-triage-web: Flask health route,",
                                      "prometheus_client /metrics"], icon="doc")
    d.box("plat", 760, 420, 440, 180, ["Platform checks · rolled up into capabilities",
                                       "oauth2-proxy: /ready, /metrics",
                                       "rabbitmq: diagnostics ping, metrics plugin",
                                       "keycloak: /health/ready on port 9000",
                                       "mysql: query-level check",
                                       "garage: admin GET /health",
                                       "mailpit: readyz",
                                       "calendar-sim: calendar sync capability"], icon="doc")

    d.edge([(250, 129), (250, 230)], "GET /status/api", at=(258, 152))
    d.edge([(360, 272), (490, 272)], "/status/api", at=(425, 260), anchor="middle")
    d.edge([(1300, 129), (1300, 230)], "access in demo: open", at=(1308, 152), dashed=True)
    d.edge([(1190, 272), (1060, 272)], "queries", at=(1125, 260), anchor="middle")
    d.edge([(840, 272), (710, 272)], "scrape", at=(775, 260), anchor="middle")
    d.edge([(950, 230), (950, 198), (316, 198), (316, 230)], "scrape · network open (P-01)",
           at=(830, 198), anchor="middle", dashed=True)
    d.edge([(250, 314), (250, 420)], "readiness of issue,\ndispatch, notification", at=(258, 342))
    d.edge([(540, 314), (540, 420)], "readiness", at=(548, 340))
    d.edge([(680, 314), (680, 390), (800, 390), (800, 420)], "platform checks", at=(688, 340))
    d.edge([(880, 314), (880, 405), (450, 405), (450, 420)], "scrape /metrics", at=(888, 340))
    d.edge([(990, 314), (990, 420)], "scrape oauth2-proxy,\nrabbitmq", at=(998, 342))

    d.note(1250, 440, ["Logs are structured with correlationId and",
                       "traceparent; where they are collected is",
                       "left to DEVOPS-02 (EN01-U12), so no log",
                       "collector is drawn."])
    return d


def p6():
    d = Diagram("p6-delivery-path", "P6 Environments and delivery path", 1800, 700)
    d.pool(20, 20, 1760, "Proposed delivery path · ADR-004, PR #40 (open) · no pipeline, image or host exists yet",
           [("Developer\nlaptop", 140), ("GitHub", 240), ("Demonstration\nhost", 280)])

    d.event("start", 150, 90, "Commit on a\nfeature branch")
    d.box("push", 230, 55, 220, 70, ["Push the branch", "open a pull request"],
          icon="person")
    d.note(500, 50, ["The laptop runs the same compose.yaml with a smaller", "set of profiles (ADR-004)."])

    d.box("repo", 120, 235, 210, 90, ["Repository", "feature/* → dev → main", "release: protected v* tag"])
    d.group(370, 200, 1080, 160, "GitHub Actions · proposed stages")
    stages = [["Lint and", "unit tests"], ["Contract checks", "buf lint, buf breaking"],
              ["Boundary tests", "ArchUnit, import-linter,", "ESLint"],
              ["Integration tests", "real MySQL 8.4", "and RabbitMQ"],
              ["Multi-arch build", "amd64 and arm64", "method open (EN01-U9)"]]
    for i, lines in enumerate(stages):
        d.box(f"s{i}", 390 + 210 * i, 240, 190, 90, lines, icon="gear")
        if i:
            d.edge([(390 + 210 * i - 20, 285), (390 + 210 * i, 285)])
    d.box("ghcr", 1530, 240, 220, 90, ["GHCR", "one image per app", "built once, promoted by tag"],
          icon="cloud")

    d.edge([(170, 90), (230, 90)])
    d.edge([(340, 125), (340, 180), (225, 180), (225, 235)], "push", at=(290, 168), anchor="middle")
    d.edge([(330, 285), (390, 285)])
    d.edge([(1420, 285), (1530, 285)], "push tagged\nimages", at=(1488, 252), anchor="middle")

    d.box("pull", 1530, 450, 220, 80, ["docker compose pull", "the same image, by tag"], icon="gear")
    d.box("up", 1170, 450, 230, 80, ["docker compose up -d", "rollback: previous tag"], icon="gear")
    d.event("run", 1000, 490, "Release running", end=True)
    d.box("env", 1170, 580, 230, 70, ["Host or CI environment", ".env with secrets, never in Git"], icon="doc")

    d.edge([(1640, 330), (1640, 450)])
    d.edge([(1530, 490), (1400, 490)])
    d.edge([(1170, 490), (1020, 490)])
    d.edge([(1285, 580), (1285, 530)], "injected at deploy", at=(1293, 560))

    d.note(470, 420, ["Multi-arch availability is recorded for the Traefik, RabbitMQ,",
                      "MySQL, Mailpit, Temurin and python images, not yet for",
                      "Keycloak, oauth2-proxy, Garage, Prometheus, Grafana or nginx",
                      "(spike item 8, ADR-004)."], attach=d.p("s4", "s"))
    d.note(1050, 50, ["Required checks are configured only when", "the pipeline exists (ADR-004)."])
    return d


def p7():
    d = Diagram("p7-compose-profiles", "P7 Compose profiles and rollout", 1520, 640)
    d.pool(20, 20, 1480, "Compose profiles in the proposed rollout order · ADR-004",
           [("First\nprofile core", 200), ("When the slice\nneeds it", 200), ("Later\nown profiles", 200)])

    d.event("start", 160, 120, "First vertical\nslice")
    d.group(240, 45, 790, 150, "core · eight containers")
    for i, lines in enumerate((["edge and sign-in", "traefik · oauth2-proxy", "keycloak"],
                               ["data and messaging", "mysql · rabbitmq"],
                               ["business and client", "issue · dispatch", "client"])):
        d.box(f"c{i}", 260 + 255 * i, 80, 240, 96, lines)

    d.group(240, 245, 790, 150, "no profile name yet")
    for i, lines in enumerate((["AI triage", "ai-triage-web", "ai-triage-consumer", "reporting works without them"],
                               ["notification", "as soon as US-10 is", "in the slice"],
                               ["calendar-sim", "when dispatch", "books a visit"])):
        d.box(f"l{i}", 260 + 255 * i, 280, 240, 100, lines)

    d.group(240, 445, 1045, 170, "own profiles · storage and status are proposed names")
    for i, lines in enumerate((["demo", "mailpit, synthetic", "realm users"],
                               ["status", "gatus, /status page", "and banner"],
                               ["observability", "prometheus, grafana"],
                               ["storage", "garage, before the backup", "and restore exercise"])):
        d.box(f"x{i}", 260 + 255 * i, 485, 240, 100, lines)
    d.event("end", 1380, 530, "All seventeen\ncontainers", end=True)

    d.edge([(180, 120), (240, 120)])
    d.edge([(635, 195), (635, 245)], "then", at=(643, 233))
    d.edge([(635, 395), (635, 445)], "then", at=(643, 433))
    d.edge([(1285, 530), (1360, 530)])

    d.note(1100, 260, ["A proposal to decide at the team review", "(EN01-U1). Memory of each set is not", "measured (EN01-U3, spike item 8)."])
    return d


VIEWS = [p1, p2, p3, p4, p5, p6, p7]


def render_png(svg_path, width, height):
    chrome = os.environ.get("CHROME", "chrome-headless-shell")
    subprocess.run([chrome, "--headless", "--hide-scrollbars", "--force-device-scale-factor=2",
                    f"--window-size={width},{height}", f"--screenshot={svg_path.with_suffix('.png')}",
                    svg_path.as_uri()], check=True, capture_output=True)


if __name__ == "__main__":
    for view in VIEWS:
        diagram = view()
        out = HERE / f"{diagram.name}.svg"
        out.write_text(diagram.svg(), encoding="utf-8")
        if "--png" in sys.argv:
            render_png(out, diagram.width, diagram.height)
        print(out.name)
