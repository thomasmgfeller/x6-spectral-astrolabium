# CST-DUST · Was die Phase der Staubuhr 5 auslesen könnte

23. November 2026 · Endliche Ordnung 2097151 · markierte Dosis 1

Die ursprünglichen N15-Quellen und ihre Wirkungsableitungen erhalten bis zur Pulswahl den Paketträger der Uhr 5. Unter der bisher verwendeten positiven Hilfsnorm liefert jeder so erzeugte frühe Ergebniseffekt dieselbe Statistik für die beiden entgegengesetzten Phasenzustände. Eine Auslese des zur Uhr konjugierten Fourier-Impulses würde die nötige Verbindung zwischen den Paketen herstellen. Sie ist ein neuer, explizit prüfbarer Randzugriff.

| Prüfung | Befund |
|---|---|
| Frühe Uhr- und Quellenmessung | Kleinster maximaler Fehler eines phasenblinden Effekts gegenüber der idealen projektiven Phasenauslese auf allen Zweipaketzuständen gleich ½. |
| Physisch zu begründender Übergang | Kleinster Abstand zwischen den Trägern in u₅ rund 0,001952641. Eine Translation um 0,002074711 bringt die Mittelpunkte zur Deckung. |
| Hypothetische periodische Impulsauslese | Maximaler Kontrastfaktor 2/π innerhalb der untersuchten periodischen Impulseffekte. Bei gleichen Vorwahrscheinlichkeiten 50,00005113 % richtige Einzelzuordnungen der alten Dichtefenster. |
| Zustand nach dieser projektiven Auslese | 29,73576327 % der Hilfsnorm gelangen bei ungelesenem Ergebnis aus den beiden Paketfenstern. Die Fortsetzung dieser Komponente erfordert zusätzliche Randdaten. |
| Positive Mischung später, einzeln festgehaltener Enddaten | Jede geprüfte Mischung bevorzugt dieselbe relative Phasenrichtung. Sie liefert auf dem untersuchten Zweimodenraum keine Norm, welche die beiden idealen frühen Phasenergebnisse orthogonal macht. |
| P3 | 60 × NOT_RUN. Der physisch zugelassene Zugriff auf den konjugierten Impuls, das physikalische Skalarprodukt und die unabhängige Masseneichung sind offen. |

## Reproduzieren

Alle Prüfungen laufen lokal auf der CPU. Die Intervalle und die Wirkungsidentitäten erfordern nur die Python-Standardbibliothek. Die unabhängigen Integrationen verwenden zusätzlich NumPy.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
OPENBLAS_NUM_THREADS=1 python3 -B auslese.py
```

HERLEITUNG.md beschreibt den Beweis, die Vergleichspräparationen, die Grenzen der Modellrechnung und die Anforderungen an einen physischen Eingriff. exakt.json enthält rationale Intervallgrenzen. auslese.json enthält beide Integrationen, eine direkte Fourier-Kontrolle sowie eine phasenblinde Gegenprobe. In quellen/herkunft.json stehen Commit, Git-Blob-IDs und SHA-256 der Referenzen sowie die verwendeten Auszüge der vorangegangenen Rechnung. Der lokal gehashte Prüfplan besitzt keinen externen Zeitstempel.

[Geprüfter Stand der Staubball-Rechnungen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/f6d78fd5ef60b120da406a92b65b847494fa9cdf/research/rax_cqg/dust_collapse)
