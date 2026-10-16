# RAX-CQG Forschungsarchitektur

Relational kausales Modell und effektive Quantendynamik

Version 0.1 · 16. Oktober 2026 · Projektinitiative Thomas Gfeller

## Ziel und wissenschaftlicher Status

RAX-CQG verbindet das relationale Forschungsprogramm RAX mit kausalen Mengen, einer regulierten Historienamplitude und einer getrennten Rekonstruktions- und Analyseebene. Ziel ist zu untersuchen, ob eine registrierte mikroskopische Dynamik stabile, vorhersagefähige und gegebenenfalls lorentzgeometrische effektive Beschreibungen hervorbringt. Die Architektur legt die mathematischen Schnittstellen fest; sie behauptet weder eine abgeschlossene Quantengravitationstheorie noch einen Nachweis neuer Physik.

Der gewünschte Arbeitsname lautet **Maximales relational kausales Modell emergenter Quantendynamik**. „Maximal“ bezeichnet den Umfang des Programms, keine mathematische Maximalität oder Überlegenheit. Für die wissenschaftliche Kommunikation wird die kürzere Bezeichnung **RAX-CQG Forschungsarchitektur** verwendet.

| Ebene | Was diese Fassung liefert |
|:--|:--|
| Endlicher Kern | Ordnungen, Intervallzählung, Wirkung, Amplitudensummen und positiv konstruierbare Dekohärenzfunktionale |
| Methodik | Vergröberung, prädiktive Destillation, Gegenkontrollen und getrennte Evidenzklassen |
| Forschungsziele | Dynamische Geometrieselektion, stabile Rekonstruktion, effektive Quantendynamik |
| Offene Hauptfragen | Masswahl, Randzustände, unendliche Grenzprozesse, Dimension und Einstein-Dynamik |
| Evidenz | Definitionen und elementare Herleitungen; keine neue Simulationskampagne und keine physische Messung |

Die wichtigsten Trennungen sind verbindlich: Eine angenommene Kausalordnung ist keine emergente Kausalität. Eine quantenmechanische Eingangsstruktur ist keine Herleitung der Quantenmechanik. Ein unterdrückter KR-Sektor beweist keine vierdimensionale Mannigfaltigkeitsdominanz. Ein Spektrum bestimmt eine Geometrie im Allgemeinen nicht eindeutig.

Diese Fassung führt die Regeln des RAX-Forschungsprogramms v0.1 vom 14. Oktober 2026 fort: neutrale Kandidatenprüfung, nichttriviale Reduktion, neue Bestätigungsdaten und getrennte Geometrie- und Singularitätsgates. Die hier vergebenen Kennungen CQG ersetzen keine vorhandenen RAX-U1- oder X6-Testkennungen.

**Leitfrage:** Unter welchen expliziten Annahmen konzentrieren sich physikalisch interpretierbare makroskopische Vorhersagen auf einen Bereich, der eine eindeutige und stabile lorentzsche Rekonstruktion erlaubt?

# 1 Modellobjekte und Geltungsbereich

Eine allgemeine relationale Mikrostruktur ist $R=(V,\mathcal R,\xi)$ mit Trägermenge $V$, einer Familie benannter Relationen $\mathcal R$ und ausdrücklich deklarierten Zusatzdaten $\xi$. RAX-CQG wählt daraus zunächst ein **kausales Profil**:

$$C=(V,\prec),\qquad x\nprec x,\qquad (x\prec y\land y\prec z)\Rightarrow x\prec z.$$

Die strikte Ordnung ist damit asymmetrisch und azyklisch. Lokale Endlichkeit bedeutet

$$I(x,y)=\{z\in V:x\prec z\prec y\},\qquad |I(x,y)|<\infty.$$

Bei endlichem $V$ ist die letzte Bedingung automatisch erfüllt; ihre nichttriviale Bedeutung entsteht erst für unendliche Historien. Ein endlicher DAG repräsentiert einen Causal Set erst zusammen mit seiner transitiven Hülle. Eine Eingabekantenliste muss deshalb als Linkliste oder vollständige Ordnungsrelation gekennzeichnet sein.

Für $N\geq1$ bezeichnet $\Omega_N$ die endliche Menge der Isomorphieklassen von Ordnungen mit $N$ Elementen. Physikalische Grössen müssen unter bijektiver Umbenennung invariant sein. Die zeitliche Orientierung gehört zum Profil; Ordnungsumkehr wird nicht automatisch als Eichäquivalenz behandelt.

Der Kern eines registrierten Modells ist das Paket

$$\mathfrak M_N=(\Omega_N,\mathcal E_N,w_N,s_N,\mathcal D_N,\mathcal O_N,\mathcal C_N,\mathfrak K).$$

Hier sind $\mathcal E_N=2^{\Omega_N}$ die endlichen Ereignisse, $w_N$ das Zählgewicht, $s_N=S_N/\hbar$ die dimensionslose Wirkung, $\mathcal D_N$ ein Dekohärenzfunktional, $\mathcal O_N$ die registrierten Observablen, $\mathcal C_N$ die zugelassenen Vergröberungen und $\mathfrak K$ die Klasse möglicher effektiver Geometrien. Rand- und Materiedaten erweitern $\Omega_N$ und benötigen eigene Masse und Integrationsregeln.

Die Ordnung beschreibt zunächst die mögliche kausale Erreichbarkeit. Sie liefert weder von selbst eine Interventionssemantik noch ein Feldgesetz, eine Metrik oder eine Born-Regel. Die Zuordnung „ein Element entspricht einem Volumenquantum“ ist eine zusätzliche Brückenannahme mit Dichteparameter.

**Zwei getrennte Profile:** CQG-C nimmt die Kausalordnung an. CQG-R untersucht später ihre Entstehung aus allgemeineren Relationen; dazu braucht es einen grösseren Zustandsraum und ein Auswahlgesetz. Erfolge von CQG-C dürfen nicht als Erfolge von CQG-R berichtet werden.

# 2 Skalen und Referenzgeometrien

Eine glatte Referenz ist ein zeitlich orientierter lorentzischer Raum $(M,g)$ mit Signatur $(-,+,+,+)$ im vierdimensionalen Profil. Eine endliche kausal konvexe Beobachtungsregion besitzt Volumen $V_g$. Poisson-Sprinkling mit Dichte $\rho$ ergibt

$$N\sim\operatorname{Poisson}(\rho V_g),\qquad \ell=\rho^{-1/d}.$$

Bedingt auf $N$ werden die Punkte unabhängig nach dem normierten Volumenmass gezogen. Ihre chronologische Ordnung erzeugt den Kontroll-Causal-Set. Bei glatten Referenzen haben exakt nullseparierte Zufallspaare Mass null; numerische Grenzfälle benötigen dennoch eine dokumentierte Regel. Koordinaten dienen dem Referenzgenerator und dem unabhängigen Prüfer, nicht dem Rekonstruktionsalgorithmus.

| Symbol | Bedeutung und Grenze |
|:--|:--|
| $N$ | Ereigniszahl; allein weder physische Zeit noch Grenzwertvorschrift |
| $\ell$ | Diskretisierungslänge im vorgegebenen $d$-Profil |
| $\ell_k$ | Nichtlokalitäts- beziehungsweise Mittelungsskala des Operators |
| $L$ | Beobachtungs- oder Krümmungsskala der Referenz |
| $p$ | Retentionswahrscheinlichkeit einer klassischen Ausdünnung |
| $\varepsilon$ | Ausschliesslich der jeweils bezeichnete numerische oder geometrische Fehler |

Zwei Grenzprozesse werden getrennt geführt. Im **Verfeinerungslimes** bleibt die physische Region fest und $\rho\to\infty$. Im **makroskopischen Grenzbereich** bleibt die fundamentale Diskretheit fest und $L/\ell\to\infty$. Eine wachsende Ereigniszahl bei zugleich wechselndem Volumen oder wechselnden Kopplungen ist ein drittes, gesondert zu spezifizierendes Experiment.

Für gemittelte Krümmungsoperatoren ist eine kontrollierte Hierarchie wie $\ell\ll\ell_k\ll L$ ein Kandidat, keine automatische Fehlerschranke. Die Literatur motiviert nichtlokale Operatoren und deren Kontinuumsnäherung; konkrete Fluktuations- und Randfehler bleiben zu kontrollieren. [1,2]

Die erste Geometriekontrolle verwendet einen vierdimensionalen Minkowski-Diamanten mit Spitzen $(-T/2,0,0,0)$ und $(T/2,0,0,0)$ sowie $V_g=\pi T^4/24$. Die Punktverteilung muss volumenuniform sein. Gleichverteilte Zeitkoordinaten mit nachträglicher räumlicher Befüllung sind ohne die korrekte Gewichtung kein äquivalenter Generator.

Kontrollen in anderen Dimensionen, gekrümmte Referenzen und nichtgeometrische Ordnungen werden separat erzeugt. Eine vierdimensionale Kontrollfamilie beweist keine dynamische Auswahl von $d=4$.

# 3 Diskrete Wirkung und Operatoren

Wir zählen offene Intervalle mit genau $k$ inneren Elementen:

$$N_k(C)=\#\{(x,y):x\prec y,\ |I(x,y)|=k\}.$$

Damit zählt $N_0$ die Links. Der dimensionslose vierdimensionale BDG-Kern lautet in dieser Indexkonvention

$$I_4(C)=N-N_0+9N_1-16N_2+8N_3,$$
$$s_{\mathrm{BDG}}^{(4)}(C)=\gamma_4 I_4(C),\qquad
\gamma_4=\frac4{\sqrt6}\frac{\ell^2}{\ell_p^2},\quad \ell_p^2=8\pi G\hbar.$$

Es gilt $c=1$; $\ell_p$ ist hier die rationalisierte Plancklänge. Andere Plancklängenkonventionen verändern den Vorfaktor. Die Benincasa-Dowker-Glaser-Wirkung ist durch den Zusammenhang diskreter d’Alembert-Operatoren mit $\Box-R/2$ motiviert; sie ist keine universelle Punkt-für-Punkt-Gleichheit mit der Einstein-Hilbert-Wirkung. [1,2]

Für den lokalen Vier-Schichten-Operator gilt

$$B_C\phi(x)=\frac4{\sqrt6\ell^2}\left[-\phi(x)+\sum_{y\prec x}c_{|I(y,x)|}\phi(y)\right],$$
$$c_0=1,\quad c_1=-9,\quad c_2=16,\quad c_3=-8,\quad c_k=0\ (k\geq4).$$

Die Normierung erfüllt exakt $\sum_x[-B_C1](x)=4I_4(C)/(\sqrt6\ell^2)$. Der Krümmungsschätzer $-2B_C1$ enthält den zusätzlichen Faktor zwei. Die nichtlokale Variante $B_{C,\ell_k}$ erhält eine eigene Formel- und Versionskennung; ihre Grenzwerte werden nicht mit dieser lokalen Kontrolle vermischt.

Eine allgemeine Forschungswirkung ist

$$s_\theta(C,\phi)=s_{\mathrm{BDG}}^{(d)}(C)-\lambda_N N+s_m(C,\phi)+s_\partial(C,\phi)+\sum_a g_a O_a(C,\phi).$$

$\lambda_N$ ist eine dimensionslose Volumenkopplung; ihre physische Zuordnung wird im jeweiligen Profil festgelegt. Bei festem $N$ ist ihr Beitrag eine gemeinsame Phase und verändert keine relativen Gewichte innerhalb dieses Sektors. Zusätzliche Operatoren sind neue Modellannahmen und werden durch Ablationen geprüft.

Randbeiträge können bereits aus der BDG-Wirkung entstehen. Ein zusätzliches $s_\partial$ darf sie nicht doppelt zählen. Die Kontinuumsprüfung muss Erwartungswert, Varianz, Region und Randbedingungen getrennt behandeln. [3]

Der Basiskern fixiert $d=4$ in den Koeffizienten. Dimensionsselektion verlangt einen eigenen Vergleich verschiedener Profile oder eine begründete dimensionsunabhängige Dynamik. Ein Strafterm $(d_{\mathrm{spec}}-4)^2$ wäre eine eingebaute Zielpräferenz.

# 4 Historienamplituden und Zählmass

Ein endlicher Causal Set beschreibt bereits eine vollständige diskrete Raumzeitgeschichte. Eine Reihenfolge, in der ein Algorithmus seine Elemente erzeugt, ist nicht automatisch eine zusätzliche physische Zeit. Gleichwertige Erzeugungsreihenfolgen dürfen nicht unbemerkt mehrfach gezählt werden.

Für das reine, endliche Ordnungsprofil definieren wir

$$a_N(C)=w_N(C)e^{is_N(C)},\qquad Z_N(A)=\sum_{C\in A}a_N(C).$$

Zwei mögliche Konventionen sind $w_N(C)=1$ auf Isomorphieklassen und $w_N(C)=1/|\operatorname{Aut}(C)|$. Sie definieren verschiedene Modelle. Für eine isomorphieinvariante Funktion $f$ gilt die exakte Identität

$$\frac1{N!}\sum_{C\ \mathrm{voll\ beschriftet}}f(C)
=\sum_{[C]\in\Omega_N}\frac{f(C)}{|\operatorname{Aut}(C)|}.$$

Begründung: Die Bahn einer Ordnung besitzt $N!/|\operatorname{Aut}(C)|$ verschiedene Beschriftungen. Eine Summe nur über topologisch sortierte Beschriftungen hat andere Multiplizitäten und ist von dieser Identität nicht erfasst.

Für Materie werden ein Raum $\Phi_C$, ein Mass $d\nu_C$ und ein regulatorisch definierter Integrationsweg benötigt. Dann ersetzt $\int_{\Phi_C}e^{is_N(C,\phi)}d\nu_C$ die reine Phasenamplitude. Ein oszillatorisches Integral ist ohne Konvergenz- oder Distributionsvorschrift nicht automatisch definiert.

Eine optionale Summe über Grössen wird zunächst abgeschnitten:

$$Z_{\leq M}(A;z)=\sum_{N=0}^{M}z^N Z_N(A\cap\Omega_N).$$

Der Limes $M\to\infty$ ist ein eigenes Problem. Ein endlicher Cutoff löst weder Divergenzen noch die Definition eines unendlichen quantalen Masses. Auch eine formal passende endliche Familie $\mathcal D_N$ besitzt nicht automatisch eine konsistente Erweiterung auf unendliche Historien. [4]

**Keine Wahrscheinlichkeitsregel:** $Z_N(A)/Z_N(\Omega_N)$ kann komplex oder bei verschwindendem Nenner undefiniert sein. Auch $|Z_N(A)|^2$ ist auf beliebigen disjunkten Ereignissen nicht additiv. Ein positives Hilfsensemble $\pi_N(C)\propto w_N(C)e^{-s_E(C)}$ ist ein klassisches Samplingmodell. Ohne begründete analytische Fortsetzung oder Regewichtung liefert es keine lorentzischen Quantenwahrscheinlichkeiten.

CQG-0 startet mit festem $N$, reinen Ordnungen und offen ausgewiesener Gewichtskonvention. Die spätere Entscheidung für ein physisches Zählmass bleibt Teil der Forschung.

# 5 Dekohärenz und messbare Vorhersagen

Die endliche Quantenebene verlangt ein hermitesches, biadditives und stark positives Funktional $\mathcal D_N$ mit $\mathcal D_N(\Omega_N,\Omega_N)=1$. Starke Positivität bedeutet, dass $[\mathcal D_N(A_i,A_j)]_{ij}$ für jede endliche Ereignisfamilie positiv semidefinit ist. Die Quantalmass-Grösse ist $\mu_N(A)=\mathcal D_N(A,A)$. [4,5]

Eine algebraisch wohldefinierte Konstruktion wählt für jede Historie einen Vektor $v_C=a_N(C)b_C$ in einem gemeinsamen komplexen Hilbertraum. Für $v_A=\sum_{C\in A}v_C$ und $\|v_{\Omega_N}\|^2>0$ setzen wir

$$\mathcal D_N(A,B)=\frac{v_A^\dagger v_B}{\|v_{\Omega_N}\|^2}.$$

Hermitizität, Biadditivität und Normierung folgen unmittelbar. Für beliebige $z_i$ gilt

$$\sum_{ij}\bar z_i\mathcal D_N(A_i,A_j)z_j
=\frac{\|\sum_i z_i v_{A_i}\|^2}{\|v_{\Omega_N}\|^2}\geq0.$$

Das ist ein endlicher Konsistenzsatz, keine Herleitung der physikalisch richtigen Vektoren $b_C$. Randzustände, Verklebung von Regionen und Kovarianz müssen deren Wahl begründen. Sind alle $b_C$ identisch, entsteht im Wesentlichen eine Rang-eins-Amplitude. Sind alle orthogonal, verschwinden die Interferenzterme und damit die Phasenwirkung zwischen Historien. Beide Grenzfälle sind Pflichtkontrollen.

Eine Partition $\{A_r\}$ wird hier nur bei **mittlerer Dekohärenz**, also $\mathcal D_N(A_r,A_s)=0$ für $r\neq s$, als klassische Ergebnisalternative verwendet. Dann gelten $p_N(r)=\mathcal D_N(A_r,A_r)\geq0$ und $\sum_r p_N(r)=1$. Für ungefähre Dekohärenz wird der gesamte Fehler kontrolliert:

$$\epsilon_{\mathrm{dec}}=\sum_{r\neq s}|\mathcal D_N(A_r,A_s)|.$$

Eine kleine paarweise Abweichung reicht bei sehr vielen Alternativen nicht aus. Konditionierung und Interventionsprotokolle werden nur auf einem kompatiblen, dokumentierten Ergebnisraum eingeführt.

Ein reines Hilfsbeispiel mit $v_1=(1,0)$, $v_2=(1+i,0)$ und $v_3=(0,1)$ ergibt $\mu(\{1,2\})=5/6$, während $\mu(\{1\})+\mu(\{2\})=1/2$. Die Partition $\{\{1,2\},\{3\}\}$ dekohäriert und hat Wahrscheinlichkeiten $5/6$ und $1/6$. Damit ist die Nichtadditivität unmittelbar sichtbar.

# 6 Was emergente Quantendynamik bedeuten darf

**Profil CQG-Q:** Ein Dekohärenzfunktional oder eine andere Quantenstruktur wird auf mikroskopischer Ebene angenommen. Untersucht wird, ob daraus eine effektive Quantenfeld- oder Quantensystembeschreibung entsteht. **Profil CQG-EQ:** Die Quantenstruktur selbst soll aus allgemeinerer relationaler Dynamik rekonstruiert werden. Dafür fehlen hier noch die hinreichenden mikroskopischen Prinzipien. Das zweite Profil bleibt eine eigene offene Hypothese.

Eine gewöhnliche positive, lokale verborgene-Variablen-Verteilung mit messwahlunabhängigem $\pi$ hat die Form

$$p(a,b|x,y)=\int\pi(d\lambda)\,p_A(a|x,\lambda)p_B(b|y,\lambda).$$

Für binäre Ergebnisse gilt die CHSH-Schranke $|E_{00}+E_{01}+E_{10}-E_{11}|\leq2$. Messwahlunabhängige lokale Nachverarbeitung erhält diese Form. Eine solche Destillation allein erzeugt daher keine Bell-verletzenden Korrelationen. Ein anderer Ausgang erfordert die transparente Änderung einer Voraussetzung; Nachselektion darf sie nicht verdecken. [6]

Für einen effektiven Quantenrückstand ist mindestens das Paket

$$\mathfrak Q=(\mathcal A,\mathcal S,\mathcal T,\mathcal I,\mathcal M)$$

zu spezifizieren: Observablenalgebra, positive normierte Zustände, Dynamik, Messinstrumente und die Zuordnung zu Ergebnisverteilungen. Nichtkommutativität, Systemkomposition, Positivität bei Kopplung an Hilfssysteme und Vorhersagen auf neuen Protokollen bilden eigenständige Gates. Eine Matrixdarstellung allein genügt nicht.

Als begrenzter Materieanschluss bietet sich ein freies skalares Feld auf festem $C$ an. Ein begründeter retardierter Propagator $G_R$, $G_A=G_R^T$ und $\Delta=G_R-G_A$ ermöglichen eine CCR-Algebra mit $[\hat\phi_x,\hat\phi_y]=i\Delta_{xy}\mathbf1$ in passend normierten Einheiten. Die positive Spektralkomponente von $i\Delta$ liefert einen Kandidaten für die Zweipunktfunktion. Dies ist ein Anschluss an vorhandene kausale Mengenfeldtheorie, keine Herleitung von Materie. [7]

Nullmoden, Randabhängigkeit, Kontinuumsverhalten und Zustandswahl sind separat zu prüfen. Endlich viele Feldorte bedeuten nicht endlichdimensionale Hilberträume: Exakte nichttriviale CCR können wegen der Spur eines Kommutators nicht durch endliche Matrizen dargestellt werden.

Ein weiterer Schutz gegen Scheinschlüsse: Aus $S_m=\tfrac12\phi^T B_C\phi$ folgt bei Variation nur $(B_C+B_C^T)\phi/2$. Ein unsymmetrischer retardierter Operator wird so nicht unverändert zum Euler-Lagrange-Operator. Feldwirkung und kausale Antwort brauchen eine konsistente gemeinsame Konstruktion.

# 7 Sektorselektion und KR Unterdrückung

Die Kleitman-Rothschild-Problematik betrifft den entropisch grossen Anteil stark geschichteter Ordnungen. Veröffentlichte Resultate zeigen unter bestimmten Annahmen eine Unterdrückung von KR- und weiteren geschichteten Sektoren im lorentzischen Pfadsummenansatz. Sie liefern keinen allgemeinen Beweis, dass alle verbleibenden Ordnungen vierdimensionale Raumzeiten approximieren. [8,9]

Für eine elementare Diagnose fixieren wir zwei beschriftete Schichten mit $n_1,n_2$ Elementen und $m=n_1n_2$ möglichen Relationen. Jede Kantenwahl ist eine Zweischichtenordnung; alle Relationen sind Links. Bei $w=1$ und $s=\gamma(N-N_0)$ gilt exakt

$$Z_{n_1,n_2}=e^{i\gamma N}(1+e^{-i\gamma})^m,$$
$$|Z_{n_1,n_2}|=(2|\cos(\gamma/2)|)^m,\qquad
\frac{|Z_{n_1,n_2}|}{2^m}=|\cos(\gamma/2)|^m.$$

Die Identität folgt aus der unabhängigen Summe „Relation fehlt oder ist vorhanden“ für jedes Paar. Die normierte mittlere Phase kann abfallen, während die unnormierte Summe noch wächst. Absolute Unterdrückung dieser Summe verlangt $2|\cos(\gamma/2)|<1$. Bei $\gamma=2\pi q$ mit ganzzahligem $q$ gibt es keine Phasenauslöschung. Diese Diagnose gilt für den festgelegten Zweischichten-Zählraum und ist kein Ersatz für die KR-Asymptotik.

Das Sektorregister umfasst zusätzlich Posts, Ketten, baumartige Ordnungen, gemischte Ordnungen sowie Schichtenfamilien mit wachsender Höhe. Überlappende Klassen benötigen eine feste Zuordnungsregel oder eine explizite Überlappungsanalyse.

Eine nützliche Grössenordnungskontrolle ist die Erweiterung $T(C)$ durch ein neues grösstes Element. Alte Intervalle bleiben erhalten; genau $N$ neue vergleichbare Paare kommen hinzu. Deshalb gilt für den lokalen Kern

$$|I_4(T(C))-I_4(C)|\leq1+16N.$$

Begründung: Jedes neue Paar gehört genau einer Intervallklasse an; der grösste Betrag eines hier verwendeten Koeffizienten ist 16. Das neue grösste Element ist ein Post. Eine reine $N^2$-Asymptotik darf solche Beiträge nicht ohne weiteren Vergleich als erledigt behandeln.

Für quantitative Sektoraussagen werden Amplituden, Quantalmass und Wahrscheinlichkeiten dekohärenter Sektoren getrennt berichtet. Ein kleiner Sektorbeitrag zu $Z$ ist nicht automatisch eine kleine messbare Sektorwahrscheinlichkeit. Dieselbe Unterscheidung gilt für jedes zusätzliche spektrale Straf- oder Projektormodell.

# 8 Relationale und spektrale Observablen

Das erste Observablenregister enthält $N$, die Anzahl vergleichbarer Paare $R=\sum_kN_k$, Höhe, Breite, minimale und maximale Elemente, Postzahl und induzierte Teilordnungsstatistiken. Für $N\geq2$ ist $c_N=2R/[N(N-1)]$ eine dimensionslose Ordnungsdichte. Für $N=1$ wird sie als nicht definiert markiert.

Die längste Kette eines Intervalls ist zusätzlich ein Eigenzeitkandidat. Ein Schätzer $\widehat\tau_d=a_d\ell L$ benötigt eine festgelegte Endpunktzählung und eine separat kalibrierte Konstante $a_d$. Seine Vorhersage wird an neuen Referenzen geprüft; auf einer beliebigen Ordnung wird Kettenlänge dadurch nicht automatisch zur physikalischen Eigenzeit.

Sei $C_{ij}=\mathbf1_{i\prec j}$. Unter einer topologischen Beschriftung ist $C$ strikt obere Dreiecksmatrix. Daher

$$C^N=0,\qquad \operatorname{spec}(C)=\{0,\ldots,0\}.$$

Dies gilt für jede endliche Ordnung. Auch der lokale retardierte Operator aus Abschnitt 3 besitzt bei konstanter Diagonale ausschliesslich diesen einen Diagonalwert als Eigenwert. Seine nichttriviale Struktur liegt in den Matrixelementen und nichtnormalen Eigenschaften, nicht in einer generischen Streuung seiner Eigenwerte.

| Analyseoperator | Mögliche Information | Verbindliche Grenze |
|:--|:--|:--|
| $C^TC$ | Singulärwerte und relationale Muster | Kein vollständiges Ordnungsinvariant |
| $A=C+C^T$ | Spektrum des Vergleichbarkeitsgraphen | Zeitrichtung wird teilweise verworfen |
| $L=\operatorname{diag}(A\mathbf1)-A$ | Positive Graph-Diffusion | Kein lorentzischer d’Alembertian |
| $i\Delta$ | Spektrum eines begründeten Feldkommutators | Benötigt Propagator und Zustandsvertrag |

Eine Pflichtgegenkontrolle ist die V-Ordnung $a\prec b,a\prec c$ gegenüber ihrer Umkehrung. Die erste hat ein minimales, die zweite zwei minimale Elemente; sie sind als orientierte Ordnungen nicht isomorph. Beide haben für $A$ die Eigenwerte $-\sqrt2,0,\sqrt2$, für $L$ die Werte $0,1,3$ und für $C$ die Singulärwerte $\sqrt2,0,0$. Diese Spektren können die Ordnung nicht rekonstruieren.

Ein positiver Hilfsoperator $L$ erlaubt die diagnostische Grösse $P(t)=N^{-1}\operatorname{Tr}e^{-tL}$ und $d_s(t)=-2\,d\log P/d\log t$. Sie gilt nur für diesen Operator, seine Normierung und das geprüfte Skalenfenster. In einem endlichen Graphen entstehen Randregime ohne Kontinuumsinterpretation. Insbesondere ist $d_s\approx4$ kein alleiniger Nachweis einer vierdimensionalen lorentzischen Raumzeit.

Eigenräume werden bei Entartung über Projektoren verglichen. Eigenvektoren benötigen Ausrichtung; Vorzeichen, Phase oder willkürliche Basen innerhalb eines entarteten Unterraums sind keine physikalischen Unterschiede.

# 9 Vergröberung und wirksame Dynamik

Die erste klassische Vergröberung ist Bernoulli-Ausdünnung: Jedes Element bleibt unabhängig mit Wahrscheinlichkeit $p$ erhalten. Auf der erhaltenen Teilmenge wird die **ursprüngliche volle Ordnung eingeschränkt**. Das blosse Löschen von Links kann kausale Beziehungen verlieren, die durch entfernte Zwischenpunkte vermittelt waren.

Für den dadurch definierten Markov-Kern $K_p$ gilt exakt in Verteilung

$$K_qK_p=K_{pq}.$$

Jedes ursprüngliche Element überlebt beide Schritte mit Wahrscheinlichkeit $pq$, unabhängig von den anderen. Bei Poisson-Kontrollen sinkt die Dichte auf $p\rho$. Dieselbe physische Region bleibt erhalten; das physische Volumengewicht je Punkt muss entsprechend angepasst werden.

Diese klassische Identität definiert noch kein quantales Vergröberungsverfahren. Ein stochastischer Kern auf Einzelhistorien bestimmt insbesondere nicht die Interferenz zwischen zwei verschiedenen Historien. Dafür braucht es ein zusätzliches Instrument oder eine begründete Umgebungskonstruktion.

Für eine deterministische Ereignisabbildung $T:\Omega\to\Omega'$ ist dagegen die quantale Bildkonstruktion eindeutig:

$$\mathcal D'(A,B)=\mathcal D(T^{-1}A,T^{-1}B).$$

Hermitizität, Biadditivität, Normierung und starke Positivität bleiben erhalten, weil jede Ereignisfamilie auf ihre Urbilder zurückgeführt wird. Auch Komposition ist exakt verträglich. Dieser Satz gilt ohne die Behauptung, dass die grobe Dynamik wieder dieselbe Wirkungsform besitzt.

Auf Amplitudenebene kann man für feste grobe Historie $c$ definieren

$$a_{\mathrm{eff}}(c)=\sum_{T(C)=c}a(C).$$

Die Darstellung $a_{\mathrm{eff}}=w_{\mathrm{eff}}e^{is_{\mathrm{eff}}}$ ist bei Nullstellen problematisch und bei nichtverschwindenden Amplituden nicht eindeutig. Effektive Wirkungen können komplexe, nichtlokale und neue Mehrpunktterme enthalten. Ein erneuter Fit nur an den BDG-Kern ist eine Trunkationsannahme und benötigt einen Vorhersagefehler.

Eine Renormierungsstudie ergänzt deshalb die Vergröberung um Kopplungsfluss, Reskalierung, Beobachtungsfenster und Fehlerfortpflanzung. Mindestens zwei methodisch verschiedene zulässige Verfahren müssen auf gemeinsame prädiktive Aussagen geprüft werden. Ein System bis zu einer einzigen Restvariable zu reduzieren ist keine Universalitätsevidenz.

Bei Zustandsalgebren wird eine Reduktion durch einen vollständig positiven spurtreuen Kanal und die entsprechende duale Observablenabbildung modelliert. Beliebiges Mittelwertbilden von Matrizen ersetzt diesen Nachweis nicht.

# 10 Destillation als Vorhersagevertrag

Ein RAX-Rückstand ist das Paket aus Observablen, Zuständen, Dynamik, Eingriffen und Messabbildungen. Er muss verworfene mikroskopische Einzelheiten durch eine kleinere, vorhersagefähige Beschreibung ersetzen. Bei einem quantalen Modell werden die verglichenen Ergebnisverteilungen nur aus zulässigen Messinstrumenten oder dekohärenten Ergebnispartitionen gewonnen.

Für einen registrierten Protokollkatalog $\mathcal P$ und eine Skala $r$ lautet das Ziel

$$\sup_{e\in\mathcal P}\operatorname{TV}\bigl(p_{\mathrm{micro}}(\cdot|e),
p_{\mathrm{eff}}(\cdot|e)\bigr)\leq\delta_r.$$

Die totale Variationsdistanz bezieht sich auf gleich bezeichnete Ausgänge. Exakte Gleichheit für alle zugelassenen Protokolle definiert eine operationale Äquivalenzrelation. Nähe innerhalb einer Toleranz ist im Allgemeinen nicht transitiv und wird nicht ohne eigene Clusterregel als Äquivalenz behandelt.

| Gate | Obligatorischer Inhalt |
|:--|:--|
| Nichttrivialität | Eine konstante Reduktion scheitert an mindestens einer vorab bestimmten Kontrolle |
| Vorhersage | Neue Realisationen und zurückgehaltene Eingriffsprotokolle |
| Aufwand | Festgelegter Code, Speicher- oder Laufzeitmassstab und gleiches Vergleichsbudget |
| Skalenstabilität | Grössenfolge, physische Skalierung und mindestens zwei Vergröberungen |
| Negativkontrolle | Ein relevanter anderer Generator bleibt unterscheidbar |
| Mehrschrittprüfung | Eigene Fehlerkontrolle für mehrere Zeit- oder Protokollschritte |

Die reduzierte Vorhersage darf nur den Rückstand und das zugelassene Protokoll sehen. Verborgene Simulatorkoordinaten, Familienkennungen oder Rohdaten dürfen keine verworfene Information zurückführen. Prüfer dürfen solche Daten für die Gegenkontrolle verwenden.

„Destillation“ bedeutet hier prädiktive Modellreduktion. Sie ist nicht automatisch die quanteninformationstheoretische Destillation von Verschränkung; diese würde eine andere Ressourcen- und Operationsklasse verlangen.

Ein Fixpunkt des Flusses ist ein möglicher Befund. Grenzzyklen, mehrere stabile Beschreibungen, Gedächtniseffekte und fehlende Reduktion bleiben zulässige Ergebnisse. Von einer Universalitätsklasse wird erst gesprochen, wenn unterschiedliche Mikromodelle unter kontrollierter Skalierung dieselben spezifizierten Vorhersagen tragen.

Eine Entdeckungsphase darf Toleranzen und Kandidaten entwickeln. Vor der Bestätigungsphase werden sie eingefroren. Nach Sichtung der Prüfdaten geänderte Regeln beginnen eine neue Kampagne. Die Unterscheidung zwischen fehlender Teststärke und einem positiven Äquivalenznachweis bleibt erhalten.

# 11 Geometrische Rekonstruktion

Die Rekonstruktion erhält eine registrierte Klasse $\mathfrak K$ zeitlich orientierter lorentzischer Massräume, eine Volumennormierung und einen tatsächlich definierten Vergleichsabstand $d_L$. Eine geeignete gemessene lorentzsche Gromov-Hausdorff-Konstruktion ist ein möglicher Anschluss. Ihr konkreter Definitionsbereich, die Behandlung von Rändern und gegebenenfalls von Punkten mit identischen Distanzprofilen müssen vor Verwendung festgelegt sein. [10,11]

Zur Festlegung eines endlichen Datenvertrags sei $\mathcal P_k$ die Menge unbeschrifteter $k$-elementiger Ordnungen. Für $k\leq N$ definieren wir

$$t_k(Q;C)=\binom Nk^{-1}\#\{U\subseteq V:|U|=k,\ C|_U\cong Q\}.$$

Für eine Referenz $X$ sei $\nu_k^X(Q)$ die Wahrscheinlichkeit derselben induzierten Ordnung bei $k$ unabhängigen Punkten aus ihrem normierten Volumenmass. Die protokollierte Diskrepanz für einen endlichen Cutoff $K\leq N$ ist

$$d_{\mathrm{ord}}^{K}(C,X)=\sum_{k=1}^{K}2^{-k}\operatorname{TV}(t_k(\cdot;C),\nu_k^X).$$

Alle Grössen sind hier invariant unter Beschriftung. Diese Diskrepanz ist ein Datenvergleich, kein bereits bewiesener geometrischer Abstand. Sie enthält ohne separate Volumeninformation keine absolute Längenskala. Die Summe ausgelassener Gewichte beträgt $2^{-K}$; das begrenzt nur den abgeschnittenen Statistikanteil, nicht automatisch den geometrischen Fehler.

Neuere Rekonstruktionsarbeit verbindet die Gesetze sämtlicher endlicher chronologischer Ordnungsstichproben mit Isometrie. Eine präzise Fassung setzt unter anderem gleiche Dimension $d\geq3$, gleiches endliches Gesamtvolumen, kausale Stetigkeit und Zukunfts-Chronovollständigkeit voraus. Das ist ein Identifizierbarkeitssatz unter Voraussetzungen, kein Algorithmus mit endlicher Stichprobengarantie. [12]

Für Daten $y$ wird die zulässige Rekonstruktionsmenge definiert durch

$$\mathscr R_{N,\epsilon}(y)=\{X\in\mathfrak K:
d_{\mathrm{data}}(y,F_{K_N}(X))\leq\epsilon_N,\ \text{Volumenvertrag erfüllt}\}.$$

$F_{K_N}$ enthält die registrierten Ordnungsstatistiken und bei Bedarf zusätzliche Messkanäle; $d_{\mathrm{data}}$ legt deren Gewichtung fest. Endliche Daten verlangen eine kalibrierte Überdeckungsregel. Die vielen Teilmengen einer einzigen Ordnung sind abhängig und dürfen nicht wie unabhängige Sprinklings gezählt werden.

Die Menge muss entweder kontrolliert approximiert oder ihre nicht untersuchten Bereiche ausgewiesen werden. Eine einzelne gute Optimiererlösung beweist weder Nichtleere der korrekten Modellklasse unter Unsicherheit noch Eindeutigkeit aller Lösungen.

# 12 Dynamische Hauptvermutung als Forschungsziel

Die klassische Hauptvermutung betrifft die makroskopische Eindeutigkeit einer geeigneten Kontinuumsapproximation. RAX-CQG ergänzt eine **dynamische Forschungsfassung DH**, die Auswahl und Eindeutigkeit ausdrücklich verbindet. Sie wird nicht als bereits bewiesene CST-Aussage bezeichnet.

Wir wählen eine Folge zulässiger dekohärenter makroskopischer Ergebnisräume mit Wahrscheinlichkeiten $p_N$ aus Abschnitt 5. Ein Ergebnis $r$ liefert rekonstruierbare Daten $y_N(r)$. Die Grenzvorschrift fixiert Volumen beziehungsweise Beobachtungsskala, Kopplungen, statistische Toleranzen und $K_N\to\infty$ mit $K_N\leq N$.

Für $\delta_N\to0$ definieren wir das gute Ereignis

$$G_N=\{r:\mathscr R_{N,\epsilon}(y_N(r))\neq\varnothing,
\quad\operatorname{diam}_{d_L}\mathscr R_{N,\epsilon}(y_N(r))\leq\delta_N\}.$$

**Vermutung DH:** Für mindestens ein nichttriviales, offen beschriebenes Parameterregime und eine begründete makroskopische Ergebnisstruktur gilt

$$p_N(G_N)\longrightarrow1.$$

Die Nichtleere ist notwendig: Eine leere Rekonstruktionsmenge darf nicht durch eine Durchmesser-Konvention als erfolgreiche Eindeutigkeit zählen. Die Ereignisse müssen in der zugelassenen Ergebnisalgebra liegen. Ohne Dekohärenz wird $\mu_N(G_N)$ nicht stillschweigend als gewöhnliche Wahrscheinlichkeit behandelt. Eine entsprechende Aussage unter einem positiven Hilfsensemble $\pi_N$ bleibt eine Aussage über dieses Ensemble.

Die Kandidatenklasse muss relevante Alternativen enthalten und vorab feststehen. Ihre nachträgliche Einschränkung auf die bevorzugte Geometrie wäre kein Eindeutigkeitsnachweis.

DH wird in vier getrennte Beweisaufgaben zerlegt:

1. **Existenz und Straffheit:** Dynamisch relevante Daten besitzen Rekonstruktionen und entweichen nicht vollständig aus einer kontrollierten Geometrieklasse.
2. **Identifizierbarkeit:** Der vollständige Grenzdatenvertrag trennt geometrisch verschiedene Kandidaten im gewählten Geltungsbereich.
3. **Stabilität:** Kleine Datenfehler führen quantitativ nur zu kleinen geometrischen Unsicherheiten.
4. **Dynamische Konzentration:** Das zugrunde liegende Modell weist den so kontrollierten Ergebnissen asymptotisch das erforderliche Gewicht zu.

Ein nützlicher bedingter Satz: Ist $\mathfrak K$ kompakt und die vollständige Beobachtungsabbildung $F$ stetig und injektiv in einen metrischen Datenraum, besitzt $F^{-1}$ auf $F(\mathfrak K)$ eine gleichmässig stetige Umkehrung. Beweis: Eine stetige Bijektion von einem kompakten Raum in einen Hausdorffraum ist ein Homöomorphismus; auf kompaktem Bild ist die Umkehrung gleichmässig stetig. Die Anwendung auf lorentzische Klassen verlangt gerade den Nachweis dieser Voraussetzungen.

Selbst bewiesenes DH würde keine Einstein-Gleichungen, Materiesektoren oder Auswahl von $d=4$ liefern. Diese benötigen zusätzliche dynamische Grenzwertsätze und unabhängige Vorhersagen.

# 13 Singularitäten und Verlust der Rekonstruierbarkeit

Der Ausdruck „Singularität als Verlust stabiler Rekonstruierbarkeit“ erhält zunächst eine operationale Bedeutung relativ zu Datenvertrag und Kandidatenklasse. Für Störniveau $\eta$ setzen wir

$$\mathscr U_{N,\eta}(y)=\bigcup_{d_{\mathrm{data}}(y,y')\leq\eta}
\mathscr R_{N,\epsilon}(y'),\qquad
\omega_N(y,\eta)=\operatorname{diam}_{d_L}\mathscr U_{N,\eta}(y).$$

Nichtleere der relevanten Mengen ist separat zu verlangen. Stabile Rekonstruktion entlang einer kontrollierten Folge bedeutet beispielsweise

$$\lim_{\eta\downarrow0}\limsup_{N\to\infty}\omega_N(y_N,\eta)=0,$$

zusammen mit konsistenter Datenfehler- und Grenzskalierung. Ein solches uniformes Kriterium ist stärker als die Stabilität eines einzelnen endlichen Fits. Die Reihenfolge der Grenzwerte ist Teil des Vertrags.

| Diagnose | Mathematische Bedeutung | Mögliche alternative Erklärung |
|:--|:--|:--|
| Keine Rekonstruktion | Zulässige Menge leer | Falsche Modellklasse, Datenfehler oder falsches Randmodell |
| Mehrdeutigkeit | Durchmesser bleibt makroskopisch | Unzureichende Observablen oder echte Nichtidentifizierbarkeit |
| Instabilität | Störmodul verschwindet nicht | Schlecht konditioniertes inverses Problem |
| Nichtkonvergenz | Kontrollierte Folge besitzt keinen passenden Grenzpunkt | Ungeeignete Skalierung oder Phasenwechsel |

Diese Diagnosen werden zunächst als **Rekonstruktionsdefekt** geführt. Ihre Deutung als Raumzeitsingularität ist eine weitere Hypothese. Relativistische Singularitätstheoreme beziehen sich auf geodätische Unvollständigkeit unter bestimmten Voraussetzungen; Krümmungsdivergenz und Fortsetzbarkeit sind davon zu unterscheiden. [13]

Eine singuläre klassische Geometrie könnte durch diskrete relationale Daten weiterhin stabil beschrieben sein. Umgekehrt kann eine reguläre Geometrie aufgrund ungeeigneter Daten schlecht rekonstruierbar sein. Es wird daher keine allgemeine Äquivalenz zwischen den beiden Begriffen postuliert.

Der erste S-Test vergleicht reguläre Kontrollfamilien, absichtlich informationsarme Messkanäle und Familien mit unabhängig bekannter geometrischer Grenzpathologie. Er variiert Rauschen, Systemgrösse, Kandidatenklasse und Rekonstruktionsverfahren. Erst ein gegen diese Kontrollen robuster Zusammenhang rechtfertigt eine begrenzte geometrische Interpretation.

Ein Rückstand, der an einer Grenze seine Vorhersagefähigkeit behält, wäre ein wissenschaftlich interessanter Befund. Eine „Auflösung von Singularitäten“ verlangt zusätzlich eine begründete Fortsetzung, konsistente Dynamik und eine klare Messbedeutung.

# 14 X6 als unabhängige Analyseebene

X6 erhält ein versioniertes Datenpaket und die ausdrücklich benannten Analyseoperatoren. Der Historiengenerator, die Wirkungsberechnung und der unabhängige Referenzprüfer bleiben logisch getrennt. Die Unabhängigkeit ist eine überprüfbare Eigenschaft der Implementierung und Datenführung, kein allein durch die Bezeichnung erreichter Zustand.

| Ebene | Verantwortlichkeit | Prüfausgabe |
|:--|:--|:--|
| Generator | Ordnungen, Felder und Randbedingungen gemäss Vertrag | Rohdaten und Stichprobenherkunft |
| Dynamikkern | Wirkung, Amplituden oder Dekohärenzfunktional | Modellvorhersagen und Fehlerbudget |
| Referenzprüfer | Direkte Intervallzählung und unabhängige lineare Algebra | Gegenwerte und Residuen |
| X6 | Spektren, Sektoren, Moden, Korrelationen und Skalenvergleiche | Analysewerte und Diagnosegrenzen |
| Evidenzregister | Verträge, Datenphasen und Status | Nachvollziehbarer Entscheidungsbericht |

Der Export enthält mindestens Modell- und Vertragsversion, Ordnungsdarstellung, $N$, Dichte- und Skalenkonvention, Randprofil, Zählmass, Wirkungsprofil, Operator-ID, Einheiten, Realisations-ID, Seedverfahren, Datenphase und Evidenzklasse. Rohdatenhash und Software-Commit binden die verwendeten Inhalte. Ein Hash allein beweist keine korrekte Rechnung oder rechtzeitige Präregistrierung.

Zugelassene Evidenzklassen sind **analytische Identität**, **synthetische Softwarekontrolle**, **numerische Modellstudie** und **physische Messung**. Ein Befund behält seine Klasse über alle Exporte. Ein bestandener X6-Test hebt ein numerisches Modell nicht auf die Ebene physischer Evidenz.

Pflichtkontrollen umfassen Umbenennung, Ordnungsumkehr, bekannte Spektralkollisionen, entartete Eigenräume, isolierte Komponenten und Änderungen der numerischen Präzision. Fehlende Messgrössen werden als nicht gemessen oder nicht anwendbar gekennzeichnet und nicht mit null ersetzt.

Ein positiver Graph-Laplacian darf als X6-Analyseoperator dienen. Er wird dadurch weder zum physikalischen Hamiltonoperator noch zur lorentzischen Geometrie. Eine spektrale Wirkung darf als neuer Dynamikkandidat untersucht werden, muss dann jedoch eine eigene Modellkennung und Vergleichsläufe ohne diesen Zusatz erhalten.

Entdeckung und Bestätigung verwenden getrennte Realisationen. X6 darf in der Entdeckungsphase informative nächste Protokolle vorschlagen. Die abschliessende Gegenprüfung arbeitet mit eingefrorenen Vorhersagen. Daten, die eine Reparatur auslösen, dienen nicht zugleich als deren unabhängige Bestätigung.

# 15 Erste Prüfkampagne CQG 0

CQG-0 qualifiziert den endlichen mathematischen Kern. Es ist keine Suche nach einer neuen physikalischen Signatur. Für jeden Test werden erwartetes Ergebnis und Fehlermodus vor der Implementierung festgelegt.

| Kennung | Testgegenstand | Abnahme |
|:--|:--|:--|
| CQG-01 | Strikte Ordnung und transitive Hülle | Zyklen werden verworfen; unabhängige Hüllen stimmen exakt überein |
| CQG-02 | Intervallzählung und BDG-Kern | Ganzzahlige Referenzwerte der Tabelle unten exakt |
| CQG-03 | Beschriftung und Zählmass | Observablen invariant; Bahnformel samt Automorphismen exakt |
| CQG-04 | Spektrale Gegenkontrolle | V-Ordnung und Umkehrung kollidieren spektral und werden relational getrennt |
| CQG-05 | Zweischichtensumme | Vollständige kleine Summe stimmt mit der Produktformel überein |
| CQG-06 | Dekohärenzfunktional | Positivität, Normierung und grobe Beispielwahrscheinlichkeiten korrekt |
| CQG-07 | Vergröberung | Klassische Ausdünnung und deterministischer quantaler Pushforward erfüllen ihre jeweils eigene Identität |
| CQG-08 | Replay und Datenvertrag | Identische Eingaben reproduzieren identische exakte Ausgaben |

Die folgenden Werte sind aus den Definitionen direkt herleitbare Sollwerte, keine Ergebnisse einer ausgeführten CQG-Kampagne:

| Ordnung | $N$ | $N_0$ | $N_1$ | $N_2$ | $N_3$ | $I_4$ |
|:--|--:|--:|--:|--:|--:|--:|
| Vierer-Antikette | 4 | 0 | 0 | 0 | 0 | 4 |
| Viererkette | 4 | 3 | 2 | 1 | 0 | 3 |
| Viererdiamant | 4 | 4 | 0 | 1 | 0 | −16 |
| V-Ordnung | 3 | 2 | 0 | 0 | 0 | 1 |
| Umgekehrte V-Ordnung | 3 | 2 | 0 | 0 | 0 | 1 |

Der Viererdiamant hat eine untere Spitze, zwei unvergleichbare Mittelelemente und eine obere Spitze. Sein einziges Intervall mit zwei inneren Elementen erklärt den negativen Kernwert. Eine Wirkung muss hier weder nichtnegativ noch eine Energiefunktion sein.

Die Spektralkontrolle benutzt exakte charakteristische Polynome, wo möglich. Gleitkommarechnungen benötigen eine vorab deklarierte Kombination aus absoluter und relativer Toleranz sowie Residuen. Der bestehende X6-Status wird nicht automatisch auf einen neuen CQG-Adapter übertragen.

Status dieser Fassung: **CQG-0 spezifiziert, nicht ausgeführt**. Die nächste Umsetzung ist klein genug für einen transparenten Referenzkern mit anschliessender unabhängiger Gegenprüfung.

# 16 Forschungsfolge und Entscheidungspunkte

| Stufe | Konkretes Ziel | Grenze eines erfolgreichen Ergebnisses |
|:--|:--|:--|
| CQG-0 | Endlicher Kern und Gegenkontrollen | Korrekte Software und Identitäten |
| CQG-1 | Bekannte Sprinklings rekonstruieren | Kalibrierte Geometrieanalyse auf vorgegebenen Referenzen |
| CQG-2 | Sektorsummen und Phasenauslöschung | Begrenzte Aussagen im deklarierten Ensemble |
| CQG-3 | Physikalisch begründete Rand- und Quantaldynamik | Konsistente endliche Quantenmodellklasse |
| CQG-4 | Vergröberung und Vorhersagedestillation | Nichttriviale effektive Beschreibung im geprüften Bereich |
| CQG-5 | Dynamische Hauptvermutung prüfen | Geometrische Auswahl und Rekonstruktion unter genannten Voraussetzungen |
| CQG-6 | Materie, Einstein-Grenze und Singularitätsdiagnostik | Getrennte theoretische und numerische Resultate |

CQG-1 und CQG-2 können nach CQG-0 unabhängig bearbeitet werden. CQG-5 benötigt sowohl Rekonstruktionskontrolle als auch eine passende Dynamik. Quantale Aussagen aus CQG-4 benötigen CQG-3; klassische Reduktionskontrollen können früher stattfinden. Aussagen über physische Anwendbarkeit benötigen darüber hinaus Messmodelle und Daten.

Vor einem statistischen Bestätigungslauf werden Stichprobenzahl, unabhängige Realisationseinheit, Toleranzen, Testfamilie, gemeinsames Fehlerbudget und Stopregel registriert. Effektgrössen aus der Entwicklung dürfen die Planung bestimmen; die Bestätigungsdaten dürfen es nicht. Bis diese Angaben vollständig sind, bleibt das betreffende statistische Gate **NOT_READY**.

Entscheidungen lauten **SUPPORTED**, **REJECTED**, **INCONCLUSIVE** oder **INVALID**, jeweils mit genau benanntem Geltungsbereich. Ein Ressourcenabbruch erzeugt fehlende Evidenz. Ein schlechter Mischungsdiagnostikwert oder ein unkontrolliertes Vorzeichenproblem verhindert eine positive asymptotische Schlussfolgerung.

Die verbindlichen offenen Hauptprobleme sind die Auswahl des Historienmasses, physikalisch begründete Randvektoren beziehungsweise Klassenoperatoren, konsistente unendliche Erweiterung, ein kontrolliertes nichtperturbatives Quantenregime, geometrische Stabilität und die Herleitung effektiver Feldgleichungen. Kein dieser Probleme wird durch einen Definitionsnamen als gelöst behandelt.

**Arbeitsentscheidung für v0.1:** Zuerst wird der reine endliche Kern ohne zusätzlichen spektralen Strafterm aufgebaut. Danach folgen bekannte Geometrien als blinde Kontrollaufgabe und explizite Sektorvergleiche. Erst auf dieser Grundlage wird die dynamische Rekonstruktionshypothese quantitativ geprüft. Das breite Programm bleibt erhalten, während jeder Schluss einen überprüfbaren Eingang und eine klar begrenzte Bedeutung erhält.

# 17 Quellen und Herkunft

Die folgenden Quellen begründen die übernommenen Anschlussstellen. Die RAX-CQG-spezifischen Verträge, Diagnosebegriffe und die dynamische Fassung DH sind Vorschläge dieser Architektur. Ihre Neuheit gegenüber der gesamten Fachliteratur wird nicht behauptet. Recherche und Fassungsstand: 16. Oktober 2026.

**[1] Benincasa und Dowker.** The Scalar Curvature of a Causal Set. Physical Review Letters 104, 181301 (2010). Verwendet wird die korrigierte arXiv-Fassung v4 von 2011; der Eintrag weist auf einen Druckfehler in der veröffentlichten Fassung hin. <https://arxiv.org/abs/1001.2725v4>

**[2] Dowker und Glaser.** Causal set d’Alembertians for various dimensions. Classical and Quantum Gravity 30, 195016 (2013), arXiv v2. Quelle der hier fixierten Operator-, Intervall- und rationalisierten Plancklängenkonvention. <https://arxiv.org/abs/1305.2588v2>

**[3] Dowker.** Boundary contributions in the causal set action. Classical and Quantum Gravity 38, 075018 (2021). Evidenz und Beispiele zu Randbeiträgen; kein pauschaler Satz über jede endliche Region. <https://arxiv.org/abs/2007.13206>

**[4] Sorkin.** Toward a fundamental theorem of quantal measure theory. Mathematical Structures in Computer Science (online 2012). Behandelt das Erweiterungsproblem quantaler Masse, unter anderem für Causal-Set-Wachstum. [Verlagsseite](https://www.cambridge.org/core/journals/mathematical-structures-in-computer-science/article/abs/toward-a-fundamental-theorem-of-quantal-measure-theory/4C28820DE3B988D6B1147182CF120900).

**[5] Sorkin.** Quantum Mechanics as Quantum Measure Theory. Modern Physics Letters A 9, 3119–3128 (1994). <https://arxiv.org/abs/gr-qc/9401003>

**[6] Bell.** On the Einstein Podolsky Rosen paradox. Physics Physique Fizika 1, 195–200 (1964). Grundlage des Lokalitätsvorbehalts; die CHSH-Form wird hier als elementare Folgerung der angegebenen faktorisierenden Wahrscheinlichkeitsform verwendet. <https://doi.org/10.1103/PhysicsPhysiqueFizika.1.195>

**[7] Johnston.** Feynman Propagator for a Free Scalar Field on a Causal Set. Physical Review Letters 103, 180401 (2009). Anschluss für Feldkommutator und Zustandskonstruktion auf vorgegebenem Causal Set. <https://arxiv.org/abs/0909.0944>

**[8] P. Carlip, S. Carlip und Surya.** Path integral suppression of badly behaved causal sets. Classical and Quantum Gravity (2023), DOI 10.1088/1361-6382/acc50c. <https://arxiv.org/abs/2209.00327>

**[9] P. Carlip, S. Carlip und Surya.** The Einstein-Hilbert Action for Entropically Dominant Causal Sets. Verwendete Fassung arXiv:2311.18238v2, 19. Juni 2024. Die Resultate betreffen die dort definierten geschichteten Klassen und Parameterannahmen. <https://arxiv.org/abs/2311.18238v2>

# 18 Quellen und Statusregister

**[10] Braun und Sämann.** Gromov’s reconstruction theorem and measured Gromov-Hausdorff convergence in Lorentzian geometry. arXiv:2506.10852 (2025). Liefert einen Anschluss für gemessene lorentzische Rekonstruktion und verschiedene Konvergenzbegriffe. <https://arxiv.org/abs/2506.10852>

**[11] Mondino und Sämann.** Lorentzian Gromov-Hausdorff convergence and pre-compactness. arXiv:2504.10380 (2025). Anschluss für lorentzische Kompaktheitsbedingungen; die Bedingungen müssen für eine verwendete Klasse separat überprüft werden. <https://arxiv.org/abs/2504.10380>

**[12] Braun.** Spacetime reconstruction by order and number. Verwendeter Volltext arXiv:2507.01907v1 (2025), insbesondere Theorem 1.4. Die in dieser Architektur genannte Identifizierbarkeit bezieht sich auf die vollständigen Stichprobengesetze und die Voraussetzungen dieses Satzes. <https://arxiv.org/abs/2507.01907v1>

**[13] Senovilla.** A critical appraisal of the singularity theorems. Philosophical Transactions A 380, 20210174 (2022), Preprint 2021. <https://arxiv.org/abs/2108.07296>

**Projektgrundlage.** RAX Relationales Forschungsprogramm, Version 0.1, 14. Oktober 2026, Projektinitiative Thomas Gfeller. Übernommen werden die Regeln für operationale Äquivalenz, prädiktive Reduktion, neutrale Kandidatenprüfung und getrennte Singularitätsdiagnosen. Diese Quelle ist ein eigenes Forschungsprogramm und keine externe Bestätigung seiner Hypothesen.

| Aussage | Status in RAX-CQG v0.1 |
|:--|:--|
| Ordnungs-, Intervall- und Amplitudenkern | Endlich definiert |
| Bahnformel, Nilpotenz, Zweischichtenidentität | Elementar hergeleitet |
| Positivität der Vektorkonstruktion | Elementar hergeleitet |
| Quantaler deterministischer Pushforward | Strukturerhaltung hergeleitet |
| Physische Rand- und Materiedynamik | Offen |
| Eigene KR-Unterdrückung im vollständigen Modell | Nicht nachgewiesen |
| Dynamische Hauptvermutung DH | Forschungsziel |
| Emergenz der Quantenstruktur selbst | Eigenständige offene Hypothese |
| Singularitätsauflösung | Nicht nachgewiesen |
| Neue CQG-Simulations- oder Messdaten | In dieser Fassung keine |

Die Architektur ist vollständig hinsichtlich der benannten Module, Schnittstellen und Beweisaufgaben. Sie ist bewusst keine vollständig gelöste mathematische oder etablierte physikalische Theorie. Ihre erste belastbare Leistung wird ein reproduzierbarer endlicher Kern sein, der auch die vorgegebenen Gegenbeispiele korrekt erkennt.
