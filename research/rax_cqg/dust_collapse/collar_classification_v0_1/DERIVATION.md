# CST-DUST: Zulässige Randdaten und Störungsgrenzen v0.1

8. November 2026 (Zürich). Ausgangspunkt: PR 269, Main
`adb6ea2de0dc56417da3493e8aabf8903981090f`.

## 0. Ergebnis und klar abgegrenzte Klasse

Die in PR 269 konstruierte Zweiblock-Lösung wird vollständig innerhalb
derselben **Sechserkette** klassifiziert. Vier äußere Uhren a<b<c<d sind fest.
Die beiden inneren Uhren t,u und ihre Gewichte w,v werden frei variiert;
gesucht wird d<t<u und 0<w,v<1. Die vier äußeren Dichtezeilen sind hier null.
Andere feste Vergangenheitswirkungen ändern die inneren Gleichungen nicht,
können aber zusätzliche äußere Reaktionen beitragen; die unten angegebenen
Randreaktionen gelten für den ausdrücklich genannten Nullzeilen-Kragen.

Es gibt genau zwei unabhängige Gleichheitsbedingungen an die vier äußeren
Uhren sowie zwei strikte Ungleichungen. Sie sind notwendig und hinreichend.
Die zulässigen Kragendaten bilden eine glatte zweidimensionale Fläche in
der vierdimensionalen Menge geordneter Randuhren. Alle zulässigen Kragen
werden unten durch einen Formparameter und eine gemeinsame Verschiebung
parametrisiert. Auf dieser Fläche bleiben zwei positive Dichteparameter frei.

Die Lösung ist gegenüber beliebigen unabhängigen Randstörungen **nicht offen
robust**: Außerhalb der Fläche kann keine Neuwahl der inneren Uhren oder
positiven Dichten die exakten stationären Gleichungen erfüllen. Entlang der
Fläche existiert dagegen eine glatte Fortsetzung. Das ist eine lokale
Kompatibilitäts- und Sensitivitätsaussage, kein Satz über zeitliche Stabilität
einer physikalischen Kollapsentwicklung.

Alle acht physikalischen Gates bleiben HOLD. Keine physikalisch ausgewählte
Randpräparation, kein Vakuum-Außenraum, keine Geometrievariation, kein Bounce.
Die Resultate betreffen den geerbten endlichen Wirkungsansatz in seinen
reduzierten Einheiten. Kein n=5-Produktionslauf, keine kostenpflichtige Rechnung.

## 1. Reduktion der ursprünglichen Gleichungen

Die unveränderten Gewichte lauten B(k)=(1,-9,16,-8,0,...). Für die beiden
positiven Zeilen der Sechserkette ist

    S_d = -(w C_f + v C_g)/2,
    C_f = 1 + [-8(t-a)^2+16(t-b)^2-9(t-c)^2+(t-d)^2]/2,
    C_g = 1 + [-8(u-b)^2+16(u-c)^2-9(u-d)^2+(u-t)^2]/2.    (1)

Die Geometrie ist fest. Die geerbte gravitative Wirkung besitzt deshalb
keine Ableitung nach diesen Uhren oder Materiedichten. Definiere

    P = -8a+16b-9c+d,
    A = 1+(-8a^2+16b^2-9c^2+d^2)/2,
    t_* = 8b-16c+9d,
    D = 1+(-8b^2+16c^2-9d^2)/2,
    E = D+t_*^2/2,
    F = A-P t_*.                                         (2)

Dann gelten als Polynomidentitäten, auch abseits jeder Lösung,

    C_f = A-Pt,
    C_g = D+t^2/2-(t-t_*)u,
    q_t = partial_t S_d = [wP+v(u-t)]/2,
    q_u = partial_u S_d = v(t-t_*)/2.                     (3)

Da w,v im offenen positiven Intervall frei variiert werden, verlangen ihre
Gleichungen C_f=C_g=0. Die Uhrgleichung q_u=0 erzwingt wegen v>0 exakt t=t_*.
An diesem Wert sind die beiden Normierungen F und E, unabhängig von u,w,v.
Schließlich erzwingt q_t=0

    u = t_* - (w/v)P.                                    (4)

**Klassifikationssatz.** Für gegebene a<b<c<d existiert eine streng geordnete
gemeinsame innere stationäre Lösung mit 0<w,v<1 genau dann, wenn

    E=0,   F=0,   t_*>d,   P<0.                          (5)

Beweis der Notwendigkeit: die vier Variationsgleichungen ergeben (3)-(4);
die strikte Ordnung liefert die letzten beiden Ungleichungen. Beweis der
Hinlänglichkeit: Wähle beliebige w,v in (0,1), setze t=t_* und u nach (4).
Dann verschwinden C_f,C_g,q_t,q_u, und d<t<u gilt. Das beweist zugleich die
Vollständigkeit innerhalb der erklärten Klasse. Der Fall v=0, eingeschränkte
Variationen, weitere Elemente und andere Kausalordnungen gehören nicht zu (5).

Mit eta=t-t_* und xi=u-t_* lautet die gesamte Normalform

    S_d = -(wF+vE)/2 + eta(wP+v xi)/2 - v eta^2/4.         (6)

Die frühere Normalform ist der Spezialfall E=F=0 und P=-k. Ein fester
Zukunftsabstand wäre eine zusätzliche Randbedingung; er wurde nicht benutzt.

## 2. Alle streng geordneten Kragen explizit parametrisiert

Verwende die vergangenheitsseitigen Abstände

    x=c-b>0,   y=d-c>0,   z=b-a>0,   s=y-x.

Es folgen

    t_*=d+8s,              P=8z-7x+s,
    E=1-8x^2+36s^2.                                    (7)

Die Bedingung t_*>d verlangt s>0. E=0 bedeutet 8x^2-36s^2=1.
Setze h=2x+9s=t_*-b und

    Z = sqrt[(71x^2+414xs+559s^2)/8].

Unter E=0 ist F=0 äquivalent zu (h+z)^2=Z^2. Da h,z>0 sein müssen,
ist ausschließlich

    z=Z-2x-9s                                           (8)

zulässig. Dieser Wert ist tatsächlich positiv: Es gilt

    Z^2-h^2=(39x^2+126xs-89s^2)/8 > 0,

denn x^2>9s^2/2, x,s>0. Der negative Quadratwurzelzweig liefert keine
chronologisch geordneten äußeren Uhren.

Nun ist P=8Z-23x-71s. Beide Seiten des Vergleichs 8Z<23x+71s sind positiv,
weshalb Quadrieren das Vorzeichen nicht verfälscht:

    P<0  <=>  39x^2+46xs-569s^2<0.                     (9)

Für r=s/x ergibt sich die vollständige globale Parametrisierung

    r_0 = (23+8 sqrt(355))/569,
    r_0 < r < sqrt(2)/3,
    x = 1/sqrt(8-36r^2),   s=r x,
    z = x {sqrt[(71+414r+559r^2)/8]-2-9r},
    d = lambda,
    c = lambda-x-s,
    b = lambda-2x-s,
    a = b-z.                                            (10)

Hier sind lambda beliebig reell und r genau im angegebenen offenen
Intervall. Die obere Grenze folgt aus E=0; die untere ist die positive
Nullstelle von 569r^2-46r-39. Die negative Nullstelle ist für s>0 irrelevant.
Der Kragen aus PR 269 besitzt r=1/3, x=1/2, s=1/6 und lambda=-4/3.
Mit diesen Werten liefert (8) z=(sqrt(305)-15)/6 und damit a=-sqrt(305)/6.

Am unteren Formrand P=0 kollidieren die beiden inneren Uhren u=t und die
strikte Ordnung endet. Gegen die obere Formgrenze divergiert x in diesen
festen Modelleinheiten. Daraus folgt weder eine physikalische Singularität
noch ein universeller minimaler Eigenzeitabstand.

Die Kontrollen verwenden rational parametrisierte Punkte derselben Hyperbel:

    delta=(3m-2)/(2-9m^2),
    x=1/2+delta,  s=1/6+m delta.                         (11)

Sieben vorher deklarierte rationale m-Werte liefern vier zulässige und
drei wegen P>=0 unzulässige Formen. Die Radikale werden in jeweils exakten
quadratischen Zahlkörpern ausgewertet. Die Kontrollwerte sind konstruierte
algebraische Zeugen, keine unabhängig vorhergesagten Präparationen.

## 3. Zwei unabhängige Bedingungen und die äußeren Reaktionen

Die Gradienten nach (a,b,c,d) sind

    grad E = (0, 16x+72s, -16x-144s, 72s),
    grad F = (8(t_*-a),
              16(b-t_*)-8P,
              -9(c-t_*)+16P,
              d-t_*-9P).                               (12)

Im zulässigen Bereich gilt partial_a F=8(t_*-a)>0 und
partial_b E=16x+72s>0, aber partial_a E=0. Der betreffende 2x2-Minor ist
ungleich null. Der Jacobi-Rang von (E,F) ist daher überall zwei. Zusammen
mit den strikten offenen Ungleichungen beweist der Satz über reguläre
Niveaumengen die glatte zweidimensionale Kragenfläche. Insbesondere enthält
sie keine offene vierdimensionale Umgebung eines zulässigen Kragens.

Setzt man die inneren Uhren (4) ein, ist S_d=-(wF+vE)/2. Die Uhrableitungen
q_t,q_u verschwinden dort auch für Randdaten außerhalb E=F=0. Deshalb folgt
für die äußeren Reaktionen an jeder zulässigen Lösung

    q_outer = -(w grad F + v grad E)/2.                  (13)

Die Reaktion liegt im Konormalraum der Kragenfläche: Sie verschwindet auf
jedem Tangentialvektor mit delta E=delta F=0. Die beiden unabhängigen
Normalrichtungen tragen die Gewichte w und v. Bei 0<w,v<1 ist dieser
Faserbereich beschränkt; er wird nicht als vollständiger unbeschränkter
Konormalkegel ausgegeben. Die gemeinsame Randrelation besitzt Dimension
2+2=4, aber ist dadurch noch kein physikalisch ausgewählter Zustandsraum.

Am ältesten Kragenelement gilt sogar die strikte Aussage

    q_a = -4w(t_*-a)<0.                                (14)

Die äußeren Reaktionen können also nicht sämtlich verschwinden. Die
Verschiebungsinvarianz und die quadratische Homogenität von E-1,F-1 ergeben

    sum_outer q_i=0,
    sum_outer T_i q_i=w+v>0.                            (15)

Eine gemeinsame Uhrverschiebung ist hier eine Symmetrie des deklarierten
Ansatzes. Daraus wird weder ihre physikalische Eichinterpretation noch eine
Hamiltonsche Constraintalgebra abgeleitet. Zusätzliche Vergangenheitszeilen
oder ein anderes Außenraummodell müssen ihre eigenen Reaktionen mitführen.

## 4. Unabhängige Randstörungen können nicht innerlich repariert werden

Für jeden gestörten Kragen erzwingt q_u=0 weiterhin den **neu berechneten**
Wert t=t_*. E und F sind dann die verbleibenden Normierungsreste. Diese
Prüfung hält die inneren Werte nicht künstlich auf ihrem alten Stand fest.
Sie schließt auch jede nachträgliche Neuwahl positiver w,v und u ein.

Verschiebe zuerst nur a um epsilon. t_* und E bleiben gleich, während

    delta F = 8(t_*-a)epsilon -4epsilon^2.               (16)

Für alle hinreichend kleinen epsilon!=0 ist das ungleich null, bei weiterhin
strenger äußerer Ordnung. Deshalb gibt es keinen inneren Ausgleich.

Am PR-269-Zeugen a=-sqrt(305)/6, b=-5/2, c=-2, d=-4/3, t_*=0 ergeben
die vier einzeln veränderten Uhren die folgenden exakten Hindernisse:

| Allein verschobene Uhr | Nichtverschwindendes Hindernis |
|---|---|
| a | F=(4 sqrt(305)/3)epsilon-4epsilon^2; E=0 |
| b | E=20epsilon+28epsilon^2 |
| c | E=-32epsilon+136epsilon^2 |
| d | E=12epsilon+36epsilon^2 |

Alle Werte epsilon=±10^-3, ±10^-4, ±10^-5 bewahren die strikten
Ordnungs-/Vorzeichenbedingungen t_*>d und P<0, verletzen aber mindestens
eine Gleichheit. Alle 24 Fälle scheitern damit an den vollständigen
inneren Gleichungen, nicht lediglich an der alten Lösung.

Eine gleichzeitige konstante Verschiebung aller vier Randuhren und beider
inneren Uhren erhält hingegen P,E,F und sämtliche Abstände. Allgemeine
korrelierte Änderungen gemäß (10) bleiben ebenfalls zulässig. Der Satz
lautet daher nicht, jede Störung vernichte jede Lösung, sondern dass die
unabhängigen vier Randwerte zwei Kompatibilitätsbedingungen erfüllen müssen.

Auf der Fläche und bei festem Dichteverhältnis rho=w/v gilt exakt für
zwei zulässige Kragen

    delta t = 8 delta b -16 delta c +9 delta d,
    delta u = delta t -rho delta P.

Für max|delta(a,b,c,d)|<=epsilon folgt

    |delta t|<=33epsilon,
    |delta u|<=(33+34rho)epsilon.                        (17)

Dies ist eine konditionale endliche Sensitivitätsgrenze bei festem rho,
keine offene Robustheit außerhalb der Fläche. Ohne obere Schranke für rho
ist die zweite Konstante nicht uniform. Bei P gegen null fehlt außerdem
ein uniformer relativer Abstand der inneren Uhren.

## 5. Zertifizierbare Grenzen bei endlichen Restfehlern

Eine numerische Rechnung braucht mehr als eine Prüfung auf exakt null.
Setze für beliebige äußere Daten und beliebige innere Uhren

    eta=t-t_*,   g=u-t,
    q_u=v eta/2.

Direkt aus (1)-(3) folgen die exakten Identitäten

    F=C_f+P eta,
    E=C_g+eta g+eta^2/2.                                (18)

Unter den ausdrücklich zusätzlichen Budgetbedingungen

    v>=v_min>0,   0<g<=G

erhält man die notwendigen Grenzen

    |F| <= |C_f| + (2|P|/v_min)|q_u|,
    |E| <= |C_g| + (2G/v_min)|q_u| + 2|q_u|^2/v_min^2.    (19)

Sind akzeptable Reste epsilon_f,epsilon_g,epsilon_q festgelegt, kann ihre
Gleichzeitigkeit ausgeschlossen werden, sobald |F| oder |E| die entsprechende
rechte Seite mit diesen Toleranzen übersteigt. Bestehen dieser notwendigen
Prüfung beweist umgekehrt noch keine Lösung; etwa q_t muss ebenfalls geprüft
werden. Alle Größen und Toleranzen stehen in den deklarierten reduzierten
Einheiten; unterschiedliche Resttypen werden nicht unbemerkt gleichgesetzt.

Der Dichteboden und der obere Zukunftsabstand sind Budgetannahmen, keine
Herleitungen des Kandidaten. Die Normierungsbedingungen müssen separat
kontrolliert werden: Bei w,v gegen null können die gewichteten Uhrreste
beliebig klein werden, obwohl eine Normierung ungleich null bleibt. Die
Kontrolle enthält einen solchen konkreten Gegenfall. 432 rationale Fälle
mit v_min=1/4 und G=1 prüfen (18)-(19) ohne nachträgliche Randanpassung.

## 6. Kontrollen, Beweisgrenze und nächste Forschungsentscheidung

Das Standardbibliothek-Skript prüft 16 symbolische Polynomidentitäten durch
vollständigen rationalen Koeffizientenvergleich. Dazu kommen 21 parametrisierte
Kragen (12 zulässig, 9 chronologisch ausgeschlossen), 108 gemeinsame
stationäre Fälle, 168 unabhängige Randableitungen, 24 unabhängige
Randstörungen, 432 Restfehlerbudgets mit 1296 Identitätsprüfungen und
108 gemeinsame Verschiebungen. Sechs Negativkontrollen werden zurückgewiesen.
Die Rechnungen verwenden rationale Arithmetik und exakte quadratische
Zahlkörper. Es gibt keine Gleitkommatoleranz für als exakt ausgegebene Nullen.

Die allgemeinen Resultate folgen aus den obigen Beweisen; die endlichen
Kontrollen sind zusätzliche Fehlerprüfungen. Der lokale Plan wurde nach
analytischem Entwurf und vor dem ersten endlichen Kontrolllauf gehasht.
Keine externe Präregistrierung, keine unabhängige externe Replikation,
kein Beweisassistenten-Zertifikat. Vier Ergebnisdateien sind isoliert
reproduzierbar. Quellidentitäten und Paketdateien sind gehasht.

**Nächster sinnvoller Schritt:** Den Rand-/Zukunftsblock außerhalb dieser
reinen Zeitkettenklasse vorab festlegen. Mindestens eine Verzweigung und
die vollständigen Intervalländerungen müssen einbezogen werden. Dann ist
erneut abzuleiten, wie viele unabhängige Randbedingungen und welche
Reaktionen erforderlich sind. Erst ein begründetes Modell für die
Vorgeschichte könnte erklären, warum seine Randdaten auf der hier gefundenen
Fläche liegen. Nachträgliches Einstellen auf E=F=0 wäre keine physikalische
Vorhersage. Ein großer Produktionslauf beantwortet diese Modellfrage nicht.

## Quellen und Herkunft

* Projekt PR 269: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/269.
  Unveränderte Herleitung, Vertrag und Referenzcode sind unter `inputs/`
  übernommen und über `provenance.json` an Main gebunden.
* Dittrich und Höhn, Constraint analysis for variational discrete systems,
  J. Math. Phys. 54, 093505 (2013), https://arxiv.org/abs/1303.4294v3.
  Methodischer Kontext für Variationsgleichungen und diskrete Constraints;
  die dort untersuchten Bedingungen ersetzen weder eine Herleitung der
  hier gewählten Materiewirkung noch deren physikalische Validierung.

Die neuen Klassifikations-, Reaktions- und Störungsresultate für diesen
konkreten endlichen Kandidaten sind in diesem Dokument eigenständig bewiesen.
