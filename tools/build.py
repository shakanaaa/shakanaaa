import os, re, sys
from lib import *
from lib import _n
import art

OUT = sys.argv[1]
os.makedirs(OUT + "/m", exist_ok=True)

DOCS = []
SRC_W, SRC_H = 2576, 1182
_ART = {}


def save(doc, mob):
    if doc.name in MERGED:
        doc = head_into(doc, MERGED[doc.name], mob)
    path = "%s/%s%s.svg" % (OUT, "m/" if mob else "", doc.name)
    open(path, "w", encoding="utf-8").write(doc.svg())
    DOCS.append(path)


def crop_box(cx, cy, width, ratio):
    """Source crop centred on (cx, cy), `width` wide, height = width / ratio, kept inside the image."""
    w = min(width, SRC_W)
    h = w / ratio
    if h > SRC_H:
        h = SRC_H
        w = h * ratio
    x0 = min(max(cx - w / 2, 0), SRC_W - w)
    y0 = min(max(cy - h / 2, 0), SRC_H - h)
    return (int(x0), int(y0), int(x0 + w), int(y0 + h))


def art_image(cx, cy, width, w, h, pitch, scale=2):
    """Stylised artwork as a data URI for a w x h area."""
    box = crop_box(cx, cy, width, w / h)
    key = (box, w, h, pitch, scale)
    if key not in _ART:
        _ART[key] = art.data_uri(art.stylize(box, int(w * scale), int(h * scale), pitch=pitch))
    return _ART[key]


def put_image(d, uri, x, y, w, h, clip=None):
    c = ' clip-path="url(#%s)"' % clip if clip else ""
    d.add('<image href="%s" x="%s" y="%s" width="%s" height="%s" preserveAspectRatio="none"%s/>' % (uri, _n(x), _n(y), _n(w), _n(h), c))


def lab(d, s, x, y, size=12, fill=GRAY, anchor="s"):
    return d.text(s, x, y, size, "600", fill, 0.0, anchor)


def word_d(word, x, y, size, track, sy=1.0):
    s, w = text_path(word, x, y, size, "900", INK, track, sy=sy)
    return re.search(r'd="([^"]*)"', s).group(1), w


def diamonds(d, cx, cy, u):
    """Four diamonds, the identity mark."""
    def dia(x, y, fill):
        d.add('<path d="M%s %sL%s %sL%s %sL%s %sZ" fill="%s" stroke="%s" stroke-width="1.5"/>'
              % (_n(x), _n(y - u), _n(x + u), _n(y), _n(x), _n(y + u), _n(x - u), _n(y), fill, PAPER))
    dia(cx, cy - u, BLUE)
    dia(cx - u, cy, BLUE)
    dia(cx + u, cy, PEACH)
    dia(cx, cy + u, ORANGE)


def slashes(d, x, y, h, fill=INK):
    w = h * 0.5
    lean = h * 0.32
    for i in range(2):
        xx = x + i * (w + h * 0.12)
        d.add('<path d="M%s %sH%s L%s %sH%s Z" fill="%s"/>'
              % (_n(xx + lean), _n(y), _n(xx + lean + w), _n(xx + w), _n(y + h), _n(xx), fill))


def slab(d, x0, y, x1, h, lean=None):
    lean = h * 0.3 if lean is None else lean
    d.add('<path d="M%s %sH%s V%s H%s Z" fill="%s"/>' % (_n(x0 + lean), _n(y), _n(x1), _n(y + h), _n(x0), SLAB))


NAV = [("About", "about"), ("Work", "work"), ("Stack", "stack"), ("Stats", "stats"),
       ("Interests", "interests"), ("Contact", "contact")]


def nav_chip(text, name):
    w = round(measure(text, 15, "700", 0.0) + 32)
    d = Doc("nav-" + name, w, 44, "Menu: " + text, "Link ke bagian %s" % text, rx=6)
    d.text(text, w / 2, 27, 15, "700", INK, 0.0, "m")
    save(d, False)


def home_mark():
    d = Doc("nav-home", 44, 44, "Portfolio Rizki", "Buka portfolio Rizki", rx=6, bg=False)
    d.rect(0, 0, 44, 44, BLUE, 6)
    d.text("R", 22, 32, 24, "900", PAPER, 0.0, "m")
    save(d, False)


# ------------------------------------------------------------------ hero
def hero(mob):
    W = 480 if mob else 1000
    M = 20 if mob else 32
    sy = 1.2
    word, tr = "RIZKI", -0.02
    wm_w = W - 2 * M
    size = wm_w / measure(word, 1, "900", tr)
    cap = cap_px(size) * sy
    box_y, box_h = 24, (104 if mob else 64)
    top = box_y + box_h + (22 if mob else 30)
    base = top + cap
    my = base + (40 if mob else 46)
    if mob:
        slab_y = my + 408
        H = round(slab_y + 96 + 24)
    else:
        slab_y = my + 232
        H = round(slab_y + 112 + 32)
    d = Doc("hero", W, H, "Rizki, developer dan artist dari Indonesia",
            "Wordmark RIZKI berisi ilustrasi halftone biru, peach, dan oranye. Rizki, Full-Stack Developer dan Digital Artist dari Indonesia, terbuka untuk proyek menarik. Code with curiosity, create with feeling, live with imagination.")

    # status box
    d.rect(M + 0.75, box_y + 0.75, W - 2 * M - 1.5, box_h - 1.5, "none", 10, INK, 1.5)
    if not mob:
        c2 = M + 660
        d.add('<circle cx="%s" cy="%s" r="6" fill="%s"/>' % (M + 28, box_y + 33, ORANGE))
        lab(d, "Collab", M + 46, box_y + 26, 13)
        d.text("Open to interesting projects", M + 46, box_y + 48, 18, "700", INK)
        d.rect(c2 - 24, box_y + 12, 1.5, box_h - 24, HAIR)
        lab(d, "Base", c2, box_y + 26, 13)
        d.rect(c2, box_y + 33, 34, 20, BLUE, 3)
        d.text("ID", c2 + 17, box_y + 48, 12, "800", PAPER, 0.04, "m")
        d.text("Indonesia", c2 + 46, box_y + 49, 18, "700", INK)
    else:
        d.add('<circle cx="%s" cy="%s" r="6" fill="%s"/>' % (M + 24, box_y + 26, ORANGE))
        lab(d, "Collab", M + 42, box_y + 22, 13)
        d.text("Open to interesting projects", M + 42, box_y + 44, 17, "700", INK)
        d.hline(M + 16, W - M - 16, box_y + 56, HAIR)
        lab(d, "Base", M + 16, box_y + 78, 13)
        d.rect(M + 62, box_y + 64, 34, 20, BLUE, 3)
        d.text("ID", M + 79, box_y + 79, 12, "800", PAPER, 0.04, "m")
        d.text("Indonesia", M + 106, box_y + 81, 17, "700", INK)

    # wordmark with artwork inside
    wd, _ = word_d(word, M, base, size, tr, sy)
    d.defs.append('<clipPath id="wm"><path d="%s"/></clipPath>' % wd)
    uri = art_image(930, 512, 1700 if not mob else 1500, int(wm_w), int(cap + 6), 7 if not mob else 6.5, 2)
    put_image(d, uri, M, top - 3, wm_w, cap + 6, "wm")
    d.add('<path d="%s" fill="none" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (wd, INK))

    if not mob:
        c1, c2, c3 = M, M + 330, M + 660
        d.text("Rizki //", c1, my + 22, 28, "800", INK, -0.01)
        d.lines(["Full-Stack", "Developer", "& Digital Artist"], c1, my + 72, 36, 40, "800", INK, -0.02)
        d.rect(c2, my, 280, 3, INK)
        for i, (k, v) in enumerate((("Focus", "Full-stack development"), ("Creative", "Drawing & digital art"), ("Off-screen", "Anime"))):
            yy = my + 36 + i * 62
            lab(d, k, c2, yy, 13)
            d.text(v, c2, yy + 25, 20, "700", INK)
        diamonds(d, c3 + 16, my + 18, 13)
        d.text("リズキ", c3 + 52, my + 30, 30, "800", INK)
        d.lines(["好奇心でコードを書き、", "感情で創り、", "想像力で生きる。"], c3, my + 88, 17, 28, "800", INK)
        slashes(d, M, slab_y, 112)
        sx0 = M + 188
        slab(d, sx0, slab_y, W - M, 112)
        cw = (W - M - sx0 - 70) / 3
        for i, (v, p) in enumerate((("Code", "with curiosity"), ("Create", "with feeling"), ("Live", "with imagination"))):
            x = sx0 + 56 + i * cw
            d.text(v, x, slab_y + 56, 34, "900", PAPER, -0.01)
            d.text(p, x, slab_y + 86, 16, "500", PAPER)
    else:
        d.text("Rizki //", M, my + 20, 24, "800", INK, -0.01)
        d.lines(["Full-Stack Developer", "& Digital Artist"], M, my + 62, 31, 36, "800", INK, -0.02)
        yy = my + 118
        d.rect(M, yy, W - 2 * M, 3, INK)
        for i, (k, v) in enumerate((("Focus", "Full-stack development"), ("Creative", "Drawing & digital art"), ("Off-screen", "Anime"))):
            y3 = yy + 34 + i * 52
            lab(d, k, M, y3, 13)
            d.text(v, M, y3 + 22, 18, "700", INK)
        diamonds(d, W - M - 70, yy + 52, 11)
        d.text("リズキ", W - M, yy + 130, 26, "800", INK, 0, "e")
        d.lines(["好奇心でコードを書き、", "感情で創り、", "想像力で生きる。"], M, my + 118 + 34 + 3 * 52 + 14, 16, 26, "800", INK)
        slashes(d, M, slab_y, 40)
        sx0 = M + 92
        slab(d, sx0, slab_y, W - M, 96, 22)
        cw = (W - M - sx0 - 20) / 3
        for i, (v, p) in enumerate((("Code", "with curiosity"), ("Create", "with feeling"), ("Live", "with imagination"))):
            x = sx0 + 30 + i * (cw - 8)
            d.text(v, x, slab_y + 44, 22, "900", PAPER, -0.01)
            d.text(p, x, slab_y + 68, 12.5, "500", PAPER)
    save(d, mob)


# ------------------------------------------------------------------ strip
def strip(mob):
    items = ["Building something interesting.", "Turning ideas into code.",
             "Creating art and digital experiences.", "Always learning something new."]
    desc = "Building something interesting. Turning ideas into code. Creating art and digital experiences. Always learning something new."
    if not mob:
        W, H, M = 1000, 140, 32
        d = Doc("strip", W, H, "Empat prinsip kerja", desc)
        d.rect(M, 26, W - 2 * M, 3, INK)
        cw = (W - 2 * M) / 4
        for i, t in enumerate(items):
            x = M + i * cw + (0 if i == 0 else 22)
            if i:
                d.rect(M + i * cw, 44, 1.5, 70, HAIR)
            d.text("//", x, 68, 20, "800", BLUE)
            d.lines(wrap(t, 19, cw - 40, "700"), x, 96, 19, 25, "700", INK)
    else:
        W, H, M = 480, 232, 20
        d = Doc("strip", W, H, "Empat prinsip kerja", desc)
        d.rect(M, 22, W - 2 * M, 3, INK)
        cw = (W - 2 * M) / 2
        for i, t in enumerate(items):
            x = M + (i % 2) * cw + (0 if i % 2 == 0 else 16)
            y = 44 + (i // 2) * 92
            if i % 2:
                d.rect(M + cw, y - 4, 1.5, 76, HAIR)
            d.text("//", x, y + 20, 18, "800", BLUE)
            d.lines(wrap(t, 17, cw - 28, "700"), x, y + 46, 17, 22, "700", INK)
    save(d, mob)


# ------------------------------------------------------------------ section headers
def draw_header(d, title, jp, mob, H):
    W, M = d.w, (20 if mob else 32)
    fs = 44 if mob else 64
    base = H - (30 if mob else 36)
    tw = d.text(title, M, base, fs, "900", INK, -0.02)
    d.text("//", M + tw + fs * 0.16, base, fs, "900", BLUE, -0.02)
    d.text(jp, W - M, base - (2 if mob else 4), 18 if mob else 22, "800", GRAY, 0, "e")
    d.rect(M, H - 18, W - 2 * M, 3, INK)


def head_into(inner, key, mob):
    title, jp = MERGED_HEADS[key]
    hh = 84 if mob else 112
    d = Doc(inner.name, inner.w, inner.h + hh, inner.title, inner.desc)
    draw_header(d, title, jp, mob, hh)
    d.defs = inner.defs
    d.add('<g transform="translate(0,%d)">' % hh)
    d.body.extend(inner.body[1:])
    d.add("</g>")
    return d


def header(title, jp, name, mob):
    d = Doc("sec-" + name, 480 if mob else 1000, 84 if mob else 112, title, "Judul bagian %s" % title)
    draw_header(d, title, jp, mob, d.h)
    save(d, mob)


MERGED = {"about": "about", "work": "work", "stack": "stack", "interests": "interests", "chat": "contact"}
MERGED_HEADS = {"about": ("About", "自己紹介"), "work": ("Work", "作品"), "stack": ("Stack", "技術"),
                "interests": ("Interests", "興味"), "contact": ("Contact", "連絡")}


# ------------------------------------------------------------------ about
def about(mob):
    rows = [("Name", "Rizki  リズキ"), ("Location", "Indonesia"), ("Role", "Full-Stack Developer"),
            ("Focus", "Full-Stack Development"), ("Creative", "Drawing & Digital Art"),
            ("Off-screen", "Anime"), ("Collab", "Open to interesting projects")]
    intro = "Developer sekaligus artist dari Indonesia. Aku suka mengeksplorasi programming, menggambar, digital art, dan anime. Saat ini aku sedang memperdalam full-stack development sambil terus membuat hal-hal kreatif."
    note = "hor hor hor~ thanks for stopping by"
    alt = ("Halo, aku Rizki. " + intro + " Nama Rizki, lokasi Indonesia, peran Full-Stack Developer, fokus Full-Stack Development, "
           "sisi kreatif Drawing dan Digital Art, di luar layar Anime, terbuka untuk kolaborasi proyek menarik.")
    if not mob:
        W, M = 1000, 32
        lw, vx = 420, 160
        y = 58
        lay = []
        for k, v in rows:
            ls = wrap(v, 20, lw - (vx - M) + 20, "700")
            lay.append((k, ls, y))
            y += max(1, len(ls)) * 26 + 26
        left_end = y
        rx = 520
        pl = wrap(intro, 19, W - M - rx, "500")
        right_end = 232 + len(pl) * 29 + 70
        H = round(max(left_end, right_end) + 24)
        d = Doc("about", W, H, "Tentang Rizki", alt)
        for k, ls, yy in lay:
            d.hline(M, M + lw, yy - 30, HAIR)
            lab(d, k, M, yy, 13)
            d.lines(ls, vx, yy + 1, 20, 26, "700", INK)
        d.add('<path d="M%s 32H%s V176 H%s Z" fill="%s"/>' % (rx + 44, W - 0.5, rx, BLUE))
        d.add('<path d="M%s 32 L%s 32 L%s 76 Z" fill="%s"/>' % (rx, rx + 44, rx, PAPER))
        d.text("Halo, aku", rx + 72, 96, 40, "900", PAPER, -0.02)
        d.text("Rizki.", rx + 72, 150, 56, "900", PAPER, -0.03)
        d.lines(pl, rx, 232, 19, 29, "500", INK)
        d.text(note, rx, 232 + len(pl) * 29 + 36, 15, "700", BLUE)
    else:
        W, M = 480, 20
        pl = wrap(intro, 17, W - 2 * M, "500")
        y = 202 + len(pl) * 26 + 70
        lay = []
        for k, v in rows:
            ls = wrap(v, 18, 280, "700")
            lay.append((k, ls, y))
            y += max(1, len(ls)) * 24 + 26
        H = round(y + 6)
        d = Doc("about", W, H, "Tentang Rizki", alt)
        d.add('<path d="M%s 22H%s V138 H%s Z" fill="%s"/>' % (M + 32, W - 0.5, 0.5, BLUE))
        d.add('<path d="M0.5 22 L%s 22 L0.5 54 Z" fill="%s"/>' % (M + 32, PAPER))
        d.text("Halo, aku", M + 24, 78, 32, "900", PAPER, -0.02)
        d.text("Rizki.", M + 24, 122, 44, "900", PAPER, -0.03)
        d.lines(pl, M, 176, 17, 26, "500", INK)
        d.text(note, M, 176 + len(pl) * 26 + 28, 14, "700", BLUE)
        for k, ls, yy in lay:
            d.hline(M, W - M, yy - 28, HAIR)
            lab(d, k, M, yy - 4, 13)
            d.lines(ls, 170, yy - 3, 18, 24, "700", INK)
    save(d, mob)


# ------------------------------------------------------------------ work
def work(mob):
    desc = "Personal website inspired by the pause menu of Persona 3 Reload."
    alt = "Featured project: Persona 3 Reload Portfolio. " + desc + " Personal website, best viewed on desktop. Open live demo."

    def arrow(d, x, y, s, col):
        d.add('<path d="M%s %s L%s %s M%s %s H%s V%s" fill="none" stroke="%s" stroke-width="2.4" stroke-linecap="square"/>'
              % (x, y + s, x + s, y, x, y, x + s, y + s, col))

    if not mob:
        W, H, M = 1000, 400, 32
        d = Doc("work", W, H, "Proyek unggulan: Persona 3 Reload Portfolio", alt)
        d.defs.append('<clipPath id="slab"><path d="M650 1H999V399H560Z"/></clipPath>')
        uri = art_image(1700, 640, 1180, 440, 398, 6.5)
        put_image(d, uri, 560, 1, 440, 398, "slab")
        d.add('<path d="M650 1H999V399H560Z" fill="none" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % INK)
        lab(d, "Featured project", M, 56, 14)
        d.text("Persona 3 Reload", M, 130, 54, "900", INK, -0.03)
        d.text("Portfolio", M, 190, 54, "900", INK, -0.03)
        d.lines(wrap(desc, 19, 440, "500"), M, 238, 19, 28, "500", INK)
        tx = M
        for t in ("Personal website", "Best viewed on desktop"):
            w = measure(t, 14, "700") + 26
            d.rect(tx + 0.5, 298.5, w, 32, "none", 4, INK, 1.2)
            d.text(t, tx + 13, 319, 14, "700", INK)
            tx += w + 10
        lab(d, "More little creations will be added here as they grow~", M, 372, 14)
        d.rect(690, 296, 250, 58, INK, 6)
        d.text("Open live demo", 716, 332, 18, "800", PAPER)
        arrow(d, 902, 316, 16, PAPER)
    else:
        W, H, M = 480, 570, 20
        d = Doc("work", W, H, "Proyek unggulan: Persona 3 Reload Portfolio", alt)
        d.defs.append('<clipPath id="slab"><path d="M1 1H479V118L1 156Z"/></clipPath>')
        uri = art_image(1700, 640, 1500, 480, 156, 6)
        put_image(d, uri, 0, 1, 480, 156, "slab")
        d.add('<path d="M1 1H479V118L1 156Z" fill="none" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % INK)
        lab(d, "Featured project", M, 196, 14)
        d.text("Persona 3 Reload", M, 244, 38, "900", INK, -0.03)
        d.text("Portfolio", M, 286, 38, "900", INK, -0.03)
        d.lines(wrap(desc, 17, W - 2 * M, "500"), M, 324, 17, 25, "500", INK)
        tx, ty = M, 384
        for t in ("Personal website", "Best viewed on desktop"):
            w = measure(t, 13, "700") + 24
            if tx + w > W - M:
                tx, ty = M, ty + 40
            d.rect(tx + 0.5, ty + 0.5, w, 30, "none", 4, INK, 1.2)
            d.text(t, tx + 12, ty + 20, 13, "700", INK)
            tx += w + 10
        d.rect(M, 462, W - 2 * M, 56, BLUE, 6)
        d.text("Open live demo", M + 24, 497, 18, "800", PAPER)
        arrow(d, W - M - 40, 481, 16, PAPER)
        lab(d, "More little creations will be added here.", M, 546, 13)
    save(d, mob)


# ------------------------------------------------------------------ stack
STACK = [("Languages", ["C", "C++", "C#", "Java", "JavaScript", "PHP", "Python"]),
         ("Frontend", ["HTML", "CSS", "Bootstrap", "Tailwind CSS", "Angular", "React", "Vue"]),
         ("Backend", ["Node.js", "Express", "Laravel", "NestJS", "Next.js"]),
         ("Database & ORM", ["MySQL", "SQLite", "Prisma"]),
         ("Design & Creative", ["Figma", "Illustrator", "After Effects"]),
         ("Others", ["TensorFlow", "OpenGL", "WebGL", "Git", "GitHub"])]


def stack(mob):
    alt = "Tech stack. " + " ".join("%s: %s." % (k, ", ".join(v)) for k, v in STACK)
    W, M = (480, 20) if mob else (1000, 32)
    fs = 20 if mob else 26
    ix = M if mob else 280
    iw = W - M - ix
    gap = 22 if mob else 28

    def flow(items):
        lines, cur, curw = [], [], 0
        for it in items:
            w = measure(it, fs, "800", -0.01)
            if cur and curw + gap + w > iw:
                lines.append(cur); cur, curw = [], 0
            curw += (gap if cur else 0) + w
            cur.append((it, w))
        lines.append(cur)
        return lines

    y = 30 if mob else 36
    plan = []
    for i, (k, items) in enumerate(STACK):
        ls = flow(items)
        lh = fs + 14
        h = (36 + len(ls) * lh + 20) if mob else max(len(ls) * lh + 36, 84)
        plan.append((i, k, ls, y, h, lh))
        y += h
    H = round(y + (10 if mob else 14))
    d = Doc("stack", W, H, "Tech stack", alt)
    for i, k, ls, y0, h, lh in plan:
        if i:
            d.hline(M, W - M, y0, HAIR)
        if mob:
            d.text(k, M, y0 + 30, 15, "800", BLUE)
            by = y0 + 36 + fs + 2
        else:
            by = y0 + 28 + fs + 6
            d.text(k, M, by, 16, "800", BLUE)
        for li, row in enumerate(ls):
            x = ix
            for j, (it, w) in enumerate(row):
                d.text(it, x, by + li * lh, fs, "800", INK, -0.01)
                x += w
                if j < len(row) - 1:
                    d.text("/", x + gap / 2, by + li * lh, fs, "500", BLUE, 0, "m")
                    x += gap
    save(d, mob)


# ------------------------------------------------------------------ interests
INT = [("Anime", "Penggemar anime; daftar tontonan ada di MyAnimeList."),
       ("Digital Art", "Suka menggambar dan membuat karya digital."),
       ("Creative Projects", "Mengubah ide menjadi karya visual dan aplikasi."),
       ("Programming", "Terus belajar dan memperdalam full-stack development.")]


def interests(mob):
    alt = "Interests. " + " ".join("%s: %s" % i for i in INT)
    if not mob:
        W, M, H = 1000, 32, 460
        d = Doc("interests", W, H, "Minat", alt)
        poly = "M999 1H660L600 60V459H999Z"
        d.defs.append('<clipPath id="blk"><path d="%s"/></clipPath>' % poly)
        uri = art_image(850, 470, 900, 400, 460, 6.5)
        put_image(d, uri, 600, 0, 400, 460, "blk")
        d.add('<path d="M600 312H999V459H600Z" fill="%s"/>' % PAPER)
        d.add('<path d="M600 312H999" stroke="%s" stroke-width="2.5"/>' % INK)
        d.add('<path d="%s" fill="none" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (poly, INK))
        d.text("Digital Art", 632, 372, 44, "900", INK, -0.03)
        d.lines(wrap(INT[1][1], 17, 340, "600"), 632, 408, 17, 25, "600", INK)
        rx = M
        y = 40
        for i, (k, v) in enumerate([INT[0], INT[2], INT[3]]):
            d.hline(rx, 560, y, INK if i == 0 else HAIR, 3 if i == 0 else 1)
            d.text(k, rx, y + 56, 40, "800", INK, -0.02)
            d.lines(wrap(v, 17, 520 - rx, "500"), rx, y + 88, 17, 25, "500", GRAY)
            y += 136
        d.hline(rx, 560, y, HAIR)
    else:
        W, M = 480, 20
        d = Doc("interests", W, 600, "Minat", alt)
        poly = "M1 1H420L479 40V282H1Z"
        d.defs.append('<clipPath id="blk"><path d="%s"/></clipPath>' % poly)
        uri = art_image(850, 470, 1000, 480, 240, 6)
        put_image(d, uri, 0, 1, 480, 240, "blk")
        d.add('<path d="M1 190H479V282H1Z" fill="%s"/><path d="M1 190H479" stroke="%s" stroke-width="2.5"/>' % (PAPER, INK))
        d.add('<path d="%s" fill="none" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (poly, INK))
        d.text("Digital Art", M, 232, 34, "900", INK, -0.03)
        d.lines(wrap(INT[1][1], 16, W - 2 * M, "600"), M, 262, 16, 22, "600", INK)
        y = 304
        for i, (k, v) in enumerate([INT[0], INT[2], INT[3]]):
            d.hline(M, W - M, y, INK if i == 0 else HAIR, 3 if i == 0 else 1)
            d.text(k, M, y + 44, 30, "800", INK, -0.02)
            d.lines(wrap(v, 16, W - 2 * M, "500"), M, y + 72, 16, 23, "500", GRAY)
            y += 96
        d.hline(M, W - M, y, HAIR)
        d.h = round(y + 12)
        d.body[0] = d.body[0].replace('height="599"', 'height="%d"' % (d.h - 1))
    save(d, mob)


# ------------------------------------------------------------------ chat
def chat(mob):
    msgs = [("r", "Open to interesting projects?"), ("l", "Yes. Pick a channel below."), ("r", "Art or code?"), ("l", "Both.")]
    alt = "Percakapan singkat. Pengunjung: Open to interesting projects? Rizki: Yes. Pick a channel below. Pengunjung: Art or code? Rizki: Both."

    def avatar(d, cx, cy, r, side):
        if side == "r":
            d.add('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (cx, cy, r, PEACH, INK))
            d.text("V", cx, cy + r * 0.34, r * 0.95, "800", INK, 0, "m")
        else:
            d.add('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (cx, cy, r, BLUE))
            d.text("R", cx, cy + r * 0.34, r * 0.95, "800", PAPER, 0, "m")

    if not mob:
        W, H, M = 1000, 340, 32
        d = Doc("chat", W, H, "Say hi", alt)
        d.text("Say", M, 150, 120, "900", INK, -0.04)
        d.text("hi.", M, 262, 120, "900", INK, -0.04)
        d.text("こんにちは", M + 4, 308, 22, "800", GRAY)
        y = 40
        for side, t in msgs:
            fs, r = 18, 20
            w = measure(t, fs, "700") + 40
            if side == "r":
                x = W - M - 2 * r - 12 - w
                ax = W - M - r
            else:
                x = 520 + 2 * r + 12
                ax = 520 + r
            d.rect(x, y, w, 46, BLUE if side == "r" else SLAB, 14)
            d.text(t, x + 20, y + 30, fs, "700", PAPER)
            avatar(d, ax, y + 23, r, side)
            y += 66
    else:
        W, H, M = 480, 420, 20
        d = Doc("chat", W, H, "Say hi", alt)
        d.text("Say hi.", M, 92, 78, "900", INK, -0.04)
        d.text("こんにちは", M + 2, 126, 18, "800", GRAY)
        y = 160
        for side, t in msgs:
            fs, r = 16, 17
            w = measure(t, fs, "700") + 36
            if side == "r":
                x = W - M - 2 * r - 10 - w
                ax = W - M - r
            else:
                x = M + 2 * r + 10
                ax = M + r
            d.rect(x, y, w, 44, BLUE if side == "r" else SLAB, 12)
            d.text(t, x + 18, y + 28, fs, "700", PAPER)
            avatar(d, ax, y + 22, r, side)
            y += 56
    save(d, mob)


CHIPS = [("discord", "Discord", "Server invite", False), ("instagram", "Instagram", "@this_whisky69", False),
         ("tiktok", "TikTok", "@ryynx20", False), ("x", "X", "@ThisRizky699", False),
         ("email", "Email", "rizkyclip69@gmail.com", True), ("mal", "MyAnimeList", "Shakanaa", False),
         ("art-gallery", "Art gallery", "Instagram", False), ("anime-list", "Anime list", "MyAnimeList", False)]


def chip(name, top, sub, primary):
    W, H = 280, 64
    d = Doc("chip-" + name, W, H, "%s, %s" % (top, sub), "Link ke %s: %s" % (top, sub), rx=0, bg=False)
    fill = BLUE if primary else PAPER
    d.add('<path d="M1 1H%s L%s 18 V%s H1Z" fill="%s" stroke="%s" stroke-width="1.5" stroke-linejoin="round"/>' % (W - 18, W - 1, H - 1, fill, INK))
    d.text(top, 20, 28, 17, "800", PAPER if primary else INK)
    d.text(sub, 20, 49, 14, "600", PAPER if primary else GRAY)
    save(d, False)


def button():
    d = Doc("button-88x31", 88, 31, "Portfolio Rizki", "Buka portfolio Rizki", rx=3, bg=False)
    d.rect(0, 0, 88, 31, BLUE, 3)
    d.text("rizki", 44, 21, 15, "900", PAPER, -0.01, "m")
    save(d, False)


# ------------------------------------------------------------------ footer
def footer(mob):
    star = "Kalau kamu suka karya dan proyekku, beri star untuk repo ini ya~"
    made = "Made with code, creativity, and a little bit of kawaii magic"
    alt = "Thanks for visiting my little corner of GitHub. Arigatou gozaimasu. Mata ne. " + star
    if not mob:
        W, H = 1000, 330
        d = Doc("footer", W, H, "Terima kasih sudah berkunjung", alt)
        slashes(d, 32, 34, 202)
        slab(d, 200, 34, 968, 202, 60)
        fs = 410 / measure("Arigatou gozaimasu.", 1, "900", -0.03)
        d.text("Thanks for visiting my little corner of GitHub", 290, 74, 14, "600", PAPER)
        d.text("Arigatou gozaimasu.", 290, 74 + 14 + fs, fs, "900", PAPER, -0.03)
        d.text("Mata ne.", 290, 74 + 14 + fs * 2 + 6, fs, "900", ORANGE, -0.03)
        d.text("ありがとうございます。またね。", 290, 222, 18, "800", PAPER)
        d.lines(wrap(star, 16, 230, "600"), 722, 112, 16, 24, "600", PAPER)
        d.text("Until next time  リズキ", 722, 222, 14, "600", PAPER)
        d.text(made, W / 2, 286, 14, "600", GRAY, 0, "m")
    else:
        W, H, M = 480, 540, 20
        d = Doc("footer", W, H, "Terima kasih sudah berkunjung", alt)
        slashes(d, M, 22, 70)
        slab(d, 20, 112, 460, 336, 40)
        d.text("Thanks for visiting my little corner of GitHub", 64, 146, 13, "600", PAPER)
        d.text("Arigatou", 64, 202, 50, "900", PAPER, -0.03)
        d.text("gozaimasu.", 64, 252, 50, "900", PAPER, -0.03)
        d.text("Mata ne.", 64, 300, 42, "900", ORANGE, -0.03)
        d.text("ありがとうございます。またね。", 64, 336, 16, "800", PAPER)
        d.lines(wrap(star, 15, 380, "600"), 64, 372, 15, 22, "600", PAPER)
        d.text("Until next time  リズキ", 64, 428, 14, "600", PAPER)
        d.lines(wrap(made, 13, W - 2 * M, "600"), M, 484, 13, 19, "600", GRAY)
    save(d, mob)


if __name__ == "__main__":
    home_mark()
    for t, n in NAV:
        nav_chip(t, n.lower())
    for mob in (False, True):
        hero(mob); strip(mob); about(mob); work(mob); stack(mob); interests(mob); chat(mob); footer(mob)
        header("Stats", "統計", "stats", mob)
    for c in CHIPS:
        chip(*c)
    button()
    print(len(DOCS), "files")
