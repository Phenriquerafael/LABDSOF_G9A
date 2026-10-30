"""Small SVG kit for the BMC physical views as C4 deployment diagrams.

Draws deployment nodes, containers, databases, queues, people, external
systems, boundaries, UML notes and orthogonal relationships in the Visual
Paradigm palette used by the team's other diagrams. Coordinates are absolute
pixels; every view in views.py places its shapes by hand.
"""

from html import escape

FONT = "Arial, 'Liberation Sans', Helvetica, sans-serif"

NODE = "#87DCF5"       # deployment node: host, device, platform
NODE_IN = "#BDEBFA"    # a deployment node nested in another: network, runner
ELEMENT = "#EEF57A"    # container instance
PART = "#F7FAC4"       # something inside a container: middleware, queue, database
EXTERNAL = "#C3F57A"   # person or system outside the BMC deployment
NOTE = "#FFFFFF"
BOUNDARY = "#C0392B"   # trust boundary
INK = "#000000"
GREY = "#333333"
LINE = 15


def _shade(hex_colour, factor=0.82):
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % (int(r * factor), int(g * factor), int(b * factor))


def _lines_svg(x, y, rows, anchor="middle"):
    """rows: list of (text, size, weight, colour, italic); first row baseline-centred at y."""
    out = []
    for i, (text, size, weight, colour, italic) in enumerate(rows):
        style = ' font-style="italic"' if italic else ""
        out.append(f'<text x="{x}" y="{y + i * LINE}" font-size="{size}" font-weight="{weight}" '
                   f'fill="{colour}" text-anchor="{anchor}" dominant-baseline="central"{style}>'
                   f'{escape(text)}</text>')
    return "".join(out)


def _c4_rows(name, tech, desc):
    rows = [(name, 14, "bold", INK, False)]
    if tech:
        rows.append((f"[{tech}]", 11, "normal", GREY, False))
    rows += [(line, 12, "normal", INK, False) for line in desc]
    return rows


class Diagram:
    def __init__(self, name, title, subtitle, width, height):
        self.name, self.title = name, title
        self.width, self.height = width, height
        self.back, self.edges, self.front = [], [], []
        self.shapes = {}
        self.front.append(_lines_svg(20, 28, [(title, 18, "bold", INK, False)], anchor="start"))
        self.front.append(_lines_svg(20, 50, [(subtitle, 12, "normal", GREY, False)], anchor="start"))

    # ---- deployment nodes and boundaries -----------------------------------
    def node(self, key, x, y, w, h, name, tech, fill=NODE, dashed=False):
        """A UML/C4 deployment node: a three-dimensional box, name and
        technology at the bottom left (the C4 convention)."""
        d = 12
        dash = ' stroke-dasharray="8 5"' if dashed else ""
        s = f'stroke="{INK}" stroke-width="1.6"{dash}'
        target = self.back
        target.append(f'<path d="M{x} {y} l{d} {-d} h{w} l{-d} {d} z" fill="{_shade(fill, 0.9)}" {s}/>')
        target.append(f'<path d="M{x+w} {y} l{d} {-d} v{h} l{-d} {d} z" fill="{_shade(fill)}" {s}/>')
        target.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" {s}/>')
        rows = [(name, 13, "bold", INK, False)] + [(f"[{t}]", 11, "normal", GREY, False) for t in tech.split("\n")]
        target.append(_lines_svg(x + 12, y + h - 14 - (len(rows) - 1) * LINE, rows, anchor="start"))
        self.shapes[key] = (x, y, w, h)

    def boundary(self, key, x, y, w, h, label, colour=BOUNDARY):
        """A dashed boundary, label at the bottom left: a trust boundary or a set."""
        self.back.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="none" '
                         f'stroke="{colour}" stroke-width="2" stroke-dasharray="10 6"/>')
        self.back.append(_lines_svg(x + 12, y + h - 16, [(label, 12, "bold", colour, False)], anchor="start"))
        self.shapes[key] = (x, y, w, h)

    # ---- elements -----------------------------------------------------------
    def container(self, key, x, y, w, h, name, tech, desc=(), shape="box", fill=ELEMENT, dashed=False):
        """A C4 element: name in bold, [technology], short description.

        shape: box (container), db (cylinder), queue (horizontal cylinder),
        person (C4 person) or system (external system box).
        """
        dash = ' stroke-dasharray="8 5"' if dashed else ""
        s = f'stroke="{INK}" stroke-width="1.8"{dash}'
        rows = _c4_rows(name, tech, desc)
        top = y + h / 2 - (len(rows) - 1) * LINE / 2
        if shape == "db":
            e = 9
            self.front.append(f'<path d="M{x} {y+e} a{w/2} {e} 0 0 1 {w} 0 v{h-2*e} a{w/2} {e} 0 0 1 {-w} 0 z" '
                              f'fill="{fill}" {s}/>')
            self.front.append(f'<path d="M{x} {y+e} a{w/2} {e} 0 0 0 {w} 0" fill="none" {s}/>')
            top += e / 2
        elif shape == "queue":
            e = 12
            self.front.append(f'<path d="M{x+e} {y} h{w-2*e} a{e} {h/2} 0 0 1 0 {h} h{-(w-2*e)} '
                              f'a{e} {h/2} 0 0 1 0 {-h} z" fill="{fill}" {s}/>')
            self.front.append(f'<path d="M{x+w-e} {y} a{e} {h/2} 0 0 0 0 {h}" fill="none" {s}/>')
        elif shape == "person":
            r = 18
            self.front.append(f'<circle cx="{x+w/2}" cy="{y+r}" r="{r}" fill="{fill}" {s}/>')
            self.front.append(f'<rect x="{x}" y="{y+2*r-4}" width="{w}" height="{h-2*r+4}" rx="18" fill="{fill}" {s}/>')
            top = y + 2 * r + (h - 2 * r) / 2 - (len(rows) - 1) * LINE / 2
        else:
            rx = 4 if shape == "system" else 10
            self.front.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {s}/>')
        self.front.append(_lines_svg(x + w / 2, top, rows))
        self.shapes[key] = (x, y, w, h)

    def note(self, x, y, w, lines, attach=None):
        """A UML note with a folded corner, joined to its subject by a dashed line."""
        h = len(lines) * LINE + 16
        f = 12
        if attach:
            ax, ay = attach
            tx = x if ax < x else x + w if ax > x + w else ax
            ty = y + h / 2 if tx != ax else (y if ay < y else y + h)
            self.edges.append(f'<path d="M{ax} {ay} L{tx} {ty}" stroke="{INK}" stroke-width="1.2" '
                              f'stroke-dasharray="4 4" fill="none"/>')
        self.front.append(f'<path d="M{x} {y} h{w-f} l{f} {f} v{h-f} h{-w} z" fill="{NOTE}" '
                          f'stroke="{INK}" stroke-width="1.4"/>')
        self.front.append(f'<path d="M{x+w-f} {y} v{f} h{f}" fill="none" stroke="{INK}" stroke-width="1.4"/>')
        rows = [(line, 12, "normal", INK, False) for line in lines]
        self.front.append(_lines_svg(x + 10, y + 8 + LINE / 2, rows, anchor="start"))

    # ---- relationships ------------------------------------------------------
    def p(self, key, side, t=0.5):
        """A point on a side of a shape: n, s, e or w, at fraction t along it."""
        x, y, w, h = self.shapes[key]
        return {"n": (x + w * t, y), "s": (x + w * t, y + h),
                "w": (x, y + h * t), "e": (x + w, y + h * t)}[side]

    def rel(self, points, label=None, at=None, dashed=False, anchor="start", bg="#FFFFFF"):
        """An orthogonal relationship with rounded bends; the label gets a
        halo in the colour of the area it sits on."""
        d = f"M{points[0][0]} {points[0][1]}"
        for i in range(1, len(points) - 1):
            (x0, y0), (x1, y1), (x2, y2) = points[i - 1], points[i], points[i + 1]
            r = min(8, (abs(x1 - x0) + abs(y1 - y0)) / 2, (abs(x2 - x1) + abs(y2 - y1)) / 2)
            ux, uy = _unit(x1 - x0, y1 - y0)
            vx, vy = _unit(x2 - x1, y2 - y1)
            d += f" L{x1 - ux*r} {y1 - uy*r} Q{x1} {y1} {x1 + vx*r} {y1 + vy*r}"
        d += f" L{points[-1][0]} {points[-1][1]}"
        dash = ' stroke-dasharray="8 6"' if dashed else ""
        self.edges.append(f'<path d="{d}" stroke="{INK}" stroke-width="1.8" fill="none"{dash} '
                          f'marker-end="url(#arrow)"/>')
        if label:
            rows = [(line, 12 if i == 0 else 11, "normal", INK if i == 0 else GREY, False)
                    for i, line in enumerate(label.split("\n"))]
            x, y = at
            halo = _lines_svg(x, y, rows, anchor).replace(
                "<text ", f'<text stroke="{bg}" stroke-width="5" stroke-linejoin="round" ')
            self.edges.append(halo + _lines_svg(x, y, rows, anchor))

    def legend(self, x, y):
        """A key to the shapes, drawn small."""
        self.front.append(f'<rect x="{x}" y="{y}" width="430" height="128" fill="#FFFFFF" stroke="{INK}" stroke-width="1"/>')
        self.front.append(_lines_svg(x + 10, y + 14, [("Key", 12, "bold", INK, False)], anchor="start"))
        items = [("node", "Deployment node"), ("box", "Container"), ("db", "Database"), ("queue", "Queue"),
                 ("ext", "Person or external system"), ("note", "Note: open item or remark"),
                 ("solid", "Relationship [protocol]"), ("dashed", "Optional, open or dead-letter")]
        for i, (kind, text) in enumerate(items):
            cx, cy = x + 12 + (i // 4) * 215, y + 36 + (i % 4) * 24
            s = f'stroke="{INK}" stroke-width="1.2"'
            if kind == "node":
                self.front.append(f'<path d="M{cx} {cy-5} l4 -4 h22 l-4 4 z M{cx+22} {cy-5} l4 -4 v12 l-4 4 z" '
                                  f'fill="{_shade(NODE)}" {s}/><rect x="{cx}" y="{cy-5}" width="22" height="12" fill="{NODE}" {s}/>')
            elif kind == "box":
                self.front.append(f'<rect x="{cx}" y="{cy-7}" width="26" height="14" rx="3" fill="{ELEMENT}" {s}/>')
            elif kind == "db":
                self.front.append(f'<path d="M{cx+3} {cy-5} a10 3 0 0 1 20 0 v11 a10 3 0 0 1 -20 0 z M{cx+3} {cy-5} '
                                  f'a10 3 0 0 0 20 0" fill="{PART}" {s}/>')
            elif kind == "queue":
                self.front.append(f'<path d="M{cx+4} {cy-6} h18 a4 6 0 0 1 0 12 h-18 a4 6 0 0 1 0 -12 z M{cx+22} {cy-6} '
                                  f'a4 6 0 0 0 0 12" fill="{PART}" {s}/>')
            elif kind == "ext":
                self.front.append(f'<rect x="{cx}" y="{cy-7}" width="26" height="14" rx="2" fill="{EXTERNAL}" {s}/>')
            elif kind == "note":
                self.front.append(f'<path d="M{cx} {cy-7} h20 l6 6 v8 h-26 z" fill="{NOTE}" {s}/>')
            else:
                dash = ' stroke-dasharray="5 4"' if kind == "dashed" else ""
                self.front.append(f'<path d="M{cx} {cy} h24" stroke="{INK}" stroke-width="1.6"{dash} marker-end="url(#arrow)"/>')
            self.front.append(_lines_svg(cx + 34, cy, [(text, 11, "normal", INK, False)], anchor="start"))

    # ---- output -------------------------------------------------------------
    def svg(self):
        defs = (f'<defs><marker id="arrow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" '
                f'markerHeight="11" markerUnits="userSpaceOnUse" orient="auto">'
                f'<path d="M1 1 L11 6 L1 11 Z" fill="{INK}"/></marker></defs>')
        body = "\n".join(self.back + self.edges + self.front)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
                f'viewBox="0 0 {self.width} {self.height}" font-family="{FONT}">\n'
                f'<title>{escape(self.title)}</title>\n{defs}\n'
                f'<rect width="100%" height="100%" fill="#FFFFFF"/>\n{body}\n</svg>\n')


def _unit(dx, dy):
    n = (dx * dx + dy * dy) ** 0.5 or 1
    return dx / n, dy / n
