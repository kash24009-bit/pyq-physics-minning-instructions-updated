# PHY-07 · CLAUDE CODE RUNBOOK · Physics (042)

*How the mining runs in Claude Code. CLAUDE.md holds the rules; this file holds the procedures. Cited as R§n. Written 2026-09-30 for kit edition 2026-09-30b and tested that day in a three-repository simulation. Updated 2026-10-01 and 2026-10-02 after the Batch 2 trial and its audit; 2026-10-05 after Batch 3 (one thorough reading per paper with `--single-read`, the year check, the fixed planner); and 2026-10-21 after Batches 4 to 6: every reader, checker and adjudicator a `phy-reader` subagent; the rule card's lean reading (bands, step budget, calibration); gate edition 2026-10-21 with its lint and normalised year-check comparison; `phy_marks.py`, the printed-marks list for scheme units; the lean boot; a new session after every usage stop.*

Shorthand: `K` = `python3 /home/claude/pyqkit.py` · `G` = `python3 /home/claude/phy_gate.py` · `V` = `/home/claude/vault` · `T` = the `outputs/tools` folder of the project repository (`/home/user/pyq-physics-minning-instructions-updated/outputs/tools`) · `<N>` = the session batch the setup printed (`<nn>` = the same number with two digits) · `<pid>` = a paper_id · `<outputs>` = `/mnt/user-data/outputs` (a link into the project repository's `outputs/`). `pages` and `render` always take `--vault V`: without it they cannot find a document by file_id.

## R§0 · Reading order
- Every session: CLAUDE.md §6 says what to read at boot (PHY-08 in full; the vault's rule card, CONVENTIONS and PHY-03 addendum in full; the open lines of PROGRESS and QQUEUE). Read a section of this file when the step you start cites it, and only that section.
- After a compaction: CLAUDE.md, the open lines of PROGRESS and the R§ or Y§ section of the current step.
- Readers never read this file: their rules are the vault's `notes/RULE-CARD.md` and their brief (R§6, R§7, R§8, R§10.1).

## R§1 · The first Claude Code session (Batch 2, 2026-10-01)
Done; never repeated. Its one-time steps and texts (the route change in CONVENTIONS, Q-009 and Q-010, addendum entries W-14 to W-16, S1b originals matched to their bundle twins) are in the vault and in the 2026-10-05 edition of this file.

## R§2 · The setup script (`phy_code_env.py`)
- Run it as CLAUDE.md §6 says. The first run takes a few minutes (packages: poppler-utils if possible; pillow, openpyxl, pypdfium2, pypdf, reportlab). It never edits a file she put in a repository.
- A repository holding only PDFs (a schemes repository) gets the role `schemes` and is linked into `/mnt/project`. Every file of the instructions repository except `outputs/` is linked into `/mnt/project` too, so `PHY-0x` files, `phy_marks.py`, the one-time `phy_replay_2024.py` and the delivery copy `RULE-CARD.md` appear there.
- If the newest vault sits on an earlier session's branch, the setup merges that branch into this session's branch, so every earlier report, log and pack stays together on the newest branch. A merge that would conflict is undone and reported. (Her uploads go to the root of the instructions repository's main branch, never into `outputs/`, so they cannot conflict with that merge.)
- Tool and instruction files a browser saved as `phy_gate (1).py` or `PHY-07-CLAUDE-CODE-RUNBOOK (1).md` are linked under their plain names in `/mnt/project`. When two copies exist, the newest commit wins (for the gate, the newest `GATE_EDITION`), and a warning names the extra copies. CLAUDE.md must carry its exact name; a misnamed one is only warned about.
- It prints: the roles with branch and commit; the folder links; every vault candidate found in working trees and on all branches, with the CHOSEN one and the stale ones; the kit edition and where it came from (the newest edition wins; a tie goes to the vault's own copy); this session's batch and why; the validate line; `pyqkit status`; warnings. It writes `/home/claude/phy_env.json` (never edit it by hand) and links `/home/claude/phy_gate.py`.
- The batch: if the newest vault was packed by this same Claude Code session (its `cc_session` matches), the batch stays; otherwise it is the restored batch + 1. Only if that reasoning is wrong for a reason you can state: `PHY_BATCH=<n> python3 …` and say why in the report.
- **The reader agent.** Claude Code loads `.claude/agents/phy-reader.md` of the instructions repository when the session starts. If the Agent tool does not offer `phy-reader`, use a general-purpose subagent with the same brief, add "Read /home/claude/vault/notes/RULE-CARD.md first; it is your rule set" to it, and say so once in the report.
- Rerun the setup only when the cloud machine was replaced (your files are gone).

| Warning | Do |
|---|---|
| several CLAUDE.md files | Name the others in the report; she deletes them. The instructions-repository copy is the one that counts. |
| no file named exactly CLAUDE.md | First line of your report: she renames it (Claude Code loads only CLAUDE.md by itself). Read the misnamed file by its path meanwhile. |
| name clash | Two different files share a name; the first was linked. Open the other by its full path. |
| git fetch failed | Vault copies on other branches may be missing; say so once and continue with what was found. |
| no papers repository | Paper stages wait; scheme, classification and derive work continues. |
| python packages MISSING | Rerun once. If pages still cannot render, stop paper work and say so in one line. |

## R§3 · Reading a page
Commands (the kit opens documents by `file_id`; CONVENTIONS "Documents are opened by file_id"):
- `K pages --vault V <file_id>`: the page table (language, text characters, visual flag). `K pages --vault V <file_id> --text <page>`: the text layer of one page, for the digit cross-check only.
- Bands: `python3 T/phy_bands.py --fid <file_id> --pages <a-b> --out /home/claude/render/<unit>/bands` renders the pages once at 180 dpi without `--crop` and cuts each into a top band (0–52 % of the height) and a bottom band (48–100 %).
- Crops: `K render --vault V <file_id> <page> --dpi 400 --region x0,y0,x1,y1 --out /home/claude/render/<unit>/<label>`; the region is in fractions of the whole page (`0,0.40,1,0.62` = full width, 40–62 % down); every crop in its own `--out` folder (the kit names files `p<page>.png`). Pack crops on sheets with `python3 T/phy_tile.py --out /home/claude/render/<unit>/sheets/<name> --dpi 400 <pngs>`, which never rescales a crop and prints each one's effective dpi.

Rules (the readers' version is the rule card, sections A and B):
1. Every number, unit, exponent, sign, option, figure value, direction and half mark is read from the page image at full resolution: a 180 dpi half-page band on a born-digital page; a 300–400 dpi crop on scans, for figure labels, plate lengths and directions, and for any doubt. Never from a shrunk whole page.
2. Dual-read (P§6.1): structure from the image; every digit cross-checked against the text layer; a conflict gets a closer crop; still unsure → an UNREADABLE row (`LOWRES`) and a note. Known text-layer damage: 10⁸ read as "108", hν as "h", ¹⁶₈O as "168O", 30° as "300", B₁/B₂ as "B and B", dropped decimal points ("38 eV" for 3.8 eV), 1.6 µA as "1.6 mA".
3. **Born-digital or scan:** decide once per new file from its text layer. The 2024 schemes and the 2024 papers 55/1 to 55/3 were born-digital; the 2024 papers 55/4 and 55/5 and the 2026 schemes were scans. A scan has no dual-read: say so in the note, use 300 dpi tiles and 400 dpi crops, save them as 8-bit grayscale, and never render above the scan's own resolution (`pdfimages -list <pdf>`).
4. **Image sizes** (card A9): every image within 1568 px on its long side and under 450 KB. Anthropic's limits for Opus 5.5 (vision docs, read 2026-10-21): a long edge up to 2576 px and 4,784 visual tokens (⌈width/28⌉ × ⌈height/28⌉); a request with more than 20 images is refused when any image passes 2000 px on a side; Claude Code re-encodes an image still over 500 KB after resizing as a lower-quality JPEG (Claude Code tools reference, from v2.1.196). 1568 px keeps a margin under all three.
5. **Bilingual originals:** English pages only. Hindi and English pages alternate, and the page table marks the Hindi pages "en" because their text layer is not Unicode (CONVENTIONS "Bilingual originals"), so a Devanagari count misses them. The sibling worksheet (from 2023) lists the English pages from the share of common English words in each page's text layer; any page it cannot settle, and every page of a scan, is decided on one sheet of small page thumbnails. A Hindi page is the backup for a damaged English one (`read_from = hi-translation`). Hindi-medium twin files (2024: `55-S-1 hindi_merged.pdf`, `55(B)_S (1).pdf`) carry Unicode Devanagari and are found by it.
6. If `render --vault V <file_id>` cannot find the document, find the file by its sha256 under `/mnt/user-data/uploads`, `/mnt/project` and `V/work/_intake`, and pass the path instead.

## R§4 · Part files, ids, templates
### R§4.1 · Part files
- `V/work/<unit>__<TABLE>.csv`; `<unit>` is the paper_id for paper work, or a label (`S1-2024`, `S2A-2024`, `FIX-8`, `S6-CH02`, `TR-2026C-5571`, `S8-FILES`, `SQP-GAPS`, `YC-2025`).
- TABLE: INSTANCES, FIGURES, FORMULAE, CASES, BLUEPRINTS, UNREADABLE at S3/S4; STEP-AWARDS (+ FORMULAE results, + ERRATA statuses) at S5; CONSTANTS at S2a; ERRATA for corrections; CLASSIFY at S6.
- Header = the first line of the vault's own table (`head -1 V/l1/INSTANCES.csv`; CLASSIFY is `V/j/CLASSIFY.csv`), same column order. Write with Python's `csv.DictWriter`, never by joining strings.
- `batch` = `<N>` on every row that has the column.

### R§4.2 · Ids (CI§10, Batch 1 style)
| What | Format | Example |
|---|---|---|
| question part | `<pid>-Q<nn><side>[-<part>…]`, question number with two digits | `2026-5532-Q08`, `2026-5532-Q24B-b`, `2026-5532-Q22A-b-i` |
| figure | `F-<pid>-<nn>` | `F-2026-5532-01` |
| formula | `EQ-<pid>-<nnn>`, continuing after the paper's last number | `EQ-2026-5532-001` |
| case | `CS-<pid>-Q<nn>` | `CS-2026-5532-Q29` |
| choice pair | `OR-<pid>-Q<nn>` | `OR-2026-5532-Q31` |
| erratum | `ER-B<nn>-<nnn>`, the next free number of this batch (the gate's own status errata take numbers too) | `ER-B07-001` |
| scoring line | `SA-<instance_id>-<nn>` | `SA-2026-5532-Q24A-02` |
| 2022 papers | `T1-2022-<code digits>`, `T2-2022-<code digits>` (CI§10) | `T2-2022-5511` |

### R§4.3 · Templates: real Batch 1 rows of 2026-5512 (match them field for field; blank fields omitted)
- **Shuffle row:** instance_id=2026-5512-Q08 · paper_id=2026-5512 · file_id=FL-bbc9339e7e · year=2026 · exam=MAIN · paper_code=55/1/2 · q_no=8 · section=A · q_marks_printed=1 · chapter=02 · topic_id=T-02-08 · q_type=MCQ · command_verb=The ratio of electric fields ... will be · has_figure=n · wants_figure=n · wants_graph=n · givens=spheres of radii r_1, r_2 joined by a conducting wire; separation >> radii · unknown=E_A/E_B at the surfaces · options=A) r_1/r_2 | B) r_2/r_1 | C) r_1^2/r_2^2 | D) r_2^2/r_1^2 · stem=A conducting wire connects two charged metallic spheres A and B of radii r_1 and r_2 respectively. The distance between the spheres is very large compared to their radii. The ratio of electric fields, (E_A/E_B) at the surfaces of spheres A and B will be · source_page=7 · read_from=image · rel=shuffle · rel_to=2026-5511-Q02 · syllabus_status=IN · note=shuffle of 2026-5511-Q02, text and numbers identical on the page image · batch=1
- **New MCQ row:** instance_id=2026-5512-Q01 · … q_no=1 · section=A · q_marks_printed=1 · chapter=02 · topic_id=T-02-01 · q_type=MCQ · command_verb=The potential difference ... is · givens=vec(E) = 4x i^ N/C; A at x = 1 m, B at x = 3 m · unknown=V_A - V_B · options=A) -16 V | B) 16 V | C) -8 V | D) 8 V · stem=In a region electric field is given by vec(E) = 4x i^ N/C. The potential difference between points A (x = 1 m) and B (x = 3 m), (V_A - V_B) is · source_page=5 · read_from=image · rel=origin · syllabus_status=IN
- **New NUM part row:** instance_id=2026-5512-Q18-a · q_no=18 · part=a · section=B · q_marks_printed=2 · chapter=11 · topic_id=T-11-05 · q_type=NUM · command_verb=Find the ratio · givens=alpha particle and proton moving with the same velocity · unknown=lambda_a/lambda_p · stem=Find the ratio (lambda_a/lambda_p) of de Broglie wavelength lambda_a associated with an alpha particle to de Broglie wavelength lambda_p associated with a proton if both are moving with the (a) same velocity · source_page=13 · read_from=image · rel=origin
- **BLUEPRINTS:** paper_id=2026-5512 · year=2026 · exam=MAIN · n_questions=33 · total_marks=70 · sections=A:1-16:1;B:17-21:2;C:22-28:3;D:29-30:4;E:31-33:5 · choice_rule=B:17;C:24;D:29,30;E:31,32,33 · calculators=n · constants_listed=y · bp_class=P33 · reading_time=15 min (cover note V) · source_page=3
- **FIGURES:** figure_id=F-2026-5512-01 · instance_id=2026-5512-Q24B-b · fig_type=circuit · printed_or_demanded=printed · description=Resistor network between terminals A and B: A to M 2R; M to O R (lower); … N to B 3R. [same figure as F-2026-5511-01] · values=2R, R, R, R, R, R, 3R · source_page=17 · from_image=y
- **FORMULAE:** formula_id=EQ-2026-5512-002 · instance_id=2026-5512-Q17A · role=asked · formula=single-slit minima y_n = n*lambda*D/a; coincidence n_1*lambda_1 = n_2*lambda_2 · quantities=y, n, lambda, D, a · units=m · source=QP · source_page=13 · from_image=y
- **CASES:** case_id=CS-2026-5512-Q29 · paper_id=2026-5512 · q_no=29 · context=(two sentences) · chapter=11 · n_subparts=4 · subpart_types=MCQ,MCQ,MCQ,MCQ · attempt_rule=all four; internal choice inside (IV): an OR alternative printed without its own label · source_page=19
- `extra` keys already in use (same key for the same situation; `grep` the vault's INSTANCES to see how): ARSET, choice_in_part, figure_page, marks_from, options_page, options_pages, printed_split, series, vi_paper. Several keys are joined with "; ".

## R§5 · What goes into the rows at S3 and S4
The authority is PHY-02 §6–§7 and the vault's CONVENTIONS.md; the readers' version is the rule card, section D. The points the years settled:
- One row per printed part label; sides and choices as card D3; `marks_part` only where a mark is printed beside the part; halves as 0.5.
- **Lead-in numbers** (her decision 2026-10-21, Q-094): the numbers of a shared lead-in (the text printed above a question's sub-parts) go into the givens of every sub-part row, so each row stands alone, as 2024-5511-Q24-b and SQP2627-042-Q17-II do. Case studies keep their convention: the passage in CASES, each sub-part's givens what it uses, "as in the passage" for the rest (card D5).
- **Options** on MCQ rows only, `A) … | B) … | C) … | D) …`; assertion-reason rows keep options blank and the paper's first A-R row carries the printed set as `ARSET=…`; a copied row that is not the paper's first A-R row drops its ARSET (B5-1).
- **FIGURES values** hold the numbers the figure prints (each in the text layer near the figure or confirmed on a 400 dpi crop), and a stem value only marked "(stem)" (Q-097); a measurement never: it goes in the description, marked "measured, not printed" (card D10; six 2024 rows fixed by FIX-6 and FIX-7).
- **Notation** as card D11: powers of ten as `1e-2`, never `10^-2`.
- FORMULAE `given` and `asked` (a derivation's whole chain); CASES with a two-sentence context; BLUEPRINTS from the paper's own instructions page; `chapter`, `topic_id`, `syllabus_status` from the vault's syllabus table; `read_from = image`; a misprint with `(sic)` and a note.

**S4 sibling method** (card D15; CONVENTIONS "S4 method (B01)"): match each printed question to its series' rows on disk by content (never by number); identical wording and every value → a shuffle row copied from the origin with this paper's ids and pages; any difference, however small, or any doubt → a full new row with "resembles <id>: <what differs>".
- **From 2023, the sibling worksheet** (her decision 2026-10-21; built at the start of the 2023 session as an extension of `T/phy_s3_prep.py`): it aligns each sibling question with its series' origin rows by text, compares every number, unit, sign, exponent, option and option order token by token, and marks each question "variant, full row" or "repeat candidate", never "repeat". It prints the origin row beside each candidate and lists the English pages (R§3 rule 5). The reader confirms every repeat candidate on its band and crops every figure at 400 dpi (a figure can change while the text stays the same); the script writes the confirmed repeats from the origin rows, and the reader writes only new and variant rows. Test it before use on one 2024 sibling (2024-5512, whose 78 rows hold 61 shuffles): every one of its shuffles must come out a repeat candidate, and every variant a variant.
- **Visually-impaired letter-code papers:** every row carries `extra` `series=<s>; vi_paper=y` (card D9 lists the tags; 2024-55B uses `series=55/B` because its code word matches no series). Unchanged questions are shuffles of their own series; a question rewritten for visually-impaired candidates is a full row with note "VI adaptation of <id>". VI alternatives inside a normal paper follow CONVENTIONS "VI alternatives" (`vi_alt = y`).

## R§6 · The reader brief (S2a, S3, S4 and S5 units)
Start a fresh `phy-reader` subagent (R§2) with a brief of at most 15 lines; pass no model or effort. The agent's own prompt already tells it to read the rule card and the worksheet first. Template:
```
Unit <unit> · stage <S2a | S3 | S4 sibling of series <s>, origin <origin pid> | S5> · paper <pid> · batch <N>.
File <file_id> (<file name>), pages <a-b> (English pages <list>; <born-digital | scan>).
Worksheet: /home/claude/render/<unit>/PREP.md.
Calibration: <yes: first band unit of this file | no>.
Next free ids: EQ-<pid>-<nnn>, F-<pid>-<nn>; ER-B<nn>-<nnn> only if this unit sets a file status.
Write the part files in /home/claude/vault/work/ (card A6); never CONSTANTS outside S2a.
Then python3 /home/claude/phy_gate.py check <unit> --stage <stage> until CHECK PASS, settling every LINT warning (card A10).
Return as card E2; drafts to /home/claude/render/<unit>/NOTES-DRAFT.md.
```
- The main session's chained call before the Agent call writes the worksheet: `T/phy_s3_prep.py` for an S3 unit (from 2023, the sibling worksheet for S4); for S5 `T/phy_s5_prep.py` and then `python3 /mnt/project/phy_marks.py --fid <scheme fid> --pages <a-b> --out /home/claude/render/<unit>/PREP.md` (R§10). The call prints only the worksheet's "located n of N" line (`grep -m1 located` on PREP.md) and phy_marks.py's one-line summary; a worksheet that locates fewer questions than the paper prints is fixed before any reader starts (B6-5).
- A reader stopped by a usage or server limit loses only its context, not its files: resume it by message when its context is intact, else start a fresh reader on the same unit, which reuses the renders already on disk (B5-2).
- Doubts the reader returns unsettled go to a fresh `phy-reader` with the crop paths and the rows concerned (CLAUDE.md §7 step 3).

## R§7 · The blind checker brief (year check)
In the year check (PHY-08 Y§11), after `G yearcheck <year>`, start a fresh `phy-reader` with this brief: once for the question rows (`<unit>__SKELETON.csv`), once for the scheme parts (`<unit>__SKELETON-S5.csv`, with the R§10.1 differences). `<unit>` is `YC-<year>` (or `YC-<year>-<pid>` in a second round). Never pass it the reader's report or anything from the vault.
```
You are the BLIND CHECKER of year check <unit> · batch <N>. The rule card's sections A and B apply; by card A3 you never open the vault's tables, part files, sealed files or any earlier reading of these pages: your reading is valuable only because it is independent.
Your only input is /home/claude/vault/work/<unit>__SKELETON.csv: which row is which printed part, of which file (file_id), on which page, and why it was chosen.
Read every listed part on its page: 180 dpi bands on born-digital pages; a 300-400 dpi crop for every figure value and direction, every small digit, sign or exponent, and on scans (card B3, B4); crops in their own folders under /home/claude/render/<unit>/check/. Write /home/claude/vault/work/<unit>__VERIFY.csv with Python's csv module, columns:
instance_id, marks_part, q_marks_printed, numbers, options, figure_values, note
- marks_part: the marks printed beside this part only; blank if none are printed there.
- q_marks_printed: the question's printed total.
- numbers: every number printed in this part's own text; where a question's sub-parts share a lead-in printed above them, also the lead-in's numbers on every sub-part row (not for a case study: a case passage's numbers belong to the first sub-part's row only). Each with its unit or the symbol it belongs to, in reading order, separated by " | ". Powers of ten as 3e8; fractions as printed (1/2); degrees as 30 deg; keep signs; include numbers inside expressions (for E = 4x i^ write 4x). Leave out question numbers, marks, part labels and sub-labels such as (1) or (i); subscripts are labels, not numbers (write r_1).
- options: for an MCQ, every option: A) ... | B) ... | C) ... | D) ..., in the project's ASCII notation (sqrt(2), r_1, 2*p_2, lambda_a, microF, microC, vec(E), i^); for an assertion-reason row, the four printed options in full.
- figure_values: every value printed in a figure that belongs to this part (2 ohm | 6 V | 30 deg); "same as <instance_id>" if that figure was listed for an earlier row; blank if there is no figure. Never a measurement of the drawing. In note, also write the direction of every cell (which side its longer plate faces), diode, arrow, current or field drawn, e.g. "E_2: longer plate toward C; D_1 points right".
- note: anything you could not read. For every printed part on these pages that the skeleton lacks, add a row whose instance_id is <pid>-Q<nn>-extra and whose note starts "MISSING:" followed by what and where.
Return, in at most 8 lines: rows written, pages read, MISSING rows, anything unreadable.
```

## R§8 · Settling mismatches
1. `G yearcheck <year> --compare` lists each mismatch (also in `V/work/YC-<year>__DIFF.csv`). From gate 2026-10-21 it first clears what is only notation or a vault convention (R§9); `--raw` compares the 2026-10-05 way.
2. Each unsettled mismatch goes to a fresh `phy-reader` adjudicator (never the main session, which opens no images), with this brief:
```
You are the ADJUDICATOR of year check <unit> · batch <N>. The rule card's sections A and B apply.
Your input: the rows of /home/claude/vault/work/<unit>__DIFF.csv whose resolved column starts "no" (instance_id, field, the vault's value, the checker's value, detail).
For each, render a 400 dpi crop of exactly that spot into its own folder /home/claude/render/<unit>/adj-<n>/ and read it. The crop decides; never the majority, memory or the text layer alone.
Append one row per mismatch to /home/claude/vault/work/<unit>__ADJUDICATE.csv: instance_id, field (as in DIFF), decision, final_value, crop (the PNG you read), note.
Where the page does not support the vault's value, also write the ERRATA rows to /home/claude/vault/work/FIX-<n>__ERRATA.csv (errata_id from ER-B<nn>-<nnn> on, file, row_id, field, old, new, reason starting "<unit>:", evidence = the crop path and what it shows, batch), and check every shuffle copy of the corrected row (card D15): each wrong copy gets its own ERRATA row.
For figure directions, compare the checker's direction notes with the FIGURES descriptions; settle each difference on a 400 dpi crop (measure plate lengths by script when the drawing is small); record it with field figure_direction.
Return, in at most 12 lines: decisions by kind; every part_fixed with its crop; ERRATA rows written; anything unreadable.
```

| Decision | When | Then |
|---|---|---|
| `extractor_right` | The vault matches the page; the checker misread. | Recorded. |
| `part_fixed` | The page shows the checker's value, or a third value. | ERRATA rows in a FIX unit; the mismatch must be gone at the next compare. |
| `unreadable_logged` | Neither reading can be confirmed at 400 dpi. | `UNK` and an UNREADABLE row (`LOWRES`) through a FIX unit. |
| `part_added` | The checker found a real printed part the vault lacks. | The full row (and its figures and formulae) through a FIX unit; `final_value` = its instance_id. |
| `not_a_part` | The "missing" part is not a separately printed part. | Recorded. |

3. The gate refuses a decision whose crop does not exist.
4. A mismatch of field `row` (the checker skipped a part) is not settled by a decision: a fresh checker reads those skeleton rows only and appends to VERIFY.
5. Commit the FIX unit (`G commit FIX-<n> --stage OTHER`), record `part_fixed`, and compare again until the compare exits 0.
6. A real error among a paper's sampled rows sends that paper to a second round (PHY-08 Y§11 step 4).
7. When the compare exits 0 the gate writes `outputs/reports/PHY-YEARCHECK-<year>.md` and copies every check file to `outputs/logs/doublecheck/B<nn>/`; save with `G checkpoint --message "Y<year> year check done" --tick "Y<year> YC"`.

## R§9 · The gate (`phy_gate.py`, edition 2026-10-21)
| Command | Does |
|---|---|
| `G check <unit> --stage S3\|S4\|S5\|OTHER` | Schema, ids, batch, coverage (figures, formulae, cases, blueprint), a rel on every row, options only on MCQ and AR rows, then a trial merge into a copy of the vault with check-paper and validate. Changes nothing. For S3, S4 and S5 it ends with the lint's warnings (`LINT n warning(s)`, one line per warning starting `!`). |
| `G lint <unit> --stage S3\|S4\|S5` | The lint alone. Warnings: figure-printed (numbers in FIGURES values that are not in the page's text layer, the stem, givens or options), figure-measured (a measurement in values), notation (`10^n`), marks-format (½ or 1/2 in marks), scheme-sum (a part's lines against its printed marks; a line noting "no mark of its own" is exempt), scheme-key (an MCQ or A-R row with no key line), scheme-result (a NUM row with real data, printed lines and no FORMULAE result row), arset (a second ARSET in one paper). Warnings never change the exit code. |
| `G lint --all [--year <year>]` | The same over the vault's rows (notation and figure-printed are skipped there), plus shuffle-copy (an ERRATA row corrected an origin's field and a shuffle copy still holds the old value) → `V/work/LINT-<scope>__FINDINGS.csv`. On 2026-10-21 the whole vault gave 1 finding (SQP2627-042-Q25-II). |
| `G skeleton <unit> --stage S3\|S4\|S5` | Writes `<unit>__SKELETON.csv` and moves the part files to `/home/claude/.sealed/<unit>/` (sealed per-paper checks; not used since the single reading). |
| `G verify <unit> --stage …` | Brings the sealed files back, compares them with VERIFY (+ ADJUDICATE), writes DIFF. |
| `G commit <unit> --stage … [--progress "<text in the line>" \| --progress-new "<new line>" \| --no-progress] [--unverified "<reason>"] [--single-read]` | check + verify + trial merge, then the real merge (rolled back if anything fails), status erratum (S3/S4), PROGRESS line with computed counts, validate, pack into `<outputs>/vault/`, archive of the part files to `V/work/done/`, gate log, git commit and push. An S5 commit must name its line (`--progress "S5 scheme 55/1/1 ("`) or say `--no-progress`. `--single-read` saves after one thorough reading (her decision 2026-10-03; the year check covers it). `--unverified` belongs to sealed per-paper checks, not used since the single reading. |
| `G checkpoint --message "…" [--progress-new "…" \| --tick "<text in an open line>" \| --open-line "<text>"]` | validate + pack + gate log + commit + push, for work that is not a part-file merge (text files such as the rule card, REGISTRY, ticking a line a script has proved, adding an open line). |
| `G checkpoint --message "Y<year> planned" --plan-year <year>` | After a year's S1 identity commit: writes the year's PROGRESS lines from FILES (PHY-08 Y§2 step 8). A scheme file whose note starts "Hindi-medium" gets no S5 line (edition 2026-10-21, Q-067). Refuses while an identity is incomplete. |
| `G checkpoint --message "<reason>" --defer-year <year>` | Marks every open line of that year DEFERRED to the closing sweep. |
| `G yearcheck <year> [--paper <pid> --all] [--rate 0.10]` | Tier 1 by script over every row of the year (coverage, options, shuffle identity, scoring-line sums and keys, every number against the PDF text layer, and every finding of `lint --all --year <year>` as a suspect named `lint-<check>`), then the re-reading lists `YC-<year>__SKELETON.csv` and `__SKELETON-S5.csv` (PHY-08 Y§11). `--paper <pid> --all` lists every new row of one paper. |
| `G yearcheck <year> [--paper <pid>] --compare [--raw]` | The checkers' VERIFY files against the vault → DIFF; when every mismatch is settled, the report. Normalised by default: numbers in one form (10^-2 = 1e-2 = 0.01, signs kept), Greek letters and roots by name in options, an A-R row's blank options read as the paper's ARSET, a blank marks_part on an unlabelled question read as the question's mark (card D4), lead-in numbers repeated on sub-parts (Q-094), numbers printed in the part not taken as figure values, and an MCQ key line's option value. Unit prefixes, signs and the order of numbers are never normalised. It prints "N cleared by notation and conventions (raw comparison: M)". `--raw` compares the 2026-10-05 way. |
| `G push` | Retry the push. |
| `G show` | What waits in `V/work/` and what is sealed. |

| Exit | Means | Do |
|---|---|---|
| 0 | Done | Next step. |
| 1 | Mismatches not settled | R§8. |
| 2 | Refused | Read each `x` line, fix the part file against the images, rerun. |
| 3 | Merge failed; the vault was rolled back to before this commit | Read the message, fix, rerun. If the kit itself is wrong, R§11. |
| 4 | Committed, push failed | `G push`; if it fails again, keep working and report it. |

Outputs: `<outputs>/vault/` keeps the newest three packs of this route (chat-era files are never deleted); `<outputs>/logs/GATE-LOG-B<nn>.md`; `<outputs>/logs/doublecheck/B<nn>/` (the check files of every year check); `<outputs>/README.md`, the dashboard, rewritten at every commit and checkpoint from the vault. The gate prints its link; copy it into your report.

## R§10 · S5: scoring lines from the schemes
- **Units.** One unit per set section of a scheme, under the paper_id of the paper it marks (55/1/2 → `2024-5512`); 2024 and 2025 print one PDF per series holding sets 1 to 3 (page ranges in CONVENTIONS "Y<year> schemes"). Read the original scheme file, never a bundle. A Hindi-medium twin is set DONE with its English unit and never gets a unit of its own (card C12).
- **Worksheet.** In the chained call before the Agent call: `python3 T/phy_s5_prep.py --pid <pid> --scheme <fid> --pages <a-b> [--origin-scheme <fid> --origin-pages <a-b>] --out /home/claude/render/<pid>/PREP.md` (rows needing lines with their scheme pages, the rows in full, formats, shuffled questions against the origin's scheme, examiner-instruction words), then `python3 /mnt/project/phy_marks.py --fid <fid> --pages <a-b> --out /home/claude/render/<pid>/PREP.md`, which appends the printed-marks list (card C8). On the 2024 schemes (20 set sections, tested 2026-10-21) it listed 2,715 printed marks; its own check matched 649 of 667 printed totals and marked the other 18 with `**`; and against the year-checked lines no question differed except where an OR or "Alternatively" explains it. On a scan it prints "no text layer": the marks are then compared on the image only.
- **Born-digital schemes** (2024): bands as card B3, with the text layer as the digit cross-check; **scanned schemes** (2026): no dual-read, 400 dpi crops for every mark and half mark.
- The examiner-instructions pages: to CONVENTIONS and register R14 (PHY-02 scheme-pass rule). Once per year; later sets note only differences from the newest CONVENTIONS "Examiner instructions, <year> board schemes" entry (card C13).
- Map the scheme's answers to the paper's rows by content (numbering can differ; the mapping goes in `V/notes/Y<year>.md`).
- Scoring lines only for this paper's `rel = origin` rows; shuffle rows inherit their origin's lines. If a scheme prints different values for a shuffled question, note it and add a Q-QUEUE item; never a second set of rows (card C2).
- One STEP-AWARDS row per printed scoring line, in printed order, as card C4 (template there); MCQ and A-R keys as card C5; unmarked routes and alternatives as C6; special awards as C7; marks layout as C8 (a half belongs to the line it is printed beside; page breaks as C15); physics check as C9; FORMULAE result rows as C11.
- In the unit that finishes the last set of a scheme file, `<pid>__ERRATA.csv`: status DONE for the scheme file and its Hindi-medium twin (card C12).
- Then: `G check <pid> --stage S5` (the reader, until CHECK PASS with every LINT warning settled) → `G commit <pid> --stage S5 --single-read --progress "S5 scheme <code> ("`.
- **No scheme** (2026 compartment 55/7 and 55/B/7; 2025C-55S2 and -55S3; any 2023 or 2022 paper without one): in the closing sweep, after S6, because these need archetype codes. Per question: `TRANSFERRED:<award_id>` from a PRINTED line of the same archetype (structure only; this paper's numbers recomputed in Python, never the other paper's), else INFERRED; never both kinds on one question (V09). The gate checks that every TRANSFERRED source is a PRINTED line in the vault. Units `TR-<pid>`, `--stage OTHER`.

### R§10.1 · The S5 checker brief
As R§7, with these differences. Input: `<unit>__SKELETON-S5.csv` (instance_id, q_no, side, part, scheme_file_id, scheme_pages). Read the scheme pages only. VERIFY-S5 columns: `instance_id, step_marks, key, numbers, note`:
- step_marks: the marks of every scoring line printed for this answer, in printed order, separated by " | " (0.5 for ½), each the mark printed beside its own line;
- key: for an MCQ or assertion-reason answer, the printed option letter;
- numbers: the final numerical answers printed, each with its unit;
- note: anything unreadable, and for each half, the words printed beside it when they help (e.g. "½ beside 'For non-conducting sheet'").

## R§11 · Changing the kit and the tools (rare)
The kit and the gate change only for a real bug that blocks correct data, never to make a check pass on wrong data.
1. **The kit** (`pyqkit.py`): add a Q-QUEUE item describing the failure; copy `/home/claude/pyqkit.py` to `/home/claude/pyqkit_before_fix.py`; make the smallest fix with a comment `# kit <new edition>: <why>`; set `KIT_EDITION` later; test (`K validate V` as before; `K check-paper V <pid>` for every mined paper; a planted case shows the bug gone); log it (CONVENTIONS entry, PHY-03 addendum entry); `G checkpoint --message "kit <edition>: <what>"`. The pack carries the kit inside the vault (`tools/pyqkit.py`), and the setup prefers the newer copy. Put a copy in `<outputs>/tools/pyqkit.py` and tell her once to replace the instructions-repository copy.
2. **The gate, the setup and `phy_marks.py`** live in the instructions repository. A new edition is made and tested in the project chat on a copy of the vault and uploaded by her to the root of main (gate 2026-10-21 and `phy_marks.py` were made that way). A bug found here: the smallest fix in a copy at `<outputs>/tools/`, run by its full path until she uploads it; log it as for the kit.
3. **Claude Code's own tools** in `T` (`phy_bands.py`, `phy_tile.py`, `phy_s5_prep.py`, `phy_s3_prep.py`, `phy_measure.py`, `phy_notes_apply.py`): Claude Code may extend them for her decisions (the size warnings, the weighted measurement, the sibling worksheet), each change with a one-line CONVENTIONS note and a test on real files before its first use. They only locate, render and measure; none ever writes a value into a row from a text layer.

## R§12 · The closing sweep: S5 without schemes, S6, S7, S8 (after 2022; PHY-08 Y§12)
**S6 classification** (P§10.3; CONVENTIONS "Classification rule (P§10.2 applied)"):
1. `K derive V`; estimate the sweep in usage windows (Y§12 step 1); then, per year, newest first, predict which existing codes the year should contain and write the prediction in `V/notes/Y<year>.md` before classifying.
2. A script groups origin rows whose text and numbers match across years and sets (questions CBSE repeated); one decision per group, written to every member as its own CLASSIFY row.
3. Chapter by chapter, by a `phy-reader` working from text only (no images; figures through their FIGURES rows): for each row, `K candidates V --instance <id> --k 5`; apply the granularity test; assign an existing code, promote a DRAFT seed (it keeps its number), or issue a new code (next serial in the chapter) with name, asks_you_to, skeleton and traps. Check names by a script against CI§10 (name ≤ 12 words, no symbols; asks_you_to ≤ 30 words and starts "Asks you to").
4. CLASSIFY rows in `V/work/S6-CH<cc>__CLASSIFY.csv`, every field as the vault's existing CLASSIFY rows, `rule_version` "P10.3/B<nn>-<date>". Shuffle rows copy their origin's values.
5. REGISTRY changes: `j/REGISTRY.csv` is re-runnable Layer 1.5; write it with the kit's own `read_table` and `write_table` in a short script. Never write an `l1/` table that way.
6. `G commit S6-CH<cc> --stage OTHER` after each chapter (validate checks every code exists and is VERIFIED); the last chapter adds `--progress "S6 classify"`. Then the misses per year in `notes/Y<year>.md`: predicted but absent; present but never seen before.

**Before S7 and S8, per year:** tick the S2b line when a script shows every paper has a BLUEPRINTS row; FILES statuses through ERRATA (unit `S8-FILES`, `--stage OTHER`): question papers DONE once their S5 and S6 are done; Q-010 (the Batch 0 SQP rows' FIGURES and FORMULAE, unit `SQP-GAPS`); Q-097 and the other closing-sweep items in QQUEUE.

**S7:** `K derive V` · `K export-xlsx V <year> --out <outputs>/reports` · judged observations in `notes/Y<year>.md` · `G checkpoint --message "S7 derive and workbook" --tick "Y<year> S7"`.

**S8:** `K validate V` · `K year-close V <year> --xlsx-dir <outputs>/reports` (every line must PASS; a FAIL keeps the year open and names what is left) · copy the year report it names to `<outputs>/reports/PHY-YEAR-<year>-REPORT.md` · `G checkpoint --message "year <year> closed" --tick "Y<year> S8"`.

## R§13 · `Fix:` and `Audit.`
- `Fix: <text>` (from her, or a chat-audit finding she passes on): find the row(s); a fresh `phy-reader` confirms on a crop of the page and writes the ERRATA rows (old, new, reason, evidence = the crop path and what it shows) to `V/work/FIX-<n>__ERRATA.csv` (n = the next free number), including every shuffle copy of a corrected origin row; `G commit FIX-<n> --stage OTHER`; `K derive V` if Layer 2 depends on it; a one-line confirmation. If the crop shows the vault was right, say so in one line with the crop path, and change nothing.
- `Audit.`: `K validate V`; `K check-paper V <pid>` for every mined paper; `G lint --all`; a fresh blind checker on a 10 % sample of every paper's rows (a skeleton of the sampled rows, R§7, compared by a script against the vault rows); findings settled from crops and fixed as ERRATA through the gate; `K derive V`; a report in `<outputs>/reports/PHY-AUDIT-<date>.md`.
- Standing permission (CLAUDE.md §12): a queued fix whose page evidence is already logged is applied without waiting for her `Fix:` line, after a reader confirms it again on the page image.

## R§14 · Context, usage, the cloud machine, pushes
- **Measure every unit** (her decision 2026-10-21): after each commit, `T/phy_measure.py` on the unit's reader transcript gives steps, images (count, total bytes, largest file), the first step's cache read against its cache write, cache misses, the raw sum and the weighted sum in base-input equivalents (cache read 0.05, 5-minute cache write 1.25, 1-hour cache write 2, uncached input 1, output 5) and each component's share, and the image check (each image's width and height as sent, from the image data stored in the transcript when it is there, else from the file on disk; its cost ⌈width/28⌉ × ⌈height/28⌉; for steps that read only images, that sum against the step's context growth minus its own output, per kind of image: a ratio well below 1 means an image was shrunk before the model saw it). One line per unit in the gate log's unit block or the session report; the baseline is `outputs/reports/PHY-USAGE-BASELINE.md`.
- Compaction: CLAUDE.md is re-read automatically; also re-read the open lines of PROGRESS and this file's section for the stage, and run `G show`. Part files in `V/work/` and sealed files survive a compaction.
- **Usage stop** (her decision 2026-10-21): stop at a unit boundary; the last commit is the checkpoint; end the report with `next: new session, then Go`. She starts a new session after the reset: a conversation idle past its cache lifetime re-sends everything at the full write rate on its next turn, and a new session with the lean boot costs less.
- Machine replaced (files gone): rerun the setup (it keeps the batch for this session), then redo the unfinished unit from the start. At most one unit is lost.
- Push failure: `G push`; commits pile up locally until it works; report it.
- Branches: the gate pushes to this session's branch, and the setup has already carried the earlier results forward into it, so the newest branch holds everything. She never merges anything; the dashboard link shows it all.

## R§15 · Reports
- Session report as CLAUDE.md §11. Numbers come from the gate output, `<outputs>/logs/GATE-LOG-B<nn>.md`, `K status V` and `T/phy_measure.py`. Add one line on usage: the units' weighted sums against the baseline, and which component (output, cache writes, cache reads) took the largest share. The line before the RESUME line is `Dashboard: <link>`, the link the gate printed at its last save.
- A year-check report is written by the gate (R§8 step 7); a year's lessons go to `V/notes/PHY-03-ADDENDUM.md`.

## R§16 · Exceptions on this route
| Situation | Action |
|---|---|
| Setup exit 4 (no vault anywhere) | Stop. One line to her: upload the newest PHY-VAULT file to the project repository, then type `Go.` |
| Two copies of a tool or instruction file | The setup uses the newest and warns; name the extra copies in your report for her to delete. |
| A repository missing (exit 5 or 6, or no papers) | One line to her; do the work that doesn't need it. |
| Kit in the instructions repository older than the vault's | Fine: the setup uses the newer one. Mention once. |
| `phy-reader` not offered by the Agent tool | General-purpose subagent with the same brief plus "read the rule card first" (R§2); say so once. |
| `render` cannot find a file | Find it by sha256 (R§3 rule 6). |
| A reader fails or returns nothing | Resume it if its context is intact, else run a fresh reader with the same brief (R§6). Still failing: one line in the report; the unit waits. Never read the pages in the main session. |
| An image over 450 KB or over 1568 px | Split it (more bands or smaller crops), never send it (card A9). |
| A worksheet locates fewer questions than the paper prints | Fix the worksheet before any reader starts (B6-5). |
| `phy_marks.py` prints "no text layer" or many `**` lines on a scheme | Compare the marks on the image only; mention it once in the report. |
| A LINT warning the reader could not settle | Its return names it; a fresh reader settles it on a crop before the commit. |
| The checker disagrees on many values of one page | Re-render that page; a fresh checker redoes that page's rows only. |
| The kit rejects a correct row | R§11. |
| A paper fails check-paper after a re-read | Quarantine it (CI§2.12): Q-QUEUE item with the failing line, PROGRESS note, continue with the next paper. |
| Context heavy | Stop at the next gate commit; report; she types `Go.` |
| Usage runs out | Stop at a unit boundary; `next: new session, then Go` (R§14). |
| She asks a physics question | One line + "that belongs in the study project". |
| A file of another year appears | Inventory logs it NEW; it waits for its year (CI§7). |
| A file of a year before 2022 appears | Logged NEW and left alone: five years only (her decision 2026-10-21). |
