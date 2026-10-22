# Audit of the Claude Code work on 2024 · Batches 4 to 6 · 2026-10-21

*Every number below was computed from the vault PHY-VAULT-B06-20261021-1112-16960r.json, the git log, gate logs and check files of branch claude/bold-rubin-sk5l5o (head 44731cb), and the 2024 scheme PDFs in her repositories. This audit read the vault and changed nothing in it; the replays and tests ran on copies.*

## Verdict
The 2024 work is complete, and after its year check it is clean. Every 2024 paper (20: the 15 main-series papers, 55(B), and the four compartment papers), every 2024 scheme section, and the 2023-24 sample paper with its scheme are in the vault. All 16 vault checks pass after every save, no paper is quarantined, and no row is unreadable. Four things matter for what comes next:
- the year check found ten real errors in 2024's single readings, six of one kind (measurements written as figure values), and all ten are fixed;
- two of those kinds are now caught at the unit, not a year later: the gate's lint catches the figure-value kind, and `phy_marks.py` puts the half-mark kind in front of the reader;
- the normalised comparison would have cleared 94 of the year check's 161 mismatches as the false alarms they were, losing no real error;
- six queue items addressed to the 2024 year check are still open; three are page checks for the next session's first FIX unit.

## Size
- Vault: 16,960 rows (INSTANCES 4,639; FORMULAE 4,681; STEP-AWARDS 4,528; FIGURES 881; CONSTANTS 717; ERRATA 603; and the smaller tables).
- 2024 board papers: 1,442 question rows, of which 782 are unique and 660 are shuffles; 179 unique numericals; 1,441 scoring lines, all printed.
- Unique 2024 question types: MCQ 242, NUM 179, CON 102, DRV 71, DEF 67, AR 32, GRF 27, PRD 26, CMP 16, DGM 9, DEV 8, EXP 3.
- 2023-24 sample paper: 63 rows, 108 scoring lines, 7 constants.

## The papers
| paper | code | exam | rows | new | shuffles | figures | formulae (paper) | scoring lines | result rows (scheme) |
|---|---|---|---|---|---|---|---|---|---|
| 2024-5511 | 55/1/1 | MAIN | 79 | 79 | 0 | 12 | 76 | 137 | 19 |
| 2024-5512 | 55/1/2 | MAIN | 78 | 17 | 61 | 14 | 72 | 29 | 5 |
| 2024-5513 | 55/1/3 | MAIN | 79 | 19 | 60 | 11 | 75 | 29 | 5 |
| 2024-5521 | 55/2/1 | MAIN | 66 | 66 | 0 | 13 | 73 | 139 | 11 |
| 2024-5522 | 55/2/2 | MAIN | 68 | 17 | 51 | 16 | 75 | 25 | 4 |
| 2024-5523 | 55/2/3 | MAIN | 65 | 14 | 51 | 12 | 73 | 23 | 4 |
| 2024-5531 | 55/3/1 | MAIN | 73 | 73 | 0 | 17 | 84 | 146 | 15 |
| 2024-5532 | 55/3/2 | MAIN | 70 | 16 | 54 | 20 | 81 | 30 | 5 |
| 2024-5533 | 55/3/3 | MAIN | 71 | 17 | 54 | 14 | 86 | 35 | 5 |
| 2024-5541 | 55/4/1 | MAIN | 69 | 69 | 0 | 17 | 76 | 142 | 15 |
| 2024-5542 | 55/4/2 | MAIN | 70 | 15 | 55 | 19 | 77 | 31 | 7 |
| 2024-5543 | 55/4/3 | MAIN | 68 | 13 | 55 | 17 | 76 | 33 | 6 |
| 2024-5551 | 55/5/1 | MAIN | 71 | 71 | 0 | 8 | 76 | 132 | 13 |
| 2024-5552 | 55/5/2 | MAIN | 71 | 18 | 53 | 9 | 80 | 33 | 7 |
| 2024-5553 | 55/5/3 | MAIN | 69 | 15 | 54 | 9 | 80 | 32 | 8 |
| 2024-55B | 55/B | MAIN | 73 | 73 | 0 | 0 | 67 | 126 | 8 |
| 2024C-55BS | 55/B/S | COMPT | 81 | 81 | 0 | 0 | 82 | 121 | 13 |
| 2024C-55S1 | 55/S/1 | COMPT | 74 | 74 | 0 | 12 | 73 | 135 | 22 |
| 2024C-55S2 | 55/S/2 | COMPT | 75 | 18 | 57 | 10 | 75 | 32 | 2 |
| 2024C-55S3 | 55/S/3 | COMPT | 72 | 17 | 55 | 10 | 77 | 31 | 3 |
| SQP2324-042 | (sample paper) | SQP | 63 | 63 | 0 | 18 | 77 | 108 | 17 |

Every paper has its blueprint row and its two case rows. Every 2024 paper has its constants (220 rows). The 2024 visually-impaired paper's code word matches no main series, so its rows carry `series=55/B` and are all origins (CONVENTIONS Batch 5). The 2024 compartment scheme covers all three sets, so no 2024 paper waits for transferred lines.

## Checks
1. **Vault checks:** 16/16 pass, at every save of Batches 4 to 6.
2. **Coverage:** no gaps in 2024: every figure question has its figure row, every numerical and derivation its formula row; no blank relations; no options on non-choice rows.
3. **Scoring lines:** all 1,441 lines of 2024 are printed lines; every part's lines add up to its printed marks and every multiple-choice row has its key line; 53 lines carry a "(sic; …)" correction of a scheme error and 115 record accepted alternatives. Of the 563 numerical rows across the vault that have printed lines, 551 have a scheme result row and the other 12 have symbolic answers.
4. **The lint over the whole vault** (gate 2026-10-21, run on a copy): one finding, outside 2024: SQP2627-042-Q25-II, whose one scoring line carries 0 against the printed 1 of a 2+1 split. It goes to the next session's first steps.
5. **Detail of the new rows** (all unique rows of each year's board papers):

| | figure description | formula rows per numerical or derivation | rows with a note | rows with givens |
|---|---|---|---|---|
| 2024 | 631 characters | 1.38 | 91 % | 73 % |
| 2025 | 615 characters | 1.46 | 89 % | 75 % |
| 2026 | 180 characters | 1.04 | 37 % | 64 % |

## The lean reading trial (19 October, read in the project chat)
Every line of 2024-5512 and 2024-5513, the first two units read by the rule card's method, was checked on the scheme pages: 58 of 58 lines exact, Section A keys 32 of 32, every numerical correct. 95 lines of the old-method 2024-5511 were checked the same way: 95 of 95 exact. The method was approved for quality that day (CONVENTIONS "Lean reading, part 2"); its saving was then still to be measured.

## The 2024 year check
| | first round (all 2024) | second round (2024-5531) |
|---|---|---|
| Tier 1 suspects | 122 (text layer) | 12 (text layer) |
| question rows re-read | 262 (direction 66, sample 88, text layer 122; 14 rows were both direction and text layer) | 73 (all 57 new rows, direction 6, text layer 12) |
| scheme parts re-read | 88 (sample) | 73 |
| values compared | 1,732 | 557 |
| mismatches | 132 at the first compare, 126 after the fixes | 29 |
| decisions | 137: vault right 127, vault fixed 10 | 29: vault right 29 |

The ten real errors, and how each was found:
- **Six figure-value errors:** measurements of the drawing written into FIGURES `values` (93 px and 44 px plate lengths; a drawn "45 deg" three times; slopes "about 42 deg against about 30 deg"; axis intercepts "about 0.20, 0.39, 0.57"): F-2024-5512-03, F-2024-5521-11 and its two shuffle copies F-2024-5522-16 and F-2024-5523-12, F-2024-5542-01, F-2024-5532-02. Four were found through the figure-direction list and two through the text-layer check. Fixed by FIX-6 (ER-B06-013 to -017) and FIX-7 (ER-B06-021, -022).
- **One half-mark shift:** 2024-5531-Q31B-ii's halves sat one line off, with the right total. A later reader had queued it from a sibling scheme's page (Q-078); the year check's sample confirmed it; FIX-7 (ER-B06-023 to -027) re-attached the halves. Because it was a real error in a sampled scheme part, 2024-5531 went to a second round, which found nothing else.
- **Three page citations:** lines running over a page break cited the page where their text starts, not where the mark is printed (SA-2024-5512-Q28-a-01, SA-2024-5513-Q27-d1-01 and -02), queued by the lean trial under the new rule (Q-072) and aligned by FIX-6 (ER-B06-018 to -020).

The 156 decisions that found the vault right were false alarms of the comparison: by field, numbers 79, options 39, marks_part 22, figure values 14, scheme marks 1, key 1. 47 of their notes name the lead-in rule (Q-094); all 22 marks_part ones are the card's D4 convention (no mark printed beside an unlabelled question).

## The upgrades, tested on 2024's own files
- **The normalised comparison** (gate 2026-10-21), replayed on a copy of the vault as it stood before the fixes, with 2024's own check files: the first round's 132 mismatches fell to 62 and the second round's 29 to 5. All 94 cleared mismatches had been decided "vault right"; none was added; all six real-error mismatches stayed. The half-mark shift was found by the sample, not by a mismatch, so the comparison cannot hide it. The raw way (`--raw`) still gives 132 and 29.
- **The lint**, run on the same pre-fix copy: exactly the six figure-value errors (six "figure-measured" findings, no other). With only the origin's erratum applied to F-2024-5521-11, it named both shuffle copies still holding the old value. On the current vault: the one finding above.
- **`phy_marks.py`** (new, made in the chat): on all 20 set sections of the 2024 schemes (16 main, 4 compartment) it listed 2,715 printed marks with the text at their height; its own check matched 649 of the 667 printed totals and marked the other 18; against the year-checked lines, 368 questions agree exactly, 31 differ only where an OR or "Alternatively" explains it (cards C5 and C6), 255 are shuffles with no lines of their own, and none differs without an explanation. On 2024-5531-Q31B-ii it lists the four halves beside E_c, "For non-conducting sheet", "Since surface charge density is same." and "2E_nc = E_c", and none beside the figure: the error FIX-7 corrected.

## Pace
Minutes from one save to the next within a run (git log):
- Batch 4 (6 October): the opening steps, 2024 intake (32 new files, 115 identity errata), the year plan and 2024's constants; its saves ran from 03:38 to 03:58 UTC.
- Batch 5 (6 to 18 October, stops of five and six days between runs): origin papers 18.7 to 20.1 minutes, sibling papers 12.5 to 17.1, the two visually-impaired papers 19.7 and 20.4.
- Batch 6 (19 to 21 October): origin schemes 10.2 to 13.7 minutes, the visually-impaired papers' schemes 9.9 and 12.0, sibling schemes 4.5 to 7.8; then the sample paper and the year check.
- Usage: Claude Code's figures give a sibling scheme 1.53 million raw tokens under the bands and the step budget (55/2/2), against 5.56 million before (55/1/2). Raw sums count re-read history like new input, which the plan meter does not, so from now on every unit is measured by its weighted sum (her decision 2026-10-21; PHY-08 Y§1).

## Corrections made in Batches 4 to 6
166 errata: 118 in Batch 4 (115 FILES identities from page-1 images for the 32 new files, and FIX-4's three: 2025-5553-Q29-ii made a full row, as the 2025 year-check script had found), 21 in Batch 5 (20 file statuses, and FIX-5's ARSET removal from a shuffle), 27 in Batch 6 (12 file statuses, and the 15 year-check fixes of FIX-6 and FIX-7). No other saved row needed a correction.

## Open questions raised in Batches 4 to 6
- **Left open by the 2024 year check, though addressed to it.** Page checks, for the next session's first FIX unit: Q-073 (55/2/1 Q31(a): which part a printed half belongs to; 2024-5521-Q31A totals 4.5 against 5), Q-085 (the 55/5/1 Q17(a) drawing's labels against SA-2024-5551-Q17A-01), Q-088 (a sixth half below 2024C-55BS-Q22B's r_eq line). Decisions about doubtful keys, for the mocks: Q-075 (55/2/3 Q1's key ignores a sign), Q-077 (55/3/1 Q30: 6 or 5 peaks), Q-082 (55/4/2 Q2: magnitudes only).
- **Scheme against physics, kept as printed:** Q-074, Q-079, Q-080, Q-081, Q-083, Q-086, Q-089, Q-090, Q-091.
- **Marks layout:** Q-070, Q-084, Q-087, Q-095, Q-096, and Q-097 (case rows' `printed_split`; stem values marked "(stem)" in figure values), the last for the closing sweep.
- **Papers:** Q-076 (a gold-foil exponent: the 2025 year check settles 2025-5562's value from its own page), Q-093 (SQP2324-042 Q28's OR).
- **Rows:** Q-094, settled by her on 2026-10-21 (lead-in numbers on every sub-part row): three SQP2324-042 rows to align.
- **Files and tools:** Q-067 (Hindi-medium scheme twins given S5 lines by the planner: fixed in gate 2026-10-21, tested on 2024's files, 24 S5 lines becoming the 20 real ones), Q-068 (sample paper 2023-24), Q-069 (FILES `lang` on bilingual papers, for the closing sweep), Q-071 (the runbook to name the rule card: answered by PHY-07 2026-10-21).
- **For the 2025 year check:** Q-065 and Q-066 (2025C-55S1 and 2025C-55BS schemes saved without the double-read).
- **Resolved in Batch 6:** Q-072, Q-078, Q-092, Q-098.

## Lessons recorded
Batches 5 and 6 wrote their lessons into the ledger addendum (B5-1 to B5-3, B6-1 to B6-5). PHY-03 2026-10-21 adds what this audit and the upgrades found (W-17 to W-23).

## Left for later
- **Next session (Batch 7):** PHY-08 Y§0.5: the tools' size warnings and the weighted measurement; the rule card edition 2026-10-21 installed; the gate's replay repeated on Claude Code's machine; the lint finding settled; one FIX unit for Q-094's three rows and the page checks Q-073, Q-085 and Q-088; a CONVENTIONS correction of "Viewer limit (B06)"; then the 2025 year check.
- **Then:** 2023 (with the sibling worksheet built and tested at its start), 2022 (Term 2 and Term 1), and the closing sweep (PHY-08 Y§12).

## What changed in the instructions (2026-10-21)
- **CLAUDE.md:** the lean boot; `phy-reader` subagents for every reading, check and adjudication; the main session never opens an image; two main-session steps per unit; a new session after every usage stop; five years only; the gate's lint and normalised comparison in use.
- **`.claude/agents/phy-reader.md`** (new): the reader agent; its prompt points to the rule card.
- **Rule card edition 2026-10-21** (installed into the vault by the next session): blind checkers never open the vault (A3); image sizes (A9); the lint (A10); the printed-marks list (C8); lead-in numbers on every sub-part, case studies as before (D5); measurements never in figure values (D10); the sibling worksheet (D15).
- **PHY-07, PHY-08:** new editions for all of the above.
- **Gate (edition 2026-10-21):** the advisory lint in `check` and as `lint`; the normalised comparison with `--raw`; lint findings as year-check suspects; the cleared count printed exactly; no S5 line for a Hindi-medium twin scheme (Q-067).
- **`phy_marks.py`** (new, edition 2026-10-21): the printed-marks list for S5 worksheets.
- **`phy_replay_2024.py`** (new, one-time): repeats this audit's replay on Claude Code's machine before the 2025 year check (PHY-08 Y§0.5 step 3).
- **Setup (edition 2026-10-02b) and kit (2026-09-30b):** unchanged; nothing in Batches 4 to 6 needed a change to them.
