#!/usr/bin/env python3
"""Render pages once at 180 dpi (no --crop) and cut each into a top band (0-52 %) and a
bottom band (48-100 %), so every band stays inside the image viewer's limit at full
resolution (her decision 2026-10-19b, rule card B3). Prints only the band list.
  python3 phy_bands.py --fid FL-xxxx --pages 3-16 --out /home/claude/render/<unit>/bands [--dpi 180]
"""
import argparse, os, subprocess, sys, tempfile
from PIL import Image
ap = argparse.ArgumentParser()
ap.add_argument('--fid', required=True); ap.add_argument('--pages', required=True)
ap.add_argument('--out', required=True); ap.add_argument('--dpi', type=int, default=180)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
tmp = tempfile.mkdtemp(prefix='bands_', dir=a.out)
r = subprocess.run([sys.executable, '/home/claude/pyqkit.py', 'render', '--vault', '/home/claude/vault', a.fid, a.pages,
                    '--dpi', str(a.dpi), '--out', tmp], capture_output=True, text=True)
if r.returncode:
    print(r.stdout[-800:], r.stderr[-800:]); sys.exit(1)
out = []
for f in sorted(os.listdir(tmp), key=lambda s: int(''.join(c for c in s if c.isdigit()) or 0)):
    if not f.endswith('.png'):
        continue
    im = Image.open(os.path.join(tmp, f)); w, h = im.size; stem = f[:-4]
    for tag, (y0, y1) in (('top', (0, 0.52)), ('bot', (0.48, 1.0))):
        b = im.crop((0, int(h * y0), w, int(h * y1)))
        path = os.path.join(a.out, f'{stem}-{tag}.png'); b.save(path); out.append((path, b.size))
    os.remove(os.path.join(tmp, f))
os.rmdir(tmp)
big = [p for p, s in out if max(s) > 1568]
print(f'{len(out)} bands at {a.dpi} dpi in {a.out} (band {out[0][1][0]}x{out[0][1][1]} px)' + (f'; WARNING over the viewer limit: {len(big)}' if big else ''))
print(' '.join(os.path.basename(p) for p, _ in out))
