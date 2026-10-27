# Eigenzeit 3+1: geometrische Konsistenz in der Zertifizierung, v0.5

27. Oktober 2026. **Der bedingte Primärtest für die 20 festgelegten
Geometrien besteht am bisherigen hohen Budget.** Alle 1.280 Fälle erhalten
ein intern geprüftes 10%-Eigenzeitfehlerzertifikat. Beim ursprünglichen
Budget bleibt das geometrieweise Verfügbarkeitskriterium HOLD.

Die zwei exakten Normbedingungen der Zielpunkte werden nun direkt in
Schätzung und Fehlerabschätzung genutzt. Der Vergleich verwendet 2.560
neue unabhängige Zählvektoren, eine vorab eingefrorene Methode und dieselben
beiden Budgets wie die entsprechenden v0.4-Vergleichsstufen. Das hohe Budget
wurde gegenüber dem bisherigen offenen Fall nicht erhöht.

## Ergebnis des neuen Vergleichs

| Budget | Erwartete äußere Punktzahl | v0.5-Zertifikate | v0.4 auf denselben Daten | Geometrien mit Verfügbarkeits-Untergrenze ≥90 % |
| --- | ---: | ---: | ---: | ---: |
| Ursprünglich | 268.435.456 | 957 / 1.280 | 957 / 1.280 | 14 / 20 |
| Sechzehnfach, primärer Test | 4.294.967.296 | **1.280 / 1.280** | 1.228 / 1.280 | **20 / 20** |

Die zuvor offene Geometrie **`fresh_11` erreicht 64/64 statt 12/64** auf
denselben neuen Daten. Alle 52 zusätzlichen Zertifikate entstehen dort.
Die übrigen 19 Geometrien erreichen am hohen Budget ebenfalls je 64/64.
Die einseitige Clopper-Pearson-Untergrenze beträgt dann rund 91,06 % je
Geometrie, mit Bonferroni-Niveau 0,05/20. Damit besteht das vorab festgelegte
Kriterium von mindestens 90 % für jede der 20 Geometrien.

Beim ursprünglichen Budget bleibt `fresh_06` bei 61/64, während die fünf
Familie-3-Geometrien kein Zertifikat ausstellen. Das dortige Kriterium
bleibt HOLD. Die niedrige Budgetstufe ist ein sekundärer Vergleich;
die primäre Freigabe betrifft ausdrücklich nur das hohe Budget.

Insgesamt wurden **2.237 Zertifikate** der neuen Methode validiert,
gegenüber 2.185 der Vorversion. Alle 2.237 stammen direkt aus der
geometrischen Korrektur; der vorab vorgesehene Rückfall auf v0.4 wurde in
diesem Versuch nicht benötigt. Kein ausgestelltes neues Zertifikat
widersprach dem bekannten Simulationsziel. Diese Beobachtung ersetzt
nicht die statistische Herleitung.

## Wie die geometrische Information genutzt wird

Für jeden der beiden Zielpunkte muss seine aus den fünf Ankerabständen
rekonstruierte Norm mit der direkt gegebenen Norm übereinstimmen. Die
zugehörigen Residuen `r_p` und `r_q` sind daher bei einem zulässigen
Modellmittelwert exakt null. Wir verwenden

```text
F = q + k_p r_p + k_q r_q.
```

Auf der Modellgeometrie gilt F=q. Bei verrauschten Zählungen wird F am
beobachteten Mittelpunkt zur korrigierten Punktschätzung. Die Koeffizienten
werden aus den beobachteten Zählungen vorgeschlagen und als exakte dyadische
Zahlen festgehalten. Wahre Koordinaten, Geometrienamen und der gesuchte
Zielabstand werden dem Zertifizierer nicht übergeben.

Die gemeinsame Poisson-Konfidenzregion bleibt unverändert. Eine vollständige
Fehlerabschätzung für F über diese Region begrenzt zugleich q auf ihrem
geometrisch zulässigen Teil. Quadratwurzelreste und der exakte nichtlineare
Matrix-Inversenrest werden mitgeführt. Jedes positive Zertifikat wird mit
gerichteter Intervallrechnung bei 60 signifikanten Dezimalstellen geprüft.
[THEORY.md](THEORY.md) enthält die Herleitung einschließlich Koeffizientenwahl,
Restterm und Rückfallregel.

Für jeden festen zulässigen Modellparameter bleibt die unbedingte
Wahrscheinlichkeit, ein falsches Zertifikat auszustellen, höchstens
`2^30 exp(-24)`, also rund 4,054 % pro Beobachtung. Das ist keine identische
Garantie bedingt auf die Auswahl zertifizierter Beobachtungen und keine
simultane Garantie für alle Versuche. Die datenabhängige Wahl der
Koeffizienten und der Rückfall verwenden dasselbe Konfidenzereignis.

## Validierung und Grenzen

- 290 Kontrollen bestanden, darunter 60 exakte rationale Matrixidentitäten,
  206 Positivitätsprüfungen des Restterm-Majoranten und 20 Prüfungen an
  exakten Modellmittelwerten.
- Alle 2.560 neuen Zählvektoren exakt aus dem Seed reproduziert.
- Alle 2.237 ausgestellten Zertifikate mit exakten Entscheidungsungleichungen
  und einer separaten Intervallberechnung der korrigierten Punktschätzung geprüft.
- 70 verschiedene Zertifikate zusätzlich mit 90 Dezimalstellen nachgerechnet.
- 17.920 Randrichtungen des Ellipsoids mit festgehaltenen Koeffizienten und
  40 Maskierungsprüfungen der unbenutzten Zielzählung bestanden. Die Randtests
  ergänzen die analytische Einschließung.
- Der Publikationsprüfer wiederholt beide Zertifikatsmethoden, Audit und
  Entwicklungsdiagnostik vollständig in einer temporären Kopie.

Die 20 Geometrien sind die bisherigen festen Geometrien aus v0.2. Namen wie
`fresh_11` sind übernommene Bezeichnungen und kennzeichnen hier keine neu
gezogene Geometrie. Die neue Validierung betrifft neue **Zählungen**.
Eine unabhängige fachliche Begutachtung oder Beweisassistenten-Verifikation
liegt nicht vor; der lokale Freeze ist keine externe Präregistrierung.

Vorausgesetzt bleiben bekannte Dichte, flache 3+1-Minkowski-Geometrie und
extern festgelegte, beschriftete Landmarken. Neue Geometrien, intrinsische
Landmarkenwahl, Krümmung, Operatorrekonstruktion und ein allgemeiner
GFEST-Stabilitätssatz sind nicht freigegeben. Die bestehenden 38 HOLD-Zellen
aus PR #122 werden durch diesen bedingten Eigenzeit-Test nicht geschlossen.

Die Milliardenwerte sind erwartete Punktzahlen im Modell. Die gemeinsame
Zählverteilung wird über 20 unabhängige Zellen erzeugt; vollständige
Milliardenpunkte-Causal-Sets wurden nicht aufgebaut oder zeitlich vermessen.

## Reproduktion und nächste Forschungsstufe

[PROTOCOL.json](PROTOCOL.json), [FREEZE.json](FREEZE.json),
[RESULTS.json](RESULTS.json), [CERTIFICATES.json](CERTIFICATES.json),
[AUDIT.json](AUDIT.json), [fresh_counts.npz](fresh_counts.npz).
[DEVELOPMENT.json](DEVELOPMENT.json) enthält ausschließlich explorative
Kandidaten auf archivierten v0.4-Daten. Das Datenformat beschreibt
[DATA_LAYOUT.json](DATA_LAYOUT.json).

Aus dem Repository-Hauptverzeichnis, Python 3.12:

```sh
python3 -m pip install -r research/eigenzeit_4d/poisson_v0_2/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/eigenzeit_4d/verify_constrained_publication.py
```

Der nächste Generalisierungstest benötigt vorab festgelegte, bisher
unbenutzte Geometrien mit größerer Variation und gezielt schlechter
Ankerkonditionierung. Danach ist die intrinsische Landmarkenwahl mit ihrer
zusätzlichen Selektionsunsicherheit separat zu behandeln. Der Erfolg auf
den bisherigen 20 Geometrien ersetzt diese Schritte nicht.

Code und eigener Text folgen der Apache-2.0-Lizenz des Repositorys.
Es wird kein Neuheitsanspruch erhoben.
