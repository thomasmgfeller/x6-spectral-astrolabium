# Wird das Vorzeichen des Anfangsstroms mit dem Staub bis zum Zukunftsrand transportiert?

**CST-DUST · N15-Typ 375841 · 21. November 2026**

Der Quellzeiger aus PR #340 speichert eine frühere Ladung. Der Strom der ursprünglichen Wirkung hat auf denselben Feinhistorien einen anderen Verlauf. Am Zwischenschnitt $Y=0$ ist er in beiden Originalpaketen negativ. Unmittelbar vor dem Zukunftskragen ist er in beiden positiv und auf gepaarten Historien exakt gleich. Eine zusätzliche Gegenkonstruktion zeigt, warum lokale Daten am Zwischenschnitt für eine allgemeine Auslese des Anfangsvorzeichens nicht ausreichen. [Quellzeigerversuch auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/340)

## 1. Den Strom an drei Stellen der gleichen Historie auslesen

Für ein nach unten abgeschlossenes Gebiet $A$ verschieben wir alle seine Uhren gemeinsam um $\tau$. Bei der Ableitung bleiben die übrigen Felder, das Gebiet und die Präparation fest. In der Orientierung von PR #340 ist die Ladung

$$
p_A=-\partial_\tau S(T+\tau\,1_A)|_0
=\frac{1}{19\Delta}\sum_{i\in A,\,j\notin A}w_j b_{ij}(Y_i-Y_j),
\qquad Y=T/\Delta,\quad \Delta^4=3/722.
$$

Sie ist das Negative des in der früheren Kantenstrom-Tabelle als $Q(A)$ bezeichneten Flusses. Bei festem Ordnungstyp hängen Skalar- und Gravitationsteil der Wirkung von dieser Uhrverschiebung nicht ab. Die Dichte sitzt jeweils am späteren Ereignis. [Projektdefinition des Wirkungsstroms](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/46b2aa4d82d44dafe02930778ec07ba6db19558d/research/rax_cqg/dust_collapse/material_current_surface_v0_1/README.md)

| Gebiet $A$ | Ladung im eingangs positiven Paket | Ladung im eingangs negativen Paket | Gepaarte Differenz am Zentrum |
|---|---:|---:|---:|
| Anfangskragen | [0,0018750; 0,0018870] | [−0,0013278; −0,0013158] | $1217081/380000000$ |
| Bis $Y=0$, maximal sind die Ereignisse 5 und 11 | [−0,0326901; −0,0325594] | [−0,0328402; −0,0327094] | $456161/3040000000$ |
| Bis unmittelbar vor dem Zukunftskragen | [0,0478122; 0,0480643] | [0,0478122; 0,0480643] | exakt 0 auf den ganzen Paketen |

Die Intervalle sind nach aussen gerundet und schliessen die vollständigen Uhr- und Dichtezellen sowie die Zukunftsbox ein. Am Ausgang gilt die Gleichheit punktweise, weil nur Zukunftsdichten als Empfänger in die Summe eingehen. Alle Uhren und alle Zukunftsdichten sind im gepaarten Vergleich gleich. Die unterschiedlichen inneren Dichten können nur Wirkungsterme mit einem inneren Ziel verändern. Deren Koeffizienten sind unabhängig von allen späteren Feldern. Somit stimmen auch die Antworten auf beliebige gemeinsame Änderungen der Zukunftsuhren und -dichten im festgelegten Quellenvertrag überein.

Die inneren Ketten haben Längen drei und vier. Ihre Präfixe liefern genau $4\cdot5=20$ Ideale zwischen den Kragen. Für die Differenz $p_A(h_+)-p_A(h_-)$ ergeben sich über die ganzen gepaarten Zellen zehn strikt positive, acht strikt negative und zwei identisch verschwindende Fälle. Diese Anzahlen betreffen die **Differenz**. Nur ein Teil dieser Ideale ist durch einen für beide Ketten gemeinsamen Uhrwert realisierbar. [Alle 20 exakten Einschlüsse](schnitte.json)

Wird der zusätzliche Zeiger von PR #340 jeweils neu an den *dortigen* Strom gekoppelt, ergeben sich in der Hilfspaarung folgende bedingte Wahrscheinlichkeiten für denselben Ausgang $Y_{\mathrm{Zeiger}}=+1$.

| Platzierung der Quelle | Eingangs positives Paket | Eingangs negatives Paket |
|---|---:|---:|
| Anfang | 50,094051 % | 49,933909 % |
| Zwischenschnitt | 48,369053 % | 48,361554 % |
| Ausgang | 52,395994 % | 52,395994 % |

Die Zahlen sind Quadraturwerte. Der Kontrast null in der letzten Zeile ist zusätzlich analytisch bewiesen. Die Spalten unterscheiden Pakete in ein und derselben Präparation. Jede Zeile ist ein eigener Quellenversuch. Der am Anfang gekoppelte Zeiger aus PR #340 kann den früheren Unterschied bei seiner Weitergabe behalten. [Vollständige Rechnung auf drei Stufen und zwei Verwürfelungen](ward.json)

## 2. Wie weit trägt die vorhandene Dichte am Zwischenschnitt?

Für das ursprüngliche Paar ist das Ereignis 5 durch seine Ordnungsrolle ausgezeichnet. Es ist das zweite Ereignis der kürzeren inneren Kette. Auf der Antikette $\{5,11\}$ trennt schon die Schwelle $w_5/\Delta=17/160$ die Pakete. Sie ist die Dichte im unverschobenen Zentrum. Im positiven Paket liegt $w_5/\Delta$ zwischen 0,1059650 und 0,1059655, im negativen zwischen 0,1065345 und 0,1065350. Auf elf der zwanzig linken Idealränder liegt mindestens eine trennende Dichte. Auf den übrigen neun stimmen die lokalen Feldwerte des Originalpaars unter der Paarzuordnung überein. Der linke Idealrand vor dem Zukunftskragen enthält noch Ereignis 13. Die empfangenden Ereignisse des Zukunftskragens liegen *jenseits* dieses Randes.

**Ein zweites Paar widerlegt die Verallgemeinerung.** Dieser zusätzliche Versuch entstand nach der ersten Schnittrechnung. Die Paketbreiten, Uhren, gemeinsame Präparation und Skalierung der Dichteverschiebung wurden beibehalten. Für das Gegenpaar werden im Inneren die Dichten an $4,12,13$ verschoben. Auf diesen drei Achsen benutzen wir mit demselben $k=7600/8000000$ wie im ursprünglichen Beweis

$$
d=k(C_{12}-C_{13},\,C_{13}-C_4,\,C_4-C_{12}),\qquad
C_v=1+\tfrac1{19}\sum_{i\prec v} b_{iv}(Y_i-Y_v)^2.
$$

Für alle Uhrwerte gelten $\sum d_v=0$ und $\sum C_v d_v=0$. Die Verschiebung zwischen $f-d+\xi$ und $f+d+\xi$ erhält Gesamtdichte, Wirkung und Integrationsmass. Bei festen Uhren ist sie eine Translation der inneren Dichten. Beide offenen Zellen liegen vollständig in den ursprünglichen 1-%-Bändern. Am Zentrum sind die Anfangsladungen $1754179/1520000000$ und $-904179/1520000000$. Auf den ganzen Zellen sind sie grösser als $0{,}001148$ bzw. kleiner als $-0{,}000588$.

Beide Schnittuhren, beide Schnittdichten und die identisch gepaarten Skalarfelder stimmen beim Gegenpaar überein. Auch die Zukunftsbelegungen stimmen überein. Für jede gemeinsame beschränkte Testfunktion dieser Koordinaten sind daher die kohärenten Amplituden gleich. **Kein Detektor allein aus den Feldkoordinaten dieser Antikette und des gewählten Zukunftsrands kann das Anfangsvorzeichen auf dem vollständigen Präparationsbereich zuverlässig bestimmen.** Eine Schnittladung wie $p_A$ benutzt über den Schnitt reichende Beziehungen und weitere Feldwerte. Sie fällt ausserhalb dieses Ausschlusses. [Zertifizierte Pakete](schnittkoordinaten.json) · [Unabhängige direkte Wirkungsprüfung](gegenprobe.json)

## 3. Warum sich der Fluss ändern kann

Setze $E_v=\partial S/\partial T_v$. Für zwei verschachtelte Ideale gilt die Variationsidentität

$$
p_A-p_B=\sum_{v\in B\setminus A}E_v .
$$

Der Prüfer kontrolliert die Koeffizienten aller geordneten Paare für alle 130 strikt verschachtelten Idealpaare. Für Anfang und Ausgang ist die rechte Seite auf dem ursprünglichen positiven Paket in $[-0{,}046190,-0{,}045925]$, auf dem negativen in $[-0{,}049393,-0{,}049128]$. Damit enthält keines der zwei Pakete ein Feld, das alle sieben inneren klassischen Uhrgleichungen gleichzeitig erfüllt. Die endliche Quantensumme umfasst auch solche nichtstationären Historien. [Frühere Constraint-Prüfung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/46b2aa4d82d44dafe02930778ec07ba6db19558d/research/rax_cqg/dust_collapse/quantum_structure_v0_1/PUBLICATION.md)

Für den kohärenten Versuch wurde der Term auf dem Rand der festen Präparation eigens mitgerechnet. Bei festen äusseren Daten sei $V=\sum_{v\in I}\partial_{T_v}$. Bei flachem innerem Feldmass gilt auf jeder Zelle durch partielle Integration $\int E_I e^{iS_d}d\mu=(1/i)\int_{\partial P}e^{iS_d}V\cdot n\,d\sigma$ mit $E_I=V S_d$ und dem entsprechend induzierten Randmass. Unter der Verschiebung aller inneren Uhren gilt $V u_v=1/D_T$, $D_T=\Delta(4-e)$. In den Koordinaten $x=f\mp d+\xi$ unterscheiden sich die Geschwindigkeiten der Dichtefenster um $V\xi_+-V\xi_-=2Vd$. Die Uhrflächenbeiträge heben sich beim gepaarten Abzug auf. Es bleiben die Flächen der drei verschobenen Dichtekoordinaten. Einschliesslich der gemeinsamen Phasenfaktoren im Staubintegral gilt punktweise für deren kombinierten Einsatz

$$
2\sum_v(Vd_v)\partial_{\xi_v}S_d
=-M D_T\sum_v C_v Vd_v
=M D_T\sum_v d_v VC_v
=p_{\rm Anfang,+}-p_{\rm Anfang,-}.
$$

Die mittlere Gleichheit folgt durch Ableitung von $C\cdot d=0$. Die gepaarte Volumeneinfügung hat für jeden zugelassenen Zukunftswert nach Ausklammern der gemeinsamen skalaren und gravitativen Faktoren einen Realteil **grösser als $1/400$ je Paketmass**. Dazu genügen die strikten Schranken $p_{\rm Anfang,+}-p_{\rm Anfang,-}>1/320$ und $\operatorname{Re}e^{iS_d}>4/5$. Der Term verschwindet somit auch nach der Integration nicht.

Die separate numerische Flächenrechnung integriert die oberen und unteren Dichteflächen mit ihren entgegengesetzten Normalen. Die Volumenrechnung differenziert die Ausgangswirkung. Auf der feinsten Stufe der zweiten Verwürfelung mit 1 024 inneren und 32 äusseren Punkten ergibt sich auf beiden Wegen $0{,}002787293157-0{,}001564132468\,i$ in der gemeinsamen Referenzvolumennormierung. Der absolute Unterschied liegt dort unter $2\cdot10^{-17}$. Ein Weglassen der beweglichen Dichtefenster würde den nichtverschwindenden Beitrag verlieren. Diese endliche Ward-Identität bestimmt keine neue physikalische Paarung.

## 4. Welche Zeigernorm folgt aus den Annahmen?

Für eine gemeinsame konstante positive Zeigermetrik $G$ und $U(p)=\mathrm{diag}(1,e^{ip})$ fordert Isometrie $U^\dagger G U=G$. Schon für ein $p$ mit $e^{ip}\ne1$ folgt $G_{01}=0$. Alle $\mathrm{diag}(a,d)$ mit $a,d>0$ erfüllen diese Bedingung. Fordert man zusätzlich, dass genau die projektive Pauli-$Y$-Auslese aus PR #340 selbstadjungiert ist, gilt $GY=YG$ und damit $a=d$. Erst **beide** Instrumentannahmen bestimmen die Zeigermetrik bis auf einen gemeinsamen Faktor. Dass die gekoppelte Staubdynamik dieses Instrument realisiert, bleibt offen. Die Zeigerarme sind Referenz und Quelle. Ihre Normen begründen weder physikalische Stromsektoren noch eine Ruhemasse. [Beispiele und Status](zeigerprodukt.json)

## Nachrechnung und Geltungsbereich

`strom.py`, `schnittkoordinaten.py`, `gegenprobe.py` und `zeigerprodukt.py` benötigen die Python-Standardbibliothek. `ward.py` verwendet NumPy und SciPy. Die 33 rationalen Feldpunkte der Gegenprobe prüfen das zusätzliche Paar mit direkter Wirkungsdifferenz. Die Aussagen über ganze Pakete folgen aus den Koeffizientenidentitäten, positiven Volumina und rationalen Intervallschranken.

```sh
sha256sum -c SHA256SUMS
python3 -B strom.py
python3 -B schnittkoordinaten.py
python3 -B gegenprobe.py
python3 -B zeigerprodukt.py
OPENBLAS_NUM_THREADS=1 python3 -B ward.py
```

[Prüfvertrag](pruefvertrag.json) und [Hash](pruefvertrag.sha256) wurden lokal vor der Hauptrechnung fixiert. Die zusätzliche Schnittdichteprüfung und das Gegenpaar sind nachträgliche konstruktive Kontrollen. Die Werte des früheren Zeigertests waren bekannt. Die aus PR #340 übernommenen Funktionen liegen in drei unveränderten Quelldateien. Die neuen Prüfprogramme verwenden sie für Paketgeometrie, Phasengrenzen und Quadratur. [Quellstand](quellen.json) · [Lizenz](LICENSE) · [NOTICE](NOTICE)

Der Ausschluss betrifft die genannten Koordinaten auf diesem Typ und unter der geprüften Präparation. Das Prüfpaket entscheidet über diese endliche Auslese. Ob dynamische Constraints eine physische Randpaarung und ein Gedächtnis für die frühere Ladung zulassen, bleibt `HOLD`. Für P3 wurden keine physischen Radiuswerte berechnet.

