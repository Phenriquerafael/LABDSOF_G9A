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
    d = Diagram("observability-0-containers", "Observability · Containers and hosts",
                "Proposal from OBSERVABILITY.md · Traefik per ADR-004 · the database host and P-08 are open",
                1500, 840)
    d.comp("uptime", 1200, 100, 260, 70, "External uptime check", "external system", ["runs outside both hosts"])
    d.comp("discord", 1200, 220, 260, 70, "Discord webhook", "external system", ["alerts"])
    d.comp("sentry", 1200, 340, 260, 70, "Sentry (hosted)", "external system", ["error reports, scrubbed"])

    d.node("app", 40, 130, 1040, 430, "Application host", "device", ["Docker Compose · Traefik, services, observability"])
    d.comp("grafana", 70, 200, 200, 60, "grafana", "container", ["dashboards and alerts"])
    d.comp("prom", 330, 200, 220, 60, "prometheus", "container", ["scrapes every 30 s"])
    d.comp("traefik", 70, 300, 200, 60, "traefik", "container", ["gateway, TLS"])
    d.comp("issue", 330, 300, 190, 60, "issue", "container", ["Spring Boot"])
    d.comp("dispatch", 540, 300, 190, 60, "dispatch", "container", ["Spring Boot"])
    d.comp("notif", 750, 300, 190, 60, "notification", "container", ["Spring Boot"])
    d.comp("kc", 330, 400, 190, 60, "keycloak", "container", ["sign-in"])
    d.comp("ai", 540, 400, 190, 60, "ai-triage", "container", ["classifies"])
    d.comp("rmq", 750, 400, 190, 60, "rabbitmq", "container", ["under consideration"], dashed=True)

    d.node("db", 40, 600, 1040, 150, "Database host", "device",
           ["MySQL and Garage; private link to the application host (P-08)"])
    d.comp("mysql", 330, 690, 190, 60, "mysql", "container", ["MySQL 8.4"], icon="database")
    d.comp("garage", 540, 690, 190, 60, "garage", "container", ["Garage 2.5"])
    d.comp("mysqld", 750, 690, 190, 60, "mysqld_exporter", "container", ["proposal, P-08"], dashed=True)

    d.dep([(270, 230), (330, 230)], "query", at=(300, 220), anchor="middle", bg=BLUE)
    d.path([(600, 560), (600, 600)], "private link (P-08)", at=(608, 580), anchor="start", bg=BLUE, dashed=True)
    d.note(40, 780, 1100, ["The operator reads Grafana over an SSH tunnel or Traefik sign-in (section 12).",
                           "Items marked P-08 are not in ADR-004. Metrics paths: observability-1-metrics.svg.",
                           "OBSERVABILITY.md text still says nginx where this figure shows Traefik."])
    return d


def obs1():
    d = Diagram("observability-1-metrics", "Observability · Metrics paths",
                "Prometheus pulls from each target · OBSERVABILITY.md section 4.4 · P-08 and proposals are marked",
                1500, 720)
    d.comp("grafana", 60, 200, 200, 70, "grafana", "container", ["dashboards and alerts"])
    d.comp("prom", 340, 200, 240, 70, "prometheus", "container", ["scrapes every 30 s", "keeps 15 days"])
    d.path([(260, 235), (340, 235)], "query", at=(300, 222), anchor="middle", bg=BLUE)

    d.node("app", 40, 90, 1420, 420, "Application host", "device",
           ["Docker Compose · Prometheus and Grafana run here, next to the services"])
    d.comp("svc", 690, 150, 230, 60, "issue, dispatch, notification", "container", ["/metrics on each service"])
    d.comp("rmq", 690, 250, 230, 60, "rabbitmq", "container", ["plugin metrics, port 15692"])
    d.comp("nodeexp", 690, 350, 230, 60, "node_exporter, cAdvisor", "container", ["proposal; host and containers"],
           dashed=True)
    d.comp("tr", 960, 150, 230, 60, "traefik", "container", ["metrics; health check"])
    d.comp("bb", 960, 250, 230, 60, "blackbox_exporter", "container", ["probes public URL (proposal)"], dashed=True)

    d.node("db", 660, 540, 800, 150, "Database host", "device", ["P-08: not in ADR-004"])
    d.comp("mysqld", 690, 615, 230, 50, "mysqld_exporter", "container", ["proposal, P-08"], dashed=True)
    d.comp("garage", 960, 615, 230, 50, "garage", "container", ["metrics endpoint unverified"], dashed=True)

    d.dep([(580, 235), (690, 180)])
    d.dep([(580, 235), (690, 280)])
    d.dep([(580, 235), (690, 380)])
    d.dep([(580, 235), (620, 235), (620, 640), (690, 640)], "private link (P-08)", at=(628, 470), anchor="start",
          bg=BLUE)
    d.note(60, 330, 500, ["Scrape interval 30 seconds, 15-day retention (OBSERVABILITY-configs.md).",
                          "Prometheus stays on the application host: one Prometheus, one Grafana.",
                          "The 'service gone' alert uses the up series of each target."])
    return d


def obs2():
    d = Diagram("observability-2-requests-logs", "Observability · Requests and logs",
                "Correlation ID created at the gateway and forwarded · OBSERVABILITY.md sections 4.1 and 4.2",
                1500, 600)
    d.actor("client", 120, 60, "Browser", ["sends a request"])
    d.node("app", 300, 100, 1000, 400, "Application host", "device", ["Docker Compose"])
    d.comp("traefik", 320, 170, 200, 70, "traefik", "container", ["creates X-Request-ID"])
    d.comp("issue", 640, 170, 200, 70, "issue", "container", ["logs JSON, forwards ID"])
    d.comp("disp", 900, 170, 200, 70, "dispatch", "container", ["logs JSON, forwards ID"])
    d.comp("out", 640, 330, 200, 60, "container stdout", "artifact", ["JSON lines, one per event"], icon="artifact")
    d.comp("loki", 1340, 300, 140, 90, "Loki (optional)", "container", ["by request_id"], dashed=True)

    d.dep([(120, 90), (120, 205), (320, 205)], "HTTPS 443", at=(150, 195), anchor="start", bg=BLUE)
    d.dep([(520, 205), (640, 205)], "X-Request-ID", at=(580, 190), anchor="middle", bg=BLUE)
    d.dep([(840, 205), (900, 205)])
    d.dep([(740, 240), (740, 330)], "logs", at=(748, 290), anchor="start", bg=BLUE)
    d.dep([(840, 360), (1340, 345)], "optional", at=(1090, 340), anchor="middle", bg=BLUE, )
    d.note(40, 520, 1200, ["The ID is created at the gateway, returned to the client, and forwarded by every service.",
                           "OpenTelemetry (traceparent) is the upgrade path (OBSERVABILITY.md section 4.2).",
                           "Text still says nginx for the gateway; ADR-004 and this figure say Traefik."])
    return d


def obs3():
    d = Diagram("observability-3-alerts-errors", "Observability · Alerts and errors",
                "Alerts leave the hosts through the Discord webhook · OBSERVABILITY.md sections 4.5 and 7",
                1500, 640)
    d.node("app", 40, 100, 820, 300, "Application host", "device")
    d.comp("prom", 80, 160, 200, 70, "prometheus", "container", ["up series per target"])
    d.comp("grafana", 330, 160, 200, 70, "grafana", "container", ["alert rules"])
    d.comp("issue", 80, 300, 200, 70, "issue", "container", ["errors to Sentry"])
    d.comp("disp", 330, 300, 200, 70, "dispatch", "container", ["errors to Sentry"])

    d.node("db", 40, 440, 820, 130, "Database host", "device", ["P-08: no up series yet"])
    d.comp("mysqld", 80, 505, 200, 50, "mysqld_exporter", "container", ["proposal"], dashed=True)
    d.comp("garage", 330, 505, 200, 50, "garage", "container", ["unverified"], dashed=True)

    d.comp("discord", 1100, 160, 300, 70, "Discord webhook", "external system", ["alert messages"])
    d.comp("uptime", 1100, 300, 300, 70, "External uptime check", "external system", ["down: outside both hosts"])
    d.comp("sentry", 1100, 440, 300, 70, "Sentry (hosted)", "external system", ["stack traces, scrubbed"])

    d.dep([(530, 195), (1100, 195)], "alert rule fires", at=(800, 185), anchor="middle", bg=BLUE)
    d.dep([(1250, 300), (1250, 230)], "down", at=(1258, 270), anchor="start", bg=BLUE)
    d.dep([(530, 335), (900, 335), (900, 475), (1100, 475)], "errors, scrubbed", at=(930, 465), anchor="start",
          bg=BLUE)
    d.note(40, 580, 1000, ["Alerts: a target's up series is missing; disk above threshold; nightly backup missing or failed "
                           "(DR.md section 4.1).",
                           "Not covered yet: MySQL and Garage have no up series (P-08)."])
    return d


def main():
    out = HERE.parent
    for make in (dr1, dr2, dr3, obs0, obs1, obs2, obs3):
        d = make()
        (out / f"{d.name}.svg").write_text(d.svg(), encoding="utf-8")
        print("wrote", out / f"{d.name}.svg")


if __name__ == "__main__":
    main()
