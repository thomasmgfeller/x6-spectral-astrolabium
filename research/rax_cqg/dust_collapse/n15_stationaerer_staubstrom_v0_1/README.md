# CST-DUST · Stationärer Staubstrom und P3-Masseneichung

25. November 2026 · Endlicher N15-Katalog · Physischer P3-Status **HOLD**, alle 60 Einträge **NOT_RUN**

Eine frühere Messung mit zwei Stellungen der Eingangsuhren liest auf Typ 2324 die über sieben Ereignisse summierte markierte Dosis. Hier wird untersucht, ob die bestehende Staubwirkung bei frei wählbaren inneren Feldern selbst eine stationäre Geschichte mit monotoner Uhr und erhaltenem Strom trägt. Die Radien und die drei P3-Sollmassen gehen in keine Rechnung ein.

## Befund

* Mit der ursprünglichen Randpräparation schliessen die beiden Tests über die vollen Uhrfenster auf sämtlichen 1 048 Typen eine stationäre Lösung mit sieben strikt positiven inneren Dichten im Projektsupport aus. Der Ausschluss verwendet alle kausal zulässigen inneren Uhrwerte. Auf elf Typen, darunter 2324, gilt er auch bei inneren Dichten auf dem Nullatom, sofern die inneren Uhren weiter frei variiert werden.
* Auf Typ 1767356 existiert innerhalb des rechten Uhrfensters ein reeller kausal geordneter Lösungszweig, wenn die einheitliche Zukunftsdichte von 1/8 auf 1/64 gesenkt wird. Die sieben Dichten liegen dann im Support und die positive Gesamtladung in der Konvention p ist auf allen 15 Schnitten identisch. Acht positive und sieben negative Einzelbeiträge kreuzen den Eingang. Die Bestimmung eines positiven materiellen Transports aus diesem signierten Strom bleibt offen.
* Bei den ursprünglichen Breiten um die **neuen** Feldzentren liefert eine konkrete Geschichte 13,488 % Schnittabweichung. Bei einem Achtel beider Halbbreiten gilt auf dem ganzen geprüften Paket eine obere Schranke von 1,728 %. Diese Werte betreffen den endlichen klassischen Feldtest. Sie liefern keine unabhängig geeichte physische Ruhemasse.

## Nachrechnung

Im entpackten Verzeichnis mit Python 3.10 oder neuer ausführen. Es genügen Standardbibliothek und lokale Dateien.

```sh
python3 -B pruefen.py
python3 -B pruefen.py --rohform
```

Die zweite Variante berechnet zusätzlich die 66 rechten Katalogfälle ohne die expliziten Sonderformeln für Minimalereignisse und Gabelungen. Sie verwendet dieselbe Intervallarithmetik und dieselbe Verzweigungslogik. Beide Wege wurden ausgeführt. Für die 66 Typen benötigen sie 757 beziehungsweise 61 151 abgeschlossene Teilintervalle. Der Prüfer bricht bei einem offenen Teilintervall ab. Zur Kontrolle der Rechnungen aus der Wirkung werden die ursprüngliche Kantenroutine, zwei Formen der quadratischen Uhrwirkung und die Gradientenroutine verwendet. Alle Intervalle werden mit ganzzahliger Arithmetik auf einem Raster von 10⁻¹⁴ nach aussen gerundet. Rationale Identitäten und die affinen Kontrollhistorien werden mit exakten Brüchen überprüft. Die Konstruktion der neuen Beispiele erfolgte explorativ nach dem vorigen Ergebnis. Es gab keine externe Vorregistrierung.

## 1. Gleichungen und Geltungsbereich

P und F seien die vier ursprünglichen Vergangenheits- und Zukunftsereignisse. I enthält die sieben inneren Ereignisse. Es gilt Δ⁴=3/722, Y=T/Δ und e=δ/Δ. Die vergangenen Uhren sind (−5,−4,−3,−2+e), die zukünftigen (2,3,4,5). Die zwei δ-Intervalle sind [−3/32,−1/32] und [1/32,3/32]. Für den Ausschluss genügen die etwas grösseren e-Intervalle [−3/8,−3/25] und [3/25,3/8]. Der Code beweist die Enthaltung mit den rationalen Originalschranken für Δ. Die Zukunftsdichte f ist ursprünglich auf allen vier Ereignissen 1/8. Beide ursprünglichen Vergangenheitsdichtezentren sind erfasst, weil diese Dichten in den inneren Gleichungen und der Schnittladung am Eingang nicht vorkommen.

Für i≺j hat bᵢⱼ je nach Anzahl der strikt zwischenliegenden Ereignisse die Werte 1, −9, 16, −8 und anschliessend 0. Auf der festen Ordnung lautet die normierte Staubwirkung

```text
Cⱼ = 19 + Σᵢ bᵢⱼ (Yᵢ−Yⱼ)²
S  = −Σⱼ wⱼ Cⱼ / 38
Hⱼ = Σᵢ bᵢⱼ (Yᵢ−Yⱼ)
19 ∂S/∂Yⱼ = wⱼ Hⱼ + Σₖ bⱼₖ wₖ (Yₖ−Yⱼ).
```

Im offenen positiven Dichtesektor fordert freie innere Variation Cⱼ=0 sowie ∂S/∂Yⱼ=0. Auf dem diskreten Nullatom wird **keine** kontinuierliche Dichtevariation verlangt. Wir fordern Yᵢ<Yⱼ auf vergleichbaren Ereignissen und 0<wⱼ<1 für besetzte kontinuierliche Dichten, entsprechend dem Produktmass der ursprünglichen Präparation. Die Rechnung betrifft den klassischen stationären Sektor der regulierten Materiewirkung bei fester Ordnung. Eine kohärente Summe kann auch andere Historien enthalten.

Für ein Ideal A mit P⊆A und A∩F=∅ gilt in der Konvention der vorigen Massenablesung

```text
19 Δ p(A) = Σᵢ∈A,ⱼ∉A bᵢⱼ wⱼ (Yᵢ−Yⱼ).
```

Die Differenz zweier solcher Schnittladungen ist bis auf das vereinbarte Vorzeichen die Summe der Uhrgradienten dazwischen. Auf einer innerlich stationären Geschichte ist die Ladung daher schnittkonstant. Der Test setzt weder die markierte Verweildauerregel noch das bekannte P3-Massenverhältnis als Nebenbedingung ein.

## 2. Warum die beiden ursprünglichen Uhrfenster scheitern

Jedes innere Minimalereignis mit positiver Dichte hat wegen Cⱼ=0 denselben Uhrwert a=(e²−4e−2)/(2(1+e)). Betrachte darüber einen Knoten, dessen sämtliche k inneren Vorgänger minimal sind.

* k=1. Seine Uhrgleichung aus der Dichtevariation ist linear in y. Der Abstand y−a ist (e⁴+36e³−44e²−96e−8)/[4(1+e)(17e²+18e−2)]. Auf beiden vollständigen Fenstern ist dieser Bruch negativ. Die Ordnung würde y>a verlangen.
* k=2. Die Gleichung ist 19−8(y+3)²+16(y+2−e)²+2(y−a)²=0. Ihre Diskriminante beträgt 8(62e⁴+248e³+313e²+130e−15)/(1+e)². Sie ist im linken Fenster negativ. Rechts ist der Wert der quadratischen Funktion bei y=a negativ. Seine Zählerform ist 2e⁴+8e³−5e²−26e+3, der Nenner ist (1+e)². Nur die grössere Wurzel liegt nach a. Dort ist Hⱼ negativ. Ist j maximal, ergibt sein Zukunftsbeitrag −f und die Uhrvariation fordert wⱼHⱼ=f>0. Das ist ausgeschlossen.
* k≥4. Alle direkten Koeffizienten vom Eingangsrand verschwinden. Cⱼ=19+k(y−a)² ist strikt positiv.

Der Prüfer benutzt zur Vorzeichenprüfung 256 rationale Teilintervalle je Fenster. Pro Typ wird der erste anwendbare Zeuge gezählt. Überschneidungen der Motive werden so genau einmal erfasst.

| Erster Ausschlussgrund | Linkes Fenster | Rechtes Fenster |
| --- | ---: | ---: |
| Ein innerer Vorgänger, umgekehrte Uhrreihenfolge | 780 | 912 |
| Zwei minimale Vorgänger, keine reelle Uhr | 264 | 0 |
| Zwei minimale Vorgänger an einem maximalen Knoten, falsches Dichtevorzeichen | 0 | 66 |
| Mindestens vier minimale Vorgänger | 4 | 4 |
| Vollständiger Intervalltest der restlichen Typen | 0 | 66 |
| **Ausgeschlossene Typen** | **1 048** | **1 048** |

Für die letzten 66 Fälle wird die Zeitgleichung Cⱼ=0 in kausaler Reihenfolge gelöst. Relativ zu einer Vorgängeruhr y₀ ergibt sich für z=y−y₀ die Gleichung A z²−2H z+C=0. Der Prüfer umschliesst jede reelle Wurzel, verwirft mit der Kausalordnung unvereinbare Bereiche und löst anschliessend die Gradientenbedingungen rückwärts nach den Dichten auf. Ein Nennerintervall mit null liefert allein keinen Ausschluss. Beide Endpunkte jedes Teilintervalls werden mitgeführt. Die zweite Rechnung verwendet für diese Typen die unreduzierten Kantenpolynome auch an Minimalereignissen und Gabelungen. In beiden Verfahren ist die maximal erlaubte positive Dichte 1.

### Erweiterung auf Nullatome bei Typ 2324

Auf Typ 2324 hat das minimale Ereignis 4 genau die beiden maximalen Nachfolger 13 und 11. Ereignis 13 hat allein 4 als inneren Vorgänger, Ereignis 11 zusätzlich 6. Maximalität und die unveränderten Zukunftsfelder erzwingen w₁₃H₁₃=w₁₁H₁₁=f>0. Beide Enddichten sind positiv, selbst wenn Nullatome erlaubt sind. Bei w₄>0 greift bereits der Ein-Vorgänger-Ausschluss an 13. Bei w₄=0 fordert die freie Uhr an 4

```text
0 = w₁₁(Y₁₁−Y₄) + w₁₃(Y₁₃−Y₄) + 8f(1−Y₄).
```

Die ersten beiden Terme sind strikt positiv. Folglich ist Y₁₁>Y₄>1. Andererseits ist H₁₁=−8+16e+Y₄+Y₆−10Y₁₁<−8+16e−8Y₁₁<0. Das widerspricht w₁₁H₁₁=f. Dieselbe Inzidenzstruktur wurde auf elf Typen direkt aus den Originalkoeffizienten bestätigt. Für die anderen 1 037 Typen wird keine vollständige Aussage über Nullatomsektoren gemacht.

## 3. Eine positive Lösung durch Ändern der Zukunftsdichte

Auf Typ 1767356 wird e=1/6 gewählt. Ein ganzes zusätzlich geprüftes Intervall mit Halbbreite 2⁻²² liegt im rechten ursprünglichen Uhrfenster. Die vergangenen Uhren und die zukünftigen Zeitstempel bleiben die ursprünglichen. Zuerst werden die sieben Dichtevariationsgleichungen vorwärts gelöst. An den drei Minimalereignissen sind sie linear. An 11, 12, 13 und 14 wird die Wurzel mit Vorzeichen +, −, −, − in der Formel (H±√(H²−AC))/A gewählt. Alle Diskriminanten sind strikt positiv, jede kausale Ungleichung gilt strikt. Danach liefern die Uhrgradienten alle wⱼ/f rückwärts. In dieser Lösung ist w₆ am grössten. Bei e=1/6 beträgt die obere Grenze für f, bei der alle wⱼ<1 bleiben, zwischen 0,05473612 und 0,05473613. Die Grenze selbst gehört wegen des offenen Supports nicht dazu.

| Am Mittelpunkt e=1/6 | Alter Zukunftsrand f=1/8 | Neuer Zukunftsrand f=1/64 |
| --- | ---: | ---: |
| Dichte w₆ | 2,283684 | 0,285460 |
| Zulässigkeit des untersuchten Zweigs | Dichteschranke überschritten | Alle sieben Dichten im Support |

Auf dem neuen Zweig liegt 19Δp am Mittelpunkt zwischen 0,31527470 und 0,31527472. Über das ganze kleine e-Intervall liegt diese Grösse zwischen 0,31504 und 0,31551. Alle 15 Ideale wurden direkt summiert. Die exakte Schnittkonstanz folgt aus den gelösten Gleichungen. Das positive Vorzeichen des Gesamtstroms ist mit gegenläufigen Einzelbeiträgen verträglich. Eine Umrechnung in physische Ruhemasse würde eine unabhängige Referenz erfordern.

### Endliches Paket um den neuen Zweig

Für jeden zugelassenen Versatz im kleinen e-Intervall werden die sieben Uhren und sieben Dichten unabhängig um ihre stationären Werte variiert. Bei Stufe k beträgt die Halbbreite jeder Uhr in Y-Einheiten (4−e)/(64·2ᵏ), jene jeder Dichte wⱼ/(100·2ᵏ). Für die Uhren entspricht dies einer Halbbreite von 1/(64·2ᵏ) in der relativen Zeit. Das sind endliche Boxen im stetigen Teil des Eingabemasses. Die Feldzentren und der Zukunftsrand wurden gegenüber der alten Präparation geändert.

Für jede einzelne Feldgeschichte wird die Abweichung |p(A)−p(P)|/p(P) berechnet beziehungsweise eingeschlossen. Die Grundladung der stationären Geschichte fällt aus dem Zähler heraus. Zur Einfassung bleiben die in den kleinen Feldänderungen linearen Terme und alle gemischten Dichte-Uhr-Terme erhalten. Der Eingang wird auf derselben gestörten Geschichte ausgewertet und bleibt im ganzen Test positiv. Der Prüfer kontrolliert die strikte Kausalordnung und den Dichtesupport auch am breitesten Paket.

| Breitenfaktor relativ zum früheren Ansatz | Obere Schranke über alle 15 Schnitte und die ganze Feldbox |
| --- | ---: |
| 1 | 17,213 % |
| 1/2 | 7,569 % |
| 1/4 | 3,560 % |
| 1/8 | **1,728 %** |

Am breitesten Paket ist die Toleranz tatsächlich verletzt. Bei e=1/6 ergibt das Ideal mit inneren Ereignissen {4,5,6,11,13} für konkrete Uhr- und Dichteverschiebungen eine Zunahme der Ladung um 13,48817 bis 13,48818 %. Die beiden Ladungen wurden zusätzlich durch direkte Kantensummen der verschobenen Geschichte neu berechnet. Der Faktor 1/8 ist der erste garantierte Wert im untersuchten Halbierungsraster. Für 1/2 und 1/4 beweist allein die obere Schranke keine Verletzung. Die Garantie ist eine Aussage über jede Feldgeschichte der deklarierten Box. Für eine kohärente Paarung mit komplexen Gewichten braucht es eine gesonderte Rechnung.

## 4. Kontrollvergleich von Dosis und erhaltenem Strom

Bei festem f=1/8 wurden ausserhalb der beiden Eingangsfenster, am affinen Vergleichswert e=0, zwei andere Katalogtypen mit strikt positiven Dichten gefunden. Uhren und Dichten lösen dort beide inneren Gleichungen. Die Dosisantwort stammt aus den zwei direkten Auswertungen der alten gepulsten Staubwirkung mit korrigiertem Vergangenheitsanteil. Die Ladung wurde separat mit der ursprünglichen Kantenroutine auf jedem Ideal summiert. Q=−p ist hier die entgegengesetzte Orientierung.

| Typ | Geprüfte Schnitte | Dosis Σw/(4−e) | Quellenphase | 19ΔQ |
| --- | ---: | ---: | ---: | ---: |
| 39441 | 32 | 7/32 | 315/608 | 25/8 |
| 39456 | 36 | 9/32 | 405/608 | 5/8 |

Auf dem zweiten Typ nimmt die Dosis gegenüber dem ersten um den Faktor 9/7 zu, der Betrag der erhaltenen Ladung fällt auf 1/5. Ein gemeinsamer multiplikativer Faktor kann beide Auslesen auf diesen zwei Typen nicht gleichsetzen. Das Gegenbeispiel setzt sich auf |e|≤2⁻²⁰ fort. Dort liegen die Verhältnisse der Ladungsbeträge in [0,1996; 0,2004] und der Dosen in [1,2415; 1,3322]. Die Dosis kann auf ihrer bisherigen markierten Präparation weiterhin korrekt ausgelesen werden.

## 5. Bedeutung für den physischen P3-Test

Das Ergebnis liefert eine prüfbare Randpräparation für einen stationären **Gesamtstrom** und ein endliches Paket mit kontrolliertem Schnittfehler. Die Wahl der kleineren Zukunftsdichte ist eine Modellentscheidung. Es gibt keine unabhängige Ruhemasse-Eichung dieses Zweigs, keine kohärent nachgewiesene Stromerhaltung des Pakets und keine daran geometrisch ausgelesene materielle Oberfläche bei T*=5√5/6. Der physische P3-Lauf steht bei 0 von 60. Der nächste an diesem Paket entscheidbare Test ist die kohärente Auswertung der Anfangs- und Schnittladung mit derselben Endpaarung, einschliesslich der beweglichen Paketgrenzen. Für eine physische Massenzuordnung ist zusätzlich eine eigenständige Referenz erforderlich.

## Herkunft

Die ursprüngliche Variationsroutine, der Katalog, der P3-Status, die Lizenz und die Quelldateien sind mit SHA-256 und dem Git-Stand in `herkunft.json` referenziert. Ebenfalls dokumentiert sind die SHA-256-Werte der zwei vorherigen Prüfpakete. Der vorliegende Versuch verwendet die endlichen Projektgleichungen. [Ausgangsstand auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/dcda14fa2206ad87c04bd0e0966a86a6ba067241/research/rax_cqg/dust_collapse) · [P3-Prüfvertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/dcda14fa2206ad87c04bd0e0966a86a6ba067241/research/rax_cqg/dust_collapse/correspondence_v0_1)
