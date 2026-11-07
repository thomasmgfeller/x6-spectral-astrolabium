# CST-DUST: Eichstruktur, Uhrmaß und Randkonsistenz v0.1

7. November 2026. Projektinterne wissenschaftliche Prüfung des unveränderten
endlichen Kandidaten auf Main nach PR 246.

**Ergebnis:** Gemeinsame Umbenennung und vollständig mittransformierte
Uhrverschiebung sind konsistent. Das induzierte Maß relativer Uhren ist exakt
bestimmt. Ein unverändertes rechteckiges Maß nach Zurücksetzen der Referenzuhr,
die freie Entfernung aller Vakuumuhren und das unabhängige Zurücksetzen
gekoppelter Teilgebiete ohne relative Daten sind keine äquivalenten Umschreibungen.

Physikalischer CST-Zustandsraum, dynamische Constraints, Randladungen,
Anomaliefreiheit, Junction-Gesetz, Regularität und globaler Bounce bleiben offen.
Keine neuen dynamischen 4D-Ensembles und keine kostenpflichtigen Rechnungen.

## Nachrechnung

```sh
python3 -O -B analyze.py
python3 -O -B replay.py
```

Die exakten Rechnungen benötigen nur Python 3.10+ und die Standardbibliothek.
Die zusätzliche unabhängige Gleitkomma-Quadratur benötigt SciPy:

```sh
python3 -O -B verify_quadrature.py
```

PDF und Abbildung erneut erzeugen: `python3 build_report.py` mit ReportLab,
Matplotlib, NumPy und den im Skript angegebenen DejaVu-Schriften. Diese
Abhängigkeiten werden nur zur Darstellung benötigt. Das Paket enthält die
fertige PDF und die Abbildung.

## Inhalt und Aussagegrenzen

- `DERIVATION.md`: allgemeine Beweise, genaue Geltungsbereiche und Primärquellen.
- `plan.json`, `plan.sha256`: lokaler Plan vor der Rechnung, keine externe Präregistrierung.
- `supplement_01.json`: offen deklarierte ergänzende Prüfung mit w=1/2.
- `analyze.py`: rationale Algebra und zertifizierte Taylor-Einschließungen.
- `verify_quadrature.py`: ergänzende unabhängige Integration; kein Intervallbeweis.
- `replay.py`: isolierte Reproduktion von sieben exakten Ergebnisdateien.
- `inputs/`: unveränderte Ausgangsdefinitionen, Code und SHA-256-Herkunft.
- `results/`: Einzelbefunde, acht getrennte physikalische HOLD-Entscheidungen,
  quadraturbasierte Kontrolle und Reproduktionsnachweis.
- `MANIFEST.sha256`: Dateiprüfsummen des Pakets, ohne die Manifestdatei selbst.

Der Gültigkeitsbereich der algebraischen Symmetrien ist nicht gleich einem
physikalischen Eichquotienten. Weder die Kovarianz einer regulatorabhängigen
Amplitude noch das neue Pushforward-Maß liefern eine gravitative Quantisierung.
Die vorherige rohe Evolutionsinterpretation bleibt in ihrem geprüften Umfang
verworfen. Ihre Entscheidung wird hier nicht überschrieben.

Lizenz: Apache-2.0 für Projektcode und Dokumentation gemäß dem übernommenen
Repository. Literatur wird nur zitiert und nicht mitgeliefert.
