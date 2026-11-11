# Erster paritätserlaubter Atom/Positiv-Mischblock

Version 0.1, 11. November 2026. Anschluss an PR #279–281.

## 1. Ergebnis und genaue Reichweite

Für den unten vollständig festgelegten endlichen Kontrollversuch ist der Matrixeintrag

$$\mathcal M_\lambda=\langle A,+,0_m|K_\lambda|A,0,0_m\rangle$$

bei beiden Endpunkten $\lambda=1$ (ursprüngliche Wirkung) und $\lambda=0$ (entkoppelte Referenzwirkung) **zertifiziert nicht null**. Die zusätzliche Skalarwirkung ist bei $\lambda=0$ unabhängig von der Historie; ihre kinetischen Terme und die innere Gaußlücke bleiben erhalten. Die untersuchte Kopplung ist die **Geometrieabhängigkeit des zusätzlichen Skalarfelds**, nicht eine direkte Staub-Skalar-Kopplung. Letztere ist im Vorgängermodell bereits null.

| Größe | Realteil | Imaginärteil | Fehler je angezeigter Komponente |
|---|---:|---:|---:|
| $\mathcal M_1$ | $-0.155730245646$ | $+0.132674294297$ | $\leq10^{-12}$ |
| $\mathcal M_0$ | $+0.021300694129$ | $-0.066660937892$ | $\leq10^{-12}$ |
| $\Delta=\mathcal M_1-\mathcal M_0$ | $-0.177030939775$ | $+0.199335232189$ | $\leq10^{-12}$ |

Die Komponentenfehler enthalten die Rundung dieser Tabelle. Es handelt sich um deterministische Einschließungen, nicht um statistische Konfidenzintervalle. Die Beträge haben die konservativen unteren Schranken

$$|\mathcal M_1|>0.20458,\qquad |\mathcal M_0|>0.06998,\qquad |\Delta|>0.26659.$$

**Ursachenaussage:** Die getestete Skalar-Geometrie-Kopplung ist für die Existenz dieses Mischungszeugen nicht notwendig, denn die entkoppelte Referenz mischt bereits. Sie verändert dessen komplexe Amplitude jedoch nachweislich. Weder diese Nichtnullaussage noch die Amplitudenänderung beweist physikalische Stauberzeugung, Verschränkung, Unitarität oder einen Bounce.

## 2. Vor der numerischen Auswertung festgelegter Versuch

Die Datei `experiment_contract.json` wurde vor dem ersten numerischen Lauf angelegt. Der Kontrollpunkt ist:

- alle 33 abgedeckten AA-Ordnungen auf $L=\{0,1\}$, $I=\{2\}$, $R=\{3,4\}$;
- genaues gelabeltes Historiengewicht $c_C=1/33$, ohne weiteren Orbitfaktor;
- volle Gravitationsphase $\exp(iF_4(C))$, also $\kappa=1$;
- masseloses zusätzliches Skalarfeld, $\mu=0$;
- Randbreiten $\sigma_s=\sigma_a=1$;
- gleiche Maße und Skalen wie in Schritt 2: $T_b=\ell$, $W=\hbar$, $F=\sqrt\hbar/\ell$;
- keine äußere gravitative Randwirkung zusätzlich zum deklarierten Kontrollwert null;
- unnormalisierter innerer Abel-Regulator, dessen Grenzwert analytisch ausgewertet wird;
- primäre Uhrenquadratur: 40 Gauß-Legendre-Knoten je Achse und 128 Bit Ballarithmetik.

Das gleichmäßige gelabelte Gewicht und $\kappa=1$ sind **explizite Kontrollentscheidungen**, keine abgeleitete physikalische CST-Gewichtung. Die im Vorgänger verwendete Konvention lautet $\kappa=(4/\sqrt6)\ell^2/(8\pi G\hbar)$. Es wird keine Gravitationsphase nachträglich entfernt oder zur Verstärkung des Signals angepasst. Die primären Amplituden werden insbesondere nicht durch die komplexe Gravitationssumme $Z$ geteilt.

Unter $S_2(L)\times S_2(R)$ zerfallen die 33 Historien in zehn Orbits. Ihre Repräsentanten, Multiplizitäten und Aktionen sind:

| Ordnungscode | Multiplizität $m_C$ | $F_4(C)$ |
|---:|---:|---:|
| 8476 | 4 | 10 |
| 8592 | 4 | 11 |
| 8600 | 4 | 10 |
| 8604 | 4 | 19 |
| 8732 | 4 | 10 |
| 8988 | 4 | 9 |
| 9116 | 2 | 18 |
| 24860 | 4 | 19 |
| 25372 | 2 | 18 |
| 25500 | 1 | 37 |

Die Zeilen werden mit $m_C/33$ summiert. Das ist lediglich die exakte Zusammenfassung des gelabelten Versuchs. Ein zusätzliches Teilen durch die Orbitgröße oder den Stabilisator wäre eine andere Gewichtung. Die volle Enumeration, alle ursprünglichen Hessians und alle $F_4$-Werte werden unabhängig gegen die eingefrorenen Daten geprüft.

## 3. Randzustände, Maße und Normierungsfaktoren

Es gelten an allen fünf Punkten

$$d\lambda(t)=\tfrac12\mathbf1_{[-1,1]}dt,\qquad
d\nu(r)=\tfrac12\delta_0(dr)+\tfrac12\mathbf1_{(0,1)}dr,$$

am jeweiligen Zweipunktrand das Quotientmaß

$$d\mu_A=\tfrac12\prod_{j\in A}d\lambda(t_j)d\nu(r_j)dq_j.$$

Der Eingang ist $d_0=2\mathbf1_{00}$, der Ausgang

$$d_+=\frac2{\sqrt3}(\mathbf1_{10}+\mathbf1_{01}+\mathbf1_{11}).$$

$+$ umfasst mindestens eine positive Randdichte als kohärenten Zustand mit gleichen positiven Maskenamplituden. Es bezeichnet keine statistische Mischung. Das Feldgrundpaket ist bei Einheitsbreiten

$$h_0(q_1,q_2)=\pi^{-1/2}e^{-(q_1^2+q_2^2)/2},\qquad
\Psi_{s,0}=\sqrt2\,d_sh_0.$$

Beide Zustände haben bezüglich $d\mu_A$ Norm eins; ihr kinematischer Überlapp ist null. Die hier berechnete Nichtnullzahl ist ein Matrixelement des deklarierten Integraloperators und kein Überlapp zweier unnormierter Präparationen. Zeilen bezeichnen ausgehende, Spalten eingehende Zustände.

Für jeden Beitrag aus einer der drei ausgehenden Masken und einer der beiden inneren Masken ist der konstante Dichtevorfaktor

$$\underbrace{\frac14}_{\text{zwei Randquotienten}}
\underbrace{2}_{\sqrt2\sqrt2}
\underbrace{2}_{d_0}
\underbrace{\frac2{\sqrt3}}_{d_+}
\underbrace{\frac1{32}}_{\text{fünf Atom/Positivgewichte}}
=\frac1{16\sqrt3}.$$

Die beiden Eingangsdichten liegen am Atom. Damit bleiben sechs relevante Maskenbeiträge; die übrigen Masken des vollständigen Maßes werden vom Eingangspaket annihiliert. Alle Uhren werden auch an Atomstellen beibehalten.

## 4. Entkopplung unmittelbar auf Wirkungsebene

Die ursprüngliche Skalarwirkung lautet $S_\Phi(C)=\frac12\Phi^TH_C\Phi$, mit

$$H_C=-\frac12D_{\rm inc}^T\operatorname{diag}(vB_{xy})D_{\rm inc},\quad
v=\ell^4,\quad B_{xy}=\frac4{\sqrt6\ell^2}c_{xy},$$

wobei $c_{xy}=(1,-9,16,-8)$ nach Intervallschicht. Die gesamte Wirkung lautet $S_g(C)+S_d(C,T,w)+S_\Phi(C)$; die direkte $T,w$-Abhängigkeit des Skalarblocks fehlt.

Definiere **vor der Gaußintegration**

$$\overline H=\frac1{33}\sum_CH_C,\qquad
S_{\Phi,\lambda}(C)=\frac12\Phi^T[\overline H+\lambda(H_C-\overline H)]\Phi,\quad0\leq\lambda\leq1.$$

Alle anderen Wirkungsterme, Gewichte, Maße und Zustände bleiben gleich. Bei $\lambda=1$ erhält man exakt den ursprünglichen Kandidaten. Bei $\lambda=0$ ist das zusätzliche Skalarfeld bezüglich der Historienwahl ein unabhängiger Zuschauer. Es hat weiterhin eine nichttriviale quadratische Wirkung. Deshalb bleibt die innere Integration definiert, anders als beim unzulässigen bloßen Nullsetzen der gesamten Skalarwirkung.

Mit $M_C=F^2H_C/\hbar=\beta H_C^{(0)}$, $\beta=4/\sqrt6$, ist die exakte Referenzmatrix

$$\frac{\overline M}{\beta}=
\begin{pmatrix}
28/11&0&10/33&-47/33&-47/33\\
0&28/11&10/33&-47/33&-47/33\\
10/33&10/33&-40/33&10/33&10/33\\
-47/33&-47/33&10/33&28/11&0\\
-47/33&-47/33&10/33&0&28/11
\end{pmatrix}.$$

Sie ist unter beiden Randvertauschungen invariant, hat Zeilensumme null und behält die innere Lücke $\overline\alpha=40\beta/33>0$. Für die gesamte Interpolation gilt $\alpha_{C,\lambda}\geq\beta$. Die Referenz ist eine offen deklarierte feste Vergleichswirkung; sie muss nicht der Operator einer einzelnen Kausalordnung sein. Sie ist keine neue behauptete physikalische CST-Dynamik. Ohne diese Festlegung wäre „Entkopplung“ mehrdeutig.

## 5. Alle Phasen der skalaren Gaußprojektion

Ordne die Feldvariablen als $b=(q_0,q_1,q_3,q_4)$ und $x=q_2$. Schreibe

$$M_{C,\lambda}=\begin{pmatrix}B&J^T\\J&-\alpha\end{pmatrix},\qquad
z=\epsilon+i\alpha.$$

Die innere Integration liefert

$$\int_{\mathbb R}e^{-zx^2/2+i(Jb)x}dx
=\frac{\sqrt{2\pi}}{\sqrt z}\exp\!\left[-\frac{(Jb)^2}{2z}\right].$$

Die beiden normierten Grundpakete liefern zusammen $\pi^{-1}e^{-|b|^2/2}$. Daher

$$Q_\epsilon=I-iB+\frac{J^TJ}{z},\qquad
A_{C,\lambda}(\epsilon)=\frac{4\pi\sqrt{2\pi}}{\sqrt z\prod_{j=1}^4\sqrt{d_j(\epsilon)}},$$

wobei $d_j$ die komplexsymmetrischen Gauß-Eliminationspivots von $Q_\epsilon$ sind. Jeder Pivot liegt in der rechten Halbebene; alle vier Wurzeln werden dort auf dem Hauptzweig genommen. Auch $\sqrt z$ wird aus $\epsilon>0$ fortgesetzt. Im Grenzwert gilt

$$Q_0=I-iK,\qquad K=B+\frac{J^TJ}{\alpha},\qquad
\frac1{\sqrt{i\alpha}}=\alpha^{-1/2}e^{-i\pi/4}.$$

Der Realteil von $Q_\epsilon$ ist positiv definit. Die Akkretivität bleibt bei Schur-Elimination erhalten: Für den zur Elimination passend ergänzten Vektor reduziert $v^*Qv$ auf die quadratische Form des Schurkomplements. Damit sind die Pivotzweige wohldefiniert. Die Lücke aus Schritt 3 rechtfertigt die analytische Abel-Entfernung für beide Endpunkte.

**Die Hauptwurzel der gesamten Determinante darf nicht unbesehen eingesetzt werden.** Die Summe der Einzelphasen kann über einen Zweigschnitt laufen. Die unabhängige Kontrolle verwendet die reellen Eigenwerte $k_j$ von $K$:

$$A_{C,\lambda}(0)=4\pi\sqrt{\frac{2\pi}{\alpha}}
\prod_j(1+k_j^2)^{-1/4}
\exp\!\left[-\frac{i\pi}4+\frac i2\sum_j\arctan k_j\right].$$

Diese Formel bestätigt sämtliche Pivotphasen. Ein separater Test mit $K=10I_4$ zeigt explizit das falsche Vorzeichen, das die naive Wurzel des gesamten Determinantenprodukts ergeben würde.

Der Referenzfaktor ist

$$A_{\rm ref}\simeq0.5073499675465727+1.6840996012876250\,i.$$

Es wird kein komplexer Faktor nachträglich auf Betrag eins normiert. Der vollständige Eintrag ist

$$\mathcal M_\lambda=\frac1{33}\sum_Ce^{iF_4(C)}D_C A_{C,\lambda}(0),\qquad
\mathcal M_0=A_{\rm ref}\frac1{33}\sum_Ce^{iF_4(C)}D_C.$$

## 6. Exakte Dichteintegration und Uhrenkontraktion

Aus $S_d/\hbar=-\sum_xr_x\kappa_x(t)$ folgt

$$\kappa_x(t)=\frac12+\frac\beta4\sum_{y\prec x}c_{xy}(t_x-t_y)^2.$$

Der gesamte Positivachsenfaktor ist die ganze Funktion

$$E(k)=\int_0^1e^{-ikr}dr=e^{-ik/2}\operatorname{sinc}(k/2),\qquad E(0)=1.$$

Mit $E_x=E(\kappa_x)$ ergeben die sechs Masken exakt

$$D_C=\frac1{16\sqrt3}\int d\lambda^5(t)\,(1+E_2)(E_3+E_4+E_3E_4).$$

Die Ausgangspunkte bilden eine Antichain; $E_3$ hängt nicht von $t_4$ ab und $E_4$ nicht von $t_3$. Definiere daher

$$F_x(t_0,t_1,t_2)=\int d\lambda(t_x)E(\kappa_x),\quad x=3,4.$$

Dann lautet derselbe Staubfaktor

$$D_C=\frac1{16\sqrt3}\int d\lambda^3(t)\,(1+E_2)(F_3+F_4+F_3F_4).$$

Wendet man auf jeder Achse dieselbe Gaußregel an, ist die Kontraktion eine **exakte Umordnung endlicher Summen**. Sie verändert die zugrunde liegende fünfdimensionale Tensorquadratur nicht. Ausgangsfaktoren werden nur unter bewiesenen Symmetrien wiederverwendet: gleiche Koeffizienten dürfen vertauscht werden, und die gemeinsame Vorzeichenumkehr aller Uhren erhält die Quadrate. Im primären Lauf entstehen 34.040 verschiedene Ausgangsuhr-Summen mit 1.361.600 Auswertungen von $E$; die restlichen inneren $E_2$-Auswertungen kommen hinzu. Die Berechnung benötigt keine großen Historien- oder Produktionssimulationen.

## 7. Ein unabhängiges analytisches Quadraturfehlerbudget

Ein Unterschied zweier Quadraturordnungen ist kein Beweis einer Fehlergrenze. Die primäre Schranke wird deshalb unabhängig aus Analytizität hergeleitet.

Sei $f$ in der Bernsteinellipse $\mathcal E_\rho$, $\rho>1$, analytisch und durch $M$ beschränkt. Aus der Laurentdarstellung unter $z=(w+w^{-1})/2$ folgt für die Chebyshevkoeffizienten $|a_k|\leq2M\rho^{-k}$. Abschneiden nach Grad $m=2n-1$ ergibt auf $[-1,1]$

$$\|f-p_m\|_\infty\leq\frac{2M\rho^{-2n}}{1-\rho^{-1}}.$$

Sowohl das normierte Integral $dt/2$ als auch die normierte positive Gaußregel besitzen Operatornorm eins; die Regel ist für $p_m$ exakt. Somit

$$|I(f)-Q_n(f)|\leq\frac{4M\rho^{-2n}}{1-\rho^{-1}}.$$

Diese Abschätzung gilt auch für komplexe $f$. Eine Teleskopsumme über die fünf Achsen benötigt lediglich komplexe Fortsetzung jeweils einer Achse; die übrigen bleiben reell. Die positiven Gewichte verhindern zusätzliche Normverstärkung.

Die Ellipse hat Halbachsen $a=(\rho+\rho^{-1})/2$ und $b=(\rho-\rho^{-1})/2$. Wird nur $t_j=\xi+i\eta$ komplex, gilt pro inzidentem Paar

$$|\operatorname{Im}(t_x-t_y)^2|\leq2b(a+1).$$

Setze $W_j(C)=\sum_{(x,y)\ni j}|c_{xy}|$. Wegen $|E(k)|\leq e^{\max(0,\operatorname{Im}k)}$ und der sechs Maskenterme ist eine Majorante des vollständigen Staubintegranden

$$M_j\leq\frac6{16\sqrt3}\exp\!\left[\frac\beta2b(a+1)W_j(C)\right].$$

Daraus folgt die tatsächlich verwendete, für jede Historie separat ausgewertete Schranke

$$\boxed{e_C(n)\leq\frac{\sqrt3}{2}\frac{\rho^{-2n}}{1-\rho^{-1}}
\sum_{j=0}^4\exp\!\left[\frac\beta2b(a+1)W_j(C)\right].}$$

Für $\rho=2$ gilt $a=5/4,b=3/4$ und in der ganzen Familie $W_j\leq19$. Die Formel ist konservativ: Vorzeichen der BD-Koeffizienten werden in dieser Fehlerschranke nicht zur Auslöschung verwendet. Die Singularität von $\sin k/k$ bei null ist hebbar, die analytische Fortsetzung von $E$ bleibt ganz.

Für die gekoppelte, entkoppelte und gepaarte Differenz summieren wir

$$e_1\leq\sum_C\frac1{33}|A_C|e_C,\quad
e_0\leq\sum_C\frac1{33}|A_{\rm ref}|e_C,\quad
e_\Delta\leq\sum_C\frac1{33}|A_C-A_{\rm ref}|e_C.$$

Die letzte Formel kontrolliert dieselben Staubquadraturdaten direkt; sie ist keine Subtraktion zweier unabhängig geschätzter Fehlerbalken.

## 8. Ballarithmetik, Fehleranteile und unabhängige Prüfungen

Alle Knoten, Gewichte, Wurzeln, trigonometrischen Funktionen, komplexen Gaußpivots und Summen werden mit Python-FLINT/Arb/Acb eingeschlossen. Die Gaußknoten und Gewichte kommen aus `arb.legendre_p_root(..., weight=True)`. Vorzeichen und rechte Halbebenen werden als Intervallaussagen geprüft. Nichtendliche Ausgaben führen zum Abbruch, nicht zu einem Nullbefund. Für Differenzquadrate wird explizite Multiplikation benutzt, damit auch Intervalle um null endlich bleiben.

| Fehleranteil | $\mathcal M_1$ | $\mathcal M_0$ | $\Delta$ |
|---|---:|---:|---:|
| Analytischer Uhrenquadraturfehler, komplexer Betrag | $<1.723\cdot10^{-13}$ | $<2.861\cdot10^{-13}$ | $<2.602\cdot10^{-13}$ |
| Interne arithmetische komplexe Radiusgrenze | $<8.13\cdot10^{-35}$ | $<4.21\cdot10^{-35}$ | $<1.02\cdot10^{-34}$ |
| Dichtequadratur | 0: analytisch | 0: analytisch | 0: analytisch |
| Abel-Extrapolation | 0: analytischer Grenzwert | 0 | 0 |
| Historienauslassung innerhalb der 33er-Familie | 0 | 0 | 0 |

Der analytische komplexe Fehler wird konservativ zu beiden Komponentenradien addiert. Dezimalexporte enthalten ihre eigene nach außen gerundete Darstellung; die 30-stelligen Rohdatenexporte tragen zusätzlich weniger als $10^{-29}$. Die Tabelle in Abschnitt 1 rundet auf zwölf Dezimalstellen und erweitert deshalb auf $10^{-12}$ pro Komponente. Ein eigener Test bestätigt, dass diese veröffentlichten Intervalle die gespeicherten Einschließungen enthalten.

Zwei zusätzliche Kontrollen sind von diesem Fehlerbeweis getrennt:

1. **Andere Ordnung und Präzision:** 48 Knoten, 192 Bit. Die Einschließungen überlappen die primären Ergebnisse; die analytischen Amplitudenfehler sind dann kleiner als $4.37\cdot10^{-18}$. Die primäre Aussage verwendet weiterhin die vorab festgelegte 40er-Regel.
2. **Unabhängige Implementierung:** Eine direkte fünfdimensionale Float64-Regel mit acht Knoten integriert alle 33 gelabelten Historien ohne Orbitreduktion und ohne Ausgangsuhr-Kontraktion. Sie stimmt mit der separat kontrahierten 8er-Regel überein. Ihre Skalarfaktoren werden aus reellen Schur-Eigenwerten und addierten Einzelphasen berechnet. Diese Kontrolle prüft Summationsstruktur, Normierung und Phasen; sie wird nicht als zertifizierte Genauigkeit der primären Rechnung ausgegeben.

27 Tests prüfen diese Punkte, die Quelle aller Matrizen, genaue Maskenfaktoren, Wirkungssymmetrien, das Entkopplungsmodell, die Gaußmomente, die reguläre Dichtefunktion und die Nichtnullentscheidungen. Die Reproduktion führt die primäre Ballrechnung erneut aus und vergleicht die Ergebnisdatei bytegleich.

**Nicht im numerischen Fehlerbudget enthalten:** die physikalische Auswahl der 33 Historien, $c_C$, $\kappa$, Maß und Randpräparation, der Wechsel zu anderen Kopplungen, eine unendliche CST-Summe oder ein Kontinuumsgrenzwert. Dafür gibt es hier keine bezifferte Fehlerschranke.

## 9. Ursache der Änderung: zwei algebraisch getrennte Beiträge

Der Unterschied $\Delta$ ist ein eindeutiger Vergleich der zwei deklarierten Wirkungen. Er allein isoliert aber nicht eine Staub-Skalar-Korrelation: Die Gaußantwort einer mittleren Wirkung ist im Allgemeinen nicht die mittlere Gaußantwort.

Für eine zusätzliche diagnostische Zerlegung setze

$$p_C=\frac{e^{iF_4(C)}}{33},\quad Z=\sum_Cp_C,\quad
d=\sum_Cp_CD_C,\quad \widetilde A=\frac{\sum_Cp_CA_C}{Z}.$$

Hier ist $Z\simeq-0.072101781033-0.343279080577i$ zertifiziert von null getrennt. Die komplexen $p_C/Z$ sind **keine Wahrscheinlichkeiten**. Die primären Amplituden bleiben unnormalisiert bezüglich $Z$. Rein algebraisch gilt

$$\Delta=
\underbrace{\sum_Cp_CD_C(A_C-\widetilde A)}_{R_{\rm conn}=\mathcal M_1-d\widetilde A}
+\underbrace{d(\widetilde A-A_{\rm ref})}_{R_{\rm mean}}.$$

Die eingeschlossenen Werte sind

$$R_{\rm conn}=-0.080381634846+0.002889997971i,$$
$$R_{\rm mean}=-0.096649304929+0.196445234218i,$$

mit höchstens $2\cdot10^{-12}$ Fehler je angezeigter Komponente. Beide sind nicht null. Die erste Größe misst einen zusammenhängenden Amplitudenrest im festen Ensemble, die zweite die Änderung der mittleren Skalarantwort gegenüber der Referenzwirkung. Das liefert eine stärkere Diagnose als die bloße Endpunktdifferenz; es ist weiterhin kein allgemeiner physikalischer Verschränkungs- oder Kausalitätsnachweis.

Es folgt präzise:

- **Mischung:** für diesen $0\to+$-Grundpaketkanal nachgewiesen.
- **Notwendigkeit der untersuchten Kopplung:** verneint, weil $\mathcal M_0\neq0$.
- **Änderung durch die deklarierte Wirkungskopplung:** nachgewiesen, weil $\Delta\neq0$.
- **Bloße mittlere Skalarantwort als vollständige Erklärung der Änderung:** nicht ausreichend, denn auch $R_{\rm conn}\neq0$.
- **Direkte Staub-Skalar-Wechselwirkung als Ursache:** hier nicht getestet; sie fehlt bereits in beiden Wirkungen.

Ein nichtdiagonaler Dichtekernel kann orthogonale Atom- und Positivpakete verbinden, ohne dass eine neu zugeschaltete direkte Wechselwirkung existiert. Deshalb darf das Nichtnullresultat nicht als physikalischer Teilchen- oder Stauberzeugungsprozess umbenannt werden.

## 10. Paritätskontrolle und Status

Die gesamte skalare Wirkung ist quadratisch und unter gemeinsamer Feldumkehr invariant; die Skalarmaße und Regulatoren sind symmetrisch. Der Grundpaketübergang $0_m\to0_m$ ist gerade und daher erlaubt. Ersetzt man nur das ausgehende Paket durch $h_1$, wechselt der Integrand das Vorzeichen. Somit ist

$$\langle A,+,1_m|K_\lambda|A,0,0_m\rangle=0$$

für beide Endpunkte exakt, auch vor der Abel-Entfernung. Das ist die Nullkontrolle; ein kleiner numerischer Wert wird nicht als Beweis einer solchen Paritätsidentität verwendet.

Erstmals liegt für diesen deklarierten endlichen Kontrollpunkt ein vollständig normierter, phasenrichtiger und numerisch eingeschlossener paritätserlaubter Mischungszeuge vor. Die physikalische CST-Übergangsmatrix bleibt **NOT_CONSTRUCTED**, der physikalische $K_{0+}$ bleibt **NOT_COMPUTED** und sämtliche acht physikalischen Gates bleiben **HOLD**. Die numerische Kandidatenamplitude und der physikalische Kern sind verschiedene Statusaussagen.

### Quellen und Reproduktion

- Projektbasis: [Main d2ad347fc6028e5a85f745e95fd5737e840e03a9](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/d2ad347fc6028e5a85f745e95fd5737e840e03a9), PR #279–281. Exakte eingefrorene Pfade und Blobwerte: `provenance.json`.
- [Python-FLINT 0.9.0: Arb](https://python-flint.readthedocs.io/en/latest/arb.html), insbesondere Gauß-Legendre-Knoten und Ballarithmetik; [Acb](https://python-flint.readthedocs.io/en/latest/acb.html), komplexe Einschließungen und analytische Wurzelzweige. Die hier verwendete Tensorfehlerschranke wird in Abschnitt 7 eigenständig bewiesen.
- `python verify.py` prüft Integrität, Herkunft, 27 Tests, primären Ergebnis-Replay und die Ursachendiagnostik. `python verify.py --extended` wiederholt zusätzlich die 48er-Kontrolle.
