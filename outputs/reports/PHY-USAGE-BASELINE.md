# PHY usage baseline (B08, 2026-10-26)

Weighted sums in base-input equivalents (Opus 5.5 list rates against base input: uncached input 1, cache read 0.05, 5-minute cache write 1.25, 1-hour cache write 2, output 5; thinking is billed as output). This machine's transcripts carry no usage.cache_creation split, so subagents count as 5-minute writes and the main session as 1-hour writes (her decision 2026-10-21). Measured by outputs/tools/phy_measure.py (edition 2026-10-26) on the reader transcripts of this session's first units. The main-session column covers the main session's calls from the previous unit's end to this unit's end; the FIX-8 figure includes the boot and the tool building (Y§0.5 steps 1-6, the sibling worksheet).

| unit | steps | images (n · KB · largest) | first step read / write | cache misses (step) | raw sum | weighted sum | output (thinking share) | cache writes | cache reads | uncached input | main session weighted | minutes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FIX-8 | 16 | 5 · 251 · q33c_1.png 89 | 0 / 8,023 | 0 | 442,569 | 122,965 | 43 % (40 %) | 41 % | 16 % | 0 % | 874,100 | 2.3 |
| S1-2023 | 23 | 74 · 6,815 · p1-top.png 208 | 0 / 8,079 | 0 | 3,096,950 | 697,514 | 33 % (50 %) | 47 % | 20 % | 0 % | 1,232,209 | 11.0 |
| S2A-2023 | 21 | 83 · 7,620 · p1-bot.png 251 | 5,594 / 2,267 (shared) | 0 | 2,915,951 | 581,891 | 26 % (50 %) | 51 % | 23 % | 0 % | 231,978 | 7.4 |

Image check (steps that read only images): visual tokens = sum of ceil(w/28) x ceil(h/28) as sent; growth = next step's context - this step's context - its output.

| unit | kind | images opened (all steps) | largest w x h | images in image-only steps | visual tokens | growth - output | ratio |
|---|---|---|---|---|---|---|---|
| FIX-8 | crops | 2 | 497 x 702 | 2 | 936 | 1,026 | 1.10 |
| FIX-8 | sheets | 3 | 1555 x 1166 | 3 | 6,192 | 6,325 | 1.02 |
| S1-2023 | bands | 72 | 1530 x 1094 | 74 | 153,744 | 156,174 | 1.02 |
| S1-2023 | crops | 2 | 960 x 281 | 0 | 0 | 0 | - |
| S2A-2023 | bands | 60 | 1489 x 1095 | 60 | 129,600 | 131,520 | 1.01 |
| S2A-2023 | sheets | 23 | 1550 x 1543 | 23 | 50,053 | 50,833 | 1.02 |

Largest share of the weighted sum over these units: cache writes (49 %; output 31 %, cache writes 49 %, cache reads 21 %, uncached input 0 %).
