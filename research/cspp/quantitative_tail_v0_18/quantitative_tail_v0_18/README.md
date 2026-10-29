# CSPP v0.18: Quantitative Restmajoranten

Die nächste Stufe nach v0.17 ist ausgeführt: explizite KG-Quellkonstanten,
eine scharfe globale Schichtgewichtsschranke und vollständig transportierte
bedingte Erwartungswertschranken für die vier vorhandenen Omega5-Archive.

**Ergebnis:** Die pfadweise Summation benötigt nur bedingte Faktoren zwischen
2,73 und 3,79. Die pauschalen Quell- und Archivschranken machen die gesamte
Restmajorante trotzdem unbrauchbar für die Genauigkeitsfreigabe: Die besten
ausgewerteten Obergrenzen liegen um 10^54. Das beweist keinen großen Fehler.
METHOD_HOLD, G1 HOLD und das individuelle Fehlerziel bleiben unverändert.

Die ferne History erhält eine abklingende numerische Majorante mit allen
Konstanten. Ihre geringe Größe bei extrem großen Abschneidezeiten ist keine
Schranke für den weiterhin fehlenden endlichen Teil hinter Omega5.
Es wurden keine neuen Zufallsdaten erzeugt und keine neue statistische
Freigaberegel eingeführt.

## Reproduktion

```sh
python3 -m pip install python-flint==0.8.0
python3 reproduce.py
```

Python 3.12; alle Eingaben sind enthalten. `PROOF.md` enthält die
mathematischen Voraussetzungen und vollständige Herleitung.
`PROTOCOL.json` hält die vorab erklärten analytischen Gitter fest.
`results/BOUNDS_*.json` enthält alle Werte, nicht nur ausgewählte Minima.
`results/CHECKS.json` dokumentiert die Kontrollen. `reproduce.py` prüft zunächst
die Paketprüfsummen, rechnet in einem temporären Verzeichnis mit 128 und
192 Bit neu und vergleicht die drei wissenschaftlichen JSON-Ergebnisse exakt.
Die enthaltenen Ergebnisse werden dabei nicht überschrieben.

`report/Quantitative_Restmajoranten_v0_18.pdf` ist der geprüfte Bericht.
Für seinen optionalen Neubau: `python3 -m pip install -r requirements.txt`,
dann `python3 build_report.py`. Dafür werden die Systemschriften
DejaVuSans, DejaVuSans-Bold und DejaVuSansMono unter
`/usr/share/fonts/truetype/dejavu/` benötigt. PDF- und SVG-Metadaten können
beim Neubau abweichen; die exakte Reproduktion bezieht sich auf die
wissenschaftlichen JSON-Ergebnisse. Ein Bericht-Neubau ändert Paketdateien
und damit deren Prüfsummen.

Die Rechenprüfungen ersetzen keine unabhängige Begutachtung des analytischen
Beweises. Eine Erwartungswertschranke ist kein konkreter Realisierungsfehler
und keine statistische Freigabe.

Die nächste Berechnung muss Quellableitungen und tatsächliche geometrische
Intervallüberlappungen gezielt einschließen. Die pauschale Majorante wird
nicht durch ein astronomisch großes neues Ensemble weiterverfolgt.
