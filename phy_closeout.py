#!/usr/bin/env python3
"""phy_closeout.py - the session close-out (her decision 2026-11-10). Edition 2026-11-10.

Run it once at the end of every session (and before a usage stop), then save with the gate:
    python3 /mnt/project/phy_closeout.py [--lesson "<one change for next time, with its evidence>"]
                                         [--usage-start <her %> --usage-end <her %>] [--note "<text>"]
    python3 /home/claude/phy_gate.py checkpoint --message "close-out B<nn>"

It measures this session with outputs/tools/phy_measure.py (readers and the main session, weighted as
the plan meter counts), writes one block for this session into outputs/reports/PHY-USAGE-LEDGER.md
(a rerun replaces this session's block), and keeps outputs/LESSONS.md: what makes mining cheap without
losing accuracy, written so that the Chemistry and Maths mining can start from it.
It reads transcripts and writes those two files only. It never touches the vault's tables.
"""
import argparse, datetime, glob, json, os, re, subprocess, sys

ENV = "/home/claude/phy_env.json"
CAP = 6000
SEED = """# LESSONS · what keeps PYQ mining cheap without losing accuracy
*Kept by phy_closeout.py. One dated line per lesson, each with its evidence. Under 6,000 characters: merge old lines before adding. Written for any subject: the Chemistry and Maths mining start from this file.*

## What the measurements say (Physics, to 2026-11-10)
- One thorough reading is enough when a year check follows: on the two double-read 2026 papers 747 values were compared and the first reading had no wrong value; the 2024 year check found 10 real errors in 1,732 re-read values, none of them a misread digit on a band (figure values measured off the drawing, one half mark a line off, three page citations).
- A lean single reading of 2023 is as clean as the double-read 2026 work by the year check's own script: 13.2 doubtful numbers per 100 original rows against 14.9 (2025) and 14.1 (2026); a blind re-read of 12 questions on 10 papers matched 72 of 72 numbers (2026-11-10).
- What a reading unit costs: page images are the largest part (written to the cache once, then re-read at every step), then output (half of it thinking). So: only the pages a unit needs, each opened once, at the tested size (180 dpi half-page bands); text steps before images; few steps.
- The main session is paid for again after every reader: its whole context is written to the cache once more whenever a reader runs longer than the cache lifetime. Measured before the stage boot pack on the one clean unit (S2A-2023): 231,978 for the main session against 581,891 for its reader. So the main session reads only what its next unit needs (phy_boot.py: about 64,000 characters for a scheme stage against about 200,000 before), never opens an image, and keeps tool output to counts.
- A fresh reader per set, not one reader per scheme file (decided 2026-11-10): one reader for three sets would save two reader start-ups and two main-session rounds, but every later step would re-read the first set's page images, and three sets' answers would sit in one view (the W-1 risk). By the same measurements the gain is a few per cent at most; the stage boot pack gets more without that risk. Also not adopted: clearing year-check flags that are only printed constants (on the 2024 check's own files it would have taken 3 of 262 rows off the list, each on the single digit 4).
- A year's intake needs only the top band of each identity page (series word, set, code, subject line; a scheme's header); open a bottom band only when one of those is missing (2023's intake opened 74 images, 72 of them half-page bands).
- Sessions: a new session after every usage stop; an idle conversation re-sends everything at the full write rate.
- Worksheets by script (locate answers, align sibling sets, list printed marks) let the reader spend its thinking on the page; no script ever writes a value.

## Lessons by session
"""


def md_num(s):
    s = s.strip().replace(",", "")
    try:
        return float(s)
    except ValueError:
        return 0.0


def parse_table(text):
    """Rows of phy_measure's first table: (unit, weighted, main weighted, minutes, steps, images)."""
    rows = []
    for line in text.split("\n"):
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 13 and c[0] not in ("unit",) and not set(c[0]) <= set("-"):
            rows.append({"unit": c[0], "steps": md_num(c[1]), "images": md_num(c[2].split("·")[0]),
                         "weighted": md_num(c[6]), "main": md_num(c[11]) if c[11] != "-" else 0.0, "minutes": md_num(c[12])})
        if line.startswith("Image check"):
            break
    return rows


def find_transcripts(sid):
    """(main transcript, session folder) of this session: by its id, else the newest transcript on the machine."""
    cands = glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl"))
    if not cands:
        return None, None
    hit = [c for c in cands if sid and sid in os.path.basename(c)]
    main = hit[0] if hit else max(cands, key=os.path.getmtime)
    return main, main[:-len(".jsonl")]


def model_of(path):
    seen = {}
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                m = re.search(r'"model"\s*:\s*"(claude-[^"]+)"', line)
                if m:
                    seen[m.group(1)] = seen.get(m.group(1), 0) + 1
    except OSError:
        pass
    return " + ".join(sorted(seen, key=seen.get, reverse=True)) or "unknown"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson", action="append", default=[]); ap.add_argument("--note", default="")
    ap.add_argument("--usage-start", default=""); ap.add_argument("--usage-end", default="")
    ap.add_argument("--table", help="test only: a file holding phy_measure output")
    a = ap.parse_args()
    try:
        E = json.load(open(ENV, encoding="utf-8"))
    except (OSError, ValueError):
        print(f"! {ENV} is missing: run the setup first (CLAUDE.md section 6)."); return 2
    out = E["outputs"]; batch = int(E["session_batch"]); sid = E.get("cc_session", "") or "unknown"
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    os.makedirs(os.path.join(out, "reports"), exist_ok=True)
    table, model, why = "", "unknown", ""
    if a.table:
        table = open(a.table, encoding="utf-8").read()
    else:
        main_t, folder = find_transcripts(sid)
        tool = os.path.join(out, "tools", "phy_measure.py")
        if not main_t:
            why = "no transcript found under ~/.claude/projects"
        elif not os.path.exists(tool):
            why = f"{tool} is missing"
        else:
            model = model_of(main_t)
            r = subprocess.run([sys.executable, tool, "--dir", folder, "--main", main_t], capture_output=True, text=True, timeout=600)
            table = r.stdout
            if r.returncode != 0 or "| unit |" not in table:
                why = "phy_measure.py gave no table: " + (r.stderr.strip().split("\n")[-1][:160] if r.stderr.strip() else "empty output")
    rows = parse_table(table)
    head = f"## {today} · B{batch:02d} · session {sid[:12]} · model {model}"
    L = [head]
    if rows:
        rw = sum(r["weighted"] for r in rows); mw = sum(r["main"] for r in rows); tot = rw + mw or 1
        L.append(f"{len(rows)} unit(s) · readers' weighted sum {rw:,.0f} · main session {mw:,.0f} ({100 * mw / tot:.0f} % of all) · "
                 f"per unit {tot / len(rows):,.0f} · reader minutes {sum(r['minutes'] for r in rows):.0f}"
                 + (f" · her meter {a.usage_start} % to {a.usage_end} %" if a.usage_start and a.usage_end else ""))
    else:
        L.append("not measured: " + (why or "no unit rows in the table"))
    if a.note:
        L.append("note: " + a.note)
    if table.strip():
        L += ["", table.strip()]
    block = "\n".join(L) + "\n"
    led = os.path.join(out, "reports", "PHY-USAGE-LEDGER.md")
    old = open(led, encoding="utf-8").read() if os.path.exists(led) else (
        "# PHY usage ledger\n*One block per session, written by phy_closeout.py from phy_measure.py. Weighted sums in base-input "
        "equivalents (PHY-07 R§14). Compare sessions by 'per unit' within one kind of unit; the baseline is PHY-USAGE-BASELINE.md.*\n")
    parts = re.split(r"(?m)^(?=## )", old)
    parts = [p for p in parts if not p.startswith(f"## {today} · B{batch:02d} · session {sid[:12]} ")]
    with open(led, "w", encoding="utf-8") as f:
        f.write("".join(parts).rstrip() + "\n\n" + block)
    les = os.path.join(out, "LESSONS.md")
    text = open(les, encoding="utf-8").read() if os.path.exists(les) else SEED
    for x in a.lesson:
        line = f"- {today} · B{batch:02d} · {x.strip()}"
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    with open(les, "w", encoding="utf-8") as f:
        f.write(text)
    print(L[0]); print(L[1])
    print(f"ledger: {led} · lessons: {les} ({len(text):,} chars" + (f"; over {CAP:,}: merge old lines" if len(text) > CAP else "") + ")")
    print('next: python3 /home/claude/phy_gate.py checkpoint --message "close-out B%02d"' % batch)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as ex:                        # a close-out must never cost a session its last save
        print(f"! phy_closeout.py failed ({type(ex).__name__}: {ex}); save with the gate and say so in the report.")
        sys.exit(0)
