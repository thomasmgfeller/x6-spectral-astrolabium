# Frühe Uhr-5-Auslese und unabhängiger kosmologischer Referenzfit

Der Bericht im Paket fasst zwei Untersuchungen zusammen. Im Staubballmodell stammt die frühe Phasendifferenz aus der Originalwirkung auf dem festen N15-Typ. Die Ableitung einer vollständigen physikalischen Messung und die positive Masseneichung bleiben offen. Die kosmologische Rechnung verwendet das Standardmodell flaches ΛCDM und liefert separat einen Referenzwert aus DESI DR2 und Pantheon+.

## Unterlagen

* `uhr5/HERLEITUNG.md` enthält die genaue Reichweite des Ergebnisses, die bedingte Orthogonalität, die Vierphasen-Normkorrektur und die Grenzen der trägertreuen Messung. `uhr5/ergebnis.json` enthält die numerischen und algebraischen Kontrollen. Die geerbten Originalquellen und das eingefrorene P3-Register sind beigefügt.
* `daten/README.md` beschreibt Priors, Likelihood, Vergleichszahlen, Empfindlichkeitsprüfung und die numerische Gegenprobe. `daten/ergebnis.json` und `daten/gegenprobe.json` speichern die Ergebnisse.
* `gegenprobe/desi_gegenprobe.py` wiederholt die DESI-Rechnung mit adaptiver Quadratur und gleichzeitiger Optimierung beider Parameter, unabhängig vom Hauptcode. Die vor der Auswertung gewählte Vergleichsschwelle von 0,5 in gemeinsamer Mahalanobis-Distanz dient als Plausibilitätskontrolle gegenüber den publizierten Posteriorparametern. Beide Verfahren verwenden denselben Datensatz.

## Reproduktion

Python ab 3.11, NumPy und SciPy reichen aus. Das erste Kommando prüft die Dateiintegrität. Der Uhrtest läuft vollständig offline. Für den kosmologischen Vergleich werden beim ersten Lauf die vier in `daten/quelldaten.json` aufgeführten, frei verfügbaren Originaldateien heruntergeladen und gegen SHA-256 geprüft. Die Dateien können anschliessend offline wiederverwendet werden.

```sh
sha256sum -c SHA256SUMS
python -B uhr5/pruefen.py
python -B daten/datenpilot.py
python -B daten/gegenprobe.py
python -B gegenprobe/desi_gegenprobe.py daten/cache/desi_gaussian_bao_ALL_GCcomb_mean.txt daten/cache/desi_gaussian_bao_ALL_GCcomb_cov.txt
```

Für den Datenpilot sind dieselben Befehle mit getrennten `--output`-Dateien möglich. Die Hashes bezeichnen den ausgelieferten Stand. Der lokale Prüfplan der Uhruntersuchung besitzt keinen unabhängigen Zeitstempel. Der Pilot enthält keine gemessenen P3-Daten und keine stochastische Λ-Trajektorie.
