# CST-DUST: Markierte Zustände, Ereignisse und Endauslese v0.1

Dieses Paket erweitert den kohärenten Quotienten auf die vollständigen
kontinuierlichen Uhr- und Materiefelder bei festem endlichem Regulator.
Es konstruiert bedingte positive Produkte und transportierte
Präparationsprojektoren. Die physikalische Auswahl bleibt offen.

Ein exaktes Gegenbeispiel zeigt, warum eine labelinvariante aktuelle
Staubaussage nicht ungeprüft als Messprojektor verwendet werden darf:
Ihr naiver Erwartungswert ist für einen Hilfsraumzustand −1/149.
Die skalierte kohärente Endauslese benötigt außerdem eine eigene Norm-
und Schnittprüfung. Eine kompatible transportierte Auslese verändert die
ursprüngliche Summenkontraktion.

Alle acht physikalischen Gates bleiben HOLD. Kein Bounce-Nachweis.

## Lesen

- `CST_DUST_Markierte_Zustaende_Ereignisse_v0_1.pdf`: kompakter Bericht.
- `DERIVATION.md`: Definitionen, allgemeine Beweise und Grenzen.
- `event_contract.json`: aktueller, maschinenlesbarer Geltungsbereich.
- `results/`: rationale Matrizen, Gegenbeispiele und Prüfprotokolle.
- `inputs/`: sieben gepinnte Quellen aus Main nach PR 250.

## Exakt nachrechnen

Python 3.10 oder neuer, keine externen Pakete oder Netzwerkzugriffe:

```bash
python3 -O -B analyze.py
python3 -O -B replay.py
python3 verify_package.py
```

`analyze.py` verifiziert die Quellen und den eingefrorenen Plan und
rechnet die sechs Ergebnisdateien neu. `replay.py` führt die Rechnung
aus Quellen allein in einem frischen temporären Verzeichnis aus und
vergleicht alle sechs Dateien byteweise. Die binären Markierungen sind
ein diskreter Maß-Ersatz, keine kontrollierte Quadratur. Allgemeine
kontinuierliche Aussagen werden analytisch bewiesen, nicht durch den
begrenzten Scan zertifiziert. Die PDF ist mit ReportLab und den
DejaVu-Schriften durch `build_report.py` reproduzierbar.

## Offene nächste Entscheidung

Einen konkreten physikalischen Kandidaten für Präparation, relationalen
Uhrschnitt, Skalarprodukt und Ausleseinstrument begründen und gemeinsam
prüfen. Natürliche Geburtslabels sind keine physikalische Uhr.

Lizenz: Apache-2.0 für die Paketdateien. Externe Literatur ist nur verlinkt.

