# CST-DUST: Expansion und Trapping v0.1

**Ausgeführt: klassische Referenzdiagnostik. Physikalische CST-Entscheidung:
HOLD_NOT_ELIGIBLE / NOT_RUN. Regularität: separat HOLD.**

Für die bereits geprüfte, marginal gebundene Einstein-Staub-Referenz werden
Staubexpansion, beide Null-Expansionen runder Symmetrieflächen, Trapping und die
einseitige Klassifikation der marginalen Röhren untersucht. Der endliche Ball
wird an seinen Schwarzschild-Außenraum angeschlossen. Die Zukunft außerhalb
des freigegebenen Zeitfensters wird nicht zur Ereignishorizontbestimmung benutzt.

## Nachrechnung

Python 3.12 oder neuer, ausschließlich Standardbibliothek:

```sh
python3 -O -B analyze.py
```

Das Skript prüft eingefrorenen Plan und Herkunftshashes, propagiert die
archivierten Fehlerintervalle, vergleicht eine unabhängige Flächenableitung
entlang radialer Nullstrahlen und schließt Ereigniszeiten auf vier numerischen
Gittern ein. `-O` deaktiviert keine Kontrolle. Für Bericht und Figuren:

```sh
python3 -m pip install -r report-requirements.txt
python3 build_report.py
```

Zusätzlich werden DejaVu-Schriften benötigt. Die PDF-Ausgabe liegt unter
`../output/pdf/`; das fertiggestellte PDF ist auch im Paket enthalten.

## Inhalt und Grenzen

- `plan.json`, `plan.sha256`: lokaler Plan-Freeze vor der Rechnung, keine externe Präregistrierung.
- `DERIVATION.md`: vollständige Definitionen, Ableitungen, Fehlerregeln und Quellen.
- `analyze.py`, `intervals.py`: deterministische Rechnung mit nach außen gerundeten Intervallen und exakten rationalen Wurzelschranken.
- `inputs/`: unveränderte veröffentlichte Vorgängerdaten mit Herkunfts- und Dateihashes.
- `results/`: Expansionen, Ereigniseinschließungen, Negativkontrollen und getrennte P4-Entscheidungen.
- `figures/`: aus den Referenzgleichungen erzeugte wissenschaftliche Darstellungen.
- `SHA256SUMS`: Inhaltsprüfsummen des vollständigen Pakets, ohne Selbsthash.

420 innere Kugelfälle, 420 Außenraum-Prüfplätze mit expliziter Gebietsprüfung,
216 Flächenableitungen und 12 numerische Ereigniseinschließungen sind dokumentiert.
Die absolute numerische Toleranz bezieht sich auf `e = R theta / 2`, nicht auf
einen relativen Fehler einer gegen null gehenden Expansion. 72 P4-Datensätze
behalten alle physikalischen CST-Gates separat auf HOLD.

Kein neues CST-Ensemble, keine physikalische Dichteverfeinerung und keine
Singularitätsauflösung. Ein fehlender runder Trapping-Nachweis schließt weder
allgemeine nicht-runde gefangene Flächen noch einen globalen Ereignishorizont aus.
