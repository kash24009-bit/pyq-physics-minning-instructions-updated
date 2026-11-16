# PHY-09 · Closing plan for Physics (042) · written 2026-11-16

*The order of the work left after Batch 10, its size, and the upgrades that come with it. It replaces CLAUDE.md §12's work order and the CONVENTIONS order entries of 2026-10-26, 2026-11-12 and 2026-11-15 from the next session on. It changes nothing in the truth rules (CLAUDE.md §4), the gate, the rule card, one unit at a time or one fresh reader per unit. The draft PHY-09 of 2026-11-10 on the branch claude/boot-pack-closeout-fable-week (the Fable week, `phy_boot.py`, `phy_closeout.py`) was never merged into main and is not used; this file takes its name.*

## §1 · Where it stands (vault B10, computed 2026-11-16)
- Mined: every paper and scheme of 2026 to 2022 in the repositories: 107 papers, 3,130 questions, 6,842 rows, 6,917 scoring lines; 16/16 vault checks pass. Not yet mined: the Term 1 sample paper 2021-22 with its scheme, and the 2024-25 sample paper (its scheme is not in any repository).
- Done once per year: the 2024 year check. Open: the 2025, 2023 and 2022 year checks.
- Deferred to now: pattern sorting (S6) for every year, derive and workbooks (S7), scoring lines for the papers without a scheme, and the year-closes (S8).
- The audit of 2026-11-16 (PHY-AUDIT-2023-2022-B10) found four things to fix; they are its `Fix:` lines.

## §2 · Order of work (a new session at each step and after every usage stop)
If her message names a step ("year checks first", "2025 check now"), that step comes first and the rest keep this order. A step whose repositories are not attached is skipped with one line in the report; the next step that can run goes on.

**Step 1 · Opening steps (about 1 session).** Repositories: the instructions repository; PHY-PHYSICS-2023 and PHY-PHYSICS-2023-MS for the fixes.
1. Install the kit edition 2026-11-16 that the setup picked from the instructions repository (it differs from 2026-09-30b only in Q-145: a section mark written UNK stays unknown and its mark sums are not checked; tested in the project chat: identical check-paper output on all 107 papers, a 55-question Term 1 paper passes, a missing question still fails): copy `/home/claude/pyqkit.py` over `/home/claude/vault/tools/pyqkit.py`, run `python3 /home/claude/pyqkit.py validate /home/claude/vault`, then `python3 /home/claude/phy_gate.py checkpoint --message "kit 2026-11-16 (Q-145) shipped in the vault"`.
2. CONVENTIONS, one entry of at most eight lines, "Closing plan and pattern sorting (her decision 2026-11-16)": this file's order, PHY-10 (families as skill groups; the prediction made leave-one-year-out after sorting), kit 2026-11-16, `phy_s6.py` 2026-11-16. Through `G checkpoint`.
3. FIX-10: the four `Fix:` lines of PHY-AUDIT-2023-2022-B10, each confirmed again on the page image by a `phy-reader` (55/2/1 pp21-23 with the 55/2 scheme pp14-15; 55/5/1 pp17-19; the 55/5/1 scheme at Q16), every shuffle copy given its own ERRATA row (W-20), then `G lint --all` shows no finding left in 2023.
4. Tick the Y2022 S2b line: every 2022 paper has its BLUEPRINTS row (21 of 21 on 2026-11-16): `G checkpoint --message "Y2022 S2b" --tick "Y2022 S2b"`.
5. T1-2022-SQP (`Physics-SQP 2022.pdf`, 15 pages, at the root of the instructions repository): S3 as one unit, all MCQs; BLUEPRINTS sections `A:1-25:UNK;B:26-49:UNK;C:50-55:UNK` and the printed attempt rules as its choice rule (Q-126); q_marks_printed UNK on every row (nothing printed per question). Then its scheme (`Physics-MS 20022.pdf`) as one S5 unit. Settles Q-126 and Q-145.
6. SQP2425-042, the 2024-25 sample paper: copy it from history (`git show 7454b3225ed18eaa79219c66f287f53a34f48b3a:"Physics-SQP (1).pdf"` into `V/work/_intake/sqp2425/`, sha256 checked against FILES 1234670d7284…, opened only by its full path; CONVENTIONS B08 "For the later 2025 session"), then S2a and S3. Its scheme (FL-cab79baad0) is in no repository: it stays on her optional list and its S5 line waits for it.

**Step 2 · Pattern sorting, S6 (about 3 to 4 sessions).** No papers or schemes repository needed. PHY-10, chapter by chapter: 02, 01, then 03 to 14 (09 in two halves), the review unit, the misses, each year's S6 line ticked when `phy_s6.py coverage` shows it complete.

**Step 3 · Derive and the papers without a scheme (about 1.5 sessions).** No repository needed.
1. S7 for 2026, 2025, 2024, 2023, 2022 and 2027 (PHY-07 R§12): `K derive`, `K export-xlsx` per year, judged observations in `notes/Y<year>.md`, each S7 line ticked.
2. Scoring lines for the papers without a scheme, after S6 (PHY-08 Y§12 step 2, R§10): 2026C-5571, -5572, -5573 and 2026C-55B7; the new rows of 2025C-55S2 and -55S3 (their shuffles inherit 55/S/1's lines). TRANSFERRED from a printed line of the same code (structure only; this paper's numbers solved in Python with a unit check) or INFERRED, never both on one question.

**Step 4 · Year checks (about 3.5 to 4.5 sessions), one year per fresh session, PHY-08 Y§11 as written.**
1. 2025 (about 2 sessions). Repositories: PHY-PHYSICS-2025, PHY-PHYSICS-2025-2-, PHY-PHYSICS-2025-marking-scheme, PHY-PHYSICS-2025-2-MS, and PHY-PHYSICS-2024-MS for the three 2024 page checks that wait for this session (Q-073, Q-085, Q-088). 55/1 and 55/2 are scans with no text layer, so the script tier cannot cross-check their digits and the sample there is the main guard.
2. 2023 (about 1.5 sessions). Repositories: PHY-PHYSICS-2023, PHY-PHYSICS-2023-2, PHY-PHYSICS-2023-MS. The script tier was run in the project chat on 2026-11-16: 137 text-layer suspects, 272 question rows and 92 scheme parts to re-read (2024: 262 and 88).
3. 2022 (about 1 session). Repositories: PHY-PHYSICS-2022, PHY-PHYSICS-2022-2, PHY-PHYSICS-2022-MS. It may share the end of the 2023 session if usage allows.
Each check ends with Y§11 step 6: every open queue item that names the year is settled or re-addressed (W-21).

**Step 5 · Close (about 1 session).**
1. The queue. 205 items are open; about two thirds only record a printed scheme slip that the line already keeps with "(sic; …)". Those are closed in one checkpoint as "recorded in the line". Convention items (Q-094, Q-097, Q-129, Q-132 and the like) are settled by counting how the vault already does it and back-applying the majority by ERRATA (W-19); one that would change earlier rows against their majority goes to her optional list in one line.
2. FILES: `lang` on bilingual papers (Q-069) and every question paper's status DONE (unit S8-FILES), the Batch 0 sample-paper gaps (Q-010).
3. S8 for 2022 to 2027: `K validate`, `K year-close <year>` until every Definition-of-Done line passes, each year report copied to `outputs/reports/PHY-YEAR-<year>-REPORT.md`, each S8 line ticked.
4. A last `Audit.` (R§13) and the report that says Physics is closed.

| Step | Sessions |
|---|---|
| 1 Opening steps | about 1 |
| 2 Pattern sorting | 3 to 4 |
| 3 Derive; papers without a scheme | about 1.5 |
| 4 Year checks 2025, 2023, 2022 | 3.5 to 4.5 |
| 5 Close | about 1 |
| **All** | **about 10 to 12** |

A session here means what hers have been since the lean method: a little over an hour and about 15 % of a week. Every unit's weighted usage is measured (PHY-08 Y§1); after Step 2's first two units the report says once whether the estimate holds.

## §3 · Upgrades that come with this plan
**In use from the next session**
1. **Pattern sorting by chapter sheets** (PHY-10, `phy_s6.py`): one sheet per chapter, read once, instead of one `candidates` command per row (3,648 commands avoided); repeats and shuffles decided by script; registry, decisions and checks by the tool; the gate's own check on every unit.
2. **Kit 2026-11-16** (Step 1.1).
3. **A lint warning is settled, never queued.** In 2023 two lint findings (the 55/2/1 case choice and the 55/5/1 split marks) went to the queue and stayed wrong until the audit. From now on a reader that cannot settle a warning on its page image returns it as a doubt, and the doubt reader settles it on a crop before the commit (CLAUDE.md §7 step 2, rule card A10). The queue is only for a printed conflict: a scheme against its paper or against physics.
4. **One year per year-check session**, with the repositories named in its handover line.

**Measured, not built (kept for Chemistry)**
- **A number check that reads what the text layer loses.** A prototype tried on the 2023 year check's 137 text-layer suspects cleared 72 by reading a raised dot as a decimal point, a power of ten printed as "10" followed by its exponent, and the paper's own constants (minus signs never cleared, because the text layer drops them). It would cut the 2023 re-reading list by about a quarter, and do little for 2025, whose two scanned series have no text layer. It needs a replay on the 2024 year check's own files before any use, so it is built into the Chemistry gate from the start rather than added now.

**Tested earlier and not adopted** (from the 10 November draft; not to be tried again without new measurements): one reader for a whole scheme file; clearing year-check flags that are only printed constants.

## §4 · The report (CLAUDE.md §11), one line more
The repositories the next step needs, in plain words, when they differ from this session's.
