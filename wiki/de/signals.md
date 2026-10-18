# Signale und Filter verstehen

Eine ruhigere Kurve ist nicht automatisch eine bessere Messung. Entscheidend ist, ob die wichtige Information erhalten bleibt.

[English](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/signals.md) · [Wiki-Übersicht](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/)

Quellenstand: 2026-10-18 · `e947dfbdd49890dcb119940548537d1db59272c2`

## Vom Signal zum Spektrum

Ein Signal ist eine Folge von Werten über die Zeit, zum Beispiel eine gemessene Schwingung. Ein Spektrum zeigt, welche Frequenzanteile darin vorkommen. Die Fourierzerlegung beschreibt das Signal mithilfe von Schwingungsbausteinen.

Die Amplitude sagt, wie stark ein Anteil ist. Die Phase beschreibt seine Lage im Schwingungszyklus. Ein Leistungsspektrum allein enthält deshalb nicht alles, was zur Rekonstruktion der ursprünglichen Zeitkurve nötig ist.

## Vier Verfahren, ein fairer Eingang

| Verfahren | Was es tut | Worauf du achten solltest |
| --- | --- | --- |
| Identität | Lässt den Eingang unverändert. | Referenz für den Zustand ohne Filter. |
| Gleitender Mittelwert | Mittelt benachbarte Werte. | Kann kurze Impulse und Amplitude abschwächen. |
| FFT-Tiefpass | Entfernt Anteile oberhalb einer Grenzfrequenz. | Kann auch nützliche hohe Frequenzen entfernen; Randartefakte sind möglich. |
| X6-Phasenfilter | Wählt Fourieranteile anhand ihres Winkels aus. | Ist kein gewöhnlicher Tiefpass und kann ein sauberes Sollsignal entfernen. |

Diese Vergleiche arbeiten mit vollständigen gespeicherten Signalen. Der zentrierte Mittelwert nutzt auch spätere Werte und ist so kein unmittelbar kausaler Echtzeitfilter. Aus einer guten Offlinekurve folgt keine Eignung für eine schnelle Maschinenregelung.

## Welche Zahlen helfen?

| Kennzahl | Einfach erklärt |
| --- | --- |
| RMSE | Typischer Fehler auf der Skala des Signals; kleiner ist meist besser bei gleichem Ziel. |
| NRMSE | Fehler relativ zur festgelegten Referenznorm; die genaue Definition zählt. |
| PSD | Verteilung der Signalleistung über Frequenzen. |
| Kohärenz | Frequenzbezogene lineare Übereinstimmung; allein keine Rekonstruktionsgarantie. |
| Phase und Zeitversatz | Ob Schwingungen passend liegen und eine Ausgabe früher oder später ankommt. |

Ein anschauliches Gegenbeispiel ist y = −x: Die Kurve ist umgekehrt. Ihr Leistungsspektrum bleibt gleich, und die Betragsquadrat-Kohärenz kann eins sein. Trotzdem ist das ursprüngliche Signal nicht korrekt rekonstruiert. Deshalb prüft X6 mehrere Kriterien gemeinsam.

## So wird der Versuch aussagekräftig

- Verändere zunächst jeweils einen Parameter.
- Vergleiche alle Verfahren mit derselben bekannten Referenz.
- Prüfe kurze Ereignisse und Phasenlage zusätzlich zum Rauschen.
- Bewahre Seed, Einstellungen, Rohdaten und Prüfbericht zusammen auf.
- Übertrage ein synthetisches Ergebnis erst nach neuen Prüfungen auf reale Sensoren.

- [Signal Lab](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/signal-lab.html)
- [Kennzahlen und Grenzen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SIGNAL_LAB_METHODS.md)
- [Gegenprüfung der Polaritätsumkehr](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/signal-lab/wolfram-polarity-v0.1/README.md)
