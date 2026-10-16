# Geometrieprüfung mit exakt angepasster Relationsdichte und Höhe

Der vorab festgelegte Hauptvergleich zeigt **erneut keinen nachgewiesenen
Zusatznutzen von P123**. Diesmal stimmen Knotenzahl, Relationszahl und Höhe
innerhalb jedes Vergleichspaars exakt überein. Der ausschließlich aus diesen
Größen gebildete Kontrollklassifikator erreicht in allen auswertbaren Zellen
genau 50 %.

Das begrenzt eine mögliche Erklärung des Ergebnisses: Die noch erkennbare
Gitterstruktur bei N=16 und N=36 lässt sich nicht allein auf Relationsdichte
oder Höhe zurückführen. Eine zuverlässige Trennung von Minkowski-Ziehungen
und gestörten Gittern bei N=64 gelingt mit den getesteten Merkmalen weiterhin
nicht. **Keiner dieser Befunde ist ein Geometrie- oder Mannigfaltigkeitszertifikat.**

## Festgelegter Versuch

Anschluss an [PR #40](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/40).
Die früheren Rechenquellen und Ergebnisse bleiben unverändert.
Der neue [Vertrag](contract.json) und die [Methoden mit mathematischer Begründung](METHODS.md)
legen Auswahl, Fallzahlen, Modell und Hauptkriterium vor der Datenerzeugung fest.

- 24.576 neue Kandidaten: N=16,36,64; vier Erzeugerfamilien; getrennte Trainings-
  und Testpools mit jeweils 1.024 Ziehungen pro Familie und Größe.
- Jede Paarung enthält eine Minkowski-Ordnung und eine Kontrollordnung mit
  **identischem (N,R,H)**. R zählt alle strikten Relationen, H die längste Kette
  in Knoten. Gleiche Relationsdichte folgt bei gleichem N aus gleichem R.
- Die Auswahl verwendet nur diese Größen und eine feste Priorität der IDs.
  Spektren und Schnittprofile werden erst nach gespeicherter Auswahl berechnet.
- Eine Zelle wird nur bei mindestens 64 verfügbaren Trainingspaaren **und**
  128 Testpaaren ausgewertet. Fehlende Unterstützung wird nicht durch weitere
  Ziehungen, größere Toleranzen oder Wiederverwendung derselben Ordnung ersetzt.

Dies ist eine bedingte **binäre** Vergleichsaufgabe mit Zufallsmarke 50 %.
Die Prozentwerte sind deshalb nicht direkt mit der früheren Vierklassenaufgabe
aus PR #40 vergleichbar. Die genaue Auswahl verändert außerdem die
Erzeugerverteilung: Aussagen gelten für die ausgewählte gemeinsame Teilmenge,
nicht für alle möglichen Minkowski-Ordnungen oder Kontrollen.

## Welche Kontrollen tatsächlich vergleichbar waren

Die Zahlen geben alle im festen Pool verfügbaren exakten Paare an, vor der
Begrenzung auf 64 beziehungsweise 128:

| Kontrolle | N | Trainingspaare verfügbar | Testpaare verfügbar | Auswertung |
| --- | ---: | ---: | ---: | --- |
| Dreischicht | 16 | 2 | 1 | Unzureichende gemeinsame Unterstützung |
| Gitter | 16 | 415 | 388 | 64 Training / 128 Test |
| Gestörtes Gitter | 16 | 755 | 803 | 64 Training / 128 Test |
| Dreischicht | 36 | 0 | 0 | Unzureichende gemeinsame Unterstützung |
| Gitter | 36 | 213 | 219 | 64 Training / 128 Test |
| Gestörtes Gitter | 36 | 575 | 580 | 64 Training / 128 Test |
| Dreischicht | 64 | 0 | 0 | Unzureichende gemeinsame Unterstützung |
| Gitter | 64 | 89 | 84 | Test-Mindestzahl nicht erreicht |
| Gestörtes Gitter | 64 | 404 | 424 | 64 Training / 128 Test |

Die bisherigen Dreischichtordnungen haben Höhe höchstens drei. Sie liefern in
diesem Pool deshalb keine hinreichende faire Vergleichsmenge für die gewählten
Minkowski-Ziehungen. Beim Gitter mit N=64 wären 84 Testpaare verfügbar, aber der
vorab festgelegte Mindestwert 128 wird nicht erreicht. Diese vier Zellen bleiben
**ohne Leistungsbewertung**. Fehlender Abgleich ist kein Erfolg eines Merkmals.

In fünf auswertbaren Zellen entstehen 960 Paarverwendungen und 1.920
Beobachtungsverwendungen. Es sind **1.879 verschiedene ausgewählte Ordnungen**,
weil Minkowski-Beobachtungen zwischen verschiedenen Kontrollvergleichen
wiederverwendet werden dürfen. Innerhalb einer Zelle gibt es keine Wiederverwendung
und keine Übernahme aus Training in Test. Die Zellen sind damit keine fünf
statistisch unabhängigen Wiederholungen desselben Versuchs.

## Testergebnisse

Alle Modelle verwenden denselben festgelegten Schwerpunkt-Klassifikator mit
ausschließlich am Training berechneter Standardisierung:

- **D:** nur Relationsdichte und normalisierte Höhe; Fehlerkontrolle.
- **B:** getrennte Linkgradhistogramme, Intervallhäufigkeiten und Eigenwerte des
  kombinatorischen Laplace-Operators des symmetrisierten Hasse-Diagramms.
- **P123:** gemeinsame strikte Vorgänger-/Nachfolgerzahlen aller Ein-, Zwei-
  und Dreiermengen, als Histogramme einschließlich Nullen und Multiplizitäten.
- **B+P123:** unveränderte Kombination aus dem vorigen Versuch.

R2+Pall, H7, N1 und Q1 werden hier nicht getestet. Auch ein anderer Klassifikator
wird nicht nach Betrachtung der Ergebnisse hinzugefügt.

Gleichgewichtete Klassentrefferquote auf jeweils 256 Testordnungen:

| Kontrolle | N | D | B | P123 | B+P123 | Zusatz zur Basis |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Gitter | 16 | 50,00 % | 71,88 % | 60,94 % | 75,39 % | +3,52 Prozentpunkte |
| Gestörtes Gitter | 16 | 50,00 % | 48,05 % | 55,08 % | 51,56 % | +3,52 Prozentpunkte |
| Gitter | 36 | 50,00 % | 96,48 % | 67,58 % | 96,88 % | +0,39 Prozentpunkte |
| Gestörtes Gitter | 36 | 50,00 % | 55,86 % | 55,08 % | 60,55 % | +4,69 Prozentpunkte |
| **Gestörtes Gitter, primär** | **64** | **50,00 %** | **54,30 %** | **45,70 %** | **50,39 %** | **−3,91 Prozentpunkte** |

Der primäre Zusatz beträgt exakt −10/256 = **−3,90625 Prozentpunkte**.
Das 95%-Intervall des Bootstrap mit 2.000 vollständigen Paarziehungen lautet
**[−9,765625; +1,5625] Prozentpunkte**. Die Erfolgsschwelle von mindestens
+5 Prozentpunkten und positiver unterer Intervallgrenze wird nicht erreicht:
`NO_DEMONSTRATED_INCREMENT`.

Für die primäre Kombination B+P123 liegt die eigene bedingte Trefferquotenspanne
bei **44,14–57,03 %**; der beschreibende exakte einseitige Labeltauschwert beträgt
0,5. Das unterstützt hier keine robuste Trennung vom gestörten Gitter.
Es beweist weder die Gleichheit beider Erzeuger noch eine prinzipielle
Unmöglichkeit ihrer Unterscheidung.

Alle übrigen Vergleiche sind sekundär und beschreibend. Insbesondere wird der
höhere Wert für das gestörte Gitter bei N=36 nicht nachträglich zum Hauptbefund
erklärt. Keine der fünf Zellen erreicht die vorab festgelegte Kombination aus
mindestens +5 Prozentpunkten Zusatz und positiver unterer Intervallgrenze.

Die exakte D-Kontrolle ist in allen fünf Zellen erfüllt: Jede ihrer möglichen
Eingaben kommt im Test gleich oft mit beiden Labels vor. Ein deterministischer
Entscheider aus D allein muss deshalb genau 50 % erreichen. Der Befund bei
unbewegten Gitterpunkten betrifft folglich weitere Struktur, nicht bloß R oder H.
Ob diese Struktur eine brauchbare geometrische Information oder hauptsächlich
ein Artefakt des Gittererzeugers ist, bleibt offen.

## Unsicherheit und Grenzen

Die Bootstrap-Einheit ist das ganze Paar; beide Mitglieder bleiben zusammen.
Die berichteten Intervalle halten Training und ausgewählte gemeinsame
Unterstützung fest. Sie erfassen nicht die Unsicherheit durch neue Pools,
erneutes Matching, erneutes Training, andere Randbedingungen oder andere
Erzeugerfamilien. Zusätzliche Labeltauschwerte sind nicht für die mehrfachen
sekundären Vergleiche korrigiert und werden nicht als Entdeckungsnachweise benutzt.

Der Klassifikator ist bewusst unverändert. Dass zusätzliche Merkmale seine
Leistung nicht verbessern, beweist nicht, dass diese Merkmale grundsätzlich
keine Information tragen. Ebenso beweist ein Scheitern der endlichen Auswahl
nicht, dass exakte Abgleichpaare außerhalb des Pools unmöglich wären.
Der Versuch liefert keine Dimension, Krümmung, Kontinuumsgrenze oder
physikalische Qualifikation.

## Reproduktion und Archiv

Voraussetzungen: Linux/POSIX, vollständiger Git-Checkout, Python 3.12 und
NumPy 2.3.5. Der Test benutzt nach der Installation keine Netzwerkzugriffe;
die [CI-Reproduktion](../../.github/workflows/lorentz-matched-controls.yml)
erzwingt einen Netzwerk-Namespace ohne Netzwerkzugang. Jede Phase ist auf
1.800 Sekunden und 2 GiB Adressraum begrenzt. Ein frisches Ausgabeverzeichnis
ist erforderlich; Fehler bleiben als `INCONCLUSIVE.json` erhalten.

```sh
python3 -m pip install -r research/lorentz_matched_controls/requirements.txt
OPENBLAS_NUM_THREADS=1 python3 -B -O research/lorentz_matched_controls/run.py --selftest
OPENBLAS_NUM_THREADS=1 python3 -B -O research/lorentz_matched_controls/run.py \
  --run /tmp/x6-matched-controls \
  --source-ref ef182efc4af8551295a754df32c2875f44b84574
python3 research/lorentz_matched_controls/compare.py \
  research/lorentz_matched_controls/results /tmp/x6-matched-controls
```

Archivierte Dateien unter [results/](results/):

- `candidate_ledger.json.gz`: jeder der 24.576 Kandidaten, Zufallsschlüssel,
  Abgleichsgrößen und Hash der vollständigen gerichteten Relation.
- `selection.json.gz`: jede Häufigkeitsgruppe, alle verfügbaren Paare und
  vollständige Auswahl, einschließlich nicht auswertbarer Zellen.
- `selected_records.json.gz`: alle 1.879 verwendeten Ordnungen mit Koordinaten,
  vollständigen Relationsmatrizen und Merkmalsvektoren.
- `evaluation.json.gz`: Trainingstransformationen, Klassenschwerpunkte,
  Einzelvorhersagen, Distanzen und paarweise Auswertung.
- `support.json`, `summary.json`, `verification.json`, `costs.json` und
  `RESULTS.json`: lesbare Unterstützung, Ergebnisse, Gegenprüfung und Provenienz.

Alle Kandidaten werden vom getrennten Prüfer neu erzeugt, ihre vollständigen
Relationshashes bestätigt und (R,H) unabhängig berechnet. Die Paarbildung wird
getrennt rekonstruiert. Sämtliche ausgewählten Merkmale werden mit getrennten
Formeln sowie unter Umnummerierung geprüft; ein skalarer Klassifikator
bestätigt alle Testvorhersagen. Die Kleintests prüfen außerdem Labeltauschformel,
fehlende Kandidaten, ungleiche Abgleichswerte, Wiederverwendung, beschädigte
Schnittprofile und Testdaten-Leckage.

Der Vertrag wurde am 16.10.2026 um 18:08:17 UTC im Commit
[`fd42f9c`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/fd42f9c4dc630c34c619a12c6e1a986781ab673e)
veröffentlicht, die geprüften Quellen um 18:13:46 UTC im Commit
[`ef182ef`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/ef182efc4af8551295a754df32c2875f44b84574).
Die erste Zielausführung begann um 18:14:03 UTC und endete um 18:17:29 UTC.
Erzeugung, Auswahl und Auswertung benötigten lokal 80,32 Sekunden,
die getrennte Gegenprüfung 125,43 Sekunden. Die Erzeugungsphase erreichte
145,42 MiB Linux-Prozess-Spitzenspeicher einschließlich Interpreter und NumPy;
dies ist eine Einzellaufmessung, kein Geschwindigkeitsvergleich.

Die Quellen und Zeitpunkte stehen in [publication.json](publication.json)
und [freeze.json](freeze.json). Rechenquellen werden nach Ergebnissichtung
nicht verändert. Die getrennten Prüfwege sind interne Gegenrechnungen;
eine externe Replikation steht aus.

Die nächste sachliche Entscheidung ist, einen geometrischen Zielparameter oder
eine neue begründete Merkmalsfamilie festzulegen. Dafür braucht es einen eigenen
vorab festgelegten Versuch mit neuen Testziehungen. Die aktuellen negativen
Befunde und nicht auswertbaren Kontrollen bleiben als Referenz erhalten.
