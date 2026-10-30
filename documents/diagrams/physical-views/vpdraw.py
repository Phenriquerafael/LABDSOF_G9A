"""Small SVG drawing kit for the BMC physical views.

Draws pools, lanes, elements, diamonds, events, notes and orthogonal
connectors in the Visual Paradigm BPMN palette used by the team's other
diagrams. Coordinates are absolute pixels; every view in views.py places
its shapes by hand, so the layout only changes when a source changes.
"""

from html import escape

FONT = "Arial, 'Liberation Sans', Helvetica, sans-serif"

POOL = "#87DCF5"      # pools, lanes and host groupings
GROUP = "#C2ECFA"     # a grouping drawn inside a lane
ELEMENT = "#EEF57A"   # a container or item that runs on the host
DECISION = "#FF992E"  # a routing decision: Traefik rule, exchange
OUTSIDE = "#C3F57A"   # a node outside the Docker host; start events
STOP = "#F57A7A"      # a refused request, an end event
INK = "#000000"

BAND = 40             # width of the vertical title band of a pool or lane
LINE = 16             # text line height


def _text(x, y, lines, size=13, anchor="middle", weight_first=False, rotate=False):
    """Return a <text> block whose lines are centred vertically on y."""
    out = []
    top = y - (len(lines) - 1) * LINE / 2
    transform = f' transform="rotate(-90 {x} {y})"' if rotate else ""
    out.append(f'<text x="{x}" y="{top}" font-size="{size}" text-anchor="{anchor}" '
               f'dominant-baseline="central"{transform}>')
    for i, line in enumerate(lines):
        weight = ' font-weight="bold"' if weight_first and i == 0 else ""
        dy = 0 if i == 0 else LINE
        out.append(f'<tspan x="{x}" dy="{dy}"{weight}>{escape(line)}</tspan>')
    out.append("</text>")
    return "".join(out)


# Icons are drawn at (x, y), about 20 x 20 px, like the task markers of BPMN.
def _icon(kind, x, y):
    s = f'stroke="{INK}" stroke-width="1.2" fill="none"'
    if kind == "node":  # UML node: a three-dimensional box
        return (f'<path d="M{x} {y+6} h13 v13 h-13 z M{x} {y+6} l5 -5 h13 l-5 5 '
                f'M{x+13} {y+19} l5 -5 v-13" {s}/>')
    if kind == "db":
        return (f'<path d="M{x} {y+4} v13 a9 3.5 0 0 0 18 0 v-13" {s}/>'
                f'<ellipse cx="{x+9}" cy="{y+4}" rx="9" ry="3.5" {s}/>')
    if kind == "queue":
        return (f'<rect x="{x}" y="{y+4}" width="20" height="12" rx="2" {s}/>'
                f'<path d="M{x+5} {y+4} v12 M{x+10} {y+4} v12 M{x+15} {y+4} v12" {s}/>')
    if kind == "bucket":
        return (f'<path d="M{x+1} {y+5} l3 14 h12 l3 -14" {s}/>'
                f'<ellipse cx="{x+10}" cy="{y+5}" rx="9" ry="3" {s}/>')
    if kind == "cloud":
        return (f'<path d="M{x+5} {y+17} a5 5 0 0 1 0 -10 a6 6 0 0 1 11 -2 '
                f'a5 5 0 0 1 3 12 z" {s}/>')
    if kind == "person":
        return (f'<circle cx="{x+10}" cy="{y+6}" r="4.5" {s}/>'
                f'<path d="M{x+2} {y+20} v-3 a8 6 0 0 1 16 0 v3" {s}/>')
    if kind == "gear":
        spokes = "".join(
            f'<path d="M{x+10} {y+10} m{dx} {dy} l{dx*0.45:.1f} {dy*0.45:.1f}" stroke="{INK}" stroke-width="2.4"/>'
            for dx, dy in ((0, -7), (0, 7), (-7, 0), (7, 0), (5, 5), (-5, -5), (5, -5), (-5, 5)))
        return spokes + (f'<circle cx="{x+10}" cy="{y+10}" r="6.5" stroke="{INK}" stroke-width="1.2" fill="{ELEMENT}"/>'
                         f'<circle cx="{x+10}" cy="{y+10}" r="2.5" {s}/>')
    if kind == "doc":
        return (f'<path d="M{x+2} {y+1} h10 l5 5 v14 h-15 z M{x+12} {y+1} v5 h5 '
                f'M{x+5} {y+10} h9 M{x+5} {y+13} h9 M{x+5} {y+16} h9" {s}/>')
    if kind == "device":
        return (f'<rect x="{x+3}" y="{y+1}" width="13" height="19" rx="2" {s}/>'
                f'<path d="M{x+7} {y+17} h5" {s}/>')
    return ""


class Diagram:
    def __init__(self, name, title, width, height):
        self.name, self.title = name, title
        self.width, self.height = width, height
        self.back, self.front, self.edges = [], [], []
        self.shapes = {}

    # ---- containers -------------------------------------------------------
    def pool(self, x, y, w, title, lanes):
        """A pool with a vertical title band and horizontal lanes.

        lanes is a list of (label, height); a single lane with an empty label
        gives a pool without lane bands. Returns the y of each lane top.
        """
        h = sum(height for _, height in lanes)
        self.back.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{POOL}" '
                         f'stroke="{INK}" stroke-width="2"/>')
        self.back.append(f'<path d="M{x+BAND} {y} v{h}" stroke="{INK}" stroke-width="2"/>')
        self.back.append(_text(x + BAND / 2, y + h / 2, title.split("\n"), rotate=True))
        tops, top = [], y
        for i, (label, height) in enumerate(lanes):
            tops.append(top)
            if label:
                self.back.append(f'<path d="M{x+2*BAND} {top} v{height}" stroke="{INK}" stroke-width="2"/>')
                self.back.append(_text(x + 1.5 * BAND, top + height / 2, label.split("\n"), size=12, rotate=True))
            if i:
                self.back.append(f'<path d="M{x+BAND} {top} h{w-BAND}" stroke="{INK}" stroke-width="2"/>')
            top += height
        return tops

    def group(self, x, y, w, h, title, dashed=False):
        """A titled grouping inside a lane, such as a database instance."""
        dash = ' stroke-dasharray="7 5"' if dashed else ""
        self.back.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{GROUP}" '
                         f'stroke="{INK}" stroke-width="1.6"{dash}/>')
        self.back.append(_text(x + 14, y + 16, [title], size=12, anchor="start", weight_first=True))
        self.shapes[title] = ("box", x, y, w, h)

    # ---- elements ---------------------------------------------------------
    def box(self, key, x, y, w, h, lines, icon="node", fill=ELEMENT, dashed=False):
        """A rounded element; the first line is the name and is set in bold."""
        dash = ' stroke-dasharray="8 5"' if dashed else ""
        self.front.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" '
                          f'stroke="{INK}" stroke-width="2"{dash}/>')
        self.front.append(_icon(icon, x + 7, y + 6))
        self.front.append(_text(x + w / 2, y + h / 2 + 4, lines, weight_first=True))
        self.shapes[key] = ("box", x, y, w, h)

    def diamond(self, key, cx, cy, label=None, at=(0, -46), size=29):
        self.front.append(f'<path d="M{cx} {cy-size} L{cx+size} {cy} L{cx} {cy+size} L{cx-size} {cy} Z" '
                          f'fill="{DECISION}" stroke="{INK}" stroke-width="2"/>')
        if label:
            self.front.append(_text(cx + at[0], cy + at[1], label.split("\n"), size=12))
        self.shapes[key] = ("box", cx - size, cy - size, 2 * size, 2 * size)

    def event(self, key, cx, cy, label, end=False, at=(0, 42)):
        """A start event (green) or an end event (red); a label offset to the
        right of the circle is left-aligned."""
        fill, width = (STOP, 4) if end else (OUTSIDE, 2)
        anchor = "start" if at[0] > 0 else "end" if at[0] < 0 else "middle"
        self.front.append(f'<circle cx="{cx}" cy="{cy}" r="20" fill="{fill}" stroke="{INK}" stroke-width="{width}"/>')
        self.front.append(_text(cx + at[0], cy + at[1], label.split("\n"), size=12, anchor=anchor))
        self.shapes[key] = ("box", cx - 20, cy - 20, 40, 40)

    def text(self, x, y, lines, anchor="start", size=12):
        """Free text, such as the name of an exchange next to its diamond."""
        self.front.append(_text(x, y, lines, size=size, anchor=anchor))

    def note(self, x, y, lines, attach=None, size=12):
        """A BPMN text annotation: an open bracket, text, a dotted association.

        The association meets the bracket, the right end of the text when the
        attached point lies to the right, or the top edge when it lies above.
        """
        h = len(lines) * LINE + 12
        if attach:
            ax, ay = attach
            width = max(len(line) for line in lines) * 6.4 + 16
            if ax > x + width:
                tx, ty = x + width, y + h / 2
            elif ay < y and ax > x:
                tx, ty = x + 40, y
            else:
                tx, ty = x, y + h / 2
            self.edges.append(f'<path d="M{ax} {ay} L{tx} {ty}" stroke="{INK}" stroke-width="1.5" '
                              f'stroke-dasharray="2 4" fill="none"/>')
        self.front.append(f'<path d="M{x+12} {y} H{x} V{y+h} H{x+12}" stroke="{INK}" stroke-width="2" fill="none"/>')
        self.front.append(_text(x + 10, y + h / 2, lines, size=size, anchor="start"))

    # ---- connectors -------------------------------------------------------
    def p(self, key, side, t=0.5):
        """A point on a side of a shape: n, s, e or w, at fraction t along it."""
        _, x, y, w, h = self.shapes[key]
        return {"n": (x + w * t, y), "s": (x + w * t, y + h),
                "w": (x, y + h * t), "e": (x + w, y + h * t)}[side]

    def edge(self, points, label=None, at=None, dashed=False, arrow=True, anchor="start"):
        """An orthogonal connector through the given points, with rounded bends."""
        d = f"M{points[0][0]} {points[0][1]}"
        for i in range(1, len(points) - 1):
            (x0, y0), (x1, y1), (x2, y2) = points[i - 1], points[i], points[i + 1]
            r = min(8, abs(x1 - x0) / 2 + abs(y1 - y0) / 2, abs(x2 - x1) / 2 + abs(y2 - y1) / 2)
            ux, uy = _unit(x1 - x0, y1 - y0)
            vx, vy = _unit(x2 - x1, y2 - y1)
            d += f" L{x1 - ux*r} {y1 - uy*r} Q{x1} {y1} {x1 + vx*r} {y1 + vy*r}"
        d += f" L{points[-1][0]} {points[-1][1]}"
        dash = ' stroke-dasharray="8 6"' if dashed else ""
        head = ' marker-end="url(#arrow)"' if arrow else ""
        self.edges.append(f'<path d="{d}" stroke="{INK}" stroke-width="2" fill="none"{dash}{head}/>')
        if label:
            self.edges.append(_label(at, label.split("\n"), anchor))

    # ---- output -----------------------------------------------------------
    def svg(self):
        defs = (f'<defs><marker id="arrow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" '
                f'markerHeight="12" markerUnits="userSpaceOnUse" orient="auto">'
                f'<path d="M1 1 L11 6 L1 11 Z" fill="{INK}"/></marker></defs>')
        body = "\n".join(self.back + self.edges + self.front)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
                f'viewBox="0 0 {self.width} {self.height}" font-family="{FONT}" fill="{INK}">\n'
                f'<title>{escape(self.title)}</title>\n{defs}\n'
                f'<rect width="100%" height="100%" fill="#FFFFFF"/>\n{body}\n</svg>\n')


def _unit(dx, dy):
    n = (dx * dx + dy * dy) ** 0.5 or 1
    return dx / n, dy / n


def _label(at, lines, anchor):
    """An edge label with a halo in the pool colour, so it stays legible over lines."""
    x, y = at
    halo = _text(x, y, lines, size=12, anchor=anchor).replace(
        "<text ", '<text stroke="#87DCF5" stroke-width="5" stroke-linejoin="round" ', 1)
    return halo + _text(x, y, lines, size=12, anchor=anchor)
