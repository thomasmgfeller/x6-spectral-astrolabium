# Expansion und lokales Trapping auf der geprüften Referenz

6. November 2026 · CST-DUST-EXPANSION-TRAPPING-001 · v0.1

## 1. Geltungsbereich und Herkunft

Der geprüfte Dynamikpfad ist die eingesetzte klassische Einstein-Staub-Referenz
REF-DUST-FB-01. Der gekoppelte CST-Kandidat hat weiterhin keinen geschlossenen
Dynamikkern und keine vollständigen Messadapter. Deshalb folgt aus den hier
berechneten klassischen gefangenen Flächen kein physikalischer CST-Trapping-PASS.

Der veröffentlichte Vorgängerstand ist Main-Commit
`b4a52636c506288462e21d88e0f6bd152a78b540` in
`thomasmgfeller/x6-spectral-astrolabium` (PR 241). `inputs/provenance.json`
enthält die SHA-256-Werte aller übernommenen Eingaben. Die arithmetische
Intervallbibliothek bleibt bytegleich zum Vorgänger.

Der lokale Plan wurde vor den neuen Rechnungen fixiert. Bekannte analytische
Eigenschaften der Referenz bestimmen die Fragestellung; es handelt sich nicht
um eine externe Präregistrierung oder verblindete Entdeckung. Neue physikalische
CST-Ensembles, Zufallsstichproben und bezahlte Läufe: jeweils null.

## 2. Geometrie des endlichen Balls

Signatur $(-+++)$, $G=c=1$, $R_0=10$, $M\in\{1/4,1,4\}$, $\Lambda=0$.
Mit $x=T/T_E$, $T_E=5\sqrt5/3$, $q=\sqrt M/4$, $s=1-qx$ gilt

$$R_b(T)=10s^{2/3},\qquad H=-\frac{2}{3(T_s-T)},\qquad T_s=T_E/q.$$

Für alle Massen wird dasselbe physikalische Zeitfenster $0\le x\le1$ verwendet;
immer ist $s\ge1/2$. $\chi\in(0,1]$ bezeichnet die feste mitbewegte Schale,
$R=\chi R_b$ ihren Arealradius und $m=M\chi^3$ ihre eingeschlossene Masse.
Der Rand $\chi=1$ ist eine Materieoberfläche und keine periodische Zellgrenze.

Die marginal gebundene FLRW-Innenmetrik lautet
$ds^2=-dT^2+R_b(T)^2(d\chi^2+\chi^2d\Omega^2)$.
Der Wechsel zu $R=\chi R_b$ ergibt einen gemeinsamen Painlevé-Gullstrand-Ansatz:

$$ds^2=-dT^2+[dR+v(T,R)dT]^2+R^2d\Omega^2,$$

$$v(T,R)=\begin{cases}-H(T)R,&0<R\le R_b(T),\\
\sqrt{2GM/R},&R\ge R_b(T).
\end{cases}$$

Außen ist dies der ingoing PG-Zweig der Schwarzschild-Metrik. Seine Zeit ist
die Eigenzeit der $E=1$-Freifallkongruenz, die am bewegten Rand zur Staubuhr passt.
Die PG-Darstellung bleibt bei $R=2GM$ regulär. Die Rechnung betrifft die
marginal gebundene Referenz mit nichtverschwindender Anfangsgeschwindigkeit,
nicht einen anfangs ruhenden geschlossenen FLRW-Ball.

## 3. Drei verschiedene Expansionen

Setze $u=\partial_T-v\partial_R$, $e=\partial_R$ und

$$l=u+e=\partial_T+(1-v)\partial_R,\qquad
n=u-e=\partial_T-(1+v)\partial_R.$$

Dann gilt $u^2=-1$, $e^2=1$, $u\cdot e=0$, $l^2=n^2=0$, $l\cdot n=-2$.
Beide Nullrichtungen sind zukunftsgerichtet; das auswärts gerichtete Label wird
von der Orientierung des räumlichen Normalenvektors übernommen. Hinter einer
Trapping-Grenze kann auch $l(R)<0$ sein. Die Normierung ist durch $l(T)=n(T)=1$
festgelegt; $T$ ist im Allgemeinen kein affiner Nullparameter.

Für eine runde Symmetriesphäre mit Fläche $A=4\pi R^2$ gilt definitionsgemäß

$$\theta_l=\frac{\mathcal L_l A}{A}=\frac{2(1-v)}R,\qquad
\theta_n=\frac{\mathcal L_n A}{A}=-\frac{2(1+v)}R.$$

Für die Fehlerprüfung werden $e_l=R\theta_l/2=1-v$ und
$e_n=R\theta_n/2=-1-v$ verwendet. Diese dimensionslosen Größen bleiben am
Vorzeichenwechsel geeignet; ein relativer Fehler von $\theta_l=0$ wäre undefiniert.

Die Volumenexpansion der Staubkongruenz ist dagegen

$$\Theta_{\rm dust}=\nabla_a u^a=-\partial_Rv-2v/R=3H<0.$$

Sie wird ausschließlich im Materieinneren als Staubobservable bezeichnet.
Außen hat die gewählte Freifallkongruenz die Divergenz $-3v/(2R)$, aber dort
existiert kein positiver Staubstrom. Negative Staubexpansion allein impliziert
keine gefangene Fläche. Am regulären Zentrum wird keine entartete Fläche
$R=0$ geprüft; $\theta_l\sim2/R$, $\theta_n\sim-2/R$ für kleine Kugeln
sind kein Krümmungssingularitätsnachweis.

Unter $l\mapsto b l$, $n\mapsto b^{-1}n$, $b>0$, skalieren die Expansionen
entsprechend. Ihre Vorzeichen, ihr Produkt und auf $\theta_l=0$ das Vorzeichen
von $\mathcal L_n\theta_l$ bleiben invariant. Magnitudenvergleiche erfordern
jedoch dieselbe Normierung. Eine Umkehr der Zeitrichtung ist kein zulässiger Boost.

## 4. Geometrischer Trapping-Test

In der sphärischen klassischen Geometrie ist die Misner-Sharp-Masse geometrisch
durch $1-2Gm_{\rm MS}/R=g^{ab}\partial_aR\partial_bR$ definiert. Hier gilt

$$g^{ab}\partial_aR\partial_bR=1-v^2,\quad
\theta_l\theta_n=\frac4{R^2}\left(\frac{2Gm_{\rm MS}}R-1\right).$$

Erst die eingesetzte Einstein-Staub-Lösung identifiziert diese geometrische
Masse mit $M\chi^3$ innen und $M$ außen. Sie darf für einen ungeprüften CST-Kern
nicht allein aus Materiezählungen übernommen werden.

Da auf diesem Kollapszweig $v>0$, gilt überall $\theta_n<0$. Runde Sphären
sind zukunftsgefangen genau dann, wenn $v>1$ oder $2Gm/R>1$. Für expandierende
Referenzen könnte dieselbe Kompaktheit vergangenheitsgefangene Flächen anzeigen;
deshalb werden beide Nullvorzeichen geprüft. Aufgrund der Symmetrie sind die
Vorzeichen auf jeder gesamten Sphäre konstant. Bei einer allgemein deformierten
CST-Fläche würde ein negativer Flächenmittelwert nicht genügen: Man benötigt eine
kontrollierte Aussage auf der ganzen geschlossenen Fläche einschließlich der
räumlichen Rekonstruktionsfehler.

Innen sind die marginalen Sphären bei

$$R_A=1/|H|=\sqrt{R_b^3/(2GM)},\qquad
\chi_A=\sqrt{R_b/(2GM)}.$$

Solange $R_b>2GM$, liegt dieser formale Innenradius außerhalb des Materiegebiets
und ist dort nicht als innere Lösung verwendbar. Ebenso ist die formale
Schwarzschild-Sphäre $R=2GM$ vor dem Oberflächendurchgang im Materieinneren und
keine gültige Vakuum-Marginalfläche. Im Inneren muss die eingeschlossene Masse
verwendet werden. Beispiel: Bei $M=4$, $T=0$, $R=8$ ist $m=4(8/10)^3$,
$2m/R=0,512<1$; der Ersatz $m\to M$ würde eine falsche Marginalfläche erzeugen.

Für $R_b<2GM$ bilden alle runden Sphären mit

$$R_A<R<2GM$$

einen zukunftsgefangenen Ringbereich im räumlichen Schnitt. Sein innerer Teil
$R_A<R\le R_b$ liegt im Staub, sein äußerer Teil $R_b<R<2GM$ im Vakuum.
Das Zentrum und kleine zentrale Kugeln bleiben im betrachteten Fenster regulär
und ungefangen, während äußere runde Sphären bereits gefangen sind.

## 5. Innerer und äußerer marginaler Ast

Auf beiden Ästen gilt $\theta_l=0$ und $\theta_n=-4/R<0$.
Für den Staubast folgt mit $h=|H|$, $\dot h=3h^2/2$:

$$\mathcal L_n\theta_l=-2\dot h+\frac{2(1+hR)}{R^2}
\mathrel{\mathop=\limits_{R=1/h}}+\frac1{R_A^2}>0.$$

Dieser Ast ist im Sinn der einseitigen lokalen Klassifikation **future inner**.
Mit $\dot R_A=-3/2$ und $v=1$ hat sein Tangentenvektor die Norm
$-1+(\dot R_A+1)^2=-3/4$: Die Röhre ist zeitartig. Ihre Fläche nimmt ab.

Auf dem stationären Vakuumast $R=2GM$ gilt dagegen

$$\mathcal L_n\theta_l=-2/R^2<0.$$

Er ist **future outer** und null, denn $\dot R=0$, $v=1$ und damit
$-1+(\dot R+1)^2=0$. Seine Fläche ist konstant.

Beim ersten Oberflächendurchgang treffen beide Äste zusammen. Wegen des
Dichtesprungs besitzt $\mathcal L_n\theta_l$ verschiedene einseitige Werte;
auch die Röhrentangenten stimmen nicht überein. Die Klassifikation gilt auf den
jeweiligen offenen Ästen. Es wird keine durchgehend glatte marginale Röhre über
diesen Eckpunkt hinweg behauptet. Insbesondere ist der zeitartige innere Ast
kein stationärer Reissner-Nordström-Cauchyhorizont.

## 6. Expliziter Innen-/Rand-/Außenanschluss

Die Oberfläche folgt $\dot R_b=-\sqrt{2GM/R_b}$. Die Normale nach außen ist
$e^a=\partial_R$. Der induzierte Tensor ist auf beiden Seiten

$$h_{ij}dy^idy^j=-dT^2+R_b^2d\Omega^2.$$

Die Oberfläche ist geodätisch. Aus $K_{TT}=-e_a a^a=0$ und
$K_{\theta\theta}=R_b e(R)=R_b$ folgt
$K_{\phi\phi}=R_b\sin^2\theta$. Daher $[h_{ij}]=[K_{ij}]=0$; die klassische
Darmois-Israel-Bedingung benötigt hier keine dünne Oberflächenschicht.

Auch die Oberflächenbeschleunigung stimmt überein. Innen sind
$\partial_Tv=3v^2/(2R_b)$ und $\partial_Rv=v/R_b$, außen
$\partial_Tv=0$ und $\partial_Rv=-v/(2R_b)$. Entlang der bewegten Oberfläche ist
jeweils $dv/dT=v^2/(2R_b)=GM/R_b^2$, also $\ddot R_b=-GM/R_b^2$.
Die Massen sind beidseitig $M$, der Druck und der mitbewegte Massenfluss null.
Das Skript kontrolliert die beiden Geschwindigkeits- und Beschleunigungswege
an 15 gemeinsamen Massen-/Zeitpunkten.

Die Dichte und Krümmung dürfen einen endlichen Sprung haben. Dies ist von einem
distributionellen Oberflächenstress zu unterscheiden. Die Expansionen sind
am Rand stetig, ihre transversalen Ableitungen im Allgemeinen nicht.
Dieser explizite klassische Anschluss ist kein aus CST abgeleitetes Randgesetz.

## 7. Ereigniszeiten und kontrollierte Numerik

Für eine feste Schale $\chi$ liegt der eindeutige Übergang bei

$$x_h(M,\chi)=\frac{1-(2GM\chi^2/R_0)^{3/2}}q.$$

Es werden nur Wurzeln mit $0\le x_h\le1$ als Ereignisse im geprüften Fenster
gewertet. Die Formel nutzt die strikte Monotonie von $R_b$; Werte außerhalb des
Fensters werden nicht als zusätzliche dynamische Validierung ausgegeben.

Bei $M=4$ liegt der erste runde Übergang an der Oberfläche bei
$x_h=0,5689164944001346$, $T_h=2,120226591665966$, $R_b=8$.
Die vordefinierten Schalen $\chi=0,95$ und $0,9$ folgen bei
$x_h=0,7730247793863154$ und $0,9567401244176981$.
Die anderen 18 Kandidaten des 21-Schalen-Plans liegen außerhalb des Fensters.
Für $M=1/4$ und $M=1$ ist selbst die maximale Oberflächenkompaktheit im ganzen
Fenster kleiner als eins. Daher gibt es dort keine gefangenen runden
Symmetriesphären im Inneren oder Außenraum.

Die vier Euler-Stufen $N=128,256,512,1024$ verwenden unverändert die zuvor
bewiesene Zustandsfehlerhülle. Für $r=R_b/10$, $u=dr/dx$, $\kappa=M/72$:

$$r'=u,\quad u'=-\kappa/r^2,\quad
E_n=\frac{B}{2N}\big[(1+1/N)^n-1\big],\quad B=125\kappa/27.$$

Der Zustand liegt im geprüften Gebiet $0,6\le r\le1,05$, $-0,5\le u\le0$.
Die globalen Hüllen schließen die exakte klassische Lösung ein. Die archivierten
Hüllen für $r,H T_E$ werden auf $\Theta, e_l,e_n$ propagiert. Alle 420 inneren
Vergleiche enthalten die analytischen Werte; die Massen- und kinematische
Darstellung stimmen innerhalb der Hüllen überein. Die maximalen absoluten
$e$-Fehlerhüllen sind 0,011711; 0,005886; 0,002951; 0,001477. Ab $N=512$ wird
das vorher festgelegte numerische Cap 0,005 eingehalten. Dies ist keine relative
Prozentangabe für $\theta_l$ und keine physikalische CST-Dichteverfeinerung.

Die Ereignissuche führt den bewiesenen Euler-Fehler auch zwischen den bisherigen
Ablesezeiten mit. Letzter Punkt mit $r_{\rm lo}>2GM\chi^2/10$ und erster Punkt
mit $r_{\rm hi}<2GM\chi^2/10$ begrenzen die eindeutige Wurzel. Alle zwölf
numerischen Zeitintervalle enthalten die analytischen Wurzeln und sind schmaler
als das vorab festgelegte Cap $0,025T_E$. Null enthaltende Expansionsintervalle
allein werden ausdrücklich nicht als Nachweis einer exakt marginalen Fläche benutzt.

100 exakte rationale Bisektionen schließen Quadrat- und Kubikwurzeln ein.
Alle zertifizierten Transformationen verwenden anschließend nach außen gerundete
Decimal-Arithmetik mit 60 Stellen. Binäre Gleitkommawerte werden nur zur
Darstellung benutzt; grafische Kurven sind keine zusätzlichen numerischen Beweise.

## 8. Flächenableitung entlang unabhängiger Nullstrahlen

Im Staub gilt entlang radialer Nullstrahlen

$$\chi(x_0+\delta)=\chi_0\pm\frac{\sqrt5}{2q}
\left[(1-qx_0)^{1/3}-(1-q(x_0+\delta))^{1/3}\right].$$

Diese Gleichung wird separat zur Entwicklung von $R_\pm$ und damit $A_\pm$
verwendet. Der symmetrische Flächenquotient liefert

$$\widehat e=\frac{R(x_0+\delta)^2-R(x_0-\delta)^2}
 {4\delta T_E R(x_0)}.$$

Für drei Massen, drei innere Zeiten, drei innere Schalen, zwei Richtungen und
vier Schrittweiten werden 216 Fälle ausgewertet. Jeder Strahl bleibt nachweislich
innerhalb des Zeitfensters, außerhalb des Zentrums und innerhalb der Materie.
Der Ableitungsfehler wird direkt gegen die eingeschlossene analytische Expansion
begrenzt. Bei $\delta=1/512$ beträgt die größte absolute $e$-Fehlerhülle
höchstens $2,142\cdot10^{-6}$. Der ungefähr quadratische Abfall ist eine
numerische Konsistenzbeobachtung; der belastbare Nachweis sind die einzelnen
Intervallvergleiche, nicht eine gefittete Konvergenzordnung.

## 9. Vorzeichen und bisherige Toleranzen

Ein Trapping-PASS verlangt strikte Negativität der vollständigen Intervalle
beider Null-Expansionen. Unbekannte Fehlerbeiträge führen zu HOLD. Für spätere
Messungen müssen Flächenauswahl, Nullrichtungen, Zeitnormierung, Randfehler,
Operatorfehler und statistische Unsicherheiten gemeinsam berücksichtigt werden.
Eine nachträgliche Auswahl günstiger Flächen erfordert zudem eine vorab definierte
Such- und Mehrfachtestregel; solche physikalischen Daten wurden nicht erzeugt.

Als rein hypothetische Sensitivitätsdiagnose werden gleichzeitig
$|\widehat H/H-1|\le0,05$ und $|\widehat R/R-1|\le0,05$ eingesetzt.
Ohne Unabhängigkeitsannahme folgt für $v=|H|R$:

$$0,9025v\le\widehat v\le1,1025v.$$

Dann ist $e_l<0$ erst sicher, wenn $0,9025v>1$; $e_l>0$ erst, wenn
$1,1025v<1$. Dazwischen bleibt die Vorzeichenaussage HOLD. Von den 105
vordefinierten inneren Kugelfällen sind in der genau eingeschlossenen klassischen
Referenz vier gefangen und 101 ungefangen. Unter dieser hypothetischen
5-%-Fehlerbox bleiben eine gefangene und 95 ungefangene Entscheidungen eindeutig;
neun sind unentschieden. Dies sind keine empirischen Fehlerraten oder wirklichen
CST-Konfidenzintervalle. Weitere unbekannte Fehler können das Ergebnis nur schwächen.

## 10. Regularität bleibt eigenständig

Im gesamten festen Fenster gelten die bereits bewiesenen klassischen Schranken

$$ (\rho/\rho_0)^2\le16,\qquad
K_{\rm in}/K_0\le960,\qquad K_{\rm out}/K_0\le768,$$

mit $\rho_0=M/(4\pi R_0^3/3)$, $K_0=(GM/R_0^3)^2$. Die Außenraumgrenze folgt
aus $R\ge R_b$, die Dichte ist dort null. Beide einseitigen Oberflächenwerte
sind endlich; die klassische Anschlussprüfung schließt eine dünne Schicht aus.
Beim Oberflächendurchgang für $M=4$ sind
$K_{\rm in}=15/4096$ und $K_{\rm out}=3/1024$ endlich.
Trapping kann somit bereits in einem regulären Abschnitt dieser später singulären
klassischen Lösung auftreten. Trapping-PASS und Singularitätsauflösung sind
verschiedene Aussagen.

60 feste Massen-/Zeit-/Dichtestufen-Datensätze und zwölf Ereignis-Datensätze
werden als P4 gegen den unveränderten Modellvertrag bewertet. Alle 72 sind
formal gültig; sämtliche physikalischen Gates einschließlich TRAPPING,
BOUNDARY, REGULARITY und EXTENSION bleiben HOLD. Für CST fehlen weiterhin
physikalische Operatoren, uniforme Momentenschranken, Tailkontrolle,
physikalisch abgeglichene Konvergenz und eine kontrollierte kausale Fortsetzung.

## 11. Keine globale Horizontaussage

Die nachgewiesenen Flächen sind lokale runde gefangene bzw. marginale Flächen
der ausdrücklich gewählten klassischen Raumzeit. Aus dem endlichen Zeitfenster
wird kein Ereignishorizont als Grenze des kausalen Vergangenheitsbereichs der
zukünftigen Nullunendlichkeit bestimmt. Dazu wären eine Zukunftsfortsetzung
und globale Randannahmen nötig. Das Ausbleiben runder gefangener Sphären schließt
keine allgemeinen deformierten gefangenen Flächen aus. Die Literatur zeigt,
dass solche Flächen die Materieoberfläche überschreiten können [2].

Der nächste modellabhängige Nachweis muss zunächst die dynamischen und
geometrischen CST-Voraussetzungen schließen. Erst danach kann dieselbe
Diagnostik mit unabhängigen, vollständig unsicherheitskontrollierten
CST-Flächen und beiden Nullrichtungen physikalisch qualifiziert werden.

## Quellen und Einordnung

Die Formeln und Schranken oben sind für die feste Referenz direkt hergeleitet;
die Literatur liefert die Begriffe und Kontextgrenzen. Es werden keine
Literaturergebnisse als neue CST-Ergebnisse ausgegeben.

1. S. A. Hayward, *General laws of black-hole dynamics*, Phys. Rev. D 49, 6467
   (1994), DOI https://doi.org/10.1103/PhysRevD.49.6467,
   https://arxiv.org/abs/gr-qc/9303006, insbesondere Abschnitt III und V.
2. I. Bengtsson, E. Jakobsson, J. M. M. Senovilla, *Trapped surfaces in
   Oppenheimer-Snyder black holes*, Phys. Rev. D 88, 064012 (2013),
   https://doi.org/10.1103/PhysRevD.88.064012, https://arxiv.org/abs/1306.6486.
3. H. Andréasson, G. Rein, *Oppenheimer-Snyder type collapse for a collisionless
   gas*, https://arxiv.org/abs/2410.06701, Abschnitt 5.1 zur marginal gebundenen
   Staubreferenz in PG-Koordinaten. Die Vlasov-Ergebnisse werden hier nicht benutzt.
4. Eigener veröffentlichter Modellvertrag (PR 239), Stromkalibrierung (PR 240)
   und Korrespondenzvorprüfung (PR 241):
   https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/b4a52636c506288462e21d88e0f6bd152a78b540/research/rax_cqg/dust_collapse
