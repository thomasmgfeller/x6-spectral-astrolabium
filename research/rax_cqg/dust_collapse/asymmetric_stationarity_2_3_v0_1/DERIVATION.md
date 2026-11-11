# CST-DUST: Vollständige Asymmetrieprüfung (2,3) v0.1

8. November 2026. Quelle: PR 272, Main
`c544521e4db792b9d01b083378a2cba5879a8a59`.

## 0. Ergebnis und genaue Klasse

Die Endpunkt-Uhrgleichung allein lässt die Astlängen (2,3) zu. Das
vollständige innere Variationsproblem dagegen besitzt **keine stationäre
Lösung in der folgenden Klasse**:

- Vier feste äußere Vorgänger a<b<c<d bilden eine Kette. Ihre vier
  Dichtezeilen sind null und werden nicht variiert.
- Zwei Ketten d≺e≺f≺j und d≺g≺h≺i≺j besitzen keine Kreuzrelationen.
  Alle transitiven Relationen werden mitgezählt: zehn Ereignisse insgesamt.
- Alle sechs inneren Uhren und alle sechs Dichten werden frei variiert.
  Jede innere Dichte liegt strikt zwischen null und eins.
- Die Uhren steigen entlang kausaler Relationen strikt. Zwischen
  unvergleichbaren Ereignissen wird keine Uhrreihenfolge vorausgesetzt.
- j hat keine Nachfolger; seine Uhr U und Dichte r sind frei.
- Die ursprüngliche Wirkung und ihre Normierung bleiben unverändert.

Der Beweis behandelt den regulären und den besonderen Kragenfall getrennt.
Er liefert unter einer notwendigen Teilmenge der Stationaritätsgleichungen
die konservative, nicht als scharf beanspruchte Schranke

    C_j > 1 + (87/32)(h-g)^2 > 1.                      (1)

Die freie Dichtevariation verlangt aber C_j=0. Damit ist das gesamte
Zwölfgleichungssystem ausgeschlossen; es ist nicht erforderlich, jede
überzählige Gleichung einzeln zu lösen. Dasselbe gilt durch vollständigen
Asttausch für (3,2).

Dies ist ein Satz über dieses feste endliche Variationsmodell. Es ist kein
allgemeines Asymmetrieverbot, kein Ausschluss der CST, keine physikalische
Randpräparation und kein Bounce-Nachweis. Alle acht physikalischen Gates
bleiben HOLD. Keine kostenpflichtige Rechnung, kein n=5-Produktionslauf.

## 1. Wirkung und globale Intervalle

Mit k(y,x) als Anzahl strikt innerer Intervallereignisse gilt

    B_yx=b(k(y,x)),  b=(1,-9,16,-8,0,...),
    C_x=1+(1/2) sum_(y≺x) B_yx(T_x-T_y)^2,
    S_d=-(1/2) sum_(x=e,f,g,h,i,j) w_x C_x.            (2)

Die gravitative Wirkung wird bei fester Ordnung nur als konstanter Anteil
mitgeführt. Es wird keine Variation der Geometrie ausgeführt. Die hier
verwendeten Uhr- und Normgrößen besitzen die unveränderten dimensionslosen
Einheiten der geerbten Referenzwirkung.

Die aktiven Vorgängergewichte jeder inneren Zeile sind:

| Zeile | Vorgänger mit nichtverschwindendem B, jeweils älter zu jünger |
|---|---|
| e, g | a:-8, b:16, c:-9, d:1 |
| f | b:-8, c:16, d:-9, e:1 |
| h | b:-8, c:16, d:-9, g:1 |
| i | c:-8, d:16, g:-9, h:1 |
| j | e:-9, f:1, g:16, h:-9, i:1 |

Am Endpunkt haben a,b,c,d die Intervallgrößen 8,7,6,5 und damit
Gewicht null. Die Summe der fünf aktiven Endpunktgewichte ist null.
Die Uhrenvergleichbarkeit erzeugt keine zusätzlichen Relationen.

## 2. Alle sechs Normgleichungen

Im Folgenden stehen a,...,i auch für die jeweiligen Uhrwerte. Definiere

    P=-8a+16b-9c+d,
    A=1+(-8a²+16b²-9c²+d²)/2,
    P_e=-8b+16c-9d+e,   P_g=-8b+16c-9d+g,
    A_e=1+(-8b²+16c²-9d²+e²)/2,
    A_g=1+(-8b²+16c²-9d²+g²)/2,
    Q=-8c+16d-9g+h,
    B=1+(-8c²+16d²-9g²+h²)/2,
    L=9e-f-16g+9h-i,
    M=-9e²+f²+16g²-9h²+i².

Weil die inneren Dichten frei im offenen Bereich (0,1) variiert werden,
gilt ∂S_d/∂w_x=-C_x/2=0. Das vollständige Normsystem lautet

    C_e=A-Pe=0,              C_f=A_e-P_e f=0,
    C_g=A-Pg=0,              C_h=A_g-P_g h=0,
    C_i=B-Qi=0,              C_j=1+UL+M/2=0.            (3)

Hier sind `Pe` und `Pg` ohne Unterstrich Produkte P·e und P·g;
P_e und P_g mit Unterstrich sind die zuvor definierten Koeffizienten.

## 3. Alle sechs Uhrgleichungen

Mit r=w_j und q_x=∂S_d/∂T_x gilt vollständig

    2q_e = w_e P + w_f(f-e) - 9r(U-e),
    2q_f = w_f P_e + r(U-f),
    2q_g = w_g P + w_h(h-g) - 9w_i(i-g) + 16r(U-g),
    2q_h = w_h P_g + w_i(i-h) - 9r(U-h),
    2q_i = w_i Q + r(U-i),
    2q_j = -rL.                                        (4)

Alle sechs rechten Seiten müssen null sein. Die späteren Materiezeilen
tragen zu den früheren Uhrableitungen bei; sie dürfen nicht durch eine
rein zeilenweise Ableitung ausgelassen werden. Die äußeren Uhrreaktionen
werden nicht auf null gesetzt, da die äußeren Uhren festgehalten werden.

## 4. Gemeinsame Endpunktreduktion

Setze die positiven inneren Astlücken

    t=f-e>0,  v=h-g>0,  w=i-h>0,
    s=g-e (ohne a priori festgelegtes Vorzeichen).

Wegen r>0 folgt aus q_j=0 die Gleichung

    L=-8s+8v-t-w=0,
    s=v-(t+w)/8.                                      (5)

Setzt man (5) in die Endpunktnorm ein, fällt U heraus und man erhält

    C_j=1+(9t²+7w²)/16+2vw-8v².                       (6)

Diese Identität gilt unabhängig von den Dichten und den Kragenwerten,
aber nur auf L=0. Die nützliche Quadratsummenidentität lautet

    9t²+7w²-(7/2)(t+w)²
      =(7/2)(t-w)²+2t² >= 0.                          (7)

Insbesondere folgt aus t+w>7v bereits

    C_j >= 1+(7/32)(t+w)²+2vw-8v²
        > 1+(87/32)v².                                (8)

Die positive Lücke w>0 wird dabei erhalten. Diese Schranke ist bewusst
konservativ. Ein scharfer minimaler Normrest wird nicht behauptet.

## 5. Regulärer Kragen: P ungleich null

Die beiden ersten Normgleichungen ergeben

    C_e-C_g=P(g-e)=0.

Ist P ungleich null, so ist e=g, also s=0. Zusammen mit (5) folgt
t+w=8v>7v, womit (8) bereits den Widerspruch liefert.
Direktes Einsetzen liefert sogar die stärkere Identität

    C_j=1+(w-7v/2)²+(63/4)v² > 1.                    (9)

Dieser Fall setzt keine Gleichheit der beiden Ereignisse und keine neue
Kausalrelation voraus. Es handelt sich nur um gleiche Skalaruhrwerte an
zwei unvergleichbaren Ereignissen.

## 6. Besonderer Kragen: P gleich null

Bei P=0 verlangen C_e=C_g=0 zusätzlich A=0. Dieser Zweig darf nicht
durch Division durch P verloren gehen. Der folgende Ausschluss benötigt
A=0 sogar nicht: Er gilt bereits für eine schwächere notwendige Teilmenge.

Schreibe

    K=8b-16c+9d,   gamma=K-e,   u=U-f>0.

Dann ist P_e=e-K=-gamma. Aus q_f=0 und positiven w_f,r,u folgt gamma>0.
Aus q_e=q_f=0 folgt bei P=0

    w_f t=9r(u+t),    w_f gamma=ru,
    u(t-9gamma)=9gamma t,
    t>9gamma.                                        (10)

Für s<=0 folgt aus (5) sofort t+w>=8v>7v. Es bleibt s>0.

Definiere R=1+(-8b²+16c²-9d²)/2 und D=R+K²/2. Dann gilt

    C_f=D-gamma²/2+t gamma,
    C_h=D-(gamma-s)²/2+v(gamma-s).

Aus der notwendigen Gleichheit C_f=C_h folgt die Differenzgleichung

    gamma(v+s-t)=s(v+s/2).                            (11)

Da gamma,s,v positiv sind, ist v+s-t>0. Daher

    gamma = s (v+s/2)/(v+s-t).

Der Quotient ist größer als 1/2, denn

    2(v+s/2)-(v+s-t)=v+t>0.

Somit gamma>s/2. Mit (10) folgt t>9s/2>s/2. Der Quotient ist deshalb
sogar größer als eins, denn

    (v+s/2)-(v+s-t)=t-s/2>0.

Also gamma>s und t>9s. Zusammen mit t<v+s folgt v>8s. Gleichung (5)
liefert jetzt die benötigte strikte Trennung

    t+w=8(v-s)>7v.                                   (12)

Damit gilt (8) auch im besonderen Kragenfall. Beide P-Fälle führen zu
C_j>1, im Widerspruch zur freien Endpunkt-Dichtevariation C_j=0.
Die Klasse (2,3) besitzt also keine vollständige innere stationäre Lösung.

## 7. Stärke und Grenze der Aussage

Der Beweis verwendet nur die beiden Normdifferenzen C_e=C_g und C_f=C_h
sowie q_e=q_f=q_j=0 und die strikte Domäne. Die einzelnen Normen müssen
für diese Teilprüfung noch nicht null sein. Schon diese schwächeren
notwendigen Bedingungen erzwingen (1).
Die übrigen drei Uhrgleichungen und C_i=0 wurden vollständig hergeleitet
und überprüft; sie können den Widerspruch einer notwendigen Teilmenge
nicht aufheben. Die freie Endpunkt-Dichteableitung erfüllt unter diesen
Teilbedingungen sogar ∂S_d/∂r<-1/2 in der geerbten Normierung.

Die Schranke ist **kein zertifiziertes Toleranzbudget für nur ungefähr
erfüllte Teilgleichungen**. Eine solche Aussage würde zusätzliche Fehler-
und Domänenbudgets verlangen. Der Satz behandelt exakte Stationarität.

Bei festgehaltenem U wird q_j=0 nicht verlangt; bei zusätzlichen Nachfolgern
kommen weitere Uhrbeiträge hinzu. Null-Dichte-Zweige oder festgehaltene
Dichten ändern ebenfalls die Variationsdomäne. Bei r=0 verschwindet zwar
der Term -rL/2, die freie Dichteableitung bleibt jedoch -C_j/2; ob diese
Variation am Rand zugelassen wird, muss gesondert festgelegt werden.
Keiner dieser anderen Fälle ist hier gelöst oder als Reparatur bewiesen.

## 8. Aktualisierter endlicher Forschungsstand

Aus PR 272 und dem neuen Satz ergibt sich für die 16 geordneten
Astlängenfelder folgende Einordnung:

| p / q | 1 | 2 | 3 | >=4 |
|---|---|---|---|---|
| 1 | stationäre Familie bekannt | ausgeschlossen | ausgeschlossen | offen |
| 2 | ausgeschlossen | ausgeschlossen | neu ausgeschlossen | offen |
| 3 | ausgeschlossen | neu ausgeschlossen | ausgeschlossen | offen |
| >=4 | offen | offen | offen | offen |

Acht Felder sind nun ausgeschlossen. Für (1,1) existiert die in PR 271
klassifizierte Familie bei passenden Randdaten. Sieben Felder bleiben
für vollständige Stationarität offen. Die Zeile/Spalte >=4 fasst unendlich
viele endliche Längen zusammen; aus der Endpunkt-Uhrmachbarkeit folgt
keine vollständige Lösung irgendeiner konkreten Länge.

Als nächste kleinste noch offene konkrete Ordnung wird (1,4) vorgeschlagen.
Vor einem freiwilligen Community-Rechenlauf sollten wieder sämtliche
Norm- und Uhrgleichungen analytisch geprüft werden. Dieser Bericht führt
keinen neuen Produktionslauf oder Community-Aufruf aus.

## 9. Exakte Kontrollen und Reproduktion

`analyze.py` nutzt ausschließlich die Python-Standardbibliothek und
`fractions.Fraction`. Es prüft 26 vollständige Polynomidentitäten,
einschließlich aller zwölf Variationsgleichungen und der Ausschlussidentitäten.
Für 1.458 streng geordnete Profile werden jeweils sechs Uhr- und sechs
Dichteableitungen unabhängig als exakte zentrale Wirkungsdifferenzen
gerechnet: jeweils 8.748 Komponenten. Bei der quadratischen Uhr- und
linearen Dichteabhängigkeit entsteht dabei kein Diskretisierungsfehler.

Neun streng geordnete rationale Zeugen erfüllen P=0, q_e=q_f=q_j=0 und
C_f=C_h exakt. Sie erfüllen damit die schwächere notwendige Teilmenge des Beweises
und zeigen, dass diese nicht leer ist. Ihre einzelnen Normen sind nicht null; sie werden ausdrücklich
nicht als vollständige Lösungen ausgegeben. Weitere 27 Kontrollen prüfen
die Gleichuhridentität (9). Sechs Negativkontrollen prüfen Fehlinterpretationen.
Ein vollständiger Asttausch erhält Wirkung, alle Normen und Uhrableitungen
(zehn Komponenten) und trägt die Übertragung auf (3,2).

Die allgemeinen Ausschlüsse folgen aus den analytischen Beweisen, nicht
aus den endlichen Stichproben. Der Plan wurde nach dem ersten analytischen
Fallentwurf vor den endlichen Kontrollen gehasht. Das ist keine externe
Präregistrierung oder unabhängige Replikation.

    python3 -O -B verify_package.py
    python3 -O -B replay.py

Vier Ergebnisdateien werden in einem separaten Ausgabeverzeichnis bytegleich
neu erzeugt. Das Manifest bindet alle Paketdateien; die vier geerbten Dateien
werden zusätzlich gegen ihre unveränderten Git-Blob-Identitäten geprüft.

## 10. Quellen und physikalischer Status

- [PR 272: Asymmetrie und Endpunktkriterium](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/272).
  Geerbte Definitionen, Endpunkt-Uhrzeugen und Quellen sind im Paket enthalten.
- [PR 271: Verzweigung und Wiederanschluss](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/271).
  Referenz für den vollständig stationären symmetrischen Diamanten.

Neue Beweise und Kontrollen dieses Pakets sind projektspezifische eigene
Rechnungen innerhalb der angegebenen Wirkung. Sie begründen keine
physikalische Auswahl dieser Wirkung oder der Randzustände.

MODEL, BOUNDARY, CURRENT, CORRESPONDENCE, EXTENSION, TRAPPING,
REGULARITY und BOUNCE: jeweils **HOLD**.
