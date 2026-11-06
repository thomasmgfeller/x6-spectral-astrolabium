# Singularitätsauflösung separat prüfen - Regularität v0.2

Stand: 6. November 2026. Eigenständige Fortsetzung der Berichte vom 4. und 5. November. Keine neue CST-Simulation und keine Veröffentlichung auf GitHub in diesem Arbeitsschritt.

## 1. Abgegrenztes Ergebnis

Die Singularitätsauflösung des CST-Staubballs ist **nicht nachgewiesen (HOLD)**. Drei belastbare Aussagen sind getrennt möglich:

1. **Reduzierte Dirichlet-Quantisierung:** Das erste inverse Volumenmoment ist bei endlicher Energie zeituniform beschränkt. Das zweite inverse Moment ist nicht dynamisch geschützt. Ein unten explizit angegebener, anfänglich kontrahierender Zustand mit endlichem zweiten inversen Moment verliert diese Eigenschaft zu jeder späteren Zeit, obwohl sein mittleres Volumen ein strikt positives Minimum erreicht.
2. **Postulierte effektive Metrik:** Das homogene Innere mit `V=b+ct²`, `b>0`, besitzt bei festen Modellparametern beschränkte Dichte und Krümmung sowie einen glatten lokalen Durchgang. Die bisherige Sinus-Skalierung besitzt jedoch keine uniforme Krümmungsschranke für `ν→0`.
3. **Endlicher Ball:** Dasselbe flache homogene Bounce-Innere lässt sich unter den Einstein-Darmois-Israel-Bedingungen nicht ohne Oberflächenschicht an einen Schwarzschild-Außenraum mit konstanter positiver Masse anschließen. Eine konsistente äußere Lösung bleibt zu bestimmen. Das ist ein bedingter Ausschluss genau dieser Kombination, kein Ausschluss anderer Außenräume oder einer vollständig hergeleiteten modifizierten Gravitation.

Der eigentliche Fortschritt gegenüber v0.1 ist das vorwärts entwickelte, anfangs momentenreguläre Gegenbeispiel, ein explizites hinreichendes Kriterium für uniforme inverse Momente und die algebraische Prüfung des räumlichen Ballrandes. Die Hardy-Schranke, der frühere Satz über offene Zeitintervalle und die effektive Krümmungsformel sind übernommene, hier eingeordnete Resultate.

## 2. Modell, Observable und Domäne

Festgelegt sind `q=√V>0`, `H=κℏ²∂q²`, `κ=3πG/2`, das Maß `dq` und die Dirichlet-Erweiterung auf `L²(R+,dq)`. Mit `E=ℏ²∫|ψ'|²dq` ist die erhaltene mittlere Staubmasse `⟨M̂⟩=κE`, wobei `M̂=-H`.

Ein endlicher positiver Erwartungswert wird im Sinn einer quadratischen Form verstanden:

\[
\langle V^{-p}\rangle=\|q^{-p}\psi\|_2^2.
\]

Das verlangt nicht die stärkere Operatorbedingung `ψ∈D(V^{-p})`, die ein weiteres Quadrat erfordert. Normerhaltung durch einen selbstadjungierten Hamiltonoperator erhält nicht automatisch diese gewichteten Domänen.

Für `ψ∈H¹₀(R+)` liefert partielle Integration mit anschließendem Cauchy-Schwarz die Hardy-Ungleichung

\[
\int_0^\infty |\psi|^2/q^2\,dq
=2\Re\int_0^\infty\bar\psi\psi'/q\,dq
\le2\|\psi/q\|_2\|\psi'\|_2,
\qquad \langle V^{-1}\rangle\le4E/\hbar^2.
\]

Die Identität wird zunächst für glatte kompakt getragene Funktionen bewiesen und durch Dichte fortgesetzt. Das spektrale Kalkül erhält die Energiedomäne unter der Zeitentwicklung; die Schranke gilt deshalb für alle Zeiten. Bei gleichmäßig beschränkten Energien gilt sie auch uniform für eine Zustandsfamilie bei festem ℏ und unverändertem Operator. Sie ist nicht uniform für beliebiges `ℏ→0`.

**Physikalische Dichte:** Für eine separat definierte skalare Referenzmasse `m₀` kontrolliert dies den Proxy `m₀⟨V⁻¹⟩`. Im vorliegenden Quantenmodell ist die Masse selbst ein Operator. Eine lokalisierte Packung ist kein scharfer Massenzustand, und `M̂` kommutiert nicht mit `V`. Daher darf `⟨M̂⟩⟨V⁻¹⟩` nicht als hergeleiteter Dichteerwartungswert ausgegeben werden. Ein physikalischer Dichteoperator benötigt Ordnung, Domäne und eine Herleitung aus dem gekoppelten Modell.

Auch `V⁻²` ist kein bereits hergeleiteter Krümmungsoperator. Nur im klassischen, flachen Einstein-Staub-Inneren mit `c=1`, `Λ=0` gilt `R=8πGρ` und `K=(320/3)π²G²ρ²`. Diese klassischen Gleichungen dürfen nicht unbesehen auf einen Quantenzustand übertragen werden.

## 3. Vorwärts entwickeltes Gegenbeispiel

Wähle bei `t=0`

\[
\psi_0(q)=Nq^3e^{-zq^2},\quad z=\alpha-i\beta,
\quad\alpha>0,\quad\beta>0,
\quad N^2=\frac{2(2\alpha)^{7/2}}{\Gamma(7/2)}.
\]

Die ungerade Fortsetzung ist Schwartz; die Norm und alle gewöhnlichen Orts- und Energiemomente sind endlich. Insbesondere

\[
A=\langle q^2\rangle_0=\frac7{4\alpha},\quad
J=2\hbar\int q\Im(\bar\psi_0\psi'_0)dq=\frac{7\hbar\beta}{\alpha},
\quad E=\hbar^2\left(\frac{11\alpha}{5}+\frac{7\beta^2}{\alpha}\right),
\]
\[
\langle V^{-1}\rangle_0=\frac{4\alpha}{5},\qquad
\langle V^{-2}\rangle_0=\frac{16\alpha^2}{15}.
\]

Da `d⟨V⟩/dt|₀=-2κJ<0`, beginnt die Präparation kontrahierend. Die freie ungerade Entwicklung erhält

\[
\langle V(t)\rangle=A-2\kappa Jt+4\kappa^2Et^2,
\quad t_b=J/(4\kappa E),\quad V_b=A-J^2/(4E)>0.
\]

Setze `τ=κℏt`, `D=1-4izτ`. Weil `Re(z)>0`, kann `D` für reelles `t` nicht verschwinden. Die exakte Entwicklung lautet

\[
\psi(q,t)=ND^{-7/2}q(q^2-6i\tau D)e^{-zq^2/D}.
\]

**Herleitung:** `U(t)[q exp(-zq²)]=qD^{-3/2} exp(-zq²/D)`. Ableitung nach `-z` erzeugt `q³ exp(-zq²)` und die angegebene Lösung. Der Zweig wird stetig ab `D(0)=1` gewählt. Für reelles `t` ist `Re(z/D)=α/|D|²>0`, also bleibt der Zustand normierbar.

Am Ursprung folgt

\[
\psi(q,t)=s(t)q+O(q^3),\qquad
s(t)=-6i\tau ND^{-5/2},\qquad
|s(t)|^2=36\tau^2N^2/|D|^5.
\]

Damit ist `s(t)≠0` für jedes `t≠0` und

\[
I_2(\epsilon,t)=\int_\epsilon^\infty |\psi|^2/q^4\,dq
=|s(t)|^2/\epsilon+O(1),\qquad
\langle V^{-2}\rangle_t=\infty\quad(t\ne0).
\]

Der Zustand ist somit am Anfang bezüglich dieses Moments regulär und zu jeder späteren Zeit nicht mehr. Es wird keine Entwicklung von physikalisch bewiesener Krümmungsregularität zu einer Raumzeitsingularität behauptet.

Für `α=κ=ℏ=1`, `β=1/2` erhält man exakt `A=7/4`, `J=7/2`, `E=79/20`, `t_b=35/158`, `V_b=77/79`. Am Minimum ist `|s|²≈9,5788530104`. Das erste inverse Moment bleibt durch `4E=15,8` beschränkt.

## 4. Ausgeführte Kontrolle und unterschiedliche Regulatoren

`verify.py` prüft sechs Zeiten durch adaptive Quadratur, elf untere q-Cutoffs und fünf unabhängige Sinusentwicklungen auf `0<q<16` mit 512 bis 8192 inneren Punkten. Die Sinusentwicklung benutzt die Eigenphasen des festgelegten Operators; es gibt keinen Zeitschrittfehler und keinen an die Vorhersage angepassten Fit. Das endliche obere Intervall ist eine numerische Näherung der Halbgeraden. Der direkte Vergleich mit der exakten Lösung prüft seinen Einfluss an den verwendeten Zuständen und Zeiten, nicht einen allgemeinen Fehlerbeweis.

| q-Cutoff ε | I₂(ε,t_b) | ε I₂ |
|---:|---:|---:|
| 2⁻⁶ | 583,801869 | 9,121904 |
| 2⁻⁸ | 2422,600094 | 9,463282 |
| 2⁻¹⁰ | 9779,073805 | 9,549877 |
| 2⁻¹² | 39205,288903 | 9,571604 |
| 2⁻¹⁴ | 156910,229357 | 9,577040 |

Der Grenzwert ist analytisch `|s|²`; die Zahlen sind Gleitkommakontrollen ohne Intervallzertifikat. Maximale Normabweichung: `8,89·10⁻¹⁶`; maximaler diskreter L²-Abstand der Sinusentwicklung von der exakten Lösung: `9,43·10⁻¹⁶` im ausgeführten Lauf. Diese Maschinengenauigkeit einer glatten Wellenfunktion regularisiert das divergente inverse Moment nicht.

Ein Gitter mit `q_j=jh` liefert dagegen `h Σ|ψ(jh)|²/(jh)⁴ ~ (π²/6)|s|²/h`. Der Koeffizient unterscheidet sich vom Integralausschnitt `q≥ε`. Der Faktor `π²/6` folgt aus `Σj⁻²`; daher dürfen `h` und `ε` nicht ohne Anpassung gleichgesetzt werden. Die fünf Gitter ergeben `h I₂≈14,8444; 15,2965; 15,5256; 15,6408; 15,6986`, gegenüber dem Grenzwert `15,7566`.

## 5. Hinreichendes Kriterium unter Verfeinerung

Sei `V_n(t)>0` eine positive Volumenobservable mit normierter spektraler Einzeitverteilung. Der Index `n` bezeichnet eine explizit physikalisch abgeglichene Verfeinerung, `t∈I` ein festes kompaktes Zeitfenster. Es gebe feste `v₀>0`, `δ>0`, `C<∞` mit

\[
\sup_{n,t\in I}\Pr(V_n(t)\le v)\le C v^{2+\delta}
\quad(0<v\le v_0).
\]

`C` hat die zu den gewählten Volumeneinheiten passende Dimension. Die Voraussetzung schließt ein Atom bei null aus. Die Schichtintegration für positive Zufallsgrößen liefert

\[
\mathbb E[V^{-2}]=2\int_0^\infty F(v)v^{-3}dv
\le v_0^{-2}+\frac{2C}{\delta}v_0^\delta.
\]

Für den abgeschnittenen kleinen Volumenteil gilt zudem

\[
\sup_{n,t}\mathbb E[V_n^{-2};V_n<\eta]
\le C(1+2/\delta)\eta^\delta\longrightarrow0.
\]

Dies beweist uniforme Integrierbarkeit. Bei zusätzlicher schwacher Konvergenz der Volumenverteilungen folgen konvergierende inverse zweite Momente zu jeder festen Zeit; für Konvergenz uniform in der Zeit braucht es zusätzlich zeituniforme Konvergenz der beschränkten abgeschnittenen Observablen. Das Kriterium ist hinreichend, nicht notwendig, und bisher für keinen dynamischen CST-Staubball erfüllt.

Die Gegenbeispielzustände besitzen bei `t≠0` `F(v)~|s(t)|²v^(3/2)/3`, daher sind lokal nur inverse Momente mit `p<3/2` endlich. Anfangs ist `F(v)~N²v^(7/2)/7`; dort sind `p<7/2` endlich. Allgemein gilt bei `ψ(q)~q^r` die Schwelle `p<r+1/2`; Gleichheit führt zur logarithmischen Divergenz.

**Warum endliche Läufe nicht reichen:** Setze `Pr(V_n=ε_n)=ε_n^a`, `Pr(V_n=1)=1-ε_n^a` mit `ε_n=2⁻ⁿ`. Für `a=1` geht das mittlere Volumen gegen eins, während `E[V_n⁻²]` divergiert. Für `a=2` bleiben die Momente beschränkt und gehen gegen zwei, obwohl `V_n` schwach gegen eins konvergiert und dessen inverses Moment eins ist. Erst beispielsweise `a=3` beseitigt diese konkrete kleine-Volumen-Restlast. 24 rationale Kontrollwerte sind im Paket enthalten. Null Treffer bei winzigen Volumina in einem endlichen Monte-Carlo-Lauf beweisen keine Schranke für den gesamten unbeobachteten Tail.

Eine physikalische Krümmungsaussage folgt erst aus einem separat begründeten, zur selben Theorie gehörenden Operator oder geometrischen Funktional. Ein nachgewiesener Formvergleich, etwa `0≤K̂≤a₀+a₂V̂⁻²`, wäre eine mögliche Brücke. Dieser Vergleich wird hier nicht vorausgesetzt oder behauptet. Beschränkte skalare Momente allein beweisen auch keine geodätische Vollständigkeit.

## 6. Effektive Innenmetrik: fester Parameter versus physikalischer Grenzwert

Das getrennt postulierte Sinus-Modell verwendet `V=b+ct²`, `b=M/ρ_B>0`, `c=6πGM`, `a∝V^(1/3)` und `ρ_B=24πGℏ²/ν²`. Hier bezeichnet `M` eine feste klassische Staubmasse; sie ist nicht die Quantenmasse der vorherigen Packung.

Die Staubdichte erfüllt `ρ_d=M/V≤ρ_B`. Aus `H_a=Vdot/(3V)` ergibt sich

\[
K=12[(\dot H_a+H_a^2)^2+H_a^4]
=\frac{16}{27}\frac{c^2}{b^2}\frac{9-6x+5x^2}{(1+x)^4},
\quad x=ct^2/b,
\quad K\le192\pi^2G^2\rho_B^2.
\]

Der globale obere Wert wird bei `t=0` erreicht, weil
`9(1+x)^4-(9-6x+5x²)=42x+49x²+36x³+9x⁴≥0` für `x≥0`.

Bei festen positiven `b,c` ist die Innenmetrik glatt. Die geodätischen Differentialgleichungen lassen sich lokal durch den Bounce fortsetzen. Für die zusätzliche homogene Fortsetzung auf ganz `R³` und alle Zeiten folgt Vollständigkeit aus `dt/dλ=√(ε+P²/a²)` und `a≥a_min>0`; der Ballaußenraum ist davon nicht abgedeckt.

Für numerische Zeitschritte `Δt→0` bei festem `ν` konvergiert die Ablesung zum endlichen Maximum. Bei `ν→0` mit festem `M,G,ℏ` gilt dagegen `ρ_B∝ν⁻²`, `Kmax∝ν⁻⁴`. In Einheiten `6πG=M=ℏ=1` liefert `ν=1,1/2,1/4,1/8` die Krümmungsmaxima `256/3,4096/3,65536/3,1048576/3`. Auf jedem kompakten Bereich abseits `t=0` konvergiert die Metrik zur klassischen Kollaps-/Expansionsform, aber nicht regulär durch `t=0`.

Soll `ν` eine feste physikalische Skala sein, muss die mikroskopische Theorie ihren Wert und die effektive Dynamik begründen. Ein numerischer Meshparameter ist dafür kein Ersatz.

## 7. Endlicher Staubball: explizite Randprüfung

Die bisherige periodische Zelle hat keinen materiellen räumlichen Rand. Nun wird die effektive flache FRW-Metrik auf `0≤r≤r_b` eingeschränkt und ihr Volumen als gesamtes Ballvolumen identifiziert:

\[
ds_-^2=-dt^2+a(t)^2(dr^2+r^2d\Omega^2),\quad
R_b=a r_b,\quad V=4\pi R_b^3/3.
\]

Diese Identifikation ist eine neue zu prüfende metrische Annahme, keine Herleitung des Ball-Hamiltonoperators aus der periodischen Quantisierung. Es wird `k=0` untersucht; Aussagen für räumlich gekrümmte oder inhomogene Innenräume folgen daraus nicht.

Für eine reguläre Naht ohne dünne Materieschicht müssen die induzierte Metrik und die extrinsische Krümmung übereinstimmen: `[h_ab]=[K_ab]=0`. Die geometrische Misner-Sharp-Masse am Rand ist

\[
m_-(t)=\frac{R_b}{2G}(1-g^{ab}\partial_aR\partial_bR)
=\frac{H_a^2R_b^3}{2G}=\frac{\dot V^2}{24\pi GV}.
\]

Die Winkelkomponente liefert innen `K^θ_θ=1/R_b`, außen bei Schwarzschild `K^θ_θ=√(Rdot_b²+1-2GM_+/R_b)/R_b` mit kompatibler Normalenorientierung. Ihre Gleichheit verlangt `Rdot_b²=2GM_+/R_b`, also `m_-=M_+`. Das ist eine notwendige Bedingung, unabhängig von einer Schwarzschild-Koordinatensingularität; die Misner-Sharp-Form ist invariant.

Für den klassischen Ast `b=0`, `c=6πGM` ergibt sich `m_-=M`, konsistent mit dem marginal gebundenen Staubkollaps. Für das Bounce-Innere dagegen

\[
m_-(t)=M\left(1-\frac bV\right),\quad
\frac{M-m_-}{M}=\frac bV=\frac1{1+x}.
\]

Am Bounce ist `m_-=0` bei `M>0`. Für `x=0,1,4,9` beträgt die relative Massenabweichung `100 %,50 %,20 %,10 %`. Keine Verfeinerung des numerischen Gitters beseitigt diese algebraische Abweichung. Auch eine andere konstante Außenmasse kann den zeitabhängigen Wert nicht auf einem offenen Zeitintervall treffen.

Schreibt man dieselbe Metrik als Einstein-Lösung mit effektivem Stress, ergeben sich

\[
\rho_{eff}=\frac M V\left(1-\frac bV\right),\qquad
p_{eff}=-\frac{Mb}{V^2}.
\]

Der endliche, aber nichtverschwindende effektive Druck an der mitbewegten Oberfläche ist eine zweite Darstellung derselben Unverträglichkeit mit einem Vakuumanschluss ohne Oberflächenschicht. Die negative Zusatzdichte und der Druck sind aus der angenommenen Metrik abgelesen, keine hergeleitete CST-Materie. 19 rationale Auswertungen kontrollieren Massen-, Druck- und Krümmungsidentitäten; die allgemeinen Aussagen folgen aus den Formeln.

Mögliche Anschlusswege benötigen eine eigenständige dynamische Herleitung: einen geeigneten nichtvakuumartigen Außenraum, einen endlichen Übergangsbereich oder modifizierte Anschlussgesetze aus derselben gravitativen Wirkung. Eine willkürlich eingesetzte dünne Schale verschiebt die Frage; ihre distributionelle Krümmung lässt sich nicht naiv zu einem Kretschmann-Skalar quadrieren. Umgekehrt ist ein endlicher Sprung der gewöhnlichen Dichte an einem klassischen Staubrand nicht schon eine Singularität: Die extrinsische Krümmung kann dort stetig bleiben.

## 8. Übergang zu CST und Freigabekriterien

Drei Ränder sind zu unterscheiden: `q=0` ist ein Rand im reduzierten Konfigurationsraum; `r=r_b` ist die materielle zeitartige Oberfläche; Anfangs-/Endzeiten sind Begrenzungen des Beobachtungs- oder Wirkungsgebiets. Die früheren Korrekturen endlicher Zeitfenster beseitigen nicht automatisch den materiellen Oberflächenfehler.

Ein kompletter Staubball samt Vakuumaußenraum endet nicht an der Stauboberfläche. Kausalrelationen und Wirkungsintervalle dürfen diese Oberfläche kreuzen. Schneidet man den Außenraum weg, entstehen ein künstlicher zeitartiger Gebietsrand und fehlende Intervalle. In Minkowski-Teilgebieten gibt es analytische und numerische Evidenz für einen divergenten mittleren CST-Wirkungsbeitrag proportional zu `ell⁻¹` an zeitartigen Rändern [L2]. Das ist dort eine gestützte Vermutung, kein hier bewiesener Satz für gekrümmte Staubbälle und keine Krümmungssingularität. Die bekannten raumartigen Randterme [L3] dürfen nicht ohne neue Ableitung als Korrektur der Stauboberfläche eingesetzt werden.

Der nächste CST-Prüfvertrag muss festlegen:

| Prüfung | Für Freigabe erforderlich | Stand |
|---|---|---|
| Physikalische Observablen | Dichte-/Krümmungsoperator, Domäne, Normierung, Klassikbezug | HOLD |
| Zeitentwicklung | Gemeinsamer Materie-Geometrie-Kern und geeignete reguläre Anfangsdaten | HOLD |
| Seltene kleine Volumina | Uniforme Tail- oder gleichwertige Operatorabschätzung über ein festes Zeitfenster | HOLD |
| Numerische Verfeinerung | Mesh, Quadratur, Endgebiete und Stichprobenfehler bei festem Modell getrennt kontrolliert | Referenz geprüft |
| CST-Verfeinerung | `ell=lambda_sprinkle^(-1/4)`; gleiche Masse, Region, Präparation und physikalische Glättung, konsistente Zustands-/Operatorabbildung | NOT_RUN |
| Endlicher Ball | Innen-/Außenraum, vollständige kreuzende Intervalle, Randwirkung und Anschluss aus derselben Theorie | HOLD; einfacher Schwarzschild-Anschluss ausgeschlossen |
| Kausale Fortsetzung | Innenraum, Oberfläche und Außenraum mit einheitlicher Fortsetzungsregel | HOLD |

Bei nichtlokalen Operatoren ist ein nur qualitativ großer Abstand zur Oberfläche kein Fehlerbeweis. Nötig ist eine quantitative Abschätzung ausgelassener Intervalle beziehungsweise Kern-Tails bei festgehaltener physikalischer Mittelungsskala. Der räumliche Randbereich muss mitgemessen werden; ihn immer schmaler auszuschließen beweist keine globale Ballregularität.

Erst eine gemeinsame Kontrolle dieser Punkte rechtfertigt weitergehende Aussagen über eine reguläre globale Raumzeit. Lokale Horizontgrößen auf bereits vorgegebenen Metriken bleiben zulässige Referenzdiagnostik; sie belegen weder Singularitätsauflösung noch einen CST-Schwarzes-Loch-Mechanismus.

## 9. Quellen und Reproduktion

Projektquellen, in ihrer aktuellen Fassung gelesen:

- [P1] Staubball_Bounce_Regularitaet.pdf, 4.11.2026, 3 Seiten. Hardy-Schranke, Zeitintervall-Ausschluss und effektive Innenmetrik.
- [P2] CST_Staubball_Unabhaengige_Bounce_Vorhersage_v0_1.pdf, 5.11.2026, 6 Seiten. Gaußfälle, Vorhersageprüfung, anfangs bereits divergentes zweites Moment.
- [P3] CST_Staubball_Klassik_Rueckwirkung_v0_1.pdf und Historiengewichtung_v0_1.pdf, 5.11.2026. Hamiltonoperator, Maß und Grenzen des Klassikbezugs.
- [P4] https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/rax_cqg/dust_collapse/README.md ; gelesener Blob-SHA `b77d3bbcd80f0ed9b4c8fcde3913c33ebbf1db6d`.

Primärliteratur, am 6.11.2026 geprüft; die neuen Rechnungen oben sind eigene Ableitungen, keine zugeschriebenen Literaturresultate:

- [L1] H. Maeda, Unitary evolution of the quantum universe with a Brown-Kuchař dust, CQG 32 (2015), 235023. https://arxiv.org/abs/1502.06954 . Hintergrund zu reduzierter Staubquantisierung und selbstadjungierten Randwahlen; unsere direkte q-Quantisierung ist eigens festgelegt.
- [L2] F. Dowker, R. Liu, D. Lloyd-Jones, Timelike boundary and corner terms in the causal set action, CQG 42 (2025), 205006. https://arxiv.org/abs/2501.00139 . Verwendet wird die im Abstract ausdrücklich als Vermutung bezeichnete zeitartige Randskalierung in Minkowski-Teilgebieten.
- [L3] M. Buck, F. Dowker, I. Jubb, S. Surya, Boundary Terms for Causal Sets, CQG 32 (2015), 205004. https://arxiv.org/abs/1502.05388 . Raumartige Ränder und Mittelwert-Kontinuumslimit.
- [L4] L. Buoninfante, F. Di Filippo, I. Kolář, F. Saueressig, Dust collapse and horizon formation in Quadratic Gravity, https://arxiv.org/html/2410.05941v2 , Abschnitt 5.1-5.2, insbesondere (44a), (45), (46). Hier nur für die explizite Trennung der üblichen Darmois-Israel-Bedingungen von zusätzlichen Bedingungen modifizierter Gravitation verwendet; deren No-go-Sätze werden nicht auf CST übertragen.
- [L5] I. Jubb, J. Samuel, R. Sorkin, S. Surya, Boundary and Corner Terms in the Action for General Relativity, https://arxiv.org/abs/1612.00149 . Hintergrund zum Variationsprinzip mit verschiedenen Randtypen.

Ausführung: `python3 verify.py`. Erforderlich sind Python 3.10+, NumPy und SciPy; Abbildungen und PDF benötigen zusätzlich Matplotlib und ReportLab. `results/verification.json` und CSV-Dateien enthalten tatsächlich berechnete Werte. Keine Zufallsdaten, keine externe Rechenleistung, keine experimentelle Validierung, keine Intervallzertifizierung. Vor Wiederholung kann `sha256sum -c SHA256SUMS` die archivierten Dateien prüfen. Rundungsletzte Stellen können sich bei anderer Software ändern.
