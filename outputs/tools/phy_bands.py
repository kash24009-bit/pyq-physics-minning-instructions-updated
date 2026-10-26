#!/usr/bin/env python3
"""Render pages once (no --crop) and cut each into a top band (0-52 %) and a bottom band
(48-100 %), so every band stays inside the card's limits at full resolution (rule card A9, B3).
Prints the band list with each file's size; warns above 1568 px or 450 KB and splits any band
over 450 KB in two (with a 4 % overlap), so nothing larger is ever sent.
  python3 phy_bands.py --fid FL-xxxx --pages 3-16 --out /home/claude/render/<unit>/bands [--dpi 180] [--gray] [--scan PDF]
--gray  saves 8-bit grayscale PNG (scans and photos, unless colour carries meaning in a figure).
--scan  PDF path: caps the dpi at the scan's own resolution (pdfimages -list, images covering
        at least half the page) and implies --gray.
Edition 2026-10-26 (B08): file sizes, the 450 KB split, --gray and --scan (her decision 2026-10-21).
"""
import argparse, os, re, subprocess, sys, tempfile
from PIL import Image
LIMIT_PX, LIMIT_KB = 1568, 450
ap = argparse.ArgumentParser()
ap.add_argument('--fid', required=True); ap.add_argument('--pages', required=True)
ap.add_argument('--out', required=True); ap.add_argument('--dpi', type=int, default=180)
ap.add_argument('--gray', action='store_true'); ap.add_argument('--scan', default='')
a = ap.parse_args()

def page_list(spec):
    out = []
    for part in spec.split(','):
        if '-' in part:
            x, y = part.split('-'); out += list(range(int(x), int(y) + 1))
        elif part:
            out.append(int(part))
    return out

dpi = a.dpi
if a.scan:
    a.gray = True
    pages = set(page_list(a.pages))
    info = subprocess.run(['pdfinfo', '-f', '1', '-l', '1', a.scan], capture_output=True, text=True).stdout
    m = re.search(r'Page.*size:\s+([\d.]+) x ([\d.]+)', info)
    pw, ph = (float(m.group(1)) / 72, float(m.group(2)) / 72) if m else (8.27, 11.69)
    ppis = []
    for line in subprocess.run(['pdfimages', '-list', a.scan], capture_output=True, text=True).stdout.splitlines()[2:]:
        f = line.split()
        try:
            pg, w, h, xp, yp = int(f[0]), int(f[3]), int(f[4]), float(f[12]), float(f[13])
        except (ValueError, IndexError):
            continue
        if pg in pages and xp > 0 and yp > 0 and (w / xp) * (h / yp) >= 0.5 * pw * ph:
            ppis.append(min(xp, yp))
    if ppis and min(ppis) < dpi:
        dpi = int(min(ppis))
        print(f'scan resolution {min(ppis):.0f} ppi: rendering at {dpi} dpi')
    elif not ppis:
        print('no full-page raster image on these pages (vector page): dpi kept')

os.makedirs(a.out, exist_ok=True)
tmp = tempfile.mkdtemp(prefix='bands_', dir=a.out)
r = subprocess.run([sys.executable, '/home/claude/pyqkit.py', 'render', '--vault', '/home/claude/vault', a.fid, a.pages,
                    '--dpi', str(dpi), '--out', tmp], capture_output=True, text=True)
if r.returncode:
    print(r.stdout[-800:], r.stderr[-800:]); sys.exit(1)

def save(im, path):
    if a.gray:
        im = im.convert('L')
    im.save(path, optimize=True)
    return os.path.getsize(path) / 1024

out, split = [], 0
for f in sorted(os.listdir(tmp), key=lambda s: int(''.join(c for c in s if c.isdigit()) or 0)):
    if not f.endswith('.png'):
        continue
    im = Image.open(os.path.join(tmp, f)); w, h = im.size; stem = f[:-4]
    for tag, (y0, y1) in (('top', (0, 0.52)), ('bot', (0.48, 1.0))):
        b = im.crop((0, int(h * y0), w, int(h * y1)))
        path = os.path.join(a.out, f'{stem}-{tag}.png'); kb = save(b, path)
        if kb > LIMIT_KB:           # split, never send a band over 450 KB
            os.remove(path); split += 1
            bh = b.size[1]
            for t2, (z0, z1) in (('1', (0, 0.52)), ('2', (0.48, 1.0))):
                p2 = os.path.join(a.out, f'{stem}-{tag}{t2}.png')
                kb2 = save(b.crop((0, int(bh * z0), w, int(bh * z1))), p2)
                out.append((p2, Image.open(p2).size, kb2))
        else:
            out.append((path, b.size, kb))
    os.remove(os.path.join(tmp, f))
os.rmdir(tmp)
big = [p for p, s, kb in out if max(s) > LIMIT_PX]
heavy = [p for p, s, kb in out if kb > LIMIT_KB]
kbs = [kb for _, _, kb in out]
print(f'{len(out)} bands at {dpi} dpi{" grayscale" if a.gray else ""} in {a.out} (band {out[0][1][0]}x{out[0][1][1]} px; '
      f'{sum(kbs):.0f} KB in all, mean {sum(kbs)/len(kbs):.0f} KB, largest {max(kbs):.0f} KB)'
      + (f'; {split} band(s) over {LIMIT_KB} KB split in two' if split else '')
      + (f'; WARNING over {LIMIT_PX} px: {len(big)}' if big else '')
      + (f'; WARNING still over {LIMIT_KB} KB: {len(heavy)}' if heavy else ''))
print(' '.join(f'{os.path.basename(p)}({kb:.0f}K)' for p, _, kb in out))
