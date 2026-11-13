# Unabhängiger Audit des physikalischen Rand- und Auslesevertrags

Stand: 13. November 2026. Der Audit rekonstruiert die N=11-Intervallkoeffizienten selbst; er importiert keine Rechnermodule der anderen Agenten. `checks/independent_audit/check.py` prüft Quelle, Legendreabbildungen, nichtlinearen Variantenpfad und gemeinsame skalare Reduktion exakt mit rationaler Algebra. `contract_checks.py` prüft unabhängig die kompakten Ward-Identitäten, Paketnormen, Historienzähler und Gaußpointer. `reduced_kernel.py` prüft die konkrete skalare Rigging-Normierung einschließlich des distributionellen Variantenkernels. `coherent_gaussian.py` kontrolliert die phasenfesten skalaren Ausgänge und ihre kohärente q7-Auslese. Alle vier Rechner bestehen. Es wurden keine neuen großen Quadraturen ausgeführt.

## Ergebnis und Reichweite

Der bisherige relative Effekt des gemeinsam veränderten Randparameters ist im geprüften Dirichletvertrag vollständig eine Zukunftsrandantwort. Gleichzeitig existiert eine konkrete gemeinsame **bedingte skalare Reduktion auf drei kanonische Paare**, auf der beide Geometrieabbildungen unitär quantisiert werden können. Diese positive Konstruktion wird durch den zuvor gefundenen Konflikt zweier starker Zwangsbedingungen nicht ausgeschlossen.

Der damit gewählte Quotienten- und Normvertrag wird jedoch nicht eindeutig durch die ursprüngliche Wirkung und das kompakte Atom-/Intervallmaß ausgewählt. Die Rechnung leitet deshalb weder einen eindeutigen physikalischen Gesamtzustandsraum noch einen eindeutigen Historienprior her. Sie zeigt genau, welche Randverträge funktionieren und welche weitergehenden Behauptungen die Daten nicht tragen.

## 1. Einseitige Anfangsdichteantwort

Seien P={0,1,2,3}, I={4,5,6}, F={7,8,9,10}. Die beiden Ordnungen sind die vollständige Kette C0 und C1 mit allein entfernten Relationen (4,5),(5,6), bei behaltenem (4,6). Die unabhängige Rekonstruktion ergibt bei den festgehaltenen affinen äußeren Uhren

\[
(C_0,C_1,C_2,C_3)=(1,20/19,-16/19,128/19),
\qquad \sum_{j\in P}C_j=151/19.
\]

Die Gleichheit gilt für beide Ordnungen und unabhängig von sämtlichen inneren Uhren. Bereits vor der affinen Substitution hängen diese vier C_j ausschließlich von vergangenen Uhren ab. Mit getrennten Dichteparametern folgt daher exakt

\[
W_c(\rho_P,\rho_F)=e^{-i151\rho_P/38}V_c(\rho_F),
\qquad \partial_{\rho_P}\log(W_1/W_0)=0
\]

überall dort, wo der Quotient definiert ist. Äquivalent gilt die Quotientenaussage ohne Logarithmus als gemeinsame Phasenfaktorisierung auch an Nullstellen einzelner Gewichte. Bei festem Historienmaß und fester, quellenunabhängiger Auslese verschwindet dieser gemeinsame Phasenfaktor aus normierten Recordvorhersagen. Die vorher berechnete relative Ableitung auf der Diagonale ρP=ρF stammt vollständig aus der Änderung des Zukunftskragens.

Dies ist **kein allgemeines Verbot einer Anfangsantwort**. Werden vergangene Uhren mit Wellenpaketen integriert, steht der gemeinsame Faktor innerhalb des Uhrenintegrals und kann die beiden geometrieabhängigen Beiträge unterschiedlich gewichten. Auch ein ausdrücklich quellenabhängiger Detektor wäre ein anderer Vertrag. Die neue einseitige Rechnung ist daher eine Korrektur der Interpretation des geprüften Experiments, kein universeller kausaler No-go-Satz.

## 2. Kompakte Maße, Ward-Identitäten und Randpakete

Die positive Dichtekomponente erfüllt die gewöhnliche Integration durch Teile

\[
\frac12\int_0^1(f'-iCf/2)e^{-irC/2}\,dr
=\frac{f(1)e^{-iC/2}-f(0)}2.
\]

Der zusätzliche Atomwert bei r=0 wird durch diese Formel nicht differenziert. Insbesondere ist das ursprüngliche Dichteintegral keine Zwangsprojektordistribution: Für D(C)=1/2+(1-e^{-iC/2})/(iC) gilt C D(C)=2π bei C=4π. Eine homogene Identität C D=0 ist damit widerlegt.

Beim Uhrenintegral über eine feste Box bleiben Endflächen. Die globale Verschiebungsinvarianz der Wirkung allein entfernt diese Flächen nicht. Als unabhängiges Gegenbeispiel liefert S=−(t−τ)²/2 auf [−3/2,3/2] bei τ=1/4 einen Verschiebungsfluss mit Betragsquadrat 4 sin²(3/8)/9>0.

Die eingeführten positiven Randpakete sind auf dem deklarierten Hilfsmaß korrekt normiert. Für b(u)=(1−u²)³ auf |u|<1 gilt ∫b²du=2048/3003, Var(u)=1/15. Die Dichteamplitude hat Normfaktorquadrat 3003/(1024ε), die Uhramplitude 3003L/(1024η). Dieses kompakte Paket ist C², nicht C∞; das getrennt angegebene Exponential-Bump-Paket ist tatsächlich glatt. Keine dieser Hilfsnormierungen beweist bereits eine physische Randnorm.

Die klassischen vergangenen Dichte-Präconstraints erzeugen Dichtetranslationen. Das Maß (δ0+dr auf (0,1))/2 ist nicht translationsinvariant. Eine Gruppenmittelung oder kanonische Quotientierung auf diesem ursprünglichen Maß benötigt daher einen zusätzlichen Domänen- und Maßvertrag. Vier Nullzeilen in einer Legendreabbildung allein legitimieren keine quantenmechanische Eichvolumenentfernung.

## 3. Skalare Legendreabbildung und enger starker-Constraint-Befund

Aus Sφ=−β qᵀLq/4 folgt H/β=−L/2. Die unabhängig rekonstruierte Matrix mit Zeilen (I,P) und Spalten (I,F) hat für C0 Rang 7 und Determinante −16384β⁷; für C1 hat sie Rang 6. Die Skalarmomenta werden als π=p/β geschrieben. Die primitiven Prä- und Postbedingungen können mit den Vorzeichen

\[
A_-=-128q_0+241q_1+119q_2-232q_3-46\pi_0-32\pi_1-16\pi_2,
\]
\[
A_+=-232q_7+119q_8+241q_9-128q_{10}+16\pi_8+32\pi_9+46\pi_{10}
\]

gewählt werden. Sei M0 die volle symplektische C0-Randabbildung und B=A+∘M0. Die exakte Klammer in den skalierten (q,π)-Koordinaten lautet

\[
\{A_-,B\}_{q,\pi}=-52625/32.
\]

In den ursprünglichen (q,p)-Koordinaten kommt der Faktor 1/β hinzu. Auf einem gemeinsamen kompatiblen CCR-Testbereich kann kein von null verschiedener Vektor gleichzeitig im starken Kern beider Operatoren liegen: Ihr Kommutator ist eine von null verschiedene Konstante.

**Der Schluss ist eng:** Er verbietet diese gleichzeitige starke Kernauswahl. Er verbietet weder einen zweitklassigen klassischen Reduktionsvertrag noch eine Rigging-Sandwichkonstruktion, Quotientenräume, eine größere direkte Summe oder einen anders definierten physikalischen Randraum.

## 4. Positiver Gegenbefund: gemeinsame skalare Reduktion und explizite unitäre Faktoren

Der unabhängige Rechner konstruiert eine gemeinsame Eingangssektion q0=0,A−=0 mit Koordinaten (q1,q2,q3;π1,π2,π3) und eine Ausgangssektion q10=0,A+=0 mit Koordinaten (q7,q8,q9;π7,π8,π9).

Für C1 wird die Randrelation direkt gelöst und der freie Ausgang entlang der Postconstraint-Richtung quotiert. Für C0 wird zunächst auf der A−-Flussbahn der eindeutig bestimmte Vertreter B=0 gewählt. Danach wird M0 angewendet und die Ausgangssektion q10=0 genommen. Die von null verschiedene Klammer macht gerade diese Gaugefixierung regulär. Dies ist eine andere Operation als die verbotene gleichzeitige starke Kernbedingung.

Beide resultierenden verschiedenen 6×6-Matrizen R0,R1 erfüllen exakt RᵀJ6R=J6. Ihre vollständigen rationalen Einträge stehen in `checks/independent_audit/results.json`. Für die oberen linken 3×3-Blöcke A gilt

\[
\det A_0=-68229107961/14253376000,
\qquad \det A_1=3303/135424.
\]

Beide sind invertierbar. Für R=(A B;C D) prüft der Rechner die exakte Faktorisierung

\[
R=
\begin{pmatrix}I&0\\ CA^{-1}&I\end{pmatrix}
\begin{pmatrix}A&0\\0&A^{-\mathsf T}\end{pmatrix}
\begin{pmatrix}I&A^{-1}B\\0&I\end{pmatrix},
\]

wobei CA⁻¹ und A⁻¹B symmetrisch sind. Daraus entsteht auf dem ausdrücklich gewählten L²(R³,dx) ein konkreter unitärer Operator: zuerst ein Impulschirp über die normierte Fouriertransformation, dann die Dilation ψ(x)↦|det A|⁻¹/²ψ(A⁻¹x), zuletzt der Ortschirp exp(iβxᵀCA⁻¹x/2). Der Impulschirp multipliziert in der π-Darstellung mit exp(−iβπᵀA⁻¹Bπ/2). Jeder Faktor erhält die erklärte L²-Norm direkt.

Der B-Block von R1 hat Rang 2 und Determinante null; dies verhindert einen gewöhnlichen vollen Konfigurations-Gaußkern, aber nicht diese unitäre Faktorenkonstruktion. Es wird nirgends B⁻¹ benutzt.

Auch die konkrete Kernelreduktion wurde unabhängig geprüft. In den adaptierten Koordinaten q=Ex+bt haben beide Randtransformationen Jacobi-Betrag 46. Nach den Constraint-Chirps und der Auswahl verschwindenden Gaugeimpulses hat das C0-Sandwich relativ zum unitär normierten reduzierten Kernel das Normquadrat β/[2π(52625/32)]. Der positive Korrekturfaktor ist deshalb

\[
N_{\rm FP}=\sqrt{\frac{2\pi}{\beta}\frac{52625}{32}}.
\]

Die zwei integrierten Gaugekoordinaten besitzen die Hesseform −(1/9)[[7696,4096],[4096,7696]], Determinante 4716800/9 und Signatur −2. Ihr Fresnelfaktor −i muss mit der übrigen Phasenkonvention mitgeführt werden; der positive Normfaktor ersetzt diese Phase nicht.

Für C1 ergibt die direkte Integration des inneren Skalarpaars und der verbleibenden Fourierkoordinate auf der Sektion

\[
K_{1,\rm bare}(y,x)=\frac{8\pi^2}{\beta^2}\delta(\ell(x,y))e^{i\beta\Phi(x,y)},
\]

mit ℓ=8x0−9x1/2+x2/2+y0/2−9y1/2+8y2. Die unabhängige Prüfung von K†K liefert nach einer Deltaelimination und zwei Fourierintegralen den Constraint-Jacobi-Betrag 2116. Der unitäre positive Vorfaktor vor δ(ℓ)e^(iβΦ) ist 92√2 β/(2π), entsprechend der Multiplikation des bloßen Sektionskernels mit 23√2 β³/(4π³). Damit ist die Normierung innerhalb dieses erklärten skalaren Lebesgue-/Riggingvertrags konkret überprüft, nicht nur abstrakt postuliert.

**Was damit konstruiert ist:** Ein gemeinsamer bedingter skalarer Drei-Paar-Vertrag mit zwei explizit normerhaltenden kanonischen Quantisierungen und kontrollierter Kernel-Normierung. **Was damit nicht ausgewählt ist:** Warum der C1-Prä-/Postquotient auch für die reguläre C0-Geometrie gelten soll, warum genau dieser Rigging- und Gruppenmaßvertrag physikalisch gelten soll, die physische Auswahl der relativen Historiengewichte sowie der volle kompakte Uhr-/Dichtevertrag. Der Kernelvergleich macht den gewählten skalaren Vertrag überprüfbar; er leitet seine physikalische Auswahl nicht aus dem ursprünglichen Gesamtmaß ab.

## 5. Uhr-/Dichte-Legendreabbildung und exakter Variantenpfad

Die volle 14×14-Matrix verwendet die sechs inneren Uhr-/Dichtevariablen, acht vergangene kanonische Daten und acht zukünftige Felder. Ihre letzten vier Zeilen sind bereits vor jeder stationären Auswertung identisch null. Auf den geprüften stationären Familien sind die exakten Ränge 10 für C0 und 9 für C1. Die innere 6×6-Hesseform hat für beide Determinante −19⁻⁶.

Bei festgehaltenen Zukunftsdichten ist der relevante 10×10-Minor für C0 gleich 2²⁷ρ⁴/19¹⁰; für C1 bleibt der Rang 9. Die Variantenmehrdeutigkeit ist nicht nur eine lineare Tangentenerscheinung. Mit festen Anfangsdaten und unverändertem Inneren gilt für alle hinreichend kleinen α

\[
u_F=(7,8,9,10)+\alpha(0,8,16,23),
\quad r_F=\rho,
\]

und alle sechs inneren Eulerreste sowie alle acht vergangenen Impulse bleiben exakt gleich. Dagegen

\[
\Delta S=-\alpha\rho(932\alpha+217)/19,
\quad \Delta p_{u_F}=\alpha\rho(232,-119,-241,128)/19.
\]

Auch die vier zukünftigen Dichteimpulsänderungen sind im Rechner exakt geprüft. Kleine α bleiben im offenen zulässigen Uhrbereich. Die ursprünglichen Anfangsdaten bestimmen daher innerhalb dieses Vertrags nicht eindeutig alle zukünftigen Felder. Eine Eichidentifikation dieser verschiedenen Ausgänge wird daraus nicht abgeleitet.

## 6. Historiengewicht und Auslese

Die Historienfamilie exp(−λR(C)) ist invariant und multipliziert sich exakt entlang natürlicher Präfixe, ohne dadurch bereits stochastisch normiert zu sein. Unabhängig bestätigt wurden für C0/C1 die Zähler (R,L,I)=(55,10,0)/(53,11,2), jeweils ein randfixierender Automorphismus und eine beziehungsweise drei natürliche Beschriftungen. Die normalisierte klassische Perkolationsfamilie liefert das Verhältnis p(1−p)² je festem natürlichen Vertreter oder 3p(1−p)² nach Vergessen der natürlichen Beschriftung. Schon p=1/2 und p=3/4 unterscheiden sich. Diese Zählkonventionen dürfen nicht vermischt werden; klassische Wahrscheinlichkeiten sind außerdem nicht automatisch Quantenamplitudengewichte.

Der Gaußpointer ist auf dem deklarierten Hilfsraum korrekt: M_y=(2πσ²)⁻¹/⁴ exp[−(y−gQ)²/(4σ²)] erfüllt ∫dy M_y†M_y=I, und die nichtselektive Kohärenzfunktion ist exp[−g²(Q−Q′)²/(8σ²)]. Die Apparaturparameter und die gemessene Observable sind neue Auslesedaten, nicht aus der Gravitationswirkung gewonnene Zahlen.

Auf dem unreduzierten L²(R⁴)-Vertrag ist ein nichtverschwindender C1-Ausgang mit A+ψ=0 entlang einer nichtkompakten Constraint-Richtung betragskonstant und nicht normierbar. Ein vollständiger Pointer kann die unendliche Norm wegen positiver Tonelli-Integration nicht reparieren. Bei nichtinvarianter Ortsauslese entsteht entlang dieser Richtung eine in y konstante, ebenfalls nicht integrierbare Recorddichte. Bei invarianter Auslese bleibt das unendliche Orbitvolumen in jedem Record erhalten.

Diese Obstruktion gilt für den unreduzierten Vertrag. Auf der oben konstruierten bedingten Drei-Paar-Reduktion kann beispielsweise q7 als gemeinsame gaugeinvariante Ausgangsobservable mit demselben Gaußpointer korrekt gemessen werden. Die aktualisierte Detektorrechnung liefert einen vollständigen erklärten Vertrag: ein normiertes skalares Eingangsgaußpaket, die zwei reduzierten unitären Operatoren V_c, den Hilfsumweltraum L²(μ) des ursprünglichen normierten inneren Uhr-/Dichtemaßes und einen normierten Kontrollzustand |w> mit Gewichten ωc≥0, Σωc=1. Die kontrollierte Multiplikation mit exp(iS_c) und V_c ist unitär. Projektion der Hilfsumwelt und Kontrolle auf denselben Ausgangszustand ergibt

\[
K=\sum_c\omega_c W_c V_c,
\qquad \|K\|\leq\sum_c\omega_c|W_c|\leq1.
\]

Die akzeptierten lokalen Records besitzen Operatoren M_y K. Das orthogonale Ancillakomplement liefert einen vollständigen Failure-Kanal mit Effekt I−K†K; zusammen summieren sich sämtliche Effekte zu I. Ein einzelner Operator √(I−K†K) wäre zwar ebenfalls eine mögliche Vervollständigung, hätte aber im Allgemeinen einen anderen Zustand nach dem Failure-Record. Die Detektorrechnung trennt dies korrekt.

Für das erklärte Eingangspaket mit Kovarianz I6/(2β) sind die Ausgangskovarianzen R_c R_cᵀ/(2β). Die geprüften Formeln ergeben bei g=σ=1 die unterschiedlichen Pointervarianzen ungefähr 21,55928 und 2,41176. Der Betrag der vollen Zweigzustandsüberlappung ist ungefähr 0,00814923; er ist kein frei gewähltes Klassen-γ und kein Pointer-Recordüberlapp. Die Phase wird nicht aus der Kovarianz abgelesen. Diese Zahlen beziehen sich auf den neu erklärten reduzierten Vertrag und sind keine Vorhersagen des unreduzierten ursprünglichen Randintegrals.

Der gemeinsame Anfangsdichte-Phasenfaktor multipliziert auch K insgesamt. Deshalb bleiben in diesem Vertrag sowohl akzeptierte Recordwahrscheinlichkeiten als auch Failure-Wahrscheinlichkeiten bei Variation von ρP und festem ρF exakt unverändert. Eine vollständige Detektornormierung und die Auswahl des physikalisch geltenden Randvertrags bleiben verschiedene Aufgaben.

## 7. Abschließender phasenfester Kohärenzaudit

Die letzten skalaren Ausgänge wurden zusätzlich aus den eigenen rationalen Matrizen und dem eigenen distributionellen Phasenpolynom rekonstruiert. Für C0 wird die geerbte reduzierte Kernelphase −π/4, für C1 die positive reelle Delta-Kernelamplitude verwendet. Die komplexen Gaußwurzeln werden über aufeinanderfolgende Schur-Pivots mit positivem Realteil fortgesetzt; dies ist eine unabhängige Kontrolle der Eigenwert-/Cholesky-Fortsetzung des Skalaragenten und verwendet keine beliebig gewählte Hauptwurzel von det P.

Für ψc(Q)=Nc exp(−QᵀPcQ/2) stimmen beide Präzisionsmatrizen exakt mit den kanonischen Abbildungen überein, und beide Normen bestehen die hochpräzise Kontrolle. Die Überlappung und der komplexe Pointerparameter bei g=σ=1 sind

\[
z=\langle\psi_0|\psi_1\rangle
\simeq0.00311695032117691677+0.00752958276498214751i,
\]
\[
u=1+[(\bar P_0+P_1)^{-1}]_{11}
\simeq1.15596228880048533-0.00632240560461981113i.
\]

Allgemein ersetzt man u durch σ²+g²[(P̄0+P1)⁻¹]11. Die Determinantenlemma-/Woodbury-Rechnung liefert unabhängig die Kreuzrecorddichte

\[
D_{01}(y)=\frac{z}{\sqrt{2\pi u}}e^{-y^2/(2u)},
\quad \int D_{01}\,dy=z,
\quad \int y^2D_{01}\,dy=zu,
\quad \int_{-a}^aD_{01}\,dy=z\,\operatorname{erf}(a/\sqrt{2u}).
\]

Die Wurzel wird auf Re u>0 fortgesetzt. D01 allein ist komplex und keine Wahrscheinlichkeitsdichte; erst die vollständige Summe mit den diagonalen Beiträgen und dem konjugierten Kreuzterm ist der positive akzeptierte Record. Für ac=ωcWc gilt pacc=|a0|²+|a1|²+2Re(ā0a1z). Die geprüfte Varianz- und Binformel verwendet dieselbe Konjugationskonvention und normiert mit pacc.

Für ω0=ω1=1/2 stimmen die unabhängigen Diagnosen mit der Detektorrechnung überein:

| ρF bei festem ρP | pacc | Varianz bei Akzeptanz | P(−1≤y≤1 bei Akzeptanz) |
|---|---:|---:|---:|
| 1/8 | 0,3128994543 | 7,8121158308 | 0,3919028692 |
| 1/4 | 0,2906494475 | 6,7076157488 | 0,4099076347 |

Die 70-stellige skalare Gaußauswertung macht die eingesetzten Float64-Uhrgewichte nicht zu rigorosen Intervallen. Die angezeigten Zahlen sind deshalb numerische Diagnosen des erklärten bedingten Vertrags. Die beobachteten Unterschiede beim bloßen Wechsel von ρP liegen auf dessen Rundungsniveau; die unabhängige algebraische Faktorisierung beweist ihre exakte Abwesenheit.

## Gesamturteil

Die neue Arbeit liefert einen schärferen Anfangs-/Zukunftsrandtest und einen konstruktiven gemeinsamen skalaren Reduktionskandidaten. Die Nullantwort und die starken Constraint-Obstruktionen sind auf ihre erklärten Verträge beschränkt. Die verbleibende Unterbestimmtheit ist konkret: Der ursprüngliche kompakte Uhr-/Dichtevertrag, die gemeinsame Rigging-Auswahl und das Historiengewicht wählen den physikalischen Rand- und Auslesevertrag noch nicht eindeutig aus. Die bedingte Drei-Paar-Konstruktion ist ein echter Fortschritt und keine Herleitung dieser fehlenden Auswahl aus der bisherigen Wirkung.
