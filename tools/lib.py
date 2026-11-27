import math
import os
from xml.sax.saxutils import escape
from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

PAPER = "#FFFFFF"
INK = "#1B1B1F"
SLAB = "#2E2E32"
LINE = "#1B1B1F"
HAIR = "#D5D6DB"
GRAY = "#5B5E66"
BLUE = "#1E50D0"
PEACH = "#FFDCC4"
ORANGE = "#F2A33A"

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
FILES = {
    "400": "InterDisplay-Regular-latin.otf",
    "500": "InterDisplay-Medium-latin.otf",
    "600": "InterDisplay-SemiBold-latin.otf",
    "700": "InterDisplay-Bold-latin.otf",
    "800": "InterDisplay-ExtraBold-latin.otf",
    "900": "ArchivoBlack-latin.ttf",
}


class Face:
    def __init__(self, font):
        self.f = font
        self.gs = font.getGlyphSet()
        self.cmap = font.getBestCmap()
        self.upm = font["head"].unitsPerEm
        os2 = font["OS/2"]
        self.cap = getattr(os2, "sCapHeight", 0) or int(self.upm * 0.7)

    def has(self, ch):
        return ord(ch) in self.cmap

    def adv(self, ch):
        return self.f["hmtx"][self.cmap[ord(ch)]][0]


def _load_cjk():
    bundled = os.path.join(FONT_DIR, "NotoSansCJKjp-Bold-subset.otf")
    if os.path.exists(bundled):
        return Face(TTFont(bundled))
    col = TTCollection("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc")
    for f in col.fonts:
        if "JP" in f["name"].getDebugName(1):
            return Face(f)
    raise SystemExit("no JP face")


FACES = {w: Face(TTFont(os.path.join(FONT_DIR, fn))) for w, fn in FILES.items()}
CJK = _load_cjk()


def face_for(ch, weight):
    base = FACES[weight]
    if base.has(ch):
        return base
    if CJK.has(ch):
        return CJK
    raise KeyError("missing glyph %r" % ch)


def _n(v):
    s = ("%.1f" % v).rstrip("0").rstrip(".")
    return s if s != "-0" else "0"


def measure(text, size, weight="800", track=0.0):
    w = 0.0
    for ch in text:
        fc = face_for(ch, weight)
        w += fc.adv(ch) * size / fc.upm + track * size
    return w - track * size if text else 0.0


def text_path(text, x, y, size, weight="800", fill=INK, track=0.0, anchor="s", extra="", sy=1.0):
    w = measure(text, size, weight, track)
    if anchor == "m":
        x -= w / 2
    elif anchor == "e":
        x -= w
    parts = []
    pen_x = x
    for ch in text:
        fc = face_for(ch, weight)
        k = size / fc.upm
        if ch != " ":
            pen = SVGPathPen(fc.gs, ntos=_n)
            tp = TransformPen(pen, (k, 0, 0, -k * sy, pen_x, y))
            fc.gs[fc.cmap[ord(ch)]].draw(tp)
            parts.append(pen.getCommands())
        pen_x += fc.adv(ch) * k + track * size
    d = "".join(parts)
    return '<path d="%s" fill="%s"%s/>' % (d, fill, extra), w


def wrap(text, size, maxw, weight="500", track=0.0):
    words, lines, cur = text.split(" "), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if measure(trial, size, weight, track) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def cap_px(size, weight="900"):
    f = FACES[weight]
    return f.cap * size / f.upm


class Doc:
    def __init__(self, name, w, h, title, desc, rx=6, bg=True, border=True):
        self.name, self.w, self.h, self.title, self.desc = name, w, h, title, desc
        self.defs, self.body = [], []
        if bg:
            st = ' stroke="%s"' % HAIR if border else ""
            self.body.append(
                '<rect x="0.5" y="0.5" width="%s" height="%s" rx="%s" fill="%s"%s/>'
                % (_n(w - 1), _n(h - 1), rx, PAPER, st)
            )

    def add(self, s):
        self.body.append(s)

    def text(self, *a, **k):
        s, w = text_path(*a, **k)
        self.body.append(s)
        return w

    def lines(self, lines, x, y, size, lh, weight="500", fill=GRAY, track=0.0, anchor="s"):
        for i, ln in enumerate(lines):
            self.text(ln, x, y + i * lh, size, weight, fill, track, anchor)
        return y + len(lines) * lh

    def rect(self, x, y, w, h, fill, rx=0, stroke=None, sw=1):
        st = ' stroke="%s" stroke-width="%s"' % (stroke, sw) if stroke else ""
        self.body.append(
            '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"%s/>'
            % (_n(x), _n(y), _n(w), _n(h), rx, fill, st)
        )

    def hline(self, x1, x2, y, color=HAIR, h=1):
        self.rect(x1, y, x2 - x1, h, color)

    def svg(self):
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s" viewBox="0 0 %s %s" role="img" aria-labelledby="t d">\n'
            "<title id=\"t\">%s</title><desc id=\"d\">%s</desc>\n"
            "<defs>%s</defs>\n%s\n</svg>\n"
            % (_n(self.w), _n(self.h), _n(self.w), _n(self.h), escape(self.title), escape(self.desc),
               "".join(self.defs), "\n".join(self.body))
        )


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def halftone(x0, y0, x1, y1, pitch, rfn, color, deg=45):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    n = int(math.hypot(x1 - x0, y1 - y0) / 2 / pitch) + 2
    out = []
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            gx, gy = i * pitch, j * pitch
            x = cx + gx * ca - gy * sa
            y = cy + gx * sa + gy * ca
            if x < x0 - pitch or x > x1 + pitch or y < y0 - pitch or y > y1 + pitch:
                continue
            r = rfn((x - x0) / (x1 - x0), (y - y0) / (y1 - y0)) * pitch * 0.64
            if r >= 0.8:
                out.append('<circle cx="%s" cy="%s" r="%s"/>' % (_n(x), _n(y), _n(r)))
    return '<g fill="%s">%s</g>' % (color, "".join(out))


def lum(hexc):
    h = hexc.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
