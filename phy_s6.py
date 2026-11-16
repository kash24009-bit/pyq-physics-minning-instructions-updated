#!/usr/bin/env python3
"""phy_s6.py - pattern sorting (S6 classification) helper for PYQ Pattern Mining - Physics (042).
Edition 2026-11-16. Written and tested in the project chat on a copy of vault B10 (25,179 rows).

It never writes Layer 1. It prepares what a reader needs, turns the reader's decisions into part files the
gate merges (`<unit>__CLASSIFY.csv`, `<unit>__ERRATA.csv`), applies the reader's REGISTRY rows (Layer 1.5,
re-runnable, through the kit's own read_table/write_table, as PHY-07 R§12 step 5 says) and checks everything
before the gate commit. Every count it prints is computed from the vault.

  status                                  rows to classify per chapter, done so far, repeat groups
  groups                                  repeat groups across all years -> work/S6-GROUPS.csv (run once, first)
  sheet   --chapter 04 [--max 380]        the reader's sheet(s): work/S6-CH04__SHEET.md (-1, -2 parts above 380 rows)
  lines   <instance_id> [...]             the printed scoring lines of rows (for skeletons and traps)
  registry --unit S6-CH04                 check and apply work/S6-CH04__REGISTRY.csv to j/REGISTRY.csv
  expand  --unit S6-CH04                  work/S6-CH04__DECISIONS.csv -> __CLASSIFY.csv (+ __ERRATA.csv)
  check   --unit S6-CH04                  every check, PASS/FAIL lines; run before `phy_gate.py commit`
  review  [--chapter 04]                  granularity review list (codes used once, look-alike codes)
  alias   --unit S6-REVIEW --from X --to Y --reason "..."   merge X into Y (ALIAS) with ERRATA for X's rows
  expand  --unit S6-REVIEW --any          re-decide any rows (a split, or a change found in review)
  misses  [--write-notes]                 per-year prediction (leave one year out) against what was asked
  coverage                                which rows still lack a CLASSIFY row, by year (the DoD line 5 view)
Paths: vault /home/claude/vault, kit /home/claude/pyqkit.py (override with PHY_VAULT, PHY_KIT).
"""
import argparse, csv, datetime as dt, importlib.util, json, os, re, shutil, sys
from collections import Counter, defaultdict

EDITION = "2026-11-16"
V = os.environ.get("PHY_VAULT", "/home/claude/vault")
KIT = os.environ.get("PHY_KIT", "/home/claude/pyqkit.py")
ENV = os.environ.get("PHY_ENV", "/home/claude/phy_env.json")
csv.field_size_limit(10 ** 8)


def kit():
    spec = importlib.util.spec_from_file_location("pyqkit", KIT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


K = kit()
W = os.path.join(V, "work")
COG, YN, DIFF, CONF = {"REM", "UND", "APP", "ANL"}, {"y", "n"}, {"E", "M", "H"}, {"H", "M", "L"}
DEC_COLS = ["instance_id", "code", "cog_level", "competency", "difficulty", "confidence"]
BOARD = ("MAIN", "COMPT", "T1", "T2")


def batch():
    if os.path.exists(ENV):
        try:
            return int(json.load(open(ENV, encoding="utf-8"))["session_batch"])
        except Exception:
            pass
    return int(K.load_state(V).get("batch", 0))


def read_csv(p):
    with open(p, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        return list(rd.fieldnames or []), [dict(r) for r in rd]


def write_csv(p, header, rows):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p + ".tmp", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header, extrasaction="raise")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in header})
    os.replace(p + ".tmp", p)


def load():
    I = K.table(V, "l1/INSTANCES.csv")
    T = {"I": I, "byid": {r["instance_id"]: r for r in I},
         "reg": {r["code"]: r for r in K.table(V, "j/REGISTRY.csv")},
         "cls": {r["instance_id"]: r for r in K.table(V, "j/CLASSIFY.csv")},
         "steps": defaultdict(list), "figs": defaultdict(list), "cases": {}}
    for s in K.table(V, "l1/STEP-AWARDS.csv"):
        T["steps"][s["instance_id"]].append(s)
    for f in K.table(V, "l1/FIGURES.csv"):
        T["figs"][f["instance_id"]].append(f)
    for c in K.table(V, "l1/CASES.csv"):
        T["cases"][c["case_id"]] = c
    return T


def judged(r):
    """Rows a reader decides: origin rows that are not visually-impaired alternatives."""
    return r["rel"] == "origin" and r.get("vi_alt", "") != "y"


def needs_row(r):
    """Rows the Definition of Done line 5 counts (kit year-close): every row except vi_alt rows."""
    return r.get("vi_alt", "") != "y"


def chap_of(T, r):
    if r["rel"] == "shuffle" and r.get("rel_to") in T["byid"]:
        return T["byid"][r["rel_to"]]["chapter"]
    return r["chapter"]


def norm_text(s):
    s = (s or "").lower()
    s = re.sub(r"^\s*(?:\(?[a-z0-9]{1,5}\)\s*)+", "", s)          # printed labels (a) (ii) at the start
    s = s.replace("...", " ")
    return re.sub(r"[^a-z0-9.]+", " ", s).strip()


def numset(r):
    return tuple(sorted(K_nums(" ".join((r["stem"], r["givens"], r["options"])))))


def K_nums(t):
    return set(re.findall(r"-?\d+(?:\.\d+)?(?:e-?\d+)?", t or ""))


def toks(s):
    return {w for w in norm_text(s).split() if len(w) > 2 and not re.fullmatch(r"[\d.]+", w)}


# ------------------------------------------------------------------------------------------------ groups
def cmd_groups(a):
    T = load()
    rows = [r for r in T["I"] if judged(r)]
    key = defaultdict(list)
    for r in rows:
        n = norm_text(r["stem"])
        if len(n) >= 30:
            key[(r["chapter"], r["q_type"], n, numset(r), r["options"])].append(r)
    groups = [v for v in key.values() if len(v) > 1]
    used = {r["instance_id"] for g in groups for r in g}
    # near repeats: same chapter, q_type and numbers, word overlap >= 0.85
    pool = [r for r in rows if r["instance_id"] not in used and len(toks(r["stem"])) >= 6]
    idx = defaultdict(list)
    for i, r in enumerate(pool):
        idx[(r["chapter"], r["q_type"], numset(r))].append(i)
    parent = list(range(len(pool)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for lst in idx.values():
        for i in range(len(lst)):
            ti = toks(pool[lst[i]]["stem"])
            for j in range(i + 1, len(lst)):
                tj = toks(pool[lst[j]]["stem"])
                if len(ti & tj) / max(1, len(ti | tj)) >= 0.85:
                    parent[find(lst[i])] = find(lst[j])
    near = defaultdict(list)
    for i in range(len(pool)):
        near[find(i)].append(pool[i])
    groups += [v for v in near.values() if len(v) > 1]
    out = []
    for n, g in enumerate(sorted(groups, key=lambda g: (g[0]["chapter"], g[0]["instance_id"])), 1):
        # leader: the newest main-exam row, then the lowest id (the decision is written once, applied to all)
        g = sorted(g, key=lambda r: (-(K.year_int(r) or 0), r["exam"] not in ("MAIN", "T2"), r["instance_id"]))
        how = "exact" if norm_text(g[0]["stem"]) == norm_text(g[-1]["stem"]) else "near"
        for k, r in enumerate(g):
            out.append({"group_id": f"G{n:04d}", "instance_id": r["instance_id"], "leader": "y" if k == 0 else "n",
                        "chapter": r["chapter"], "year": r["year"], "exam": r["exam"], "paper_id": r["paper_id"],
                        "how": how})
    write_csv(os.path.join(W, "S6-GROUPS.csv"), ["group_id", "instance_id", "leader", "chapter", "year", "exam",
                                                 "paper_id", "how"], out)
    ng = len({x["group_id"] for x in out})
    yrs = Counter(len({x["year"] for x in out if x["group_id"] == g}) > 1 for g in {x["group_id"] for x in out})
    print(f"groups: {ng} repeat groups, {len(out)} rows ({len(out) - ng} rows decided by their leader); "
          f"{yrs[True]} groups span two or more years -> work/S6-GROUPS.csv")


def group_map():
    p = os.path.join(W, "S6-GROUPS.csv")
    if not os.path.exists(p):
        sys.exit("REFUSED: work/S6-GROUPS.csv is missing: run `phy_s6.py groups` first")
    rows = read_csv(p)[1]
    lead, members = {}, defaultdict(list)
    for r in rows:
        if r["leader"] == "y":
            lead[r["group_id"]] = r["instance_id"]
    for r in rows:
        if r["leader"] == "n":
            members[lead[r["group_id"]]].append(r["instance_id"])
    follower = {m: l for l, ms in members.items() for m in ms}
    return members, follower


# ------------------------------------------------------------------------------------------------ status
def cmd_status(a):
    T = load()
    members, follower = group_map() if os.path.exists(os.path.join(W, "S6-GROUPS.csv")) else ({}, {})
    by = defaultdict(Counter)
    for r in T["I"]:
        if not needs_row(r):
            continue
        c = chap_of(T, r)
        by[c]["rows"] += 1
        by[c]["done"] += r["instance_id"] in T["cls"]
        if judged(r):
            by[c]["judged"] += 1
            if r["instance_id"] not in follower:
                by[c]["decisions"] += 1
        elif r["rel"] == "shuffle":
            by[c]["shuffles"] += 1
    print("chapter | rows (DoD) | already classified | origin rows | reader decisions (repeats folded) | shuffles (copied)")
    tot = Counter()
    for c in sorted(by):
        b = by[c]
        tot.update(b)
        print(f"  {c} | {b['rows']} | {b['done']} | {b['judged']} | {b['decisions']} | {b['shuffles']}")
    print(f"  all | {tot['rows']} | {tot['done']} | {tot['judged']} | {tot['decisions']} | {tot['shuffles']}")


# ------------------------------------------------------------------------------------------------ sheet
STOPW = None


def candidates(T, r, k=3):
    global STOPW
    q = K.norm_tokens(r["stem"] + " " + r["unknown"])
    stems = T.setdefault("_stems", None)
    if stems is None:
        stems = defaultdict(set)
        for iid, c in T["cls"].items():
            if iid in T["byid"]:
                stems[c["code"]] |= K.norm_tokens(T["byid"][iid]["stem"])
        T["_stems"] = stems
    out = []
    for code, g in T["reg"].items():
        if g["chapter"] != r["chapter"] or g["status"] not in ("DRAFT", "VERIFIED"):
            continue
        t = K.norm_tokens(g["name"] + " " + g["asks_you_to"] + " " + g["skeleton"]) | stems.get(code, set())
        u = len(q | t)
        s = (len(q & t) / u if u else 0) + (0.10 if g["q_type"] == r["q_type"] else 0) \
            + (0.05 if g["topic_id"] == r["topic_id"] else 0)
        out.append((s, code))
    out.sort(key=lambda x: -x[0])
    return out[:k]


def skel(T, iid):
    ss = T["steps"].get(iid, [])
    if not ss:
        return "no lines"
    ab = {"formula": "f", "substitution": "s", "result": "r", "unit": "u", "diagram": "d", "label": "l",
          "reason": "why", "definition": "def", "key": "key", "other": "o"}
    return " ".join(f"{ab.get(s['step_kind'], s['step_kind'])}{s['marks']}" for s in ss)


def short(s, n):
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "~"


def cmd_sheet(a):
    T = load()
    members, follower = group_map()
    cc = a.chapter.zfill(2)
    rows = [r for r in T["I"] if judged(r) and r["chapter"] == cc and r["instance_id"] not in follower]
    vi = [r for r in T["I"] if r.get("vi_alt") == "y" and r["rel"] == "origin" and r["chapter"] == cc]
    rows.sort(key=lambda r: (r["topic_id"], r["q_type"], -(K.year_int(r) or 0), r["instance_id"]))
    k = -(-len(rows) // a.max) or 1                 # parts of equal size, never more than --max rows each
    size = -(-len(rows) // k) if rows else 1
    parts = [rows[i:i + size] for i in range(0, len(rows), size)] or [rows]
    syl = {s["topic_id"]: s for s in K.table(V, "j/SYLLABUS.csv")}
    written = []
    for n, part in enumerate(parts, 1):
        unit = f"S6-CH{cc}" + (f"-{n}" if len(parts) > 1 else "")
        L = [f"# {unit} · pattern-sorting sheet · chapter {cc} · phy_s6.py {EDITION} · batch B{batch():02d}",
             f"Rows to decide here: {len(part)} (part {n} of {len(parts)}); repeats folded into their leader: "
             f"{sum(len(members.get(r['instance_id'], [])) for r in part)}; shuffles copied by script.",
             "Write work/" + unit + "__DECISIONS.csv (" + ",".join(DEC_COLS) + ") and, for new or changed codes, "
             "work/" + unit + "__REGISTRY.csv (the REGISTRY header). Rules: PHY-10.", "",
             "## Registry of this chapter (code [status] q_type · name · asks_you_to · used n)"]
        used = Counter(c["code"] for c in T["cls"].values())
        for code, g in sorted(T["reg"].items()):
            if g["chapter"] == cc and g["status"] in ("DRAFT", "VERIFIED"):
                L.append(f"- {code} [{g['status']}] {g['q_type']} · {g['name']} · {short(g['asks_you_to'], 140)} · "
                         f"{g['family'].split(' ', 1)[0]} · used {used[code]}")
        fams = sorted({g["family"] for g in T["reg"].values() if g["chapter"] == cc and g["family"]})
        L += ["", "Families: " + "; ".join(fams), "", "## Rows (grouped by topic)",
              "id · year exam · type marks · stem · asks · lines · candidates [· now <code>] [· repeats]"]
        last_topic, seen_case = None, set()
        for r in part:
            if r["topic_id"] != last_topic:
                last_topic = r["topic_id"]
                t = syl.get(last_topic, {})
                L += ["", f"### {last_topic} · {t.get('topic', '')[:90]} · {t.get('status', '')}"]
            if r["case_id"] and r["case_id"] not in seen_case and r["case_id"] in T["cases"]:
                seen_case.add(r["case_id"])
                L.append(f"  CASE {r['case_id']}: {short(T['cases'][r['case_id']]['context'], 220)}")
            mk = r["marks_part"] or r["q_marks_printed"] or "?"
            cand = ", ".join(f"{c} {s:.2f}" for s, c in candidates(T, r))
            now = T["cls"].get(r["instance_id"], {}).get("code", "")
            fig = ""
            if r["has_figure"] == "y" and T["figs"].get(r["instance_id"]):
                fig = " · fig: " + short(T["figs"][r["instance_id"]][0]["description"], 110)
            rep = members.get(r["instance_id"], [])
            L.append(f"- {r['instance_id']} · {r['year']} {r['exam']} · {r['q_type']} {mk} · "
                     f"{short(r['stem'], 230)}{(' · OPTIONS ' + short(r['options'], 120)) if r['q_type'] in ('MCQ', 'AR') else ''}"
                     f" · asks: {short(r['unknown'], 70)}{fig} · lines: {skel(T, r['instance_id'])} · cand: {cand or 'none'}"
                     + (f" · now {now}" if now else "") + (f" · repeats {len(rep)}: {', '.join(rep[:4])}" if rep else ""))
        if n == len(parts) and vi:
            L += ["", "## Visually-impaired alternatives (optional: classify only when an existing code fits cleanly)"]
            for r in vi:
                L.append(f"- {r['instance_id']} · {r['q_type']} · {short(r['stem'], 160)}")
        p = os.path.join(W, f"{unit}__SHEET.md")
        open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
        write_csv(os.path.join(W, f"{unit}__TODO.csv"), ["instance_id"], [{"instance_id": r["instance_id"]} for r in part])
        written.append((unit, len(part), os.path.getsize(p)))
    for u, n_, sz in written:
        print(f"sheet {u}: {n_} rows to decide · {sz // 1024} KB (about {sz // 4000}k tokens) -> work/{u}__SHEET.md")


# ------------------------------------------------------------------------------------------------ lines
def cmd_lines(a):
    T = load()
    for iid in a.ids:
        r = T["byid"].get(iid)
        if not r:
            print(f"{iid}: no such row")
            continue
        print(f"{iid} · {r['q_type']} {r['marks_part'] or r['q_marks_printed']} · {short(r['stem'], 200)}")
        for s in T["steps"].get(iid, []):
            alt = f" | alt: {short(s['alt_accepted'], 120)}" if s["alt_accepted"] else ""
            print(f"   {s['marks']:>4} {s['step_kind']:<12} {short(s['step_text'], 160)}{alt}")
        if not T["steps"].get(iid):
            print("   (no printed lines: shuffle, no scheme, or not scored)")


# ------------------------------------------------------------------------------------------------ registry
NAME_OK = re.compile(r"^[A-Za-z0-9 ,'()\-]+$")


def reg_problems(g, reg_before):
    p = []
    c = g["code"]
    if not re.fullmatch(r"PH-(\d\d|X11)-\d{3}", c):
        p.append(f"{c}: code must read PH-<chapter 2 digits>-<serial 3 digits>")
    elif c.split("-")[1] != g["chapter"]:
        p.append(f"{c}: chapter field {g['chapter']} differs from the code")
    if g["status"] not in ("DRAFT", "VERIFIED", "ALIAS", "SPLIT"):
        p.append(f"{c}: status {g['status']}")
    if g["status"] == "ALIAS" and g["alias_of"] not in reg_before and not g["alias_of"]:
        p.append(f"{c}: ALIAS without alias_of")
    if g["status"] == "VERIFIED":
        nm = g["name"].strip()
        if not nm or len(nm.split()) > 12 or not NAME_OK.match(nm):
            p.append(f"{c}: name must be a plain phrase of 12 words or fewer, no symbols: '{nm}'")
        at = g["asks_you_to"].strip()
        if not at.startswith("Asks you to ") or len(at.split()) > 30:
            p.append(f"{c}: asks_you_to must start 'Asks you to' and have 30 words or fewer")
        for k in ("skeleton", "traps", "family", "q_type", "topic_id", "first_instance"):
            if not g.get(k, "").strip():
                p.append(f"{c}: {k} is empty")
        if g["q_type"] not in K.ENUM["q_type"]:
            p.append(f"{c}: q_type {g['q_type']}")
        if not re.match(r"^FAM-\d\d-\d\d ", g["family"] or ""):
            p.append(f"{c}: family must read 'FAM-cc-nn Name'")
    old = reg_before.get(c)
    if old:
        if old["status"] in ("ALIAS", "SPLIT") and g["status"] == "VERIFIED":
            p.append(f"{c}: a retired code ({old['status']}) is never reused")
        if old["issued_batch"] and g["issued_batch"] != old["issued_batch"]:
            p.append(f"{c}: issued_batch changed ({old['issued_batch']} -> {g['issued_batch']})")
    return p


def cmd_registry(a):
    unit = a.unit
    p = os.path.join(W, f"{unit}__REGISTRY.csv")
    if not os.path.exists(p):
        print(f"registry {unit}: no part file, nothing to apply")
        return
    hdr, new = read_csv(p)
    if hdr != K.SCHEMA["j/REGISTRY.csv"]:
        sys.exit(f"REFUSED: {os.path.basename(p)} header must be exactly: {','.join(K.SCHEMA['j/REGISTRY.csv'])}")
    rel = "j/REGISTRY.csv"
    _, rows = K.read_table(V, rel)
    before = {r["code"]: r for r in rows}
    probs = []
    dup = [c for c, n in Counter(r["code"] for r in new).items() if n > 1]
    probs += [f"{c}: twice in the part file" for c in dup]
    I = {r["instance_id"] for r in K.table(V, "l1/INSTANCES.csv")}
    for g in new:
        probs += reg_problems(g, before)
        if g["status"] == "VERIFIED" and g["first_instance"] and g["first_instance"] not in I:
            probs.append(f"{g['code']}: first_instance {g['first_instance']} is not a row")
        if g["code"] not in before:
            ch = g["code"].split("-")[1]
            top = max([int(c.split("-")[2]) for c in before if c.split("-")[1] == ch] or [0])
            if int(g["code"].split("-")[2]) <= top:
                probs.append(f"{g['code']}: a new code takes the next free serial of its chapter (above {top:03d})")
            if g["issued_batch"] != f"B{batch():02d}":
                probs.append(f"{g['code']}: issued_batch must be B{batch():02d}")
    if probs:
        print("REFUSED:")
        for x in probs[:80]:
            print("  x " + x)
        sys.exit(2)
    bak = os.path.join(W, f"{unit}__REGISTRY-BEFORE.csv")
    if not os.path.exists(bak):
        shutil.copy2(os.path.join(V, rel), bak)
    by = {r["code"]: r for r in rows}
    changed = added = 0
    for g in new:
        if g["code"] in by:
            changed += by[g["code"]] != g
            by[g["code"]].update(g)
        else:
            rows.append(g)
            by[g["code"]] = g
            added += 1
    K.write_table(V, rel, rows)
    print(f"registry {unit}: {added} new code(s), {changed} changed; j/REGISTRY.csv now {len(rows)} rows "
          f"(before-copy: work/{unit}__REGISTRY-BEFORE.csv)")


# ------------------------------------------------------------------------------------------------ expand
def next_errata_ids(n, b):
    seen = set(r["errata_id"] for r in K.table(V, "l1/ERRATA.csv", errata=False))
    for f in os.listdir(W) if os.path.isdir(W) else []:
        if f.endswith("__ERRATA.csv"):
            seen |= {r["errata_id"] for r in read_csv(os.path.join(W, f))[1]}
    pre = f"ER-B{b:02d}-"
    used = [int(x[len(pre):]) for x in seen if x.startswith(pre) and x[len(pre):].isdigit()]
    k = max(used or [0])
    return [f"{pre}{k + i:03d}" for i in range(1, n + 1)]


def decisions(unit):
    p = os.path.join(W, f"{unit}__DECISIONS.csv")
    if not os.path.exists(p):
        sys.exit(f"REFUSED: work/{unit}__DECISIONS.csv is missing")
    hdr, rows = read_csv(p)
    if hdr[: len(DEC_COLS)] != DEC_COLS:
        sys.exit("REFUSED: DECISIONS header must start " + ",".join(DEC_COLS))
    return rows


def cmd_expand(a):
    unit = a.unit
    T = load()
    members, follower = group_map()
    b = batch()
    today = dt.date.today().isoformat()
    D = decisions(unit)
    probs = []
    tp = os.path.join(W, f"{unit}__TODO.csv")
    if a.any:                       # review and split units: the decisions themselves are the list
        write_csv(tp, ["instance_id"], [{"instance_id": d["instance_id"].strip()} for d in D])
    if not os.path.exists(tp):
        sys.exit(f"REFUSED: work/{unit}__TODO.csv is missing: run `sheet` for this unit (or expand --any for a review unit)")
    todo = [r["instance_id"] for r in read_csv(tp)[1]]
    dmap = {}
    for d in D:
        iid = d["instance_id"].strip()
        if iid in dmap:
            probs.append(f"{iid}: decided twice")
        dmap[iid] = {k: d[k].strip() for k in DEC_COLS}
    probs += [f"{i}: no decision" for i in todo if i not in dmap]
    for iid, d in dmap.items():
        r = T["byid"].get(iid)
        if not r:
            probs.append(f"{iid}: not a row")
            continue
        if r.get("vi_alt") != "y" and iid not in todo:
            probs.append(f"{iid}: not on this unit's TODO list")
        g = T["reg"].get(d["code"])
        if not g:
            probs.append(f"{iid}: code {d['code']} is not in REGISTRY (apply the unit's REGISTRY part first)")
        elif g["status"] != "VERIFIED":
            probs.append(f"{iid}: code {d['code']} is {g['status']}, not VERIFIED")
        elif g["chapter"] != r["chapter"]:
            probs.append(f"{iid}: code {d['code']} is chapter {g['chapter']}, the row is chapter {r['chapter']}")
        for k, ok in (("cog_level", COG), ("competency", YN), ("difficulty", DIFF), ("confidence", CONF)):
            if d[k] not in ok:
                probs.append(f"{iid}: {k} '{d[k]}' not in {sorted(ok)}")
    if probs:
        print("REFUSED:")
        for x in probs[:80]:
            print("  x " + x)
        if len(probs) > 80:
            print(f"  ... and {len(probs) - 80} more")
        sys.exit(2)
    rv = f"P10.3/B{b:02d}-{today}"
    out, err = [], []

    def put(iid, d, src):
        g = T["reg"][d["code"]]
        row = {"instance_id": iid, "code": d["code"], "family": g["family"], "cog_level": d["cog_level"],
               "competency": d["competency"], "difficulty": d["difficulty"], "ncert_ref": "",
               "confidence": d["confidence"], "batch": str(b), "rule_version": rv}
        old = T["cls"].get(iid)
        if old is None:
            out.append(row)
        else:
            for k in ("code", "family", "cog_level", "competency", "difficulty", "confidence"):
                if (old.get(k) or "") != row[k]:
                    err.append({"file": "j/CLASSIFY.csv", "row_id": iid, "field": k, "old": old.get(k, ""),
                                "new": row[k], "reason": f"S6 pattern sorting {unit} ({src}; PHY-10)",
                                "evidence": f"work/{unit}__DECISIONS.csv; REGISTRY {row['code']}", "batch": str(b)})
    leaders = list(dmap.items())
    for iid, d in leaders:
        put(iid, d, "reader decision")
        for m in members.get(iid, []):
            put(m, d, f"repeat of {iid}")
    decided = {x["instance_id"] for x in out} | {e["row_id"] for e in err} | set(dmap) | \
              {m for i in dmap for m in members.get(i, [])}
    for r in T["I"]:
        if r["rel"] == "shuffle" and r.get("rel_to") in decided and r.get("vi_alt") != "y":
            src = dmap.get(r["rel_to"]) or dmap.get(follower.get(r["rel_to"], ""))
            if src:
                put(r["instance_id"], src, f"shuffle of {r['rel_to']}")
    ids = next_errata_ids(len(err), b)
    for e, i in zip(err, ids):
        e["errata_id"] = i
    write_csv(os.path.join(W, f"{unit}__CLASSIFY.csv"), K.SCHEMA["j/CLASSIFY.csv"], out)
    if err:
        write_csv(os.path.join(W, f"{unit}__ERRATA.csv"), K.SCHEMA["l1/ERRATA.csv"], err)
    elif os.path.exists(os.path.join(W, f"{unit}__ERRATA.csv")):
        os.remove(os.path.join(W, f"{unit}__ERRATA.csv"))
    print(f"expand {unit}: {len(dmap)} decisions -> {len(out)} new CLASSIFY rows "
          f"({sum(len(members.get(i, [])) for i in dmap)} repeats, the rest shuffles), "
          f"{len(err)} ERRATA row(s) changing earlier CLASSIFY rows")


# ------------------------------------------------------------------------------------------------ alias
def cmd_alias(a):
    """Merge: code --from becomes ALIAS of --to; every CLASSIFY row on --from is re-pointed by an ERRATA row."""
    T = load()
    x, y = T["reg"].get(a.src), T["reg"].get(a.dst)
    probs = []
    if not x or not y:
        probs.append("both codes must exist in REGISTRY")
    else:
        if x["status"] != "VERIFIED" or y["status"] != "VERIFIED":
            probs.append(f"both codes must be VERIFIED ({a.src} {x['status']}, {a.dst} {y['status']})")
        if x["chapter"] != y["chapter"] or x["q_type"] != y["q_type"]:
            probs.append("a merge keeps one chapter and one q_type; anything else is a split or a new decision")
    if len(a.reason.split()) < 4:
        probs.append("--reason must say why the granularity test passes (PHY-10 section 3)")
    if probs:
        print("REFUSED:\n  x " + "\n  x ".join(probs))
        sys.exit(2)
    b = batch()
    err = []
    for iid, c in T["cls"].items():
        if c["code"] == a.src:
            for k, new in (("code", a.dst), ("family", y["family"])):
                if c.get(k, "") != new:
                    err.append({"file": "j/CLASSIFY.csv", "row_id": iid, "field": k, "old": c.get(k, ""), "new": new,
                                "reason": f"S6 merge {a.src} -> {a.dst} (ALIAS): {a.reason}",
                                "evidence": f"REGISTRY {a.src} alias_of {a.dst}; phy_s6.py review", "batch": str(b)})
    ep = os.path.join(W, f"{a.unit}__ERRATA.csv")
    have = read_csv(ep)[1] if os.path.exists(ep) else []
    for e, i in zip(err, next_errata_ids(len(err), b)):
        e["errata_id"] = i
    write_csv(ep, K.SCHEMA["l1/ERRATA.csv"], have + err)
    rel = "j/REGISTRY.csv"
    _, rows = K.read_table(V, rel)
    bak = os.path.join(W, f"{a.unit}__REGISTRY-BEFORE.csv")
    if not os.path.exists(bak):
        shutil.copy2(os.path.join(V, rel), bak)
    for r in rows:
        if r["code"] == a.src:
            r["status"], r["alias_of"] = "ALIAS", a.dst
            r["note"] = (r["note"] + "; " if r["note"] else "") + f"merged into {a.dst} at B{b:02d}: {a.reason}"
    K.write_table(V, rel, rows)
    if not os.path.exists(os.path.join(W, f"{a.unit}__CLASSIFY.csv")):
        write_csv(os.path.join(W, f"{a.unit}__CLASSIFY.csv"), K.SCHEMA["j/CLASSIFY.csv"], [])
    print(f"alias {a.src} -> {a.dst}: {len(err)} ERRATA row(s) into work/{a.unit}__ERRATA.csv; REGISTRY {a.src} is ALIAS")


# ------------------------------------------------------------------------------------------------ check
def cmd_check(a):
    unit = a.unit
    T = load()
    fails, notes = [], []
    pc = os.path.join(W, f"{unit}__CLASSIFY.csv")
    if not os.path.exists(pc):
        sys.exit(f"REFUSED: work/{unit}__CLASSIFY.csv is missing: run expand first")
    hdr, C = read_csv(pc)
    if hdr != K.SCHEMA["j/CLASSIFY.csv"]:
        fails.append("CLASSIFY part header differs from the schema")
    have = set(T["cls"]) | {r["instance_id"] for r in C}
    clash = [r["instance_id"] for r in C if r["instance_id"] in T["cls"]]
    if clash:
        fails.append(f"{len(clash)} CLASSIFY id(s) already in the vault (they need ERRATA): {clash[:3]}")
    todo = [r["instance_id"] for r in read_csv(os.path.join(W, f"{unit}__TODO.csv"))[1]]
    members, _ = group_map()
    want = set(todo) | {m for i in todo for m in members.get(i, [])}
    want |= {r["instance_id"] for r in T["I"] if r["rel"] == "shuffle" and r.get("rel_to") in want and needs_row(r)}
    miss = sorted(want - have)
    if miss:
        fails.append(f"{len(miss)} row(s) of this unit still without a CLASSIFY row: {miss[:5]}")
    b = str(batch())
    for r in C:
        g = T["reg"].get(r["code"])
        if not g or g["status"] != "VERIFIED":
            fails.append(f"{r['instance_id']}: code {r['code']} not VERIFIED in REGISTRY")
        if r["batch"] != b:
            fails.append(f"{r['instance_id']}: batch {r['batch']} (session batch {b})")
        src = T["byid"].get(r["instance_id"])
        if src and g and chap_of(T, src) != g["chapter"]:
            fails.append(f"{r['instance_id']}: chapter {chap_of(T, src)} against code {r['code']}")
    used = {r["code"] for r in C} | {c["code"] for c in T["cls"].values()}
    before = {}
    bp = os.path.join(W, f"{unit}__REGISTRY-BEFORE.csv")
    if os.path.exists(bp):
        before = {r["code"]: r for r in read_csv(bp)[1]}
    for code in sorted(used):
        g = T["reg"].get(code)
        if g:
            for x in reg_problems(g, before or {}):
                if "issued_batch changed" not in x:
                    fails.append(x)
    shuf_bad = 0
    allc = dict(T["cls"])
    allc.update({r["instance_id"]: r for r in C})
    for r in T["I"]:
        if r["rel"] == "shuffle" and r["instance_id"] in allc and r.get("rel_to") in allc:
            if allc[r["instance_id"]]["code"] != allc[r["rel_to"]]["code"]:
                shuf_bad += 1
    if shuf_bad:
        fails.append(f"{shuf_bad} shuffle(s) carry a code different from their origin's")
    cnt = Counter(r["code"] for r in C if T["byid"].get(r["instance_id"], {}).get("rel") == "origin")
    notes.append(f"codes used by this unit's origin rows: {len(cnt)}; used once: {sum(1 for v in cnt.values() if v == 1)}")
    for x in fails[:60]:
        print("  x " + x)
    print(("CHECK FAIL" if fails else "CHECK PASS") + f" {unit}: {len(C)} CLASSIFY rows · " + "; ".join(notes))
    sys.exit(2 if fails else 0)


# ------------------------------------------------------------------------------------------------ review
def cmd_review(a):
    T = load()
    use = defaultdict(list)
    for iid, c in T["cls"].items():
        r = T["byid"].get(iid)
        if r and r["rel"] == "origin":
            use[c["code"]].append(r)
    L = ["# S6 granularity review · " + dt.date.today().isoformat(), ""]
    for cc in sorted({g["chapter"] for g in T["reg"].values()}):
        if a.chapter and cc != a.chapter.zfill(2):
            continue
        codes = [c for c, g in T["reg"].items() if g["chapter"] == cc and g["status"] == "VERIFIED"]
        once = [c for c in codes if len(use[c]) == 1]
        L.append(f"## Chapter {cc}: {len(codes)} codes, {sum(len(use[c]) for c in codes)} origin rows, used once {len(once)}")
        for c in sorted(once):
            r = use[c][0]
            L.append(f"- once: {c} {T['reg'][c]['q_type']} · {T['reg'][c]['name']} · {r['instance_id']}")
        for i, x in enumerate(sorted(codes)):
            for y in sorted(codes)[i + 1:]:
                gx, gy = T["reg"][x], T["reg"][y]
                tx, ty = toks(gx["name"]), toks(gy["name"])
                if gx["q_type"] == gy["q_type"] and tx and len(tx & ty) / len(tx | ty) >= 0.5:
                    L.append(f"- look-alike: {x} '{gx['name']}' · {y} '{gy['name']}' ({len(use[x])} and {len(use[y])} uses)")
        L.append("")
    p = os.path.join(W, "S6-REVIEW.md")
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"review -> work/S6-REVIEW.md ({len(L)} lines)")


# ------------------------------------------------------------------------------------------------ misses
def cmd_misses(a):
    T = load()
    by_year = defaultdict(set)
    for iid, c in T["cls"].items():
        r = T["byid"].get(iid)
        if r and r["exam"] in ("MAIN", "T2") and r["rel"] in ("origin",) and r.get("vi_alt") != "y":
            by_year[r["year"]].add(c["code"])
    years = sorted(by_year)
    out = ["# S6 prediction and misses (leave one year out, main exam) · " + dt.date.today().isoformat(),
           "Predicted for a year = codes asked in the main papers of at least two of the other years. "
           "Uncalibrated: no probability is shown (CI§12).", ""]
    for y in years:
        others = [by_year[o] for o in years if o != y]
        cnt = Counter(c for s in others for c in s)
        pred = {c for c, n in cnt.items() if n >= 2}
        seen = set().union(*others) if others else set()
        act = by_year[y]
        out += [f"## {y}", f"- predicted {len(pred)}; asked {len(act)}; predicted and asked {len(pred & act)}",
                f"- predicted but absent ({len(pred - act)}): " + ", ".join(sorted(pred - act)),
                f"- asked and never seen in another year ({len(act - seen)}): " + ", ".join(sorted(act - seen)), ""]
    p = os.path.join(W, "S6-MISSES.md")
    open(p, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"misses -> work/S6-MISSES.md ({len(years)} years)")
    if a.write_notes:
        for y in years:
            np_ = os.path.join(V, "notes", f"Y{y}.md")
            blk = "\n".join(out[out.index(f"## {y}"): out.index(f"## {y}") + 4])
            with open(np_, "a", encoding="utf-8") as f:
                f.write(f"\n### S6 prediction and misses (phy_s6.py {EDITION}, {dt.date.today()})\n" + blk.split("\n", 1)[1] + "\n")
        print("appended to notes/Y<year>.md for " + ", ".join(years))


# ------------------------------------------------------------------------------------------------ coverage
def cmd_coverage(a):
    T = load()
    c = Counter()
    m = Counter()
    for r in T["I"]:
        if needs_row(r):
            c[r["year"]] += 1
            m[r["year"]] += r["instance_id"] not in T["cls"]
    for y in sorted(c):
        print(f"  {y}: {c[y]} rows, {c[y] - m[y]} classified, {m[y]} to go")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("status").set_defaults(fn=cmd_status)
    sp.add_parser("groups").set_defaults(fn=cmd_groups)
    s = sp.add_parser("sheet")
    s.add_argument("--chapter", required=True)
    s.add_argument("--max", type=int, default=380)
    s.set_defaults(fn=cmd_sheet)
    s = sp.add_parser("lines")
    s.add_argument("ids", nargs="+")
    s.set_defaults(fn=cmd_lines)
    for name, fn in (("registry", cmd_registry), ("expand", cmd_expand), ("check", cmd_check)):
        s = sp.add_parser(name)
        s.add_argument("--unit", required=True)
        if name == "expand":
            s.add_argument("--any", action="store_true", help="review or split unit: no sheet TODO list")
        s.set_defaults(fn=fn)
    s = sp.add_parser("alias")
    s.add_argument("--unit", required=True)
    s.add_argument("--from", dest="src", required=True)
    s.add_argument("--to", dest="dst", required=True)
    s.add_argument("--reason", required=True)
    s.set_defaults(fn=cmd_alias)
    s = sp.add_parser("review")
    s.add_argument("--chapter")
    s.set_defaults(fn=cmd_review)
    s = sp.add_parser("misses")
    s.add_argument("--write-notes", action="store_true")
    s.set_defaults(fn=cmd_misses)
    sp.add_parser("coverage").set_defaults(fn=cmd_coverage)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
