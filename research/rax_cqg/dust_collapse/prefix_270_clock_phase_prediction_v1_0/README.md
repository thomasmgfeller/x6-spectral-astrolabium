# Staubuhr-Transfertest am Kettenpräfix 270

**REGISTERED / NOT_RUN.** Der Kettenpräfix 270 hat 15 markierte Fortsetzungen zu elf Endtypen, allesamt ausserhalb des früheren Zehnerträgers. Für dieselbe Uhrmaske ist eine Obergrenze von 1 % für das unnormierte äussere Normquadrat relativ zur Referenz vorregistriert. Geprüft werden sollen die Dichten 1/8 und 1/4 sowie alle nichtverschwindenden komplexen Gewichtsvektoren. Die 22 unmodulierten Referenzen, ihre positiven Nenner, die skalare Gram-Matrix und die Fehlerbudgets sind qualifiziert. Die vorab hergeleiteten Referenzschranken und die Kriterien für den künftigen Lauf stehen im [Protokoll](Protokoll.md).

## Vorregistrierung prüfen

Die Dateien enthalten die für die spätere Auswertung verbindlichen Rechenregeln. registration.json bindet sie durch SHA-256 und dokumentiert den Stand beim Einfrieren. Die zentrale Referenzdatei enthält ausschliesslich unmodulierte Amplituden. Die Kurzprüfung verwendet für den zukünftigen siebenfachen Integrationsweg synthetische Polynome.

~~~sh
sha256sum -c SHA256SUMS
python3 -B verify_registration.py
~~~

Die Reproduktion der unabhängigen Gram-Prüfung und der unmodulierten Referenzen verwendet das mitgelieferte, unveränderte Neun-Richtungen-Archiv. Die übrigen Projektdaten, der Ausgangscode und dessen Lizenzinformationen sind bereits darin eingebettet. Reproduktionsumgebung ist Python 3.12.14 mit NumPy 2.3.5, SymPy 1.14.0 und mpmath 1.3.0. Es genügt ein CPU-Thread.

~~~sh
python3 -B select270.py selection_replay.json
cmp selection.json selection_replay.json
python3 -B gram/gram270.py --source CST_DUST_Praefix_1564_Neun_Richtungen_v0_1_Pruefpaket.zip --output gram_replay.json
cmp gram/gram.json gram_replay.json
python3 -B reference270.py reference_replay.json
cmp reference.json reference_replay.json
python3 -B qualification270.py qualification_replay.json
cmp qualification.json qualification_replay.json
~~~

## Getrennter späterer Ziellauf

Die folgenden Befehle sind für die Ausführung nach öffentlicher Registrierung und gesonderter Beauftragung vorgesehen. Für jede Wiederholung wird ein frischer Ausgabepfad gewählt. Das Ziel umfasst alle 22 modifizierten Amplituden und die 22 gleichgitterigen positiven Kontrollen. Bei einer technischen Unterbrechung wird HOLD mit dem Grund dokumentiert. Das Ergebnis des Zieltests gehört in einen eigenen Nachtrag.

~~~sh
python3 -B run_later.py target_001.json
python3 -B score.py target_001.json
~~~
