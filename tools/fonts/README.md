# Fonts used by the panel generator

All glyphs are converted to outlines in the SVGs, so visitors do not need these fonts.
The files here are subsets so `build.py` runs offline, with no `npm install`.

| File | Role | License |
| --- | --- | --- |
| `ArchivoBlack-latin.ttf` | Wordmark and display headings | SIL OFL 1.1 (see `OFL-ArchivoBlack.txt`) |
| `InterDisplay-*-latin.otf` | Body, labels, names | SIL OFL 1.1, The Inter Project Authors |
| `NotoSansCJKjp-Bold-subset.otf` | Japanese text (only the characters in `build.py`) | SIL OFL 1.1, Adobe / Google |

If you add new Japanese text to `build.py`, regenerate the Noto subset (see `tools/README.md`).
