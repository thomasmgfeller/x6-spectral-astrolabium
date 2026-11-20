---
title: "Welche Randdaten überleben das Vergessen eines Ereignisses?"
subtitle: "CST-DUST · Markierter Präfix 1564 · Ein-Ereignis-Reduktion"
date: "20. November 2026 · v0.1"
lang: de-CH
---

## Ergebnis

Auf dem endlichen Träger von PR 326 lässt sich die Abbildung der **kontinuierlichen Felder** für jede der 16 markierten N14-Fortsetzungen vollständig angeben. Sie behält die 13 alten Feldwerte als Argumente und integriert die Skalar-, Uhr- und Dichtevariable des zusätzlichen Ereignisses mit ihren festgelegten Massen. Auf 14 Pfaden entsteht eine gewöhnliche effektive quadratische Skalarwirkung. Die beiden übrigen Pfade führen zum gleichen unmarkierten Endtyp 926 und hinterlassen zwei verschiedene lineare Delta-Bedingungen auf den alten Feldern.

Der Staubfaktor beider Delta-Beiträge ist auf dem positiv gewichteten Sektor mit fünf alten inneren Nulldichten nachweislich von null verschieden. Damit kann die direkte Reduktion als Verteilung auf den verbleibenden Feldern bei strikt positiven Pfadgewichten die glatte, eigenständig berechnete N13-Wirkung nicht reproduzieren. Auch für den äusseren skalaren Zustand lässt sich eine Erweiterung der bisherigen Identifikation ausschliessen. Werteerhaltende Phasenkorrekturen je Endtyp können die falsche Abklingrate des Zustands nicht beheben.

### Gegenstand der Prüfung

Acht äussere Ereignisse bilden den alten Kragen. Fünf innere Ereignisse haben die Marken $4,5,6,11,12$. Die zusätzliche Marke $a=13$ bezeichnet das vierzehnte Ereignis. Die Integration entfernt diese Marke ungeachtet ihrer Stelle in einer kausalen Anordnung. Alle alten Skalarwerte werden in $X=(q_0,\ldots,q_{12})$ gesammelt. Für Uhren und Dichten bleiben zunächst ebenfalls sämtliche alten Werte stehen. Auf dem äusseren Rand gelten die Präparation, die zwei Uhrpaketlappen, die Dichtezentren $1/8$ und $1/4$ und die skalare Randnorm aus PR 326.

Der Vergleich auf 13 verbleibenden Feldern prüft die Wirkung gegen Testfunktionen dieser Variablen. Nach anschliessender Integration der alten inneren Felder ist nur noch der äussere Rand zugänglich. Beide Ebenen erfordern eigene Aussagen.

### Definition der Abbildung

Das Vergessen ist die Projektion $\pi:(X,x,T,s,\rho,r)\mapsto(X,T,\rho)$, mit $x=q_a$, $s=T_a$ und $r=\rho_a$. Eine Testfunktion der alten Daten wird auf jeder Fortsetzung durch Komposition mit $\pi$ ausgewertet. Für die zugehörigen Amplitudendichten liefert Integration über die drei entfernten Variablen den Pushforward $\pi_*$. Das Lebesgue-Mass des Skalars wird mit dem geerbten Abel-Grenzwert verstanden. Die Uhren- und Dichteintegrale sind kompakt. Damit ist der Vorgang innerhalb einer markierten Geschichte definiert. Zur kohärenten Summe über Geschichten gehören zusätzlich deren bedingte lineare Amplitudenkoeffizienten.

\newpage

## Skalarwirkung und Normierung

Für einen markierten Pfad $c$ bestimmen die Intervallkoeffizienten $b_{ij}$ den reellen Hessian $H_c$. Jedes kausale Paar mit Gewicht $b_{ij}$ trägt $-b_{ij}(q_i-q_j)^2/2$ zu $q^T H_c q$ bei. $\beta=4/\sqrt 6$. Die Zerlegung in alte und neue Felder lautet
$$
q^T H_c q=X^T A_c X+2x u_c^TX+h_c x^2.
$$
Bei $h_c\ne0$ folgt durch quadratische Ergänzung
$$
\int dx\,e^{i\beta q^TH_cq/2}=
\sqrt{\frac{2\pi}{\beta|h_c|}}\,
e^{i\pi\operatorname{sgn}(h_c)/4}
\exp\!\left[\frac{i\beta}{2}X^T
\left(A_c-\frac{u_cu_c^T}{h_c}\right)X\right].
$$
Der unabhängig aus der N13-Ordnung gebildete Hessian heisst $H_p$. Die Abweichung $D_c=A_c-u_cu_c^T/h_c-H_p$ hat in den 14 regulären Fällen Rang 6 oder 7. Der gemeinsame Nullraum aller 14 Matrizen ist exakt die Gerade der konstanten Verschiebung aller 13 Skalarwerte. Dieser Vergleich betrifft die quadratischen Wirkungen vor den äusseren Sektionsphasen.

| Endtyp | Anzahl markierter Pfade | $h_c$ auf diesen Pfaden |
|:---|---:|:---|
| 766 | 4 | $25/2,25/2,-5,-5$ |
| 926 | 2 | $0,0$ |
| 990, 1790 | je 1 | $15/2$ bzw. $-10$ |
| 2013 | 2 | $5/2,13$ |
| 2014, 2015 | je 1 | $8$ bzw. $-25/2$ |
| 5374, 5566, 27006 | 1, 2, 1 | $-17$ bzw. $-9/2,-9/2$ bzw. $-11/2$ |

Bei $h_c=0$ liefert die Fourierintegration
$$
(2\pi/\beta)\,e^{i\beta X^T A_cX/2}\,\delta(u_c^TX).
$$
Die beiden Normalen $u_c$ sind linear unabhängig. Beim Auflösen nach dem alten Skalar $q_4$ sind die jeweiligen Faktoren $1/|u_{c,4}|=2/9$ und $2$. Die vollständigen Normalen und Matrizen stehen in result.json.

Die geerbte Normierung des Skalartransports bleibt pro Endtyp fest. Im Randrahmen sei $V$ der Block der $m$ Integrationskoordinaten einschliesslich der beiden Sektionskoordinaten, $K$ der reduzierte äussere Hessian. Alle untersuchten $V$ und $K_{xy}$ sind invertierbar. Vor der inneren Integration normiert der positive Faktor $(\beta/2\pi)^{(m+3)/2}\sqrt{|\det V\det K_{xy}|}$ den nachherigen Kern auf die gewählte unitäre Dreimodenpaarung. Die Fresnelphase stammt aus der Signatur. Direkter und schrittweiser Abbau liefern in allen 16 Fällen denselben $K$, dieselbe Determinante und Signatur. Im Delta-Fall benutzt der Vergleich den Zweierpivot mit Determinante $-u_{c,4}^2$ und Signatur null.

\newpage

## Gemeinsame Staub-, Uhr- und Gravitationswirkung

Für jede Ordnung $c$ sei $C_k^c=1+(\beta/2)\sum_{i\prec k}b_{ik}^c(T_k-T_i)^2$. Beim Einfügen können sich auch die Intervallkoeffizienten zwischen zwei alten Ereignissen ändern. Der Prüfer berechnet sie neu. Für das zusätzliche Ereignis gelten $ds/3$ auf $[-3/2,3/2]$ und $d\nu(r)=\tfrac12\delta_0(dr)+\tfrac12\mathbf{1}_{[0,1]}dr$. Mit $\operatorname{sinc}(z)=\sin(z)/z$ ist
$$
d(C)=\int d\nu(r)e^{-irC/2}
     =\tfrac12[1+e^{-iC/4}\operatorname{sinc}(C/4)].
$$
Relativ zum separat berechneten N13-Staub- und Gravitationsfaktor ergibt sich für feste alte Uhren und Dichten
$$
I_c(T,\rho)=e^{i(F_c-F_p)}
\int_{-3/2}^{3/2}\frac{ds}{3}\,d(C_a^c)
\exp\!\left[-\frac i2\sum_{k\ne a}\rho_k(C_k^c-C_k^p)\right].
$$
$F_p=-9$. Für A = 1790 gilt $F_A-F_p=61$, für B = 5374 gilt $F_B-F_p=-23$. Im Produkt mit dem alten Faktor tritt die Gravitation genau einmal auf. Zusammen mit der Skalarformel des vorigen Abschnitts, der Randnormierung und der geerbten Präparation ist dies die markierte Feldabbildung. Im vorliegenden Vertrag zerfällt der Feldintegrand bei fester Ordnung in Skalar- und Staubfaktor. Die Ordnung und ihre Intervallkoeffizienten sind beiden gemeinsam.

### Warum die Delta-Beiträge die Staubintegration überstehen

Setze die fünf alten inneren Dichten auf ihr Atom bei null. Dessen Produktmass ist $1/32$. Die alten äusseren Dichten und Uhrpakete bleiben präparationsgemäss. Nach Ausklammern einer konstanten Phase hängt die alte Staubphase im neuen Uhrwert nur über die Zukunftsreihe ab. Schreibe $S=\sum_{k\in F}b_{ak}$ und $L=\sum_{k\in F}(k-5)b_{ak}$. Für die beiden Markierungen sind $(S,L)=(0,-1)$ und $(-1,-2)$. Mit $\Delta=\sqrt{2/(19\beta)}<1/3$, $T_k=(k-5)\Delta$ auf dem Zukunftskragen und $\rho_k=1/8$ gilt
$$
|\theta(s)-\theta(0)|\le\frac{\beta}{32}
\bigl(|S|s^2+2|L|\Delta|s|\bigr)<85/384.
$$
Für jedes reelle $C$ gilt $|d(C)|\le1$ und $\Re d(C)=[1+\operatorname{sinc}(C/2)]/2>1/3$. Letzteres folgt aus $\operatorname{sinc}(v)\ge-1/\pi$. Aus $|e^{iz}-1|\le|z|$ folgt nach der Uhrintegration ein Realteil **grösser als $43/384$** in der herausgedrehten Phase. Die Schranke gilt für alle verbliebenen inneren Uhrwerte in diesem Sektor.

Die zwei Dirac-Verteilungen liegen auf verschiedenen Hyperebenen. Um einen Punkt der ersten Ebene ausserhalb der zweiten kann man lokal allein den ersten singulären Anteil prüfen. Ein glatter Beitrag kann diese Singularität nicht aufheben. Dasselbe gilt mit vertauschten Ebenen. Eine glatte nackte N13-Amplitudendichte könnte bei wörtlichem Vergessen der drei neuen Feldvariablen nur dann mit der Summe übereinstimmen, wenn beide markierten Koeffizienten null wären. Beide sind im betrachteten strikt positiven Sektor von null verschieden. Diese Aussage gilt vor der Integration der fünf alten inneren Ereignisse.

\newpage

## Was sich über den äusseren Rand beweisen lässt

Nach Integration der alten inneren Skalare entstehen in der geerbten Dreimodenpaarung glatte zentrierte Gausszustände. Schreibe ihren Betrag als $|N_j|\exp[-\beta y^TR_j y/2]$ mit $R_j=\Re\Omega_j>0$. Die elf rationalen Werte $e_1^TR_j e_1$ für Elternzustand und zehn Endtypen sind paarweise verschieden. Aufsteigend beginnen sie bei $0{,}371692$ (A), $0{,}859833$ (2015), $0{,}906708$ (2014) und $1{,}988791$ (2013). Der Elternzustand folgt bei $2{,}286602$. B liegt bei $50{,}613322$. Die Dezimalzahlen sind gerundet.

Auch eine eigene ortsabhängige Phase $e^{i\chi_j(y)}$ pro **unmarkiertem Endtyp** kann diese Raten nicht ändern. In jeder nichtleeren Summe mit konstanten, von null verschiedenen Koeffizienten besitzt genau ein beitragender Endtyp die kleinste Rate. Auf einem gemeinsamen Kegel um $e_1$ klingt er langsamer ab als alle übrigen. Die umgekehrte Dreiecksungleichung begrenzt den Summenbetrag von unten, die Dreiecksungleichung von oben. Sein exponentielles Abklingen entspricht damit dem langsamsten beitragenden Typ. Die Elternrate liegt für jede solche Auswahl strikt darüber oder darunter. Gleichheit mit einem von null verschiedenen nackten Elternzustand ist ausgeschlossen. Für die Nullsumme gilt das unmittelbar.

Die Ungleichungen gelten gleichmässig auf einem Kegel positiven Raumwinkels. Der Prüfer sichert $|y_2/y_1|,|y_3/y_1|<1/65536$ mit rationalen Matrixeinträgen und einer oberen Schranke der Richtungsabweichung. Damit trägt das Argument auch im gewählten $L^2$-Raum, selbst bei lediglich messbaren Phasen. Die komplexen Staub- und Uhramplituden sind ortsunabhängige Koeffizienten. Die Nichtnull-Bedingung für den N13-Uhrfaktor bei beiden Dichtezentren wurde in PR 326 numerisch geprüft. Der Skalarsatz selbst ist exakt. Er betrifft unitäre Phasenmultiplikation bei festen skalaren Randkoordinaten. Allgemeinere Integralkerne, zusätzliche Randvariablen oder ein aus einer neuen Theorie hergeleitetes Randmass benötigen eigene Prüfungen.

### Entscheidung und verbleibender physikalischer Input

Für gegebene markierte Koeffizienten $w(c\mid p)$ lautet die gemeinsame induzierte Dichte
$$
\mathcal A^{\mathrm{eff}}_p=\sum_{c\mapsto p} w(c\mid p)\,\pi_*\mathcal A_c.
$$
Jedes $\pi_*\mathcal A_c$ ist jetzt ohne Detektor bestimmt. Die Summe enthält die zu bestimmenden Koeffizienten. Als Sollwert derselben Gleichung würde sie die Gewichte bereits verwenden. Der separat berechnete nackte N13-Kandidat liefert hingegen den oben bewiesenen Widerspruch.

Die Auswahl erfordert eine unabhängig bestimmte Dynamik oder Paarung auf der gröberen Randbeschreibung, die insbesondere vorschreibt, was mit den beiden verschiedenen linearen Bedingungen beim weiteren Zusammenfassen geschieht. Alternativ kann ein mikroskopisches Mass auf den markierten Erweiterungen die Koeffizienten liefern. Eine neue Wahl wäre als zusätzliche Modellannahme zu prüfen. Der Status von Etappe 6 und P3 bleibt HOLD.

