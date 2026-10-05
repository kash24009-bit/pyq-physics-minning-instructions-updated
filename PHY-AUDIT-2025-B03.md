# Audit of the Claude Code work on 2025 · Batch 3 · 2026-10-05

*Every number below was computed from the vault PHY-VAULT-B03-20261005-1539-11354r.json, its gate log and its double-check files (branch claude/pyq-physics-batch-3-964jya). This audit only read the vault; it changed nothing.*

## Verdict
The work is complete and clean. Every 2025 paper (23: 19 main including 55(B), and 4 compartment including 55(B)/S), every 2025 scheme, and the 2026-27 sample paper with its scheme are in the vault. All 16 vault checks pass, no paper is quarantined, and the single-reading papers are the most detailed in the vault. Three things matter for what comes next:
- the double-read caught real slips in 2025, so the year check is needed;
- one planner bug (now fixed) left a wrong progress line;
- one syllabus question must be settled before any mock.

## Size
- Vault: 11,354 rows.
- 2025: 1,642 question rows, of which 868 are unique and 774 are shuffles; 224 unique numericals; 1,641 scoring lines.
- Unique 2025 question types: MCQ 262, NUM 224, CON 95, DRV 88, DEF 68, AR 36, PRD 30, CMP 20.
- 2026-27 sample paper: 71 rows and 115 scoring lines.

## The papers
| paper | code | exam | rows | new | shuffles | figures | formulae (paper) | scoring lines |
|---|---|---|---|---|---|---|---|---|
| 2025-5511 | 55/1/1 | MAIN | 71 | 71 | 0 | 16 | 65 | 140 |
| 2025-5512 | 55/1/2 | MAIN | 72 | 16 | 56 | 15 | 71 | 34 |
| 2025-5513 | 55/1/3 | MAIN | 71 | 15 | 56 | 18 | 69 | 33 |
| 2025-5521 | 55/2/1 | MAIN | 80 | 80 | 0 | 24 | 71 | 128 |
| 2025-5522 | 55/2/2 | MAIN | 78 | 18 | 60 | 18 | 80 | 30 |
| 2025-5523 | 55/2/3 | MAIN | 78 | 18 | 60 | 21 | 76 | 31 |
| 2025-5541 | 55/4/1 | MAIN | 71 | 71 | 0 | 18 | 71 | 149 |
| 2025-5542 | 55/4/2 | MAIN | 72 | 17 | 55 | 16 | 75 | 32 |
| 2025-5543 | 55/4/3 | MAIN | 72 | 17 | 55 | 15 | 76 | 35 |
| 2025-5551 | 55/5/1 | MAIN | 64 | 64 | 0 | 15 | 65 | 143 |
| 2025-5552 | 55/5/2 | MAIN | 65 | 14 | 51 | 16 | 67 | 31 |
| 2025-5553 | 55/5/3 | MAIN | 67 | 16 | 51 | 17 | 65 | 31 |
| 2025-5561 | 55/6/1 | MAIN | 68 | 68 | 0 | 15 | 88 | 139 |
| 2025-5562 | 55/6/2 | MAIN | 66 | 12 | 54 | 12 | 84 | 33 |
| 2025-5563 | 55/6/3 | MAIN | 70 | 16 | 54 | 12 | 85 | 33 |
| 2025-5571 | 55/7/1 | MAIN | 71 | 71 | 0 | 8 | 80 | 131 |
| 2025-5572 | 55/7/2 | MAIN | 72 | 17 | 55 | 7 | 90 | 37 |
| 2025-5573 | 55/7/3 | MAIN | 73 | 18 | 55 | 9 | 88 | 33 |
| 2025-55B | 55/B | MAIN | 73 | 73 | 0 | 0 | 77 | 137 |
| 2025C-55BS | 55/B/S | COMPT | 71 | 71 | 0 | 0 | 52 | 140 |
| 2025C-55S1 | 55/S/1 | COMPT | 73 | 73 | 0 | 13 | 62 | 141 |
| 2025C-55S2 | 55/S/2 | COMPT | 73 | 17 | 56 | 13 | 66 | 0 |
| 2025C-55S3 | 55/S/3 | COMPT | 71 | 15 | 56 | 12 | 65 | 0 |

Every paper has its blueprint row and its two case rows; none has an unreadable row. There was no 55/3 series in 2025 (her statement, CONVENTIONS). The two compartment papers with no scoring lines are the only 2025 papers without a scheme: the compartment scheme covers set 1 only.

## Checks
1. **Vault checks:** 16/16 pass.
2. **Coverage:** no gaps. Every figure question has its figure row, and every numerical and derivation its formula row. No blank relations, and no options on non-choice rows.
3. **Scoring lines:**
   - all 1,756 lines of 2025 and the 2026-27 sample paper are printed lines;
   - every part's lines add up to its printed marks, and every multiple-choice row has its key line;
   - 53 lines carry a "(sic; …)" correction of a scheme error, and 183 lines record accepted alternative answers.
4. **Shuffles:** the year check's script compares each one with its origin. It found one suspect: 2025-5553-Q29-ii is stored as a shuffle of 2025-5551-Q29-iii, but its stem and givens differ. This is linked to Q-048, the 55/5/3 scheme's "award 1 mark to all students".
5. **Detail** (new rows):

| | figure description | formula rows per numerical | rows with a note | rows with givens |
|---|---|---|---|---|
| 2025, one thorough reading | 461 characters | 1.55 | 99 % | 77 % |
| 2025, double-read | 402 characters | 1.39 | 82 % | 73 % |
| 2026 trial | 201 characters | 1.00 | 61 % | 74 % |

## The double-read, while it ran
| unit | values compared | mismatches | real errors fixed |
|---|---|---|---|
| sample paper 2026-27, paper | 305 | 37 | 0 |
| sample paper 2026-27, scheme | 168 | 12 | 0 |
| 55/1/1 | 338 | 29 | 2 |
| 55/2/1 | 317 | 55 | 0 |
| 55/4/1 | 306 | 18 | 0 |
| 55/5/1 | 311 | 10 | 1 |
| 55/6/1 | 303 | 18 | 0 |
| 55/7/1 | 316 | 16 | 0 |
| 55/S/1 | 324 | 11 | 1 |
| 55/1/2 | 365 | 56 | 0 |

Most mismatches were notation, settled in the vault's favour. But unlike 2026, the double-read caught 4 real reading slips in these 10 units. From 2025-5513 on, 36 saves were made after one thorough reading, by her decision of 3 October. At the same rate, a few slips are likely among them. That is what the 2025 year check (PHY-08 Y§11) is for, and its escalation re-reads a whole paper whenever its sample finds one.

## Pace
58 saves between 2 October 08:54 and 5 October 15:39 UTC: about 9 hours of work and 70 hours of usage pauses. One-reading sibling papers took 13 to 27 minutes each. The plan's usage limit set the calendar, not the work.

## Corrections made in Batch 3
150 FILES corrections: identities from page-1 images, combined-scheme coverage, and statuses. No question row needed a correction after it was saved.

## Open questions raised in Batch 3
- **Must be settled before any mock:** Q-020. The 2026-27 sample paper asks Gauss's law for magnetism (SQP2627-042-Q20B), but the syllabus file lists that topic as possibly deleted (VERIFY-DEL). Mocks never use such a topic, so this decides whether it can appear in your mocks.
- **Scheme against paper or physics:**
  - Q-021: sample paper 2026-27, Q21 and Q25 marks.
  - Q-048: 55/5/3, Q29(ii), award to all.
  - Q-049: 55/5/1 Q21, box against lines.
  - Q-053: 55/6/2 Q20, one working for two parts.
  - Q-057: 55/7/3 Q23, box against lines.
  - Q-063: 55/S/1 keys Q11 as "attract" for two parallel proton beams moving the same way. For speeds far below light's, the electric repulsion wins, so the beams repel.
  - Q-064: 55/S/1 Q25(a), box against lines.
  - Q-016 from Batch 2 is still open.
- **Files:** Q-062. The 2024-25 sample paper is recorded but not in any repository (its scheme arrived). It waits for the end phase (CI§4).
- **Tools:** Q-022, the year planner filing 55/S as visually-impaired and ignoring three-set scheme files. Fixed in gate edition 2026-10-05, and checked against 2025's real files.
- **Method:** Q-017 (her work order against CI§5) and Q-018 (classification granularity) wait for the closing sweep.
- **Resolved in Batch 3:** Q-019 and Q-037.

## Lessons recorded
Batch 3 wrote its own lessons into the ledger addendum (B3-1 to B3-8), including the planner bug. The next session adds the 2025 year check's findings there.

## Left for later
- **Next session:** the 2025 year check, and a corrected 2025 "papers with no scheme" line (only 2025C-55S2 and 2025C-55S3).
- **Closing sweep:** transferred or inferred scoring lines for those two papers, and classification, workbooks and the year-close of 2025.

## What changed in the instructions (2026-10-05)
- **CLAUDE.md, PHY-07, PHY-08:** one thorough reading per paper, saved with `--single-read`; the year check; Batch 3's scheme conventions; tight-crop rules.
- **Gate (edition 2026-10-05):** `--single-read`, `yearcheck`, `--open-line`, and the fixed planner.
- **Setup (edition 2026-10-02b):** unchanged.
