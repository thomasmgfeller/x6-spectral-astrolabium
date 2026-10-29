# CSPP v0.19 - Quellnormen und geometrischer Rest

Die globale KG-Feldmajorante sinkt auf weniger als 6.429644. Eine geometrische
Beschränkung der Archivüberlappung und die gemeinsame Integration der Feld-
und Kernhüllen reduzieren die vollständige bedingte L1-Restmajorante von
etwa 1e54 auf 2.36e14 bis 3.39e14. Dies sind obere Schranken, keine Fehlerbefunde.

METHOD_HOLD und G1 HOLD bleiben bestehen. Individuelle Genauigkeit ist
NOT_CERTIFIED; kein neues Ensemble und keine neue statistische Freigaberegel.

## Reproduktion

Python 3.12 und python-flint 0.8.0:

```sh
python3 -m pip install -r requirements.txt
python3 -B reproduce.py
```

Der isolierte Lauf prüft alle Paket-Hashes, rechnet beide Präzisionen neu und
wiederholt die algebraischen, quadraturbasierten und Poisson-Kontrollen.
Die wissenschaftlichen JSON-Dateien müssen exakt übereinstimmen. Auf dem
Entwicklungsrechner dauern beide Hauptrechnungen zusammen ungefähr eine Minute.

- `PROOF.md`: vollständige Herleitung und Aussagegrenzen.
- `PROTOCOL.json`: deklarierte Abschätzungsfamilien und Kontrollen.
- `source_norms.py`: exakte Ableitungsrekursion und Quellnormen.
- `kernel.py`: exakter bedingter absoluter Gewichtskern.
- `run.py`: vollständig transportierte Restmajoranten.
- `verify.py`: Gegenprüfungen und Negativkontrollen.
- `results/`: Intervallresultate bei 384/512 Bit und Kontrollen.
- `evidence/`: unveränderte Vorgängerbelege und externer Wolfram-Output.

Die hohen Präzisionen kontrollieren Auslöschung in den Ableitungssummen.
Sie verändern keine physikalische Skala. Die lokalen Überlappungsvolumina
aller Archivintervalle sind noch nicht ausgewertet. Der externe Wolfram-
Check ist mit seinem ursprünglichen Ergebnis archiviert; der lokale Replay
fragt den externen Dienst nicht erneut ab.

`build_report.py` benötigt zusätzlich reportlab, matplotlib und Pillow; diese
Bibliotheken sind nicht für die wissenschaftliche Reproduktion erforderlich.
Das Paket ist auf Main-Commit 995b2184cb5346aee502d8e69089681181c5853e
aufgebaut; seine neue Version v0.19 ist noch nicht auf GitHub veröffentlicht.
