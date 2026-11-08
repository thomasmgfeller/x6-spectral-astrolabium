# CST-DUST: Zweiblock-Kopplung und gemeinsame Randreaktion v0.1

8. November 2026 (Zürich). Basis: Main nach PR 268,
`483358692a06cc1f17e12f9e392fad550a7494ca`.

## 0. Ergebnis und Reichweite

Der nächste Block wird hier aus derselben Materiewirkung angefügt. Die
Wirkung wird weder durch einen passenden Randterm noch durch eine neue
Präparationsphase verändert. Die schon vorhandene Verklebungsbuchhaltung
für disjunkte Blöcke wird auf überlappende induzierte Blöcke erweitert.
Neu geprüft werden die minimal nötige gemeinsame Vorgeschichte auf Ketten,
die tatsächlichen gemeinsamen stationären Gleichungen und ein exakter
Kontrollfall mit veränderten äußeren Kragendaten.

Ergebnisse:

1. Auf einer Kette reichen vier gemeinsame Vorgängerelemente für die exakte
   Verklebung der Materie- und festen BDG-Wirkung; für beliebige Felddaten
   sind drei nicht ausreichend. Das ist kein universelles Vier-Element-Gesetz
   für breitere Kausalsets.
2. Beim unverändert festgehaltenen Kragen aus PR 266 kann weder ein noch
   können zwei zusätzlich angehängte positive Zukunftselemente zusammen
   mit dem bisherigen freien Element innerlich stationär sein, wenn alle
   neuen Uhren und positiven Dichten frei variiert werden.
3. Mit einem anderen, ausdrücklich konstruierten äußeren Kragen existiert
   eine exakte gemeinsame stationäre Familie für zwei freie positive Elemente.
   Die beiden Blockreaktionen am gemeinsamen Element sind einzeln nicht null,
   heben sich aber in der gemeinsamen Wirkung genau auf.

Der zweite Block ist ein **Zukunftsblock mit positiver Materiedichte**, kein
hergeleiteter Vakuum-/Schwarzschild-Außenraum. Der Erfolg ist ein endlicher
Variationskontrollfall auf einer festgehaltenen Kette. Er liefert keine
physikalische Zustandspräparation, keine Geometrie-Rückwirkung und keinen
Bounce. Alle acht physikalischen Gates bleiben HOLD. Kein n=5-Produktionslauf,
keine kostenpflichtige Rechnung, keine externe Replikation.

## 1. Unveränderte Wirkung und überlappende Blöcke

Im geerbten normierten Kandidaten (BD-Vorfaktor A=1) gilt für ein endliches
Kausalset C und induzierte Teilmengen X:

    B^X_yx = b(k_X(y,x)),   b=(1,-9,16,-8,0,...),
    S_d(X) = -1/2 sum_{x in X} w_x
             -1/4 sum_{y≺x in X} w_x B^X_yx (T_x-T_y)^2,
    F_g(X) = |X| - sum_{y≺x in X} B^X_yx,
    S_g(X) = hbar kappa_g F_g(X).                           (1)

Die kompakte Formel für F_g ist dieselbe geerbte 4D-BDG-Kombination
N-N0+9N1-16N2+8N3. Die hier verwendeten kleinen Ordnungen sind keine
vierdimensionalen geometrischen Ensembles. Die Geometrie ist fest, daher
trägt S_g keine Uhrableitung bei; ihre Verklebungsidentität wird dennoch
mitgeführt. Eine Geometrievariation wird nicht ausgeführt.

Für C=L union R und D=L intersection R definiere auf jedem Paar in C

    delta B_yx = B^C_yx
                 -1_{x,y in L} B^L_yx
                 -1_{x,y in R} B^R_yx
                 +1_{x,y in D} B^D_yx.                    (2)

Dann gelten exakt

    S_d(C) = S_d(L)+S_d(R)-S_d(D)+Delta S_d,
    Delta S_d = -1/4 sum w_x delta B_yx (T_x-T_y)^2,
    F_g(C) = F_g(L)+F_g(R)-F_g(D)-sum delta B_yx.            (3)

Beweis: Jeder Vertex wird in der Inklusions-Exklusions-Summe genau einmal
gezählt. Die verbleibenden Paarkoeffizienten sind gerade (2). Die Korrektur
enthält sowohl Paare zwischen den exklusiven Blockteilen als auch
Umklassifizierungen interner Intervalle. Die disjunkte Variante war bereits
in der geerbten Variationsarbeit enthalten; sie wird nicht als neues
allgemeines Kopplungsgesetz ausgegeben.

Es muss die gesamte globale Ordnung einschließlich blockübergreifender
Relationen vorgegeben sein. Zwei lokale Restriktionen bestimmen diese Daten
im Allgemeinen nicht. Ein unbegründeter transitiver Abschluss oder ein
zusätzlicher interner Oberflächenterm wäre keine Anwendung von (3).

Mit q_z^X=partial_Tz S_d(X) folgt am geteilten Rand

    q_z^C = q_z^L + q_z^R - q_z^D + partial_z Delta S_d.     (4)

Die gemeinsame freie Variation setzt diese Summe auf null. Sie verlangt
nicht, dass jeder Summand separat verschwindet. Bei entgegengesetzt
orientierten Randimpulsen entspricht (4) dem Impulsabgleich. Wir verwenden
die rohen Wirkungsableitungen, um Vorzeichenkonventionen transparent zu halten.

## 2. Exakte Kettenverklebung mit vier gemeinsamen Elementen

Sei C die Kette 0≺1≺...≺N-1. Schneide nach j und verwende

    L={0,...,j},   R={j-m+1,...,N-1},   |D|=m.

Beide Blöcke und ihre Überlappung sind ordnungskonvex. Für Paare innerhalb
eines Blocks ändern sich deshalb keine Intervallgrößen. Die einzigen
fehlenden Paare verbinden L\R mit R\L. Das kürzeste solche Paar ist

    y=j-m,   x=j+1,   k_C(y,x)=m.

Falls beide exklusiven Teile nichtleer sind, folgt:

* m>=4: Alle fehlenden Paare haben k>=4 und damit B=0. Es gilt delta B=0
  paarweise; (3) schließt ohne Zusatzkorrektur für beliebige T,w.
* m=1,2,3: Beim kürzesten fehlenden Paar ist B=b(m)=-9,16,-8 ungleich null.
  Für allgemeine nichttriviale Felddaten darf der Term nicht entfallen.

Das beweist die minimale Überlappung **für diese Ketten- und Blockklasse**.
Ältere Dichtewerte müssen weiterhin konsistent im bereits akkumulierten
Wirkungsanteil geführt werden; die Aussage ist keine allgemeine
Quantenzustandskompression oder Unitaritätsbehauptung.

Gegenbeispiel außerhalb der Kettenklasse: Fünf untereinander unvergleichbare
Vorgänger 0,...,4 liegen alle vor 5. Wähle L={0,...,4} und R={1,...,5};
D besitzt vier Elemente. Trotzdem fehlt der direkte Link 0≺5 mit k=0,B=1.
Die allgemeine CST-Nichtlokalität wird durch die endliche Kettenreichweite
also nicht beseitigt.

## 3. Warum ein einzelnes geteiltes Element nicht genügt

Auf der Sechserkette seien 0,...,3 feste Vergangenheit, f=4 mit Uhr t und
Dichte w sowie g=5 mit Uhr u>t und Dichte v>0. Für L={0,...,4}, R={4,5}
und D={4} enthält die zweite isolierte Teilwirkung am neuen Element nur

    C_g^R = 1+(u-t)^2/2 >= 1.

Die vollständige Wirkung enthält dagegen zusätzlich

    Delta S_d = -v/4[-9(u-T3)^2 +16(u-T2)^2 -8(u-T1)^2].    (5)

Der noch ältere Vorgänger T0 hat zur Zeile g bereits Gewicht null.
Die fehlenden Terme können sogar die Vorzeichenlage der Normierung ändern.
Ihre Wirkung auf die früheren Randuhren darf nicht vergessen werden.

Bei dieser speziellen Zerlegung hängt (5) nicht von t ab. Deshalb bleibt
der Beitrag des neuen Elements zur t-Reaktion v(u-t)/2 auch nach vollständiger
Ergänzung bestehen. Dieses Detail ist für den folgenden Ausschluss wichtig:
Das Scheitern des alten Kragens wird nicht nur durch einen Buchhaltungsfehler
der Zweipunkt-Teilwirkung verursacht.

Eine korrigierungsfreie Alternative lautet L={0,...,4}, R={1,...,5},
D={1,...,4}. Dann gilt (3) mit Delta S_d=0. Die Überlappungswirkung muss
abgezogen werden, oder die Wirkungszeilen werden eindeutig nach ihrem
späteren Endpunkt auf die Blöcke verteilt. Einfach S_d(L)+S_d(R) würde
Zeilen doppelt zählen.

## 4. Ausschluss beim unveränderten Kragen aus PR 266

Fixiere weiterhin

    (T0,T1,T2,T3)=(-5/2,-2,-4/3,0).

Für das bisherige freie Element f gilt C_f(t)=0 und seine isolierte
Uhrreaktion ist null für jedes t>0 und 0<w<1.

### Ein zusätzliches positives Element

Mit genau einem angehängten g, u>t und v>0, folgt aus der vollständigen
Wirkung zwingend

    q_f^C = v(u-t)/2 > 0.                                  (6)

Damit ist eine gemeinsame innere Stationarität unmöglich, unabhängig davon,
ob die Normierung am neuen Element lösbar wäre. Ein angehängtes Nullatom
v=0 trägt hingegen keine zusätzliche Materiezeile bei. Das ist kein aktiver
Materieanschluss. Null-Dichte-Elemente innerhalb von Intervallen können die
Gewichte anderer Zeilen weiterhin verändern; diese spezielle Zukunftsanhängung
beweist keine allgemeine Wirkungslosigkeit von Vakuumelementen.

### Zwei zusätzliche positive Elemente

Auf der Siebenerkette seien die drei freien Uhren t<u<z und die positiven
Dichten w,v,r. Aus den Uhrgleichungen am letzten und vorletzten Element folgt

    q_z = r(u-9t+32/3)/2 = 0,
    q_u = [v(t-16/3)+r(z-u)]/2 = 0.

Damit sind u=9t-32/3 und wegen der Ordnung sowie positiver Dichten notwendig

    4/3 < t < 16/3.                                       (7)

Die Normierung am mittleren freien Element ist aber

    C_g = t²/2-tu+16u/3-7/9
        = H(t) := -17t²/2+176t/3-173/3.

H ist konkav und besitzt die positiven Randwerte

    H(4/3)=49/9,   H(16/3)=121/9.

Auf dem ganzen Intervall (7) liegt H über seiner positiven Verbindungsgeraden.
Somit ist C_g>0 und kann nicht null sein. Auch diese Erweiterung scheitert.
Der Beweis betrifft exakt den eingefrorenen Kragen, freie innere Uhr-/Dichte-
variationen, die feste Kette und positive zusätzliche Dichten. Längere
Zukunft, andere Ordnungen, andere Kragen, fixierte statt variierte Felder und
zusätzliche physikalisch begründete Kopplungen sind damit nicht ausgeschlossen.

## 5. Positivkontrolle: gemeinsame Lösung mit veränderten Randdaten

Dass der Ausschluss kein allgemeines Verbot des Materiekandidaten ist,
zeigt ein anderer **äußerlich vorgegebener** Kragen. Setze

    R = sqrt(305),
    k = (70-4R)/3 = 20/[3(70+4R)] > 0,
    (T0,T1,T2,T3)=(-R/6,-5/2,-2,-4/3).                      (8)

Für das erste freie Element mit Uhr t und das zweite mit Uhr u gilt nun

    C_f(t)=k t,
    C_g(t,u)=-ut+t²/2.

Die gemeinsame Materiewirkung reduziert sich exakt auf

    S_d(t,u,w,v) = t(vu-wk)/2 - v t²/4.                    (9)

Diese Normalform gilt auch abseits stationärer Punkte. Es folgt für alle
0<w,v<1 die gemeinsame innere Lösung

    t=0,   u=k w/v>0.                                     (10)

Beide Dichteableitungen und beide Uhrableitungen verschwinden. Die äußeren
Uhren sind streng geordnet, denn R/6>5/2. Jede gemeinsame konstante
Uhrverschiebung erzeugt denselben relativen Lösungsfall.

Für w=v=1/2 ist u=k, eingeschlossen durch die rationalen Grenzen in
`results/retuned_stationary_family.json` (ungefähr 0,0476677 in den
reduzierten Uhreinheiten). Der Wert ist keine gemessene Eigenzeit.
Die Kontrollen rechnen vollständig im Zahlkörper Q(sqrt(305)); es wird
kein Gleitkommarest als exakte Null akzeptiert.

Am geteilten Element f sind die getrennten Reaktionen

    q_f^links = -wk/2,
    q_f^Zukunft = vu/2 = wk/2,
    q_f^gesamt = 0.                                       (11)

Die linke Teilwirkung ist hier also gerade nicht isoliert stationär.
Erst die gemeinsame Kopplung schließt ihre innere Uhrgleichung. Dies ist der
konkrete Impulsabgleich, der in PR 268 noch nicht an einem zweiten Block
realisiert war. Er benötigt keine zusätzlich angepasste Randphase, wohl
aber die ausdrücklich konstruierten äußeren Kragendaten (8).

Die Kontrollgeometrie ist eine zeitlich geordnete Kette mit einem weiteren
positiven Materieelement. Sie repräsentiert keinen raumzeitlichen Vakuum-
Außenraum und entscheidet keine Einstein-/Israel-/GHY-Anschlussbedingung.

## 6. Verbleibende Randreaktion und Nicht-Eindeutigkeit

Die alten äußeren Uhren werden in (8) festgehalten. Ihre Reaktionen bleiben
nicht null. Aus der geerbten Homogenitätsidentität und C_f=C_g=0 folgt

    sum_{aussen} q_y = 0,
    sum_{aussen} T_y q_y = w+v > 0.                        (12)

Die neue innere Stationarität schließt deshalb nicht die äußere
Präparationsaufgabe. Die Werte (8) wurden analytisch so konstruiert, dass ein
Positivkontrollfall existiert; sie sind keine unabhängige physikalische Vorhersage.
Schon eine beliebige kleine Verschiebung von T0 allein verletzt im Allgemeinen
C_f=0. Eine Robustheit auf einer offenen Menge unabhängiger Randdaten wird
nicht behauptet.

In der Variablenfolge (t,u,w,v) hat die Hesse-Matrix von (9) an (10) die Form

    1/2 * [[-v, v, -k, u],
           [ v, 0,  0, 0],
           [-k, 0,  0, 0],
           [ u, 0,  0, 0]].                               (13)

Ihr Rang ist zwei. Die zwei freien Dichteparameter bleiben eine stationäre
Familie. Der nichttriviale (t,u)-Hauptminor ist -v²/4<0: Es handelt sich um
einen Sattel mit flachen Richtungen, nicht um ein stabiles Minimum oder eine
ausgewählte normierte Quantenzustandspräparation. Der endliche Pfadintegralkern
muss weiterhin das deklarierte Maß, Integrationsränder und alle Strata enthalten.

## 7. Prüfung, Herkunft und nächster Schritt

Die endlichen Kontrollen umfassen:

* 50 natürlich beschriftete partielle Ordnungen bis N=4 und alle 3350
  nichtleeren Zweimengen-Überdeckungen;
* 6700 rationale Materie-Wirkungsvergleiche, 3350 gravitative
  Inklusions-Exklusions-Identitäten und 26388 Reaktionskomponenten;
* 95 Kettenüberlappungen sowie ein Gegenbeispiel mit Breite fünf;
* 81 Fälle des eingefrorenen Kragens mit einem Zukunftselement und den
  analytischen Positivitätsbeweis für zwei Zukunftselemente;
* 27 exakte neue stationäre Fälle im Zahlkörper Q(sqrt(305)), 108 unabhängige
  Wirkungsableitungen und 432 Hesse-Komponenten;
* acht konkrete Negativkontrollen. 1422 Überdeckungen haben nichtverschwindende
  Korrekturkoeffizienten, 308 enthalten interne Intervallumklassifizierungen.

Vier Ergebnisdateien werden isoliert bytegleich reproduziert. Die Kontrollen
von Ketten bis zehn Elementen sind kleine algebraische Buchhaltungstests;
sie sind keine hochdimensionale n=5-Produktionsintegration. Die Ergebnisse
stehen nicht für eine externe Replikation oder Beweisassistentenprüfung.
Der lokale Plan wurde nach analytischem Entwurf vor den endlichen Kontrollen
gehasht; keine externe Präregistrierung.

Nächster wissenschaftlicher Schritt ist die Klassifikation und
Störungsprüfung der gemeinsam zulässigen Kragendaten: Welche Bedingungen
muss die Vorgeschichte erfüllen, damit der gefundene positive gekoppelte
Zweig existiert, und welche äußeren Reaktionen bleiben dabei zu tragen?
Dabei dürfen Randwerte nicht nachträglich an ein gewünschtes Ergebnis
angepasst werden. Anschließend ist ein außerhalb der Zeitkettenklasse
qualifizierter Rand-/Außenblock zu untersuchen. Ein großer Rechenlauf ersetzt
diese Auswahl- und Robustheitsfragen nicht.

## Primärquellen und Abgrenzung

* Projektstand PR 268: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/268.
  Vier unveränderte Projektquellen und Lizenz sind in `provenance.json` gebunden.
  Insbesondere die allgemeine disjunkte Verklebung und die Variationsströme
  stammen bereits aus der früheren gemeinsamen Variationsarbeit.
* Dittrich und Höhn, Constraint analysis for variational discrete systems,
  J. Math. Phys. 54, 093505 (2013), https://arxiv.org/abs/1303.4294.
  Kontext für aktionsbasierte diskrete Impulsabgleiche; keine Übertragung einer
  dort entwickelten Gravitationsdynamik auf dieses CST-Testmodell.
* Benincasa und Dowker, The Scalar Curvature of a Causal Set,
  Phys. Rev. Lett. 104, 181301 (2010), https://arxiv.org/abs/1001.2725.
  Hintergrund der kausalen Operatorgewichte, nicht Quelle der hier
  zusätzlich konstruierten Staubpräparation oder des neuen Kragenzeugen.

Die algebraischen Resultate für den konkreten endlichen Kandidaten werden
oben eigenständig bewiesen. Die Literatur begründet keine physikalische
Validierung der projektinternen Maß- und Randwahl.
