# Unabhängige Gegenprüfung: Geometriedynamik v0.1

13. November 2026. Interne KI-Gegenprüfung, kein externes Fachgutachten.

## Urteil

Der neue Kettenansatz beseitigt ein konkretes Quellenhindernis des alten Piloten und liefert überprüfbare stationäre Kandidaten. Im anschließenden N=11-Vergleich gelingt außerdem ein **quellenabhängiger stationärer Vergleich zweier geometrischer Wirkungsphasen bei identischen äußeren Randdaten**. Dieser stärkere, nachträglich gegengeprüfte Befund steht in Abschnitt 8. Die vorhandene Interferenzrechnung und diese neuen Kandidaten ergeben jedoch noch keine physikalische Geometriedynamik: Die bisherige Recordrechnung setzt eine Hilfspaarung voraus; der neue Wirkungsvergleich legt keine physikalische gemeinsame Gewichtung, Wahrscheinlichkeits- oder Evolutionsregel für die Geometriehistorien fest.

Der unabhängige Rechner `checks/independent_audit/check.py` reproduziert die unten genannten endlichen Identitäten ohne Import der anderen Agentenrechner. Er führt keine Amplitudenquadratur aus.

## 1. Die bisherigen Ausschlüsse bleiben eng

Für die sechs ursprünglichen Historien wird die transitive Ordnung separat aus den erzeugenden Kanten rekonstruiert. Die vier Klasse-1- und zwei Klasse-2-Historien ergeben erneut F4=9 beziehungsweise −7. Die Vorläufer von A1 und A2 bestehen jeweils nur aus P0. Damit gilt in allen sechs Fällen

\[
C_{A_i}=1+\frac\beta2(T_i-T_0)^2\geq1,\qquad \beta=4/\sqrt6.
\]

Dies verbietet frei variierte positive stationäre A-Dichten. Es verbietet weder festgehaltene Randquellen noch off-shell Quantenrandzustände. Die positive Dichtekomponente von `gplus` war deshalb kein mathematisch unzulässiges Hilfspaket; sie war nur keine gelöste stationäre Quelle.

Die Wirkung ist unter T↦−T gerade, der lineare gerichtete Strom ungerade. Bei den früheren geraden Uhrpaketen und ihrem symmetrischen Support verschwinden die entsprechenden linearen Amplitudeninsertionen. Daraus folgt weder ein physischer Erwartungswert Null noch ein Verbot gerader Stromkorrelationen. Eine gerichtete Randpräparation kann diesen Paritätsschluss aufheben; ihre physische Wahl und ihr Norm-/Maßvertrag bleiben gesonderte Angaben.

Der induzierte Endrand R ist in jeder Historie dieselbe Zweierantichain. Nur intrinsische Funktionen dieses isolierten Randordnungsobjekts sind daher konstant. Es gibt durchaus nichtkonstante kovariante Vollhistorienfunktionen. Die unabhängige Prüfung bestätigt die vom Geometrieagenten eingeführten Profile

\[
|D_k|=(1,3,4,5,6)\quad\hbox{bzw.}\quad(1,3,3,5,6),
\qquad D_k=\{x:|\operatorname{Past}(x)|\leq k\}.
\]

Sie sind Downsets: y≺x impliziert |Past(y)|<|Past(x)|. Der neue Wert |D2|=3+1_{Klasse1} enthält hier allerdings genau das alte Klassenlabel, keinen zusätzlichen geometrischen Freiheitsgrad. Ein gemessener Klassenmarker und eine ungemessene interferierende Historienalternative sind unterschiedliche Experimente. Eine Änderung dieses Kardinalitätsprofils ist ohne weitere Kalibrierung keine Radius-, Krümmungs- oder Eigenzeitkurve.

## 2. Positive Dichtesumme ist kein Constraint-Projektor

Das bisherige Dichtemaß ist

\[
d\nu(r)=\tfrac12\delta_0+\tfrac12 1_{(0,1)}dr.
\]

Für einen festen reellen Dichtekoeffizienten C liefert es exakt

\[
F(C)=\int e^{-irC/2}d\nu(r)
=\frac12+\frac{1-e^{-iC/2}}{iC},\qquad F(0)=1.
\]

Das ist eine glatte beschränkte charakteristische Funktion, keine δ(C)-Distribution. Sogar

\[
\Re F(C)=\frac{1+\operatorname{sinc}(C/2)}2
\geq\frac{1-1/\pi}{2}>0.
\]

Beweis der einfachen globalen Schranke: Für |u|≤π ist sin(u)/u≥0, für |u|≥π ist sin(u)/u≥−1/|u|≥−1/π. Das ursprüngliche Einzel-Dichteintegral projiziert somit keine off-shell Konfiguration durch C≠0 exakt heraus. Globale Interferenzauslöschung verschiedener Historien bleibt davon unberührt.

Die vom Zustandsraumagenten diskutierte Coarea-Paarung auf C=0 kann als neue mathematische Konstruktion positiv und lokal wohldefiniert sein. Sie folgt nicht aus dem Ersetzen des originalen F(C) durch δ(C). Eine solche Ersetzung ändert den Quantenvertrag. Auch eine volle reelle Gruppenmittelung wäre ein neues Maß und benötigt eine begründete Eichgenerator-Deutung; Linearität der Wirkung in r allein liefert diese nicht.

## 3. Uhrsymmetrie der Wirkung ist keine Symmetrie des gesamten Vertrags

Eine Differenzwirkung kann unter gemeinsamem T-Shift invariant sein. Das Produkt endlicher Uhrboxen ist dennoch nicht translationsinvariant. Bereits für ein einzelnes uniformes T∈[−1,1] gilt exakt

\[
\mathbb E[(T+a)^2]=\tfrac13+a^2\ne\tfrac13.
\]

Ein Argument, das den gemeinsamen Uhrshift als Eichvolumen entfernt, muss deshalb den Rand- und Supportvertrag verändern oder dessen Randterme mitführen. Die exakte punktweise Identität der Summe der Wirkungsableitungen ist davon zu unterscheiden; sie bleibt richtig. Der Quellenagent hat bestätigt, keine unzulässige globale Ward-Identität für das ursprüngliche Würfelmaß zu verwenden.

## 4. Neue Kettenquellen: unabhängige Bestätigung und Grenze

Der supporttreue Neunknoten-Kettenpunkt des Quellenagenten lautet

\[
T=(-1,-a,-\tfrac12,-\tfrac14,0,\tfrac14,\tfrac12,a,1),
\quad a^2=\frac{163}{256}-\frac{\sqrt6}{32}.
\]

Bei positiver konstanter Dichte, q=0, innerem Knoten4 und festem beidseitigem Vierknotenkragen bestätigt die unabhängige Symbolik C4=0 und ∂S/∂T4=0. Außerdem

\[
\partial_{T4}C4=\beta(16a-49/4)<-\beta/4<0,
\]

weil a<3/4. Dies ist ein nichtsingulärer lokaler **Staub-/Uhr**-Constraintzweig im ursprünglichen Uhrintervall. Die Ordungsfamilie und die Randpräparation sind neu. Es handelt sich nicht um dieselbe sechs-Historien-Amplitude.

Der vollständig innere Skalarblock dieses N=9-Kontrollfalls ist H44=0. Seine Skalarintegration kann daher nicht als nichtsinguläres eindimensionales Fresnelintegral behandelt werden. Eine Gesamtregularitätsbehauptung einschließlich q wäre hier falsch.

Ein gezielter nächster Kontrollfall ist N=10 mit zwei inneren Knoten4,5. Sein Skalarblock ist unabhängig bestätigt:

\[
H_{\phi,\mathrm{int}}=\begin{pmatrix}0&\beta/2\\\beta/2&0\end{pmatrix},
\qquad \det H_{\phi,\mathrm{int}}=-\beta^2/4=-2/3\ne0.
\]

Er kann mit der affinen stationären Familie des Quellenagenten verbunden werden; deren Uhrsupport ist explizit erweitert. Die allgemeine innere Staub-Hesseform mit A=∂C/∂T besitzt bei invertiblem A

\[
\det\begin{pmatrix}H&-A^T/2\\-A/2&0\end{pmatrix}
=(-1)^m\det(A)^2/4^m\ne0.
\]

Der Rechner überprüft die ersten beiden Größen symbolisch. Die allgemeine Identität folgt durch Vertauschen der beiden m-Spaltenblöcke zur Blockdreiecksform. Dies entfernt innere linearisierte Nullrichtungen am festgehaltenen Rand. Globale Symmetrien mit bewegtem Rand, die Wahl der Quantenpaarung und die Geometrievariation werden dadurch nicht entschieden.

Der Quellenagent hat anschließend einen stärkeren, nichtaffinen N=10-Zeugen innerhalb derselben Box [−1,1] angegeben. Die Gegenprüfung des Zertifikats bestätigt die Struktur: die symmetrischen Uhrwerte (−1,−a,−b,−1/4,−d,d,1/4,b,a,1) mit a=(25b+d+11/2)/24 lösen beide Uhrbilanzen identisch; eine isolierte quartische d-Wurzel und ein aus der Gröbner-Basis abgeleitetes b(d) lösen beide Dichtebedingungen. Die rationalen Intervallschranken für √6, entgegengesetzte Polynom-Endpunktzeichen und eine von null getrennte Ableitung zertifizieren die eindeutige Wurzel im genannten kleinen Intervall. Die Größenordnung d≈0,123211768878575, b≈0,48571982651345, a≈0,740258642988116 liegt strikt geordnet in der Box. Die negative, von null getrennte gemeinsame Diagonale von (∂C/∂T)/β und der oben unabhängig rekonstruierte Skalarblock sichern die volle lokale innere (T,r,q)-Hesse-Regularität. Dieser Zusatz wurde durch Prüfung der algebraischen und Intervallzertifikatslogik des Quellenagenten kontrolliert; der eigene Audit-Rechner beansprucht hierfür keine zweite vollständige Quartik-Isolation.

**Entscheidende Kontrolle:** F4(C) ist für festes C eine Konstante bezüglich T,r,q. Alle diese Materie-Stationaritätsgleichungen und Hesseformen sind deshalb auch nach Entfernung des reinen Gravitationsphasenfaktors dieselben. Die stationären Quellen sind ein Fortschritt; sie allein demonstrieren keine gravitative Rückwirkung oder Dynamik der Kausalordnung. Eine finite totale Ordnung ist außerdem noch keine nachgewiesene vierdimensionale Verfeinerungsfamilie.

## 5. Die bisherigen Records identifizieren keine Geometriedynamik

Eine allgemeine, vom CST-Modell getrennte Identifizierbarkeitskontrolle zeigt die Lücke exakt. Für beliebige Krausoperatoren Mj und ein ungemessenes geometrisches Zusatzsystem G liefern Mj⊗UG dieselben Recordwahrscheinlichkeiten für jedes unitäre UG. Die Spur über G entfernt UG. Eine geometrische Observable auf G kann gleichzeitig beliebig andere Verläufe haben.

Der Rechner benutzt M0=diag(1/2,1/3), MF=diag(√3/2,2√2/3), Eingang (1,1)/√2 und geometrischen Anfangszustand (1,0). Für UG=I und UG=exp(−iπσx/4) sind die Recordwahrscheinlichkeiten identisch (13/72,59/72), während der Erwartungswert von VG=diag(0,1) gleich0 beziehungsweise1/2 ist. Dies ist **kein** Gegenbeispiel innerhalb derselben CST-Wirkung. Es beweist nur, dass die bisherigen instrumentellen Daten allein die fehlende dynamische Ergänzung nicht bestimmen. Die gemeinsame Wirkung und deren physikalische Paarung müssen diese Zusatzfreiheit einschränken.

## 6. Gegenprüfung der anderen Teilansätze

- **Zustandsraum:** Ein kompakter Operator auf einem unendlichdimensionalen Hilbertraum wird durch beschränkt invertible äquivalente Normänderung nicht unitär. Ein Hilbert-Schmidt-Argument benötigt hier ausdrücklich einen kompakten Uhr-/Dichtepatch und feste skalare Projektionen oder geeignete gewichtete Räume. Es erfasst nicht pauschal den unbeschränkten distributionellen Skalar-Fresnelkern, eine unbeschränkte neue Metrik oder einen echt anders reduzierten physikalischen Sektor. Diese Einschränkung wurde dem Agenten mitgeteilt.
- **Geometrie:** Die neuen Past-Kardinalitätsprofile sind unabhängig bestätigt. Nichtverschwindende Interferenz der akzeptierten Klassenäste verhindert eine klassische Additivitätsdeutung genau dieser ungemessenen Alternativen. Ohne klassenweise Erweiterung des Failure-Kanals ist dies kein Satz über ein bereits konstruiertes vollständiges physisches Dekohärenzfunktional.
- **Verklebung:** Die vom Verklebungsagenten angekündigte nichtfaktorisierende Kreuzphase ist konsistent mit dem ursprünglichen Bedarf an Schnitt-Memory. Das Hauptziel muss ein begründeter gemeinsamer bedingter Amplituden-/Maßvertrag bleiben. Externzeitliche Schrödinger-Unitarität ist nicht die einzig zulässige Form einer kovarianten Physik.

## 7. Wann die fehlende Aufgabe geschlossen wäre

Drei zusammenhängende Aussagen genügen als Arbeitsdefinition, ohne eine neue Liste willkürlicher Prüfgates:

1. Ein gemeinsamer Wirkungs-, Maß- und Randvertrag definiert zulässige Quellen sowie eine positive physikalische Paarung oder eine entsprechend begründete kovariante Historiendeutung; seine Schnittzusammensetzung ist konsistent.
2. Derselbe Vertrag definiert ein nichttriviales kovariantes geometrisches Ereignis oder eine relationale Geometrieobservable samt physisch begründeter Uhr-/Skalendeutung. Ein Klassenindex oder Skalarmodus wird nicht lediglich umbenannt.
3. Eine Quellenänderung erzeugt darin einen geometrischen Effekt, dessen Ursache sich gegen festgehaltene Randselektion, Maßänderung und bloßen Materieeffekt abgrenzen lässt. Ein klassischer Gravitations-/Staubanspruch benötigt anschließend den entsprechenden Korrespondenzbereich. Aussagen über Kollaps oder Singularitätsauflösung benötigen zusätzlich ihren bereits vereinbarten globalen Rand und Verfeinerungsbereich.

Eine echte Lösung kann in einer histories-/Dekohärenzfunktional-Form vorliegen; ein künstlich eingeführtes H und U(t) sind nicht nötig. Die jetzt konstruierten Quellen, der stationäre geometrische Phasenvergleich und die kompakten Memorydaten sind sinnvolle Bauteile dafür. Der physikalische gemeinsame Vertrag ist noch nicht konstruiert.

## 8. Stärkerer N=11-Befund: zwei stationäre Geometrien mit gemeinsamem Rand

Der Root-/Ordnungsvariationsansatz wurde nach der ersten Gegenprüfung mit einem zweiten unabhängig geschriebenen Rechner `checks/independent_audit/check_n11.py` überprüft. Dieser baut die Ordnungen, offenen Intervalle und sämtliche b-Koeffizienten von Grund auf neu auf.

Der äußere Kragen ist B={0,1,2,3,7,8,9,10}, der innere Bereich I={4,5,6}. Die erste Historie ist die totale Kette. Die zweite entfernt ausschließlich die Vergleichsrelationen 4≺5 und 5≺6, behält jedoch 4≺6. Sie bleibt transitiv; die induzierte äußere Ordnung und alle I/B-Vergleichsrelationen bleiben identisch. Trotzdem verändern sich mehrere Intervallkardinalitäten und damit die volle Wirkung. Eine Auswertung nur der beiden entfernten Kanten wäre falsch.

Setze Tj=Δ(uj−5), Δ²=2/(19β). Auf B sind uj=j, rj=ρ und qj=0 für beide Historien gleich. Stationäre innere Daten sind

| Historie | u4,u5,u6 | r4,r5,r6 | F4 | vollständige stationäre Wirkung bei q=0 |
|---|---|---|---|---|
| Kette | (4,5,6) | (ρ,ρ,ρ) | 10 | 10−151ρ/38 |
| Zwei entfernte Vergleiche | (4,4,5) | (2ρ,ρ,ρ) | 18 | 18−105ρ/38 |

Für 0<ρ<1/2 liegen alle Dichten im positiven Originalintervall. Der Rechner bestätigt in beiden Fällen exakt C4=C5=C6=0 und sämtliche drei inneren Uhr-Euler-Lagrange-Gleichungen. Die Randdichten und Randuhren werden nicht mitvariiert. Die beiden inneren Dichte-Constraint-Jacobimatrizen in u-Koordinaten haben dieselbe nichtverschwindende Determinante −8/6859. Somit sind die entsprechenden lokalen Staub-/Uhr-Hesseformen regulär.

Die vollständige Wirkungsdifferenz lautet

\[
\Delta S(\rho)=8+\frac{23}{19}\rho,
\qquad \partial_\rho\Delta S=\frac{23}{19}\ne0.
\]

Dies schließt die bloße Fest-C-Kontrolle aus Abschnitt 4 konstruktiv weiter auf: Nun werden tatsächlich zwei Ordnungen unter demselben äußeren Quellenvertrag verglichen. Die Quelle verändert den relativen stationären Wirkungswert. Der reine F4-Anteil ist8; die Quellenabhängigkeit stammt hier aus der auf den jeweils stationären Innenzweigen ausgewerteten Staubwirkung. Es ist keine Variation eines kalibrierten Newton-Parameters und kein aus einem einzelnen endlichen Ordnungswechsel abgeleitetes Einstein-Gesetz.

Der Skalarblock der Kette, skaliert als Q=2Hφ/β, ist

\[
Q_{II}=\begin{pmatrix}0&1&-9\\1&0&1\\-9&1&0\end{pmatrix},\quad\det Q_{II}=-18.
\]

Bei der zweiten Ordnung ist er

\[
Q_{II}=\begin{pmatrix}0&0&1\\0&0&0\\1&0&0\end{pmatrix},
\]

mit Nullrichtung e5. Entscheidend ist jedoch: In **beiden** Historien haben die vollständigen inneren Spalten H[:,I] Rang3. Die zweite Nullrichtung koppelt an den äußeren Skalarbereich. Für positive Gaußdämpfung auf allen acht Randfeldern und gemeinsame Abeldämpfung ε>0 auf den Innenfeldern existiert daher ein nichtsingulärer ε→0+-Gaußpaarungsgrenzwert. Begründung: (PB−iH)z=0 erzwingt durch den Realteil z†PBz=0, also zB=0; danach H[:,I]zI=0 und wegen Rang3 zI=0. Die Phase ist durch den gemeinsamen Abelpfad festzuhalten. Dies behauptet keine absolute Konvergenz des undämpften inneren Skalarintegrals und keine bereits integrierte Uhr-/Dichteamplitude.

**Vertragsänderung:** Nach Zentrierung benötigt der affine N=11-Fall einen Uhrhalbbreite 5Δ>1. Die ursprüngliche Box [−1,1] wird somit erweitert; außerdem sind die Historiensumme und Randpräparation neu. Dieser Punkt darf nicht als Ergebnis innerhalb des unveränderten sechs-Historien-Vertrags dargestellt werden.

**Abschließendes Audit dieses stärkeren Befunds:** Der präzise Ausdruck „stationärer quellenabhängiger geometrischer Wirkungsvergleich“ ist gedeckt. Die Ausdrücke „physikalische Übergangswahrscheinlichkeit“, „gelöste gravitative Geometriedynamik“, „Einstein-Gleichung“ oder „Kollapskurve“ sind weiterhin nicht gedeckt. Die notwendige gemeinsame physikalische Paarung, Gewichtung und Dynamikdeutung darf nicht allein aus der endlich berechneten relativen Phase ergänzt werden.

## Primärliteratur und ihre begrenzte Rolle

- Brightwell, Dowker, Garcia, Henson, Sorkin, *“Observables” in causal set cosmology*, Phys. Rev. D67 (2003)084031, [arXiv:gr-qc/0210061](https://arxiv.org/abs/gr-qc/0210061). Unterscheidet labelunabhängige Ereignisse und ihren Maßkontext; die bewiesene Stem-Satz-Reichweite betrifft die dortige klassische Wachstumsfamilie, nicht automatisch unseren endlichen quantenmechanischen Piloten.
- Dowker, Johnston, Surya, *On extending the Quantum Measure*, J. Phys. A43 (2010)505305, [arXiv:1007.2725](https://arxiv.org/abs/1007.2725). Stark positive Dekohärenzfunktionale können als Vektormaße beschrieben werden; Erweiterung auf größere Ereignisalgebren ist eine zusätzliche Frage und folgt nicht aus endlichen Daten allein.
- Oeckl, *General boundary quantum field theory: Foundations and probability interpretation*, Adv. Theor. Math. Phys.12 (2008)319–352, [arXiv:hep-th/0509122](https://arxiv.org/abs/hep-th/0509122). Verallgemeinert Raumzeit-Randamplituden und ihre Wahrscheinlichkeitsinterpretation. Dient als methodischer Hinweis, dass fehlende Standard-Zeitunitarität kein allgemeines No-go ist; validiert keinen der vorliegenden CST-Kandidaten.

Diese Literatur begründet Begriffsunterscheidungen. Die neuen algebraischen Identitäten stammen aus den expliziten lokalen Rechnungen, nicht aus einer Behauptung, die Literatur habe die offene CST-DUST-Dynamik bereits gelöst.
