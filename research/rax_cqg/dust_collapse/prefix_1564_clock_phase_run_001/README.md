# Staubuhr am Präfix 1564 · Ziellauf 001

**PASS** gemäss der am 20. November 2026 vorregistrierten 1-%-Vorhersage. Die obere Grenze liegt bei beiden Dichten unter oder auf der vorab festgelegten Schwelle.

Sechs Phasenumkehrungen je Lappen erhalten die punktweise Eingangsintensität. Geprüft wurde das Verhältnis der unnormierten äusseren skalaren Normquadrate mit und ohne die Umkehrungen. Die Grenzen schliessen bei jeder Dichte das Supremum dieses Verhältnisses über alle von null verschiedenen komplexen Gewichtsvektoren der zehn Endtypen ein. In Zähler und Nenner wird derselbe Vektor verwendet.

| Dichte | Untere Grenze des Supremums | Obere Grenze des Supremums |
| --- | ---: | ---: |
| 1/8 | 0,000000 % | 0,002197 % |
| 1/4 | 0,000000 % | 0,002217 % |

Alle Prozentgrenzen sind nach aussen gerundet. Die exakten rationalen Schranken stehen in `score_001.json`. Die Kontrollsummen aus denselben sieben Teilintervallen mit durchgehend positivem Vorzeichen sind für alle 20 Kombinationen von Endtyp und Dichte mit den archivierten Referenzen verträglich. Der Fehlerkreis hat je komplexer Zielamplitude den vorab festgelegten Radius 1/50000.

Das Ergebnis betrifft das endliche kohärente Modell mit der registrierten Randpräparation. Die physikalische Auswahl der Historiengewichte und die Frage eines Bounce bleiben offen. Für Etappe 6 und P3 gilt weiterhin **HOLD**.

## Rohdaten und Nachrechnung

`target_run_001.json` enthält alle direkt berechneten Zielamplituden und Kontrollsummen. `score_001.json` ist die Ausgabe des versiegelten Auswerters. `provenance.json` dokumentiert Zeit, Softwarestand und Prüfsummen. `audit.py` kontrolliert die 20 Referenzüberlappungen, das Fehlerbudget und die Wertung nochmals mit rationaler Arithmetik. Seine Ausgabe ist in `audit.json` festgehalten.

Das enthaltene Originalarchiv bindet die Vorregistrierung, die Referenz und die unveränderten Rechenprogramme. Nach dem Entpacken dieses Ergebnispakets im gleichen Verzeichnis ausführen. Für `audit.py` genügt die Python-Standardbibliothek. Die Auswertung und die Integration verwenden die in `provenance.json` dokumentierte Umgebung.

~~~sh
sha256sum -c SHA256SUMS
unzip -q CST_DUST_Praefix_1564_Vorhersage_Uhrphase_v1_0_Pruefpaket.zip -d registration
python3 -B registration/score.py target_run_001.json
python3 -B audit.py
~~~

Für eine erneute Integration mit frischem Ausgabepfad genügen die folgenden Befehle.

~~~sh
python3 -B registration/run_later.py target_replay.json
python3 -B registration/score.py target_replay.json
~~~

[Öffentliche Vorregistrierung am fixierten Commit](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/357a3214355ed56dd9e6b887c322278701f15145/research/rax_cqg/dust_collapse/prefix_1564_clock_phase_prediction_v1_0/registration.json)
