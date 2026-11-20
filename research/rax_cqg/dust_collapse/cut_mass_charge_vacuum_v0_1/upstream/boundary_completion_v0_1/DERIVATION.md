# CST-DUST: vollständiger Innen-/Rand-/Außenraum-Anschluss

6. November 2026 · CST-DUST-BOUNDARY-001 · v0.1

## 1. Was hier geschlossen wird

**Die klassische Referenz REF-DUST-FB-01 wird als zusammenhängendes
Innen-/Rand-/Außenraum-Modell geschlossen. Der physikalische CST-Anschluss
bleibt HOLD_NOT_ELIGIBLE / NOT_RUN. Regularität und Fortsetzung bleiben
für CST eigenständig HOLD.**

Der Unterschied ist sachlich notwendig: CST-DUST-C1 besitzt noch keine vollständig
festgelegte Materie-Geometrie-Wirkung mit Maß, Außenraumzustand und Randgesetz.
Eine neue äußere Metrik einzusetzen würde diese Lücke durch eine Annahme ersetzen.
Daher werden drei getrennte Ergebnisse ausgegeben:

1. Ein notwendiges und hinreichendes klassisches Anschlusskriterium, explizite
   Realisierung, distributionelle Erhaltung und regulärer Horizontdurchgang.
2. Ein verstärkter Ausschluss des alten Bounce-plus-Schwarzschild-Ansatzes und
   eine bedingte, ausdrücklich nicht-vakuumartige Vergleichskonstruktion.
3. Exakte Kausalset-Kontrollen, die zeigen, warum die periodische Modellzelle
   nicht durch Abschneiden in den endlichen Staubball überführt werden darf.

Grundlage ist Main-Commit `bb59cc03e762b5b2133f4f12fdd975b219bf4406` nach PR 242.
Die Originaleingaben sind in `inputs/` mit SHA-256 dokumentiert. Der lokale
Plan-Freeze vor der Rechnung ist keine externe Präregistrierung. Bekannte
analytische Referenzen sind keine verblindeten Vorhersagen. Keine neuen
physikalischen CST-Ensembles, Zufallsstichproben oder bezahlten Läufe.

## 2. Vollständiges Anschlusskriterium

Signatur $(-+++)$, $c=1$, $G>0$, $M>0$, $\Lambda=0$. Das Innere sei

$$ds_-^2=-d\tau^2+R_b(\tau)^2(d\chi^2+\chi^2d\Omega^2),\quad0\le\chi\le1,$$

mit $R_b>0$, $R_b\in C^2$ und mitbewegter zeitartiger Oberfläche $\Sigma:\chi=1$.
Der Außenraum ist Schwarzschild mit konstanter Masse $M$. Beide Normalen werden
vom Inneren zum gewöhnlichen Außenraum orientiert; keine Wurmloch-Verklebung.
Die gemeinsame induzierte Metrik ist

$$h=-d\tau^2+R_b^2d\Omega^2.$$

Setze $f(R)=1-2GM/R$ und $\beta_+=\sqrt{\dot R_b^2+f(R_b)}>0$.
Die gemischten Komponenten der zweiten Fundamentalform lauten

$$K^{-\tau}{}_{\tau}=0,\quad K^{-\theta}{}_{\theta}=K^{-\phi}{}_{\phi}=1/R_b,$$
$$K^{+\tau}{}_{\tau}=\frac{\ddot R_b+GM/R_b^2}{\beta_+},\quad
K^{+\theta}{}_{\theta}=K^{+\phi}{}_{\phi}=\frac{\beta_+}{R_b}.$$

**Satz im angegebenen Sektor:** Ein Anschluss ohne Oberflächenschicht besteht
auf einem offenen Intervall genau dann, wenn

$$\dot R_b^2=\frac{2GM}{R_b},\qquad \ddot R_b=-\frac{GM}{R_b^2}.$$

Notwendigkeit folgt aus der Winkel- und Zeitkomponente von $[K^i{}_j]=0$.
Umgekehrt ergeben diese Gleichungen $\beta_+=1$ und gleiche Fundamentalformen;
die unten angegebene äußere Einbettung liefert die gemeinsame erste Form.
Auf einem offenen Intervall folgt die zweite Gleichung auch durch Ableiten der
ersten: Wegen $M>0$ kann $\dot R_b$ dort nicht null sein. An einem einzelnen
Prüfpunkt ist die Massenbedingung allein dagegen nicht hinreichend.

Die geometrische Innenmasse ist $m_-=R_b\dot R_b^2/(2G)$.
Damit entspricht die Winkelgleichung $m_-=M$, die Zeitgleichung der geodätischen
Oberfläche. Aus den Einstein-Gleichungen des flachen homogenen Inneren folgen
$\rho=3M/(4\pi R_b^3)$ und $p=0$. Der gewählte kollabierende Ast mit
$R_b(0)=R_0$ ist eindeutig innerhalb dieser Modellklasse:

$$R_b^3=\frac{9GM}{2}(T_s-\tau)^2,\qquad
T_s=\frac23\sqrt{\frac{R_0^3}{2GM}},\quad\tau<T_s.$$

Dies ist weder ein Eindeutigkeitssatz für alle Außenräume noch für CST.
Inhomogenität, Raumkrümmung, nichtmitbewegte Oberflächen, Oberflächenschichten
oder geänderte Feldgleichungen verändern die Voraussetzungen.

## 3. Koordinaten, Außenraum und Durchgang durch R = 2GM

Im Inneren setze $R=\chi R_b$. Ein gemeinsamer ingoing
Painlevé-Gullstrand-Ansatz ist

$$ds^2=-dT^2+(dR+v\,dT)^2+R^2d\Omega^2,$$
$$v_-=h(T)R,\quad h=\frac{2}{3(T_s-T)},\qquad
v_+=\sqrt{2GM/R},\quad\dot R_b=-v_b.$$

$T$ ist die Staubeigenzeit innen und die fortgesetzte $E=1$-Freifallzeit außen.
Außerhalb existiert kein materieller Staubzeitgeber. Die Metrik ist an der
Oberfläche stetig; erste Ableitungen können in diesem Chart springen.

Mit der äußeren ingoing Eddington-Finkelstein-Zeit $V_E$ gilt

$$ds_+^2=-f\,dV_E^2+2dV_EdR+R^2d\Omega^2,$$
$$dV_E=dT+\frac{dR}{1+\sqrt{2GM/R}},\qquad
\frac{dV_E}{d\tau}\bigg|_\Sigma=\frac1{1+\sqrt{2GM/R_b}}.$$

Bei $R_b=2GM$ ist diese Ableitung $1/2$, nicht divergent. Direktes Einsetzen
liefert $-f\dot V_E^2+2\dot V_E\dot R_b=-1$. Ein Divergieren der äußeren
Schwarzschild-Zeit ist somit keine Störung des materiellen Anschlusses.

Die radialen Nullrichtungen aus P4 sind $l=\partial_T+(1-v)\partial_R$ und
$n=\partial_T-(1+v)\partial_R$. Sie stimmen am Rand beidseitig überein.
Außen gilt $l(V_E)=2/(1+v)$, $n(V_E)=0$, also $dR/dV_E=f/2$ für auslaufende
Strahlen. Relativ zur bewegten Oberfläche haben die beiden Richtungen die
Geschwindigkeiten $+1$ und $-1$; der Durchgang ist transversal.

Die klassische Geometrie kann lokal in geeigneten Anschlusskoordinaten mit
stetigen ersten und beschränkten stückweisen zweiten Ableitungen dargestellt
werden. Geodäten setzen sich durch die reguläre Oberfläche und durch $R=2GM$
fort. Das gilt nicht für die spätere Krümmungssingularität bei $T=T_s$.

Der gesamte Außenraum $R\ge R_b(T)$ wird analytisch angegeben, nicht bei einem
willkürlichen Rechenradius abgeschnitten. Für $R\to\infty$ nähert sich die
Metrik asymptotisch flachem Schwarzschild; $m_{MS}=M$ und der Energiefluss ist
null. $M$ ist die asymptotische Masse in üblicher asymptotischer Normierung.
Die intrinsisch flachen PG-Schnitte dürfen nicht mit der Standard-ADM-Formel
unter unzutreffenden asymptotischen Falloff-Annahmen zu einer Nullmasse führen.
Für einen diskreten nichtlokalen CST-Operator ist daraus keine verschwindende
Rechengebietsabweichung ableitbar.

## 4. Feldgleichungen und distributionelle Erhaltung

Aus der vierdimensionalen PG-Metrik werden Christoffel-Symbole, Ricci- und
Einstein-Tensor unabhängig berechnet. Im orthonormalen radialen Rahmen
$u=\partial_T-v\partial_R$, $e=\partial_R$ ergeben sich

$$8\pi G\rho=\frac{v^2+2Rv\partial_Rv}{R^2},\quad G(u,e)=0,$$
$$8\pi Gp_r=\frac{2R\partial_Tv-v^2-2Rv\partial_Rv}{R^2},$$
$$8\pi Gp_t=\frac{\partial_Tv}{R}+\partial_T\partial_Rv
 -(\partial_Rv)^2-v\partial_R^2v-\frac{2v\partial_Rv}{R}.$$

Innen werden daraus $8\pi G\rho=3h^2$ und
$8\pi Gp=2\dot h-3h^2=0$. Außen verschwinden alle Stresskomponenten.

Die einzige mögliche Delta-Krümmung aus den zweiten Ableitungen hat hier den
Koeffizienten $[\partial_Tv]-v_b[\partial_Rv]$. Am Rand sind

$$[\partial_Rv]=-\frac{3v_b}{2R_b},\quad
[\partial_Tv]=-\frac{3v_b^2}{2R_b},$$

also ist dieser Koeffizient exakt null. Der Dichtesprung ist ein endlicher
Sprung ohne dünne Stressschicht. Einseitige Krümmungswerte dürfen verschieden
sein; quadrierte Delta-Distributionen werden nicht eingeführt.

Für $J=\rho u\,\mathbf1_{R<R_b}$ gilt im Inneren die lokale Kontinuitätsgleichung.
Der verbleibende Delta-Anteil von $\nabla_aJ^a$ ist proportional zu
$\rho_b(\dot R_b+v_b)=0$. Die gesamte Staubmasse ist konserviert.
Zudem sind die normale Energiefluss- und Druckprojektion auf beiden Seiten null:
$[T_{ab}u^an^b]=[T_{ab}n^an^b]=0$.

Im Einstein-Wirkungsprinzip liefern EH- plus passend orientierte GHY-Terme die
kanonische Nahtbedingung. Ohne eigene Oberflächenwirkung verschwindet der Sprung
von $K_{ij}-Kh_{ij}$; mit einer Oberflächenwirkung steht rechts ihr Stress.
Die Materieoberfläche ist eine innere Grenzfläche: künstlich eingeführte
innere Randterme müssen bei korrekter Verklebung zusammenpassen. Äußere,
zeitliche und Eckränder sind getrennte Daten. Diese klassische Variation ist
kein hergeleitetes BDG-Materie-Randgesetz.

## 5. Oberflächenschicht: Gleichungen und ein stärkerer Ausschluss

Für eine geometrisch zulässige beliebige $C^2$-Bahn im genannten
Schwarzschild-Sektor liefert die Israel-Gleichung
$S^i{}_j=\operatorname{diag}(-\sigma,p_\Sigma,p_\Sigma)$:

$$\sigma=\frac{1-\beta_+}{4\pi GR_b},$$
$$p_\Sigma=\frac1{8\pi G}\left[
\frac{\ddot R_b+GM/R_b^2}{\beta_+}+\frac{\beta_+-1}{R_b}\right].$$

Mit $M_\Sigma=4\pi R_b^2\sigma$ ist

$$M=m_-+M_\Sigma-\frac{GM_\Sigma^2}{2R_b}.$$

Bei verschwindendem normalen Energiefluss gilt
$\dot\sigma+2\dot R_b(\sigma+p_\Sigma)/R_b=0$.
Auch die normale Druckbilanz wird unabhängig algebraisch geprüft. Diese
Identitäten bestimmen noch kein mikroskopisches Materialgesetz für die Schicht.

Am Bounce ist $\dot R_b=0$. Für $R_b<2GM$ ist $\beta_+^2=f<0$: Es existiert
keine zeitartige Schwarzschild-Einbettung mit dieser Bahn. Bei $R_b=2GM$ und
$\dot R_b=0$ würde die EF-Normierungsbedingung $0=-1$ verlangen. Daher kann
auch eine Israel-Schicht einen zeitartigen Bounce bei $R_b\le2GM$ nicht durch
bloßes Ergänzen eines Oberflächenstresses reparieren.

Bei $R_b>2GM$ ist eine zeitartige Einbettung möglich, aber
$\sigma=(1-\sqrt f)/(4\pi GR_b)>0$; für $\ddot R_b>0$ ist auch $p_\Sigma>0$.
Dies ist kein schichtfreier Anschluss und keine reine Staubschicht.
Ein flaches Einstein-Staubinneres mit positiver Dichte kann seinerseits nicht
bei $H=0$ bouncen. Eine äußere Schicht beseitigt diesen inneren Zwang nicht.

Eine Vaidya-Masse willkürlich durch $M(V_E)=m_-(T)$ zu ersetzen hilft ebenfalls
nicht unter den alten Voraussetzungen: Im ingoing Vaidya-Modell ist
$T_{ab}u^an^b=M_{,V_E}\dot V_E^2/(4\pi R_b^2)$. Bei einer schichtfreien
mitbewegten perfekten Flüssigkeit ohne Wärmefluss ist der innere Wert null;
dann muss $M_{,V_E}=0$ gelten. Strahlung verlangt eine entsprechend geänderte
Materie- und Flussbilanz. Die Aussage ist auf diesen Vaidya-Ansatz begrenzt.

## 6. Bedingte nicht-vakuumartige Vergleichskonstruktion

Der alte verworfene Bounce-Kandidat wird nicht wieder freigegeben. Um den
notwendigen Modellwechsel quantitativ sichtbar zu machen, wird ausschließlich
seine frühere metrische Form $V=b+6\pi GM T^2$ eingesetzt. Mit
$r_*^3=3b/(4\pi)>0$ gilt

$$R_b^3=r_*^3+\frac92GM T^2,\quad
\dot R_b^2=\frac{2GM}{R_b}\left(1-\frac{r_*^3}{R_b^3}\right).$$

**Zusätzlicher Ansatz:** sphärischer statischer Außenraum mit reziproken
Metrikfunktionen, asymptotischer Masse $M$, gewöhnlichem Normalensektor und
schichtfreier geodätischer Randbahn. Der Anschluss legt dann auf den besuchten
Radien $R\ge r_*$ fest:

$$ds_+^2=-f(R)dt^2+f(R)^{-1}dR^2+R^2d\Omega^2,$$
$$f(R)=1-\frac{2GM}{R}+\frac{2GM r_*^3}{R^4},\quad
m_+(R)=M\left(1-\frac{r_*^3}{R^3}\right).$$

$\dot R_b^2+f(R_b)=1$ und
$\ddot R_b+f'(R_b)/2=0$ liefern beide Darmois-Komponenten. Die gleiche
Funktionsform ist aus effektiven OS-Modellen bekannt [3]; hier ist sie eine
bedingte geometrische Rekonstruktion, keine neue CST-Vorhersage.

Unter den gewöhnlichen Einstein-Gleichungen besitzt dieser Außenraum effektiven
anisotropen Stress, in einem radialen orthonormalen Bezugssystem:

$$\rho_+=\frac{3M r_*^3}{4\pi R^6},\qquad
p_{r,+}=-\rho_+,\qquad p_{t,+}=2\rho_+.$$

Der geometrisch erforderliche innere Effektivdruck ist
$p_-=-3M r_*^3/(4\pi R_b^6)=p_{r,+}|_\Sigma$; der normale Energiefluss bleibt
null. Für die geometrische Innenmasse gilt
$\dot m_-=-4\pi R_b^2p_-\dot R_b$. Der äußere Massenanteil erfüllt
$4\pi\int_{R_b}^\infty\rho_+R^2dR=M-m_-$. Am Bounce ist $m_-=0$ und der
Außenanteil $M$. Die konservierte Staubrestmasse und die geometrische Masse
sind in dieser effektiven Konstruktion verschiedene Größen.

Die äußere dominante Energiebedingung ist wegen $p_t=2\rho>\rho$ verletzt;
innen ist $\rho_{eff}+p_{eff}<0$ nahe dem Bounce. Das ist ein Vergleichsmodell
mit effektivem Stress, kein klassischer Staub-plus-Vakuum-Abschluss und noch
kein geschlossenes Materiemodell mit aus derselben Wirkung abgeleiteten Feldern.

Für $z=r_*^3/R^3\in[0,1]$ gilt

$$K_+=\frac{(GM)^2}{R^6}(48-480z+1872z^2)
\le1440\frac{(GM)^2}{r_*^6}.$$

Denn die Ableitung von $z^2(48-480z+1872z^2)$ ist
$96z(1-15z+78z^2)>0$; das Quadratpolynom besitzt die positive Darstellung
$78(z-5/52)^2+29/104$. Innen gilt die zuvor hergeleitete Grenze
$K_-\le108(GM)^2/r_*^6$. Beide sind bei festem $r_*>0$ endlich, aber nicht
uniform für $r_*\to0$. Eine Änderung von $r_*$ ist keine numerische Verfeinerung.

$f$ hat sein Minimum bei $R=4^{1/3}r_*$ mit
$f_{min}=1-3GM/(2\,4^{1/3}r_*)$. Je nach Skala gibt es zwei einfache Nullstellen,
eine doppelte oder keine. Nullstellen der statischen Koordinaten sind keine
Krümmungssingularitäten. Ein einziger ingoing PG-Chart deckt den Bounce und
anschließende Expansion nicht automatisch ab; sein Vorzeichenwechsel ist kein
hinreichender Nachweis einer physischen Stoßwelle [3]. Eine vollständige globale
Verklebung, die Auswahl asymptotischer Regionen und die Stabilität möglicher
innerer Horizonte sind hier **nicht** qualifiziert. Aus lokalen Nahtgleichungen
folgen diese Aussagen nicht.

## 7. Vollständige klassische Zukunft: ausdrücklich zusätzliche Annahme

Das bisher geprüfte Fenster bleibt $0\le T\le T_E=5\sqrt5/3$.
Zusätzlich wird die bekannte analytische klassische Lösung bis $T_s$ fortgesetzt
und ein unveränderter Schwarzschild-Außenraum bis zur zukünftigen Nullunendlichkeit
angenommen. Kein Bounce, keine neue Schicht und kein zusätzlicher Strahlungsfluss.
Erst unter dieser Zukunftswahl ist ein Ereignishorizont bestimmt.

Mit $\Delta=T_s-T$ und $A=(9GM/2)^{1/3}$ ist der innere Erzeuger

$$\chi_E(T)=3-\frac3A\Delta^{1/3}
=3\left[1-\left(\frac{2\Delta}{9GM}\right)^{1/3}\right],$$

für $T_c\le T\le T_h$, wobei

$$T_c=T_s-\frac92GM,\qquad T_h=T_s-\frac43GM.$$

$R_E=R_b\chi_E$ erfüllt exakt $dR_E/dT=1-hR_E$. Am äußeren Endpunkt gilt
$R_b=R_E=2GM$; danach liegt der Erzeuger im Vakuum bei $R=2GM$. Strahlen, die
vor dieser Grenze ins äußere Gebiet mit $R>2GM$ gelangen, können die zukünftige
Nullunendlichkeit erreichen. Später auslaufende Strahlen können die Grenze nicht
nach außen überschreiten. Ein negativer $T_c$ bezeichnet nur den Ursprung in
der analytischen Vergangenheit; er ist kein negativer Prüfzeitpunkt.

Für $M=4$, $R_0=10$ ist $R_E(0)=10(3-\sqrt5)=7,639320225...$,
obwohl im Anfangsschnitt noch keine gefangene runde Sphäre existiert.
Dies illustriert die Abhängigkeit des Ereignishorizonts von der Zukunftswahl.
Die vorherige endliche P4-Prüfung wird dadurch nicht nachträglich zu einem
globalen CST-Horizontnachweis.

Die klassische Zukunft ist singulär:
$\rho=1/(6\pi G\Delta^2)$ und $K_-=80/(27\Delta^4)$ divergieren bei
endlicher Staubeigenzeit. Die mitbewegten Zeitlinien sind dort unvollständig;
eine reguläre $C^2$-Fortsetzung dieser klassischen Lösung ist ausgeschlossen.
Im festen früheren Fenster bleiben dagegen die alten gemeinsamen Schranken
$(\rho/\rho_0)^2\le16$, $K_-/K_0\le960$ und $K_+/K_0\le768$ gültig,
auch für den gesamten Außenraum. Das Zentrum ist dort regulär.

## 8. Periodische Zelle ist kein endlicher Ball

Die materielle Weltfläche $\Sigma$ ist keine Raumzeitkante. Kausale Beziehungen
und Wirkungsbeiträge durch die Oberfläche müssen erhalten bleiben. Die äußere
Rechengrenze, zeitliche Anfangs-/Endränder und Ecken sind getrennt zu behandeln.
Eine periodische Zelle besitzt andere globale Daten und keinen solchen
materiellen Außenraum. Eine Übertragung erfordert eine Abbildung von Zuständen,
Maßen, Materiemarken und Dynamik einschließlich kontrollierter Fehler.

Als exakte algebraische Kontrolle wird der dimensionslose 4D-BDG-Zähler

$$F_4(C)=N-N_0+9N_1-16N_2+8N_3$$

verwendet; hier zählt $N_k$ Paare mit genau $k$ zwischenliegenden Elementen.
Der gemeinsame physikalische Vorfaktor ist für die Additivitätsprüfung irrelevant.
Die hier gewählten kleinen Ketten sind keine vierdimensionalen dynamischen Daten.

Für die Viererkette $a\prec b\prec c\prec d$ gilt
$(N,N_0,N_1,N_2,N_3)=(4,3,2,1,0)$ und $F_4=3$.
Die isolierten Teilketten $\{a,b\}$ und $\{c,d\}$ ergeben zusammen nur $F_4=2$.
Vier kausale Beziehungen wurden abgeschnitten. Selbst bei innerhalb eines
Teilgebiets verbleibenden Endpunkten kann ein künstlicher Schnitt die
Intervallgröße ändern: Bei $\{a,c\}$ hat das Paar $(a,c)$ im Vollset ein
Zwischenelement, im isolierten Teilset keines. Es zählt dann in einer anderen
Wirkungsschicht. 27 Schnitte und alle 24 Umbenennungen der Viererkette werden
exakt kontrolliert.

Die Primärliteratur unterscheidet eingebettete von isolierten Regionen und
behandelt zeitartige Grenzen ausdrücklich [4]. Die dort untersuchte
$l^{-1}$-Divergenz des mittleren Wirkungsbeitrags ist eine durch analytische und
numerische Evidenz gestützte Vermutung für die betrachteten Raumzeitregionen.
Sie ist kein Satz über die innere materielle Oberfläche unseres Staubballs.
Spacelike GHY-Grenzresultate [5] schließen eine zeitartige Materie-Verklebung
nicht automatisch. Weder wird hier ein universeller Gegenrandterm erfunden
noch werden oberflächenübergreifende Intervalle entfernt.

## 9. Ausgeführte Prüfung und Entscheidung P5

`symbolic_checks.py` berechnet die Tensoren aus den vierdimensionalen Metriken
und prüft exakt die Anschluss-, Schicht-, Druckarbeits- und Flussidentitäten.
`analyze.py` führt 15 klassische Randfälle, 75 Außenraumwerte, neun reguläre
EF-Einbettungen, drei bedingte klassische Ereignishorizontfälle, 20 bedingte
Nichtvakuum-Anschlüsse, 27 Kettenschnitte und 24 Labelpermutationen aus.
Die neun EF-Fälle sind teilweise außerhalb des früheren numerischen Fensters
und werden ausdrücklich als analytische Referenzfortsetzung markiert.

Quadrat- und Kubikwurzeln werden mit 100 rationalen Bisektionen eingeschlossen;
Transformationen benutzen 60-stellige nach außen gerundete Decimal-Arithmetik.
Der vorab fixierte Rest-Cap $10^{-20}$ ist eine technische algebraische
Nachrechnungsgrenze, keine physikalische Messgenauigkeit. Symbolische Restwerte
müssen exakt null sein. Keine wissenschaftliche Toleranz aus P3/P4 wird gelockert.

Alle 60 P5-Datensätze der festen Massen-/Zeit-/geplanten Dichtestufen-Matrix
werden gegen den unveränderten Modellvertrag ausgewertet. Alle acht
physikalischen Gates bleiben HOLD. Besonders fehlen für den wirklichen
CST-Anschluss:

- dieselbe endliche Materie-Geometrie-Wirkung mit Rand-/Ecktermen und
  oberflächenübergreifenden Beiträgen;
- Außenraumzustand, Maß und zulässige Zusammensetzung der Historien;
- kalibrierte relationale Randgeometrie, Fluss- und Stressobservablen;
- kontrollierte äußere Gebietsfehler und physikalisch abgeglichene Verfeinerung;
- uniforme Dichte-/Krümmungsmomente und eine kausale Fortsetzung im behaupteten Gebiet.

**Abschluss:** Die klassische Referenznaht ist geschlossen. Die gewählte
klassische Zukunft bleibt singulär. Die bedingte Bounce-Vergleichsgeometrie
benötigt geänderten effektiven Stress und weitere globale Daten. Ein vollständiger
physikalischer CST-Modellschluss ist mit den vorhandenen Definitionen nicht
nachgewiesen und wird nicht als erledigt ausgegeben.

## Quellen

Alle spezifischen Identitäten werden im Paket direkt hergeleitet und nachgerechnet.
Quellen liefern den etablierten Formalismus und Vergleichsmodelle; keine fremden
Befunde werden als neue CST-Ergebnisse ausgegeben.

1. P. Musgrave, K. Lake: *Junctions and thin shells in general relativity using
   computer algebra I: The Darmois-Israel Formalism*, Class. Quantum Grav. 13
   (1996) 1885-1900. https://arxiv.org/abs/gr-qc/9510052, Abschnitt 2.
2. H. Andréasson, G. Rein: *Oppenheimer-Snyder type collapse for a collisionless
   gas*, https://arxiv.org/abs/2410.06701, Abschnitt 5.1 zur Staubreferenz.
   Ihre Vlasov-Sätze werden hier nicht auf CST übertragen.
3. F. Fazzini, C. Rovelli, F. Soltani: *Painlevé-Gullstrand coordinates
   discontinuity in the quantum Oppenheimer-Snyder model*,
   https://arxiv.org/abs/2307.07797. Vergleich zu effektiven Modellen und Chartgrenzen.
4. F. Dowker, R. Liu, D. Lloyd-Jones: *Timelike boundary and corner terms in the
   causal set action*, https://arxiv.org/abs/2501.00139v2, insbesondere Abschnitte
   2.4-2.5 und Anhang A. Untersuchte Grenzen sind nicht automatisch Materienähte.
5. M. Buck, F. Dowker, I. Jubb, S. Surya: *Boundary Terms for Causal Sets*,
   https://arxiv.org/abs/1502.05388. Ergebnis für raumartige Grenzen im Mittel.
6. Eigener Vorgängerstand: https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/bb59cc03e762b5b2133f4f12fdd975b219bf4406/research/rax_cqg/dust_collapse
