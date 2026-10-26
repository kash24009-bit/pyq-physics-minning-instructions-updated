#!/usr/bin/env python3
"""Pack several crop PNGs onto as few sheets as possible, never rescaling a crop.

Every sheet stays within 1568 px on its long side and under 450 KB (rule card A9): a sheet
over 450 KB is split into smaller sheets; a single crop over either limit is kept alone with
a warning to crop tighter. Prints, for each sheet, its size in px and KB and the effective dpi
its crops will be seen at. Sheets are 8-bit grayscale unless --color (colour carries meaning).
  python3 phy_tile.py --out /home/claude/render/<pid>/sheets/s --dpi 400 [--color] a.png b.png ...
Writes s_1.png, s_2.png, ... Each crop gets a label strip with its folder name.
Edition 2026-10-26 (B08): file sizes, the 450 KB split, --color (her decision 2026-10-21).
"""
import argparse, os
from PIL import Image, ImageDraw

LIMIT = 1568
LIMIT_KB = 450
GAP = 8
LABEL = 18

def pack(items, limit):
    sheets, cur, x, y, row_h = [], [], 0, 0, 0
    for name, im in items:
        w, h = im.size[0], im.size[1] + LABEL
        if w > limit or h > limit:
            if cur:
                sheets.append(cur)
            sheets.append([(name, im, 0, 0)]); cur, x, y, row_h = [], 0, 0, 0; continue
        if x + w > limit:            # new shelf
            x, y, row_h = 0, y + row_h + GAP, 0
        if y + h > limit:            # new sheet
            sheets.append(cur); cur, x, y, row_h = [], 0, 0, 0
        cur.append((name, im, x, y))
        x += w + GAP; row_h = max(row_h, h)
    if cur:
        sheets.append(cur)
    return sheets

def draw(sh, mode):
    W = max(px + im.size[0] for _, im, px, _ in sh)
    H = max(py + im.size[1] + LABEL for _, im, _, py in sh)
    canvas = Image.new(mode, (W, H), 255 if mode == 'L' else (255, 255, 255))
    d = ImageDraw.Draw(canvas)
    for name, im, px, py in sh:
        d.text((px + 2, py + 2), name, fill=0 if mode == 'L' else (0, 0, 0))
        canvas.paste(im, (px, py + LABEL))
    return canvas

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, help='sheet path prefix')
    ap.add_argument('--dpi', type=float, default=0, help='render dpi of the crops (for the effective-dpi report)')
    ap.add_argument('--limit', type=int, default=LIMIT)
    ap.add_argument('--color', action='store_true', help='keep colour (only where colour carries meaning)')
    ap.add_argument('crops', nargs='+')
    a = ap.parse_args()
    mode = 'RGB' if a.color else 'L'
    items = []
    for p in a.crops:
        im = Image.open(p).convert(mode)
        items.append((os.path.basename(os.path.dirname(p)) + '/' + os.path.basename(p), im))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    queue, done, tmp = [pack(items, a.limit)], [], a.out + '_tmp.png'
    # split any sheet over 450 KB into two halves (by crop order) until each fits
    pending = list(queue[0])
    while pending:
        sh = pending.pop(0)
        draw(sh, mode).save(tmp, optimize=True)
        kb = os.path.getsize(tmp) / 1024
        if kb > LIMIT_KB and len(sh) > 1:
            half = len(sh) // 2
            pending[0:0] = pack([(n, im) for n, im, _, _ in sh[:half]], a.limit) + pack([(n, im) for n, im, _, _ in sh[half:]], a.limit)
            continue
        done.append(sh)
    if os.path.exists(tmp):
        os.remove(tmp)
    for i, sh in enumerate(done, 1):
        canvas = draw(sh, mode)
        path = f'{a.out}_{i}.png'
        canvas.save(path, optimize=True)
        W, H = canvas.size
        kb = os.path.getsize(path) / 1024
        shrink = min(1.0, a.limit / max(W, H))
        eff = f' effective {a.dpi*shrink:.0f} dpi' if a.dpi else ''
        warn = ''
        if shrink < 1:
            warn += '  WARNING: larger than 1568 px; crop tighter'
        if kb > LIMIT_KB:
            warn += f'  WARNING: over {LIMIT_KB} KB; crop tighter'
        print(f'{path}: {W}x{H} px, {kb:.0f} KB, {len(sh)} crop(s){eff}{warn}')
        for name, _, _, _ in sh:
            print('   ', name)

if __name__ == '__main__':
    main()
