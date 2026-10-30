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
           ["one Docker host · Docker Engine + Compose · linux/amd64 or linux/arm64 · host choice open (EN01-U3)"])
    d.node("n1", 70, 430, 1080, 200, "edge network only", "network", align="left")
    d.comp("traefik", 180, 490, 240, 85, "traefik", "container", ["Traefik 3.7", "only published ports: 80, 443"])
    d.comp("client", 520, 490, 240, 85, "client", "container", ["nginx", "serves the React build"])
    d.comp("o2p", 860, 490, 240, 85, "oauth2-proxy", "container", ["oauth2-proxy 7.15", "browser session (BFF)"])
    d.lollipop(300, 468, "HTTPS 443", (300, 490))
    d.dep([(300, 277), (300, 459)], "uses", at=(308, 320))
    d.path([(420, 532), (520, 532)], "/, /status", at=(470, 520), anchor="middle", bg=BLUE)
    d.path([(372, 575), (372, 600), (980, 600), (980, 575)], "/oauth2/*", at=(676, 600), anchor="middle", bg=BLUE)

    d.node("n2", 70, 680, 1500, 175, "edge + internal networks", "network", align="left")
    routed = [("issue", ["issue", SPRING, "reports, issues, memberships"], "/api/issue/*"),
              ("dispatch", ["dispatch", SPRING, "interventions, bookings"], "/api/dispatch/*"),
              ("notification", ["notification", SPRING, "in-app inbox, email"], "/api/notifications/*"),
              ("keycloak", ["keycloak", "Keycloak 26.8", "sign-in and accounts"], "/auth/*"),
              ("gatus", ["gatus", "Gatus 5.37", "capability checks"], "/status/api")]
    for i, (key, (name, *details), route) in enumerate(routed):
        x = 345 + 250 * i
        d.comp(key, x, 740, 220, 85, name, "container", details)
        d.path([(300, 575), (300, 660), (x + 110, 660), (x + 110, 740)], route, at=(x + 118, 722), bg=BLUE)

    d.node("n3", 70, 900, 1500, 250, "internal network only", "network", align="left")
    for key, x, name, details in (
            ("sim", 95, "calendar-sim", ["Spring Boot · Java 25", "in memory, fixed seed"]),
            ("mailpit", 345, "mailpit", ["Mailpit 1.32", "SMTP capture"]),
            ("aiweb", 595, "ai-triage-web", ["Python 3.14 · Flask", "Gunicorn"]),
            ("grafana", 845, "grafana", ["Grafana 13", "operator dashboard"]),
            ("prom", 1095, "prometheus", ["Prometheus 3.x", "metrics and alerts"])):
        d.comp(key, x, 955, 220, 85, name, "container", details)
    for key, x, name, details, icon in (
            ("rabbitmq", 95, "rabbitmq", ["RabbitMQ 4.x", "quorum queues, DLQs"], "component"),
            ("mysql", 345, "mysql", ["MySQL 8.4 LTS", "four databases"], "database"),
            ("aicon", 595, "ai-triage-consumer", ["same image as ai-triage-web", "consumer process"], "component"),
            ("garage", 845, "garage", ["Garage 2.5 · single node", "attachments, backups"], "component")):
        d.comp(key, x, 1050, 220, 85, name, "container", details, icon=icon)

    d.node("ai", 595, 1230, 220, 90, "AI provider API", "external system", ["candidate: Gemini Flash", "(DEC-05)"])
    d.node("r2", 845, 1230, 220, 90, "Cloudflare R2", "external system", ["optional off-host", "backup copy"],
           dashed=True)
    d.path([(705, 1135), (705, 1230)], "HTTPS · classifies report text", at=(713, 1198))
    d.path([(955, 1135), (955, 1230)], "S3 · backup copy", at=(963, 1198), dashed=True)
    d.path([(1670, 240), (1670, 350)], "image pull · HTTPS", at=(1678, 318))

    d.note(1200, 450, 330, ["This document's reading, not ADR text:", "keycloak joins internal because",
                            "its database is in MySQL."], attach=d.p("keycloak", "n"))
    d.note(1600, 955, 240, ["Open (P-01): prometheus is on", "internal only, yet ADR-004 has",
                            "it scrape traefik and", "oauth2-proxy, on edge only."], attach=d.p("prom", "e"))
    d.note(1095, 1060, 460, ["Connections from the services to the broker, databases,",
                             "storage, mail and the calendar are drawn in P3 and P4."])
    d.note(150, 1225, 420, ["Open (P-02): if internal is declared internal: true,",
                            "the AI containers cannot reach the provider, and a",
                            "later real SMTP server is unreachable."], attach=d.p("ai", "w"))
    d.legend(1240, 1220)
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
    d.note(1420, 385, 420, ["Never routed: no Traefik rule (ADR-004)", "Gatus UI · Traefik API and dashboard",
                            "liveness, readiness, Actuator, /metrics", "AI /classify · simulator control",
                            "RabbitMQ management, Garage, Mailpit", "Open: Keycloak paths kept unrouted,",
                            "how Grafana is reached in demo"])

    d.boundary("public", 70, 690, 1030, 240, "Public routes · no ForwardAuth, no API session")
    for key, x, w, name, details, route, drop in (
            ("client", 95, 220, "client", ["nginx", "static files, /status page"], "/, /status", 205),
            ("gatus", 335, 220, "gatus", ["Gatus 5.37", "read-only JSON API"], "/status/api", 445),
            ("keycloak", 575, 220, "keycloak", ["Keycloak 26.8", "sign-in pages"], "/auth/*", 685),
            ("o2p", 815, 240, "oauth2-proxy", ["oauth2-proxy 7.15", "session, OIDC client"], "/oauth2/*", 875)):
        d.comp(key, x, 745, w, 95, name, "container", details)
        d.path([(570, 540), (570, 665), (drop, 665), (drop, 745)], route, at=(drop + 8, 727), bg=BLUE)
    d.lollipop(1000, 722, "session check", (1000, 745))
    d.dep([(1000, 540), (1000, 713)], "asks", at=(1008, 668), bg=BLUE)

    d.boundary("tb2", 1110, 690, 730, 240, "Trust boundary 2 · inside each service")
    for i, (key, check) in enumerate((("issue", "membership check"), ("dispatch", "assignment check"),
                                      ("notification", "inbox owner check"))):
        x = 1130 + 240 * i
        cx = x + 112
        d.comp(key, x, 745, 225, 95, key, "container", ["Spring Boot", "validates the JWT;", check])
        route = f"/api/{'notifications' if key == 'notification' else key}/*"
        d.path([(1242, 540), (1242, 665), (cx, 665), (cx, 745)] if cx != 1242 else [(1242, 540), (1242, 745)],
               route, at=(cx + 8, 727), bg=BLUE)

    d.note(300, 1010, 470, ["/status/api exists only if spike item 11 shows that Gatus",
                            "strips hosts, URLs and errors from its JSON; it must win",
                            "over /status, rule priority to confirm (ADR-004, ADR-012)."],
           attach=d.p("gatus", "s"))
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
    services = [("issue", "issue", [SPRING, "outbox publisher with confirms;", "idempotent consumer"]),
                ("dispatch", "dispatch", [SPRING, "outbox publisher with confirms;", "idempotent consumer"]),
                ("notification", "notification", [SPRING, "idempotent consumer"]),
                ("ai", "ai-triage-consumer", ["Python 3.14", "stateless: classifies,", "publishes, then acknowledges"])]
    for cx, (key, name, details) in zip(cols, services):
        d.comp(key, cx - 140, 150, 280, 100, name, "container", details)

    d.holder("rabbitmq", 95, 330, 1740, 520, "rabbitmq", "container",
             ["RabbitMQ 4.x · one node · one broker user per service (ADR-005)"])
    d.lollipop(1710, 307, "AMQP", (1710, 330))
    d.comp("ex", 200, 610, 1300, 62, "bmc.events", "exchange",
           ["durable topic exchange · routing key <producer>.<eventType>"])
    queues = [("qi", "issue.inbox", ["quorum · delivery limit 5"], "TriageSuggested,\ndispatch events",
               "ack after commit"),
              ("qd", "dispatch.inbox", ["quorum · delivery limit 5"], "IssueStateChanged,\nMembership*",
               "ack after commit"),
              ("qn", "notification.inbox", ["quorum · delivery limit 5"], "NotificationRequested", "ack after commit"),
              ("qa", "ai-triage.requests", ["quorum · delivery limit 5", "point to point, private text"],
               "issue.TriageRequested\nonly", "ack after publishing")]
    for cx, (key, name, details, binding, ack) in zip(cols, queues):
        d.comp(key, cx - 105, 410, 210, 90, name, "queue", details)
        d.dep([(cx, 610), (cx, 500)], binding, at=(cx + 8, 545), bg=BLUE)
        d.dep([(cx, 410), (cx, 250)], f"delivers\n{ack}", at=(cx + 8, 280), bg=BLUE)
        d.dep([(cx - 125, 250), (cx - 125, 610)], "publishes" + ("\nwith confirms" if key != "qa" else ""),
              at=(cx - 133, 368), anchor="end", bg=BLUE)

    d.comp("dlx", 1600, 410, 220, 90, "bmc.dlx", "exchange", ["dead-letter · at-least-once"])
    d.comp("dlq", 1600, 570, 220, 100, "<queue>.dlq", "queue", ["one per queue · TTL 7 days", "replay by runbook"])
    d.dep([(1485, 455), (1600, 455)], "after 5 deliveries\n(every queue)", at=(1542, 420), anchor="middle", bg=BLUE)
    d.dep([(1710, 500), (1710, 570)], "routes", at=(1718, 535), bg=BLUE)

    d.note(200, 705, 430, ["Outbox rows wait as pending while the broker is",
                           "down; the publisher retries with backoff (2 s",
                           "doubling, cap 5 min) without limit."], attach=(205, 510))
    d.note(680, 705, 430, ["The Spring consumers keep processed event IDs,",
                           "so a duplicate is acknowledged without",
                           "repeating the effect (ADR-003)."])
    d.note(1160, 705, 430, ["TriageRequested is the only message with private",
                            "report text: bound only to ai-triage.requests,",
                            "never logged; its DLQ copy expires after 7 days."], attach=(1380, 672))
    return d


def p4():
    d = Diagram("p4-data-and-platform", "P4 · Data stores and platform connections",
                "UML deployment diagram of stores and platform calls · ADR-001, ADR-004, ADR-010 · arrows from user "
                "to used · proposed", 1900, 830)
    d.node("host", 40, 80, 1820, 720, "Demonstration host", "device", ["Docker host · internal network"])

    d.comp("sim", 140, 150, 220, 90, "calendar-sim", "container", ["Spring Boot · Java 25", "in memory, fixed seed"])
    d.comp("mailpit", 380, 150, 220, 90, "mailpit", "container", ["Mailpit 1.32", "SMTP capture, demo only"])
    d.comp("keycloak", 680, 150, 220, 90, "keycloak", "container", ["Keycloak 26.8", "accounts, account email"])
    d.lollipop(250, 262, "HTTP API", (250, 240))
    d.lollipop(490, 262, "SMTP", (490, 240), at="w")
    d.lollipop(800, 262, "Admin API", (800, 240), at="w")

    d.comp("dispatch", 140, 340, 220, 100, "dispatch", "container", ["Spring Boot", "interventions, bookings"])
    d.comp("notification", 380, 340, 220, 100, "notification", "container", ["Spring Boot", "inbox, delivery log"])
    d.comp("issue", 960, 340, 320, 100, "issue", "container", ["Spring Boot",
                                                               "reports, issues, memberships, attachments"])
    d.comp("backup", 1370, 340, 220, 100, "backup job", "job", ["container and schedule", "not placed (P-03)"],
           dashed=True)

    d.holder("mysql", 120, 520, 980, 200, "mysql", "container", ["MySQL 8.4 LTS · one instance"])
    for x, owner in ((150, "dispatch"), (390, "notification"), (630, "keycloak"), (870, "issue")):
        d.comp("db-" + owner, x, 540, 200, 100, owner, "database", ["owner: " + owner], icon="database")
    d.holder("garage", 1130, 520, 480, 200, "garage", "container", ["Garage 2.5 · S3 subset · single node"])
    d.lollipop(1240, 497, "S3 API", (1240, 520), at="w")
    d.comp("ba", 1150, 540, 210, 100, "bmc-attachments", "bucket", ["report photos;", "candidate, post-MVP"],
           icon="artifact")
    d.comp("bb", 1380, 540, 210, 100, "bmc-backups", "bucket", ["MySQL dumps"], icon="artifact")

    d.dep([(250, 340), (250, 271)], "books visits\nIdempotency-Key", at=(258, 292), bg=BLUE)
    d.dep([(490, 340), (490, 271)], "sends email", at=(498, 305), bg=BLUE)
    d.dep([(700, 240), (700, 262), (499, 262)])
    d.dep([(600, 390), (800, 390), (800, 271)], "Admin API · view-users", at=(700, 378), anchor="middle", bg=BLUE)
    d.dep([(860, 240), (860, 505), (730, 505), (730, 540)], "JDBC", at=(868, 460), bg=BLUE)
    d.dep([(250, 440), (250, 540)], "JDBC", at=(258, 488), bg=BLUE)
    d.dep([(490, 440), (490, 540)], "JDBC", at=(498, 488), bg=BLUE)
    d.dep([(990, 440), (990, 540)], "JDBC", at=(998, 488), bg=BLUE)
    d.dep([(1240, 440), (1240, 488)], "stores photos", at=(1248, 462), bg=BLUE)
    d.dep([(1480, 440), (1480, 497), (1249, 497)], "writes dumps", at=(1488, 466), bg=BLUE)
    d.dep([(1590, 390), (1700, 390), (1700, 765), (610, 765), (610, 720)], "dump · placement open (P-03)",
          at=(1150, 765), anchor="middle", bg=BLUE)

    d.note(1000, 140, 520, ["Every Spring service also needs Keycloak's signing keys;",
                            "that connection is not drawn and its route is open (P-05).",
                            "Calls to a platform component or to the calendar are not",
                            "service-to-service calls (ADR-001)."], attach=d.p("keycloak", "e", 0.4))
    return d


def p5():
    d = Diagram("p5-health-and-metrics", "P5 · Health, metrics and logs",
                "UML deployment diagram of health and metrics paths · ADR-004, ADR-012 · proposed", 1720, 900)
    d.node("device", 40, 80, 480, 190, "User device", "device", ["browser or installed PWA"])
    d.comp("web", 225, 150, 290, 80, "BMC web app", "component", ["/status page and banner", "public, no login"])
    d.actor("operator", 1380, 90, "Operator", ["reads the dashboard"])
    d.note(560, 85, 600, ["Public capabilities: Report a fault, Schedule interventions, Notifications,",
                          "Suggestions, Calendar sync, Sign-in, Photo upload; infrastructure is",
                          "never listed by name (ADR-012)."], attach=(690, 420))

    d.node("host", 40, 320, 1640, 490, "Demonstration host", "device", ["Docker host"])
    d.comp("traefik", 255, 420, 230, 90, "traefik", "container", ["Traefik 3.7", "health check before routing"])
    d.comp("gatus", 575, 420, 230, 90, "gatus", "container", ["Gatus 5.37", "capability checks, 30 days"])
    d.comp("prom", 895, 420, 230, 90, "prometheus", "container", ["Prometheus 3.x", "scrapes /metrics, alerts"])
    d.comp("grafana", 1265, 420, 230, 90, "grafana", "container", ["Grafana 13", "operator dashboard"])
    d.lollipop(370, 401, "HTTPS 443", (370, 420), at="w")
    d.dep([(370, 230), (370, 392)], "GET /status/api", at=(378, 285))

    d.boundary("bmc", 70, 580, 560, 200, "BMC services · readiness covers own database")
    for x, y, name, check in ((85, 595, "issue", "Actuator readiness · /metrics"),
                              (355, 595, "dispatch", "Actuator readiness · /metrics"),
                              (85, 670, "notification", "Actuator readiness · /metrics"),
                              (355, 670, "ai-triage-web", "Flask health · /metrics")):
        d.comp(name, x, y, 260, 62, name, "container", [check])
    d.boundary("plat", 660, 580, 990, 200, "Platform checks · rolled up into public capabilities")
    for i, (name, check) in enumerate((("oauth2-proxy", "/ready · /metrics"),
                                       ("rabbitmq", "diagnostics ping · metrics plugin"),
                                       ("keycloak", "/health/ready, port 9000"), ("mysql", "query-level check"),
                                       ("garage", "admin GET /health"), ("mailpit", "readyz"),
                                       ("calendar-sim", "calendar sync capability"))):
        d.comp("t-" + name, 675 + 240 * (i % 4), 595 + 75 * (i // 4), 230, 62, name, "container", [check])

    d.dep([(485, 465), (575, 465)], "/status/api", at=(530, 453), anchor="middle", bg=BLUE)
    d.dep([(895, 465), (805, 465)], "scrape", at=(850, 453), anchor="middle", bg=BLUE)
    d.dep([(1265, 465), (1125, 465)], "queries", at=(1195, 453), anchor="middle", bg=BLUE)
    d.dep([(1010, 420), (1010, 394), (440, 394), (440, 420)], "scrape · network open (P-01)", at=(725, 394),
          anchor="middle", bg=BLUE)
    d.path([(1380, 196), (1380, 420)], "access in demo: open", at=(1388, 270), dashed=True)
    d.dep([(370, 510), (370, 580)], "readiness of issue,\ndispatch, notification", at=(378, 530), bg=BLUE)
    d.dep([(600, 510), (600, 580)], "readiness", at=(608, 545), bg=BLUE)
    d.dep([(790, 510), (790, 580)], "platform checks", at=(798, 545), bg=BLUE)
    d.dep([(950, 510), (950, 560), (530, 560), (530, 580)], "/metrics", at=(958, 532), bg=BLUE)
    d.dep([(1080, 510), (1080, 580)], "/metrics of oauth2-proxy,\nrabbitmq", at=(1088, 530), bg=BLUE)

    d.note(70, 830, 620, ["Logs are structured with correlationId and traceparent; where they are",
                          "collected is left to DEVOPS-02 (EN01-U12), so no log collector is drawn."])
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
                "team review (EN01-U1)", 1900, 560)
    d.node("host", 40, 80, 1820, 450, "Demonstration host", "device", ["one compose.yaml with profiles"])

    d.node("core", 70, 150, 540, 355, "First: profile core", "profile set", ["eight containers"])
    core = [("traefik", "Traefik 3.7"), ("oauth2-proxy", "oauth2-proxy 7.15"), ("keycloak", "Keycloak 26.8"),
            ("client", "nginx"), ("issue", "Spring Boot"), ("dispatch", "Spring Boot"),
            ("mysql", "MySQL 8.4 LTS"), ("rabbitmq", "RabbitMQ 4.x")]
    for i, (name, version) in enumerate(core):
        d.comp("c-" + name, 85 + 260 * (i % 2), 210 + 70 * (i // 2), 245, 60, name, "container", [version],
               icon="database" if name == "mysql" else "component")

    d.node("slice", 670, 150, 540, 355, "When the slice needs it", "profile set", ["no profile name yet"])
    for i, (name, details) in enumerate((("ai-triage-web", ["reporting works", "without it (NFR-03)"]),
                                         ("ai-triage-consumer", ["with ai-triage-web"]),
                                         ("notification", ["as soon as US-10", "is in the slice"]),
                                         ("calendar-sim", ["when dispatch", "books a visit"]))):
        d.comp("l-" + name, 685 + 260 * (i % 2), 210 + 103 * (i // 2), 250, 92, name, "container", details)
    d.note(685, 425, 505, ["Memory of each set is not measured (EN01-U3, spike item 8)."])

    d.node("later", 1270, 150, 560, 355, "Later: own profiles", "profile set",
           ["demo, status, observability, storage"])
    for i, (name, profile, details) in enumerate((("mailpit", "profile demo", ["email channel only"]),
                                                  ("gatus", "profile status (proposed)", ["/status page, banner"]),
                                                  ("prometheus", "profile observability", []),
                                                  ("grafana", "profile observability", []),
                                                  ("garage", "profile storage (proposed)",
                                                   ["before backup and restore"]))):
        d.comp("x-" + name, 1285 + 275 * (i % 2), 210 + 90 * (i // 2), 260, 80, name, "container",
               [profile] + details)

    d.dep([(610, 330), (670, 330)], "then", at=(640, 318), anchor="middle", bg=BLUE)
    d.dep([(1210, 330), (1270, 330)], "then", at=(1240, 318), anchor="middle", bg=BLUE)
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
