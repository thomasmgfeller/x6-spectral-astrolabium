# Physikalische Auslese: konsistente bedingte Instrumente, keine abgeleitete Norm

## Ergebnis und unveränderte Amplitudenkonvention

Aus zwei geprüften endlichen N11-Amplituden lässt sich eine mathematisch konsistente Familie bedingter Interferenzinstrumente konstruieren. Ihre Positivität, Normierung und Failure-Vervollständigung sind explizit prüfbar. **Die Wirkung und die beiden Zahlen bestimmen aber weder die Historiengewichte noch das physische Record-Gramfeld oder das physikalische Rand-Skalarprodukt.** Diese Unterbestimmtheit ist im endlichen Ansatz nachweisbar; sie ist kein allgemeiner Unmöglichkeitssatz für physikalische CST-Dynamik.

Für die aktuelle Fortsetzung gilt genau

\[
a_c(\rho)=\omega_c W_c(\rho)g_c,\qquad c=0,1.
\]

**W enthält bereits \(e^{iF_c}\), sämtliche Beiträge der festen äußeren Staubdaten und das vollständige innere Uhr-/Dichteintegral einschließlich aller acht Atom-/Positivstrata.** Ein weiterer Faktor \(e^{iS_{\mathrm{on},c}}\) oder \(e^{i\Delta S_{\mathrm{on}}}\) darf nicht an diese vollständigen Amplituden angehängt werden. Die frühere stationäre Wirkungsdifferenz ist eine getrennte asymptotische Diagnose.

Die äußeren Werte \(T_B\) und \(r_B=\rho\) sind bislang **Dirichlet-Kerndaten**, keine normierten physischen Uhr-/Dichte-Randpakete. Der geprüfte skalare Gaußfaktor \(g_c\) paart den Skalarteil mit identischen Schwartz-Testpaketen; er liefert nicht zugleich die fehlende physische Uhr-/Staub-Randpaarung. Die komplexen Zahlen \(a_c\) sind daher zunächst bedingte Kernauswertungen.

## 1. Exaktes Record-Gram-Modell

Füge hypothetische normierte Recordzustände \(e_c\) und ihren festen, präparationsunabhängigen Überlapp hinzu. Wir benutzen ausdrücklich die Indexkonvention

\[
\eta_{cd}=\langle e_d|e_c\rangle,
\qquad
\eta=\begin{pmatrix}1&\gamma\\\overline\gamma&1\end{pmatrix},
\quad |\gamma|\le1.
\]

Dann ist

\[
D_{cd}=a_c\overline{a_d}\,\eta_{cd},
\qquad D=\operatorname{diag}(a)\eta\operatorname{diag}(a)^\dagger
\]

positiv semidefinit. Für beide nichtverschwindenden Amplituden gilt

\[
\det D=|a_0a_1|^2(1-|\gamma|^2)\ge0.
\]

Das garantiert starke Positivität auf jeder endlichen Sammlung von Ereignissen: ihre Matrix ist eine Kongruenztransformierte der atomaren Matrix D durch die zugehörigen Inzidenzvektoren. Diese Eigenschaft wird hier algebraisch hergestellt; sie wird nicht aus einer bereits vorhandenen physischen CST-Paarung gewonnen.

Für die gesamte akzeptierte Alternative \(\Omega=\{0,1\}\) ist der Gesamtwert

\[
Z=D(\Omega,\Omega)=\sum_{c,d}D_{cd}
=|a_0|^2+|a_1|^2+2\operatorname{Re}(a_0\overline{a_1}\gamma).
\]

**Normiert wird mit Z, nicht generell mit \(\operatorname{tr}D\).** Für Z>0 ist D/Z ein auf \(\Omega\) normiertes Dekohärenzfunktional. Für Z=0 existiert dieser bedingte akzeptierte Zustand nicht; das Failure-Ereignis bleibt wohldefiniert.

- \(\gamma=0\): orthogonale Klassenrecords; D ist diagonal.
- \(\gamma=1\): gemeinsamer phasengleicher Record; \(Z=|a_0+a_1|^2\).
- Komplexes \(\gamma\): teilweise erhaltene Klasseninformation und zusätzliche relative Recordphase.

Ein nachträgliches Weglassen eines bereits aufgezeichneten orthogonalen Klassenlabels erzeugt keine Interferenz. Der Wechsel von \(\gamma=0\) zu \(\gamma=1\) beschreibt ein anderes Record-Instrument beziehungsweise eine eigens implementierte, gegebenenfalls konditionierte Quantenlöschung.

## 2. Warum die Diagonalen keine allgemeinen Geometrieprobabilitäten sind

Die Einzelereigniswerte \(D_{00}/Z\), \(D_{11}/Z\) sind im kohärenten Fall positive Quantenmaße. Ohne konsistente Grobvergröberung müssen sie weder zu eins addieren noch einzeln kleiner als eins sein.

Exakte Gegenkontrolle:

\[
a=(1,-1/2),\quad\gamma=1
\quad\Longrightarrow\quad
Z=1/4,\qquad D_{00}/Z=4,\quad D_{11}/Z=1.
\]

Dies ist mit starker Positivität vereinbar, aber keine Wahrscheinlichkeitsverteilung für zwei sich ausschließende Geometrien. Die vollständige Destruktionskontrolle \(a=(1,-1),\gamma=1\) liefert Z=0 und damit keinen bedingten Erfolgszustand.

Für die Zwei-Ereignis-Summenregel reicht \(\operatorname{Re}D_{01}=0\). Das ist schwächer als \(D_{01}=0\) und liefert nicht automatisch orthogonale stabile Records. Beispielsweise gilt bei \(a=(1,i),\gamma=1\) die additive Summenregel, obwohl \(D_{01}=-i\ne0\) und beide Recordzustände gleich sind.

Auch die Trace-Normierung muss präzise unterschieden werden: D/trD kann eine positive Dichtematrix auf einem **zusätzlich gewählten orthogonalen History-Hilbertraum** sein. Sie ist bei Interferenz jedoch kein auf \(\Omega\) normiertes Dekohärenzfunktional, weil ihre gesamte Eintragssumme nicht eins ist. Erst das explizite Entfernen der Offdiagonalen ist Dephasierung. Die Born-Diagonalwerte Dcc/trD entsprechen einem aufgelösten Alternativexperiment, nicht automatisch der gemeinsamen kohärenten Randakzeptanz.

Eine intrinsische Geometriegröße, die den beiden Ordnungen unterschiedliche Werte zuweist, kann deshalb nicht ohne weiteren Messvertrag mit diesen kohärenten Einzelwerten klassisch gemittelt werden. Ein Quotient wie \((n_0a_0+n_1a_1)/(a_0+a_1)\) wäre im Allgemeinen komplex; seine bloße Berechnung macht ihn nicht zum erwarteten Radius, Volumen oder klassischen geometrischen Mittelwert.

## 3. Tatsächliche Detektorports und Failure-Vervollständigung

Eine konkrete Realisierung der Recordvektoren ist

\[
e_0=(1,0)^T,\qquad
e_1=(\overline\gamma,\sqrt{1-|\gamma|^2})^T.
\]

In der orthonormalen Detektorbasis sind die unskalierten Portgewichte

\[
q_0=|a_0+\overline\gamma a_1|^2,
\qquad q_1=(1-|\gamma|^2)|a_1|^2,
\qquad q_0+q_1=Z.
\]

Das sind zulässige Detektorports. Für \(\gamma\ne0\) ist Port 0 ausdrücklich kein exklusiver Geometrie-0-Record. Andere orthonormale Auslesebasen sind weitere, offenzulegende Apparateentscheidungen.

Um ein lineares vollständig positives Instrument für mehrere Eingänge zu erhalten, muss man zusätzlich einen normierten endlichen Eingangsraum E und beschränkte Amplitudenfunktionale \(\ell_c:E\to\mathbb C\) festlegen. Die bisherigen Dirichlet-Daten legen einen solchen Raum nicht automatisch fest. Unter dieser Zusatzannahme definiere

\[
M\psi=\lambda\sum_ce_c\ell_c(\psi),
\qquad
M_F=(I_E-M^\dagger M)^{1/2}
\]

mit einem vor der Zahlenanpassung gewählten Gain, der \(\|M\|\le1\) garantiert. Die Messung der zwei orthonormalen Detektorports und ein eigener orthogonaler Failure-Flag geben dann eine vollständige CP-Instrumentfamilie. Der Stern bezeichnet hier ausschließlich den Adjungierten auf dem **erklärten endlichen Hilfsraum**. Es wird kein globales \(K^\dagger K\) der ursprünglichen distributionellen Amplitude vorausgesetzt.

Eine konservative gemeinsame Schranke lautet
\(\|M\|\le\lambda(\|\ell_0\|+\|\ell_1\|)\); sie gilt für sämtliche zulässigen \(\gamma\). Damit kann derselbe Gain in kohärenten und aufgelösten Kontrollen benutzt werden. Eine Gain-Wahl für das tatsächliche N11-Modell benötigt zusätzlich den gewählten Eingangsraum und seine Paketnormen.

Der ausführbare Algebra-Test benutzt als **klar markierte, nicht aus N11 berechnete Testdaten**

\[
A=\begin{pmatrix}1&1/2\\1/2&i\end{pmatrix},\qquad \lambda=1/4.
\]

Es gelten \(\|A\|_F^2=5/2\) und \(\|M\|^2\le5/16\) für jedes \(\gamma\). Der Failure-Effekt ist deshalb positiv und mindestens \(11I/16\). Fünf verschiedene Gramfelder und drei normierte Eingänge werden exakt geprüft. Alle Port- plus Failure-Wahrscheinlichkeiten addieren sich zu eins.

Für einen einzelnen festgelegten Eingang lässt sich auch die Historienmatrix um den orthogonalen Failure-Sektor ergänzen:

\[
D_{\mathrm{gesamt}}=\begin{pmatrix}\lambda^2D&0\\0&1-\lambda^2Z\end{pmatrix}.
\]

Sie ist stark positiv und ihre gesamte Eintragssumme ist eins. Der ergänzte Failure-Sektor ist ein Bestandteil des hypothetischen Apparats, keine zusätzliche hergeleitete CST-Geometriehistorie.

## 4. Exakte Unterbestimmtheit bei gleichen Wirkungsamplituden

Zwei voneinander unabhängige Freiheiten bleiben:

**Recordvertrag.** Für dieselben beiden nichtverschwindenden a und denselben Eingangsvertrag liefert \(\gamma=0\) eine History-Gram-Matrix von Rang zwei, \(|\gamma|=1\) eine von Rang eins. Der aus D durch Quotientierung konstruierte abstrakte positive Raum hat also selbst eine vom Recordvertrag abhängige Dimension. Ein solcher mathematischer Hilbertraum existiert, ist dadurch aber nicht als physischer CST-Raum ausgezeichnet. Bei festgehaltenen Amplitudenbeträgen liegt der mögliche Gesamtwert in

\[
(|a_0|-|a_1|)^2\le Z\le(|a_0|+|a_1|)^2.
\]

Die Extremwerte folgen aus zulässigen Phasen von \(\gamma\). Ein tatsächlich gewähltes \(\gamma\) ist über alle verglichenen Präparationen festzuhalten; es darf nicht für jeden \(\rho\)-Wert nachgestellt werden.

**Historiengewichte.** Setze \(b_c=W_cg_c\). Falls beide b ungleich null sind, kann bereits das aufgelöste Instrument jeden Zielwert \(p\in(0,1)\) für Geometrie 1 erzeugen, indem man positive Gewichte wählt:

\[
\omega_0\propto|b_1|\sqrt{1-p},\qquad
\omega_1\propto|b_0|\sqrt p.
\]

Dann gilt exakt

\[
\frac{|\omega_1b_1|^2}{|\omega_0b_0|^2+|\omega_1b_1|^2}=p.
\]

Beide Gewichte können gemeinsam auf \(\omega_0+\omega_1=1\) normiert werden, ohne den Quotienten zu ändern. Diese Konstruktion ist ein Unterbestimmtheitsbeweis, **keine zulässige Datenanpassung oder neue physische Gewichtswahl**. Der Befund bleibt unabhängig davon gültig, welche von null getrennten N11-Zahlen der Integrator liefert. Ein physikalisches Prinzip könnte die Gewichte später einschränken oder bestimmen; ein solches Prinzip ist bisher nicht hergeleitet.

## 5. Warum das ursprüngliche Maß die fehlende Paarung nicht auswählt

Die lokale Atom-plus-kompakte Dichteintegration ist

\[
J(C)=\frac12+\frac12\int_0^1e^{-irC/2}\,dr
=\frac12+\frac{1-e^{-iC/2}}{iC},\qquad J(0)=1.
\]

Sie ist glatt, kein \(\delta(C)\), und wird nicht durch Multiplikation mit C annihiliert. Schon bei \(C=2\pi\) gilt
\(CJ(C)=\pi-2i\ne0\); auch \(J(C)^2\ne J(C)\). Die ursprüngliche Dichteintegration ist daher keine lokale RAQ-Projektion. Die Existenz regulärer klassischer Sättel ändert diese Identität nicht.

Aus den vorliegenden Daten wird kein neuer erstklassiger Constraint, keine Rigging Map und keine kanonische physische Paarung abgeleitet. Die korrekte Aussage ist, dass zahlreiche positive und vollständige **zusätzlich deklarierte** endliche Readouts möglich sind. Positivität und Failure-Vervollständigung testen deren interne Konsistenz; sie wählen die Physik nicht aus.

## 6. Kontrollen und nächster sachlicher Anschluss

`checks/physical_readout/check.py` benötigt SymPy und prüft acht Gruppen: die allgemeine Determinante und Summenregel; zwanzig exakte Gram-/Amplitudenbeispiele; die unzulässigen Geometrieprobabilitäten (4,1); schwache Additivität ohne orthogonale Records; Ablehnung von \(|\gamma|>1\); fünf CP-Instrumente mit insgesamt fünfzehn Eingangsprüfungen; freie positive Gewichtungsverhältnisse; die Nichtprojektor-Identität des ursprünglichen Dichtemaßes. Alle bestehen. Es wurden keine zusätzlichen N11-Integrale ausgewertet.

Sobald W und g eingeschlossen vorliegen, ist der nächste begrenzte Vergleich konkret: **dieselben** vollständigen Amplituden, **dieselben** festgelegten Historiengewichte, **derselbe** Gain und Eingangsvertrag; dann \(\gamma=0\), ein festes partielles \(\gamma\) und \(\gamma=1\) vergleichen. Interferenzantwort, dephasierte Quellenantwort, Portwahrscheinlichkeiten und Failure werden getrennt berichtet. Die frühere stationäre Phase wird nicht zusätzlich eingesetzt. Ein dabei gefundener Nichtnull-Kontrast ist ein bedingter Auslesebefund; die physische Uhr-/Staub-Randpaarung, Gewichtsauswahl und Geometriedynamik bleiben eigene offene Aufgaben.

## Primärliteratur und Aussagegrenzen

Methodisch geprüft am 13. November 2026:

- Á. Mozota Frauca und R. D. Sorkin, *How to Measure the Quantum Measure*, https://arxiv.org/abs/1610.02087. Die Arbeit trennt Quantenmaße von gewöhnlichen POVM-Wahrscheinlichkeiten und beschreibt zusätzliche Ancilla-/Ausleseanordnungen. Sie begründet keinen konkreten CST-Detektor für dieses Paket.
- F. Dowker und H. Wilkes, *An Argument for Strong Positivity of the Decoherence Functional*, https://arxiv.org/abs/2011.06120. Starke Positivität wird als zentrale Konsistenzbedingung für zusammensetzbare Quantensysteme untersucht. Sie ersetzt keine Herleitung unseres konkreten D.

Alle 2×2-Formeln, Gegenkontrollen und Failure-Konstruktionen oben sind hier ausgeführte endliche Ableitungen. Das Ergebnis bleibt **CONDITIONAL_READOUT_CONSTRUCTED; PHYSICAL_PAIRING_NOT_DERIVED**.
