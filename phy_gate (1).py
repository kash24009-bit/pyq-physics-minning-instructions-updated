#!/usr/bin/env python3
"""phy_gate.py - the only door into the vault on the Claude Code route (PYQ Pattern Mining - Physics 042).

Nothing reaches the vault except through `commit` or `checkpoint`, and `commit` refuses unless every check passes.
Paths come from /home/claude/phy_env.json (written by phy_code_env.py). Part files live in /home/claude/vault/work/
as <unit>__<TABLE>.csv (unit = a paper_id such as 2026-5532, or a label such as S1B or FIX-1).

  check <unit> --stage S3|S4|S5|OTHER     schema, ids, batch, coverage; trial merge + check-paper + validate
  skeleton <unit> --stage S3|S4|S5        write the blind checker's input and SEAL the part files away
  unseal <unit>                           bring sealed part files back (verify and commit do this themselves)
  verify <unit> --stage S3|S4|S5          part files vs <unit>__VERIFY.csv (+ __ADJUDICATE.csv) -> __DIFF.csv
  commit <unit> --stage S3|S4|S5|OTHER [--progress "<text in the line>" | --progress-new "<new line>" |
                --no-progress] [--unverified "<reason>"] [--no-push]     (S5 must name its line or say --no-progress)
                                          check + verify + merge + status erratum + PROGRESS + validate + pack + push
  checkpoint --message "<what>" [--progress-new "<new line>" | --tick "<text in an open line>"] [--no-push]
                                          validate + pack + push (no part files)
  push                                    retry the git push of the project repository
  show                                    what is waiting in vault/work
Every commit and checkpoint also rewrites <outputs>/README.md (the dashboard) and prints its link.

Exit codes: 0 ok | 1 mismatches not settled | 2 refused (fix and rerun) | 3 merge failed, vault rolled back |
            4 committed but the push failed (run `push`)
"""
import argparse
import csv
import datetime as dt
import glob
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict

csv.field_size_limit(10 ** 8)
ENV_JSON = os.environ.get("PHY_ENV", "/home/claude/phy_env.json")
MERGE_ORDER = ["BLUEPRINTS", "CONSTANTS", "CASES", "INSTANCES", "FIGURES", "FORMULAE", "STEP-AWARDS", "UNREADABLE",
               "CLASSIFY", "ERRATA"]
SEALABLE = ["BLUEPRINTS", "CONSTANTS", "CASES", "INSTANCES", "FIGURES", "FORMULAE", "STEP-AWARDS"]
READ_FROM = {"image", "bundle-image", "photo", "hi-translation"}
DECISIONS = {"extractor_right", "part_fixed", "unreadable_logged", "part_added", "not_a_part"}
PID_TOKEN = re.compile(r"(?<![\w-])(?:SQP\d{4}-\d{3}|T[12]-\d{4}-[0-9A-Z]{3,}|\d{4}C?-[0-9A-Z]{3,}|UNK-X[0-9a-f]{6})(?!\w)")
VERIFY_COLS = {"S3": "instance_id,marks_part,q_marks_printed,numbers,options,figure_values,note",
               "S4": "instance_id,marks_part,q_marks_printed,numbers,options,figure_values,note",
               "S5": "instance_id,step_marks,key,numbers,note"}
ADJ_COLS = "instance_id,field,decision,final_value,crop,note"


# ------------------------------------------------------------------------------------------------ basics
def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def die(code, msg):
    print(msg)
    sys.exit(code)


def refuse(probs):
    print("REFUSED:")
    for p in probs[:60]:
        print("  x " + p)
    if len(probs) > 60:
        print(f"  ... and {len(probs) - 60} more")
    sys.exit(2)


def run(cmd, timeout=900):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except (OSError, subprocess.TimeoutExpired) as e:
        return 99, "", str(e)


def env():
    if not os.path.exists(ENV_JSON):
        die(2, f"REFUSED: {ENV_JSON} is missing. Run phy_code_env.py first (CLAUDE.md section 6).")
    E = json.load(open(ENV_JSON, encoding="utf-8"))
    E["nn"] = int(E["session_batch"])
    E["py"] = sys.executable
    return E


_K = None


def kit(E):
    global _K
    if _K is None:
        spec = importlib.util.spec_from_file_location("pyqkit_for_gate", E["kit"])
        _K = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_K)
    return _K


def work(E):
    return os.path.join(E["vault"], "work")


def part_path(E, unit, t):
    return os.path.join(work(E), f"{unit}__{t}.csv")


def parts(E, unit):
    return [(t, part_path(E, unit, t)) for t in MERGE_ORDER if os.path.exists(part_path(E, unit, t))]


def read_csv(p):
    with open(p, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        rows = [dict(r) for r in rd]
        return list(rd.fieldnames or []), rows


def write_csv(p, header, rows):
    tmp = p + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in header})
    os.replace(tmp, p)


# ------------------------------------------------------------------------------------------------ reading values
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")


def canon(s):
    s = str(s or "")
    for x, y in (("−", "-"), ("–", "-"), ("—", "-"), ("×", "*"), ("·", "*"), ("⋅", "*"), ("½", " 0.5 "),
                 ("¼", " 0.25 "), ("¾", " 0.75 "), ("°", " deg ")):
        s = s.replace(x, y)
    return re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+", lambda m: "^" + m.group(0).translate(SUP), s)


def nums(text):
    """The set of numeric values in a text, one canonical form per value (3e8 == 3 x 10^8 == 3 × 10⁸).
    Subscript labels (r_1, B_{12}), digits glued to names (eps0, R1) and exponents of units (m^2, s^-1) are not values."""
    s = canon(text)
    s = re.sub(r"_\{[^}]*\}|_[A-Za-z0-9]+", " ", s)
    out = set()

    def take(x):
        try:
            out.add("%.6g" % x)
        except (OverflowError, ValueError):
            pass
        return " "

    s = re.sub(r"(-?\d+(?:\.\d+)?)\s*[*xX]\s*10\s*\^\s*\(?\s*([+-]?\d+)\s*\)?",
               lambda m: take(float(m.group(1)) * 10.0 ** int(m.group(2))), s)
    s = re.sub(r"(?<![\d.])10\s*\^\s*\(?\s*([+-]?\d+)\s*\)?", lambda m: take(10.0 ** int(m.group(1))), s)
    s = re.sub(r"(?<![\w.])(-?\d+(?:\.\d+)?)[eE]([+-]?\d+)(?![\w.])",
               lambda m: take(float(m.group(1)) * 10.0 ** int(m.group(2))), s)
    s = re.sub(r"(?<=[A-Za-z)\]])\s*\^\s*\(?\s*[+-]?\d+(?:\.\d+)?\s*\)?", " ", s)
    s = re.sub(r"(?<=[A-Za-z])\d+(?:\.\d+)?", " ", s)
    for m in re.finditer(r"(?<![\w.])(-)?(\d+(?:\.\d+)?)", s):
        take(float(m.group(2)) * (-1 if m.group(1) else 1))
    return out


def compact(s):
    s = canon(s).lower().replace("**", "^")
    return re.sub(r"\s+|[{}]", "", s).rstrip(".")


def opts(s):
    items = [x.strip() for x in re.split(r"\s*\|\s*", str(s or "")) if x.strip()]
    return [re.sub(r"^\(?\s*[a-dA-D]\s*[).:]\s*", "", x) for x in items]


def frac(x):
    s = canon(x).strip()
    toks = re.findall(r"-?\d+(?:\.\d+)?(?:/\d+(?:\.\d+)?)?", s)
    if not toks:
        return None
    tot = 0.0
    for t in toks:
        if "/" in t:
            a, b = t.split("/")
            tot += float(a) / float(b) if float(b) else 0.0
        else:
            tot += float(t)
    return tot


def same_mark(a, b):
    fa, fb = frac(a), frac(b)
    if fa is None or fb is None:
        return fa is None and fb is None
    return abs(fa - fb) < 1e-9


def bar(s):
    return [x.strip() for x in re.split(r"\s*\|\s*", str(s or "")) if x.strip()]


def key_letter(s):
    m = re.search(r"(?<![A-Za-z])\(?([A-Da-d])\)?(?![A-Za-z])", str(s or ""))
    return m.group(1).upper() if m else ""


def fmt_mark(x):
    return "?" if x is None else ("%g" % x)


# ------------------------------------------------------------------------------------------------ lint
def lint(E, unit, stage):
    K = kit(E)
    v = E["vault"]
    b = str(E["nn"])
    probs, info, data = [], [], {}
    ps = parts(E, unit)
    if not ps:
        return [f"no part files named {unit}__<TABLE>.csv in {work(E)}"], info, data
    for t, p in ps:
        rel = K.resolve_table(t)
        hdr, rows = read_csv(p)
        if hdr != K.SCHEMA[rel]:
            probs.append(f"{t}: the header is not the kit schema. Expected: {','.join(K.SCHEMA[rel])}")
            continue
        data[t] = rows
        info.append(f"{t} {len(rows)}")
        idc = K.ID_COL.get(rel)
        if "batch" in hdr:
            bad = [(r.get(idc) if idc else r.get("paper_id", "?")) for r in rows if str(r.get("batch", "")).strip() != b]
            if bad:
                probs.append(f"{t}: batch must be {b} on every row (e.g. {bad[:3]})")
        if idc:
            ids = [str(r.get(idc, "")).strip() for r in rows]
            if any(not i for i in ids):
                probs.append(f"{t}: {sum(1 for i in ids if not i)} row(s) without an id")
            dup = [i for i, n in Counter(ids).items() if n > 1 and i]
            if dup:
                probs.append(f"{t}: ids repeated inside the part file: {dup[:4]}")
            if rel != "l1/BLUEPRINTS.csv":
                have = {r[idc] for r in K.table(v, rel, errata=False)}
                clash = [i for i in ids if i in have]
                if clash:
                    probs.append(f"{t}: {len(clash)} id(s) already in the vault, e.g. {clash[:3]} "
                                 f"(a correction is an ERRATA row, never a second row)")
            dots = [i for i in ids if "." in i]
            if dots:
                probs.append(f"{t}: ids must not contain dots: {dots[:3]}")
    inst = data.get("INSTANCES", [])
    vinst = K.table(v, "l1/INSTANCES.csv")
    all_ids = {r["instance_id"] for r in vinst} | {r["instance_id"] for r in inst}
    if stage in ("S3", "S4"):
        if not inst:
            probs.append("stage S3/S4 needs an INSTANCES part file")
        figs = {r["instance_id"] for r in K.table(v, "l1/FIGURES.csv")} | {r["instance_id"] for r in data.get("FIGURES", [])}
        frms = {r["instance_id"] for r in K.table(v, "l1/FORMULAE.csv")} | {r["instance_id"] for r in data.get("FORMULAE", [])}
        cases = {r["case_id"] for r in K.table(v, "l1/CASES.csv")} | {r["case_id"] for r in data.get("CASES", [])}
        for r in inst:
            i = r["instance_id"]
            if r["paper_id"] != unit:
                probs.append(f"{i}: paper_id is {r['paper_id']}, not {unit}")
            if not i.startswith(unit + "-Q"):
                probs.append(f"{i}: an instance_id starts with {unit}-Q")
            if r["read_from"] not in READ_FROM:
                probs.append(f"{i}: read_from '{r['read_from']}' (image, bundle-image, photo or hi-translation)")
            if not str(r["source_page"]).strip().isdigit():
                probs.append(f"{i}: source_page '{r['source_page']}'")
            if r["has_figure"] == "y" and i not in figs:
                probs.append(f"{i}: has_figure=y but no FIGURES row")
            if r["q_type"] in ("NUM", "DRV") and i not in frms:
                probs.append(f"{i}: a {r['q_type']} row needs a FORMULAE row")
            if r["case_id"] and r["case_id"] not in cases:
                probs.append(f"{i}: case {r['case_id']} has no CASES row")
            if r["rel"] in ("shuffle", "variant", "repeat") and r["rel_to"] not in all_ids:
                probs.append(f"{i}: rel_to {r['rel_to'] or '(blank)'} is not a known instance")
            if r["q_type"] == "MCQ" and not str(r["options"]).strip():
                probs.append(f"{i}: an MCQ row needs its options")
        if unit not in {r["paper_id"] for r in K.table(v, "l1/BLUEPRINTS.csv")} and not data.get("BLUEPRINTS"):
            probs.append(f"no BLUEPRINTS row for {unit}: write it from this paper's own instructions page (S2b)")
    for t in ("FIGURES", "FORMULAE"):
        idc = K.ID_COL[K.resolve_table(t)]
        for r in data.get(t, []):
            if r.get("from_image") != "y":
                probs.append(f"{t} {r[idc]}: from_image must be y")
            if r["instance_id"] not in all_ids:
                probs.append(f"{t} {r[idc]}: unknown instance {r['instance_id']}")
    if stage != "OTHER":
        for t in ("BLUEPRINTS", "CONSTANTS", "CASES", "UNREADABLE"):
            wrong = sorted({r["paper_id"] for r in data.get(t, []) if r["paper_id"] != unit})
            if wrong:
                probs.append(f"{t}: rows for {wrong}, but this unit is {unit}")
    if data.get("BLUEPRINTS"):
        if len(data["BLUEPRINTS"]) > 1:
            probs.append("BLUEPRINTS: more than one row")
        again = sorted({r["paper_id"] for r in data["BLUEPRINTS"]} & {r["paper_id"] for r in K.table(v, "l1/BLUEPRINTS.csv")})
        if again:
            probs.append(f"BLUEPRINTS for {again} already in the vault")
    if data.get("CONSTANTS"):
        again = sorted({r["paper_id"] for r in data["CONSTANTS"]} & {r["paper_id"] for r in K.table(v, "l1/CONSTANTS.csv")})
        if again:
            probs.append(f"CONSTANTS for {again} are already in the vault (saved at S2a): delete the CONSTANTS part file")
    steps = data.get("STEP-AWARDS", [])
    printed = {x["award_id"]: x for x in K.table(v, "l1/STEP-AWARDS.csv")}
    printed.update({x["award_id"]: x for x in steps})
    for s in steps:
        if s["provenance"].startswith("TRANSFERRED:"):
            src = printed.get(s["provenance"].split(":", 1)[1].strip())
            if not src or src["provenance"] != "PRINTED":
                probs.append(f"{s['award_id']}: {s['provenance']} does not name a PRINTED scoring line in the vault")
        if s["instance_id"] not in all_ids:
            probs.append(f"{s['award_id']}: unknown instance {s['instance_id']}")
        pv = s["provenance"]
        if not (pv in ("PRINTED", "INFERRED") or pv.startswith("TRANSFERRED:")):
            probs.append(f"{s['award_id']}: provenance '{pv}'")
    if stage == "S5":
        if not steps:
            probs.append("stage S5 needs a STEP-AWARDS part file")
        wrong = sorted({s["paper_id"] for s in steps if s["paper_id"] != unit})
        if wrong:
            probs.append(f"STEP-AWARDS rows for {wrong}, but this unit is {unit}")
    return probs, info, data


def validate_delta(K, before, after, unit, res):
    b, _ = K.validate(before)
    a, quar = K.validate(after)
    bm = {c: r for c, n, r, d in b}
    probs = [f"{c} {n}: {d}" for c, n, r, d in a if r == "FAIL" and bm.get(c) == "PASS"]
    if unit in quar and not probs:
        probs.append(f"{unit} would be quarantined")
    res["validate"] = f"{sum(1 for x in a if x[2] == 'PASS')}/{len(a)} checks pass"
    old = [c for c, n, r, d in b if r == "FAIL"]
    if old:
        res["validate"] += f" (already failing before: {', '.join(old)})"
    return probs


def trial(E, unit, stage):
    K = kit(E)
    v = E["vault"]
    tmp = tempfile.mkdtemp(prefix="phygate-")
    try:
        sv = os.path.join(tmp, "vault")
        shutil.copytree(v, sv, ignore=shutil.ignore_patterns("work"))
        os.makedirs(os.path.join(sv, "work"), exist_ok=True)
        for t, p in parts(E, unit):
            rc, o, e = run([E["py"], E["kit"], "merge", sv, p, "--table", t])
            if rc != 0:
                return [f"trial merge of {t} refused: {(o + e).strip()[-300:]}"], {}
        res = {}
        if stage in ("S3", "S4"):
            rc, o, e = run([E["py"], E["kit"], "check-paper", sv, unit])
            res["check"] = (o.strip().splitlines() or [e.strip()])[0]
            if rc != 0:
                return ["check-paper on the trial merge: " + " / ".join(o.strip().splitlines())], res
        return validate_delta(K, v, sv, unit, res), res
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------------------------------------------ seal / skeleton
def sealed_dir(E, unit):
    return os.path.join(E["home"], ".sealed", unit)


def seal(E, unit):
    d = sealed_dir(E, unit)
    os.makedirs(d, exist_ok=True)
    n = 0
    for t in SEALABLE:
        p = part_path(E, unit, t)
        if os.path.exists(p):
            shutil.move(p, os.path.join(d, os.path.basename(p)))
            n += 1
    return n


def unseal(E, unit):
    d = sealed_dir(E, unit)
    if not os.path.isdir(d):
        return 0
    n = 0
    for f in sorted(os.listdir(d)):
        dst = os.path.join(work(E), f)
        if os.path.exists(dst):
            die(2, f"REFUSED: {dst} exists and a sealed copy waits in {d}. Keep one of the two, then rerun.")
        shutil.move(os.path.join(d, f), dst)
        n += 1
    os.rmdir(d)
    return n


def cmd_skeleton(a):
    E = env()
    unit, stage = a.unit, a.stage
    unseal(E, unit)
    if stage in ("S3", "S4"):
        p = part_path(E, unit, "INSTANCES")
        if not os.path.exists(p):
            die(2, f"REFUSED: {p} is missing; the extractor writes it first")
        rows = read_csv(p)[1]
        cols = ["instance_id", "q_no", "side", "part", "section", "q_type", "has_figure", "case_id", "vi_alt", "file_id",
                "source_page"]
        out = [{c: r.get(c, "") for c in cols} for r in rows]
    else:
        p = part_path(E, unit, "STEP-AWARDS")
        if not os.path.exists(p):
            die(2, f"REFUSED: {p} is missing; the scheme reader writes it first")
        steps = read_csv(p)[1]
        vi = {r["instance_id"]: r for r in kit(E).table(E["vault"], "l1/INSTANCES.csv")}
        by = defaultdict(list)
        for s in steps:
            by[s["instance_id"]].append(s)
        cols = ["instance_id", "q_no", "side", "part", "scheme_file_id", "scheme_pages"]
        out = []
        for iid, ss in by.items():
            r = vi.get(iid, {})
            pages = sorted({int(s["source_page"]) for s in ss if str(s["source_page"]).strip().isdigit()})
            out.append({"instance_id": iid, "q_no": r.get("q_no", ""), "side": r.get("side", ""), "part": r.get("part", ""),
                        "scheme_file_id": ss[0].get("file_id", ""), "scheme_pages": " ".join(map(str, pages))})
    sp = os.path.join(work(E), f"{unit}__SKELETON.csv")
    write_csv(sp, cols, out)
    n = seal(E, unit)
    print(f"skeleton: {sp} | {len(out)} rows | {n} part file(s) sealed away until verify")
    print(f"the blind checker writes {os.path.join(work(E), unit + '__VERIFY.csv')} with columns: {VERIFY_COLS[stage]}")


def cmd_unseal(a):
    E = env()
    print(f"unsealed {unseal(E, a.unit)} file(s)")


# ------------------------------------------------------------------------------------------------ verify
def settled(E, unit, x, adj):
    if not adj:
        return False, ""
    dec = str(adj.get("decision", "")).strip()
    crop = str(adj.get("crop", "")).strip()
    if dec not in DECISIONS:
        return False, f"unknown decision '{dec}'"
    if not crop or not os.path.exists(crop):
        return False, "the crop file named in ADJUDICATE does not exist"
    if x["field"] == "missing-part":
        if dec == "not_a_part":
            return True, dec
        if dec == "part_added":
            ip = part_path(E, unit, "INSTANCES")
            ids = {r["instance_id"] for r in read_csv(ip)[1]} if os.path.exists(ip) else set()
            fv = str(adj.get("final_value", "")).strip()
            return (True, dec) if fv in ids else (False, f"final_value '{fv}' is not in the INSTANCES part file")
        return False, f"{dec} cannot settle a missing part"
    if dec == "extractor_right":
        return True, dec
    if dec == "unreadable_logged":
        up = part_path(E, unit, "UNREADABLE")
        ok = os.path.exists(up) and len(read_csv(up)[1]) > 0
        return (True, dec) if ok else (False, "no UNREADABLE part row")
    return False, f"{dec}: the mismatch is still there; fix the part file or choose another decision"


def verify(E, unit, stage):
    w = work(E)
    res = {"values": 0, "diffs": 0, "rows": 0, "unresolved": [], "adj": [], "note": ""}
    vp = os.path.join(w, f"{unit}__VERIFY.csv")
    if not os.path.exists(vp):
        res["unresolved"] = [{"instance_id": unit, "field": "file", "part_value": "", "check_value": "",
                              "detail": f"{os.path.basename(vp)} is missing: run the blind checker first (PHY-07 section 7)",
                              "resolved": "no"}]
        return res
    vrows = read_csv(vp)[1]
    adj = {}
    ap = os.path.join(w, f"{unit}__ADJUDICATE.csv")
    if os.path.exists(ap):
        for r in read_csv(ap)[1]:
            adj[(str(r.get("instance_id", "")).strip(), str(r.get("field", "")).strip())] = r
    res["adj"] = list(adj.values())
    diffs = []

    def d(i, f, pv, cv, det):
        diffs.append({"instance_id": i, "field": f, "part_value": pv, "check_value": cv, "detail": det})

    by = {}
    for r in vrows:
        if str(r.get("note", "")).strip().upper().startswith("MISSING"):
            d(str(r.get("instance_id", "")).strip(), "missing-part", "", r.get("note", ""),
              "the checker saw a printed part that the part file lacks")
        else:
            by[str(r.get("instance_id", "")).strip()] = r
    if stage in ("S3", "S4"):
        ip, fp = part_path(E, unit, "INSTANCES"), part_path(E, unit, "FIGURES")
        inst = read_csv(ip)[1] if os.path.exists(ip) else []
        fb = defaultdict(list)
        for f in (read_csv(fp)[1] if os.path.exists(fp) else []):
            fb[f["instance_id"]].append(f)
        res["rows"] = len(inst)
        for r in inst:
            i = r["instance_id"]
            c = by.get(i)
            if c is None:
                d(i, "row", "", "", "the checker wrote no row for this part")
                continue
            for fld in ("marks_part", "q_marks_printed"):
                res["values"] += 1
                if not same_mark(r.get(fld), c.get(fld)):
                    d(i, fld, r.get(fld, ""), c.get(fld, ""), "marks differ")
            V, Es = nums(c.get("numbers")), nums(r.get("stem"))
            Eall = Es | nums(r.get("givens"))
            res["values"] += len(V | Es)
            a1, a2 = sorted(V - Eall), sorted(Es - V)
            if a1 or a2:
                d(i, "numbers", " ".join(sorted(Eall)), " ".join(sorted(V)),
                  f"only in the checker's reading: {a1 or '-'}; only in the part file: {a2 or '-'}")
            eo, co = opts(r.get("options")), opts(c.get("options"))
            if eo or co:
                n = max(len(eo), len(co))
                res["values"] += n
                bad = [k for k in range(n) if k >= len(eo) or k >= len(co) or compact(eo[k]) != compact(co[k])]
                if bad:
                    d(i, "options", r.get("options", ""), c.get("options", ""),
                      "options differ at " + ", ".join("ABCDEFGH"[k] if k < 8 else str(k + 1) for k in bad))
            fv = str(c.get("figure_values", "") or "").strip()
            if fv and not fv.lower().startswith("same as"):
                Ea, Ev = set(), set()
                for f in fb.get(i, []):
                    Ea |= nums(f.get("values", "") + " " + f.get("description", ""))
                    Ev |= nums(f.get("values", ""))
                Vf = nums(fv)
                res["values"] += len(Vf | Ev)
                b1, b2 = sorted(Vf - Ea), sorted(Ev - Vf)
                if b1 or b2:
                    d(i, "figure_values", " ".join(sorted(Ea)), " ".join(sorted(Vf)),
                      f"only in the checker's reading: {b1 or '-'}; only in the part file: {b2 or '-'}")
    else:
        sp, fp = part_path(E, unit, "STEP-AWARDS"), part_path(E, unit, "FORMULAE")
        steps = read_csv(sp)[1] if os.path.exists(sp) else []
        frm = read_csv(fp)[1] if os.path.exists(fp) else []
        bi = defaultdict(list)
        for s in steps:
            bi[s["instance_id"]].append(s)
        res["rows"] = len(bi)
        for i, ss in bi.items():
            ss.sort(key=lambda s: int(s["step_no"]) if str(s["step_no"]).strip().isdigit() else 0)
            c = by.get(i)
            if c is None:
                d(i, "row", "", "", "the checker wrote no row for this part")
                continue
            em, cm = [frac(s["marks"]) for s in ss], [frac(x) for x in bar(c.get("step_marks"))]
            res["values"] += max(len(em), len(cm))
            if len(em) != len(cm) or any(x is None or y is None or abs(x - y) > 1e-9 for x, y in zip(em, cm)):
                d(i, "step_marks", " | ".join(fmt_mark(x) for x in em), " | ".join(fmt_mark(x) for x in cm),
                  "scoring-line marks differ")
            ek = next((key_letter(s["step_text"]) for s in ss if s["step_kind"] == "key"), "")
            ck = key_letter(c.get("key", ""))
            if ek or ck:
                res["values"] += 1
                if ek != ck:
                    d(i, "key", ek, ck, "answer keys differ")
            V = nums(c.get("numbers"))
            Eall = nums(" ".join(s["step_text"] for s in ss)) | nums(" ".join(f["formula"] for f in frm if f["instance_id"] == i))
            res["values"] += len(V)
            if V - Eall:
                d(i, "numbers", " ".join(sorted(Eall)), " ".join(sorted(V)),
                  f"results the checker read that are in no scoring line: {sorted(V - Eall)}")
    for x in diffs:
        ok, why = settled(E, unit, x, adj.get((x["instance_id"], x["field"])))
        x["resolved"] = why if ok else ("no" + (f" ({why})" if why else ""))
        if not ok:
            res["unresolved"].append(x)
    write_csv(os.path.join(w, f"{unit}__DIFF.csv"), ["instance_id", "field", "part_value", "check_value", "detail", "resolved"], diffs)
    res["diffs"] = len(diffs)
    return res


def report_verify(r):
    print(f"double-read: {r.get('rows', 0)} rows | {r['values']} values compared | {r['diffs']} mismatch(es) | "
          f"{len(r['unresolved'])} not settled")
    for x in r["unresolved"][:40]:
        print(f"  x {x['instance_id']} | {x['field']} | part: {str(x['part_value'])[:70]} | checker: "
              f"{str(x['check_value'])[:70]} | {str(x['detail'])[:110]} | {x.get('resolved', '')}")


def cmd_verify(a):
    E = env()
    unseal(E, a.unit)
    r = verify(E, a.unit, a.stage)
    report_verify(r)
    print(f"details: {os.path.join(work(E), a.unit + '__DIFF.csv')}  |  decisions go in {a.unit}__ADJUDICATE.csv "
          f"with columns {ADJ_COLS}")
    sys.exit(0 if not r["unresolved"] else 1)


def cmd_check(a):
    E = env()
    unseal(E, a.unit)
    probs, info, _ = lint(E, a.unit, a.stage)
    if probs:
        refuse(probs)
    tprobs, res = trial(E, a.unit, a.stage)
    if tprobs:
        refuse(tprobs)
    print(f"CHECK PASS | {a.unit} | {', '.join(info)} | {res.get('check', 'no check-paper at this stage')} | "
          f"validate {res.get('validate', '')}")


# ------------------------------------------------------------------------------------------------ vault writes
def next_errata_id(E):
    mx = 0
    for r in kit(E).table(E["vault"], "l1/ERRATA.csv", errata=False):
        m = re.match(rf"^ER-B{E['nn']:02d}-(\d+)$", r["errata_id"])
        if m:
            mx = max(mx, int(m.group(1)))
    return f"ER-B{E['nn']:02d}-{mx + 1:03d}"


def status_erratum(E, unit, stage, res, ver, data):
    K = kit(E)
    inst = data.get("INSTANCES", [])
    if not inst:
        return None
    fid = Counter(r["file_id"] for r in inst).most_common(1)[0][0]
    frow = next((f for f in K.table(E["vault"], "l1/FILES.csv") if f["file_id"] == fid), None)
    if not frow or frow["status"] != "NEW":
        return None
    eid = next_errata_id(E)
    kind = "origin paper" if stage == "S3" else "sibling paper"
    row = {"errata_id": eid, "file": "l1/FILES.csv", "row_id": fid, "field": "status", "old": "NEW", "new": "IN-PROGRESS",
           "reason": f"{kind} mined at {stage} (B{E['nn']:02d}, Claude Code route); DONE after S5-S6",
           "evidence": f"PROGRESS.md; {res.get('check', '')}; double-read {ver.get('values', 0)} values",
           "batch": str(E["nn"])}
    p = os.path.join(work(E), "_gate__ERRATA.csv")
    write_csv(p, K.SCHEMA["l1/ERRATA.csv"], [row])
    rc, o, e = run([E["py"], E["kit"], "merge", E["vault"], p, "--table", "ERRATA"])
    os.remove(p)
    if rc != 0:
        raise RuntimeError("status erratum refused: " + (o + e).strip()[-200:])
    return eid


def progress_note(E, unit, stage, res, ver):
    K = kit(E)
    v = E["vault"]
    nn = E["nn"]
    if stage in ("S3", "S4"):
        rows = [r for r in K.table(v, "l1/INSTANCES.csv") if r["paper_id"] == unit]
        c = Counter(r["rel"] or "origin" for r in rows)
        nf = sum(1 for r in K.table(v, "l1/FIGURES.csv") if r["instance_id"].startswith(unit + "-"))
        nfo = sum(1 for r in K.table(v, "l1/FORMULAE.csv") if r["instance_id"].startswith(unit + "-"))
        m = re.search(r"(\d+/\d+) questions . total (\S+)", res.get("check", ""))
        s = f"B{nn:02d}: {len(rows)} rows = {c.get('shuffle', 0)} shuffle + {c.get('origin', 0)} new"
        for k in ("variant", "repeat"):
            if c.get(k):
                s += f" + {c[k]} {k}"
        s += f"; {nf} figures, {nfo} formulae; check-paper PASS {m.group(1) + ', ' + m.group(2) if m else ''}".rstrip()
    elif stage == "S5":
        steps = [x for x in K.table(v, "l1/STEP-AWARDS.csv") if x["paper_id"] == unit and x["batch"] == str(nn)]
        s = f"B{nn:02d}: {len(steps)} scoring lines for {len({x['instance_id'] for x in steps})} question parts"
    else:
        s = f"B{nn:02d}"
    if ver.get("note"):
        s += f"; {ver['note']}"
    elif stage in ("S3", "S4", "S5"):
        s += f"; double-read {ver['values']} values, {ver['diffs']} mismatch(es) settled"
    return s


def progress_update(E, unit, note, match, new_line):
    p = os.path.join(E["vault"], "PROGRESS.md")
    lines = open(p, encoding="utf-8").read().split("\n")
    if new_line:
        at = next((i for i, ln in enumerate(lines) if ln.startswith("## Open")), len(lines))
        while at > 0 and not lines[at - 1].strip():
            at -= 1
        lines.insert(at, f"- [x] {new_line} ({note})")
        open(p, "w", encoding="utf-8").write("\n".join(lines))
        return "added a ticked line"
    pat = re.compile(rf"(?<![\w-]){re.escape(unit)}(?![\w-])")
    target = None
    for i, ln in enumerate(lines):
        if not ln.lstrip().startswith("- [ ]"):
            continue
        if match:
            if match in ln:
                target = i
                break
        elif any(not ln[m.end():].startswith(" done") for m in pat.finditer(ln)):
            target = i              # the unit is named on this line and not yet marked done
            break
    if target is None:
        return "no open PROGRESS line matched (give --progress or --progress-new)"
    ln = lines[target]
    m = next((m for m in pat.finditer(ln) if not ln[m.end():].startswith(" done")), None)
    ln = (ln[:m.end()] + f" done ({note})" + ln[m.end():]) if m else (ln + f" - done ({note})")
    tokens = set(PID_TOKEN.findall(ln))
    pending = [t for t in tokens if not re.search(rf"(?<![\w-]){re.escape(t)} done", ln)]
    ticked = not tokens or not pending
    if ticked:
        ln = ln.replace("- [ ]", "- [x]", 1)
    lines[target] = ln
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    return "line ticked" if ticked else "line updated (" + ", ".join(sorted(pending)) + " still to do)"


def tick_line(E, text, message):
    """Tick the first open PROGRESS line containing `text` (for lines whose condition a script just proved)."""
    p = os.path.join(E["vault"], "PROGRESS.md")
    lines = open(p, encoding="utf-8").read().split("\n")
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("- [ ]") and text in ln:
            lines[i] = ln.replace("- [ ]", "- [x]", 1) + f" - done (B{E['nn']:02d}: {message})"
            open(p, "w", encoding="utf-8").write("\n".join(lines))
            return "line ticked"
    return f"no open PROGRESS line contains '{text}'"


def add_qqueue(E, text):
    p = os.path.join(E["vault"], "QQUEUE.md")
    body = open(p, encoding="utf-8").read() if os.path.exists(p) else "# Q-QUEUE (never blocking)\n"
    ns = [int(x) for x in re.findall(r"\[Q-(\d+)", body)]
    q = f"Q-{(max(ns) + 1) if ns else 1:03d}"
    open(p, "w", encoding="utf-8").write(body.rstrip("\n") + f"\n- [{q} · {dt.date.today().isoformat()} · open] {text}\n")
    return q


def stamp_session(E):
    sid = os.environ.get("CLAUDE_CODE_REMOTE_SESSION_ID", "") or E.get("cc_session", "")
    if not sid:
        return
    p = os.path.join(E["vault"], "STATE.json")
    st = json.load(open(p, encoding="utf-8"))
    st["cc_session"] = sid
    json.dump(st, open(p, "w", encoding="utf-8"), indent=2)


def prune(E):
    def key(f):
        m = re.match(r"PHY-VAULT-B(\d+)-(\d{8}-\d{4})-(\d+)r\.json$", os.path.basename(f))
        return (int(m.group(1)), m.group(2), int(m.group(3))) if m else (-1, "", 0)
    packs = sorted(glob.glob(os.path.join(E["packs_dir"], "PHY-VAULT-B*.json")), key=key)
    gone = [f for f in packs[:-3] if key(f)[0] >= 2]     # chat-era vault files (B00, B01) are never deleted
    for f in gone:
        os.remove(f)
    return len(gone)


def do_pack(E):
    stamp_session(E)
    os.makedirs(E["packs_dir"], exist_ok=True)
    rc, o, e = run([E["py"], E["kit"], "pack", E["vault"], "--batch", str(E["nn"]), "--out", E["packs_dir"]])
    if rc != 0:
        die(3, "PACK FAILED: " + (o + e).strip()[-300:])
    path = o.strip().splitlines()[-1]
    prune(E)
    return path


def archive(E, unit, stage):
    w = work(E)
    d = os.path.join(w, "done", f"{unit}-{stage}")
    os.makedirs(d, exist_ok=True)
    keep = os.path.join(E["logs_dir"], "doublecheck", f"B{E['nn']:02d}")
    for f in glob.glob(os.path.join(w, f"{unit}__*.csv")):
        base = os.path.basename(f)
        if base.split("__", 1)[1] in ("VERIFY.csv", "DIFF.csv", "ADJUDICATE.csv", "SKELETON.csv"):
            os.makedirs(keep, exist_ok=True)
            shutil.copy2(f, os.path.join(keep, f"{unit}-{stage}__{base.split('__', 1)[1]}"))
        shutil.move(f, os.path.join(d, base))


def log(E, lines):
    os.makedirs(E["logs_dir"], exist_ok=True)
    p = os.path.join(E["logs_dir"], f"GATE-LOG-B{E['nn']:02d}.md")
    new = not os.path.exists(p)
    with open(p, "a", encoding="utf-8") as f:
        if new:
            f.write(f"# Gate log - batch B{E['nn']:02d}\nEvery line below was written by phy_gate.py from the data, never typed.\n")
        f.write("\n" + "\n".join(lines) + "\n")


def git(E, *args, timeout=300):
    return run(["git", "-C", E["repos"]["project"]] + list(args), timeout=timeout)


def branch(E):
    return git(E, "rev-parse", "--abbrev-ref", "HEAD")[1].strip() or "?"


def push_now(E, sha=""):
    rc, o, e = git(E, "push", "-q", "-u", "origin", "HEAD", timeout=600)
    b = branch(E)
    if rc != 0:
        return {"sha": sha, "branch": b, "pushed": False, "msg": "PUSH FAILED: " + (o + e).strip()[-300:]}
    return {"sha": sha, "branch": b, "pushed": True, "msg": f"pushed to {b}"}


def commit_push(E, message, push=True):
    git(E, "add", "-A", "outputs")
    if git(E, "diff", "--cached", "--quiet")[0] == 0:
        return {"sha": "", "branch": branch(E), "pushed": False, "msg": "nothing new to commit"}
    rc, o, e = git(E, "commit", "-q", "-m", message)
    if rc != 0 and ("tell me who you are" in (o + e) or "user.email" in (o + e)):
        git(E, "config", "user.name", "Claude Code")
        git(E, "config", "user.email", "noreply@anthropic.com")
        rc, o, e = git(E, "commit", "-q", "-m", message)
    if rc != 0:
        return {"sha": "", "branch": branch(E), "pushed": False, "msg": "COMMIT FAILED: " + (o + e).strip()[-300:]}
    sha = git(E, "rev-parse", "--short", "HEAD")[1].strip()
    if not push:
        return {"sha": sha, "branch": branch(E), "pushed": False, "msg": f"committed {sha}, not pushed (--no-push)"}
    return push_now(E, sha)


def web_base(E):
    url = git(E, "remote", "get-url", "origin")[1].strip()
    m = re.search(r"[:/]([^/:]+)/([^/]+?)(?:\.git)?/?$", url)
    return f"https://github.com/{m.group(1)}/{m.group(2)}" if m else ""


def dashboard_link(E):
    base = web_base(E)
    return f"{base}/blob/{branch(E)}/outputs/README.md" if base else os.path.join(E["outputs"], "README.md")


def write_dashboard(E):
    """outputs/README.md: one front page, rewritten at every save from the vault itself."""
    K = kit(E)
    v = E["vault"]
    packs = sorted(glob.glob(os.path.join(E["packs_dir"], "PHY-VAULT-B*.json")), key=os.path.getmtime)
    newest = os.path.basename(packs[-1]) if packs else ""
    m = re.search(r"-(\d+)r\.json$", newest)
    total = m.group(1) if m else "?"
    papers, meta = defaultdict(Counter), {}
    for r in K.table(v, "l1/INSTANCES.csv"):
        papers[r["paper_id"]][r["rel"] or "origin"] += 1
        meta.setdefault(r["paper_id"], (r["paper_code"], r["exam"]))
    figs = Counter(r["instance_id"].split("-Q", 1)[0] for r in K.table(v, "l1/FIGURES.csv"))
    frms = Counter(r["instance_id"].split("-Q", 1)[0] for r in K.table(v, "l1/FORMULAE.csv"))
    steps = Counter(r["paper_id"] for r in K.table(v, "l1/STEP-AWARDS.csv"))
    res, quar = K.validate(v)
    passed = sum(1 for x in res if x[2] == "PASS")
    status = run([E["py"], E["kit"], "status", v])[1].strip()
    out = [f"# Physics (042) PYQ mining · dashboard",
           f"*Rewritten by phy_gate.py at every save, from the vault itself. Updated {now()} · batch B{E['nn']:02d}.*", "",
           "## Where things stand",
           f"- Newest vault: [{newest}](vault/{newest}) · {total} rows in all" if newest else "- Newest vault: none yet",
           f"- Checks: {passed}/{len(res)} pass" + (f" · quarantined: {', '.join(quar)}" if quar else ""), "", status, "",
           "## Papers in the vault",
           "| paper | code | exam | rows | new | shuffles | figures | formulae | scoring lines |",
           "|---|---|---|---|---|---|---|---|---|"]
    for pid in sorted(papers):
        c = papers[pid]
        code, exam = meta[pid]
        out.append(f"| {pid} | {code} | {exam} | {sum(c.values())} | {c.get('origin', 0)} | {c.get('shuffle', 0)} | "
                   f"{figs.get(pid, 0)} | {frms.get(pid, 0)} | {steps.get(pid, 0)} |")
    rep_dir = E.get("reports_dir") or os.path.join(E["outputs"], "reports")
    reports = sorted(os.listdir(rep_dir)) if os.path.isdir(rep_dir) else []
    out += ["", "## Reports"] + ([f"- [{f}](reports/{f})" for f in reports] or ["- none yet"])
    logs = sorted(os.path.basename(f) for f in glob.glob(os.path.join(E["logs_dir"], "GATE-LOG-B*.md")))
    out += ["", "## Gate logs (every save, every double-read decision)"] + ([f"- [{f}](logs/{f})" for f in logs] or ["- none yet"])
    with open(os.path.join(E["outputs"], "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


def rollback(v, snap):
    keep, tmpw = os.path.join(v, "work"), v.rstrip("/") + "_work_keep"
    shutil.rmtree(tmpw, ignore_errors=True)
    if os.path.isdir(keep):
        shutil.move(keep, tmpw)
    shutil.rmtree(v, ignore_errors=True)
    shutil.copytree(snap, v)
    if os.path.isdir(tmpw):
        shutil.rmtree(os.path.join(v, "work"), ignore_errors=True)
        shutil.move(tmpw, os.path.join(v, "work"))


# ------------------------------------------------------------------------------------------------ commands
def cmd_commit(a):
    E = env()
    K = kit(E)
    unit, stage, nn, v = a.unit, a.stage, E["nn"], E["vault"]
    unseal(E, unit)
    if stage == "S5" and not (a.progress or a.progress_new or a.no_progress):
        refuse(['an S5 commit names its PROGRESS line: --progress "S5 scheme 55/1/1 (" (text of that line), '
                'or --no-progress for a part of a scheme'])
    probs, info, data = lint(E, unit, stage)
    if probs:
        refuse(probs)
    ver = {"values": 0, "diffs": 0, "rows": 0, "unresolved": [], "adj": [], "note": ""}
    if stage in ("S3", "S4", "S5"):
        if a.unverified:
            ver["note"] = "UNVERIFIED: " + a.unverified
        else:
            ver = verify(E, unit, stage)
            if ver["unresolved"]:
                report_verify(ver)
                die(1, "REFUSED: settle every mismatch first (PHY-07 section 8), then rerun commit")
    tprobs, res = trial(E, unit, stage)
    if tprobs:
        refuse(tprobs)
    snap = os.path.join(E["home"], "vault_snapshot")
    shutil.rmtree(snap, ignore_errors=True)
    shutil.copytree(v, snap, ignore=shutil.ignore_patterns("work"))
    merged, erratum, qid, prog, fin = [], None, None, "", {}
    try:
        for t, p in parts(E, unit):
            rc, o, e = run([E["py"], E["kit"], "merge", v, p, "--table", t])
            if rc != 0:
                raise RuntimeError(f"merge {t}: {(o + e).strip()[-300:]}")
            merged.append(o.strip())
        if stage in ("S3", "S4"):
            erratum = status_erratum(E, unit, stage, res, ver, data)
        if a.unverified:
            qid = add_qqueue(E, f"{unit} ({stage}) was merged without the double-read: {a.unverified}. "
                                f"Run the blind check on it at the next session.")
        note = progress_note(E, unit, stage, res, ver)
        if not a.no_progress and (stage != "OTHER" or a.progress or a.progress_new):
            prog = progress_update(E, unit, note, a.progress, a.progress_new)
        after = validate_delta(K, snap, v, unit, fin)
        if after:
            raise RuntimeError("validate after the merge: " + "; ".join(after))
    except Exception as ex:
        rollback(v, snap)
        die(3, f"MERGE FAILED, the vault was rolled back to its state before this commit: {ex}")
    pack = do_pack(E)
    archive(E, unit, stage)
    lines = [f"## {now()} | {unit} | {stage} | GATE PASS", f"- part files: {', '.join(info)}"]
    lines += [f"- {m}" for m in merged]
    if res.get("check"):
        lines.append(f"- check-paper: {res['check']}")
    lines.append(f"- validate after merge: {fin.get('validate', '')}")
    if stage in ("S3", "S4", "S5"):
        lines.append(f"- double-read: {ver.get('note') or str(ver['values']) + ' values compared, ' + str(ver['diffs']) + ' mismatch(es), all settled'}")
        for x in ver.get("adj", []):
            lines.append(f"  - {x.get('instance_id', '')} | {x.get('field', '')} | {x.get('decision', '')} | final "
                         f"{x.get('final_value', '')} | crop {x.get('crop', '')} | {x.get('note', '')}")
    if erratum:
        lines.append(f"- status erratum {erratum}: NEW -> IN-PROGRESS")
    if qid:
        lines.append(f"- Q-QUEUE {qid} added (merged without the double-read)")
    lines.append(f"- PROGRESS: {prog or 'not touched (stage OTHER)'}")
    lines.append(f"- pack: {os.path.basename(pack)}")
    log(E, lines)
    write_dashboard(E)
    n_rows = len(data.get("INSTANCES", [])) or len(data.get("STEP-AWARDS", [])) or sum(len(x) for x in data.values())
    msg = (f"B{nn:02d} | {unit} | {stage} | {n_rows} rows | {res.get('check', 'no check-paper')} | "
           f"validate {fin.get('validate', '')} | " + (ver.get("note") or f"double-read {ver['values']} values, {ver['diffs']} settled"))
    g = commit_push(E, msg, push=not a.no_push)
    print(f"GATE PASS | {unit} | {stage} | {', '.join(info)}")
    if res.get("check"):
        print(f"  {res['check']}")
    print(f"  validate {fin.get('validate', '')} | " + (ver.get("note") or f"double-read {ver['values']} values, "
          f"{ver['diffs']} mismatch(es) settled"))
    print(f"  {('erratum ' + erratum + ' | ') if erratum else ''}PROGRESS: {prog or 'not touched'}")
    print(f"  pack {os.path.basename(pack)} | commit {g['sha'] or '-'} | {g['msg']}")
    print(f"  Dashboard: {dashboard_link(E)}")
    sys.exit(4 if (not a.no_push and g["sha"] and not g["pushed"]) else 0)


def cmd_checkpoint(a):
    E = env()
    K = kit(E)
    res, quar = K.validate(E["vault"])
    passed = sum(1 for x in res if x[2] == "PASS")
    vline = f"{passed}/{len(res)} checks pass" + (f"; quarantined: {', '.join(quar)}" if quar else "")
    prog = ""
    if a.progress_new:
        prog = progress_update(E, "", f"B{E['nn']:02d}", None, a.progress_new)
    elif a.tick:
        prog = tick_line(E, a.tick, a.message)
    pack = do_pack(E)
    log(E, [f"## {now()} | checkpoint | {a.message}", f"- validate: {vline}"] + ([f"- PROGRESS: {prog}"] if prog else [])
        + [f"- pack: {os.path.basename(pack)}"])
    write_dashboard(E)
    g = commit_push(E, f"B{E['nn']:02d} | checkpoint | {a.message} | validate {passed}/{len(res)}", push=not a.no_push)
    print(f"CHECKPOINT | {a.message} | validate {vline}" + (f" | PROGRESS: {prog}" if prog else ""))
    print(f"  pack {os.path.basename(pack)} | commit {g['sha'] or '-'} | {g['msg']}")
    print(f"  Dashboard: {dashboard_link(E)}")
    sys.exit(4 if (not a.no_push and g["sha"] and not g["pushed"]) else 0)


def cmd_push(a):
    E = env()
    g = push_now(E, git(E, "rev-parse", "--short", "HEAD")[1].strip())
    print(g["msg"])
    sys.exit(0 if g["pushed"] else 4)


def cmd_show(a):
    E = env()
    w = work(E)
    units = defaultdict(list)
    for f in sorted(glob.glob(os.path.join(w, "*__*.csv"))):
        u, t = os.path.basename(f)[:-4].split("__", 1)
        units[u].append(f"{t} {len(read_csv(f)[1])}")
    sealed = sorted(os.path.basename(x) for x in glob.glob(os.path.join(E["home"], ".sealed", "*")))
    print(f"session batch B{E['nn']:02d} | vault {E['vault']} | project branch {branch(E)}")
    for u, items in units.items():
        print(f"  {u}: {', '.join(items)}")
    if not units:
        print("  nothing waiting in vault/work")
    if sealed:
        print(f"  sealed (waiting for verify): {', '.join(sealed)}")


def main():
    ap = argparse.ArgumentParser(prog="phy_gate", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    stages = ["S3", "S4", "S5", "OTHER"]
    s = sp.add_parser("check")
    s.add_argument("unit")
    s.add_argument("--stage", required=True, choices=stages)
    s.set_defaults(fn=cmd_check)
    s = sp.add_parser("skeleton")
    s.add_argument("unit")
    s.add_argument("--stage", required=True, choices=["S3", "S4", "S5"])
    s.set_defaults(fn=cmd_skeleton)
    s = sp.add_parser("unseal")
    s.add_argument("unit")
    s.set_defaults(fn=cmd_unseal)
    s = sp.add_parser("verify")
    s.add_argument("unit")
    s.add_argument("--stage", required=True, choices=["S3", "S4", "S5"])
    s.set_defaults(fn=cmd_verify)
    s = sp.add_parser("commit")
    s.add_argument("unit")
    s.add_argument("--stage", required=True, choices=stages)
    s.add_argument("--progress", default="")
    s.add_argument("--progress-new", dest="progress_new", default="")
    s.add_argument("--no-progress", dest="no_progress", action="store_true")
    s.add_argument("--unverified", default="")
    s.add_argument("--no-push", dest="no_push", action="store_true")
    s.set_defaults(fn=cmd_commit)
    s = sp.add_parser("checkpoint")
    s.add_argument("--message", required=True)
    s.add_argument("--progress-new", dest="progress_new", default="")
    s.add_argument("--tick", default="", help="tick the first open PROGRESS line containing this text")
    s.add_argument("--no-push", dest="no_push", action="store_true")
    s.set_defaults(fn=cmd_checkpoint)
    s = sp.add_parser("push")
    s.set_defaults(fn=cmd_push)
    s = sp.add_parser("show")
    s.set_defaults(fn=cmd_show)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
