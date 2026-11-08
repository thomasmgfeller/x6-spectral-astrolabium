# CST-DUST: Verzweigung und Wiederanschluss v0.1

8. November 2026 (Zürich). Basis: PR 270,
Main `3ddc2a6a22f2cc084806b2917c036593912e3d43`.

## 0. Ergebnis und festgelegte Klasse

Die frühere reine Zeitkette wird durch zwei **unvergleichbare** positive
Materieelemente f und g ersetzt. Als erste Kontrolle endet die Ordnung an
diesen beiden Ästen (Gabel). Als zweites, vor dem endlichen Kontrolllauf
festgelegtes Modell folgt ein gemeinsames positives Zukunftselement j
(Diamant). Vier feste äußere Vorgänger a<b<c<d bilden weiter eine Kette;
ihre Dichtezeilen sind null. Sämtliche inneren Uhren und positiven Gewichte
werden frei variiert. Die äußeren Uhrwerte sind streng entlang ihrer Kette
geordnet. Eine Ordnung zwischen den Uhrwerten der unvergleichbaren f,g wird
nicht zusätzlich gefordert.

Die ursprüngliche Materiewirkung bleibt unverändert. Die Ergebnisse sind:

1. Die offene Gabel erlaubt gemeinsame innere Stationarität genau bei
   P=A=0. Die beiden Astuhren können dann unabhängig voneinander gewählt werden.
2. Der positive Wiederanschluss erzwingt P<0, gleiche Skalaruhrwerte der
   beiden unvergleichbaren Äste und gleiche Astgewichte. Eine vollständige
   Familie geordneter Randdaten ist explizit bestimmbar.
3. Auf der zulässigen äußeren Domäne bleibt eine unabhängige
   Gleichheitsbedingung J=0. Die Randfläche hat Dimension drei, während bei
   festem Kragen nur ein innerer positiver Dichteparameter frei bleibt.
4. Das Addieren zweier Kettenarme ohne Intervallkorrektur liefert die falsche
   Wirkung. Trotz fünf gemeinsamer Elemente ist die Korrektur ungleich null.
5. Die äußere Reaktion ist explizit nicht null. Die Randpräparation ist damit
   weiterhin eine offene physikalische Aufgabe.

Die Gleichheit von Skalaruhren identifiziert keine Ereignisse und erzeugt
keine neue Kausalrelation. Kein Vakuum-/Schwarzschild-Außenraum, keine
vierdimensionale geometrische Einbettung, keine Geometrievariation,
keine physikalisch ausgewählte Präparation, keine dynamische Stabilität,
kein Bounce. **Alle acht physikalischen Gates bleiben HOLD.** Kein
n=5-Produktionslauf und keine kostenpflichtige Rechnung.

## 1. Ordnung und unveränderte Wirkung

Die Gabel hat die erzeugenden Relationen

    a<b<c<d,   d≺f,   d≺g,   f und g unvergleichbar.

Der Diamant ergänzt f≺j und g≺j. Sämtliche transitiven Relationen werden
mitgeführt. Die Beschriftung wird in der Rechnung als 0,...,6 geführt, aber
die numerische Etikettenreihenfolge erzwingt keine Relation zwischen 4 und 5.
Für jede induzierte Teilmenge X der festgelegten globalen Ordnung gilt

    B^X_yx = b(k_X(y,x)),   b=(1,-9,16,-8,0,...),
    S_d(X) = -1/2 sum_x w_x
             -1/4 sum_(y≺x) w_x B^X_yx (T_x-T_y)^2,
    F_g(X) = |X|-sum_(y≺x) B^X_yx.                       (1)

Die Gravitation ist hier nur als festes Ordnungsgewicht mitgeführt;
ihre Variation nach Uhren oder Materiedichten ist null. Daraus wird keine
gravitative Rückwirkung abgeleitet.

Die Astuhren seien t1,t2, die gemeinsame Zukunftsuhr U und die positiven
Gewichte w1,w2,r in (0,1). Definiere für die äußeren Uhren

    P=-8a+16b-9c+d,
    A=1+(-8a²+16b²-9c²+d²)/2.

Die beiden Astnormierungen sind unverändert

    C1=A-Pt1,   C2=A-Pt2.                                (2)

Zum gemeinsamen Nachfolger verändern sich dagegen die Intervallzahlen:

| Vorgänger y von j | Globales k(y,j) | B global | B im Kettenarm mit y | B im gemeinsamen Teil |
|---|---:|---:|---:|---:|
| a | 5 | 0 | 0 | -8 |
| b | 4 | 0 | -8 | 16 |
| c | 3 | -8 | 16 | -9 |
| d | 2 | 16 | -9 | 1 |
| f bzw. g | 0 | 1 | 1 | nicht enthalten |

Damit ist die zusätzliche Normierung exakt

    Cj = 1+[(U-t1)²+(U-t2)²+16(U-d)²-8(U-c)²]/2,
    S_d = -(w1 C1+w2 C2+r Cj)/2.                         (3)

Die vier äußeren Dichtezeilen sind null. Andere feste Vergangenheitswirkungen
würden die hier betrachteten inneren Gleichungen nicht ändern, könnten
jedoch zusätzliche äußere Reaktionen tragen.

## 2. Die offene Gabel ist noch kein Wiederanschluss

Ohne j ist S_d=-(w1 C1+w2 C2)/2. Aus den beiden freien Uhrvariationen folgt

    q1=w1 P/2=0,   q2=w2 P/2=0.

Für positive w1,w2 ist deshalb P=0. Die Dichtevariationen verlangen dann
A=0. Umgekehrt genügen P=A=0: Beliebige t1>d, t2>d und beliebige
w1,w2 in (0,1) erfüllen alle vier inneren Gleichungen. Eine Gleichheit oder
strikte Reihenfolge zwischen t1 und t2 ist nicht nötig.

Der frühere Kragen (-5/2,-2,-4/3,0) erfüllt P=A=0 und liefert somit eine
exakte Gabelkontrolle. Die Flächenbedingungen P=A=0 sind bei streng
geordneten äußeren Uhren unabhängig: Die Gradienten könnten nur bei
a=b=c=d proportional werden. Der äußere Kragenraum hat hier Dimension zwei.
Das ist ein endlicher Variationsbefund, kein Beweis physikalischer
Unabhängigkeit der Äste in einer quantisierten Theorie.

Wird ein positives gemeinsames Zukunftselement angefügt, erhält jede
Astgleichung den zusätzlichen Beitrag r(U-ti)/2>0. Der alte P=0-Kragen
kann diesen Beitrag nicht ausgleichen. Deshalb lässt sich die erfolgreiche
Gabel nicht einfach mit unveränderten Randdaten wieder schließen.

## 3. Vollständige gemeinsame Stationarität des Diamanten

Aus (3) folgen die drei Uhrgleichungen

    q1=[w1 P+r(U-t1)]/2,
    q2=[w2 P+r(U-t2)]/2,
    qj=-r[10U-t1-t2-16d+8c]/2.                           (4)

Die freien positiven Dichtevariationen verlangen C1=C2=Cj=0.
Für U>t1,t2 und positive Gewichte erzwingen die ersten beiden Gleichungen
P<0. Die Astnormierungen ergeben daher zwingend

    t1=t2=tau=A/P.                                      (5)

Diese Uhrgleichheit ist mit der Unvergleichbarkeit der Ereignisse verträglich.
Aus q1=q2=0 folgt w1=w2=w. Die letzte Uhrgleichung setzt

    U=(tau+8d-4c)/5,
    g=U-tau=4(2d-c-tau)/5,
    w=-r g/P.                                          (6)

Setze L=d-c>0 und h=tau-d. Die strikte kausale Uhrordnung verlangt
0<h<L. Die verbleibende Normierung ist

    J(a,b,c,d) := 1+(4/5)(h²-2hL-9L²)=0.                (7)

**Existenzsatz.** Für gegebene a<b<c<d existiert der erklärte positive,
gemeinsam stationäre Diamant genau dann, wenn

    P<0,   d<tau=A/P<2d-c,   J=0.                       (8)

Dann sind alle Lösungen durch (5)-(6) und

    0<r<min(1,-P/g),   w1=w2=-r g/P                     (9)

gegeben. Die Notwendigkeit folgt aus den Variationen und der Ordnung.
Für die Hinlänglichkeit liefert jedes r im nichtleeren Intervall (9)
positive Gewichte unter eins; alle drei Normierungen und alle drei
Uhrgleichungen verschwinden exakt. Es gibt bei festem Kragen einen freien
positiven Gewichtsparameter. Andere Vorzeichen, Null-Dichte-Zweige,
fixierte innere Felder oder weitere Ereignisse sind nicht Teil des Satzes.

## 4. Sämtliche zulässigen Diamantkragen

Schreibe k=L-h. Aus (7) folgt

    k²=10L²-5/4,   0<k<L.

Damit ist notwendig und hinreichend für den geordneten jüngeren Kragenteil

    1/8<L²<5/36,
    k=sqrt(10L²-5/4),   h=L-k.                          (10)

Die beiden Endpunkte sind ausgeschlossen: Am unteren gilt U=tau, am oberen
tau=d. Es sind Grenzen dieser reduzierten Uhreinheiten, keine physikalisch
abgeleiteten Planck- oder Singularitätsskalen.

Für die älteren Abstände x=c-b>0 und ell=b-a>0 setze

    H=h+L,
    Z=sqrt[1/4+2(H+x)²-(9/8)H²+h²/8],
    ell=Z-H-x.                                         (11)

Die Gleichung C1(tau)=0 ist genau die quadratische Gleichung hinter (11).
Nur der positive Wurzelzweig erhält die Ordnung a<b. Er liefert ell>0:

    Z²-(H+x)² = (H+x)²-(9/8)H²+h²/8+1/4
              > [2-2hL-L²]/8 > 0,

weil x>0, 0<h<L und L²<5/36. Die letzte Ungleichung folgt insbesondere
aus 2-3L²>0. Nun gilt P=8ell-8x+L. Der Vergleich P<0 kann ohne
Vorzeichenverlust quadriert werden, da H+2x-L/8>0. Er ist äquivalent zu

    2x²-Lx/2-7L²/64-1/4>0,
    x>x_min(L):=L/8+(1/4)sqrt(2+9L²/8).                 (12)

Die vollständige Parametrisierung lautet damit:

    L in (1/(2sqrt(2)), sqrt(5)/6),
    x>x_min(L),   lambda beliebig,
    d=lambda, c=lambda-L, b=lambda-L-x, a=b-ell,

wobei k,h,ell nach (10)-(11) bestimmt sind. Sie erfasst alle Lösungen von
(8), ohne nachträglich die Wirkungsgewichte zu verändern. Die Familie besitzt
drei äußere Parameter: lambda,L,x. Sie ist eine mathematisch konstruierte
Existenzfamilie, keine physikalische Auswahl ihrer Randdaten.

Für die exakten Kontrollen wird p=k/L in (0,1) vorgegeben. Dann ist

    L²=5/[4(10-p²)],   h/L=1-p,   x/L=X.

Mit rationalen p,X sind alle skalierten Uhren Y=T/L in einem einzigen
quadratischen Zahlkörper darstellbar. Die Ergebnisse speichern L² und Y;
die Normierungen verwenden den Faktor L² exakt. Reaktionen werden als q/L
gespeichert. Dadurch werden verschachtelte Gleitkomma-Näherungen vermieden.
Gemeinsame Verschiebungen der Y sind echte gemeinsame Uhrverschiebungen
um L mal den angegebenen Wert.

Ein konkreter im Kontrollraster enthaltener Zeuge ist p=1/2, X=2,
lambda=0 und r=1/2. Mit L=sqrt(5/39) gilt exakt

    (a,b,c,d)=L((5-sqrt(2395))/10, -3, -1, 0),
    t1=t2=L/2,   U=9L/10,
    w1=w2=1/(215-4sqrt(2395)).                           (12a)

Alle Gewichte liegen in (0,1). Diese Werte sind ein konstruierter
algebraischer Kontrollfall und keine unabhängig ausgewählte Präparation.

## 5. Wiederanschluss erfordert die volle Intervallkorrektur

Wähle die beiden induzierten Kettenarme

    Larm={a,b,c,d,f,j},  Rarm={a,b,c,d,g,j},
    D=Larm intersection Rarm={a,b,c,d,j}.

Die geerbte allgemeine Überlappungsformel wird unverändert angewandt:

    delta B=Bglobal-Bleft-Bright+Bshared,
    Sglobal=Sleft+Sright-Sshared+Delta S,
    Delta S=-sum w_x delta B_yx (T_x-T_y)²/4.            (13)

Hier sind genau vier Koeffizienten ungleich null:

| Paar | delta B |
|---|---:|
| a≺j | -8 |
| b≺j | 32 |
| c≺j | -49 |
| d≺j | 35 |

Also

    Delta S=-r[-8(U-a)²+32(U-b)²-49(U-c)²+35(U-d)²]/4.   (14)

Die Summe dieser Koeffizienten ist 10. Für die feste BDG-Kombination folgen

    Fglobal=-4,   Fleft=Fright=5,   Fshared=4,
    Fglobal-Fleft-Fright+Fshared=-10.                   (15)

Die fünf gemeinsamen Elemente sind kein hinreichender Speicherindikator:
Die Kettenarme sind in der globalen Ordnung nicht ordnungskonvex, denn
jeweils ein innerer Ast des gemeinsamen Intervalls fehlt. Deshalb ändern
sich Intervallgrößen innerhalb beider Arme. Das widerspricht nicht dem
früheren Vier-Element-Satz für ordnungskonvexe Überlappungen einer Kette.

Die Uhrreaktionen müssen aus der vollständigen Wirkung einschließlich (14)
berechnet werden. Ein separat angepasster Randterm oder das einfach
doppelte Zählen des gemeinsamen Teils wäre keine Anwendung von (13).

## 6. Randfläche, äußere Reaktion und Restfehler

Auf der Domäne P<0, d<tau<2d-c ist die Kompatibilitätsfunktion J glatt.
Da tau=A/P, gilt

    partial_a tau=8(tau-a)/P,
    partial_a J=-64k(tau-a)/(5P)>0.                    (16)

Die Gleichung J=0 besitzt daher überall Rang eins. Zusammen mit den
strikten offenen Ungleichungen ist der zulässige Randbereich eine glatte
dreidimensionale Hyperfläche. Die geringere Zahl äußerer Gleichheiten
gegenüber der Kette ist keine universelle Regel für Verzweigungen: Hier
kommen ein neues Ereignis, eine weitere Normierung und zusätzliche innere
Kopplungsgleichungen hinzu. Insbesondere werden zuvor freie Astwerte gebunden.

Setzt man tau,U und w aus (5)-(6) ein, sind C1=C2=0 und alle inneren
Uhrableitungen null, auch vor dem Setzen von J=0. Bei festem r reduziert sich
die Wirkung auf -rJ/2. Die beim Ableiten mitveränderten Astgewichte erzeugen
keinen Zusatzbeitrag, weil ihre Normierungen bereits null sind. Damit

    q_outer=-(r/2) grad J,                              (17)
    q_a=-8w(tau-a)<0,
    sum_outer q_i=0,
    sum_outer T_i q_i=2w+r>0.                           (18)

Die letzte Identität folgt aus der quadratischen Homogenität der
ursprünglichen Zeilen (1), nicht aus einer unbegründeten Homogenitätsannahme
für die rationale Funktion J. Die Randreaktion ist eine Konormalrichtung
mit positivem, nach (9) begrenztem Gewicht. Drei Randparameter und ein
Gewichtsparameter ergeben eine vierdimensionale Randrelation. Das liefert
noch keinen physikalischen Zustandsraum oder eine ausgewählte Präparation.

Für beliebige innere Werte im selben Diamanten gelten die exakten
Ast-Differenzidentitäten

    C1-C2=-P(t1-t2),
    q1-q2=[P(w1-w2)-r(t1-t2)]/2.                       (19)

Bei P!=0 folgen die notwendigen endlichen Grenzen

    |P||t1-t2| <= |C1|+|C2|,
    |P||w1-w2| <= 2(|q1|+|q2|)+r|t1-t2|.              (20)

Ohne einen unteren Betrag für P sind diese Grenzen nicht uniform als
Schranken für die Astabweichungen invertierbar. Sie sind notwendige
Kompatibilitätsprüfungen, keine hinreichenden Lösungstests und kein
dynamischer Stabilitätssatz. Die Kontrollen prüfen sie mit bewusst
ungleichen Astuhren und Astgewichten. Skalaruhr-Gleichheit darf weder als
zusätzliche Kausalrelation noch als allgemeines Gesetz für verzweigte CST
interpretiert werden.

## 7. Prüfung und Forschungsentscheidung

Zehn Polynomidentitäten werden durch vollständigen rationalen
Koeffizientenvergleich geprüft. Die diskrete Intervallzählung wird direkt
aus der Relation neu berechnet. 32 rationale Verklebungsfälle und 224
Reaktionskomponenten bestätigen (13)-(15). Der offene Gabelzweig hat
81 exakte stationäre Kontrollfälle.

Zwölf vorab festgelegte Diamantformen ergeben sechs zulässige Formen.
Die anderen sechs werden einschließlich dreier Verschiebungen als 18
Kragen wegen des falschen Vorzeichens der notwendigen Astgewichte
zurückgewiesen. Drei Verschiebungen und drei positive Zukunftsgewichte
liefern 54 vollständige stationäre Fälle. 216 Randableitungen werden durch
automatisches Differenzieren der ursprünglichen Normierungszeile unabhängig
gegen (17) geprüft. 108 Astuhrstörungen, 108 Restfehlerbudget-Fälle und acht
konkrete Negativkontrollen ergänzen die Prüfung.

Rationale Arithmetik und exakte quadratische Zahlkörper werden verwendet;
keine numerische Toleranz ersetzt eine als exakt ausgegebene Null.
Vier Ergebnisdateien werden isoliert bytegleich reproduziert. Der lokale
Plan wurde nach analytischem Entwurf vor dem ersten endlichen Kontrolllauf
gehasht. Keine externe Präregistrierung, keine externe Replikation und
kein Beweisassistenten-Zertifikat. Die allgemeinen Aussagen folgen aus den
Beweisen, nicht allein aus der endlichen Stichprobe.

**Nächster sinnvoller Schritt:** Eine asymmetrische kleine Verzweigung vorab
festlegen, etwa mit unterschiedlich langer Vorgeschichte beider Äste.
Damit ist zu prüfen, welche der Gleichheiten (5) und (6) nur aus identischen
Astzeilen folgen und welche Kopplungsbedingungen bestehen bleiben. Die
Intervallzahlen müssen erneut aus der globalen Ordnung berechnet werden.
Erst danach kann ein ausdrücklich begründeter Rand-/Außenraumsektor
qualifiziert werden. Der jetzige positive Wiederanschluss ist kein
Vakuum-Außenraum und ersetzt diese Modellwahl nicht.

## Quellen und Abgrenzung

* Projekt PR 270: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/270.
  Geerbte Wirkung, Kettenklassifikation, Aussagegrenzen und Referenzcode;
  unveränderte Quellen samt Lizenz in `provenance.json` gebunden.
* Die allgemeine Überlappungsidentität stammt aus PR 269 und der darin
  dokumentierten früheren Variationsarbeit. Hier neu sind die konkret
  gezählten Diamantkoeffizienten und die vollständigen Gabel-/Diamantbedingungen.
* Dittrich und Höhn, Constraint analysis for variational discrete systems,
  J. Math. Phys. 54, 093505 (2013), https://arxiv.org/abs/1303.4294v3:
  methodischer Kontext für diskrete Variations- und Anschlussgleichungen,
  keine physikalische Validierung dieser zusätzlichen Modellwahl.
