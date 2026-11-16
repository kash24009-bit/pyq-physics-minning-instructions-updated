#!/usr/bin/env python3
"""Usage of reader subagents from their transcripts (.jsonl), weighted as the plan meter counts
(her decision 2026-10-21; PHY-07 R§14, PHY-08 Y§1). Edition 2026-10-26 (B08).

  python3 phy_measure.py --dir ~/.claude/projects/<slug>/<session-id> [--units U1,U2] [--main <session>.jsonl] [--md out.md]
  python3 phy_measure.py label=transcript.jsonl ... [--main <session>.jsonl]

--dir finds every subagent transcript under <dir>/subagents/ and names it by the "Unit <x>" that
opens its brief (or the brief's first words). --main adds each unit's main-session cost: the
main-session calls after the previous unit's reader ended, up to this unit's reader end.

Weights against base input (Opus 5.5 list rates): uncached input 1, cache read 0.05,
5-minute cache write 1.25, 1-hour cache write 2, output 5 (thinking is billed as output).
The 5-minute/1-hour split comes from usage.cache_creation (ephemeral_5m_input_tokens,
ephemeral_1h_input_tokens) where present; otherwise subagents 5-minute, main session 1-hour.

Per unit: steps (model calls); images (count, total bytes, largest file); the first step's
cache read against its cache write; cache misses (a step whose cache read falls below half of
the previous step's context); raw sum (input + cache writes + cache reads + output) and the
weighted sum with each component's share.
Image check: every image a reader opened, its width and height as sent (from the image data
in the transcript, else the file on disk) and its cost ceil(w/28) x ceil(h/28) visual tokens;
for steps that read only images, that sum against the next step's context growth minus the
step's own output, as a ratio per kind (bands, crops, sheets, pages). A ratio well below 1
means an image was shrunk before the model saw it.
"""
import argparse, base64, glob, json, math, os, re, struct, sys
from datetime import datetime

W_IN, W_CR, W_5M, W_1H, W_OUT = 1.0, 0.05, 1.25, 2.0, 5.0

def ts(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))

def dims_from_bytes(b):
    if b[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', b[16:24])
    if b[:2] == b'\xff\xd8':
        i = 2
        while i < len(b) - 9:
            if b[i] != 0xFF:
                i += 1; continue
            m = b[i + 1]
            if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack('>HH', b[i + 5:i + 9]); return w, h
            seg = struct.unpack('>H', b[i + 2:i + 4])[0]; i += 2 + seg
    return None

def image_info(block, path):
    """(width, height, bytes, source) of one image as sent."""
    data = None
    src = block.get('source') or {}
    if isinstance(src, dict) and src.get('data'):
        data = src['data']
    if data:
        raw = base64.b64decode(data[:200000] if len(data) > 200000 else data)
        d = dims_from_bytes(raw[:200000])
        size = len(data) * 3 // 4 - data[-2:].count('=')
        if d:
            return d[0], d[1], size, 'transcript'
    if path and os.path.exists(path):
        from PIL import Image
        with Image.open(path) as im:
            return im.size[0], im.size[1], os.path.getsize(path), 'disk'
    return None

def kind_of(path):
    p = (path or '').lower()
    for k in ('bands', 'sheets', 'pages', 'thumbs'):
        if f'/{k}/' in p or f'/{k}_' in p or os.path.basename(os.path.dirname(p)).startswith(k):
            return k
    return 'crops'

def load(path, default_split):
    calls, order = {}, []
    tool_inputs = {}                      # tool_use id -> (name, input)
    call_tools = {}                       # message id -> [tool_use ids]
    results = {}                          # tool_use id -> list of image infos
    t, first_prompt = [], None
    for line in open(path):
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get('timestamp'):
            t.append(d['timestamp'])
        m = d.get('message') or {}
        if not isinstance(m, dict):
            continue
        if d.get('type') == 'user' and first_prompt is None:
            c = m.get('content')
            if isinstance(c, str):
                first_prompt = c
            elif isinstance(c, list):
                for x in c:
                    if isinstance(x, dict) and x.get('type') == 'text':
                        first_prompt = x.get('text', ''); break
        if d.get('type') == 'assistant':
            mid = m.get('id'); u = m.get('usage') or {}
            if mid and u:
                if mid not in calls:
                    order.append(mid); calls[mid] = {'_ts': d.get('timestamp')}
                cu = calls[mid]
                for k, v in u.items():
                    if isinstance(v, (int, float)):
                        cu[k] = max(cu.get(k, 0), v)
                    elif k == 'output_tokens_details' and isinstance(v, dict):
                        cu['_think'] = max(cu.get('_think', 0), v.get('thinking_tokens', 0) or 0)
                    elif k == 'cache_creation' and isinstance(v, dict):
                        cc = cu.setdefault('cache_creation', {})
                        for k2, v2 in v.items():
                            if isinstance(v2, (int, float)):
                                cc[k2] = max(cc.get(k2, 0), v2)
            for c in m.get('content', []) or []:
                if isinstance(c, dict) and c.get('type') == 'tool_use':
                    tool_inputs[c['id']] = (c.get('name'), c.get('input', {}))
                    if mid:
                        call_tools.setdefault(mid, []).append(c['id'])
        if d.get('type') == 'user' and isinstance(m.get('content'), list):
            for c in m['content']:
                if isinstance(c, dict) and c.get('type') == 'tool_result':
                    tid = c.get('tool_use_id'); imgs = []
                    name, inp = tool_inputs.get(tid, (None, {}))
                    fp = inp.get('file_path') if isinstance(inp, dict) else None
                    if isinstance(c.get('content'), list):
                        for x in c['content']:
                            if isinstance(x, dict) and x.get('type') == 'image':
                                info = image_info(x, fp)
                                imgs.append((fp, info))
                    results[tid] = imgs
    return dict(split=default_split, calls=calls, order=order, call_tools=call_tools, tool_inputs=tool_inputs, results=results,
                t0=t[0] if t else None, t1=t[-1] if t else None, prompt=first_prompt or '')

def split_cw(u, default_split):
    cc = u.get('cache_creation') or {}
    e5, e1 = cc.get('ephemeral_5m_input_tokens', 0), cc.get('ephemeral_1h_input_tokens', 0)
    tot = u.get('cache_creation_input_tokens', 0)
    if e5 + e1 == 0 and tot:
        return (tot, 0) if default_split == '5m' else (0, tot)
    return e5, e1

def ctx(u):
    return u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0)

def weigh(u, default_split):
    e5, e1 = split_cw(u, default_split)
    return dict(inp=u.get('input_tokens', 0) * W_IN, cr=u.get('cache_read_input_tokens', 0) * W_CR,
                cw=e5 * W_5M + e1 * W_1H, out=u.get('output_tokens', 0) * W_OUT)

def unit_stats(r, default_split=None):
    default_split = default_split or r.get('split', '5m')
    calls, order = r['calls'], r['order']
    us = [calls[m] for m in order]
    raw = sum(ctx(u) + u.get('output_tokens', 0) for u in us)
    comp = dict(inp=0.0, cr=0.0, cw=0.0, out=0.0)
    for u in us:
        for k, v in weigh(u, default_split).items():
            comp[k] += v
    wsum = sum(comp.values())
    misses = [i + 1 for i in range(1, len(us)) if us[i].get('cache_read_input_tokens', 0) < 0.5 * ctx(us[i - 1])]
    imgs = [(fp, info) for tid in r['results'] for fp, info in r['results'][tid]]
    sizes = [info[2] for _, info in imgs if info]
    largest = max(imgs, key=lambda x: x[1][2] if x[1] else 0) if imgs else None
    # image check: steps whose tool calls are all Reads returning images
    check = {}
    for i, mid in enumerate(order[:-1]):
        tids = r['call_tools'].get(mid, [])
        if not tids:
            continue
        if not all(r['tool_inputs'].get(t, (None,))[0] == 'Read' and r['results'].get(t) for t in tids):
            continue
        vis, kinds = 0, {}
        ok = True
        for t in tids:
            for fp, info in r['results'][t]:
                if not info:
                    ok = False; continue
                v = math.ceil(info[0] / 28) * math.ceil(info[1] / 28)
                vis += v; k = kind_of(fp); kinds[k] = kinds.get(k, 0) + v
        if not ok or not vis:
            continue
        growth = ctx(calls[order[i + 1]]) - ctx(calls[mid]) - calls[mid].get('output_tokens', 0)
        k = max(kinds, key=kinds.get) if len(kinds) > 1 else next(iter(kinds))
        c = check.setdefault(k, [0, 0, 0]); c[0] += sum(len(r['results'][t]) for t in tids); c[1] += vis; c[2] += growth
    allk = {}
    for fp, info in imgs:
        if info:
            k = kind_of(fp); a = allk.setdefault(k, [0, 0, 0, 0]); a[0] += 1; a[1] += math.ceil(info[0] / 28) * math.ceil(info[1] / 28)
            a[2] = max(a[2], info[0]); a[3] = max(a[3], info[1])
    mins = (ts(r['t1']) - ts(r['t0'])).total_seconds() / 60 if r['t0'] else 0
    first = us[0] if us else {}
    think = sum(u.get('_think', 0) for u in us); outt = sum(u.get('output_tokens', 0) for u in us)
    return dict(think=think, outt=outt, steps=len(us), raw=raw, w=wsum, comp=comp, misses=misses, n_img=len(imgs), bytes=sum(sizes),
                largest=(os.path.basename(largest[0] or '?'), largest[1][2]) if largest and largest[1] else None,
                first_read=first.get('cache_read_input_tokens', 0), first_write=first.get('cache_creation_input_tokens', 0),
                first_ctx=ctx(first), first_w=sum(weigh(first, default_split).values()) if first else 0,
                check=check, kinds=allk, minutes=mins, t0=r['t0'], t1=r['t1'])

def unit_name(prompt, fallback):
    m = re.match(r'\s*Unit\s+(\S+)', prompt or '')
    if m:
        return m.group(1).rstrip('·').strip()
    return (prompt or fallback).strip().split('\n')[0][:40] or fallback

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir'); ap.add_argument('--units', default=''); ap.add_argument('--main')
    ap.add_argument('--md'); ap.add_argument('pairs', nargs='*')
    a = ap.parse_args()
    units = []
    for p in a.pairs:
        label, path = p.split('=', 1)
        units.append((label, load(path, '1h' if label == 'main' else '5m')))
    if a.dir:
        for path in sorted(glob.glob(os.path.join(os.path.expanduser(a.dir), 'subagents', '*.jsonl'))):
            r = load(path, '5m')
            units.append((unit_name(r['prompt'], os.path.basename(path)), r))
    want = [u for u in a.units.split(',') if u]
    if want:
        units = [(l, r) for l, r in units if l in want]
    units = [(l, r) for l, r in units if r['order']]
    units.sort(key=lambda x: x[1]['t0'] or '')
    main_r = load(os.path.expanduser(a.main), '1h') if a.main else None
    L = []
    L.append('| unit | steps | images (n · KB · largest) | first step read / write | cache misses (step) | raw sum | weighted sum | output (thinking share) | cache writes | cache reads | uncached input | main session weighted | minutes |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    prev_end = None; tot = dict(inp=0.0, cr=0.0, cw=0.0, out=0.0)
    for label, r in units:
        s = unit_stats(r)
        for k in tot:
            tot[k] += s['comp'][k]
        mw = '-'
        if main_r:
            w = 0.0
            for mid in main_r['order']:
                u = main_r['calls'][mid]; t = u.get('_ts')
                if t and (prev_end is None or t > prev_end) and t <= s['t1']:
                    w += sum(weigh(u, '1h').values())
            mw = f'{w:,.0f}'
        prev_end = s['t1']
        c = s['comp']; W = s['w'] or 1
        lg = f" · {s['largest'][0]} {s['largest'][1]/1024:.0f}" if s['largest'] else ''
        L.append(f"| {label} | {s['steps']} | {s['n_img']} · {s['bytes']/1024:,.0f}{lg} | {s['first_read']:,} / {s['first_write']:,}"
                 f"{' (shared)' if s['first_read'] > s['first_write'] else ''} | {len(s['misses'])}{' (' + ','.join(map(str, s['misses'])) + ')' if s['misses'] else ''} | "
                 f"{s['raw']:,} | {s['w']:,.0f} | {100*c['out']/W:.0f} % ({100*s['think']/max(1,s['outt']):.0f} %) | {100*c['cw']/W:.0f} % | {100*c['cr']/W:.0f} % | {100*c['inp']/W:.0f} % | {mw} | {s['minutes']:.1f} |")
    L.append('')
    L.append('Image check (steps that read only images): visual tokens = sum of ceil(w/28) x ceil(h/28) as sent; growth = next step\'s context - this step\'s context - its output.')
    L.append('')
    L.append('| unit | kind | images opened (all steps) | largest w x h | images in image-only steps | visual tokens | growth - output | ratio |')
    L.append('|---|---|---|---|---|---|---|---|')
    for label, r in units:
        s = unit_stats(r)
        for k in sorted(set(s['kinds']) | set(s['check'])):
            a_ = s['kinds'].get(k, [0, 0, 0, 0]); c_ = s['check'].get(k)
            ratio = f"{c_[2]/c_[1]:.2f}" if c_ and c_[1] else '-'
            L.append(f"| {label} | {k} | {a_[0]} | {a_[2]} x {a_[3]} | {c_[0] if c_ else 0} | {c_[1] if c_ else 0:,} | {c_[2] if c_ else 0:,} | {ratio} |")
    T = sum(tot.values()) or 1
    names = dict(out='output', cw='cache writes', cr='cache reads', inp='uncached input')
    big = max(tot, key=tot.get)
    L.append('')
    L.append(f"Largest share of the weighted sum over these units: {names[big]} ({100*tot[big]/T:.0f} %; output {100*tot['out']/T:.0f} %, cache writes {100*tot['cw']/T:.0f} %, cache reads {100*tot['cr']/T:.0f} %, uncached input {100*tot['inp']/T:.0f} %).")
    out = '\n'.join(L)
    print(out)
    if a.md:
        with open(a.md, 'a') as f:
            f.write(out + '\n')

if __name__ == '__main__':
    main()
