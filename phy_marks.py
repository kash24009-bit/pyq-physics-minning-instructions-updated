#!/usr/bin/env python3
"""phy_marks.py - the marks a born-digital marking scheme prints, each with the text printed at its height.

A locator for the S5 reader's second look (rule card C8, E1): which line each printed mark sits beside, so a half
attached one line off (2024-5531-Q31B-ii, Q-078) is seen at the unit, not a year later. Everything comes from the
scheme's TEXT LAYER, so nothing in its output may be copied into a row: every mark is read on the page image, and
where a mark sits between two lines, or beside an equation the text layer cannot spell, the image decides.

  python3 phy_marks.py --pdf <scheme.pdf> --pages 25-46 [--out PREP.md]      (appends to --out, else prints)
  python3 phy_marks.py --fid FL-xxxx --pages 25-46 [--out PREP.md]           (finds the PDF by its sha256)
  add --check <paper_id> to compare each question's printed marks with the vault's PRINTED lines of that paper

The columns come from the answer table's own header line ("MARKS" and "TOTAL MARKS", any case); without one,
from the section's most crowded column of mark tokens (½, 1, 1½, ½+½ ...) in the right part of the page. Marks
further left (an answer's head box) are not listed. The list starts at the first page with the answer-table
header, so the examiner-instruction pages are skipped. Each total closes an answer, or one side of an OR, and the
marks listed since the previous total must add up to it, else the list says so in a line marked **; an answer
whose only mark stands in the total column (some Section A tables) is listed from there. A page with no text
layer prints "no text layer". Uses poppler's pdftotext when installed, else pypdfium2 (the setup installs both).
Edition 2026-10-21 (made in the project chat; tested on the 2024 schemes, see PHY-AUDIT-2024-B06.md).
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
from collections import defaultdict

MARK = re.compile(r"^(?:\d+(?:\.\d+)?|\d*½|\d+/\d+)(?:\+(?:\d+(?:\.\d+)?|\d*½|\d+/\d+))*$")
FURNITURE = re.compile(r"Page\s+\d+\s+of\s+\d+|MARKING\s+SCHEME|\bCODE\s*:|VALUE\s+POINTS|^\s*(?:TOTAL\s+)?MARKS\s*$|"
                       r"^\s*TOTAL\s*$|^\s*Q\.?\s*NO\b", re.I)            # page headers and footers
HEADER = re.compile(r"VALUE\s*POINTS|MARKING\s+SCHEME\s*:\s*PHYSICS")          # the answer-table header


def mark_value(tok):
    tot = 0.0
    for part in tok.split("+"):
        if part.endswith("½"):
            tot += (float(part[:-1]) if part[:-1] else 0.0) + 0.5
        elif "/" in part:
            a, b = part.split("/")
            tot += float(a) / float(b) if float(b) else 0.0
        elif part:
            tot += float(part)
    return tot


def words_pdftotext(path, pno):
    """Words with their boxes (points, top-left origin) from pdftotext -bbox; None when poppler is missing."""
    if not shutil.which("pdftotext"):
        return None
    r = subprocess.run(["pdftotext", "-f", str(pno), "-l", str(pno), "-bbox", path, "-"], capture_output=True, text=True)
    m = re.search(r'<page width="([\d.]+)" height="([\d.]+)"', r.stdout)
    if not m:
        return [], 0.0, 0.0
    out = []
    for x0, y0, x1, y1, t in re.findall(
            r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', r.stdout):
        t = t.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&amp;", "&")
        out.append({"t": t, "x0": float(x0), "y0": float(y0), "x1": float(x1), "y1": float(y1)})
    return out, float(m.group(1)), float(m.group(2))


def words_pdfium(page):
    """The same from pypdfium2, with loose (font-height) character boxes."""
    tp = page.get_textpage()
    W, H = page.get_size()
    out, cur = [], None
    for i in range(tp.count_chars()):
        c = tp.get_text_range(i, 1)
        if not c or c.isspace():
            if cur:
                out.append(cur)
                cur = None
            continue
        l, b, r, t = tp.get_charbox(i, loose=True)
        x0, y0, x1, y1 = l, H - t, r, H - b
        if cur and abs((y0 + y1) / 2 - (cur["y0"] + cur["y1"]) / 2) < 3 and -1 < x0 - cur["x1"] < 2.5:
            cur["t"] += c
            cur["x1"] = max(cur["x1"], x1)
            cur["y0"], cur["y1"] = min(cur["y0"], y0), max(cur["y1"], y1)
        else:
            if cur:
                out.append(cur)
            cur = {"t": c, "x0": x0, "x1": x1, "y0": y0, "y1": y1}
    if cur:
        out.append(cur)
    return out, W, H


def yc(w):
    return (w["y0"] + w["y1"]) / 2


def xc(w):
    return (w["x0"] + w["x1"]) / 2


def join_marks(ws):
    """Glue a cell printed as separate words ('½', '+', '½' or '½ +½') into one token '½+½'."""
    out = []
    for w in sorted(ws, key=lambda w: (round(yc(w)), w["x0"])):
        t = w["t"].replace(" ", "")
        if out and abs(yc(out[-1]) - yc(w)) < 3 and w["x0"] - out[-1]["x1"] < 8 and \
                (t.startswith("+") or out[-1]["t"].endswith("+")):
            out[-1] = dict(out[-1], t=out[-1]["t"] + t, x1=w["x1"])
        else:
            out.append(dict(w, t=t))
    return out


def lines_of(ws):
    lines = []
    for w in sorted(ws, key=yc):
        if lines and abs(lines[-1]["yc"] - yc(w)) < 3:
            lines[-1]["w"].append(w)
        else:
            lines.append({"yc": yc(w), "w": [w]})
    for ln in lines:
        ln["w"].sort(key=lambda w: w["x0"])
        ln["y0"], ln["y1"] = min(w["y0"] for w in ln["w"]), max(w["y1"] for w in ln["w"])
        ln["text"] = " ".join(w["t"] for w in ln["w"])
    return lines


def mark_tokens(ws, W):
    ws = [w for ln in lines_of(ws) if not FURNITURE.search(ln["text"]) for w in ln["w"]]
    return [w for w in join_marks(ws) if MARK.match(w["t"]) and xc(w) > 0.70 * W]


def header_columns(pages):
    """Column bounds from the answer table's own header line, the line printing "MARKS" and "TOTAL" (any case) in
    the right part of the page: (lowest x of a line mark, lowest x of a total)."""
    for ws, W, _ in pages:
        for ln in lines_of(ws):
            right = [w for w in ln["w"] if w["x0"] > 0.6 * W]
            m = [w["x0"] for w in right if w["t"].upper() == "MARKS"]
            t = [w["x0"] for w in right if w["t"].upper() == "TOTAL"]
            if m and t and min(t) > min(m):
                return min(m) - 15, min(t) - 6
    return None


def marks_column(pages):
    """The x of the line-marks column for a whole section: the 12-pt cluster of mark tokens holding the most tokens
    (an answer's head box and the totals column hold fewer)."""
    xs = sorted(xc(w) for ws, W, _ in pages if ws for w in mark_tokens(ws, W))
    if not xs:
        return None
    cols = [[xs[0]]]
    for x in xs[1:]:
        if x - cols[-1][-1] <= 12:
            cols[-1].append(x)
        else:
            cols.append([x])
    best = max(cols, key=len)
    return min(best), max(best)


def page_marks(ws, W, column=None, bounds=None):
    """{rows, totals, starts, ors} for one page, or None without a text layer. rows: {y, mark, value, where, text,
    total}; totals: [(y, {value, mark, text, where})]; starts: [(y, question number)]; ors: [(y, "OR" or
    "Alternatively")]. Page headers and footers are left out."""
    if not ws:
        return None
    ws = [w for ln in lines_of(ws) if not FURNITURE.search(ln["text"]) for w in ln["w"]]
    starts, ors = [], []
    for ln in lines_of(ws):
        w0 = ln["w"][0]
        if w0["x0"] < 0.2 * W and re.fullmatch(r"\d{1,2}\.?", w0["t"]):
            starts.append((ln["yc"], int(w0["t"].rstrip("."))))
    cand = [w for w in join_marks(ws) if MARK.match(w["t"]) and xc(w) > 0.70 * W]
    if not cand or not (column or bounds):
        return {"rows": [], "totals": [], "starts": starts, "ors": ors}
    if bounds:                                   # the header's MARKS and TOTAL columns
        marks = [w for w in cand if bounds[0] <= w["x0"] and w["x1"] < bounds[1] + 6]
        totals = [w for w in cand if w["x0"] >= bounds[1]]
    else:                                        # no header: the section's most crowded column of marks
        lo, hi = column[0] - 8, column[1] + 8
        marks = [w for w in cand if lo <= xc(w) <= hi]
        totals = [w for w in cand if xc(w) > hi + 10]
    left = min(w["x0"] for w in marks) if marks else (bounds[0] if bounds else column[0] - 8)
    lines = lines_of([w for w in ws if w["x1"] < left - 4])
    for ln in lines:                             # "OR" and "Alternatively" lines start a new side
        t = ln["text"].strip()
        if t == "OR" or re.match(r"Alternatively\b", t):
            ors.append((ln["yc"], "OR" if t == "OR" else "Alternatively"))
    rows = []

    def text_at(m):
        """The line the mark shares most of its height with ('beside'), else the lines above and below it."""
        h = max(m["y1"] - m["y0"], 1.0)
        ov = sorted(((max(0.0, min(m["y1"], ln["y1"]) - max(m["y0"], ln["y0"])), i) for i, ln in enumerate(lines)),
                    reverse=True)
        best, second = (ov[0] if ov else (0.0, None)), (ov[1][0] if len(ov) > 1 else 0.0)
        if best[1] is not None and best[0] >= 0.5 * h and best[0] - second >= 1.5:
            return lines[best[1]]["text"], "beside"
        above = [ln for ln in lines if 0 < yc(m) - ln["yc"] <= 14]
        below = [ln for ln in lines if 0 <= ln["yc"] - yc(m) <= 14]
        a = above[-1]["text"] if above else ""
        b = below[0]["text"] if below else ""
        return (f"{a}  /  {b}" if (a or b) else "(no text near it)"), "between"
    for m in sorted(marks, key=yc):
        text, where = text_at(m)
        tot = [t["t"] for t in totals if abs(yc(t) - yc(m)) < 4]
        rows.append({"y": yc(m), "mark": m["t"], "value": mark_value(m["t"]), "where": where, "text": text,
                     "total": tot[0] if tot else ""})
    tots = []
    for t in totals:
        text, where = text_at(t)
        tots.append((yc(t), {"value": mark_value(t["t"]), "mark": t["t"], "text": text, "where": where}))
    return {"rows": rows, "totals": tots, "starts": starts, "ors": ors}


def load_kit(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("pyqkit", path)
    K = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(K)
    return K


def resolve(vault, fid, kit_path):
    K = load_kit(kit_path)
    row = {f["file_id"]: f for f in K.table(vault, "l1/FILES.csv")}.get(fid)
    if not row:
        raise SystemExit(f"phy_marks: no file {fid} in the vault's FILES table")
    want = row["sha256"]
    for root in ("/mnt/project", "/mnt/user-data/uploads", os.path.join(vault, "work", "_intake")):
        for dp, _, fns in os.walk(root, followlinks=True):
            for fn in fns:
                if fn.lower().endswith(".pdf"):
                    p = os.path.join(dp, fn)
                    h = hashlib.sha256()
                    with open(p, "rb") as f:
                        for blk in iter(lambda: f.read(1 << 20), b""):
                            h.update(blk)
                    if h.hexdigest() == want:
                        return p
    raise SystemExit(f"phy_marks: no PDF on disk with the sha256 of {fid}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf")
    ap.add_argument("--fid")
    ap.add_argument("--pages", required=True)
    ap.add_argument("--out")
    ap.add_argument("--check")
    ap.add_argument("--vault", default="/home/claude/vault")
    ap.add_argument("--kit", default="/home/claude/pyqkit.py")
    ap.add_argument("--backend", choices=("auto", "pdfium"), default="auto")
    a = ap.parse_args()
    import pypdfium2 as pdfium
    path = a.pdf or resolve(a.vault, a.fid, a.kit)
    p0, p1 = map(int, a.pages.split("-"))
    doc = pdfium.PdfDocument(path)
    L = ["", "## Printed marks with the text at their height (text layer; locate only)", "",
         "Read every mark on the page image. 'beside': the text printed on the mark's own line. 'between': no text",
         "shares its line, so the lines just above and below are shown, and the image decides (card C8).", ""]
    q, want, per_q, seg, sides, flags, checked, split = None, 1, defaultdict(float), 0.0, [], 0, 0, set()
    pages = {}
    for pno in range(p0, p1 + 1):
        got = words_pdftotext(path, pno) if a.backend == "auto" else None
        pages[pno] = got if got is not None else words_pdfium(doc[pno - 1])
    # answers begin at the first page with the answer-table header ("MARKING SCHEME : PHYSICS", "VALUE POINTS");
    # the examiner-instruction pages before it are skipped. A range without that header starts mid-section.
    head = [pno for pno, (ws, W, _) in pages.items() if HEADER.search(" ".join(w["t"] for w in ws))]
    first = head[0] if head else p0
    section = [pages[pno] for pno in range(first, p1 + 1)]
    bounds = header_columns(section)
    column = None if bounds else marks_column(section)
    for pno in range(first, p1 + 1):
        ws, W, _ = pages[pno]
        pm = page_marks(ws, W, column, bounds)
        if pm is None:
            L.append(f"- p{pno}: no text layer: compare every mark on the image")
            continue
        events = ([(y, 0, n) for y, n in pm["starts"]] + [(r["y"], 1, r) for r in pm["rows"]] +
                  [(y, 2, t) for y, t in pm["totals"]] + [(y, 3, k) for y, k in pm["ors"]])
        for _, kind, x in sorted(events, key=lambda e: (e[0], e[1])):
            if kind == 0:
                if x == want or (q is None and x > want):      # a page range may start mid-section
                    q, want, seg, sides = x, x + 1, 0.0, []
                    L.append(f"### Q{q:02d}")
            elif kind == 3:                           # an OR: the marks so far are one side
                if seg:
                    sides.append(seg)
                seg = 0.0
                if q is not None:
                    split.add(q)
                L.append(f"- {x} (a new side starts)")
            elif kind == 1:
                L.append(f"- p{pno} · {x['mark']} · {x['where']}: {x['text'][:110]}" +
                         (f"   (total {x['total']})" if x["total"] else ""))
                if q is not None:
                    per_q[q] += x["value"]
                seg += x["value"]
            else:                                     # a total closes an answer, or one side of an OR
                if not seg and not sides:             # an answer whose only printed mark stands in the total column
                    L.append(f"- p{pno} · {x['mark']} (total column, no line mark) · {x['where']}: {x['text'][:100]}")
                    if q is not None:
                        per_q[q] += x["value"]
                    seg = x["value"]
                x = x["value"]
                allsides = sides + [seg]
                checked += 1
                if sides:      # either one side carries the total (a side that replaces only part of the answer,
                    # such as a choice inside a case, carries less), or the mark sits on the OR line, shared
                    ok = (any(abs(x - v) < 1e-9 for v in allsides) and all(v <= x + 1e-9 for v in allsides)) \
                        or abs(x - sum(allsides)) < 1e-9
                else:
                    ok = abs(x - seg) < 1e-9
                if not ok:
                    flags += 1
                    L.append(f"- **p{pno}: the marks listed since the previous total add up to "
                             f"{' and '.join(f'{v:g}' for v in allsides)}; the printed total is {x:g}: a mark here was "
                             f"missed or misread, so read these marks on the image**")
                seg, sides = 0.0, []
    if a.check:
        K = load_kit(a.kit)
        rows_ = [r for r in K.table(a.vault, "l1/INSTANCES.csv") if r["paper_id"] == a.check]
        qof = {r["instance_id"]: int(r["q_no"]) for r in rows_}
        shuffled = {int(r["q_no"]) for r in rows_} - {int(r["q_no"]) for r in rows_ if r["rel"] == "origin"}
        have = defaultdict(float)
        for s in K.table(a.vault, "l1/STEP-AWARDS.csv"):
            if s["instance_id"] in qof and s["provenance"] == "PRINTED":
                try:
                    have[qof[s["instance_id"]]] += float(s["marks"] or 0)
                except ValueError:
                    pass
        L += ["", f"## Printed marks against the vault's PRINTED lines of {a.check} (question sums only)", "",
              "An answer that prints OR or Alternatively can differ for a known reason: an alternative method's marks go",
              "in alt_accepted (card C6), and an OR-alternative key takes the sub-part's mark (card C5).", ""]
        for qq in sorted(set(per_q) | set(have)):
            same = abs(per_q.get(qq, 0) - have.get(qq, 0)) < 1e-9
            if qq in shuffled and not have.get(qq):
                L.append(f"- Q{qq:02d}: printed {per_q.get(qq, 0):g} · a shuffle: its lines are its origin's")
                continue
            L.append(f"- Q{qq:02d}: printed {per_q.get(qq, 0):g} · lines {have.get(qq, 0):g}" +
                     ("" if same else ("   <- differs (OR or Alternatively printed)" if qq in split
                                       else "   <- differs: look at the page")))
    L.insert(6, f"Totals checked against the marks listed: {checked}; not matched: {flags} (each one marked ** below).")
    L.insert(7, "")
    text = "\n".join(L) + "\n"
    n = sum(1 for x in L if x.startswith("- p"))
    if a.out:
        with open(a.out, "a", encoding="utf-8") as f:
            f.write(text)
        print(f"phy_marks: {n} printed marks listed for pp {a.pages}; totals checked {checked}, not matched {flags} -> {a.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
