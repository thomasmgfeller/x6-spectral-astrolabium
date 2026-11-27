# Kann ein positives Zukunftsereignis die geometrische Halbsonde stationär machen?

Für die drei in PR 413 geometrisch trennenden Bahnen und die beiden veröffentlichten Randpräparationen ergibt sich am exakten Halbschnitt **kein stationäres Feld**. Der Ausschluss umfasst jede Erweiterung, die genau ein positives, freies Innenereignis 23 mit 22 ≺ 23 einfügt und die N23-Ordnung als induzierte Teilordnung erhält. Das Ergebnis gilt sowohl für eine leere als auch für eine positive Sonde 22.

| Präparation | Start → Durchgang | Terminales 23 | 23 mit altem Nachfolger | Ausgeschlossen |
|---|---|---:|---:|---:|
| schwer | 3 → 11 | 108 | 366 | 474 |
| schwer | 4 → 11 und 5 → 11 | 128 | 438 | 566 |
| leicht | 3 → 11, 4 → 11 und 5 → 11 | 108 | 366 | 474 |

Die 1 514 Zeilen zählen Kombinationen aus Präparation und beschrifteter Erweiterung. Bahnen mit identischer Ausgangsordnung und Präparation teilen dasselbe Register. Die 22 alten Ereignisse sowie die geometrische Sonde 22 ergeben N23, der Helfer die neue N24-Ordnung. Der Durchgangspunkt ist stets 11.

## Bedingungen und Vollständigkeit

Fest sind nur die archivierten Kragenbedingungen, die Nullquellen, die vier Gerätekorrekturen, die Besetzungssektoren und die Ordnung. Die alten inneren Uhren und positiven Gewichte dürfen sich neu einstellen. Es gilt exakt 2 Y22 = Y3 + Y7. Die Ereignisse 15, 17 und 20 haben Gewicht null. Ereignis 23 ist frei, ungetrieben und positiv mit 0 < w23 ≤ 1. Die im Vergleichspaar archivierten inneren Feldlösungen dienen nicht als Eingangsboxen. Die frühe Projektion berechnet ihre eigenen notwendigen Grenzen. Für die leichte Präparation skaliert der Prüfer sämtliche Gewichte der homogenen Uhrgleichungen einheitlich mit 16.

Die alte Zukunft von 22 ist die Kette 7 ≺ 8 ≺ 9 ≺ 10. Die Zukunft von 23 muss deshalb eine ihrer fünf Endstrecken sein, einschließlich der leeren. Seine Vergangenheit ist ein Ideal der N23-Ordnung, das 22 enthält. Jedes Vergangenheitsereignis muss unter jedem alten Zukunftsereignis liegen. Diese Bedingungen sind notwendig und hinreichend für eine induzierte Erweiterung. Die Gegenprobe erzeugt die Ideale und Filter unabhängig aus den Antiketten der N23-Ordnung und vergleicht alle einzelnen Mengenpaare.

## Feldgleichungen und Ausschluss

Jedes vergleichbare Paar hat nach seiner offenen Intervallgröße den Koeffizienten 1, −9, 16, −8 oder 0 ab Größe vier. Auf den vier ursprünglichen Gerätekanten wird zusätzlich 10⁻¹¹ abgezogen. Das Skript berechnet jede neue Intervallgröße auf der vollständigen N24-Ordnung. Es benutzt die Dichtevariation Dⱼ = 19 + Σᵢ kᵢⱼ(Yⱼ−Yᵢ)² für positive Innenereignisse und die freie Uhrgleichung Gᵢ = Σⱼ kᵢⱼ wⱼ(Yⱼ−Yᵢ) − wᵢ Σₕ kₕᵢ(Yᵢ−Yₕ). Eine verletzte notwendige Gleichung schließt die gemeinsame Lösung aus.

* **Positives 22.** Ereignis 23 liegt in seiner Zukunft. Sämtliche eingehenden Intervalle an 22 und an den frühen positiven Vorfahren bleiben unverändert. Die neu berechneten rationalen Hüllen für D22 am Halbschnitt liegen vollständig unter −4,59, −35,45 bzw. −5,13 in der Tabellenreihenfolge. Daher scheitert D22=0 bereits vor der Wahl des Helfergewichts.
* **Leeres 22.** Das Skript prüft die Kragenbeiträge und die möglichen Vorzeichen in G22. Anschließend kontrahiert es die Dichte- und Uhrgleichungen, die Kausalordnung und das nach Elimination von w23 gebildete Gleichungspaar aus G22 und G23. Terminale Uhren mit nichtverschwindender quadratischer Dichtekomponente erhalten eine Cauchy-Wurzelschranke oder eine gewichtsfreie lineare Gleichung. Die Intervallrechnung rundet mit ganzen Zahlen auf dem Raster 2⁻⁶⁴ nach außen. Bei Unterteilung werden für einen Ausschluss beide geschlossenen Hälften geprüft.
* **Die letzten zwölf terminalen Fälle.** Mit A = Σᵢkᵢ₂₃, B = Σᵢkᵢ₂₃Yᵢ und H = A Y23 − B erzwingt G23 wegen w23 > 0 die Gleichung H=0. Für A ≠ 0 lauten die projizierten Bedingungen Y23=B/A und 19A + Σᵢ<ⱼ kᵢ₂₃kⱼ₂₃(Yᵢ−Yⱼ)²=0. Für A=0 bleiben B=0 und 19+Σᵢkᵢ₂₃Yᵢ²=0. Sei F22 der alte ausgehende Kragenbeitrag an 22 und k=k₂₂,₂₃ ≠ 0. In jeder alten Uhrgleichung ersetzt −F22/k + w23(Y22−Yᵢ) genau den Helferterm w23(Y23−Yᵢ). Damit entfällt Y23 auch in den beiden Fällen ohne bewiesene endliche Schranke für diese Uhr. Die lineare äußere Hülle verwendet notwendige Produkt-, Quadrat- und Ordnungsungleichungen. Zwölf archivierte rationale Positivkombinationen dieser Zeilen ergeben je einen strikten Widerspruch, dessen kleinste Marge über alle Fälle größer als 0,00212 ist. Die Marge gehört zum algebraischen Zertifikat und hat keine physische Einheit.

## Reproduktion

Im entpackten Verzeichnis mit Python ab 3.10 ausführen.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
python3 -B gegenprobe.py
```

Der Hauptlauf rekonstruiert das Fallregister und die Ergebnisse und vergleicht sie byteweise. Er prüft die rationalen Widerspruchsmargen ohne Optimierungsbibliothek. Die Gegenprobe verifiziert die Enumeration und die verwendeten Eliminationsidentitäten auf rationalen Kontrollwerten. `Zertifikate.json` enthält die positiven rationalen Zeilengewichte. `terminal.py` baut die Ungleichungen neu auf. Nur die optionale Suche nach anderen Zertifikaten mit `discover` verwendet SciPy. Das Hauptprogramm kann mit `--ausgabe` seine beiden Ergebnisdateien erneut schreiben.

Die Eingangsdaten und die unveränderten Basisroutinen stammen aus [PR 413](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/413) und [PR 416](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/416), gelesen am [Repository-Stand von PR 418](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/2c08c72af7fa7d075f50decc48c9531d64d61c66). Lizenz und Urheberhinweis liegen in `basis/`.

## Reichweite

Der Nachweis umfasst exakt die drei identifizierten PR-413-Geometrien bei x22=1/2 und die beiden veröffentlichten Kragenpräparationen im festgehaltenen Sektor. Die Prüfung lässt für 23 alle zulässigen Ordnungsanbindungen zu, einschließlich solcher, für die keine geometrische Einbettung nachgewiesen wurde. Eine Einbettungsforderung kann die ausgeschlossene Familie nur verkleinern. Andere Schnittzeiten im Fenster, andere Sondenvergangenheiten, zusätzliche Ereignisse, veränderte Quellen, eine andere Materiebesetzung oder andere Randbedingungen brauchen eigene Untersuchungen. Die acht physischen Radien und 60 P3-Punkte stehen weiter auf NOT_RUN.
