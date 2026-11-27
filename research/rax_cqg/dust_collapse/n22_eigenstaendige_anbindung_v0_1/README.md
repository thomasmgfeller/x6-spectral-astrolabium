# Kann eine eigene Anbindung von Ereignis 21 das Staubball-Messpaar ins Zeitfenster bringen?

CST-DUST · Endliches N22-Modell · 27. November 2026

Für die drei ausgewählten N21-Projektionen ist ein gemeinsames stationäres Messpaar im geschlossenen Fenster [31/64, 33/64] bei allen 482 neuen Anbindungen ausgeschlossen. Das gilt jeweils bei fest leerem und bei frei positivem Gewicht von Ereignis 21. Alle 964 neuen Fälle sind einzeln im Register entschieden. Die drei Referenzen wurden vor der Fensterprüfung gewählt, weil für ihre serielle Erweiterung eine stationäre Lösung bekannt ist. Auch diese drei Lösungen wurden ausserhalb des gemeinsamen Messfensters erneut zertifiziert. [Serieller Ausgangsstand auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/404)

| Referenz | Lage von 21 | Neue Anbindungen | Davon mit einer geänderten Relation | Neue Gewichtsfälle |
|---|---|---:|---:|---:|
| 216141 | unmittelbar vor 19 | 163 | 2 | 326 |
| 216427 | unmittelbar nach 20 | 239 | 3 | 478 |
| 217269 | unmittelbar nach 20 | 80 | 1 | 160 |
| Gesamt | | 482 | 6 | 964 |

## Versuch

Die induzierte Ordnung der Ereignisse 0 bis 20 bleibt je Referenz fest. In Lage A gilt 21 ≺ 19, in Lage B gilt 20 ≺ 21. In beiden Fällen ist das eine Überdeckungsrelation. Mit dem jeweils anderen Messpunkt bleibt 21 unvergleichbar. Vergangenheit und Zukunft von 21 in den alten Ereignissen 0 bis 18 dürfen frei gewählt werden, soweit die Ordnungsvoraussetzungen es erlauben. Der Abstand zählt geänderte Relationen nach transitivem Abschluss. Die sechs Einzelschritte ergeben sich unabhängig durch Umlegen jedes der 38 Maskenbits und erneute Transitivitätsprüfung.

| Referenz | Einzeln zulässige Änderung gegenüber der seriellen Ordnung |
|---|---|
| 216141 | 16 ≺ 21 entfernen oder 21 ≺ 18 hinzufügen |
| 216427 | 21 ≺ 7 entfernen, 3 ≺ 21 hinzufügen oder 17 ≺ 21 hinzufügen |
| 217269 | 21 ≺ 18 entfernen |

Die normierte Uhr ist xⱼ = (Yⱼ − Y₃)/(Y₇ − Y₃). Beide Ereignisse, der positive Messpunkt 19 und der leere Messpunkt 20, müssen gleichzeitig das Zeitfenster erreichen. Die alten Innenfelder dürfen sich einstellen. Wirkung, drei Quellen, 256 Driftintervalle, zulässige Nachimpulse und Geräteparameter stammen aus dem seriellen Versuch. Für jedes Vergleichspaar werden die Schichtkoeffizienten auf der neuen Ordnung gezählt. Zwei unabhängige Aufzählungen liefern dieselben 485 Ordnungen einschliesslich der drei Kontrollen.

## Einseitige Anbindungen

373 Ordnungen haben alte Ereignisse vor und nach 21. Bei den übrigen 112 fehlt eine der beiden Seiten. Die 48 A-Ordnungen ohne alte Vergangenheit von 21 erhalten eine untere Schranke für Y₂₁ aus D₁₉ = 0. Der unmittelbare Term (Y₁₉ − Y₂₁)² hat dort den Koeffizienten +1. Die anderen negativen Terme werden mit ihren maximal möglichen Beträgen eingeschlossen.

Bei den 64 B-Ordnungen ohne alten Nachfolger ist 21 terminal. Bei Gewicht null entfällt es aus allen alten Gleichungen. Die Uhr kann deshalb zur Rechnung auf den Wert 6 oberhalb aller alten Uhren gesetzt werden. Für ein positives Gewicht seien cᵢ = cᵢ₂₁ und A = Σcᵢ. Für A ≠ 0 folgt aus G₂₁ = 0 die endliche Hülle Y₂₁ = (ΣcᵢYᵢ)/A. Genau sechs Ordnungen haben A = 0. Dann liefern G₂₁ und D₂₁ die beiden notwendigen Momentengleichungen

    Σ cᵢ Yᵢ = 0
    19 + Σ cᵢ Yᵢ² = 0.

Für diese sechs Fälle wird Y₂₁ algebraisch eliminiert. Bezeichne Gⱼ⁽ᵃˡᵗ⁾ den Staubgradienten ohne den Endpunkt. Dann gilt G₂₀⁽ᵃˡᵗ⁾ = −w₂₁(Y₂₁−Y₂₀) < 0. Der gemeinsame Term w₂₁Y₂₁ verschwindet in Gⱼ − cⱼG₂₀. Die verbleibende Kombination Gⱼ⁽ᵃˡᵗ⁾ − cⱼG₂₀⁽ᵃˡᵗ⁾ + cⱼw₂₁(Y₂₀−Yⱼ) muss für alte freie Uhren im jeweiligen Gerätetoleranzintervall liegen. Die Rechnung verwendet den Zeitwert 6 ausschliesslich für die Kontrolle der alten Chronologie in diesem Teilverfahren. Kein Gradient dieser sechs Fälle wird bei vorgegebener Enduhr ausgewertet. Die sechs Fälle erfordern insgesamt 24 Gewichtsbereiche. Bei 23 genügt die Ausgangsbox, bei einem genügt eine Halbierung.

## Prüfungen und Reichweite

Die vier Teilbereiche für die Gewichte 16 und 18 überdecken auch beliebig kleine positive Werte. In den 964 neuen Fällen ergeben sich 3 856 abgeschlossene Suchbäume mit 12 799 geschlossenen und null offenen Blättern. Residuen und Jacobimatrix wurden an 11 088 Einträgen mit exakten Wirkungsdifferenzen oder den expliziten Gewichtsbedingungen verglichen. Alle 485 Koeffiziententabellen wurden zwischen der Python- und der C++-Rechnung abgeglichen. Die drei stationären Referenzen werden mit der rationalen Kontraktionsprüfung für alle 25 freien Gleichungen reproduziert.

Die sechs seriellen Ordnungs- und Gewichtsfälle sind gesondert im Register ausgewiesen (Abstand null). Bei den zwei positiven B-Kontrollen verbleibt im allgemeinen Prüfer mit dem angegebenen Budget je ein offener Gewichtsbereich. Der zusätzlich wiederholte publizierte serielle Prüfer schliesst für beide Referenzen alle vier Bereiche. Ergebnisse.json zeichnet die beiden Verfahren getrennt auf.

Der Ausschluss gilt für die drei angegebenen Projektionen und die jeweils festgelegte Lage zu den Messpunkten. Für andere Projektionen oder eine geänderte Rolle von 21 bleibt die Fensterfrage offen. Ein physischer Arealradius ist offen. Die 60 physischen P3-Prüfpunkte stehen auf NOT_RUN.

## Offline wiederholen

Benötigt werden Python ab 3.10, GNU g++ mit C++17 und die Python-Standardbibliothek. Die Archivkette mit den Referenzlösungen und den früheren Programmen ist beigefügt. Es ist kein Netzzugang erforderlich.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py --jobs 4
```

Fallregister.tsv enthält die Masken P21 und F21 in Dezimaldarstellung. Bit j benennt Ereignis j mit 0 ≤ j < 19. Das Gewicht + bezeichnet 0 < w₂₁ < 1. Die Spalte „Offene_Gewichtsbereiche_im_Wiederholungslauf“ bezieht sich auf den allgemeinen Prüfer. Die Spalte „Nachweis“ nennt das entscheidende Verfahren. Ergebnisse.json enthält unter trees die allgemeinen Suchbäume, unter serial_trees die zusätzliche serielle Kontrollrechnung, unter controls die rational eingeschlossenen normierten Uhren und unter audit die unabhängigen Vergleiche. Rundungsabhängig gewählte Vorkonditionierer können andere Baumgrössen liefern. Entscheidend sind die vollständige Überdeckung und dieselbe Klassifikation.
