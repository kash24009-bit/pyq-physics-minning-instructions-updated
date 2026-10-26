#!/usr/bin/env python3
"""Sibling worksheet for one S4 paper unit (her decision 2026-10-21; PHY-07 R§5, card D15).
The S4 extension of phy_s3_prep.py. Edition 2026-10-26 (B08). It locates and compares only:
no value it prints may be copied into a row except through --write-repeats, after the reader
has confirmed the repeat on its band.

Prepare:
  python3 phy_s4_prep.py --pid 2023-5512 [--fid FL-x] [--pdf PATH] --series 55/1 [--compare 55/2,55/3]
                         [--exclude PID,...] --out /home/claude/render/<unit>/PREP.md
  Aligns each sibling question with its series' origin questions (the questions of the series
  holding rel = origin rows) by text, then compares the sibling's text layer with the origin
  paper's own text layer token by token (every number, unit, sign, exponent, option and option
  order): any difference -> "variant, full row"; none -> "repeat candidate", never "repeat".
  A question matching no origin question -> "new question, full row". English pages are found
  by the share of common English words in each page's text layer; pages it cannot settle, and
  every page of a paper without a text layer, go on one sheet of small page thumbnails.
  Writes PREP.md and REPEATS.csv (one line per row to copy, status "candidate") beside it.

Confirm, then write the repeats (the reader, after checking every candidate on its band and
cropping every figure at 400 dpi; status "confirmed" or "variant" in REPEATS.csv):
  python3 phy_s4_prep.py --write-repeats --pid 2023-5512 --repeats /home/claude/render/<unit>/REPEATS.csv
  Writes the confirmed shuffle rows into V/work/<pid>__INSTANCES.csv (and their FIGURES,
  FORMULAE with source QP, and CASES) copied from the origin rows with this paper's ids, q_no,
  section, choice and case ids and pages; merges with the rows already there.

Add a repeat the text layer could not show (papers without a text layer), or single confirmed parts
of a question the worksheet called a variant (--only <origin row ids>):
  python3 phy_s4_prep.py --add-repeat --pid 2023-5522 --repeats .../REPEATS.csv --q 7 --origin-q 2023-5521:12 --page 5 [--only ID,ID]
"""
import argparse, csv, difflib, glob, hashlib, html, io, json, os, re, subprocess, sys, zipfile
sys.path.insert(0, '/home/claude'); import pyqkit as K
V = os.environ.get('PHY_VAULT', '/home/claude/vault')   # PHY_VAULT only for tests on a copy
PAGE_KEYS = ('figure_page', 'options_page', 'options_pages', 'ARSET_page')
COMMON = set('''the of a an and to in is are be by for with on at as from that this which what will its it if when
then than or not into their there has have was were been his her they can each two one find calculate show
state explain write obtain draw give why how where between same two three also these those such any both
current field charge value energy light wave lens figure shown given'''.split())
RCOLS = ['status', 'sib_id', 'origin_row', 'rel_to', 'q_no', 'side', 'part', 'section', 'choice_pair_id',
         'case_id', 'source_page', 'q_page', 'fig_pages', 'extra_pages', 'note_add']

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

# K.table applies ERRATA, so every table below is read with its corrections.
FILES = {f['file_id']: f for f in K.table(V, 'l1/FILES.csv')}

def resolve_pdf(fid):
    """The file on disk whose sha256 matches FILES (names clash between years)."""
    f = FILES[fid]; name, want = f['name'], f['sha256']
    cands = [os.path.join('/mnt/user-data/uploads', name), os.path.join('/mnt/project', name)]
    cands += glob.glob('/home/user/*/' + glob.escape(name)) + glob.glob('/home/user/*/*/' + glob.escape(name))
    for c in cands:
        if os.path.isfile(c) and sha(c) == want:
            return c
    if f['where'].startswith('zip:'):
        zname = f['where'][4:]
        for z in [os.path.join('/mnt/user-data/uploads', zname)] + glob.glob('/home/user/*/' + glob.escape(zname)):
            if os.path.isfile(z):
                with zipfile.ZipFile(z) as zf:
                    for m in zf.namelist():
                        if os.path.basename(m) == name:
                            out = f'/home/claude/render/_zipcache/{fid}.pdf'
                            os.makedirs(os.path.dirname(out), exist_ok=True)
                            open(out, 'wb').write(zf.read(m))
                            if sha(out) == want:
                                return out
    return None

def page_text(pdf, p):
    return subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), pdf, '-'], capture_output=True, text=True).stdout

def n_pages(pdf):
    m = re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout)
    return int(m.group(1)) if m else 0

JUNK = set('{}$¡©§±^~µ¢£¤¥¦«»ÊÎÕÿÁÀÝàåÚèéÉûüîïöôòñ®ŠŒ¿Ð')
def lang_stats(text):
    w = re.findall(r'[A-Za-z]{2,}', text); ch = [c for c in text if not c.isspace()]
    if len(w) < 15:
        return None, None
    return sum(1 for x in w if x.lower() in COMMON) / len(w), sum(1 for c in ch if c in JUNK) / max(1, len(ch))

def classify_pages(pdf):
    """page -> 'en' | 'hi' | 'unsettled' | 'notext'. Calibrated B08 on 2024 55/1/2 and 2023 55/1/1, 55/3/1:
    English pages 0.41-0.57 common words (2+ letters) with symbol share < 0.02; Hindi (legacy font) pages
    <= 0.09 with symbol share 0.15-0.25; bilingual covers 0.25 with 0.08 (unsettled)."""
    out = {}
    for p in range(1, n_pages(pdf) + 1):
        s, j = lang_stats(page_text(pdf, p))
        if s is None:
            out[p] = 'notext' if len(page_text(pdf, p).split()) < 15 else 'hi'
        elif s >= 0.2 and j < 0.03:
            out[p] = 'en'
        elif s < 0.15 and j >= 0.05:
            out[p] = 'hi'
        else:
            out[p] = 'unsettled'
    return out

def page_lines(pdf, p):
    """Lines of words from the word boxes, clustered by vertical position (shift-invariant, so a question
    typeset identically gives the same lines wherever it sits on the page). [(text, words, x0_first)]"""
    x = subprocess.run(['pdftotext', '-bbox', '-f', str(p), '-l', str(p), pdf, '-'], capture_output=True, text=True).stdout
    pw = re.search(r'<page width="([\d.]+)"', x); pw = float(pw.group(1)) if pw else 595.0
    ws = []
    for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', x):
        t = html.unescape(m.group(5))
        ws.append(((float(m.group(2)) + float(m.group(4))) / 2, float(m.group(1)), t))
    ws.sort()
    lines, cur, cy = [], [], None
    for y, x0, t in ws:
        if cur and y - cy > 2.5:
            lines.append(cur); cur = []
        if not cur:
            cy = y
        cur.append((x0, t))
    if cur:
        lines.append(cur)
    out = []
    for ln in lines:
        ln.sort()
        out.append((' '.join(t for _, t in ln), [t for _, t in ln], ln[0][0] / pw))
    return out

FOOT = re.compile(r'P\.?\s*T\.?\s*O|Page\s+\d+\s+of\s+\d+|\b\d{2}\s*/\s*[\w()&]+\s*/\s*\d\b|^\s*\d{1,2}-\d{2}/')
HEAD = re.compile(r'^\s*SECTION\s*[-–—]?\s*[A-E]\s*$', re.I)
BLOCK = re.compile(r'^(Directions?|Note\s*:|For Questions|Questions?\s+(number|no\.?|numbers)?\s*\d+\s*(to|and)\s*\d+|Question\s+numbers?)', re.I)
QSTART = re.compile(r'^(\d{1,2})\.$')

def segment(pdf, pages, kinds):
    """q_no -> dict(page = start page, lines = [(page, [words])])."""
    qs, cur, started, expect = {}, None, False, 1
    for p in pages:
        if kinds.get(p) != 'en':
            continue
        skipping = False
        for text, words_, x0 in page_lines(pdf, p):
            if not started:
                if re.search(r'SECTION\s*[-–—]?\s*A\b', text, re.I):
                    started = True
                continue
            if FOOT.search(text):
                continue
            if HEAD.match(text):
                skipping = True; continue
            m = QSTART.match(words_[0])
            k0 = 1
            if not m and len(words_) > 1 and re.fullmatch(r'\d{1,2}', words_[0]) and words_[1] == '.':
                m = re.match(r'(\d{1,2})', words_[0]); k0 = 2      # "23" and "." as two word boxes
            if m and int(m.group(1)) == expect and x0 < 0.2:
                cur = {'q': expect, 'page': p, 'lines': []}; qs[expect] = cur; expect += 1; skipping = False
                if len(words_) > k0:
                    cur['lines'].append((p, words_[k0:]))
                continue
            if BLOCK.match(text):
                skipping = True; continue
            if skipping or cur is None:
                continue
            cur['lines'].append((p, words_))
    return qs

TOK = re.compile(r'\d+(?:[·.]\d+)?|[A-Za-z]+|[^\sA-Za-z\d]')
def tokens(q):
    out = []
    for p, ws in q['lines']:
        for w in ws:
            for t in TOK.findall(w.replace('·', '.')):
                out.append((t, p))
    return out

def words(toks):
    return [t.lower() for t, _ in toks if t.isalpha() and len(t) > 1]

def diffs(a, b, n=6):
    sm = difflib.SequenceMatcher(None, [t for t, _ in a], [t for t, _ in b], autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != 'equal':
            out.append(f"{' '.join(t for t, _ in a[i1:i2]) or '-'} -> {' '.join(t for t, _ in b[j1:j2]) or '-'}")
    return out[:n], len(out)

MATH = set('+-−–=<>×÷/√^°%*')
def is_digit_tok(t):
    return any(c.isdigit() for c in t)

def option_bags(toks):
    """tokens after each printed option marker (A)-(D) or (a)-(d), as sorted lists per letter."""
    out, cur = {}, None
    for i, (t, _) in enumerate(toks):
        if t == '(' and i + 2 < len(toks) and toks[i + 2][0] == ')' and toks[i + 1][0] in ('A', 'B', 'C', 'D', 'a', 'b', 'c', 'd'):
            cur = toks[i + 1][0].upper(); out.setdefault(cur, []); continue
        if cur and t.isalpha() and t not in ('A', 'B', 'C', 'D', 'a', 'b', 'c', 'd'):
            out[cur].append(t)              # words only: numbers are compared in order over the whole question
    return {k: sorted(v) for k, v in out.items()}

def strip_stray(q, toks, known):
    """Drop number-only lines at the start or end of a question segment whose numbers are not in the
    origin rows (text-layer fragments); return (tokens, list of dropped numbers)."""
    lines = q['lines']; drop, keep_from, keep_to = [], 0, len(lines)
    while keep_to > keep_from and all(re.fullmatch(r'[\d.·]+', w) for w in lines[keep_to - 1][1]) and not any(w in known for w in lines[keep_to - 1][1]):
        drop += lines[keep_to - 1][1]; keep_to -= 1
    while keep_from < keep_to and all(re.fullmatch(r'[\d.·]+', w) for w in lines[keep_from][1]) and not any(w in known for w in lines[keep_from][1]):
        drop += lines[keep_from][1]; keep_from += 1
    return tokens({'lines': lines[keep_from:keep_to]}), drop

def compare(oq, sq, known, mcq=False):
    """(verdict, differences, looks). Differences make a variant; looks are text-layer gaps for the reader."""
    ot, od = strip_stray(oq, tokens(oq), known); st, sd = strip_stray(sq, tokens(sq), known)
    looks = [f"stray number line '{' '.join(x)}' in the {side} text layer (not in the origin rows)" for side, x in (('origin', od), ('sibling', sd)) if x]
    if [t for t, _ in ot] == [t for t, _ in st]:
        return 'repeat candidate', [], looks
    difs = []
    dn = lambda T: [t for t, _ in T if is_digit_tok(t)]
    if dn(ot) != dn(st):
        sm = difflib.SequenceMatcher(None, dn(ot), dn(st), autojunk=False)
        difs += [f"numbers {' '.join(dn(ot)[i1:i2]) or '-'} -> {' '.join(dn(st)[j1:j2]) or '-'}" for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal']
    ms = lambda T: [t for t, _ in T if t in MATH]
    if ms(ot) != ms(st):
        sm = difflib.SequenceMatcher(None, ms(ot), ms(st), autojunk=False)
        difs += [f"signs/symbols {' '.join(ms(ot)[i1:i2]) or '-'} -> {' '.join(ms(st)[j1:j2]) or '-'}" for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal']
    ob, sb = (option_bags(ot), option_bags(st)) if mcq else ({}, {})
    if ob != sb:
        difs += [f"option ({k}) {' '.join(ob.get(k, [])) or '-'} -> {' '.join(sb.get(k, [])) or '-'}" for k in sorted(set(ob) | set(sb)) if ob.get(k) != sb.get(k)]
    wd = lambda T: [t for t, _ in T if t.isalpha()]
    wo, ws_ = wd(ot), wd(st)
    if sorted(wo) == sorted(ws_):
        if wo != ws_:
            looks.append('the same words in another order (lines reflowed)')
    else:
        sm = difflib.SequenceMatcher(None, wo, ws_, autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == 'replace':
                difs.append(f"words {' '.join(wo[i1:i2])} -> {' '.join(ws_[j1:j2])}")
            elif op == 'delete':
                looks.append(f"words only in the origin text layer: '{' '.join(wo[i1:i2])}'")
            elif op == 'insert':
                looks.append(f"words only in this paper's text layer: '{' '.join(ws_[j1:j2])}'")
    if difs:
        return 'variant, full row', difs, looks
    looks.append('punctuation differs') if not looks else None
    return 'repeat candidate', [], looks

def index_map(ot, st):
    sm = difflib.SequenceMatcher(None, [t for t, _ in ot], [t for t, _ in st], autojunk=False)
    blocks = sm.get_matching_blocks()
    def f(i):
        best = None
        for a_, b_, n in blocks:
            if a_ <= i < a_ + n:
                return b_ + (i - a_)
            if a_ + n <= i:
                best = b_ + n - 1 if n else best
        return best
    return f

def page_for(ot, st, page, label=None, side_b=False):
    """The sibling page holding the origin's token that starts this row on `page`."""
    idx = [i for i, (_, p) in enumerate(ot) if p == page]
    if not idx:
        return None
    i = idx[0]
    if side_b:
        ors = [j for j, (t, p) in enumerate(ot) if t == 'OR' and p <= page]
        if ors:
            i = min(ors[-1] + 1, len(ot) - 1)      # the first token after OR: the alternative's own label
    elif label:
        for j in idx[:-2]:
            if ot[j][0] == '(' and ot[j + 1][0] == label and ot[j + 2][0] == ')':
                i = j; break
    j = index_map(ot, st)(i)
    return st[j][1] if j is not None and 0 <= j < len(st) else None

def sections(pid):
    for b in K.table(V, 'l1/BLUEPRINTS.csv'):
        if b['paper_id'] == pid:
            out = []
            for s in b['sections'].split(';'):
                name, rng, *_ = s.split(':'); lo, hi = rng.split('-'); out.append((name, int(lo), int(hi)))
            return out
    return []

def section_of(secs, q):
    for name, lo, hi in secs:
        if lo <= q <= hi:
            return name
    return ''

def csvrow(x):
    b = io.StringIO(); csv.DictWriter(b, fieldnames=list(x.keys())).writerow(x); return b.getvalue().strip()

def prepare(a):
    I = K.table(V, 'l1/INSTANCES.csv')
    sib = [f for f in FILES.values() if f['paper_id'] == a.pid and f['kind'] == 'QP']
    fid = a.fid or (sib[0]['file_id'] if sib else None)
    if not fid:
        sys.exit(f'no QP file for {a.pid} in FILES')
    pdf = a.pdf or resolve_pdf(fid)
    if not pdf or sha(pdf) != FILES[fid]['sha256']:
        sys.exit(f'cannot find the file of {fid} with its FILES sha256')
    excl = set([a.pid] + [x for x in a.exclude.split(',') if x])
    own = [s for s in a.series.split(',') if s]
    other = [s for s in a.compare.split(',') if s]
    def in_series(r, ss):
        code = r['paper_code']
        ser = re.search(r'series=([^;]+)', r['extra'])
        return any(code.startswith(s + '/') or code == s or (ser and ser.group(1) == s) for s in ss)
    year = FILES[fid]['year']
    rows = [r for r in I if r['paper_id'] not in excl and r['year'] == year and (in_series(r, own) or in_series(r, other))]
    groups = {}
    for r in rows:
        groups.setdefault((r['paper_id'], int(r['q_no'])), []).append(r)
    groups = {k: v for k, v in groups.items() if any(r['rel'] == 'origin' for r in v)}
    opids = sorted({k[0] for k in groups})
    ofid = {}
    for p in opids:
        f = [x for x in FILES.values() if x['paper_id'] == p and x['kind'] == 'QP']
        ofid[p] = f[0]['file_id'] if f else None
    # text layers
    kinds = classify_pages(pdf)
    s_q = segment(pdf, sorted(kinds), kinds)
    o_q, o_pdf = {}, {}
    for p in opids:
        if not ofid[p]:
            continue
        op = resolve_pdf(ofid[p]); o_pdf[p] = op
        if op:
            k2 = classify_pages(op); o_q[p] = segment(op, sorted(k2), k2)
    first_origin = opids[0] if opids else ''
    secs = sections(a.pid) or sections(first_origin)
    expect_n = 0
    for b in K.table(V, 'l1/BLUEPRINTS.csv'):
        if b['paper_id'] == first_origin:
            expect_n = int(b['n_questions'] or 0)
    outdir = os.path.dirname(os.path.abspath(a.out)); os.makedirs(outdir, exist_ok=True)
    en = [p for p, k in kinds.items() if k == 'en']; hi = [p for p, k in kinds.items() if k == 'hi']
    uns = [p for p, k in kinds.items() if k in ('unsettled', 'notext')]
    thumbs = ''
    if uns:
        tdir = os.path.join(outdir, 'thumbs'); os.makedirs(tdir, exist_ok=True)
        subprocess.run([sys.executable, '/home/claude/pyqkit.py', 'render', '--vault', V, fid, ','.join(map(str, uns)),
                        '--dpi', '24', '--out', tdir], capture_output=True, text=True)
        pngs = sorted(glob.glob(os.path.join(tdir, 'p*.png')), key=lambda s: int(re.sub(r'\D', '', os.path.basename(s)) or 0))
        if pngs:
            r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'phy_tile.py'),
                                '--out', os.path.join(outdir, 'thumbs_sheet'), '--dpi', '24'] + pngs, capture_output=True, text=True)
            thumbs = ' '.join(l.split(':')[0] for l in r.stdout.splitlines() if l.endswith(')') or 'px' in l)
    # align
    verdicts, rep = [], []
    byid0 = {r['instance_id']: r for r in I}
    used = {}; LOOK = {}; FIG = K.table(V, 'l1/FIGURES.csv')
    for q in sorted(s_q):
        st = tokens(s_q[q]); sw = words(st)
        best, br = None, 0.0
        for (p, oq), _ in groups.items():
            if p not in o_q or oq not in o_q[p]:
                continue
            r_ = difflib.SequenceMatcher(None, sw, words(tokens(o_q[p][oq])), autojunk=False).ratio()
            if r_ > br:
                best, br = (p, oq), r_
        if best is None or br < 0.55:
            verdicts.append((q, s_q[q]['page'], 'new question, full row', best, br, [], 0)); continue
        st = tokens(s_q[q])
        ot = tokens(o_q[best[0]][best[1]])
        grp = groups[best]
        known = set(TOK.findall(' '.join(' '.join([r['stem'], r['options'], r['givens']]) for r in grp)))
        known |= set(TOK.findall(' '.join(f['values'] + ' ' + f['description'] for f in FIG if f['instance_id'] in {r['instance_id'] for r in grp})))
        v, d, looks = compare(o_q[best[0]][best[1]], s_q[q], known, any(r['q_type'] == 'MCQ' for r in grp))
        nd = len(d)
        own_s = any(in_series(r, own) for r in grp)
        if v == 'repeat candidate' and not own_s:
            v = 'identical text in another series: full row'
        LOOK[q] = looks
        used.setdefault(best, []).append(q)
        verdicts.append((q, s_q[q]['page'], v, best, br, d, nd))
        if v == 'repeat candidate':
            for r in sorted(grp, key=lambda x: x['instance_id']):
                m = re.match(re.escape(r['paper_id']) + r'-Q(\d+)(.*)$', r['instance_id'])
                sid = f"{a.pid}-Q{q:02d}{m.group(2) if m else ''}"
                lab = r['part'].split('-')[-1] if r['part'] else None
                sp = page_for(ot, st, int(r['source_page']), lab, r['side'] == 'B') or s_q[q]['page']
                figs = [f for f in K.table(V, 'l1/FIGURES.csv') if f['instance_id'] == r['instance_id']]
                fp = ';'.join(str(sp if f['source_page'] == r['source_page'] else (page_for(ot, st, int(f['source_page'])) or sp)) for f in figs)
                ex = []
                for kv in r['extra'].split('; '):
                    k = kv.split('=')[0]
                    if k in PAGE_KEYS[:3] and '=' in kv:
                        try:
                            ex.append(f"{k}={page_for(ot, st, int(kv.split('=')[1].split(',')[0])) or sp}")
                        except ValueError:
                            ex.append(f'{k}=CHECK')
                rep.append(dict(status='candidate', sib_id=sid, origin_row=r['instance_id'],
                                rel_to=r['instance_id'] if r['rel'] == 'origin' else r['rel_to'], q_no=str(q),
                                side=r['side'], part=r['part'], section=section_of(secs, q) or r['section'],
                                choice_pair_id=f'OR-{a.pid}-Q{q:02d}' if r['choice_pair_id'] else '',
                                case_id=f'CS-{a.pid}-Q{q:02d}' if r['case_id'] else '', source_page=str(sp),
                                q_page=str(s_q[q]['page']), fig_pages=fp, extra_pages='; '.join(ex), note_add=''))
    # ARSET_page for a copied first assertion-reason row: the origin's offset from its row page
    ar_q = sorted(int(x['q_no']) for x in rep if byid0[x['origin_row']]['q_type'] == 'AR')
    full_ar = [q for q, p_, v, best, *_ in verdicts if v != 'repeat candidate' and best and any(r['q_type'] == 'AR' for r in groups[best])]
    if ar_q and (not full_ar or ar_q[0] < min(full_ar)):
        x = [x for x in rep if int(x['q_no']) == ar_q[0]][0]
        src = [r for r in I if r['paper_id'] == byid0[x['origin_row']]['paper_id'] and 'ARSET_page=' in r['extra']]
        if src:
            off = int(re.search(r'ARSET_page=(\d+)', src[0]['extra']).group(1)) - int(src[0]['source_page'])
            x['extra_pages'] = '; '.join([e for e in [x['extra_pages'], f"ARSET_page={int(x['source_page']) + off}"] if e])
    # worksheet
    L = [f'# S4 sibling worksheet {a.pid} · file {fid} · series {",".join(own)}' + (f' (compared also with {",".join(other)})' if other else ''),
         f'Origin questions from {", ".join(opids)} ({len(groups)} questions holding rel = origin rows); file {pdf}.', '',
         'Locating only. A repeat candidate is not a repeat until you confirm it on its band against the origin row below, '
         'and every figure on a 400 dpi crop (values and directions: a figure can change while the text stays the same). '
         'A text-layer mismatch is a reason to look, not a verdict (card A1). Any difference or doubt: a full row.', '']
    L += ['## Pages',
          f'- English pages (common-word share): {",".join(map(str, sorted(en))) or "none"}',
          f'- Hindi pages: {",".join(map(str, sorted(hi))) or "none"}',
          f'- not settled from the text layer: {",".join(map(str, sorted(uns))) or "none"}' + (f' -> thumbnail sheet {thumbs}: decide each from it' if thumbs else '')]
    if not s_q:
        L += ['- **No text layer could be segmented: every question is matched by you on the images against the origin rows listed at the end; record each confirmed repeat with --add-repeat.**']
    L += ['', f'located {len(s_q)} of {expect_n or "?"} questions in the text layer', '',
          '## Verdicts', '| this paper Q | page | verdict | origin question | word similarity | differences (origin -> this paper) |', '|---|---|---|---|---|---|']
    nrep = sum(1 for v in verdicts if v[2] == 'repeat candidate')
    for q, p, v, best, br, d, nd in verdicts:
        lk = LOOK.get(q, [])
        L.append(f"| {q} | {p} | {v}{' (look: ' + '; '.join(lk) + ')' if lk and v == 'repeat candidate' else ''} | {best[0] + ' Q' + str(best[1]) if best else '-'} | {br:.2f} | {'; '.join(d)} |")
    dup = {k: v for k, v in used.items() if len(v) > 1}
    if dup:
        L += ['', 'Origin questions matched twice: ' + '; '.join(f'{k[0]} Q{k[1]} <- Q{",".join(map(str, v))}' for k, v in dup.items())]
    L += ['', f'Summary: {nrep} repeat candidates ({len(rep)} rows), '
          f'{sum(1 for v in verdicts if v[2].startswith("variant"))} variants, '
          f'{sum(1 for v in verdicts if v[2].startswith("new"))} new questions, '
          f'{sum(1 for v in verdicts if v[2].startswith("identical"))} identical to another series.', '']
    F = K.table(V, 'l1/FIGURES.csv'); E = K.table(V, 'l1/FORMULAE.csv')
    L += ['## Repeat candidates: the origin rows to confirm on the band (sibling id, page as located)']
    byid = {r['instance_id']: r for r in I}
    for x in rep:
        r = byid[x['origin_row']]
        L.append(f"- **{x['sib_id']}** p{x['source_page']} <- {r['instance_id']} (p{r['source_page']}; rel_to {x['rel_to']})"
                 f" | {r['q_type']} | marks {r['marks_part'] or '-'}/{r['q_marks_printed']} | stem: {r['stem']}"
                 + (f" | givens: {r['givens']}" if r['givens'] else '') + (f" | options: {r['options']}" if r['options'] else '')
                 + (f" | extra: {r['extra']}" if r['extra'] else ''))
        for f in [f for f in F if f['instance_id'] == r['instance_id']]:
            L.append(f"  - figure {f['figure_id']} (p{f['source_page']} -> p{x['fig_pages']}): values: {f['values']} | {f['description'][:400]}")
        fs = [e for e in E if e['instance_id'] == r['instance_id'] and e['source'] == 'QP']
        if fs:
            L.append('  - formulae (QP): ' + ' ; '.join(f"{e['role']}: {e['formula']}" for e in fs))
    L += ['', '## Variants and new questions: what they resemble (for the note "resembles <id>: <what differs>")']
    for q, p, v, best, br, d, nd in verdicts:
        if v != 'repeat candidate' and best:
            ids = [r['instance_id'] for r in groups[best]]
            L.append(f"- Q{q} (p{p}): {v}; nearest {best[0]} Q{best[1]} ({', '.join(ids)}); text-layer differences: {'; '.join(d) or 'none'}")
    ar = [r for r in I if r['paper_id'] in opids and 'ARSET=' in r['extra']]
    L += ['', '## Finishing',
          f'1. Confirm each candidate on its band; crop every figure at 400 dpi. In {os.path.join(outdir, "REPEATS.csv")} set status to '
          '`confirmed` (or `variant`), correct q_no, source_page, fig_pages (one page per figure, in the order above) or extra_pages if the band '
          'shows otherwise, and put what the figure crops showed in note_add.',
          f'2. `python3 {os.path.abspath(__file__)} --write-repeats --pid {a.pid} --repeats {os.path.join(outdir, "REPEATS.csv")}` writes the confirmed '
          'shuffle rows, their FIGURES, FORMULAE (source QP) and CASES into the part files and merges them with yours; rerun it after any change.',
          '3. Write the new and variant rows yourself (full rows, card D); then the BLUEPRINTS row; then G check.',
          '4. ARSET: only the paper\'s first assertion-reason row carries it; --write-repeats drops it from copies that are not, '
          'and copies it onto a copy that is (confirm the printed set). Origin ARSET rows: ' + ', '.join(r['instance_id'] for r in ar)]
    open(a.out, 'w').write('\n'.join(L) + '\n')
    with open(os.path.join(outdir, 'REPEATS.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=RCOLS); w.writeheader(); w.writerows(rep)
    print(f'{a.out}: located {len(s_q)} of {expect_n or "?"}; {nrep} repeat candidates ({len(rep)} rows); '
          f'{sum(1 for v in verdicts if v[2] != "repeat candidate")} full-row questions; English pages {len(en)}, unsettled {len(uns)}')
    return verdicts, rep

def part_file(pid, t):
    return f'{V}/work/{pid}__{t}.csv'

def read_part(pid, t):
    p = part_file(pid, t)
    return list(csv.DictReader(open(p))) if os.path.exists(p) else []

def write_part(pid, t, rows):
    hdr = open(f'{V}/l1/{t}.csv').readline().strip().split(',')
    with open(part_file(pid, t), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=hdr); w.writeheader(); w.writerows(rows)

def batch_no():
    return str(json.load(open(f'{V}/STATE.json')).get('batch', ''))

def write_repeats(a):
    R = [r for r in csv.DictReader(open(a.repeats)) if r['status'].strip() == 'confirmed']
    I = {r['instance_id']: r for r in K.table(V, 'l1/INSTANCES.csv')}
    F = K.table(V, 'l1/FIGURES.csv'); E = K.table(V, 'l1/FORMULAE.csv'); C = {c['case_id']: c for c in K.table(V, 'l1/CASES.csv')}
    sib = [f for f in FILES.values() if f['paper_id'] == a.pid and f['kind'] == 'QP'][0]
    B = batch_no(); ids = {r['sib_id'] for r in R}
    ins = [r for r in read_part(a.pid, 'INSTANCES') if r['instance_id'] not in ids]
    figs = [r for r in read_part(a.pid, 'FIGURES') if r['instance_id'] not in ids]
    frm = [r for r in read_part(a.pid, 'FORMULAE') if r['instance_id'] not in ids]
    cases = read_part(a.pid, 'CASES')
    def nxt(rows, pre, w):
        n = [int(m.group(1)) for r in rows for m in [re.match(re.escape(pre) + r'(\d+)$', list(r.values())[0])] if m]
        return max(n) + 1 if n else 1
    nf, ne = nxt(figs, f'F-{a.pid}-', 2), nxt(frm, f'EQ-{a.pid}-', 3)
    new, warn = [], []
    for x in R:
        o = dict(I[x['origin_row']])
        oq = o['q_no']
        o.update(instance_id=x['sib_id'], paper_id=a.pid, file_id=sib['file_id'], paper_code=sib['paper_code'], q_no=x['q_no'],
                 side=x['side'], part=x['part'], section=x['section'], choice_pair_id=x['choice_pair_id'], case_id=x['case_id'],
                 source_page=x['source_page'], rel='shuffle', rel_to=x['rel_to'], read_from='image', batch=B)
        moved = f'; printed as Q{x["q_no"]} here, Q{oq} in the origin' if x['q_no'] != oq else ''
        o['note'] = (f'shuffle of {x["rel_to"]}, text and numbers identical on the page image (sibling worksheet; confirmed on the band)'
                     + moved + (f'; {x["note_add"]}' if x['note_add'].strip() else ''))
        exp = dict(kv.split('=', 1) for kv in x['extra_pages'].split('; ') if '=' in kv)
        ex = []
        for kv in o['extra'].split('; '):
            if not kv:
                continue
            k = kv.split('=')[0]
            if k in ('ARSET', 'ARSET_page'):
                continue                      # decided below
            if k in PAGE_KEYS and k in exp:
                kv = f'{k}={exp[k]}'
            ex.append(kv)
        o['_arset'] = [kv for kv in I[x['origin_row']]['extra'].split('; ') if kv.startswith('ARSET=')]
        o['_exp'] = exp
        o['extra'] = '; '.join(ex)
        new.append(o)
        ofigs = [f for f in F if f['instance_id'] == x['origin_row']]
        fps = [p for p in x['fig_pages'].split(';') if p.strip()]
        for i, f in enumerate(ofigs):
            g = dict(f); g.update(figure_id=f'F-{a.pid}-{nf:02d}', instance_id=x['sib_id'],
                                  source_page=fps[i] if i < len(fps) else x['source_page'], batch=B)
            nf += 1; figs.append(g)
        for e in [e for e in E if e['instance_id'] == x['origin_row'] and e['source'] == 'QP']:
            g = dict(e); g.update(formula_id=f'EQ-{a.pid}-{ne:03d}', instance_id=x['sib_id'], source_page=x['source_page'], batch=B)
            ne += 1; frm.append(g)
        if x['case_id'] and not any(c['case_id'] == x['case_id'] for c in cases):
            oc = C.get(I[x['origin_row']]['case_id'])
            if oc:
                c = dict(oc); c.update(case_id=x['case_id'], paper_id=a.pid, q_no=x['q_no'], source_page=x['q_page'] or x['source_page'], batch=B)
                cases.append(c)
    # ARSET: only the paper's first A-R row
    allrows = ins + new
    ars = sorted([r for r in allrows if r['q_type'] == 'AR'], key=lambda r: (int(r['q_no']), r['instance_id']))
    first = ars[0]['instance_id'] if ars else None
    for o in new:
        arset, exp = o.pop('_arset'), o.pop('_exp')
        if o['instance_id'] == first:
            if not arset:
                src = [r for r in I.values() if r['paper_id'] == I[[x for x in R if x['sib_id'] == first][0]['origin_row']]['paper_id'] and 'ARSET=' in r['extra']]
                arset = [kv for kv in src[0]['extra'].split('; ') if kv.startswith('ARSET=')] if src else []
                warn.append(f'{first}: ARSET copied from {src[0]["instance_id"] if src else "?"}; confirm the printed set')
            extra = [kv for kv in o['extra'].split('; ') if kv] + arset
            if 'ARSET_page' in exp:
                extra.append(f'ARSET_page={exp["ARSET_page"]}')
            elif arset:
                warn.append(f'{first}: give ARSET_page in extra_pages if the set is printed on another page')
            o['extra'] = '; '.join(extra)
    keyq = lambda r: (int(r['q_no']), r['instance_id'])
    write_part(a.pid, 'INSTANCES', sorted(ins + new, key=keyq))
    write_part(a.pid, 'FIGURES', figs); write_part(a.pid, 'FORMULAE', frm)
    if cases:
        write_part(a.pid, 'CASES', cases)
    print(f'wrote {len(new)} shuffle rows, {sum(1 for f in figs if f["instance_id"] in ids)} figure rows, '
          f'{sum(1 for e in frm if e["instance_id"] in ids)} formula rows, {sum(1 for c in cases if c["batch"] == B)} case rows into {V}/work/{a.pid}__*.csv')
    for w in warn:
        print('check:', w)

def add_repeat(a):
    I = K.table(V, 'l1/INSTANCES.csv')
    opid, oq = a.origin_q.split(':'); q = int(a.q)
    grp = [r for r in I if r['paper_id'] == opid and int(r['q_no']) == int(oq)]
    if a.only:
        grp = [r for r in grp if r['instance_id'] in set(a.only.split(','))]   # single confirmed parts of a mixed question
    secs = sections(a.pid) or sections(opid)
    rows = list(csv.DictReader(open(a.repeats))) if os.path.exists(a.repeats) else []
    have = {r['sib_id'] for r in rows}
    for r in sorted(grp, key=lambda x: x['instance_id']):
        m = re.match(re.escape(opid) + r'-Q(\d+)(.*)$', r['instance_id'])
        sid = f"{a.pid}-Q{q:02d}{m.group(2)}"
        if sid in have:
            continue
        figs = [f for f in K.table(V, 'l1/FIGURES.csv') if f['instance_id'] == r['instance_id']]
        rows.append(dict(status='confirmed', sib_id=sid, origin_row=r['instance_id'],
                         rel_to=r['instance_id'] if r['rel'] == 'origin' else r['rel_to'], q_no=str(q), side=r['side'],
                         part=r['part'], section=section_of(secs, q) or r['section'],
                         choice_pair_id=f'OR-{a.pid}-Q{q:02d}' if r['choice_pair_id'] else '',
                         case_id=f'CS-{a.pid}-Q{q:02d}' if r['case_id'] else '', source_page=str(a.page), q_page=str(a.page),
                         fig_pages=';'.join(str(a.page) for _ in figs), extra_pages='', note_add=''))
    with open(a.repeats, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=RCOLS); w.writeheader(); w.writerows(rows)
    print(f'{a.repeats}: {len(grp)} rows of {opid} Q{oq} as Q{q} (status confirmed; correct pages per row before --write-repeats)')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--pid', required=True); ap.add_argument('--fid', default=''); ap.add_argument('--pdf', default='')
    ap.add_argument('--series', default=''); ap.add_argument('--compare', default=''); ap.add_argument('--exclude', default='')
    ap.add_argument('--out', default=''); ap.add_argument('--write-repeats', action='store_true'); ap.add_argument('--repeats', default='')
    ap.add_argument('--add-repeat', action='store_true'); ap.add_argument('--q', default=''); ap.add_argument('--origin-q', default='')
    ap.add_argument('--page', default=''); ap.add_argument('--only', default='')
    a = ap.parse_args()
    if a.write_repeats:
        write_repeats(a)
    elif a.add_repeat:
        add_repeat(a)
    else:
        prepare(a)
