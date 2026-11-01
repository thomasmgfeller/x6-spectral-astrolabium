# Eigenzeit · Eine Ordnung aus 128 Ereignissen

Aus einer einzelnen unbeschrifteten Kausalordnung soll ein Test zwischen einem flachen und zwei de-Sitter-Diamanten wählen. Im vollständig beobachteten 4D-Diamanten, bei fester Ereigniszahl und gleichmäßiger Beprobung nach physischem Volumen, blieben bei 11.551 von 12.288 frischen Einzeltests alle drei Kandidaten zulässig.

[Einzelordnungen im Browser ansehen](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/eigenzeit-einzelordnung/index.html) · [Forschungsbericht (PDF)](Eigenzeit_Einzelordnung_128_v0_1.pdf) · [Vollständiges Prüfpaket (ZIP)](Eigenzeit_Einzelordnung_128_v0_1_Pruefpaket.zip)

| Dimensionslose Krümmungen RT² | Höchstmögliche Trennleistung bei N = 128¹ | Notwendige Ereigniszahl für 80 % |
|---|---:|---:|
| 0 und 0,758 | 7,66 % | 150.272 |
| 0 und 3,131 | 15,82 % | 8.999 |
| 0,758 und 3,131 | 13,18 % | 15.775 |

¹ Sichere Obergrenzen bei höchstens 5 % Fehlalarm. Sie gelten für jedes Verfahren aus dieser Ordnung. Die notwendigen Elementzahlen garantieren keine hinreichende Trennleistung. Von 113 eindeutigen Ausgaben des kalibrierten Paarzähltests waren 44 richtig. Der lokale Prüfvertrag ging der Simulation voraus. Eine externe Replikation steht aus.

[Herleitung](DERIVATION.md) · [Einzelwolken und Kalibrierauswertung](result.json) · [Analytische Gegenrechnung und Budgetgrenzen](audit.json) · [Veröffentlichungsnachweis](PUBLICATION.json)

## Prüfen und wiederholen

Im Repository prüft der folgende Befehl sämtliche Paketdateien, die Übereinstimmung mit der Browseransicht und die Entscheidungen aus allen archivierten Ordnungen.

```sh
python3 research/eigenzeit/single_order_128_v0_1/publication_check.py
```

Im entpackten ZIP stehen der eingefrorene Vertrag, der vollständige wissenschaftliche Quellcode, die unabhängige Kalibrierbank, die Rohordnungen und die Anleitung für den vollständigen Simulationslauf in `README.md`. Die Ansicht lässt sich mit `Ansicht.html` auch offline öffnen.
