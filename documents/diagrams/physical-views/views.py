"""The seven BMC physical views as UML deployment diagrams, drawn with vpdraw.

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

from vpdraw import BLUE, Diagram

HERE = Path(__file__).resolve().parent
SPRING = "Spring Boot 4.1.2 · Java 25"


def p1():
    d = Diagram("p1-deployment-overview", "P1 · Deployment overview",
                "UML deployment diagram of the proposed BMC stack · ADR-004 · proposed, nothing is deployed",
                1900, 1360)
    d.node("device", 40, 90, 420, 210, "User device", "device", ["phone or computer"])
    d.node("browser", 70, 165, 360, 120, "Browser or installed PWA", "executionEnvironment", align="left")
    d.comp("web", 95, 215, 310, 62, "BMC web app", "component", ["React + Vite build"])
    d.node("github", 1480, 90, 380, 210, "GitHub", None, ["github.com"])
    d.comp("ghcr", 1510, 160, 320, 80, "GitHub Container Registry", "external service",
           ["one multi-arch image per app"])

    d.node("host", 40, 350, 1820, 830, "Demonstration host", "device",
           ["one Docker host · Docker Engine + Compose · fifteen services · linux/amd64 or linux/arm64 · "
            "host choice open (EN01-U3)"])
    d.node("n1", 70, 430, 1080, 200, "edge network only", "network", align="left")
    d.comp("traefik", 180, 490, 240, 85, "traefik", "container", ["Traefik 3.7", "only published ports: 80, 443"])
    d.comp("client", 520, 490, 240, 85, "client", "container", ["nginx", "serves the React build"])
    d.comp("o2p", 860, 490, 240, 85, "oauth2-proxy", "container", ["oauth2-proxy 7.15", "browser session (BFF)"])
    d.lollipop(300, 468, "HTTPS 443", (300, 490))
    d.dep([(300, 277), (300, 459)], "uses", at=(308, 320))
    d.path([(420, 532), (520, 532)], "/", at=(470, 520), anchor="middle", bg=BLUE)
    d.path([(372, 575), (372, 600), (980, 600), (980, 575)], "/oauth2/*", at=(676, 600), anchor="middle", bg=BLUE)

    d.node("n2", 70, 680, 1500, 175, "edge + internal networks", "network", align="left")
    routed = [("issue", ["issue", SPRING, "reports, issues, memberships"], "/api/issue/*"),
              ("notification", ["notification", SPRING, "in-app inbox, email"], "/api/notifications/*"),
              ("keycloak", ["keycloak", "Keycloak 26.8", "sign-in and accounts"], "/auth/*"),
              ("dispatch", ["dispatch", SPRING, "also on egress"], "/api/dispatch/*")]
    for i, (key, (name, *details), route) in enumerate(routed):
        x = 345 + 250 * i
        d.comp(key, x, 740, 220, 85, name, "container", details)
        d.path([(300, 575), (300, 660), (x + 110, 660), (x + 110, 740)], route, at=(x + 118, 722), bg=BLUE)

    d.node("n3", 70, 900, 1500, 250, "internal network only", "network", align="left")
    for key, x, name, details in (
            ("sim", 95, "calendar-sim", ["Spring Boot · Java 25", "tests, offline, failure demos"]),
            ("mailpit", 345, "mailpit", ["Mailpit 1.32", "SMTP capture · demo inbox"]),
            ("grafana", 595, "grafana", ["Grafana 13", "operator dashboard"]),
            ("prom", 845, "prometheus", ["Prometheus 3.x", "metrics and alerts"]),
            ("ai", 1095, "ai-triage", ["Python 3.14 · web + consumer", "also on egress"])):
        d.comp(key, x, 955, 220, 85, name, "container", details)
    for key, x, name, details, icon in (
            ("rabbitmq", 95, "rabbitmq", ["RabbitMQ 4.x", "quorum queues, DLQs"], "component"),
            ("mysql", 345, "mysql", ["MySQL 8.4 LTS", "one database per service"], "database"),
            ("garage", 595, "garage", ["Garage 2.5 · single node", "attachments, backups"], "component")):
        d.comp(key, x, 1050, 220, 85, name, "container", details, icon=icon)

    d.node("egress", 1610, 780, 220, 95, "egress", "network", ["the only way out"])
    d.path([(1315, 782), (1610, 782)], "HTTPS", at=(1460, 770), anchor="middle", bg=BLUE)
    d.path([(1315, 997), (1720, 997), (1720, 875)], "HTTPS", at=(1515, 985), anchor="middle", bg=BLUE)

    d.node("gcal", 1380, 1230, 220, 90, "Google Calendar API", "external system", ["live calendar", "(ADR-006)"])
    d.node("aiprov", 1630, 1230, 220, 90, "AI provider API", "external system", ["candidate: Gemini Flash", "(DEC-05)"])
    d.node("r2", 700, 1230, 220, 90, "Cloudflare R2", "external system", ["optional off-host copy,", "not in the release"],
           dashed=True)
    d.path([(1650, 875), (1650, 1200), (1490, 1200), (1490, 1230)], "Google Calendar API",
           at=(1500, 1188), anchor="start")
    d.path([(1790, 875), (1790, 1230)], "classifies report text", at=(1782, 1198), anchor="end")
    d.path([(790, 1135), (790, 1230)], "S3 · optional copy", at=(798, 1198), dashed=True)
    d.path([(1670, 240), (1670, 350)], "image pull · HTTPS", at=(1678, 318))

    d.note(1200, 450, 330, ["ADR-004: keycloak joins edge for /auth/*", "and internal for its MySQL database."],
           attach=d.p("keycloak", "n"))
    d.note(860, 1052, 290, ["Open (P-01): prometheus is on internal", "only, yet ADR-004 has it scrape",
                            "traefik and oauth2-proxy, on edge only."], attach=d.p("prom", "s"))
    d.note(1180, 1052, 380, ["Connections from the services to the broker,",
                             "databases, storage, mail and the calendar",
                             "simulator are drawn in P3 and P4."])
    d.note(1600, 655, 250, ["No allow-list proxy on egress", "for the MVP (open, EN-01-04)."],
           attach=d.p("egress", "n"))
    d.legend(40, 1225)
    return d


def p2():
    d = Diagram("p2-edge-and-trust", "P2 · Edge routing and trust boundaries",
                "UML deployment diagram of the edge · routes from ADR-004, authorisation from ADR-005 · proposed",
                1900, 1100)
    d.node("device", 250, 80, 520, 180, "User device", "device", ["browser or installed PWA"])
    d.comp("web", 420, 150, 300, 70, "BMC web app", "component", ["one origin, no CORS"])

    d.node("host", 40, 320, 1820, 670, "Demonstration host", "device", ["Docker host"])
    d.boundary("tb1", 70, 385, 1330, 260, "Trust boundary 1 · internet → traefik")
    d.holder("traefik", 95, 425, 1280, 185, "traefik", "container",
             ["Traefik 3.7 · the only published ports, 80 and 443"])
    d.lollipop(570, 407, "HTTPS 443", (570, 425))
    d.dep([(570, 220), (570, 398)], "uses", at=(578, 290))
    d.comp("router", 460, 445, 220, 95, "Router", "entrypoint", ["TLS terminates here;", "matches the route rules"])
    d.comp("fa", 790, 445, 220, 95, "ForwardAuth", "middleware", ["/api/* only: asks oauth2-proxy;",
                                                                  "no session → 401"])
    d.comp("strip", 1132, 445, 220, 95, "StripPrefix", "middleware", ["removes /api/<service>;",
                                                                      "then RateLimit, Headers"])
    d.dep([(680, 492), (790, 492)], "/api/*", at=(735, 480), anchor="middle", bg=BLUE)
    d.dep([(1010, 492), (1132, 492)], "session valid", at=(1071, 480), anchor="middle", bg=BLUE)
    d.note(1420, 385, 420, ["Never routed: no Traefik rule (ADR-004)", "Traefik API and dashboard",
                            "liveness, readiness, Actuator, /metrics", "AI /classify · simulator control",
                            "RabbitMQ management, Garage", "Mailpit UI (SSH tunnel in demos)",
                            "Open: Keycloak paths kept unrouted,", "how Grafana is reached in demo"])

    d.boundary("public", 70, 690, 1030, 240, "Public routes · no ForwardAuth, no API session")
    for key, x, w, name, details, route, drop in (
            ("client", 95, 240, "client", ["nginx", "static files"], "/", 215),
            ("keycloak", 375, 240, "keycloak", ["Keycloak 26.8", "sign-in pages"], "/auth/*", 495),
            ("o2p", 655, 300, "oauth2-proxy", ["oauth2-proxy 7.15", "Authorization: Bearer <access token>"],
             "/oauth2/*", 715)):
        d.comp(key, x, 745, w, 95, name, "container", details)
        d.path([(570, 540), (570, 665), (drop, 665), (drop, 745)], route, at=(drop + 8, 727), bg=BLUE)
    d.lollipop(900, 722, "session check", (900, 745))
    d.dep([(900, 540), (900, 713)], "asks", at=(908, 668), bg=BLUE)

    d.boundary("tb2", 1110, 690, 730, 240, "Trust boundary 2 · inside each service")
    for i, (key, check) in enumerate((("issue", "membership check"), ("dispatch", "assignment check"),
                                      ("notification", "inbox owner check"))):
        x = 1130 + 240 * i
        cx = x + 112
        d.comp(key, x, 745, 225, 95, key, "container", ["Spring Boot", "validates the JWT;", check])
        route = f"/api/{'notifications' if key == 'notification' else key}/*"
        d.path([(1242, 540), (1242, 665), (cx, 665), (cx, 745)] if cx != 1242 else [(1242, 540), (1242, 745)],
               route, at=(cx + 8, 727), bg=BLUE)

    d.note(200, 1010, 560, ["oauth2-proxy builds Authorization from the access_token claim",
                            "(injectResponseHeaders, prefix \"Bearer \"); --set-authorization-header",
                            "would send the ID token (E86). Audience checked in spike item 3."],
           attach=d.p("o2p", "s"))
    d.note(1130, 1010, 520, ["Traefik Proxy has no JWT middleware: each Spring service is an",
                             "OAuth2 resource server, authorises against its own data and",
                             "answers 404 outside the caller's scope (ADR-005)."],
           attach=d.p("issue", "s"))
    return d


def p3():
    d = Diagram("p3-messaging", "P3 · Messaging through RabbitMQ",
                "UML deployment diagram of the broker · topology from ADR-003 · arrows follow the message · proposed",
                1900, 920)
    d.node("host", 40, 80, 1820, 810, "Demonstration host", "device", ["Docker host · internal network"])
    cols = [330, 680, 1030, 1380]
    services = [("issue", "issue", [SPRING, "outbox publisher;", "idempotent consumer"]),
                ("dispatch", "dispatch", [SPRING, "outbox publisher;", "idempotent consumer"]),
                ("notification", "notification", [SPRING, "idempotent consumer"]),
                ("ai", "ai-triage", ["Python 3.14 · consumer process", "stateless: classifies, publishes,",
                                     "acks after the confirm"])]
    for cx, (key, name, details) in zip(cols, services):
        d.comp(key, cx - 140, 150, 280, 100, name, "container", details)

    d.holder("rabbitmq", 95, 330, 1740, 520, "rabbitmq", "container",
             ["RabbitMQ 4.x · one node · one broker user per service (ADR-005)"])
    d.lollipop(1710, 307, "AMQP", (1710, 330))
    d.comp("ex", 200, 610, 1300, 62, "bmc.events", "exchange",
           ["durable topic exchange · routing key <producer>.<eventType> · topic permissions per producer prefix"])
    queues = [("qi", "issue.inbox", ["quorum · delivery limit 5"], "TriageSuggested,\ndispatch events",
               "ack after commit"),
              ("qd", "dispatch.inbox", ["quorum · delivery limit 5"], "IssueStateChanged,\nMembership*",
               "ack after commit"),
              ("qn", "notification.inbox", ["quorum · delivery limit 5"], "NotificationRequested", "ack after commit"),
              ("qa", "ai-triage.requests", ["quorum · delivery limit 5", "point to point, private text"],
               "issue.TriageRequested\nonly", "ack after confirmed reply")]
    for cx, (key, name, details, binding, ack) in zip(cols, queues):
        d.comp(key, cx - 105, 410, 210, 90, name, "queue", details)
        d.dep([(cx, 610), (cx, 500)], binding, at=(cx + 8, 545), bg=BLUE)
        d.dep([(cx, 410), (cx, 250)], f"delivers\n{ack}", at=(cx + 8, 280), bg=BLUE)
        if key != "qn":  # whether Notification publishes events is not stated (ADR-007)
            d.dep([(cx - 125, 250), (cx - 125, 610)], "publishes\nmandatory, confirms",
                  at=(cx - 133, 368), anchor="end", bg=BLUE)

    d.comp("dlx", 1600, 410, 220, 90, "bmc.dlx", "exchange", ["dead-letter · at-least-once"])
    d.comp("dlq", 1600, 570, 220, 100, "<queue>.dlq", "queue", ["one per queue", "TTL 7 days (DLQ only)",
                                                                "replay by runbook"])
    d.dep([(1485, 455), (1600, 455)], "after 5 deliveries\n(every queue)", at=(1542, 420), anchor="middle", bg=BLUE)
    d.dep([(1710, 500), (1710, 570)], "routes", at=(1718, 535), bg=BLUE)

    d.note(170, 705, 470, ["Outbox rows wait as pending while the broker is down.",
                           "A row is marked sent only on a positive confirm with no",
                           "return; queues and bindings are declared by the",
                           "deployment before any publisher starts (E84)."], attach=(205, 510))
    d.note(665, 705, 440, ["The Spring consumers keep processed event IDs,",
                           "so a duplicate is acknowledged without",
                           "repeating the effect. Consumers reject an",
                           "envelope whose producer does not match the key."])
    d.note(1130, 705, 460, ["TriageRequested is the only message with private",
                            "report text: bound only to ai-triage.requests, never",
                            "logged. Its DLQ copy expires after 7 days; live-queue",
                            "and outbox retention are not set yet (EN01-U6)."], attach=(1380, 672))
    return d


def p4():
    d = Diagram("p4-data-and-platform", "P4 · Data stores and platform connections",
                "UML deployment diagram of stores and platform calls · ADR-001, ADR-004, ADR-006, ADR-010 · arrows "
                "from user to used · proposed", 1900, 950)
    d.node("gcal", 140, 80, 260, 85, "Google Calendar API", "external system", ["live calendar, over egress"])
    d.node("host", 40, 200, 1820, 720, "Demonstration host", "device", ["Docker host · internal network"])

    d.comp("sim", 140, 270, 220, 90, "calendar-sim", "container", ["tests, offline and", "failure demos"])
    d.comp("mailpit", 380, 270, 220, 90, "mailpit", "container", ["Mailpit 1.32 · core profile", "inbox via SSH tunnel"])
    d.comp("keycloak", 680, 270, 220, 90, "keycloak", "container", ["Keycloak 26.8", "accounts, account email"])
    d.lollipop(250, 382, "HTTP API", (250, 360))
    d.lollipop(490, 382, "SMTP", (490, 360), at="w")
    d.lollipop(800, 382, "Admin API", (800, 360), at="w")

    d.comp("dispatch", 140, 460, 220, 100, "dispatch", "container", ["CalendarPort: Google", "or simulator (config)"])
    d.comp("notification", 380, 460, 220, 100, "notification", "container", ["Spring Boot", "inbox, delivery log"])
    d.comp("issue", 960, 460, 320, 100, "issue", "container", ["Spring Boot",
                                                               "reports, issues, memberships, attachments"])
    d.comp("backup", 1370, 460, 220, 100, "nightly backup", "cron job", ["on the host, not a container",
                                                                         "mysqldump of each database"])

    d.holder("mysql", 120, 640, 980, 200, "mysql", "container",
             ["MySQL 8.4 LTS · one instance, one database per service · scales vertically"])
    for x, owner in ((150, "dispatch"), (390, "notification"), (630, "keycloak"), (870, "issue")):
        d.comp("db-" + owner, x, 660, 200, 100, owner, "database", ["owner: " + owner], icon="database")
    d.holder("garage", 1130, 640, 480, 200, "garage", "container", ["Garage 2.5 · S3 subset · single node"])
    d.lollipop(1240, 617, "S3 API", (1240, 640), at="w")
    d.comp("ba", 1150, 660, 210, 100, "bmc-attachments", "bucket", ["report photos;", "candidate, post-MVP"],
           icon="artifact")
    d.comp("bb", 1380, 660, 210, 100, "bmc-backups", "bucket", ["nightly dumps"], icon="artifact")

    d.dep([(140, 510), (110, 510), (110, 122), (140, 122)], "HTTPS", at=(102, 300), anchor="end")
    d.dep([(250, 460), (250, 391)], "tests, failure\ndemos", at=(258, 412), bg=BLUE)
    d.dep([(490, 460), (490, 391)], "sends email", at=(498, 425), bg=BLUE)
    d.dep([(700, 360), (700, 382), (499, 382)])
    d.dep([(600, 510), (800, 510), (800, 391)], "Admin API · view-users", at=(700, 498), anchor="middle", bg=BLUE)
    d.dep([(860, 360), (860, 625), (730, 625), (730, 660)], "JDBC", at=(868, 580), bg=BLUE)
    d.dep([(250, 560), (250, 660)], "JDBC", at=(258, 608), bg=BLUE)
    d.dep([(490, 560), (490, 660)], "JDBC", at=(498, 608), bg=BLUE)
    d.dep([(990, 560), (990, 660)], "JDBC", at=(998, 608), bg=BLUE)
    d.dep([(1240, 560), (1240, 608)], "stores photos", at=(1248, 582), bg=BLUE)
    d.dep([(1480, 560), (1480, 617), (1249, 617)], "writes dumps", at=(1488, 586), bg=BLUE)
    d.dep([(1590, 510), (1700, 510), (1700, 885), (610, 885), (610, 840)],
          "mysqldump · read-only backup user", at=(1150, 885), anchor="middle", bg=BLUE)

    d.note(1000, 262, 560, ["Every Spring service also needs Keycloak's signing keys; that",
                            "connection is not drawn and its route is open (P-05). Calls to a",
                            "platform component or to the calendar are not service-to-service",
                            "calls (ADR-001)."], attach=d.p("keycloak", "e", 0.4))
    d.note(430, 92, 560, ["Google Calendar does not guarantee that event-ID collisions are",
                          "detected at creation (E87), so Dispatch still queries by ID",
                          "before any re-send (reconcile before retry)."], attach=(400, 122))
    return d


def p5():
    d = Diagram("p5-health-and-metrics", "P5 · Health, metrics and logs",
                "UML deployment diagram of health and metrics paths for the MVP · ADR-004, ADR-012 · proposed",
                1720, 930)
    d.actor("operator", 1010, 60, "Operator", ["reads the dashboard"])
    d.note(1120, 70, 560, ["Deferred past the MVP: the public /status page, the /status/api",
                           "route and the status banner, which relied on Gatus (ADR-012).",
                           "Users still see degraded states in context: booking pending,",
                           "\"triage pending — classify manually\", delayed email."])

    d.node("host", 40, 220, 1640, 550, "Demonstration host", "device", ["Docker host"])
    d.comp("traefik", 255, 345, 230, 90, "traefik", "container", ["Traefik 3.7", "health check before routing"])
    d.comp("prom", 575, 345, 230, 90, "prometheus", "container", ["Prometheus 3.x", "scrapes /metrics, alerts on up"])
    d.comp("grafana", 895, 345, 230, 90, "grafana", "container", ["Grafana 13", "operator dashboard (§6.7)"])
    d.comp("bbx", 1265, 345, 230, 90, "blackbox_exporter", "container", ["only if readiness must", "be probed directly"],
           dashed=True)

    d.path([(1010, 166), (1010, 345)], "access in demo: open", at=(1018, 192), dashed=True)
    d.dep([(895, 390), (805, 390)], "queries", at=(850, 378), anchor="middle", bg=BLUE)
    d.dep([(575, 390), (485, 390)], "scrape (P-01)", at=(530, 378), anchor="middle", bg=BLUE)
    d.dep([(750, 345), (750, 318), (1380, 318), (1380, 345)], "probes, only if needed", at=(1200, 318),
          anchor="middle", bg=BLUE)

    d.boundary("bmc", 70, 510, 560, 210, "BMC services · readiness covers own database")
    for x, y, name, check in ((85, 525, "issue", "Actuator readiness · /metrics"),
                              (355, 525, "dispatch", "Actuator readiness · /metrics"),
                              (85, 600, "notification", "Actuator readiness · /metrics"),
                              (355, 600, "ai-triage", "Flask health · /metrics")):
        d.comp(name, x, y, 260, 62, name, "container", [check])
    d.boundary("plat", 660, 510, 990, 210, "Platform checks · Compose health checks")
    for i, (name, check) in enumerate((("oauth2-proxy", "/ready · /metrics (P-01)"),
                                       ("rabbitmq", "diagnostics ping · metrics plugin"),
                                       ("keycloak", "/health/ready, port 9000"), ("mysql", "mysqladmin ping"),
                                       ("garage", "admin GET /health"), ("mailpit", "readyz"),
                                       ("calendar-sim", "no health check stated (P-04)"))):
        d.comp("t-" + name, 675 + 240 * (i % 4), 525 + 75 * (i // 4), 230, 62, name, "container", [check])

    d.dep([(370, 435), (370, 510)], "readiness of issue,\ndispatch, notification", at=(378, 458), bg=BLUE)
    d.dep([(640, 435), (640, 490), (600, 490), (600, 510)], "/metrics", at=(648, 458), bg=BLUE)
    d.dep([(740, 435), (740, 510)], "/metrics of rabbitmq,\noauth2-proxy", at=(748, 458), bg=BLUE)

    d.note(70, 790, 760, ["Every container should have a Compose health check; startup order uses condition: service_healthy.",
                          "Open for client, calendar-sim and the ai-triage consumer process (P-04). Logs are structured with",
                          "correlationId and traceparent; where they are collected is left to DEVOPS-02 (EN01-U12)."])
    return d


def p6():
    d = Diagram("p6-delivery-path", "P6 · Environments and delivery path",
                "UML deployment diagram of the proposed delivery path · ADR-004, PR #40 (open) · no pipeline, image "
                "or host exists yet", 1900, 790)
    d.node("laptop", 40, 80, 300, 220, "Developer laptop", "device", ["Docker Engine + Compose"])
    d.comp("wc", 65, 160, 250, 80, "Working copy", "artifact", ["Git checkout, compose.yaml", "smaller profile set"],
           icon="artifact")

    d.node("github", 380, 80, 1480, 400, "GitHub", None, ["github.com · DEVOPS-01 proposal, PR #40 (open)"])
    d.comp("repo", 405, 160, 230, 100, "Repository", "repository", ["Git · feature/* → dev → main",
                                                                    "release: protected v* tag"])
    d.node("actions", 670, 150, 890, 300, "GitHub Actions", "executionEnvironment",
           ["proposed stages, no pipeline yet"], align="left")
    stages = [("Lint, unit tests", []), ("Contract checks", ["buf lint,", "buf breaking"]),
              ("Boundary tests", ["ArchUnit,", "import-linter, ESLint"]),
              ("Integration tests", ["real MySQL 8.4", "and RabbitMQ"]),
              ("Multi-arch build", ["amd64, arm64;", "method open (EN01-U9)"])]
    for i, (name, details) in enumerate(stages):
        x = 690 + 175 * i
        d.comp(f"s{i}", x, 215, 155, 125, name, f"job {i + 1}", details)
        if i:
            d.dep([(x - 20, 277), (x, 277)])
    d.comp("ghcr", 1590, 160, 250, 100, "GHCR", "registry", ["one image per app;", "built once, promoted by tag"])

    d.node("host", 1100, 540, 760, 220, "Demonstration host", "device", ["Docker host"])
    d.comp("env", 1130, 610, 300, 110, "Host or CI environment", "artifact", [".env with secrets,", "never in Git"],
           icon="artifact")
    d.comp("stack", 1560, 610, 270, 110, "Docker Compose", "executionEnvironment",
           ["compose.yaml", "compose pull, then up -d;", "rollback: previous tag"])

    d.dep([(315, 200), (405, 200)], "push", at=(360, 188), anchor="middle")
    d.dep([(635, 250), (690, 250)], "runs", at=(662, 238), anchor="middle", bg=BLUE)
    d.dep([(1545, 250), (1590, 250)])
    d.path([(1715, 260), (1715, 610)], "pull the same image · HTTPS", at=(1723, 505))
    d.dep([(1560, 665), (1430, 665)], "reads at deploy", at=(1495, 653), anchor="middle", bg=BLUE)

    d.note(1000, 360, 540, ["Multi-arch availability is recorded for the Traefik, RabbitMQ,",
                            "MySQL, Mailpit, Temurin and python images, not yet for",
                            "Keycloak, oauth2-proxy, Garage, Prometheus, Grafana or nginx",
                            "(spike item 8, ADR-004)."], attach=d.p("s4", "s"))
    d.note(405, 300, 240, ["Required checks are configured", "only when the pipeline exists."])
    return d


def p7():
    d = Diagram("p7-compose-profiles", "P7 · Compose profiles and rollout",
                "UML deployment diagram of the Compose profile sets in the proposed order · ADR-004 · to decide at the "
                "team review (EN01-U1)", 1900, 640)
    d.node("host", 40, 80, 1820, 530, "Demonstration host", "device", ["one compose.yaml with profiles"])

    d.node("core", 70, 150, 540, 430, "First: profile core", "profile set", ["nine containers"])
    core = [("traefik", "Traefik 3.7"), ("oauth2-proxy", "oauth2-proxy 7.15"), ("keycloak", "Keycloak 26.8"),
            ("client", "nginx"), ("issue", "Spring Boot"), ("dispatch", "Spring Boot"),
            ("mysql", "MySQL 8.4 LTS"), ("rabbitmq", "RabbitMQ 4.x"), ("mailpit", "SMTP for Keycloak email")]
    for i, (name, version) in enumerate(core):
        d.comp("c-" + name, 85 + 260 * (i % 2), 210 + 70 * (i // 2), 245, 60, name, "container", [version],
               icon="database" if name == "mysql" else "component")

    d.node("slice", 670, 150, 540, 430, "When the slice needs it", "profile set", ["no profile name yet"])
    for i, (name, details) in enumerate((("ai-triage", ["web + consumer, one image;", "reporting works without it"]),
                                         ("notification", ["as soon as US-10", "is in the slice"]),
                                         ("calendar-sim", ["tests and failure demos", "of the calendar"]))):
        d.comp("l-" + name, 685 + 260 * (i % 2), 210 + 103 * (i // 2), 250, 92, name, "container", details)
    d.note(685, 425, 505, ["Memory of each set is not measured (EN01-U3, spike item 8)."])

    d.node("later", 1270, 150, 560, 430, "Later: own profiles", "profile set", ["observability, storage, demo"])
    for i, (name, profile, details) in enumerate((("prometheus", "profile observability", []),
                                                  ("grafana", "profile observability", []),
                                                  ("garage", "profile storage (proposed)",
                                                   ["before backup and restore"]))):
        d.comp("x-" + name, 1285 + 275 * (i % 2), 210 + 90 * (i // 2), 260, 80, name, "container",
               [profile] + details)
    d.note(1285, 405, 520, ["Profile demo adds only the synthetic realm users (ADR-005).",
                            "The status profile went with Gatus (ADR-012)."])

    d.dep([(610, 365), (670, 365)], "then", at=(640, 353), anchor="middle", bg=BLUE)
    d.dep([(1210, 365), (1270, 365)], "then", at=(1240, 353), anchor="middle", bg=BLUE)
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
