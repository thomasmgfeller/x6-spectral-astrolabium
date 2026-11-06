# Geglätteter Massestrom am homogenen Staubball

Für eine externe Übernahme der beiden offenen Probeläufe zuerst [UEBERGABE.md](UEBERGABE.md) lesen.

Dieses Prüfpaket führt die lokale Einzelmessung aus dem Astrolabium-Projekt mit einem bedingten Mittel über alle Bernoulli-Ausdünnungen fort. Alle Massen sind in Einheiten der Sollmasse angegeben. Der Zeitursprung und die Staubreferenz stimmen mit der veröffentlichten Referenz überein. Der spätere Endpunkt trägt die Dichtemarke. Die ungeglättete Kontrollgrösse wird auf derselben Ordnung berechnet.

**Vorgängerstand**  
https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/b7eae25987be232a5a1a15ae49fcdac0286f664c/research/rax_cqg/dust_collapse

## Ergebnisse

Das Einzelziel erfordert eine Trefferwahrscheinlichkeit von mindestens 95 % im Massenband [0,9, 1,1]. Die Grenzen beziehen sich auf die ganze Kugel im räumlich unbeschränkten Modell.

| Eingangsdichte | Vergangenheit | Zukunft | Mittlerer Fehler | Obergrenze für die Trefferchance | Einzelziel |
| --- | --- | --- | --- | --- | --- |
| 1,2 Millionen | 0,11 | 0,24 | +9,16 % | 85,0 % im Haupttest | verfehlt |
| 1,2 Millionen | 0,24 | 0,11 | +9,61 % | 86,1 % im unabhängigen Zusatztest | verfehlt |
| 6 Millionen | 0,11 | 0,24 | +9,16 % | keine informative Grenze | offen |
| 6 Millionen | 0,24 | 0,11 | +9,61 % | keine informative Grenze | offen |

Die beiden angegebenen endlichen Obergrenzen sind nach aussen gerundet. Die Fehlerwahrscheinlichkeit für sämtliche Grenzen beider Testfamilien zusammen beträgt höchstens 1,1 %. Bei sechs Millionen waren die lokalen gekoppelten Unterschiede stark gedämpft. Durch Aufteilen des feineren Poisson-Prozesses in fünf unabhängige Farbklassen folgt ausserdem eine Populationsschranke. Die wahre Standardabweichung bei sechs Millionen ist höchstens 1/√5 derjenigen bei 1,2 Millionen, jeweils für denselben geglätteten Strom, dieselbe Geometrie und dasselbe Fenster.

## Reihenfolge und Daten

- `design.json` und `design.sha256` beschreiben die vor den Hauptziehungen fixierte Konstruktion, Zufallsstarts, Stichproben und Entscheidungskriterien. Die effektive Dichte ist stets 600 000. Die Dichten der Eingangsordnungen sind 1,2 und 6 Millionen je Einheit physischen Vierervolumens. Der Schnitt ist bei 0,47. Fenster 0 hat eine Zukunft von 0,24 und Fenster 1 eine Zukunft von 0,11.
- `expectations.csv` enthält die geometrischen Integrale an beiden Eingangsdichten und der effektiven Dichte. `reference` und `lens` sind zwei numerische Auswertungen der endlichen Poisson-Erwartung. `mean` ist `reference/Rpred`. Der geglättete Strom verwendet die Zeile für die effektive Dichte. Der lokale Vergleich verwendet die Zeile für die Eingangsdichte.
- `caps.csv` enthält 512 unabhängige Paare mit gemeinsamer äusserer Ordnung. `sm0` und `sm1` sind die unnormierten Beiträge aus dem Endkegel. Ihre Differenz nach Division durch den passenden Randfaktor ist der normierte Unterschied der vollständigen Ströme. Beide Einzelbeträge sind nur Beiträge des lokalen Endgebiets.
- `full.csv` enthält die zwölf vollständigen gepaarten Masseströme im periodischen Würfel. `smooth` und `local` sind die unnormierten Flüsse. `full_scores.csv` enthält die normierten Einzelwerte und ihre absoluten Abschneidefehler. Laufzeiten sind maschinenabhängig. Die konfigurierte Seitenlänge 1,6 trägt einen räumlichen Torus. Für jedes einzelne Endpunktmittel gibt es eine eindeutige kausale Umgebung. Korrelationen zwischen weit getrennten Endpunkten können sich gegenüber dem unbeschränkten Raum verändern. Die Globalaussage im unbeschränkten Raum folgt aus den gekoppelten Kegeln. Die Binomialgrenzen des lokalen Kontrollstroms in `full_summary.json` sind zusätzliche Einzelvergleiche und gehören nicht zur gemeinsamen Hauptfamilie.
- `bounds.csv` und `thresholds.csv` enthalten Hauptgrenzen und Zählungen. `coverage_upper` begrenzt die Trefferwahrscheinlichkeit der ganzen Kugel. `cap_rms_smooth` und `cap_rms_local` beziehen sich nur auf die Kegeldifferenzen. Für die Untergrenze `sd_floor` passen K räumlich disjunkte Endkegel in die Kugel. Bei fester Umgebung sind ihre Beiträge unabhängig. Somit gilt Var(S) ≥ K E[D²]/2. Eine Treppenfunktion der vorab festgelegten Schwellen schätzt E[D²] von unten. Der Code verwendet je Schwelle eine exakte einseitige Binomialuntergrenze.
- `extension_design.json` und die zugehörige SHA-256-Datei fixieren einen gesonderten Zusatztest. Er wurde nach teilweiser Sichtung der Hauptdaten und vor den Zusatzziehungen festgelegt. Das ist im Design vermerkt. Seine 40 neuen unabhängigen Paare mit grösserem Endkegel im kurzen Zukunftsfenster bei 1,2 Millionen stehen in `extension.csv`. Die gesonderte 99,9-Prozent-Grenze steht in `extension_summary.json`. Für die gesamte Hauptfamilie gilt 99 % gemeinsame Überdeckung, für beide Familien zusammen mindestens 98,9 %.
- `checks.csv`, `coupling_checks.csv` und `halo_checks.csv` überprüfen die analytische Mittelung, die Zählung aller Zwischenereignisse, die ganze gekoppelte Massendifferenz und den nichtperiodischen Generator. `halo_cost.csv` enthält geplante Punktzahlen aus dem Vierervolumen. Der Bericht unterscheidet Punktzahlprognosen von durchgeführten Hochdichtemessungen.

## Reproduktion

Getestet unter Linux x86-64 mit Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, Matplotlib 3.10.8 und GCC 13.3.0. Der Kern benötigt einen C++17-Compiler mit OpenMP-SIMD-Unterstützung. Für den Bericht werden pdfLaTeX, Latin Modern, microtype, fancyhdr, embedfile, hyperref und die übrigen im Vorspann angegebenen Standardpakete benötigt. Im entpackten Verzeichnis arbeiten. Die Neuberechnung der Hauptziehungen überschreibt die entsprechenden CSV-Dateien. Für eigene Läufe eine Arbeitskopie verwenden. Die Stichproben richten sich ausschliesslich nach Design, Dichte, Fenster und Laufindex. Ergebnisse von parallelen Vollordnungen können in anderer Zeilenfolge ankommen.

```sh
sha256sum -c SHA256SUMS
sha256sum -c design.sha256
sha256sum -c extension_design.sha256
export OPENBLAS_NUM_THREADS=1
export CST_WORKERS=4
python3 -c 'from analysis import expectations; expectations()'
python3 cap_run.py
python3 full_run.py
python3 extension.py
python3 checks.py
python3 coupling_check.py
python3 halo_reference.py
python3 analysis.py
python3 report_data.py
pdflatex -halt-on-error -jobname=CST_Staubkollaps_Geglaetteter_Massestrom report.tex
pdflatex -halt-on-error -jobname=CST_Staubkollaps_Geglaetteter_Massestrom report.tex
```

Mit den mitgelieferten Rohdaten reicht zum Nachrechnen der Grenzen und der PDF `analysis.py` ab der entsprechenden Zeile. Die Kennzahlen des Zusatzversuchs lassen sich mit `python3 -c 'from extension import summary; summary()'` erneut berechnen. Ein unterbrochener Hauptkegellauf kann mit `python3 cap_run.py --resume` die fehlenden festgelegten IDs ergänzen. Für die unabhängigen Zählkontrollen die beiden C++-Kerne zuerst über `python3 -c 'import cap_run, full_run; cap_run.compile_kernel(); full_run.compile_kernel()'` bauen.

## Endlicher Test bei sechs Millionen

Der Laufzeittest bei sechs Millionen wertete in jeder Zeitfensterorientierung 32 nach Zeit geschichtete Endpunkte einer neuen, korrekt aufgefüllten Ordnung aus. Die grobe Hochrechnung auf einen Prozessorkern beträgt 16 beziehungsweise 27 CPU-Stunden je vollständiger Ordnung. Auf andere Rechner und Algorithmen ist diese Kostenschätzung nur bedingt übertragbar. Diese Teilwerte sind von der Trefferstatistik getrennt. Mit `python3 high_cost.py` wird die Messung reproduziert.

Der ausführbare Generator `halo_reference.py` erfasst sämtliche möglichen Vorfahren aller markierten Kugelpunkte im unbeschränkten Raum. Seine acht kleinen vollständigen Gegenrechnungen laufen mit `python3 halo_reference.py`. Der gesonderte, rechenintensive Befehl `python3 halo_reference.py --one 20261102901 --window 0 --density 6000000` wertet eine neue vollständige Ordnung für das lange Zukunftsfenster aus. Fenster 1 wählt die kurze Zukunft. Die Hauptentscheidung bei sechs Millionen verwendet nur die festgelegten Endbereiche. Eine Hochdichte-Kohorte im unbeschränkten Raum bleibt offen.

## Quellen

Benincasa und Dowker, *The Scalar Curvature of a Causal Set* (2010).  
https://arxiv.org/abs/1001.2725

Last und Penrose, *Lectures on the Poisson Process*, insbesondere Kapitel 5 zu Markierung und Ausdünnung.  
https://stoch.math.kit.edu/english/297.php
