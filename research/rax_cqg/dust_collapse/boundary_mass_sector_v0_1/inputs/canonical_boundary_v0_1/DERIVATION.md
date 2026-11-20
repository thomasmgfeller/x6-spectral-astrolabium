# CST-DUST: kanonische Randrelation und lokale Reduktion v0.1

8. November 2026 (Zürich). Basis: Main nach PR 267,
`a373f318e4a99bf1e2496f4d5bc674da6f6ea59c`.

## 0. Ergebnis und Anspruchsgrenze

Aus der vorhandenen reduzierten Materiewirkung lässt sich die klassische
stationäre Randrelation vollständig für den offenen positiven Dichtesektor
bestimmen. Sie ist ein offener Teil des Konormalbündels einer explizit
parametrisierten zweidimensionalen Momentfläche. Die vierdimensionale
Relation ist lagrangesch im acht-dimensionalen Rand-Kotangentialraum.
Das ist eine geometrische Aussage über die Wirkung, noch keine
vierdimensionale Raumzeitdynamik, kein physikalischer Zustandsraum und kein
entwickelndes Hamiltonsystem.

Der nichtverschwindende Kommutator aus PR 267 bleibt richtig. Er entsteht
bei der dort zusätzlich geprüften gemeinsamen Operatorforderung. Ergänzt
man formal alle kanonischen Impulse, kommutieren die Gradienten-Graphoperatoren;
dieser rein kinematische Trick wählt aber keine Physik aus. Eine ausdrücklich
bedingte Dirac-Reduktion der normalen Koordinaten zeigt, wie eine mathematisch
konsistente Alternative aussehen kann. Ihr Tangentialraum besitzt weder eine
ausgewählte Dynamik noch eine ausgewählte Präparation.

Das ursprüngliche Dichte-Nullatom und das positive Kontinuum bleiben getrennt.
Der Atomzweig erlaubt beliebige geordnete Randuhren und darf nicht nachträglich
auf die Momentfläche projiziert werden. Ein endliches normiertes Dichteintegral
wird auch in den neuen Variablen nicht zu einer Deltafunktion.

**Alle acht physikalischen Gates bleiben HOLD.** Kein n=5-Produktionslauf,
keine kostenpflichtige Rechnung, keine externe Replikation. Alle hier
verwendeten Uhren und Wirkungsparameter behalten ihre reduzierte
Projektnormierung. Die Konstruktion ist nicht als neue allgemeine Methode
beansprucht.

## 1. Wirkung als erzeugende Familie

Auf der festen Kette mit vier Vorgängern, deren Dichten null bleiben, sei

    B = (-8,16,-9,1),   T0<T1<T2<T3<t,   0<w<1,
    F1(T) = sum B_y T_y,
    F2(T) = 2 + sum B_y T_y^2,
    C = -t F1 + F2/2,
    S(T,t,w) = (wt/2)F1 - (w/4)F2.                         (1)

Das entspricht genau S=-wC/2 aus PR 267. Es gibt keine neue Randwirkung.
Mit inneren Variablen t,w gilt

    partial_t S = w F1/2,
    partial_w S = t F1/2 - F2/4.                            (2)

Für w>0 sind beide Gleichungen genau dann null, wenn F1=F2=0.
Die Jacobi-Matrix von (partial_t S,partial_w S) nach (F1,F2) ist

    [[w/2, 0], [t/2, -1/4]],   Determinante -w/8.           (3)

Sie ist invertierbar. Sobald dF1 und dF2 unabhängig sind, ist die Familie
im üblichen Sinn einer erzeugenden Familie nichtentartet: Die Differentiale
ihrer zwei kritischen Gleichungen haben Rang zwei. Das steht nicht im
Widerspruch zur verschwindenden inneren (t,w)-Hesse-Matrix auf F=0.
Eine nichtentartete kritische Gleichungsmenge ist kein isolierter Sattel.

Wir behalten die Konvention von PR 267: Der Impuls der stützenden
Randamplitude ist p=-partial_T S. Damit

    p = alpha dF1 + beta dF2,
    alpha = -wt/2,   beta = w/4.                            (4)

Das eigentliche Wirkungsdifferential hätte das entgegengesetzte Vorzeichen;
alle folgenden Aussagen sind mit der gewählten Kontraktionsorientierung
konsistent.

## 2. Vollständige Parametrisierung der geordneten Momentfläche

Setze c=T3 und die positiven Lücken

    a=c-T0,   b=c-T1,   d=c-T2,   a>b>d>0.

F1=0 liefert d=(16b-8a)/9. Einsetzen in F2=0 ergibt

    17a² - 32ab + 14b² = 9/4.

Die einzige mit a>b verträgliche Lösung ist

    D(b) = sqrt(72b²+153),
    a(b) = (32b+D(b))/34,
    d(b) = (16b-8a(b))/9,
    T(c,b) = (c-a(b), c-b, c-d(b), c),
    c in R,   b > 1/(2 sqrt(2)).                            (5)

Beweis der Domäne: Der Minuszweig der quadratischen Lösung hat a<b und
ist unzulässig. Auf dem Pluszweig ist a>b automatisch. Die weitere Bedingung
d>0 ist äquivalent zu a<2b und zu b²>1/8. Dann gilt auch d<b. Umgekehrt
besitzt jedes geordnete Lösungstupel eindeutig die Koordinaten c,b. Das ist
also eine globale Karte dieser geordneten Momentfläche M, keine nur am
früheren Zeugen gefittete Parametrisierung. Der Zeuge von PR 266 ist c=0,b=2.

Für eine lokale Fortsetzung abseits von M verwenden wir

    Q(T) = (c=T3, b=T3-T1, F1, F2).

Der Betrag der Jacobi-Determinante ist

    |det DQ| = 144(T2-T0) > 0.                              (6)

Damit ist dies in einer Umgebung jedes geordneten Punkts eine gültige
lokale Koordinatenwahl. Es wird keine globale eindeutige Fortsetzung für
alle Werte von F1,F2 behauptet. Auf M vereinfacht sich (6) zu 8D(b).

## 3. Die Randrelation ist lagrangesch, nicht bereits eine Evolution

Die positive innere stationäre Randrelation lautet

    L+ = {(T,p): T in M,
          p=alpha dF1+beta dF2,
          0<beta<1/4,   alpha < -2 beta c}.                 (7)

Die letzte Ungleichung entspricht genau t>c; w=4beta und
t=-alpha/(2beta) rekonstruieren die inneren Parameter. Für endliche
zusätzliche Uhrfenster wird dieser offene Sektor entsprechend eingeschränkt.
Weil dF1,dF2 unabhängig sind, sind die Parameter (c,b,alpha,beta) lokal
unabhängig. L+ hat Dimension vier.

Für die kanonische Einsform theta=sum p_y dT_y gilt auf L+

    theta|L+ = alpha dF1 + beta dF2 = 0.                    (8)

Denn tangential an M verschwinden dF1 und dF2. Deshalb verschwindet auch
dtheta auf L+; zusammen mit der halben Dimension beweist das die
Lagrange-Eigenschaft. Die Relation erhält also die symplektische Struktur
im Sinn einer Randbedingung, liefert aber keinen ausgewählten Verlauf.

In den Kotangentialkoordinaten zu Q sei

    p = (DQ)^T (Pc,Pb,Pi1,Pi2).

Dann ist (7) schlicht

    F1=F2=0,   Pc=Pb=0,   Pi1=alpha, Pi2=beta,              (9)

wobei alpha,beta in (7) frei laufen. Wichtig: (9) ist eine Beschreibung
einer Lösungsmannigfaltigkeit. Würde man sämtliche vier Gleichungen
F1=F2=Pc=Pb=0 zusätzlich als erstklassige Eichconstraints interpretieren
und alle ihre lokalen Flüsse ausquotientieren, blieben lokal keine
Freiheitsgrade. Eine solche Eichdeutung folgt nicht aus der Lagrange-Eigenschaft.
Auch die starre Verschiebung von c ist nicht allein deshalb Eichfreiheit.
Die sechsvariable Zahlfunktion S enthält keinen externen Evolutionsparameter
und bestimmt weder einen physikalischen Hamiltonian auf M noch eine
Abbildung zwischen zwei vollständig spezifizierten Rand-Schnitten.

## 4. Woher der Kommutator kommt und was seine Ergänzung wirklich leistet

Auf einer lokalen offenen positiven Konfigurationsdomäne mit
z=(T0,T1,T2,T3,t,w) kann man als zusätzliche kinematische Struktur die
kanonischen Impulse P_i=-i hbar partial_zi einführen. Auf C_c^infinity gilt
für die Graphoperatoren

    R_i = P_i + partial_zi S,
    [R_i,R_j] = i hbar(partial_j partial_i S
                         -partial_i partial_j S) = 0.      (10)

Konkret hebt der Term [P_t,q_y]=-i hbar w B_y/2 den Term
[q_t,P_y]=+i hbar w B_y/2 genau auf. In PR 267 wurde hingegen bei fixem t,w
q_t als Multiplikationsbedingung getestet; der Impuls P_t gehörte nicht zu
diesem Raum. Dort bleibt [q_t,R_y]=i hbar w B_y/2 korrekt. Die zwei
Operatoransätze dürfen nicht gleichgesetzt werden.

Gleichung (10) ist keine hergeleitete physikalische CST-Constraintalgebra.
Jede glatte skalare Funktion erzeugt einen solchen flachen Gradienten-Graphen.
Formal löst exp(-iS/hbar) alle R_i psi=0; Normierung, Randdomänen,
Zustandsauswahl und physikalische Observablen folgen daraus nicht.
Das Hinzufügen von sechs kanonischen Paaren plus sechs solchen Constraints
und anschließende vollständige lokale Quotientieren ergäbe wiederum keinen
nichttrivialen reduzierten Freiheitsgrad. Insbesondere ist P_w nicht ohne
weitere Begründung ein selbstadjungierter Impuls auf dem ursprünglichen
Maß mit einem isolierten Dichte-Nullatom. (10) gilt nur lokal im offenen
kontinuierlichen Stratum; eine globale Selbstadjungiertheit wird nicht behauptet.

## 5. Eine bedingte Dirac-Reduktion statt widersprüchlicher Nulloperatoren

Jetzt halten wir ein Paar t*,w* ausdrücklich als zusätzliche äußere Daten fest.
Setze alpha*=-w*t*/2 und beta*=w*/4. Auf einer lokalen Karte mit c<t* betrachte
im Rand-Kotangentialraum die vier Bedingungen

    chi=(F1,F2, Pi1-alpha*, Pi2-beta*).                     (11)

Sie fixieren die beiden normalen Konfigurationsrichtungen und ihre
normalen Impulse. Die Poissonmatrix ist exakt

    Delta = [[0,I2],[-I2,0]],  det Delta=1,
    Delta^(-1)=-Delta.                                     (12)

Dies sind zweitklassige Bedingungen. Mit der Dirac-Klammer

    {A,B}_D = {A,B} - {A,chi_i}(Delta^-1)_ij{chi_j,B}        (13)

werden die vier chi zu Casimiren. Für die verbleibenden Koordinaten gilt

    {c,Pc}_D={b,Pb}_D=1, alle übrigen Basisklammern null.    (14)

Der reduzierte Raum ist lokal T*M. Die normale Unschärfe aus PR 267 wird
nicht verletzt: F und die eliminierten normalen Impulse sind hier keine
unabhängigen Operatorpaare des ursprünglichen L2(d4T)-Raums mehr. Man hat
Raum und Klammer ausdrücklich verändert. Nachträglich zusätzlich alte
Ambient-Operatoren als exakte Bedingungen aufzuerlegen wäre unzulässig.

Die Randrelation der ursprünglichen Wirkung verlangt außerdem Pc=Pb=0.
Das ist im reduzierten T*M eine lagrangesche Nullsektion, kein Hamiltonian
und keine Auswahl eines normierten Quantenzustands. Beliebige Pc,Pb im
reduzierten Phasenraum sind mathematisch möglich, gehören aber ohne
zusätzliche Kopplung nicht zur stationären Randrelation (7). Die Reduktion
ist ein konsistenter bedingter Prüfvertrag und keine Begründung der
festgehaltenen Werte t*,w* oder der physikalischen Präparation.

## 6. Konfigurationsmaß, Phasenraummaß und Zustandstransport

Die geerbte Wahl eines konditionierten Lebesgue-Konfigurationsmaßes ergibt
in der Karte (5) durch (6)

    d4T delta(F1)delta(F2) = k(b) dc db,
    k(b) = 1/[8 sqrt(72b²+153)].                            (15)

Am Zeugen b=2 ist k=1/168. Dies stimmt mit dem Coarea-Faktor aus PR 267
überein: J_F²=87744 und det(g)=457/147, sodass sqrt(det g)/J_F=1/168.
Die explizite Herleitung bestimmt nur dieses deklarierte bedingte Maß,
kein physikalisches Skalarprodukt.

Andererseits ist die kanonische Liouville-Dichte unter dem Punkttransform
(T,p)->(Q,Pi) invariant: Die Konfigurationsdeterminante und ihre inverse
Impulsdeterminante heben sich auf. Der zweitklassige Reduktionsausdruck

    d4Q d4Pi delta^4(chi) sqrt(|det Delta|)

reduziert sich genau auf dc db dPc dPb. Eine konstante invertierbare
Umdefinition chi'=A chi multipliziert die Deltafunktionen mit 1/|det A|
und die Wurzeldeterminante mit |det A|. Der Produktfaktor bleibt eins.
Ein Konfigurations-Coarea-Faktor darf deshalb nicht ungeprüft ein zweites
Mal in die Phasenraumreduktion eingefügt werden. Auch ein Liouville-Maß
bestimmt allein noch keine Quantenpolarisation oder einen physikalischen Zustand.

Zwei mögliche kinematische Konfigurationsdarstellungen sind
L2(M,k dc db) und L2(M,dc db). Weil k glatt und positiv ist, verbindet sie
der unitäre Transport U psi=sqrt(k) psi. Unterschiede der Maßdichte allein
beweisen daher keine physikalische Ungleichwertigkeit. Die zugehörigen
lokal symmetrischen Impulse auf C_c^infinity lauten in der k-Darstellung

    Pc = -i hbar partial_c,
    Pb = -i hbar[partial_b -36b/(72b²+153)].                 (16)

U führt sie auf die gewöhnlichen Ableitungsoperatoren der flachen
Darstellung zurück. Selbstadjungierte Fortsetzungen am Rand b=1/(2sqrt2),
Zustände und Dynamik sind nicht festgelegt. Fordert man zusätzlich beide
Tangentialimpulse als Nullbedingungen, wäre lokal psi=const/sqrt(k).
Auf der gesamten offenen M (oder c<t* mit unbeschränkter Vergangenheit)
ist dieser Zustand nicht normierbar: Seine Norm ist proportional zu
Integral dc db. Es gibt hier keinen kanonisch ausgewählten normierten
'konstanten physikalischen Zustand'.

## 7. Warum die Maßänderung keine Fourier-Delta-Präparation liefert

Die positive Variablenänderung aus (4) hat

    |partial(alpha,beta)/partial(t,w)| = w/8,
    dt dw = (2/beta) d alpha d beta.                        (17)

Für das ursprüngliche Modellmaß nu(dw)=1/2 delta0+1/2 dw auf (0,1)
und ein gleichförmiges Uhrfenster t in [c+u0,c+u1] der Länge L>0 ist
der kontinuierliche Anteil daher

    (dt/L)(dw/2) = [1/(L beta)] d alpha d beta,
    0<beta<1/4,
    -2beta(c+u1)<alpha<-2beta(c+u0).                        (18)

Die scheinbare 1/beta-Singularität ist zusammen mit der schrumpfenden
alpha-Breite integrierbar. Die Gesamtmasse dieses Anteils ist 1/2, sein
erstes w-Moment 1/4 und sein zweites w-Moment 1/6. Ein flaches unabhängiges
Fouriermaß auf R² wäre eine andere Konstruktion. Selbst eine nachträgliche
Normierung eines fälschlich flachen Maßes auf demselben Kegel repariert
nicht die Momente: Der erste Moment wäre 1/3 statt 1/4.

Ein konkreter Gegencheck: Bei F1=0,F2=1 ist die Materieamplitude

    G = 1/2 + (1/2) Integral_0^1 exp(-iw/4) dw,
    Re G >= 191/192 > 0.                                  (19)

Die Schranke folgt unmittelbar aus cos x>=1-x²/2. Ein endliches normiertes
Integral projiziert also auch abseits der Momentfläche nicht exakt auf null.
Keine Sattelpunktsprache darf (18) in delta(F1)delta(F2) verwandeln.

## 8. Das Nullatom bleibt ein anderer Zweig

Am isolierten Atom w=0 ist S=0. Eine infinitesimale Dichtevariation ist dort
nicht Bestandteil dieses Stratumvertrags. Es folgt keine Forderung F2=0;
auch die Uhrvariation erzwingt F1=0 nicht. Die stationäre Randrelation des
Atomzweigs ist deshalb die Nullsektion

    L0={(T,p): T0<T1<T2<T3, p=0}.                          (20)

Sie ist wie L+ vierdimensional und lagrangesch. Die Grenze w->0 der
positiven inneren stationären Familie bei endlichem t hat dagegen nur
T in M,p=0. Sie deckt den vollen Atomzweig nicht ab. Eine ausschließlich
auf M aufgebaute Quantisierung würde ohne weitere Begründung einen Teil
des ursprünglichen Atomsektors entfernen. Bei unbeschränkt mit w skaliertem
t können weitere Grenzfragen entstehen; (20) wird damit nicht durch eine
solche gekoppelte Grenzfolge ersetzt.

Diese Klassifikation betrifft innere positive stationäre Punkte und das
separat vorhandene Atom. Endpunkte der kontinuierlichen w-Integration,
Uhrfensterränder, komplexe Sättel und Beiträge nichtstationärer Punkte sind
nicht durch die klassische Relation klassifiziert. Die volle Amplitude
bleibt das jeweilige Integral mit seinem tatsächlichen Träger.

## 9. Reproduktion und nächster konkreter Test

Sparse rationale Polynome prüfen alle 36 Klammern der sechs
Graphoperatoren symbolisch. Eine unabhängige rationale Parametrisierung
der Hyperbel liefert exakte Kontrollpunkte ohne Rundungsfehler; dort werden
Randreaktion, Karten-Jacobian, Coarea-Faktor, Kotangentialtransport und die
Dirac-Reduktion geprüft. Acht konkrete Negativannahmen werden zurückgewiesen.
Drei wissenschaftliche Ergebnisdateien sind isoliert bytegleich reproduzierbar.
Der lokale Kontrollplan wurde nach dem analytischen Entwurf vor Ausführung
gehasht; keine externe Präregistrierung und keine externe Replikation.

Damit sind drei Vorarbeiten geschlossen: (i) die stationäre Randrelation
im angegebenen Modell, (ii) der Unterschied zwischen Graphgleichung und
physikalischem Constraint, (iii) eine bedingte, mathematisch konsistente
Reduktion samt Maßtransport. Die physikalische Auswahl ist nicht geschlossen.

Als nächstes muss ein expliziter zweiter Rand-/Außenblock aus derselben
Materiewirkung gekoppelt werden. Zu prüfen sind die Impulsbilanz am
geteilten Rand, alle neu entstehenden beziehungsweise umklassifizierten
Kausalintervalle und die tatsächlich durch beide Blöcke bestimmten Daten.
Erst daraus kann eine nicht willkürlich vorgegebene Randantwort entstehen.
Die feste Geometrie bleibt dabei zunächst eine kontrollierte Testklasse;
eine volle Geometriesumme oder ein physikalischer Außenraum folgt daraus
noch nicht. Die hier konstruierten Randkoordinaten und Impulse machen diesen
Verklebungstest konkret und ohne Großrechenlauf durchführbar.

## Primärquellen und Abgrenzung

* Projekt: PR 267, https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/267.
  Vier unveränderte Projektquellen und Lizenz mit Git-Identitäten in provenance.json.
* Dittrich und Höhn, Canonical simplicial gravity,
  https://arxiv.org/abs/1108.1974, Class. Quantum Grav. 29 (2012) 115009.
  Kontext für aktionsbasierte kanonische Beschreibungen diskreter Systeme;
  die dortige Regge-Dynamik wird nicht auf CST übertragen.
* Cattaneo, Mnev und Reshetikhin, Classical BV theories on manifolds with
  boundary, https://arxiv.org/abs/1201.0290, Commun. Math. Phys. 332 (2014)
  535-603. Kontext für Randphasenräume und Verklebung; keine Behauptung,
  hier eine BV/BFV-Quantisierung des CST-Modells ausgeführt zu haben.

Alle für den endlichen Kandidaten benötigten Identitäten sind oben
selbständig hergeleitet. Die Quellen ersetzen keine physikalische
Validierung des projektspezifischen Materie- und Maßmodells.
