# Was ändert das Auslesen des Uhrmodus am letzten Dichtedetektor?

Auf N15-Typ 375841 betrachten wir den stromerhaltenden Anschluss über die Viererkette und das gemeinsame N17-Zukunftsereignis aus PR #349. Bei beiden bekannten Vorzeichenpaaren unterscheidet sich der Kontrast am letzten Dichtedetektor danach, ob der kohärente Uhrmodus ausgewählt oder das Ergebnis der Uhrmessung ignoriert wird. Die Eingangspakete, sämtliche Fenster, die letzte Uhr und die Auslese der Dichte sind für beide Auswertungen gleich.

| Differenz der Wahrscheinlichkeiten der oberen Dichtehälfte | Originalpaar, $\lvert q\rvert=2^{-24}$ | Transferpaar, $\lvert q\rvert=2^{-25}$ |
|---|---:|---:|
| Festuhr aus PR #349, Betrag | $<6{,}203\cdot10^{-29}$ | $<6{,}203\cdot10^{-29}$ |
| Modus null ausgewählt, kohärent (PR #349) | $[-3{,}569;\,-3{,}178]\cdot10^{-27}$ | $[-1{,}841;\,-1{,}534]\cdot10^{-27}$ |
| Alle Uhrmodi summiert, zeitgemischt, Betrag | $<6{,}203\cdot10^{-29}$ | $<6{,}203\cdot10^{-29}$ |
| Kohärenter minus zeitgemischter Vorzeichenkontrast | $[-3{,}631;\,-3{,}116]\cdot10^{-27}$ | $[-1{,}903;\,-1{,}472]\cdot10^{-27}$ |

Ein Vorzeichenkontrast ist jeweils $P(t>1/8\mid +)-P(t>1/8\mid -)$. Alle Intervallgrenzen in der Tabelle sind nach aussen gerundet und umfassen die vollständigen Pakete. Die Zentren des Zeitgemischs haben exakt denselben binären Messwert. Die Null liegt im Ganzpaketintervall des Zeitgemischs. Alle vier differenzierten Eingangsströme behalten in diesem Anschluss exakt ihr Vorzeichen.

## Ein Instrument mit zwei Auswertungen

Sei $x=Y_{15}-6$, $h=2^{-20}$, $d\mu=dx/(2h)$ auf $[-h,h]$. Die Enddichte $t$ liegt bei $m=1/8$ im Fenster $[m-h,m+h]$ mit normiertem Mass $d\nu=dt/(2h)$. $A_s(t,x)$ ist die Amplitude für das ganze Paket $s$ nach den identischen früheren Randoperationen und vor dem Schliessen der Uhr. Der gemeinsame skalare Endfaktor ist quadratintegrierbar und hat strikt positive Norm, wie in PR #349 nachgewiesen. Alle folgenden normierten Wahrscheinlichkeiten enthalten ihn im selben Verhältnis.

Die Uhr lebt in $L^2(d\mu)$. Wir lesen sie in der vollständigen Fourierbasis $e_n(x)=\exp(i\pi n x/h)$ aus. Die Operatoren $K_n=\langle e_n|\otimes I$ erfüllen $\sum_{n\in\mathbb Z}K_n^*K_n=I$ im starken Sinn. Für $A_{s,n}(t)=\int \overline{e_n(x)} A_s(t,x)\,d\mu(x)$ ist das Endereignis immer $E=\mathbf1_{t>m}$. Die erste Auswertung konditioniert auf $n=0$. Die zweite summiert alle gemeinsamen Wahrscheinlichkeiten von $n$ und $E$ vor der Normalisierung. Parseval und Tonelli geben

$$
P_{s,0}(E)=\frac{\int_E|A_{s,0}(t)|^2d\nu}{\int|A_{s,0}(t)|^2d\nu},
\qquad
P_{s,\mathrm{mix}}(E)=
\frac{\iint_E|A_s(t,x)|^2d\nu\,d\mu}
     {\iint|A_s(t,x)|^2d\nu\,d\mu}.
$$

Die zweite Auswertung entspricht dem Ignorieren des Uhrregisters. Beim Mitteln bedingter Festuhr-Wahrscheinlichkeiten ist mit den jeweiligen Ausgangsnormen zu gewichten. Für das kohärente Ergebnis bestimmt die Summe der Amplituden die Gewichte der Enddichte. Die Festuhr bei $x=0$ ist die eigene frühere Präparation aus PR #349.

## Warum das Zeitgemisch an den Zentren verschwindenden Kontrast hat

Der Rechenkern verifiziert aus den Intervallgewichten, dass die beiden Uhrprofile der Paketzentren sich allein an Knoten 6 unterscheiden. Unter den vier früheren Zukunftsdichten hängt nur die Steigung an Knoten 7 von dieser Uhr ab. Der zugehörige Uhrwert $Y_7$ ist fest. Die neuen aktiven Vorgänger an N16 haben die Gewichte $b_6=-8$, $b_{11}=16$, $b_{12}=-9$ und $b_{13}=1$. Bei festem $x$ ist ihr Dichteintegral daher ein Skalar je Zweig. Die letzte Geburt hängt nur von den früheren Zukunftsuhren und $Y_{15}$ ab, jeweils durch separate quadratische Terme. Nach Schliessen aller übrigen Daten besitzt die zentrierte Amplitude die Form

$$
A_{s,c}(t,x)=G(t)\,a_s(x)\exp\!\left[it\left(x/19-x^2/38\right)\right].
$$

Damit ist die über den oberen Halbbereich integrierte normierte Dichte bei jedem festen $x$ eine gemeinsame Zahl $p_c$ für beide Zentren. Dies gilt auch beim Vergessen von $x$. Der Beweis benutzt die Diagonalität von $E$ in $t$.

## Gleichmässiger Fehler für die ganzen Pakete

Für die 15 früheren schmalen Paketachsen liefert die N16-Rechnung ein Maximum $U_0$ der Phasenabweichung und eine Schranke $B$ für deren signiertes Mittel. Bei festem $|x|\le h$ entsteht zusätzlich ein in jeder versteckten Uhrverschiebung ungerader Term. Sein Mittel ist null und sein Betrag ist durch $u=\sum_i(m+h)|b_{i,15}|\,2hr/38$ beschränkt, mit $r=2^{-32}$ und Summe über betroffene schrumpfende Paketachsen. Der komplexe Taylorrest ergibt den gleichmässigen, punktweisen Amplitudenfehler $e=B+(U_0+u)^2/2$ nach dem Integrieren dieser 15 Achsen bei festgehaltenen äusseren Variablen. Eine normierte kohärente Integration der verbleibenden Variablen erhält diese Schranke.

Die zentrierten Phasen *aller* $t,x$ und übrigen Integrationsvariablen eines Zweiges liegen im bereits in PR #349 berechneten gemeinsamen Bogen der Breite $L$. Sei $c=1-L^2/8>0{,}99$. Die Projektion auf die Mitte des Bogens gibt für jede Mischung der zentrierten Amplituden mit positivem normiertem Integrationsmass den Modulunterwert $c$. Für die exakten Amplituden ist $c-e>0$. Das gilt bei festem $x$ und auch nach kohärenter Integration über $x$.

Für den Vergleich von Zentrum und Ganzpaket bei **festem** $x$ entfernen wir die gleiche Trägerphase in beiden Ausgängen. Von $m$ nach $t$ variiert der verbleibende Endfaktor höchstens um

$$
\eta=h\sum_{i\in\{8,9,10\}} |b_{i,16}|\big(2|Y_{i,c}-7|h+h^2\big)/38.
$$

Der Beitrag der fixierten Uhr $x$ liegt für diesen Vergleich in der gemeinsamen Trägerphase. Die Berechnung des kohärenten Modus verwendet die ursprüngliche Phase vor jeder solchen Entfernung. Die letzte Dichtesteigung enthält keine der 15 schmalen Paketachsen. Deshalb ändert sich die um die Trägerphase bereinigte Differenz $A_s-A_{s,c}$ zwischen $m$ und $t$ um höchstens $\eta e$. Für die zentrierte Amplitude ist die entsprechende Änderung höchstens $\eta$. Der Vergleich der am Mittelpunkt verankerten Verhältnisse ergibt

$$
\left|\frac{A_s(t,x)}{A_s(m,x)}-
        \frac{A_{s,c}(t,x)}{A_{s,c}(m,x)}\right|
\le \frac{\eta e(1+1/c)}{c-e}.
$$

Die $L^2(d\nu)$-Norm des zentrierten Verhältnisses ist mindestens $1-\eta/c$. Das Normalisieren beider Vektoren erhöht die vorangehende Fehlerschranke höchstens um den Faktor $2/(1-\eta/c)$. Der Spurabstand der resultierenden reinen Zustände ist durch diese Vektordifferenz beschränkt. Nenne die resultierende Schranke $d_s$. Sie gilt gleichzeitig für jeden festen Uhrwert im Fenster. Die exakte Wahrscheinlichkeit konditioniert auf $x$ liegt daher für alle $x$ im Intervall $[p_c-d_s,p_c+d_s]$. Die normgewichtete Mittelung im Zeitgemisch erhält dieses Intervall für jeden der beiden Zweige. Die obige Nullkontrolle verwendet $|\Delta P_{\mathrm{mix}}|\le d_++d_-$.

## Erfolgsnorm des kohärenten Uhrmodus

Die Wahrscheinlichkeiten im Modell lassen auch eine Schranke für die zusätzliche Modusselektion zu. Der normierte Eingang hierfür ist der gemeinsame Uhr-Endzustand *nach* den früheren Randprojektionen, jeweils für das betreffende Vorzeichenpaket. Seine unnormierte Staubnorm liegt bei $(c-e)^2\le\iint|A_s|^2\le1$. Dasselbe Intervall gilt für den Anteil $\int|A_{s,0}|^2$, da alle unveränderten Pfadphasen vor der kohärenten Integration durch den gemeinsamen zentrierten Bogen und $e$ kontrolliert sind. Das Verhältnis beider Normen ist der Erfolgsanteil.

Für eine schärfere untere Grenze berechnet der Rechenkern direkt aus beiden Geburtstermen eine obere Schranke $L_x$ für $|\partial_x S|$ auf dem vollständigen Integrationsbereich. Daraus folgt $|A_s(t,x)-A_s(t,y)|\le L_x|x-y|$ gleichmässig in $t$, mit den tatsächlichen Phasen vor der Modusmessung. Die Summe der Normen aller übrigen Fouriermodi ist die über $t$ integrierte Uhrvarianz. Ihre obere Grenze lautet $L_x^2h^2/3$, da $\mathrm{Var}_\mu(x)=h^2/3$. Für das ursprüngliche wie für das halbierte Paketpaar folgt in beiden Zweigen

$$
P_s(n=0\mid\text{gemeinsamer vorbereiteter Uhr-Endzustand})
\ \ge\ 1-\frac{L_x^2h^2}{3(c-e)^2}
\ >\ 1-6{,}515\cdot 10^{-13}.
$$

Diese Aussage quantifiziert die Zusatzselektion im festgelegten positiven Modellraum. Der absolute Erfolg der vorgelagerten Projektionen im physikalischen Historienmass ist offen. Aus dem hier gemessenen Unterschied zweier vorzeichenreiner Präparationen folgt keine allgemeine Abhängigkeit vom Stromvorzeichen allein.

## Nachrechnung

`python3 -B kontrolle.py` berechnet alle Grenzen mit rationaler Arithmetik und gleicht die wiederholten Festuhr- und kohärenten Rechnungen mit den archivierten N17-Zahlen ab. [Exakte Intervalle und Einzelgrenzen](kontrolle.json) · [Rechenkern](kontrolle.py)
