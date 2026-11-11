# Lokale Bilanzen und Randbeiträge

Gültigkeit: Baseline aus [MODEL.md](MODEL.md), konstante Massen, lokale
hermitesche Potentialmatrix, hinreichende Regularität. Die Ortsvariablen
(Q,φ) bilden einen Konfigurationsraum; diese Bilanzen sind kein bereits
hergeleiteter räumlicher Energie-Impuls-Tensor der CST.

## Norm und Stratumtransfer

$$n_s=|\psi_s|^2,\quad j_{Q,s}=\frac\hbar{M_Q}\operatorname{Im}
(\psi_s^*\partial_Q\psi_s),\quad
j_{\varphi,s}=\frac\hbar{m_\varphi}\operatorname{Im}
(\psi_s^*\partial_\varphi\psi_s),$$
$$J=\frac2\hbar\operatorname{Im}(G\psi_0^*\psi_+),$$
$$\partial_\chi n_0+\partial_Q j_{Q,0}+\partial_\varphi j_{\varphi,0}=J,
\quad \partial_\chi n_++\partial_Q j_{Q,+}+\partial_\varphi j_{\varphi,+}=-J.$$

Äußere Normflüsse müssen im integrierten Transfer mitgeführt werden. Für
nichtlokales G gilt die einfache lokale Produktform nicht; die integrierte
Rate bleibt (2/ℏ) Im⟨ψ_0,Gψ_+⟩.

## Energie

$$\varepsilon=a|\partial_Q\Psi|^2+b|\partial_\varphi\Psi|^2+
\Psi^\dagger\mathcal V\Psi,$$
$$S_Q=-2a\operatorname{Re}(\partial_\chi\Psi^\dagger\partial_Q\Psi),
\quad S_\varphi=-2b\operatorname{Re}
(\partial_\chi\Psi^\dagger\partial_\varphi\Psi),$$
$$\partial_\chi\varepsilon+\partial_QS_Q+\partial_\varphi S_\varphi
=\Psi^\dagger(\partial_\chi\mathcal V)\Psi.$$

Die rechte Seite verschwindet in der zeitunabhängigen Baseline. Getrennte
Energieanteile H_a müssen eigens definiert werden; ihre Austauschbilanz ist
d⟨H_a⟩/dχ=(i/ℏ)⟨[H,H_a]⟩+⟨∂_χH_a⟩, sofern die Ausdrücke definiert sind.
Die Verteilung einer Wechselwirkungsenergie auf Teilsysteme ist nicht eindeutig.

## Geometrischer Impuls

$$p_Q=\hbar\operatorname{Im}(\Psi^\dagger\partial_Q\Psi),$$
$$\Pi_{Qj}=\frac{\hbar^2}{m_j}\operatorname{Re}
[(\partial_Q\Psi)^\dagger\partial_j\Psi]
-\frac{\hbar^2}{4m_j}\partial_Q\partial_j(\Psi^\dagger\Psi),
\quad m_Q=M_Q,$$
$$\partial_\chi p_Q+\partial_Q\Pi_{QQ}+\partial_\varphi\Pi_{Q\varphi}
=-\Psi^\dagger(\partial_Q\mathcal V)\Psi.$$

Diese Wahl der Flüsse ist explizit festgelegt; äquivalente lokale
Verbesserungsterme benötigen konsistente Randterme. Für reelles g_1 zerfällt
die Volumenkraft in

$$f_{\rm geom}=-\sum_s U_s' n_s,\quad
f_{\rm matter}=-\sum_s m_\varphi\omega_s\omega_s'\varphi^2 n_s,
\quad f_{\rm mix}=-2g_1'\varphi\operatorname{Re}(\psi_0^*\psi_+).$$

Transfer misst den Imaginärteil, Mischkraft den gewichteten Realteil der
Kohärenz. Keines folgt quantitativ aus dem anderen. Bei g_1'=0 entfällt die
direkte Mischkraft; geänderte Kanalbelegungen können weiterhin diagonale
Kräfte verändern. Eine verschwindende ungewichtete Stratumkohärenz schließt
eine gewichtete Mischkraft nicht aus.

## Dirichlet-Wand und endliche Box

Auf der Halbgeraden mit verschwindenden Fernflüssen folgt

$$\frac{dP_Q}{d\chi}=-\langle\partial_Q\mathcal V\rangle+F_{\rm wall},
\quad F_{\rm wall}=\frac{\hbar^2}{2M_Q}
\int d\varphi\sum_s|\partial_Q\psi_s(0,\varphi)|^2.$$

P_Q ist hier die integrierte Impulsdichte, kein stillschweigend angenommener
selbstadjungiger gewöhnlicher Halbgeradenimpuls. Am festen Dirichlet-Rand
verschwinden Norm- und Energiefluss, aber nicht Π_QQ. In einer endlichen Box
kommen der entgegengesetzt orientierte rechte Q-Rand und alle Materieränder
hinzu. Ein reiner Wandbounce kann norm- und energietreu sowie gitterkonvergent sein.

## Optionale geometrieabhängige Modenmasse

Diese Erweiterung ist in der Baseline NICHT übernommen. Wenn sie aus dem
Randkern folgt, ist für gemeinsame m_φ(Q)>0 bereits

$$-\partial_Q\left[\frac{p_\varphi^2}{2m_\varphi(Q)}+
\tfrac12m_\varphi(Q)\omega_s^2(Q)\varphi^2\right]
=\frac{m_\varphi'}{2m_\varphi^2}p_\varphi^2
-\tfrac12\partial_Q(m_\varphi\omega_s^2)\varphi^2.$$

Damit sind kinetische Materierückwirkung, lokale Flüsse, Domäne und mögliche
Verbindungen einer Q-abhängigen Modenbasis neu zu bestimmen. Eine Reskalierung
der Modenkoordinate kann Beiträge umverteilen, aber nicht ohne Kompensation
entfernen. Für nichtlokale oder derivative Off-Diagonalkopplungen müssen auch
die einfachen Mischkraft- und Transferformeln neu abgeleitet werden.
