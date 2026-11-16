# PHY-10 · Pattern sorting (S6 classification) · written 2026-11-16

*How every Physics (042) row gets its pattern code, for all six exam years at once. It carries out CI§5 S6, P§10, PHY-07 R§12 and PHY-08 Y§12 step 3 and changes none of the truth rules (CLAUDE.md §4). Where it differs from them it says so (§9 and §3.4); her approval of this file is that decision, recorded in CONVENTIONS "Pattern sorting (her decision 2026-11-16)" by the first session that uses it. Tool: `phy_s6.py`, edition 2026-11-16b, tested in the project chat on copies of vaults B10 and B11, including the gate's own `check` on its part files (CHECK PASS, validate 16/16). Edition b (after Batch 11) adds save-as-you-go: §6 step 4, §7 steps 2-4.*

## §1 · What it produces and why it matters
- Every row gets one code from REGISTRY: the **pattern** (archetype) a student must master to score it. Codes, their plain names, their "asks you to" lines, their scoring skeletons and their traps are what the registers, chapter cards, statistics, predictions and mocks are built from. Without this step the vault is a ledger; with it, it is a map of what CBSE asks.
- **Families** group the codes of one skill across formats, so a skill asked once as a numerical and twice as an MCQ shows as one family with three appearances (§3.4).

## §2 · Scope, computed 2026-11-16 on vault B10
- 6,829 rows need a code (the Definition of Done counts every row except visually-impaired alternatives).
- 3,787 are new (origin) rows. 139 of them repeat another row word for word or nearly (120 groups, 21 across years); a group is decided once, by its leader, so **3,648 rows are decided by a reader**.
- 3,042 shuffle rows copy their origin's decision by script; no reader looks at them.
- 236 rows were sorted earlier (Batch 0: 71 sample-paper rows; Batch 2: chapters 01 and 02 of 2026). They come back on the sheets with "now <code>" and are re-tested under §3; a changed decision becomes an ERRATA row written by the tool.
- Per chapter, reader decisions: 01 191 · 02 256 · 03 323 · 04 361 · 05 63 · 06 184 · 07 254 · 08 197 · 09 492 (two parts) · 10 318 · 11 305 · 12 226 · 13 159 · 14 319. Run `phy_s6.py status` for the live numbers.

## §3 · What one pattern is
### 3.1 The test (P§10.2, unchanged)
> Two rows share a code **iff** a student who has mastered the scoring skeleton of one would score full marks on the other with no new idea — only different numbers, wording or context.

### 3.2 Applying it: same code when all of these hold
1. Same chapter and the same q_type group (written answer, MCQ, or assertion-reason; §3.4).
2. The same governing law or relation, used in the same chain, for the same kind of unknown.
3. The scheme's lines would be the same lines with the same marks, up to numbers and wording (`phy_s6.py lines <id>` shows them).
4. Nothing extra carries a mark: no added sub-result, graph, diagram, sign argument or limiting case that the other row does not ask for.

### 3.3 Different code when any of these holds
- A different law or a new formula is needed (an isolated sphere's capacitance in a medium, C = 4πε0KR, is not the parallel-plate dielectric pattern).
- A derivation and its use: "derive C with a dielectric" and "find C with two slabs side by side" are two codes.
- A graph or diagram that the scheme marks on its own, against a numerical of the same law.
- The same topic but a different unknown that changes the chain (fringe width against the position where two wavelengths' bright fringes first coincide).
- A case sub-part is coded by its own demand, never by the passage's topic.

### 3.4 Formats and families
- MCQ and assertion-reason rows keep their own codes, named by the concept tested plus "(MCQ)" or "(A-R)" (P§10.3 rule 5), because they carry no skeleton.
- **Families are skill groups** (tighter than before, her decision through this file): one family holds the written code and the MCQ or A-R codes of the same skill. Example from the pilot: work and energy of a dipole in a uniform field, PH-02-031 (MCQ), PH-02-032 (NUM), PH-02-035 (MCQ). A family is named "FAM-cc-nn <skill in plain words>". Moving a code into a better family is a REGISTRY edit (Layer 1.5), never a new code.

### 3.5 Calibration examples from the vault
| Rows | Decision | Why |
|---|---|---|
| 2026-5521-Q21B (500 and 600 nm, 2 marks) and T2-2022-5533-Q06-ii (600 and 500 nm, 3 marks) | same code | same chain: positions of bright fringes of each wavelength, least common position; the extra mark of 2022 is the same lines split finer |
| 2025-5551-Q25-d2, 2024-5551-Q27-b, 2023-5551-Q32B-d2 (full-wave rectifier with circuit diagram) | same code | same skeleton: diagram, working for both halves, output waveform |
| 2026-5511-Q01 (V = 10 − 50x, find E) and 2026-5512-Q01 (E = 4x î, find V_A − V_B) | two codes, one family | E = −dV/dx against V = −∫E dx: the second needs integration, a new idea; same skill family |
| PH-02-013 (predict how C, Q, V, U change when a slab or the gap changes; 12 uses) and PH-02-016 (an isolated sphere's capacitance in another medium) | two codes | the second needs C = 4πε0KR |
| PH-02-010 (derive C with a dielectric) and PH-02-038 (C with two slabs side by side) | two codes | derivation against application |

### 3.6 Granularity check (Q-018)
No quota. After all chapters, `phy_s6.py review` lists codes used once and look-alike codes (same q_type, names sharing half their words). A code used once stays when no other code passes §3.1; look-alikes that pass are merged (`phy_s6.py alias`, status ALIAS, the newer into the older, every row re-pointed by ERRATA); a code that holds two patterns is split (new codes, the rows re-decided with `expand --any`, the old code SPLIT with a note).

## §4 · The judged fields of every decision
| Field | Values | Meaning |
|---|---|---|
| cog_level | REM, UND, APP, ANL | REM: recall a statement, definition or fact. UND: explain, compare, describe why. APP: use a relation in a stated situation (most numericals, standard derivations). ANL: analyse a graph or data, reason through an unfamiliar or multi-step situation, evaluate, design. The syllabus target is 27/22/21 marks (P§10.1). |
| competency | y, n | y when the row applies a concept to an unfamiliar or real situation, interprets data or a graph, or is case- or assertion-based. |
| difficulty | E, M, H | E: one step or recall. M: two or three standard steps. H: several ideas together, an unfamiliar set-up, or a long derivation. |
| confidence | H, M, L | the reader's confidence in the code. L rows are listed in the unit's return. |
ncert_ref stays blank (end phase). family, batch and rule_version are filled by the tool.

## §5 · REGISTRY entries
- **code:** `PH-<chapter>-<serial>`. A DRAFT seed that a row matches is promoted and keeps its number. A new code takes the next free serial of its chapter; a number is never reused, not even an ALIAS's or SPLIT's.
- **name:** a plain verb phrase of 12 words or fewer, no symbols (CI§10); MCQ and A-R codes end "(MCQ)" or "(A-R)".
- **asks_you_to:** one sentence of 30 words or fewer, starting "Asks you to", in the chapter's own words.
- **skeleton:** the lines that score and their marks, from the printed lines of one or two of its rows (`phy_s6.py lines <id>`), written without the numbers: "relation E = −dV/dx (1/2); magnitude with unit (1/2)". A code whose rows have no printed lines anywhere (only the compartment papers without a scheme) writes "INFERRED (no printed scheme): …".
- **traps:** what loses marks, each with year and paper, from the printed lines (a unit half, a sign, a direction), the "(sic)" notes and the accepted alternatives. When nothing in the schemes shows one: "No trap printed in the 2022-2026 schemes". Never invented.
- **family, topic_id, q_type, status VERIFIED, first_instance** (the row that verified it), **issued_batch** (`B<nn>` for a new code; unchanged for a seed or an earlier code), **note** ("issued at S6 from <row>" or "seed promoted at S6 from <row>").
- Seeds never matched stay DRAFT and never enter statistics (CI§2.8).

## §6 · The unit: one chapter (two for chapter 09), one fresh reader, text only
**Main session, once before the first unit:** `python3 /mnt/project/phy_s6.py groups` (S6-GROUPS.csv, the repeat groups).
**Then per unit, two main-session steps, as in mining:**
1. Bash: `python3 /mnt/project/phy_s6.py sheet --chapter <cc>` (chained after the previous unit's commit, because candidates use the codes committed so far; chapter 09 gives S6-CH09-1 and S6-CH09-2: make the second sheet only after the first is committed).
2. Agent: a fresh `phy-reader` with this brief: *"S6 unit <unit>. Read /mnt/project/PHY-10-PATTERN-SORTING.md §3 to §8 and /home/claude/vault/work/<unit>__SHEET.md. Follow §7. Return at most 12 lines."* Pass no model or effort.
3. Bash: `python3 /home/claude/phy_gate.py commit <unit> --stage OTHER --no-progress && python3 /mnt/project/phy_s6.py coverage && python3 /mnt/project/phy_s6.py sheet --chapter <next>`.
4. **A stop with a unit in flight** (`Stop.`, a usage stop, a reader that fails): save what it decided, never throw it away: `python3 /mnt/project/phy_s6.py expand --unit <unit> --partial && python3 /mnt/project/phy_s6.py check --unit <unit> && python3 /home/claude/phy_gate.py commit <unit> --stage OTHER --no-progress`. With a codebook applied but no decision yet: `python3 /home/claude/phy_gate.py checkpoint --message "S6 <unit> codebook"`. The next session resumes that chapter with `python3 /mnt/project/phy_s6.py sheet --chapter <cc> --remaining` (unit `S6-CH<cc>-r<HHMM>`: only the rows not yet decided, and pilot rows not yet re-tested).

Order: 02, 01 (the pilot chapters first: their existing codes calibrate the test), then 03 to 14. After every unit, `phy_measure.py` records the weighted usage (PHY-08 Y§1).

## §7 · Inside the unit (the reader)
1. Read the whole sheet once: the chapter's registry, then every row with its candidates, lines and repeats.
2. **Codebook first, on disk by your sixth step.** Decide the chapter's patterns: which existing codes and seeds are used, which new codes are needed, which families. Write every new or changed REGISTRY row to `work/<unit>__REGISTRY.csv` (the exact REGISTRY header; full rows). For skeletons and traps, `python3 /mnt/project/phy_s6.py lines <id> …` on one or two rows of each code. A code found missing later is added to the same file and applied again (re-running is safe).
3. `python3 /mnt/project/phy_s6.py registry --unit <unit>` until it applies (it refuses bad names, numbering, a reused number or a missing field).
4. **Decisions, saved topic by topic.** `work/<unit>__DECISIONS.csv` with header `instance_id,code,cog_level,competency,difficulty,confidence`, one row per id on `work/<unit>__TODO.csv`, in sheet order. After each topic's rows, append them to the file at once: the file grows as you go, and no more than one topic's decisions is ever held only in your head. Visually-impaired alternatives at the end of the sheet are optional: decide one only when an existing code fits cleanly.
5. `python3 /mnt/project/phy_s6.py expand --unit <unit>` (repeats and shuffles follow their leader; earlier decisions that changed become ERRATA rows), then `python3 /mnt/project/phy_s6.py check --unit <unit>` and `python3 /home/claude/phy_gate.py check <unit> --stage OTHER`, until both print CHECK PASS.
6. Return, at most 12 lines: rows decided; codes reused, seeds promoted, new codes, changed earlier decisions; every L-confidence row; any row whose chapter or q_type looks wrong (queued, never changed here).

## §8 · Never
- Never open an image or a PDF: the sheet, `lines` and the vault's FIGURES and CASES text are the whole input.
- Never write `l1/` or `j/CLASSIFY.csv` by hand; never edit a row's chapter, topic or q_type here (a wrong one is queued for a FIX unit).
- Never assign a DRAFT, ALIAS or SPLIT code; never reuse a number; never invent a skeleton line or a trap.
- Never decide a row from memory of another chapter or from chat history.
- Never hold a chapter's decisions in your head to write at the end: what is not on disk is lost at a stop (§6 step 4 saves only what is written).
- If the registry itself is damaged half way (a crash during `registry`), `work/<unit>__REGISTRY-BEFORE.csv` holds it as it was: copy it back over `vault/j/REGISTRY.csv` before the unit is redone.

## §9 · After the last chapter
1. **Review unit S6-REVIEW** (one reader): `phy_s6.py review`; merges with `phy_s6.py alias --unit S6-REVIEW --from X --to Y --reason "<why §3.1 passes>"`; splits with new REGISTRY rows and `expand --unit S6-REVIEW --any`; then `check` and the gate commit.
2. **Prediction and misses, per year** (CI§5 S6): `phy_s6.py misses --write-notes` writes, for each year, the codes predicted from the other years (asked in the main papers of at least two other years), the predicted codes that were absent, and the codes never seen in another year. *This replaces "predict before classifying": with all years sorted together a prediction written first could use only the 2026 pilot codes, so the leave-one-year-out prediction is the honest form (her decision through this file).* Uncalibrated; no probability is shown (CI§12).
3. **Tick each year's S6 line** when `phy_s6.py coverage` shows 0 to go for it: `python3 /home/claude/phy_gate.py checkpoint --message "S6 classify <year>" --tick "Y<year> S6 classify"`.
4. Then S7 for every year (PHY-07 R§12) and the transferred scoring lines of the papers without a scheme (PHY-09 §2 step 4).

## §10 · Budget
The fifteen sheets total about 1.4 MB of text, about 350,000 tokens (chapter 05 about 6,000; chapter 04, the largest single sheet, about 36,000; each half of chapter 09 about 25,000), measured on vault B10. A reader reads its sheet once and writes short rows, so the cost is mostly its judgement, not reading. **Measured in Batch 11:** the chapter 02 reader, stopped after 21 steps, had used 610,265 weighted tokens, 91 % of its output thinking, and had written nothing, so its work was lost; save-as-you-go (§6 step 4, §7) exists because of it. The estimate is three to four sessions for the fifteen units and the review, possibly more; each unit's weighted usage is measured, and the first complete unit sets the real figure for the rest (said once in the report).
