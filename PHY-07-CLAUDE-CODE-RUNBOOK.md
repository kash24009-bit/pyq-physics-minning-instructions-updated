# PHY-07 · CLAUDE CODE RUNBOOK · Physics (042)

*How the mining runs in Claude Code. CLAUDE.md holds the rules; this file holds the procedures. Cited as R§n. Written 2026-09-30 for kit edition 2026-09-30b. Every command below was run in a three-repository simulation on that date (setup, extraction check, sealing, blind check with planted errors, settling, commit, push, refusals, checkpoints). Updated 2026-10-01 after the Batch 2 trial and 2026-10-02 after its audit (PHY-08 holds the year procedure; browser-renamed copies; `--plan-year`, `--defer-year`; two new refusals): `--vault` on page commands, a role for a schemes-only repository, earlier session branches carried forward, the dashboard, the checker's notation, scope and direction notes, standing fixes.*

Shorthand: `K` = `python3 /home/claude/pyqkit.py` · `G` = `python3 /home/claude/phy_gate.py` · `V` = `/home/claude/vault` · `<N>` = the session batch the setup printed (`<nn>` = the same number with two digits) · `<pid>` = a paper_id · `<outputs>` = `/mnt/user-data/outputs` (a link into the project repository's `outputs/`). `pages` and `render` always take `--vault V`: without it they cannot find a document by file_id.

## R§0 · Reading order
- Every session: CLAUDE.md, then PHY-08 (the year playbook), then this file in full, then the files CLAUDE.md §6 lists.
- Before each stage, and after any compaction: this file's section for that stage again.

## R§1 · The first Claude Code session (Batch 2, the trial; done 2026-10-01, never repeat it)
Once, in this order, before the first paper:
1. Boot (CLAUDE.md §6). Expected: restored vault batch 1, 2,088 rows, 744 question rows, validate 16/16; kit edition 2026-09-30b, taken from the instructions repository (the vault still carries 2026-09-30 until the first pack ships the new edition inside it). Anything different: one line in the report, then continue from the vault as restored.
2. S1b (R§4.4): the scheme PDFs, and any other file the chat saw only as a 924-px bundle, arrive from GitHub as originals with new FILES rows. Give each its twin's identity.
3. Log the route change with the texts in R§1.1.
4. `G commit S1B --stage OTHER --progress-new "Y2026 S1b originals from GitHub matched to their bundle copies"`. If inventory added no file needing a match: `G checkpoint --message "route change logged" --progress-new "Y2026 S1b: no originals to match"`.
5. The trial papers named in her kickoff message, each through the loop in CLAUDE.md §7.
6. The trial report (R§15.2), then `G checkpoint --message "trial report"`.

### R§1.1 · Texts for the first session (fill the placeholders)
Append to `V/CONVENTIONS.md`:
```
## <date> (UTC) · Batch <N> · Claude Code route
- **Route.** Mining moved to Claude Code cloud sessions over three GitHub repositories found by content: instructions (read only), project (vault file and the year's schemes; the only repository committed to), papers (question-paper ZIPs; read only). The chat project audits read only while Claude Code mines; its findings arrive as `Fix:` lines (one writer at a time).
- **Checkpoint.** `phy_gate.py` merges part files, writes the status erratum and the PROGRESS line with counts computed from the tables, validates, packs into `outputs/vault/` of the project repository, commits and pushes after every paper. This replaces the auto-vault database and her manual vault swap. `STATE.json` gains the key `cc_session` (additive).
- **Double-read.** From Batch <N>, every paper's marks, numbers, options and figure values are read twice: by an extractor and by a blind checker who sees only the row skeleton. The gate compares the two readings; every mismatch is settled from a 300-400 dpi crop and logged (`outputs/logs/GATE-LOG-B<nn>.md`, `outputs/logs/doublecheck/`).
- **Originals.** Files the chat saw as 924-px bundles now come from GitHub as original PDFs with their own FILES rows; each takes its twin's identity through ERRATA (S1b). Scoring lines are read from the originals.
- **Kit edition 2026-09-30b** (made and tested in the chat on 2026-09-30, first used at Batch <N>): a row may name its series in `extra` as `series=55/3`; V07 and `similar` use it. The letter-code visually-impaired papers carry it on every row: 2026-55B `series=55/3; vi_paper=y`, 2026C-55B7 `series=55/7; vi_paper=y`, so their unchanged questions are shuffles of their own series and are not counted twice. Tests: validate 16/16 on the Batch 1 vault; a 55B shuffle of a 2026-5531 row passes V07 only with the key; a 55B7 row with `series=55/7` pointing at a 55/3 row fails.
```
Append to `V/QQUEUE.md` (the next two free numbers; Q-008 was the last on 2026-09-30):
```
- [Q-009 · <date> · open · CI conflict] The Custom Instructions still describe the chat route (Artifact auto-vault, present_files, vault file in project knowledge, `Audit.` writing ERRATA). While Claude Code mines, CLAUDE.md and PHY-07 govern process and the chat audits read only. Update CI§3, §4, §6 and §9 wording at the next edit.
- [Q-010 · <date> · open] Batch 0 left 6 SQP 2025-26 rows with has_figure=y and no FIGURES row (SQP2526-042-Q18-II, -Q27A-B, -Q27A-C, -Q30-II, -Q33B-A-ii, -Q33B-A-iii) and 2 NUM/DRV rows with no FORMULAE row (SQP2526-042-Q26, -Q32A-A). Definition of Done line 7 fails on them: write them from the SQP page images before S8 (R§12).
```
Append to `V/notes/PHY-03-ADDENDUM.md` (W-14 to W-16; if the last entry there is not W-13, take the next free numbers):
```
### Part 3 additions (Batch <N>, Claude Code route)
- **W-14 · Two miners writing one vault** (the chat and Claude Code at once): restore keeps only the newest copy, so the other one's work vanishes silently.
  → One writer at a time: Claude Code mines; the chat audits read only and sends `Fix:` lines → CLAUDE.md §3, PHY-07 R§13
- **W-15 · An agent that can run code is tempted to fill rows from the text layer with a script.**
  → Every value is read from a page image; the text layer only cross-checks digits; a blind second reading is compared by the gate before any merge → CI§2.2, PHY-07 R§6-R§8
- **W-16 · A long session compacts and loses rules held only in conversation.**
  → Rules live in CLAUDE.md (re-read after compaction); state lives on disk (PROGRESS, part files, pushed packs) → CLAUDE.md §9
```

## R§2 · The setup script (`phy_code_env.py`)
- Run it as CLAUDE.md §6 says. The first run takes a few minutes (packages). It never edits a file she put in a repository.
- A repository holding only PDFs (her schemes repository) gets the role `schemes` and is linked into `/mnt/project`.
- If the newest vault sits on an earlier session's branch, the setup merges that branch into this session's branch, so every earlier report, log and pack stays together on the newest branch. A merge that would conflict is undone and reported.
- Tool and instruction files a browser saved as `phy_gate (1).py` or `PHY-07-CLAUDE-CODE-RUNBOOK (1).md` are also linked under their plain names in `/mnt/project`. When two copies exist, the newest commit wins (for the gate, the newest `GATE_EDITION`), and a warning names the extra copies. CLAUDE.md must carry its exact name; a misnamed one is only warned about.
- It prints: the three roles with branch and commit; the folder links; every vault candidate found in working trees and on all branches, with the CHOSEN one and the stale ones; the kit edition and where it came from (the newest edition wins; a tie goes to the vault's own copy); this session's batch and why; the validate line; `pyqkit status`; warnings. It writes `/home/claude/phy_env.json` (never edit it by hand) and links `/home/claude/phy_gate.py`.
- The batch: if the newest vault was packed by this same Claude Code session (its `cc_session` matches), the batch stays; otherwise it is the restored batch + 1. Only if that reasoning is wrong for a reason you can state: `PHY_BATCH=<n> python3 …` and say why in the report.
- Rerun it only when the cloud machine was replaced (your files are gone).

| Warning | Do |
|---|---|
| several CLAUDE.md files | Name the others in the report; she deletes them. This file's instructions-repository copy is the one that counts. |
| no file named exactly CLAUDE.md | First line of your report: she renames it (Claude Code loads only CLAUDE.md by itself). Read the misnamed file by its path meanwhile. |
| name clash | Two different files share a name; the first was linked. Open the other by its full path. |
| git fetch failed | Vault copies on other branches may be missing; say so once and continue with what was found. |
| no papers repository | Paper stages wait; scheme, classification and derive work continues. |
| python packages MISSING | Rerun once. If pages still cannot render, stop paper work and say so in one line. |

## R§3 · Reading a page
Commands (the kit opens documents by `file_id`; CONVENTIONS "Documents are opened by file_id"):
- `K pages --vault V <file_id>`: the page table (language, text characters, visual flag) and the pages to view.
- `K render --vault V <file_id> <pages> --dpi 200 --crop --out /home/claude/render/<pid>/pages`: whole pages; `<pages>` is `5`, `5-9`, `5,7,9` or `all`. Look at every PNG with the Read tool.
- `K render --vault V <file_id> <page> --dpi 300 --region x0,y0,x1,y1 --out /home/claude/render/<pid>/<label>`: a crop; the region is in fractions of the page (`0,0.40,1,0.62` = full width, 40–62 % down). Use 400 dpi for small superscripts, dense circuits and scheme half-marks. Every crop gets its own `--out` folder: the kit names files `p<page>.png`, so a shared folder overwrites earlier crops.
- `K pages --vault V <file_id> --text <page>`: the text layer of one page, for the digit cross-check only.

Rules:
1. Digits are never taken from a whole-page view. Every number, unit, exponent, sign, option, figure value and half mark is read from a crop.
2. Dual-read (P§6.1): structure from the image; every digit cross-checked against the text layer; a conflict gets a closer crop; still unsure → an UNREADABLE row (`LOWRES`) and a note. Known text-layer damage: 10⁸ read as "108", hν as "h", ¹⁶₈O as "168O", 30° as "300", B₁/B₂ as "B and B", dropped decimal points ("38 eV" for 3.8 eV).
3. Bilingual originals: English pages only. The page table marks the Hindi pages "en" because their text layer is not Unicode; decide from the image (CONVENTIONS "Bilingual originals"). A Hindi page is the backup for a damaged English one (`read_from = hi-translation`).
4. Scans with no text layer (the scheme PDFs): dual-read is impossible; say so in the note and use 300–400 dpi crops.
5. If `render --vault V <file_id>` cannot find the document, find the file by its sha256 under `/mnt/user-data/uploads`, `/mnt/project` and `V/work/_intake`, and pass the path instead.

## R§4 · Part files, ids, templates, S1b
### R§4.1 · Part files
- `V/work/<unit>__<TABLE>.csv`; `<unit>` is the paper_id for paper work, or a label (`S1B`, `FIX-3`, `S6-CH02`, `TR-2026C-5571`, `S8-FILES`, `SQP-GAPS`).
- TABLE: INSTANCES, FIGURES, FORMULAE, CASES, BLUEPRINTS, UNREADABLE at S3/S4; STEP-AWARDS (+ FORMULAE results, + ERRATA statuses) at S5; ERRATA for corrections; CLASSIFY at S6.
- Header = the first line of the vault's own table (`head -1 V/l1/INSTANCES.csv`; CLASSIFY is `V/j/CLASSIFY.csv`), same column order. Write with Python's `csv.DictWriter`, never by joining strings.
- `batch` = `<N>` on every row that has the column.
- CONSTANTS: all 20 papers of 2026 already have them (Batch 1, S2a). Never write them again.

### R§4.2 · Ids (CI§10, Batch 1 style)
| What | Format | Example |
|---|---|---|
| question part | `<pid>-Q<nn><side>[-<part>…]`, question number with two digits | `2026-5532-Q08`, `2026-5532-Q24B-b`, `2026-5532-Q22A-b-i` |
| figure | `F-<pid>-<nn>` | `F-2026-5532-01` |
| formula | `EQ-<pid>-<nnn>`, continuing after the paper's last number | `EQ-2026-5532-001` |
| case | `CS-<pid>-Q<nn>` | `CS-2026-5532-Q29` |
| choice pair | `OR-<pid>-Q<nn>` | `OR-2026-5532-Q31` |
| erratum | `ER-B<nn>-<nnn>`, the next free number of this batch (the gate's own status errata take numbers too) | `ER-B02-007` |
| scoring line | `SA-<instance_id>-<nn>` | `SA-2026-5532-Q24A-02` |

### R§4.3 · Templates: real Batch 1 rows of 2026-5512 (match them field for field; blank fields omitted)
- **Shuffle row:** instance_id=2026-5512-Q08 · paper_id=2026-5512 · file_id=FL-bbc9339e7e · year=2026 · exam=MAIN · paper_code=55/1/2 · q_no=8 · section=A · q_marks_printed=1 · chapter=02 · topic_id=T-02-08 · q_type=MCQ · command_verb=The ratio of electric fields ... will be · has_figure=n · wants_figure=n · wants_graph=n · givens=spheres of radii r_1, r_2 joined by a conducting wire; separation >> radii · unknown=E_A/E_B at the surfaces · options=A) r_1/r_2 | B) r_2/r_1 | C) r_1^2/r_2^2 | D) r_2^2/r_1^2 · stem=A conducting wire connects two charged metallic spheres A and B of radii r_1 and r_2 respectively. The distance between the spheres is very large compared to their radii. The ratio of electric fields, (E_A/E_B) at the surfaces of spheres A and B will be · source_page=7 · read_from=image · rel=shuffle · rel_to=2026-5511-Q02 · syllabus_status=IN · note=shuffle of 2026-5511-Q02, text and numbers identical on the page image · batch=1
- **New MCQ row:** instance_id=2026-5512-Q01 · … q_no=1 · section=A · q_marks_printed=1 · chapter=02 · topic_id=T-02-01 · q_type=MCQ · command_verb=The potential difference ... is · givens=vec(E) = 4x i^ N/C; A at x = 1 m, B at x = 3 m · unknown=V_A - V_B · options=A) -16 V | B) 16 V | C) -8 V | D) 8 V · stem=In a region electric field is given by vec(E) = 4x i^ N/C. The potential difference between points A (x = 1 m) and B (x = 3 m), (V_A - V_B) is · source_page=5 · read_from=image · rel=origin · syllabus_status=IN
- **New NUM part row:** instance_id=2026-5512-Q18-a · q_no=18 · part=a · section=B · q_marks_printed=2 · chapter=11 · topic_id=T-11-05 · q_type=NUM · command_verb=Find the ratio · givens=alpha particle and proton moving with the same velocity · unknown=lambda_a/lambda_p · stem=Find the ratio (lambda_a/lambda_p) of de Broglie wavelength lambda_a associated with an alpha particle to de Broglie wavelength lambda_p associated with a proton if both are moving with the (a) same velocity · source_page=13 · read_from=image · rel=origin
- **BLUEPRINTS:** paper_id=2026-5512 · year=2026 · exam=MAIN · n_questions=33 · total_marks=70 · sections=A:1-16:1;B:17-21:2;C:22-28:3;D:29-30:4;E:31-33:5 · choice_rule=B:17;C:24;D:29,30;E:31,32,33 · calculators=n · constants_listed=y · bp_class=P33 · reading_time=15 min (cover note V) · source_page=3
- **FIGURES:** figure_id=F-2026-5512-01 · instance_id=2026-5512-Q24B-b · fig_type=circuit · printed_or_demanded=printed · description=Resistor network between terminals A and B: A to M 2R; M to O R (lower); … N to B 3R. [same figure as F-2026-5511-01] · values=2R, R, R, R, R, R, 3R · source_page=17 · from_image=y
- **FORMULAE:** formula_id=EQ-2026-5512-002 · instance_id=2026-5512-Q17A · role=asked · formula=single-slit minima y_n = n*lambda*D/a; coincidence n_1*lambda_1 = n_2*lambda_2 · quantities=y, n, lambda, D, a · units=m · source=QP · source_page=13 · from_image=y
- **CASES:** case_id=CS-2026-5512-Q29 · paper_id=2026-5512 · q_no=29 · context=(two sentences) · chapter=11 · n_subparts=4 · subpart_types=MCQ,MCQ,MCQ,MCQ · attempt_rule=all four; internal choice inside (IV): an OR alternative printed without its own label · source_page=19
- `extra` keys already in use (same key for the same situation; `grep` the vault's INSTANCES to see how): ARSET, choice_in_part, figure_page, marks_from, options_page, options_pages, printed_split; from Batch 2 also series and vi_paper (R§5). Several keys are joined with "; ".

### R§4.4 · S1b: originals of files the chat saw as bundles
List the candidates:
```python
import sys; sys.path.insert(0, '/home/claude'); import pyqkit as K
v = '/home/claude/vault'; F = K.table(v, 'l1/FILES.csv')
twins = {f['name']: f for f in F if f['fmt'] == 'bundle'}
for f in F:
    if f['batch'] == '<N>' and f['name'] in twins:
        t = twins[f['name']]
        print(f['file_id'], f['name'], f['pages'], '<- twin', t['file_id'], t['kind'], t['paper_id'], t['pages'], t['status'])
```
For each pair with the same name and the same page count, confirm on the original's page-1 image (200 dpi) that it is the same document (code, session, title). Then write ERRATA rows on the new row:
- for each of `kind, exam, year, year_evidence, paper_code, paper_id, sets_covered` whose value differs from the twin's: old = the new row's value, new = the twin's value (`year_evidence`: the twin's text + "; original of <twin file_id>, same document on the p1 image");
- `status`: a scheme original stays NEW (its S5 commit sets it and its twin DONE, R§10); the sample-paper original becomes IN-PROGRESS like its twin; the syllabus original becomes DONE like its twin;
- `note`: "original PDF of <twin file_id>; read this file from Batch <N> on".

Evidence on every row: what the p1 image shows. Write them all to `V/work/S1B__ERRATA.csv` and commit as R§1 step 4. A different page count or a different first page means it is not a twin: normal intake (P§5, CI§7).

## R§5 · What goes into the rows at S3 and S4
The authority is PHY-02 §6–§7 and the vault's CONVENTIONS.md (Batch 0 and Batch 1 sections, read in full). This list repeats what the Batch 1 rows show; it does not replace them.
- One row per printed part label ((I), (II), (A), (B), (a), (i) …): CONVENTIONS "Part rows"; printed sub-labels inside a part get their own rows (`-Q22A-b-i`). Two separate demands in one stem: `-d1`/`-d2` (CI§7).
- Sides and choices exactly as CONVENTIONS "Sides printed as (a) OR (b)" and "Choice inside a case sub-part (2026 boards)" say; OR pairs get `choice_pair_id`.
- `q_marks_printed` on every row; `marks_part` only where a mark is printed beside that part; never split marks yourself (CI§2.6). Halves as decimals (0.5) or ½, never 1/2 (the kit cannot read 1/2).
- `command_verb`: the printed demand words, `...` for the elided middle. `stem`: the full printed text of the part, normalised as P§6.3 and the templates. `givens`/`unknown` wherever quantities are printed.
- `options` for every MCQ: `A) … | B) … | C) … | D) …`. The first assertion–reason row of a paper carries the printed option set in `extra` as `ARSET=…`.
- `has_figure`, `wants_figure`, `wants_graph` as the page shows. A FIGURES row for every printed figure (netlist, ray or graph description + values); a shared case figure has one full description on the first dependent row and pointer rows after (CONVENTIONS "A shared case figure").
- FORMULAE: `given` for printed relations, `asked` for the relation a printed demand requires (CONVENTIONS "FORMULAE role asked"); every NUM and DRV row has at least one.
- CASES for each case-based question: two-sentence context, attempt rule as printed.
- `chapter`, `topic_id`, `syllabus_status` from the vault's syllabus table (PHY-05); Class 11 content `chapter = X11`; deleted topics kept with their status (CI§7).
- BLUEPRINTS from the paper's own instructions page; choice positions from the body (`choice_rule`); `reading_time` from the cover note.
- `read_from = image` for original PDFs (`bundle-image` was for the 924-px bundles).
- A misprint is transcribed as printed with `(sic)` and a note (CI§7).

**S4 sibling method** (CONVENTIONS "S4 method (B01)"): match each printed question to the series rows already in `V/l1/INSTANCES.csv` (text similarity may find candidates; values never come from the text layer). Then, on the crops:
- wording and every number, unit, sign, option and figure value identical → a **shuffle** row: a copy of the origin row with this paper's instance_id, file_id, paper_code, q_no, side/part as printed, section, choice_pair_id, case_id and source_page; `rel = shuffle`, `rel_to = <origin instance_id>`, note "shuffle of <id>, text and numbers identical on the page image"; its FIGURES and FORMULAE rows copied with this paper's ids and pages;
- any difference, however small → a full new row (`rel = origin`) with note "resembles <id>: <what differs>".

**Visually-impaired letter-code papers** (2026-55B, 2026C-55B7): every row carries `extra` `series=55/3; vi_paper=y` (2026C-55B7: `series=55/7; vi_paper=y`). Unchanged questions are shuffles of their own series; a question rewritten for visually-impaired candidates (a figure turned into words, a different question) is a full row with note "VI adaptation of <id>". Alternatives printed for visually-impaired candidates inside a normal paper follow CONVENTIONS "VI alternatives" (`vi_alt = y`).

## R§6 · The extractor brief
Start a fresh subagent (the Agent tool) with this brief as its whole task, placeholders filled. Give it nothing else from your context.
```
You are the EXTRACTOR for one paper of the Physics (042) PYQ mining project. CLAUDE.md is in your context; its rules bind you.
Paper: <pid> · file_id <file_id> (<file name>) · stage <S3 origin | S4 sibling of series <series>, origin <origin pid>> · batch <N>.

Read first, from disk: /mnt/project/PHY-07-CLAUDE-CODE-RUNBOOK.md sections R§3, R§4 and R§5; /home/claude/vault/CONVENTIONS.md in full; /mnt/project/PHY-02-PROTOCOL.md §6 and §7.

Then:
1. python3 /home/claude/pyqkit.py pages --vault /home/claude/vault <file_id> ; decide the English pages from the text and the images.
2. Render the English pages (python3 /home/claude/pyqkit.py render --vault /home/claude/vault ...) at 200 dpi with --crop into /home/claude/render/<pid>/pages and look at every one.
3. For every printed question part: render a 300 dpi crop (400 for small superscripts or dense figures), each in its own folder under /home/claude/render/<pid>/, and read every number, unit, exponent, sign, symbol, option and figure value from the crop. Cross-check the digits against the text layer (pyqkit.py pages --vault /home/claude/vault <file_id> --text <page>); a conflict gets a closer crop.
4. S4 only: compare every question with the series rows on disk (/home/claude/vault/l1/INSTANCES.csv, FIGURES.csv, FORMULAE.csv), never from memory, and write shuffle or full rows exactly as R§5 says.
5. Write the part files in /home/claude/vault/work/ (R§4): <pid>__INSTANCES.csv, __FIGURES.csv, __FORMULAE.csv, __CASES.csv, __BLUEPRINTS.csv, and __UNREADABLE.csv only if something is unreadable. Never CONSTANTS.
6. Run: python3 /home/claude/phy_gate.py check <pid> --stage <S3|S4> ; fix every listed problem against the images; repeat until it prints CHECK PASS.
7. Stop there. Do not run skeleton, verify or commit, and do not touch git.

Return, in at most 12 lines: rows per file; shuffle and new counts; the English pages read; every doubt you settled and how; anything unreadable; the CHECK PASS line.
```

## R§7 · The blind checker brief
After `G skeleton <pid> --stage <S3|S4>`, start a second fresh subagent with this brief. Never pass it the extractor's report.
```
You are the BLIND CHECKER for one paper of the Physics (042) PYQ mining project. CLAUDE.md is in your context; its rules bind you.
Paper: <pid> · file_id <file_id> · batch <N>.
Your only input is /home/claude/vault/work/<pid>__SKELETON.csv: which row is which printed part, and on which page. Do not open any other file in /home/claude/vault/work/ or /home/claude/.sealed/, nor the vault's l1/ tables, nor any earlier reading of this paper. Your reading is valuable only because it is independent.

Read /mnt/project/PHY-07-CLAUDE-CODE-RUNBOOK.md R§3 and R§7 first. For every skeleton row, read the part on its page (200 dpi pages; a 300-400 dpi crop for every number, each crop in its own folder under /home/claude/render/<pid>/check/). Write /home/claude/vault/work/<pid>__VERIFY.csv with Python's csv module, columns:
instance_id, marks_part, q_marks_printed, numbers, options, figure_values, note
- marks_part: the marks printed beside this part only; blank if none are printed there.
- q_marks_printed: the question's printed total.
- numbers: every number printed in this part's own question text, each with its unit or the symbol it belongs to, in reading order, separated by " | ". Powers of ten as 3 × 10^8 (or 3e8); fractions as printed (1/2); degrees as 30°; keep signs; include numbers inside expressions (for E = 4x i^ write 4x). Leave out question numbers, marks and part labels; subscripts are labels, not numbers (write r_1). A number printed once in a shared lead-in or case passage belongs to the first sub-part's row only; leave it out of the later sub-parts. Leave out sub-labels such as (1) or (i).
- options: for an MCQ, every option: A) ... | B) ... | C) ... | D) ..., written in the project's ASCII notation as its rows are (sqrt(2), r_1, 2*p_2, lambda_a, microF, microC, vec(E), i^): Greek letters, roots and unit prefixes spelled out, subscripts with _.
- figure_values: every value printed in a figure that belongs to this part (2 ohm | 6 V | 30°); "same as <instance_id>" if that figure was listed for an earlier row; blank if there is no figure. In note, also write the direction of every cell (which side its longer plate faces), diode, arrow, current or field drawn, e.g. "E_2: longer plate toward C; D_1 points right".
- note: anything you could not read. For every printed part on these pages that the skeleton lacks, add a row whose instance_id is <pid>-Q<nn>-extra and whose note starts "MISSING:" followed by what and where.

Return, in at most 8 lines: rows written, pages read, MISSING rows, anything unreadable.
```

## R§8 · Settling mismatches
1. `G verify <pid> --stage <S3|S4|S5>` lists each mismatch (also in `V/work/<pid>__DIFF.csv`).
2. For each one, render a 400 dpi crop of exactly that spot into its own folder (`/home/claude/render/<pid>/adj-<n>/`) and read it yourself. The crop decides; never majority, memory or the text layer alone.

| Decision | When | Then |
|---|---|---|
| `extractor_right` | The part file matches the page; the checker misread. | Record it. |
| `part_fixed` | The page shows the checker's value, or a third value. | Correct the part file (csv module); record it. The mismatch must be gone at the next verify. |
| `unreadable_logged` | Neither reading can be confirmed at 400 dpi. | Write `UNK` in the part file, add an UNREADABLE part row (`LOWRES`), record it. |
| `part_added` | The checker found a real printed part the extractor missed. | Add the full row (and its figures and formulae) to the part files; `final_value` = its instance_id. |
| `not_a_part` | The "missing" part is not a separately printed part. | Record it. |

3. Record each decision in `V/work/<pid>__ADJUDICATE.csv`, columns `instance_id,field,decision,final_value,crop,note` (`field` as printed by verify; `crop` = the path of the PNG you read: the gate refuses a decision whose crop does not exist).
4. A mismatch of field `row` (the checker skipped a part) is not settled by a decision: start a fresh checker for those skeleton rows only and append its rows to VERIFY.
5. Rerun `G verify` until it exits 0.
6. Directions: compare the checker's direction notes with the FIGURES descriptions. Settle every difference from a 400 dpi crop (measure plate lengths by script when the drawing is small, as the Batch 2 trial did), correct the part file if it is wrong, and record it in ADJUDICATE with field `figure_direction`.
7. `G commit`. Every decision is copied into the gate log and `outputs/logs/doublecheck/`.

## R§9 · The gate (`phy_gate.py`)
| Command | Does |
|---|---|
| `G check <unit> --stage S3\|S4\|S5\|OTHER` | Schema, ids, batch, coverage (figures, formulae, cases, blueprint), a rel on every row, options only on MCQ and AR rows, then a trial merge into a copy of the vault with check-paper and validate. Changes nothing. |
| `G skeleton <unit> --stage S3\|S4\|S5` | Writes `<unit>__SKELETON.csv` and moves the part files to `/home/claude/.sealed/<unit>/`. |
| `G verify <unit> --stage …` | Brings the sealed files back, compares them with VERIFY (+ ADJUDICATE), writes DIFF. |
| `G commit <unit> --stage … [--progress "<text in the line>" \| --progress-new "<new line>" \| --no-progress] [--unverified "<reason>"]` | check + verify + trial merge, then the real merge (rolled back if anything fails), status erratum (S3/S4), PROGRESS line with computed counts, validate, pack into `<outputs>/vault/`, archive of the part files to `V/work/done/`, gate log, git commit and push. An S5 commit must name its line (`--progress "S5 scheme 55/1/1 ("`) or say `--no-progress`. `--unverified` is only for when no checker could run (R§16); it adds a Q-QUEUE item. |
| `G checkpoint --message "…" [--progress-new "…" \| --tick "<text in an open line>"]` | validate + pack + gate log + commit + push, for work that is not a part-file merge (text files, REGISTRY, ticking a line a script has proved). |
| `G checkpoint --message "Y<year> planned" --plan-year <year>` | After a year's S1 identity commit: writes the year's PROGRESS lines from FILES (PHY-08 Y§2 step 7). Refuses while an identity is incomplete. |
| `G checkpoint --message "<reason>" --defer-year <year>` | Marks every open line of that year DEFERRED to the closing sweep. |
| `G push` | Retry the push. |
| `G show` | What waits in `V/work/` and what is sealed. |

| Exit | Means | Do |
|---|---|---|
| 0 | Done | Next step. |
| 1 | Mismatches not settled | R§8. |
| 2 | Refused | Read each `x` line, fix the part file against the images, rerun. |
| 3 | Merge failed; the vault was rolled back to before this commit | Read the message, fix, rerun. If the kit itself is wrong, R§11. |
| 4 | Committed, push failed | `G push`; if it fails again, keep working and report it. |

Outputs: `<outputs>/vault/` keeps the newest three packs of this route (chat-era files are never deleted); `<outputs>/logs/GATE-LOG-B<nn>.md`; `<outputs>/logs/doublecheck/B<nn>/` (SKELETON, VERIFY, DIFF, ADJUDICATE of every unit); `<outputs>/README.md`, the dashboard, rewritten at every commit and checkpoint from the vault (status, every paper's counts, links to every report, log and the newest vault). The gate prints its link; copy it into your report.

## R§10 · S5: scoring lines from the schemes
- One unit per scheme: the paper_id of the paper it marks (55/1/1 → `2026-5511`). Read the **original** scheme file (its S1b row), never the bundle. The schemes are scans: no dual-read; every mark and half mark from a 400 dpi crop.
- The examiner-instructions pages: to CONVENTIONS and register R14 (PHY-02 scheme-pass rule: e.g. both options marked and the higher counts; an error penalised once; competency credit). Once per series when the sets repeat them word for word; later sets note only differences.
- Map the scheme's answers to the paper's rows by content (numbering can differ; write the mapping in `V/notes/Y2026.md`).
- Scoring lines only for this paper's `rel = origin` rows. Shuffle rows inherit their origin's lines (the kit's year-close counts them through `rel_to`). If a scheme prints different values for a shuffled question, note it in `notes/Y2026.md` and add a Q-QUEUE item; never a second set of rows.
- One STEP-AWARDS row per printed scoring line, in printed order: `award_id` `SA-<instance_id>-<nn>`; `file_id` = the scheme original; `step_no` 1, 2, …; `step_text` = what the line awards, normalised as P§6.3; `marks` as printed, in decimals (0.5, 1, 1.5); `step_kind` one of formula, substitution, result, unit, diagram, label, reason, definition, key, other; `mandatory` = y where the scheme makes the line compulsory; `alt_accepted` for "any other relevant answer" and alternative methods; `provenance` = PRINTED; `source_page`; `batch`.
- MCQ and assertion–reason: one `key` row, step_text `(B)`, marks 1.
- Numeric results printed only in the scheme: FORMULAE rows, `role = result`, `source = MS`, ids continuing after the paper's last `EQ-<pid>-` number.
- A scheme misprint: as printed with `(sic)`; the correct physics computed in Python and written in the note (CI§7).
- In the same unit, `<pid>__ERRATA.csv`: status DONE for the scheme original and its bundle twin ("read from the original <file_id>; the bundle <file_id> is the same document").
- Then: `G check <pid> --stage S5` → `G skeleton <pid> --stage S5` → the S5 checker (R§10.1) → `G verify <pid> --stage S5` → settle (R§8) → `G commit <pid> --stage S5 --progress "S5 scheme 55/1/1 ("`.
- No scheme (compartment 55/7, 55/B/7; the SQP): after S6, because these need archetype codes. Per question: `TRANSFERRED:<award_id>` from a PRINTED 2026 line of the same archetype (structure only; this paper's numbers recomputed in Python, never the other paper's), else INFERRED; never both kinds on one question (V09). The gate checks that every TRANSFERRED source is a PRINTED line in the vault. Units `TR-<pid>`, `--stage OTHER`; the last unit of each line adds `--progress "S5 compartment 55/7"` or `--progress "S5 SQP2526-042"`.

### R§10.1 · The S5 checker brief
As R§7, with these differences. Input: `<pid>__SKELETON.csv` (instance_id, q_no, side, part, scheme_file_id, scheme_pages). Read the scheme pages only. VERIFY columns: `instance_id, step_marks, key, numbers, note`:
- step_marks: the marks of every scoring line printed for this answer, in printed order, separated by " | " (½ or 0.5 as printed);
- key: for an MCQ or assertion–reason answer, the printed option letter;
- numbers: the final numerical answers printed, each with its unit;
- note: anything unreadable.

## R§11 · Changing the kit (rare)
The kit changes only for a real bug that blocks correct data, never to make a check pass on wrong data.
1. Add a Q-QUEUE item describing the failure. Copy `/home/claude/pyqkit.py` to `/home/claude/pyqkit_before_fix.py`.
2. Make the smallest fix, with a comment `# kit <new edition>: <why>`; set `KIT_EDITION` to a later string (a new date, or the same date with the next letter).
3. Test: `K validate V` gives the same result as before; `K check-paper V <pid>` passes for every mined paper; a small planted case shows the bug is gone.
4. Log it: a CONVENTIONS entry (what, why, tests) and a PHY-03 addendum entry; then `G checkpoint --message "kit <edition>: <what>"`. The pack carries the new kit inside the vault (`tools/pyqkit.py`), and the setup prefers it over the older copy in the instructions repository. Put a copy in `<outputs>/tools/pyqkit.py` and tell her, once, to replace the instructions-repository copy.
- The same applies to `phy_gate.py` and `phy_code_env.py`, except they don't travel in the vault: the fixed copy goes to `<outputs>/tools/` and she replaces the instructions-repository copy. Until then, run the fixed copy by its full path.

## R§12 · S6, S7, S8 (DEFERRED to the closing sweep after 2022's printed documents: CLAUDE.md §12, PHY-08 Y§0)
**S6 classification** (P§10.3; CONVENTIONS "Classification rule (P§10.2 applied)"):
1. `K derive V`, then predict which existing codes 2026 should contain; write the prediction in `V/notes/Y2026.md` before classifying.
2. Chapter by chapter: for each row, `K candidates V --instance <id> --k 5`; apply the granularity test; assign an existing code, promote a DRAFT seed (it keeps its number), or issue a new code (next serial in the chapter) with name, asks_you_to, skeleton and traps. Check names by a script against CI§10 (name ≤ 12 words, no symbols; asks_you_to ≤ 30 words and starts "Asks you to").
3. CLASSIFY rows in `V/work/S6-CH<cc>__CLASSIFY.csv`, every field as the vault's existing CLASSIFY rows, `rule_version` "P10.3/B<nn>-<date>". Shuffle rows copy their origin's values.
4. REGISTRY changes: `j/REGISTRY.csv` is re-runnable Layer 1.5; write it with the kit's own `read_table` and `write_table` in a short script. Never write an `l1/` table that way.
5. `G commit S6-CH<cc> --stage OTHER` after each chapter (validate checks every code exists and is VERIFIED); the last chapter adds `--progress "S6 classify"`. Then the misses in `notes/Y2026.md`: predicted but absent; present but never seen before.

**Before S7 and S8:**
- Tick the S2b line when a script shows every 2026 paper has a BLUEPRINTS row: `G checkpoint --message "every 2026 paper has a BLUEPRINTS row (<n>/<n>)" --tick "Y2026 S2b"`.
- FILES statuses through ERRATA (unit `S8-FILES`, `--stage OTHER`): question papers DONE once their S5 and S6 are done; the SQP and its original DONE after its scoring lines.
- Q-010: the eight Batch 0 SQP rows get their FIGURES and FORMULAE rows from the SQP original's page images (unit `SQP-GAPS`, `--stage OTHER`).

**S7:** `K derive V` · `K export-xlsx V 2026 --out <outputs>/reports` · judged observations in `notes/Y2026.md` · `G checkpoint --message "S7 derive and workbook" --tick "Y2026 S7"`.

**S8:** `K validate V` · `K year-close V 2026 --xlsx-dir <outputs>/reports` (every line must PASS; a FAIL keeps the year open and names what is left) · copy the year report it names to `<outputs>/reports/PHY-YEAR-2026-REPORT.md` · `G checkpoint --message "year 2026 closed" --tick "Y2026 S8"`. Her steps at year close become: nothing to download (the vault is already in GitHub); in the schemes repository, replace the year's scheme PDFs with the next year's; add the next year's ZIP(s) to the papers repository. She then starts the next session with the same goal line.

## R§13 · `Fix:` and `Audit.`
- `Fix: <text>` (from her, or a chat-audit finding she passes on): find the row(s); confirm on a crop of the page; write ERRATA rows (old, new, reason, evidence = the crop path and what it shows) to `V/work/FIX-<n>__ERRATA.csv` (n = the next free number); `G commit FIX-<n> --stage OTHER`; `K derive V` if Layer 2 depends on it; a one-line confirmation. If the crop shows the vault was right, say so in one line with the crop path, and change nothing.
- `Audit.`: `K validate V`; `K check-paper V <pid>` for every mined paper; a fresh blind checker on a 10 % sample of every paper's rows (a skeleton of the sampled rows, R§7, compared by a script against the vault rows); findings settled from crops and fixed as ERRATA through the gate; `K derive V`; a report in `<outputs>/reports/PHY-AUDIT-<date>.md`.

- Standing permission (2026-10-01, CLAUDE.md §12): a queued fix whose page evidence is already logged is applied without waiting for her `Fix:` line, after you confirm it again on the page image. Q-013 comes first.

## R§14 · Context, usage, the cloud machine, pushes
- Compaction: CLAUDE.md is re-read automatically; also re-read PROGRESS and this file's section for the stage, and run `G show`. Part files in `V/work/` and sealed files survive a compaction.
- Usage limit: the session pauses; the last commit is the checkpoint. When she types `Go.`, continue from the first unfinished paper.
- Machine replaced (files gone): rerun the setup (it keeps the batch for this session), then redo the unfinished paper from the start. At most one paper is lost.
- Push failure: `G push`; commits pile up locally until it works; report it.
- Branches: the gate pushes to this session's branch, and the setup has already carried the earlier results forward into it, so the newest branch holds everything. She never needs to merge anything; the dashboard link shows it all.

## R§15 · Reports
### R§15.1 · Session report
As CLAUDE.md §11. Numbers come from the gate output, `<outputs>/logs/GATE-LOG-B<nn>.md` and `K status V`. The line before the RESUME line is `Dashboard: <link>`, the link the gate printed at its last save.

### R§15.2 · Trial report (first session only)
`<outputs>/reports/PHY-CLAUDE-CODE-TRIAL.md`. Run `date -u` when you open each paper; the gate log has the commit times. Every number is copied from the gate log or computed by a script in the session:
```
# Claude Code trial · Batch <N>
## What ran
session start and end (UTC); papers attempted and finished; S1b result (files matched, errata ids)
## Papers
| paper | rows (shuffle + new) | figures | formulae | check-paper | values double-read | mismatches | extractor wrong (part_fixed) | checker wrong (extractor_right) | unreadable | minutes |
## Every mismatch
| paper | row | field | extractor | checker | decision | crop |
## Checks
the validate line after each commit; commits (short sha, branch); pushes
## What went wrong or was slow
## Recommendation
continue as is, or change what (one paragraph, judged)
```

## R§16 · Exceptions on this route
| Situation | Action |
|---|---|
| Setup exit 4 (no vault anywhere) | Stop. One line to her: upload the newest PHY-VAULT file to the project repository, then type `Go.` |
| Two copies of a tool or instruction file | The setup uses the newest and warns; name the extra copies in your report for her to delete. |
| A repository missing (exit 5 or 6, or no papers) | One line to her; do the work that doesn't need it. |
| Kit in the instructions repository older than the vault's | Fine: the setup uses the newer one. Mention once. |
| `render` cannot find a file | Find it by sha256 (R§3 rule 5). |
| A subagent fails or returns nothing | Run it once more with the same brief. Extractor still failing: extract yourself, and the checker must still be a fresh subagent. Checker impossible (subagents unavailable): `G commit … --unverified "<reason>"` (queued for a later blind check). |
| The checker disagrees on many values of one page | Re-render that page at 300 dpi; a fresh checker redoes that page's rows only. |
| The kit rejects a correct row | R§11. |
| A paper fails check-paper after a re-read | Quarantine it (CI§2.12): Q-QUEUE item with the failing line, PROGRESS note, continue with the next paper. |
| Context heavy | Stop at the next gate commit; report; she types `Go.` |
| She asks a physics question | One line + "that belongs in the study project". |
| A file of another year appears | Inventory logs it NEW; it waits for its year (CI§7). |
