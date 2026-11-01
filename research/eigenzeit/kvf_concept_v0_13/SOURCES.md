# Quellen und Aussagegrenzen

Recherchegrundlage des Entwurfs vom 1. November 2026. Die Dokumente wurden
über die offiziellen Herausgeberseiten beziehungsweise arXiv geprüft.
Dieser Ordner enthält eigene Zusammenfassungen; Abbildungen und fremde
Volltexte werden nicht mitveröffentlicht.

## Metrologie

- **G1 · JCGM 100:2008**, *Evaluation of measurement data — Guide to the
  expression of uncertainty in measurement*.
  [BIPM-PDF](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf).
  Abschnitt 8 gibt die Arbeitsschritte vor; Abschnitte 4 bis 7 behandeln
  Eingangsgrößen, Unsicherheitsfortpflanzung und Ergebnisangabe.
- **G2 · JCGM 100:2008/Amd.1:2026**, *Nonlinearity in measurement models*.
  [Offizieller DOI](https://doi.org/10.59161/PPDI3267).
  Ergänzt insbesondere den Umgang mit nichtlinearen Messmodellen.
- **G3 · JCGM 102:2011**, *Supplement 2 — Extension to any number of output
  quantities*.
  [BIPM-PDF](https://www.bipm.org/documents/20126/2071204/JCGM_102_2011_E.pdf).
  Abschnitt 6.2.1, Gleichung (3), beschreibt die Kovarianzfortpflanzung;
  Abschnitt 6.5 behandelt Überdeckungsbereiche; Abschnitt 7 behandelt die
  Fortpflanzung von Verteilungen.
- **G4 · JCGM 101:2008**, *Supplement 1 — Propagation of distributions using
  a Monte Carlo method*.
  [Offizieller DOI](https://doi.org/10.59161/JCGM101-2008).
  Ergänzende Grundlage der Monte-Carlo-Methode; für den gemeinsamen
  Vektorausgang wird G3 herangezogen.
- **G5 · JCGM 106:2012**, *The role of measurement uncertainty in conformity
  assessment*.
  [BIPM-PDF](https://www.bipm.org/documents/20126/2071204/JCGM_106_2012_E.pdf).
  Relevant für die zusätzliche Bewertung von Entscheidungsrisiken.

Die [aktuelle JCGM-Publikationsliste des BIPM](https://www.bipm.org/en/committees/jc/jcgm/publications)
führt diese Dokumente einschließlich der Ergänzung 2026. Keine dieser
Quellen bescheinigt unserem Aufbau eine erreichte Messunsicherheit.

## Quantenfeldmessung

- **Q1 · Settembrini, F. F. et al. (2022)**, *Detection of quantum-vacuum
  field correlations outside the light cone*, Nature Communications 13,
  3383. [DOI](https://doi.org/10.1038/s41467-022-31081-1).
  Experimenteller Bezug für elektrooptisch erfasste Vakuumkorrelationen
  bei kausal getrennten Wechselwirkungen. Solche Korrelationen sind kein
  Nachweis überlichtschneller Kommunikation.
- **Q2 · Herter, A. et al. (2026)**, *Experimentally separating vacuum
  fluctuations from source radiation*, Nature Communications 17, 2863.
  [Veröffentlichte Fassung](https://doi.org/10.1038/s41467-026-69142-4),
  [Preprint von 2025](https://arxiv.org/abs/2502.18208).
  Untersucht getrennte Beiträge zu Pulskorrelationen durch
  phasenempfindliche Detektion. Der veröffentlichte Aufbau verwendet einen
  elektrooptischen ZnTe-Kristall bei 4 K. Die Arbeit motiviert unsere
  Architektur, ohne eine 2-ppm-Spezifikation oder Quantengravitation zu
  bestätigen. Für den Entwurf ist die veröffentlichte Fassung maßgeblich.
- **Q3 · Lindel, F. et al. (2023)**, *Probing vacuum field fluctuations and
  source radiation separately in space and time*, Physical Review Research
  5, 043207. [DOI](https://doi.org/10.1103/PhysRevResearch.5.043207),
  [arXiv](https://arxiv.org/abs/2305.06387).
  Theoretische Grundlage für die Trennung von Korrelation und retardierter
  Antwort, einschließlich der Bedeutung der Operatorordnung.

## Kausalsets und Rekonstruktion

- **T1 · Johnston, S. (2009)**, *Feynman Propagator for a Free Scalar Field
  on a Causal Set*, Physical Review Letters 103, 180401.
  [DOI](https://doi.org/10.1103/PhysRevLett.103.180401),
  [arXiv](https://arxiv.org/abs/0909.0944).
  Konstruktion einer freien skalaren Quantenfeldtheorie mit Vakuumzustand
  auf einem Kausalset. Diese Theorie allein definiert keinen optischen
  Labortransfer.
- **T2 · Surya, S. (2019)**, *The causal set approach to quantum gravity*,
  Living Reviews in Relativity 22, 5.
  [DOI](https://doi.org/10.1007/s41114-019-0023-1).
  Insbesondere Abschnitt 5.2 zur Sorkin-Johnston-Konstruktion und ihren
  Voraussetzungen beziehungsweise Einschränkungen im Kontinuum.
- **T3 · Braun, M. (2025)**, *Spacetime reconstruction by order and number*.
  [arXiv:2507.01907](https://arxiv.org/abs/2507.01907).
  Rekonstruktionsaussage aus den Gesetzen zufälliger Ordnungsdaten im
  angegebenen glatten Rahmen. Daraus folgt keine allgemeine eindeutige
  Rekonstruktion mit Fehlerkontrolle aus einer einzelnen endlichen Wolke.

## Projektbezug

Die unmittelbare Grundlage ist
[Eigenzeit v0.12, PR #175](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/175),
zusammengeführt als
[`a633886`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/a6338862528c88998c432e270eb2c5686b307838).
Die dortigen synthetischen C01-Beispiele und ihre GUM-Bilanz sind keine
KVF-Messdaten. Ihr Feldstatus wird durch diesen Entwurf nicht angehoben.
