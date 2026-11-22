# Welche Information über den Anfangsstrom liefert eine zweite Uhrantwort am Eingangsrand?

**CST-DUST · N15 · Einzeltyp 375841 und endlicher Ordnungskatalog · 21. November 2026**

Auf Typ 375841 lässt sich die tatsächlich realisierte Summe der sieben inneren Staubdichten aus vier Werten der ursprünglichen Wirkung am Eingangsrand bestimmen. Damit entfällt eine bislang extern vorgegebene Zahl in der Rückrechnung des Anfangsstroms. Besonders aussagekräftig ist das Zusatzpaar aus PR #342. Seine zwei Pakete haben am Zwischenschnitt und am Zukunftsrand für alle dort betrachteten Quellen identische Antworten. Die neue Eingangsquelle trennt diese Pakete auch nach der kohärenten Summation. Die Skalarreduktion ohne Eingangsquelle liefert weiterhin dasselbe Bild für beide. [Ausgangsversuch und Inversion, PR #342](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/342)

## Zwei feste Uhrverschiebungen lesen die innere Dichtesumme

Wir verwenden $Y=T/\Delta$, $W=w/\Delta$, $\Delta^4=3/722$ und die normierte Staubwirkung

$$
\widehat S=S_d/\Delta=-\tfrac12\sum_jW_j-\tfrac1{38}\sum_{i\prec j}b_{ij}W_j(Y_i-Y_j)^2.
$$

Der Koeffizient $b_{ij}$ hat für null, eins, zwei und drei Zwischenereignisse die Werte $1,-9,16,-8$. Bei mehr Zwischenereignissen verschwindet er. Die vier Eingangsereignisse bilden eine geordnete Kette. Die Profile $u,v$ werden nach dem Rang auf dieser Kette zugeordnet und sind ausserhalb null. Für $Y\mapsto Y+a u+b v$ halten wir Ordnung, alle übrigen Felder, Gewichte und Integrationsfenster fest. Die Uhrquellen sind Argumente der Wirkung. Die Präparationsfenster werden bei ihrer Variation nicht neu zentriert.

Bei einem inneren Ziel $j$ sei $d_j$ die **Anzahl aller seiner inneren Vorgänger**. Zwischen dem Eingang vom Rang $i=0,1,2,3$ und $j$ liegen $3-i+d_j$ Ereignisse. Zeilenweise nach $d_j=0,1,2,3$ ergibt sich die Matrix

$$
B=\begin{pmatrix}-8&16&-9&1\\0&-8&16&-9\\0&0&-8&16\\0&0&0&-8\end{pmatrix}.
$$

Wir setzen $u=(1,1,1,1)$ und verlangen denselben Koeffizienten für jede dieser vier Klassen. Die ganzzahlige Normierung $Bv=-64u$ ergibt eindeutig $v=(76,47,24,8)$. Diese Wahl benutzt allein die Ordnung und den Wirkungsansatz. Da $u$ auf der Eingangskette konstant ist, entfallen alle Beiträge innerhalb des Eingangs. Zwischen Eingang und Zukunft liegen sämtliche sieben inneren Ereignisse. Daher verschwinden auch die direkten Zukunftsbeiträge. Die gemischte Antwort lautet exakt

$$
\frac{19}{64}\partial_a\partial_b\widehat S
= -\frac{1}{64}\sum_{i\prec j}b_{ij} W_j(u_i-u_j)(v_i-v_j)
=\sum_{j\in I,\ d_j<4}W_j.
$$

Auf Typ 375841 sind die beiden inneren Ketten $4\prec5\prec14$ und $6\prec11\prec12\prec13$. Jedes Ziel hat höchstens drei innere Vorgänger. Hier ist die rechte Seite also $W_{\rm ges}=\sum_{j\in I}w_j/\Delta$. Für die unskalierte Wirkung und dieselben dimensionslosen Uhrverschiebungen beträgt der Vorfaktor $19/(64\Delta)$.

Die gemischte Ableitung folgt bei dieser quadratischen Wirkung ohne Differenzenfehler aus den vier Werten $\widehat S(Y\pm h u\pm k v)$, kombiniert mit Vorzeichen $+,-,-,+$ und geteilt durch $4hk$. Die Eingangssteigungen fallen dabei heraus. Die erste gemeinsame Eingangsvariation, die den Vergleichsstrom definiert, wird der Rückrechnung nicht mitgeteilt. [Quelle und Vierpunktformel](randquelle.py)

## Rückrechnung und Kontrolle am bisherigen Gegenpaar

Die Inversion aus PR #342 erhält die so gewonnene Summe, das Uhrprofil, die beiden Schnittdichten, die vier Zukunftsdichten sowie die ersten Uhrantworten bei 5 und 11 und die zweite bei 11. Erst nach der Prognose werden die wirkliche Summe und $p_P=-\partial_a\widehat S(Y+a u)|_{a=0}$ zum Vergleich berechnet. Beide Ergebnisse stimmen in **224 von 224** rationalen Feldbelegungen exakt. Der Prüfer benutzt zwei feste Schrittpaare $(1/256,1/16384)$ und $(1/512,1/32768)$, jeweils für dieselbe Historie. Die Stichprobe umfasst vier bekannte Paarfamilien mit je 20 Paaren einschliesslich ihrer Zentren und 64 weitere Belegungen aus dem breiteren Präparationsfenster. Unter diesen 64 tragen 50 positiven und 14 negativen Strom. Der Test verwendet die unentwickelte Wirkung und einen neuen Zufallsstartwert. Die bekannten Konstruktionen sind Teil des internen Tests. [Nachrechnung](nachrechnen.py) · [Ergebnisse](ergebnis.json)

| Grösse am Zentrum des Zusatzpaars | Positiver Anfangsstrom | Negativer Anfangsstrom |
|---|---:|---:|
| Rekonstruierte innere Dichtesumme $W_{\rm ges}$ | $10584931/9961472$ | $10583197/9961472$ |
| Anschliessend rekonstruierter Strom $p_P$ | $2601/757071872$ | $-2601/757071872$ |

Auch ohne Paarzuordnung lassen sich die zwei ganzen Zellen anhand ihrer Summen unterscheiden. Bei $M=1/4$ und $e_0=-1/4$ liegt die Schwelle $M(4-e_0)=17/16$ zwischen den disjunkten Wertebereichen. Nach aussen gerundet liegen diese bei $[1{,}06258610,1{,}06258797]$ für das positive und $[1{,}06241203,1{,}06241390]$ für das negative Paket. Für den Beweis summieren sich die normierten Verweilanteile jeder Kette durch Teleskopieren zu eins und die zwei gemeinsamen Dichteverschiebungen zu null. Zu berücksichtigen sind die sieben unabhängigen Dichteabweichungen mit Halbbreite $10^{-7}$ und die entgegengesetzten Verschiebungen $\pm(C_6-C_4)/64$ der normierten Dichtesumme. Hier ist $C_j=1+\sum_{i\prec j} b_{ij}(Y_i-Y_j)^2/19$.

Der Schwellentest ist auf dieses Paar begrenzt. In den drei anderen Paarfamilien tragen die Zweige bei gleicher Summe entgegengesetzte Ströme. Eine zweite *gleichförmige* Eingangsvariation als Negativkontrolle ergibt beim Zusatzpaar identische Antworten, weil die Zeile der minimalen Ziele 4 und 6 die Summe null hat. [Rationale Intervalle für die ganzen Zellen](zellen.py)

## Was in der kohärenten Amplitude übrig bleibt

Die Vierpunktformel für die Wirkung setzt vier Quellenwerte derselben Feinhistorie voraus. Für die kohärente Amplitude $A_\pm(a,b)=\int_{P_\pm}e^{iS_d(Y+au+bv)}\,d\mu$ muss zuerst die komplexe Exponentialfunktion variiert werden. Die gemeinsame Gravitationsphase und der gemeinsame Skalarzustand des Einzeltyps sind ausgeklammert. Es gilt

$$
\partial_a\partial_b e^{iS_d}=(iS_{ab}-S_aS_b)e^{iS_d}.
$$

Am Nullpunkt der Quellen haben die gepaarten Historien exakt dieselbe Phase. Mit $\delta$ für positives minus negatives Paket ist der reelle Anteil von $-i$ mal ihrer gemischten Amplitudendifferenz folglich $\cos(S_d)\,\delta S_{ab}-\sin(S_d)\,\delta(S_aS_b)$. Auf den ganzen Zellen gilt $S_d\in(-0{,}618,-0{,}392)$, $\delta S_{ab}>0{,}00014858$ und $|\delta(S_aS_b)|<0{,}00001671$. Der Prüfer schliesst hierfür die tatsächlichen ersten Antworten beider Profile und die gemeinsame Eingangsdichte ein. Die Paarabbildung ist bei festen Uhren eine Dichtetranslation mit Jacobi-Determinante eins. Damit gilt bei allen freigegebenen Zukunftsdaten und für das gemeinsame positive Hilfsmass

$$
\frac{\operatorname{Re}[-i\partial_a\partial_b(A_+-A_-)(0,0)]}{\mu(P_+)}
>10^{-4},\qquad \mu(P_+)=\mu(P_-)>0.
$$

Als ergänzende numerische Kontrolle liefert die direkte Vierpunktdifferenz der unintegrierten Phasenfaktoren **am Zentrum** bei den beiden Schrittweiten $0{,}00012679253504$ und $0{,}00012679252568$ für ihren gemischten Imaginärteil. Die Schranke über die ganzen Pakete folgt aus den rationalen Einschlüssen der Ableitung am Nullpunkt.

Eine Quellenableitung der bereits summierten Amplitude enthält somit auch ein Produkt erster Antworten. Beispielsweise ist für die beiden gleich gewichteten, gleichphasigen Zentrumshistorien $\operatorname{Cov}(S_a,S_b)/\Delta^2=701325837/71644727421698048$. Dieser Term tritt bei $A\ne0$ in $\partial_{ab}\log A=i\langle S_{ab}\rangle_A-\operatorname{Cov}_A(S_a,S_b)$ auf. Die Klammern sind normierte komplexe Amplitudengewichte. Der endliche Befund ist eine von null getrennte Amplitudenantwort. Wie ein Instrument daraus mit der physikalischen Randpaarung einen auslesbaren Record erzeugt, bleibt offen.

## Geltungsbereich im N15-Katalog

Für jedes der 1 048 zugelassenen Ordnungsdiagramme wurden die offenen Intervalle zwischen den vier Eingangsereignissen und allen inneren und zukünftigen Zielen direkt gezählt. Die Zahl der erfassten inneren Dichten verteilt sich wie folgt.

| Erfasste Dichten von sieben | Zahl der Typen |
|---:|---:|
| 7 | 202 |
| 6 | 534 |
| 5 | 291 |
| 4 | 21 |

Im bisher gewichteten Ensemble sind **35 von 453** Typen vollständig sichtbar. Zusammen erhalten sie unter den zwei archivierten, je zur Hälfte mit dem Kettengesetz kombinierten Typverteilungen rund **1,825 %** (1:1) bzw. **1,862 %** (1:3) der eingesetzten Gewichte. Diese Anteile zählen Typgewichte vor der kohärenten Summation. Ein konkreter Fall ist Typ 39391. Sein Ereignis 12 hat vier innere Vorgänger. Jede seiner vier Wirkungsbeziehungen vom Eingang hat Koeffizient null. Eine Variation seiner Dichte bei sonst festen Feldern ändert die Gesamtsumme. Ihr Beitrag zur Wirkung ist jedoch unabhängig von allen Eingangsuhrquellen und verschwindet aus jeder quelleninduzierten Wirkungsänderung. Auch der direkt definierte Anfangsstrom hängt bei festen Feldern nur von sichtbaren Zielen ab. Aus der Reichweite der Summenmessung folgt deshalb noch keine Reichweite für die Strominversion auf anderen Typen. [Katalogrechnung](katalogtest.py) · [Verwendete GitHub-Quellen](quellen.json)

Der unmittelbar offene Test betrifft die übrigen Eingaben der Inversion. Welche Kombination der inneren Uhren lässt sich aus denselben zugänglichen Rand- und Schnittquellen bestimmen? Eine solche Inversion müsste auch an Gegenpaaren mit identischen zugelassenen Eingaben bestehen. Die physikalische Paarung, eine unabhängige Masse-Ladungs-Kalibrierung und die mitbewegte Fläche für P3 sind eigene offene Aufgaben.

## Reproduktion

Im entpackten Studienordner ausführen. Python 3 mit Standardbibliothek genügt.

```sh
sha256sum -c SHA256SUMS
python3 -B nachrechnen.py > nachrechnung.json
cmp ergebnis.json nachrechnung.json
```

Der [Prüfvertrag](pruefvertrag.json) wurde vor den neuen Prüfläufen lokal festgehalten. Die Schwelle für die beiden ganzen Zellen, die Aufteilung der Typgewichte und die numerische Kontrolle der endlichen Amplitudendifferenz ergänzen diesen Vertrag. Die zwölf übernommenen Quelldateien sind über ihre Git-Blob-IDs an den Merge von PR #342 gebunden. [Quellenstand](quellen.json) · [Lizenz](LICENSE) · [NOTICE](NOTICE)
