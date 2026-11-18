# CST-DUST · Erweiterungsstabilität auf allen 23 erreichbaren N13-Endtypen (v0.4)

Die Dichteantwort liegt jetzt für sämtliche 23 Dreizehn-Ereignis-Geometrien vor, die von den zwei N11-Ausgangshistorien über eine zulässige Zwölf-Ereignis-Geometrie erreichbar sind. Die Studie setzt den in PR #297 publizierten endlichen Versuch fort. Der gemeinsame Vergangenheits- und Zukunftskragen, die kohärente Uhrenpräparation, die Dichtezentren 1/8 und 1/4 und die Auslese des q₇-Detektors gelten unverändert. Erfolg bezeichnet pro präpariertem Versuch einen der drei akzeptierten Zeigerausgänge. Der Fehlschlag bildet den vierten Ausgang.

## Umfang und Quellen

Die 408 möglichen markierten Zwei-Schritt-Wege führen zu 58 Endtypen. 24 Endtypen bestehen die skalare Endprüfung. Für Typ 510 fehlt ein zulässiger Zwischenschritt. Die übrigen 23 Typen sind zusammen über 188 vorwärts zulässige markierte Wege erreichbar. Davon sind 142 auch bei vertauschten Einfügungsmarken zulässig. Die frühere Auslese umfasste sieben N13-Typen. Hier wurden alle 23 mit demselben Rechenverfahren ausgewertet. Die fünf N12-Typen und die zwei N11-Eltern vervollständigen den berechneten Träger von 30 Typen.

Jeder ursprüngliche Elternzweig besitzt den reellen Amplitudenkoeffizienten 1/2. Unterschiedliche Wege zur selben unmarkierten Geometrie werden vor Anwendung der Detektoreffekte kohärent zusammengefasst. Die nichtnegativen Gewichte dürfen auf einzelnen Wegen null sein. Die Einfügungsreihenfolge kennzeichnet den Aufbau der endlichen Summe. Staubzeit, physikalische Wachstumsgewichte und Kollapsentwicklung sind davon zu unterscheiden.

[Publizierter Ausgangsversuch auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/cf35adb4ce5d35f6fc79ce05e2db07b8e2a3dd60/research/rax_cqg/dust_collapse/extension_stability_v0_3)

## Vier Vorschriften auf gemeinsamem Rand

ΔP bezeichnet die Änderung der unbedingten Erfolgswahrscheinlichkeit bei Wechsel von Dichtezentrum 1/8 auf 1/4. Die Referenzantwort beträgt −6,68047 × 10⁻⁶. λ bezeichnet den Anteil, den beide ursprünglichen Eltern jeweils abgeben. In den vier benannten Wachstumsvorschriften wird von diesem Anteil der Bruchteil μ über N12 hinaus nach N13 weitergegeben. Bei der folgenden 5-%-Spalte verbleiben 95 % auf N11 und die gesamten übrigen 5 % gehen bis N13 (μ = 1).

| Verteilung innerhalb jeder ursprünglichen Elternhistorie | N13-Typen mit Gewicht | ΔP bei λ = 5 % in 10⁻⁶ | ΔP bei vollständigem N13-Ersatz in 10⁻⁶ | Änderung des vierteiligen Dichtekontrasts bei vollem Ersatz |
|---|---:|---:|---:|---:|
| Markierte Einfügungen schrittweise gleich | 23 | −6,03025 | −0,12068 | 98,19 % |
| Unterschiedliche Tochtertypen schrittweise gleich | 23 | −6,03015 | −0,15114 | 97,74 % |
| Alle vorwärts zulässigen vollständigen markierten Wege gleich | 23 | −6,03027 | −0,12146 | 98,18 % |
| Vertauschungssymmetrische Ergänzung aus v0.3 | 22 | −6,03051 | −0,13924 | 97,92 % |

Die letzte Vorschrift erhält die schrittweise gleichgewichteten N12-Einfügungen als erste Randverteilung. Jeder in beiden Reihenfolgen zulässige Weg hat dasselbe Gewicht wie sein vertauschter Partner. Für einen der 23 erreichbaren Typen gibt es aus beiden Eltern zusammen keinen beidseitig zulässigen Weg. Sein Nullgewicht folgt aus dieser Vorschrift. Die Gleichgewichtung vollständiger Vorwärtswege induziert dagegen ihre eigene erste Randverteilung. `results.json` enthält die rationalen Verteilungen je Grössenstufe, sämtliche vier Detektorausgänge für fünf Präparationen, die Vergleiche zum N11-Ausgang sowie zur vorherigen Stufe.

## Wo erstmals eine beliebige Aufteilung scheitern kann

Jeder ursprüngliche Elternzweig gibt denselben Anteil λ ab und darf diesen frei auf seine erreichbaren N12- und N13-Nachkommen verteilen. Die Aufteilung darf von der ursprünglichen Elternhistorie abhängen, und der auf N12 verbleibende Anteil darf je Zweig verschieden sein. Die vier benannten Wachstumsvorschriften bilden Spezialfälle. Das resultierende Gewicht hat die Form w = (1−λ)b + λv. Der Ausgangsvektor b trägt je 1/2 auf den zwei N11-Eltern. Der Endpunkt v gehört zur konvexen Hülle von 624 Wahlpaaren aus je einem erreichbaren Nachkommen pro Elternzweig.

Pro Dichte darf der Totalvariationsabstand maximal 10 % des ursprünglichen Erfolgs betragen. Die relative Änderung des vierteiligen Dichtekontrasts ist auf 25 % begrenzt, das Vorzeichen von ΔP muss erhalten bleiben. Die drei Bedingungen beziehen sich auf die ursprüngliche kohärente Uhrpräparation.

* Für jede erlaubte Aufteilung und jeden Anteil bis einschliesslich **5,1179 %** sind alle Bedingungen erfüllt. Der pauschale 5-%-Befund aus v0.3 gilt damit auf dem ganzen berechneten Träger.
* Bei **5,1180 %** überschreitet eine explizite, nachträglich ermittelte Gewichtsaufteilung die Niveautoleranz. Ein einfacherer Fall überträgt je 5,2 % von der Kette auf N13-Typ 1023 und von der Ein-Kanten-Ordnung auf N13-Typ 255. Bei diesem Fall liegen beide Niveauabweichungen bei rund 10,128 %.
* Das Vorzeichen bleibt auf dem 30-Typen-Träger für jeden nichtverschwindenden reellen Gewichtsvektor negativ. Eine physikalische Bedeutung der numerischen Toleranzgrenze ist offen.

**Nachweis auf den endlichen Auslesematrizen.** Die akzeptierten Effekte werden als exakte Brüche ihrer symmetrisierten binären Gitterwerte behandelt. Der vierte Effekt ist durch das exakte Komplement festgelegt. Zunächst ergibt die Polarisierung über alle Wahlpaare und ihre Kreuzterme bei λ = 0,05 für die beiden Niveauabstände höchstens 0,987 ihrer Toleranz. Die anschliessende engere Eingrenzung nutzt die Konvexität der Erfolgswahrscheinlichkeit.

1. Bei beiden Dichten und für jeden der drei akzeptierten Ausgänge ist die Ableitung längs jeder erlaubten Gewichtsgeraden bis λ = 0,06 negativ. Die Schranke verwendet das Maximum bzw. Minimum aller Eltern-Endpunkt-Kreuzterme und ein oberes Matrixelement als Schranke für den Tochterterm bei nichtnegativ normiertem v. Die Ableitung ist affin in λ. Der Totalvariationsabstand ist daher in diesem Intervall exakt der Verlust an Erfolg. Der vierteilige Kontrast erreicht höchstens 0,486 seiner Toleranz. Die symmetrische Erfolgsdifferenzmatrix ist streng negativ definit, geprüft an ihren Zeilensummen.
2. Für jede Dichte ist die symmetrische Erfolgsmatrix S streng positiv definit. Für x = (1−λ)b + λv₀ unterschätzt die Tangente von wᵀSw die Funktion überall. Ihre Untergrenze über alle Aufteilungen beträgt xᵀSx + 2λ min_c xᵀS(c−v₀), wobei c alle 624 Wahlpaare durchläuft. Bei 5,1179 % übersteigt diese Untergrenze für beide Dichten das erforderliche 0,9-Fache des ursprünglichen Erfolgs. Die Monotonie überträgt dies auf das ganze Intervall ab null.
3. Bei 5,1180 % liegen die tatsächlich berechneten Erfolgsquotienten der expliziten Vergleichspunkte unter 0,9. Die Elternverteilungen stehen vollständig in `tangent_points.json`. Sie wurden numerisch mit projiziertem Gradientenverfahren gesucht und auf ganzzahlige Anteile mit Nenner 10⁸ gerundet. Für die Aussage genügen die anschliessend unabhängig mit rationaler Arithmetik geprüften Ungleichungen. Auf beiden Produktionsgittern gilt dieselbe Klammer. Ihre Breite beschreibt die numerischen Gittermodelle. Für die exakten Uhrintegrale liegt ein empirischer Gittervergleich vor.

## Vollständiger Ersatz bei festgehaltener N12-Verteilung

Hier darf jede N12-Historie ihr ganzes Gewicht beliebig auf ihre zulässigen N13-Töchter verteilen. Die N12-Gesamtgewichte werden zuvor nach einer der beiden schrittweisen Standardvorschriften festgelegt.

| N12-Zwischengewichtung | Maximaler N13-Erfolg bei 1/8, relativ zum N11-Erfolg | Maximum bei 1/4 | Erforderliches Minimum |
|---|---:|---:|---:|
| Markierte Einfügungen gleich | 31,0421 % | 31,0968 % | 90 % |
| Unterschiedliche N12-Tochtertypen gleich | 44,6567 % | 44,5345 % | 90 % |

Die Erfolgsmatrix ist positiv, also ist der Erfolg eine konvexe Funktion des Gewichts. Ein Maximum liegt unter den 10 × 11 × 10 × 10 × 7 = **77 000** deterministischen Zuordnungen der fünf N12-Eltern. Eine ganzzahlige, aufwärts gerundete Schranke sortiert Kandidaten aus, die das Maximum sicher verfehlen. Alle verbleibenden Kandidaten werden mit den exakten Brüchen der numerischen Matrixeinträge verglichen. Deshalb schliesst diese Prüfung auch beliebige Mischungen bei festem Zwischengewicht ein. Das notwendige 90-%-Minimum folgt daraus, dass der Totalvariationsabstand mindestens die absolute Änderung der Erfolgswahrscheinlichkeit beträgt.

Das veröffentlichte Gegenbeispiel mit frei gewählter Zwischenverteilung wurde ebenfalls reproduziert. Liegen auf N12 99,6 % bei Typ 11 und 0,4 % bei Typ 14 und enden diese Anteile bei den N13-Typen 184 und 22, scheitert die N12-Stufe und die N13-Stufe erfüllt die Kriterien. Das Ergebnis beruht auf der besonderen Zwischenverteilung. Die Vergrösserung des erlaubten Trägers lässt dieses Beispiel mit Nullgewicht auf allen übrigen Zweigen bestehen.

## Uhrintegrale und unabhängige Kontrollen

Der lokale C99-Kern wertet dieselben Gauss-Legendre-Summen wie v0.3 in anderer Reihenfolge aus. Er summiert zuerst über die fünfte innere Uhr bei festgehaltenen Vorgängern. Die übrigen vier Uhren werden danach gegen diese bedingte Summe integriert. Bei den fünf dichtesten Geometrien koppelt die variierte äussere Uhr mit Koeffizient null an die letzte innere Uhr. Dort kann deren bedingter Tensor über alle äusseren Stützstellen wiederverwendet werden. Der grösste dauerhaft gespeicherte dichte Uhrentensor hat vier Achsen. Die bedingte Summation kann weiterhin Rechenarbeit fünfter Ordnung erfordern.

Der Dichtefaktor lautet d(C) = 1/2 + [1−exp(−iC/2)]/(iC), mit d(0) = 1. Die Exponentialphase faktorisiert nach den quadratischen Paarbeiträgen zu C. In der Nähe von null verwendet der C-Kern eine Taylor-Auswertung. Diese Auswertung wurde gegen die ursprüngliche sinc-Form und gegen direkte kartesische Summation geprüft.

* Für alle Zweige stimmt die direkte Fünf-Uhren-Summe bei vier Knoten pro Achse auf besser als 1,6 × 10⁻¹⁵. Die komplette unabhängige Paketquadratur bei sechs inneren und drei äusseren Knoten stimmt auf besser als 5,5 × 10⁻¹⁶.
* Ein erster Gittervergleich ergab beim Kontrollversuch mit fester Uhr einen Eintragsunterschied von 5,04 × 10⁻¹¹. Daraufhin wurden die Typen 239, 255 und 859 zusätzlich verfeinert. Nach der Verfeinerung beträgt die grösste beobachtete Änderung eines Matrixeintrags über alle fünf Präparationen 5,89 × 10⁻¹³, bei geforderten 5 × 10⁻¹². Für 13 Typen genügte als letztes Gitter (48, 8), für zehn war (64, 10) erforderlich.
* Für die sieben veröffentlichten Typen beträgt die grösste Abweichung der Uhramplituden 1,04 × 10⁻¹⁴. Die kohärente Teilmatrix der v0.3 wird auf besser als 6,3 × 10⁻¹⁹ reproduziert. Die unabhängige skalare Abel-Auswertung bei ε = 10⁻²⁸ wurde für alle 23 Typen wiederholt. Der maximale beobachtete Fehler in Präzision oder Einheitsphase beträgt 3,72 × 10⁻²².

## Lokale Wiederholung

Im entpackten Verzeichnis verifiziert der folgende Befehl die Prüfsummen, übersetzt den C99-Kern temporär, wiederholt die Rechnungen auf einem CPU-Thread und vergleicht alle gespeicherten Ergebnisfelder.

```sh
python -B verify.py
```

Getestet unter Linux mit Python 3.12, einem lokalen C-Compiler unter `cc` und den Versionen in `v03/upstream/requirements.txt`. Bei Bedarf installiert `python -m pip install -r v03/upstream/requirements.txt` die Python-Abhängigkeiten in einer eigenen Umgebung. `clocks_all.json` enthält die Quadraturdaten und `results.json` die beiden kohärenten Matrixgitter, die exakten Testentscheidungen, alle Gewichtsvorschriften und die Daten zu den Kontrollpräparationen. `study.json` dokumentiert den lokal vorab fixierten Versuchsplan. Die engere Toleranzklammer ist eine ergänzende Auswertung. 19 unveränderte Referenzdateien sind in `v03/ORIGIN.json` mit ihren Git- und SHA-256-Kennungen ausgewiesen.

Die Aussagen gelten für die gewählten zwei Elternhistorien mit festem Kragen und die zwei zulässigen Einfügungsschritte. Weitere Grössenstufen, eine physikalische Auswahl des Historienmasses und eine CST-Kollapsentwicklung bleiben offen.
