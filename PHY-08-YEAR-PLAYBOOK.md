# PHY-08 · YEAR PLAYBOOK · Physics (042)

*How to mine one year's printed documents, learned from 2026 (Batches 1 and 2). Every decision below was already made and tested on real papers: follow it, don't work it out again. Cited as Y§n. Written 2026-10-02 from the audit of the Batch 2 vault; updated 2026-10-05 from Batch 3 (PHY-VAULT-B03-20261005-1539-11354r.json): one thorough reading per paper, the year check (Y§11), the fixed planner. Shorthand as in PHY-07: `K` = `python3 /home/claude/pyqkit.py`, `G` = `python3 /home/claude/phy_gate.py`, `V` = `/home/claude/vault`, `<N>`/`<nn>` = the session batch.*

## Y§0 · The work order (her decision, 2026-10-02)
1. **Printed documents first, newest year to oldest:** 2025, then 2024, 2023, 2022 (Term 2 and Term 1). For each year: S1 intake (Y§2) → S2a constants (Y§3) → S3 origins and S4 siblings (Y§4) → S5 for every scheme of that year that is in the schemes repository (Y§5). Then the year check (Y§11). Then the next year whose files are attached, without waiting for her. Each paper gets one thorough reading (her decision 2026-10-03); each year gets one thorough check (her decision 2026-10-05).
2. **Deferred to the closing sweep** (after 2022's printed documents): each year's S5 lines for papers without a scheme (TRANSFERRED/INFERRED; they need S6 codes), S6 classification, S7 derive and workbook, S8 year-close, and 2026's open items (Q-010 sample-paper gaps, FILES statuses, the 53-code prediction's misses). The gate marks these lines `DEFERRED`; skip them when looking for the next line.
3. **Schemes not uploaded yet:** when a year's papers are done and its schemes are not in the schemes repository, tell her once which to upload, leave the S5 lines open, and go on to the next year's papers. Do the open S5 lines when the schemes appear. W-1 holds per S5 unit: a scheme is only ever applied to its own paper_id.
4. **Opening steps of the first session after 2026-10-05 (Batch 4):**
   - CONVENTIONS: a dated "Batch 4" section with two entries: *Year check* (her decision 2026-10-05: one thorough reading per paper with the extractor's second look, one thorough check per year, Y§11) and *Gate edition 2026-10-05* (`--single-read`; `yearcheck`; `--open-line`; the planner reads a letter series such as 55/S as a normal series and only the letter B as visually-impaired, gives a scheme file covering several sets one S5 line per set, and adds a YC line per year).
   - PROGRESS: the open line "Y2025 S5 papers with no scheme (…)" also lists main siblings whose schemes are in the combined PDFs. Find by script the 2025 papers whose new rows have no scoring lines (on 2026-10-05: 2025C-55S2 and 2025C-55S3 only) and rewrite the line's list to exactly those, keeping its DEFERRED tag.
   - Add the 2025 year-check line: `G checkpoint --message "2025 year-check line" --open-line "Y2025 YC year check: every row checked by script, then a blind re-reading of the suspects, the figure directions and a sample (PHY-08 Y§11)"`.
   - QQUEUE and PROGRESS "Open": close Q-022 (planner fixed, gate 2026-10-05). The single-reading items of 2025 ("merged without the double-read", from Q-023 on) stay open until the 2025 year check closes them.
   - Save with one checkpoint. Then the 2025 year check (Y§11) if the 2025 repositories are attached; if they are not, tell her once, leave the Y2025 YC line open, and go on to Y§2 for 2024.

## Y§1 · Pace benchmarks (Batch 2, gate log times)
- Sibling paper (S4), double-read included: 10 to 16 minutes each.
- Origin scheme (S5, every line): 15 to 37 minutes. Sibling scheme: 6 to 10 minutes.
- Origin paper (S3): not yet timed on this route (Batch 1 did them in the chat); expect about twice a sibling.
- The first trial papers took 38 and 47 minutes, mostly spent working out things this file now settles.
- Batch 3 (2025, one thorough reading from 2025-5513 on): sibling papers 13 to 27 minutes each, with the most detailed rows yet; about 9 hours of work in all, spread over three days by 70 hours of usage pauses. The plan's usage limit, not the work, sets the calendar.
- A paper running far past these means something settled here is being redone: stop, re-read the Y§ for the step, follow it.

## Y§2 · S1 intake and identity (once per year; the step that needs the most care)
1. `K inventory V /mnt/user-data/uploads /mnt/project --batch <N>` (boot already ran it). Papers and schemes may sit in several repositories, as ZIPs or loose PDFs; inventory reads them all. It records every new PDF and ZIP member, skips byte-identical files, and guesses kind, exam, year, paper code and paper_id with its evidence.
2. List the year's new rows:
   ```python
   import sys; sys.path.insert(0, '/home/claude'); import pyqkit as K
   for f in K.table('/home/claude/vault', 'l1/FILES.csv'):
       if f['batch'] == '<N>': print(f['file_id'], f['name'], f['where'], f['kind'], f['exam'], f['year'], f['paper_code'], f['paper_id'], f['pages'])
   ```
3. For every QP and MS row: render page 1 (`K render --vault V <file_id> 1 --dpi 200 --crop --out /home/claude/render/S1-<year>/<file_id>`) and read, from the image: the series code word (2026: QPSR1, R2SQP, PQS3R, RP4QS, R5QPS, S7PQR), SET number, Q.P. Code, a letter code for visually-impaired papers (55(B), 55(B)/7), the subject line; for schemes, the header "MARKING SCHEME ... Session ... Code" (on a value-point page when page 1 is a contents or instructions page, as in 2026).
4. Identity ERRATA, only where the image proves inventory wrong or weak (Batch 1 templates):
   - `year_evidence` → "pdf-meta:<y>; scheme-session:<session> (same code); zip-identity:<zip>" (a board paper prints no year: its year comes from the same-code scheme's session line, e.g. 2026 exams ↔ "Session 2025-26").
   - `note` → "identity confirmed on p1 image at B<nn> (series <code word>, set <n>)".
   - Compartment (supplementary) papers: `exam` COMPT, paper_id `<year>C-<code digits>`. Evidence: the ZIP, folder, repository or file name ("compartment", "supplementary"), confirmed on page 1 (their own series and code). Inventory files loose compartment PDFs as MAIN; correct them.
   - Letter codes: 55(B) → paper_code `55/B`, paper_id `<year>-55B`; 55(B)/7 → `55/B/7`, `<year>C-55B7`.
   - Year in a file name ≠ year on the page: the page wins. Year unprovable: `UNK`, Q-QUEUE item (CI§7).
   - Evidence on every row: what the page-1 image shows.
   Write them to `V/work/S1-<year>__ERRATA.csv`, then `G commit S1-<year> --stage OTHER`.
5. Scheme-year check (W-1): every scheme's session line matches the year's exams.
6. CONVENTIONS: a dated "Y<year> series (p1 images)" entry like Batch 1's "2026 series": code words, sets, letter-code papers, the compartment series.
7. `G checkpoint --message "Y<year> planned" --plan-year <year>` writes the year's PROGRESS lines from FILES: S1 ticked with computed counts; S2a; S2b; one S3 line per series origin (set 1 of each series, compartment included); one S4 line per series; one visually-impaired line; one S5 line per scheme; DEFERRED lines for papers without a scheme, S6, S7 and S8. It refuses while any identity is incomplete.

## Y§3 · S2a constants (one unit per year)
- Read every paper's instructions pages (pp 1–3) at 200 dpi; read each printed constant from a 300 dpi crop. 2026 had four wording variants of the instructions page across its 20 papers; note any variant in CONVENTIONS.
- One CONSTANTS row per printed constant per paper, exactly as the 2026 rows (`grep 2026-5511 V/l1/CONSTANTS.csv`).
- Check every value by script against its standard value (c, h, e, m_e, m_p, epsilon_0, mu_0, …): a difference is either a misread (re-read at 400 dpi) or a printed value to keep with a note.
- `V/work/S2A-<year>__CONSTANTS.csv` → `G commit S2A-<year> --stage OTHER --progress "Y<year> S2a"`.

## Y§4 · S3 origin papers, S4 siblings, visually-impaired and compartment papers
- The loop in CLAUDE.md §7: one thorough reading per paper (the R§6 brief with its second look), saved with `--single-read`; the blind reading happens once per year in the year check (Y§11). `--stage S3` for origins, `--stage S4` for the rest. One paper, one gate commit.
- A shuffle is a shuffle only when the wording and every value are identical. The 2025 year check's script found 2025-5553-Q29-ii stored as a shuffle of 2025-5551-Q29-iii although its stem and givens differ. When in doubt, a full row with a "resembles" note.
- Order: every S3 origin of the year (main series, then the compartment series), then S4 series by series, then the visually-impaired papers last, because they are compared with every series.
- Each paper's BLUEPRINTS row is written with it from its own instructions page and the choice positions printed in its body (2026 template: `sections=A:1-16:1;B:17-21:2;C:22-28:3;D:29-30:4;E:31-33:5`, `choice_rule=B:17;C:24;D:29,30;E:31,32,33`, `bp_class=P33`). A different year can have a different pattern: read it, never assume 2026's.
- Siblings: compare each question with the series rows on disk (a short script finds candidates by text; the crops decide). Identical wording and every number, unit, sign, option and figure value identical → shuffle; any difference → a full new row with note "resembles <id>: <what differs>" (CONVENTIONS "S4 method (B01)"). In 2026, 48 to 58 of each sibling's 64 to 73 rows were shuffles.
- Visually-impaired papers: compare with every series of the year. In 2026 both turned out to be separate papers (63 of 65 and all 66 questions matched no series question closely), so expect full rows with "resembles …" notes. Every row carries `extra` `series=<its series>; vi_paper=y` (kit 2026-09-30b); a question that is identical to a series question is still a shuffle. They have no figures (figures become words).
- Compartment: its own series with its own origin (set 1) and visually-impaired paper.

## Y§5 · S5 schemes
R§10, plus the conventions Batch 2 settled (CONVENTIONS "S5 scheme pass"):
- **Key rows:** an MCQ or assertion-reason answer is one `key` line, step_text the printed letter only, e.g. `(C)`, marks 1.
- **"Award full marks for attempting" or "no option is correct":** one `other` line with the printed words, not a key line (2026-5531-Q02, 2026-5553-Q03, 2026-5521-Q29-iii).
- **Combined mark cells** ("½ + ½" beside one line listing several items): one line per printed half.
- **Unmarked routes** ("Alternatively", "award full marks for any other correct …"): in `alt_accepted` of the line they belong to (2026: 201 lines).
- **Scheme symbols** that differ from the paper's are kept as printed; the mapping goes in `notes/Y<year>.md`.
- **Split box against line marks:** the marks printed beside lines decide; the box decides only a half printed between two parts; a conflict becomes a Q-QUEUE item (2026: Q-014, Q-016).
- **Physics errors in a scheme:** compute every numerical answer in Python. Keep the printed text and append "(sic; <correct working and value>)", on the line and on the FORMULAE `result` row (2026-5531-Q31A-ii: "= 8.85 J (sic; … U = 6 + 15 − 0.15 = 20.85 J)"), plus a notes line. A wrong key: the origin keeps the correct key; the scheme's printed key goes into a Q-QUEUE item (2026: Q-015).
- **Shuffles inherit:** lines only for the paper's `rel = origin` rows. Every part's lines must add up to its printed marks (all 1,222 lines of 2026 did).
- **"Award 1 mark to all students" / "give full marks for any choice":** one `other` line with the printed words (2025-5553-Q29-ii, Q-048; 2025C-55BS-Q29-iii, Q-037).
- **A description box against the line marks** (55/5/1 Q21, Q-049): the line marks are kept; the conflict is a Q-QUEUE item.
- **Two printed keys** for one MCQ (55/2/1 Q12): CONVENTIONS "Two printed keys (B03)". **A printed answer with no mark beside it** (SQP 2026-27): a marks-0 line.
- **One PDF for several sets** (2025): each set's section is its own S5 unit, the paper_id of that set. **A compartment scheme for set 1 only** (2025: 55/S/1): the other sets' new rows go to the DEFERRED "papers with no scheme" line.
- In the same unit, ERRATA setting the scheme file DONE. Commit with `--progress "Y<year> S5 scheme <code> ("`.

## Y§6 · The detail standard
Measured on 2026's sibling papers' new rows, the trial (xhigh) wrote figure descriptions of about 200 characters, 1.86 formula rows per numerical or derivation row, and notes on 61 % of rows; the overnight run (max) wrote 143 characters, 1.38 and 35 %. Both were equally accurate on values. Write every new row to the trial's level:
- **stem:** the complete printed text of the part, its printed sub-labels included, normalised per P§6.3.
- **givens and unknown** on every row that has quantities.
- **FIGURES:** every element named with its value and position, and every direction: which side each cell's longer plate faces, which way each diode and arrow points, current, field and ray directions, a graph's axes, labels, intercepts and shape.
- **FORMULAE:** `given` for each printed relation; `asked` for every relation the demand needs (a derivation's chain, not just its end); `result` from the scheme at S5.
- **note:** on every new sibling row "resembles <id>: <what differs>" or "new question"; on any row, every reading decision (text layer overruled, (sic), choice layout).
- **Notation:** the project's ASCII forms (sqrt(2), r_1, lambda_a, microF, vec(E), i^, 3e8). A plain v printed is a plain v, never vec(v).

## Y§7 · Traps 2026 actually hit
| Trap | Where | Guard |
|---|---|---|
| A cell's polarity read backwards from a small drawing | Batch 1, 55/3/1 Q17(a); fixed ER-B02-081/082 | measure plate lengths in a 400 dpi crop; the checker's direction notes (R§8 step 6) |
| Note text typed into the options column | Batch 2, 55/B/7, 36 rows; caught by the double-read | the gate refuses options on non-MCQ/AR rows |
| `rel` left blank on new rows | Batch 2, 55/5/2, 15 rows; fixed ER-B02-088..102 | the gate refuses a blank rel |
| vec(v) written where the page prints a plain v | Batch 1, 55/7/1 Q29(iii); fixed ER-B02-104/105 | notation check on every symbol |
| Numbers of a shared lead-in listed under every sub-part | Batch 2 checker readings | they belong to the first sub-part's row only |
| Text-layer damage: 10⁸ read "108", 30° read "300", decimal points dropped | Batches 1 and 2 | digits only from crops |
| A scheme's value or key wrong | 55/3/1 Q31 (8.85 J for 20.85 J), 55/5/2 Q11 (Q-015) | Python check of every numerical answer at S5 |
| Scheme split box against line marks | Q-014, Q-016 | line marks decide; Q-QUEUE |
| `pages`/`render` without `--vault` | Batch 2 | always `--vault V` |
| The planner read 55/S/1 as visually-impaired and ignored a scheme file's sets | Batch 3, Q-022 | fixed in gate 2026-10-05 |
| A row stored as a shuffle although its wording differs | Batch 3, 2025-5553-Q29-ii | the year check compares every shuffle with its origin |

## Y§8 · Saving usage without losing accuracy
- Don't open the source of `pyqkit.py`, `phy_gate.py` or `phy_code_env.py` to learn how they work; R§9 and this file are enough (the first Batch 2 session spent much of its time this way). A suspected kit bug is the only exception (R§11).
- Render a paper's English pages once at 200 dpi; crop only what carries digits, symbols or directions.
- Siblings: find candidates by a short script against the rows on disk; confirm on crops; never re-extract a shuffle from scratch.
- Keep judged notes to 2–4 lines per paper in `notes/Y<year>.md`, each with instance ids.
- Don't re-run what the gate runs (check-paper, validate, coverage).
- One fresh subagent per role per paper, given its brief and nothing else.
- What uses the most: page images (every whole-page render and every large crop is a full image to read), each subagent's reading at the start of its paper, and long thinking. The per-paper blind reading was the largest single cost and is gone; the year check re-reads about a fifth of a year instead of all of it.
- Crop tightly: one line or one figure costs a fraction of a page. Never render a page twice; reuse the PNGs in /home/claude/render/<pid>/pages.
- Shuffle candidates: the 200 dpi page and the text layer decide; crop only where a digit, exponent, sign or direction is small or the text layer disagrees. Every new row still gets its crops.

## Y§9 · Older years
- **2022** was a two-term year: Term 1 (MCQ, OMR sheet) and Term 2 (written) are separate papers with their own blueprint classes; paper ids `T1-2022-<code>` and `T2-2022-<code>` (CI§10). They feed presence and method, never structure (CI§7 "Old-pattern paper").
- **Every year:** read the instructions page; the blueprint class comes from the page. A year with a single paper is a full year.

## Y§10 · End of a year's printed pass
- Run the year check (Y§11) before the next year starts.
- When a script shows every paper of the year has a BLUEPRINTS row: `G checkpoint --message "every <year> paper has a BLUEPRINTS row (<n>/<n>)" --tick "Y<year> S2b"`.
- Report: papers and schemes done (gate numbers), open questions, and, if needed, the scheme swap: "schemes repository: delete the <year> scheme PDFs, upload the <next year> ones".
- Then Y§2 for the next year whose ZIP is in the papers repository.

## Y§11 · The year check (her decision 2026-10-05)
Each paper gets one thorough reading (CLAUDE.md §7); each year then gets one thorough check, aimed where errors hide.
1. `G yearcheck <year>`. Tier 1, by script, every row of the year: coverage (figures, formulae, cases, blueprints); four options on every MCQ; every shuffle identical to its origin; every scoring line adding up to its printed marks and a key line on every MCQ; and every number of every row compared with the PDF's own text layer (a check only: values come from images). It writes `YC-<year>__SUSPECTS.csv` (every finding); `__SKELETON.csv` (the question rows to re-read: every suspect, every figure with a direction — cells, diodes, arrows, polarity, a field into or out of the page — and a sample of 10 %, at least 2, of each paper's new rows); and `__SKELETON-S5.csv` (scheme parts: every suspect and a 10 % sample of each paper's scored rows). On 2025's data it lists 154 question rows and 87 scheme parts, about a fifth of the year.
2. A fresh blind checker subagent with the R§7 brief, once for `__SKELETON.csv` (it writes `__VERIFY.csv`) and once for `__SKELETON-S5.csv` with the R§10.1 differences (it writes `__VERIFY-S5.csv`). If the Agent tool lets you choose the subagent's model, a model different from yours makes the second reading more independent.
3. `G yearcheck <year> --compare`. Settle every mismatch from a 400 dpi crop (R§8): the vault right (`extractor_right`), or wrong, fixed by a FIX unit (R§13) whose ERRATA reasons start with `YC-<year>:`, then `part_fixed`, then compare again.
4. **Escalation.** A real error among a paper's sampled rows means that paper's single reading was not clean: `G yearcheck <year> --paper <pid> --all`, the blind checker on every new row of that paper, `--paper <pid> --compare`, settle (unit `YC-<year>-<pid>`).
5. When the compare exits 0 it writes `outputs/reports/PHY-YEARCHECK-<year>.md`. Close the year's single-reading Q-QUEUE items; append the year's lessons to `notes/PHY-03-ADDENDUM.md` (what the check found, by kind, each with its guard); save with `G checkpoint --message "Y<year> year check done" --tick "Y<year> YC"`.
6. Then the next year.
