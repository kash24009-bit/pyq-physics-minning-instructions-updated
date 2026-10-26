#!/usr/bin/env python3
"""Pack several crop PNGs onto as few sheets as possible, never rescaling a crop.

The image viewer shrinks any image whose long side exceeds about 1568 px, so a
crop wider than that loses the detail its dpi promised. This tool keeps every
sheet within the limit and prints, for each crop, the effective dpi it will be
seen at. Usage:
  python3 phy_tile.py --out /home/claude/render/<pid>/sheets/s --dpi 400 a.png b.png ...
Writes s_1.png, s_2.png, ... Each crop gets a label strip with its folder name.
"""
import argparse, os, sys
from PIL import Image, ImageDraw

LIMIT = 1568
GAP = 8
LABEL = 18

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, help='sheet path prefix')
    ap.add_argument('--dpi', type=float, default=0, help='render dpi of the crops (for the effective-dpi report)')
    ap.add_argument('--limit', type=int, default=LIMIT)
    ap.add_argument('crops', nargs='+')
    a = ap.parse_args()
    items = []
    for p in a.crops:
        im = Image.open(p).convert('L')
        name = os.path.basename(os.path.dirname(p)) + '/' + os.path.basename(p)
        items.append((name, im))
    sheets, cur, x, y, row_h, sheet_w = [], [], 0, 0, 0, 0
    def flush():
        nonlocal cur, x, y, row_h, sheet_w
        if cur:
            sheets.append(cur)
        cur, x, y, row_h, sheet_w = [], 0, 0, 0, 0
    for name, im in items:
        w, h = im.size[0], im.size[1] + LABEL
        if w > a.limit or h > a.limit:
            flush(); sheets.append([(name, im, 0, 0)]); continue
        if x + w > a.limit:          # new shelf
            x, y = 0, y + row_h + GAP
            row_h = 0
        if y + h > a.limit:          # new sheet
            flush()
        cur.append((name, im, x, y))
        x += w + GAP; row_h = max(row_h, h); sheet_w = max(sheet_w, x)
    flush()
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    for i, sh in enumerate(sheets, 1):
        W = max(px + im.size[0] for _, im, px, _ in sh)
        H = max(py + im.size[1] + LABEL for _, im, _, py in sh)
        canvas = Image.new('L', (W, H), 255)
        d = ImageDraw.Draw(canvas)
        for name, im, px, py in sh:
            d.text((px + 2, py + 2), name, fill=0)
            canvas.paste(im, (px, py + LABEL))
        path = f'{a.out}_{i}.png'
        canvas.save(path)
        long_side = max(W, H)
        shrink = min(1.0, a.limit / long_side)
        eff = f' effective {a.dpi*shrink:.0f} dpi' if a.dpi else ''
        print(f'{path}: {W}x{H} px, {len(sh)} crop(s){eff}' + ('' if shrink == 1 else '  WARNING: larger than the viewer limit; crop tighter'))
        for name, _, _, _ in sh:
            print('   ', name)

if __name__ == '__main__':
    main()
