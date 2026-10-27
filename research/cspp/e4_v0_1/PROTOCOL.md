# CSPP E4-V0.1: mathematischer und statistischer Prüfvertrag

**Revision:** draft-1, 2026-10-27. **Status:** NOT_FROZEN, NOT_RUN.
`contract.json` enthält die numerischen Werte dieses Entwurfs. Bei einem
Widerspruch zwischen Text und JSON wird nicht ausgeführt; die Abweichung
muss vor dem Freeze aufgelöst werden.

## 1. Ziel, Referenz und Gültigkeitsbereich

Wir untersuchen numerische Korrespondenz auf festem flachem Hintergrund.
Das Primärziel ist eine quantifizierte endliche Genauigkeit, kein Nachweis
eines Naturgesetzes und kein Beweis eines Grenzwerts aus endlich vielen
Dichtestufen. Das Poisson-Ensemble ist zunächst ein Benchmark-Ensemble.

Für jede Dichtestufe vergleichen wir dieselben physikalischen Eingaben mit
einer kontinuierlichen Referenz. Die kontinuierliche Referenz selbst muss
validierte Fehlergrenzen liefern. Unterschiede zwischen zwei numerischen
Lösern allein sind keine solche Grenze. Kein verrauschter Operator wird
als unbekannte Funktion `build_dirac_candidate` ohne Definition zugelassen.

Die drei Fehlerstufen sind:

1. gemeinsame Geometrieregion aus Ordnung/Zählungen;
2. diskreter Operator, Zustandsentwicklung und ihre deterministischen Fehler;
3. gemeinsame Observablenintervalle und Ensembleauswertung.

Die Entwicklungsfolge Skalar → Dirac → Zertifikatsweitergabe → E4 ändert
diese Architektur nicht. Fehlerzuordnung bedeutet keine angenommene
statistische Unabhängigkeit der Fehlerquellen.

## 2. Einheiten, Region und Sprinkling

Natürliche Einheiten: c = hbar = 1. Eine feste Referenzlänge L0 definiert
alle dimensionslosen Zahlen. Koordinatenreihenfolge (t,x,y,z), Signatur
eta = diag(-1,+1,+1,+1), Box = -d_t^2 + Laplace.

Die offene Primärregion ist der Alexandrov-Diamant

    Omega = { (t,x): |t| + ||x|| < 4 L0 }.

Seine Spitzen liegen bei (-4 L0,0) und (4 L0,0). Seine Dauer ist 8 L0,
sein Vierervolumen V = pi (8 L0)^4 / 24 = (512 pi / 3) L0^4.
Die Skalenparameter sind nu = rho V und N ~ Poisson(nu). Nach dem
Poisson-Zug werden N unabhängige Punkte volumenuniform in Omega erzeugt.
Fixes N ist nicht das Primärmodell. Die erwartete Zahl nu und die tatsächlich
gezogene Zahl N werden beide gespeichert. rho hat Dimension L0^-4.

Kausalrelation: x precedes y genau dann, wenn dt > 0 und dt^2 >= ||dx||^2.
Zufällige exakt lichtartige Paare haben Maß null. Fast lichtartige Paare
benötigen beim Implementieren eine dokumentierte Fehler-/Präzisionsregel;
sie dürfen nicht still durch eine beliebige Toleranz umgeordnet werden.
IDs sind Verwaltungskennungen, keine physikalischen Koordinaten.

Entwicklungspilot: nu = 512, 1024, 2048, 4096, zunächst 16 unabhängige
Sprinklings je Zelle, maximal 100. Ein Entwicklungsjob erhält höchstens
6 Stunden Wandzeit und 4 GiB Arbeitsspeicher. Erschöpfung wird protokolliert;
sie ist kein physikalischer Negativbefund. Dies ist ein vorgeschlagener
Pilotplan, keine tatsächlich erzeugte Stichprobe. Zusätzliche Zellen werden
als Entwicklungsversion dokumentiert. Finale nu-Werte und M sind offen.

Der diskrete Maßstab ell = rho^(-1/4) wird mit L0, Feldwellenlänge und
Glättungsmaßstab ell_k verglichen. Für einen geglätteten Operator muss vor
dem Freeze der gekoppelte Grenzplan für ell und ell_k feststehen.
ell → 0 bei festem ell_k darf nicht als lokaler Grenzübergang ausgegeben werden.

## 3. Konkreter Zweiflavor-Eingangszustand

Zwei freie Dirac-Massenfelder haben m1 L0 = 1 und m2 L0 = 2.
Die reale Mischungsmatrix ist

    U = [[cos(theta), sin(theta)], [-sin(theta), cos(theta)]], theta = pi/6,
    Psi_flavor = U Psi_mass.

Flavornamen sind f0 und f1; dies sind Benchmarklabels, keine kalibrierten
Elektron-/Myon-Neutrinoraten. CP-Phase und Materiepotential sind null.

Auf der Referenz-Cauchyfläche t0 = -L0 liegt eine normierte Quelle:

    f(x) = A exp(-1/(1-r^2/a^2)) exp(i k0 z),  r<a; sonst 0,
    a = L0/2, k0 = 4/L0, u = (1,0,0,0)^T,
    Psi_flavor(t0,x) = (f(x)u, 0),
    A^-2 = 4 pi integral_0^a r^2 exp(-2/(1-r^2/a^2)) dr.

Damit sind Norm, Quelle, relative Phase, Spinbasis und Einheiten eindeutig.
Der Zustand ist glatt und räumlich kompakt getragen. Er ist nicht auf
positive Energie projiziert und beschreibt deshalb keine reine physikalische
Neutrinoproduktion. Eine positive-Energie-/Produktionsvariante wäre eine neue
Version einschließlich Behandlung ihrer räumlichen Ausläufer.

Referenzentwicklung jeder Massenkomponente:

    i d_t psi_j = H_j psi_j, H_j = -i alpha dot grad + beta m_j.

Wir verwenden die Standard-Dirac-Darstellung beta=diag(I2,-I2),
alpha_i=[[0,sigma_i],[sigma_i,0]] mit den Pauli-Matrizen. In Impulsdarstellung
ist H_j(p)^2 = (|p|^2+m_j^2) I4, daher

    U_j(p,dt) = cos(E_j dt) I4 - i sin(E_j dt) H_j(p)/E_j.

Fourierintegration und Quellennormierung sind numerisch zu validieren;
die Formel selbst liefert noch kein zertifiziertes Integrationsresultat.
Gleichmassen- und Nullmischungsfälle liefern exakte Negativkontrollen.

Primärer Auswertungszeitpunkt: td = +L0. Die maximale Trägerausdehnung
aus endlicher Ausbreitungsgeschwindigkeit ist a+(td-t0)=2.5 L0.
Der Diamantradius ist dort 3 L0: Reserve 0.5 L0. Diese Trägereinschließung
gilt für die lokale Kontinuumsreferenz. Sie beweist keine entsprechende
Randunabhängigkeit eines nichtlokalen diskreten Operators.

Die Slice-Daten werden nicht durch die Forderung erzeugt, dass Poissonpunkte
exakt auf t=t0 oder t=td liegen: ein solches Ereignis hat Wahrscheinlichkeit
null. Injektion, Interpolation und Quadratur benötigen einen expliziten
Adapter mit Fehlergrenze. Seine Wahl ist ein Freeze-Blocker. Wahre
Einbettungskoordinaten sind im Referenzarm erlaubt, im intrinsischen
Rekonstruktionsarm nur für die nachgelagerte Bewertung.

## 4. Detektor, Dichtematrix und Observablen

Der ideale Diagnose-Detektor ist das räumliche Ballfenster

    D = { x: ||x-(0,0,1.5 L0)|| < 0.5 L0 } auf t=td.

Es ist ein festes Fenster der Referenzraumzeit, keine festgelegte Knotenmenge.
Es beschreibt eine ideale Orts-/Flavorprojektion, keine schwache Wechselwirkung.
Sein äußerster Radius 2 L0 liegt innerhalb des Diamanten. Definiere

    R_ab(C) = integral_D sum_spin psi_a(td,x) conj(psi_b(td,x)) d^3x,
    q = tr R, w0=R_00, w1=R_11, C_det=2 |R_01|.

Für einen normierten Gesamtzustand gilt R>=0, 0<=q<=1 und 0<=C_det<=q.
Die **primären Observablen** sind die unbedingten Gewichte w0,w1 und C_det.
Alle liegen in [0,1]. C_det ist ein detektionsgewichtetes Kohärenzmaß in der
festgelegten Flavorbasis, kein universelles basisunabhängiges Kohärenzmaß.

Nur wenn eine zertifizierte Untergrenze q_lower >= 0.05 gilt, werden
rho_D=R/q, P(f_a|D)=w_a/q und C_l1(rho_D)=2|rho_D,01| als sekundäre
Observablen ausgegeben. Bei kleinerem q: CONDITIONAL_NORMALIZATION_HOLD;
die unbedingten Größen bleiben erhalten. Quotienten werden gemeinsam mit
ihrem Nenner eingeschlossen. Eine mittlere bedingte Wahrscheinlichkeit ist
nicht gleich dem Verhältnis zweier Ensemble-Mittelwerte.

Zur Zustandseinschließung verwenden wir die normierte erweiterte Matrix

    sigma = R direct_sum [1-q].

Der dritte Zustand bezeichnet Nichtdetektion, nicht einen dritten Flavor.
D_tr(sigma,sigma') = ||sigma-sigma'||_1/2 liegt in [0,1]. Daraus folgen
|w_a-w'_a|<=D_tr und |C_det-C'_det|<=2 D_tr. Die zweite Schranke folgt aus
der dualen Norm mit einer phasenangepassten offdiagonalen 2x2-Messmatrix.
Die Daten erlauben sowohl E[C_det(R_C)] als auch C_det(E[R_C]); beide
Auswertungen werden getrennt berichtet. Eine Ensemble-Mittelung unbekannter
Phasen ist kein Nachweis intrinsischer physikalischer Dekohärenz.

## 5. Kontrollen und Operatorqualifikation

Alle Methoden benutzen innerhalb einer Realisierung dieselbe Punktwolke.
Die Kontinuumsauswertung wird durch Einbettung/Interpolation auf dieselben
physikalischen Testgrößen bezogen, nicht durch identische Knoten-IDs.

**G1, skalar:** kompakt unterstützte glatte Testfelder, darunter konstante,
affine und quadratische Jets in einem inneren Bereich sowie modulierte
Wellenpakete mit k L0 in {0,2,4,8}. Ein vor dem Freeze festgelegter
glatter Cutoff und seine Ableitungen gehören zum Feld; er darf nicht bei
der Referenzauswertung vergessen werden. Für Propagation wird dieselbe
räumliche Quelle f mit phi(t0)=f und d_t phi(t0)=0 in den KG-Gleichungen
zu m L0 in {0,1,2} verwendet. Fermion und Skalar werden jeweils gegen
ihre passende Referenz verglichen, nicht durch Gleichsetzen ihrer Amplituden.

**G2, Dirac:** direkte Wirkung erster Ordnung, Quadrat-Konsistenz,
Spintransformation, Umnummerierung, Dispersions-/Zusatzmodendiagnose,
Norm/Strom und kausale Stabilität. Vorzeichenkonvention explizit:

    gamma^0=i beta, gamma^j=i beta alpha_j, Q=gamma^mu d_mu,
    {gamma^mu,gamma^nu}=2 eta^mu_nu I4, Q^2=Box I4,
    (Q-m)(Q+m)=Box-m^2.

Dies ist mit dem oben definierten Hamiltonian konsistent. Wir vergleichen
Q_C psi_C mit (Q psi)_C und Q_C^2 psi_C mit (B_C tensor I4) psi_C.
Eine Matrixwurzel allein qualifiziert keine Dirac-Dynamik. In gekrümmter
Raumzeit wären Spinverbindung und Krümmungsterme gesondert zu behandeln.

Für G1/G2 wird die normierte RMS auf einem vorab festgelegten inneren
Auswertungsfenster verwendet. Der Nenner für einen Operator der Ordnung r
ist max(||F||/L0^r, ||A_ref F||); daher kein Dividieren durch einen
verschwindenden Referenzwert. Das Fenster, Quadratur und die vollständige
Testfeldliste müssen im Freeze stehen. Entwurfsgrenze: 0.10 für skalare
Wirkung, direkte Dirac-Wirkung und Quadratvergleich. Sie sind notwendige
Diagnosegrenzen, keine hinreichende Zustandsfehlergarantie.

G2 verlangt zusätzlich unabhängige Prüffelder und frische Prüfwolken,
normierte globale Normdrift <=1e-8 und nachgewiesene Kontrolle der
numerischen Fehler auf dem Intervall [-L0,+L0]. Lorentz-/Spinvergleich und
Kausalitätsprüfung müssen auf gemeinsam transformierten Regionen und
Eingaben erfolgen. Ausführungstoleranzen und der unabhängige Prüfer für
diese Kontrollen sind offen und müssen vor dem Freeze konkretisiert werden.

**G3, Ende-zu-Ende:** gleichmäßige Fehlergrenzen über eine gemeinsame
Geometrieregion Gamma, einschließlich der für Spinoren nötigen Struktur,
der Quelle und der Detektorabbildung. Alle Zustände werden auf denselben
endlichen Observablenraum sigma abgebildet. Die drei Stufen brauchen keine
gemeinsame Knotenzahl, wohl aber nachgewiesene Identifikationsabbildungen.

## 6. Deterministisches Fehlerbudget

Ziel für die primären Gewichte: absolute Abweichung <=0.010, also ein
Prozentpunkt. Für C_det: <=0.020. Diese Ziele wurden vor neuen Daten gewählt;
ihre Erreichbarkeit ist offen. Fehlergrenzen addieren wir über eine
explizite Vergleichskette; keine quadratische Addition ohne Begründung.

| Beitrag | Budget in Spurabstand sigma |
| --- | ---: |
| Geometrierekonstruktion, gleichmäßig über Gamma | 0.003 |
| Diskreter Dirac-Operator einschließlich Injektion/Detektorprojektion | 0.003 |
| Zeitintegration, lineare Algebra und Rundung | 0.001 |
| Berechnung der kontinuierlichen Referenz | 0.001 |
| Summe der vier Zustandsbeiträge | 0.008 |

Die statistische Intervallhalbbreite für Mittelwerte wird auf höchstens
0.002 begrenzt. Damit ergeben sich höchstens 0.010 für ein Gewicht und
2*0.008+0.002=0.018 für C_det, unterhalb des Kohärenzziels 0.020.
Es gibt keine automatische Übertragung dieser Budgets auf normalisierte
bedingte Wahrscheinlichkeiten bei kleinem q.

Die einzelnen Schranken gelten gleichmäßig über den jeweils verbleibenden
Parameterbereich. Abhängigkeiten zwischen Geometrie und Operator bleiben
dadurch enthalten. Ein unabhängiger Vergleich auf exakter Geometrie, mit
rekonstruierter Geometrie und mit strengerem Löser ergänzt die Diagnose.
Korrelationen von Residuen und Flavorfehlern sind keine Ursachenbeweise.

**Zielgrößen nicht vermischen:** O_C bezeichnet die Observable des exakt
gelösten deklarierten diskreten Kandidaten auf der jeweiligen wahren
Benchmarkgeometrie. Seine Abweichung zur Kontinuumsreferenz ist der zu
untersuchende Modell-/Diskretisierungsbias. Das Operatorbudget ist eine
Anforderung an diesen Unterschied, keine nachträglich abzuziehende
Bias-Korrektur. Die Roh-Biasintervalle schließen O_C aus Geometrie- und
Rechenunsicherheit ein und werden mit dem Referenzintervall verglichen.
Daneben steht die vollständige Vergleichsketten-Schranke von höchstens
0.008 im Spurabstand. Kein Beitrag darf zweimal zur selben Schranke addiert
oder als Messrauschen aus der beobachteten Sprinkling-Streuung herausgerechnet
werden. Die volle Kette liefert eine konservative hinreichende Freigabe;
ihre Nichterreichbarkeit allein beweist keinen Genauigkeitsfehler.

## 7. Statistischer Auswertungsvertrag

Primär: unabhängiger Entwicklungspilot, dann feste Ensemblegröße M je
Bestätigungszelle. M wird erst nach dem Pilot und vor neuen Testdaten
festgelegt. Nur Laufzeit/Varianz/Verfügbarkeit dürfen die Planung informieren;
die gewünschte Richtung eines Effekts darf kein Auswahlkriterium sein.
Eine zeituniforme adaptive Variante wäre eine explizite Vertragsänderung.

Gesamtrisiko einer falschen gemeinsamen Aussage: höchstens 0.05 unter
den deklarierten Modellannahmen, aufgeteilt in:

- alpha_G=0.020 für alle gemeinsamen Geometrieregionen der Kampagne;
- alpha_E=0.025 für die gemeinsame Ensembleauswertung;
- alpha_A=0.005 für die Verfügbarkeitsaussagen.

Für J Bestätigungszellen mit M_j Versuchen wird alpha_G über alle geplanten
Geometrieregionen verteilt, etwa alpha_G / sum_j M_j. Eine Region muss
gemeinsam alle innerhalb eines Versuchs benötigten Größen abdecken.
Die v0.5-Grenze 2^30 exp(-24) pro Beobachtung passt nicht automatisch in
dieses Budget. Bekannte Referenzgeometrie benötigt keinen statistischen
Geometrieschätzer; unbenutztes alpha wird nicht nachträglich umverteilt.

Ein konservativer, vollständig spezifizierter Fallback ist feste-M-
Hoeffding-Auswertung für begrenzte Größen. Je Zelle werden acht Größen
gleichzeitig eingeschlossen: w0,w1,C_det, ihre drei Quadrate sowie
Re R01 und Im R01. Alle haben Wertebereichsbreite höchstens 1.
Für K=8J gilt für jede Zelle

    h_j = sqrt(log(2K/alpha_E)/(2 M_j)).

Die Vereinigungsabschätzung liefert simultane Intervalle, ohne unabhängige
Observablen innerhalb einer Realisierung vorauszusetzen. Unsichere numerische
Eingaben werden durch ihre Einschließungen [l_i,u_i] weitergegeben:
[mean(l)-h, mean(u)+h], mit dem bekannten Wertebereich geschnitten.
Die Geometrieüberdeckung ist ein separates gemeinsames Ereignis.

Varianzen folgen aus E[X^2]-(E[X])^2 unter Intervallrechnung. Die Halbbreite
eines Mittelwertintervalls ist keine Schranke der Realisierungsstreuung.
Primäre Wahrscheinlichkeiten werden direkt aus dem Zustand berechnet;
zusätzliche simulierte Mess-Shots sind ausgeschaltet. Spätere Shot-Simulation
benötigt eigene Streams und eine bedingte Varianzzerlegung.

Der Hoeffding-Fallback kann sehr teuer sein. Eine engere begrenzte
empirische-Bernstein-Methode darf vor dem Freeze ersetzt werden, muss aber
mit Formel, Implementierung und Überdeckungsnachweis hinterlegt sein.
Pilot-M=16 oder M=100 ist ausdrücklich kein Akzeptanzkriterium.

**Kein Survivorship-Bias:** Alle Versuche behalten ihren Platz im Nenner.
Scheitert eine numerische Berechnung bei weiterhin wohldefiniertem physischem
Ziel, wird die volle zulässige Zielmenge weitergegeben: z.B. [0,1] für w/C
und [-1/2,1/2] für Re/Im R01. Ist das zugrunde gelegte Modell selbst nicht
definiert oder sind seine Voraussetzungen verletzt, lautet der Kampagnenstatus
MODEL_HOLD; das lässt sich nicht durch ein künstliches Intervall reparieren.
Statistiken nur für G2-bestandene Fälle sind zusätzlich erlaubt, aber als
bedingt gekennzeichnet und niemals Ersatz der Primäranalyse.

Für jede Zelle wird aus allen M Versuchen eine einseitige exakte
Clopper-Pearson-Untergrenze mit alpha_A/J berechnet. Ziel: mindestens 0.90
Verfügbarkeit vollständiger G1/G2/G3-Nachweise. Verfügbarkeit ist eine
eigene Anforderung; sie ersetzt kein Genauigkeitskriterium.

## 8. Entscheidungen und Skalierungsdiagnosen

Für jede vorab deklarierte Bestätigungszelle werden Biasintervalle relativ
zur eingeschlossenen Referenz gebildet. Ein numerisches Genauigkeits-PASS
erfordert gleichzeitig:

1. alle Modell-/Operatorvoraussetzungen und der Evidence-Prüfer bestehen;
2. Biasintervalle w0,w1 vollständig in [-0.010,+0.010], C_det in [-0.020,+0.020];
3. obere Schranke der Sprinkling-Standardabweichung <=0.010 für w0,w1
   und <=0.020 für C_det;
4. statistische Halbbreite <=0.002 und Verfügbarkeitsuntergrenze >=0.90;
5. ein vollständiger G3-Nachweis der Methode und keine nachträgliche Zellenauswahl.

Punkt 5 betrifft die Fehlerabschätzung der Methode. Einzelne numerisch
unverfügbare Realisierungen bleiben gemäß Abschnitt 7 mit voller Zielspanne
enthalten; ihre Unsicherheit muss in den übrigen Kriterien mitgetragen werden.

Die feste Behauptungsmenge (welche Dichten/Skalen sollen bestehen) ist ein
Freeze-Blocker. Niedrige Diagnosezellen müssen nicht dieselbe Genauigkeit
erreichen, dürfen aber nicht nach Einsicht in Testdaten umklassifiziert werden.
Liegt ein Biasintervall vollständig außerhalb seiner Toleranz oder die
Streuungsuntergrenze darüber: FAIL_TOLERANCE im deklarierten Modell.
Überlappende oder zu breite Intervalle: INCONCLUSIVE. Fehlende Methode,
Nachweise oder Modellvoraussetzungen: HOLD. Kein Nichtverwerfen von
Bias=0 wird als Äquivalenznachweis ausgegeben.

Skalierungsfits sind sekundär. Kandidaten: a nu^-p; a nu^-p+b;
gegebenenfalls theoretisch begründete logarithmische Korrektur. Mindestens
sechs Stufen und Faktor 32 in nu sind Voraussetzung für einen modellbasierten
Plateauvergleich in diesem Entwurf. Andernfalls nur tabellarische Werte.
Vorzeichenwechsel, heteroskedastische Unsicherheit und absichtlich gekoppelte
Dichtesamples werden in der Auswertung berücksichtigt. Die Primär-Ensembles
verschiedener Dichten sind unabhängig. Zusatzkontrollen mit gemeinsamen
Punkten werden als gekoppelt ausgewiesen. Keine log(abs(Bias))-Regression
ohne explizites Messmodell. Ein endlicher Scan beweist kein asymptotisches
Plateau und keinen Natur-Diskretheitseffekt.

## 9. Zufall, Kontrollen und Datenintegrität

NumPy 2.3.5, explizit PCG64DXSM, SeedSequence mit ganzzahligen IDs:

    [phase_id, scenario_id, density_id, realization_id, role_id, master_seed].

Keine Floats und kein Python-hash als IDs. Masterseed wird mit der jeweiligen
Phase fixiert; der Bestätigungs-Masterseed bleibt bis zum Freeze unbenutzt.
Phase und Rolle haben disjunkte IDs. Skalar/Dirac verwenden dieselbe gespeicherte
Geometrie, nicht getrennte, nur gleich benannte Sprinklings. Paarungen und
alle Zufallszwecke werden im Datenregister festgehalten. BitGenerator,
Versions-/Buildangaben, Quelldigests und die Rohwolken gehören zur Provenienz.
SeedSequence ersetzt weder mathematische Unabhängigkeitsannahmen noch
RNG-Regressionstests.

Pflichtkontrollen: Nullmischung, gleiche Massen, exakte Kontinuumsdaten,
höhere Löserpräzision, Umnummerierung, gemeinsam transformierter Lorentzfall,
Randvergrößerung bei gleichbleibender innerer Versuchsanordnung, bekannte
fehlerhafte Vorzeichen/Spinzuordnung, und identische Diagonalen mit
verschiedenen Offdiagonalen. Entwicklungs-, Methodenprüf- und
Bestätigungsdaten werden nicht wiederverwendet.

## 10. Darstellung, Freeze und Folgearbeit

Vier Ansichten: Kausalstruktur, Detektions-/Ausbreitungsgewicht, bedingte
Flavorzusammensetzung, Phase/Kohärenz. Ein zusätzlicher sichtbarer Status
zeigt Unsicherheit und HOLD. Ein fehlendes Zertifikat ist kein dunkles Pixel.
RGB wird erst für einen späteren Dreiflavorvertrag eingesetzt; zwei Flavor
werden nicht durch einen erfundenen dritten Kanal ergänzt. Vollständige
komplexe Zustände/Dichtematrizen bleiben Datenquelle. BD-Schichten sind
Intervallkardinalitätsklassen, keine Zeitframes. Referenz-t ist ausschließlich
eine deklarierte Diagnosekoordinate.

Ein Freeze ist erst zulässig, wenn alle offenen Entscheidungen in
`contract.json` aufgelöst, ihre Quellen/Evidence verifiziert, Dichtestufen,
M, Risikozuordnung und Gesamtressourcen festgelegt sind. Das Paket wird vor
Benutzung der Bestätigungsseeds gehasht und veröffentlicht. Ein Hash dieses
Entwurfs ist weder dieser spätere Freeze noch eine externe Präregistrierung.
`check_contract.py --require-frozen` muss den jetzigen Stand zurückweisen.

**Nächster Schritt:** skalarer Entwicklungspilot gemäß Abschnitt 5.
Keine automatische Freigabe von G2/G3 und keine Änderung früherer HOLDs.
