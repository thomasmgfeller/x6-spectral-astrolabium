# Skalarausgang im markierten N15-Rahmen

Die beiden Strompakete behalten ihre gemeinsame skalare Eingangspräparation
$\exp(-\beta x^T x/2)$ mit $x\in\mathbb R^3$ und $\beta=4/\sqrt6$.
Für das neue maximale Ereignis führen wir eine weitere markierte
Skalar-Randkoordinate $u=q_n$ ein. Wir benutzen bei allen drei Anschlüssen
und beiden Paketen **dasselbe Fenster** $-1\le u\le1$, mit dem normierten
flachen Mass $du/2$ in den bestehenden dimensionslosen Skalarkoordinaten.
Es ist eine zusätzliche Auslesebedingung. Die zwei Arme des Dichtedetektors
werden beim selben $u$ und denselben alten Ausgangskoordinaten $y$ verglichen.
Über $u$ wird erst bei der Randpaarung integriert. Der Staubdetektor wirkt
als Identität auf diesen Skalarfaktor.

Der Prüfer rekonstruiert alle Intervallgewichte und die ganze reelle
Skalarmatrix. Für $n=15$ entspricht sein Rahmen einschließlich der beiden
Randphasenterme dem archivierten [Skalartransport](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d7de6876f571ece2dca8030f30d8fdda839b8404/research/rax_cqg/dust_collapse/joint_charge_distribution_v0_1/model.py).
Für $n=16$ ergänzt er die unabhängige Koordinate $q_n$. Insbesondere bleiben
die Paare mit dem früher verborgenen $q_6$ im ungeschirmten Anschluss in
der **gemeinsamen** Wirkung $-\beta\sum b_{ij}(q_i-q_j)^2/4$ erhalten.
Die skalare Ausgangsfunktion kann sich beim Wechsel des Ideals ändern.

Sei $H$ der innere Block für die sieben alten inneren Felder und die zwei
alten Rahmenvariablen. Für jede der vier Ordnungen ist er invertierbar.
Seine Elimination ergibt die reelle Schurmatrix $K$ auf $(x,y,u)$, bzw.
$(x,y)$ auf N15. Setze $A=K_{xx}$, $B=K_{xy}$ und $c=K_{xu}$.

| Ordnung / Vorgänger von $n$ | $\det H$ | $\det B$ |
| --- | ---: | ---: |
| N15 unverändert | −6291456000 | 134314687/2000 |
| $P\cup\{6\}$ | −10913841152 | 2013668124/41633 |
| ganze alte Ordnung | −9890488320 | 19856077422/402445 |
| $P\cup\{6,11,12,13\}$ | −61228711936 | 4534858848/233569 |

Bei positivem Abel-Regulator $\exp(-\epsilon\|z\|^2/2)$ für alle neun
verdeckten Skalarvariablen $z$ sind die Integrale über $(x,z)$ für
jedes feste $(y,u)$ absolut integrierbar. Dies gilt gemeinsam mit den
endlichen Staubboxen. Fubini erlaubt die Vertauschung beim regulierten
Integral. Im Grenzwert liefert der invertierbare Block $H$ das
gewöhnliche nichtverschwindende Fresnel-Integral. Beim nachfolgenden
Gaußintegral über $x$ ist die Matrix $I-iA$ invertierbar. Das ergibt
für die Ausgangsamplitude, mit einer vom Rand unabhängigen Konstanten
$C_J>0$,

$$
 |\psi_J(y,u)|^2=C_J\exp[-\beta(By+cu)^T(I+A^2)^{-1}(By+cu)].
$$

Auf N15 entfällt der Term $cu$. Weil $B$ invertierbar und
$I+A^2$ positiv definit ist, hat die reelle Ausgangspräzision
$\beta B^T(I+A^2)^{-1}B$ drei positive Hauptminoren. Der Prüfer gibt
deren exakte Werte nach Division der Matrix durch $\beta$ an.
Die Verschiebung $y\mapsto y+B^{-1}cu$ zeigt, dass die
$L^2(d^3y)$-Norm endlich, strikt positiv und unabhängig von $u$ ist.
Das normierte endliche Fenster erhält diesen Wert. Die Integration über
die ganze reelle $u$-Achse mit Lebesgue-Mass ergäbe eine unendliche Norm.
In jeder **bedingten** normierten Staubwahrscheinlichkeit kürzt sich
der gemeinsame Skalarfaktor exakt. Eine Gewichtung verschiedener
Wachstumsideale untereinander wird hier nicht festgelegt.

Die Verschiebung von $y$ in einer Integration beweist keine Eichsymmetrie.
Eine Verschiebung allein von $q_n$ bei festgehaltenen alten Feldern verändert
die neuen Paarterme. Eine gemeinsame Translation aller Skalarfelder lässt
die nackten Differenzterme invariant. Für eine Aussage auf einem
physikalischen Quotienten müsste zusätzlich die Verträglichkeit der
Präparation, des Rahmens, des Fensterankers und des Instruments mit seiner
Identifikation gezeigt werden. Diese Rechnung definiert die Auslese im
markierten Rahmen. Die physikalische Randpaarung bleibt offen.

Die Prüfung benötigt Python 3 und die Standardbibliothek.

```sh
python3 -B skalar.py | cmp - skalar.json
```
