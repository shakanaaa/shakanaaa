"""Rebuilds the bundled font subsets in tools/fonts. Needs the Inter, Archivo Black and
Noto Sans CJK fonts installed on the system (paths below). Run after adding new
characters to build.py:  python3 subset_fonts.py
"""
import os
import re
from fontTools import subset
from fontTools.ttLib import TTCollection

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
LATIN = list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) + [0x2019, 0x201C, 0x201D, 0x2026, 0x2013, 0x00D7, 0x2197]
INTER = "/usr/share/fonts/opentype/inter/InterDisplay-%s.otf"
ARCHIVO = "/usr/share/fonts/truetype/google-fonts/ofl/archivoblack/ArchivoBlack-Regular.ttf"
NOTO = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"


def cut(src, dst, unicodes, layout=("kern",)):
    opts = subset.Options()
    opts.notdef_outline = True
    opts.layout_features = list(layout)
    f = subset.load_font(src, opts)
    s = subset.Subsetter(opts)
    s.populate(unicodes=unicodes)
    s.subset(f)
    subset.save_font(f, dst, opts)


cut(ARCHIVO, os.path.join(FONTS, "ArchivoBlack-latin.ttf"), LATIN)
for w in ("Regular", "Medium", "SemiBold", "Bold", "ExtraBold"):
    cut(INTER % w, os.path.join(FONTS, "InterDisplay-%s-latin.otf" % w), LATIN)

src = open(os.path.join(HERE, "build.py"), encoding="utf-8").read()
jp = sorted({ord(c) for c in src if ord(c) > 0x2400})
col = TTCollection(NOTO)
font = [f for f in col.fonts if "JP" in f["name"].getDebugName(1)][0]
opts = subset.Options()
opts.notdef_outline = True
opts.layout_features = []
s = subset.Subsetter(opts)
s.populate(unicodes=jp)
s.subset(font)
font.save(os.path.join(FONTS, "NotoSansCJKjp-Bold-subset.otf"))
print("done,", len(jp), "Japanese characters")
