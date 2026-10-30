"""The seven BMC physical views as C4 deployment diagrams, drawn with vpdraw.

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

from vpdraw import ELEMENT, EXTERNAL, GREY, NODE, NODE_IN, PART, Diagram

HERE = Path(__file__).resolve().parent
SPRING = "Container: Spring Boot 4.1.2 · Java 25"


def p1():
    d = Diagram("p1-deployment-overview", "P1 · Deployment overview",
                "C4 deployment view of the proposed BMC stack · ADR-004 · proposed, nothing is deployed",
                1900, 1250)
    d.node("device", 40, 90, 420, 190, "User device", "Deployment node: phone or computer")
    d.container("web", 175, 108, 250, 95, "BMC web app", "PWA: React + Vite build", ["online only, nothing queued"])
    d.node("github", 1480, 90, 380, 190, "GitHub", "Deployment node: github.com")
    d.container("ghcr", 1550, 108, 290, 95, "GitHub Container Registry", "Container registry",
                ["one multi-arch image per app"], shape="system", fill=EXTERNAL)

    d.node("host", 40, 330, 1820, 760, "Demonstration host",
           "Deployment node: one Docker host · Docker Engine + Compose\n"
           "linux/amd64 or linux/arm64 · host choice open (EN01-U3)")
    d.node("n1", 70, 360, 1080, 170, "edge network only", "Docker network: edge", fill=NODE_IN)
    d.container("traefik", 180, 380, 240, 90, "traefik", "Container: Traefik 3.7", ["only published ports: 80, 443"])
    d.container("client", 520, 380, 240, 90, "client", "Container: nginx", ["serves the React build"])
    d.container("o2p", 860, 380, 240, 90, "oauth2-proxy", "Container: oauth2-proxy 7.15", ["browser session (BFF)"])

    d.node("n2", 70, 570, 1760, 170, "edge + internal networks", "Docker networks: edge and internal", fill=NODE_IN)
    routed = [("issue", "issue", SPRING, ["reports, issues, memberships"], "/api/issue/*"),
              ("dispatch", "dispatch", SPRING, ["interventions, bookings"], "/api/dispatch/*"),
              ("notification", "notification", SPRING, ["in-app inbox, email"], "/api/notifications/*"),
              ("keycloak", "keycloak", "Container: Keycloak 26.8", ["sign-in and accounts"], "/auth/*"),
              ("gatus", "gatus", "Container: Gatus 5.37", ["capability checks"], "/status/api")]
    for i, (key, name, tech, desc, route) in enumerate(routed):
        x = 345 + 280 * i
        d.container(key, x, 600, 240, 90, name, tech, desc)
        d.rel([(300, 470), (300, 550), (x + 120, 550), (x + 120, 600)], route, at=(x + 128, 586), bg=NODE_IN)

    d.node("n3", 70, 780, 1760, 250, "internal network only", "Docker network: internal", fill=NODE_IN)
    for key, x, name, tech, desc in (
            ("sim", 95, "calendar-sim", "Container: Spring Boot · Java 25", ["in memory, fixed seed"]),
            ("mailpit", 395, "mailpit", "Container: Mailpit 1.32", ["SMTP capture"]),
            ("aiweb", 695, "ai-triage-web", "Container: Python 3.14 · Flask", ["Gunicorn"]),
            ("grafana", 995, "grafana", "Container: Grafana 13", ["operator dashboard"]),
            ("prom", 1295, "prometheus", "Container: Prometheus 3.x", ["metrics and alerts"])):
        d.container(key, x, 795, 240, 80, name, tech, desc)
    d.container("rabbitmq", 95, 890, 240, 80, "rabbitmq", "Container: RabbitMQ 4.x", ["quorum queues, DLQs"],
                shape="queue")
    d.container("mysql", 395, 885, 240, 90, "mysql", "Container: MySQL 8.4 LTS", ["four databases"], shape="db")
    d.container("aicon", 695, 890, 240, 80, "ai-triage-consumer", "Container: same image as ai-triage-web",
                ["consumer process"])
    d.container("garage", 995, 890, 240, 80, "garage", "Container: Garage 2.5 · single node",
                ["buckets: attachments, backups"])

    d.container("ai", 695, 1130, 240, 80, "AI provider API", "External system",
                ["candidate: Gemini Flash (DEC-05)"], shape="system", fill=EXTERNAL)
    d.container("r2", 995, 1130, 240, 80, "Cloudflare R2", "External system · optional",
                ["off-host backup copy"], shape="system", fill=EXTERNAL, dashed=True)

    d.rel([(300, 203), (300, 380)], "uses\n[HTTPS 443]", at=(308, 291))
    d.rel([(420, 425), (520, 425)], "/, /status", at=(470, 413), anchor="middle", bg=NODE_IN)
    d.rel([(372, 470), (372, 492), (980, 492), (980, 470)], "/oauth2/*", at=(676, 492), anchor="middle", bg=NODE_IN)
    d.rel([(1695, 203), (1695, 330)], "image pull\n[HTTPS]", at=(1703, 291))
    d.rel([(815, 970), (815, 1130)], "classifies report text\n[HTTPS]", at=(823, 1103))
    d.rel([(1115, 970), (1115, 1130)], "backup copy\n[S3]", at=(1123, 1103), dashed=True)

    d.note(1200, 372, 330, ["This document's reading, not ADR text:", "keycloak joins internal because",
                            "its database is in MySQL."], attach=d.p("keycloak", "n", 0.5))
    d.note(1560, 795, 260, ["Open (P-01): prometheus is on", "internal only, yet ADR-004 has it",
                            "scrape traefik and oauth2-proxy,", "which are on edge only."],
           attach=d.p("prom", "e"))
    d.note(1295, 893, 520, ["Connections from the services to the broker, the databases,",
                            "storage, mail and the calendar are drawn in P3 and P4."])
    d.note(150, 1110, 500, ["Open (P-02): if internal is declared internal: true, the",
                            "AI containers cannot reach the provider, and a later real",
                            "SMTP server is unreachable for notification and keycloak."],
           attach=d.p("ai", "w"))
    d.legend(1430, 1110)
    return d


def p2():
    d = Diagram("p2-edge-and-trust", "P2 · Edge routing and trust boundaries",
                "C4 deployment view of the edge · routes from ADR-004, authorisation from ADR-005 · proposed",
                1900, 1050)
    d.node("device", 250, 80, 520, 170, "User device", "Deployment node: browser or installed PWA")
    d.container("web", 445, 98, 250, 85, "BMC web app", "PWA", ["one origin, no CORS"])

    d.node("host", 40, 300, 1820, 630, "Demonstration host", "Deployment node: Docker host")
    d.boundary("tb1", 70, 325, 1330, 255, "Trust boundary 1 · internet → traefik")
    d.node("traefik", 95, 345, 1280, 195, "traefik",
           "Container: Traefik 3.7 · the only published ports, 80 and 443", fill=ELEMENT)
    d.container("router", 460, 365, 220, 100, "Router", "Entrypoint", ["TLS terminates here;", "matches the route rules"],
                fill=PART)
    d.container("fa", 790, 365, 220, 100, "ForwardAuth", "Middleware · /api/* only", ["asks oauth2-proxy;",
                                                                                     "no session → 401"], fill=PART)
    d.container("strip", 1132, 365, 220, 100, "StripPrefix", "Middleware · /api/* only",
                ["removes /api/<service>;", "then RateLimit, Headers"], fill=PART)
    d.note(1420, 325, 420, ["Never routed: no Traefik rule (ADR-004)", "Gatus UI · Traefik API and dashboard",
                            "liveness, readiness, Actuator, /metrics", "AI /classify · simulator control",
                            "RabbitMQ management, Garage, Mailpit", "Open: Keycloak paths kept unrouted,",
                            "how Grafana is reached in demo"])

    d.boundary("public", 70, 620, 1010, 255, "Public routes · no ForwardAuth, no API session", colour=GREY)
    for key, x, w, name, tech, desc, route, drop in (
            ("client", 95, 220, "client", "Container: nginx", ["static files, /status page"], "/, /status", 205),
            ("gatus", 335, 220, "gatus", "Container: Gatus 5.37", ["read-only JSON API"], "/status/api", 445),
            ("keycloak", 575, 220, "keycloak", "Container: Keycloak 26.8", ["sign-in pages"], "/auth/*", 685),
            ("o2p", 815, 240, "oauth2-proxy", "Container: oauth2-proxy 7.15", ["session, OIDC client"],
             "/oauth2/*", 875)):
        d.container(key, x, 680, w, 100, name, tech, desc)
        d.rel([(570, 465), (570, 655), (drop, 655), (drop, 680)], route, at=(drop + 8, 668), bg=NODE)

    d.boundary("tb2", 1110, 620, 730, 255, "Trust boundary 2 · inside each service (ADR-005)")
    for i, (key, check) in enumerate((("issue", "membership check"), ("dispatch", "assignment check"),
                                      ("notification", "inbox owner check"))):
        x = 1130 + 240 * i
        cx = x + 112
        d.container(key, x, 680, 225, 100, key, "Container: Spring Boot", ["validates the JWT;", check])
        route = f"/api/{'notifications' if key == 'notification' else key}/*"
        d.rel([(1242, 465), (1242, 655), (cx, 655), (cx, 680)] if cx != 1242 else [(1242, 465), (1242, 680)],
              route, at=(cx + 8, 668), bg=NODE)

    d.rel([(570, 183), (570, 365)], "uses\n[HTTPS 443]", at=(578, 259))
    d.rel([(680, 415), (790, 415)], "/api/*", at=(735, 403), anchor="middle", bg=ELEMENT)
    d.rel([(1010, 415), (1132, 415)], "session valid", at=(1071, 403), anchor="middle", bg=ELEMENT)
    d.rel([(1000, 465), (1000, 680)], "session check\n[HTTP]", at=(1008, 593), bg=NODE)

    d.note(300, 950, 470, ["/status/api exists only if spike item 11 shows that Gatus",
                           "strips hosts, URLs and errors from its JSON; it must win",
                           "over /status, rule priority to confirm (ADR-004, ADR-012)."],
           attach=d.p("gatus", "s"))
    d.note(1130, 950, 500, ["Traefik Proxy has no JWT middleware: each Spring service",
                            "is an OAuth2 resource server, authorises against its own",
                            "data and answers 404 outside the caller's scope."],
           attach=d.p("issue", "s"))
    return d


def p3():
    d = Diagram("p3-messaging", "P3 · Messaging through RabbitMQ",
                "C4 deployment view of the broker · topology from ADR-003 · arrows follow the message · proposed",
                1900, 910)
    d.node("host", 40, 80, 1820, 800, "Demonstration host", "Deployment node: Docker host · internal network")
    cols = [330, 680, 1030, 1380]
    services = [("issue", "issue", SPRING, ["outbox publisher with confirms;", "idempotent consumer"]),
                ("dispatch", "dispatch", SPRING, ["outbox publisher with confirms;", "idempotent consumer"]),
                ("notification", "notification", SPRING, ["idempotent consumer"]),
                ("ai", "ai-triage-consumer", "Container: Python 3.14", ["stateless: classifies,",
                                                                        "publishes, then acknowledges"])]
    for cx, (key, name, tech, desc) in zip(cols, services):
        d.container(key, cx - 140, 110, 280, 110, name, tech, desc)

    d.node("rabbitmq", 95, 280, 1740, 520, "rabbitmq",
           "Container: RabbitMQ 4.x · one node · one broker user per service (ADR-005)", fill=ELEMENT)
    queues = [("qi", "issue.inbox", ["delivery limit 5"], "TriageSuggested,\ndispatch events", "ack after commit"),
              ("qd", "dispatch.inbox", ["delivery limit 5"], "IssueStateChanged,\nMembership*", "ack after commit"),
              ("qn", "notification.inbox", ["delivery limit 5"], "NotificationRequested", "ack after commit"),
              ("qa", "ai-triage.requests", ["delivery limit 5;", "point to point, private text"], "issue.TriageRequested\nonly",
               "ack after publishing")]
    d.container("ex", 200, 560, 1300, 62, "bmc.events", "Durable topic exchange · routing key <producer>.<eventType>",
                fill=PART)
    for cx, (key, name, desc, binding, ack) in zip(cols, queues):
        d.container(key, cx - 105, 360, 210, 90, name, "Quorum queue", desc, shape="queue",
                    fill=PART)
        d.rel([(cx, 560), (cx, 450)], binding, at=(cx + 8, 505), bg=ELEMENT)
        d.rel([(cx, 360), (cx, 220)], f"delivers\n[AMQP · {ack}]", at=(cx + 8, 243), bg=NODE)
        d.rel([(cx - 125, 220), (cx - 125, 560)], "publishes\n[AMQP" + (", confirms]" if key != "qa" else "]"),
              at=(cx - 133, 315), anchor="end", bg=ELEMENT)

    d.container("dlx", 1600, 360, 220, 90, "bmc.dlx", "Dead-letter exchange", ["at-least-once"], fill=PART)
    d.container("dlq", 1600, 520, 220, 100, "<queue>.dlq", "Quorum queue · TTL 7 days",
                ["one per queue;", "replay by runbook"], shape="queue", fill=PART)
    d.rel([(1485, 405), (1600, 405)], "after 5 deliveries\n(every queue)", at=(1542, 372), anchor="middle",
          dashed=True, bg=ELEMENT)
    d.rel([(1710, 450), (1710, 520)], "routes", at=(1718, 485), dashed=True, bg=ELEMENT)

    d.note(200, 665, 430, ["Outbox rows wait as pending while the broker is",
                           "down; the publisher retries with backoff (2 s",
                           "doubling, cap 5 min) without limit."], attach=(205, 470))
    d.note(680, 665, 430, ["The Spring consumers keep processed event IDs,",
                           "so a duplicate is acknowledged without",
                           "repeating the effect (ADR-003)."])
    d.note(1160, 665, 430, ["TriageRequested is the only message with private",
                            "report text: bound only to ai-triage.requests,",
                            "never logged; its DLQ copy expires after 7 days."], attach=(1380, 622))
    return d


def p4():
    d = Diagram("p4-data-and-platform", "P4 · Data stores and platform connections",
                "C4 deployment view of stores and platform calls · ADR-001, ADR-004, ADR-010 · arrows from client "
                "to server · proposed", 1900, 830)
    d.node("host", 40, 80, 1820, 720, "Demonstration host", "Deployment node: Docker host · internal network")

    d.container("sim", 140, 110, 220, 90, "calendar-sim", "Container: Spring Boot · Java 25", ["in memory, fixed seed"])
    d.container("mailpit", 380, 110, 220, 90, "mailpit", "Container: Mailpit 1.32", ["SMTP capture, demo only"])
    d.container("keycloak", 680, 110, 220, 90, "keycloak", "Container: Keycloak 26.8",
                ["accounts, credentials,", "account email"])

    d.container("dispatch", 140, 300, 220, 100, "dispatch", "Container: Spring Boot",
                ["interventions, bookings,", "contractors"])
    d.container("notification", 380, 300, 220, 100, "notification", "Container: Spring Boot",
                ["inbox, preferences,", "delivery log"])
    d.container("issue", 960, 300, 320, 100, "issue", "Container: Spring Boot",
                ["reports, issues, memberships,", "attachments"])
    d.container("backup", 1370, 300, 220, 100, "backup job", "Not placed (P-03)",
                ["container and schedule", "still open"], dashed=True)

    d.node("mysql", 120, 480, 980, 240, "mysql", "Container: MySQL 8.4 LTS · one instance", fill=ELEMENT)
    for x, owner in ((150, "dispatch"), (390, "notification"), (630, "keycloak"), (870, "issue")):
        d.container("db-" + owner, x, 500, 200, 110, owner, "Database", ["owner: " + owner], shape="db", fill=PART)
    d.node("garage", 1130, 480, 480, 240, "garage", "Container: Garage 2.5 · S3 subset · single node", fill=ELEMENT)
    d.container("ba", 1150, 500, 210, 110, "bmc-attachments", "Bucket", ["report photos;", "candidate, post-MVP"],
                fill=PART)
    d.container("bb", 1380, 500, 210, 110, "bmc-backups", "Bucket", ["MySQL dumps"], fill=PART)

    d.rel([(250, 300), (250, 200)], "books visits\n[HTTP, Idempotency-Key]", at=(258, 240), bg=NODE)
    d.rel([(490, 300), (490, 200)], "sends email\n[SMTP]", at=(498, 240), bg=NODE)
    d.rel([(680, 155), (600, 155)], "[SMTP]", at=(640, 143), anchor="middle", bg=NODE)
    d.rel([(600, 350), (800, 350), (800, 200)], "Admin API · view-users", at=(700, 338), anchor="middle",
          dashed=True, bg=NODE)
    d.rel([(860, 200), (860, 465), (730, 465), (730, 500)], "[JDBC]", at=(868, 420), bg=NODE)
    d.rel([(250, 400), (250, 500)], "[JDBC]", at=(258, 445), bg=NODE)
    d.rel([(490, 400), (490, 500)], "[JDBC]", at=(498, 445), bg=NODE)
    d.rel([(990, 400), (990, 500)], "[JDBC]", at=(998, 445), bg=NODE)
    d.rel([(1240, 400), (1240, 500)], "stores photos\n[S3]", at=(1248, 440), bg=NODE)
    d.rel([(1480, 400), (1480, 500)], "writes dumps\n[S3]", at=(1488, 440), dashed=True, bg=NODE)
    d.rel([(1590, 350), (1700, 350), (1700, 760), (610, 760), (610, 720)], "dump · placement open (P-03)",
          at=(1150, 760), anchor="middle", dashed=True, bg=NODE)

    d.note(1000, 105, 520, ["Every Spring service also needs Keycloak's signing keys;",
                            "that connection is not drawn and its route is open (P-05).",
                            "Calls to a platform component or to the calendar are not",
                            "service-to-service calls (ADR-001)."], attach=d.p("keycloak", "e", 0.4))
    return d


def p5():
    d = Diagram("p5-health-and-metrics", "P5 · Health, metrics and logs",
                "C4 deployment view of health and metrics paths · ADR-004, ADR-012 · proposed", 1720, 840)
    d.node("device", 40, 80, 480, 170, "User device", "Deployment node: browser or installed PWA")
    d.container("web", 245, 98, 250, 85, "BMC web app", "PWA · /status page and banner", ["public, no login"])
    d.container("operator", 1280, 70, 200, 120, "Operator", "Person", ["reads the dashboard"], shape="person",
                fill=EXTERNAL)
    d.note(560, 85, 600, ["Public capabilities: Report a fault, Schedule interventions, Notifications,",
                          "Suggestions, Calendar sync, Sign-in, Photo upload; infrastructure is",
                          "never listed by name (ADR-012)."], attach=(690, 340))

    d.node("host", 40, 300, 1640, 440, "Demonstration host", "Deployment node: Docker host")
    d.container("traefik", 255, 340, 230, 90, "traefik", "Container: Traefik 3.7", ["health check before routing"])
    d.container("gatus", 575, 340, 230, 90, "gatus", "Container: Gatus 5.37", ["capability checks, 30 days"])
    d.container("prom", 895, 340, 230, 90, "prometheus", "Container: Prometheus 3.x", ["scrapes /metrics, alerts"])
    d.container("grafana", 1265, 340, 230, 90, "grafana", "Container: Grafana 13", ["operator dashboard"])

    d.boundary("bmc", 70, 500, 560, 200, "BMC services · readiness covers own database", colour=GREY)
    for x, y, name, check in ((85, 515, "issue", "Actuator readiness · /metrics"),
                              (355, 515, "dispatch", "Actuator readiness · /metrics"),
                              (85, 585, "notification", "Actuator readiness · /metrics"),
                              (355, 585, "ai-triage-web", "Flask health · /metrics")):
        d.container(name, x, y, 255, 58, name, None, [check])
    d.boundary("plat", 660, 500, 990, 200, "Platform checks · rolled up into public capabilities", colour=GREY)
    for i, (name, check) in enumerate((("oauth2-proxy", "/ready · /metrics"),
                                       ("rabbitmq", "diagnostics ping · metrics plugin"),
                                       ("keycloak", "/health/ready, port 9000"), ("mysql", "query-level check"),
                                       ("garage", "admin GET /health"), ("mailpit", "readyz"),
                                       ("calendar-sim", "calendar sync capability"))):
        d.container("t-" + name, 675 + 240 * (i % 4), 515 + 70 * (i // 4), 230, 58, name, None, [check])

    d.rel([(370, 183), (370, 340)], "GET /status/api\n[HTTPS]", at=(378, 258))
    d.rel([(485, 385), (575, 385)], "/status/api", at=(530, 373), anchor="middle", bg=NODE)
    d.rel([(1380, 190), (1380, 340)], "reads dashboards\n[access in demo: open]", at=(1388, 252), dashed=True)
    d.rel([(1265, 385), (1125, 385)], "queries", at=(1195, 373), anchor="middle", bg=NODE)
    d.rel([(895, 385), (805, 385)], "scrape", at=(850, 373), anchor="middle", bg=NODE)
    d.rel([(1010, 340), (1010, 318), (440, 318), (440, 340)], "scrape · network open (P-01)", at=(725, 318),
          anchor="middle", dashed=True, bg=NODE)
    d.rel([(370, 430), (370, 500)], "readiness of issue,\ndispatch, notification", at=(378, 455), bg=NODE)
    d.rel([(600, 430), (600, 500)], "readiness", at=(608, 462), bg=NODE)
    d.rel([(760, 430), (760, 500)], "platform checks", at=(768, 462), bg=NODE)
    d.rel([(950, 430), (950, 482), (530, 482), (530, 500)], "scrape /metrics", at=(958, 455), bg=NODE)
    d.rel([(1080, 430), (1080, 500)], "scrape oauth2-proxy,\nrabbitmq", at=(1088, 455), bg=NODE)

    d.note(70, 760, 620, ["Logs are structured with correlationId and traceparent; where they are",
                          "collected is left to DEVOPS-02 (EN01-U12), so no log collector is drawn."])
    return d


def p6():
    d = Diagram("p6-delivery-path", "P6 · Environments and delivery path",
                "C4 deployment view of the proposed delivery path · ADR-004, PR #40 (open) · arrows follow code and "
                "images · no pipeline, image or host exists yet", 1900, 730)
    d.node("laptop", 40, 80, 300, 200, "Developer laptop", "Deployment node: Docker Engine + Compose")
    d.container("wc", 65, 100, 250, 100, "Working copy", "Git · compose.yaml", ["smaller profile set"])

    d.node("github", 380, 80, 1480, 360, "GitHub", "Deployment node: github.com · DEVOPS-01 proposal, PR #40 (open)")
    d.container("repo", 405, 100, 230, 100, "Repository", "Git", ["feature/* → dev → main;", "release: protected v* tag"])
    d.node("actions", 670, 100, 890, 280, "GitHub Actions",
           "Deployment node: runners · proposed stages, no pipeline yet", fill=NODE_IN)
    stages = [("Lint, unit tests", []), ("Contract checks", ["buf lint,", "buf breaking"]),
              ("Boundary tests", ["ArchUnit,", "import-linter, ESLint"]),
              ("Integration tests", ["real MySQL 8.4", "and RabbitMQ"]),
              ("Multi-arch build", ["amd64, arm64;", "method open (EN01-U9)"])]
    for i, (name, desc) in enumerate(stages):
        x = 690 + 175 * i
        d.container(f"s{i}", x, 115, 155, 125, name, f"Stage {i + 1}", desc, fill=PART)
        if i:
            d.rel([(x - 20, 177), (x, 177)])
    d.container("ghcr", 1590, 100, 250, 100, "GHCR", "Container registry", ["one image per app;",
                                                                           "built once, promoted by tag"])

    d.node("host", 1100, 500, 760, 200, "Demonstration host", "Deployment node: Docker host")
    d.container("env", 1130, 520, 300, 110, "Host or CI environment", "Configuration source",
                [".env with secrets,", "never in Git"])
    d.container("stack", 1560, 520, 270, 110, "BMC stack", "Docker Compose · compose.yaml",
                ["compose pull, then up -d;", "rollback: previous tag"])

    d.rel([(315, 150), (405, 150)], "push", at=(360, 138), anchor="middle")
    d.rel([(635, 150), (690, 150)], "runs", at=(662, 138), anchor="middle", bg=NODE)
    d.rel([(1545, 150), (1590, 150)])
    d.rel([(1715, 200), (1715, 520)], "pulls the same image\n[HTTPS]", at=(1723, 462))
    d.rel([(1430, 575), (1560, 575)], "injected at deploy", at=(1495, 563), anchor="middle", bg=NODE)

    d.note(1000, 258, 540, ["Multi-arch availability is recorded for the Traefik, RabbitMQ,",
                            "MySQL, Mailpit, Temurin and python images, not yet for",
                            "Keycloak, oauth2-proxy, Garage, Prometheus, Grafana or nginx",
                            "(spike item 8, ADR-004)."], attach=d.p("s4", "s"))
    d.note(405, 230, 240, ["Required checks are configured", "only when the pipeline exists."])
    return d


def p7():
    d = Diagram("p7-compose-profiles", "P7 · Compose profiles and rollout",
                "C4 deployment view of the Compose profile sets in the proposed order · ADR-004 · to decide at the "
                "team review (EN01-U1)", 1900, 530)
    d.node("host", 40, 80, 1820, 420, "Demonstration host", "Deployment node: one compose.yaml with profiles")

    d.node("core", 70, 100, 520, 345, "First", "Compose profile: core · eight containers", fill=NODE_IN)
    core = [("traefik", "Traefik 3.7", "box"), ("oauth2-proxy", "oauth2-proxy 7.15", "box"),
            ("keycloak", "Keycloak 26.8", "box"), ("client", "nginx", "box"),
            ("issue", "Spring Boot", "box"), ("dispatch", "Spring Boot", "box"),
            ("mysql", "MySQL 8.4 LTS", "db"), ("rabbitmq", "RabbitMQ 4.x", "queue")]
    for i, (name, tech, shape) in enumerate(core):
        d.container("c-" + name, 90 + 250 * (i % 2), 115 + 72 * (i // 2), 235, 62, name, tech, shape=shape)

    d.node("slice", 660, 100, 520, 345, "When the slice needs it", "Compose: no profile name yet", fill=NODE_IN)
    for i, (name, desc) in enumerate((("ai-triage-web", ["reporting works", "without it (NFR-03)"]),
                                      ("ai-triage-consumer", ["with ai-triage-web"]),
                                      ("notification", ["as soon as US-10", "is in the slice"]),
                                      ("calendar-sim", ["when dispatch", "books a visit"]))):
        d.container("l-" + name, 680 + 250 * (i % 2), 115 + 105 * (i // 2), 235, 92, name, None, desc)
    d.note(680, 345, 480, ["Memory of each set is not measured", "(EN01-U3, spike item 8)."])

    d.node("later", 1250, 100, 580, 345, "Later", "Compose profiles, own names", fill=NODE_IN)
    for i, (name, profile, desc) in enumerate((("mailpit", "profile demo", ["email channel only"]),
                                               ("gatus", "profile status (proposed)", ["/status page, banner"]),
                                               ("prometheus", "profile observability", []),
                                               ("grafana", "profile observability", []),
                                               ("garage", "profile storage (proposed)", ["before backup and restore"]))):
        d.container("x-" + name, 1270 + 280 * (i % 2), 115 + 90 * (i // 2), 260, 78, name, profile, desc)

    d.rel([(590, 270), (660, 270)], "then", at=(625, 258), anchor="middle", bg=NODE)
    d.rel([(1180, 270), (1250, 270)], "then", at=(1215, 258), anchor="middle", bg=NODE)
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
