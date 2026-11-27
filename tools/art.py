"""Turns the source artwork into the flat blue / peach / orange print look.

Four tones: paper white, peach (skin and gloves), orange (the backdrop), blue (hair, cloak,
shadows). Midtones become blue halftone dots on a 45 degree screen.
"""
import base64
import io
import os

import numpy as np
from scipy import ndimage
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "art", "wallhaven-ml2j69.jpg")

PAPER = (255, 255, 255)
PEACH = (255, 220, 196)
ORANGE = (242, 163, 58)
BLUE = (30, 80, 208)


def _smooth(a, r):
    im = Image.fromarray(np.uint8(np.clip(a, 0, 255)))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(r)), dtype=np.float32)


def stylize(box, out_w, out_h, pitch=7.0, ss=2, colors=24):
    """box = (x0, y0, x1, y1) crop in source pixels. Returns PNG bytes at out_w x out_h."""
    src = Image.open(SRC).convert("RGB").crop(box)
    W, H = out_w * ss, out_h * ss
    src = src.resize((W, H), Image.LANCZOS)
    a = np.asarray(src, dtype=np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    lum_s = _smooth(lum, 1.2 * ss)

    sat = a.max(axis=2) - a.min(axis=2)
    orange = ((r - b) > 55) & (r > g + 15) & (g > b)
    orange = _smooth(orange.astype(np.float32) * 255, 1.5 * ss) > 127
    cyan = (g > 170) & (b > 190) & (r < 190)
    cyan = _smooth(cyan.astype(np.float32) * 255, 1.0 * ss) > 110

    # paper = the flat light backdrop (large low-saturation light regions)
    cand = (lum_s > 226) & (sat < 22) & ~orange
    lab, n = ndimage.label(cand)
    sizes = ndimage.sum(cand, lab, range(1, n + 1))
    keep = [i + 1 for i, s_ in enumerate(sizes) if s_ > 0.012 * W * H]
    paper = np.isin(lab, keep) if keep else np.zeros_like(cand)

    out = np.empty((H, W, 3), np.float32)
    out[:] = PEACH
    out[orange] = ORANGE
    out[paper] = PAPER

    solid = (lum_s < 60) & ~orange
    solid |= cyan
    # darkest orange areas (shaded cloak edge) go blue too
    solid |= orange & (lum_s < 52)

    # coverage for the halftone: figure uses the full tonal range, orange only its darker part
    cov_fig = np.clip((205.0 - lum_s) / (205.0 - 70.0), 0, 1) ** 1.35
    cov_org = np.clip((118.0 - lum_s) / (118.0 - 52.0), 0, 1) ** 1.2
    cov = np.where(orange, cov_org, cov_fig)

    ang = np.radians(45)
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    p = pitch * ss
    u = (xs * np.cos(ang) + ys * np.sin(ang)) / p
    v = (-xs * np.sin(ang) + ys * np.cos(ang)) / p
    ci, cj = np.rint(u), np.rint(v)
    cx = (ci * np.cos(ang) - cj * np.sin(ang)) * p
    cy = (ci * np.sin(ang) + cj * np.cos(ang)) * p
    sx = np.clip(cx.astype(np.int32), 0, W - 1)
    sy = np.clip(cy.astype(np.int32), 0, H - 1)
    c = cov[sy, sx]
    rad = np.sqrt(c / np.pi) * p * 1.02
    dist = np.hypot(u - ci, v - cj) * p
    dots = (dist < rad) & (c > 0.08) & ~paper
    out[dots] = BLUE
    out[solid] = BLUE

    img = Image.fromarray(np.uint8(out)).resize((out_w, out_h), Image.LANCZOS)
    img = img.quantize(colors=colors, method=Image.MEDIANCUT, dither=Image.NONE)
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def data_uri(png):
    return "data:image/png;base64," + base64.b64encode(png).decode("ascii")


if __name__ == "__main__":
    import sys
    box = tuple(int(v) for v in sys.argv[1:5])
    w, h = int(sys.argv[5]), int(sys.argv[6])
    png = stylize(box, w, h, pitch=float(sys.argv[7]) if len(sys.argv) > 7 else 7.0)
    open(sys.argv[8] if len(sys.argv) > 8 else "/tmp/art.png", "wb").write(png)
    print(len(png), "bytes")
