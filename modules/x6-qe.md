# X6-QE: exakte Graphreferenzen und Grenzen spektraler Unterscheidbarkeit

Registerstand: 2026-10-16. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 7ea315830f9c5ccee8bad5bebfaa7666c342e3d5

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7ea315830f9c5ccee8bad5bebfaa7666c342e3d5/research/x6_qe/README.md)

## Dokumentierte Aussage

Vier Graphen in drei bekannten Referenzen: Stern mit trivialer Ihara-Zeta; primitiver Viererzyklus mit zusammengesetzter Länge; Turmgraph/Shrikhande mit gleichem Spektrum und gleicher globaler Ihara-Zeta, aber K4=8/0. Keine neue Mathematik, Quantengedächtnis- oder Arithmetikbehauptung.

- [research/x6_qe/evidence/local-results.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7ea315830f9c5ccee8bad5bebfaa7666c342e3d5/research/x6_qe/evidence/local-results.json): Vollständige exakte Polynome, getrennte Determinantenprüfungen und K4-Zählwege, Quellenhashes und Fehlerkontrollen. Interne Rechnung; keine personell unabhängige Wiederholung.

## Reproduzieren

Python 3.12, nur Standardbibliothek. Für gemeinsame Suite zusätzlich Node.js 24. Neue Ausgabewege; keine Downloads/Wolfram-Aufrufe.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-x6-qe
cd x6-x6-qe
git checkout --detach 7ea315830f9c5ccee8bad5bebfaa7666c342e3d5
python3 -S -B research/x6_qe/verify.py --output /tmp/x6-qe.json
python3 -S -B research/x6_qe/verify.py --verify-report /tmp/x6-qe.json
```

Erwartete Ausgabe: PASS_WITH_SCOPE_LIMITS; 3 Referenzfälle, 4 Graphen, 12 Umbenennungen, 21 zurückgewiesene Fehlerfälle. Fehler: Exit 1.

## Offene Prüfung

Externe Wiederholung des eingefrorenen Umfangs; vor Spider-/Billiard-Auswertung Originalbild/Erzeugungsregel beschaffen und eigenen Numerikvertrag qualifizieren. Lorentz-n=7 bleibt Priorität.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
