# Eigenzeit in 3+1 dimensions

Published 27 October 2026. Conditional flat-space research pilot; known density,
fixed labelled landmarks, and synthetic Poisson counts.

## Latest: sharper bounds and information budgets, v0.4

[Full German report, evidence and limitations](refined_bound_v0_4/README.md).
On 3,840 fresh observations, the refined bound issues 3,146 certificates,
versus 3,142 from v0.3 on the same data. At 16 times the previous expected
outer count, 1,229/1,280 cases are certified and 19/20 geometries pass the
predeclared availability criterion. `fresh_11` remains open; the overall
gate is **HOLD**, and the original-budget gate remains HOLD too.

All ten tested unrestricted-region witness means violate necessary
flat-landmark norm constraints. This identifies conservatism in the region;
it is not a physical impossibility result. Constraining the region by these
exact model conditions is the next research step, not an implemented gain.

```sh
python3 -m pip install -r research/eigenzeit_4d/poisson_v0_2/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 research/eigenzeit_4d/verify_refined_publication.py
```

## Earlier: joint-region certificates, v0.3

[Full follow-up report / vollständiger Folgebericht](joint_region_v0_3/README.md).
A new finite-sample joint region and outward interval arithmetic issue 1,910
10%-proper-time certificates in 2,560 fresh high-density observations;
0/2,560 at the lower density. The old bound issues none on the same data.
All 1,910 certificates replay; no incorrect issued certificate was observed.
The predeclared availability gate across all 20 geometries remains **HOLD**.
For each fixed model parameter, the probability of issuing a wrong certificate
is bounded by 2^30 exp(-24) < 0.040536 per observation, under the stated model.
This is not conditional coverage after selecting certified cases or simultaneous
coverage of the full experiment. Geometries remain the fixed v0.2 set.

```sh
python3 -m pip install -r research/eigenzeit_4d/poisson_v0_2/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 research/eigenzeit_4d/verify_joint_publication.py
```


**Historical v0.2 observed accuracy gate: PASS at the highest tested density. Data-dependent
10% error certification: HOLD.** These are separate decisions. No intrinsic
landmark selection, operator, curvature or general GFEST stability claim.

## Earlier v0.2 results / frühere Ergebnisse

The frozen v0.2 campaign contains 40,960 joint count observations across 20
geometries and four densities. At the primary density (268,435,456 expected
background events in the outer interval), 10,239/10,240 trials satisfy all
predeclared guards and have at most 10% proper-time error. Each geometry
passes its simultaneous one-sided success-probability gate. **Zero trials
produce a 10% data-dependent error certificate.**

The joint law is sampled through exact disjoint chain regions, preserving
overlap correlations without generating every background point. Separately,
1,024 directly sprinkled clouds contain 4,193,689 points. All count vectors
and direct clouds replay; 160 cases were cross-checked by a separate
80-decimal-digit elimination. These are internal checks, not external review.

Die Ergebnisse sind Simulationen mit vorgegebenen Landmarken und bekannter
Dichte. Der Genauigkeits-Pilot besteht bei hoher Dichte; die aus den Daten
abgeleitete 10%-Fehlergarantie bleibt offen. Die bestehenden 38 HOLD-Zellen
aus PR #122 und die GFEST-Aussagen werden nicht verändert.

- [Vollständiger Bericht / full German report](poisson_v0_2/README.md)
- [Mathematische Herleitung / mathematical derivation](poisson_v0_2/THEORY.md)
- [Alle Resultate / all results](poisson_v0_2/RESULTS.json)
- [Replay und Dezimalprüfung / audit](poisson_v0_2/AUDIT.json)
- [Unverändertes Prüfpaket v0.2 / original archive](Eigenzeit_4D_Poisson_v0_2.zip)
- [Exakter geometrischer Einstieg v0.1 / original preflight](Eigenzeit_4D_Start_v0_1.zip)

The two archives are preserved byte for byte from the executed work. The
unpacked `poisson_v0_2/` directory matches the v0.2 archive, including its
original hashes and freeze. A publication verifier works in a temporary
copy and compares regenerated data with the preserved evidence:

```sh
python3 -m pip install -r research/eigenzeit_4d/poisson_v0_2/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 research/eigenzeit_4d/verify_publication.py
```

Original project code and text follow the repository Apache-2.0 license;
external cited publications retain their own terms. The package does not
claim novelty, external peer review or physical spacetime measurements.
