# N15 · Uhr 11 als früher Zeiger für die beiden Pakete der Uhr 5

**24. November 2026.** Die frühe N15-Wirkung, die disjunkten Pakete und die Dichtefenster stammen aus [PR 363](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/363). Bei beibehaltener Uhr 5 ist eine diagonale Auslese des Uhr-11-Fensters unter der positiven Hilfsnorm phasenblind. Bei zusätzlicher kohärenter Zusammenfassung beider Pakete zum gleichen Zeigerausgang liegt die normierte Spaltenüberlappung dagegen für jede gemeinsame positive skalare Gewichtung bei mindestens 0,999987156. Den zur Vollständigkeit nötigen Gegenbeitrag liefert im Vergleichsgerät die Projektion auf den gesamten orthogonalen Rest. Der Wirkungsvertrag begründet diesen Eingriff und die physische Wahrscheinlichkeit bislang nicht.

Eine zulässige Fortsetzung mit dem ursprünglichen Paar 5→12 zeigt an den vollen Uhrpaketen, dass die frühe gemeinsame Amplitude allein die spätere lineare Auswertung auf dem Zweimodenraum nicht bestimmt. Die normalisierte Determinante liegt über 0,00102615. Die 60 physischen P3-Prüfpunkte stehen auf NOT_RUN.

[Kurzbericht](Kurzbericht.pdf) · [Herleitung und Geltungsbereich](HERLEITUNG.md) · [Strenge Schranken](schranke.json) · [Numerische Gegenrechnung](zeiger.json)

## Nachrechnen

Für Quellen- und Intervalltest genügen Python ab 3.10 und seine Standardbibliothek. Der numerische Test benötigt ausserdem NumPy. Alle Eingaben sind im Paket. Die beiden Befehle schreiben ihre Ergebnisse als JSON auf die Standardausgabe. Auf unterschiedlichen Plattformen können sich die hintersten Gleitkommastellen unterscheiden.

```sh
sha256sum -c SHA256SUMS
python3 -B schranke.py
OPENBLAS_NUM_THREADS=1 python3 -B zeiger.py
```

`herkunft.json` identifiziert die eingefrorenen Quellen. `quellen/LICENSE` und `quellen/NOTICE` begleiten die übernommenen Dateien. Mit `OPENBLAS_NUM_THREADS=1 python3 -B verifizieren.py` werden zusätzlich die Neuberechnungen mit den archivierten Ergebnissen verglichen. Die zwei lokalen Prüfpläne halten die Reihenfolge von Hauptprüfung und Anschlusszeugen fest.
