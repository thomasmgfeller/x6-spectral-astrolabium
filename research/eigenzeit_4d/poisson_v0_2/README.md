# Eigenzeit 3+1: korrelierte Poisson-Zählungen, v0.2

27. Oktober 2026. Anschluss an den exakten Fünf-Landmarken-Test v0.1.

**Ergebnis:** Der vorab festgelegte Test der beobachteten Eigenzeitgenauigkeit
besteht bei der höchsten untersuchten Dichte. Die datenabhängige
10%-Fehlerzertifizierung besteht nicht. Damit bleibt die allgemeine
wissenschaftliche Freigabe auf HOLD.

## Was tatsächlich ausgeführt wurde

- 20 vorab festgelegte 3+1-Minkowski-Geometrien: vier Referenzen und 16 neue,
  kleine rationale Variationen mit eigener, vorab festgelegter Zufallsfolge.
- Vier Dichten, jeweils 512 unabhängige Zählwiederholungen je Geometrie:
  insgesamt **40.960 gemeinsame Poisson-Zählvektoren**.
- 40.960 zusätzliche Vektoren mit fälschlich unabhängigen Marginalzählungen
  als ausdrücklich gekennzeichnete Negativkontrolle.
- **1.024 direkt erzeugte Punktwolken mit 4.193.689 Punkten** zur Gegenprüfung
  der Zählverteilung; weitere 100.000 Punkte für Verteilungstests des Samplers.
- Vollständige Reproduktion sämtlicher Zählvektoren und direkter Punktwolken.
- 160 zusätzliche Rechnungen mit 80 Dezimalstellen und einem separaten
  Eliminationsverfahren; grösste relative Abweichung zum Float64-Ergebnis
  2,733e-9. Das ist eine interne Gegenprüfung, keine externe Replikation.

Protokoll, Geometrien und ausführbare Quellen wurden vor den primären
Zählläufen per SHA-256 gebunden (`FREEZE.json`). Es gab keine nachträgliche
Änderung der Geometrien, Seeds, Dichten oder Erfolgsschwellen. `audit.py`
wurde anschliessend als interne Reproduktionsprüfung ergänzt.

## Resultate mit vollständigen Nennern

Pro Dichte sind 10.240 Wiederholungen enthalten. N bezeichnet die erwartete
Zahl zufälliger Hintergrundereignisse im äusseren Intervall I(a0,q).

| N | Rechnerisch gültige Eigenzeit | Gültig und Fehler <=10%, ohne Mindestzähl-Gate | Alle Erfolgskriterien erfüllt | 10%-Fehlerzertifikat |
|---:|---:|---:|---:|---:|
| 65.536 | 4.617 | 2.327 | 0 | 0 |
| 1.048.576 | 9.016 | 7.492 | 3.320 | 0 |
| 16.777.216 | 10.196 | 9.581 | 9.581 | 0 |
| 268.435.456 | 10.240 | 10.239 | 10.239 | 0 |

Die Erfolgskriterien verlangen die zulässige Lorentz-Signatur, numerische
Invertierbarkeit, positive rekonstruierte Eigenzeit, mindestens 16 Ereignisse
in jedem der 20 verwendeten Intervalle und höchstens 10% relativen
Eigenzeitfehler. Ungültige oder unzureichend gezählte Fälle bleiben im Nenner.
Insbesondere bedeutet die Null in der ersten Zeile nicht, dass jeder einzelne
Punktschätzer um mehr als 10% abweicht: Kein Fall erfüllt dort das
Mindestzähl-Gate.

Bei der höchsten Dichte bestehen 10.239/10.240 Fälle (99,9902%). Die primäre
Freigaberegel betrachtet aber jede der 20 Geometrien einzeln. Ihre jeweils
512 Wiederholungen liefern einseitige Clopper-Pearson-Untergrenzen, mit
Bonferroni-Korrektur auf insgesamt 95% Konfidenzniveau. Die kleinste dieser
Untergrenzen beträgt **98,4073%** und liegt über der vorab verlangten
90%-Erfolgswahrscheinlichkeit. Das ist eine Aussage zu diesen 20 festen
Geometrien im deklarierten Modell, keine Garantie für beliebige Geometrien.

## Warum trotzdem HOLD gilt

Die Punktschätzer werden anhand der bekannten Simulationswahrheit beurteilt.
In einer unbekannten Geometrie ist diese Wahrheit nicht verfügbar. Dort
brauchen wir zusätzlich eine aus den Beobachtungen ableitbare Fehlergrenze.

Für jede Beobachtung wurden simultane Poisson-Mittelwertintervalle gebildet
und durch die Rekonstruktion fortgepflanzt. Die analytische Konstruktion
liefert unter dem Modell mindestens 95% Überdeckung, wenn exakt gerechnet
wird; hier wurden die Quantile und Normen numerisch ausgewertet, ohne
gerichtete Rundung oder formale Intervallverifikation.

Diese Schranke bleibt sehr konservativ. Bei höchster Dichte sind nur
6.049/10.240 Eigenzeitintervalle nach oben endlich; kein einziges sichert
10% relativen Fehler ab. Bei den Rahmen mit epsilon=1 sind alle 5.120
Intervalle endlich, ihre mediane volle Breite beträgt jedoch rund 110% der
wahren Eigenzeit. Bei epsilon=1/4 sind nur 929/5.120 endlich; deren mediane
volle Breite beträgt rund 742%. Die 100%-Überdeckung der wahren Eigenzeit
in diesem Lauf ist angesichts dieser breiten oder unbeschränkten Intervalle
kein Präzisionsnachweis.

Die gute beobachtete Genauigkeit und das fehlende Zertifikat widersprechen
sich nicht. Es fehlt eine ausreichend scharfe Fehlerrechnung. Ob die
konservative rechteckige Region durch eine Rechnung mit dem vollständigen
gemeinsamen Zählgesetz genügend verbessert werden kann, bleibt zu prüfen.

## Gemeinsame Zählverteilung ohne Integrationsnäherung

Die sieben vorgegebenen Ereignisse bilden in jedem Fall eine strenge
zeitartige Kette a0 < ... < a4 < p < q. Deshalb lassen sich die Intervalle
exakt in 21 disjunkte Bereiche zerlegen. Deren Volumina sind endliche
Differenzen bekannter 4D-Diamantvolumina. Unabhängige Poisson-Zahlen auf
diesen disjunkten Bereichen erzeugen durch Summieren die richtigen,
korrelierten Intervallzählungen. Die Herleitung steht in `THEORY.md`.

Dadurch mussten für die hohen Dichten nicht tatsächlich 268 Millionen
Punkte pro Wiederholung erzeugt werden. Diese Zahl beschreibt die erwartete
Population des simulierten äusseren Intervalls. Der primäre Simulator zieht
21 Bereichszählungen; die Zerlegung ist analytisch exakt, die Zufallszahlen
und ihre Mittelwerte werden mit der dokumentierten numerischen Software
berechnet. Die Methode setzt die hier verwendete Kettengeometrie voraus.

Alle 8.820 exakten Kovarianzidentitäten (441 je Geometrie) wurden geprüft.
Für ein verschachteltes Intervallpaar beträgt die über alle Fälle gemittelte
theoretische standardisierte Kovarianz 0,360651, beobachtet werden 0,361370.
Die unabhängige Negativkontrolle ergibt -0,000882, bei theoretisch null.
Das illustriert, welche Abhängigkeit ein unabhängiges Ziehen der
Intervallzählungen verlieren würde; es ist kein allgemeiner Beweis, dass
Korrelationen die Genauigkeit immer verbessern.

## Diagnosearme

| N | Vollständige Rekonstruktion | Exakte Landmarkenmetrik, verrauschte Stützpunktabstände | Direkte p-q-Zählung |
|---:|---:|---:|---:|
| 65.536 | 0 | 0 | 0 |
| 1.048.576 | 3.320 | 4.409 | 9.709 |
| 16.777.216 | 9.581 | 10.184 | 10.240 |
| 268.435.456 | 10.239 | 10.240 | 10.240 |

Wieder jeweils von 10.240. Die exakte Landmarkenmetrik nutzt wahre Geometrie
und ist ausschliesslich diagnostisch. Die direkte p-q-Zählung ist ein anderer
Beobachtungsweg; sie geht weder in den primären Schätzer noch in dessen
Fehlergrenze ein. Eine gezielte Manipulation dieser zurückgehaltenen Zählung
ändert beide primären Ausgaben nicht. Beim direkten Vergleich gilt das
Mindestzähl-Gate für sein einzelnes Intervall; bei der Rekonstruktion für
alle 20 benötigten Intervalle. Die Verfügbarkeitsanforderungen sind also
unterschiedlich.

## Geltungsbereich und verbleibende Arbeit

Die Landmarken sind fest vorgegeben, die Dichte und die flache
3+1-Modellklasse sind bekannt. Simuliert wird ein unabhängiger zufälliger
Hintergrund. Die sieben vorgegebenen Ereignisse selbst werden nicht als
zufällige Poisson-Punkte mitgezählt. Wenn sie in einer vollständigen Liste
mitgeführt werden, sind von der Rohzählung in I(e_i,e_j) die bekannten
j-i-1 eingefügten inneren Kettenereignisse abzuziehen.

Damit ist noch keine intrinsische Landmarkenauswahl aus derselben
zufälligen Wolke implementiert oder validiert. Eine solche Auswahl verändert
die bedingte Verteilung und braucht eigene Absicherung, etwa unabhängige
Poisson-Färbungen für Auswahl und Zählung. Der neue direkte 4D-Sampler wurde
geprüft; die historische radiale Auffälligkeit eines anderen Samplers wird
dadurch weder erklärt noch geschlossen.

Der nächste fachliche Schritt ist eine schärfere gemeinsame Konfidenzregion
unter Verwendung des jetzt expliziten Zählgesetzes, zunächst in dieser
Kettenklasse. Parallel dazu ist die datenabhängige Auswahl gut konditionierter
Landmarken als separates Experiment vorzubereiten. Ein 4D-Operator,
Krümmungsrekonstruktion und der allgemeine GFEST-Stabilitätsclaim sind mit
diesem Paket nicht freigegeben. Die alten 38 HOLD-Zellen werden nicht berührt.

## Reproduktion und Dateien

Voraussetzungen: Python 3.12, NumPy 2.3.5, SciPy 1.17.0.

```sh
python3 -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 run.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 audit.py
```

In einer Arbeitskopie ausführen; Ergebnisdateien werden überschrieben.
`prepare.py` dokumentiert die ursprüngliche Geometrieerzeugung und
Quellenbindung. Für den Replay die vorhandene `FREEZE.json` verwenden und
`prepare.py` nicht erneut ausführen. Die Laufzeit in `RESULTS.json` ist
Metadatum und muss bei Wiederholung nicht übereinstimmen.

- `PROTOCOL.json`, `geometries.json`, `FREEZE.json`: vorher festgelegte Eingaben.
- `model.py`, `run.py`, `prepare.py`: Modell und Ausführung.
- `RESULTS.json`: sämtliche 80 Geometrie-Dichte-Zellen mit allen Nennern.
- `campaign_arrays.npz`: Zählungen, Negativkontrolle, Schätzer, Fehlergrenzen.
- `direct_cloud_counts.npz`: Zählungen der 1.024 direkten Punktwolken.
- `audit.py`, `AUDIT.json`: Replay und separate Dezimalrechnung.
- `THEORY.md`: Beweis der Bereichszerlegung und Fehlerfortpflanzung.
- `exact_start.py`: unveränderter exakter Ausgangstest v0.1.
- `SHA256SUMS`: Prüfsummen des ausgelieferten Pakets.

In `campaign_arrays.npz` ist die erste Achse nach Dichte, dann Geometrie
geordnet, jeweils wie `RESULTS.json/records`; die zweite Achse enthält die
512 Wiederholungen. `counts` und `iid_negative` verwenden die lexikographisch
geordneten 21 Paare aus den Knoten 0,...,6. `metrics` hat die Spalten
tau, valid, count_eligible, success, oracle_tau, iid_tau, direct_tau.
`bounds` hat lo, hi, certificate_10pct, mean_box_cover, tau_cover,
perturbation_ratio. Unverfügbare Schätzer stehen als NaN, unbeschränkte
Obergrenzen als +Inf; sie wurden nicht gelöscht.

## Quellen

- S. Surya, *The causal set approach to quantum gravity*, Abschnitt 4.1,
  4D-Intervallvolumen: https://arxiv.org/html/1903.11544v2
- G. Last, M. Penrose, *Lectures on the Poisson Process*, Poisson-Zählmasse,
  unabhängige Zählungen auf disjunkten Mengen:
  https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf
- Astropy-Dokumentation, zentrale frequentistische Poisson-Intervalle:
  https://docs.astropy.org/en/stable/api/astropy.stats.poisson_conf_interval.html
- Vorheriger Projektstand:
  https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/main/research/lorentz_local_dalembert

Neue Rechnungen sind interne Simulationsbefunde. Kein Neuheitsanspruch,
keine externe Replikation, keine Messung einer physischen Raumzeit.
