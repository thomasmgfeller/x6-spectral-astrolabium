# Eigenzeit 3+1: gemeinsame Konfidenzregion, v0.3

27. Oktober 2026. **Teilweise 10%-Zertifizierung erreicht; die vorab
festgelegte Freigabe für alle 20 Geometrien bleibt HOLD.**

Die bisherige Schranke aus v0.2 stellte trotz guter beobachteter Genauigkeit
keine 10%-Zertifikate aus. Dieser Folgeschritt erhält die Korrelationen der
Intervallzählungen bei der Fehlerfortpflanzung. Auf 5.120 neuen Zählvektoren
liefert er 1.910 mit gerichteter Rundung geprüfte Zertifikate. Alle entstehen
bei der höheren der beiden untersuchten Dichten.

## Ergebnis des eingefrorenen Versuchs

| Erwartete Hintergrundpunkte im äußeren Intervall | Neue Zählvektoren | Neue 10%-Zertifikate | Bisherige Schranke auf denselben Daten |
| --- | ---: | ---: | ---: |
| 16.777.216 | 2.560 | 0 | 0 |
| 268.435.456 | 2.560 | 1.910 (74,61 %) | 0 |

Die 20 Geometrien stammen unverändert aus v0.2: vier Grundgeometrien und
16 dort bereits festgelegte rationale Variationen. Neu sind die unabhängigen
Zählziehungen, jeweils 128 pro Geometrie und Dichte. Die Bezeichnungen
`fresh_00` bis `fresh_15` sind übernommene Namen; sie bezeichnen hier **keine
neu gezogenen Geometrien**. Protokoll und Kernquellen wurden vor den neuen
Zählziehungen gehasht; der lokale Freeze ist keine externe Präregistrierung.

Bei hoher Dichte ergeben sich für die Familien 0, 1, 2 und 3 jeweils
640/640, 640/640, 630/640 und 0/640 Zertifikate. Insgesamt bestehen 14 der
20 Geometrien das Verfügbarkeitskriterium: simultane einseitige
Clopper-Pearson-Untergrenze mindestens 90 %, mit Bonferroni-Korrektur
0,05/20. `fresh_06` erreicht 118/128 Zertifikate, aber nur eine Untergrenze
von 83,20 %. Die fünf Geometrien der Familie 3 stellen kein Zertifikat aus.
Deshalb besteht das globale, vorab festgelegte Kriterium nicht.

Keines der 1.910 ausgestellten Zertifikate widerspricht dem bekannten
Simulationsziel. Diese Beobachtung ersetzt keine statistische Garantie.

## Was das Zertifikat aussagt

Aus den 20 beobachteten Intervallzählungen werden invertierbar 20 unabhängige
Poisson-Zellzählungen gewonnen. Die zurückgehaltene Zählung zwischen den
Zielpunkten wird dafür nicht benötigt. Eine gemeinsame Likelihood-Region
hat die hergeleitete endliche Nichtabdeckungsgrenze

```text
P(wahrer Mittelwert außerhalb der Region) <= 2^30 exp(-24) < 0,040536.
```

Eine deterministische Fehlerfortpflanzung über eine umschließende Ellipse
(in 20 Dimensionen: ein Ellipsoid) erfasst lineare Korrelationen, den
Quadratwurzelrest und einen exakten inversen Matrixrest. Gerichtete
Dezimal-Intervallrechnung prüft anschließend, ob der relative Eigenzeitfehler
über die gesamte Region höchstens 10 % beträgt. Herleitung und Annahmen
stehen in [THEORY.md](THEORY.md).

Für jeden festen zulässigen Modellparameter beträgt damit die
**unbedingte Wahrscheinlichkeit, ein falsches Zertifikat auszustellen,
höchstens 4,054 % pro Beobachtung**. Das ist weder dieselbe Fehlerquote
bedingt auf die Auswahl zertifizierter Beobachtungen noch eine simultane
95%-Garantie für sämtliche 5.120 Versuche. Nicht zertifizierte Fälle bleiben
HOLD; daraus folgt nicht, dass ihre Punktschätzung falsch ist.

## Geltungsbereich und Prüfung

Vorausgesetzt werden flache 3+1-Minkowski-Geometrie, bekannte Intensität,
extern festgelegte und beschriftete zeitartig geordnete Landmarken sowie
fünf affin unabhängige Anker. Intrinsische Landmarkenwahl, beliebige
kausale Mengen, Krümmung und Operatorrekonstruktion sind nicht qualifiziert.
Die bestehenden GFEST-Aussagen und 38 HOLD-Zellen aus PR #122 bleiben bestehen.

- 2.207 algebraische und arithmetische Kontrollen bestanden.
- Alle 5.120 neuen Zählvektoren exakt aus dem Seed reproduziert.
- Alle 1.910 Zertifikate mit 60 signifikanten Dezimalstellen neu berechnet.
- 30 ausgewählte Zertifikate zusätzlich mit 90 Stellen geprüft.
- 40 Maskierungsprüfungen für die unbenutzte Zielzählung bestanden.
- 15.360 zusätzliche Randrichtungen des Ellipsoids ohne Verletzung geprüft.
  Dies ist ein Stresstest, kein Ersatz für die analytische Einschließung.

Diese Prüfungen sind intern. Unabhängige fachliche Begutachtung und formale
Verifikation durch einen Beweisassistenten liegen nicht vor.

## Dateien und Reproduktion

- [PROTOCOL.json](PROTOCOL.json), [FREEZE.json](FREEZE.json): vor den Ziehungen festgelegte Methode und Kernquellen.
- [RESULTS.json](RESULTS.json): alle 40 Geometrie-Dichte-Zellen, einschließlich Fehlschlägen.
- [CERTIFICATES.json](CERTIFICATES.json): sämtliche ausgestellten Intervallzertifikate.
- [fresh_counts.npz](fresh_counts.npz): Zählungen und Diagnostik aller Versuche.
- [AUDIT.json](AUDIT.json): vollständige Nachprüfung.
- [joint.py](joint.py), [intervals.py](intervals.py): Schranke und gerichtete Arithmetik.
- [run.py](run.py), [audit.py](audit.py), [controls.py](controls.py): Versuch und Kontrollen.

Aus dem Repository-Hauptverzeichnis, Python 3.12:

```sh
python3 -m pip install -r research/eigenzeit_4d/poisson_v0_2/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/eigenzeit_4d/verify_joint_publication.py
```

Der Prüfer arbeitet in einer temporären Kopie, wiederholt den gesamten
Versuch und Audit und vergleicht die Resultate mit den veröffentlichten
Daten. Originale Freeze- und Ergebnisdateien bleiben erhalten. README,
Audit und Publikationsprüfer wurden nach dem Versuch hinzugefügt; sie
gehören nicht zum vorab eingefrorenen Methodenkern.

## Nächste offene Forschungsstufe

1. Die konservativen Restterme für Familie 3 und `fresh_06` getrennt
   diagnostizieren; eine schärfere Schranke an einem neuen Versuch prüfen.
2. Anschließend neue Geometrien mit größerer Variation und geringere
   Dichten vorab festlegen; die bisherigen 20 Geometrien reichen für
   geometrische Generalisierung nicht aus.
3. Intrinsische Landmarkenwahl als eigenes Selektionsproblem behandeln,
   bevor die bedingte Aussage auf unbekannte kausale Mengen übertragen wird.

Code und eigener Text stehen unter der Apache-2.0-Lizenz des Repositorys.
Es wird kein Neuheitsanspruch erhoben.
