# Ein neues Ereignis liest eine Spur des erhaltenen Anfangsstroms aus

**CST-DUST · N15-Typ 375841 mit einem markierten N16-Ausgang · 21. November 2026**

Bei einer geeigneten Fortsetzung über die lange innere Kette unterscheidet ein gemeinsamer Dichtedetektor die beiden ganzen, vorzeichenreinen Pakete aus PR #345. Die unveränderte Staubwirkung koppelt eine früher verborgene Uhr an die Dichte des neuen Ereignisses. Der Anfangsstrom, jetzt aus der gesamten N16-Wirkung abgeleitet, bleibt für jede Feldbelegung exakt der alte. Der Unterschied der bedingten Wahrscheinlichkeiten desselben Ausgangs beträgt rund $1{,}25639\cdot10^{-11}$. Die frühere Zukunftsdichte wurde dabei bereits kohärent geschlossen. Ein zweites Paketpaar innerhalb derselben Modellfamilie reproduziert den Effekt ohne Nachanpassung des Detektors. Die Resultate gelten für einzeln präparierte, markierte Fortsetzungen und eine festgelegte positive Randpaarung. [Offener N15-Rand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/345) · [Schliessen des N15-Fensters](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/346)

Der zugehörige elfseitige [Teilartikel bis PR #346 (PDF)](manuskript/Teilartikel.pdf) und seine [editierbare Fassung](manuskript/Teilartikel.html) fassen die vorherige Beweiskette zusammen. Der [Offline-Prüfumfang](altstudien/README.md) umfasst 14 Originalrechnungen und vier zusätzliche Gegenkontrollen.

## Drei Anschlüsse mit demselben Messprinzip

Sei $\delta P=P(E\mid p_P^{(15)}>0)-P(E\mid p_P^{(15)}<0)$. Die Tabelle gibt **Einschlüsse für die ganzen Pakete**, nach aussen gerundet. $P$ in der ersten Spalte ist die viergliedrige alte Eingangskette. $q$ bezeichnet die Verschiebung der Paketzentren aus PR #344.

| Vorgänger des neuen Ereignisses | Wirkung auf den Anfangsstrom | $\delta P$ bei publiziertem Paar, $\lvert q\rvert=2^{-24}$ | $\delta P$ beim Transfer, $\lvert q\rvert=2^{-25}$ |
|---|---|---:|---:|
| $P$ und erstes Ereignis der Viererkette | Beide neuen Ströme sind positiv | $[-1{,}570494,-1{,}570482]\cdot10^{-12}$ | $[-7{,}852494,-7{,}852384]\cdot10^{-13}$ |
| $P$ und vollständige Viererkette | Beide Vorzeichen exakt erhalten | $[1{,}2563894,1{,}2563909]\cdot10^{-11}$ | $[6{,}281943,6{,}281958]\cdot10^{-12}$ |
| Alle 15 alten Ereignisse | Beide Vorzeichen exakt erhalten | $\lvert\delta P\rvert<1{,}494\cdot10^{-29}$ | $\lvert\delta P\rvert<1{,}494\cdot10^{-29}$ |

Die Schranke in der dritten Zeile gilt für den festgelegten Port. Für *jeden* binären Effekt auf dem abgeschirmten Ausgang gilt beim publizierten Paar die gröbere Schranke $4{,}658\cdot10^{-18}$. Am Paketzentrum verschwindet der abgeschirmte Kontrast exakt. Die Wahrscheinlichkeit jeder einzelnen Präparation darf bei festgehaltenen restlichen Randdaten von deren Werten abhängen. Nach Dephasierung zwischen den neuen Dichtehälften gilt exakt $P(E)=1/2$ für jeden Fall. Der mitgeführte alte Selektor bezeichnet die Paketherkunft. Beim ersten Anschluss unterscheidet der neue Ausgang diese Herkunft auch dann, wenn beide **neuen** Anfangsströme dasselbe Vorzeichen haben. [Rationale Ergebnisdaten](ergebnis.json)

## Randrollen und Wirkung

Die alte Ordnung besteht aus einer Eingangskette $P=(0,1,2,3)$, den unvergleichbaren inneren Ketten $(4,5,14)$ und $(6,11,12,13)$ sowie einer Zukunftskette $F=(7,8,9,10)$. Das neue maximale Ereignis $n$ erhält je Fall ein vorab bestimmtes Vorgängerideal. In den ersten beiden Fällen ist es mit allen vier Ereignissen des alten Zukunftskragens unvergleichbar. Die verbleibenden alten Randdaten und der neue Port bilden ein markiertes Auslesesystem. Es ist kein vollständiger späterer Staubschnitt. Beim Anschluss hinter allen alten Ereignissen gibt es nur ein maximales Ereignis.

Die Uhr des neuen Ports ist $Y_n=Y_7+4=6$. Seine physische Dichte $v$ liegt bei $m=1/8$ mit Halbbreite $h=2^{-20}$. Auf der Naht wird die alte Dichte $w_7$ wie in PR #346 flach und kohärent integriert. Die Eingangsdichte durchläuft weiter das volle ursprüngliche Band $[3/32,5/32]$. Die beiden Pakete haben auf ihren 15 früheren Achsen dieselbe Halbbreite $2^{-32}$ wie in PR #345. Die sechs übrigen offenen Staubkoordinaten des alten Kragens bleiben verfügbar. Es gibt weder ein nach dem Stromvorzeichen gewähltes Kopplungsgesetz noch ein zusätzliches Quellfeld. Das gewählte neue Dichte- und Skalarfenster und die kohärente Auslese sind reguläre Bestandteile dieses bedingten Versuchs.

Bei unveränderten alten Intervallen, $\Delta^4=3/722$ und $b(0),\ldots,b(3)=(1,-9,16,-8)$ hat das neue Ereignis die Zusatzwirkung
$$
S_{16}-S_{15}=vD_n(Y),\qquad D_n=-\frac12-\frac1{38}\sum_{i\prec n} b_{in}(Y_i-Y_n)^2
$$
für den Staubteil. Die alte Dichte $w_7$ erscheint darin nie. Dagegen tritt $Y_6$, die einzige zwischen den alten Paketzentren verschiedene Uhr, in 16 der 28 Ideale auf. Zehn dieser 16 haben zusätzlich **keine** aktiven Paare vom Eingang zum neuen Ziel. Für den Anfangsstrom ergibt die Verschiebung sämtlicher Eingangsuhren in physischen Einheiten
$$
p_P^{(16)}-p_P^{(15)}
=\frac{v}{19\Delta}\sum_{i\in P} b_{in}(Y_i-Y_n).
$$
Am kleinsten aktiven Ideal ist der Zusatz in den Zentren $41v/(76\Delta)$ und führt auf beiden ganzen ursprünglichen Paketen zu Strömen zwischen 0,26560 und 0,26561. Beim stromerhaltenden und beim abgeschirmten Anschluss verschwindet er identisch. In allen drei Fällen ergibt auch eine unabhängige symmetrische Differenz der vollständigen Wirkungen den Strom in den Zentren.

## Detektor und Fehler für vollständige Pakete

Für jede alte präparierte Historie wird **zuerst** die neue Phase eingesetzt. Danach werden die 15 inneren Paketachsen, die alte Eingangsdichte und $w_7$ kohärent summiert. Die resultierende Randamplitude ist $A_s(v,z)$ für Paket $s$ und die sechs alten Staubkoordinaten $z$. Die zusätzliche skalare Ausgangsfunktion und die feste Gravitationsphase sind je Ordnung beiden Zweigen gemeinsam. Ihre Berechtigung ist unten gesondert geprüft.

Für $v$ in der unteren Fensterhälfte paart der Detektor $a=A_s(v,z)$ mit $b=e^{-ihD_*}A_s(v+h,z)$. Der Referenzwert $D_*$ wird für jede Ordnung am selben neutralen Uhrprofil berechnet. Der Pauli-$Y$-Ausgang hat die Wahrscheinlichkeit
$$
 P_s=\tfrac12+
 \frac{\int \mathrm{Im}(\overline a b)\,dv\,d\nu(z)}
      {\int(|a|^2+|b|^2)\,dv\,d\nu(z)} .
$$
Die drei Referenzen für minimalen, stromerhaltenden und abgeschirmten Anschluss sind $277282759/249036800$, $4479033/31129600$ und $0$. Eine Zusatzprüfung setzt **in allen drei Fällen dieselbe Referenz null**. Beide ungeschirmten Abstände behalten auf beiden Paaren ihr Vorzeichen. Auch die abgeschirmte Obergrenze gilt mit dieser gemeinsamen Referenz. Ein fester Unterschied nur in der globalen Phase könnte keinen solchen Ausgang trennen.

Auf den Zentren der 15 schmalen Achsen verbleibt bei den zwei ungeschirmten Fällen $A_{s,c}(v,z)=a_{s,c}(z)\exp(ivD_{n,s})$. Die breite Eingangsdichte und die ehemalige Zukunftsdichte sind in $a_{s,c}$ weiterhin integriert. Dort ist $P_{s,c}=[1+\sin(h(D_{n,s}-D_*))]/2$. Im ursprünglichen Paar gilt exakt
$$
D_{n,+}-D_{n,-}=
\begin{cases}
 -19029/5777653760 & \text{minimales Ideal},\\
  19029/722206720 & \text{stromerhaltender Anschluss},\\
  0 & \text{Vollideal bei gleichen restlichen Randdaten}.
\end{cases}
$$
Der Halbierungstest rekonstruiert neue Zentren mit exakt gleicher unverschobener N15-Wirkung durch den publizierten Transfer einer Dichtemenge von Ereignis 6 nach 4. Die strikten Paketvorzeichen und die Lage innerhalb der alten 1-%-Dichtebänder werden erneut rational bewiesen. Es handelt sich um einen lokalen Transfer innerhalb einer bekannten Familie mit denselben Detektoreinstellungen.

Für die vollständigen Boxen werden die 15 unabhängigen, symmetrisch verteilten Abweichungen um das Zentrum berücksichtigt. Sei $U$ eine obere Schranke der absoluten gesamten Phasenabweichung, $B$ eine Schranke ihres absoluten Mittelwerts. Aus $|e^{ix}-1-ix|\le x^2/2$ folgt der Amplitudenfehler je Paketmass $e\le B+U^2/2$. Zu den N15-Schranken kommt pro veränderlicher alter Quelluhr $i$ im neuen Ziel der Beitrag
$$
 U_i=\frac{(m+h)|b_{in}|}{38}\big(2|Y_{i,c}-Y_n|r+r^2\big),\qquad
 B_i=\frac{(m+h)|b_{in}|}{38}\,\frac{r^2}{3},\qquad r=2^{-32}.
$$
Die Terme erster Ordnung haben Mittelwert null. Für festgehaltene neue und verbleibende alte Ausgabedaten ist die zentrumsbezogene Zusatzphase ein Einheitsfaktor. Die Norm der alten zentrumsbezogenen Amplitude einschliesslich beider breiten Dichteintegrale ist je Paketmass mindestens $c=1-L^2/8>0{,}99$, wobei $L$ die zertifizierte alte Phasenspanne bezeichnet. Der Spurabstand des normierten Paketzustands zum normierten Zentrumszustand ist dadurch höchstens $2e/c$. Die Summe beider Fehler überträgt den Sinusvergleich auf die vollständigen Pakete. Alle für die Tabelle verwendeten Endpunkte sind rationale Zahlen. [Prüfer](pakettest.py) · [Genaue Fehler je Zweig](ergebnis.json)

Beim abgeschirmten Anschluss hängt $D_n$ nur von den verbleibenden Uhren ab. Die neue Abbildung multipliziert bei jedem $z$ lediglich mit $e^{ivD_n(z)}$ und ist im normierten flachen $v$-Mass isometrisch. Bereits nach dem alten $w_7$-Integral sind die beiden Zentrumszustände proportional. Denn ihre einzige von alten Zukunftsvariablen abhängige relative Phase war proportional zu $w_7$, und dessen Zentrumssteigungen hängen ausschliesslich von festen Uhren ab. Auf den ganzen alten Zuständen misst der neue Port die Multiplikation mit $f(z)=[1+\sin(h(D_n(z)-D_*))]/2$. Der Abstand ist höchstens der alte Spurabstand mal $\sup f-\inf f$. Die kleine Variation von $D_n$ über dem alten Uhrfenster liefert so die schärfere Portgrenze aus der Tabelle. Für Einzelheiten der Originaleingaben siehe [Quellenstand](quellen.json).

## Verklebung, Skalarfeld und Reichweite

Der innere Schnitt bei $Y=0$ hat die Antikette $\{5,11\}$. Gesamtordnung und über den Schnitt wieder aufgebaute Ordnung liefern in allen drei Fällen exakt dieselben Intervallkoeffizienten. Beim minimalen Ideal muss die Beziehung $6\prec n$ als eigene, den Schnitt überbrückende Kante mitgeführt werden. Lässt man sie weg, fehlen fünf Beziehungen. Beim stromerhaltenden Anschluss ergibt sich die richtige Ordnung aus den lokalen Teilordnungen und gemeinsamem Schnitt. In allen Fällen sind die **Wirkungsbeiträge** der aktiven Kreuzbeziehungen und ihre früheren Felder bis zur Integration mitzuführen. Weil beide Wege punktweise dieselbe Phase haben und die Integrationsmasse genau einmal einsetzen, stimmen auch alle komplexen Produkte der Amplituden überein, einschliesslich der Einträge zwischen den beiden Paketarten sowie den zwei Dichtearmen. Das ist eine bedingte Zusammensetzungsidentität. Ein autonomer physikalischer Transportoperator auf der Antikette allein ist damit offen. [Schnittrechnung](schnitt.py) · [Ergebnisse](schnitt.json)

Der neue skalare Ausgang $q_n$ wird bei sämtlichen Fällen im selben Fenster $[-1,1]$ mit $dq_n/2$ geführt. Der alte Eingang behält seine Gaußpräparation. Wir haben die verdeckten Skalarfelder **mit** den neuen Kreuztermen integriert. In allen drei Fällen ist der Fresnelblock regulär und das verbleibende Skalarpaket hat bei jedem $q_n$ eine endliche, strikt positive Norm. Sie ist von $q_n$ unabhängig. Der Skalarfaktor kürzt sich in beiden Stromzweigen jeder einzelnen Ordnung aus der normierten Auslese. Ohne eine Masswahl für den zusätzlichen skalaren Ausgang ergäbe die ungewichtete Integration über die ganze reelle Achse hier eine unendliche Norm. [Skalarherleitung und Minoren](SKALAR.md) · [Exakte Skalarrechnung](skalar.json)

Eine weitere Kontrolle erhält das frühere exakte Gegenbeispiel aus PR #339. Dessen Translation verschiebt ausschliesslich alte innere Dichten, ist masserhaltend, hat Jacobi-Determinante eins und lässt die alte Wirkung bei gleichen Uhren unverändert. Weil die gesamte neue Zusatzwirkung von diesen alten Dichten unabhängig ist, bleiben die zwei alten Randbilder bei allen drei Fortsetzungen identisch. Ein Port, der für ein geeignetes Paar Information trägt, ist also auch nach dem Wachstum kein universeller Vorzeichendetektor.

Die alten Vorzeichenhäufigkeiten, die physikalische Paarung, die Häufigkeiten der einzelnen Wachstumsordnungen und ein gewöhnlicher gemeinsamer späterer Staubschnitt sind eigene Fragen. Der stromerhaltende Versuch zeigt eine statistische Unterscheidung des entsprechenden Anfangsstroms in einer bedingten endlichen Auslese. Die alte ungerade $w_7$-Nahtmode wird dabei nicht transportiert. Der neue Informationsweg läuft über frühere Uhren und die Phase der **neuen** Dichte.

## Reproduktion und Designentscheidungen

Der [ursprüngliche Prüfvertrag](pruefvertrag.json) legt die beiden ersten Rollen minimaler Anschluss und Abschirmung, die Fenster, die Ausleseregel sowie das Transferpaar fest. Nach der Strukturprüfung des Zusatzstroms wurde die [Ergänzung](ergaenzung.json) für die stromerhaltende Geburt und das gemeinsame skalare Fenster lokal festgehalten. Die Geometrie ist intrinsisch über die vollständige längere Kette definiert. Die Entwicklung war nicht öffentlich verblindet. Die Abschätzung für identisch auf null gesetzte Detektorreferenz, die engere Portgrenze des abgeschirmten Anschlusses und der interne Schnittest sind ergänzende Prüfungen.

Im entpackten Gesamtpaket genügt `python3 pruefen.py` für die exakten Prüfungen einschliesslich des Teilartikels. `python3 pruefen.py --quadratur` ergänzt die unabhängige Zentrumskontrolle mit mpmath 1.3.0. Der Gegenlauf integriert die ursprüngliche Staubwirkung an drei Sätzen äusserer Koordinaten und wiederholt bei 60 und 85 Dezimalstellen. Die vollständigen Paketgrenzen stammen aus dem analytischen Nachweis. [Unabhängige Gegenrechnung](AUDIT.md) · [Numerische Ergebnisse](gegenprobe.json) · [Lizenz](LICENSE)
