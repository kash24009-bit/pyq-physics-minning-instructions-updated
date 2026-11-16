| unit | steps | images (n · KB · largest) | first step read / write | cache misses (step) | raw sum | weighted sum | output (thinking share) | cache writes | cache reads | uncached input | main session weighted | minutes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FIX-10 | 21 | 22 · 1,330 · p15-top.png 101 | 0 / 7,960 | 0 | 1,787,423 | 424,262 | 44 % (61 %) | 37 % | 19 % | 0 % | 858,491 | 6.5 |
| T1-2022-SQP | 34 | 40 · 2,510 · fig_5.png 199 | 5,618 / 2,256 (shared) | 0 | 3,817,391 | 769,212 | 45 % (53 %) | 32 % | 23 % | 0 % | 287,694 | 11.4 |
| T1-2022-SQP | 26 | 39 · 1,252 · cal_1.png 69 | 5,618 / 2,253 (shared) | 1 (10) | 2,998,555 | 706,655 | 30 % (65 %) | 52 % | 19 % | 0 % | 344,097 | 47.4 |
| SQP2425-042 | 30 | 40 · 2,679 · figA_2.png 139 | 5,618 / 2,222 (shared) | 0 | 3,393,463 | 907,236 | 53 % (62 %) | 30 % | 17 % | 0 % | 109,120 | 14.4 |
| S6 unit S6-CH02. Read /mnt/project/PHY-1 | 21 | 0 · 0 | 5,618 / 1,373 (shared) | 0 | 2,180,936 | 610,265 | 50 % (91 %) | 34 % | 16 % | 0 % | 128,895 | 9.9 |

Image check (steps that read only images): visual tokens = sum of ceil(w/28) x ceil(h/28) as sent; growth = next step's context - this step's context - its output.

| unit | kind | images opened (all steps) | largest w x h | images in image-only steps | visual tokens | growth - output | ratio |
|---|---|---|---|---|---|---|---|
| FIX-10 | bands | 16 | 1530 x 1095 | 16 | 34,310 | 34,808 | 1.01 |
| FIX-10 | sheets | 6 | 1324 x 1519 | 6 | 11,176 | 11,362 | 1.02 |
| T1-2022-SQP | bands | 30 | 1530 x 1030 | 30 | 61,050 | 61,974 | 1.02 |
| T1-2022-SQP | sheets | 10 | 1564 x 1535 | 10 | 18,713 | 19,008 | 1.02 |
| T1-2022-SQP | bands | 36 | 1530 x 1030 | 36 | 73,260 | 74,352 | 1.01 |
| T1-2022-SQP | sheets | 3 | 1564 x 1476 | 3 | 5,123 | 5,208 | 1.02 |
| SQP2425-042 | bands | 26 | 1489 x 1095 | 26 | 56,160 | 56,952 | 1.01 |
| SQP2425-042 | crops | 3 | 1364 x 755 | 2 | 650 | 688 | 1.06 |
| SQP2425-042 | sheets | 11 | 1488 x 1510 | 12 | 21,845 | 22,217 | 1.02 |

Largest share of the weighted sum over these units: output (45 %; output 45 %, cache writes 36 %, cache reads 19 %, uncached input 0 %).
