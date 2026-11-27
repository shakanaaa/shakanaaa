# Panel generator

Every panel in `assets/` is generated here, with text converted to outlines so the fonts look the same on any device.

```bash
cd tools
npm install
pip install fonttools
python3 build.py ../assets
```

- Colors and layout live in `lib.py` (palette constants) and `build.py` (one function per panel, each with a desktop and a mobile version).
- Latin text uses Archivo. Japanese text needs Noto Sans CJK Bold at `/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc`; change the path in `lib.py` if yours differs.

## Hero artwork

`build.py` embeds `tools/art/wallhaven-ml2j69.jpg` in the hero in its original colors, cut into three arches. To use another picture, replace that file or change `ART` and the crop `box` values in `hero()`. The hero needs Pillow (`pip install pillow`) in addition to fontTools.
