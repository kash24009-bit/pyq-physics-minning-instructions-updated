# PHY-03 · MISTAKES LEDGER — Physics (042)
### Every mistake made so far in PYQ mining, why it happened, and the rule in this project that prevents it

**How to use this file (Claude):**
1. Read Part 1 and Part 4 at every boot.
2. Before any year starts, read Part 3 (new-workflow risks).
3. A mistake listed here that happens again is the worst possible outcome of a session.
4. Every new mistake gets an entry here, with its fix, before the session closes (P§21).

`→ CI§n` = Custom Instructions section. `→ P§n` = Protocol section.

---

## PART 1 — The ten root causes

| # | Root cause | What it produced | Cure |
|---|---|---|---|
| R1 | Work held in the chat, not on disk | Chemistry Batch 8: five turns, zero rows saved. Batch 11: zero rows after opening six papers. Batch 7: two lost days | One paper → write → check → save → tick → next. A row not on disk does not exist → CI§6 |
| R2 | Continuity depended on her carrying a file | The Chemistry running ZIP was missing six batches in a row, so no codes, maps or registers existed for 11 batches | The vault restores itself (artifact database + vault file in project knowledge); boot takes the newest verified copy → CI§3 |
| R3 | Claims asserted instead of computed or checked | A fake "duplicate" paper was never extracted (B4); "29 OR" typed when 30 existed (B11); "competency is 50%" stated from a news site | Every number comes from `pyqkit`. Every fact is labelled VERIFIED or REPORTED → CI§2 |
| R4 | Rules invented mid-stream, not back-applied | Batches 1–3 lacked later conventions; Batch 8 broke earlier ones | The schema starts with every convention Chemistry had to discover. A new rule is back-applied the same session → P§21 |
| R5 | Scripts rewritten every batch | Checker bugs in B5, B6 and B10; a broken CSV in B2 | One tested toolkit, never rewritten inside a session → P§4 |
| R6 | File names and labels trusted over content | 80 of 81 Chemistry names had no year; five files shared one code; "Main_paper" was a marking scheme; she typed 2024 for 2023 papers | Kind, code and year are read from the pages, with evidence → P§5 |
| R7 | Instructions that blocked progress or didn't match reality | "Stop if counts mismatch"; "tiers locked until complete"; "papers stay in chat" (they went to project knowledge) | Strict on truth, flexible on process: quarantine a paper, never stop the session → CI§1 |
| R8 | Outputs she couldn't use | A 200-page Maths map; a cluttered top-up list; a thin setup document | One-page briefs, plain three-part status, mocks she can sit → P§17, CI§11 |
| R9 | Work deferred to "later" | Chemistry archetype codes, registers, index and naming were all left for a merge session that never finished | **Year Definition of Done:** a year is closed only when `pyqkit year-close` passes. Nothing is deferred → CI§5, P§11 |
| R10 | Resources available but not used | 28 Sep build: the lesson file in memory unread; the examiner rules in the 2026 scheme unread; CBSE archives unresearched; the installed-skill path guessed | Boot checklist reads every listed resource; the CBSE dossier is a permanent file; skill paths are found by search, not assumed → CI§3, P§22 |

---

## PART 2 — The full log

### A · Maths project
- **MA-1 · Marking schemes never mined,** so the scoring lines (where marks actually live) were missing.
  → The scheme pass is mandatory; STEP-AWARDS is Layer 1 → P§9
- **MA-2 · The output was a 200-page command map she couldn't act on.**
  → One-page chapter briefs + mocks; the command map is capped at 2 pages per chapter → P§17, P§20
- **MA-3 · Extraction scaffolding inside the study project competed with the real material for retrieval.**
  → Ledgers stay here; only briefs, map and mocks move → P§20
- **MA-4 · She reports gaps that were never filled.**
  → Coverage matrix, question-continuity checks, `Audit.`; the same kit will audit Maths later → P§13

### B · Physics, first attempt
- **PV2-1 · Her papers were rejected "on scope".**
  → No-rejection rule; three evidence scopes → CI§1, P§2
- **PV2-2 · 2023 had a different question count and section meanings.**
  → Blueprint read per paper; classes defined → P§8

### C · Chemistry — design flaws in its instructions
- **C3-1 · The running ZIP had to be re-attached by her every batch.** It was missing six batches in a row.
  → Auto-vault + vault file + newest-copy restore → CI§3
- **C3-2 · "If counts don't match, stop" and "never proceed past a failing check".**
  → Quarantine the paper; the session continues → CI§7
- **C3-3 · Tiers and briefs locked until "coverage complete".**
  → Outputs at every milestone, with coverage stamps → P§14
- **C3-4 · She typed batch numbers and years and got them wrong four times.**
  → She types `Go.`; Claude derives both → CI§10
- **C3-5 · Rules said papers stay in the chat; reality put them in project knowledge.**
  → This project is designed around her real routine (rotating schemes, papers in chat) → CI§4
- **C3-6 · "Skip Devanagari entirely".** A missing English page was recovered only from the Hindi page.
  → Hindi is the backup source → P§6
- **C3-7 · No rule for cross-series repeats.**
  → shuffle / variant / repeat defined before row one → P§7.4
- **C3-8 · Archetype codes could be issued only in a separate "merge session",** so they were never issued.
  → Codes are issued inside every year, by the same session that classifies → CI§5

### D · Chemistry batches
- **B1 · Schema gaps; condensed rows; MCQs typed as mechanisms; options unrecorded.**
  → Full schema from row one; options mandatory → P§7
- **B2 · An unquoted comma broke the CSV.**
  → Kit writer only → P§4
- **B2 · Two scanned papers were deferred and forgotten until B12.**
  → Scans are normal (image-first). Nothing is deferred without a PROGRESS line → P§6, P§11
- **B2 · No year printed; attributed from PDF creation dates.**
  → `year_evidence` mandatory; the scheme-footer code `YY-SS-SSN` is a new proof → P§5
- **B3 · STEP-AWARDS empty (no scheme);** no transfer of templates.
  → TRANSFERRED steps, labelled → P§9
- **B4 · A paper falsely declared a duplicate was never extracted;** a "fix" moved Section-E rows into the wrong paper.
  → Similarity is computed + checked on images; rows are never moved; ERRATA only → P§7.4
- **B4 · 150 dpi too low for a structure.**
  → Originals at 200 dpi, crops at 300 dpi; bundles use dual-read → P§6
- **B5 · choice_pair_id collided with instance_id;** the validator scanned its own report.
  → Fixed ID namespaces; validator reads ledgers only → P§7
- **B6 · The validator read "§1" as a number;** the compaction transcript held no question text.
  → Tested validator; chat history is never a data source → P§12
- **B7 · Two days lost to many past-chat searches and staged work.**
  → Maximum two lookups per boot; write rows, then one build call → CI§3
- **B8 · Five turns of extraction held only in reasoning.**
  → Per-paper save + tick → CI§6
- **B8 · Earlier conventions broken:** equal-split part marks, cross-series marked duplicate, `OR-` prefix missing, dotted IDs, two-demand stems not split, printed_as missing, DRAFT registers missing. Delhi rows carried All-India wording.
  → Conventions enforced by schema + validator; stems from that paper's own page → P§7, P§12
- **B9 · Low row counts in B1–B6** came from deferred scans and unchecked skips.
  → Question continuity is checked by code → P§12
- **B10 · An empty tool call needed "Continue";** a checker regex misread IDs.
  → Tested kit; cheap resume → P§4
- **B11 · Opened every page of six papers before writing a row,** and was cut off with zero rows.
  → One paper at a time → CI§6
- **B11 · Hard-coded "29 OR" was wrong (30).**
  → Computed report lines only → P§12
- **B11 · A 2009 file was missing printed page 11.**
  → Page-continuity check; UNREADABLE row → P§6
- **B11 · A printed mark contradicted the paper's own instructions.**
  → Record both; blueprint wins for totals; flag → P§8
- **B12 · Batch 0 and Batch 1 both shipped as `PYQ-CHEM-043.zip`;** the empty one was audited.
  → Vault files carry batch, date and row count in the name; restore never trusts names; zero-row guard → P§3
- **B12 · Superseded reports inside a ZIP (208 vs 346 rows).**
  → Derived files are regenerated, stale ones dropped → P§4
- **B12 · Part shares were checked only against the question total.**
  → Checked against the printed group total → P§12
- **B12 · Conventions never back-applied.**
  → Same-session migration → P§21
- **B13 · A misread half-mark ("2 × 1½ = 3" recorded 1+1)** failed validation for weeks.
  → Half-marks from images; failing papers re-read, not carried → P§6
- **B13 · The top-up list was cluttered and asked for unobtainable papers.**
  → Three plain sections; UNAVAILABLE is never asked again → CI§11
- **Inputs · Set-wise schemes exist only from 2022;** earlier years have single one-page schemes.
  → Expected; TRANSFERRED/INFERRED covers it; never nag → P§9
- **Inputs · Every paper she sends is everything she could find.**
  → Never ask for missing ones again; never drop one she sent → CI§8
- **Papers · A Physics constants block inside Chemistry papers; a misprinted value.**
  → Record as printed with `(sic)` and a flag → P§6

### E · The 28 September build — the mistakes she caught
- **S28-1 · "v4" in every file and project name.** She never asked for version labels.
  → No version numbers in any name → CI§10
- **S28-2 · Designed only for papers-in-chat;** ignored her plan to rotate each year's marking schemes through project knowledge.
  → The year cycle is built on her plan → CI§4
- **S28-3 · Custom Instructions thin, with the substance pushed into another file.**
  → The CI now holds every rule and every exception → CI (whole)
- **S28-4 · Kit path wrong:** it said `/mnt/skills/user/`; the installed skill lives at `/mnt/skills/plugins/cbse-pyq-kit/`.
  → Boot searches `/mnt/skills` for `pyqkit.py` → CI§3
- **S28-5 · Resources unused:** the Chemistry lesson file in memory unread; examiner rules in the 2026 scheme unread; CBSE archives unresearched; toppers' books, question bank, competency volumes and Learning Framework missing.
  → PHY-04 dossier; boot resource checklist → P§22
- **S28-6 · "Competency is 50%" told to her as fact.** The syllabus design table is 38/32/30 by thinking level; 50% is a reported general figure.
  → VERIFIED/REPORTED labels on every fact → CI§2
- **S28-7 · The syllabus link was not verified.** 2026-27 syllabi moved to `SecPart2` URLs.
  → Only verified links in her order list → PHY-00
- **S28-8 · "One ZIP per year with papers and schemes"** clashed with her rotation plan.
  → Papers in chat as a ZIP; schemes in project knowledge → CI§4
- **S28-9 · No per-year Definition of Done, no index spec, no naming spec.**
  → `year-close` gate; INDEX; naming rules → CI§5, CI§10, P§11
- **S28-10 · Sample papers scheduled early.** She wants the decision after all board years.
  → SQPs 2023-24 → 2025-26 are an end-phase decision; only 2026-27 is permanent → CI§4
- **S28-11 · No decision on Claude Code;** left as a vague option.
  → A clear rule for when to use it, with setup → PHY-00
- **S28-12 · The kit needed poppler,** so it could not run on her own computer.
  → Fallbacks (pypdfium2 / PyMuPDF / pypdf) → P§4
- **S28-13 · The auto-vault was never live-tested** yet was presented as primary.
  → The vault file in project knowledge is the guaranteed route; auto-vault is tested at Batch 0 → CI§3
- **S28-14 · Bundles called "risky for superscripts"** with no fix offered.
  → Dual-read: structure from the image, digits cross-checked against the page text; conflicts flagged → P§6
- **S28-15 · The reply over-summarised.** She read every file and found the gaps herself.
  → Files complete and self-checking; replies short but specific → CI§11

### F · The 29 September rebuild
- **S29-1 · A tool call writing the 141-row archetype catalogue in one piece was aborted.** Nothing was saved, and she had to type "Continue" (the Batch 10 pattern).
  → Large content is written in parts, each saved and counted before the next (the catalogue was then written as part A + part B, verified by code) → CI§6
- **S29-2 · The first catalogue check found three names over the 12-word limit.**
  → Every generated catalogue or ledger is checked by code against the naming rules before it is ticked → CI§10
- **S29-3 · Tests on sparse data showed the first mock planner overflowing mark-group quotas** in stress and seed modes (e.g. G5 4/7).
  → Scarcity rule (bigger slots go to groups short of archetypes), seed retries, and a quality gate: a failing plan is never shown → P§15.3

---

## PART 3 — Risks created by the new yearly workflow (pre-empted)

- **W-1 · Last year's schemes left in project knowledge.**
  → At intake, the scheme year (printed year / footer code) is compared with the paper year. A mismatch is reported in one line; a scheme is never used for another year's paper → CI§7
- **W-2 · RAG search returns a chunk from the wrong scheme.**
  → Scheme lines are read from the file on disk (`/mnt/project`), never from search snippets → CI§4
- **W-3 · Two vault files in project knowledge.**
  → Restore picks the newest verified one and names the other as stale → CI§3
- **W-4 · A year spans several chats and the ZIP is not re-attached.**
  → The first line of the session says exactly which files are missing; work that doesn't need them continues (scheme pass, classification) → CI§7
- **W-5 · Archetype names drift between chats.**
  → Seed catalogue + `candidates` search + registry read before any new code → CI§5
- **W-6 · Seed (DRAFT) archetypes counted as evidence.**
  → DRAFT never enters statistics; promoted only by a real instance → CI§2
- **W-7 · The 2026 "both options, higher score" rule assumed for 2027.**
  → Flagged as a 2026 fact; checked against the 2027 scheme when it exists → PHY-04
- **W-8 · Case passages copied at length.**
  → Context summary only → P§7.3
- **W-9 · An OR pair spanning two chapters breaks unit quotas.**
  → Side A counts for quotas; R12 records cross-chapter pairs → P§15
- **W-10 · Compartment papers mixed into main statistics.**
  → `exam = COMPT` kept separate in every statistic unless stated → P§10
- **W-11 · Visually-impaired papers (letter codes) double-count.**
  → Their repeated questions are shuffles/variants of the main sets → P§7.4
- **W-12 · A year declared "done" with loose ends.**
  → Only `year-close` PASS closes a year; its report lists anything left → CI§5

---

## PART 4 — Physics-specific traps (pre-empted)

- **PM-1 · Circuit values live only in figures.**
  → FIGURES netlists → P§6.4
- **PM-2 · Visually-impaired alternatives double-count marks.**
  → `vi_alt = y`, excluded from sums → P§7
- **PM-3 · Choice layout changes by year** (2026-27: 2 in B, 1 in C, 3 in E).
  → Read per paper → P§8
- **PM-4 · Assertion–reason option sets change.**
  → Stored per paper → P§7
- **PM-5 · Units, signs and directions** (lens sign convention, "along −î", T m A⁻¹).
  → Units stay with values; directions copied exactly → P§6.3
- **PM-6 · Half-syllabus 2022 terms create false "never asked".**
  → Term-aware eligibility → P§10
- **PM-7 · Deleted topics leaking into mocks.**
  → The syllabus status gate → P§15
- **PM-8 · Probabilities shown without testing.**
  → Labelled `uncalibrated` until backtested → P§16
- **PM-9 · Wrong answers in generated schemes.**
  → Python-solved, unit-checked → P§15
- **PM-10 · Archetypes too coarse or too fine.**
  → Granularity test → P§10
- **PM-11 · Text layers mangle physics** (10⁸ → 108, hν → h, ¹⁶₈O → 168O, 30° → 300, B₁/B₂ → B and B).
  → Image-first always → P§6
- **PM-12 · Syllabus limitations ignored.** A derivation asked for a "no derivation" topic, or numericals for "qualitative only".
  → The limitation column blocks those mock types → P§15
