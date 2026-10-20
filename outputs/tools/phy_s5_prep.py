#!/usr/bin/env python3
"""Worksheet for one S5 scheme unit: which rows need lines, where their answers sit,
and which shuffled questions the scheme may print differently from the origin's scheme.

Everything here comes from the vault tables and the scheme's TEXT LAYER, so it only
locates and flags. No value in it may be copied into a row: every value is read from
a page image crop (CLAUDE.md §4 rule 2, §8).

  python3 phy_s5_prep.py --pid 2024-5512 --scheme FL-f9e28e6de8 --pages 25-46 \
      [--origin-scheme FL-f9e28e6de8 --origin-pages 1-24] --out /home/claude/render/2024-5512/PREP.md
"""
import argparse, collections, re, subprocess, sys
sys.path.insert(0, '/home/claude')
import pyqkit as K

V = '/home/claude/vault'

def page_text(fid, p):
    r = subprocess.run([sys.executable, '/home/claude/pyqkit.py', 'pages', '--vault', V, fid, '--text', str(p)],
                       capture_output=True, text=True)
    return r.stdout

def answers(fid, first, last):
    """Split the section's text layer into answers by question number (1, 2, 3 ... in order)."""
    out, cur, want = {}, None, 1
    start = re.compile(r'^\s{0,10}(\d{1,2})\s*(?:\.(?!\d)|$|\s{2,}|\()')   # '17.', '17' alone, '17   text', '17 (a)'
    begun = False                     # answers start after the first answer-page header
    for p in range(first, last + 1):
        for line in page_text(fid, p).splitlines():
            if not begun:
                begun = bool(re.search(r'VALUE\s*POINT|MARKING\s+SCHEME\s*:', line, re.I))
                continue
            m = start.match(line)
            if m and int(m.group(1)) == want:
                cur = want; want += 1
                out[cur] = {'pages': [p], 'text': ''}
            if cur is not None:
                if p not in out[cur]['pages']:
                    out[cur]['pages'].append(p)
                out[cur]['text'] += line + '\n'
    return out

def nums(t, q=None):
    keep = []
    for i, line in enumerate(t.splitlines()):
        if re.search(r'Page\s+\d+\s+of|\b55\s*/|CODE\s*:|MARKING SCHEME|VALUE POINT', line, re.I):
            continue                      # footers and headers
        if i == 0:
            line = re.sub(r'^\s*\d{1,2}\s*\.?', '', line)   # the question number itself, with or without its dot
        keep.append(line)
    return collections.Counter(re.findall(r'\d', '\n'.join(keep)))   # digits, so spacing differences in the text layer do not flag

def keys(t):
    return ''.join(re.findall(r'\(\s*([A-D])\s*\)', t))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pid', required=True); ap.add_argument('--scheme', required=True)
    ap.add_argument('--pages', required=True); ap.add_argument('--origin-scheme')
    ap.add_argument('--origin-pages'); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    f, l = map(int, a.pages.split('-'))
    I = K.table(V, 'l1/INSTANCES.csv'); S = K.table(V, 'l1/STEP-AWARDS.csv')
    F = K.table(V, 'l1/FORMULAE.csv'); E = K.table(V, 'l1/ERRATA.csv'); FG = K.table(V, 'l1/FIGURES.csv')
    rows = [r for r in I if r['paper_id'] == a.pid]
    byid = {r['instance_id']: r for r in I}
    ans = answers(a.scheme, f, l)
    oans = {}
    if a.origin_scheme and a.origin_pages:
        of, ol = map(int, a.origin_pages.split('-'))
        oans = answers(a.origin_scheme, of, ol)
    L = [f'# S5 worksheet {a.pid} · scheme {a.scheme} pp {a.pages}', '',
         'Text-layer locator only: every value you write comes from a page image crop.', '']
    eq = [int(x['formula_id'].rsplit('-', 1)[1]) for x in F if x['formula_id'].startswith(f'EQ-{a.pid}-')]
    L.append(f'- next FORMULAE id: EQ-{a.pid}-{(max(eq) + 1 if eq else 1):03d}')
    import json as _j
    b = _j.load(open(V + '/STATE.json')).get('batch', '')
    ern = [int(x['errata_id'].rsplit('-', 1)[1]) for x in E if x['errata_id'].startswith(f'ER-B{int(b):02d}-')]
    L.append(f'- next ERRATA id (only if this unit sets a file status): ER-B{int(b):02d}-{(max(ern) + 1 if ern else 1):03d}')
    L.append(f'- question numbers located in the text layer: {len(ans)} of {max([int(r["q_no"]) for r in rows] or [0])}')
    L += ['', '## Rows that need scoring lines (rel = origin)', '',
          '| instance_id | q_type | marks_part | q_marks | scheme pages | stem (start) |', '|---|---|---|---|---|---|']
    for r in rows:
        if r['rel'] != 'origin':
            continue
        q = int(r['q_no']); pg = ','.join(map(str, ans.get(q, {}).get('pages', ['?'])))
        L.append(f"| {r['instance_id']} | {r['q_type']} | {r['marks_part']} | {r['q_marks_printed']} | {pg} | {r['stem'][:90]} |")
        if r['q_type'] in ('MCQ', 'AR') and r['options']:
            L.append(f"|  | options |  |  |  | {r['options'][:150]} |")
    L += ['', '## The rows that need lines, in full (from the vault; the paper side is already saved)', '']
    for r in rows:
        if r['rel'] != 'origin':
            continue
        L.append(f"- **{r['instance_id']}** · {r['q_type']} · marks_part {r['marks_part'] or '-'} · q_marks {r['q_marks_printed']} · p{r['source_page']}")
        L.append(f"  stem: {r['stem']}")
        if r['givens'] or r['unknown']:
            L.append(f"  givens: {r['givens']} · unknown: {r['unknown']}")
        if r['options']:
            L.append(f"  options: {r['options']}")
        for fg in [x for x in FG if x['instance_id'] == r['instance_id']]:
            L.append(f"  figure {fg['figure_id']} (paper p{fg['source_page']}): {fg['description'][:400]} · values: {fg['values'][:120]}")
        m = re.search(r'resembles (\S+?)[:;, ]', r['note'] or '')
        if m and m.group(1) in byid:
            tl = [x for x in S if x['instance_id'] == m.group(1)]
            for x in tl[:6]:
                L.append(f"  lines of {m.group(1)} (the row it resembles; a format guide, never a value source): {x['step_text'][:140]} | {x['marks']} | {x['step_kind']} | alt: {x['alt_accepted'][:60]}")
    hdr_s = open(V + '/l1/STEP-AWARDS.csv').readline().strip(); hdr_f = open(V + '/l1/FORMULAE.csv').readline().strip()
    L += ['', '## Formats (headers and real rows of this year; match them field for field)', '',
          f'- STEP-AWARDS header: `{hdr_s}`', f'- FORMULAE header: `{hdr_f}`']
    yr = rows[0]['year'] if rows else ''
    same_year = [x for x in S if x['paper_id'].startswith(yr)]
    picks = []
    for want in ('key', 'formula', 'substitution', 'result', 'diagram', 'reason'):
        for x in same_year:
            if x['step_kind'] == want and x not in picks:
                picks.append(x); break
    for x in same_year:
        if 'in one cell' in x['step_text'] and x not in picks:
            picks.append(x); break
    for x in same_year:
        if 'any two' in (x['step_text'] + x['alt_accepted']).lower() and x not in picks:
            picks.append(x); break
    for x in same_year:
        if x['alt_accepted'].startswith('Alternatively') and x not in picks:
            picks.append(x); break
    import csv as _csv, io as _io
    for x in picks:
        b = _io.StringIO(); w = _csv.DictWriter(b, fieldnames=list(x.keys())); w.writerow(x)
        L.append(f'- `{b.getvalue().strip()[:400]}`')
    fr = [x for x in F if x['role'] == 'result' and x['source'] == 'MS' and x['formula_id'].startswith(f'EQ-{yr}')][:2]
    for x in fr:
        b = _io.StringIO(); w = _csv.DictWriter(b, fieldnames=list(x.keys())); w.writerow(x)
        L.append(f'- `{b.getvalue().strip()}`')
    L += ['', '## Shuffled questions: this scheme against the origin scheme (text layer; check every flag on the image)', '',
          '| q_no | origin rows | origin key line(s) | this scheme key (text) | numbers only here | numbers only in origin | pages |',
          '|---|---|---|---|---|---|---|']
    seen = set()
    for r in rows:
        if r['rel'] != 'shuffle':
            continue
        q = int(r['q_no'])
        if q in seen:
            continue
        seen.add(q)
        o = byid.get(r['rel_to'], {})
        oq = int(o['q_no']) if o else None
        orows = sorted({x['rel_to'] for x in rows if int(x['q_no']) == q and x['rel'] == 'shuffle'})
        okeys = [s['step_text'] for s in S if s['instance_id'] in orows and s['step_kind'] == 'key']
        t = ans.get(q, {}).get('text', ''); ot = oans.get(oq, {}).get('text', '') if oq else ''
        k = keys(t) if any(x['q_type'] in ('MCQ', 'AR') for x in rows if int(x['q_no']) == q) else ''
        if ot:
            n1, n2 = nums(t), nums(ot)
            only_here = ' '.join(sorted((n1 - n2).elements()))[:60]; only_o = ' '.join(sorted((n2 - n1).elements()))[:60]
        else:
            only_here = only_o = '(origin text not given)'
        flag = ''
        if okeys and k and ''.join(x.strip('() ')[:1] for x in okeys) != k[:len(okeys)]:
            flag = ' **KEYS DIFFER?**'
        L.append(f"| {q}{flag} | {', '.join(orows)} (origin Q{oq}) | {' '.join(okeys)} | {k} | {only_here} | {only_o} | {','.join(map(str, ans.get(q, {}).get('pages', ['?'])))} |")
    L += ['', 'Numbers differing in the text layer are often layout noise (marks, page numbers, question numbers); '
          'look at the page image of every flagged question and report real differences only.']
    if oans:
        import difflib
        def words(fid, a0, a1):
            t = ''
            for pg in range(a0, a1 + 1):
                t += page_text(fid, pg)
                if re.search(r'MARKING SCHEME\s*:\s*PHYSICS', t):
                    break
            t = t.split('MARKING SCHEME')[0] if 'MARKING SCHEME :' in t or 'MARKING SCHEME:' in t else t
            return re.findall(r'\S+', t)
        w1 = words(a.scheme, f, min(f + 2, l)); w0 = words(a.origin_scheme, of, min(of + 2, ol))
        diff = [d for d in difflib.ndiff(w0, w1) if d[:1] in '+-']
        L += ['', '## Examiner instructions of this section against the origin section (text layer, words)', '',
              f'- origin words {len(w0)}, this section {len(w1)}; differing words: {len(diff)}',
              '- ' + ' '.join(diff[:80])]
    open(a.out, 'w').write('\n'.join(L) + '\n')
    print(a.out)

if __name__ == '__main__':
    main()
