# MIT-Multimode-Glasfaser im Stabilitätslab

Li-Yu Yu und Sixian You haben die Übertragung einer Gradientenindex-Multimodefaser experimentell kalibriert. Die Datei `complexTM.hdf5` enthält die komplexen Feldkoeffizienten für zwei orthogonale Ausgangspolarisationen. Im Stabilitätslab öffnet „Glasfaser“ einen Ausschnitt für einen einzigen Ausgangsort (Zeile 0) und zwei Eingangskanäle (Spalten 0 und 1). Die Auswahl ist fest und richtet sich weder nach Intensität noch nach vermuteter Auslöschung.

## Automatischer Import

Im Repository-Hauptverzeichnis, mit Python 3.12 unter Linux oder macOS:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r agent/hanford-requirements.txt
python -m agent.dryad_fibre
```

Der Import fragt die öffentliche Dryad-API nach der DOI und dem festen Versionsdatensatz 296860. Er prüft Dateiname, Länge und SHA-256 des Dateieintrags 3201802. Ohne Zugangsdaten bezieht er die Bytes aus der von Dryad auf Zenodo gepflegten Erhaltungskopie. Dazu prüft er die DOI, die Zugehörigkeit zur Dryad-Community und den Dateieintrag auch auf Zenodo. Mit einem lokal gesetzten `DRYAD_API_TOKEN` verwendet er den Dryad-Download. Der Token wird nur an die Dryad-Domain gesendet. Ein vorhandenes Original lässt sich mit `python -m agent.dryad_fibre --file /pfad/complexTM.hdf5` einlesen.

Der erste vollständige Abruf lädt 773.234.336 Bytes und speichert das Original standardmässig unter `runs/dryad-fibre/`. Bei weiteren Läufen wird der lokale Cache erneut per SHA-256 geprüft. `--cache` und `--archive` ändern die Ziele. Jeder vollständige Lauf speichert den geprüften Ausschnitt, die Quellenangaben und fünf berechnete Phasenstellungen atomar in `app/causal-stability/fibre-data/record.json`. Ein fehlgeschlagener Download oder ein reiner Metadatenlauf (`--metadata-only`) lässt einen bereits verifizierten Ausschnitt erhalten. Auf der veröffentlichten Seite benötigt der Browser nur diese kleine JSON-Datei.

## Bedeutung der Anzeige

Für jede Polarisation p und Koeffizienten aₚ, bₚ berechnet das Lab das Ausgangsfeld für zwei gleich starke Eingänge mit gemeinsamer Eingangsleistung eins.

```text
Eₚ = (aₚ + exp(iφ) bₚ) / √2
φ = π + arg(a₁) − arg(b₁) + δ
Iₚ = |Eₚ|²
Igesamt = I₁ + I₂
```

δ ist die im Browser veränderte Phase. T1 wird relativ zu seiner konstruktiven Referenz (|a₁|+|b₁|)²/2 dargestellt. T2 trägt separat zur Gesamtintensität bei. Die komplexen Matrixelemente kommen aus der veröffentlichten Messung. Die Intensitäten sind Modellvorhersagen in relativen Einheiten. Eine unabhängige Auslesung der vorhergesagten Auslöschung oder ein statistischer Schwankungsnachweis wäre ein weiterer Versuch.

Die beiden Originalmatrizen haben je 12.449 Zeilen und 1.941 Spalten, Datentyp complex128. Aus dem festgelegten Ausschnitt ergeben sich bei δ = 0°, +10° und +30° relative T1-Intensitäten von 7,451 %, 8,154 % und 13,651 %. Bei 0° bleibt wegen der ungleichen Beträge beider Eingangskoeffizienten Restlicht übrig. Diese Zahlen gelten für die ausgewählte Zeile und das gewählte Eingangspaar.

## Daten und Nachprüfung

- [Yu & You, Originaldatensatz und Zitierangaben](https://doi.org/10.5061/dryad.wdbrv15wk). Dryad führt die Daten unter CC0-1.0.
- [Dryad-Dateimetadaten](https://datadryad.org/api/v2/files/3201802) und [Dryads Erhaltungskopie auf Zenodo](https://zenodo.org/records/11399077)
- [Beschreibung der Dryad-Zenodo-Partnerschaft](https://zenodo.org/communities/dryad/about)
- [Software der Autoren](https://doi.org/10.5281/zenodo.10795289) und [Publikation in Science Advances](https://doi.org/10.1126/sciadv.adn2846)

SHA-256 der vollständigen Originaldatei: `3006be2727f3e5761219b02c1c28eef2955a04f09f3c01f9c88d1adbe042ae6f`.
