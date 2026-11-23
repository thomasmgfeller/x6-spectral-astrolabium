# N15 · Die Randpaarung hinter Ereignis 13

**24. November 2026.** Untersucht wird die frühe Zweipaketpräparation im Staubball beim ersten gewöhnlichen Schnitt, der Uhr 5 vollständig integriert. Die beiden letzten Paarbeiträge 5→12 und 5→13 hinterlassen an den zentralen Uhren und Dichten zusammen genau 1/2736 rad relative Phase. Über alle geprüften Fenster bleiben die beiden Ausgangsspalten bei jeder gemeinsamen positiven diagonalen Gewichtung fast parallel. Für den angegebenen vollständig durchgerechneten Referenzfall läge das nötige Gewichtungsverhältnis einer neuen orthogonalisierenden Paarung bei rund 42 Millionen zu eins.

Beim üblichen kohärenten Abschluss von x₁₂ hängt die aus dem späteren Randgewicht berechnete Statistik der Uhr 11 geringfügig von der rechten Pulswahl ab. Bleibt der Wert x₁₂ bis zur Bildung von Gewichten aufgelöst, fällt die Pulsphase für jeden Dichtewert exakt heraus. Zwei und vier Dichteklassen werden als Zwischenfälle geprüft. Die physische Entstehung eines solchen Records, die frühe Messkopplung und die unabhängige positive Masseneichung sind offen. Alle 60 P3-Prüfpunkte führen NOT_RUN.

[Kurzbericht](Kurzbericht.pdf) · [Herleitung, Definition des Randmasses und Grenzen](HERLEITUNG.md) · [Strenge Fensterschranken](einschluss.json) · [Ergebnisse der Randrechnung](randtest.json) · [Dichte- und Pulsvergleich](dichte.json)

## Reproduktion

Für die Intervallschranken reicht Python ab 3.10 mit der Standardbibliothek. Für die numerischen Prüfungen wird zusätzlich NumPy benötigt. Alle Eingaben sind beigefügt. Der erste Befehl überprüft die archivierten Bytes. Der zweite wiederholt die Rechnung mit einem BLAS-Thread, vergleicht Schranken und Quadraturen und prüft den früher publizierten zentralen N15-Fall bei drei Pulsen.

```sh
sha256sum -c SHA256SUMS
OPENBLAS_NUM_THREADS=1 python3 -B verifizieren.py
```

Einzelaufrufe von `einschluss.py`, `randtest.py` und `dichte.py` geben JSON auf die Standardausgabe aus. Die Pulse verändern ausschliesslich die rechte Verwendung von Uhr 6. Die neue Klasseinteilung für x₁₂ ist ein Vergleich möglicher Randverträge. Die drei lokalen Prüfpläne dokumentieren die Reihenfolge der Hauptrechnung und der Ergänzungen.
