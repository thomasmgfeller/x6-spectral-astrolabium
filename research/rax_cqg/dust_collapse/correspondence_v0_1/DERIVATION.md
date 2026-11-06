# CST-DUST: Korrespondenz vor der Singularität v0.1

6. November 2026 · CST-DUST-PRE-SINGULARITY-001

## Entscheidung

**Physikalische CST-Korrespondenz: HOLD_NOT_ELIGIBLE; Ausführung: NOT_RUN.**
Der veröffentlichte Kandidat CST-DUST-C1 besitzt noch keinen geschlossenen
gekoppelten Dynamikkern und keine vollständig unabhängig kalibrierten
physikalischen Messadapter. Ein Referenz-PASS kann diese Zulassung nicht ersetzen.

Abgeschlossen sind die Zulassungsprüfung, der vor neuen lokalen Rechnungen
fixierte Toleranz- und Verfeinerungsplan, seine ausführbaren Negativkontrollen,
eine mit Einschließungen geprüfte klassische Integrationsreferenz und eine
gesonderte Messbudgetprüfung für zeitliche Ableitungen. Keine neuen
Zufallsstichproben, dynamischen CST-Ensembles oder kostenpflichtigen Läufe.
Der lokale Planhash ist keine externe Präregistrierung.

## 1. Festgelegtes Prüfgebiet und Zielgrößen

Der Elternvertrag CST-DUST-MC-001 bleibt unverändert: G=c=1, R₀=10,
M∈{1/4,1,4}, ein endlicher homogener Staubball mit mitbewegender Oberfläche
und Schwarzschild-Außenraum gleicher Masse. Im klassischen Referenzmodell gibt
es keine zusätzliche dünne Oberflächenschicht. Periodische Identifikationen
werden nicht verwendet.

\[
T_s(M)=\frac23\sqrt{\frac{R_0^3}{2GM}},\qquad
T_{\rm end}=\frac12\min_M T_s=\frac{5\sqrt5}{3},\qquad
x=T/T_{\rm end}\in[0,1].
\]

Alle Massen werden bei denselben physikalischen Zeiten
x∈{0,1/4,1/2,3/4,1} ausgewertet. Eine individuelle Zeitnormierung T/Tₛ(M)
würde unterschiedliche physikalische Zeiten vergleichen und ist für diesen
Test unzulässig. Die Verwendung von x ist dagegen eine gemeinsame, massenunabhängige
Einheitenumrechnung.

Die Primärgrößen sind Oberflächenradius R, Staubdichte ρ, Hubble-Rate H und
Beschleunigung A=ä/a. Die spätere CST-Radiusmessung benötigt einen unabhängigen
Arealradius- beziehungsweise Geometrieadapter. Ein allein aus V berechneter
Kugelradius ist eine zusätzliche Diagnose unter Kugelsymmetrie und ersetzt
keine unabhängige Geometrierekonstruktion.

Die klassische Referenz ist räumlich homogen, daher stimmt ihre globale
materialseitige Mittelwertdichte mit der lokalen Dichte überein. Für einen
inhomogenen Kandidaten muss die exakt deklarierte gemittelte Observable
verglichen werden. Kandidaten-Oberfläche, Uhr und Messwerte dürfen nicht aus
der zu bestätigenden klassischen Lösung eingesetzt werden.

## 2. Toleranzen, Fehlerbudget und Entscheidung

Die Toleranzen werden aus dem bereits veröffentlichten Elternvertrag übernommen,
nicht nach den hier erzeugten Referenzdaten angepasst:

| Vergleich | Zulässiger normierter Fehler |
|---|---:|
| R, ρ, H und A | jeweils ±5 % des Betrags des Referenzwertes |
| Masse und integrierter Randfluss | ±2 % der gesamten Anfangsmasse M |
| Anfangsgeschwindigkeit und deren Massenantwort | ±5 % |
| Differenz der beiden feinsten physikalischen Stufen | ±2,5 % des Referenzbetrags |

Für H und A ist der Referenzwert negativ, der Fehler wird trotzdem durch
seinen positiven Betrag normiert. Die Toleranz für einen verschwindenden
Materialseitenfluss verwendet M als Skala; es wird niemals durch null dividiert.
Andere Messgrößen mit Referenzwert null brauchen vorab eine eigene absolute Skala.

Für jeden Vergleich gilt: **PASS**, wenn das vollständige gleichzeitige
Fehlerintervall in der geschlossenen Toleranz liegt; **FAIL**, wenn beide
Intervalle disjunkt sind; sonst **HOLD**. Ein überlappender oder zu breiter
Bereich ist kein nachgewiesener physikalischer Widerspruch.

Das vorab fixierte Budget teilt die jeweilige Toleranz auf:

| Beitrag | Anteil der Toleranz | Halbbreitencap beim 5-%-Test |
|---|---:|---:|
| Stichprobe | 40 % | 2,00 % |
| Operator | 15 % | 0,75 % |
| Coarse map / Messabbildung | 10 % | 0,50 % |
| Anfangszustand | 10 % | 0,50 % |
| Rand / Außenraum | 15 % | 0,75 % |
| Numerik | 10 % | 0,50 % |

Die Caps sind Obergrenzen, keine Zusicherung, dass ihre volle Ausschöpfung
noch einen von null verschiedenen gemessenen Bias zulässt. Für PASS muss
das Gesamtintervall einschließlich zentraler Abweichung innerhalb der Toleranz
bleiben. Unbekannte Beiträge sind HOLD, nicht null. Für 2-%- und
2,5-%-Vergleiche gelten dieselben Budgetanteile. Keine nachträgliche
Budgetverschiebung ohne neue Planversion und gegebenenfalls frische Daten.

Die geplante physikalische Familie enthält 240 dynamische Vergleiche
(4 Dichten × 3 Massen × 5 Zeiten × 4 Observablen), 60 Massenvergleiche,
144 Seitenflussvergleiche (drei bereits deklarierte Weltrohre, vier Zeitintervalle),
12 Anfangsgeschwindigkeiten, acht Massenantwortvergleiche und 60 Differenzen
der letzten beiden Stufen: insgesamt **524**. Der globale Fehler erster Art
beträgt höchstens 0,05; die feste Bonferroni-Aufteilung ist 0,05/524 pro Vergleich.
Gleichzeitige Intervalle brauchen keine Unabhängigkeit. Diese Zahl allein
liefert noch kein gültiges Intervallverfahren und keine Stichprobengröße;
beides muss der gekoppelte Kandidat unter seinem physikalischen Maß begründen.

## 3. Was physikalisch abgeglichene Verfeinerung bedeutet

Die geplanten Zähldichten besitzen die Verhältnisse λ/λ₀∈{1,2,4,8}.
In vier Dimensionen gilt ℓ=λ⁻¹/⁴, also
ℓ/ℓ₀∈{1;2⁻¹/⁴;2⁻¹/²;2⁻³/⁴}. Eine Verdopplung der Zähldichte halbiert
nicht die Diskretheitslänge.

Fest bleiben physikalische Einheiten, G, R₀, M, das gemeinsame Zeitraster,
Gebietsdefinition, äußere Randregel, Nichtlokalitätslänge Lₖ, Mittelungslänge
L_cg, Uhr, relationale Detektordefinition, Anfangspräparation und Messkalibrierung.
Die Materialoberfläche ist eine beobachtete Eigenschaft des Kandidaten; ihre
Detektionsregel bleibt gleich, nicht ihr vorab eingesetzter klassischer Radius.
Der Außenraum und der Fehler durch seine Abschneidung gehören zum Abgleich.

Mikroskopische Kopplungen dürfen sich entlang einer **vorher festgelegten**
Abgleich- beziehungsweise Renormierungsvorschrift ändern, sofern deren
physikalische Bedeutung unabhängig begründet ist. Gleiche Dateinamen oder
gleiche dimensionslose Zahlen allein beweisen keinen physikalischen Abgleich.
Wird ℓ als fundamentale physikalische Konstante variiert, ist dies ein Vergleich
verschiedener Modelle und nicht automatisch ein Regulatorgrenzprozess.

Der vorhandene λ₀-Wert der Zählkalibrierung wird ausschließlich in der sekundären
Referenz-Budgetdiagnose wiederverwendet. **Absolute physikalische CST-Dichten,
Lₖ, L_cg, Ensemblegrößen, Seeds, Kopplungsabgleich und vollständiges
Unsicherheitsverfahren sind noch nicht freigegeben.** Der Laufplan darf deshalb
keine neuen Bestätigungsdaten erzeugen.

`matching_guard` prüft vier Metadatensätze. Kontrollfälle mit schrumpfender
Mittelungslänge, schrumpfendem Gebiet bei fester Punktzahl, massenabhängiger
Zeitnormierung, geändertem G, falscher ℓ-Skalierung, nachträglich gelockerten
Toleranzen oder fehlender Abgleichvorschrift erhalten HOLD. Sein positiver
Ausgang heißt ausdrücklich PASS_METADATA_ONLY; er ist kein Physikbeweis.

## 4. Klassische numerische Referenz mit kontrolliertem Fehler

Zur unabhängigen Prüfung des Integrations- und Auswertepfades werden die
bereits klassischen Gleichungen integriert. Setze r=R/R₀ und u=dr/dx. Dann

\[
r'=u,\qquad u'=-\kappa/r^2,\qquad
\kappa=M/72,\qquad r(0)=1,\quad u(0)=-\sqrt M/6.
\]

Die Anfangsgeschwindigkeit folgt dem Anfangszwang und wird nicht für alle
Massen künstlich gleich gehalten. Die Vergleichslösung lautet mit q=√M/4:

\[
s=1-qx,\qquad r=s^{2/3},\qquad u=-\frac{\sqrt M\,r}{6s}.
\]

Verglichen werden die dimensionslosen, durch feste physikalische Einheiten
normierten Größen r, ρ/ρ₀=r⁻³, H T_end=u/r und A T_end²=−κ/r³. Das ist
dieselbe relative Fehlerprüfung wie für die dimensionalen Größen. Masse,
Materiegesetz und gravitative Kraft sind hier eingesetzt, nicht aus CST erzeugt.

Vorab fixiert sind Euler-Gitter mit N∈{128,256,512,1024}, h=1/N. Dies ist
**numerische Schrittverfeinerung** derselben klassischen Gleichung. Diese
vier N-Werte werden ausdrücklich nicht als die vier physikalischen λ-Stufen
ausgegeben.

### Analytische Einschließung

Für alle drei Massen und das gesamte Fenster liegt die exakte Lösung in
D={3/5≤r≤21/20, −1/2≤u≤0}. Denn q≤1/2 impliziert r≥2⁻²/³>3/5 und
|u|≤2¹/³/3<1/2. Auf D ist f(r,u)=(u,−κ/r²) in der Maximumsnorm
Lipschitz-stetig mit L=1: die beiden Zeilensummen des Jacobioperators sind
1 und höchstens 2κ/(3/5)³≤125/243<1.

Außerdem gilt entlang der exakten Lösung

\[
\|y''\|_\infty\le B=\frac{125}{27}\kappa.
\]

Für exakte Euler-Arithmetik folgt aus dem lokalen Taylorrest
e_{n+1}≤(1+h)e_n+Bh²/2 bei e₀=0 die globale Schranke

\[
E_n=\frac{B}{2N}\left[(1+1/N)^n-1\right].
\]

Jeder Euler-Zustand wird mit nach außen gerundeter Decimal-Intervallarithmetik
bei 60 Dezimalstellen eingeschlossen. Alle numerischen Iterierten werden auf
Zugehörigkeit zu D geprüft. Ihre Intervalle, erweitert um ±E_n, schließen
deshalb die exakte ODE-Lösung ein. Die analytischen Kubikwurzeln werden durch
100 Schritte **exakter rationaler Bisektion** eingeschlossen; die Kuben der
rationalen Endpunkte werden unabhängig geprüft. Keine binäre Gleitkommazahl
geht in diese Einschließungsrechnung ein. Druckausgabe und Diagramme runden
erst nach der Entscheidung.

| N | Vergleiche innerhalb des numerischen 0,5-%-Caps | Größte eingeschlossene relative Abweichung |
|---:|---:|---:|
| 128 | 54/60 | 1,033346 % |
| 256 | 58/60 | 0,519993 % |
| 512 | 60/60 | 0,260835 % |
| 1024 | 60/60 | 0,130628 % |

Alle 240 Referenzwerte liegen in ihren berechneten ODE-Einschließungen. Auf den
beiden feinsten Gittern ist der numerische Teil freigegeben. Alle 60 Vergleiche
der beiden feinsten **numerischen** Stufen erfüllen auch die 2,5-%-Bandkontrolle.
Die Aussage gilt für die deklarierten Auswertezeitpunkte; ein physikalischer
CST-Grenzwert oder ein unabhängiger Rückwirkungsnachweis folgt daraus nicht.

Negativkontrollen: Eine für alle Massen gleiche Anfangsgeschwindigkeit verletzt
die Massenantwort in zwei der drei Fälle. Eine um den Faktor 6/5 veränderte
Kraft ergibt bereits bei x=0 eine 20-%-Abweichung der Beschleunigung und wird
in allen drei Fällen zurückgewiesen. Hierfür wird keine modifizierte Dynamik
über das gesamte Zeitfenster simuliert.

## 5. Warum Dichtekalibrierung zeitliche Ableitungen nicht freigibt

Eine sekundäre Diagnose untersucht den vorhandenen ganzen Kugelvolumen-Adapter.
Verwendet werden dieselben symmetrischen (1,1)-Zeitfenster mit tatsächlicher
Abschneidung an den Endpunkten und exakt bekannter Exposition A_exp. Es gilt
V̂=N/(λA_exp). Für die bekannte Referenz ist V/V₀=s² quadratisch in x.

Auf dem festen Raster Δx=1/4 seien D₁ und D₂ die üblichen Dreipunktdifferenzen,
innen zentriert und an den Endpunkten einseitig. Damit sind

\[
H_{\rm diff} T_{\rm end}=\frac{D_1V}{3V},\qquad
A_{\rm diff} T_{\rm end}^2=\frac{D_2V}{3V}-\frac29\left(\frac{D_1V}{V}\right)^2
\]

für das quadratische klassische Referenzvolumen exakt. Der Expositionsfaktor
A_exp und der Beschleunigungsadapter A_diff sind verschiedene Größen.

Für allgemeine CST-Verläufe ist der zeitliche Diskretisierungsfehler dagegen
nicht null. Er benötigt unabhängige Schranken auf die entsprechenden dritten
und vierten zeitlichen Ableitungen oder eine direkt kalibrierte Rate/Expansion.
Eine quadratische Anpassung darf nicht stillschweigend die zu testende
klassische Dynamik voraussetzen.

Angenommen, alle fünf Volumenwerte besitzen relative Fehler höchstens ε<1.
Setze q₁=D₁V/V, q₂=D₂V/V und S_k=Σ_j|w_{kj}|V_j/V. Dann folgt rein algebraisch

\[
b_k=\frac{\epsilon}{1-\epsilon}(S_k+|q_k|),\qquad
|\widehat q_k-q_k|\le b_k,
\]

\[
\frac{|\widehat H_{\rm diff}-H_{\rm diff}|}{|H_{\rm diff}|}\le\frac{b_1}{3|H_{\rm diff}T_{\rm end}|},\qquad
\frac{|\widehat A_{\rm diff}-A_{\rm diff}|}{|A_{\rm diff}|}\le
\frac{b_2/3+(2/9)(2|q_1|b_1+b_1^2)}{|A_{\rm diff}T_{\rm end}^2|}.
\]

Diese hinreichenden Fehlerhüllen werden für sechs **vorab festgelegte** ε-Werte
mit exakten rationalen Zahlen ausgewertet:

| Gemeinsamer relativer Volumenfehler | Größte H-Fehlerhülle | Größte A-Fehlerhülle | Freigabe über diese Hülle |
|---:|---:|---:|---|
| 10⁻² | 62,6894 % | 6489,02 % | keine |
| 10⁻³ | 6,21246 % | 629,021 % | keine |
| 10⁻⁴ | 0,620687 % | 62,7067 % | keine |
| 10⁻⁵ | 0,0620631 % | 6,26872 % | keine |
| 5·10⁻⁶ | 0,0310314 % | 3,13430 % | 5-%-Gesamttoleranz, nicht das 2-%-Stichprobencap |
| 10⁻⁶ | 0,00620626 % | 0,626852 % | auch innerhalb des 2-%-Stichprobencaps |

Die großen Fehlerhüllen sind **keine gemessenen Fehler** und keine notwendigen
Mindestfehler. Die Abschätzung nutzt keine günstige Kovarianz oder gemeinsame
Kurvenanpassung. Direkte Rate-/Beschleunigungsobservablen und bessere statistische
Methoden können andere Anforderungen besitzen.

## 6. Verbindung zur bisherigen Zähldichte

Aus der Poisson-Momentenerzeugenden folgt für ε>0 die zweiseitige hinreichende
Schranke

\[
P(|N/\mu-1|>\epsilon)\le
2\exp\!\left[-\frac{\mu\epsilon^2}{2(1+\epsilon/3)}\right].
\]

Begründung: log E exp[t(N−µ)]=µ(eᵗ−1−t); für 0<t<3 ist
eᵗ−1−t≤t²/[2(1−t/3)]. Chernoff-Optimierung liefert die obere Tail-Hülle,
die untere besitzt die stärkere Schranke exp(−µε²/2) für ε≤1; für ε>1
verschwindet der untere Tail. Die Vereinigungsabschätzung benötigt keine
Unabhängigkeit der Zählfenster.

Für die gesonderte Diagnose werden J=60 Zählwerte (3 Massen × 5 Zeiten ×
4 Dichten), α=0,05 und L=log(2J/α) benutzt. Die konservative gemeinsame
Volumenfehlerhülle einer Stufe folgt aus ihrem kleinsten µ:

\[
\epsilon_{\rm suff}=\frac{L/3+\sqrt{L^2/9+2\mu L}}{\mu}.
\]

Das frühere λ₀=92,894688446 L⁻⁴ liefert für die hier ausgewählten ganzen
Kugelzeitfenster min µ={40000;80000;160000;320000}. Auf der feinsten Stufe
ist ε_suff≈0,00698272. Daraus ergeben sich H- und A-Hüllen von etwa 43,64 %
und 4484,08 %. **Keine der vier geerbten Zähldichten wird über diese
konservative Ableitungs-Budgetprüfung freigegeben.** Das widerlegt weder den
vorherigen Dichtebefund noch den möglichen Erfolg eines besseren Schätzers.

Die zu ε=5·10⁻⁶ gehörige hinreichende Basisdichte wäre etwa 1,4460·10⁹ L⁻⁴;
das entspricht rund 1,32·10¹³ bis 1,99·10¹³ Punkten je vollständigem inneren
Referenzweltrohr. Dieser ε-Wert erfüllt noch nicht das 2-%-Stichprobencap.
Bei ε=10⁻⁶ wären über dieselbe hinreichende Hülle etwa 3,29·10¹⁴ bis
4,97·10¹⁴ Punkte erforderlich. Das sind **Ressourcenprognosen einer gewählten
hinreichenden Methode, keine unteren Komplexitätsschranken**. Es wurden keine
solchen Punktwolken erzeugt. Diese Diagnose begründet keine Anforderung, das
Rechenbudget tatsächlich zu erhöhen.

Die rationalen Sensitivitätshüllen sind exakt. Die logarithmischen
Wahrscheinlichkeits- und Ressourcenwerte werden mit binärer Gleitkommaarithmetik
ausgewertet; sie sind nicht zusätzlich durch Intervallarithmetik zertifiziert.
Das getrennte 60er-Diagnosebudget ersetzt nicht die geplante 524er-CST-Testfamilie.

## 7. Eigenständige Regularität und P3-Datensätze

Für die **eingesetzte deterministische Referenz** gilt im ganzen festen Fenster
ρ/ρ₀=s⁻²≤4. Daher ist (ρ/ρ₀)²≤16. Mit K₀=(GM/R₀³)² gilt
K_in/K₀=60s⁻⁴≤960 und K_out/K₀≤48s⁻⁴≤768. Die einseitigen Grenzwerte
an der Oberfläche sind endlich; eine zusätzliche Materieschicht wird in dieser
Referenz nicht eingesetzt. Die Zähldichte λ tritt in der klassischen Metrik
nicht auf. Das ist keine aus einer CST-Verfeinerung bewiesene Momentenschranke.

Für CST-DUST-C1 bleiben physikalische Operatoren und Domänen, Maß, uniforme
Momentschranken, Tails, Konvergenz und gegebenenfalls kausale Fortsetzung offen.
Regularität bleibt deshalb **HOLD**, unabhängig von den Referenzkontrollen.
Ein Volumenminimum oder kleiner Integrationsfehler darf das nicht überschreiben.

Für jede der 4 geplanten Dichten, 3 Massen und 5 Zeiten liegt ein eigener
P3-Datensatz vor: **60 gültige Bewertungsdatensätze**, jeweils mit eigener
Regularitätsentscheidung. Sie werden durch das unveränderte Eltern-Gate
geprüft. Alle acht physikalischen Gates bleiben HOLD; Ausführungsstatus ist
NOT_RUN. Eine gültige Akte ist keine unabhängige Begutachtung der Physik.

## 8. Konkreter nächster Freigabeschritt

Zunächst muss ein ausführbarer gekoppelter Kandidat die Materiemarken und
Geometrieobservablen aus eigenen Daten erzeugen. Dazu gehören D1–D4
(Träger, Materiegesetz/Maß, Geometriewirkung/Randterme, Zustand/Komposition),
die offenen Teile von D5 (intrinsische Messadapter und Historiengewichte),
D6 (dynamischer Innen-/Rand-/Außenraumabgleich) und D7 (tatsächlicher
physikalischer Laufplan mit gültiger Unsicherheit und erreichbarem Budget).

Für H und A ist insbesondere zu entscheiden, ob direkte Observablen verfügbar
sind oder ein Zeitreihenadapter mit unabhängig kontrolliertem Glättungsbias,
Kovarianz und Differentiationsfehler entwickelt wird. Die klassische
Differentialgleichung darf nicht als Rekonstruktionsregel benutzt werden,
wenn gerade ihre Emergenz getestet werden soll.

Erst danach werden die fehlenden Laufparameter vor frischen Bestätigungsdaten
geschlossen und alle 524 Vergleiche im physikalisch abgeglichenen Test
ausgeführt. Auch ein solcher endlicher PASS wäre noch kein Kontinuumssatz,
keine globale Regularität und kein Nachweis eines Schwarzen Lochs.

## Herkunft und Primärbezug

- [CST-DUST Model Contract v0.1](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/0e47038f15d93edef486fbb68da5dad6bf017221/research/rax_cqg/dust_collapse/model_contract_v0_1/PUBLICATION.md), unveränderte Vertrags- und Gate-Kopie im Paket.
- [Staubstrom-Kalibrierung v0.1, PR #240](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/240), Main-Commit `eabb4ece77563b049caa3a30bacd7b75b850d3a8`; übernommene Eingaben mit SHA-256 dokumentiert.
- Brown und Kuchař, *Dust as a Standard of Space and Time in Canonical Quantum Gravity*, [arXiv:gr-qc/9409001](https://arxiv.org/abs/gr-qc/9409001), [Phys. Rev. D 51, 5600](https://doi.org/10.1103/PhysRevD.51.5600). Kontinuumsbezug; keine Begründung der noch offenen diskreten Materiedynamik.

Euler-Einschließung, Ableitungssensitivität und Poisson-Hülle sind oben direkt
hergeleitet. Dateien mit Referenzwerten oder synthetischen Kontrollfehlern
stellen keine physikalischen CST-Messdaten dar.
