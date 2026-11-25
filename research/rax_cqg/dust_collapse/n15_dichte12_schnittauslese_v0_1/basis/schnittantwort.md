# CST-DUST · Kohärente Schnittantwort auf der N15-Kette

Anschluss an PR #358 auf dem im Herkunftsregister bezeichneten Git-Stand. Zwei positive Präparationen mit derselben markierten Massendosis liefern unter den äusseren Quellen dieselben Antworten. Ein zusätzlicher Eingriff hinter Ereignis 11 trennt sie auch nach der kohärenten Integration. Aus drei Eingriffen am selben Schnitt und der früheren Eingangsquelle ergibt sich eine neue Massenauslese. Diese Ergebnisse betreffen die geprüfte N15-Totalordnung.

## Was die beiden Ausgänge unterscheiden

Das Instrument verschiebt rechts vom Schnitt die gespeicherte Uhr 4 um +h/√D in skalierten Einheiten, mit h = 1/8 und der unverschobenen präparierten Dauer D. Nur die Phase des Paares 4 → 12 reagiert. Ein Nullarm und ein verschobener Arm werden bei festem Winkel −π/2 kohärent zusammengeführt. R bezeichnet die Wahrscheinlichkeit des ersten Ausgangs abzüglich jener des zweiten. ΔR vergleicht diese Balance zwischen den Präparationen. Die nach aussen gerundeten Grenzen unten sind beweisbare Einschlüsse. Die mittlere Zahl stammt aus der feinsten Gauss-Rechnung.

| Frühe mittlere Randdichte | +h, Einschluss für ΔR in 10⁻⁵ | +h, numerisch in 10⁻⁵ | −h, Einschluss in 10⁻⁵ |
|---|---:|---:|---:|
| 1/8 | [6,34354; 6,48603] | 6,41534 | [−6,94472; −6,80727] |
| 1/4 | [6,24251; 6,48603] | 6,37607 | [−6,94472; −6,70908] |

Bei Winkel 0 ergibt die numerische Rechnung für +h die kleineren Werte 2,731·10⁻⁶ und 5,567·10⁻⁶. Wird der benutzte Arm perfekt aufgezeichnet und das Armregister ausgespurt, ist die Balance für beide Präparationen exakt null. Eine zweite positive Gegenbelegung besitzt dieselbe Dichte an 12 und bleibt unter jeder Einzelverschiebung der Uhr 4 ununterscheidbar, obwohl sich Gesamtdichte und die Markierung 9x₁₃ unterscheiden.

## Massenauslese am selben Schnitt

Sechs gerichtete Verschiebungen der Uhren 4, 5 und 6, vier Einstellungen am äusseren Eingang und ein gemeinsamer Nullarm ergeben elf Einstellungen. Ihre Wirkungsdifferenzen liefern auf jeder einzelnen Konfiguration die Summe der sieben inneren Dichten in den Masseneinheiten xⱼ = wⱼ/D. In der integrierten Auslese werden stattdessen die relativen Phasen arg(Zₐ Z₀*) verwendet. Die Kalibrierung benutzt das leere Innere und die Vierteldosis beim ersten Randdichtezentrum. Der positive Faktor 0,999929259365 und der auf zwölf Dezimalstellen gerundete Nullpunkt 0 wurden vor den folgenden Übertragungen lokal festgehalten.

| Markierte Referenzmasse M | Ergebnis bei ρ = 1/8 | Ergebnis bei ρ = 1/4 |
|---:|---:|---:|
| 1/4 | 0,25000000 (Eichpunkt) | 0,25003587 |
| 1 | 1,00000554 | 1,00016863 |
| 4 | 3,99909690 | 4,00006386 |

Der grösste relative Fehler unter den fünf positiven Übertragungen ist 0,02258 %. Die grösste Differenz der beiden feinsten Quadraturen auf der unkalibrierten Massenskala ist kleiner als 5,4·10⁻¹⁰. Die Quadraturkontrolle liefert einen numerischen Konvergenzvergleich. Der Intervallbeweis oben betrifft den Kontrast der beiden Präparationen.

### Kleine Dosen und Vakuum

Leeres Inneres mit positivem Randkragen, vollständiges Vakuum und rechtsseitiger Grenzwert M → 0⁺ ergeben strukturell null. Nach der Hauptauswertung wurde dieselbe Eichung an drei kleinen Dosen geprüft. Die Zahlen sind relative Fehler in Prozent. Die Vergleichsspalte benutzt die publizierte Eichung des Instruments aus PR #356.

| M | Neue Auslese, ρ = 1/8 | Neue Auslese, ρ = 1/4 | Frühere Auslese, ρ = 1/4 |
|---:|---:|---:|---:|
| 2⁻¹² | −0,00075 % | +0,01294 % | −3,074 % |
| 2⁻¹⁶ | −0,00075 % | +0,01294 % | −49,623 % |
| 2⁻²⁰ | −0,00075 % | +0,01296 % | −794,403 % |

Die Stichprobe belegt die drei angegebenen Dosen. Für ein ganzes Massenintervall wäre zusätzlich eine Kontrolle der relativen Antwort zwischen den Prüfpunkten nötig.

## Bedeutung für P3

Die positive Referenz setzt die Markermasse im Präparationsmass ein. Das Instrument setzt Zugriff auf drei einzeln ansteuerbare, kohärent weitergereichte Uhrwerte am offenen Schnitt und auf die Dauer D voraus. Die Herleitung dieser Operation aus der gekoppelten Staubwirkung und dem physikalischen Randzustandsraum ist offen. Für die positive Eichung fehlt ein davon unabhängiger Ruhemasse- oder Stromladungsstandard. Alle 60 physischen P3-Prüfpunkte im mitgelieferten Originalregister führen den Status NOT_RUN.

## Nachrechnung

Im entpackten Verzeichnis genügt für die rationalen Identitäten, Git-Quellhashes und die 256-Bit-Intervallschranken die Python-Standardbibliothek.

    python3 -B pruefen.py --nur-exakt

Für die vollständige Wiederholung wird zusätzlich NumPy benötigt. Die Rechenprogramme lesen die Daten aus dem Paket.

    OPENBLAS_NUM_THREADS=1 python3 -B pruefen.py

HERLEITUNG.md gibt Gleichungen und Geltungsbereich an. exakt.json und schranken.json enthalten die algebraischen Ergebnisse und die Intervallschranken. rechnung.json und kleinmassen.json enthalten die Antworten je Quadratur und die elf komplexen Amplituden der feinsten Gauss-Stufe für die Massenläufe. eichung.json hält die Eichung fest. Die drei Textpläne dokumentieren die lokale Reihenfolge von Primärversuch, Massenauslese und explorativer Nachprüfung. Die SHA-256-Werte erlauben Inhaltsvergleiche. Eine unabhängige zeitgestempelte Vorregistrierung oder Verblindung gegen die bekannten Referenzmassen fand hier nicht statt.

[Git-Stand nach PR #358](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/74274857c30d491815b49bb34c2456c8fd6aa474)
