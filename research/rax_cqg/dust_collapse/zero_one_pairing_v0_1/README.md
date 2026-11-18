# CST-DUST · Gemeinsame Norm für null und ein inneres Ereignis

[Bericht (PDF)](../reports/CST_DUST_Null_Und_Ein_Ereignis_Norm.pdf) · [Offline-Prüfpaket (ZIP)](../packages/CST_DUST_Null_Und_Ein_Ereignis_Pruefpaket.zip) · [Vorstudie zur Zwischenrandnorm](../seam_pairing_v0_1/README.md)

Der Bericht untersucht eine offene Voraussetzung der Endklassifikation. Legen die gemeinsame Randwirkung, die Einheitsnorm des Nullzweigs und die bereits verwendeten Messpakete das relative Normquadrat des Ein-Ereignis-Zweigs fest?

Zwei positive Skalarprodukte erfüllen diese Bedingungen und liefern bei drei erhaltenen Paketpaarungen und Uhrfenster `d = 1/8` die verschiedenen Werte 0,000636203548 und 0,000614789365. Die Bessel-Ungleichung begrenzt zugleich, wie viele weitere ursprüngliche Paarungen ein solches Produkt erhalten kann. In der angegebenen orthonormalen Hermite-Folge überschreitet die Summe beim 2 238. Paket erstmals eins.

## Voraussetzungen und Reichweite

Beide Zweige haben dieselben vier äusseren Ereignisse, dasselbe Eingangsgrundpaket und dasselbe Dichteatom am Ausgang. Das innere Uhrereignis wird im Ein-Ereignis-Zweig kohärent über das Zeitfenster integriert. Für den Nullzweig wird die veröffentlichte Wirkung auf den sieben eingeschränkten Ordnungen neu berechnet. Ihre Vergleichsgewichte folgen aus den Häufigkeiten innerhalb der 33 Ein-Ereignis-Ordnungen. Die Verbindung zwischen diesem endlichen Randmodell und dem leeren Präfix der offenen Uhr bleibt offen. Eine Auswahl der physikalischen Geburtsrate oder einer Endklasse setzt weitere Daten voraus.

## Nachrechnung

Im Verzeichnis dieser Studie oder im entpackten Prüfpaket ausführen. Für die Hauptrechnung genügt die Python-Standardbibliothek. Die separate numerische Gegenprobe benötigt zusätzlich NumPy. Die Referenzausgabe wurde mit Python 3.12.14 und NumPy 2.3.5 geprüft.

```sh
python3 -B vergleich.py --out nachrechnung.json
cmp ergebnis.json nachrechnung.json
OPENBLAS_NUM_THREADS=1 python3 -B gegenprobe.py
```

Im entpackten ZIP kontrolliert zusätzlich `sha256sum --check SHA256SUMS` alle ausgelieferten Dateien. Die Hauptrechnung prüft auch die Git-Kennungen der ursprünglichen Eingaben. Der Bytevergleich prüft die Reproduktion im Referenzumfeld. Einige ergänzende Zahlen verwenden Gleitkommaarithmetik und können plattformabhängig in der letzten Stelle variieren.

## Inhalt

| Datei | Zweck |
|---|---|
| `CST_DUST_Null_Und_Ein_Ereignis_Norm.pdf`, `bericht.tex` | Bericht, Herleitung, Quellen und bearbeitbarer Satz |
| `vergleich.py` | Aufbau beider Zweige, 1 600 geordnete Historienpaare, Paketpaarungen und Uhrvergleich |
| `schranken.py` | Rationale Einschliessungen der Staubantwort und des Normquotienten |
| `paketgrenze.py` | Rationale Bessel-Schranken und erster Index oberhalb der Einheitsnorm |
| `gegenprobe.py` | Numerische Kontrolle aus den vollen Wirkungen, einschliesslich 6 400 Paarintegralen |
| `ergebnis.json` | Referenzwerte, rationale Intervalle und Status der physikalischen Normierung |
| `quellen.json` | Git-Kennungen und Repository-Pfade der verwendeten Eingaben und Hilfsfunktionen. Im Offline-Paket liegen die Eingaben bei. |
| `SHA256SUMS`, `LICENSE` im Offline-Paket | Dateiprüfsummen und [Apache-2.0-Lizenz](../amplitude_existence_v0_1/LICENSE) |

[Quellenstand nach PR 308](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/8222202f6b27a60218afe6cfbf1a5b8c7be423ea/research/rax_cqg/dust_collapse)
