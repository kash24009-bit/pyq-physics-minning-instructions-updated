#!/usr/bin/env python3
"""Worksheet for one S2a unit (a year's printed constants, PHY-08 Y§3). Edition 2026-10-26 (B08).
Locating only: lists every question paper of the year with its file, its English instructions
pages and the text-layer lines that look like constants (papers without a text layer: none), the
template rows and the standard values for the script check. No value may be copied from it.
  python3 phy_s2a_prep.py --year 2023 --template 2024-5511 --out /home/claude/render/S2A-2023/PREP.md
"""
import argparse, os, re, subprocess, sys
sys.path.insert(0, '/home/claude'); import pyqkit as K
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location('s4', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'phy_s4_prep.py'))
S4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(S4)
V = '/home/claude/vault'
STD = {'c': '2.998e8 m/s', 'h': '6.626e-34 J s', 'e': '1.602e-19 C', 'mu0': '4*pi*1e-7 T m/A', 'eps0': '8.854e-12 C^2 N^-1 m^-2',
       '1/(4*pi*eps0)': '8.988e9 N m^2 C^-2', 'm_e': '9.109e-31 kg', 'm_n': '1.675e-27 kg', 'm_p': '1.673e-27 kg',
       'N_A': '6.022e23 per mol', 'k_B': '1.381e-23 J/K', 'R_nucleus': '~1e-15 m'}
ap = argparse.ArgumentParser(); ap.add_argument('--year', required=True); ap.add_argument('--template', required=True)
ap.add_argument('--out', required=True); a = ap.parse_args()
F = [f for f in K.table(V, 'l1/FILES.csv') if f['year'] == a.year and f['kind'] in ('QP', 'SQP')]
L = [f'# S2a worksheet {a.year} · {len(F)} question papers · locating only: every value from a 300 dpi crop', '',
     f'CONSTANTS header: `{open(f"{V}/l1/CONSTANTS.csv").readline().strip()}`', '',
     f'## Template rows ({a.template})'] + [f'- `{",".join(r.values())}`' for r in K.table(V, 'l1/CONSTANTS.csv') if r['paper_id'] == a.template]
L += ['', '## Standard values for the script check (a difference is a misread, re-read at 400 dpi, or a printed value kept with a note)']
L += [f'- {k} = {v}' for k, v in STD.items()]
L += ['', '## Papers (English instruction pages among pp 1-5; constant-like lines from the text layer, to locate only)']
for f in sorted(F, key=lambda x: x['paper_id']):
    pdf = S4.resolve_pdf(f['file_id'])
    if not pdf:
        L.append(f"- {f['paper_id']} {f['file_id']} {f['name']}: FILE NOT FOUND"); continue
    kinds = S4.classify_pages(pdf)
    first = {p: k for p, k in kinds.items() if p <= 5}
    hits = []
    for p in range(1, 6):
        t = subprocess.run(['pdftotext', '-layout', '-f', str(p), '-l', str(p), pdf, '-'], capture_output=True, text=True).stdout
        for ln in t.splitlines():
            if re.search(r'(c\s*=\s*3|h\s*=\s*6|e\s*=\s*1\.6|1\.6\s*[x×]|Avogadro|Boltzmann|constant|mass of (electron|neutron|proton)|=\s*9\s*[x×]\s*10)', ln, re.I):
                hits.append(f'p{p}: ' + re.sub(r'\s{2,}', ' ', ln.strip())[:110])
    L.append(f"- **{f['paper_id']}** {f['file_id']} {f['name']} ({f['pages']} pp): pages 1-5 {first}")
    L += [f'  - {h}' for h in hits[:16]] or ['  - no text layer: read the instructions pages from the images']
open(a.out, 'w').write('\n'.join(L) + '\n')
print(a.out, len(F), 'papers')
