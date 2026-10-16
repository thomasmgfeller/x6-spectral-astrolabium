# Lorentzian priority: reference, comparison and research gates

Research baseline: 11 October 2026; navigation/window reconciled 15 October 2026.
The user's priority is Lorentzian spectral
geometry. Both Lorentzian tracks run first; the three existing signal/graph
controls follow with 24 cases each. The authorised exclusive cutoff is
19 October 2026 at 00:00:00 Europe/Zurich (`2026-10-18T22:00:00Z`), including
Sunday 18 October. See `MATH_AGENT.md` for control and the
[central module register](MODULE_REGISTRY.md) for source pins and evidence.

This page describes the scheduled main-branch n=3..5/propagator baseline.
The full n=6 atlas generator remains on `research/lorentz-v1-workpackages`.
The byte-identical independent verifier and fixed atlas are also available in
main through the [offline reference suite](OFFLINE_REFERENCE.md), with exact
source provenance. Fingerprints, Fabric and Neutral Discovery
have later branch sources. Their exact entry points, finite results and next
acceptance gates are in the register. They are not automatically part of this
scheduled agent or evidence of a general reconstruction theorem.

## Research reference and exact replication

Yazdi, Letizia and Kempf, *Lorentzian Spectral Geometry with Causal Sets*,
CQG 38 (2021), [preprint v1](https://arxiv.org/abs/2008.02291v1), studied
orders up to nine elements. Tables 1–2 give our small-order targets. Additional
invariants and quill perturbations improve discrimination; finite enumerations
do not settle reconstruction for arbitrary orders.

Our first track independently enumerates binary upper-triangle relations on
3–5 elements, retains transitively closed relations, and identifies isomorphic
orders by all permutations. Every finite order has a natural labeling, so this
covers these sizes. Reverse orders remain distinct unless isomorphic. This
is not a replication of the full nine-element study.

For `C_ij = 1` iff i precedes j, we use `S=C+C.T`, `A=C-C.T`, `K=SA-AS`.
These are fixed nonzero multiples of the self-adjoint part, anti-self-adjoint
part, and their commutator. Scaling preserves equality classes of spectra.
We classify tuples of characteristic polynomials using arbitrary-precision
integer Faddeev–LeVerrier with exact division. No tolerance or eigenvalue
rounding decides a collision. A has imaginary eigenvalues; multiplying it
by i would yield equivalent classification.

| Elements | Nonisomorphic orders | Classes from three spectra | Classes adding ordered minimal/maximal counts |
|---|---:|---:|---:|
| 3 | 5 | 4 | 5 |
| 4 | 16 | 14 | 16 |
| 5 | 63 | 53 | 63 |

These literature expectations are not newly discovered numbers. A mismatch
fails the run. Every representative, polynomial, relabeling check and unresolved
group is retained in `lorentz_orders.json`. Opposite three-element forks
illustrate lost time orientation. Minimal/maximal counts form an ordered pair.

## Two sequences against a known Lorentzian operator

Jones and Yazdi, *Spectral Density of the Causal Propagator*,
[arXiv:2606.00311v3](https://arxiv.org/html/2606.00311v3), revised 29 September
2026, propose an asymptotic spectral-density conjecture with supporting
examples. It remains a conjecture. We use the established massless 1+1
Minkowski diamond example in equations 11–14 for calibration.

Uniform null coordinates u,v in [-1,1] give a diamond of volume V=4.
Sampling is conditional on fixed N, not an unconditioned Poisson count.
Causality requires both coordinates to increase. In the paper's convention:

```
Delta_c = (C.T - C)/2
H = i Delta_c V/N
```

V/N supplies the integration measure. The continuum positive eigenvalues
combine `1/(n*pi)` for positive integers n and `1/z` for positive nonzero
roots of `tan(z)=2z`. Bisection stays between tangent poles and excludes zero.
Both mode families are included in the sorted analytic reference.

The comparison protocol is fixed before the comparison sequence:

- Sizes 64 and 128, three independent samples per size and sequence.
- Reference seed base 20260805, reused identically each slot.
- Comparison seed base changes with the recorded slot. Samples are independent
  of the reference and not nested across sizes.
- Metric: relative L2 error of the largest eight positive eigenvalues against
  the analytic values. Also report distance between sequence mean spectra and
  each individual error, with no selective seed/rank removal.
- Hermiticity, plus/minus pairing and relabeling checks use absolute tolerance
  1e-10. They test implementation, not physical Lorentz invariance.
- Archive coordinates, seeds, normalization and every positive eigenvalue in
  `lorentz_propagator.json`, separately from the exact polynomial track.

The frozen sample is a reproducibility reference; the analytic spectrum is
the comparison target. Neither sequence is an empirical spacetime dataset.
Three replicates cannot justify a reliable uncertainty model, p-value or
general convergence rate. Errors need not fall on every increase of N. We do
not fit an exponent or test the general 2026 conjecture at these sizes. Small
eigenvalues near the discreteness scale require a justified cutoff later.

## Priorities and evidence gates

| Priority | Work | Completion criterion |
|---|---|---|
| 1, implemented | Exact n=3..5 replication and two finite-diamond sequences | Literature counts match; complete artifacts and numerical checks |
| 2, next | Larger collision corpus and quill-response invariants | Independently checked isomorphism; explicit unresolved pairs; comparison to 2021 method |
| 3 | Finite-size study of the 1+1 propagator | Preregistered sizes/ranks, more seeds, justified cutoff, uncertainty estimates and compute budget |
| 4 | Restricted stability or identifiability theorem | Explicit assumptions, proof, counterexamples and novelty review |
| 5 | Other geometries or dimensions | Correct dimension-dependent Green function, volume measure and independent controls |
| Supporting | Held-out denoising benchmark and source agents | Untouched test sequences, clean targets or defensible proxies, fair comparator tuning |

For the main scheduled baseline, items 2–5 and the full denoising comparison
remain outside its executed scope. Item 2 now has a finite n=6 branch result
as recorded above; larger/general reconstruction questions remain open. Good finite
tests do not automatically extend the runtime window or establish a physical
interpretation. A useful near-term output is an independently checkable
benchmark and negative-result corpus. New mathematics requires a proved
statement and separate literature/expert review.

## Forecast revision

Earlier probability ranges in `MATH_FORECAST_2026_10.md` concern a finite-signal
and undirected-graph program. They are retained as historical judgments and
must not be relabeled as probabilities for Lorentzian discovery. There is no
calibrated success estimate here. Known-case replication is directly testable;
a general reconstruction theorem or Lorentzian Weyl analogue is a much larger
research goal.

The scheduled review reads evidence and primary literature, explains changes
and proposes the next falsifiable question. It cannot promote a conjecture to
a theorem, self-modify code or extend the pilot.

## Fortsetzung: vier Restpaare bei n=6

Die [exakte Restpaaranalyse](../research/lorentz_n6_residuals/README.md) ist in main
ausführbar und Teil der gemeinsamen Offline-Suite. Alle vier Paare sind getrennt;
drei sind Zeitumkehrpaare. Der Bericht enthält die neue Wolfram-Gegenprüfung,
n=7/n=8-Gegenbeispiele und die damals offene Hypothese
H7-bidirectional-moments für n=7 mit Höhe ≥3. Die ursprünglichen Agentenläufe
n=3–5 bleiben historische Replikationsevidenz.


## Fortschreibung 16.10.2026: H7 vollständig geprüft und widerlegt

Die [vollständige n=7-Studie](../research/lorentz_n7_complete/README.md) erfasst
alle 2.045 Ordnungen. F0 und beide gerichteten Gabelzählungen ergeben nur 2.043
Klassen: Zwei nichtisomorphe Paare der Höhe drei bleiben. Beide sind vollständig
als [Gegenbeispiele](../research/lorentz_n7_complete/COUNTEREXAMPLES.md) dokumentiert.
Die Gegenprüfung verwendet einen getrennten Enumerator und exakte Algebra.
H7 ist damit widerlegt; ein stärkeres Gradmultiset ersetzt diesen Test nicht.
Der nächste sinnvolle Schritt ist die strukturelle Analyse dieser minimalen
Kollisionen sowie eine externe Replikation. Keine physische Validierung.


## Abhängigkeitsprüfung vom 16.10.2026

Die [H7-Abhängigkeitsprüfung](../research/lorentz_h7_dependency_audit/README.md) umfasst alle 39 registrierten Module. Keine konkrete laufende H7-Eindeutigkeitsabhängigkeit wurde gefunden. Historische Teilbefunde bleiben begrenzt gültig; Rekonstruktion und Historienreduktion benötigen eigene Identitäts- und Informationsverlustprüfungen. Unzugängliche Quellen werden nicht entlastet.


## Strukturelle Erklärung vom 16.10.2026

Die [nachträgliche Strukturanalyse](../research/lorentz_h7_structure/README.md) liefert exakte Switching-Zertifikate für beide n=7-Paare, einen Beweis zusammenhängender H7-Kollisionen für jedes n≥8 und eine begrenzte Ununterscheidbarkeitsaussage für Matrixpolynom-Spektren. Historische Verträge und Resultate bleiben unverändert; zusätzliche Grad- oder Motivmerkmale werden nicht als universelle Identifikatoren behauptet.


## Nachfolgender Merkmalsvergleich vom 16.10.2026

Der [vorab festgelegte Vergleich](../research/lorentz_observable_comparison/README.md) prüft D, M11, N1 und Q1 im vollständigen n≤7-Korpus, an sechs bekannten Kontrollpaaren und einer festgelegten kleinen n=8/9-Stichprobe. N1 und Q1 bestehen das begrenzte Trennkriterium; N1 liegt nach der festgelegten Kostenregel vorne. Die Stichprobe besitzt keine H7-Kollision und belegt keine zusätzliche Trennwirkung. Alle Identitätsentscheidungen benötigen weiterhin vollständige Relationen.

## Belastungstest gleicher N1-Profile vom 16.10.2026

Der [anschließende Belastungstest](../research/lorentz_n1_stress/README.md) umfasst 352 feste Erzeugungen und 207 verschiedene Ordnungen mit 12 bis 20 Elementen. Innerhalb jeder Größe sind die N1-Profile konstruktiv identisch. Unter 25 nichtisomorphen Paaren mit zugleich gleichem H7 trennt Q1 24; ein Paar mit 16 Elementen bleibt unter H7+N1+Q1 ununterscheidbar. Die getrennte exakte Gegenprüfung bestätigt 23.193 Polynome. Sieben der zusätzlichen Trennungen und das Restpaar betreffen auch nach Zeitumkehr nichtisomorphe Ordnungen (nachträgliche Diagnose). Vertrag und Code wurden vorab lokal eingefroren; die blockierte öffentliche Vorabveröffentlichung ist als Abweichung dokumentiert. Die vollständige gerichtete Relation bleibt verbindliche Referenz.

## Diagnose des Restpaars vom 16.10.2026

Die [festgelegte Diagnose](../research/lorentz_residual_diagnosis/README.md) zeigt: Weitere reine Knoten-Farbrunden bleiben für diese reguläre Familie beweisbar uninformativ. Die Zweier- und Dreier-Schnittprofile I2/I3 trennen das Restpaar ebenfalls nicht; gerichtete Paarverfeinerung R2 trennt es in Runde 2 und alle 6.849 größeninternen Paare der 207 vorhandenen Ordnungen. Ein nachträglich aufgeschlüsseltes Relationszertifikat erklärt die Trennung durch ein gemeinsames Nachbarschaftsmuster mit Häufigkeit null beziehungsweise zwei. Vertrag und Ausführungsquellen wurden vor der neuen Merkmalsauswertung veröffentlicht; bekannte Matrizen und Ergebnisse machen die Untersuchung dennoch zu einer nachträglichen Diagnose, keinem unabhängigen Test. Unbekannte Größen und Familien sowie gezielte R2-Gegenbeispiele sind die nächste getrennte Abnahme.

## Familientransfer und gemeinsames Gegenbeispiel vom 16.10.2026

Der [vorab öffentlich festgelegte Transfer](../research/lorentz_relational_transfer/README.md) umfasst 72 neue Ziehungen aus regulären, nichtregulär angelegten und dreischichtigen Generatoren sowie zwei separat ausgewiesene Strukturkontrollen. Alle Quellen wurden vor der Zielerzeugung veröffentlicht. Die 72 Ziehungen ergeben 71 Isomorphieklassen und 539 nichtisomorphe größeninterne Ziehungspaare; Q1 und R2 trennen sie jeweils vollständig. Da H7+N1+Q1 bereits kein Stichprobenpaar offenlässt, belegt diese Stichprobe keinen Zusatznutzen von R2 gegenüber dieser Kombination.

Die beiden geschlossenen Nachbarschaftsordnungen der Rook-/Shrikhande-Kontrollen besitzen jeweils 32 Elemente und bleiben unter **H7+N1+Q1+R2** gleich. Ein [vollständiges Vierer-Schnittzertifikat](../research/lorentz_relational_transfer/COUNTEREXAMPLE.md) beweist ihre Nichtisomorphie; eine nachträgliche algebraische Erklärung zeigt, warum weitere R2-Runden nicht helfen. Beide Ordnungen sind selbstdual. Die getrennte Prüfung bestätigt alle 541 Paarentscheidungen und 6.294 charakteristischen Polynome je Rechenweg. Der Erfolg am vorherigen Restpaar bleibt bestehen, aber das kombinierte Merkmalsbündel ist kein universeller Identifikator. Nächste offene Arbeit ist ein eingeschränkter Rekonstruktionssatz oder ein neu festzulegender Vergleich stärkerer relationaler Informationen, einschließlich dieser Gegenbeispiele als bekannter Kontrollen.

## Informationsverlust und eingeschränkte Rekonstruktion vom 16.10.2026

Die [festgelegte Folgestudie](../research/lorentz_relational_boundary/README.md) umfasst 217 Ordnungen und alle 7.088 größeninternen Paare. Das bekannte 32er-Paar wird bereits durch dritte Schnittordnung getrennt; R2 zusammen mit den vollständigen Schnitt-Histogrammen trennt den gesamten festen Korpus. Das ist keine allgemeine Eindeutigkeitsgarantie. Alle Schnittordnungen zusammen lassen allein 886 Paare offen, darunter das zusammenhängende ursprüngliche 16er-Restpaar.

Zwei [präzise Aussagen](../research/lorentz_relational_boundary/PROOFS.md) begrenzen das Ergebnis: Für jede gerade Elementzahl ab zwölf existieren verschiedene Zweischichtenordnungen mit identischen Histogrammen aller Schnittordnungen in beiden Richtungen. Bleibt hingegen die Zuordnung jeder Schnittzahl zu ihrer beschrifteten Teilmenge erhalten, rekonstruiert klassische Möbius-Inversion bei bekannter Gradschranke die Spaltennachbarschaften vollständig. Alle 434 Richtungsrekonstruktionen sind exakt gegengeprüft. Die Zeilen-Zuordnung bleibt eine Isomorphieaufgabe; die Darstellung ist nicht generell kompakt und der Satz gilt nicht für beliebige höhere Schichten. 744 neue Polynome je Rechenweg wurden geprüft; 209 frühere H7/N1/Q1-Datensätze wurden ausdrücklich als hashgebundene Referenz übernommen. Bekannte Daten und theoriegeleitete Kontrollen begründen keine blinde Validierung.


## Knoten-Zuordnung, drei Schichten und Geometriepilot — 16. Oktober 2026

Die [Folgestudie](../research/lorentz_matching_geometry/README.md) liefert einen exakten Vergleich der aus indizierten Schnittdaten rekonstruierten Matrizen samt vollständigen Knotenbijektionen. 7.088 vorhandene Paarreferenzen stimmen überein; 651 frei umnummerierte Kopien werden korrekt wiedererkannt. Automorphismen können mehrere gültige Bijektionen erlauben; es wird keine kanonische Nummerierung behauptet.

Ein [Sechsknoten-Gegenbeispiel und ein begrenzter Satz](../research/lorentz_matching_geometry/PROOFS.md) klären die Dreischicht-Frage: unabhängig passende Nachbarbeziehungen reichen nicht. Gemeinsam indizierte Vorgänger-/Nachfolgernachbarschaften der mittleren Knoten rekonstruieren dagegen die ganze Ordnung bei festen äußeren Labels und ohne zusätzliche direkte untere–obere Verbindungen.

Der prospektive synthetische Pilot umfasst 720 Ordnungen in vier Erzeugerfamilien bei N=16,36,64. Im vorab festgelegten Hauptvergleich bei N=64 erreicht die Standardbasis 69,375 %, die Kombination mit P123 62,5 % gleichgewichtete Testtrefferquote. Die Differenz von −6,875 Prozentpunkten mit bedingtem 95%-Test-Bootstrap-Intervall [−13,75;0,00] erfüllt das Zusatznutzenkriterium nicht. Getestet wird eine definierte Erweiterung der Ein-/Zwei-/Dreifach-Schnittprofile, nicht die frühere Kombination R2+Pall. Die Verwechslung mit gestörten Gittern bleibt deutlich; Geometrieerkennung ist nicht nachgewiesen. Quellenfixierung, Rohdaten, Prüfer und netzisolierter CI-Reproduktionsweg sind veröffentlicht. Externe Replikation steht aus.


## Exakter Abgleich von Relationsdichte und Höhe — 16. Oktober 2026

Die [Kontrollstudie nach PR #40](../research/lorentz_matched_controls/README.md) erzeugt 24.576 neue Kandidaten und paart Minkowski-Ordnungen mit Kontrollen bei exakt gleichem N, R und H. Von neun Größen-/Kontrollzellen erreichen fünf die vorab verlangten 64 Trainings- und 128 Testpaare. Die Dreischichtkontrollen und das Gitter bei N=64 bleiben wegen unzureichender gemeinsamer Unterstützung ohne Leistungsbewertung; diese Auswahlgrenze wird nicht als Merkmalserfolg gewertet.

Die reine Dichte-/Höhenkontrolle liegt in allen fünf auswertbaren Zellen exakt bei 50 %. Im primären binären Vergleich Minkowski gegen gestörtes Gitter bei N=64 erreicht die Basis 54,296875 %, B+P123 50,390625 %. Der Zusatz von −3,90625 Prozentpunkten mit bedingtem 95%-Paar-Bootstrap-Intervall [−9,765625;+1,5625] erfüllt das vorab festgelegte Erfolgskriterium nicht. Unbewegte Gitter bei N=16 und N=36 bleiben beschreibend auch nach Abgleich unterscheidbar; daraus folgt kein Geometriezertifikat. Die Aussagen gelten für die ausgewählte gemeinsame Teilverteilung. Vollständiger Kandidatenledger, Auswahl, 1.879 verschiedene verwendete Ordnungen und 5.120 separat bestätigte Testvorhersagen sind veröffentlicht. Frühere Rechenquellen und Daten bleiben unverändert; externe Replikation steht aus.

## Konkrete geometrische Zielgröße: normierte Eigenzeit — 16. Oktober 2026

Die [Zieldefinition mit Prüfvertrag](../research/lorentz_proper_time/README.md) legt theta=tau(p,q)/T zwischen zwei markierten Ereignissen im bekannten flachen 1+1-Modell fest. Dieselbe endliche Ordnung kann unterschiedliche theta-Werte tragen; Ziel ist statistische Genauigkeit. Die Intervallpunktzahl K liefert sqrt(K/(N−2)) als Referenz. Ein Skalierungsargument zeigt, dass die innere Ordnung bei festem K im unselektierten uniformen Modell keine zusätzliche Information über theta enthält. Dies gilt nicht allgemein für Außenbeziehungen oder nach globalem Matching.

Der neue Vertrag umfasst 6.912 vorgesehene Ordnungen, Kalibrierung nur auf uniformen Daten, ein vorab bestimmtes Fehlerkriterium und einen getrennten Transfervergleich mit exakt auf N,R,H abgeglichenen gestörten Gittern. **Status: Design und deterministische Kleintests; Ziel-Datenlauf und vollständige Rechenquellenfixierung noch nicht ausgeführt.** Die bisherigen negativen Befunde aus PR #40/#41 bleiben unverändert. Kein Dimensionsergebnis, Kontinuums- oder Mannigfaltigkeitsnachweis wird behauptet.
