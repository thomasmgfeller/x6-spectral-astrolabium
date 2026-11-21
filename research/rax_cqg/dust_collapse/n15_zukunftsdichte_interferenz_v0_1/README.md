# Wie viel Stromvorzeichen lässt sich nach der kohärenten Summation am Zukunftsrand auslesen?

**CST-DUST · N15, Typ 375841 · 21. November 2026**

Beim wirkungsgleichen Gegenpaar aus PR #344 ist eine Spur des Anfangsstromvorzeichens bereits im geöffneten Zukunftsrand enthalten. Ein gemeinsamer Detektor vergleicht die Phase zweier benachbarter Werte der Zukunftsdichte $w_7$. Nach kohärenter Summation über zwei ganze, vorzeichenreine Pakete unterscheidet sich die bedingte Wahrscheinlichkeit desselben Ausgangs um rund $5{,}803\cdot10^{-12}$. Unter der veröffentlichten flachen Randpaarung liegt der maximal mögliche Unterschied für **jeden** binären Detektor bei rund $6{,}701\cdot10^{-12}$. Die geringe absolute Trennung liegt damit zum grössten Teil an den beiden Randzuständen selbst. Das Ergebnis ist eine Rechnung im endlichen Modell. [Ausgangspaar, PR #344](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/344) · [Definition des geöffneten Zukunftsrands](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/8d4fa91bc3b291714599f6368aaa58a59c9da215/research/rax_cqg/dust_collapse/n15_future_boundary_v0_1/Teilartikel.md)

| Grösse im gewählten Randprodukt | Zertifizierter Bereich, nach aussen gerundet |
|---|---:|
| Abstand $P(Y+\mid p>0)-P(Y+\mid p<0)$ des festen Detektors | $[5{,}802934,\,5{,}802945]\cdot10^{-12}$ |
| Grösster Abstand für einen beliebigen binären Effekt | $[6{,}700652,\,6{,}700663]\cdot10^{-12}$ |
| Anteil des festen Detektors am maximalen Abstand | $[86{,}6024,\,86{,}6027]\,\%$ |
| Obergrenze für reine Ablesung der Zukunftskoordinaten, ohne Phasenvergleich | $4{,}658\cdot10^{-18}$ |
| Wahrscheinlichkeit $P(Y+)$ bei Quellschritt null oder dephasierten Dichtehälften | exakt $1/2$ für jedes der beiden Pakete |

Die Prozentangabe bezeichnet den Anteil an einem sehr kleinen Wahrscheinlichkeitsunterschied. Bei gleich häufig angebotenen Paketen entspräche der feste Detektor einer Trefferwahrscheinlichkeit von $1/2+2{,}9015\cdot10^{-12}$. Physikalische Häufigkeiten der Pakete sind nicht bestimmt.

## Pakete und Bindung an die Vorarbeit

Die Zentren sind die beiden wirkungsgleichen Feinhistorien aus PR #344 bei $q=\pm2^{-24}$. Ihre Stromwerte sind $\mp1099/3187671040$. Die neuen Pakete sind achsenparallele offene Boxen um diese Zentren. In $e=Y_3+2$, den sieben inneren $Y_j=T_j/\Delta$ und den sieben inneren $W_j=w_j/\Delta$ beträgt die Halbbreite jeweils $2^{-32}$. Die gemeinsame physische Anfangsdichte durchläuft ihr volles Band $[3/32,5/32]$. Alle sieben freigegebenen Zukunftskoordinaten durchlaufen die ursprüngliche Box mit Halbbreite $\eta=2^{-20}$ in ihren jeweiligen Variablen $(Y_8,Y_9,Y_{10},w_7,w_8,w_9,w_{10})$. Die Uhr $Y_7=2$ bleibt fest. Es gilt $\Delta^4=3/722$.

Die rationalen Intervallprüfungen zeigen, dass beide Boxen strikt in den bisherigen Uhr- und 1-%-Dichtebändern liegen und positives Hilfsmass haben. Die Beträge der Anfangsströme liegen auf beiden ganzen Boxen zwischen $3{,}4350\cdot10^{-7}$ und $3{,}4603\cdot10^{-7}$, mit jeweils festem Vorzeichen. Die Boxen verwenden das flache frühere Hilfsmass in den ursprünglichen Feldkoordinaten. Die Wahl ihrer Halbbreite ist Teil des vorab festgelegten Versuchs. Die Wirkungsgleichheit aus der Vorarbeit bezieht sich auf die Zentren und die dort geprüften Quellen. Gleiche unverschobene Amplituden der neuen ganzen Pakete werden hier nirgends vorausgesetzt. [Prüfvertrag](pruefvertrag.json) · [Zentren aus PR #344](basis/pr344_ergebnis.json)

## Ein gemeinsamer Detektor auf dem bereits reduzierten Rand

Sei $A_s(x,z)$ die kohärente Amplitude des Pakets $s$ beim physischen Dichtewert $x=w_7$ und den sechs übrigen Zukunftskoordinaten $z$. Der Skalarzustand und die Gravitationsphase sind auf dem Einzeltyp gemeinsam. Die Staubwirkung ist affin in $w_7$. Mit $b_{i7}$ aus den offenen Kausalintervallen ergibt sich

$$
D_7=\partial_{w_7}S_d=\partial_{W_7}\widehat S
=-\frac12-\frac1{38}\sum_{i\prec7} b_{i7}(Y_i-Y_7)^2 .
$$

Der gemeinsame Phasenbezug ist $D_*=-21166501/6225920$. Er folgt aus dem neutralen Uhrprofil der Präparation aus PR #344. Die Auslese benutzt weder die verborgenen Uhren der einzelnen Historie noch das Stromvorzeichen. Sie greift nur auf die fertige Randfunktion zu.

Paare jedes $x$ in der unteren Hälfte $[1/8-\eta,1/8)$ mit $x+h$ in der oberen Hälfte, $h=\eta$. Die zwei Komponenten der Randfunktion sind $a_s=A_s(x,z)$ und $b_s=e^{-ihD_*}A_s(x+h,z)$. Das Zusammenfassen zu Paaren erhält die flache Randnorm bei Integration über die untere Hälfte mit dem ursprünglichen Mass. Der feste Ausgang ist der Projektor $E_+=(1+\sigma_y)/2$ auf diesen zwei Komponenten. Sein Gegenstück ergänzt ihn zur Identität. Daher gilt

$$
P_s=\frac12+
\frac{\int \mathrm{Im}(\overline a_s b_s)}
{\int (|a_s|^2+|b_s|^2)} .
$$

Der Detektor vergleicht verschiedene Dichtewerte nach der Reduktion. Die zwei Komponenten stammen aus demselben schon definierten $L^2$-Raum. Insbesondere respektiert der Effekt jede Nullrichtung der benutzten Randabbildung. Der frühere Versuch koppelte einen eigenen Zeiger vor der Reduktion an den Anfangsstrom. [Früherer Zeigerversuch, PR #340](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/340)

Bei Quellschritt null sind beide Arme identisch und der Ausgang hat Wahrscheinlichkeit $1/2$. Eine zweite Kontrolle verwendet den ganzen unveränderten Rand und löscht nur die Kohärenz zwischen den zwei Dichtehälften. Dann verschwindet der Kreuzterm ebenfalls exakt. Als dritte Kontrolle dient das alte Paketpaar, bei dem eine Dichtetranslation die Wirkung für *jeden* Zukunftswert und das Integrationsmass erhält. Seine beiden Randfunktionen sind identisch. Der hier verwendete Detektor ergibt deshalb für dieses Paar exakt gleiche Wahrscheinlichkeiten. Ein allgemeiner Vorzeichendetektor für die ganze Präparation ist damit weiterhin ausgeschlossen.

## Warum die Trennung die kohärente Summation überlebt

Für festes $(x,z)$ bringt der Wechsel auf $x+h$ jeder Historie im zweiten Arm die Phase $\theta=h(D_7-D_*)$. In den positiven Paketen ist $D_7-D_*>6{,}0828\cdot10^{-6}$, in den negativen $D_7-D_*<-6{,}0828\cdot10^{-6}$. Die Staubphasen beider Pakete liegen auf der ganzen Zukunftsbox zwischen $-0{,}618$ und $-0{,}393$ rad. Hat ein Paket Phasenspanne $L$ und Mass $m$, so ist $|a|\ge m(1-L^2/8)>0$. Für die im jeweiligen Zentrum berechnete Phase $\theta_c$ folgt

$$
\left|\frac ba-e^{i\theta_c}\right|
\le \frac{\sup|\theta-\theta_c|}{1-L^2/8}.
$$

Einsetzen in $\mathrm{Im}(b/a)/(1+|b/a|^2)$ schliesst den Wahrscheinlichkeitsunterschied bereits zwischen $5{,}8010\cdot10^{-12}$ und $5{,}8049\cdot10^{-12}$ ein. Die Schranke gilt für jedes Paar von Randwerten und damit nach der Integration. Dieser Vorzeichennachweis verträgt auch ein gemeinsames positives endliches Gewicht auf den gepaarten Randwerten, das beide Hälften gleich gewichtet und Gesamtgewicht grösser null hat. Die engeren Zahlen in der Tabelle verwenden das festgelegte flache Mass. [Rationale Intervallrechnung](zertifikat.py)

## Wie nahe der Detektor am Optimum liegt

Für den ergänzenden Vergleich verbleiben Eingangsdichte und Zukunftsbox als Integrationsvariablen. Zunächst fixiert man nur die 15 symmetrischen früheren Achsen in ihrem jeweiligen Zentrum. Die so entstehenden Randfunktionen haben konstanten Betrag über der Zukunftsbox. Die Integration der gemeinsamen Eingangsdichte liefert einen von $z$ und $x$ unabhängigen Betragsfaktor. Zwischen den beiden Zentrumshistorien ändert sich nur die innere Uhr bei 6. Zu 8, 9 und 10 sind ihre Wirkungskoeffizienten null. Die Differenz der inneren Wirkungsterme ist eine Konstante. Die einzige zukunftsabhängige relative Phase lautet somit $\kappa w_7$ bis auf eine additive Konstante, mit $\kappa=D_{7,+}-D_{7,-}=8789/722206720$.

Der Überlapp der normierten Zentrumszustände hat daher den Betrag $|\operatorname{sinc}(\kappa h)|$, mit $\operatorname{sinc}(v)=\sin(v)/v$. Für zwei normierte reine Zustände ist der grösste Unterschied der Wahrscheinlichkeit eines gemeinsamen binären Effekts ihr Spurabstand $\sqrt{1-|\langle\psi_+,\psi_-\rangle|^2}$. Er folgt durch Diagonalisieren der Differenz der beiden Projektoren auf ihrem zweidimensionalen Spann. Die positive Eigenrichtung realisiert das Maximum. [Watrous, *The Theory of Quantum Information*, Kapitel 3, Satz 3.4](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf)

Um diesen Vergleich auf die ganzen Pakete zu übertragen, sei $v=S_d-S_{d,c}$ die Phasenänderung auf den 15 Achsen bei festen äusseren Daten. Die linearen Beiträge mitteln sich auf den symmetrischen Boxen zu null. Das gilt auch für die Dichteverschiebungen, da sie unabhängig von den Uhrverschiebungen sind. Für jede Kante verbleibt im Mittel des quadratischen Terms höchstens $|b_{ij}|w_{j,c} n_{ij}R^2/114$, wobei $R=2^{-32}$ und $n_{ij}$ die Zahl ihrer variierten Uhrendpunkte ist. Mit $|e^{iv}-1-iv|\le v^2/2$ folgt

$$
|\langle e^{iv}\rangle-1|
\le |\langle v\rangle|+\tfrac12\sup |v|^2 .
$$

Der Code schliesst beide Summanden für jedes feste äussere Datum ein. Nach der Integration und Normierung beträgt das gesamte Spurabstands-Fehlerbudget beider Pakete zusammen weniger als $4{,}658\cdot10^{-18}$. Die Dreiecksungleichung überträgt damit sowohl das Optimum als auch den Ausgang des festen Detektors von den Zentren auf die ganzen Pakete. Für einen rein diagonalen Effekt, also eine Multiplikation mit einer Funktion der sieben Zukunftskoordinaten zwischen null und eins, haben die beiden normierten Zentrumszustände exakt dieselbe Wahrscheinlichkeit. Der gesamte mögliche Unterschied für diese Klasse ist deshalb durch dasselbe Fehlerbudget begrenzt. Die Winkel und Quadratwurzeln der Zertifikate werden mit rationalen Schranken eingeschlossen. [Fehlerbudget und Optimalitätsvergleich](optimal.py) · [Maschinenlesbare Ergebnisse](ergebnis.json)

## Unabhängige Gegenrechnung und offene physikalische Frage

Eine direkte Quadratur bildet das Doppelintegral mit getrennten früheren Variablen in Amplitude und konjugierter Amplitude am gemeinsamen Zukunftswert. Zwei Sobol-Verwürfelungen mit jeweils 256, 1 024 und 4 096 Punkten ergeben rund $5{,}8029393\cdot10^{-12}$ für die Differenz. Zur numerischen Stabilität werden die kleinen Abweichungen von $1/2$ unmittelbar berechnet. Die sechs Quadraturen sind Gegenproben. Die Fehlergrenzen und die Optimalitätsaussage stammen aus den analytischen Einschlüssen. [Quadraturcode](quadratur.py) · [Alle sechs Läufe](quadratur.json)

Die physikalische Frage lässt sich als Kommutatortest formulieren. Sei $M$ die Multiplikation mit $w_7$. Die normierten Zentrumszustände sind bis auf eine globale Phase durch $U=\exp(i\kappa M)$ verbunden. Für jeden Effekt $0\le E\le 1$ gilt

$$
|P_+(E)-P_-(E)|\le \varepsilon+|\kappa|\,\|[M,E]\|,
\qquad \varepsilon<4{,}658\cdot10^{-18}.
$$

Dazu integriert man die Ableitung von $e^{-itM}Ee^{itM}$ von null bis $\kappa$ und addiert das Fehlerbudget der beiden Pakete. Die kleine Schranke gilt daher sogar für **jeden mit $w_7$ kommutierenden Effekt**, auch wenn er die sechs übrigen Zukunftskoordinaten kohärent mischt. Im Zweierblock des festen Detektors ist $M=\operatorname{diag}(x,x+h)$ und die Norm seines Kommutators mit $E_+$ ist exakt $h/2$. Jeder Detektor mit mindestens demselben zertifizierten Kontrast benötigt mehr als $0{,}99999\,h/2$ Kommutatornorm. Erlauben die Constraints des gekoppelten Modells einen solchen Effekt? Unter der geprüften Paarung ist er positiv und wohldefiniert. Eine aus der Dynamik hergeleitete Randpaarung und die experimentelle Realisierung dieser kohärenten Auslese stehen aus.

### Breitenkontrolle und Nachrechnung

Eine ergänzende Breitenkontrolle vergrössert alle 15 neuen Halbachsen von $2^{-32}$ auf $2^{-24}$. Auch dort sind beide Pakete durchgehend vorzeichenrein, und der bedingte Wahrscheinlichkeitsabstand desselben Ports übersteigt $5{,}3124\cdot10^{-12}$. Bei $2^{-23}$ trennen sich die Portantworten weiter, aber die benutzten Stromeinschlüsse überdecken null. Die Optimalitätstabelle bezieht sich ausschliesslich auf die vorab festgelegte Breite $2^{-32}$.

Im entpackten Studienordner ausführen. Die exakten Zertifikate verwenden nur die Python-Standardbibliothek.

```sh
sha256sum -c SHA256SUMS
python3 -B nachrechnen.py > nachrechnung.json
cmp ergebnis.json nachrechnung.json
```

Die numerische Gegenrechnung läuft mit `python3 -B quadratur.py`. Verwendet wurden NumPy 2.3.5 und SciPy 1.17.0. Der [Prüfvertrag](pruefvertrag.json) wurde lokal vor der neuen Rechnung festgelegt. Die Optimalitäts- und Kommutatorschranken sowie die Breitenkontrolle wurden anschliessend ergänzt. Der [Quellenstand](quellen.json) bindet die übernommenen Dateien über Git-Blob-IDs an den Merge von PR #344. [Lizenz](LICENSE) · [NOTICE](NOTICE)
