# Geometrie aus der vorhandenen Historienfamilie

Stand 13. November 2026. Ausgangspunkt: PR 290 / `f5ee44d7cb4dc1f924eee580f1eaf0cfcb4a5bc6`; unveränderte ursprüngliche sechs Historien, Rollen P={0}, A={1,2}, I={3}, R={4,5}, ursprüngliche Wirkungen und Randpakete. Dies ist ein neuer analytischer Geometrieaudit, keine neue große Integration und keine physikalische Kalibrierung.

**Ergebnis:** Innerhalb der bestehenden Familie lassen sich zwei intrinsische geometrische Verlaufssignaturen exakt definieren und unterscheiden. Die Familie liefert jedoch nur einen binären invarianten Geometriefreiheitsgrad. Dieser ist identisch mit der bisherigen Ordnungsklasse. Die aktuell kohärente Auslese liefert für diese beiden ungemessenen Alternativen keine additive Wahrscheinlichkeitsverteilung. Eine räumliche Volumen-, Radius- oder Eigenzeitdynamik ist damit noch nicht hergeleitet.

## 1. Ein intrinsischer Verlauf ohne Einbettung

Für eine endliche Kausalordnung C definiere

\[
n_C(x)=|\operatorname{Past}_C(x)|,\qquad
D_k(C)=\{x\in C:n_C(x)\leq k\},\qquad
N_k(C)=|D_k(C)|.
\]

Diese Definition benötigt weder eine gewählte Nummerierung noch zusätzliche Uhrdaten. Ist y≺x, so gilt Past(y)∪{y}⊆Past(x), also n_C(y)<n_C(x). Daher sind alle D_k vergangenheitsabgeschlossen, und jede Schicht D_k\D_(k−1) ist eine Antikette. Der Index k ist ein intrinsischer Kardinalitätsrang. Er ist keine kalibrierte Eigenzeit. Die Folge ist eine kanonisch aus jeder vollständigen Ordnung extrahierte Filtration, kein unabhängig hergeleitetes Wachstumsgesetz.

Alle sechs gelabelten Historien wurden direkt aus dem eingefrorenen Vertrag rekonstruiert. Der Audit erzeugt die transitiven Abschlüsse und sämtliche Bilder unter S2(A)×S2(R). Er benutzt die alten Geometrietabellen nicht als Sollwerte.

| Invariante | Klasse 1, vier gelabelte Historien | Klasse 2, zwei gelabelte Historien |
| --- | --- | --- |
| N_k, k=0,…,4 | (1,3,4,5,6) | (1,3,3,5,6) |
| Größen der n_C-Schichten | (1,2,1,1,1) | (1,2,0,2,1) |
| Schichten nach längster Kette ab P | (1,2,2,1) | (1,2,2,1) |
| Anzahl Relationen | 11 | 12 |
| Intervallhistogramm, 0,…,3 innere Elemente | (7,2,1,1) | (7,2,2,1) |
| F4 | 9 | −7 |
| Maximalgröße einer Antikette | 2 | 2 |
| Zahl maximaler Antiketten | 5 | 4 |
| |Past(3)∩A| | 1 | 2 |
| Sortierte Pastgrößen der R-Elemente | (3,4) | (3,4) |
| Sortierte längste P→R-Ketten, in Links | (2,3) | (2,3) |

Dies beantwortet die konkrete Frage nach zwei geometrisch verschiedenen Schnittfolgen mit **ja**, sofern mit Schnittfolge diese intrinsische Downset-Filtration gemeint ist. Keine der gezählten Größen wird deshalb bereits als räumliches Dreivolumen bezeichnet. Ein endliches Ereignisvolumen und eine räumliche Momentaufnahme sind verschieden; insbesondere ist N_k die kumulierte Zahl von Ereignissen in einem Downset.

## 2. Wie viel Geometrie kann die Familie überhaupt tragen?

Die sechs Historien bilden genau zwei rollenverträgliche Isomorphieklassen. Sie sind auch als unmarkierte Posets nicht isomorph, da die Relationenanzahlen verschieden sind. Jede reine, relabelinvariante Ordnungsfunktion auf dieser Familie hat daher die Form

\[
G(C)=G_1\Pi_1(C)+G_2\Pi_2(C).
\]

Die Algebra ist zweidimensional. Für den neuen Verlauf gilt insbesondere

\[
N_2(C)=3+\Pi_1(C),\qquad
|\operatorname{Past}(3)\cap A|=2-\Pi_1(C).
\]

Die neue geometrische Interpretation schafft keinen unabhängigen zusätzlichen Freiheitsgrad. Sie präzisiert, welcher intrinsische Ordnungsunterschied schon hinter dem früheren Klassenlabel lag. Diese Auswahl erfolgt nach Kenntnis der beiden Klassen und ist explorativ, keine neue blinde Vorhersage.

Der induzierte Endrand R und sogar der induzierte Rand P∪A∪R stimmen in allen sechs Historien exakt überein. Die auf diese Familie eingeschränkte Algebra reiner intrinsischer R-Ordnungsfunktionen besteht deshalb nur aus Konstanten. Diese Aussage betrifft keine Materiefelder und verbietet keine vollständigen Historien- oder Randgedächtnisobservablen. Sie zeigt nur, weshalb f0/f2 keine intrinsische R-Geometrie rekonstruieren.

Eine Messung von N_2 als scharfem Ordnungsrecord würde genau die Ordnungsklasse messen. Das ursprüngliche markierte Hilfsinstrument weist diesem Record additive Wahrscheinlichkeiten zu; unter dessen eigenen Annahmen gilt E[N_2|Erfolg,g]=3+P(Klasse 1|Erfolg,g). Das wäre numerisch exakt der frühere Klassenkontrast und weiterhin phasenblind. Es wäre keine neue Messung gravitativer Rückwirkung.

## 3. Gemessene Geometrie und ungemessene Interferenz sind verschiedene Versuche

Sei K_c der auf Klasse c eingeschränkte akzeptierte Zweimodenoperator in den Ausgangsraum mit Labels (f0/f2)×(Atom/Positiv). Für die beiden bestehenden Eingänge liefert die kohärente Auslese K=K_1+K_2. Als rein endliche Diagnose definiere

\[
D_{12}^{\rm acc}(g)=\langle K_2g,K_1g\rangle
=\lambda_R^2(1+\eta_1\eta_2^*)
\sum_s a_{1s}^{(0)}(g)a_{2s}^{(0)}(g)^*,
\qquad \lambda_R=1/1024.
\]

Diese Diagnose ist ein Gramprodukt der gegebenen akzeptierten Maps. Sie ist **kein** aus der vollständigen CST-Wirkung abgeleitetes physikalisches Dekohärenzfunktional. Insbesondere fehlt eine konsistente Aufspaltung des Failure-Kanals nach diesen Klassen; über die vollständige Geschichte wird hier nichts behauptet.

Der Audit rechnet mit rationalen Intervalloperationen auf den unveränderten Amplituden- und Gaußmomentrechtecken. Er erhält nach außen gerundet:

| Eingang | Re D12^acc | Additivitätsdefekt 2 Re D12^acc |
| --- | --- | --- |
| g0 | [−2,869492467829; −2,869491920090] × 10⁻¹¹ | [−5,738984935657; −5,738983840181] × 10⁻¹¹ |
| g+ | [−7,482415816812; −7,482414867032] × 10⁻¹¹ | [−1,496483163363; −1,496482973406] × 10⁻¹⁰ |

Somit gilt für den akzeptierten Sektor strikt

\[
\|K_1g+K_2g\|^2\ne\|K_1g\|^2+\|K_2g\|^2.
\]

Die ungemessenen binären Geometrieverläufe sind unter der derzeitigen kohärenten Auslese nicht einmal schwach dekoherent. Die diagonalen Quadrate durch ihre Summe zu teilen erzeugt eine mathematische Verteilung, repräsentiert aber den anders instrumentierten/dephasierten Versuch und nicht die vorhandene kohärente Erfolgswahrscheinlichkeit. Die Aussage ist keine Unmessbarkeit von N_2: Ein welcher-Weg-Record misst diese Größe, verändert aber die Kohärenz.

Eine ungemessene gewichtete Amplitudeneinfügung K_G=G_1K_1+G_2K_2 ist ebenfalls definierbar. Quotienten wie ⟨f|K_G|g⟩/⟨f|K|g⟩ sind im Allgemeinen komplex und können außerhalb des Wertebereichs von G liegen; sie dürfen ohne zusätzlich hergeleiteten schwachen Messvertrag nicht als erwartetes Volumen oder Radius verwendet werden. Eine solche Zahl wurde hier nicht als neues Ergebnis berechnet.

## 4. Die bestehende Uhrbox ist keine kausale Zeitfoliation

Die ursprünglichen Uhren sind unabhängig über [−1,1] integriert. Die Wirkung und Pakete erzwingen keine Ordnungsmonotonie. Unter dem bloßen normierten Lebesgue-Produktmaß wäre der Anteil strikt ordnungstreuer Uhrzuweisungen gleich der Zahl linearer Erweiterungen geteilt durch 6!. Exakt ergeben sich 8/720=1/90 und 6/720=1/120.

Diese Anteile sind keine Wahrscheinlichkeiten unter einer physikalischen Quantendynamik. Sie zeigen konkret, dass die Beschränkung auf t_x<t_y für x≺y die ursprüngliche Integration stark und klassenabhängig verändert. Sie ist kein bloßer globaler Wechsel T→−T und darf nicht nachträglich als bereits gewählte Eichung ausgegeben werden. Auch die intrinsische n_C-Filtration ersetzt den Staubuhr-Constraint nicht.

## 5. Minimaler weiterer Vertrag

Für die **kleinste intrinsische Geometriefrage** muss die Historienfamilie zunächst nicht vergrößert werden. N_k ist schon jetzt ein konkreter, rekonstruierbarer Zielwert. Es fehlt dafür eine physikalisch begründete Paarung sowie entweder ein Geometrieinstrument einschließlich Failure oder eine konsistente Historiendeutung. Eine Erweiterung allein der Anzahl gelabelter Geschichten löst diese Lücke nicht.

Für eine **physikalische Staubball-Dynamik R(τ)** fehlen zusätzlich ein räumlich interpretierbarer Bereich/Boundary-Memory, die Zeit- und Volumenkalibrierung aus demselben Quellenmodell und ein Verfeinerungs-/Korrespondenzargument. Wenn ausschließlich intrinsische R-Ordnungen als geometrischer Ausgang zugelassen werden, muss ein Nachfolger tatsächlich unterschiedliche R-Geometrien oder einen ausdrücklich erweiterten geometrischen Randzustand bereitstellen. Ein größerer Fall mit wieder identischen R-Antiketten wäre für diese Frage nicht ausreichend.

Der sinnvolle nächste Zulässigkeitstest ist somit konkret: Die von den anderen Fachprüfungen ausgewählte physikalische Paarung auf das bereits definierte N_k anwenden; dann feststellen, ob die entsprechenden Klassenoperatoren einen wohldefinierten, normalisierten und zusammensetzbaren Geometrievertrag ergeben. Erst bei dessen Bestehen ist eine weitere Rechenkampagne zu Geometriedynamik gerechtfertigt.

## Prüfstatus und Reproduktion

### Ergänzung: zwei innere Geometrien unter gemeinsamem N11-Dirichletrand

Nach dem ersten Audit wurde ein ausdrücklich neuer gemeinsamer Quellpatch vorgeschlagen. Er besitzt elf Elemente, äußere feste Knoten B={0,1,2,3,7,8,9,10} und innere Knoten I={4,5,6}. Die erste Ordnung ist die vollständige Kette; die zweite entfernt aus deren transitiver Relationsmenge ausschließlich (4,5) und (5,6), behält aber (4,6). Die zweite Relationsmenge ist bereits transitiv. Sie darf nicht mit dem Graphen verwechselt werden, in dem man diese beiden Kanten aus einem Hasse-Diagramm löscht und anschließend eine andere transitive Hülle bildet.

`checks/geometry/n11_check.py` rekonstruiert beide Ordnungen unabhängig. Sämtliche 28 induzierten B-Relationen und sämtliche 24 B–I-Relationen stimmen überein. Die folgenden Unterscheidungen bleiben unter beliebiger Umnummerierung der drei inneren Elemente erhalten:

| N11-Ordnungsinvariante | Kette | Modifizierte Ordnung |
| --- | --- | --- |
| Innere Relationen | 3 | 1 |
| Innere Höhe, Anzahl Elemente | 3 | 2 |
| Gesamthöhe, Anzahl Elemente | 11 | 10 |
| Intervallhistogramm N0,…,N3 | (10,9,8,7) | (11,10,8,7) |
| F4 | 10 | 18 |
| N_k, k=0,…,10 | (1,2,3,4,5,6,7,8,9,10,11) | (1,2,3,4,6,7,7,8,9,10,11) |

Damit liegen **wirklich verschiedene innere Geometrien bei gemeinsamem äußerem Dirichlet-Vertrag** vor: T_j=Δj und r_j=ρ für j∈B sowie dieselben skalaren Randwerte, beispielsweise q_j=0. Innere Daten dürfen unterschiedlich sein. Vorgeschlagen sind u_I=(4,5,6), r_I/ρ=(1,1,1) für die Kette und u_I=(4,4,5), r_I/ρ=(2,1,1) für die zweite Ordnung, mit T=Δu und Δ²=2/(19β). Für 0<ρ<1/2 liegen sämtliche vorgeschlagenen positiven Dichten strikt in (0,1). Die stationären Wirkungsgleichungen werden von den unabhängigen Wirkungsprüfungen kontrolliert, nicht von diesem kombinatorischen Skript.

Gemeinsame Dirichlet-Daten verlangen keine identischen Randimpulse. Unterschiedliche kanonische Randreaktionen könnten gerade eine messbare Antwort sein, falls der physikalische Randvertrag und die Paarung sie tragen. Aus denselben Inzidenzrelationen über den Rand folgen auch nicht identische Wirkungskoeffizienten, weil Intervallgrößen das Innere mit auswerten. Eine gemeinsame Fortsetzung in denselben Außenraum ist deshalb eine zusätzliche zu prüfende Frage.

**Reichweitenkontrolle der Uhr:** Dieser konkrete N11-Zeuge passt nicht in die alte Uhrbox [−1,1]. Bei β=4/√6 ist die minimale Spannweite zwischen den festen Endpunkten 10Δ mit (10Δ)²=50√6/19>4, numerisch etwa 2,539. Auch eine globale Uhrverschiebung verkleinert diese Spannweite nicht. Er benötigt daher ausdrücklich einen neuen Uhrausschnitt/Träger oder muss als stationärer Wirkungszeuge außerhalb des alten Integrationsvertrags bezeichnet werden. Eine Uhr-Reskalierung bei unveränderter Wirkung ist nicht kostenlos, weil die Quellenconstraints quadratische Uhrdifferenzen enthalten.

Die frühere Endrand-Konstanzaussage war auf reine intrinsische R-Observablen der alten sechs-Historien-Familie begrenzt. Sie ist **kein Grund**, verschiedene innere N11-Geometrien unter demselben äußeren Rand auszuschließen. Gerade solche Alternativen sind für einen geometrischen Kern mit festen Randdaten geeignet. Unterschiedliche F4-Werte oder stationäre Wirkungsphasen allein erzeugen allerdings noch keine geometrischen Wahrscheinlichkeiten; dafür bleiben Maß, Paarung, Interferenz-/Recordvertrag und gegebenenfalls ein gemeinsamer Außenraum zu begründen.

Der N11-Audit besteht für statische Kombinatorik, relabelinvariante Unterscheidung und gemeinsamen äußeren Datensatz. Er weist zugleich die neue Uhrträger-Anforderung nach. Er enthält keine Integration und behauptet keine physikalische Geometriedynamik.

`python -B checks/geometry/check.py` führt die endliche Rekonstruktion und die rationale Intervallrechnung aus. Die Eingaben sind gehashte Kopien des veröffentlichten Piloten, der ursprünglichen Amplituden und der unabhängig berechneten Gaußmomente. Der Code verwendet nur die Python-Standardbibliothek; keine neue Quadratur.

| Gate | Status |
| --- | --- |
| Intrinsische Downset-Filtration und zwei Verlaufssignaturen | PASS, exakt für alle sechs Historien |
| Reines intrinsisches R-Geometriesignal | Konstanz bewiesen auf dieser Familie |
| Zweiklassen-Ordnungsalgebra | PASS, Dimension 2 |
| Additivität ungemessener Klassen im akzeptierten kohärenten Map | FAIL, Re D12 strikt negativ für beide Eingänge |
| Physikalisches Gesamt-Dekohärenzfunktional einschließlich Failure | NOT_DERIVED |
| Kalibrierte Eigenzeit, Dreivolumen, Radius, Expansion | NOT_DERIVED |
| Allgemeines CST-No-go | Nicht behauptet |

## Primärliteratur und Reichweite ihrer Verwendung

1. Brightwell, Dowker, Garcia, Henson, Sorkin, *“Observables” in causal set cosmology*, Phys. Rev. D 67 (2003) 084031, [arXiv:gr-qc/0210061](https://arxiv.org/abs/gr-qc/0210061). Rollenunabhängige/covariante Ereignisse und Stemmengen motivieren eine intrinsische Ordnungssprache; der dortige CSG-Satz liefert keine Quantengewichte für diesen Piloten.
2. Major, Rideout, Surya, *On Recovering Continuum Topology from a Causal Set*, J. Math. Phys. 48 (2007) 032501, [arXiv:gr-qc/0604124](https://arxiv.org/abs/gr-qc/0604124). Die Rekonstruktion mit verdickten Antiketten benötigt treue Einbettung und hinreichend hohe Dichte. Diese Voraussetzungen liegen für die vorliegenden sechs Ereignisse nicht nachgewiesen vor.
3. Sorkin, *Quantum Mechanics as Quantum Measure Theory*, Mod. Phys. Lett. A 9 (1994) 3119–3128, [arXiv:gr-qc/9401003](https://arxiv.org/abs/gr-qc/9401003). Quantenmaß und klassisch additive Wahrscheinlichkeit sind verschiedene Begriffe. Der hier ausgewiesene Additivitätsdefekt ist direkt aus den vorhandenen endlichen Maps berechnet, keine Anwendung eines behaupteten vollständigen CST-Quantenmaßes.

Die Befunde zu den sechs Historien, Filtrationen, Intervallwerten und akzeptierten Klassenzweigen sind die neuen eigenen Rechnungen dieses Audits; die Literatur ist kein Ersatz für deren Nachweis.
