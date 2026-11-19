# N15-Erweiterung der kohärenten Staubball-Präparation

## Randvertrag und Zählung

Die vier Ereignisse des Vergangenheitskragens und die vier des Zukunftskragens bleiben fest. Sieben Ereignisse liegen im Innern. Der vierte Einfügungsschritt beginnt mit den 139 zugelassenen N14-Typen aus PR #299 und #311. Die beiden N11-Anfangshistorien haben weiterhin je Amplitudengewicht ½. Beide geben den gleichen Anteil λ ihres Gewichts ab. Jede darf diesen unabhängig auf ihre eigenen erreichbaren, zugelassenen N12- bis N15-Zweige aufteilen. Die Aufteilungen sind nichtnegativ und bei beiden Anfangsdichten dieselben. Beiträge zum gleichen Endtyp addieren sich als Amplituden. Ein markierter Pfad wird für jeden der Einfügungsschritte gezählt. Pfadzahlen bestimmen hier keine physikalischen Gewichte.

Ein neuer Punkt kann zu jedem der sechs inneren Vorgänger früher, später oder unvergleichbar sein. Die Vorwärtszählung verwirft nichttransitive Relationen und bestimmt den unmarkierten Typ durch natürliche Umetikettierung. Parallel dazu entsteht der vollständige Katalog der Sieben-Punkt-Ordnungen durch Hinzufügen eines maximalen Punkts über jedem Ideal einer natürlich beschrifteten Sechs-Punkt-Ordnung. Die kanonische Kennung ist die kleinste natürliche Relationsmaske. Für jedes Paar aus zugelassenem Eltern- und beliebigem Tochtertyp muss gelten

    markierte Einfügungen × |Aut(Tochter)| = passende Löschungen × |Aut(Eltern)|.

Beide Seiten zählen dieselben markierten Isomorphismen. Die Prüfung umfasst auch Multiplikität null. Als externe Grössenkontrollen dienen die Zahlen 2 045 und 96 428 für sieben unbeschriftete bzw. natürlich beschriftete Punkte. [OEIS A000112](https://oeis.org/A000112) · [OEIS A006455](https://oeis.org/A006455)

## Skalare Zulässigkeit

Die Kantengewichte der Wirkung sind 1, −9, 16, −8 für offene Intervallgrössen null bis drei und danach null. Die beiden Randsektionen und ihre quadratischen Phasen stammen aus v0.6. Aus der ganzzahligen doppelten, auf die Sektionen zurückgezogenen Hesse-Matrix G folgt die Zahl der reinen inneren Nullrichtungen als 7 minus Rang der sieben inneren Spalten. Für die neun integrierten Koordinaten I ist f = 9 − Rang G[:,I]. Der gemischte Defekt beträgt 12 − f − Rang G[(x,I),(y,I)]. Das Kriterium der Vorstudie verlangt reine innere Nullität und gemischten Defekt jeweils null. Vor Anwendung auf die 1 652 Kandidaten wurden die drei Rangwerte aller 238 früheren N14-Kandidaten reproduziert. Zusätzlich prüft der ursprüngliche Algorithmus mit Schurkomplement und Nullräumen alle 604 ausgeschlossenen Typen. Bei den 1 048 zugelassenen Typen konstruiert er den symplektischen Ausgang und prüft die Gaußpräzision.

## Direkte Uhrrechnung

Die Auswahl umfasst alle zugelassenen N15-Typen, für die bei der Elimination kein gemeinsamer Zwischenfaktor mehr als drei Uhren enthält. Die Suche testet jede mögliche nächste Variable, bis eine vollständige Reihenfolge gefunden ist oder alle Optionen ausscheiden. Bei den 23 ausgewählten Typen werden beide Loben bei beiden Dichten auf den Gittern (32,6), (48,8) und (64,10) berechnet. Die erste Zahl bezeichnet innere Knoten je Uhr, die zweite äussere Knoten je Lobe. Eine direkte siebendimensionale Summe auf (4,3) kontrolliert die Faktorisierung. Eine zweite Skalarrechnung mit Abel-Dämpfung 10⁻²⁸ kontrolliert Präzision und Phase dieser 23 Typen.

Zusammen mit allen 169 bisherigen Zuständen bilden sie den 192-dimensionalen Pilotträger. Die drei gespeicherten Gram-Matrizen sind durch ganzzahlige Kongruenzen auf positive Definitheit geprüft. Die rationalen Stützebenen, das Gegenbeispiel und die drei Detektorkriterien werden direkt aus dem eingebetteten v0.6-Code wiederverwendet. Jede der 23 neuen komplexen Uhramplituden darf sich beim Nachweis auf jedem Referenzgitter je Dichte innerhalb des Radius 10⁻⁷ bewegen.

## Gemeinsame Schranke für alle 1 217 Zustände

Für jeden neuen Endtyp werden die drei skalaren Detektorüberlappungen mit beiden N11-Eltern und die drei Diagonalelemente aus dem eigenen Gaußausgang bestimmt. Bei 1 025 N15-Typen wird die komplexe Uhramplitude durch eine Betragshülle ersetzt. Für jeden äusseren Uhrenknoten behalten wir alle inneren Dichtefaktoren mit höchstens einer weiteren inneren Uhr als Argument. Alle übrigen Faktoren haben Betrag höchstens eins. Jeder behaltene Knoten hat höchstens einen inneren Vorgänger. Die natürliche Kausalordnung schliesst gerichtete Kreise aus, und die Relation mit höchstens einer eingehenden Kante je Knoten bildet einen Wald. Bedingte Summation von den Blättern zu den Wurzeln integriert das Produkt der behaltenen Beträge auf dem jeweiligen Gitter. Positive normierte Gewichte erhalten die obere Schranke. Der äussere Normfaktor beträgt 1/√768 nach Mittelung der beiden Loben. Die numerische Hülle erhält wie in v0.6 einen absoluten Zuschlag von 10⁻¹². Auf 15 über den Katalog verteilten Masken kontrolliert eine unabhängige direkte Siebenfachsumme die Waldkontraktion bei (4,3).

Für eine Teilmenge der drei akzeptierten Detektorausgänge sei F ihre Effektsumme. Die vierte Wahrscheinlichkeit ist eins minus Gesamterfolg. Für Änderungen mit Komponentensumme null entspricht die halbe L¹-Norm dem grössten Absolutbetrag einer Teilsumme. Durch Komplementbildung genügen die sieben nichtleeren Teilmengen der drei akzeptierten Ausgänge.

Mit Referenz b, Nachkommenmischung v und x = (1−λ)b + λv setzen wir p = ⟨b,Fb⟩, c = Re⟨b,Fv⟩ und m = ⟨v,Fv⟩. Dann gilt

    p(x) − p = λ [2(c−p) + λ(p−2c+m)].

Exakte rationale Projektionen der zwei Elternzeilen liefern je Endtyp eine Unter- und Obergrenze für c. Für bekannte Uhren wird der Unsicherheitsradius mitgeführt, für unbekannte wird der gesamte komplexe Kreis zugelassen. Das Extremum eines linearen Ausdrucks über einen Elternsimplex wird an einem erreichbaren Endtyp angenommen. Die Elternbeiträge werden gemittelt. Positivität und Konvexität liefern 0 ≤ m ≤ M, wobei M das Maximum von Fⱼⱼ mal der quadrierten Uhrhülle ist. Für die Polynome der unteren und oberen Schranke begrenzen die drei Bernstein-Koeffizienten auf [0,T] sämtliche Zwischenwerte. Die genaue Abstufung der geprüften Obergrenze T beträgt ein Millionstel des Gewichts. Das erste Verfehlen dieser Abschätzung allein belegt keine Verletzung eines Detektorkriteriums.

Für den Dichtewechsel bezeichne D die Differenz der Referenzwerte, K eine obere Schranke für |cₕ−cₗ−D| und R eine obere Schranke für |mₕ−mₗ−D|. Erneute Entwicklung liefert

    |Änderung der Teilsumme des Dichtekontrasts| ≤ 2T(1−T)K + T²R    für 0 ≤ λ ≤ T ≤ ½.

Die Rephasierung und die Amplitudenschranken stammen aus der Wirkung und dem gemeinsamen Vergangenheitskragen in v0.5. Mit A = 0,03609, η = 0,001813 und B = max Fⱼⱼ gilt |mₕ−mₗ−D| ≤ 2AηB + |D|. Für unbekannte Uhren wird die normierte Änderung eines Nachkommen nach Rephasierung durch η begrenzt. Die zwei Eltern ändern sich um höchstens 0,000166 bzw. 0,000316. Damit lassen sich K und alle sieben Teilsummen ohne Annahmen über die unbekannten Phasen einschliessen. Als R dient der rechte Ausdruck der letzten Ungleichung. Der zusätzliche Vorzeichentest vergleicht die Schranke für den Gesamterfolg mit dem Betrag des Referenzsignals.

Die verwendeten gerundeten Ankerzeilen und Diagonalen erlauben je Effekt eine positive Vervollständigung. Der rationale Prüfer testet jeden Schurrest zum gemeinsamen positiven 2×2-Elternblock. Die Reste können in zusätzliche orthogonale Richtungen gelegt werden. Die Abschätzung gilt für jede positive Vervollständigung, weil sie ausser den genannten Diagonalen und Ankerprodukten keine Paarung zweier verschiedener Nachkommen benötigt. Die drei Effekte werden einzeln behandelt. Die Ausgangsdaten stammen aus gemeinsam konstruierten Gaußzuständen.

## Gültigkeit

Die abschliessenden Ungleichungen verwenden rationale Arithmetik auf den gespeicherten Tabellen, den Uhrhüllen und den angegebenen Radien. Die Tabellen und Hüllen entstehen numerisch. Der dritte Gittervergleich und die Abel-Kontrollen messen Konvergenz. Eine gerichtete Fehlerrechnung vom exakten kontinuierlichen Integral durch die gesamte Auswertung bleibt offen. Das geerbte Gegenbeispiel darf den neuen N15-Zweigen Gewicht null geben und ist deshalb auf dem erweiterten Träger weiterhin zulässig. Die Ergebnisse bestimmen weder ein physikalisches Historienmass noch das Kollapsverhalten.

[Ausgangsstand auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/311)
