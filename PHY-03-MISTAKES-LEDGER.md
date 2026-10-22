# PHY-03 · MISTAKES LEDGER — Physics (042)
### Every mistake made so far in PYQ mining, why it happened, and the rule in this project that prevents it

**How to use this file (Claude):**
1. Read Part 1 and Part 4 at every boot.
2. Before any year starts, read Part 3 (new-workflow risks).
3. A mistake listed here that happens again is the worst possible outcome of a session.
4. Every new mistake gets an entry here, with its fix, before the session closes (P§21).
5. On the Claude Code route (from Batch 2), new entries go to the vault's `notes/PHY-03-ADDENDUM.md`, which the lean boot reads in full (CLAUDE.md §6); this file is read when a step cites it.

*Edition 2026-10-21: the addendum's entries to Batch 6 are folded in (sections G to L, W-13 to W-16), with section M, W-17 to W-23, PM-13 and PM-14 added from the 21 October review in the project chat.*

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

### G · Batch 0 (29 September)
- **B0-1 · The project's sample paper was last session's.** `Physics-SQP.pdf` prints "CLASS – XII (2025 – 26)"; CBSE reuses that file name every year, and PHY-04 §2's "SQP 2026-27" details (VI alternative inside Q9; text damage 168O, "B and B", 300) are absent from it. Caught at boot from the page-1 image.
  → A permanent file's session is read from its page-1 image, never from its name; a mismatch is logged and the file is mined for what it is → CI§7, P§5
- **B0-2 · Two "errors in the official syllabus" in PHY-04 §1 were text-layer damage.** The page-12 image prints 7 marks for Unit IX and "Chapter–14"; the text layer had moved the 7 into the chapter line.
  → A claimed error in an official document is recorded only after its page image confirms it → CI§2, P§6
- **B0-3 · The boot search pattern `pyqkit*.py*` misses the project copy `pyqkit_py.txt`.** The kit was found by listing the folder.
  → Boot also matches `pyqkit_py.txt`; the CI wording is queued for correction → CI§3
- **B0-4 · The first Batch 0 reply stopped at the tool limit before its checkpoint,** leaving the database copy older than the disk for one turn (nothing lost; `Resume` packed first).
  → Checkpoint right after the gate items, before opening a paper, as well as after each paper → CI§6
- **B0-5 · Inventory reads identity from text only;** the 2026 scheme bundles have near-empty text layers, so kind, year and paper id came out unknown.
  → Image-only files get their identity from their page images at S1 intake, through ERRATA → P§5

### H · Batch 1 (29-30 September)
- **B1-1 · The first Batch 1 reply hit the tool limit before its first checkpoint (a repeat of B0-4).** About thirty separate calls went to boot reads and identity crops; the identity confirmations lived only in the chat until the next turn. Nothing was lost (the vault was unchanged), but a repeat is the worst outcome this ledger names.
  → Boot reads are batched into one or two calls; each stage's findings are written to disk by one script as soon as they are read; the first checkpoint comes right after S1, before any paper page is opened -> CI s6, P s11
- **B1-2 · A paper_id opened the wrong document.** After S1 gave each scheme its paper's paper_id, `render 2026-5511` rendered the scheme bundle; caught at once from the text printout, before any row was written.
  → Documents are opened by file_id; kit fix queued (Q-008) -> P s4
- **B1-3 · The kit could not total a case study whose choice sits inside one sub-part when sub-part marks are printed** (55/2/1 Q29, Q30): it summed each side alone, so the paper failed check-paper though nothing was wrong on the page.
  → Fixed once in kit edition 2026-09-30 (common sub-parts count with each alternative), tested on every mined paper plus a planted overflow, logged, shipped in tools/ -> CI s7, P s4
- **B1-4 · A test script rewrote a scratch table without closing the file before the check ran,** so the check read a half-written file and reported missing questions. Scratch copy only; the vault was never touched.
  → Test harnesses close (or use `with`) every file before calling the kit -> P s4
- **B1-5 · A row count was typed into a PROGRESS line by hand (79 for 55/3/1) instead of taken from the data; the kit had just printed 72.** Caught before the checkpoint went out; corrected from the table.
  → Progress lines take their counts from the tables in the same script, never from memory -> CI s2.7
- **B1-6 · The time estimate in a reply said 13 sibling papers were left; the tables said 12.** The count was typed before the tables were read.
  → Counts in replies, estimates included, come from a script run earlier in the same turn -> CI s2.7

### I · Batch 2 (1 October, first Claude Code session)
- **B2-1 · The setup gave the scheme repository no role.** The vault file sits in the instructions repository and the 2026 schemes in a repository with neither a vault file nor a ZIP, so `phy_code_env.py` linked none of the scheme PDFs and inventory would have missed every one. Caught at boot from the setup's role lines; the PDFs were linked into /mnt/project by hand (links only) before inventory ran as CLAUDE.md §6 writes it.
  → At boot, every repository found must have a role or be opened by hand before inventory; Q-011 → CLAUDE.md §6, R§2
- **B2-2 · R§3's `render <file_id>` stopped with "cannot find document"** because the kit's `--vault` defaults to empty. Nothing was written from it.
  → Pass `--vault /home/claude/vault` to `pages` and `render`; Q-011 → R§3
- **B2-3 · Batch 1 misread the polarity of one cell in 55/3/1 Q17(a)** (F-2026-5531-02 puts E_2's longer plates towards B; the page shows them towards C, so the cells oppose and EQ-2026-5531-003's E_1 + E_2 is wrong). Every number on the row was right, so neither check-paper nor a numbers-only double-read could see it; the B02 extractor found it by comparing the sibling figures on 600-dpi crops, and both B02 rows describe the page.
  → A figure whose meaning depends on polarity or direction (cells, diodes, arrows, field lines) gets a crop on which plate lengths or arrowheads are measured, and its FIGURES description names the orientation; the stored rows are corrected through ERRATA (Q-013) -> CI s2.2, P s6.4
- **B2-4 · The 55/B/7 extractor wrote note text into the options column of 36 non-MCQ rows** (2026C-55B7-Q19 to -Q33B-ii); the gate check passed it and only the blind double-read showed it.
  → options is filled only when q_type is MCQ or AR; the double-read stays on every paper → R§5, R§8

### J · Batch 3 (2 October; lessons from the Batch 2 audit)
- **B3-1 · Detail thinned at speed.** The overnight run (effort max) wrote figure descriptions of 143 characters against the trial's 201, 1.38 formula rows per numerical or derivation against 1.86, and notes on 35 % of new rows against 61 %; values were equally accurate, so no check saw it.
  → Every new row is written to the trial's level: complete stems, givens and unknown, every figure element with value, position and direction, given/asked/result formulas for the whole chain, a note on every new sibling row → PHY-08 Y§6
- **B3-2 · Note text passed through the options column** (2026C-55B7, 36 non-MCQ rows): the gate check of the time accepted it and only the blind double-read caught it.
  → Gate edition 2026-10-02 refuses `options` on a row whose q_type is not MCQ or AR → PHY-07 R§9, PHY-08 Y§7
- **B3-3 · A blank rel passed** (2026-5552, 15 new rows; fixed ER-B02-088..ER-B02-102).
  → Gate edition 2026-10-02 refuses a row with a blank `rel` → PHY-07 R§9, PHY-08 Y§7
- **B3-4 · The setup could not see a vault kept only on a branch**, so a new session would have found no vault on main.
  → Setup edition 2026-10-02b collects vault files from every branch, restores the newest and carries its branch forward → PHY-07 R§2, CLAUDE.md §3
- **B3-5 · Browser-renamed tool files broke the boot command** (`phy_gate (1).py`, `phy_code_env (2).py`, `PHY-07-CLAUDE-CODE-RUNBOOK (1).md`): the old command looked for exact names.
  → The boot command finds `phy_code_env*.py`; the setup links renamed copies under their plain names, picks the newest and names the extras → CLAUDE.md §6, PHY-07 R§2
- **B3-6 · Inventory files a sample paper's scheme as a board scheme** (Physics-MS.pdf 2025-26 at B02; the 2026-27 one again at B03: kind MS, exam MAIN, placeholder paper_id 2027-X7aec84).
  → Its identity is fixed at S1 from the page-1 image through ERRATA (kind SQP-MS, exam SQP, paper_id SQP<yy><yy>-042), as ER-B02-072..ER-B02-076 did → PHY-08 Y§0.4, P§5
- **B3-7 · Classification spent her usage on a stage she wanted later,** because the old CLAUDE.md said to go on until the year closed; she stopped it during chapter 03.
  → Printed documents of 2025 to 2022 first; S5-without-scheme, S6, S7 and S8 of every year are DEFERRED lines for the closing sweep and are never started without her → CLAUDE.md §12, PHY-08 Y§0
- **B3-8 · The year planner trusted code shape over FILES.** `--plan-year 2025` read the letter in 55/S/1 as a visually-impaired code and ignored sets_covered on the 2025 schemes, so PROGRESS lacked the compartment origin and called printed sibling schemes missing. Caught by reading the planned lines against FILES before the first paper.
  → After every `--plan-year`, check each planned line against FILES (series, exam, sets_covered) before mining; wrong lines are corrected through the gate and queued (Q-022), never by hand → CLAUDE.md §8, R§9

### K · Batch 5 (6-18 October; 2024 papers)
- **B5-1 · A shuffle copied its origin's ARSET.** 2024-5513-Q16 is a shuffle of 2024-5511-Q13, the origin's first assertion-reason row, and kept its ARSET although 2024-5513-Q13 already carried the paper's own; the gate check does not test it. Found by the 55/2/2 extractor; fixed by FIX-5 (ER-B05-010).
  → The extractor brief says to remove ARSET from any copied row that is not the paper's first A-R row; a one-line script after each S4 paper lists papers with more than one ARSET row → R§5, CONVENTIONS "S4 method (B01)"
- **B5-2 · An extractor stopped by a server or usage limit loses only its context, not its crops.** The 2024-5511 retry reused the first attempt's renders; three later extractors (2024-5541, -5551, -5522) were resumed with their own context by message instead of restarted.
  → Briefs say to write part files section by section; a stopped extractor is resumed, not restarted, when its context is intact → R§16
- **B5-3 · A paper count typed into two replies ("22 question papers of 2024"); FILES holds 20 (15 main-series papers, 55(B), and the four compartment papers).** Caught when the S2b check counted by script before ticking.
  → Counts in replies come from a script run in the same turn, never from memory (B1-5, B1-6 again) -> CI s2.7

### L · Batch 6 (19-21 October; 2024 schemes, the 2023-24 sample paper, the 2024 year check)
- **B6-1 · Crops wider than the image viewer's limit were shrunk without notice.** A full-width "400 dpi" crop of an A4 page (about 3300 px) is seen at about 190 dpi; the rows read that way were still right in the 2024 year check, but the margin was smaller than the rules assumed.
  → Half-page bands at 180 dpi on born-digital pages, crops kept within about 1568 px, phy_tile.py prints each sheet's effective dpi, and a twelve-crop calibration opens every new file → rule card A1, B3, B4, E3
- **B6-2 · Figure value fields held numbers the page does not print** (measured plate lengths, a drawn 45 deg, axis fractions; 6 fields of 2024-5512, -5521, -5522, -5523, -5532, -5542; FIX-6, FIX-7).
  → A figure's values column holds only printed values; measurements and estimated angles go to the description → rule card D10
- **B6-3 · A scheme's half marks were attached one line off** (2024-5531-Q31B-ii; the part's total was right, so no sum check could see it; Q-078). A later reader noticed it on a shuffle's page; the year check confirmed it and sent the paper to a second round, which found nothing else (557 values).
  → The second look compares each half mark with the line it is printed beside, not only the totals; a reader that sees a different layout on a sibling set queues it → rule card C8, E1; PHY-08 Y§11.4
- **B6-4 · Lines whose text ran over a page break cited the page where the text starts** (3 lines; FIX-6).
  → A line cites the page where its mark is printed → rule card C15
- **B6-5 · The worksheet script mistook numbered examiner instructions and dot-less question numbers for answers** (55/2/2: 16 of 33 located, then Q1-Q9 misplaced); caught by its own "located n of 33" line before any reader used it.
  → It starts counting after the first answer-page header and accepts "17" without a dot; every worksheet prints "located 33 of 33" before a reader is started → outputs/tools/phy_s5_prep.py

### M · The 21 October review and upgrade (project chat)
- **M-1 · Numbers typed into a draft playbook from memory.** Figures no script could reproduce (the hours of work of two batches, two unit times, an average line length) were written into the first draft. Caught when every number was recomputed before delivery; replaced by figures from the git log and the vault.
  → Every number in an instruction file or report is recomputed from data in the same turn, with its source named → CI§2.7, R3
- **M-2 · A claim about a tool that the tool could not do.** The morning message said the new comparison would clear Tier 1's text-layer suspects (122 in 2024); Tier 1 compares numbers as numbers, so notation never made those suspects. Caught while building the gate; withdrawn.
  → A claim about a tool is checked against its code or its output on real files before it is sent (W-23)
- **M-3 · A behaviour stated without a source.** The same message said Claude Code drops the oldest images when a request passes the image limits; no document says so, and a user report shows an error asking for /compact instead. Withdrawn.
  → Limits and tool behaviour are quoted from the current documents, with the date read (W-18)
- **M-4 · A new rule drafted wider than her decision.** Drafts applied the lead-in rule (Q-094) to case passages and banned stem values from FIGURES `values`; a count of the vault's rows found 21 case questions that never repeat passage numbers and 17 figure rows that mark stem values "(stem)". Both rules were narrowed to what she decided before delivery.
  → Before a rule is written, a script counts how the vault's rows do it now; a rule that would change earlier rows says so and goes to her or to the queue (W-19)
- **M-5 · A detection test checked on one kind of file only.** Hindi pages were to be found by counting Devanagari characters. That works on the Hindi-medium scheme twins, but not on bilingual papers, whose Hindi text layer is not Unicode (CONVENTIONS "Bilingual originals").
  → A test that sorts pages or files is tried on every kind of file it will meet; here, the share of common English words, with a thumbnail sheet for what it cannot settle → PHY-07 R§3
- **M-6 · A summary number that was not the quantity it named.** The gate's first draft printed "66 cleared" when 70 mismatches had been cleared, because it counted normalisation events.
  → The gate counts mismatches cleared and prints the raw count beside them; a summary number is checked against an independent count (here, the raw replay) → PHY-07 R§9
- **M-7 · A locator tested first on one file.** `phy_marks.py`'s drafts took examiner-instruction pages for answers, missed a header in title case, a wider left margin and Section A marks printed only in the total column, and dropped every line containing the word "Total". Running it on all 20 set sections of 2024 and comparing with the year-checked lines found each one.
  → A script that locates or flags is tested on every file of its kind, against verified rows, before its first use → PHY-07 R§11

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
- **W-13 · A permanent file replaced by last session's twin** (CBSE reuses names such as `Physics-SQP.pdf` every year).
  → Boot compares each permanent file's printed session with the one the CI names; a mismatch is logged in one line and never blocks → CI§7
- **W-14 · Two miners writing one vault** (the chat and Claude Code at once): restore keeps only the newest copy, so the other one's work vanishes silently.
  → One writer at a time: Claude Code mines; the chat audits read only and sends `Fix:` lines → CLAUDE.md §3, PHY-07 R§13
- **W-15 · An agent that can run code is tempted to fill rows from the text layer with a script.**
  → Every value is read from a page image; the text layer only cross-checks digits; a blind second reading is compared by the gate before any merge → CI§2.2, PHY-07 R§6-R§8
- **W-16 · A long session compacts and loses rules held only in conversation.**
  → Rules live in CLAUDE.md (re-read after compaction); state lives on disk (PROGRESS, part files, pushed packs) → CLAUDE.md §9
- **W-17 · Usage compared by raw token sums.** Raw sums count re-read history like new input; the plan meter weights a re-read token at 0.05 of an input token and an output token at 5.
  → Every unit is measured by its weighted sum, and methods are compared on it → PHY-08 Y§1, PHY-07 R§14
- **W-18 · Limits remembered instead of read.** The image limit was taken as 1568 px, the standard tier's, though Opus 5.5 is on the high-resolution tier; the limits that bind are the refusal of any image over 2000 px in a request with more than 20 images, and Claude Code's re-encoding of images over 500 KB.
  → Limits come from the current documents, with the date read, and what actually arrives is measured (the image check) → rule card A9, PHY-08 Y§8
- **W-19 · A rule written without counting how the vault does it now.**
  → Count first; a rule that changes earlier rows is decided by her or queued, and the change is back-applied by ERRATA → P§21
- **W-20 · A fix that stops at the origin row.** F-2024-5521-11's error had been copied into two shuffles.
  → Every shuffle copy of a corrected row gets its own ERRATA row; `G lint --all` lists copies left behind → PHY-07 R§8, R§13
- **W-21 · Items addressed to a check outlive the check.** Six queue items asked the 2024 year check to confirm or decide something; it closed without them.
  → The year check's last step lists every open queue item that names it, and settles or re-addresses each → PHY-08 Y§11 step 6
- **W-22 · A file uploaded where the vault's branch also writes.** A tool uploaded into `outputs/` on main would conflict with the merge of the vault's branch, and the setup would undo that merge.
  → Her uploads go to the root of the instructions repository only → PHY-07 R§2
- **W-23 · Instruction files that describe features not yet built.**
  → Every instruction about a tool is checked against the shipped code before delivery; a feature still to be built is named as such, with who builds it and when → PHY-07 R§11

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
- **PM-13 · A drawing invites measuring.** Plate lengths, drawn angles and axis positions look like data, but the figure does not print them.
  → `values` hold printed numbers; measurements go in the description, marked "measured, not printed" → rule card D10
- **PM-14 · Scheme keys and values can be doubtful** (a sign ignored, a magnitude given for a signed order, a slip in a printed value).
  → Kept as printed, computed in Python, queued with the working; mock answers are solved in Python, never copied from a scheme (PM-9) → rule card C9
