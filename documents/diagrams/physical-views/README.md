# Physical view sources

Sources for the seven physical (deployment) views of [07b — Physical views](../../07b-physical-views.md). The text of that document is the authority; these files only draw it, from [ADR-004](../../adr/ADR-004-deployment-contract.md) and the ADRs it references.

| Function in `views.py` | Figure | Subject |
|---|---|---|
| `p1()` | P1 | Host, the seventeen containers grouped by network, the Traefik routes, external nodes |
| `p2()` | P2 | The edge request path: Traefik rules, ForwardAuth, StripPrefix, refused requests, both trust boundaries |
| `p3()` | P3 | Publishers, `bmc.events`, quorum queues, dead-lettering, consumers |
| `p4()` | P4 | One database per service, Garage buckets, SMTP, calendar, Keycloak Admin API, backup job |
| `p5()` | P5 | Gatus checks, Prometheus scrapes, Grafana, the public status page |
| `p6()` | P6 | Laptop → GitHub → Actions stages → GHCR → host, secrets |
| `p7()` | P7 | Compose profile sets in the proposed rollout order |

The figures use the Visual Paradigm BPMN look of the team's other diagrams: a pool with a vertical title band, horizontal lanes, rounded elements with a type icon in the corner, orange diamonds for routing decisions, green start and red end events, and bracket annotations joined by a dotted line. `vpdraw.py` holds the drawing primitives and palette; `views.py` places every shape by hand, so a picture changes only when its source changes.

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
| Pool (cyan, title band on the left) | The scope of the view: the host, outside the host, or the path the view follows |
| Lane | A Compose network grouping in P1; a stage, a role or a trust boundary elsewhere, as its label says |
| Yellow rounded element | A container or an item that runs on the host; the first line is its name |
| Green rounded element | A node outside the Docker host: user device, GHCR, AI provider, R2 |
| Light-cyan box with a title | A grouping inside a lane: a MySQL instance, Garage buckets, the CI stages, a profile set |
| Corner icon | Three-dimensional box: container · cylinder: database · bars: queue · bucket: Garage bucket or the Garage container · cloud: external service · gear: a step or middleware · page: a list of checks or a configuration source · person or phone: a reader |
| Orange diamond | A routing decision: a Traefik rule or session check in P2, an exchange in P3 |
| Green circle / red circle | Where a request or flow starts / where it ends or is refused |
| Solid arrow | A connection the design requires, from the side that opens it to the side that serves it (P3 and P6 follow the message or the image instead) |
| Dashed arrow or border | Optional, administrative, not yet placed or still open, or a dead-letter path |
| Bracket with a dotted line | An annotation: an open item (P-01 to P-07 in [07b §10](../../07b-physical-views.md#10-open-items-found-while-drawing-the-views)), a limit or a source |

Nothing here may state a technology, version or placement that an ADR does not state. The `.svg` files are the primary images used by the document; the `.png` files are the same picture as a raster fallback.

## Tooling note

The look follows the Visual Paradigm palette, but the files are not Visual Paradigm projects: no `.vpp` file exists and the figures were not opened in Visual Paradigm.
