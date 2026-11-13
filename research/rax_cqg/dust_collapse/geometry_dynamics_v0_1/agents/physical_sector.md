# Physikalischer Sektor: regulärer Quellenzweig und Grenze der Quantisierung

Stand: 13. November 2026. Ausgangspunkt ist die veröffentlichte kohärente Endrandmessung v0.1 (Main `f5ee44d7cb4dc1f924eee580f1eaf0cfcb4a5bc6`). Die folgenden Resultate sind zusätzliche analytische Prüfungen, keine fertig hergeleitete physikalische Geometriedynamik.

**Ergebnis:** Der vom Quellenagenten vorgeschlagene gepufferte Kettenzweig beseitigt ein konkretes bisheriges Hindernis: seine inneren Staubgleichungen besitzen einen regulären positiven stationären Punkt und lokal einen stabilen Lösungszweig. Ein reguläres klassisches Konditionierungsmaß ist dadurch mathematisch möglich. Die ursprüngliche kompakte Dichteintegration wird dadurch weiterhin nicht zu einer physikalischen Constraint-Projektion. Bei zehn Elementen ist auch der zusätzliche masslose Skalarblock nichtdegeneriert; erstmals ist für diesen neuen Randvertrag ein gewöhnlicher lokaler stationärer-Phasenbeitrag der gemeinsamen Materiewirkung zugänglich. Der aktuelle Hauptanschluss darunter erweitert diesen Fortschritt auf zwei Ordnungen bei identischem Kragen.

## Aktueller Hauptanschluss: zwei reguläre N11-Ordnungen mit demselben Kragen

Die gemeinsame Weiterentwicklung geht inzwischen über den zuerst untersuchten festen Kettenzweig hinaus. Sie vergleicht zwei transitiv abgeschlossene Ordnungen auf elf Elementen, mit demselben äußeren Kragen B={0,1,2,3,7,8,9,10}, denselben äußeren Uhren \(T_j=\Delta(j-5)\), denselben äußeren Dichten \(r_j=\rho\), und I={4,5,6}. Die zweite Ordnung entfernt aus der Kette genau (4,5) und (5,6), behält aber (4,6). Damit ist 5 zu 4 und 6 unvergleichbar. Die induzierte äußere Ordnung bleibt gleich.

In u-Koordinaten \(T=\Delta(u-5)\) sind die inneren Lösungen

| Fall | Innere u | Innere r | Wirkung auf stationären Feldern |
|---|---|---|---|
| Kette | (4,5,6) | (rho,rho,rho) | 10 − 151 rho / 38 |
| Zweite Ordnung | (4,4,5) | (2 rho,rho,rho) | 18 − 105 rho / 38 |

Für \(0<\rho<1/2\) liegen alle Dichten im ursprünglichen positiven Dichtesupport; die Uhren sind auf allen vorhandenen kausalen Relationen strikt geordnet. Die gleichen Werte an 4 und 5 im zweiten Fall betreffen unvergleichbare Punkte. Beide inneren Staub-Hesseformen besitzen

\[
\det H_d=-19^{-6},\qquad
\det(\partial C_I/\partial u_I)=(-2/19)^3.
\]

Die lokale Coarea-Gewichtung der Uhrgleichungen ist somit in u-Koordinaten für beide Sättel endlich und gleich \(19^3/8\). Diese Regularität wurde in meinem eigenen Code direkt aus allen Intervallkardinalitäten und der vollständigen Wirkung rekonstruiert. Sie übernimmt weder eine vorausgesetzte Lösung noch die Koeffizientenliste des anderen Rechners. Der neue Vergleich beseitigt damit den alten Einwand, dass unterschiedliche Ordnungen lediglich unter unvereinbaren frei gewählten Quellenzuständen geprüft werden.

**Die relative stationäre Wirkung ist quellenabhängig:**

\[
S_1-S_0=8+\frac{23}{19}\rho.
\]

Dies ist eine exakte klassische Wirkungsantwort zweier zulässiger konditionierter Sättel. Sie ist noch keine geometrische Übergangswahrscheinlichkeit und kein Beweis ihrer Dominanz im vollständigen Integral.

### Singulärer innerer Skalarblock, aber endliche gemeinsame Randpaarung

Im zweiten Fall hat der innere Skalarblock eine Nullrichtung q5. Diese ist jedoch an den äußeren Rand gekoppelt. Sei L die volle reelle gewichtete Laplacematrix aus der Skalarwirkung \(S_\phi=-\beta q^T Lq/4\). Für beide Fälle gilt exakt

\[
\operatorname{rang}L_{:,I}=3.
\]

Beim zweiten Fall ist \(\ker L_{II}=\operatorname{span}(0,1,0)\), aber \(L_{BI}(0,1,0)^T\ne0\). Eine zuerst ausgeführte innere q5-Integration ist deshalb distributionell; sie liefert eine Randbedingung und darf nicht als gewöhnliches isoliertes Gaußintegral behandelt werden.

Paaren wir dagegen mit denselben festen Gauß-Testpaketen \(\exp(-\sum_{b\in B}q_b^2/2)\) am äußeren Rand und regulieren nur die inneren Variablen mit \(\exp(-\varepsilon\sum_{i\in I}q_i^2/2)\), dann ist die gemeinsame Matrix

\[
Q_\varepsilon=E_B+\varepsilon E_I+i\beta L/2.
\]

Für \(\varepsilon>0\) ist der Gaußwert absolut definiert. Auch \(Q_0\) ist invertibel: Aus \(Q_0x=0\) folgt durch den Realteil von \(x^*Q_0x\) zunächst \(x_B=0\), danach wegen \(L_{:,I}x_I=0\) und vollem Spaltenrang auch \(x_I=0\). Somit besitzt der skalare Gaußwert einen endlichen, nichtverschwindenden Abel-Grenzwert. Die Quadratwurzel des Determinantenfaktors wird entlang \(\varepsilon>0\) analytisch fortgesetzt; die Hauptwurzel der isolierten Enddeterminante darf nicht ohne Phasenprüfung eingesetzt werden.

Damit ist eine **gemeinsame testfunktionelle Skalarpaarung** für beide Ordnungen möglich, obwohl der zweite innere Skalarhessian singulär ist. Das ist keine positive physikalische Norm: der Gaußwert ist eine komplexe Amplitude. Die Randpakete, das Historiensummenmaß, die physische Quellenpräparation und die Observable-Paarung müssen weiterhin begründet werden. Ebenso wird aus \(C_j=0\) kein erstklassiger Eichconstraint. Die Details der Coarea- und Normabgrenzung in den folgenden Abschnitten gelten unverändert.

Der gemeinsame N11-Vertrag erweitert die äußere Uhrspanne gegenüber dem alten Sechshistorienpiloten. Die separat konstruierte nichtaffine N10-Quelle des Quellenagenten bleibt dagegen vollständig in \([-1,1]\), hat einen regulären Staub-Jacobi und einen invertiblen Skalarblock. Sie belegt, dass die lokale Quellenregularität keine notwendige Uhrboxerweiterung verlangt; sie ist nicht derselbe Zwei-Ordnungen-Vergleich.

**Entscheidung:** Der zulässige Fortschritt ist ein *gemeinsamer klassisch stationärer Zwei-Ordnungen-Vergleich mit quellenabhängiger relativer Wirkung und wohldefinierter skalarer Testpaarung*. Nicht hergeleitet sind physikalische Gewichte/Skalarprodukte, ein vollständiger Übergangskern, eine Zustandswahrscheinlichkeit oder vierdimensionale Geometriedynamik. Die weiteren Abschnitte dokumentieren die konstruktive Zwischenstufe und die verbleibenden Quantisierungsbedingungen.

## 1. Ausgangsproblem präzise erhalten

Die ursprüngliche Wirkung lautet im dimensionslosen Stand

\[
S_C=\kappa F_4(C)-\frac12\sum_jr_j-
\frac\beta4\sum_{i\prec j}b(k_{ij})\{r_j(T_j-T_i)^2+(q_j-q_i)^2\},
\quad \beta=4/\sqrt6.
\]

Die Dichten besitzen das deklarierte Atom-plus-Kontinuum-Maß
\(d\nu=\tfrac12\delta_0+\tfrac12 1_{(0,1)}dr\). Positive innere Dichtevariation ergibt die Eulerbedingungen

\[
C_j=1+\frac\beta2\sum_{i\prec j}b(k_{ij})(T_j-T_i)^2=0.
\]

Diese Gleichungen sind nicht schon erstklassige kanonische Eichconstraints. Auf der alten Anfangsantichain bzw. im späteren Sechshistorienpiloten galt an den problematischen ersten positiven Quellenzeilen \(C_j\ge1\). Eine universelle Multiplikationsconstraint-Deutung lieferte dort nur den trivialen physikalischen Raum. Das neuere klassenblinde Instrument definiert positive Effekte auf dem eigens festgelegten zweidimensionalen Präparationsraum; es leitet weder dessen physikalische Norm noch eine gravitative Constraintpaarung her.

Der Quellenagent ersetzt nun ausdrücklich die dünne Vergangenheit durch einen Kragen mit vier Schichten und hält auch vier Zukunftsschichten fest. Die lokale Wirkung bleibt gleich. Randgeometrie, Randpräparation und gegebenenfalls Uhrsupport ändern sich. Dies ist ein neuer Testvertrag, keine rückwirkende Aufwertung der sechs bisherigen Historien.

## 2. Exakte Regularität des gepufferten affinen Kettenzweigs

Sei \(N=m+8\ge9\), die Ordnung eine Kette und
\(I=\{4,\ldots,N-5\}\) die Menge der \(m\) inneren Elemente. Für Abstände \(d=1,2,3,4\) gilt
\(b_d=(1,-9,16,-8)\); weitere Abstände tragen null bei. Die Identitäten sind

\[
\sum_db_d=0,\qquad \sum_ddb_d=-1,\qquad \sum_dd^2b_d=-19.
\]

Setze

\[
T_j=\Delta\big(j-(N-1)/2\big),\qquad
\Delta^2=\frac2{19\beta},\qquad r_j=\rho\in(0,1),\qquad q_j=0.
\]

Die Kragenwerte sind fest. Alle inneren Dichte-, Uhr- und Skalargleichungen verschwinden. Die Uhrgleichung muss aus der ganzen Wirkung abgeleitet werden: Beiträge späterer aktiver Dichten sind wesentlich.

Betrachte zuerst die \(m\times m\)-Matrix
\(A_{jk}=\partial C_j/\partial T_k\), \(j,k\in I\). Aufgrund der kausalen Abhängigkeit ist sie untere Dreiecksmatrix und auf dem affinen Zweig

\[
A_{jj}=\beta\Delta\sum_ddb_d=-\beta\Delta\ne0,
\qquad \det A=(-\beta\Delta)^m.
\]

Für den vollständigen inneren **Staubblock** mit Variablen \((T_I,r_I)\) ergibt sich die Hessianstruktur

\[
H_d=\begin{pmatrix}H_{TT}&-A^T/2\\-A/2&0\end{pmatrix},
\qquad
\det H_d=(-1)^m\frac{(\det A)^2}{4^m}\ne0.
\]

Der Block besitzt durch Kongruenz genau \(m\) positive und \(m\) negative Richtungen. Einfache Begründung: Bei invertiblem gemischtem Block kann der symmetrische \(TT\)-Block durch eine Dreieckskongruenz eliminiert werden; der verbleibende reine Kreuzblock hat die angegebene Trägheit. Damit gibt es an diesem Sattel keine infinitesimale **innere** Hessian-Nullrichtung bei fixiertem Kragen. Das ist keine Aussage gegen globale Symmetrien mit mitbewegten Randdaten. Die starre Uhrverschiebung etwa hat Randkomponenten.

Der implizite Funktionensatz liefert um den Sattel eine eindeutige glatte innere Lösung als Funktion kleiner Randdatenänderungen. Die strikten Dichte- und Ordnungsungleichungen bleiben in einer genügend kleinen Umgebung erhalten. Eine konkrete maximale Umgebung oder Toleranz wird hier nicht behauptet. Diese Aussage ist stärker als ein einzelner feinabgestimmter Nullstellenzeuge; sie bleibt eine Aussage über das konditionierte Randproblem auf fester Geometrie.

Der affine Zweig liegt für \(N\ge9\) **nicht vollständig in der bisherigen Uhrbox \([-1,1]\)**. Das folgt aus
\(\max |T_j|^2=(N-1)^2/(38\beta)>1\). Der Quellenagent zertifiziert daneben nichtaffine N=9- und N=10-Zeugen in der ursprünglichen Box; N=10 besitzt zusätzlich einen invertiblen Skalarblock. Diese Fälle verwenden eigene Randpräparationen und werden im Quellenbericht separat behandelt. Das Uhrfenster darf nicht stillschweigend erweitert werden.

## 3. Zusätzlicher Skalar: weshalb N=9 noch nicht genügt

Die Staub-Hessianregularität ist nicht automatisch die Regularität der gemeinsamen Wirkung. Der zusätzliche Skalar ist von \(r,T\) entkoppelt, hängt aber von derselben Ordnung ab. Auf den gepufferten Innenpunkten hat sein Hessian

\[
(H_\phi)_{jj}=0,\qquad (H_\phi)_{jk}=\frac\beta2b_{|j-k|}\quad(1\le|j-k|\le4).
\]

Für einen einzigen Innenpunkt (N=9) ist dieser Block null. Bei festem skalarem Nullrand bleibt ein flacher innerer Skalarmodus. Man darf daher für diesen Fall keinen vollständig nichtdegenerierten gemeinsamen Sattel behaupten. Der vorhandene distributionelle Randvertrag müsste den Nullmodus behandeln.

Bei zwei Innenpunkten (N=10) gilt hingegen

\[
H_\phi=\frac\beta2\begin{pmatrix}0&1\\1&0\end{pmatrix},
\qquad \det H_\phi=-\beta^2/4\ne0.
\]

Hier ist der gesamte innere Materiehessian in \((T_I,r_I,q_I)\) invertibel. Der implizite Funktionensatz gilt damit für das gemeinsame lokale Materieproblem, auch bei kleinen Änderungen der vorbereiteten Skalar-Randwerte. Das Gravitationsstück ist auf der festen Kette konstant; es erzeugt durch diese Rechnung keine Geometrievariation.

`checks/physical_sector/check.py` rekonstruiert die gesamte endliche Wirkung und prüft die Gleichungen, Dreiecksstruktur, Kreuzblöcke und Determinanten exakt mit SymPy für N=9,10,11,12. Für skalierte Uhren \(x=T/\Delta\) lauten die Staubdeterminanten \((-1)^m/19^{2m}\). Die Skalarblöcke sind für N=10,11,12 invertibel. Diese endlichen Prüfungen stützen die symbolische Herleitung; ein allgemeiner Satz für sämtliche N oder sämtliche Ordnungen wird nicht behauptet.

## 4. Reguläre Coarea-Paarung: verfügbar, aber noch kein physikalisches Skalarprodukt

Weil \(A\) invertibel ist, ist auf einem genügend kleinen ausgewählten Zweig die klassisch konditionierte Form

\[
B_{C,b}(f,g)=\int dT_I\,\overline{f(T_I)}g(T_I)
\prod_{j\in I}\delta(C_j(T_I;b))
=\frac{\overline{f(T_*(b))}g(T_*(b))}{|\det A(T_*(b);b)|}
\]

endlich, positiv und nichttrivial. Bei Lebesgue-Maß für die inneren Uhren ist der affine Gewichtsfaktor \((\beta\Delta)^{-m}\); normierte Uhrmaße fügen ihre deklarierten Vorfaktoren hinzu. Im Gegensatz zum früheren Doppelwurzelzeugen ist keine divergent reskalierte Deltafolge erforderlich. Der Ausdruck ist lokal: mehrere entfernte Lösungszweige würden gesondert eingehen.

**Dies konstruiert eine bedingte klassische Präparationspaarung, nicht das physikalische CST-Skalarprodukt.** Insbesondere:

- Die verwendeten Deltafunktionen folgen nicht aus der ursprünglichen Atom-plus-kompakten Dichteintegration. Deren exakter Fourierfaktor ist glatt und hat Atom- und Endpunktterme.
- Das positiv gewählte Kragenmaß, Zweiggewicht und eine etwaige Normierung werden hierdurch nicht bestimmt.
- \(C_j=0\) allein ist noch nicht die ganze Stationarität; die Uhrgleichungen bestimmen zusätzlich die inneren Dichten. Eine Deltaform auf allen inneren Eulerbedingungen wäre ebenfalls eine klassische Sattelkonditionierung, keine automatisch begründete Quantisierung.
- Ein Darstellungsraum einer erstklassigen Constraintalgebra, eine zugehörige Gruppe und ihr physikalischer Observablebereich wurden nicht hergeleitet. Daher ist RAQ/Group Averaging noch nicht anwendbar als behauptete Schlussfolgerung.

Die sinnvolle nächste Quantisierungsfrage lautet nun konkreter: Erzeugt die volle diskrete Legendreanalyse der **variablen Randdaten samt vollständigem Schnittgedächtnis** einen physikalischen Vor-/Nachzustandsraum und einen damit verträglichen Propagator? Lokale Innenregularität liefert dafür einen brauchbaren Prüfstein, aber nicht bereits die Antwort.

## 5. Neuer lokaler Amplitudenanschluss aus derselben Wirkung

Für den N=10-Sattel kann man einen klar begrenzten stationären-Phasen-Test formulieren. Füge einen glatten kompakten Lokalisierer hinzu, der nahe diesem positiven inneren Sattel eins ist, und betrachte die diagnostische Familie \(e^{iS/\epsilon}\), \(\epsilon\downarrow0\). Dies skaliert die **ganze** Wirkung und ist keine neue Interpretation von kappa als Uhr oder Gravitationseinsteller. Der ursprüngliche endliche \(\epsilon=1\)-Pilot wird dadurch nicht neu berechnet.

In den Variablen \((x_I,r_I,q_I)\), \(x=T/\Delta\), besitzt N=10 sechs innere Integrationsrichtungen und Signatur null. Für die unveränderten lokalen kontinuierlichen Innenfaktoren \(dT/2\), \(dr/2\), \(dq\), mit einem Lokalisiererwert eins, gilt

\[
I_{\rm loc}(\epsilon)=e^{iS_*/\epsilon}(2\pi\epsilon)^3
\frac{57}{32}\,[1+O(\epsilon)].
\]

Denn \(\sqrt{|\det H|}=\beta/(2\,19^2)\) in den skalierten Koordinaten und der Maßfaktor ist \((\Delta/4)^2\); ihr Quotient ist exakt \(57/32\). Der Hessian ist nicht positiv, aber die je drei positiven und negativen Richtungen ergeben keinen zusätzlichen Maslov-Phasenfaktor. Standardmäßige glatte stationäre-Phasenbedingungen werden durch die lokale Auswahl hergestellt.

Das ist eine **lokale asymptotische Aussage**, keine Fehlergrenze für \(\epsilon=1\), keine gesamte Atom-plus-Kontinuum-Amplitude und keine Historiensumme. Atomstrata, andere Sättel, Ränder und geometrische Gewichtung bleiben außerhalb dieses Tests. Ein globaler physischer Propagator oder eine unitäre Norm folgt daraus nicht. Der Wert wird symbolisch aus der Hessianstruktur geprüft; es wurde kein Integrationslauf durchgeführt.

## 6. Zwei irreführende Normreparaturen bleiben ausgeschlossen bzw. unbestimmt

### Beschränkte Normreparatur eines kompakten Uhrkernels

Betrachte ausschließlich einen ausdrücklich endlichen, kompakten Uhr-/Dichtepatch und einen Staubkernel oder einen Kernel **nach festen Skalar-Testpaarungen**, dessen Betrag dort gleichmäßig beschränkt ist. Das trifft nicht automatisch auf die distributionelle volle Skalaramplitude auf \(\mathbb R^n\) zu. Der entsprechende Integralkernel liegt auf dem endlichen Randmaß in \(L^2\); sein Operator K ist Hilbert-Schmidt und damit kompakt.

Auf einem unendlichdimensionalen geschlossenen Sektor kann K unter keiner beschränkt invertierbaren äquivalenten positiven Normänderung zu einer Isometrie werden: Für positive beschränkte, beschränkt invertierbare \(G_{in},G_{out}\) wäre
\(\widetilde K=G_{out}^{1/2}KG_{in}^{-1/2}\) weiterhin kompakt. Eine Isometrie ist auf einem unendlichdimensionalen Hilbertraum nicht kompakt, da sie eine orthonormale Folge auf eine Folge mit konstantem Paarabstand abbildet.

Dieser Satz schließt keine finite physikalische Reduktion, keine singuläre Rigging Map, kein nichtäquivalentes unbeschränktes Skalarprodukt, keine nichtunitäre Grobvergröberung und keinen anderen globalen Kern aus. Er verhindert lediglich, eine glatte endliche Hilfsamplitude durch eine harmlose Normumbenennung als geschlossene unendlichdimensionale unitäre Dynamik auszugeben.

### Endliche frei gewählte Metriken bestimmen keine Physik

Für jede injektive endliche Matrix A und jede positive Eingangsnorm G kann man eine passende Ausgangsnorm erzeugen. Mit der Linksinversen \(A^+=(A^\dagger A)^{-1}A^\dagger\) und dem orthogonalen Projektor \(P=I-AA^+\) gilt beispielsweise

\[
G_{out}=(A^+)^\dagger G A^+ +cP,\qquad c>0,
\quad A^\dagger G_{out}A=G.
\]

Die Wahl ist hochgradig nicht eindeutig. Unser Prüfcode kontrolliert zwei verschiedene positive Lösungen exakt an einer festen 3×2-Matrix. Ein solcher algebraischer Erfolg wäre allein kein aus der Wirkung bestimmtes physikalisches Skalarprodukt. Observable-Adjungiertheit, derselbe Randvertrag und Komposition über unterschiedliche Schnitte sind zusätzliche Bedingungen.

## 7. Was damit wissenschaftlich gewonnen und noch offen ist

| Prüffrage | Ergebnis |
|---|---|
| Regulärer positiver innerer Staubzweig bei hinreichendem Kragen | PASS für den deklarierten Kettenvertrag |
| Vollständiger Materiesattel ohne Skalar-Nullmode | PASS ab N=10 in den geprüften Fällen; N=9 FAIL für Nichtdegeneriertheit |
| Glatte lokale Fortsetzung unter Randperturbationen | Folgt lokal aus invertiblem Hessian; keine quantifizierte große Umgebung |
| Endliche positive Coarea-Bedingung | Mathematisch möglich; zusätzliche klassische Konditionierung |
| Lokaler asymptotischer Beitrag aus derselben Wirkung | PASS unter ausdrücklich eingeführter glatter Sattellokalisierung |
| Erstklassige gravitative Constraints oder ausgewählte RAQ-Paarung | NOT_DERIVED |
| Physikalisch ausgezeichnetes positives Skalarprodukt | NOT_DERIVED |
| Zwei-Ordnungen-Wirkungsantwort unter gemeinsamem Kragen | PASS: relative stationäre Wirkung 8+23 rho/19; keine Wahrscheinlichkeit |
| Physikalische Geometriedynamik | HOLD_NOT_DERIVED |

Der vom Geometrieagenten definierte intrinsische Downset-Verlauf ist auf einer festen N-Kette stets min(k+1,N). Allein die Quellenregularität auf einer Kette hätte deshalb noch keine Geometrieantwort erzeugt. Der oben beschriebene N11-Vergleich stellt nun zwei unterschiedliche Ordnungen unter denselben zulässigen äußeren Quellen- und Randdaten bereit. Offen bleibt die abgeleitete physische Paarung, die ihren Wirkungsvergleich in eine geometrische Quantendynamik überführen würde.

## Literatur und Provenienz

Der methodische Literaturanschluss wurde am 13. November 2026 über Primärquellen nachgeprüft:

1. B. Dittrich und P. A. Höhn, *Constraint analysis for variational discrete systems*, https://arxiv.org/abs/1303.4294. Die Arbeit unterscheidet Vor-/Nachconstraints, Konsistenz und Symmetrierichtungen in variationalen diskreten Systemen. Sie begründet keine konkrete CST-Paarung für dieses Paket.
2. D. Giulini, *Group Averaging and Refined Algebraic Quantization*, https://arxiv.org/abs/gr-qc/0003040. Group Averaging betrifft eine vorhandene erstklassige Constraintstruktur; bloße Lagrangelinearität in einer Dichte liefert diese nicht.
3. P. A. Höhn, *Quantization of systems with temporally varying discretization I: Evolving Hilbert spaces*, https://arxiv.org/abs/1401.6062; DOI https://doi.org/10.1063/1.4890558. Unterschiedliche diskrete Schritte können unterschiedliche physikalische Zustandsräume und nichtunitäre Projektionen haben. Daher ist die Unitätsobstruktion in Abschnitt 6 ausdrücklich eng begrenzt.

Die neuen algebraischen Aussagen, Coarea-Anwendung und Kompaktheitsargumente oben sind eigene Ableitungen dieses Prüfauftrags. Ältere genaue Wirkungs- und Constraintspezifikationen stehen in `stage1/DERIVATION.md`, `execution_v0_1/reports/hilbert_execution.md` und `causal_order_execution_v0_1/contracts/pilot.json`. Für das vorliegende Paket sind die zugrunde gelegten Formeln im ausführbaren `checks/physical_sector/check.py` enthalten. Keine fremde Quantisierung wird als ausgeführte CST-Herleitung übernommen.
