# Können die Randuhren die zwei inneren Quellen ersetzen?

CST-DUST · Typ 2097151 · Ausgangspunkt ist die N15-Auslese aus [PR #357](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/357). Alle Ergebnisse betreffen die veröffentlichte endliche Wirkung und die jeweils angegebenen Randdaten.

**In den beiden verwendeten Randuhrfenstern gibt es keinen streng vorwärts laufenden, vollständig positiv besetzten stationären Staubpfad.** Schon die ersten beiden inneren Dichtegleichungen verlangen, dass die zweite innere Uhr einen kleineren Wert als die erste annimmt. Dieser Ausschluss gilt auch ohne die sieben inneren Präparationsfenster. Der bereits berechnete kohärente Kern integriert ausdrücklich auch nichtstationäre Konfigurationen. Seine Ergebnisse aus PR #357 werden durch diesen Befund nicht widerlegt.

## Stationarität auf der ursprünglichen Kette

Die inneren Ereignisse in kausaler Reihenfolge sind 4, 5, 6, 11, 12, 13 und 14. An den Ereignissen 11 und 13 werden die beiden Quellen angesetzt. Die Eingangswerte in der Koordinate Y = T/Δ sind −5, −4, −3, −2+e mit e = o/Δ und Δ⁴ = 3/722. Die zwei Offsetfenster sind −3/32 ≤ o ≤ −1/32 und 1/32 ≤ o ≤ 3/32. Auf dem positiven Dichtezweig ist die innere Dichte frei variierbar. Jede stationäre Feinhistorie im Inneren des Integrationsgebiets muss deshalb an jedem inneren Ziel die Gleichung 19 + Σ b(Yⱼ−Yᵢ)² = 0 erfüllen. Die vier Schichtgewichte summieren sich zu null. Damit bestimmt die Gleichung bei gegebenen vier Vorgängeruhren den nächsten Uhrwert linear, sofern der Koeffizient von null getrennt ist.

| Äusseres Offsetfenster | Garantierte Einschliessung von Y₅−Y₄ aus den ersten beiden Gleichungen | Geforderte Uhrordnung |
|---|---:|---|
| Links | [−1,231919; −0,221713] | Y₅ > Y₄ |
| Rechts | [−9,618299; −1,247569] | Y₅ > Y₄ |

Die Tabelle beruht auf einer rational überprüften Eliminationsformel mit auswärts gerundeten Intervallen. Eine zweite Rechnung setzt die Gleichungen chronologisch ein. Sie deckt beide vollständigen Offsetfenster ohne offene Zellen ab. Die Zahl 297/4096 in dichteschale.json ist eine Zellgrenze des Nachweisverfahrens. Sie bezeichnet keinen physikalischen Übergang. Die eingesetzten positiven Dichten, die markierte Masse und die beiden Anfangsdichtezentren gehen in die Dichtegleichungen nicht ein.

Die sieben Uhrgleichungen wurden zusätzlich direkt auf den ursprünglichen Dichte- und Zeitboxen geprüft. Für M = 1 bleibt die Komponente −19 ∂S/∂Y₁₂ links über 0,3307 und rechts über 0,3153. Für M = 1/4 und M = 4 weist die Komponente bei 11 über die volle Breite beider äusseren Zeitfenster einen festen, je nach Masse unterschiedlichen Vorzeichenbereich auf. Auch der zeitliche Gradient verschwindet somit bei diesen drei Massen auf keiner geprüften Box vollständig. Die Rand- und Atomsektoren sowie mögliche Beiträge von Integrationsrändern sind durch die stationäre Prüfung nicht ausgeschlossen.

## Welche Information am Rand fehlt

Für feste innere Daten wurden zwei zulässige Feinhistorien mit derselben markierten Masse M = 1 konstruiert. Sie liefern bei **jeder** Wahl der acht äusseren Uhren und acht äusseren Dichten dieselbe absolute Staubwirkung, solange die gemeinsamen inneren Daten der jeweiligen Historie bei der Randvariation festgehalten werden. Der Skalar- und der Gravitationsfaktor sind im festen Typ beim gleichen Skalarfeld unabhängig von dieser inneren Dichteänderung. Im ganzen Vergleich ist der bekannte Kragenquellterm für beide Arme gleich. Die gemischte Antwort der zwei inneren Uhrverschiebungen unterscheidet die Historien.

| Historie | Realisierte Dichtesumme Σwᵢ/D | Gemischte innere Quelle −19 ∂ₐ∂ᵦS |
|---|---:|---:|
| Minus | 0,999907931 | 1,117917008 |
| Plus | 1,000092069 | 1,132082992 |

Die Markierung 1 ist beiden Präparationen gemeinsam. Die Werte der zweiten Spalte messen die realisierte Dichte innerhalb ihres zugelassenen Jitters. Der Zeuge ist kein Fehlschlag des Zwei-Prozent-Tests. Das Argument gilt auch nach kohärenter Integration für zwei explizit konstruierbare positive Präparationen mit voller Unterstützung auf der Referenzbox. Alle äusseren Wirkungsintegrale stimmen darin paarweise überein, während sich bereits die gewöhnlichen Mittelwerte der realisierten Dichtesumme und des inneren Mischmarkers unterscheiden. Die alternativen Präparationen sind Vergleichsmasse. Die physikalische Ensemblepaarung wurde damit nicht bestimmt. [Konstruktion und Beweis](HERLEITUNG.md)

## Was eine Änderung der Randuhren bei fester Dichte bewirkt

Weil die Wirkung in den Uhren quadratisch ist, erhält ein Verschiebungsvektor t im Inneren zusammen mit einer Kragenänderung c die inneren Uhrkräfte genau dann, wenn Kᵢᵢ t + Kᵢₑ c = 0. Hier ist K das −19-Fache der Uhr-Hesse-Matrix. Die getesteten Zielrichtungen verändern ausschliesslich die vierte und die sechste innere Uhr. Die übrigen fünf sollen unverändert bleiben. Die Rechnung hält die Dichten, die Quellnormierung und den Bezug der Uhren fest. Sie untersucht eine bedingte Antwort bei gleicher innerer Kraft. Ein zuvor nichtstationärer Zustand wird dabei nicht stationär.

| Veränderbare Randuhren | Rang der Randspalten | Zahl unabhängig erreichbarer Kombinationen der beiden Zielrichtungen |
|---|---:|---:|
| Vier Eingangsuhren | 4 | 0 |
| Vier Ausgangsuhren | 4 | 0 |
| Beide Kragen, Synchronisationsuhren 3 und 7 fest | 6 | 1 |
| Beide Kragen, nur 7 fest | 7 | 2 |
| Alle acht Randuhren | 7 | 2 |

Diese Ränge gelten exakt an sechs Referenzen, M ∈ {1/4, 1, 4} und D ∈ {15/16, 17/16}, mit mittleren Zellpositionen und zentralen Dichten. Die erreichbare einzelne Kombination bei zwei festen Synchronisationsuhren hängt vom Zustand ab. Bei D = 15/16 hat sie für M = 1/4 das Verhältnis t₁₁:t₁₃ = 135/272:1 und für M = 1 das Verhältnis −135/112:1. Das gemeinsame Verändern von Anfangs- und Enddaten beschreibt hier ein zweiseitiges Randwertproblem.

Für das gesamte offene ±1-%-Dichteband liefert schon die Variation von w₁₂ und w₁₃ eine schärfere Aussage. Die dabei entstehenden zwei Kraftgleichungen fordern t₁₁ = t₁₃ = 0 für jede von den verborgenen Dichten unabhängige, gemeinsame äussere Uhränderung. Gekoppelte innere Aktoren oder eine physikalisch hergeleitete nichtstationäre Randabbildung fallen ausserhalb dieser geprüften Steuerklasse.

## Positive Kontrolle mit anderen Randuhren

Auf derselben Ordnung löst ein gleichmässiger Abstand Yⱼ₊₁−Yⱼ = 1 entlang der Kette bei konstanter Dichte 1/8 alle 14 inneren Stationaritätsgleichungen. Der Versatz ist o = 0 und die Randdauer 8Δ. Beides unterscheidet sich von der bisherigen Präparation. Die Kontrolle zeigt, dass die endliche Wirkung monotone stationäre Lösungen auf dieser Ordnung zulässt.

Wenn nur die vier Zukunftsdichten bei diesen gleichmässigen Uhren verändert werden, bestimmen die Uhrgleichungen die sieben inneren Dichten eindeutig rückwärts. Die erste innere Dichte ist die Linearkombination der vier Zukunftsdichten mit Koeffizienten (−97509, 461622, −901552, 537440). Bei unabhängigen relativen Abweichungen mit Betrag höchstens ε bleiben alle sieben inneren Dichten für jedes Vorzeichenmuster strikt positiv, solange ε < 1/1 998 123, also ungefähr 0,50047 ppm. Am Grenzwert erzeugt das Vorzeichenmuster (+,−,+,−) die erste Nulldichte. Eine gemeinsame Skalierung aller Zukunftsdichten wird hingegen gleichmässig übertragen. Die kleine Zahl betrifft diesen zweiseitigen stationären Test und die erlaubten unabhängigen Fehler, keine allgemeine Messauflösung.

## Stand von P3 und Nachrechnung

Für die ursprüngliche Präparation steht damit eine Übertragung der beiden Quellen durch einen monotonen positiven stationären inneren Pfad nicht zur Verfügung. Der offene physikalische Schritt ist eine gemeinsame Randoperation am nichtstationären gekoppelten Kern, die beide inneren Quellantworten auslöst oder zugänglich macht. Auch eine unabhängige positive Ruhemasse-Eichung fehlt. Alle 60 archivierten physischen P3-Prüfpunkte stehen auf `NOT_RUN`.

Im entpackten Ordner reproduziert der folgende Befehl alle sieben Ergebnisdateien bytegleich. Python ab 3.10 mit Standardbibliothek genügt.

    python3 -B pruefen.py

herkunft.json nennt die acht quellidentischen Git-Dateien und ihre SHA-256-Werte. Der Hauptplan und die drei Ergänzungen wurden lokal in der dokumentierten Reihenfolge festgehalten. Die Kontrolle der gleichförmigen Dichten wurde nach dem Fund der affinen Referenzlösung geplant. Es gab keine externe Vorregistrierung. [Zugehöriger Git-Stand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/2737fc792ada1de4e2a07f139f227339497fb66c)
