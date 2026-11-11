# CST-N0B Quantum Bridge Contract v0.2

Status: Anforderungen definiert; mathematische Konstruktionen und konkrete
CST-Nachweise offen. Die folgenden Bedingungen sind keine bereits geschlossenen
Brücken. RK-, QS- und NUM-Prüfungen sind nicht die acht physikalischen CST-DUST-Gates.

## Vorgeschalteter Anschluss an die bestehende Reihe

Ausgangspunkt bleibt die geerbte Geometrie-Materie-Amplitude samt Maß,
Nullatom, Randpräparation, Intervallkorrekturen und Variationsraum. Die
[kanonische Randrelation](../canonical_boundary_v0_1/DERIVATION.md) ist keine
ausgewählte Evolution. [Randgedächtnis](../boundary_memory_v0_1/PUBLICATION.md)
zeigt, dass ein fester oberer Kragen nicht allgemein genügt.
[Frühere Quantentests](../quantum_structure_v0_1/PUBLICATION.md) schließen
bestimmte rohe Kerndeutungen aus; ihre Annahmen dürfen nicht stillschweigend
durch angepasste Produkte ersetzt werden.

Zu konstruieren sind die Abbildung der ursprünglichen Randzustände auf
(Q,φ,s), ihr Definitions-/Bildbereich, das transportierte Produkt und der
Verlust verworfener Information. Die zwei Strata haben nicht automatisch
gleiche Randträger. Das isolierte Nullatom ist keine Eich-Nullrichtung.
Ein neues quadratisches skalares Materiefeld ist bis zum Nachweis seiner
Beziehung zur bisherigen Staubwirkung eine deklarierte Modellerweiterung.

## Brücke 1: Randkern und Generator

K sei zunächst eine Matrix kovarianter Randmatrixelemente zwischen
nichtorthonormalen Basen. Dann gilt

$$\widetilde K=G_{\rm out}^{-1/2}K G_{\rm in}^{-1/2}.$$

Ist stattdessen eine Koeffizientenabbildung A gegeben, lautet die Formel
G_out^(1/2) A G_in^(-1/2). Die Konvention muss in den Daten stehen. Produkte
sind vor der Unitaritätsprüfung physikalisch zu begründen, nicht nachträglich
auf das gewünschte Ergebnis zu fitten. Ein großer antihermitescher Gram-Anteil
ist ein Eingabefehler, der nicht durch Hermitisierung verborgen werden darf.
Nullrichtungen werden nur mit ausgewiesener Quotientenbegründung entfernt.

Für einen autonomen Hamiltonoperator benötigt der Grenzwert U(0)=I,
U(t+s)=U(t)U(s), U(-t)=U(t)†, beidseitige Unitarität und starke Stetigkeit
auf einem identifizierten Hilbertraum (Stone, S1). Zeitabhängige Generatoren
besitzen stattdessen U(t3,t1)=U(t3,t2)U(t2,t1). Direkte zusammengesetzte Kerne
müssen alle geerbten Kreuzintervalle berücksichtigen. Scheitern sie auf den
reduzierten Randdaten, sind fehlende Randinformation oder Gedächtnis zu prüfen.

Für endliche quadratische Matrizen wird H_full=(iℏ/Δχ)log(tilde K) untersucht.
Der Block H_0+ wird erst NACH dem vollständigen Logarithmus entnommen.
Unitaritäts-, Logarithmus-, Hermitizitäts- und Kompositionsfehler sind getrennt
und auf akkumulierte Zeitintervalle zu beziehen. Ein Defekt O(Δχ) kann einen
endlichen dissipativen Generator verbergen: K=exp(-γΔχ)I ist ein Gegenbeispiel.
Drei Schritte Δχ, Δχ/2, Δχ/4 lassen eine Energieverschiebung um 8πℏ/Δχ
unsichtbar. Ein Spektralfenster oder kontrollierte Zweigfortsetzung ist nötig.

Polarzerlegung ist Diagnose; ihr unitärer Faktor ersetzt den ursprünglichen
Kern nicht physikalisch. Nichtunitarität kann auch durch Basisabschneidung
entstehen. Eine Projektor-/Rigging-Map-Deutung verlangt eigene Beweise.
K_0+(Δχ)=0 an einem Schritt schließt Mischung nicht aus: H=gσ_x hat bei
Δχ=πℏ/|g| den Propagator -I. Nur ein über den relevanten Parameterbereich
erhaltener Stratumraum trägt die entsprechende Entkopplungsaussage.

## Brücke 2: physikalische Uhr

Ein unabhängiges Randuhrpaar und ein nichtdegenerierter Uhrsektor müssen
aus der ursprünglichen Theorie identifiziert werden. Die Wahl kausal monotoner
Uhren kann relative Amplituden ändern und ist keine folgenlose Umbenennung.
Eine vom positiven Staubsektor getragene Uhr kann am Nullatom degenerieren.
Unabhängige Uhr oder mehrere Karten benötigen tatsächliche Übergangsabbildungen
für Zustände, Produkte und Observablen; Kartenwechsel müssen konsistent komponieren.

Die Fourierstütze p_χ+E=0 ist notwendig für den behaupteten linearen Sektor,
aber kein eindeutiger Nachweis eines fundamental linearen Constraints:

$$\delta(p_\chi^2-E^2)=
\frac{\delta(p_\chi-E)+\delta(p_\chi+E)}{2E},\quad E>0.$$

Nach Sektorwahl kann dieselbe Stütze mit anderer Gewichtung entstehen.
Stütze, Gewicht, Uhrsektoren und physikalisches Produkt sind am ursprünglichen
Kern gemeinsam zu prüfen. Die Fouriertransformation einer bereits postulierten
Schrödingerevolution wäre zirkulär. Erst unter den Voraussetzungen in MODEL.md
folgt H_phys≅H_S. Das ist kein Ersatz für die Herkunft des Constraints (S3).

## Brücke 3: Materiewirkung, Schur-Komplement, Mode

Ein d'Alembert-Operator und eine Greenfunktion sind verschiedene Objekte.
Die bekannten retardierten CST-Operatoren (S5) sind nicht automatisch geeignete
symmetrische Matrizen einer reellen quadratischen Wirkung:

$$\nabla_\Phi(\tfrac12\Phi^T M\Phi)=\tfrac12(M+M^T)\Phi.$$

Bei symmetrischem M und invertierbarem Innenblock lautet die stationäre
Elimination M_eff=M_BB−M_BI M_II^(-1) M_IB. Das quantummechanische Gaußintegral
enthält zusätzlich einen Determinanten- und Phasenfaktor. Für reelles
nichtsinguläres M_II mit Fresnel-Regularisierung ist dieser proportional zu
|det M_II|^(-1/2) exp(iπ signature(M_II)/4). Geometrie- oder stratumabhängige
Faktoren ändern relative Amplituden. Nullmoden, Maß und Kontur sind separat
zu behandeln; W>0 macht eine lorentzsche Wirkungs-Hesse-Matrix nicht positiv.

Das verallgemeinerte Eigenproblem K_eff e_α=λ_α G_B e_α definiert zunächst
Randmoden. λ_α/m_φ ist nur dann eine Frequenz zum Quadrat, wenn λ_α als
Potentialsteifigkeit und m_φ als relationale kinetische Normierung identifiziert
sind. Die Randwirkung eines stabilen Oszillators hat bei einer Viertelperiode
Hesse-Eigenwerte ±mω (S6). Daraus darf keine instabile Frequenz abgelesen werden.

Für eine gemeinsame Mode ist eine Auswahlregel vor der Auswertung festzulegen.
Bei veränderlichem Gram-Produkt werden die Operatoren zuerst in einen
gemeinsamen normierten Raum überführt. Für eine kleine hermitesche Störung
liefert r²=Σ_{α≠0}|⟨e_α,ΔK e_0⟩|²/|λ_α−λ_0|² die Normquadratskorrektur
erster Ordnung. r²/(1+r²) ist KEINE allgemeine Fehlerobergrenze. Das archivierte
2×2-Beispiel liefert 0.0099 als Schätzer bei 0.2764 exaktem verworfenem Gewicht.
Direkte Unterraumvergleiche oder passende Davis-Kahan-Schranken (S7) sind nötig.
Eine statische Modenähnlichkeit kontrolliert noch keine dynamische Modenanregung.
Q-abhängige Basis und Masse erzeugen weitere kinetische/Rückwirkungsterme.

## Brücke 4: zulässige und identifizierbare Kopplung

Vor der Anpassung ist ein Symmetrietest nötig: Erhalten quadratische Wirkung,
Maß, Rand- und Uhrkonditionierung Φ→−Φ bei unveränderten Kanalzuständen, dann
kommutieren der reduzierte Kern und sein stetiger Generator mit R_φ. Der
ungerade Term g_1φσ_x wäre dann ausgeschlossen. Die postulierte kombinierte
Parität σ_z R_φ erlaubt ihn, aber diese Wirkung auf die Strata muss aus den
Randzuständen folgen. Quellen, Konditionierung oder intrinsische Stratumparität
können Voraussetzungen ändern; sie müssen offengelegt werden.

Zuerst allgemeine Operatorbasis (I,φ,φ²,p_φ,weitere Materie- und Q-Operatoren),
dann eingeschränkter Fit. Gemeinsame Oszillatorbasis, Phasen und ω_ref sind
festzulegen. Mit ℓ=√(ℏ/(2m_φω_ref)) gelten für G=Aφ+Bp_φ:

$$\frac{\langle m+1|G|m\rangle}{\ell\sqrt{m+1}}=A+i m_\varphi\omega_{ref}B,
\quad \frac{\langle m-1|G|m\rangle}{\ell\sqrt m}=A-i m_\varphi\omega_{ref}B.$$

Beide Richtungen im selben Block sind nötig, ebenso weitere Bänder und
Q-Lokalität. H_0+=H_+0† ersetzt diese Prüfung nicht. Δn=±1 betrifft eine
einzelne lineare Einwirkung, nicht die gesamte endliche Evolution.

R_lin=||H_0+−g_1(Q)φ||_w/||H_0+||_w verlangt vorab deklarierte Gewichte und
Basisbereiche, einen absoluten Fehler und eine Nachweisgrenze am Nullnenner.
Kleine Operatorreste garantieren keine kleinen Kraftreste: In dimensionslosen
Variablen hat δg=ε sin(Q/ε²) kleine Amplitude und große Ableitung. Ableitungen
oder die vollständige Kraft-/Impulsbilanz müssen kontrolliert konvergieren.
Ein kleiner endlicher Basisrest beweist keine globale lokale Kontinuumsform.

## Brücke 5: Verfeinerung und physikalischer Grenzwert

Einbettungen I_N,N' müssen mit den physikalischen Produkten isometrisch und
über mehrere Stufen kompatibel sein. Der Vergleich projizierter H allein
kontrolliert Kopplungen an zusätzliche Zustände nicht. Der zusätzliche Test
U_N≈I†U_N'I ist sinnvoll: Bei exakter Isometrie und unitären U begrenzt
ein Kompressionsfehler ε in Operatornorm die maximale Austrittswahrscheinlichkeit
auf 2ε. Zeitintervall und relevante Zustands-/Energiebereiche sind einzufrieren.

Ein unbeschränkter Hamilton-Grenzwert braucht Domänen-/Stabilitätskontrolle und
eine passende Konvergenz, etwa starke Resolventen- bzw. Propagatorkonvergenz.
Die Schreibweise lim H_phys^N allein konstruiert keinen Hilbertraum.
Bare Koeffizienten c_N∼N^(−α)c_* sind von renormierten Größen c_N→c_*
zu unterscheiden. Drei Punkte mit drei freien Fitparametern bestätigen
keinen Ansatz O_N=O_∞+cN^(−p)+o(N^(−p)).

CST-Elementzahl, Dichte bei festem Gebiet, endliche Basis, Zeit-/Raumgitter
und Fernrand sind getrennte Regulatoren. Ihre Abbildungen auf dieselben
physikalischen Observablen und Unsicherheiten sind festzulegen. Eine
PDE-Gitterstudie ersetzt keine CST-Verfeinerung. Der Ein-Modus-/Zweikanallimes
bleibt zunächst reduziert; klassischer Staubsektor, gemeinsamer Außenraum,
Trapping, Regularität und globale Fortsetzung sind unabhängig zu prüfen.

## Entscheidungskatalog

RK-GRAM, RK-GLUE, RK-UNITARY, RK-HERMITIAN, RK-BRANCH, RK-MIX,
RK-LINEAR, RK-LOCAL, RK-REFINE werden erst auf tatsächlich gelieferten Daten
und einem eingefrorenen Vertrag ausgewertet. Fehlende Daten/Toleranzen ergeben
NOT_RUN/HOLD. Ein scoped FAIL widerlegt nur die deklarierte Interpretation
oder Modellklasse. Kein fehlender oder nichtunitärer Datensatz wird durch
Polarprojektion oder neue Maßanpassung automatisch zu PASS.
