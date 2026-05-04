# Spider — axioms vs no-axioms: experimental results

Generated from 42 run logs.

## Coverage (instances solved per cell, 5 min / 4 GB budget)

| track | encoding × heuristic | solved / total |
|---|---|---:|
| opt | noaxioms + blind | 5 / 8 |
| opt | noaxioms + lmcut | 5 / 8 |
| opt | axioms + blind | 5 / 8 |
| opt | axioms + hmax | 5 / 8 |
| sat | noaxioms + lama | 3 / 5 |
| sat | axioms + lama | 5 / 5 |

## Translator stats (encoding compactness)

Per IPC instance, comparing the no-axioms baseline against the axioms reformulation. These numbers come from FD's translator and are recorded even when search times out. The ratio columns show axioms / no-axioms.

| track | inst | vars (n / a / ratio) | operators (n / a / ratio) | task size (n / a / ratio) | derived vars (a) | axioms (a) |
|---|---|---|---|---|---:|---:|
| opt | p01 | 170 / 104 / 0.61 | 2870 / 1594 / 0.56 | 44385 / 19694 / 0.44 | 48 | 299 |
| opt | p03 | 316 / 189 / 0.60 | 9645 / 5255 / 0.54 | 148112 / 64318 / 0.43 | 100 | 876 |
| opt | p05 | 494 / 290 / 0.59 | 22345 / 11097 / 0.50 | 330751 / 135404 / 0.41 | 168 | 1927 |
| opt | p07 | 170 / 104 / 0.61 | 2866 / 1516 / 0.53 | 42507 / 18814 / 0.44 | 48 | 325 |
| opt | p09 | 316 / 189 / 0.60 | 9443 / 4839 / 0.51 | 138555 / 59445 / 0.43 | 100 | 936 |
| opt | p11 | 494 / 290 / 0.59 | 22863 / 11807 / 0.52 | 337704 / 143972 / 0.43 | 168 | 1911 |
| opt | p13 | 704 / 407 / 0.58 | 44157 / 21193 / 0.48 | 636088 / 257780 / 0.41 | 252 | 3436 |
| opt | p15 | 222 / 136 / 0.61 | 4387 / 2419 / 0.55 | 63661 / 30042 / 0.47 | 64 | 499 |
| sat | p01 | 494 / 290 / 0.59 | 22438 / 11352 / 0.51 | 334718 / 138428 / 0.41 | 168 | 1897 |
| sat | p03 | 704 / 407 / 0.58 | 43267 / 19993 / 0.46 | 624511 / 243315 / 0.39 | 252 | 3458 |
| sat | p05 | 1036 / 585 / 0.56 | 103363 / 43663 / 0.42 | 1452601 / 529043 / 0.36 | 396 | 6924 |
| sat | p07 | 376 / 225 / 0.60 | 12057 / 6455 / 0.54 | 180216 / 79166 / 0.44 | 120 | 1144 |
| sat | p09 | 628 / 363 / 0.58 | 38647 / 18553 / 0.48 | 556651 / 225623 / 0.41 | 224 | 2998 |

## Optimal search — informative-admissible head-to-head

`noaxioms+lmcut` is the best informative-admissible cell on the no-axioms encoding; `axioms+hmax` is the equivalent on the axioms encoding. Same optimal cost on every instance — cells differ on expansions and time.

| inst | cost | expanded (n / a / ratio) | total time s (n / a / ratio) |
|---|---:|---|---|
| p01 | 16 | 908 / 880 / 0.97 | 0.850534 / 0.12398 / 0.15 |
| p03 | 22 | 33080 / 39642 / 1.20 | 107.064693 / 22.430748 / 0.21 |
| p07 | 16 | 1648 / 762 / 0.46 | 0.751959 / 0.087889 / 0.12 |
| p09 | 25 | 17547 / 33916 / 1.93 | 66.685985 / 16.231008 / 0.24 |
| p15 | 17 | 354 / 299 / 0.84 | 0.399812 / 0.079916 / 0.20 |

## Optimal search results

4-cell matrix: {no-axioms, axioms} × {blind, informative-admissible}. Wall-clock budget 5 min, memory 4 GB. `lmcut` runs on the no-axioms encoding; `hmax` runs on the axioms encoding (lmcut does not reliably support axioms in this FD build).

| inst | encoding | heur | status | cost | length | expanded | search time (s) | total time (s) |
|---|---|---|---|---:|---:|---:|---:|---:|
| p01 | axioms | blind | solved | 16 | 36 | 6154 | 0.028062 | 0.042695 |
| p01 | axioms | hmax | solved | 16 | 36 | 880 | 0.107945 | 0.12398 |
| p01 | noaxioms | blind | solved | 16 | 67 | 12211 | 0.055984 | 0.087964 |
| p01 | noaxioms | lmcut | solved | 16 | 69 | 908 | 0.823446 | 0.850534 |
| p03 | axioms | blind | solved | 22 | 52 | 1312563 | 10.218173 | 10.266129 |
| p03 | axioms | hmax | solved | 22 | 52 | 39642 | 22.375289 | 22.430748 |
| p03 | noaxioms | blind | solved | 22 | 116 | 3467544 | 27.388724 | 27.499891 |
| p03 | noaxioms | lmcut | solved | 22 | 117 | 33080 | 106.960717 | 107.064693 |
| p05 | axioms | blind | timeout | — | — | — | — | — |
| p05 | axioms | hmax | timeout | — | — | — | — | — |
| p05 | noaxioms | blind | timeout | — | — | — | — | — |
| p05 | noaxioms | lmcut | timeout | — | — | — | — | — |
| p07 | axioms | blind | solved | 16 | 36 | 2432 | 0.011963 | 0.035965 |
| p07 | axioms | hmax | solved | 16 | 36 | 762 | 0.071992 | 0.087889 |
| p07 | noaxioms | blind | solved | 16 | 67 | 5078 | 0.019976 | 0.051967 |
| p07 | noaxioms | lmcut | solved | 16 | 63 | 1648 | 0.723961 | 0.751959 |
| p09 | axioms | blind | solved | 25 | 55 | 710849 | 5.79987 | 5.839855 |
| p09 | axioms | hmax | solved | 25 | 55 | 33916 | 16.18711 | 16.231008 |
| p09 | noaxioms | blind | solved | 25 | 119 | 1875296 | 16.83888 | 16.926866 |
| p09 | noaxioms | lmcut | solved | 25 | 121 | 17547 | 66.594011 | 66.685985 |
| p11 | axioms | blind | timeout | — | — | — | — | — |
| p11 | axioms | hmax | timeout | — | — | — | — | — |
| p11 | noaxioms | blind | timeout | — | — | — | — | — |
| p11 | noaxioms | lmcut | timeout | — | — | — | — | — |
| p13 | axioms | blind | timeout | — | — | — | — | — |
| p13 | axioms | hmax | timeout | — | — | — | — | — |
| p13 | noaxioms | blind | timeout | — | — | — | — | — |
| p13 | noaxioms | lmcut | timeout | — | — | — | — | — |
| p15 | axioms | blind | solved | 17 | 41 | 810 | 0.004184 | 0.028112 |
| p15 | axioms | hmax | solved | 17 | 41 | 299 | 0.047968 | 0.079916 |
| p15 | noaxioms | blind | solved | 17 | 73 | 1535 | 0.008052 | 0.052129 |
| p15 | noaxioms | lmcut | solved | 17 | 79 | 354 | 0.355854 | 0.399812 |

## Satisficing — LAMA anytime trajectories

Both encodings under `--alias lama`. Trajectory is the sequence of improving solutions LAMA finds before the time budget runs out.

### p01

| encoding | t (s) | length | cost |
|---|---:|---:|---:|
| noaxioms | 10.014252 | 221 | 34 |
| axioms | 1.747746 | 77 | 37 |

### p03

| encoding | t (s) | length | cost |
|---|---:|---:|---:|
| noaxioms | (no solution) | | |
| axioms | 4.99167 | 119 | 69 |
| axioms | 57.525822 | 118 | 68 |
| axioms | 58.749776 | 117 | 67 |
| axioms | 120.817509 | 116 | 66 |
| axioms | 121.009119 | 106 | 56 |
| axioms | 121.352196 | 99 | 49 |
| axioms | 156.266025 | 98 | 48 |

### p05

| encoding | t (s) | length | cost |
|---|---:|---:|---:|
| noaxioms | (no solution) | | |
| axioms | 7.335477 | 142 | 80 |

### p07

| encoding | t (s) | length | cost |
|---|---:|---:|---:|
| noaxioms | 28.299465 | 195 | 37 |
| noaxioms | 62.061741 | 187 | 35 |
| noaxioms | 98.961123 | 186 | 34 |
| noaxioms | 168.270256 | 170 | 33 |
| noaxioms | 205.486244 | 162 | 32 |
| noaxioms | 272.616505 | 161 | 31 |
| axioms | 29.422378 | 95 | 61 |
| axioms | 30.401843 | 71 | 37 |
| axioms | 33.902546 | 67 | 33 |
| axioms | 36.357465 | 65 | 31 |
| axioms | 44.078096 | 64 | 30 |
| axioms | 155.719481 | 63 | 29 |

### p09

| encoding | t (s) | length | cost |
|---|---:|---:|---:|
| noaxioms | 11.32345 | 248 | 46 |
| noaxioms | 12.698132 | 251 | 43 |
| noaxioms | 15.180645 | 247 | 42 |
| noaxioms | 16.438487 | 237 | 41 |
| axioms | 1.704194 | 90 | 44 |
| axioms | 2.292314 | 89 | 43 |

