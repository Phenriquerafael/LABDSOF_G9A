# Physical view sources

Editable sources for the seven physical (deployment) views of [07b — Physical views](../../07b-physical-views.md). The text of that document is the authority; these files only draw it, from [ADR-004](../../adr/ADR-004-deployment-contract.md) and the ADRs it references.

| Source | Figure | Subject |
|---|---|---|
| `p1-deployment-overview.puml` | P1 | Host, the seventeen containers grouped by network, external nodes |
| `p2-edge-and-trust.puml` | P2 | Traefik routes, middlewares, the edge trust boundary, never-routed endpoints |
| `p3-messaging.puml` | P3 | Publishers, `bmc.events`, quorum queues, dead-lettering, consumers |
| `p4-data-and-platform.puml` | P4 | One database per service, Garage buckets, SMTP, calendar, Keycloak Admin API, backup job |
| `p5-health-and-metrics.puml` | P5 | Gatus checks, Prometheus scrapes, Grafana, the public status page |
| `p6-delivery-path.puml` | P6 | Laptop → GitHub → Actions stages → GHCR → host, secrets |
| `p7-compose-profiles.puml` | P7 | Compose profile sets in the proposed rollout order |

Each `.puml` is self-contained: it carries its own `skinparam` block, so it can be pasted into an editor on its own. `!pragma layout elk` makes PlantUML use the ELK layout engine; the `top to bottom direction` and the declared order of the elements drive the result, so moving a block changes the picture.

## Rendering

The images in this folder were produced with PlantUML 1.2024.8 and a Java runtime:

```bash
cd documents/diagrams/physical-views
java -jar plantuml.jar -tsvg p1-deployment-overview.puml   # primary export
java -jar plantuml.jar -tpng p1-deployment-overview.puml   # raster fallback
```

Pass one `-t` flag per run: PlantUML honours only the last one, so `-tsvg -tpng` writes PNG only. Omit the file name to render every `.puml` in the folder.

The output file name follows the `@startuml <name>` line, not the file name, so keep the two in step. ELK needs no Graphviz installation; a plain `-tsvg` run without the pragma would need `dot` instead.

## Conventions

- Colours carry meaning, not decoration: blue for edge, green for BMC services, amber for platform components and demo aids, teal for observability, violet for data stores.
- Solid arrows are connections the design requires; dashed arrows are optional, later, administrative or still open. When a view would need many parallel edges, the source lists the items in an `artifact` block instead — for example the public routes in P2 and the checks in P5.
- Nothing here may state a technology, version or placement that an ADR does not state. Details this folder needs but the ADRs leave open are listed as P-01 to P-07 in [07b §10](../../07b-physical-views.md#10-open-items-found-while-drawing-the-views).
- The `.svg` files are the primary images used by the document; the `.png` files are the same picture as a raster fallback.

## Tooling limitation

Visual Paradigm's Code editor (VPasCode) was the intended tool for this rework and could not be operated in the session that produced these files (the desktop browser was disconnected). The sources are standard PlantUML and have not been opened in VPasCode; no `.vpp` file exists.
