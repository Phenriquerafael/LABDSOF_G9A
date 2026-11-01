# Physical view sources

Sources for the seven physical (deployment) views of [07b — Physical views](../../07b-physical-views.md). The text of that document is the authority; these files only draw it, from [ADR-004](../../adr/ADR-004-deployment-contract.md) and the ADRs it references.

| Function in `views.py` | Figure | Subject |
|---|---|---|
| `p1()` | P1 | Application host with twelve services by network, database and backup hosts, the private link, the `egress` network, external nodes |
| `p2()` | P2 | Traefik routes and middlewares, the OIDC plugin, both trust boundaries, never-routed endpoints |
| `p3()` | P3 | Publishers, `bmc.events`, quorum queues, dead-lettering, consumers |
| `p4()` | P4 | Database host (MySQL, one database per service, Garage, backup cron) and backup host (`bmc-backups`) |
| `p5()` | P5 | Compose and Traefik health checks, Prometheus scrapes, Grafana, the database host and P-08; the deferred status page |
| `p6()` | P6 | Laptop → GitHub → Actions stages → GHCR → host, secrets |
| `p7()` | P7 | Compose profile sets in the proposed rollout order |

The figures are UML deployment diagrams in the style Visual Paradigm gives them: one blue fill (`#83C6EF`), black outlines, three-dimensional nodes with a bold name under a «stereotype» at the top, components with the component icon, provided interfaces as lollipops, plain communication paths labelled with the protocol, and dashed dependency arrows. `vpdraw.py` holds the shapes; `views.py` places every shape by hand, so a picture changes only when its source changes. Every figure has a title and a subtitle naming its scope and sources; P1 carries a key.

## Rendering

```bash
cd documents/diagrams/physical-views
python3 views.py          # writes the seven .svg files
CHROME=/path/to/chrome-headless-shell python3 views.py --png   # also the .png files
```

The SVG step needs only Python 3 (standard library). The PNG step screenshots each SVG at twice its size with a headless Chromium; the images in this folder were rendered on 2026-11-01 with Python 3.13 and Playwright's `chrome-headless-shell` build 1248. Labels use Arial, falling back to Liberation Sans or Helvetica, so line widths can shift slightly where none of them is installed.

## Conventions

| Element | Meaning |
|---|---|
| Three-dimensional box, name at the top | A UML node: «device» for the user device and the application, database and backup hosts, «network» for a Compose network grouping, «executionEnvironment» for the browser, the CI runners or Docker Compose, «profile set» in P7, «external system» outside the host (Google Calendar, the AI provider, R2) |
| Rectangle with the component icon | A «container» (one image, one Compose service), or a part of one: «entrypoint» and «middleware» in Traefik, «exchange» and «queue» in RabbitMQ, «bucket» in Garage, «job» in CI, «cron job» for the backup on the database host. A container drawn open shows its parts and has its name at the bottom left |
| Rectangle with the cylinder or page icon | A «database», or an «artifact» such as the working copy or the `.env` file |
| Ball on a stick (lollipop) | An interface the component provides: HTTPS 443 on Traefik, AMQP, S3 API, SMTP, Admin API, HTTP API |
| Stick figure | An actor: the operator |
| Dashed rectangle | A boundary: a trust boundary, or a set of routes or checks (not a UML element) |
| Note with a folded corner | An open item of [07b §10](../../07b-physical-views.md#10-open-items-found-while-drawing-the-views), a limit or a source, anchored by a dashed line |
| Solid line | A communication path, labelled with the route or protocol; no arrow, as UML draws it |
| Dashed arrow | A dependency or information flow, from the user to what it uses; in P3 it follows the message, in P6 the code and images, in P7 the rollout order |
| Dashed outline | Optional or only if needed: the off-host backup copy, `blackbox_exporter`, Grafana access in demo |

Nothing here may state a technology, version or placement that an ADR does not state. The `.svg` files are the primary images used by the document; the `.png` files are the same picture as a raster fallback.

## Tooling note

The notation is UML and the look is Visual Paradigm's, but the files are not Visual Paradigm projects: no `.vpp` file exists and the figures were not opened in Visual Paradigm.
