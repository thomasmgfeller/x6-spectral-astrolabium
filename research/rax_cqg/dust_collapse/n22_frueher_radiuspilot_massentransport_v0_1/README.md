# Früher Radiuspilot · Massentransport und Fläche auf N22

**Die acht physischen Radiuswerte bei halber Referenzzeit bleiben offen.** Für das Modell lässt sich jetzt beziffern, wie viel der dargestellten Staubmasse vor und nach dem Schnitt mit eigenen Ereignissen belegt werden kann. Die Auswertung umfasst die 63 Feldvorgaben aus [PR 410](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/410) und die 18 anschliessenden Impulsvorgaben. Sie verwenden dieselbe kausale Ordnung 216141/229383/0/+. Mehrfach verwendete Lösungen und identische Randdaten sind möglich.

## Ein Zeitfenster für beide Kontrollen

Der physische Sollschnitt ist T* = 5√5/6. Auf N22 wird er versuchsweise mit der normierten Mitte x = (Y−Y₃)/(Y₇−Y₃) = 1/2 verglichen. Die Halbbreite h = 1/32 ist das schmalste Fenster mit h = 2⁻ⁿ oberhalb von 0,02687714, der früher zertifizierten ausreichenden Halbbreite für das Messpaar 19/20 auf einer Referenzlösung. Die Zuordnung der Modelluhr zur physischen Staubeigenzeit ist eine zusätzliche Annahme.

Der klassische Kontrollleser behält seine auf den beiden Schalen getrennten Beobachtungen von Eigenvolumen und radialer Eigendicke mit je ±1 % Fehler sowie die Schranke 1 für die Randgeschwindigkeit. Das Programm prüft diese Geschwindigkeitsschranke neu bis zum späten Ende des breiteren Fensters. Die Vakuumkontrolle und die Kalibrierung über eine positive Referenz werden aus der bestehenden Kontrollstudie nachgerechnet. In der klassischen LTB-Familie ergibt sich:

| Vorbereitete Masse | Radiusintervall am Zielschnitt, nach aussen gerundet | Maximaler relativer Endpunktfehler, aufgerundet |
|---|---:|---:|
| 1/4 | [9,3504; 9,8166] | 2,482 % |
| 4 | [8,0382; 8,4811] | 2,741 % |

Auf allen 81 N22-Feldboxen liegen im selben Fenster die positiven Ereignisse 18 und 19 sowie die leeren 17 und 20. Bei den unvergleichbaren Paaren (19,17) und (19,20) gibt es gemeinsame positive Vergangenheits- und Zukunftsanker. Die Anker dürfen ausserhalb des Fensters liegen. Die grösste Antikette positiver Ereignisse im Fenster hat Grösse zwei. Für ein direktes geschlossenes Dreiecksnetz aus gleichzeitig ablesbaren materiellen Eckereignissen fehlen schon vier paarweise unvergleichbare positive Ereignisse. Die Paare liefern auch keine geeichten Schalenvolumina, radialen Eigendicken oder vollständige äussere Materiegrenze. Andere, räumlich nichtlokale Flächenoperatoren bleiben offen.

## Welche Masse lässt sich durch den Schnitt verfolgen?

Die ältere [Verweildauerregel](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/6a5ac4447bcd65507f9c7022019476404de00cbc/research/rax_cqg/dust_collapse/cut_mass_charge_vacuum_v0_1) verteilt das Gewicht einer markierten Staublinie auf deren Ereignisse. Eine Aufenthaltszelle reicht jeweils bis zur zeitlichen Mitte zwischen benachbarten Markierungen. Die beiden Endzellen reichen bis zum Anfang und Ende der Uhrspanne. Diese Zuordnung wird hier als bedingtes Modell geprüft.

Von den elf positiven inneren Ereignissen sind 16, 18, 19 und 21 durch keinen gerichteten Pfad von 3 nach 7 erreichbar, der das betreffende Ereignis enthält. Zusammen tragen sie mehr als 55,24 % des positiven Innengewichts. Selbst wenn jeder der vier frühen Knoten als Eintritt und jeder der vier späten Knoten als Austritt erlaubt wird, bleibt Ereignis 21 ohne solchen Austritt. Es trägt mehr als 5,312 % des Innengewichts.

Für eine grosszügigere Obergrenze werden virtuelle Enden bei x = 0 und x = 1 gewährt. Jede nichtleere kausale Kette unter den elf positiven inneren Ereignissen ist zulässig. Von den 44 verschiedenen Ketten besitzen 21 mindestens eine eigene positive Markierung auf jeder Seite von x = 1/2. Nur diese Ketten zählen im Zähler des Anteils. Der Nenner ist die gesamte mit der Verweildauerregel dargestellte Linienmasse.

Sei dⱼₚ der Anteil der Uhrspanne, den Kette p dem Ereignis j zuweist. Die Variable fₚ ist die nichtnegative Linienmasse mal die gemeinsame Uhrdauer. Auf den 21 beidseitig markierten Ketten wird die Summe der fₚ unter den Bedingungen Σₚ dⱼₚ fₚ ≤ wⱼ maximiert. Jeder verbleibende Gewichtsrest lässt sich mit einer Ein-Ereignis-Linie ausgleichen. Weil sich die Aufenthaltsanteile jeder Kette zu eins summieren, ist der gesuchte Massenanteil gleich dem Optimum geteilt durch Σⱼwⱼ.

**Über die 81 Fälle liegen die jeweiligen maximal erreichbaren Anteile zwischen 28,20610 % und 28,20637 %.** Je Fall liefern nichtnegative konkrete Linienzuteilungen eine Untergrenze. Nichtnegative Vergleichsgewichte, die jede der 21 Ketten überdecken, liefern eine Obergrenze. Alle Bedingungen werden mit exakten Brüchen und nach aussen gerichteten Grenzen für die gesamte jeweilige Feldbox geprüft. Die Breite zwischen den individuellen Anteilsgrenzen beträgt höchstens 1,051 · 10⁻¹⁰ als dimensionslose Zahl. Eine zweite Abschätzung prüft allein den minimalen Zeitanteil nach dem Schnitt gegen das verfügbare späte Gewicht. Der errechnete Anteil beschreibt die Auflösung der angenommenen Linienmarkierung. Er beziffert weder einen Verlust von Staub noch den Fehler eines physischen Radius.

## Warum eine Ladungsnormierung allein keine zwei Radien erzeugt

Die 81 Fälle teilen die vier frühen Uhrimpulse und damit die normierte Eingangsladung Q = −Σᵢ₌₀³Gᵢ = 0,181585581308965. Jede feste, nur von diesem Q abhängige Eichregel liefert einen einzigen Wert für beide Massenziele.

Zwei Varianten prüfen diese Aussage auf den 27 Nullquellen-Fallvorgaben mit geänderter Randpräparation. Die Dichtegleichungen sind bei festem Y unabhängig von w. Jede Kante i→j trägt kᵢⱼ wⱼ (Yⱼ−Yᵢ) zu Gᵢ und das Negative zu Gⱼ bei.

- Werden nur die vier Anfangsgewichte durch 16 geteilt, ändern sich ausschliesslich Beiträge von Kanten innerhalb des Anfangsideals. Diese heben sich in Q exakt auf. Alle freien Gleichungen, der späte Rand und Q bleiben gleich. Die getrennten frühen Impulsziele werden in dieser Variante freigegeben.
- Werden sämtliche Gewichte durch 16 geteilt, skalieren alle Uhrimpulse und Q exakt um 1/16. Die homogenen freien Uhrgleichungen bleiben erfüllt. Die beiden Präparationen haben dieselben Uhren, dieselbe kausale Ordnung und dieselben positiven Ereignisse. Eine Modellverstärkung kann die beiden Ladungen exakt auf 1/4 und 4 normieren. Der Normalisierungsfaktor wird durch Zuordnung gewählt. Eine unabhängige physische Massenmessung folgt daraus nicht.

Jeder deterministische Radiusleser, dessen Eingaben nur Ordnung, Uhren und Gewichtszeichen sind, gibt bei der globalen Skalierung für beide Präparationen denselben Radius aus. Für die vorgegebenen klassischen Zielradien Rₗ = 10(15/16)^(2/3) und Rₕ = 10(3/4)^(2/3) ist der kleinste erreichbare maximale relative Fehler eines solchen gemeinsamen Zahlenwertes (Rₗ−Rₕ)/(Rₗ+Rₕ) = rund 7,42443 %. Der beste gemeinsame Wert ist das harmonische Mittel. Das schliesst bei diesen Eingaben zwei erfolgreiche 5-%-Vergleiche aus. Eine physisch begründete Geometrie, die auf unterschiedliche Massen reagiert, ist damit weiterhin zu untersuchen.

## P3 und Wiederholung

Der Prüfer liest die 60 veröffentlichten P3-Einträge ein und identifiziert die acht Kombinationen aus M = 1/4, 4 und Dichteverhältnis 1, 2, 4, 8 am Schnitt x = 1/2. Die physischen Radien bleiben im Ergebnis ausdrücklich leer. Für den nächsten physischen Vergleich braucht es zwei unabhängig massengeeichte Präparationen mit Vakuumkontrolle sowie eine geometrisch auswertbare bewegte Materiegrenze auf denselben gekoppelten Historien. Die Auflösung der Linienmarkierung und die Fehler des Flächenlesers sind dort getrennt zu prüfen.

Python ab Version 3.10 mit der Standardbibliothek genügt. Nach dem Entpacken ausführen.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
```

Der Prüfer rekonstruiert die Ordnung aus den mitgelieferten Vorgängerarchiven, verifiziert die Intervall- und Optimierungszeugen und vergleicht Ergebnisdatei und Fallregister byteweise. Optimierungszeugen.json enthält numerisch vorgeschlagene Koeffizienten, deren Gültigkeit unabhängig vom verwendeten Optimierer rational entschieden wird. Das optionale Programm zeugen_suchen.py erzeugt mit NumPy und SciPy neue Vorschläge in einer eigenen Datei. Quellen.json benennt Eingaben und Prüfsummen. Pruefplan.md dokumentiert die vor der Berechnung festgelegte Prüfung, Ergaenzung.md die später ergänzte Rechnung am Anfangskragen.
