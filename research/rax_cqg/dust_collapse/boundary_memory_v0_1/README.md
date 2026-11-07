# CST-DUST: Randgedächtnis und exakte Fortsetzung v0.1

Die vollständige Vergangenheit ergibt eine hinreichende Darstellung der
geerbten endlichen Amplitude. Der Wirkungszuwachs eines neuen maximalen Elements
und der korrekte Faktor für natürliche Labels sind hergeleitet und geprüft.
Der Operator bewahrt alte Feldvariablen und fällt deshalb nicht unter das
vorherige Hindernis für beschränkte integrierte Kerne.

Das ist eine exakte Umschreibung, keine neue physikalische Wachstumsdynamik.
Ein fester oberer Ordnungskragen ist für alle zukünftigen Ideale nicht
geschlossen. Lokale Schrittnormierung verändert die ursprünglichen Amplituden.
Positive endliche Schnittprodukte hängen von Horizont und gewähltem Endprodukt
ab. Ein physikalischer Labelquotient, die unabhängige Normauswahl und die
unendliche Fortsetzung bleiben offen. Alle acht physikalischen Gates sind HOLD.

## Reproduktion

```bash
python3 -O -B analyze.py
python3 -O -B replay.py
```

Python 3.10+, nur Standardbibliothek. Fünf Ergebnisdateien werden isoliert
bytegleich erzeugt. `DERIVATION.md` enthält allgemeine Beweise und Bedingungen;
`boundary_contract.json` enthält den expliziten Zustands- und Fortsetzungsvertrag.
Die natürlichen Labels sind Rechenmarkierungen, keine physikalische Eigenzeit.

408 natürliche innere Ordnungen, 407 Erweiterungen, 2 442 rationale
Wirkungsfälle, sechs vollständig abgeglichene Labelsummen, acht Kragenzeugen
und 30 positive Endprodukt-Rückzüge sind ausgeführt. Die einzelnen Untertests
und die 268 Austauschdiamanten stehen in `results/finite_growth.json`.
Es gibt keine neuen 4D-Dynamikensembles, zufälligen Messdaten oder statistischen
Vorhersagen. Allgemeine Beweise sind nicht formal maschinenverifiziert.

Der lokale Plan wurde vor der Rechnung gehasht; die Mechanismen waren bekannt.
Keine externe Präregistrierung oder blinde Vorhersage. Sieben Vorgängerquellen
sind bytegleich auf Main nach PR 248 gepinnt. Die ursprünglichen Artefakte
bleiben unverändert. Der PDF-Bericht fasst den Modellvertrag und die Ergebnisse
zusammen; vollständige Nachweise und Quellen liegen im Prüfpaket.

## Bericht und Paket

`python3 -B build_report.py` erzeugt Abbildung und PDF (zusätzlich Matplotlib,
ReportLab und DejaVu-Schriften unter `/usr/share/fonts/truetype/dejavu/`).
`python3 -B package.py` erzeugt das ZIP mit vollständigem SHA-256-Manifest.
Vorschaubilder und Python-Caches sind vom Paket ausgeschlossen.
