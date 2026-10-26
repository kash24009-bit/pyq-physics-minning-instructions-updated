#!/usr/bin/env python3
"""Worksheet for one S3 paper unit (with its S2a constants): page table, table headers and
real rows of a template paper as format guides. Locating only; no value may be copied from it.
  python3 phy_s3_prep.py --pid SQP2324-042 --fid FL-2a095ebb9d --template SQP2627-042 --out PREP.md
"""
import argparse, csv, io, subprocess, sys
sys.path.insert(0, '/home/claude'); import pyqkit as K
V = '/home/claude/vault'
ap = argparse.ArgumentParser(); ap.add_argument('--pid', required=True); ap.add_argument('--fid', required=True)
ap.add_argument('--template', required=True); ap.add_argument('--out', required=True); a = ap.parse_args()
def row(x):
    b = io.StringIO(); csv.DictWriter(b, fieldnames=list(x.keys())).writerow(x); return b.getvalue().strip()
L = [f'# S2a + S3 worksheet {a.pid} · file {a.fid} · template rows from {a.template}', '',
     'Format guides only: every value you write comes from this paper\'s page images.', '']
pt = subprocess.run([sys.executable, '/home/claude/pyqkit.py', 'pages', '--vault', V, a.fid], capture_output=True, text=True).stdout
L += ['## Page table', '```', pt.strip()[:3000], '```', '']
I = K.table(V, 'l1/INSTANCES.csv'); T = [r for r in I if r['paper_id'] == a.template]
L += ['## Headers']
for t in ('INSTANCES', 'FIGURES', 'FORMULAE', 'CASES', 'BLUEPRINTS', 'CONSTANTS', 'UNREADABLE'):
    L.append(f'- {t}: `{open(f"{V}/l1/{t}.csv").readline().strip()}`')
L += ['', '## Template INSTANCES rows (one of each kind)']
picks, seen = [], set()
def pick(cond, tag):
    for r in T:
        if cond(r) and r['instance_id'] not in seen:
            seen.add(r['instance_id']); L.append(f'- {tag}: `{row(r)[:900]}`'); return r
pick(lambda r: r['q_type'] == 'MCQ' and not r['case_id'], 'MCQ')
pick(lambda r: 'ARSET' in r['extra'], 'first AR row (ARSET)')
pick(lambda r: r['q_type'] == 'NUM' and r['part'], 'NUM part')
pick(lambda r: r['q_type'] == 'DRV', 'DRV')
pick(lambda r: r['choice_pair_id'] and r['side'] == 'A', 'OR side A')
pick(lambda r: r['vi_alt'] == 'y', 'VI alternative')
pick(lambda r: r['case_id'], 'case sub-part')
pick(lambda r: r['has_figure'] == 'y', 'row with a figure')
for t, n in (('FIGURES', 2), ('CASES', 1), ('BLUEPRINTS', 1)):
    rows = [r for r in K.table(V, f'l1/{t}.csv') if r.get('paper_id', r.get('figure_id', '')).find(a.template) >= 0 or a.template in r.get('figure_id', '')]
    L += ['', f'## Template {t}'] + [f'- `{row(r)[:700]}`' for r in rows[:n]]
F = [r for r in K.table(V, 'l1/FORMULAE.csv') if r['formula_id'].startswith(f'EQ-{a.template}-')]
L += ['', '## Template FORMULAE'] + [f'- `{row(r)[:400]}`' for r in [x for x in F if x['role'] == 'given'][:1] + [x for x in F if x['role'] == 'asked'][:2]]
C = [r for r in K.table(V, 'l1/CONSTANTS.csv') if r['paper_id'] == a.template]
L += ['', f'## Template CONSTANTS ({len(C)} rows of {a.template})'] + [f'- `{row(r)}`' for r in C]
open(a.out, 'w').write('\n'.join(L) + '\n'); print(a.out, len(L), 'lines')
