# CST-DUST: Detektorkopplung und notwendige Historienmischung v0.1

7. November 2026. Basis: Main nach PR 261,
`7398a19f90e0c3736e2041b7f1480fc9223bbf9e`.
Vier unveränderte Quellen sind in `provenance.json` bytegenau gepinnt.

## 1. Entscheidung und Reichweite

Der Vorgänger verlangt einen qualifizierten Rang-eins-Rückkehrdetektor.
Hier wird eine konkrete Kandidatenklasse geprüft: Ein Hilfssystem koppelt
an klassische Materie- und Geometrierecords, ohne diese Historien zu mischen.
Das umfasst eine von-Neumann-artige Kopplung M_F⊗B, auch mit mehreren
zeitlich geordneten Pulsen und nichtkommutierenden Hilfssystemkontrollen,
solange die gesamte Systemoperation recorderhaltend bleibt.

**Ergebnis innerhalb des erklärten Referenzraums:** Diese Klasse erzeugt
nur diagonale Messeffekte. Sie kann den balancierten Rang-eins-Rückkehreffekt
nicht mit universellem Operatornormfehler unter 1/2 realisieren. Die
Untergrenze ist scharf. Wiederholungen, klassische Rückkopplung und
Postselektion innerhalb derselben Klasse beseitigen sie nicht.

Für eine beschränkte zusätzliche Historienmischung V(t) folgt die notwendige
Bedingung γ≥max(0,1/2−τ), wobei γ=∫||V(t)||dt/ℏ und τ der verlangte
Effektfehler ist. Eine endliche Mischrotation um π/4 zeigt, wie man die
eingeschränkte Klasse mathematisch verlassen kann. Sie ist kein aus CST
hergeleiteter Wechselwirkungsoperator. Eine zusätzliche Einbettungskontrolle
zeigt, warum die richtige Wirkung auf zwei Testmoden allein nicht genügt.

**Alle acht physikalischen Gates bleiben HOLD.** Dies ist kein allgemeines
Verbot lokaler Kopplungen, kein CST-No-go und keine Aussage, dass jede
physikalische Messung mit allen Historienrecords kommutieren müsste.
Eine Ortslokalität ist nicht dasselbe wie Diagonalität in diesem
Historienraum. Die physikalische Zulässigkeit dieses Raums und seiner
Zustände bleibt, wie im Vorgänger, eine offene Frage.

## 2. Genau geprüfte Kopplungsklasse

Sei H=L²(Ω,ν) der erklärte Historienraum bei festem Enduhrwert,
und A=L∞(Ω,ν) seine Algebra diagonaler Recordfunktionen M_f.
Das Detektorhilfssystem K startet in einem festen, vom unbekannten
Eingangszustand unabhängigen Zustand σ. Die Anfangspräparation ist ρ⊗σ.
Der Ausleseeffekt F wirkt ausschließlich auf K und erfüllt 0≤F≤I.

Die Kandidatenwechselwirkung ist eine zerlegbare unitäre Abbildung

\[
 (W\Psi)(Y)=U(Y)\Psi(Y),\qquad U(Y)^\dagger U(Y)=I_K.
\]

Äquivalent kommutiert W mit allen M_f⊗I. Ein konkreter beschränkter
Hamiltonoperator, der diese Struktur erzeugt, ist beispielsweise

\[
 H_d(t)=M_{g(t,\cdot)}\otimes I+I\otimes H_A(t)
       +\sum_r \lambda_r(t)M_{F_r}\otimes B_r(t).
\]

Alle Funktionen F_r sind reell und beschränkt. In einem endlichen
Elementzahl-/Uhrsektor kann etwa die vorhandene Materiewirkung S_d(Y)
als F verwendet werden. Sie ist dort eine gewöhnliche Recordfunktion.
Die B_r dürfen untereinander und mit H_A nicht kommutieren. Trotzdem
entwickelt sich bei jedem Y nur das Hilfssystem; die Historienindizes
werden nicht gemischt. Zeitordnung ändert diese Aussage nicht.

Das Kontrollzeitargument t ist hier ein deklarierter Parameter eines
Kopplungsmodells. Seine physikalische Identifikation mit einer CST-Materieuhr
oder einer Raumzeitentwicklung wird nicht hergeleitet. Eine Erweiterung
auf unbeschränkte Generatoren benötigt eigene Definitionsbereichs- und
Propagatornachweise; sie wird für die Hamiltonabschätzung unten nicht behauptet.

Die Reduktionsabbildung auf einen Systemeffekt lautet

\[
 E=\Phi_\sigma\!\left(W^\dagger(I\otimes F)W\right),
 \qquad\operatorname{Tr}(\rho E)
 =\operatorname{Tr}[(\rho\otimes\sigma)W^\dagger(I\otimes F)W].
\]

Hier ist Φσ(A) die Hilfssystemerwartung. Einsetzen der Faserform liefert

\[
 E=M_e,\qquad e(Y)=\operatorname{Tr}_K[\sigma U(Y)^\dagger F U(Y)],
 \qquad 0\le e(Y)\le1.
\]

Dies beweist die Diagonalität für beliebige Hilfssystemdimension und
beliebige feste gemischte σ. Eine Wahl bereits korrelierter System- und
Detektoranfangsdaten wäre eine andere Voraussetzung und wird damit nicht
als universelles Instrument auf unbekannten ρ legitimiert.

### Folgen für Phase, Wiederholung und Präparation

Ein fester solcher Effekt kommutiert mit der geerbten Wirkungsphase
D=exp(iS), also Tr(E DρD†)=Tr(Eρ). Er ist blind gegenüber einer allein
im System eingeprägten diagonalen Phase. Wenn die Apparatur selbst beim
Scan geändert wird, ist ihr Effekt nicht mehr fest; das ist ein anderes
Experiment und keine Realisierung des hier geforderten festen Projektors.

Für reine σ und eine feine Zeigerauslese sind die Krausoperatoren
Multiplikationen K_j=M_(k_j). Gemischte Anfangszustände liefern zusätzliche
Krausindizes, aber dieselbe Form. Produkte solcher Operatoren bleiben
Multiplikationen. Für endlich viele Messungen mit klassischer Rückkopplung
gilt dies auf jedem vollständigen Ergebniszweig. Summen über akzeptierte
Zweige ergeben wieder diagonale Effekte. Nullzweige dürfen nicht durch
Division in einen Zustand umgedeutet werden.

Seien Π_a und Π_c die Recordprojektoren auf Nullatom bzw. kontinuierlichen
Anteil. Aus Π_aρΠ_c=0 folgt für jeden solchen selektiven Ausgang weiterhin
Π_a KρK† Π_c=0. Auch Konditionierung mit positiver Zweigwahrscheinlichkeit
erzeugt keine Kreuzkohärenz. Für den unten verwendeten Zielzustand ψ_+
hat jeder normierte blockdiagonale Zustand deshalb Zielfidelität höchstens
1/2: Tr(P_+ρ)=(<a|ρ|a>+<c|ρ|c>)/2≤1/2. Dies ist eine unmittelbare
algebraische Folge der Blockstruktur, keine statistische Schätzung.

## 3. Scharfe Fehleruntergrenze für den vorhandenen Rückkehrtest

Im bedingten n=1-Referenzraum ist

\[
 d\nu=dx[\tfrac12\delta_0(dw)+\tfrac12\mathbf1_{(0,1)}dw],\qquad x\in(0,1).
\]

Die normierten orthogonalen Moden sind a=√2·1_(w=0) und
c=√2·1_(0<w<1), jeweils in x konstant. Setze
ψ_±=(a±c)/√2, P_+=|ψ_+><ψ_+|. Es gilt |ψ_+|²=|ψ_-|²=1 fast überall
und <ψ_+|ψ_->=0. Jede diagonale Auslese E=M_e liefert daher denselben
Wert q∈[0,1] auf ψ_+ und ψ_-. Der Zielprojektor liefert dagegen eins
beziehungsweise null. Folglich

\[
 \|M_e-P_+\|\ge\max\{1-q,q\}\ge\tfrac12.
\]

Die Operatornorm eines selbstadjungierten Operators ist das Supremum der
absoluten normierten Zustands-Erwartungswerte. Die beiden Testzustände
reichen somit für diese Untergrenze. Mit E=I/2 wird sie erreicht:
(I/2−P_+)²=I/4. Also

\[
 \boxed{\inf_{0\le e\le1}\|M_e-P_+\|=\tfrac12.}
\]

Dies ist ein universeller Effektfehler im erklärten Referenzraum, kein
gemessener Prozentfehler einer ausgewählten Einzelwahrscheinlichkeit.
Ein diagonaler Detektor kann für eine einzelne bekannte Eingabe dieselbe
Zahl liefern, ohne denselben Effekt zu implementieren. Andere Protokolle
können unter weiteren Annahmen Phasenmittelwerte schätzen; sie werden
durch diesen Satz nicht allgemein ausgeschlossen.

Unter einem äquivalenten Maßwechsel U=M_(√r) gilt
P_+,θ=U†P_+,0U und U†M_eU=M_e. Die Operatornorm zwischen den gewichteten
Hilberträumen wird von U erhalten. Die Untergrenze ist somit unabhängig
von der Maßdarstellung, sofern Ziel und Zustände korrekt mitgeführt werden.

Der Satz setzt voraus, dass beide Testzustände im verglichenen Raum
zulässig sind. Würden spätere physikalische Constraints diesen Raum
einschränken, müsste die Aussage auf dem neuen physikalischen Raum erneut
geprüft werden. Eine solche Constraint-Herleitung liegt hier nicht vor.

## 4. Wie viel Historienmischung mindestens erforderlich ist

Betrachte dieselbe Apparatur mit zwei Generatoren H_d(t) und
H(t)=H_d(t)+V(t) auf H⊗K. Für diesen Satz seien beide Generatoren
beschränkt, selbstadjungiert, stückweise normstetig und über [0,T]
normintegrierbar. H_d erzeugt eine recorderhaltende Entwicklung W_d;
V ist der deklarierte zusätzliche Anteil. Die Eingangspräparation σ
und die Hilfssystemauslese F sind in beiden Vergleichen identisch.

Setze B=I⊗F und B_d(t)=W_d(T,t)† B W_d(T,t). Dann ist 0≤B_d(t)≤I.
Für A(t)=W(t,0)† B_d(t)W(t,0) ergibt direktes Differenzieren

\[
 \dot A(t)=\frac{i}{\hbar}W(t,0)^\dagger[V(t),B_d(t)]W(t,0).
\]

Da [V,B_d]=[V,B_d−I/2] und ||B_d−I/2||≤1/2, gilt
||[V,B_d]||≤||V||. Integration zwischen t=0 und T liefert

\[
 \|W^\dagger BW-W_d^\dagger BW_d\|
 \le \gamma:=\frac1\hbar\int_0^T\|V(t)\|dt.
\]

Die positive unital normkontraktive Abbildung Φσ kann diese Norm nicht
vergrößern. Die resultierenden Effekte E und E_d erfüllen also
||E−E_d||≤γ. Mit dem vorherigen Abstandssatz folgt

\[
 \boxed{\tau:=\|E-P_+\|\ge\max(0,\tfrac12-\gamma).}
\]

Insbesondere verlangt τ≤τ_ziel<1/2 notwendig
γ≥1/2−τ_ziel. Diese Schranke ist nicht als optimaler Quantum-Speed-Limit-
Satz behauptet; sie ist weder eine hinreichende Konstruktionsbedingung
noch eine in Geld oder Rechnerzeit ausgedrückte Ressource. Die Aufteilung
H_d+V ist offenzulegen; ein unnötig großer diagonaler Anteil in V macht
die Schranke lediglich schwächer. Unbeschränkte physikalische Feldgeneratoren
sind ohne zusätzliche Kontrolle nicht automatisch abgedeckt.

| gewünschter Effektfehler höchstens | notwendiges γ mindestens |
|---:|---:|
| 0 | 1/2 |
| 1/100 | 49/100 |
| 1/10 | 2/5 |
| 1/4 | 1/4 |
| 1/2 | 0 |

Die Tabelle sind bedingte mathematische Anforderungen, keine gemessenen
Kopplungsstärken. Sie zeigt insbesondere, warum ein beliebig kleiner
Zusatzterm nicht automatisch den geforderten Rückkehrdetektor liefert.

## 5. Endlicher Mischkontrollfall und Einbettungsfalle

Auf einem ausschließlich zweidimensionalen Kontrollraum sei

\[
 R(\theta)=\begin{pmatrix}\cos\theta&\sin\theta\\-\sin\theta&\cos\theta\end{pmatrix},
 \qquad P_a=\begin{pmatrix}1&0\\0&0\end{pmatrix}.
\]

Erst R anwenden, dann den Record a messen, erzeugt den Effekt
Eθ=R†P_aR. Bei θ=π/4 ist Eθ=P_+. Ein konstanter Generator
V=−ℏθ σ_y/T über die Dauer T realisiert diese Rotation und besitzt
γ=|θ|=π/4. Dieser Term mischt die beiden Recordmoden ausdrücklich und
liegt außerhalb der geprüften recorderhaltenden Klasse.

Für rationale c=cosθ und s=sinθ mit c²+s²=1 folgt exakt

\[
 E_\theta=\begin{pmatrix}c^2&cs\\cs&s^2\end{pmatrix},\quad
 \|E_\theta-P_+\|^2=(1-2cs)/2,\quad
 \|E_\theta-P_a\|=|s|.
\]

Sechs rationale Rotationen kontrollieren diese Identitäten. Der ideale
π/4-Fall wird ohne Gleitkommazahlen über den ganzzahligen Zähler von R
und dessen Normfaktor 2 geprüft. Er zeigt, dass der Ausschlusssatz nicht
auf alle Quantenkopplungen erweitert werden darf. Eine zulässige
CST-Wechselwirkung oder physikalische Lokalität dieses Modenoperators
ist damit nicht bewiesen.

### Ein korrekter Zweimodentest zertifiziert nicht den ganzen Hilbertraum

Fügt man einen dritten Modus hinzu, kann ein Detektor
E_falsch=P_+⊕1 auf dem Testblock exakt richtig aussehen. Gegen den
gewünschten vollständigen Effekt E_ziel=P_+⊕0 hat er jedoch Normfehler
eins. Ein Eingang im dritten Modus liefert Erfolg eins statt null.

Genau diese Gefahr besteht, wenn im kontinuierlichen Raum die
Recordmessung Π_(w=0) mit dem Rang-eins-Projektor |a><a| verwechselt
wird: Π_(w=0) akzeptiert weitere Uhrmoden. Eine Rotation allein des
Spannraums {a,c} lässt diese zusätzlichen Ausgänge bestehen. Der
zweidimensionale Mischkontrollfall ist daher ausdrücklich kein vollständiger
Detektorentwurf für den kontinuierlichen Historienraum.

## 6. Exakte Kontrollen und Reproduzierbarkeit

Der nach dem algebraischen Entwurf eingefrorene Plan legt alle endlichen
Testgitter fest. Es ist keine externe Präregistrierung. Die Daten werden
mit der Python-Standardbibliothek und exakten rationalen komplexen Zahlen
berechnet. Quadratwurzeln werden durch rationale Intervalle eingeschlossen.

- 75 vollständige gemeinsame Zweipuls-Unitaritäten;
- 900 reduzierte Effekte mit direkter Kontrolle der gemeinsamen Born-Regel;
- 25 rückgekoppelte Instrumente mit 100 Zweigen, darunter 81 nichtleere
  konditionierte Zustände ohne erzeugte Kreuzkohärenz;
- 25 diagonale Effektfälle und die exakte Erreichbarkeit von 1/2;
- drei gewichtete Darstellungen derselben Untergrenze;
- sechs rationale Mischrotationen, der ideale π/4-Kontrollfall und der
  dreidimensionale Einbettungsgegenvergleich;
- sieben zurückgewiesene Negativkontrollen.

Die allgemeinen Aussagen werden durch die ausgeschriebenen Beweise
getragen; die endlichen Fälle sind Implementierungskontrollen. Vier
Ergebnisdateien werden isoliert erneut erzeugt und bytegleich verglichen.
Dies ist keine externe Replikation, keine formale Beweisassistentenprüfung
und keine Feldquadratur eines physikalischen vierdimensionalen CST-Ensembles.

## 7. Neue Entscheidung für das Forschungsprogramm

Die recorderhaltende Kandidatenklasse ist als universeller Rückkehrdetektor
mit Effektfehler unter 1/2 im erklärten Referenzraum ausgeschieden.
Weitere Hilfssystempulse oder genauere n=5-Integrale innerhalb dieses
Ansatzes lösen das strukturelle Problem nicht.

Der nächste Kandidat muss einen **aus Materie-/Randdynamik begründeten
historienmischenden Operator V** angeben, seine zulässige Zustandsdomäne,
Symmetrien und kausale Unterstützung klären und den Effekt im vollständigen
Raum samt Ausfallausgang bestimmen. Erst danach sind Präparation,
Kalibrierung, Nachmesskanal und gravitative Rückwirkung zu prüfen.
Die Schranke für γ ist dabei eine notwendige Vorprüfung, keine Abnahme.

Ein physikalisch lokales Feldmodell kann in einer Konfigurationsdarstellung
beispielsweise durch kinetische Terme außerhalb der hier geprüften
diagonalen Klasse liegen. Es wird deshalb nicht durch bloße Verwendung
des Wortes „lokal“ ausgeschlossen. Ebenso wird keine andere operationale
Observable verboten, wenn der Rang-eins-Vertrag ausdrücklich geändert wird.

`coupling_contract.json` hält diese Unterscheidungen maschinenlesbar fest.
MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben HOLD. Es wurden weder kostenpflichtige Rechenleistung
noch ein n=5-Produktionslauf gestartet.

## Primärquellen und Literaturabgrenzung

- Projektbasis: [PR 261](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/261).
  Definition des Zielinstruments und des Fehlerparameters τ aus den gepinnten Quellen.
- John Preskill, *Quantum Information*, Kapitel 3,
  https://www.preskill.caltech.edu/ph219/chap3_15.pdf .
  Kontext für von-Neumann-Kopplung, Hilfssystem und Krausdarstellung.
  Die hier eingeschränkte Kopplungsklasse und die Abstandssätze sind oben
  selbstständig hergeleitet; es wird kein neuer allgemeiner Messsatz beansprucht.
- A. Belenchia et al., *Low energy signatures of nonlocal field theories*,
  https://arxiv.org/abs/1605.03973 . Dort wird die Antwort eines an ein
  nichtlokales Skalarfeld gekoppelten Detektors untersucht. Das ist eine
  andere Ausgangsdefinition als der hier postulierte Rückkehrprojektor
  auf vollständige CST-Historien. Eine Abbildung zwischen diesen Modellen
  wurde in diesem Paket nicht hergeleitet.
- A. Belenchia, D. M. T. Benincasa, S. Liberati, *Nonlocal Scalar Quantum
  Field Theory from Causal Sets*, https://arxiv.org/abs/1411.6513 .
  Kontext für einen feldtheoretischen CST-Pfad, kein Nachweis der hier
  fehlenden vollständigen gravitativen Präparation oder Detektorkopplung.

Externe Volltexte werden nicht verteilt. Die Literaturhinweise behaupten
weder eine vollständige Literaturübersicht noch Neuheit der verwendeten
elementaren Operatorargumente.
