#!/usr/bin/env python3
"""Usage of reader subagents from their transcripts (.jsonl): one table row per unit.
  python3 phy_measure.py label=pid=transcript.jsonl[=calibration] ... [--main main.jsonl]
Steps = model calls; context = input + cache-write + cache-read tokens of a call;
sum = input + cache-write + cache-read + output over all calls.
"""
import json, sys, csv, re
V = '/home/claude/vault'
def load(path):
    calls, order, imgs, t = {}, [], 0, []
    marks = {}            # tool_use id -> 'card'/'prep'
    seen_after = None
    events = []
    for line in open(path):
        try: d = json.loads(line)
        except Exception: continue
        if d.get('timestamp'): t.append(d['timestamp'])
        m = d.get('message') or {}
        if d.get('type') == 'assistant' and isinstance(m, dict):
            mid = m.get('id'); u = m.get('usage') or {}
            if mid and u:
                if mid not in calls: order.append(mid); calls[mid] = dict(u); events.append(('call', mid))
                else:
                    for k, v in u.items():
                        if isinstance(v, int): calls[mid][k] = max(calls[mid].get(k, 0), v)
            for c in m.get('content', []) or []:
                if c.get('type') == 'tool_use':
                    s = json.dumps(c.get('input', {}))
                    if 'RULE-CARD' in s: marks[c['id']] = marks.get(c['id'], '') + 'card'
                    if 'PREP.md' in s: marks[c['id']] = marks.get(c['id'], '') + 'prep'
        if d.get('type') == 'user' and isinstance(m.get('content'), list):
            for c in m['content']:
                if isinstance(c, dict) and c.get('type') == 'tool_result':
                    events.append(('res', marks.get(c.get('tool_use_id'), '')))
                    if isinstance(c.get('content'), list):
                        imgs += sum(1 for x in c['content'] if isinstance(x, dict) and x.get('type') == 'image')
    ctx = lambda u: u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0)
    got = ''; after = None
    for kind, val in events:
        if kind == 'res': got += val
        elif 'card' in got and 'prep' in got and after is None: after = ctx(calls[val])
    total = sum(ctx(u) + u.get('output_tokens', 0) for u in calls.values())
    mins = 0
    if t:
        from datetime import datetime
        f = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00'))
        mins = (f(t[-1]) - f(t[0])).total_seconds() / 60
    return dict(steps=len(order), images=imgs, first=ctx(calls[order[0]]), after=after, end=ctx(calls[order[-1]]), total=total, minutes=mins, t0=t[0], t1=t[-1])
rows = []
for arg in sys.argv[1:]:
    if arg.startswith('--'): continue
    parts = arg.split('=')
    label, pid, path = parts[0], parts[1], parts[2]; cal = parts[3] if len(parts) > 3 else '-'
    r = load(path)
    lines = sum(1 for x in csv.DictReader(open(f'{V}/l1/STEP-AWARDS.csv')) if x['paper_id'] == pid)
    rows.append((label, r, lines, cal))
print('| unit | steps | images | context first | after card+worksheet | context end | sum all steps | minutes | lines | calibration |')
print('|---|---|---|---|---|---|---|---|---|---|')
for label, r, lines, cal in rows:
    print(f"| {label} | {r['steps']} | {r['images']} | {r['first']:,} | {r['after'] or '-':,} | {r['end']:,} | {r['total']:,} | {r['minutes']:.1f} | {lines} | {cal} |")
