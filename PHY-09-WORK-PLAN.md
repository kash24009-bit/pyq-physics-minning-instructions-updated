# PHY-09 · Work plan from 2026-11-10 (her decisions of 2026-11-10)
Pack order: S5:2023 > S6 > YC:2023 > S1:2022

`phy_boot.py` prints this file at every boot and takes the step to start from the line above (the first step that still has work). This file sets the order of work, carries the rules of the Fable week and lists the upgrades of 2026-11-10. It changes nothing in the truth rules (CLAUDE.md §4), the gate, the rule card, one paper at a time, or one fresh reader per unit.

## 1 · Order of work
It replaces the order of CONVENTIONS "Order change (her decision 2026-10-26)" from the 2023 schemes on.
1. **The 2023 marking schemes.** The twenty open `Y2023 S5` lines in PROGRESS order, exactly as R§10, Y§5 and card C say: one unit per set section, one fresh `phy-reader` each, pages as in CONVENTIONS "Y2023 schemes". Needs the schemes repository PHY-PHYSICS-2023-MS.
2. **Pattern-sorting (S6) for 2026, 2025, 2024 and 2023**, moved forward from the closing sweep (it needs no page image, and it is the judgement work the Fable week is best spent on). R§12 and Y§12 step 3 as written, with these additions:
   1. Granularity first (Q-018: 42 codes for 181 rows in chapters 01 and 02). Write the granularity test with two or three examples from those rows into CONVENTIONS as "Granularity test (2026-11-10)" and into every S6 reader's brief; re-classify chapters 01 and 02 under it. REGISTRY wins, a merge is an ALIAS, no code is renumbered or reused (CI§2.9).
   2. Then chapter by chapter over the origin rows of the four years together: the cross-year grouping script first, the per-year prediction written before classifying, the misses per year after. One fresh reader per chapter, text only.
   3. A year's `S6 classify` line is ticked through the gate only when a script shows every origin row of that year has a CLASSIFY row with a VERIFIED code. 2022's rows are classified in the closing sweep, after 2022 is mined. S7, S8 and the no-scheme S5 lines stay in the closing sweep.
   Needs no papers or schemes repository.
3. **The 2023 year check** (Y§11). Needs PHY-PHYSICS-2023, PHY-PHYSICS-2023-2 and PHY-PHYSICS-2023-MS.
4. **2022** (Term 2, then Term 1; Y§2 onwards), with the intake rule of §3. Needs the 2022 papers and schemes repositories.
The 2025 session of the 2026-10-26 entry (the three 2024 page checks, the 2024-25 sample paper, the 2025 year check) keeps its place: whenever she starts a session with the 2025 repositories attached, do it first.
If her message names a step ("2022 instead", "year check now"), that step comes first: run `phy_boot.py --stage <stage> --year <year>` for it.
A step whose repositories are not attached is skipped with one line in the report; go on to the next step that can run.

## 2 · The Fable week (until 2026-11-17 07:59 UTC, which is Tuesday 17 November, 1:29 pm IST; after that this section no longer applies)
- Her Pro plan includes the Fable models until then, up to half of her weekly limit, plus one Fable limit reset that only she can press (Settings > Usage). Fable usage uses her limits faster than other models. What other models use is not given back by the reset, and it is the usage her lessons run on.
- So this week the mining runs on Fable 5.2, the main session and the readers alike (readers inherit: pass no model or effort in an Agent call, as always).
- **The guard.** Before every Agent call, check the model you are running on (the system tells you when it changes). If it is not Fable 5.2, stop at this unit boundary: close-out, checkpoint, report, and end the RESUME line with `next: Fable allowance used; she presses Reset for free once, then a new session`. Do not go on with another model, unless her message says "any model".
- Nothing else changes for Fable: the same rule card, the same band sizes, the same calibration on every new file, the same gate.

## 3 · Upgrades of 2026-11-10
- **The stage boot pack** (CLAUDE.md §6): `python3 /mnt/project/phy_boot.py`.
- **The close-out** (CLAUDE.md §9): `python3 /mnt/project/phy_closeout.py`, then a gate checkpoint, at the end of every session. It keeps `outputs/reports/PHY-USAGE-LEDGER.md` and `outputs/LESSONS.md`.
- **A year's intake, from 2022:** in the S1 brief, the reader opens only the top band of each identity page; a bottom band only when the series word, the set, the code, the subject line or a scheme's header is not on the top band (Y§8).
- **Tested and not adopted** (do not try them again without new measurements):
  - One reader for a whole scheme file. It would save two reader start-ups and two main-session rounds per series, but every later step would re-read the first set's page images, and three sets' answers would sit in one reader's view (W-1). The stage boot pack removes more of the same cost without that.
  - Clearing year-check flags that are only the paper's printed constants. On the 2024 year check's own files it would have taken 3 of 262 rows off the re-reading list, each on the single digit 4.
- **First session after this file arrives:** add one CONVENTIONS entry, "Upgrades 2026-11-10 (her decision)", of at most eight lines (this file's order of work and upgrades, by name), with `python3 /home/claude/phy_gate.py checkpoint --message "work plan 2026-11-10"`. Then start step 1.

## 4 · The report (CLAUDE.md §11), two lines more
- The repositories the next step needs, in plain words, when they differ from this session's.
- When the guard stopped the session: that she presses Reset for free once (Settings > Usage) before the next session, and by Sunday 15 November at the latest.
