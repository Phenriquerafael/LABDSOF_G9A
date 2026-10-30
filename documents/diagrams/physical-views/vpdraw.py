"""Small SVG kit for the BMC physical views as UML deployment diagrams.

Draws UML nodes, components (containers and their parts), artifacts, provided
interfaces as lollipops, actors, boundaries, notes, communication paths and
dependencies in the style Visual Paradigm gives UML deployment diagrams:
one blue fill, black outlines, bold names under a «stereotype». Coordinates
are absolute pixels; every view in views.py places its shapes by hand.
"""

from html import escape

FONT = "Arial, 'Liberation Sans', Helvetica, sans-serif"

BLUE = "#83C6EF"      # Visual Paradigm's UML deployment fill
NOTE = "#FFFFFF"
INK = "#000000"
GREY = "#1F2A33"
LINE = 15


def _text(x, y, text, size=12, bold=False, anchor="middle", colour=INK):
    weight = ' font-weight="bold"' if bold else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}"{weight} fill="{colour}" text-anchor="{anchor}" '
            f'dominant-baseline="central">{escape(text)}</text>')


def _caption(x, y, stereo, name, details, anchor):
    """«stereotype», bold name, detail lines; returns svg and the height used."""
    out, yy = [], y
    if stereo:
        out.append(_text(x, yy, f"«{stereo}»", 11.5, anchor=anchor))
        yy += LINE
    out.append(_text(x, yy, name, 13.5, True, anchor))
    yy += LINE
    for line in details:
        out.append(_text(x, yy, line, 11, anchor=anchor, colour=GREY))
        yy += LINE - 1
    return "".join(out)


def _icon(kind, x, y):
    """The icon at the top right of a box, about 14 x 16 px."""
    s = f'stroke="{INK}" stroke-width="1.1" fill="{BLUE}"'
    if kind == "component":
        return (f'<rect x="{x+3}" y="{y}" width="11" height="16" {s}/>'
                f'<rect x="{x}" y="{y+3}" width="7" height="3.5" {s}/><rect x="{x}" y="{y+9}" width="7" height="3.5" {s}/>')
    if kind == "artifact":
        return f'<path d="M{x+1} {y} h8 l5 5 v11 h-13 z M{x+9} {y} v5 h5" {s}/>'
    if kind == "database":
        return (f'<path d="M{x} {y+3} v10 a7 3 0 0 0 14 0 v-10" {s}/>'
                f'<ellipse cx="{x+7}" cy="{y+3}" rx="7" ry="3" {s}/>')
    return ""


class Diagram:
    def __init__(self, name, title, subtitle, width, height):
        self.name, self.title = name, title
        self.width, self.height = width, height
        self.back, self.edges, self.front = [], [], []
        self.shapes = {}
        self.front.append(_text(20, 28, title, 18, True, "start"))
        self.front.append(_text(20, 50, subtitle, 12, anchor="start", colour="#444444"))

    # ---- nodes and boundaries -------------------------------------------------
    def node(self, key, x, y, w, h, name, stereo=None, details=(), align="center", dashed=False):
        """A UML node: a three-dimensional box, its name at the top."""
        d = 14
        dash = ' stroke-dasharray="8 5"' if dashed else ""
        s = f'fill="{BLUE}" stroke="{INK}" stroke-width="1.4"{dash}'
        self.back.append(f'<path d="M{x} {y} l{d} {-d} h{w} l{-d} {d} z" {s}/>')
        self.back.append(f'<path d="M{x+w} {y} l{d} {-d} v{h} l{-d} {d} z" {s}/>')
        self.back.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {s}/>')
        cx, anchor = (x + w / 2, "middle") if align == "center" else (x + 12, "start")
        self.back.append(_caption(cx, y + 18, stereo, name, list(details), anchor))
        self.shapes[key] = (x, y, w, h)

    def holder(self, key, x, y, w, h, name, stereo="container", details=(), at="bottom"):
        """A component drawn open to show its parts; caption at the bottom left
        (or top left) so connections can reach the parts from above."""
        self.back.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BLUE}" stroke="{INK}" '
                         f'stroke-width="1.4"/>')
        self.back.append(_icon("component", x + w - 24, y + 8))
        rows = (1 if stereo else 0) + 1 + len(details)
        top = y + h - 14 - (rows - 1) * LINE if at == "bottom" else y + 18
        self.back.append(_caption(x + 12, top, stereo, name, list(details), "start"))
        self.shapes[key] = (x, y, w, h)

    def boundary(self, key, x, y, w, h, label):
        """A dashed boundary (not a UML element): a trust boundary or a set."""
        self.back.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="{INK}" '
                         f'stroke-width="1.4" stroke-dasharray="9 5"/>')
        self.back.append(_text(x + 12, y + h - 14, label, 12, True, "start"))
        self.shapes[key] = (x, y, w, h)

    # ---- elements -------------------------------------------------------------
    def comp(self, key, x, y, w, h, name, stereo="container", details=(), icon="component", dashed=False):
        """A component or artifact box: «stereotype», bold name, details, icon."""
        dash = ' stroke-dasharray="8 5"' if dashed else ""
        self.front.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BLUE}" stroke="{INK}" '
                          f'stroke-width="1.4"{dash}/>')
        self.front.append(_icon(icon, x + w - 24, y + 8))
        rows = (1 if stereo else 0) + 1 + len(details)
        top = y + h / 2 - (rows - 1) * LINE / 2
        self.front.append(_caption(x + w / 2, top, stereo, name, list(details), "middle"))
        self.shapes[key] = (x, y, w, h)

    def actor(self, key, cx, y, name, details=()):
        """A UML actor: a stick figure with its name below."""
        s = f'stroke="{INK}" stroke-width="1.6" fill="none"'
        self.front.append(f'<circle cx="{cx}" cy="{y+10}" r="10" fill="{BLUE}" stroke="{INK}" stroke-width="1.6"/>'
                          f'<path d="M{cx} {y+20} v26 M{cx-18} {y+30} h36 M{cx} {y+46} l-14 20 M{cx} {y+46} l14 20" {s}/>')
        self.front.append(_caption(cx, y + 80, None, name, list(details), "middle"))
        self.shapes[key] = (cx - 20, y, 40, 66)

    def lollipop(self, cx, cy, label, to, at="e"):
        """A provided interface: a ball on a stick joined to its component."""
        tx, ty = to
        if tx == cx:
            sy = cy + 9 if ty > cy else cy - 9
            self.front.append(f'<path d="M{cx} {sy} L{tx} {ty}" stroke="{INK}" stroke-width="1.4"/>')
        else:
            sx = cx + 9 if tx > cx else cx - 9
            self.front.append(f'<path d="M{sx} {cy} L{tx} {ty}" stroke="{INK}" stroke-width="1.4"/>')
        self.front.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="#FFFFFF" stroke="{INK}" stroke-width="1.4"/>')
        lx, ly, anchor = {"e": (cx + 15, cy, "start"), "w": (cx - 15, cy, "end"),
                          "n": (cx, cy - 18, "middle")}[at]
        self.front.append(_text(lx, ly, label, 11.5, anchor=anchor))

    def note(self, x, y, w, lines, attach=None):
        """A UML note with a folded corner, anchored by a dashed line."""
        h = len(lines) * LINE + 14
        f = 10
        if attach:
            ax, ay = attach
            tx = x if ax < x else x + w if ax > x + w else ax
            ty = y + h / 2 if tx != ax else (y if ay < y else y + h)
            self.edges.append(f'<path d="M{ax} {ay} L{tx} {ty}" stroke="{INK}" stroke-width="1" '
                              f'stroke-dasharray="4 3" fill="none"/>')
        self.front.append(f'<path d="M{x} {y} h{w-f} l{f} {f} v{h-f} h{-w} z" fill="{NOTE}" stroke="{INK}" '
                          f'stroke-width="1.1"/><path d="M{x+w-f} {y} v{f} h{f}" fill="none" stroke="{INK}" '
                          f'stroke-width="1.1"/>')
        self.front.append("".join(_text(x + 9, y + 7 + LINE / 2 + i * LINE, line, 11.5, anchor="start")
                                  for i, line in enumerate(lines)))

    # ---- connections ----------------------------------------------------------
    def p(self, key, side, t=0.5):
        """A point on a side of a shape: n, s, e or w, at fraction t along it."""
        x, y, w, h = self.shapes[key]
        return {"n": (x + w * t, y), "s": (x + w * t, y + h),
                "w": (x, y + h * t), "e": (x + w, y + h * t)}[side]

    def _route(self, points):
        d = f"M{points[0][0]} {points[0][1]}"
        for i in range(1, len(points) - 1):
            (x0, y0), (x1, y1), (x2, y2) = points[i - 1], points[i], points[i + 1]
            r = min(6, (abs(x1 - x0) + abs(y1 - y0)) / 2, (abs(x2 - x1) + abs(y2 - y1)) / 2)
            ux, uy = _unit(x1 - x0, y1 - y0)
            vx, vy = _unit(x2 - x1, y2 - y1)
            d += f" L{x1 - ux*r} {y1 - uy*r} Q{x1} {y1} {x1 + vx*r} {y1 + vy*r}"
        return d + f" L{points[-1][0]} {points[-1][1]}"

    def _label(self, label, at, anchor, bg):
        if not label:
            return
        x, y = at
        rows = label.split("\n")
        for i, row in enumerate(rows):
            t = _text(x, y + i * LINE, row, 12, anchor=anchor)
            self.edges.append(t.replace("<text ", f'<text stroke="{bg}" stroke-width="5" stroke-linejoin="round" ')
                              + t)

    def path(self, points, label=None, at=None, anchor="start", bg="#FFFFFF", dashed=False):
        """A communication path: a plain line, labelled with the protocol."""
        dash = ' stroke-dasharray="8 5"' if dashed else ""
        self.edges.append(f'<path d="{self._route(points)}" stroke="{INK}" stroke-width="1.4" fill="none"{dash}/>')
        self._label(label, at, anchor, bg)

    def dep(self, points, label=None, at=None, anchor="start", bg="#FFFFFF"):
        """A dependency or information flow: dashed line with an open arrow."""
        self.edges.append(f'<path d="{self._route(points)}" stroke="{INK}" stroke-width="1.4" fill="none" '
                          f'stroke-dasharray="8 5" marker-end="url(#open)"/>')
        self._label(label, at, anchor, bg)

    def legend(self, x, y):
        w, h = 620, 120
        self.front.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFFFFF" stroke="{INK}" stroke-width="1"/>')
        self.front.append(_text(x + 10, y + 15, "Key (UML deployment)", 12, True, "start"))
        items = [("node", "Node: device, network, runner"), ("component", "«container» or a part of one"),
                 ("artifact", "«artifact»: build or file"), ("ball", "Provided interface (lollipop)"),
                 ("path", "Communication path [protocol]"), ("dep", "Dependency or flow (arrow: user → used)"),
                 ("dash", "Dashed outline: optional or not placed"), ("note", "Note: open item or remark")]
        for i, (kind, text) in enumerate(items):
            cx, cy = x + 14 + (i // 4) * 305, y + 40 + (i % 4) * 21
            s = f'fill="{BLUE}" stroke="{INK}" stroke-width="1"'
            if kind == "node":
                self.front.append(f'<path d="M{cx} {cy-5} l4 -4 h20 l-4 4 z M{cx+20} {cy-5} l4 -4 v12 l-4 4 z" {s}/>'
                                  f'<rect x="{cx}" y="{cy-5}" width="20" height="12" {s}/>')
            elif kind in ("component", "artifact"):
                self.front.append(f'<rect x="{cx}" y="{cy-8}" width="26" height="16" {s}/>' + _icon(kind, cx + 8, cy - 7))
            elif kind == "ball":
                self.front.append(f'<circle cx="{cx+7}" cy="{cy}" r="6" fill="#FFFFFF" stroke="{INK}"/>'
                                  f'<path d="M{cx+13} {cy} h13" stroke="{INK}"/>')
            elif kind == "path":
                self.front.append(f'<path d="M{cx} {cy} h26" stroke="{INK}" stroke-width="1.4"/>')
            elif kind == "dep":
                self.front.append(f'<path d="M{cx} {cy} h26" stroke="{INK}" stroke-width="1.4" stroke-dasharray="5 3" '
                                  f'marker-end="url(#open)"/>')
            elif kind == "dash":
                self.front.append(f'<rect x="{cx}" y="{cy-7}" width="26" height="14" fill="{BLUE}" stroke="{INK}" '
                                  f'stroke-dasharray="4 2"/>')
            else:
                self.front.append(f'<path d="M{cx} {cy-7} h20 l6 6 v8 h-26 z" fill="#FFFFFF" stroke="{INK}"/>')
            self.front.append(_text(cx + 36, cy, text, 11.5, anchor="start"))

    # ---- output ---------------------------------------------------------------
    def svg(self):
        defs = (f'<defs><marker id="open" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M1 1 L11 6 L1 11" fill="none" stroke="{INK}" '
                f'stroke-width="1.4"/></marker></defs>')
        body = "\n".join(self.back + self.edges + self.front)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
                f'viewBox="0 0 {self.width} {self.height}" font-family="{FONT}">\n'
                f'<title>{escape(self.title)}</title>\n{defs}\n'
                f'<rect width="100%" height="100%" fill="#FFFFFF"/>\n{body}\n</svg>\n')


def _unit(dx, dy):
    n = (dx * dx + dy * dy) ** 0.5 or 1
    return dx / n, dy / n
