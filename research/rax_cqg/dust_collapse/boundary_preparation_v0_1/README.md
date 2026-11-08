# CST-DUST: Randpräparation und Reaktionsbilanz v0.1

Eine passende Randphase trägt die notwendige mittlere Reaktion des Kragens
aus PR 266. Ihr Phasengradient wählt höchstens ein inneres Paar (t,w) am selben
Kragen; er muss als zusätzliche physikalische Randinformation begründet werden.
Ein normiertes Cosinus-Paket liefert einen expliziten Zeugen endlicher Breite.
Der nichtverschwindende Kommutator zwischen innerer Uhrfunktion und dem hier
zusätzlich getesteten Randoperator begrenzt die gemeinsame Genauigkeit.

**Alle acht physikalischen Gates bleiben HOLD.** Die physikalische Präparation,
das physikalische Skalarprodukt und die Constraintalgebra sind nicht abgeleitet.
Kein Bounce, kein n=5-Produktionslauf, keine kostenpflichtige Rechnung.

Basis: Main nach [PR 266](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/266),
`8d1a3e0906611ec23fdee3088a6bf864d0bd9edc`. 8. November 2026 (Zürich).

## Lesen

- `CST_DUST_Randpraeparation_Reaktionsbilanz_v0_1.pdf`: kompakter Bericht.
- `DERIVATION.md`: vollständige Annahmen, Beweise und Gültigkeitsgrenzen.
- `boundary_contract.json`: maschinenlesbarer Status und Anspruchsgrenzen.
- `inputs/`, `provenance.json`: vier geerbte Quellen, unverändert und commitgebunden.

## Reproduzieren

Python 3, nur Standardbibliothek für die wissenschaftlichen Kontrollen:

```sh
python3 -B verify_package.py
python3 -B replay.py
```

`analyze.py` erzeugt drei deterministische Ergebnisdateien. `package.py` baut
das ZIP mit festen Metadaten. `build_report.py` benötigt für die optionale
PDF-Neuerstellung ReportLab und DejaVu-Schriften. Die PDF-Erstellung ist
kein Bestandteil der wissenschaftlichen Nachrechnung.

27 stationäre Fälle, 729 Randstörungen, 2916 Wirkungs- und 2916
Phasenableitungen, 108 Kommutatorkoeffizienten, 108 getrennte Phasenpaare,
neun rational eingeschlossene Paketbudgets und sechs Negativkontrollen.
Der gehashte Plan ist nach analytischem Entwurf, vor Ausführung festgehalten;
keine externe Präregistrierung, keine externe Replikation.

Nächster physikalischer Schritt: Randamplitude aus einer begründeten
Materie-/Außenraumkopplung oder vollständige kanonische Reduktion herleiten.
Die hier passende Phase ist ein mathematischer Prüfzustand, keine solche Herleitung.
