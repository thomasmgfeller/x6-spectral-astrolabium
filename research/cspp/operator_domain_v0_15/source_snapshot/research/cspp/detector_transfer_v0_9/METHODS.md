# Skalarer Fluktuationstransfer zu endlichen Detektoren: v0.9

## 1. Status und feste physikalische Eingaben

Dieses Paket ist eine Entwicklungs-Machbarkeitsprüfung auf acht bereits
bekannten Archivwolken. Es zieht keine neuen Zufallszahlen und behauptet
keine unabhängige Bestätigung. Die feste Auswahl erfolgt nach Archiv-ID,
nicht nach Detektorergebnis. Die Quellen aus v0.7, der räumliche Detektorball
D=B((0,0,3/2),1/2), Omega4, nu=512, epsilon=1/16 und m=1 bleiben fest.
Wellenkontrollen haben k=0,2,4,8. Der kompakte Bump hat Radius1/2, k=4 und
g=0. Die Referenzlänge ist L0; c=1. Die Koordinaten sind exakte gespeicherte
binary64-Zahlen. Das ideale reelle Poisson-Ensemble wird dadurch nicht bewiesen.

Neu sind zwei ausdrücklich deklarierte Zeitantworten I0=[3/4,1] und
I1=[1,5/4], jeweils mit konstantem normiertem Gewicht. Sie ersetzen keinen
historischen Momentandetektor. Das Signal ist

    A_r(C) = (Vol(D)*|I_r|)^(-1) integral_(I_r x D) phi_C(t,x) dt d^3x.

Es ist eine lineare komplexe Feldamplitude, keine Wahrscheinlichkeit,
Intensität, Flavor- oder Dekohärenzdiagnose. Beide Fenster benutzen dieselbe
Wolke. Ensemblevarianz und zeitliches Messrauschen werden nicht gleichgesetzt.

## 2. Explizite Fortsetzung und endlicher Transfer

Die H1-History an den ursprünglichen Knoten t<=-1 wird unverändert aus den
Cauchy-Daten gebildet. Alle benötigten aktiven Knoten bis t<5/4 werden mit der
v0.7-Arb-Rekursion gelöst. Spätere Knoten können weder früheren Knoten noch
dem Detektor kausal vorausgehen und dürfen exakt weggelassen werden.

Für einen virtuellen Auswertungspunkt p definieren wir

    phi_C(p) = sum_(y in C, y prec p) beta*w_e(n(y,p))*phi_C(y),
    beta = a*e/(a+m^2), a=4*sqrt(e*rho/6), rho=nu/Vol(Omega4).

Der Punkt p wird nicht in C eingefügt. Die offenen Intervalle enthalten nur
ursprüngliche Wolkenpunkte. Dies ist ein koordinatenbasierter, deklarierter
Auswertungsadapter; seine Eindeutigkeit als intrinsischer physikalischer
Detektor wird nicht vorausgesetzt. Die Gleichung entspricht der bisherigen
virtuellen Punktprobe, jetzt an jedem Punkt des endlichen Detektors.

Mit History h, aktiven Knoten a und kausalen Koeffizienten K gilt exakt

    phi_a = (I-K_aa)^(-1) K_ah h,
    A_r = Q_rh h + Q_ra phi_a = T_r(C) h.

K_aa ist strikt unterdreieckig. Die Inverse ist eine endliche nilpotente
Neumann-Summe; eine Kleinheitsannahme ist hierfür nicht nötig. Q sind die
Detektorintegration der Query-Koeffizienten. Die gewichtete rückwärtige
Substitution liefert T unabhängig von der vorwärts gelösten Feldamplitude.
Beide Einschließungen müssen sich überlappen; ihr Schnitt bleibt gültig.
Ein Oberwert von sum|T_h| kontrolliert jede linf-Störung der History.

T_r(C) ist zufällig und mit der gesampelten History korreliert. Eine
Ensemble-Kovarianz darf daher nicht durch Multiplikation unabhängig gemittelter
Faktoren ersetzt werden. Eine gemeinsame Darstellung auf Funktionen bzw.
Messgrößen ist vor dem Mitteln unterschiedlich großer Wolkenoperatoren nötig.

## 3. Vollständige räumliche und zeitliche Integration mit Einschließung

Der Integrator zerlegt I_r x [-1/2,1/2]^2 x [1,2] in höchstens 256 dyadische
Boxen. Die Zellenwahl hängt nur von exakter Geometrie ab, nicht vom Feldwert
oder der Arb-Präzision. Alle Punktkoordinaten und Boxgrenzen werden auf einen
gemeinsamen ganzzahligen dyadischen Nenner gebracht. Minimale und maximale
euklidische Abstände zu einer Box sowie früheste/späteste Zeit entscheiden
mit Ganzzahlarithmetik:

- P_minus: Punkte, die jedem Punkt der Box strikt kausal vorausgehen;
- P_plus: Punkte, die mindestens einem Punkt der Box strikt vorausgehen könnten.

Die gemeinsame Vergangenheit erfüllt P_minus subset P(p) subset P_plus.
Für den fest gespeicherten Zukunftsbitvektor S_y eines Punktes y folgt

    |S_y intersection P_minus| <= n(y,p) <= |S_y intersection P_plus|.

Die nichtmonotonen, vorzeichenwechselnden Gewichte werden über ALLE ganzen
Zählwerte in diesem Bereich eingeschlossen. Ist die y-p-Relation unsicher,
wird auch null aufgenommen. Es wird weder positive Korrelation noch
Unabhängigkeit überlappender Intervalle unterstellt.

Als exakt integrierbare Kontrollfunktion dient der Koeffizient c_y am
Detektormittelpunkt:

    Q_ry = c_y + (Vol(D)*|I_r|)^(-1) integral_(I_r x D) (K_py-c_y) dp.

Der konstante Anteil verwendet das exakte Kugelvolumen pi/6. Die verbleibende
Funktion wird auf jeder Box eingeschlossen. Für Kugelrandboxen umfasst der
Wertebereich zusätzlich null, weil außerhalb D der Restintegrand null ist.
Multiplikation mit dem vollständigen Boxvolumen und Summation liefern eine
gültige Einschließung einschließlich des gesamten nicht aufgelösten Randes.
Es gibt keine unkontrollierte Restregion, keine stochastische Quadratur und
keine angenommene Glattheit der diskontinuierlichen Fortsetzung. Die
Kontrollfunktion macht einen konstanten Query-Koeffizienten bis auf Arb-Radien
exakt integrierbar, auch wenn die Kugelgrenze noch nicht aufgelöst ist.

Diese Koeffizienteneinschließungen können breit sein. Ein breites Intervall
ist keine gemessene physikalische Fluktuation. Nach Erreichen des festen
Zellenbudgets werden Auflösung oder Fenster nicht ergebnisabhängig verändert.

## 4. Getrennte Fehler und Referenzen

Der Produktionswert stammt aus Arb-Lösung und eingeschlossener Quadratur.
Zusätzlich werden exakt ausgewertete und binary64-gerundete H1-Histories
getrennt durch das Dreieckssystem propagiert. Eine separate binary64-Lösung
wird mit der Arb-Lösung derselben gerundeten History verglichen. Für jeden
Knotenfehler e_j gilt der einfache uniforme Detektor-Oberwert

    |delta A_r| <= max_n |beta*w_e(n)| * sum_j |e_j|.

Die ausgewiesene Float-Diagnose betrifft diese nodalen Fehler in der exakt
definierten Query-Fortsetzung. Sie behauptet keine unabhängig qualifizierte
Float-Kubatur. Arb-Radien und Detektorauflösung haben eigene Budgets.

Für die vier Wellen wird zusätzlich die exakte Kontinuumshistorie als Orakel
propagiert. Dadurch zerfällt der signierte Detektorfehler in H1 minus Orakel
und Orakel minus Kontinuumsreferenz. Die normierte Kontinuumsreferenz ist

    exp(i*k*3/2-i*omega*(t_mid+1))
    * 3*(sin(k/2)-(k/2)*cos(k/2))/(k/2)^3
    * sinc(omega*duration/2), omega=sqrt(k^2+1),

wobei der räumliche Faktor bei k=0 exakt eins ist. Alle Funktionen werden
eingeschlossen ausgewertet. Der massive kompakte Kontinuumsdetektor ist
weiterhin NOT_QUALIFIED. Seine punktweisen Vorgängerreferenzen ersetzen diese
fehlende Volumen-/Zeitreferenz nicht.

## 5. Statistische Aussage und spätere Fluktuationsvorhersage

Aus den acht gepaarten Signalen werden nur endliche Stichprobenmomente
eingeschlossen. Für M=8 wird die unverzerrte Stichprobenkovarianz durch

    S_rs = [M(M-1)]^(-1) sum_(i<j) (A_ir-A_jr)*conj(A_is-A_js)

berechnet. Das ist eine algebraische Identität. Die Intervalle decken die
deterministische Integrationsunsicherheit ab, nicht automatisch die
Unsicherheit über Populationsmomente. Es gibt keine Konfidenzfreigabe, keine
Student-t-Annahme und kein Abschneiden großer Ausreißer.

Für eine spätere prädiktive Theorie sind ein gemeinsamer Operator-Rauschkern
und eine stabile Antwort erforderlich. In einer definierten gemeinsamen
Darstellung ist die exakte Identität delta_phi_C=G_C*(delta_J_C-delta_L_C*phi0).
Nur unter kontrollierter Linearisierung ergibt sich C_phi approximately
G0*N_xi*G0^dagger, anschließend C_A approximately W*C_phi*W^dagger.
Korrelationen zwischen G_C und xi_C sowie der mittlere Drift dürfen nicht
unbegründet entfernt werden. Die synthetischen exakten Kontrollen prüfen
gezielt einen Kovarianz-Restterm und E(G_C) != inverse(E(L_C)).

Das v0.9-Integral ist die Integration eines diskreten Detektoradapters. Es
ist NICHT die noch offene vollständige analytische Paar-Kovarianzintegration
aus v0.4 und auch kein Ersatz für deren Zweipunkt-Erweiterung.

## 6. Abbruch- und Anschlussentscheidung

Ein Quadratur-, Präzisions- oder Ressourcen-HOLD blockiert neue
Bestätigungswolken. Selbst wenn alle Entwicklungsbudgets eingehalten werden,
ist das Ergebnis nur DETECTOR_INTEGRATION_READY_ONLY. Ein unabhängiger
Folgeversuch muss zuvor Vorhersagemodell, Fehlerbudgets, Populationsstatistik,
Stichprobenumfang/Power, Ressourcen und Abbruchregeln öffentlich festlegen.
Die alten v0.8-Holdouts zählen nicht nochmals als frische Bestätigung.

Ein Vergleich mit Festkörper-/Optomechanikmethoden ist eine methodische
Analogie. Testmassen, Astrometrie und Kosmologie benötigen zusätzliche
Geometrie- bzw. Materiekopplung. G1 bleibt HOLD, Dirac/Flavor bleiben gesperrt.

## Literatur und Abgrenzung

- Dowker, Henson, Sorkin: [Discreteness and the transmission of light from distant sources](https://arxiv.org/abs/1009.3058). Quelle–Detektor-Vorläufer mit einem anderen Propagationsmodell; keine Übernahme seiner Ergebnisse als Beleg für unseren Operator.
- Sorkin: [Does Locality Fail at Intermediate Length-Scales?](https://arxiv.org/abs/gr-qc/0703099). Diskussion lokaler Operatorfluktuationen und möglicher Mittelung.
- Hu, Roura, Verdaguer: [Induced quantum metric fluctuations and the validity of semiclassical gravity](https://arxiv.org/abs/gr-qc/0402029). Retardierte Antwort und Rauschkern in einem anderen, quantenfeldtheoretisch definierten Modell; keine Gleichsetzung mit Poisson-Sprinkling.
