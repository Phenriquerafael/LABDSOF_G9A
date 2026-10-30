# Physical view sources

Sources for the seven physical (deployment) views of [07b — Physical views](../../07b-physical-views.md). The text of that document is the authority; these files only draw it, from [ADR-004](../../adr/ADR-004-deployment-contract.md) and the ADRs it references.

| Function in `views.py` | Figure | Subject |
|---|---|---|
| `p1()` | P1 | Host, the seventeen containers grouped by network, the Traefik routes, external nodes |
| `p2()` | P2 | Traefik routes and middlewares, both trust boundaries, never-routed endpoints |
| `p3()` | P3 | Publishers, `bmc.events`, quorum queues, dead-lettering, consumers |
| `p4()` | P4 | One database per service, Garage buckets, SMTP, calendar, Keycloak Admin API, backup job |
| `p5()` | P5 | Gatus checks, Prometheus scrapes, Grafana, the public status page |
| `p6()` | P6 | Laptop → GitHub → Actions stages → GHCR → host, secrets |
| `p7()` | P7 | Compose profile sets in the proposed rollout order |

The figures are [C4](https://c4model.com/) deployment diagrams in the Visual Paradigm palette of the team's other diagrams: three-dimensional deployment nodes with the name at the bottom left, container instances labelled `[Container: technology]`, cylinders for databases and queues, dashed boundaries, UML notes and relationships labelled with `[protocol]`. `vpdraw.py` holds the shapes and palette; `views.py` places every shape by hand, so a picture changes only when its source changes. Every figure has a title and a subtitle naming its scope and sources; P1 carries a key.

## Rendering

```bash
cd documents/diagrams/physical-views
python3 views.py          # writes the seven .svg files
CHROME=/path/to/chrome-headless-shell python3 views.py --png   # also the .png files
```

The SVG step needs only Python 3 (standard library). The PNG step screenshots each SVG at twice its size with a headless Chromium; the images in this folder were rendered on 2026-10-30 with Python 3.13 and Playwright's `chrome-headless-shell` build 1248. Labels use Arial, falling back to Liberation Sans or Helvetica, so line widths can shift slightly where none of them is installed.

## Conventions

| Element | Meaning |
|---|---|
| Three-dimensional box, name at the bottom left | A C4 deployment node: the user device, GitHub, the Docker host, a Compose network grouping (lighter cyan), a runner, or a container drawn open to show what is inside it (traefik, rabbitmq, mysql, garage; yellow) |
| Yellow rounded box | A container instance (one image, one Compose service): name in bold, `[Container: technology]`, then its role |
| Pale yellow shape inside a container | Something that runs inside it: a Traefik middleware, a RabbitMQ exchange or queue, a database, a bucket, a CI stage |
| Cylinder | A database; a horizontal cylinder is a queue |
| Green box or person | A person or a system outside the BMC deployment: the operator, GHCR, the AI provider, the off-host backup copy |
| Dashed rectangle | A boundary: red for a trust boundary, grey for a set of routes or checks |
| Note with a folded corner | An open item of [07b §10](../../07b-physical-views.md#10-open-items-found-while-drawing-the-views), a limit or a source, joined to its subject by a dashed line |
| Solid arrow | A relationship the design requires, labelled with what it does and `[protocol]`, from the side that opens it to the side that serves it (P3 and P6 follow the message or the image instead, as their subtitles say; in P7 the arrows give the rollout order) |
| Dashed arrow or border | Optional, administrative, not yet placed or still open, or a dead-letter path |

Nothing here may state a technology, version or placement that an ADR does not state. The `.svg` files are the primary images used by the document; the `.png` files are the same picture as a raster fallback.

## Tooling note

The notation is C4 and the colours are Visual Paradigm's, but the files are not Visual Paradigm projects: no `.vpp` file exists and the figures were not opened in Visual Paradigm.
