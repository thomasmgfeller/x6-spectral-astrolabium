# Datenlayout und Reproduktion

Alle NPZ-Dateien enthalten ausschließlich numerische Arrays und sind mit
`numpy.load(path, allow_pickle=False)` lesbar. Koordinaten: float64,
Reihenfolge (t,x,y,z), Einheit L0, nach t sortiert. Operatorantworten und
Quellenamplituden: complex128; keine Farben oder Wahrscheinlichkeiten.

- `clouds_dD_bB.npz`: D=0,1,2 bezeichnet ν4=1024,4096,16384; B=0,1
  enthält je acht Wolken `dD_rII`. Diese sind ausschließlich D8=I((-8,0),0).
  Die sechs Dateien begrenzen die Dateigröße, ohne Rohpunkte zu entfernen.
- `RUNS.json`: alle 48 Identitäten, vollständige Seed-Entropie, N,
  Punktzahlen in D4/D6/D8, Laufstatus, Laufzeit und SHA-256 der Roharrays.
  Intervallzahlen sind ein int32-Vektor pro Wolke und werden reproduziert.
- `sprinklings.npz/values`: (3,16,3,3,4), Achsen Dichte, Realisierung,
  H=(4,6,8), ℓk=(1,1.5,2), vier Feldmoden gemäß Protokoll.
- `mean.npz/values`: (189,3,4), Achsen Parameterzeile aus `MEAN.json`,
  Quadraturordnung (96,192,384), Feldmode. Alle drei Auflösungen bleiben
  erhalten, auch die sechs Zeilen mit QUADRATURE_HOLD.
- `source.npz/query`: 284×4 Koordinaten. Die ersten 28 sind exakt die alten
  Propagationsproben; der Rest sind 256 deterministisch ausgewählte alte
  Abfragepunkte. `old_query_indices` enthält deren Indizes im v0.1-Archiv.
- `source.npz/green`: (3,284,3), Ordnungen 64/128/256, Punkte, Massen 0/1/2.
  `fourier`: (3,28,3), N=64/128/256 auf der Box der Länge 8.
  `old_reference`: (2,284,3), ursprüngliche grobe und feine v0.1-Werte.
- `RESULTS.json` enthält die vollständigen feldweisen 27 Zellen und
  Referenzvergleiche. `DIAGNOSTICS.json` ergänzt Maxima und Quotienten
  für den Bericht; diese ersetzen keine feldweisen Primärwerte.
- `COMPUTE.json`, `MEAN.json`, `SOURCE.json`, `SPRINKLING_COMPUTE.json`
  speichern Laufzeit beziehungsweise Ressourcen. Zeiten sind keine festen
  Reproduktionstargets.

Die Mittelwerte μH sind numerische Auswertungen einer exakten Formel.
Die Namen der Biasfelder in `RESULTS.json` sind deshalb stets zusammen mit
den Quadraturstatus- und Abschneideangaben aus `MEAN.json` zu lesen.
SEM ist deskriptiv und liefert keine garantierte Konfidenzüberdeckung.
Alle wissenschaftlichen Gates bleiben HOLD oder NOT_RUN.

`run.py all --out /tmp/...` wiederholt die festgelegten Entwicklungsdaten.
`audit.py --replay` prüft alle 48 Wolken, die feinste vollständige
Erwartungswertmatrix, die feinste Ortsraumreferenz, alle drei neuen Fourier-
Auflösungen und die Ergebniszusammenfassung. Es ist interne Reproduktion,
keine unabhängige externe Begutachtung.
