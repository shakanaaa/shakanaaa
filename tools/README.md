# Panel generator

Every panel in `assets/` is generated here. Text is converted to outlines, so the fonts look the same on any device, and the artwork is embedded in the SVGs, so each panel is one self-contained file.

```bash
cd tools
pip install fonttools pillow numpy scipy
python3 build.py ../assets
```

No `npm install` is needed. The fonts are bundled in `fonts/` (see `fonts/README.md`).

## What lives where

- `lib.py`: palette constants, font loading, text-to-outline, the `Doc` canvas.
- `build.py`: one function per panel, each with a desktop and a mobile version.
- `art.py`: turns the artwork in `art/` into the flat blue, peach and orange print with halftone dots. Change the crop of any panel in `build.py` (`art_image(cx, cy, width, ...)`: centre and width in source pixels).
- `subset_fonts.py`: rebuilds the font subsets. Only needed after you add new Japanese characters to `build.py` (it needs Inter, Archivo Black and Noto Sans CJK installed on your system).

## Design tokens

| Token | Value | Use |
| --- | --- | --- |
| Paper | `#FFFFFF` | Panel background |
| Ink | `#1B1B1F` | Text, outlines, rules |
| Blue | `#1E50D0` | Identity color: `//`, tags, chat bubbles, links |
| Peach | `#FFDCC4` | Skin tone in the artwork, visitor avatar |
| Orange | `#F2A33A` | The one accent: status dot, "Mata ne.", artwork |
| Slab | `#2E2E32` | Dark slanted bars |
| Gray | `#5B5E66` | Small labels (6.5:1 on paper) |

Fonts: Archivo Black for the wordmark and headings, Inter Display for everything else, Noto Sans CJK JP for Japanese.
