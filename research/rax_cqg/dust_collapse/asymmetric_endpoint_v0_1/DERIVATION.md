# CST-DUST: Asymmetrie und Endpunktkriterium v0.1

8. November 2026 (Zürich). Ausgangspunkt: PR 271,
Main `5b5907de8ab087183e9a6a0072336226ae0fa771`.

## 0. Ergebnis und Gültigkeitsbereich

Die symmetrische Gabel aus PR 271 wird um ein Ereignis in genau einem Ast
erweitert. Vier feste Vorgänger a<b<c<d bleiben eine Kette. Der lange Ast
lautet d≺e≺f≺j, der kurze d≺g≺j. Zwischen e bzw. f und g bestehen keine
Relationen. Alle transitiven Paare werden mitgeführt. Die vier inneren
Materiedichten sind positiv; insbesondere ist die Endpunktdichte r in (0,1).
Die Uhr U am gemeinsamen Nachfolger j wird frei variiert, und j hat keine
Nachfolger im geprüften Gebiet. Uhren nehmen entlang jeder kausalen Relation
streng zu. Die vier äußeren Materiezeilen sind null.

**Der erklärte asymmetrische Block besitzt keine gemeinsame innere
stationäre Lösung.** Bereits die Uhrableitung am freien positiven Endpunkt
ist für alle erlaubten Uhren strikt positiv. Änderungen der Randuhren oder
der übrigen positiven Gewichte können diesen Rest nicht beseitigen.

Für H=U-d>0 gilt die scharfe normierte Schranke

    7 < 2 q_j/(r H) < 17.                               (1)

Die Grenzen sind Infimum und Supremum im strikten Ordnungsbereich, werden
also nicht erreicht. Sie sind keine Fehlertoleranzen aus einer Stichprobe.

Eine anschließende, exakt begründete Endpunktprüfung unterscheidet 16
Astlängenklassen p,q in {1,2,3,>=4}. Sechs Klassen sind bereits durch eine
strikte Endpunktreaktion ausgeschlossen. Für die übrigen zehn existieren
exakte geordnete Uhrdaten mit q_j=0. **Das ist nur Machbarkeit dieser einen
Uhrgleichung, keine vollständige Stationarität.** Für asymmetrische Klassen
wird hier keine vollständige positive Lösung abgeleitet.

Alle acht physikalischen Gates bleiben HOLD. Keine physikalische
Randpräparation, kein Vakuum-Außenraum, keine Geometrievariation,
keine dynamische Stabilität und kein Bounce. Kein allgemeines Verbot
asymmetrischer CST-Ordnungen. Kein n=5-Produktionslauf und keine
kostenpflichtige Rechnung.

## 1. Globale Intervalle nach dem Einfügen eines Ereignisses

Die unveränderte Wirkung verwendet

    B_yx=b(k(y,x)),   b=(1,-9,16,-8,0,...),
    S_d=-1/2 sum_x w_x
        -1/4 sum_(y≺x) w_x B_yx (T_x-T_y)^2.             (2)

Die globale Ordnung besitzt acht Ereignisse. Der frühere symmetrische
Diamant hatte sieben. Das zusätzlich eingefügte e verändert nicht nur eine
Zeile, sondern alle Intervalle, in denen es liegt. Zum Endpunkt ergeben sich

| Vorgänger von j | Zahl strikt innerer Elemente | Gewicht B |
|---|---:|---:|
| a | 6 | 0 |
| b | 5 | 0 |
| c | 4 | 0 |
| d | 3 | -8 |
| e | 1 | -9 |
| f | 0 | 1 |
| g | 0 | 1 |

Die nicht vergleichbaren Astpaare werden nicht künstlich durch
Beschriftung oder Uhrwerte geordnet. Insbesondere ist k(e,j)=1, weil nur f
zwischen e und j liegt; g ist kein Nachfolger von e.

Mit U=T_j lautet die Endpunktnormierung

    C_j=1+[-8(U-d)^2-9(U-e)^2+(U-f)^2+(U-g)^2]/2.        (3)

Da j keine Nachfolger hat, trägt keine spätere Materiezeile zur Ableitung
nach U bei. Die feste gravitative Wirkung hängt ebenfalls nicht von U ab.
Daher ist die gesamte Uhrableitung dort

    q_j = partial_U S_d
        = r[8(U-d)+9(U-e)-(U-f)-(U-g)]/2.                (4)

Die positiven oder festen Werte aller früheren Dichten ändern (4) nicht.
Ein Null-Dichte-Ereignis e bleibt hingegen Bestandteil der Ordnung und
verändert die Intervallzahlen weiterhin. Dichte null ist keine Löschung
des Ereignisses.

## 2. Strikter Ausschluss und scharfe Schranke

Die rechte Seite von (4) lässt sich schreiben als

    2q_j/r = 15(U-e)+(f-e)+(g-d)+7(e-d).                 (5)

Alle vier Differenzen sind strikt positiv. Damit folgt q_j>0 ohne
Verwendung einer der Normierungsgleichungen. Die notwendige Gleichung
q_j=0 kann nicht erfüllt werden; das schließt insbesondere jede vollständige
innere stationäre Lösung in der erklärten Klasse aus.

Für die quantitative Grenze setze

    x=e-d>0,   y=f-e>0,   z=U-f>0,
    alpha=g-d>0,   beta=U-g>0,
    H=x+y+z=alpha+beta=U-d.

Dann gilt exakt

    D:=2q_j/r=7x+16y+15z+alpha,
    D-7H=9y+8z+alpha>0,
    17H-D=9x+z+beta>0.                                 (6)

Das beweist (1). Mit zusätzlich deklarierten Budgets r>=r_min>0 und
H>=H_min>0 folgt insbesondere q_j>(7/2)r_min H_min. Ohne solche Budgets
kann der absolute Rest durch kleine r oder H klein werden; die normierte
Lücke (1) bleibt bestehen. Ein kleiner absoluter Rest ist dann kein Beweis
einer vollständigen stationären Lösung.

Die Grenzen sind scharf. Bei H=1 und 0<epsilon<1/2 erhält man:

* Untere Folge: x=1-2epsilon, y=z=alpha=epsilon,
  beta=1-epsilon. Dann D=7+18epsilon gegen 7.
* Obere Folge: x=z=epsilon, y=1-2epsilon, alpha=1-epsilon,
  beta=epsilon. Dann D=17-11epsilon gegen 17.

In beiden Folgen bleiben sämtliche geforderten Kausalabstände positiv.
Die Randwerte selbst erfordern kollidierende kausale Uhren und gehören
nicht zur erklärten strikten Klasse.

## 3. Allgemeines Zweiast-Modell für die Endpunktprüfung

Der gleiche viergliedrige Kragen endet bei d. Zwei voneinander getrennte
Ketten mit p und q inneren Ereignissen führen von d zum gemeinsamen freien
positiven Endpunkt j. Der einzige gemeinsame jüngere Endpunkt ist j;
es gibt keine Kreuzrelationen zwischen den Ästen.

Schreibe

    S_j=sum_(y≺j) B_yj(U-T_y),   q_j=-r S_j/2.           (7)

Für einen Ast mit n Ereignissen seien g0=U-T_letztes, g1 die vorletzte
Lücke usw. Bis gn=T_erstes-d sind alle Lücken strikt positiv und ihre
Summe ist H=U-d. Der reine Astbeitrag zu S_j lautet

| Astlänge n | Beitrag F_n zu S_j |
|---|---|
| 1 | g0 > 0 |
| 2 | -8g0-9g1 < 0 |
| 3 | 8g0+7g1+16g2 > 0 |
| >=4 | -g1+8g2-8g3; beide Vorzeichen möglich |

Der Beweis folgt durch Einsetzen der Gewichte 1,-9,16,-8 in die
Abstände U-T_y und Zusammenfassen der Lückenkoeffizienten. Ab vier
Astereignissen ist die Summe der vier aktiven Gewichte null; ältere
Astereignisse haben mindestens vier Intervallpunkte und Gewicht null.

Zusätzlich tragen gemeinsame Vorgänger bei. Der nächste gemeinsame
Vorgänger d hat k(d,j)=p+q. Sein direkter Vorgänger c hat k(c,j)=p+q+1.
Bei p,q>=1 bleiben deshalb nur

    p+q=2: 16(U-d)-8(U-c),
    p+q=3: -8(U-d),
    p+q>=4: kein gemeinsamer Kragenbeitrag.              (8)

Ältere feste Kragenelemente haben in diesen Fällen Gewicht null. Die
Endpunktprüfung folgt vollständig aus F_p+F_q plus (8).

## 4. Vollständige Vorzeichenmatrix dieser Endpunktgleichung

In der folgenden Matrix bezeichnet „q>0“ bzw. „q<0“ einen strikten
Ausschluss für alle kausal geordneten Uhrdaten. „Uhr möglich“ bedeutet:
Es existieren geordnete Daten mit q_j=0, aber alle übrigen Gleichungen und
Normierungen müssen weiterhin geprüft werden.

| p gegen q | 1 | 2 | 3 | >=4 |
|---|---|---|---|---|
| 1 | Uhr möglich | q>0 | q<0 | Uhr möglich |
| 2 | q>0 | q>0 | Uhr möglich | Uhr möglich |
| 3 | q<0 | Uhr möglich | q<0 | Uhr möglich |
| >=4 | Uhr möglich | Uhr möglich | Uhr möglich | Uhr möglich |

Die Fälle (2,1) und (1,2) sind durch (5)-(6) ausgeschlossen. Für (1,3),
(3,1) und (3,3) ist S_j die Summe zweier strikt positiver Astbeiträge,
also q_j<0. Für (2,2) sind beide Beiträge negativ, also q_j>0. Gemeinsame
Kragenbeiträge fehlen bei diesen letzten vier Klassen wegen p+q>=4.

Für (2,3) und (3,2) können der positive und der negative Astbeitrag
gegeneinander ausgeglichen werden. Unter fester Summe H lassen sich ihre
Beträge beliebig klein machen, indem die erste Lücke nach d fast H
aufnimmt. Die aktiven Lücken bleiben dabei positiv. Beide Seiten haben
auch Werte mit einem von null getrennten Betrag. Daher existieren
streng geordnete Daten mit S_j=0.

Ein Ast der Länge mindestens vier hat durch seinen aktiven Lückenausdruck
beide Vorzeichen. Auch dessen Betrag kann unter fester Summe H beliebig
klein gewählt werden. In Verbindung mit jedem der drei kurzen Asttypen
oder einem weiteren langen Ast ist somit ein Ausgleich möglich. Die
Kontrollen geben für alle Vertreter mit Länge vier explizite rationale
Zeugen an. Für größere Längen fügt man vor dem frühesten der vier aktiven
Astereignisse zusätzliche positive Lücken bzw. Ereignisse ein und lässt
die letzten vier Uhren unverändert. Die neuen älteren Ereignisse haben
am Endpunkt Gewicht null; der Zeuge bleibt erhalten. Das setzt keine
Erfüllung der neuen inneren Normierungen voraus.

Für (1,1) kann der zusätzliche Term aus c in (8) beide Vorzeichen der
Gesamtsumme ermöglichen. Ein vollständig stationärer Spezialfall war
bereits Gegenstand von PR 271. Die hier neu erzeugten q_j=0-Zeugen dieser
Klasse werden trotzdem nur als Endpunkt-Uhrzeugen ausgewiesen.

Die sechs ausgeschlossenen Matrixfelder sind damit analytisch abgedeckt.
Die zehn übrigen besitzen exakte Machbarkeitszeugen für diese eine
Gleichung. Die Matrix ist keine Klassifikation vollständiger
CST-Stationarität oder physikalischer Außenräume.

## 5. Ein konkreter asymmetrischer Uhrzeuge und seine Grenze

Für (p,q)=(2,3) wähle U=1, d=0 und die äußeren Uhren

    (a,b,c,d)=(-21/10,-11/10,-1/10,0).

Die Astuhren seien

    linker Ast: 1/100, 1/50,
    rechter Ast: 1/100, 1/50, 9/100.

Alle Uhrwerte steigen entlang ihrer jeweiligen Kausalrelationen. Zwischen
den Ästen erzwingen gleiche oder verschiedene Zahlen keine Relation.
Die global neu gezählten Endpunktgewichte ergeben exakt S_j=0, folglich
q_j=0 für jedes positive r. Die Normierung am selben Endpunkt ist jedoch

    C_j=2507/2500 != 0.                                 (9)

Dieser Zeuge ist daher keine vollständige Lösung. Seine Rolle ist eng
begrenzt: Er zeigt, dass der Ausschluss durch ein festes Vorzeichen hier
nicht anwendbar ist. Weitere Astuhren oder Randdaten könnten andere
Normierungswerte liefern; darüber entscheidet (9) nicht.

Die allgemeinen rationalen Uhrzeugen werden durch Konvexkombination
zweier strikt geordneter Uhrvektoren mit entgegengesetzten S_j-Vorzeichen
gebildet. S_j ist linear in den Uhren; die Gewichte B bleiben bei
festgehaltener Ordnung unverändert. Strikte kausale Uhrordnung ist unter
dieser Mischung erhalten. Die Mischungsgewichte und Normierungsreste
sind im Ergebnisdatensatz exakt gespeichert.

## 6. Welche Randentscheidung der Ausschluss voraussetzt

Der Endpunkt j ist hier eine frei variierte positive Materievariable.
Ist U stattdessen eine fest vorgegebene spätere Randuhr, wird q_j=0 an
dieser Stelle nicht gefordert. Dann stellt (4) eine Randreaktion dar.
Das ist eine andere Variationsaufgabe, keine Widerlegung von (5).

Ebenso muss die Rechnung bei zusätzlichen Nachfolgern von j neu erfolgen:
Dann können spätere Wirkungszeilen zur Ableitung nach U beitragen. Es
wird nicht behauptet, eine beliebige Erweiterung repariere den Block.
Beim Null-Dichte-Zweig r=0 ist der Faktor in (4) null; dieser Zweig ist
kein positiver Endpunkt und braucht eine getrennte Behandlung seiner
Variations- und Maßbedingungen.

Der strikte Vorzeichenausschluss überträgt sich deshalb nicht ungeprüft
auf eine physikalische Geschichte mit vorgegebenem Zukunftsrand, auf
andere Ordnungen, Summen über Geometrien oder andere Wirkungsansätze.
Dass sowohl asymmetrische (1,2) als auch symmetrische (2,2),(3,3)
Klassen scheitern, zeigt zudem: Symmetrie allein entscheidet diese
Prüfung nicht. Die konkreten globalen Intervallkoeffizienten sind entscheidend.

## 7. Kontrollen, Reproduktion und nächste Aufgabe

Die Primärordnung wird aus ihren erzeugenden Relationen transitiv aufgebaut.
Fünf symbolische Polynomidentitäten vergleichen die ursprüngliche
Normierung, ihre Ableitung und die beiden strikten Schranken. Für die
16 Klassen werden 588 rationale strikt geordnete Uhrprofile geprüft;
588 unabhängige zentrale Ableitungen der quadratischen Originalwirkung
bestätigen die Endpunktreaktion exakt.

162 Fälle prüfen die normierte (2,1)-Schranke bei drei positiven
Dichten und drei gemeinsamen Verschiebungen. Sechs Folgenwerte prüfen
die scharfen Grenzformeln. 26 weitere Kontrollen über Längen vier bis
sieben prüfen den aktiven Viererelement-Suffix. Zehn rationale
Uhrzeugen sowie ihre nicht als Lösung ausgegebenen Normierungsreste sind
gespeichert. Sieben Negativkontrollen werden zurückgewiesen.

Alle Prüfungen verwenden Python-Standardbibliothek und rationale
Arithmetik. Keine Gleitkommatoleranz ersetzt eine exakte Null. Vier
Ergebnisdateien werden isoliert bytegleich reproduziert. Die allgemeinen
Aussagen folgen aus den Beweisen; die endlichen Kontrollen ergänzen sie.
Der Plan wurde nach analytischem Entwurf vor dem ersten endlichen
Kontrolllauf gehasht. Keine externe Präregistrierung, keine externe
Replikation und kein Beweisassistenten-Zertifikat.

**Nächste wissenschaftliche Aufgabe:** Für einen vorab festgelegten
Uhr-möglichen asymmetrischen Kandidaten, beispielsweise (2,3), die
vollständigen inneren Uhr- und Normierungsgleichungen gemeinsam prüfen.
Der Datensatz (9) ist dafür ausdrücklich noch kein Erfolg. Die Bedeutung
eines freien gegenüber einem festgehaltenen Zukunftsrand muss als
Modellentscheidung sichtbar bleiben. Ein großer Rechenlauf ist für diese
algebraische Vorprüfung nicht nötig.

## Quellen und Abgrenzung

* Projekt PR 271: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/271.
  Geerbte Materiewirkung, symmetrischer Diamant, Intervallbuchhaltung und
  Referenzcode. Vier unveränderte Quellobjekte einschließlich Lizenz sind
  in `provenance.json` an Main gebunden.
* Dittrich und Höhn, Constraint analysis for variational discrete systems,
  J. Math. Phys. 54, 093505 (2013), https://arxiv.org/abs/1303.4294v3.
  Methodischer Kontext für die Trennung innerer Variationsgleichungen und
  Randbedingungen; keine physikalische Validierung des hier gewählten
  Materie- oder Endpunktmodells.

Der Vorzeichenausschluss, die scharfe Schranke und die Astlängenmatrix
werden hier für den konkreten endlichen Kandidaten eigenständig bewiesen.
