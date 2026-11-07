# CST-DUST: Randgedächtnis und exakte Fortsetzung v0.1

7. November 2026. Audit `CST-DUST-BOUNDARY-MEMORY-001`.
Basis: Main `886052d8eb9d619da91896d23e0a7ede511ef30f`, nach PR 248.

## Ergebnis

Die vollständige Vergangenheit liefert eine **hinreichende Zustandsdarstellung**,
mit der die bestehende endliche Geometrie-Materie-Amplitude schrittweise und
ohne Informationsverlust aufgebaut werden kann. Dies ist eine exakte
Umschreibung des geerbten Modells bei festem endlichem Elementzahlsektor,
keine neu hergeleitete physikalische Wachstumsdynamik.

Drei Lücken werden konkret geschlossen:

1. Der vollständige Wirkungszuwachs eines neuen maximalen Elements ist aus
   den Intervallzahlen und den ersten beiden Uhrmomenten seiner Vergangenheit
   berechnet. Alte Intervalle bleiben unverändert.
2. Die Umstellung von beliebigen auf natürliche Labels erhält das bisherige
   Zählmaß genau mit dem Faktor 1/e(P), wobei e(P) die Zahl der linearen
   Erweiterungen der inneren Ordnung ist. Die Schrittquotienten e(P)/e(P′)
   teleskopieren zu diesem Faktor.
3. Der zugehörige Operator bewahrt alte Feldvariablen. Er gehört daher nicht
   zur beschränkten Integralkernklasse des vorherigen Kompaktheitshindernisses.
   Das ist ein tatsächlich anderer Ansatz für die Zustandsdarstellung, kein
   Widerspruch zum früheren Satz.

Ein allgemeiner Gegenbeispieltyp zeigt zugleich: Ein fester Kragen der letzten
r Ordnungslagen genügt unter allen zulässigen zukünftigen Ordnungsidealen
nicht. Auch eine lokale Normierung der korrekt gezählten Schritte bewahrt die
ursprüngliche Amplitude nicht. Positive Schnittprodukte lassen sich bei
vorgegebenem endlichem Endhorizont zurückziehen; sie hängen aber von dessen
frei gewähltem Produkt ab. Die unabhängige physikalische Auswahl bleibt offen.

**Alle acht physikalischen Gates bleiben HOLD.** Die Konstruktion ist weder
eine 4D-Staubballsimulation noch ein Junction-, Regularitäts- oder Bounce-Beweis.

## 1. Randvertrag: vollständige Vergangenheit statt unbegründetem Kragen

Die geerbte Spezialklasse besitzt einen fixierten Anfangsanker a und einen
fixierten Endanker f. Die m inneren Elemente liegen zwischen beiden. Die
innere Ordnung P ist beliebig. Ein Zwischenzustand enthält a, alle bisher
aufgebauten inneren Elemente, deren gesamte Relation und alle Felder T,w
einschließlich der Vakuumuhren. Der Endanker f wird erst am Ende oberhalb
aller inneren Elemente eingefügt. Äußere Randdaten bleiben fest.

Ein neues inneres Element z ist maximal; seine Vergangenheit ist
I={a}∪J, wobei J ein Ordnungsideal von P ist: x∈J und y≺x ⇒ y∈J.
Alle solchen J bleiben zugelassen. Auf diese Weise werden genau die natürlich
gelabelten inneren Ordnungen erzeugt. Die Geburtsnummer ist eine Hilfsmarkierung
einer linearen Erweiterung, **keine Staubeigenzeit**. Die kontinuierlichen
Uhren bleiben die geerbten freien Feldkoordinaten; eine zusätzliche
Monotoniebeschränkung wird nicht eingeführt.

Erhalten bleiben die Wirkung, die positiven Regulatormaße dT/(2L),
dν(w)=½δ₀+½1_(0,1)dw, die äußeren Marken und die volle gemeinsame Kopplung.
Der anfängliche Anker hat in den Kontrollen w_a=0; zur Endkontrolle wird
w_f=0 gewählt. Die Wirkungsidentität selbst gilt auch für einen anderen
deklarierten neuen Dichtewert. Die physikalische Herleitung des äußeren
Wirkungsterms S_outer=0 ist weiterhin nicht erfolgt.

Diese Darstellung ist hinreichend, aber nicht als minimal bewiesen. Ein
kleinerer Zustand wäre zulässig, wenn jede erlaubte zukünftige Anfügung samt
Maß, Feldern und Ereignissen dieselben konditionierten Amplituden erzeugt.
Eine solche vollständige zukünftige Äquivalenz ist stärker als gleiche
Elementzahl, gleiche Wirkung oder gleiche sichtbare Maxima. Die Wahl einer
physikalischen Ereignisalgebra und eine kontrollierte Näherung sind gesonderte
Aufgaben. Eine rechnerische Wachstumsschnittfläche ist nicht automatisch die
zeitartige Oberfläche des Staubballs.

## 2. Exakter Ein-Element-Zuwachs

Für y∈I sei k_y=|{u∈I:y≺u}|. Diese Menge ist genau das neue offene Intervall
I(y,z). Mit b=(1,−9,16,−8) und b(k)=0 für k≥4 definiere

\[
n_k(I)=\sum_{y\in I}\mathbf1_{k_y=k},\quad
M_k^{(j)}(I)=\sum_{y\in I,\,k_y=k}T_y^j,\quad M_k^{(0)}=n_k.
\]

**Satz.** Beim Anfügen von z mit T_z=t und w_z=w gelten exakt

\[
\Delta F_4=1-\sum_{k=0}^3b_k n_k,
\]

\[
\Delta S_d=-\frac w2-\frac w4\sum_{k=0}^3b_k
\left(n_k t^2-2M_k^{(1)}t+M_k^{(2)}\right).
\]

Im Code sind der Operatorvorfaktor A und ℏ gleich eins; κ bleibt als formaler
Koeffizient von F₄ erhalten. Allgemein ist der entsprechende A-Faktor im
quadratischen Materieterm mitzuführen. w ist ein integriertes Dichtegewicht,
keine bereits kalibrierte Ruhemasse.

**Beweis:** z ist maximal und kann deshalb in keinem Intervall zwischen zwei
alten Elementen liegen. Alle alten gravitativen und materiellen Paarbeiträge
bleiben gleich. Neu sind nur der Elementterm, die Dichtekonstante −w/2 und
die Paare y≺z. Ausmultiplizieren von (t−T_y)² und Gruppieren nach k_y liefert
die Formeln. Der geerbte direkte Wirkungsrechner bestätigt beide Identitäten.

Die zwölf Momente genügen für **dieses vorgeschlagene I**. Sie bilden nicht
automatisch einen universellen Zustand für alle späteren Ideale oder dessen
Aktualisierung. Die Zulässigkeit der Ideale und die Zugehörigkeit ihrer
Elemente benötigen weiterhin Ordnungsinformation. Vier Intervallschichten
begrenzen ferner nicht deren Anzahl von Elementen.

Bei zwei unvergleichbaren neuen Elementen können beide zulässigen
Geburtsreihenfolgen gewählt werden. Da ihre Endordnung und Felder nach
gemeinsamer Umbenennung übereinstimmen, teleskopieren die Wirkungszuwächse
zur selben Gesamtwirkung. Für die endliche Zählklasse wird dies zusätzlich
mit Feldern geprüft. Es handelt sich um endliche Darstellungsunabhängigkeit,
nicht um eine hergeleitete gravitative Constraint-Algebra.

## 3. Warum kein fester oberer Ordnungskragen genügt

Für jedes r≥1 wähle dieselbe alte Kette

\[
a\prec y\prec c_1\prec\cdots\prec c_r.
\]

Als gespeicherter Kragen seien die obersten r inneren Lagen c₁,…,c_r und der
äußere Anker a festgehalten. Alle alten Dichtegewichte sind null. Setze
T_a=−1, T_(c_j)=1+j/(r+1). Nur die unsichtbare Vakuumuhr T_y unterscheidet
sich: 1/4 beziehungsweise 3/4. Beide Zustände haben dieselbe vollständige
Ordnung, dieselbe alte Wirkung und identische gespeicherte Kragendaten.

Füge z mit Vergangenheit {a,y}, T_z=1 und w_z=1/2 an. Das ist ein zulässiges
Ordnungsideal; z bleibt zu allen c_j unvergleichbar. Der alte Knoten y bildet
nun einen Link zu z, unabhängig davon, wie weit er unter den bisherigen
Maxima lag. Nur sein neuer Paarterm unterscheidet sich:

\[
S_d^{(3/4)}-S_d^{(1/4)}
=-\frac18\left[(1-3/4)^2-(1-1/4)^2\right]=\frac1{16}.
\]

Der gemeinsame gravitative Beitrag und der Beitrag von a ändern die
Differenz nicht. Ein später identisch angefügter Endanker f mit w_f=0 stellt
den ursprünglichen Intervallträger her und bewahrt diese Differenz. Alle
gewählten Uhren liegen innerhalb der vorherigen Hilfsbox L=4; sie erfüllen
sogar die Ordnung der hier vorhandenen Kettenrelationen.

Damit gibt es für **jedes feste r** zwei beim angenommenen Kragenzustand
ununterscheidbare Vergangenheiten mit verschiedenen erlaubten
Fortsetzungsamplituden. Acht rationale Fälle r=1,…,8 prüfen die allgemeine
Familie. Der Satz schließt nicht alle komprimierten Zustände, zusätzliche
Trägerbeschränkungen oder Näherungen mit Fehlerkontrolle aus. Er sagt ebenso
wenig, dass jede Vakuumuhr schon ein physikalischer Freiheitsgrad ist.

## 4. Korrekte Umstellung des Zählmaßes

Sei e(P) die Anzahl der linearen Erweiterungen der m inneren Elemente.
Für beliebige Labels benutzt der geerbte Kandidat den Faktor 1/m!, da a und f
fixiert bleiben. Für einen isomorphieinvarianten Integranden I(P) gilt

\[
\frac1{m!}\sum_{P\in\Omega_m^{lab}}I(P)
=\sum_{P\in\Omega_m^{nat}}\frac{I(P)}{e(P)}.
\]

**Beweis:** Für einen Isomorphietyp mit Automorphismengruppe Aut(P) gibt es
m!/|Aut(P)| verschiedene beliebig gelabelte und e(P)/|Aut(P)| verschiedene
natürlich gelabelte Ordnungen. Die Automorphismengruppe wirkt frei auf
linearen Erweiterungen. Beide Seiten geben daher I(P)/|Aut(P)|. Bei
vollständigen Materiemarken werden die Stabilisatoren entsprechend kleiner;
das gleiche Kürzungsargument gilt. Für kontinuierliche Felder folgt die
Identität durch deren gemeinsame Umbenennung unter den symmetrischen
Produktmaßen. Labelabhängige fixierte Daten dürfen nicht mitgemittelt werden.

Die natürliche Geburtsreihenfolge allein ist also keine korrekte
Gauge-Fixierung mit unverändertem Zählgewicht eins. Schon für zwei innere
Elemente lauten die vollständigen gravitativen Endsektoren

\[
Z_2(z)=z^3+\tfrac12 z^{-16},\qquad z=e^{i\kappa}.
\]

Die innere Kette hat e=1, die innere Antikette e=2; beide besitzen dieselben
festen äußeren Anker. Unkorrigierte natürliche Zählung gäbe z³+z⁻¹⁶ und
veränderte das relative Gewicht.

Eine lokale Zerlegung des richtigen Faktors ist

\[
r(P\to P')=\frac{e(P)}{e(P')},\qquad
\prod_{j=0}^{m-1}r(P_j\to P_{j+1})=\frac1{e(P_m)},\quad e(\varnothing)=1.
\]

Zusammen mit den exakten Wirkungszuwächsen und allen neu integrierten Feldern
reproduziert dies die geerbte feste-m-Amplitude. Der Anfangsphasenfaktor des
Ankers und der abschließende Zuwachs durch f gehören dazu. Es wird kein
zusätzlicher Aut-Faktor daneben eingefügt. Endliche Austauschdiamanten
unvergleichbarer Geburten besitzen identische korrigierte Phasen und
Zählprodukte.

Natürliche Labels und endliche Pfadunabhängigkeit sind bekannte Bestandteile
des sequentiellen CST-Ansatzes [1]. Hier werden keine klassischen
Rideout-Sorkin-Übergangswahrscheinlichkeiten eingesetzt. Der Faktor 1/e ist
aus dem bereits gewählten festen-m-Zählmaß hergeleitet; er begründet dieses
Maß selbst nicht neu und definiert noch kein konsistentes unendliches
Wachstums-Quantenmaß. Dessen Ereignisfortsetzung bleibt eigenständig [2].

## 5. Ein Hilfszustandsraum, der alte Felder bewahrt

Für die implementierte Darstellung sei

\[
\mathcal H_m^{nat}=\bigoplus_{P\in\Omega_m^{nat}}
L^2(X_P,d\mu_P),
\]

mit orthonormalem Zählprodukt der natürlichen Ordnungen und den normierten
geerbten Feldmaßen. Die Anfangsankerdaten bleiben extern. Die natürlichen
Labels sind Rechenmarkierungen; dieser Raum ist nicht als physikalischer
Quotient der Geburtsbeschreibungen qualifiziert. Physikalische
Ereigniskandidaten müssen mit der vollständigen Umbenennung verträglich sein.

Da jedes natürlich gelabelte Kind beim Entfernen des zuletzt benannten
Elements genau einen natürlichen Elternzustand besitzt, ist die Abbildung

\[
(V_m\psi)(P',\xi,u)=
\frac{e(P)}{e(P')}e^{i\Delta S(P,\xi,u)/\hbar}\psi(P,\xi)
\]

wohldefiniert. ξ sind sämtliche alten Felder, u die neuen Uhr-/Dichtedaten.
Die alten ξ werden **nicht ausintegriert**. Die vollständige Integration
zur Endamplitude erfolgt erst mit dem Endzustand/Ereignis beziehungsweise
der deklarierten Endkontraktion. Fubini ist im endlichen regulierten Modell
zulässig, da alle inneren Maße endlich und die Phasen beschränkt sind.

In einer Integralkernschreibweise besitzt V_m Deltafaktoren in den alten
Feldvariablen. Es ist kein beschränkter quadratintegrierbarer Kern zwischen
den kompletten alten und neuen Konfigurationen. Das Kompaktheitshindernis
von v0.1 der Historienprüfung ist deshalb auf diesen Operator nicht
anwendbar. Für festes m sind die späteren Normfaktoren positiv und endlich;
auf einem unendlichdimensionalen Feldsektor ist V_m sogar nach unten
beschränkt und daher nicht kompakt. Die frühere integrierte Rohkernklasse
bleibt von diesem Ergebnis unberührt.

Das eröffnet eine präzise Route mit erhaltenem Gedächtnis. Es beweist noch
keinen physikalischen Randzustandsraum und keine unitäre Eigenzeitentwicklung.

Insbesondere behandelt das erklärte Hilfsprodukt verschiedene natürliche
Beschreibungen orthogonal. Diese Unterscheidbarkeit darf nicht ohne Prüfung
als physikalischer Endrecord benutzt werden: Die korrekte Endamplitude
summiert die redundanten Beschreibungen kohärent. Ein physikalischer
Labelquotient und die dazu passende Endkontraktion sind eine zusätzliche
Anforderung; die folgende Diagonalnorm ist ausdrücklich ein Hilfstest.

## 6. Exakter Normtest und Gefahr lokaler Nachnormierung

Weil neue Feldmaße auf eins normiert sind, die Phase Betrag eins besitzt
und verschiedene natürliche Kinder orthogonal sind, folgt

\[
V_m^\dagger V_m=Z_m(P),\qquad
Z_m(P)=\sum_{J\text{ Ideal von }P}
\left[\frac{e(P)}{e(P+_J z)}\right]^2,
\]

als Multiplikationsoperator auf der Geometriekomponente. Diese Formel gilt
für alle alten L²-Felder unter dem erklärten Hilfsprodukt; sie benötigt
keine physikalische Interpretation der Phase als Wahrscheinlichkeit.

| Innerer Elternzustand | Exakter Normfaktor |
|---|---:|
| Ein Element | 5/4 |
| Zweierkette | 49/36 |
| Zweierantikette | 2 |

Die Zweierkette hat drei Ideale mit Schrittgewichten 1/3, 1/2, 1;
die Antikette vier mit 1/3, 2/3, 2/3, 1. Bereits auf derselben Stufe m=2
existiert damit kein gemeinsamer skalarer Normierungsfaktor für alle Eltern.
Dies ist ein FAIL für das erklärte Zählprodukt, kein Ausschluss jeder
anderen unabhängig begründeten Norm.

Aus dem leeren inneren Zustand erzeugt die exakte Fortsetzung den speziellen
Vektor e^(iS)/e(P). Dieser ist unter gemeinsamen natürlichen Umbenennungen
kovariant. Ein skalarer Faktor pro Stufe kann seine **Gesamtnorm** natürlich
auf eins setzen; damit werden noch nicht alle Ereignis-Gramformen erhalten.
Im erklärten orthogonalen Hilfsprodukt hat der erreichbare Record
„die ersten beiden inneren Geburten bilden eine Kette“ zunächst Gewicht
4/5. Nach einer weiteren vollständigen Fortsetzung und erneuter gemeinsamer
Normierung hat derselbe angehobene Record Gewicht 49/67. Diese exakte
Kontrolle betrifft natürliche Wachstumsrecords. Das genannte Ereignis ist
nicht als kovariantes physikalisches Ereignis nach Quotientbildung qualifiziert;
es wird insbesondere nicht als physikalische Wahrscheinlichkeitsverletzung
oder als No-go für den tatsächlichen erreichbaren physikalischen Sektor benutzt.

Man kann formal V_m durch V_m/√Z_m(P) isometrisch machen. Dann verändert
jedoch das Produkt der Zusatzfaktoren die Endamplituden. Für denselben
inneren Endtyp aus einer Zweierkette und einem isolierten Element (e=3)
besitzen zwei lineare Erweiterungen nach dieser lokalen Normierung die
quadratischen Zählgewichte

\[
\frac{16}{245}\ne\frac{2}{45},
\]

während ihre ursprünglichen Gewichte beide 1/3 und deren Quadrate beide 1/9
waren. Die zwei Geburtsrouten unterscheiden sich durch einen Ketten- oder
Antiketten-Zwischenzustand. Die Wirkungsphasen bleiben nach gemeinsamer
Umbenennung gleich; die zusätzliche Normierung verursacht den Unterschied.

Eine nachträgliche Summe über alle natürlichen Beschreibungen kann weiterhin
isomorphieinvariant definiert werden, erhält aber nicht die ursprünglichen
Gewichte. Das ist keine nachgewiesene gravitative Anomalie. Eine solche
Änderung wäre als neues Modell mit eigenen physikalischen Annahmen zu
rechtfertigen, nicht als bloße Normierung der alten Amplitude auszugeben.

## 7. Positive Schnittprodukte bei festem Endhorizont

Für einen fest gewählten endlichen M und positive terminale Gewichte
h_M(P) kann man definieren

\[
h_m^{[M]}(P)=\sum_{J\text{ Ideal}}r(P,P')^2\,h_{m+1}^{[M]}(P').
\]

Dann ist V_m zwischen den entsprechend gewichteten Hilfsprodukten exakt
isometrisch, weil die rechte Seite gerade sein zurückgezogenes Produkt ist.
Die diagonale, feldunabhängige Familie ist eine einfache Positivkontrolle;
ein allgemeines Endprodukt hätte die vollständige Operatorrekursion
M_m=V_m†M_(m+1)V_m. Ein quantenphysikalisches Produkt wird damit nicht ausgewählt.

| Endhorizont M | Gewähltes Endgewicht | h₂(Kette) | h₂(Antikette) |
|---:|---|---:|---:|
| 2 | 1 | 1 | 1 |
| 3 | 1 | 49/36 | 2 |
| 3 | 1 + innere Relationenanzahl | 179/36 | 44/9 |
| 4 | 1 | 15863/7200 | 14879/3600 |

Die Gewichte sind positiv und isomorphieinvariant, unterscheiden sich aber
mit Horizont und Endwahl. 30 endliche Rekursionskontrollen bestätigen die
Identitäten für zwei Horizonte und zwei Endprodukte. Ein einziger
Zustandsnormierungsfaktor kann beispielsweise die unterschiedlichen
Kette-/Antikette-Verhältnisse nicht angleichen.

Die Zeile M=2 ist die definierende Endwahl, kein zurückgezogener Wert aus
einer längeren Entwicklung. Es ist nicht gezeigt, dass es keinen positiven
unendlichen konsistenten Normpfad gibt. Ebenso wenig ist ein solcher Pfad
mit regulatorunabhängigen relativen Normen, labelverträglichen Ereignissen
und klassischer Korrespondenz bereits hergeleitet. Ein gewünschtes
Endprodukt darf nicht stillschweigend als physikalisch unabhängig behandelt
werden, nachdem es passend zur Fortsetzung gewählt wurde.

## 8. Ausgeführte Prüfungen

| Prüfung | Umfang | Ergebnis |
|---|---:|---|
| Natürlich gelabelte innere Ordnungen m=0,…,5 | 408 | Zählfolge 1,1,2,7,40,357 |
| Zulässige Ein-Element-Fortsetzungen | 407 | vollständige kleine Klasse |
| Rationale Wirkungszuwächse | 2 442 | direkter geerbter Rechner stimmt überein |
| Direkte gravitative Endwirkungsvergleiche | 408 | exakt |
| Lineare Erweiterungen gegen Permutationszählung | 408 | exakt |
| Austauschdiamanten unvergleichbarer Geburten | 268 | Zählprodukte gleich |
| Zugehörige Feld-/Phasenprüfungen | 536 | exakt |
| Abschließender Endanker mit zwei Feldprofilen | 816 | exakt |
| Korrigierte natürliche versus beliebige Labelsumme | 6 Sektoren | vollständige Laurentpolynome gleich |
| Kragen-Gegenbeispiele | 8 Fälle plus allgemeine Familie | ΔS_d=1/16 |
| Positive Endprodukt-Rückzüge | 30 | exakt, konditional |

Die beliebig gelabelte Vergleichsroute enumeriert die inneren Ordnungen
unabhängig mit dem geerbten Algorithmus. Die Feldmaße werden bei den
endlichen Wirkungsprüfungen nicht statistisch abgetastet: Es sind rationale
Algebrakontrollen. Der Maßsatz für symmetrische Feldintegrale folgt aus dem
allgemeinen Umbenennungsbeweis. Die gravitativen Laurentpolynome sind
keine physikalische Wahl von κ oder ein Nachweis von 4D-Manifoldlikeness.

Fünf Ergebnisdateien sind isoliert bytegleich reproduzierbar. Plan und
Quelltexte sind gehasht; alle harten Entscheidungen bleiben unter Python -O
aktiv. Die allgemeinen Beweise stehen im Text und sind nicht durch einen
formalen Beweisassistenten geprüft. Der lokale Plan ist keine externe
Präregistrierung oder blinde Vorhersage.

## 9. Entscheidungen und nächste konkrete Forschungsfrage

| Aussage | Entscheidung |
|---|---|
| Vollständige Vergangenheit als hinreichende Darstellung der endlichen Fortsetzung | PASS_EXACT |
| Erhaltung des geerbten Zählmaßes mit 1/e(P) | PASS, unter den deklarierten Invarianzbedingungen |
| Beliebiger fester oberer Lagenkragen genügt für alle zukünftigen Ideale | FAIL |
| Ein gemeinsamer skalarer Normfaktor im natürlichen Zählprodukt | FAIL |
| Lokale Isometrisierung bewahrt die ursprüngliche Amplitude | FAIL |
| Positive Produkte durch endlichen terminalen Rückzug | PASS, abhängig von Endwahl |
| Physikalischer Randzustandsraum, Produkt und unendliche Fortsetzung | HOLD |
| Acht physikalische Audit-Gates | jeweils HOLD |

Der nächste konkrete Test ist nun bestimmter als zuvor: **Besitzt die
vollständige Gedächtnisfortsetzung einen begründeten positiven Normpfad mit
kontrollierter Horizontabhängigkeit, der die ursprünglichen relativen
Amplituden und die Redundanz der Geburtslabels erhält?** Zunächst müssen
Endwahlabhängigkeit, relative Normverhältnisse und die zulässige
Ereignisidentifikation geprüft werden. Ein endlicher Rückzug allein reicht
nicht. Falls der geerbte Ansatz diesen Test nicht trägt, braucht er eine
offen deklarierte physikalische Änderung statt einer versteckten
Schrittnormierung.

Eine Lösung dieses Konsistenzproblems würde noch nicht die klassische
Einstein-Staub-Korrespondenz oder die physikalische Innen-/Außenraum-Naht
beweisen. Neue Bounce-Auswertungen, Singularitätsauflösung und eine
Regularitätsaussage bleiben bis zur jeweiligen eigenen Prüfung offen.

## Quellen und Herkunft

1. D. P. Rideout, R. D. Sorkin, *A Classical Sequential Growth Dynamics for
   Causal Sets*, Phys. Rev. D 61, 024002 (2000),
   [arXiv:gr-qc/9904062v3](https://arxiv.org/abs/gr-qc/9904062v3),
   insbesondere natürliche Labels und diskrete allgemeine Kovarianz.
2. S. Surya, S. Zalel, *A Criterion for Covariance in Complex Sequential Growth
   Models* (2020), [arXiv:2003.11311v1](https://arxiv.org/abs/2003.11311v1).
   Fortsetzung des Quantenmaßes als zusätzliche Bedingung; die dortigen
   speziellen Modelle werden hier nicht mit der BDG-Staubamplitude gleichgesetzt.

Die verwendeten Zähl-, Wirkungs-, Kragen- und Normargumente sind oben
ausgeführt. Sie werden nicht als bereits publizierter physikalischer
Modellschluss ausgegeben. `inputs/provenance.json` enthält die sieben
bytegleich übernommenen Vorgängerquellen und den Main-Commit. Die geerbten
Codekopien enthalten ihre ursprünglichen Zeilenenden; es werden keine
älteren Dateien geändert.
