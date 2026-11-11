# Claude Code trial · Batch 2

## What ran
- Session: setup finished 2026-10-01T08:00:27Z (phy_env.json); this report written 2026-10-01T09:41:06Z; the trial-report checkpoint follows it. Session batch B02; restored vault batch 1 with 744 question rows; kit edition 2026-09-30b.
- Papers attempted 2, finished 2: 2026-5532, 2026-5533 (S4 siblings of series 55/3, origin 2026-5531), each through extractor, seal, blind checker, settle and gate commit.
- S1b: inventory added 19 FILES rows; 17 originals matched to their bundle twins (16 2026 schemes and the syllabus), each confirmed on its page images: ER-B02-001..ER-B02-071. Not twins, logged by normal intake: Physics-MS.pdf = SQP-MS SQP2526-042 (ER-B02-072..ER-B02-076); Physics-SQP (1).pdf = SQP SQP2425-042 (ER-B02-077..ER-B02-078). Unit S1B committed at 2026-10-01T08:12:36Z.

## Papers
| paper | rows (shuffle + new) | figures | formulae | check-paper | values double-read | mismatches | extractor wrong (part_fixed) | checker wrong (extractor_right) | unreadable | minutes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-5532 | 73 (57 + 16) | 16 | 41 | PASS · 2026-5532 · 33/33 questions · total 70/70 | 366 | 16 | 0 | 16 | 0 | 46 |
| 2026-5533 | 73 (58 + 15) | 13 | 40 | PASS · 2026-5533 · 33/33 questions · total 70/70 | 381 | 15 | 0 | 15 | 0 | 39 |

Minutes run from opening the paper (`date -u`) to its gate commit. Every `extractor_right` decision in this trial was a difference of notation, wording or convention, or of the row a shared value is filed on: no reading disagreed on a value.

## Every mismatch
Extractor and checker values as the gate compared them (numbers as canonical sets). Every crop was read at 400 dpi; the crops lived on the session machine and are not kept, while every decision and its note are kept in `outputs/logs/doublecheck/B02/` and the gate log.

| paper | row | field | extractor | checker | decision | crop |
|---|---|---|---|---|---|---|
| 2026-5532 | 2026-5532-Q01 | options | A) 2*n*pi \| B) 2*n*pi + pi/4 \| C) 2*n*pi + pi/2 \| D) 2*n*pi + pi | A) 2nπ \| B) 2nπ + π/4 \| C) 2nπ + π/2 \| D) 2nπ + π | extractor_right | `/home/claude/render/2026-5532/adj-1/p5.png` |
| 2026-5532 | 2026-5532-Q08 | options | A) +5 V (left), +10 V (right) \| B) -1.0 V (left), -1.5 V (right) \| C) 0 V (left), 1 V (right) \| D) -2 V (left), 0 V (right) | A) anode +5 V, cathode +10 V \| B) anode -1.0 V, cathode -1.5 V \| C) anode 0 V, cathode 1 V \| D) anode -2 V, cathode 0 V | extractor_right | `/home/claude/render/2026-5532/adj-2/p7.png` |
| 2026-5532 | 2026-5532-Q09 | options | A) 200 ohm \| B) 175 ohm \| C) 100 ohm \| D) 125 ohm | A) 200 Ω \| B) 175 Ω \| C) 100 Ω \| D) 125 Ω | extractor_right | `/home/claude/render/2026-5532/adj-3/p7.png` |
| 2026-5532 | 2026-5532-Q10 | options | A) 2.0e8 m s^-1 \| B) 4.5e7 m s^-1 \| C) 3.5e7 m s^-1 \| D) 2.5e8 m s^-1 | A) 2.0 × 10^8 ms^-1 \| B) 4.5 × 10^7 ms^-1 \| C) 3.5 × 10^7 ms^-1 \| D) 2.5 × 10^8 ms^-1 | extractor_right | `/home/claude/render/2026-5532/adj-4/p9.png` |
| 2026-5532 | 2026-5532-Q12 | options | A) R/(mu - 1) \| B) -R/(mu - 1) \| C) 2R/(mu - 1) \| D) -2R/(mu - 1) | A) R/(μ - 1) \| B) -R/(μ - 1) \| C) 2R/(μ - 1) \| D) -2R/(μ - 1) | extractor_right | `/home/claude/render/2026-5532/adj-5/p9.png` |
| 2026-5532 | 2026-5532-Q19A | marks_part | - | 2 | extractor_right | `/home/claude/render/2026-5532/adj-6/p13.png` |
| 2026-5532 | 2026-5532-Q24B-i | numbers | 0.5 3.2e-19 6.4e-27 8 | - | extractor_right | `/home/claude/render/2026-5532/adj-7/p15.png` |
| 2026-5532 | 2026-5532-Q24B-ii | numbers | 0.5 3.2e-19 6.4e-27 8 | - | extractor_right | `/home/claude/render/2026-5532/adj-8/p15.png` |
| 2026-5532 | 2026-5532-Q29-ii | options | A) 1/sqrt(2) \| B) sqrt(2) \| C) 1/2 \| D) 2 | A) 1/√2 \| B) √2 \| C) 1/2 \| D) 2 | extractor_right | `/home/claude/render/2026-5532/adj-9/p17.png` |
| 2026-5532 | 2026-5532-Q29B-iv | options | A) p_1 = p_2/2 \| B) p_1 = p_2 \| C) p_1 = 2*p_2 \| D) p_1 = 4*p_2 | A) p_1 = p_2/2 \| B) p_1 = p_2 \| C) p_1 = 2p_2 \| D) p_1 = 4p_2 | extractor_right | `/home/claude/render/2026-5532/adj-10/p19.png` |
| 2026-5532 | 2026-5532-Q30-i | options | A) 6 microF \| B) 3 microF \| C) 9 microF \| D) 2 microF | A) 6 μF \| B) 3 μF \| C) 9 μF \| D) 2 μF | extractor_right | `/home/claude/render/2026-5532/adj-11/p21.png` |
| 2026-5532 | 2026-5532-Q30A-iv | options | A) 6 microC \| B) 4 microC \| C) 12 microC \| D) 8 microC | A) 6 μC \| B) 4 μC \| C) 12 μC \| D) 8 μC | extractor_right | `/home/claude/render/2026-5532/adj-12/p21.png` |
| 2026-5532 | 2026-5532-Q33A-ii | numbers | -2 -30 0 2 30 5 900000 | -2 -30 0 30 5 900000 | extractor_right | `/home/claude/render/2026-5532/adj-13/p27.png` |
| 2026-5532 | 2026-5532-Q33B-ii-I-1 | numbers | -3 1 2 | -3 2 | extractor_right | `/home/claude/render/2026-5532/adj-14/p27.png` |
| 2026-5532 | 2026-5532-Q33B-ii-II-1 | numbers | -3 1 2 | -3 2 | extractor_right | `/home/claude/render/2026-5532/adj-15/p27.png` |
| 2026-5532 | 2026-5532-Q33B-ii-III-1 | numbers | -3 1 2 | -3 2 | extractor_right | `/home/claude/render/2026-5532/adj-16/p27.png` |
| 2026-5533 | 2026-5533-Q04 | options | A) sqrt(29)*B_0*L^2 \| B) 4*B_0*L^2 \| C) 3*B_0*L^2 \| D) 2*B_0*L^2 | A) sqrt(29) B_0 L^2 \| B) 4 B_0 L^2 \| C) 3 B_0 L^2 \| D) 2 B_0 L^2 | extractor_right | `/home/claude/render/2026-5533/adj-1/p5.png` |
| 2026-5533 | 2026-5533-Q12 | options | A) 2*n*pi \| B) 2*n*pi + pi/4 \| C) 2*n*pi + pi/2 \| D) 2*n*pi + pi | A) 2n pi \| B) 2n pi + pi/4 \| C) 2n pi + pi/2 \| D) 2n pi + pi | extractor_right | `/home/claude/render/2026-5533/adj-2/p9.png` |
| 2026-5533 | 2026-5533-Q26A-d2 | numbers | - | 1 30 6 8 | extractor_right | `/home/claude/render/2026-5533/adj-3/p15.png` |
| 2026-5533 | 2026-5533-Q29-i | options | A) 6 microF \| B) 3 microF \| C) 9 microF \| D) 2 microF | A) 6 muF \| B) 3 muF \| C) 9 muF \| D) 2 muF | extractor_right | `/home/claude/render/2026-5533/adj-4/p17.png` |
| 2026-5533 | 2026-5533-Q29-ii | numbers | 10 3 5 | 10 3 6 | extractor_right | `/home/claude/render/2026-5533/adj-5/p17.png` |
| 2026-5533 | 2026-5533-Q29-iii | numbers | - | 3 6 | extractor_right | `/home/claude/render/2026-5533/adj-6/p19.png` |
| 2026-5533 | 2026-5533-Q29A-iv | numbers | 6 | 3 6 | extractor_right | `/home/claude/render/2026-5533/adj-7/p19.png` |
| 2026-5533 | 2026-5533-Q29A-iv | options | A) 6 microC \| B) 4 microC \| C) 12 microC \| D) 8 microC | A) 6 muC \| B) 4 muC \| C) 12 muC \| D) 8 muC | extractor_right | `/home/claude/render/2026-5533/adj-8/p19.png` |
| 2026-5533 | 2026-5533-Q29B-iv | numbers | - | 3 6 | extractor_right | `/home/claude/render/2026-5533/adj-9/p19.png` |
| 2026-5533 | 2026-5533-Q30-ii | numbers | - | 1 2 | extractor_right | `/home/claude/render/2026-5533/adj-10/p21.png` |
| 2026-5533 | 2026-5533-Q30B-iv | options | A) p_1 = p_2/2 \| B) p_1 = p_2 \| C) p_1 = 2*p_2 \| D) p_1 = 4*p_2 | A) p_1 = p_2/2 \| B) p_1 = p_2 \| C) p_1 = 2p_2 \| D) p_1 = 4p_2 | extractor_right | `/home/claude/render/2026-5533/adj-11/p21.png` |
| 2026-5533 | 2026-5533-Q32A-ii | numbers | -2 -30 0 2 30 5 900000 | -2 -30 0 30 5 900000 | extractor_right | `/home/claude/render/2026-5533/adj-12/p25.png` |
| 2026-5533 | 2026-5533-Q32B-ii-I-1 | numbers | -3 1 2 | -3 2 | extractor_right | `/home/claude/render/2026-5533/adj-13/p25.png` |
| 2026-5533 | 2026-5533-Q32B-ii-II-1 | numbers | -3 1 2 | -3 2 | extractor_right | `/home/claude/render/2026-5533/adj-14/p25.png` |
| 2026-5533 | 2026-5533-Q32B-ii-III-1 | numbers | -3 1 2 | -3 2 | extractor_right | `/home/claude/render/2026-5533/adj-15/p25.png` |

## Checks
- S1B: validate after merge 16/16 checks pass (gate log 2026-10-01T08:12:36Z).
- 2026-5532: validate after merge 16/16 checks pass (gate log 2026-10-01T09:00:06Z).
- 2026-5533: validate after merge 16/16 checks pass (gate log 2026-10-01T09:39:02Z).
- Commits on claude/beautiful-pascal-k4durg: 2066ba9 (S1B); f1550a3 (2026-5532); 78878d5 (2026-5533). The trial-report checkpoint adds one more.
- Pushes: local HEAD 78878d5, origin/claude/beautiful-pascal-k4durg 78878d5: in step, every gate commit pushed.
- Draft pull request for the session branch: https://github.com/kash24009-bit/pyq-physics-minning-instructions-updated/pull/1 (merging is optional; the setup finds the newest vault on any branch).

## What went wrong or was slow
- **Setup roles.** The 2026 schemes sit in a repository with neither a vault file nor a ZIP, so the setup gave it no role and linked none of its PDFs; the vault file sits in the instructions repository, which therefore also served as the project repository. The scheme PDFs were linked into /mnt/project by hand before inventory (Q-011, PHY-03 addendum B2-1).
- **Runbook commands.** `pyqkit pages` and `render` resolve a file_id only with `--vault /home/claude/vault`; R§3 and both briefs omit it (Q-011, B2-2). The CLAUDE file is named "CLAUDE (3).md", so Claude Code did not load it by itself (Q-011). Each subagent brief therefore carried a one-line route note on these two points, and nothing about the paper.
- **The double-read spent its crops on notation.** All 31 mismatches were notation (μ, Ω, π, √, implied products, powers of ten), the row a shared lead-in or case-setup value is filed on, a printed space after a minus sign, a printed sub-label read as a number, or the marks of an OR side. Fields: options 14, marks_part 1, numbers 16. None was a value error by either reader.
- **The one real error was outside the double-read's sight.** Batch 1 had misread the polarity of one cell in 55/3/1 Q17(a) (F-2026-5531-02, EQ-2026-5531-003). Every number was right, so neither check-paper nor the numbers-only double-read could see it; the 2026-5532 extractor found it by comparing the sibling figures, and the orchestrator confirmed it by measuring plate lengths on 400 dpi crops of all three sets. The new rows describe the page; the B01 rows wait for a Fix (Q-013, B2-3).
- **New files that were not twins.** Physics-MS.pdf is the marking scheme of SQP 2025-26, which the vault listed as missing (Q-004): its S5 can now be PRINTED (Q-012). Physics-SQP (1).pdf is the 2024-25 sample paper and waits for its year. The syllabus original's p1 image prints only "Class XI-XII (2026-27)"; the "(2025-26)" Batch 0 read there is a hidden text object (CONVENTIONS, Q-002).
- **Slow parts.** The extractor and the blind checker each read every printed part on its own crops, which is most of each paper's minutes; settling took one crop per mismatch.

## Recommendation
Continue on this route. The loop did what it promises: both papers passed check-paper and the double-read at their first commit, every mismatch was settled from a crop, nothing was unreadable, and every gate step was pushed. Change four things before the next session. First, let the setup give a role to a repository that holds only scheme PDFs (or keep the vault file beside the schemes), so the S5 passes can open the scheme originals by file_id without hand-made links. Second, make the kit's default vault /home/claude/vault, or add `--vault` to R§3 and both briefs. Third, tell the blind checker to write numbers and options in P§6.3 ASCII and to file a shared lead-in's or case setup's numbers on the first row that carries them, or let the gate normalise those forms; in this trial that would have removed nearly every mismatch and left the crops for real disagreements. Fourth, add one figure-orientation entry to the checker's reading (polarity of cells and diodes, direction of arrows and fields), because that is the one kind of error a numbers-only double-read cannot catch, and Batch 1 already holds one. Under the name CLAUDE.md the instructions would load by themselves after every compaction; the next session should also run the Q-013 Fix before 2026-55B, whose questions are shuffles of this series.
