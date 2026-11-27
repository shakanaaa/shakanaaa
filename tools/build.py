import os, re, sys
from lib import *
from lib import _n

OUT = sys.argv[1]
os.makedirs(OUT + "/m", exist_ok=True)

DOCS = []


def save(doc, mob):
    if doc.name in MERGED:
        doc = head_into(doc, MERGED[doc.name], mob)
    path = "%s/%s%s.svg" % (OUT, "m/" if mob else "", doc.name)
    open(path, "w", encoding="utf-8").write(doc.svg())
    DOCS.append(path)


def label(d, s, x, y, size=12, fill=MUTE, anchor="s"):
    return d.text(s.upper(), x, y, size, "800", fill, 0.06, anchor)


def word_d(word, x, y, size, track):
    s, w = text_path(word, x, y, size, "900", BONE, track)
    return re.search(r'd="([^"]*)"', s).group(1), w


NAV = [("ABOUT", "about"), ("WORK", "work"), ("STACK", "stack"), ("STATS", "stats"),
       ("INTERESTS", "interests"), ("CONTACT", "contact")]


def nav_chip(text, name):
    w = measure(text, 13, "800", 0.06) + 36
    d = Doc("nav-" + name, round(w), 38, "Menu: " + text.title(), "Link ke bagian %s" % text.title(), rx=4)
    d.text(text, w / 2, 24, 13, "800", BONE, 0.06, "m")
    save(d, False)


ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "art", "wallhaven-ml2j69.jpg")


def photo_uri(box, w, h, scale=2, quality=86):
    """The artwork in its original colours, cropped to `box` (source pixels) and resized to w x h."""
    from PIL import Image
    import base64, io
    im = Image.open(ART).convert("RGB").crop(box).resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def diamonds(d, cx, cy, u):
    def dia(x, y, fill):
        d.add('<path d="M%s %sL%s %sL%s %sL%s %sZ" fill="%s" stroke="%s" stroke-width="1.5"/>'
              % (_n(x), _n(y - u), _n(x + u), _n(y), _n(x), _n(y + u), _n(x - u), _n(y), fill, INK))
    dia(cx, cy - u, BLUE)
    dia(cx - u, cy, BLUE_HI)
    dia(cx + u, cy, BONE)
    dia(cx, cy + u, AMBER)


def slashes(d, x, y, h):
    w = h * 0.5
    lean = h * 0.32
    for i, fill in enumerate((AMBER, BLUE_HI)):
        xx = x + i * (w + h * 0.12)
        d.add('<path d="M%s %sH%s L%s %sH%s Z" fill="%s"/>'
              % (_n(xx + lean), _n(y), _n(xx + lean + w), _n(xx + w), _n(y + h), _n(xx), fill))


def arch(x0, w, y, b, r=None):
    """Flat-bottomed arch: semicircle top, straight sides. r defaults to w / 2."""
    r = w / 2 if r is None else r
    return "M%s %sV%sA%s %s 0 0 1 %s %sV%sZ" % (_n(x0), _n(b), _n(y + r), _n(r), _n(r), _n(x0 + w), _n(y + r), _n(b))


def bubble(d, side, text, x_edge, y, fs, r, h):
    w = measure(text, fs, "700") + fs * 2
    if side == "r":
        x = x_edge - 2 * r - 10 - w
        ax = x_edge - r
        d.rect(x, y, w, h, BLUE, h / 3)
        d.text(text, x + fs, y + h / 2 + fs * 0.35, fs, "700", BONE)
        d.add('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (_n(ax), _n(y + h / 2), r, BONE))
        d.text("V", ax, y + h / 2 + r * 0.34, r * 0.95, "800", INK, 0, "m")
    else:
        x = x_edge + 2 * r + 10
        ax = x_edge + r
        d.rect(x + 0.5, y + 0.5, w, h, INK2, h / 3, LINE)
        d.text(text, x + fs, y + h / 2 + fs * 0.35, fs, "700", BONE)
        d.add('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (_n(ax), _n(y + h / 2), r, BLUE))
        d.text("R", ax, y + h / 2 + r * 0.34, r * 0.95, "800", BONE, 0, "m")


MSGS = [("r", "Open to interesting projects?"), ("l", "Yes. Pick a channel below."), ("r", "Art or code?"), ("l", "Both.")]
PRINCIPLES = (("Code", "with curiosity"), ("Create", "with feeling"), ("Live", "with imagination"))
SEGS = (BLUE, BLUE_HI, AMBER)
FACTS = (("Focus", "Full-stack development"), ("Creative", "Drawing & digital art"), ("Off-screen", "Anime"))
JP = ["好奇心でコードを書き、", "感情で創り、", "想像力で生きる。"]


def hero(mob):
    W = 480 if mob else 1000
    M = 20 if mob else 32
    cw = W - 2 * M
    top_y, top_h = (20, 40) if mob else (24, 44)
    box_y = top_y + top_h + (18 if mob else 22)
    box_h = 112 if mob else 100
    art_y = box_y + box_h + (22 if mob else 26)
    art_h = 160 if mob else 300
    art_b = art_y + art_h
    iy = art_b + (30 if mob else 36)
    if mob:
        info_h = 112 + 3 * 46 + 22 + 3 * 24 + 8 + 56 + 4 * 46 + 28
    else:
        info_h = 262
    slab_y = iy + info_h + (24 if mob else 28)
    slab_h = 96 if mob else 108
    H = round(slab_y + slab_h + 28)
    d = Doc("hero", W, H, "Rizki, developer dan artist dari Indonesia",
            "Ilustrasi karakter berambut panjang dengan jubah hijau gelap menunjuk ke arah pembaca, dipotong menjadi tiga bentuk bulat besar. Rizki, Full-Stack Developer dan Digital Artist dari Indonesia, terbuka untuk proyek menarik. Code with curiosity, create with feeling, live with imagination.")

    # ---- top bar: logo, menu, status
    d.rect(M, top_y, top_h, top_h, BLUE, 8)
    d.text("R", M + top_h / 2, top_y + top_h / 2 + (9 if mob else 10), 26 if mob else 28, "900", BONE, 0, "m")
    mx = M + top_h + (18 if mob else 30)
    fs = 14 if mob else 16
    for i, (v, _) in enumerate(PRINCIPLES):
        wgt = "800" if i == 1 else "500"
        w = d.text(v, mx, top_y + top_h / 2 + fs * 0.35, fs, wgt, BONE if i == 1 else SOFT)
        mx += w + (16 if mob else 30)
    if not mob:
        t = "Open to interesting projects"
        pw = measure(t, 15, "700") + 58
        px = W - M - pw
        d.rect(px + 0.75, top_y + 0.75, pw - 1.5, top_h - 1.5, INK2, 10, BONE, 1.5)
        d.add('<circle cx="%s" cy="%s" r="6" fill="%s"/>' % (_n(px + 22), top_y + top_h / 2, AMBER))
        d.text(t, px + 38, top_y + top_h / 2 + 5.5, 15, "700", BONE)

    # ---- status box with segmented bar
    d.rect(M + 0.75, box_y + 0.75, cw - 1.5, box_h - 1.5, "none", 12, BONE, 1.5)
    px0 = M + (18 if mob else 24)
    pw_ = cw - 2 * (18 if mob else 24)
    label(d, "Now", px0, box_y + 28, 12, MUTE)
    d.text("Deepening full-stack development", px0 + 46, box_y + 29, 15 if mob else 18, "700", BONE)
    if not mob:
        iw = measure("Indonesia", 18, "700")
        tx = W - M - 24 - iw - 10 - 34
        d.text("Indonesia", W - M - 24, box_y + 29, 18, "700", BONE, 0, "e")
        d.rect(tx, box_y + 12, 34, 20, BLUE, 3)
        d.text("ID", tx + 17, box_y + 27, 12, "800", BONE, 0.04, "m")
        label(d, "Base", tx - 14, box_y + 28, 12, MUTE, "e")
    gap = 8
    sw = (pw_ - 2 * gap) / 3
    for i, (v, p) in enumerate(PRINCIPLES):
        x = px0 + i * (sw + gap)
        d.rect(x, box_y + 44, sw, 10, SEGS[i], 5)
        if mob:
            d.text(v, x, box_y + 78, 14, "800", BONE)
            d.text(p, x, box_y + 96, 12, "500", SOFT)
        else:
            wv = d.text(v, x, box_y + 82, 15, "800", BONE)
            d.text(p, x + wv + 7, box_y + 82, 15, "500", SOFT)

    # ---- artwork in three arches
    if mob:
        aw = (cw + 20) / 3
        arches = [arch(M + i * (aw - 10), aw, art_y, art_b) for i in range(3)]
        box = (0, 150, 1860, 150 + round(1860 * art_h / cw))
    else:
        arches = [arch(M, 330, art_y, art_b, 150), arch(M + 312, 312, art_y, art_b), arch(M + 624, 312, art_y, art_b)]
        box = (0, 222, 1860, 222 + round(1860 * art_h / cw))
    d.defs.append('<clipPath id="art">%s</clipPath>' % "".join('<path d="%s"/>' % a for a in arches))
    d.add('<image href="%s" x="%s" y="%s" width="%s" height="%s" preserveAspectRatio="none" clip-path="url(#art)"/>'
          % (photo_uri(box, cw, art_h), M, art_y, cw, art_h))
    for a in arches:
        d.add('<path d="%s" fill="none" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (a, BONE))

    # ---- info columns
    if not mob:
        c1, c2, c3 = M, M + 330, M + 640
        d.text("Rizki //", c1, iy + 22, 26, "800", BONE, -0.01)
        d.lines(["Full-Stack", "Developer", "& Digital Artist"], c1, iy + 70, 36, 40, "800", BONE, -0.02)
        d.lines(JP, c1, iy + 184, 16, 26, "800", SOFT)
        d.rect(c2, iy, 280, 3, BONE)
        for i, (k, v) in enumerate(FACTS):
            yy = iy + 36 + i * 62
            label(d, k, c2, yy, 12, MUTE)
            d.text(v, c2, yy + 25, 20, "700", BONE)
        diamonds(d, c2 + 252, iy + 228, 14)
        d.text("リズキ", c2, iy + 242, 28, "800", BONE)
        d.rect(c3, iy, W - M - c3, 3, BONE)
        d.text("Say hi.", W - M, iy + 44, 36, "900", BONE, -0.02, "e")
        d.text("こんにちは", W - M, iy + 68, 14, "800", MUTE, 0, "e")
        by = iy + 90
        for side, t in MSGS:
            bubble(d, side, t, (W - M) if side == "r" else c3, by, 15, 16, 36)
            by += 40
    else:
        d.text("Rizki //", M, iy + 20, 24, "800", BONE, -0.01)
        d.lines(["Full-Stack Developer", "& Digital Artist"], M, iy + 60, 30, 34, "800", BONE, -0.02)
        yy = iy + 112
        d.rect(M, yy, cw, 3, BONE)
        for i, (k, v) in enumerate(FACTS):
            y3 = yy + 30 + i * 46
            label(d, k, M, y3, 12, MUTE)
            d.text(v, M, y3 + 21, 18, "700", BONE)
        diamonds(d, W - M - 44, yy + 56, 12)
        d.text("リズキ", W - M, yy + 124, 24, "800", BONE, 0, "e")
        jy = yy + 30 + 3 * 46 + 22
        d.lines(JP, M, jy, 16, 24, "800", SOFT)
        cy_ = jy + 3 * 24 + 8
        d.rect(M, cy_, cw, 3, BONE)
        d.text("Say hi.", M, cy_ + 40, 30, "900", BONE, -0.02)
        d.text("こんにちは", W - M, cy_ + 38, 13, "800", MUTE, 0, "e")
        by = cy_ + 56
        for side, t in MSGS:
            bubble(d, side, t, (W - M) if side == "r" else M, by, 14, 14, 34)
            by += 46

    # ---- bottom slab
    if not mob:
        slashes(d, M, slab_y, slab_h)
        sx0 = M + 188
        d.add('<path d="M%s %sH%s V%s H%s Z" fill="%s"/>' % (_n(sx0 + 34), slab_y, W - M, slab_y + slab_h, sx0, BLUE))
        col = (W - M - sx0 - 70) / 3
        for i, (k, v) in enumerate(FACTS):
            x = sx0 + 56 + i * col
            label(d, k, x, slab_y + 34, 12, BONE)
            d.text(("Full-stack", "Digital art", "Anime")[i], x, slab_y + 78, 30, "900", BONE, -0.01)
    else:
        slashes(d, M, slab_y, 44)
        sx0 = M + 92
        d.add('<path d="M%s %sH%s V%s H%s Z" fill="%s"/>' % (_n(sx0 + 22), slab_y, W - M, slab_y + slab_h, sx0, BLUE))
        col = (W - M - sx0 - 20) / 3
        names = ("Full-stack", "Digital art", "Anime")
        for i, (k, v) in enumerate(FACTS):
            x = sx0 + 30 + i * (col - 4)
            label(d, k, x, slab_y + 34, 11, BONE)
            d.text(names[i], x, slab_y + 66, 16, "900", BONE, -0.01)
    save(d, mob)


def strip(mob):
    items = ["Building something interesting.", "Turning ideas into code.",
             "Creating art and digital experiences.", "Always learning something new."]
    if not mob:
        W, H, M = 1000, 128, 32
        d = Doc("strip", W, H, "Empat prinsip kerja", "Building something interesting. Turning ideas into code. Creating art and digital experiences. Always learning something new.")
        cw = (W - 2 * M) / 4
        for i, t in enumerate(items):
            x = M + i * cw
            d.rect(x, 26, 28, 3, BLUE_HI if i else AMBER)
            label(d, "0%d" % (i + 1), x, 52, 12)
            d.lines(wrap(t, 19, cw - 28, "700"), x, 80, 19, 25, "700", BONE)
    else:
        W, H, M = 480, 224, 20
        d = Doc("strip", W, H, "Empat prinsip kerja", "Building something interesting. Turning ideas into code. Creating art and digital experiences. Always learning something new.")
        cw = (W - 2 * M) / 2
        for i, t in enumerate(items):
            x = M + (i % 2) * cw
            y = 26 + (i // 2) * 96
            d.rect(x, y, 28, 3, BLUE_HI if i else AMBER)
            label(d, "0%d" % (i + 1), x, y + 26, 12)
            d.lines(wrap(t, 17, cw - 20, "700"), x, y + 52, 17, 22, "700", BONE)
    save(d, mob)


HEADS = [("01", "About", "自己紹介", "about"), ("02", "Work", "作品", "work"), ("03", "Stack", "技術", "stack"),
         ("04", "Stats", "統計", "stats"), ("05", "Interests", "興味", "interests"), ("06", "Contact", "連絡", "contact")]


def draw_header(d, num, title, jp, mob, H):
    W, M = d.w, (20 if mob else 32)
    s = 34 if mob else 40
    ty = H / 2 - s / 2 + (2 if mob else 4)
    d.rect(M, ty, s, s, BLUE, 3)
    d.text(num, M + s / 2, ty + s / 2 + (6 if mob else 7), 16 if mob else 18, "800", BONE, 0, "m")
    fs = 40 if mob else 58
    tx = M + s + (14 if mob else 18)
    tw = d.text(title, tx, ty + s / 2 + cap_px(fs) / 2, fs, "900", BONE, -0.03)
    jw = measure(jp, 18 if mob else 22, "800")
    d.text(jp, W - M, ty + s / 2 + (7 if mob else 8), 18 if mob else 22, "800", MUTE, 0, "e")
    lx1, lx2 = tx + tw + 20, W - M - jw - 20
    if lx2 - lx1 > 24:
        d.hline(lx1, lx2, ty + s / 2, LINE, 2)


def head_into(inner, key, mob):
    num, title, jp = MERGED_HEADS[key]
    hh = 84 if mob else 112
    d = Doc(inner.name, inner.w, inner.h + hh, inner.title, inner.desc)
    draw_header(d, num, title, jp, mob, hh)
    d.defs = inner.defs
    d.add('<g transform="translate(0,%d)">' % hh)
    d.body.extend(inner.body[1:])
    d.add("</g>")
    return d


def header(num, title, jp, name, mob):
    d = Doc("sec-" + name, 480 if mob else 1000, 84 if mob else 112, "%s %s" % (num, title), "Judul bagian %s" % title)
    draw_header(d, num, title, jp, mob, d.h)
    save(d, mob)


MERGED = {"about": "about", "work": "work", "stack": "stack", "interests": "interests", "chat": "contact"}
MERGED_HEADS = {"about": ("01", "About", "自己紹介"), "work": ("02", "Work", "作品"), "stack": ("03", "Stack", "技術"),
                "interests": ("05", "Interests", "興味"), "contact": ("06", "Contact", "連絡")}


def about(mob):
    rows = [("Name", "Rizki  リズキ"), ("Location", "Indonesia"), ("Role", "Full-Stack Developer"),
            ("Focus", "Full-Stack Development"), ("Creative", "Drawing & Digital Art"),
            ("Off-screen", "Anime"), ("Collab", "Open to interesting projects")]
    intro = "Developer sekaligus artist dari Indonesia. Aku suka mengeksplorasi programming, menggambar, digital art, dan anime. Saat ini aku sedang memperdalam full-stack development sambil terus membuat hal-hal kreatif."
    if not mob:
        W, M = 1000, 32
        lw, vx = 420, 150
        y = 56
        lay = []
        for k, v in rows:
            ls = wrap(v, 20, lw - (vx - M) + 20, "600")
            lay.append((k, ls, y))
            y += max(1, len(ls)) * 26 + 26
        left_end = y
        # right
        rx = 520
        pl = wrap(intro, 19, W - M - rx, "500")
        right_end = 232 + len(pl) * 29 + 70
        H = round(max(left_end, right_end) + 24)
        d = Doc("about", W, H, "Tentang Rizki", "Halo, aku Rizki. " + intro + " Nama Rizki, lokasi Indonesia, peran Full-Stack Developer, fokus Full-Stack Development, sisi kreatif Drawing dan Digital Art, di luar layar Anime, terbuka untuk kolaborasi proyek menarik.")
        for k, ls, yy in lay:
            d.hline(M, M + lw, yy - 30, LINE)
            label(d, k, M, yy, 12)
            d.lines(ls, vx, yy + 1, 20, 26, "600", BONE)
        # slab
        d.add('<path d="M%s 32H%s V176 H%s Z" fill="%s"/>' % (rx + 44, W - 0.5, rx, BLUE))
        d.add('<path d="M%s 32 L%s 32 L%s 76 Z" fill="%s"/>' % (rx, rx + 44, rx, INK))
        d.text("Halo, aku", rx + 72, 96, 40, "900", BONE, -0.02)
        d.text("Rizki.", rx + 72, 150, 56, "900", BONE, -0.03)
        d.lines(pl, rx, 232, 19, 29, "500", SOFT)
        d.text("hor hor hor~ thanks for stopping by", rx, 232 + len(pl) * 29 + 36, 15, "700", AMBER)
    else:
        W, M = 480, 20
        pl = wrap(intro, 17, W - 2 * M, "500")
        y = 202 + len(pl) * 26 + 70
        lay = []
        for k, v in rows:
            ls = wrap(v, 18, 280, "600")
            lay.append((k, ls, y))
            y += max(1, len(ls)) * 24 + 26
        H = round(y + 6)
        d = Doc("about", W, H, "Tentang Rizki", "Halo, aku Rizki. " + intro)
        d.add('<path d="M%s 22H%s V138 H%s Z" fill="%s"/>' % (M + 32, W - 0.5, 0.5, BLUE))
        d.add('<path d="M0.5 22 L%s 22 L0.5 54 Z" fill="%s"/>' % (M + 32, INK))
        d.text("Halo, aku", M + 24, 78, 32, "900", BONE, -0.02)
        d.text("Rizki.", M + 24, 122, 44, "900", BONE, -0.03)
        d.lines(pl, M, 176, 17, 26, "500", SOFT)
        d.text("hor hor hor~ thanks for stopping by", M, 176 + len(pl) * 26 + 28, 14, "700", AMBER)
        for k, ls, yy in lay:
            d.hline(M, W - M, yy - 28, LINE)
            label(d, k, M, yy - 4, 12)
            d.lines(ls, 170, yy - 3, 18, 24, "600", BONE)
    save(d, mob)


def work(mob):
    desc = "Personal website inspired by the pause menu of Persona 3 Reload."
    alt = "Featured project 01: Persona 3 Reload Portfolio. " + desc + " Personal website, best viewed on desktop. Open live demo."

    def arrow(d, x, y, s):
        d.add('<path d="M%s %s L%s %s M%s %s H%s V%s" fill="none" stroke="%s" stroke-width="2.4" stroke-linecap="square"/>'
              % (x, y + s, x + s, y, x, y, x + s, y + s, BONE))

    if not mob:
        W, H, M = 1000, 400, 32
        d = Doc("work", W, H, "Proyek unggulan: Persona 3 Reload Portfolio", alt)
        d.defs.append('<clipPath id="slab"><path d="M650 0.5H999.5V399.5H560Z"/></clipPath>')
        d.add('<g clip-path="url(#slab)"><rect x="540" y="0" width="460" height="400" fill="%s"/>' % BLUE)
        d.add(halftone(540, 0, 1000, 400, 12, lambda u, v: clamp((v - 0.3) / 0.7) * clamp(1.1 - u * 0.9), INK))
        d.add(halftone(540, 0, 1000, 400, 12, lambda u, v: clamp((u - 0.45) / 0.55) * clamp((0.7 - v) / 0.7) * 0.9, AMBER))
        d.add("</g>")
        label(d, "Featured / 01", M, 56, 12, BLUE_TXT)
        d.text("Persona 3 Reload", M, 130, 56, "900", BONE, -0.03)
        d.text("Portfolio", M, 192, 56, "900", BONE, -0.03)
        d.lines(wrap(desc, 19, 440, "500"), M, 240, 19, 28, "500", SOFT)
        tx = M
        for t in ("PERSONAL WEBSITE", "BEST VIEWED ON DESKTOP"):
            w = measure(t, 12, "800", 0.06) + 24
            d.rect(tx + 0.5, 300.5, w, 30, "none", 3, LINE)
            d.text(t, tx + 12, 320, 12, "800", SOFT, 0.06)
            tx += w + 10
        d.text("More little creations will be added here as they grow~", M, 372, 14, "500", MUTE)
        d.rect(700, 292, 240, 56, INK, 4)
        d.text("Open live demo", 724, 327, 18, "800", BONE)
        arrow(d, 900, 311, 16)
    else:
        W, H, M = 480, 562, 20
        d = Doc("work", W, H, "Proyek unggulan: Persona 3 Reload Portfolio", alt)
        d.defs.append('<clipPath id="slab"><path d="M0.5 0.5H479.5V120 L0.5 150Z"/></clipPath>')
        d.add('<g clip-path="url(#slab)"><rect x="0" y="0" width="480" height="160" fill="%s"/>' % BLUE)
        d.add(halftone(0, 0, 480, 150, 9, lambda u, v: clamp((v - 0.2) / 0.8) * clamp(1.1 - u * 0.5), INK))
        d.add(halftone(0, 0, 480, 150, 9, lambda u, v: clamp((u - 0.4) / 0.6) * clamp((0.8 - v) / 0.8) * 0.9, AMBER))
        d.add("</g>")
        label(d, "Featured / 01", M, 190, 12, BLUE_TXT)
        d.text("Persona 3 Reload", M, 238, 40, "900", BONE, -0.03)
        d.text("Portfolio", M, 282, 40, "900", BONE, -0.03)
        d.lines(wrap(desc, 17, W - 2 * M, "500"), M, 320, 17, 25, "500", SOFT)
        tx, ty = M, 380
        for t in ("PERSONAL WEBSITE", "BEST VIEWED ON DESKTOP"):
            w = measure(t, 12, "800", 0.06) + 24
            if tx + w > W - M:
                tx, ty = M, ty + 40
            d.rect(tx + 0.5, ty + 0.5, w, 30, "none", 3, LINE)
            d.text(t, tx + 12, ty + 20, 12, "800", SOFT, 0.06)
            tx += w + 10
        d.rect(M, 456, W - 2 * M, 56, BLUE, 4)
        d.text("Open live demo", M + 24, 491, 18, "800", BONE)
        arrow(d, W - M - 40, 475, 16)
        d.text("More little creations will be added here.", M, 540, 13, "500", MUTE)
    save(d, mob)


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
        if mob:
            h = 38 + len(ls) * lh + 20
        else:
            h = max(len(ls) * lh + 36, 84)
        plan.append((i, k, ls, y, h, lh))
        y += h
    H = round(y + (10 if mob else 14))
    d = Doc("stack", W, H, "Tech stack", alt)
    for i, k, ls, y0, h, lh in plan:
        if i:
            d.hline(M, W - M, y0, LINE)
        if mob:
            d.text("0%d" % (i + 1), M, y0 + 32, 12, "800", BLUE_TXT, 0.06)
            label(d, k, M + 30, y0 + 32, 13, BONE)
            by = y0 + 38 + fs + 4
        else:
            by = y0 + 28 + fs + 6
            d.text("0%d" % (i + 1), M, by, 12, "800", BLUE_TXT, 0.06)
            label(d, k, M + 32, by, 14, BONE)
        for li, row in enumerate(ls):
            x = ix
            for j, (it, w) in enumerate(row):
                d.text(it, x, by + li * lh, fs, "800", BONE, -0.01)
                x += w
                if j < len(row) - 1:
                    d.text("/", x + gap / 2, by + li * lh, fs, "500", BLUE_HI, 0, "m")
                    x += gap
    save(d, mob)


INT = [("Anime", "Penggemar anime; daftar tontonan ada di MyAnimeList."),
       ("Digital Art", "Suka menggambar dan membuat karya digital."),
       ("Creative Projects", "Mengubah ide menjadi karya visual dan aplikasi."),
       ("Programming", "Terus belajar dan memperdalam full-stack development.")]


def interests(mob):
    alt = "Interests. " + " ".join("%s: %s" % i for i in INT)
    if not mob:
        W, M = 1000, 32
        d = Doc("interests", W, 460, "Minat", alt)
        d.defs.append('<clipPath id="blk"><path d="M999.5 0.5H660L600 60V459.5H999.5Z"/></clipPath>')
        d.add('<g clip-path="url(#blk)"><rect x="600" y="0" width="400" height="460" fill="%s"/>' % BLUE)
        d.add(halftone(600, 336, 1000, 460, 12, lambda u, v: clamp((v + 0.1) / 1.1) * clamp(1.2 - u * 0.8), INK))
        d.add(halftone(600, 336, 1000, 460, 12, lambda u, v: clamp((0.65 - u) / 0.65) * clamp((0.9 - v) / 0.9) * 0.95, AMBER))
        d.add("</g>")
        bx = 632
        label(d, "Main / 01", bx, 62, 12, BONE)
        d.text("Digital", bx, 150, 62, "900", BONE, -0.03)
        d.text("Art", bx, 212, 62, "900", BONE, -0.03)
        d.lines(wrap(INT[1][1], 18, 300, "600"), bx, 256, 18, 26, "600", BONE)
        rx = M
        y = 40
        for i, (k, v) in enumerate([INT[0], INT[2], INT[3]]):
            d.hline(rx, 560, y, LINE)
            d.text("0%d" % (i + 2), rx, y + 46, 12, "800", BLUE_TXT, 0.06)
            d.text(k, rx + 40, y + 52, 40, "800", BONE, -0.02)
            d.lines(wrap(v, 17, 560 - rx - 40, "500"), rx + 40, y + 86, 17, 25, "500", SOFT)
            y += 136
        d.hline(rx, 560, y, LINE)
    else:
        W, M = 480, 20
        d = Doc("interests", W, 560, "Minat", alt)
        d.defs.append('<clipPath id="blk"><path d="M0.5 0.5H420L479.5 40V250H0.5Z"/></clipPath>')
        d.add('<g clip-path="url(#blk)"><rect x="0" y="0" width="480" height="260" fill="%s"/>' % BLUE)
        d.add(halftone(0, 186, 480, 250, 9, lambda u, v: clamp((v + 0.1) / 1.1) * clamp(0.4 + u * 0.7), INK))
        d.add(halftone(0, 186, 480, 250, 9, lambda u, v: clamp((u - 0.5) / 0.5) * clamp((0.9 - v) / 0.9) * 0.9, AMBER))
        d.add("</g>")
        label(d, "Main / 01", M, 46, 12, BONE)
        d.text("Digital Art", M, 108, 48, "900", BONE, -0.03)
        d.lines(wrap(INT[1][1], 17, 400, "600"), M, 148, 17, 25, "600", BONE)
        y = 262
        for i, (k, v) in enumerate([INT[0], INT[2], INT[3]]):
            d.hline(M, W - M, y, LINE)
            d.text("0%d" % (i + 2), M, y + 36, 12, "800", BLUE_TXT, 0.06)
            d.text(k, M + 34, y + 42, 28, "800", BONE, -0.02)
            d.lines(wrap(v, 16, W - 2 * M - 34, "500"), M + 34, y + 68, 16, 23, "500", SOFT)
            y += 104
        d.hline(M, W - M, y, LINE)
        d.h = round(y + 12)
        d.body[0] = d.body[0].replace('height="559"', 'height="%d"' % (d.h - 1))
    save(d, mob)


def chat(mob):
    msgs = [("r", "Open to interesting projects?"), ("l", "Yes. Pick a channel below."), ("r", "Art or code?"), ("l", "Both.")]
    alt = "Percakapan singkat. Pengunjung: Open to interesting projects? Rizki: Yes. Pick a channel below. Pengunjung: Art or code? Rizki: Both."
    if not mob:
        W, H, M = 1000, 330, 32
        d = Doc("chat", W, H, "Say hi", alt)
        d.text("Say", M, 150, 120, "900", BONE, -0.04)
        d.text("hi.", M, 262, 120, "900", BONE, -0.04)
        d.text("こんにちは", M + 4, 306, 22, "800", MUTE)
        y = 38
        for side, t in msgs:
            fs = 18
            w = measure(t, fs, "800") + 40
            x = W - M - w if side == "r" else 520
            fill = BLUE if side == "r" else INK2
            st = "" if side == "r" else ' stroke="%s"' % LINE
            d.add('<rect x="%s" y="%s" width="%s" height="50" rx="14" fill="%s"%s/>' % (_n(x), y, _n(w), fill, st))
            d.text(t, x + 20, y + 32, fs, "800", BONE)
            y += 66
    else:
        W, H, M = 480, 396, 20
        d = Doc("chat", W, H, "Say hi", alt)
        d.text("Say hi.", M, 92, 78, "900", BONE, -0.04)
        d.text("こんにちは", M + 2, 124, 18, "800", MUTE)
        y = 156
        for side, t in msgs:
            fs = 16
            w = measure(t, fs, "800") + 36
            x = W - M - w if side == "r" else M
            fill = BLUE if side == "r" else INK2
            st = "" if side == "r" else ' stroke="%s"' % LINE
            d.add('<rect x="%s" y="%s" width="%s" height="42" rx="12" fill="%s"%s/>' % (_n(x), y, _n(w), fill, st))
            d.text(t, x + 18, y + 27, fs, "800", BONE)
            y += 54
    save(d, mob)


CHIPS = [("discord", "DISCORD", "Server invite", False), ("instagram", "INSTAGRAM", "@this_whisky69", False),
         ("tiktok", "TIKTOK", "@ryynx20", False), ("x", "X", "@ThisRizky699", False),
         ("email", "EMAIL", "rizkyclip69@gmail.com", True), ("mal", "MYANIMELIST", "Shakanaa", False),
         ("art-gallery", "ART GALLERY", "Instagram", False), ("anime-list", "ANIME LIST", "MyAnimeList", False)]


def chip(name, top, sub, primary):
    W, H = 280, 64
    d = Doc("chip-" + name, W, H, "%s, %s" % (top.title(), sub), "Link ke %s: %s" % (top.title(), sub), rx=0, bg=False)
    fill = BLUE if primary else INK2
    st = "" if primary else ' stroke="%s"' % LINE
    d.add('<path d="M0.5 0.5H%s L%s 16 V%s H0.5Z" fill="%s"%s/>' % (W - 16, W - 0.5, H - 0.5, fill, st))
    d.text(top, 20, 28, 15, "800", BONE, 0.06)
    d.text(sub, 20, 49, 14, "600", BONE if primary else SOFT)
    save(d, False)


def button():
    d = Doc("button-88x31", 88, 31, "Portfolio Rizki", "Buka portfolio Rizki", rx=3, bg=False)
    d.rect(0, 0, 88, 31, BLUE, 3)
    d.text("rizki", 44, 21, 15, "900", BONE, -0.01, "m")
    save(d, False)


def footer(mob):
    star = "Kalau kamu suka karya dan proyekku, beri star untuk repo ini ya~"
    made = "MADE WITH CODE, CREATIVITY, AND A LITTLE BIT OF KAWAII MAGIC"
    alt = "Thanks for visiting my little corner of GitHub. Arigatou gozaimasu. Mata ne. " + star
    if not mob:
        W, H = 1000, 330
        d = Doc("footer", W, H, "Terima kasih sudah berkunjung", alt)
        d.add('<path d="M70 34H160L120 236H30Z" fill="%s"/><path d="M178 34H246L206 236H138Z" fill="%s"/>' % (AMBER, BLUE_HI))
        d.add('<path d="M262 34H999.5V236H222Z" fill="%s"/>' % BLUE)
        fs = 410 / measure("Arigatou gozaimasu.", 1, "900", -0.03)
        label(d, "Thanks for visiting my little corner of GitHub", 300, 74, 12, BONE)
        d.text("Arigatou gozaimasu.", 300, 74 + 14 + fs, fs, "900", BONE, -0.03)
        d.text("Mata ne.", 300, 74 + 14 + fs * 2 + 6, fs, "900", INK, -0.03)
        d.text("ありがとうございます。またね。", 300, 222, 18, "800", BONE)
        d.lines(wrap(star, 16, 240, "600"), 732, 112, 16, 24, "600", BONE)
        label(d, "Until next time  リズキ", 732, 222, 12, BONE)
        d.text(made, W / 2, 286, 12, "800", MUTE, 0.06, "m")
    else:
        W, H, M = 480, 520, 20
        d = Doc("footer", W, H, "Terima kasih sudah berkunjung", alt)
        d.add('<path d="M40 22H112L92 82H20Z" fill="%s"/><path d="M126 22H176L156 82H106Z" fill="%s"/>' % (AMBER, BLUE_HI))
        d.add('<path d="M0.5 100H479.5V436H0.5Z" fill="%s"/>' % BLUE)
        label(d, "Thanks for visiting my little corner of GitHub", M, 134, 12, BONE)
        d.text("Arigatou", M, 190, 52, "900", BONE, -0.03)
        d.text("gozaimasu.", M, 242, 52, "900", BONE, -0.03)
        d.text("Mata ne.", M, 290, 42, "900", INK, -0.03)
        d.text("ありがとうございます。またね。", M, 326, 17, "800", BONE)
        d.lines(wrap(star, 15, W - 2 * M, "600"), M, 362, 15, 22, "600", BONE)
        label(d, "Until next time  リズキ", M, 418, 12, BONE)
        d.lines(wrap(made, 12, W - 2 * M, "800", 0.06), M, 474, 12, 18, "800", MUTE, 0.06)
    save(d, mob)


if __name__ == "__main__":
    for t, n in NAV:
        nav_chip(t, n.lower())
    for mob in (False, True):
        hero(mob); strip(mob); about(mob); work(mob); stack(mob); interests(mob); chat(mob); footer(mob)
        header("04", "Stats", "統計", "stats", mob)
    for c in CHIPS:
        chip(*c)
    button()
    print(len(DOCS), "files")
