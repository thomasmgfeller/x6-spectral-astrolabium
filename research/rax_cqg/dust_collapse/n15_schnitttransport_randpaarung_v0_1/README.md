# CST-DUST · Transport der drei Uhrverschiebungen auf der N15-Kette

Anschluss an PR #359. Zwei Fragen entscheiden über die Verwendung der dortigen Massenauslese. Kann man dieselbe Einfügung an einem anderen Schnitt auswerten? Legt die vorhandene physikalische Randpaarung fest, wie sie einwirkt?

**Die erste Frage ist für die endliche Referenz positiv entschieden.** Beim Verschieben des Rechenschnitts gehen die schon durchlaufenen Paarphasen mit der linken Amplitude weiter. Auf diese Weise ergeben alle vier Schnitte dieselbe Wirkung auf jeder Geschichte und dieselbe integrierte Massenauslese. **Bei der zweiten Frage bleibt eine konkrete Wahl offen.** Uhr 6 tritt auch in der noch offenen Dichtepräparation von Ereignis 11 auf. Zwei Fortsetzungen der gleichen unverschobenen Randpaarung unterscheiden sich in der vorhergesagten Antwort.

## Vergleich bei markierter Referenzmasse 1

Die beiden rechten Spalten zeigen die Wirkung des gezielten Kontrollfehlers, bereits passierte Wechselwirkungen beim Versetzen des Schnitts zu vergessen. Rundung auf acht Nachkommastellen. Eichung und Anfangsdichtezentren stammen aus PR #359.

| Schnitt hinter | Mittransport, ρ = 1/8 | Mittransport, ρ = 1/4 | Ohne Mittransport, ρ = 1/8 | Ohne Mittransport, ρ = 1/4 |
|---|---:|---:|---:|---:|
| 11 | 1,00000554 | 1,00016863 | 1,00000554 | 1,00016863 |
| 12 | 1,00000554 | 1,00016863 | 0,87494123 | 0,87507848 |
| 13 | 1,00000554 | 1,00016863 | 0,74989334 | 0,75002738 |
| 14 | 1,00000554 | 1,00016863 | 0,56250280 | 0,56261874 |

Die Gleichheit mit Mittransport ist eine algebraische Identität. Dieselben elf integrierten Amplituden wurden zusätzlich mit zwei Produktquadraturen geprüft. Die vier äusseren Eingangsarme und der gemeinsame Nullarm dienen zugleich als Kontrollen. Die sechs inneren Arme tragen je einen der beiden Uhrschritte an 4, 5 oder 6.

## Wo die physikalische Eindeutigkeit fehlt

Die offene Verweilzelle besitzt den Anteil f₁₁=(u₁₂−u₆)/2. Werden die noch offenen Massargumente zusammen mit der Wirkung verschoben, ändert sich das bedingte Intervall der Dichte w₁₁. Wird nur die weiterlaufende Wirkung verschoben, bleibt das Intervall an der ursprünglichen Präparation fest. Bei derselben Uhrbelegung und Dosis sind die beiden Intervalle für jeden der zwei Schritte am gesamten positiven Referenzträger disjunkt. Bei den Uhren 4 und 5 ist kein noch offener Dichtefaktor betroffen.

| Fortsetzung hinter 11 | Geschätzte Masse bei ρ = 1/8 | Geschätzte Masse bei ρ = 1/4 |
|---|---:|---:|
| Nur Wirkungsargument verschieben, vorbereitetes Mass wie in PR #359 | 1,00000554 | 1,00016863 |
| Offenes Dichteargument ebenfalls verschieben | 1,00409576 | 1,01617872 |

Der zweite Versuch integriert die verschobene Dichtebox vollständig und behält den gemeinsamen Nullarm, die ursprüngliche Normierung und die Eichung bei. Er ist eine Modellalternative. Beide Fortsetzungen stimmen am unverschobenen Kern überein. Ein positiver Befund zur eindeutigen physikalischen Realisierung lässt sich daraus nicht ableiten.

## Wie viel Information eine frühe Integration verdeckt

Bei beliebigen komplexen linken Testwellen und den im Paket definierten Schnittvariablen benötigt eine gemeinsame **lineare** Darstellung der sechs inneren Antworten und der unverschobenen Antwort mindestens 1, 3, 7 bzw. 7 komplexe Amplituden an den Schnitten hinter 11, 12, 13 und 14. Die Variablen einer noch offenen Verweilzelle sind dabei weiterhin verfügbare Randdaten. Wer zusätzliche historische Uhren oder Dichten aufbewahrt oder jeden Arm separat neu berechnet, verwendet eine andere Darstellung. Auf einer expliziten Dichtefaser verschwindet die unverschobene Amplitude einer normierten Testwelle exakt. Im Arm 4+ beträgt ihr Amplitudenbetrag etwa 6,71182·10⁻⁵. Das ist ein bedingtes Amplitudenbeispiel, kein Wahrscheinlichkeitskontrast der breiten Präparation. Der Rang liefert keine stabile Inversion aller sieben Antworten. Auf derselben Faser liegt die spektrale Konditionszahl über 2·10²⁵.

## Konsequenz für P3

Für die bisherige Massenauslese genügt im Referenzkern eine zusätzliche unveränderte Kopie von u₆ für die offene Dichtezelle neben der verschiebbaren Wirkungskoordinate. Die Quellkopplung und die physikalische Paarung müssten begründen, welche dieser Koordinaten eine von aussen kontrollierte Operation beeinflusst. Eine unabhängige Eichung der positiven Ruhemasse ist ebenfalls offen. Alle 60 archivierten physischen P3-Prüfpunkte führen den Status `NOT_RUN`.

## Offline nachrechnen

Im entpackten Ordner genügen Python 3.10+ und die Standardbibliothek für alle rationalen Identitäten und 256-Bit-Intervallschranken.

    python3 -B pruefen.py --nur-exakt

Die integrierten Zahlen benötigen zusätzlich NumPy. Der vollständige Prüflauf wurde mit Python 3.12 und NumPy 2.3.5 wiederholt.

    OPENBLAS_NUM_THREADS=1 python3 -B pruefen.py

HERLEITUNG.md enthält den Transportbeweis, die beiden Massfortsetzungen, den Rangbeweis und die Grenzen der physikalischen Aussage. transport.json, paarung.json und integration.json liefern die Prüfergebnisse. herkunft.json identifiziert sämtliche aus Git übernommenen Quellen. Die vier Textpläne halten die lokale Reihenfolge der Untersuchung fest. Die Rangverfeinerung folgte auf die erste Frequenzrechnung. Die Hashes belegen den Dateiinhalt. Es gab keine externe Vorregistrierung.

[Ausgangspunkt auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/18b288b8b7e448bece16e84b627055ec43b1ddda)
