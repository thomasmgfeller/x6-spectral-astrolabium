# Überlebt der Vorzeichendetektor die Weiterverklebung des N15-Zukunftsrands?

**CST-DUST · N15-Typ 375841 · Anschluss an PR #345 · 21. November 2026**

Der Detektor von PR #345 ist am offenen Rand wohldefiniert. Bei der geprüften Fortsetzung ändert sich der Randraum. Wird die ehemalige Zukunftsdichte $w_7$ an der gemeinsamen Naht mit ihrem flachen Mass kohärent ausintegriert, können zwei dort gleichwertige Amplituden nach Anwendung desselben Detektors verschiedene Ausgänge haben. Das lässt sich sowohl an einer glatten Nullrichtung als auch auf den ganzen Vorzeichenpaketen zeigen.

Für die beiden publizierten Pakete beträgt der grösstmögliche Unterschied einer Ausgangswahrscheinlichkeit **nach diesem Anschluss weniger als $4{,}658\cdot10^{-18}$**. Wird zusätzlich die Amplitudendifferenz der beiden Dichtehälften mitgeführt, erreicht derselbe Detektor wieder rund **$5{,}803\cdot10^{-12}$**. Eine gewöhnliche quellenfreie Fortsetzung der untersuchten Art erzeugt diese zweite Auslese nicht. [Detektor und Pakete, PR #345](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/345) · [Frühere Herleitung der erweiterten Verklebung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/04ded4cf96c6486b182e50df1eaa359991e02f3b/research/rax_cqg/dust_collapse/extended_sewing_v0_1)

| Geprüfte Bedingung | Befund auf diesem Typ |
|---|---|
| Gemeinsame Umbenennung aller Felder, Rollen und des Detektors | Kovariant in allen 35 Geburtsreihenfolgen der Ordnung |
| Gemeinsame Verschiebung der Uhren, ihrer Anker und Fenster | Die Dichteantwort und das Instrument bleiben invariant |
| Starke klassische Dichtestationarität | Schon am inneren Ereignis 4 erfüllen beide ganzen Pakete die Gleichung nicht |
| Bedingte Dichteableitung der Wirkung | Die selektierte Amplitude des Detektors hat einen nachweisbaren inneren Sprung |
| Verträglichkeit mit der Nullrichtung der flach geschlossenen Dichte | Widerlegt |
| Kleinste unter dem Detektor abgeschlossene Erweiterung des flachen Nahtmodus | Zwei kohärente Amplituden je Wert der übrigen Randdaten |
| Von der gekoppelten Dynamik hergeleiteter physikalischer Zustandsraum | **HOLD** |

## 1. Welcher Anschluss hier tatsächlich gerechnet wird

Wir verwenden unverändert das in PR #345 vorbereitete Fenster $w=w_7\in[m-h,m+h]$ mit $m=1/8$, $h=2^{-20}$. Alle übrigen offenen Randdaten $z$ einschliesslich der sechs Staubkoordinaten bleiben verfügbar. Die zwei vorzeichenreinen Pakete haben die dort festgelegte Halbbreite $2^{-32}$ auf den 15 früheren Achsen. Der gemeinsame normierte Skalarfaktor und die feste Gravitationsphase sind ausgeklammert.

Zuerst wird hinter den vollständigen alten Zukunftskragen $F=(7,8,9,10)$ ein neues Ereignis gesetzt, das alle alten Ereignisse in seiner Vergangenheit hat. Als Kontrollen folgen zwei neue Ereignisse in Kette bzw. zwei unvergleichbare neue Ereignisse. Die alten Intervalle ändern sich nicht. Von jedem alten Ereignis vor dem Zukunftskragen zu jedem neuen Ziel liegen mindestens vier alte Zukunftsereignisse im offenen Intervall. Für solche Beziehungen ist das Wirkungsgewicht null. Für das erste neue Ziel tragen die vier alten Zukunftsuhren die Gewichte $(-8,16,-9,1)$. Für das zweite Ziel der Kette lauten sie $(0,-8,16,-9)$. Eine neue Staubbeziehung trägt ausschliesslich die Dichte ihres neuen Ziels. Somit darf die alte Uhr $Y_7$ die neue Phase beeinflussen, während die alte Dichte $w_7$ in keinem neuen Term vorkommt.

Die Direktrechnung zählt sämtliche Intervalle der verbundenen Ordnung neu und vergleicht die gesamte Staubwirkung mit alter Wirkung plus Zusatzwirkung. Auch die Endpunktabhängigkeit des skalaren quadratischen Terms wurde kontrolliert. Bei festen neuen Feldern wirkt die neue Staubphase auf den behaltenen Daten durch Multiplikation mit einem Faktor vom Betrag eins. Das gilt ebenso für jeden endlichen hinter den ganzen Kragen gesetzten geordneten Block. Für dieses Experiment bleibt die positive Präparation im alten Fenster bestehen. Das frühere Atom bei Dichte null liegt ausserhalb des Fensters. Die weitere Integration über $w_7$ mit einheitlichem Gewicht ergibt bis auf einen gemeinsamen Normierungsfaktor die Abbildung

$$
(R f)(z)=\frac{1}{2h}\int_{m-h}^{m+h} f(w,z)\,dw .
$$

Dies ist ein **kohärentes Integral der Amplitude**. Ein Vergessen des Messwerts in einer Dichtematrix durch partielle Spur ist eine andere Operation. Die positive Form der hier geprüften Naht ist $\langle Rf,Rg\rangle$. Zwei Randfunktionen sind an dieser Naht gleichwertig, wenn $R(f-g)=0$. Die Rechnung betrifft den Dichteanteil des Anschlusses bei behaltenen übrigen Randdaten. Es wird kein neues N16-Wachstumsgewicht und keine physikalische Paarung für alle Schnitte postuliert.

Ergänzend wurden alle 28 nach unten abgeschlossenen Vorgängermengen einer einzelnen neuen Geburt an der alten Ordnung geprüft. Auch hier enthält die Zusatzwirkung keine alte Dichte. Nur bei leerer oder vollständiger Vorgängermenge stammen jedoch alle nichtverschwindenden alten Quelluhren aus dem bisherigen Zukunftskragen oder es gibt keine solchen Uhren. In den übrigen Fällen kann eine neue Amplitude über früher verborgene Uhrdaten entstehen. Die Schranke für die geschlossene Naht wird daher nicht auf alle Wachstumshistorien ausgedehnt. [Ordnungen und Wirkungsprüfung](anschluss.py)

## 2. Zwei explizite Nulltests

Schreibe $D_*=-21166501/6225920$, $a=hD_*$ und $r=e^{-ia}$. Auf gepaarten Werten $w,w+h$ aus unterer und oberer Hälfte ist der Detektor von PR #345 in den ursprünglichen Komponenten

$$
E=\tfrac12\begin{pmatrix}1&-ir\\i\bar r&1\end{pmatrix}.
$$

Damit eine Operation $\widetilde E$ nach dem Anschluss die ursprüngliche Selektion darstellen kann, muss $\widetilde E R=R E$ gelten. Bereits eine einzige Amplitude mit $Rn=0$ und $REn\ne0$ widerlegt dies. Für den normierten glatten Zeugen $n(w)=\sqrt3(w-m)/h$ ergibt sich bei jedem $z$

$$
Rn=0,\qquad R E n=-i\,\frac{\sqrt3}{4}\cos a .
$$

Hier ist $\cos a>0{,}9999999999947$. Das Gegenbeispiel benötigt keine Identifikation der beiden äusseren Fensterenden. Für $\Pi=R^\dagger R$ ist sogar $\|[\Pi,E]\|=|\cos a|/2$. Die frühere Aussage, dass $E$ die Nullrichtungen der **offenen** Randabbildung respektiert, bleibt mit diesem Befund vereinbar. Die weitere Integration erzeugt zusätzliche Nullrichtungen.

Der zweite Test verwendet die **ursprünglichen ganzen Pakete**. Bei einer Zentrumshistorie schreibe $f_D(w)=e^{iD(w-m)}$ mit $D=\partial_{w_7}S_d$. Eine Integration über die beiden Hälften ergibt

$$
\frac{R E f_D}{R f_D}
=\frac12+\frac12\left[\cos(a)\tan(hD/2)-\sin(a)\right].
$$

Für die ganzen Paketbilder $A_+,A_-$ haben die beiden Nenner $RA_s(z)$ für alle $z$ einen von null getrennten Betrag je Paketmass. Die Differenz $n_z=A_+/(R A_+)-A_-/(R A_-)$ ist also eine wohldefinierte Nullrichtung. Die Faktoren sind nur Funktionen der behaltenen Randdaten. Dies ist ein algebraischer Zeuge im getesteten Randraum. Ihre separate experimentelle Präparierbarkeit bleibt offen. Es gilt an jedem behaltenen Randwert

$$
2{,}90146\cdot10^{-12}<\operatorname{Re}(RE n_z)<2{,}90148\cdot10^{-12}.
$$

Für die Schranke wurden die symmetrischen 15-Achsen-Mittel und das punktweise Amplitudenfehlerbudget aus PR #345 neu berechnet. Ist $|A-A_c|\le e$ je Paketmass, so gilt auch $|R(A-A_c)|, |RE(A-A_c)|\le e$. Der zentrumsbezogene Nenner ist mindestens $c\operatorname{sinc}(hD)$ mit $c=1-L^2/8$ und der jeweiligen Staubphasenspanne $L$. Der Prüfer propagiert den Fehler durch beide Quotienten. Dies erfasst mögliche komplexe Unterschiede über die ganzen Pakete. [Exakte Einschlüsse](ergebnis.json)

## 3. Was nach dem Schliessen des Fensters gemessen werden kann

Bei den Zentren gilt $A_{s,c}(w,z)=c_s(z) f_{D_s}(w)$. Nach PR #345 hat $c_+(z)/c_-(z)$ einen von $z$ unabhängigen Wert. Die flache Integration multipliziert jede Zentrumsamplitude mit $\operatorname{sinc}(hD_s)$. Ihre beiden normierten fortgesetzten Zustände stimmen folglich bis auf eine globale Phase überein. Für ganze Pakete erhöht die Normierung den Abstand zum zugehörigen Zentrum höchstens um $2e/[c\operatorname{sinc}(hD_s)]$. Die Summe beider Fehler ist kleiner als $4{,}658\cdot10^{-18}$. Sie begrenzt den Unterschied der beiden Ausgangswahrscheinlichkeiten für **jeden** binären Effekt auf den behaltenen Daten. Der feste Anschluss mit denselben neuen Feldern fügt nur die gemeinsame Phase hinzu. Weitere selektive Nachpräparationen oder Postselektion auf seltene Ausgänge gehören nicht zu dieser Schranke.

Man kann den fehlenden Randwert genau benennen. Sei $s(w)=-1$ unten und $+1$ oben. Im normierten flachen Mass sind $1,s$ orthonormal. Eine um eine Komponente erweiterte Naht überträgt $R_2 f=(Rf,R(sf))$. Die beiden Koeffizienten sind die Summe bzw. die Differenz der Halbintegrale. Auf diesen Komponenten wirkt der feste Detektor durch

$$
E_2=\tfrac12\begin{pmatrix}
1-\sin a&-i\cos a\\
i\cos a&1+\sin a
\end{pmatrix},\qquad R_2 E=E_2 R_2 .
$$

Der Nachweis gilt für jede quadratintegrierbare Eingabe. Da $E1$ einen nichtverschwindenden Anteil entlang $s$ hat und $E$ diesen Zweimodenraum erhält, ist das der **kleinste abgeschlossene, unter $E$ invariante Raum von Nahtmoden, der den flachen Modus enthält**, je $z$. Die Matrix ist ein orthogonaler Projektor. Die beiden Moden sind kohärente Amplituden. Eine Registrierung nur ihrer einzelnen Wahrscheinlichkeiten würde den Kreuzterm verlieren.

Bei den Paketzentren tragen beide Halbmittel den gemeinsamen Faktor $\operatorname{sinc}(hD_s/2)$. Der normierte Zweimodendetektor erreicht damit genau die zentrumsbezogene Wahrscheinlichkeit des offenen Ports. Für die ganzen Pakete ergibt sich einschliesslich beider Normierungsfehler

$$
5{,}802934\cdot10^{-12}<P^{(2)}_+-P^{(2)}_-<5{,}802945\cdot10^{-12}.
$$

Eine zusätzliche glatte Dichtemessung kann andere Information liefern. Behält man neben $1$ nur einen normierten, zum flachen Modus orthogonalen Modus $g$, beträgt der fehlende Anteil der Funktionalauslese $RE$ in Operatornorm $|\cos a|\sqrt{1-|\langle s,g\rangle|^2}/2$. Beim linearen Dichtemoment $g=\sqrt3(w-m)/h$ ist $\langle s,g\rangle=\sqrt3/2$, und es verbleibt eine Restnorm von $|\cos a|/4$. Für die exakte Weitergabe dieses scharfen Detektors ist also auch die Form der Zusatzinformation festgelegt. Die geprüfte quellenfreie Wirkung liefert den Vorzeichenwechsel der Nahtgewichtung nicht von selbst. Sein Transport durch einen zusätzlichen physikalischen Freiheitsgrad oder eine begründete Nahtpaarung ist offen.

## 4. Was die bisherigen Constraints entscheiden

**Symmetrien.** Der Dichteort 7 ist das eindeutige minimale Ereignis des markierten Zukunftskragens. Bei gemeinsamer Umbenennung werden Ort, Rollen, Fenster und Felder mittransportiert. Die Intervalle und damit auch $D_7=-C_7/2$ sind invariant. Bei einer gemeinsamen Verschiebung sämtlicher Uhren und ihrer Fenster hängen die Koeffizienten weiter nur von Uhrdifferenzen ab. Diese Aussagen wurden auf allen 35 Verzahnungen der beiden inneren Ketten und mit zwei Uhrenursprüngen geprüft. Sie gelten algebraisch auch für beliebige gemeinsame Verschiebungen. [Labelconstraints und Reichweite der Hilfspaarung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/04ded4cf96c6486b182e50df1eaa359991e02f3b/research/rax_cqg/dust_collapse/quantum_structure_v0_1/DERIVATION.md)

**Variationsgleichungen.** Auf dem inneren positiven Dichtestratum gilt $\partial_{w_4}S_d=-C_4/2$, mit $C_4>0{,}058$ auf beiden ganzen Paketen. Eine starke klassische Forderung $C_4=0$ würde also die beiden Prüfpakete vollständig ausschliessen. Am bisher offenen Rand ist $D_7$ eine Randantwort. Selbst seine spätere Integration über das endliche positive Band ist keine Delta-Projektion auf $D_7=0$. [Wirkungsableitung, Integrationsränder und Atomgrenze](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/04ded4cf96c6486b182e50df1eaa359991e02f3b/research/rax_cqg/dust_collapse/ward_constraints_v0_1/DERIVATION.md)

**Bedingte Quellgleichung.** Bei festgehaltenen anderen Feldern ist $(-i\partial_w-D)f_D=0$ eine exakte Identität der affinen Dichtephase. Auf jeder offenen Fensterhälfte erfüllt auch $E f_D$ diese Differentialgleichung. Der rechtsseitige minus linksseitige Grenzwert am Mittelpunkt beträgt jedoch $i\cos(h(D-D_*)) f_D(m)$. Die distributionelle Ableitung liefert dort einen Delta-Term mit Koeffizient $\cos(h(D-D_*)) f_D(m)$. Endterme am äusseren Rand können einen Sprung im Inneren nicht aufheben. Bei ganzen Paketen ist der Sprung das kohärente Integral von $i\cos(h(D-D_*))e^{iS_d(m,z)}$ je Historie, bis auf die gemeinsamen Skalar- und Gravitationsfaktoren. Der Betrag ist auf beiden Paketen grösser als $0{,}99$ je Paketmass. Der scharf ausgewählte Ausgang erhält die Glattheit der ursprünglichen Quellenamplituden daher nicht. Ein beliebiges integrables Gemisch früherer Quellen erfüllt im Allgemeinen keine geschlossene Gleichung mit einem einzigen festen $D$. Weitergehende Dirac- oder Selbstadjungiertheitsbedingungen sind aus dieser bedingten Identität nicht hergeleitet.

**Physikalischer Status.** Die zwei konkreten Abbildungen $R$ und $R_2$ definieren positive, aber verschiedene Randprodukte und Nullräume. Die kinematischen Symmetrien lassen beide zu. Der unmarkierte Anschluss realisiert in diesem Dichtekanal $R$. Der zweite Modus benötigt einen eigenen Ursprung. Eine physikalische Aussage über $E$ erfordert die tatsächlich aus der gekoppelten Theorie gewählte Abbildung und die Verträglichkeit des Instruments mit ihr. Die Bedeutung dieser Auswahl für die physikalische Paarung ist auch in der allgemeinen Constraintquantisierung ausdrücklich benannt. [Etappe 4 im Projekt](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/04ded4cf96c6486b182e50df1eaa359991e02f3b/research/rax_cqg/dust_collapse/stage_reviews_4_7) · [Giulini und Marolf zur physikalischen Paarung](https://arxiv.org/abs/gr-qc/9812024)

## Reproduktion

Im entpackten Studienordner ausführen. Die Intervall- und Strukturprüfungen benötigen nur Python 3.9 oder neuer.

```sh
sha256sum -c SHA256SUMS
python3 -B nachrechnen.py > nachrechnung.json
cmp ergebnis.json nachrechnung.json
```

Die unabhängige Gegenrechnung integriert die ursprüngliche Dichtephase direkt an den Paketzentren für drei Belegungen der behaltenen Daten. Sie verwendet je zwölf Gauss-Legendre-Punkte pro Fensterhälfte und wiederholt die Auswertung bei 60 und 85 Dezimalstellen. Mit mpmath 1.3.0 liefert `python3 -B gegenprobe.py` die hinterlegte [Gegenrechnung](gegenprobe.json). Die Schranken für die ganzen Pakete stammen aus dem analytischen Nachweis.

Der lokale [Prüfvertrag](pruefvertrag.json) wurde vor den neuen Prüfläufen festgelegt. Die vollständige Aufzählung der 28 Geburtsmöglichkeiten und die Hochpräzisionsquadratur ergänzen ihn. Die übernommenen Programme, Ergebnisse und die massgeblichen früheren Herleitungen sind an den [Quellenstand](quellen.json) gebunden. [Lizenz](LICENSE) · [NOTICE](NOTICE)
