# CST-DUST: Randpräparation und Reaktionsbilanz v0.1

8. November 2026 (Zürich). Ausgangspunkt: PR 266, Main
`8d1a3e0906611ec23fdee3088a6bf864d0bd9edc`.

## Ergebnis und Reichweite

Die notwendige Randreaktion lässt sich durch zusätzliche Impulsdaten und eine
passende Phase mathematisch tragen. Solche Daten sind durch die vorhandene
Materiewirkung aber nicht physikalisch ausgewählt. Eine einzige glatte,
nichtverschwindende Randwellenfunktion kann am selben Kragen nicht die ganze
zweiparametrige innere Lösungsfamilie stationär unterstützen. Sie kann einen
Zweig auswählen, wenn ihr Phasengradient unabhängig vorgegeben wird.

Ein expliziter normierter Zustand endlicher Breite erfüllt die Reaktionsbilanz
im Mittel. Sein schärferes gemeinsames Constraint-Verständnis scheitert jedoch
an einem exakt berechneten Kommutator: Auf dem hier zusätzlich deklarierten
kinematischen Raum lassen sich innere Uhrgleichung und alle Randgleichungen
bei positivem w nicht gleichzeitig als verschwindende Operatoren fordern.
Das ist ein Audit dieses Ansatzes, kein Verbot physikalischer CST-Zustände.

Alle acht physikalischen Gates bleiben HOLD. Kein n=5-Produktionslauf,
keine kostenpflichtige Rechnung, keine externe Replikation. Die folgenden
Resultate sind analytisch; kleine rationale Kontrollen prüfen ihre Umsetzung.

## 1. Übernommene Wirkung und die offene Randvariation

Wir halten die Kettengeometrie und die vier vergangenen Dichten bei null fest.
In chronologischer Reihenfolge gelten

    B = (-8, 16, -9, 1),   T* = (-5/2, -2, -4/3, 0).
    m1 = sum B_y T_y,   m2 = sum B_y T_y^2,   sum B_y = 0.
    C(t,T) = 1 - t m1 + m2/2.
    S(t,w,T) = -w C/2,   0<w<1,   t>max T_y.

Am Kragen T* sind m1=0 und m2=-2. Deshalb sind alle t>0 und
0<w<1 innere stationäre Punkte: C=0 und q_t=partial_t S=w m1/2=0.
Die Randreaktion lautet aber

    q_y = partial_Ty S = w B_y (t-T_y)/2.                    (1)

Es gilt sum q_y=0 und sum T_y q_y=w. Die Größen sind Variationsreaktionen,
keine kalibrierten positiven Massenströme. Die Geometriewirkung ist in diesem
festen Geometrieproblem unabhängig von T und liefert keine zusätzliche
Uhrableitung. Randterme, die nur von dieser festen Geometrie abhängen, ändern
(1) ebenfalls nicht.

Ein allgemeiner Check erklärt den Bedarf: Für jede endliche feste Ordnung
mit S_d=-sum_x w_x(1+Gamma_x)/2 und quadratischem Gamma_x gilt
sum_z T_z q_z=-sum_x w_x Gamma_x. Sind alle positiven Dichten innerlich frei
variiert (Gamma_x=-1), alle übrigen Dichten null, und alle Uhren frei stationär,
so folgt 0=sum_x w_x. Nichtleere positive Lösungen sind unter genau diesen
Annahmen unmöglich. Feste Randdaten, zusätzliche Uhrkopplungen, andere
Variationsklassen oder offene Systeme verändern die Voraussetzungen. Dies
ist keine Aussage über komplexe Sättel, Pfadintegrale oder die volle Gravitation.

## 2. Welche Randphase einen klassischen Zweig tragen muss

Betrachte lokal eine Randamplitude psi_B(T)=a(T) exp(i W(T)/hbar), mit reellem
W und positivem glattem a nahe T*. Wir wählen ausdrücklich die Kontraktion
Integral dT psi_B(T) exp(i S/hbar). Für eine konjugierte Randamplitude wäre
das Vorzeichen von W umzukehren. Die reelle Phasenstationarität verlangt

    p_y := partial_Ty W(T*) = -q_y(T*)
        = (w/2) B_y(T*_y-t).                                (2)

Das ist zunächst eine notwendige lokale Sattelbedingung, keine hinreichende
Bewertung des Integrals und keine WKB-Fehlerschranke. Das Profil a und das
Integrationsmaß bleiben eigenständige Angaben.

Für beliebige vorgegebene vier Impulse p ist der stationäre positive Zweig
genau dann vorhanden, wenn die folgenden Rekonstruktionsbedingungen gelten:

    w_hat = -sum T*_y p_y,   0<w_hat<1;
    t_hat = -2 p_3/w_hat,    t_hat>0;
    p_y = (w_hat/2) B_y(T*_y-t_hat) für alle y.               (3)

Beweis: (2) und die zwei Kragenmomente ergeben die ersten beiden Gleichungen;
die letzte Bedingung ist ihre notwendige und hinreichende Rückprüfung. Sie
enthält insbesondere sum p_y=0. Ein beliebiger Impulsvektor mit Summe null
genügt nicht: Er muss im zweidimensionalen Raum span(B, B*T*) liegen und die
Positivitäts-/Kausalitätsbedingungen erfüllen. Bei verschobenem Kragen
T*=T_original+c lautet die zweite Formel t_hat=c-2p_3/w_hat.

Für t=w=1/2 lautet der eindeutige passende Vektor

    p = (6, -10, 33/8, -1/8),   p dot T* = -1/2.            (4)

Dies bestimmt keine reale Masse oder experimentell gemessenen Impulse.
Es gibt lediglich genau an, welche unabhängigen Randdaten das reduzierte
Modell noch benötigen würde. Ein nachträgliches Fitten von p an einen
gewünschten Bounce wäre keine physikalische Vorhersage.

### Keine universelle einzelne Phase für die flache Familie

Die Vektoren B und B*T* sind linear unabhängig. Für zwei Paare (t,w) und
(t',w') impliziert q(T*;t,w)=q(T*;t',w') zunächst w=w' und dann t=t'.
Eine einzige differenzierbare Phase W mit festem Gradienten an T* unterstützt
daher höchstens ein Paar. Das schließt gemischte Zustände, überlagerte
Phasenzweige, Korrelationen mit Außenvariablen oder unterschiedliche
Sattelpunkte bei unterschiedlichen T nicht aus. Es betrifft ausdrücklich
denselben Kragen und eine einzelne lokale Phase.

Das scheinbar einfache W(T;t,w)=-S(T;t,w) würde die gesamte Wirkung auslöschen,
wenn t,w als Variationsgrößen mitgeführt werden. Dann verschwinden auch
partial_w(S+W) und partial_t(S+W) identisch für beliebige T: Die Normierung
wurde entfernt, nicht dynamisch hergeleitet. Eine auf ein festes Paar
(t*,w*) abgestimmte W(T) ist dagegen ein zulässiger zusätzlicher Prüfzustand;
sie darf bei weiterer Variation nicht mit dem veränderlichen Paar nachgeführt
werden. Diese Unterscheidung ist für die Kontrollen verbindlich.
Am fest eingestellten Paar löscht diese Diagnosephase die T-Abhängigkeit
der Gesamtphase aus. Sie liefert damit keine isolierte Sattel-Lokalisierung;
die Amplitudenhülle wird weiterhin von außen vorgegeben.

## 3. Ein normiertes Paket, das die mittlere Reaktion tatsächlich trägt

Für den folgenden Diagnosevertrag sind t=t*>0 und w=w*>0 fest. Setze
delta=T-T*, Omega=(-epsilon,epsilon)^4, 0<epsilon<=1/64, t*>=1/4.
Damit bleiben die innere Kettenordnung und t*>max T erhalten. Der Raum ist
L2(Omega,d4delta); die Amplitude liegt in H0^1(Omega). Definiere

    a_epsilon(delta) = epsilon^(-2)
                      product_y cos(pi delta_y/(2epsilon)),
    psi_epsilon = a_epsilon exp(-i S(t*,w*,T*+delta)/hbar).    (5)

Jeder eindimensionale cos²-Faktor integriert zu epsilon, daher ist die
Norm eins. Das Paket ist glatt im Innern und besitzt verschwindende Randspur.
Es ist ein neuer kinematischer Diagnosezustand, nicht die Box-Amplitude von
PR 266 und keine aus der Außenraumdynamik gewonnene Präparation.

Mit P_y=-i hbar partial_Ty gilt auf dieser Domäne

    <P_y> = -<q_y> = -q_y(T*) = p_y.                        (6)

Der Ableitungsterm der reellen Amplitude integriert wegen ihrer Randspur zu
null. E delta_y=0, daher entspricht <q_y> der mittleren Reaktion des scharfen
Kragens. Das Paket trägt also genau den zuvor fehlenden mittleren Randimpuls.
P_y wird hier als symmetrischer Differentialoperator auf H0^1 benutzt; wir
behaupten keine selbstadjungierte Impulsrealisierung mit Dirichlet-Rand.

## 4. Residuen und ein scharfes Budget für die endliche Breite

Eine zusätzliche, strengere Deutung würde die Randreaktion durch

    R_y = P_y + q_y(T)                                     (7)

als Operatorgleichung erzwingen. Das wird hier geprüft, nicht als physikalische
Dirac-Quantisierung vorausgesetzt. Für (5) folgt R_y psi=-i hbar exp(-iS/hbar)
partial_y a. Damit ist

    E_R := sum_y ||R_y psi||² = pi² hbar²/epsilon².          (8)

Mehr noch: Für jedes normierte psi in H0^1(Omega) gilt dieselbe rechte Seite
als Untergrenze. Multiplikation mit exp(iS/hbar) ist unitär, führt R auf P
zurück und erhält die Nullrandspur. Die erste Dirichlet-Eigenzahl des
vierdimensionalen Würfels ist 4(pi/(2epsilon))². Der Produkt-Cosinus in (5)
erreicht diese Poincaré-Grenze. Es wird kein bloßer Mittelwert als kleine
vollständige Abweichung ausgegeben.

Die Wahrscheinlichkeit von delta ist unabhängig von der Phase. Setze

    c2 = 1/3 - 2/pi²,
    c4 = 1/5 - 4/pi² + 24/pi⁴,
    K(t) = 402 t² + 1560 t + 1568.

Aus den cos²-Momenten E delta²=c2 epsilon²,
E delta⁴=c4 epsilon⁴ und der Unabhängigkeit der vier Koordinaten folgt exakt

    E_C := ||C psi||²
         = c2 K(t*) epsilon²
           + (201/2)(c4-c2²) epsilon⁴,
    E_q := ||q_t psi||² = (201/2) w*² c2 epsilon².           (9)

Die Momentformeln lassen sich ohne Quadratur prüfen: cos²(pi x/2)
=(1+cos(pi x))/2. Für J_n=Integral_{-1}^1 x^(2n) cos(pi x) dx
gilt J_0=0 und nach zweimaliger partieller Integration
J_n=-4n/pi²-2n(2n-1)J_(n-1)/pi². Damit erhält man c2 und c4.

Die Mittelwerte von C und q_t verschwinden. Die positiven Residuen bleiben.
Bei festem hbar verbessert epsilon->0 also die innere Normierung und
Uhrgleichung, während die Randabweichung E_R divergiert. Die Summe E_q+E_R
hat in diesen normierten Modelleinheiten ohne die Ordnungsschranke das
Minimum bei epsilon⁴=pi² hbar²/[(201/2)w*² c2]; physikalische Einheiten oder
ein ausgewogenes Fehlerbudget dürfen daraus nicht ohne Kalibrierung abgeleitet
werden. Für alle zugelassenen epsilon ist das Produkt unabhängig von epsilon:

    E_q E_R = (201/2) w*² c2 pi² hbar².                    (10)

## 5. Der Kommutator erklärt die Grenze unabhängig vom Cosinus-Paket

Die innere Uhrfunktion ist q_t=w* m1/2. Weil alle q_y Multiplikationsoperatoren
sind, gilt auf glatten Funktionen mit kompakter Stütze und anschließend in
der entsprechenden schwachen Form

    [q_t, R_y] = i hbar w* B_y/2.                           (11)

Setze v=B/sqrt(402) und R_v=sum v_y R_y. Aus Integration durch Teile und
Cauchy-Schwarz (äquivalent zur üblichen Kommutator-Unschärferelation) folgt

    ||q_t psi|| ||R_v psi|| >= hbar w* sqrt(402)/4,
    E_q sum_y ||R_y psi||² >= (201/8) hbar² w*².             (12)

Die nichtzentrierten Normen sind mindestens die jeweiligen Standardabweichungen;
die zweite Zeile folgt zusätzlich aus ||R_v psi||²<=sum ||R_y psi||².
H0^1-Approximation durch kompakt getragene glatte Funktionen rechtfertigt die
Formidentität auch für (5). Es ist keine Selbstadjungiertheit von vier
Dirichlet-Impulsen erforderlich.

Bei hbar>0,w*>0 können auf diesem Raum nicht alle geforderten Residuen exakt
null sein. Schon klassisch ist die analoge kanonische Poissonklammer
{q_t,R_y}=w*B_y/2 nicht null. Das naive gemeinsame Erzwingen ist daher kein
nachgewiesenes System erstklassiger Constraints. Eine vollständige
Constraintanalyse könnte Reduktion, zusätzliche Variablen oder andere
Operatoren erfordern. Wir haben diese Auswahl nicht vorgenommen. Die
Ungleichung ist kein Beweis, dass eine physikalische CST-Randpräparation
unmöglich wäre.

Als Skalierungscheck: Wenn nur epsilon verschwindet und hbar fest bleibt,
kann E_R nicht klein werden. Im zusätzlichen formalen Doppellimit
hbar/epsilon->0 und epsilon->0 gehen beide Residuen gegen null. Das ist
keine normierte Zustandsgrenze bei festem hbar und kein physikalisch
kalibrierter semiklassischer CST-Limes.

## 6. Was ein willkürlicher Flächenträger nicht löst

Man könnte die zwei Momentbedingungen F1=m1=0 und F2=m2+2=0 durch neue
Multiplikatoren lambda1 F1+lambda2 F2 hinzufügen. Die Randgleichung würde
am stationären Kragen formal mit lambda1=-wt/2 und lambda2=w/4 schließen.
Das ist eine neue Wirkung und eine neue Quantisierungsentscheidung. Eine
unbeschränkte Fourierintegration über diese Multiplikatoren ist nicht das
vorhandene normierte Dichtemaß und keine normalisierte Präparation.

Auch das Skalarprodukt wird durch die Angabe 'auf der Momentfläche' nicht
eindeutig. Für das zusätzliche konditionierte Lebesgue-Maß würde die
Coarea-Formel d4T delta(F1)delta(F2)=dH²(T)/J_F(T) liefern, wobei

    J_F² = 4[(sum B²)(sum B²T²) - (sum B²T)²].             (13)

Am Zeugen: sum B²=402, sum B²T=-780, sum B²T²=1568,
also J_F²=87744>0. Die Fläche ist lokal glatt von Dimension zwei.
Schon die Transformation F1->a F1, F2->b F2 multipliziert dieses bedingte
Maß mit 1/|ab|; eine ortsabhängige invertierbare Neubeschreibung ändert es
entsprechend lokal. Eine mittransformierte Gewichtung könnte das ausgleichen,
müsste aber definiert werden. Die Projektquelle liefert keine solche Auswahl.
Die Rechnung illustriert Maßabhängigkeit, keine fertige Rigging-Map.

## 7. Reproduktion, Grenzen und nächster physikalischer Schritt

`analyze.py` prüft Reaktionsableitungen über zentrale Differenzen der
quadratischen Wirkung, Rekonstruktion von (t,w), Verschiebungen, das Scheitern
eines gemeinsamen Gradienten und Kommutatorkoeffizienten mit Fraction-Arithmetik.
Die cos²-Budgets werden durch rationale Intervalle eingeschlossen; pi wird
über die Machin-Identität und alternierende arctan-Reihen begrenzt.
Dezimalwerte sind nur lesbare Näherungen zu separat ausgegebenen rationalen
Intervallen. Negativkontrollen sind unabhängige konkrete Fehlannahmen,
keine Peer-Review- oder Beweisassistentenprüfung. `replay.py` reproduziert die
Ergebnisdateien isoliert und bytegleich. Der Kontrollplan ist nach analytischem
Entwurf und vor Ausführung gehasht, nicht extern präregistriert.

Die Randpräparation ist jetzt als konkrete mathematische Anforderung
ausgearbeitet, aber physikalisch offen. Der nächste sinnvolle Arbeitsschritt
ist eine aus demselben Materie-/Außenraummodell gewonnene Randamplitude
oder eine begründete kanonische Reduktion. Sie muss unabhängig vom gewünschten
Bounce angeben: (i) welche Randvariablen und Kopplungen existieren, (ii) wie
Phase, Maß und Amplitude entstehen, (iii) welche Gleichungen Sattelbedingungen
und welche tatsächliche Operator-Constraints sind. Danach ist (2) eine
prüfbare Reaktionsanforderung und (11) ein konkreter Algebra-Test.
Ein beliebiger linearer Randterm, eine passend gewählte Phase oder ein
größerer Integrationslauf schließt diese physikalische Lücke nicht.

## Primärquellen

* Projekt: PR 266 und vier unverändert beigefügte Dateien mit Commit-URLs
  und Git-Blob-Identitäten in `provenance.json`.
* Buck, Dowker, Jubb, Surya: Boundary Terms for Causal Sets (2015),
  https://arxiv.org/abs/1502.05388. Raumartige geometrische Randterme mit
  passendem Kontinuumsmittel; keine Quelle für die hier gewählte Materiephase.
* Brown, Kuchař: Dust as a standard of space and time in canonical quantum
  gravity (1995), https://doi.org/10.1103/PhysRevD.51.5600. Eigenständige
  gekoppelte kanonische Staubkonstruktion; keine direkte Quantisierung dieses
  endlichen Record-Modells.
* Dowker, Liu, Lloyd-Jones: Timelike boundary and corner terms in the causal
  set action, https://arxiv.org/abs/2501.00139. Geometrische Rand-/Eckbeiträge;
  sie liefern nicht die hier zusätzlich benötigten Uhrimpulsdaten.

Die einfachen Variations-, Unschärfe-, Poincaré- und Coarea-Argumente werden
nicht als neue allgemeine mathematische Methoden beansprucht. Neu ist hier
ihre konkrete Anwendung auf den versionierten Projektkandidaten.
