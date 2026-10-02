# Audit of the Claude Code work on 2026 · 2026-10-02

*Every number below was computed from the vault PHY-VAULT-B02-20261002-0436-5049r.json, its gate log and its double-check files (branch claude/beautiful-pascal-k4durg). This audit only read the vault; it changed nothing.*

## Verdict
The work is real, careful and accurate. Every 2026 question paper (21, compartment and visually-impaired included) and every scheme (16 board schemes and the 2025-26 sample paper's) is in the vault. All 16 vault checks pass and no paper is quarantined. Two slips happened overnight and both were caught and fixed; two old errors from the chat batch were found and fixed. What remains of 2026 is analysis, now deferred.

## Size
5,049 rows in all: 1,421 question rows across 21 papers, 1,222 scoring lines (all printed), 57 files recorded.

## Checks
1. **Vault checks:** 16/16 pass.
2. **Coverage:** every figure question has its figure row and every numerical or derivation its formula row, except the 8 sample-paper rows from Batch 0 already queued (Q-010).
3. **Shuffles:** all 622 match their originals. The 19 stem differences are only the printed sub-part label, which changes with position (correct).
4. **Scoring lines:** every part's lines add up exactly to its printed marks; no shuffled question has its own lines (they inherit); the 3 multiple-choice rows without a key line are questions the scheme awards for any attempt, stored correctly as plain lines. Two sample-paper rows for visually-impaired candidates have no lines: check at the closing sweep whether the scheme prints answers for them.
5. **Scheme errors:** flagged on the lines as "(sic; …)" with the correct value. Recomputed here: 55/3/1 Q31(a)(ii) gives U = 6 + 15 − 0.15 = 20.85 J, not the printed 8.85 J (the scheme dropped the sign of x₁). 55/5/2 Q11: α = ω/v = 1.5×10¹¹ ÷ 2×10⁸ = 750 m⁻¹, the origin's key (C); the scheme's (A) is its own misprint (Q-015).
6. **Visually-impaired papers:** zero shuffles was right. 63 of 55(B)'s 65 questions and all 66 of 55(B)/7's match no series question closely: they are separate papers.
7. **Classification (chapters 01 and 02):** 181 rows coded, every code verified, names and "asks you to" lines within the rules, every shuffle carries its origin's code.

## The double-read
- Trial papers: 366 and 381 values compared; 16 and 15 mismatches; every one was the checker's notation or scope, none a wrong value.
- Overnight papers: 267 to 340 values each; 18 to 41 mismatches each, again notation and scope, except 55(B)/7, where it caught the extractor writing note text into the options column of 36 rows (fixed before saving).
- Schemes: 0 to 8 mismatches each; on 55/4/3, two scoring values were corrected before saving.

## Max (overnight) against xhigh (trial)
New rows of the regular sibling papers, compared like for like:

| | Batch 1 (chat) | Trial (xhigh) | Overnight (max) |
|---|---|---|---|
| figure description, characters | 90 | 201 | 143 |
| formula rows per numerical or derivation | 1.85 | 1.86 | 1.38 |
| rows with a note | 20 % | 61 % | 35 % |
| rows with givens | 63 % | 74 % | 73 % |
| wrong values found by the double-read | (none run) | 0 | 0 |
| minutes per sibling paper | (chat) | 38 to 47 | 10 to 16 |

Same accuracy. The overnight run was three to four times faster because it had learned the routine, and a little thinner in figures, formula rows and notes. Max bought nothing measurable; xhigh is the right setting. PHY-08 Y§6 now asks for the trial's level of detail.

## Fixed during the run
- Batch 1 error: the 55/3/1 Q17(a) battery stored the wrong way round (ER-B02-081, -082).
- Batch 1 error: 55/7/1 Q29(iii) had vec(v) where the page prints a plain v (ER-B02-104, -105).
- Overnight slip: 15 new rows of 55/5/2 saved with a blank relation (ER-B02-088 to -102).
- Overnight slip: note text in the options column of 36 rows of 55(B)/7 (caught by the double-read).
The gate now refuses both slip types.

## Deferred to the closing sweep (after 2022's printed documents)
- Scoring lines by transfer for the 2026 compartment papers (they need classification first).
- Classification of chapters 03 to 14 and the misses against its 53-code prediction; S7 workbook; S8 year-close.
- Sample paper: 6 figure rows, 2 formula rows (Q-010), and the 2 visually-impaired rows without lines.
- File statuses (the question papers stay IN-PROGRESS until classification).
- Granularity: 42 new codes for the 181 rows of chapters 01 and 02, many used once. Review before classifying all years (Q-018).

## Your repositories
- The browser saved three uploads as `phy_gate (1).py`, `phy_code_env (2).py` and `PHY-07-CLAUDE-CODE-RUNBOOK (1).md`. The old boot command looked for exact names, so a new session would have failed at its first step. The setup now accepts these names and picks the newest copy.
- Main has no kit file. That's fine: the kit travels inside the vault and the setup takes it from there.

## What changed in the instructions
- **New PHY-08 year playbook:** the work order, year start, constants, papers, schemes, the detail standard, the traps 2026 hit, and how to save usage without losing accuracy.
- **CLAUDE.md:** your new work order (printed documents first, 2025 down to 2022), the deferral, the first-session steps, and a boot command that accepts renamed files.
- **PHY-07:** the new commands and refusals.
- **Gate (edition 2026-10-02):** refuses blank relations and options on non-choice rows; plans a year's progress lines from its files; marks deferred lines.
- **Setup (edition 2026-10-02):** accepts browser-renamed copies and picks the newest.
