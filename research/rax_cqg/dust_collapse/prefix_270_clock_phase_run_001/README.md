# Kettenpräfix 270 · Erster vorregistrierter Staubuhr-Ziellauf

**PASS** nach dem öffentlich festgelegten Auswerter. Für beide Dichtezentren wurde geprüft, welchen Anteil des unmodulierten äusseren skalaren Normquadrats sechs Phasenumkehrungen je Staubuhrlappen übrig lassen. Die registrierte Schwelle beträgt 1 %. Das Ergebnis gilt jeweils für das Supremum über alle von null verschiedenen komplexen Gewichtungen der elf Endtypen. In Zähler und Nenner wird dieselbe Gewichtung verwendet.

| Dichtezentrum | Untere Grenze des Supremums | Obere Grenze des Supremums |
| --- | ---: | ---: |
| 1/8 | 0,000000 % | 0,000786 % |
| 1/4 | 0,000000 % | 0,000797 % |

Die Tabelle gibt Prozentanteile am Referenzwert an. Die Grenzen sind nach aussen gerundet. Die exakten Brüche stehen in `score_001.json`. Alle elf Endtypen unterscheiden sich vom Zehnerträger des früheren Präfixes 1564. Je Dichte stehen elf direkte Zielamplituden und elf unmodulierte Kontrollen aus derselben Sieben-Zellen-Integration zur Verfügung. Alle 22 Kontrollen überlappen die zugehörigen archivierten Referenzkreise. Für jede komplexe Zielamplitude gilt der registrierte Fehlerradius 1/50000.

Das Ergebnis betrifft die zwei vorgegebenen Dichten, die feste Randpräparation, die Phasenmaske und die skalare Randnorm dieses endlichen Modells. Die physikalische Gewichtsregel und der Nachweis eines Bounce bleiben offen. Für Etappe 6 und P3 gilt weiterhin **HOLD**.

## Daten und Nachrechnung

Die Registrierung wurde am 20. November 2026 um 10:30:56 Uhr Schweizer Zeit versiegelt. Dieser Ziellauf begann am 20.11.2026 um 10:43:34 Uhr Schweizer Zeit und benötigte 167.7 Sekunden. `target_001.json` enthält die komplexen Zielwerte und Kontrollen, `score_001.json` die unveränderte Ausgabe des versiegelten Auswerters. `audit_001.py` kontrolliert die Referenzüberlappungen, die registrierten Fehlerkreise und die exakten rationalen Entscheidungsgrenzen aus diesen Daten. `provenance.json` dokumentiert die Softwareversionen, Zeiten und Prüfsummen. Das eingebettete Originalarchiv enthält den vorregistrierten Rechenweg und seine Referenzdaten.

Im entpackten Ergebnisverzeichnis genügen für die Integritäts- und Ergebnisprüfung die folgenden Befehle. Der Audit benötigt ausschliesslich die Python-Standardbibliothek.

~~~sh
sha256sum -c SHA256SUMS
python3 -B audit_001.py
unzip -q CST_DUST_Praefix_270_Uhrphase_Vorregistrierung_v1_0.zip -d registration
python3 -B registration/score.py target_001.json
~~~

Für eine neue Integration mit der in `provenance.json` angegebenen Softwareumgebung einen frischen Dateinamen wählen.

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B registration/run_later.py replay.json
python3 -B registration/score.py replay.json
~~~

[Öffentliche Vorregistrierung am fixierten Commit](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/5e3ae0771a06101271a0622f9757983f8c600e69/research/rax_cqg/dust_collapse/prefix_270_clock_phase_prediction_v1_0/registration.json)
