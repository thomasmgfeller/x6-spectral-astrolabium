# CST-DUST: Eichstruktur, Uhrmaß und Randkonsistenz v0.1

7. November 2026. Audit `CST-DUST-GAUGE-BOUNDARY-001`.
Ausgangspunkt: Main `374acc67cb0e6cc510ec3852fd9fe9ef2b5ed20a`, nach PR 246.

## Ergebnis und Reichweite

Die gemeinsame Umbenennungs- und Uhrverschiebungsstruktur der geerbten endlichen
Wirkung ist konsistent. Eine mittransformierte Uhrbox, passende Randdaten und
Zustände liefern exakt dieselbe Amplitude in verschobener Darstellung. Dies ist
eine Kovarianzaussage zwischen vollständig transformierten Definitionen.

Drei zusätzliche Gleichsetzungen sind dagegen im angegebenen Umfang falsch:

1. Alle Uhren auf eine Referenzuhr beziehen und anschließend unverändert
   unabhängige rechteckige Integrationsgebiete verwenden.
2. Jedes Uhrfeld auf einem Vakuumknoten als unabhängig verschiebbare, reine
   Eichvariable behandeln.
3. Die Uhrnullpunkte zweier gekoppelter Teilgebiete unabhängig zurücksetzen und
   ihre relative Lage verwerfen.

Ein exaktes induziertes Maß und ein allgemeines Nullraumkriterium ersetzen diese
Abkürzungen. Eine gravitative Constraint-Algebra, physikalische Rigging-Map,
Anomaliefreiheit, Randladungen oder eine physikalische CST-Evolution sind damit
nicht konstruiert. Alle acht physikalischen Entscheidungen bleiben HOLD. Der
frühere FAIL der ausdrücklich geprüften rohen Evolutionsinterpretation bleibt
unverändert; das Audit hebt ihn nicht auf.

Der lokale Plan wurde vor den Rechnungen gespeichert und gehasht. Die erwarteten
Mechanismen waren vorher bekannt; es handelt sich nicht um eine blinde Vorhersage
oder externe Präregistrierung. Ein offengelegter Nachtrag ergänzt Zeugen bei
w=1/2 innerhalb des positiven Dichtestratums. Die ursprünglichen binären Werte
w=0,1 bleiben algebraische Kontrollen an der abgeschlossenen Parameterbox.

## 1. Unveränderte Wirkung und genaue Begriffe

Wir verwenden dieselbe endliche strikte Ordnung C, denselben Operator und dieselbe
Materiewirkung wie der Variationskandidat. In den algebraischen Kontrollen sind
der Operatorvorfaktor A und hbar gleich eins. Die Dimensionen der geerbten
physikalischen Größen werden dadurch nicht neu bestimmt.

\[
\Gamma_x[T]=\frac12\sum_{y\prec x}B_{xy}(T_x-T_y)^2,\qquad
S_d=-\frac12\sum_xw_x-\frac14\sum_{y\prec x}w_xB_{xy}(T_x-T_y)^2.
\]

Für ein Intervall mit k Elementen gilt B_xy=A b(k), b=(1,-9,16,-8,0,...).
Die Dichtegewichte w sind integrierte Dichtegewichte, keine bereits kalibrierten
Ruhemassen. Die Gesamtwirkung enthält zusätzlich die nur von C abhängige
BDG-Wirkung. Alle folgenden Uhridentitäten lassen diesen Anteil unverändert.

Mit der Kanteninzidenz D, Zeile (-1 am Vorgänger, +1 am Nachfolger), sei

\[
L=\frac12D^T\operatorname{diag}(w_xB_{xy})D,\qquad
S_d=-\frac12T^TLT-\frac12\sum_xw_x,\qquad q=\nabla_T S_d=-LT.
\]

L ist reell symmetrisch, jedoch im Allgemeinen indefinit. Es gilt L1=0 und
sum_x q_x=0 als exakte endliche Identität. Dies beschreibt die konstante
Verschiebung des Skalarfeldes T. Es ist keine hergeleitete lokale
Raumzeit-Diffeomorphismusidentität oder gravitative Energiebilanz.

**Symmetrie ist noch keine Eichredundanz.** Eine globale Symmetrie kann eine
physikalische Ladung tragen. Ob ihr Parameter als unbeobachtbarer Uhrnullpunkt
quotientiert werden darf, hängt von Zuständen, Randdaten und der noch offenen
physikalischen Struktur ab. In diesem Audit wird kein zusätzlicher physikalischer
Quotient postuliert. Der Wechsel zu Zeitdifferenzen wird als Variablenwechsel
mit exakt mitgeführtem Maß behandelt.

Die bekannte interne Permutationsgruppe wirkt gleichzeitig auf C, T, w und
Materie-/Vakuummarken. Physikalisch fixierte externe Labels bleiben fixiert;
bei einer bloßen gemeinsamen Darstellungsänderung dürfen auch sie mitsamt ihren
Daten umbenannt werden. Die vollständigen Permutationen in der endlichen
Kontrollklasse sind algebraische Prüfungen dieses zweiten Sachverhalts. Sie
erweitern nicht die Gruppe G_fix des geerbten Randproblems.

## 2. Uhrverschiebung einschließlich Regulator und Zustand

Sei F die Menge integrierter Uhren, b die extern fixierten Uhrwerte und
I_mu=[mu-L,mu+L] mit festem L>0. Unter den übrigen unveränderten endlichen
Summen und Dichteintegralen sei

\[
K_\mu(b)=\int_{I_\mu^{|F|}}\prod_{x\in F}\frac{dT_x}{2L}
\,\exp(iS(C,T,b,w)/\hbar).
\]

**Satz.** Bei gemeinsamer Verschiebung aller Uhren gilt exakt

\[
K_{\mu+c}(b+c\mathbf1)=K_\mu(b).
\]

Beweis: T'=T+c hat Jacobi-Determinante eins, bildet I_mu bijektiv auf I_(mu+c)
ab und lässt jede Differenz im Integranden unverändert. Der Beweis gilt
summandenweise und bleibt unter der endlichen Geometriesumme und dem geerbten
positiven/atomaren Dichtemaß bestehen. Auch nichteinheitliche Uhrboxen dürfen
gemeinsam verschoben werden. Ihre relativen Mittelpunkte bleiben dann erhalten.

Bei einer Zustands-/Observableinsertion F(T,b) muss zusätzlich
F'(T+c,b+c)=F(T,b) gelten. Ein unveränderter, an einen absoluten Uhrwert gebundener
Zustand ist eine andere Präparation. Auf den Hilfsräumen mit mitbewegten Boxen
ist U_c psi(T')=psi(T'-c) eine Isometrie; die translationsinvarianten Lebesgue-
Faktoren und der übereinstimmende Träger sichern die Normgleichheit. Diese
Hilfsnorm ist nicht die bislang fehlende physikalische Norm.

Eine kompakt getragene normierte Wellenfunktion mit gleichmäßiger Dichte auf
[-1/2,1/2] hat in der Box [-1,1] Norm eins. Nach Verschiebung um eins bleiben
Zustand und mitverschobene Box gemeinsam normiert. Wird nur der Zustand
verschoben und weiter in [-1,1] integriert, beträgt die erfasste Norm 1/2.
Das ist ein Trägereffekt, keine nachgewiesene Quantenanomalie.

Eine endliche feststehende Box ist nicht unter allen reellen Translationen
invariant. Auch ein normiertes, nichttriviales translationsinvariantes
Wahrscheinlichkeitsmaß auf ganz R existiert nicht: disjunkte verschobene
Einheitsintervalle müssten denselben Massenanteil tragen, was Normierung und
Abzählbarkeit widerspricht. Eine Regulatorentfernung oder Gauge-Fixierung
braucht daher eine eigene Begründung; sie folgt nicht aus dem Verschiebungssatz.

### Endliche Ward-Identität mit Randfluss

Ohne weitere explizite Uhrabhängigkeit folgt durch Differentiation

\[
\left(\partial_\mu+\sum_{a\in\partial}\partial_{b_a}\right)K_\mu(b)=0,
\]

\[
\partial_\mu K_\mu=\frac1{(2L)^{|F|}}
\sum_{x\in F}\int_{I_\mu^{|F|-1}}dT_{\ne x}
\left[e^{iS/\hbar}\right]_{T_x=\mu-L}^{T_x=\mu+L}.
\]

Bei Insertionen gehören deren Ableitungen in dieselbe Identität. Ein Ward-Rest
nach Weglassen dieses Boxflusses misst zunächst eine ausgelassene Randantwort.
Er beweist keine gravitative Anomalie. Die Nullraumidentität sum q=0 ist die
entsprechende algebraische Voraussetzung auf Integrandenebene.

### Zertifizierter Zweistellenzeuge

Bei einem festen Dichtewert w>0, einer Kausalrelation und L=1 genügt nach
Abspaltung der gemeinsamen Phase exp(-iw/2)

\[
\widetilde K_\mu(b)=\frac1{2L}\int_{\mu-L}^{\mu+L}
e^{-iw(t-b)^2/4}\,dt.
\]

Neun gemeinsame Verschiebungen erfüllen die exakte Kovarianz; neun bloße
Verschiebungen von b bei festgehaltener Box ändern den Zeugen nachweislich.
Dies wird sowohl bei w=1 als algebraischem Randwert als auch bei w=1/2 im
offenen positiven Dichtestratum geprüft. Es ist ein bedingter Festdichtezeuge,
keine bereits ausgewertete vollständige Geometrie-Materie-Amplitude.

Für reale x wird exp(-ix) bis Grad p=60 integriert. Der komplexe Rest ist
höchstens |x|^(p+1)/(p+1)!, denn die Ableitungen entlang der reellen Achse haben
Betrag eins. Alle Polynomkoeffizienten, Integrale und Restschranken sind rational.
Die ausgegebenen Dezimalintervalle sind nach außen gerundet. Disjunkte reelle
oder imaginäre Komponenten zertifizieren die Ungleichheit. Die Ward-Ableitung
wird unabhängig aus dem integrierten Polynom und den Endpunktreihen gebildet.
Die Anzeigenpräzision ist keine physikalische Präzisionsangabe.

## 3. Das richtige Maß nach Wahl einer Referenzuhr

Dieser Abschnitt betrifft **alle N frei integrierten Uhren** mit unabhängigem
Gleichmaß in derselben Box [-L,L]. Bereits festgehaltene Randuhren sind ein
anderes Konditionierungsproblem. Es wird keine zusätzliche Monotoniebedingung
an die Uhren angenommen; solche Bedingungen müssten bei Einführung mitgeführt
werden.

Setze r_0=0, r_i=T_i-T_0 (i=1,...,N-1), s=T_0. Der Jacobi-Faktor ist eins.
Für ein festes r muss s in allen Intervallen [-L-r_i,L-r_i] liegen. Deren
gemeinsame Länge lautet

\[
\ell_L(r)=\left[2L-\{\max(0,r_1,...,r_{N-1})-
\min(0,r_1,...,r_{N-1})\}\right]_+.
\]

Für jede integrierbare translationsinvariante Funktion f folgt exakt

\[
\frac1{(2L)^N}\int_{[-L,L]^N}f(T_i-T_0)d^NT
=\int_{\mathbb R^{N-1}}f(r)W_L(r)d^{N-1}r,
\qquad W_L=\frac{\ell_L(r)}{(2L)^N}.
\]

W_L ist nicht rechteckig und koppelt die relativen Uhren. Es hat die korrekte
Dimension Zeit^(-(N-1)) und Integral eins. Ein unabhängiger Normalisierungsbeweis
zerlegt in N! Ordnungskammern der N Uhrwerte; jede trägt nach den geordneten
Abstandsintegralen die Masse 1/N!.

Das direkte Konditionieren auf T_0=0 liefert dagegen die unabhängige Box für die
anderen Uhren. Konditionierung und Integration über den ursprünglichen
Uhrnullpunkt sind verschiedene Operationen. Selbst ein formaler Deltaeinsatz
mit lokalem Jacobi-Faktor eins ersetzt nicht die r-abhängige Faserlänge des
vorhandenen Regulators. Das Audit liefert einen exakten Pushforward, keine
aus CST hergeleitete Faddeev-Popov- oder physikalische Quotientkonstruktion.

### Überprüfbarer Unterschied

Für N=2 ergibt sich die Dreiecksverteilung

\[
W_L(r)=\frac{(2L-|r|)_+}{4L^2},\qquad
E[r^2]=\frac{2L^2}{3}.
\]

Das naive Gleichmaß auf [-L,L] ergäbe L²/3. Für verschiedene i,j>0 gilt
E[r_i r_j]=L²/3, während die naive unabhängige Box null liefert. Allgemein ist
E[r^(2k)]=2(2L)^(2k)/[(2k+1)(2k+2)], die ungeraden Momente verschwinden.
Die direkte binomische Entwicklung zweier unabhängiger Uhren bestätigt diese
Momente exakt bis Grad 12. 2 340 zusätzliche rationale Schnittlängenfälle
prüfen den Dichteausdruck; mit Momenten und Normalisierung sind es 2 508 Kontrollen.

Auch die beiden Amplitudenintegrale von exp(-iwr²/4) unterscheiden sich bei
L=1/2,1,2 für w=1 und w=1/2 durch zertifiziert disjunkte Intervalle. Der
Unterschied betrifft somit die regulierte Amplitude, nicht nur einen
unbeobachtbaren gemeinsamen Normierungsfaktor des Uhrmaßes.

Für amplitudengewichtete oder zustandsabhängige Auswertungen müssen Wirkung,
Zustand und Observable gemeinsam transformiert werden. Die oben genannten
Momente sind Momente des Hilfsmaßes, keine vorhergesagten physikalischen
Staubzeitfluktuationen.

## 4. Wann ist eine Vakuumuhr wirklich flach?

Bei festem C,w und einem reellen Vektor v gilt

\[
S_d(T+av)-S_d(T)=-a\,v^TLT-\frac{a^2}{2}v^TLv.
\]

**Satz.** Die Verschiebung T->T+av lässt die Wirkung für alle T und a genau
dann unverändert, wenn Lv=0. Notwendigkeit folgt aus dem linearen Koeffizienten
für beliebiges T; Hinlänglichkeit aus Symmetrie von L. Für eine einzelne Uhr
ist v=e_z, also muss die ganze Spalte L_:z verschwinden. Für beliebige unabhängige
Verschiebungen mehrerer Vakuumuhren müssen alle entsprechenden Spalten null sein.

Das Kriterium ist stärker als w_z=0. Der Wert T_z kommt auch in Zeilen späterer
Materieelemente vor. Eine zufällig verschwindende erste Variation bei einem
einzigen T reicht nicht. Ebenso reicht v^TLv=0 bei indefinitem L nicht: der
lineare Term kann bleiben. Nullrichtungen bei einem einzelnen C,w müssen
außerdem nicht beim Wechsel der Dichte oder Geometrie erhalten bleiben.

### Expliziter innerer Vakuumknoten

Nimm die Viererkette 0<1<2<3 mit w=(0,0,w,0), 0<w<1 und
T=(0,t,1,2). Beide äußeren Dichtegewichte sind null. Element 1 ist ein innerer
Vakuumknoten, Element 2 trägt Materie. Es gilt

\[
S_d(t)=-\frac w2+\frac{9w}{4}-\frac w4(1-t)^2.
\]

Der Wechsel t=1/4 zu t=3/4 erhält die zeitliche Reihenfolge und liefert
Delta S=w/8. Für w=1/2 ist dies exakt 1/16. Die zugehörige Vakuumspalte ist
nicht null. Dagegen ist die Spalte des letzten Elements 3 hier tatsächlich
null, weil keine spätere Materie mehr koppelt.

Die Algebra-Kontrollklasse enthält alle 242 gelabelten Ordnungen mit N=1,...,4
und ihre binären Dichtemuster: 3 670 markierte Fälle. Von 7 249 w=0-Stellen
haben 2 541 eine nichtverschwindende Spalte und 4 708 eine Nullspalte. Diese
Häufigkeiten sind kombinatorische Zählwerte, keine physikalischen Wahrscheinlichkeiten.

Das Ergebnis widerlegt nur die behauptete unabhängige T-Verschiebung bei festem
C,w. Es beweist weder, dass jede gekoppelte Vakuumuhr ein physikalischer
Freiheitsgrad ist, noch dass eine größere Transformation unter gemeinsamer
Änderung von Geometrie und Materie unmöglich wäre. Auch flache Variablen dürfen
erst nach Behandlung von Maß, Zustand und Rändern eliminiert werden.

## 5. Gemeinsamer Nullpunkt und relative Randdaten

Zerlege denselben vollständigen Kausalset in A und B. Setze v=1_B und
delta=c_B-c_A. Die gemeinsame Verschiebung c_A verschwindet aus der Wirkung,
während die relative Verschiebung exakt ergibt

\[
\Delta S_d=\delta\sum_{x\in B}q_x
-\frac{\delta^2}{2}\,1_B^TL1_B.
\]

Die lineare Antwort ist die bekannte Summe des Variationsstroms über den Schnitt.
Da L1=0, betreffen diese Koeffizienten die Kopplung über den Schnitt. Eine
unabhängige Verschiebung beider Gebiete ist für alle T nur dann eine Symmetrie,
wenn L1_B=0. Andernfalls muss bei getrennten lokalen Uhrkoordinaten die relative
Nullpunktlage als Kopplungsdatum erhalten bleiben. Sie einfach auf null zu setzen
ist ein anderes Randproblem.

49 992 geordnete nichttriviale Zweiteilungen der markierten Kontrollklasse
bestätigen diese Formel und die geerbte vollständige Wirkungsverklebung. In
30 820 Fällen ist die relative Richtung gekoppelt; 19 172 sind bezüglich dieser
Richtung flach. Auch diese Zahlen sind keine physikalischen Häufigkeiten.

Dies beweist keine gravitative Randladung und konstruiert keine CST-Edge-Modes.
Es isoliert den bereits auf Wirkungsebene sichtbaren Verlust durch eine
unbegründete getrennte Reduktion. Die vollständige gemeinsame Quantensumme
benötigt weiterhin kompatible Randzustände, Maßfaktoren und die korrekte
Behandlung verbleibender Redundanzen. Die Raumzeitoberfläche des Staubs ist
weiterhin von einer künstlichen Rechengrenze zu unterscheiden.

## 6. Darstellungsänderung, Uhrskalierung und physikalische Variation

Die gemeinsame Permutation und die konstante Uhrverschiebung kommutieren.
85 034 vollständige gemeinsame Umbenennungen der Kontrollklasse bestätigen
Wirkungsinvarianz und diese Kommutation. Für die allgemeine Identität genügt,
dass eine Permutation den konstanten Vektor 1 erhält. Diese Aussage löst keine
neuen dynamischen Constraints.

Für T'=aT+b folgt exakt Gamma[T']=a² Gamma[T]. Auf einem normierten
Staubstratum Gamma=-1 bleibt deshalb unter dieser affinen Änderung bei
unveränderten Einheiten nur a²=1 möglich. Die fest gewählte Zukunftsorientierung
schließt a=-1 als bloße Uhrkonvention aus. Eine allgemeine monotone Funktion f
ist ebenfalls nicht automatisch eine zulässige Eigenzeit-Eichtransformation:
im Kontinuumsziel wird die Norm mit (f')² multipliziert. Eine zusätzliche
Lapse- oder Variablenumdefinition wäre gesondert herzuleiten.

Als relationale Hilfsobservable wird O_tau=sum_x w_x 1(T_x<=tau) verwendet.
Unter gemeinsamer Verschiebung von T und tau bleibt sie gleich. Ein fester
Schwellenwert nach Verschiebung der Felder bezeichnet im Allgemeinen ein anderes
Ereignis. O_tau ist hier eine labelinvariante Hilfsgröße, kein bereits
kalibrierter Massenoperator und keine bewiesene gravitative Dirac-Observable.

Eine Änderung der Ordnung darf nicht mit einer Eichumbenennung verwechselt
werden. Viererkette und Viererdiamant mit denselben Anfangs-/Endmarken besitzen
die verschiedenen BDG-Zähler 3 und -16. Sie bleiben verschiedene Historien.
Ebenso ist eine Änderung von Staubmasse oder relativer Randzeit nicht durch
dieses Audit als Eichfreiheit qualifiziert.

Der frühere Zweistellenkern hängt nur von Uhrdifferenzen ab. Gemeinsame
Verschiebung aller vier Randlabels lässt daher jedes Matrixelement und das
bekannte gemeinsame-M-Hindernis unverändert. Uhrnullpunkt-Kovarianz repariert
keine fehlende physikalische Normierung.

## 7. Entscheidungen und nächster Modellschluss

| Aussage | Entscheidung |
|---|---|
| Gemeinsame Label-/Uhrverschiebungsalgebra | PASS im endlichen, angegebenen Umfang |
| Kovarianz bei vollständiger Mittransformation | PASS; allgemeiner Variablenwechsel und zertifizierte Zeugen |
| Induziertes relatives Uhrmaß | PASS als exakter Pushforward des Hilfsmaßes |
| Referenzuhr null und übrige ursprüngliche Box unverändert | FAIL als äquivalente Umschreibung |
| Alle Vakuumuhren bei festem C,w frei verschiebbar | FAIL für den geerbten Wirkungsansatz |
| Unabhängiges Zurücksetzen gekoppelter Teilgebiete ohne relative Daten | FAIL |
| Physikalische Eichquantisierung / gravitative Constraints | HOLD |
| Gravitative Anomalie nachgewiesen | Nein; nicht etabliert |
| MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING, EXTENSION | jeweils HOLD für diesen Audit-Record |

Die letzten acht Entscheidungen sind ein neuer Audit-Record. Er ersetzt keine
älteren kandidatenspezifischen FAIL-Datensätze und behauptet keine Prüfung durch
einen mathematischen Beweisassistenten. Der alte Vertrag und seine Logik sind
unverändert als Herkunftseingaben enthalten.

**Nächster konkreter Schritt:** Eine physikalische Historienkonstruktion mit
vollständigen relativen Randdaten und begründetem positivem Dekohärenzfunktional
aufbauen. Zunächst keine zusätzliche Zeittranslation als Eichgruppe ausmitteln,
bevor ihre physikalische Rolle geklärt ist. Bei Bezug auf eine Referenzuhr muss
das induzierte Maß erhalten bleiben oder ein ausdrücklich neuer Regulator mit
begründeter Vergleichsabbildung definiert werden. Gekoppelte Vakuumuhren dürfen
nur durch die vollständige Integration oder eine kontrollierte Reduktion entfernt
werden; ein stationärer Ersatz allein genügt nicht.

Dann sind physikalische Schnitt-/Vergröberungskonsistenz, erlaubte Ereignisse,
Randnorm und Korrespondenz zu qualifizieren. Die Kontinuums-Hypersurface-
Deformationsalgebra wird nicht ungeprüft als exakte endliche CST-Algebra verlangt.
Eine kovariante Route muss aber ihre eigenen Konsistenzbedingungen und den
geeigneten klassischen Grenzfall liefern. Natürlich gelabelte Wachstumspfade,
Lorentz-/Tetradfragen und interne Yang-Mills-Symmetrien werden nicht durch die
hier behandelte Skalarfeldtranslation mitgeprüft. Der neutrale Staubkandidat
enthält keine U(1)- oder Yang-Mills-Verbindung.

## 8. Nachrechnung, Entwicklungshinweis und Quellen

`python3 -O -B analyze.py` benötigt nur die Standardbibliothek. Alle harten
Entscheidungen verwenden explizite Prüfungen, die unter -O aktiv bleiben.
`verify_quadrature.py` ist eine zusätzliche unabhängige Gleitkomma-Kontrolle mit
SciPy; sie ersetzt keine rationalen Zertifikate. `replay.py` führt eine isolierte
Neuberechnung aus und vergleicht die reproduzierbaren Ergebnisdateien bytegenau.
Plan, Nachtrag, geerbte Eingaben und vollständige Quellen sind im Paket enthalten.

Entwicklungshinweis: Die erste Ausführung traf auf eine ungeeignete Negativprobe
für O_tau: tau=1/2 lag vor dem einzigen positiven Gewicht und lieferte in beiden
verglichenen Fällen null. Für die aussagekräftige Probe wurde tau=3/2 gewählt.
Dies änderte keine Wirkung, Toleranz, physikalische Eingabe oder behauptete
Vorhersage; die Kontrollen sind ausdrücklich explorative Algebra-Validierung.

Primärquellen, am 7. November 2026 erneut geprüft:

1. Rideout & Sorkin, A Classical Sequential Growth Dynamics for Causal Sets,
   https://arxiv.org/abs/gr-qc/9904062 . Diskrete Kovarianz in einer bestimmten
   klassischen Wachstumsdynamik; kein Nachweis für unseren BDG-Staubkern.
2. Brown & Kuchar, Dust as a Standard of Space and Time in Canonical Quantum
   Gravity, https://arxiv.org/abs/gr-qc/9409001 . Kanonische Kontinuumsreferenz
   materieller Uhren; nicht identisch mit dem eingeschränkten irrotationalen
   endlichen Kandidaten dieses Audits.
3. Donnelly & Freidel, Local subsystems in gauge theory and gravity,
   https://arxiv.org/abs/1601.04744 . Kontinuumsansatz für Randfreiheitsgrade;
   begründet die zu prüfende Frage, liefert keine fertigen CST-Randladungen.
4. Bahr & Dittrich, Breaking and restoring of diffeomorphism symmetry in discrete
   gravity, https://arxiv.org/abs/0909.5688 . Symmetriefragen diskreter Gravitation;
   keine Diagnose einer Anomalie unseres Kandidaten.

Projektquellen (im Ordner inputs unverändert archiviert):

- `variation_v0_1/DERIVATION.md`, `variation.py`: konkrete Materiewirkung,
  Regulatoren, Variationsstrom und Aussagegrenzen.
- `quantum_structure_v0_1/DERIVATION.md`: Hilfszustandsraum und gemeinsame-M-
  Gegenbeispielklasse.
- `gluing_v0_1/DERIVATION.md`, `gluing.py`: vollständige endliche Verklebung.
- `model_contract_v0_1/contract.json`, `gate.py`: geerbte physikalische Prüfpflichten.

Alle unter https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/374acc67cb0e6cc510ec3852fd9fe9ef2b5ed20a/research/rax_cqg/dust_collapse .

Die hier abgeleiteten Identitäten und Gegenbeispiele werden als projektinterne
Rechnungen ausgewiesen. Ein Neuheitsanspruch gegenüber der mathematischen
Literatur wird nicht erhoben. Keine neuen dynamischen 4D-Ensembles, keine
bezahlten Läufe, keine Singularitätsauflösung.
