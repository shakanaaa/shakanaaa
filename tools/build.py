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


def hero(mob):
    W = 480 if mob else 1000
    M = 20 if mob else 32
    wm_w = W - 2 * M
    word, tr = "RIZKI", -0.035
    size = wm_w / measure(word, 1, "900", tr)
    top = 22 if mob else 30
    base = top + cap_px(size)
    Y = base + (46 if mob else 66)
    H = round(Y + (552 if mob else 300))
    d = Doc("hero", W, H, "Rizki, developer dan artist dari Indonesia",
            "Wordmark RIZKI dengan halftone biru dan amber di atas hitam, diikuti ringkasan profil.")
    wd, _ = word_d(word, M, base, size, tr)
    d.defs.append('<clipPath id="wm"><path d="%s"/></clipPath>' % wd)
    pitch = 8 if mob else 11
    x0, x1 = M, M + wm_w
    d.add('<g clip-path="url(#wm)"><rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (_n(x0), _n(top - 2), _n(wm_w), _n(base - top + 4), BLUE))
    d.add(halftone(x0, top, x1, base, pitch, lambda u, v: clamp((v - 0.32) / 0.68) * (0.5 + 0.5 * (1 - u)), INK))
    d.add(halftone(x0, top, x1, base, pitch, lambda u, v: clamp((u - 0.5) / 0.5) * clamp((0.9 - v) / 0.9) * 0.95, AMBER, 45))
    d.add("</g>")
    d.add('<path d="%s" fill="none" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (wd, BONE))

    # identity block
    if not mob:
        c1, c2, c3 = M, M + 330, M + 640
        d.text("Rizki //", c1, Y + 6, 30, "800")
        d.lines(["Full-Stack", "Developer", "& Digital Artist"], c1, Y + 58, 36, 40, "800", BONE)
        label(d, "In katakana", c1, Y + 178, 11)
        d.text("リズキ", c1 - 2, Y + 236, 56, "800", BONE)
        label(d, "Base", c2, Y, 12)
        d.rect(c2, Y + 12, 36, 26, BLUE, 3)
        d.text("ID", c2 + 18, Y + 31, 13, "800", BONE, 0.04, "m")
        d.text("Indonesia", c2 + 48, Y + 33, 22, "700")
        label(d, "Now", c2, Y + 82, 12)
        d.lines(wrap("Deepening full-stack development", 20, 280, "700"), c2, Y + 112, 20, 26, "700", BONE)
        label(d, "Collaboration", c2, Y + 214, 12)
        d.add('<circle cx="%s" cy="%s" r="5" fill="%s"/>' % (c2 + 5, Y + 240, AMBER))
        d.lines(wrap("Open to interesting projects", 20, 262, "700"), c2 + 22, Y + 246, 20, 26, "700", BONE)
        d.rect(c3, Y - 22, W - M - c3, 3, BONE)
        for i, (v, p) in enumerate((("CODE", "with curiosity"), ("CREATE", "with feeling"), ("LIVE", "with imagination"))):
            yy = Y + 40 + i * 84
            d.text(v, c3, yy, 46, "900", BONE, -0.02)
            d.text(p, c3, yy + 28, 17, "500", SOFT)
    else:
        d.text("Rizki //", M, Y + 4, 26, "800")
        d.lines(["Full-Stack Developer", "& Digital Artist"], M, Y + 46, 30, 34, "800", BONE)
        label(d, "In katakana", M, Y + 108, 11)
        d.text("リズキ", M - 2, Y + 150, 44, "800", BONE)
        yy = Y + 196
        d.hline(M, W - M, yy - 22, LINE)
        label(d, "Base", M, yy, 12)
        d.rect(M, yy + 10, 34, 24, BLUE, 3)
        d.text("ID", M + 17, yy + 27, 12, "800", BONE, 0.04, "m")
        d.text("Indonesia", M + 44, yy + 29, 20, "700")
        label(d, "Now", 250, yy, 12)
        d.lines(wrap("Deepening full-stack development", 18, 210, "700"), 250, yy + 28, 18, 24, "700", BONE)
        label(d, "Collaboration", M, yy + 92, 12)
        d.add('<circle cx="%s" cy="%s" r="5" fill="%s"/>' % (M + 5, yy + 116, AMBER))
        d.text("Open to interesting projects", M + 20, yy + 122, 18, "700")
        d.rect(M, yy + 156, W - 2 * M, 3, BONE)
        for i, (v, p) in enumerate((("CODE", "with curiosity"), ("CREATE", "with feeling"), ("LIVE", "with imagination"))):
            y3 = yy + 206 + i * 62
            d.text(v, M, y3, 38, "900", BONE, -0.02)
            d.text(p, W - M, y3 - 2, 16, "500", SOFT, 0, "e")
        assert yy + 206 + 2 * 62 + 24 <= H, (yy + 206 + 2 * 62 + 24, H)
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
