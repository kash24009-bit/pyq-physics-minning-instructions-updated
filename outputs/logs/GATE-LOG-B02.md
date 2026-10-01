# Gate log - batch B02
Every line below was written by phy_gate.py from the data, never typed.

## 2026-10-01T08:12:36Z | S1B | OTHER | GATE PASS
- part files: ERRATA 78
- merged 78 row(s) into l1/ERRATA.csv · now 225
- validate after merge: 16/16 checks pass
- PROGRESS: added a ticked line
- pack: PHY-VAULT-B02-20261001-0812-2185r.json

## 2026-10-01T09:00:06Z | 2026-5532 | S4 | GATE PASS
- part files: BLUEPRINTS 1, CASES 2, INSTANCES 73, FIGURES 16, FORMULAE 41
- merged 1 row(s) into l1/BLUEPRINTS.csv · now 12
- merged 2 row(s) into l1/CASES.csv · now 24
- merged 73 row(s) into l1/INSTANCES.csv · now 817
- merged 16 row(s) into l1/FIGURES.csv · now 189
- merged 41 row(s) into l1/FORMULAE.csv · now 390
- check-paper: PASS · 2026-5532 · 33/33 questions · total 70/70
- validate after merge: 16/16 checks pass
- double-read: 366 values compared, 16 mismatch(es), all settled
  - 2026-5532-Q01 | options | extractor_right | final A) 2*n*pi | B) 2*n*pi + pi/4 | C) 2*n*pi + pi/2 | D) 2*n*pi + pi | crop /home/claude/render/2026-5532/adj-1/p5.png | crop: (A) 2n pi (B) 2n pi + pi/4 (C) 2n pi + pi/2 (D) 2n pi + pi; part file writes the same in P6.3 ASCII; checker kept the printed symbols; no value differs
  - 2026-5532-Q08 | options | extractor_right | final A) +5 V (left), +10 V (right) | B) -1.0 V (left), -1.5 V (right) | C) 0 V (left), 1 V (right) | D) -2 V (left), 0 V (right) | crop /home/claude/render/2026-5532/adj-2/p7.png | crop: all four diodes point right (anode on the left): A +5 V / +10 V, B -1.0 V / -1.5 V, C 0 V / 1 V, D -2 V / 0 V; same values; part file names the ends left/right, checker anode/cathode
  - 2026-5532-Q09 | options | extractor_right | final A) 200 ohm | B) 175 ohm | C) 100 ohm | D) 125 ohm | crop /home/claude/render/2026-5532/adj-3/p7.png | crop: 200, 175, 100, 125 ohm; ohm is the P6.3 spelling of the printed omega; no value differs
  - 2026-5532-Q10 | options | extractor_right | final A) 2.0e8 m s^-1 | B) 4.5e7 m s^-1 | C) 3.5e7 m s^-1 | D) 2.5e8 m s^-1 | crop /home/claude/render/2026-5532/adj-4/p9.png | crop: 2.0 x 10^8, 4.5 x 10^7, 3.5 x 10^7, 2.5 x 10^8 m s^-1; part file uses e-notation (P6.3) as the origin row does; no value differs
  - 2026-5532-Q12 | options | extractor_right | final A) R/(mu - 1) | B) -R/(mu - 1) | C) 2R/(mu - 1) | D) -2R/(mu - 1) | crop /home/claude/render/2026-5532/adj-5/p9.png | crops adj-5 (A, B) and adj-5b (C, D): R/(mu - 1), -R/(mu - 1), 2R/(mu - 1), -2R/(mu - 1); mu is the P6.3 spelling; no value differs
  - 2026-5532-Q19A | marks_part | extractor_right | final  | crop /home/claude/render/2026-5532/adj-6/p13.png | crop: the 2 beside (a) is side (a)'s total, equal to q_marks_printed 2; B00-B01 leave marks_part blank on every single-row side (e.g. 2026-5531-Q17A, 2026-5511-Q18A), so blank stands
  - 2026-5532-Q24B-i | numbers | extractor_right | final (b) An alpha particle (mass 6.4e-27 kg and charge 3.2e-19 C) having 8.0 MeV energy, enters a region of a uniform magnetic field of 0.5 T. If the field is directed perpendicular to the velocity of the particle, find the radius of the circular path described by the particle. Mention the condition under which the particle in this region (i) describes a helical path | crop /home/claude/render/2026-5532/adj-7/p15.png | crop: 6.4 x 10^-27 kg, 3.2 x 10^-19 C, 8.0 MeV, 0.5 T are printed once, in the (b) lead-in shared by d1, (i) and (ii); the stem carries that lead-in as the origin row does, the checker listed the values on d1 only; no value differs
  - 2026-5532-Q24B-ii | numbers | extractor_right | final (b) An alpha particle (mass 6.4e-27 kg and charge 3.2e-19 C) having 8.0 MeV energy, enters a region of a uniform magnetic field of 0.5 T. If the field is directed perpendicular to the velocity of the particle, find the radius of the circular path described by the particle. Mention the condition under which the particle in this region ... (ii) goes straight undeviated. | crop /home/claude/render/2026-5532/adj-8/p15.png | crop: as for Q24B-i: the values belong to the shared (b) lead-in; the checker listed them on d1 only; no value differs
  - 2026-5532-Q29-ii | options | extractor_right | final A) 1/sqrt(2) | B) sqrt(2) | C) 1/2 | D) 2 | crop /home/claude/render/2026-5532/adj-9/p17.png | crop: 1/sqrt2, sqrt2, 1/2, 2; sqrt() is the P6.3 spelling; no value differs
  - 2026-5532-Q29B-iv | options | extractor_right | final A) p_1 = p_2/2 | B) p_1 = p_2 | C) p_1 = 2*p_2 | D) p_1 = 4*p_2 | crop /home/claude/render/2026-5532/adj-10/p19.png | crop: p_1 = p_2/2, p_1 = p_2, p_1 = 2p_2, p_1 = 4p_2; the part file writes the product as 2*p_2 (P6.3 plain maths); no value differs
  - 2026-5532-Q30-i | options | extractor_right | final A) 6 microF | B) 3 microF | C) 9 microF | D) 2 microF | crop /home/claude/render/2026-5532/adj-11/p21.png | crop: 6, 3, 9, 2 microfarad; microF as in the origin row; no value differs
  - 2026-5532-Q30A-iv | options | extractor_right | final A) 6 microC | B) 4 microC | C) 12 microC | D) 8 microC | crop /home/claude/render/2026-5532/adj-12/p21.png | crop: 6, 4, 12, 8 microcoulomb; microC as in the origin row; no value differs
  - 2026-5532-Q33A-ii | numbers | extractor_right | final (a) (ii) Two point charges - 2 microC and 5 microC are placed at (- 30 cm, 0) and (30 cm, 0) respectively in an external electric field vec(E) = (A/x^2) i^, where A = 9e5 N m^2 C^-1. Find the electrostatic potential energy of this configuration. | crop /home/claude/render/2026-5532/adj-13/p27.png | crop: the page prints '- 2 microC' and '(- 30 cm, 0)' with a space after the minus; the stem keeps the printed spacing and the givens carry -2 and -30; both readings are -2 microC; no value differs
  - 2026-5532-Q33B-ii-I-1 | numbers | extractor_right | final (ii) A small hollow conducting sphere of radius r_1 is given a charge Q. It is surrounded by a concentric conducting spherical shell of inner radius r_2 and outer radius r_3, having charge -3q. If a point charge 2q were kept at the centre, find : (I) the electric flux through a concentric spherical Gaussian surface of radius x for (1) x < r_1 | crop /home/claude/render/2026-5532/adj-14/p27.png | crop: the extra 1 is the printed sub-label (1) in 'for (1) x < r_1'; -3q and 2q agree; the sphere's charge is printed as capital Q
  - 2026-5532-Q33B-ii-II-1 | numbers | extractor_right | final (ii) A small hollow conducting sphere of radius r_1 is given a charge Q. It is surrounded by a concentric conducting spherical shell of inner radius r_2 and outer radius r_3, having charge -3q. If a point charge 2q were kept at the centre, find : (II) electric field at a point distant x from the centre for (1) x > r_3 | crop /home/claude/render/2026-5532/adj-15/p27.png | crop: the extra 1 is the printed sub-label (1) in 'for (1) x > r_3'; -3q and 2q agree
  - 2026-5532-Q33B-ii-III-1 | numbers | extractor_right | final (ii) A small hollow conducting sphere of radius r_1 is given a charge Q. It is surrounded by a concentric conducting spherical shell of inner radius r_2 and outer radius r_3, having charge -3q. If a point charge 2q were kept at the centre, find : (III) surface charge density on the inner surface of (1) sphere | crop /home/claude/render/2026-5532/adj-16/p27.png | crop: the extra 1 is the printed sub-label (1) in 'of (1) sphere'; -3q and 2q agree
- status erratum ER-B02-079: NEW -> IN-PROGRESS
- PROGRESS: line updated (2026-5533, 2026-55B still to do)
- pack: PHY-VAULT-B02-20261001-0900-2319r.json
