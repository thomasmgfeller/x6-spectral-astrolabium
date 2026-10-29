# CSPP v0.21: Detektor-Unterteilung

Der nächste dokumentierte Schritt nach v0.20 ist ausgeführt: Der direkte
Detektorbeitrag für P=[-6,-5] x [-2,2]^3 wird mit einer bewiesenen monotonen
Schichtkernhülle und 256 Endpunktboxen je Zeitfenster eingeschlossen.
Die vollständigen Patchschranken sinken um 42-55 Prozent. Der übrige
äußere Historybereich bleibt offen. METHOD_HOLD und G1 HOLD bleiben.

## Reproduktion

Python 3.12, python-flint 0.8.0 und NumPy 2.x:

```sh
python3 -m pip install -r requirements.txt
python3 reproduce.py --quick
python3 reproduce.py
```

Der volle Lauf kopiert das Paket in ein temporäres Verzeichnis, berechnet
128 und 192 Bit neu, prüft die mathematischen Kontrollen und vergleicht
alle sieben numerischen Ergebnisdateien bytegenau. Die Originalergebnisse
werden nicht überschrieben. Ein vollständiger Lauf benötigt mehrere Minuten; die Laufzeit hängt vom
Rechner ab.

- `PROOF.md`: vollständige Herleitung, Voraussetzungen und Grenzen.
- `PROTOCOL.json`: unverändertes Modell und feste Integrationsgitter.
- `results/DETECTOR_192.json`: endgültige Bilanz aller acht Fälle.
- `results/CELLS_*.json.gz`: genaue Zählbereiche und Zellmajoranten.
- `results/GEOMETRY_*.json.gz`: gemeinsame physikalische Volumengrenzen.
- `results/CHECKS.json`: Kontrollzahlen und PASS/FAIL-Ergebnis.
- `PROVENANCE.json`: 14 unveränderte Eingabedateien mit Git-Blob- und
  SHA256-Identitäten zum gepinnten Main-Commit.
- `vendor_v020/`: unveränderter importierter v0.20-Code.
- `report/Detektor_Unterteilung_v0_21.pdf`: deutschsprachiger Ergebnisbericht.

Die Detektorkugel wird nicht durch einen Würfel oder durch Punkte ersetzt.
Die 3,49 Prozent nicht durch vollständig innere Kleinstboxen aufgelöste
Kugelmasse verbleiben unter einer gültigen ganzen Kugelhülle. Das Verfahren
ist eine obere bedingte Erwartungswertschranke, kein realisierungsbezogenes
Genauigkeitszertifikat. Externes wissenschaftliches Review wird nicht
behauptet. Die Veröffentlichung auf GitHub ist ein gesonderter Schritt.
