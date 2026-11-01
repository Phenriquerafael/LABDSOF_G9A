"""Figures for DEVOPS-02 (observability and DR) as UML deployment diagrams.

Same drawing kit and style as documents/diagrams/physical-views (vpdraw.py,
copied here). Run `python3 devops_views.py`: it writes the seven SVG files
one folder up, with the names the markdown documents link to.
Sources: OBSERVABILITY.md, DR.md, ADR-004, ADR-012 and the physical views (P1,
P4, P5). Items not in ADR-004 are labelled "proposal" or "P-08".
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from vpdraw import Diagram, BLUE  # noqa: E402


def dr1():
    d = Diagram("dr-1-what-is-backed-up", "DR · What is backed up",
                "Deployment view of the data to protect · DR.md section 3 · proposal, nothing is backed up yet",
                1500, 720)
    d.node("app", 40, 90, 440, 420, "Application host", "device",
           ["Docker Compose · rebuilt from the image tag and Git"])
    for key, x, y, name in (("traefik", 60, 150, "traefik"), ("client", 270, 150, "client"),
                            ("issue", 60, 230, "issue"), ("dispatch", 270, 230, "dispatch"),
                            ("notification", 60, 310, "notification"), ("keycloak", 270, 310, "keycloak")):
        d.comp(key, x, y, 190, 56, name, "container")
    d.comp("rabbit", 60, 390, 400, 56, "rabbitmq (optional)", "container", ["definitions kept; messages via outbox"],
           dashed=True)

    d.node("db", 540, 90, 460, 420, "Database host", "device", ["backed up: the four service databases"])
    d.holder("mysql", 560, 150, 420, 170, "mysql", "container", ["MySQL 8.4 LTS · one database per service"])
    for i, owner in enumerate(("issue", "dispatch", "notification", "keycloak")):
        d.comp("db-" + owner, 572 + 100 * i, 200, 96, 60, owner, "database", icon="database")
    d.holder("garage", 560, 340, 420, 150, "garage", "container", ["Garage 2.5 · single node, no redundancy"])
    d.comp("attach", 575, 368, 220, 70, "bmc-attachments", "bucket", ["report photos, personal data", "copied nightly"],
           icon="artifact")

    d.node("bk", 1180, 90, 280, 420, "Backup host", "device", ["proposal, not in ADR-004"], dashed=True)
    d.holder("bgarage", 1200, 150, 240, 150, "garage", "container", ["Garage 2.5 · single node"])
    d.comp("bb", 1215, 195, 210, 70, "bmc-backups", "bucket", ["nightly dumps, checksum"], icon="artifact")

    d.comp("r2", 1180, 560, 280, 70, "Cloudflare R2", "external system", ["optional copy, not in the release"],
           dashed=True)
    d.comp("secrets", 40, 560, 440, 70, "Secrets store", "artifact", ["restored by hand, never from a dump"],
           icon="artifact")

    d.path([(1000, 235), (1215, 235)], "mysqldump\nnightly", at=(1108, 200), anchor="middle", bg=BLUE)
    d.dep([(140, 510), (140, 560)], "reads at start", at=(148, 540), anchor="start", bg=BLUE)
    d.dep([(480, 595), (770, 595), (770, 510)], "DB user, bucket key, app secrets", at=(625, 585), anchor="middle", bg=BLUE)
    d.dep([(480, 300), (540, 300)], "JDBC", at=(510, 288), anchor="middle", bg=BLUE)
    d.dep([(1290, 510), (1290, 560)], "optional", at=(1298, 530), bg=BLUE)
    d.note(40, 650, 1000, ["Backed up: the four service databases (outbox and Keycloak realm data included) and "
                           "the report photos in bmc-attachments.",
                           "Rebuilt from Git and the image tag: containers. Restored by hand: secrets, never from a dump."])
    return d


def dr2():
    d = Diagram("dr-2-backup-flow", "DR · Nightly backup flow",
                "Proposal following ADR-004 decision D2 · DR.md section 4.1 · not run yet",
                1000, 760)
    d.node("db", 40, 90, 600, 420, "Database host", "device", ["cron runs on the host, not in a container"])
    d.comp("cron", 70, 150, 220, 80, "nightly backup", "cron job", ["read-only backup user"])
    d.comp("mysql", 330, 150, 280, 80, "mysql", "container", ["MySQL 8.4 LTS"], icon="database")
    d.path([(290, 190), (330, 190)], "dump", at=(310, 170), anchor="middle", bg=BLUE)
    d.path([(180, 230), (180, 470), (910, 470), (910, 258)], "copy via Garage S3 API", at=(545, 458),
           anchor="middle", bg=BLUE)

    d.holder("photos", 310, 260, 300, 160, "garage", "container", ["Garage 2.5 · on the Database host"])
    d.comp("photos-bk", 330, 290, 260, 60, "bmc-attachments", "bucket", ["report photos, personal data"],
           icon="artifact")
    d.path([(460, 350), (460, 490), (940, 490), (940, 258)], "photos, nightly copy", at=(560, 508),
           anchor="middle", bg=BLUE)

    d.node("bk", 700, 90, 260, 200, "Backup host", "device", ["proposal, not in ADR-004"], dashed=True)
    d.holder("bgarage", 720, 150, 220, 130, "garage", "container", ["Garage 2.5"])
    d.comp("bb", 735, 172, 190, 50, "bmc-backups", "bucket", icon="artifact")

    d.note(40, 560, 900, ["1  mysqldump of each database with the read-only backup user; nothing is written back.",
                          "2  Compress the dump and write a SHA-256 checksum beside it.",
                          "3  Copy both files to bmc-backups with the bucket key from the host environment.",
                          "4  Copy new or changed photos to bmc-backups/attachments/ and write a checksum manifest.",
                          "5  Next night: restore the newest dump into a scratch container and compare row counts and",
                          "    the photo manifest; a failure raises an alert. Local copies older than a day are deleted."])
    return d


def dr3():
    d = Diagram("dr-3-restore-flow", "DR · Restore path",
                "Runbook steps 1 to 9 from DR.md section 6, placed on the machines they use · not tested yet",
                1400, 620)
    d.actor("operator", 150, 70, "Operator", [])
    d.node("bk", 40, 230, 300, 200, "Backup host", "device", ["the copy that survives a lost database host"],
           dashed=True)
    d.comp("bb", 70, 300, 240, 70, "bmc-backups", "bucket", ["2  newest dump that passes its checksum"],
           icon="artifact")

    d.node("db", 500, 200, 420, 280, "Database host (new or repaired)", "device")
    d.comp("mysql", 530, 260, 360, 80, "mysql", "container", ["3  empty container, same image tag", "5  load each dump"],
           icon="database")
    d.comp("checks", 530, 370, 360, 70, "integrity checks", "artifact", ["6  checksum, row counts, known records"],
           icon="artifact")

    d.node("app", 1000, 200, 360, 300, "Application host", "device", ["7 start in dependency order"])
    d.comp("kc", 1020, 260, 320, 50, "keycloak", "container", ["7a  first"])
    d.comp("svc", 1020, 330, 320, 50, "issue, dispatch, notification", "container", ["7b  then, each readiness checked"])
    d.comp("gw", 1020, 400, 320, 50, "traefik", "container", ["9  reopen writes, smoke journey"])

    d.dep([(310, 335), (420, 335), (420, 300), (530, 300)], "copy newest dump", at=(365, 325), anchor="middle",
          bg=BLUE)
    d.dep([(920, 330), (1000, 330)], "8 broker, if used", at=(960, 318), anchor="middle", bg=BLUE)
    d.dep([(710, 440), (710, 520), (190, 520), (190, 370)], "6 fails: choose an older dump (step 2)",
          at=(450, 508), anchor="middle", bg=BLUE)
    d.dep([(150, 120), (150, 230)], "1 freeze writes", at=(162, 190), anchor="start", bg=BLUE)
    d.note(40, 540, 1320, ["Steps 1 to 9 as in DR.md section 6. Step 4 restores secrets from the host environment or CI,",
                           "never from a dump. If the database host is lost without a Backup host, the bucket is lost too."])
    return d


def obs0():
    d = Diagram("observability-1-metrics", "Observability · Containers, metrics and data paths by layer",
                "Proposal from OBSERVABILITY.md · Traefik per ADR-004 · the database host and P-08 are open",
                1400, 1230)
    d.actor("user", 200, 70, "End user", ["uses the services"])
    d.actor("dev", 22, 590, "DEV", [])

    d.node("app", 40, 190, 1300, 700, "Application host", "device",
           ["Docker Compose · one Prometheus and one Grafana"])
    d.boundary("edge", 60, 230, 1260, 100, "Edge")
    d.comp("traefik", 180, 250, 160, 50, "traefik", "container", ["TLS, routes · /metrics"])
    d.boundary("svc", 60, 370, 1260, 160, "Services")
    for i, (key, name, detail, dashed) in enumerate((
            ("issue", "issue", "Spring Boot · /metrics", False),
            ("disp", "dispatch", "Spring Boot · /metrics", False),
            ("notif", "notification", "Spring Boot · /metrics", False),
            ("kc", "keycloak", "sign-in · /metrics", False),
            ("ai", "ai-triage", "classifies · /metrics", False),
            ("rmq", "rabbitmq", "internal · :15692 metrics", True))):
        d.comp(key, 80 + 200 * i, 400, 160, 70, name, "container", [detail], dashed=dashed)
    d.boundary("obs", 60, 580, 1260, 140, "Observability")
    d.comp("grafana", 180, 610, 160, 70, "grafana", "container", ["dashboards, alerts"])
    d.comp("prom", 430, 610, 200, 70, "prometheus", "container", ["scrapes every 30 s"])
    d.comp("bbx", 700, 610, 200, 70, "blackbox_exporter", "container", ["probes public URL via Traefik"],
           dashed=True)
    d.comp("nodeexp", 940, 610, 240, 70, "node_exporter", "container", ["host metrics (proposal)"],
           dashed=True)

    d.node("db", 40, 930, 1300, 170, "Database host", "device",
           ["MySQL and Garage"], align="left")
    d.comp("mysql", 180, 990, 200, 70, "mysql", "container", ["MySQL 8.4"], icon="database")
    d.comp("garage", 460, 990, 200, 70, "garage", "container", ["Garage 2.5"])
    d.comp("mysqld", 740, 990, 220, 70, "mysqld_exporter", "container", ["proposal, P-08"], dashed=True)

    d.dep([(200, 120), (200, 250)], "HTTPS 443", at=(208, 215), anchor="start", bg=BLUE)
    d.dep([(200, 300), (200, 400)], "routes to services", at=(208, 350), anchor="start", bg=BLUE)
    d.dep([(36, 650), (180, 650)], "SSH tunnel", at=(66, 638), anchor="start", bg=BLUE)
    d.dep([(380, 645), (430, 645)], "query", at=(405, 635), anchor="middle", bg=BLUE)
    d.dep([(530, 610), (530, 530)], "scrapes services", at=(538, 570), anchor="start", bg=BLUE)
    d.dep([(630, 700), (1060, 700), (1060, 680)], "scrapes host", at=(845, 692), anchor="middle", bg=BLUE)
    d.dep([(630, 640), (700, 640)], "scrapes", at=(665, 630), anchor="middle", bg=BLUE)
    d.dep([(850, 610), (850, 275), (340, 275)], "probes via Traefik", at=(600, 266), anchor="middle", bg=BLUE)
    d.dep([(600, 680), (600, 978), (850, 978), (850, 990)], "private link (P-08)", at=(610, 820),
          anchor="start", bg=BLUE)
    d.dep([(1260, 530), (1260, 855), (280, 855), (280, 990)], "JDBC: services to MySQL", at=(830, 847),
          anchor="middle", bg=BLUE)
    d.dep([(1290, 530), (1290, 880), (560, 880), (560, 990)], "S3 API: photos to Garage", at=(830, 872),
          anchor="middle", bg=BLUE)
    d.note(40, 1140, 1100, ["End users reach only the services, through Traefik. DEV reaches Grafana through an SSH tunnel (section 12).",
                            "Prometheus scrapes every 30 s: services, RabbitMQ, Traefik, host (proposal), blackbox, and the database exporter over P-08.",
                            "Items marked P-08 and the proposals are not in ADR-004."])
    return d


def obs2():
    d = Diagram("observability-2-requests-logs", "Observability · Requests, events and logs by layer",
                "Correlation ID: created at Traefik, carried in events (ADR-003) · OBSERVABILITY.md sections 4.1 and 4.2",
                1400, 900)
    d.actor("user", 200, 75, "End user", ["sends a request"])

    d.node("app", 40, 170, 1300, 600, "Application host", "device", ["Docker Compose"])
    d.boundary("edge", 60, 215, 1260, 90, "Edge")
    d.comp("traefik", 180, 240, 200, 50, "traefik", "container", ["creates X-Request-ID"])
    d.boundary("svc", 60, 310, 1260, 150, "Services")
    d.comp("issue", 120, 340, 200, 70, "issue", "container", ["logs JSON, publishes events"])
    d.comp("disp", 360, 340, 200, 70, "dispatch", "container", ["logs JSON, consumes events"])
    d.comp("notif", 600, 340, 200, 70, "notification", "container", ["logs JSON, consumes events"])
    d.comp("ai", 840, 340, 200, 70, "ai-triage", "container", ["logs JSON, consumes events"])
    d.comp("kc", 1080, 340, 200, 70, "keycloak", "container", ["sign-in, no events"])
    d.boundary("msg", 60, 490, 1260, 80, "Messaging")
    d.comp("rmq", 420, 505, 300, 50, "rabbitmq", "container", ["carries correlationid"])
    d.boundary("logs", 60, 600, 1260, 140, "Logs")
    d.comp("out", 860, 630, 240, 70, "container stdout", "artifact", ["Docker log stream, JSON lines"],
           icon="artifact")
    d.comp("loki", 520, 630, 220, 70, "Loki (optional)", "container", ["searchable by request_id"], dashed=True)

    d.dep([(200, 125), (200, 240)], "HTTPS 443", at=(208, 215), anchor="start", bg=BLUE)
    d.dep([(280, 290), (280, 340)], "REST, X-Request-ID", at=(288, 322), anchor="start", bg=BLUE)
    d.dep([(220, 410), (220, 530), (420, 530)], "event", at=(228, 470), anchor="start", bg=BLUE)
    d.dep([(480, 505), (480, 410)], "event", at=(488, 458), anchor="start", bg=BLUE)
    d.dep([(680, 505), (680, 410)], "event", at=(688, 458), anchor="start", bg=BLUE)
    d.dep([(720, 530), (940, 530), (940, 410)], "events", at=(830, 520), anchor="middle", bg=BLUE)
    d.dep([(1060, 490), (1060, 630)], "logs from every service", at=(1068, 560), anchor="start", bg=BLUE)
    d.dep([(860, 665), (780, 665)], "optional", at=(820, 655), anchor="middle", bg=BLUE)

    d.note(40, 800, 1260, ["Services do not call each other over HTTP (ADR-001); they exchange events through RabbitMQ, which carry",
                           "correlationid and traceparent (ADR-003). Outbound calls to Google Calendar and the AI provider also carry the ID in HTTP headers (not drawn).",
                           "Loki is optional; without it, logs are read with docker logs."])
    return d


def obs3():
    d = Diagram("observability-3-alerts-errors", "Observability · Alerts and errors by layer",
                "Alerts leave the hosts through a chat channel webhook · errors are logged, not sent to a third party",
                1400, 1040)

    d.node("app", 40, 90, 1040, 520, "Application host", "device", ["Docker Compose"])
    d.boundary("svc", 60, 150, 1000, 160, "Services")
    d.comp("issue", 90, 185, 240, 80, "issue", "container", ["errors as JSON logs", "errors_total counter"])
    d.comp("disp", 400, 185, 240, 80, "dispatch", "container", ["errors as JSON logs", "errors_total counter"])
    d.comp("notif", 710, 185, 240, 80, "notification", "container", ["errors as JSON logs", "errors_total counter"])
    d.boundary("obs", 60, 350, 1000, 240, "Observability")
    d.comp("prom", 90, 390, 260, 80, "prometheus", "container", ["up series per target", "errors_total, disk"])
    d.comp("grafana", 420, 390, 260, 80, "grafana", "container", ["alert rules (Page and Warn)"])

    d.node("db", 40, 650, 1040, 170, "Database host", "device", ["no up series yet (P-08)"], align="left")
    d.comp("mysqld", 90, 710, 240, 80, "mysqld_exporter", "container", ["proposal, P-08"], dashed=True)
    d.comp("garage", 400, 710, 240, 80, "garage", "container", ["metrics unverified"], dashed=True)
    d.comp("cron", 710, 710, 240, 80, "nightly backup", "cron job", ["failure posts to chat channel"])

    d.comp("webhook", 1160, 380, 210, 80, "Alert channel webhook", "external system", ["chat channel"])
    d.comp("uptime", 1160, 200, 210, 80, "External uptime check", "external system", ["runs outside both hosts"])
    d.comp("heartbeat", 1160, 690, 210, 80, "Heartbeat service", "external system", ["expects one request a day"])

    d.dep([(300, 310), (300, 390)], "scrapes services", at=(308, 352), anchor="start", bg=BLUE)
    d.dep([(680, 430), (1160, 430)], "alert rules fire", at=(920, 418), anchor="middle", bg=BLUE)
    d.dep([(1265, 280), (1265, 380)], "down", at=(1273, 330), anchor="start", bg=BLUE)
    d.dep([(210, 470), (210, 710)], "P-08: scrape not defined", at=(218, 600), anchor="start", bg=BLUE)
    d.dep([(950, 750), (1160, 730)], "daily request (HTTPS)", at=(1000, 690), anchor="start", bg=BLUE)
    d.note(40, 850, 660, ["Page (wake someone up)",
                          "Target down: up == 0 for 2 minutes",
                          "Site unreachable: blackbox probe fails for 2 minutes",
                          "High error rate: 5xx above 5% for 5 minutes",
                          "Auth unavailable: /readyz failing for 2 minutes",
                          "Backup run missing: no heartbeat request (proposal)",
                          "Backup job failed: chat message from the job (proposal)",
                          "No consumers: a queue with none, RabbitMQ only"])
    d.note(720, 850, 640, ["Warn (review in working hours)",
                           "Degraded mode active for 1 minute",
                           "Dependency failing: success under 90% for 5 minutes",
                           "Latency SLO breach: p95 above target for 10 minutes",
                           "Disk filling: predicted to fill within 24 hours",
                           "Memory low: under 10% available for 10 minutes",
                           "Container restarting: more than 2 in 15 minutes",
                           "Broker queue growing; dead letters not empty (RabbitMQ only)"])
    return d


def main():
    out = HERE.parent
    for make in (dr1, dr2, dr3, obs0, obs2, obs3):
        d = make()
        (out / f"{d.name}.svg").write_text(d.svg(), encoding="utf-8")
        print("wrote", out / f"{d.name}.svg")


if __name__ == "__main__":
    main()
