#!/usr/bin/env python3
"""phy_boot.py - the stage boot pack (her decision 2026-11-10). Edition 2026-11-10.

Run it once after the setup (CLAUDE.md section 6 step 2) and again after a compaction:
    python3 /mnt/project/phy_boot.py [--stage S1|S2a|S3|S4|S5|YC|S6|S7|S8|FIX] [--year 2023]

It prints, in one output, only what the main session needs for the unit it is about to start:
the open PROGRESS lines, the plan file in force (PHY-09-*.md), the playbook and runbook sections
of that stage, the CONVENTIONS entries of that year and stage with an index of every other entry,
the open queue items that name the year or the stage, and the newest mistakes entries.

It only selects text that is already in those files. It writes nothing, changes nothing, opens no
page and puts no value anywhere. The full files stay the authority: read a whole section or entry
(the index gives its line number) whenever a step needs more than is printed here.
Why: the main session's context is written to the cache again after every reader that runs longer
than the cache lifetime, so every line read at boot is paid for once per unit (PHY-USAGE-BASELINE,
unit S2A-2023: 231,978 weighted for the main session against 581,891 for its reader).
Paths can be overridden for tests: PHY_VAULT, PHY_MNT.
"""
import argparse, datetime, glob, os, re, sys

V = os.environ.get("PHY_VAULT", "/home/claude/vault")
MP = os.environ.get("PHY_MNT", "/mnt/project")
EDITION = "2026-11-10"

Y_SECTIONS = {"S1": ["Y§2", "Y§8"], "S2a": ["Y§3", "Y§8"], "S3": ["Y§4", "Y§6", "Y§7", "Y§8"],
              "S4": ["Y§4", "Y§6", "Y§7", "Y§8"], "S5": ["Y§5", "Y§8"], "YC": ["Y§11", "Y§8"],
              "S6": ["Y§12"], "S7": ["Y§12"], "S8": ["Y§12"], "FIX": []}
R_SECTIONS = {"S1": ["R§6", "R§9"], "S2a": ["R§6", "R§9"], "S3": ["R§6", "R§9"], "S4": ["R§6", "R§9"],
              "S5": ["R§6", "R§9", "R§10"], "YC": ["R§7", "R§8", "R§9", "R§10"], "S6": ["R§9", "R§12"],
              "S7": ["R§9", "R§12"], "S8": ["R§9", "R§12"], "FIX": ["R§9", "R§13"]}
ALWAYS_R = ["R§14", "R§15"]
KEYS = {"S1": ["series", "schemes", "Repositories", "Name clash", "intake", "text layer"],
        "S2a": ["instructions pages", "constants"],
        "S3": ["series", "instructions pages", "option letters", "worksheet", "text layer", "Name clash", "series tags"],
        "S5": ["schemes", "S5", "scheme pass", "Examiner instructions", "printed keys"],
        "YC": ["year check", "Year check", "normalis"],
        "S6": ["Classification", "classif", "granular", "S6", "archetype", "REGISTRY"],
        "FIX": ["Fix", "FIX"]}
KEYS["S4"] = KEYS["S3"]; KEYS["S7"] = KEYS["S8"] = KEYS["S6"]
QKEYS = {"S6": ["classif", "S6", "granular", "archetype", "code"], "S7": ["S7", "workbook", "derive"],
         "S8": ["S8", "year-close", "FILES"], "FIX": ["Fix", "FIX"]}
CAP = 26000      # most CONVENTIONS text printed in full; the rest stays in the index


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def section(text, tag):
    """The '## <tag> ...' section of a playbook or runbook, to the next '## ' heading."""
    m = re.search(r"(?m)^## " + re.escape(tag) + r"\b.*$", text)
    if not m:
        return None
    n = re.search(r"(?m)^## ", text[m.end():])
    return text[m.start(): m.end() + n.start()] if n else text[m.start():]


def entries(text):
    """CONVENTIONS as (line number, heading, lead, body): one per '- **lead**' bullet under its '## ' heading."""
    out, head, cur = [], "", None
    for i, line in enumerate(text.split("\n"), 1):
        if line.startswith("## "):
            if cur:
                out.append(cur)
            head, cur = line[3:].strip(), None
            out.append([i, head, "", line])            # the heading itself (lead "")
            cur = None
        elif line.startswith("- "):
            if cur:
                out.append(cur)
            m = re.match(r"- \*\*(.+?)\*\*", line)
            cur = [i, head, m.group(1) if m else line[2:80], line]
        elif cur:
            cur[3] += "\n" + line
        elif out:
            out[-1][3] += "\n" + line
    if cur:
        out.append(cur)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default=""); ap.add_argument("--year", default="")
    a = ap.parse_args()
    P = []
    say = P.append
    prog = read(os.path.join(V, "PROGRESS.md")) or ""
    open_lines = [l for l in prog.split("\n") if l.startswith("- [ ]")]
    live = [l for l in open_lines if "DEFERRED" not in l]
    stage, year = a.stage, a.year
    plans = sorted(glob.glob(os.path.join(MP, "PHY-09-*.md")))
    picked = ""
    if not stage:                                   # the plan in force names the order of work
        for path in plans:
            mo = re.search(r"(?m)^Pack order:\s*(.+)$", read(path) or "")
            for item in (mo.group(1).split(">") if mo else []):
                st, _, yr = item.strip().partition(":")
                if st in ("S6", "S7", "S8"):
                    todo = any(re.search(rf"\b{st}\b", l) and (not yr or f"Y{yr}" in l) for l in open_lines)
                elif st == "S1":
                    todo = bool(yr) and not re.search(rf"(?m)^- \[x\] Y{yr} S1\b", prog)
                else:
                    todo = any(f"Y{yr} {st}" in l for l in live)
                if todo:
                    stage, year, picked = st, year or yr, f"{item.strip()} (first step of {os.path.basename(path)} with work left)"
                    break
            if stage:
                break
    m = re.search(r"Y(\d{4}) (S2a|S2b|S\d|YC)\b", live[0]) if live else None
    if m and not stage:
        year = year or m.group(1)
        stage = m.group(2)
        picked = "the first open line of PROGRESS"
    stage = {"S2b": "S3"}.get(stage, stage) or "S5"
    if stage not in Y_SECTIONS:
        say(f"! unknown stage {stage!r}: printing the S5 pack; pass --stage with one of {', '.join(Y_SECTIONS)}")
        stage = "S5"

    say(f"# BOOT PACK · stage {stage} · year {year or 'all'} · chosen by: {picked or 'your --stage/--year'} · phy_boot.py edition {EDITION}")
    say("Selected text only; the full files are the authority. Read a whole section or entry when a step needs more "
        "(line numbers below). Pass --stage or --year for a different step.")
    card = read(os.path.join(V, "notes", "RULE-CARD.md"))
    if card:
        ed = re.search(r"(?m)^Edition [^\n]{0,60}", card)
        say(f"\nRule card (the readers' rules; readers read it themselves, {len(card):,} chars): "
            f"{ed.group(0).split(',')[0] if ed else 'edition line not found'}.")
    else:
        say("\n! MISSING V/notes/RULE-CARD.md: readers need it; see PHY-08 Y§0.")

    say(f"\n## PROGRESS · {len(live)} open line(s) to work on, {len(open_lines) - len(live)} DEFERRED to the closing sweep")
    mine = [l for l in live if year and f"Y{year} {stage}" in l]
    for l in (mine + [l for l in live if l not in mine]):
        say(l)

    now = datetime.datetime.now(datetime.timezone.utc)
    for path in plans:
        t = read(path) or ""
        u = re.search(r"(?m)^In force until:\s*(\S+)", t)
        expired = False
        if u:
            try:
                expired = now > datetime.datetime.fromisoformat(u.group(1).replace("Z", "+00:00"))
            except ValueError:
                pass
        if expired:
            say(f"\n## PLAN {os.path.basename(path)}: no longer in force (ended {u.group(1)}). Its order of work has ended; "
                "the work order of CLAUDE.md section 12 applies. Its upgrades stay (CLAUDE.md section 12).")
        else:
            say(f"\n## PLAN IN FORCE · {os.path.basename(path)} (follow its order of work)\n{t.strip()}")

    for name, tags in (("PHY-08-YEAR-PLAYBOOK.md", ["Y§0"] + Y_SECTIONS[stage]),
                       ("PHY-07-CLAUDE-CODE-RUNBOOK.md", R_SECTIONS[stage] + ALWAYS_R)):
        t = read(os.path.join(MP, name))
        if t is None:
            say(f"\n! MISSING {MP}/{name}: read it where the setup linked it."); continue
        heads = [h[3:].split(" · ")[0] + " " + h.split(" · ", 1)[-1][:60] for h in re.findall(r"(?m)^## .*$", t)]
        say(f"\n## {name} · sections printed: {', '.join(tags)} · all sections: " + " | ".join(heads))
        for tag in tags:
            s = section(t, tag)
            if s is None:
                say(f"! section {tag} not found in {name}: read the file."); continue
            if tag == "Y§0":                         # items 1 to 4; item 5 was the opening of Batch 7
                s = re.split(r"(?m)^5\. \*\*Opening steps", s)[0]
            say(s.rstrip())

    conv = read(os.path.join(V, "CONVENTIONS.md"))
    if conv is None:
        say("\n! MISSING V/CONVENTIONS.md")
    else:
        E = entries(conv)
        def wanted(e):
            lead = e[2] or e[1]
            if year and year in lead:
                return True
            subject_years = set(re.findall(r"(20\d\d)(?!-\d\d-\d\d)", lead)) - {year}
            return any(k in lead for k in KEYS.get(stage, [])) and not subject_years
        full, used = [], 0
        for e in E:
            if e[2] and wanted(e) and used + len(e[3]) <= CAP:
                full.append(e); used += len(e[3])
            elif not e[2] and wanted(e):          # a whole '## ' section whose heading matches
                body = [x for x in E if x[1] == e[1] and x[2]]
                if used + sum(len(x[3]) for x in body) <= CAP:
                    for x in body:
                        if x not in full:
                            full.append(x); used += len(x[3])
        say(f"\n## CONVENTIONS · {len([e for e in E if e[2]])} entries, {len(conv):,} chars · printed in full: "
            f"{len(full)} entries for {year or 'no year'} and stage {stage} ({used:,} chars) · binding in full all the same")
        for e in sorted(full):
            say(e[3].rstrip())
        say("\n### Index of every CONVENTIONS entry (line · lead); read one with: sed -n '<line>,+3p' V/CONVENTIONS.md")
        for e in E:
            mark = "*" if e in full else " "
            say(f"{mark}{e[0]:>4} · " + (("## " + e[1]) if not e[2] else e[2][:110]))

    qq = read(os.path.join(V, "QQUEUE.md"))
    if qq is not None:
        items = [l for l in qq.split("\n") if l.startswith("- [Q-") and "· open" in l.split("]")[0]]
        keys = ([year] if year else []) + QKEYS.get(stage, [])
        sel = [l for l in items if any(k in l for k in keys)] if keys else []
        say(f"\n## Q-QUEUE · {len(items)} open item(s); printed: the {len(sel)} that name {' / '.join(keys) or 'nothing'}. "
            "Another item: grep -n 'Q-<nnn>' V/QQUEUE.md")
        for l in sel:
            say(l)

    add = read(os.path.join(V, "notes", "PHY-03-ADDENDUM.md"))
    if add is not None:
        parts = re.split(r"(?m)^(?=### )", add)
        say(f"\n## Mistakes addendum · the two newest sections in full; every entry's lead below ({len(add):,} chars in the file)")
        for p in parts[-2:]:
            say(p.rstrip())
        say("\n### Leads of every entry")
        for l in add.split("\n"):
            mm = re.match(r"- \*\*(.+?)\*\*", l)
            if mm:
                say("- " + mm.group(1)[:120])

    if year:
        ny = read(os.path.join(V, "notes", f"Y{year}.md"))
        if ny is not None:
            hs = re.findall(r"(?m)^## .*$", ny)
            say(f"\n## notes/Y{year}.md · {len(ny):,} chars · not printed; sections: " + " | ".join(h[3:] for h in hs)
                + " · read a section only when a step needs it")
    out = "\n".join(P)
    print(out)
    print(f"\n[boot pack: {len(out):,} chars]")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:                      # never block a session: fall back to the reads of CLAUDE.md section 6
        print(f"! phy_boot.py failed ({type(ex).__name__}: {ex}). Use the fallback reads of CLAUDE.md section 6 step 2.")
        sys.exit(0)
