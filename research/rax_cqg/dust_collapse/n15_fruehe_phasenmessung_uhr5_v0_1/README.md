# CST-DUST · Eine frühe Phasenmessung der Staubuhr 5

23. November 2026 · N15-Typ 2097151 · markierte Dosis M = 1

Eine frühe projektive Messung der zwei Uhrpakete kann unter einer positiven Hilfspaarung die zwei Dichtepräparationen mit einer Trefferquote von 50,0000803 % unterscheiden. Eine feste Kalibrierung hat einen besonderen Vorteil. Wenn diese Messung hinter Ereignis 11 stattfindet, transportiert die ursprüngliche Verklebung ihre zwei orthogonalen Ergebnisräume durch den Schnitt hinter 12. Eine entsprechend eingestellte zweite ideale Auslese reproduziert das erste Bit auf jedem Zweig mit nichtverschwindender Amplitude. Die physikalische Realisierung der ersten Messung ist offen.

| Frage | Ergebnis | Reichweite |
|---|---|---|
| Können beide Dichtefenster dieselbe frühe Messbasis nutzen? | Ja. Die bewegliche Kalibrierung trennt die Plusbitwahrscheinlichkeiten in jedem Punkt der beiden Fenster auf verschiedenen Seiten von ½. | Positives Hilfsskalarprodukt, gleiche kohärente Präparation der beiden Uhrpakete. |
| Was trägt Uhr 5 selbst weiter? | Bei Kalibrierung auf den festen Referenzwert der Uhr 4 gilt eine exakte Transportidentität für die beiden Projektoren von 11 nach 12. | Ein Schnittschritt, freie Dichte an 12, ursprüngliche Dichtefenster. Die erneute ideale Messung erfordert eine phasenempfindliche Auslese. |
| Wie viel Interferenz bleibt hinter 13? | Beim pulsfreien Vergleich behält die beweglich kalibrierte Messung mit halber Stärke 86,60254 % des ursprünglichen Kontrasts. Bei voller Stärke wechselt das Vorzeichen und der Betrag fällt auf rund 2,09 Milliardstel des Ausgangswerts. | Intervallbeweis für einen festgehaltenen späten Ausgang. Die Zahlen beziehen sich auf die Intensitätsbalance zweier separater Präparationen. |
| Sind physische P3-Daten entstanden? | Das Register enthält 60 × NOT_RUN. | Der Mischer ist eine zusätzliche Operation. Physisches Skalarprodukt und unabhängige Masseneichung bleiben offen. |

## Reproduktion

Im entpackten Verzeichnis laufen die ersten drei Python-Prüfungen mit der Standardbibliothek. Für die beiden letzten ist NumPy erforderlich. Alle Rechnungen laufen lokal auf der CPU.

```sh
sha256sum -c SHA256SUMS
python3 -B modelltest.py
python3 -B paarung.py
python3 -B rueckwirkung.py
OPENBLAS_NUM_THREADS=1 python3 -B messung.py
OPENBLAS_NUM_THREADS=1 python3 -B transport.py
```

`HERLEITUNG.md` enthält Präparation, Norm, beide Kalibrierungen, Transportbeweis und Reichweite der Störungsaussage. `praefix.json`, `transport.json`, `paarung.json` und `rueckwirkung.json` enthalten die Zertifikate bzw. Kontrollwerte. `messung.json` enthält beide numerischen Integrationswege für drei Messstärken und drei Pulswahlen. Die Auswärtsintervalle für den pulsfreien Restkontrast stehen in `rueckwirkung.json`. Die in `quellen/herkunft.json` aufgeführten Dateien sind zum genannten Git-Stand bytegleich übernommen. `quellen/uhr5_ausgang.json` stammt aus dem vorausgegangenen Uhr-5-Prüfpaket. Die drei lokal gehashten Prüfpläne dokumentieren die Reihenfolge von Hauptversuch und Ergänzungen. Es gab keine externe zeitliche Registrierung.

[Repository am geprüften Stand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/f6d78fd5ef60b120da406a92b65b847494fa9cdf/research/rax_cqg/dust_collapse)
