# Physisches Gate: Quellen, orientierte Uhr und Geometrie

**Ausgeführt, Ergebnis HOLD:** Der gemeinsame kohärente Detektor und zwei skalare Endrandrecords lassen sich als endliches Quantenhilfsmodell prüfen. Daraus entsteht noch kein physischer Zwei-Quellen-Geometrievergleich. Die exakten Hindernisse und die offenen Kalibrierungsfragen wurden getrennt. Es wurden keine neuen Wirkungintegrale, physischen Messpunkte oder GitHub-Änderungen erzeugt. „Einstein“ bezeichnet die Prüfperspektive eines KI-Agenten; kein realer Wissenschaftler hat mitgewirkt.

Reproduktion: `python boundary_coherence_v0_1/checks/physical_gate.py`.
Maschinenlesbares Ergebnis: `checks/physical_gate.json`. Der Prüfer rekonstruiert alle sechs Historien selbst aus `sources/pilot.json` und prüft den unveränderten SHA256-Vertrag. Laufzeit im ausgeführten Test: ungefähr eine Sekunde.

## 1. Quellen- und Stromprüfung tatsächlich neu ausgeführt

Aus derselben Originalwirkung folgt

\[
S_d=-\frac12\sum_j r_j C_j,\qquad
C_j=1+\frac\beta2\sum_{i\prec j}b_{ij}(T_j-T_i)^2,
\qquad \beta=\frac4{\sqrt6}>0.
\]

In jeder der sechs rekonstruierten Historien besitzen die beiden A-Ereignisse genau den Vorgänger 0, jeweils mit Linkkoeffizient +1. Differentiation der **gesamten** Wirkung liefert zwölf geprüfte Identitäten

\[
-2\partial_{r_i}S=C_i=1+\frac\beta2(T_i-T_0)^2\geq1,
\qquad i=1,2.
\]

Damit ist eine frei variierte positive **stationäre innere** A-Dichte ausgeschlossen: Ihre Gleichung wäre \(C_i=0\). Dieser begrenzte Satz erklärt nicht sämtliche Quantenrandzustände für unzulässig. Die deklarierten fixierten Randkoordinaten und off-shell integrierten Pakete \(g_0,g_+\) bleiben kinematisch verwendbar. Für sie sind eine physische Constraint-Paarung, ein physisches Skalarprodukt und eine gemeinsame Massen-/Quellenkalibrierung aber weiterhin nicht hergeleitet. Off-shell-Sein allein ist kein Unzulässigkeitsbeweis.

Der Originalwirkungsstrom ist

\[
J_{ij}=\frac\beta2r_jb_{ij}(T_j-T_i),\qquad
\partial_{T_z}S=\sum_{z\prec j}J_{zj}-\sum_{i\prec z}J_{iz}.
\]

Der Prüfer bestätigt 36 Ableitungs-/Divergenzidentitäten, sechs algebraische Identitäten \(\sum_z\partial_{T_z}S=0\) und 68 nichttriviale Kantenparitäten. Die Summenidentität ist eine Eigenschaft der Wirkung; sie behauptet keine verschiebungsinvariante Integrationsdomäne für den begrenzten Uhrwürfel.

Die vollständige Wirkung ist unter simultaner Reflexion aller Uhren gerade, der einzelne Strom ungerade:

\[
S(-T)=S(T),\qquad J_{ij}(-T)=-J_{ij}(T).
\]

Maße, ursprüngliche Uhrpakete und alle Dichteevents sind reflexionsinvariant. Wittens T-unabhängige Klassenrekombination und Dowkers ausschließlich q-abhängige Endpakete erhalten diese Eigenschaft. **Jede einzelne Strominsertion und jede orientierte Schnittstrominsertion in die betreffenden Amplituden ist deshalb exakt null.** Dies gilt für jeden positiven Abelregulator und in einem existierenden gepaarten Abelgrenzwert. Eine Linearkombination solcher Nullamplituden bleibt null, auch mit verschiedenen Gravitationsphasen.

Der Satz ist kein physischer Stromerwartungswert, keine positive Wahrscheinlichkeit, keine Messung „Masse null“ und kein Ausschluss gerader Zweistromkorrelationen. Eine gegenüber dem alten Modell kohärente, unmarkierte Klassensumme kann ein korrektes deklariertes Quantenmodell sein; die physische Kalibrierung ist eine zusätzliche Frage.

## 2. Orientierte Quantenranduhr untersucht: möglicher Zustand, keine hergeleitete Quelle

Ein hartes Wegschneiden einer Uhrhälfte ist nicht nötig, um die Reflexion kinematisch zu brechen. Aus den vorhandenen Randuhren lässt sich die relative, A-permutationsinvariante Variable

\[
\chi=\frac{T_1+T_2}{2}-T_0\in[-2,2]
\]

bilden. Sie ist unter einer gemeinsamen algebraischen Uhrverschiebung invariant. Für das ursprüngliche Produktmaß gilt exakt
\(\langle\chi\rangle=\langle\chi^3\rangle=0\) und \(\langle\chi^2\rangle=1/2\).
Die vollständig analytisch geprüfte Familie

\[
h_\eta(T)=\frac{1+\eta\chi/2}{\sqrt{1+\eta^2/8}},
\qquad -1<\eta<1,
\]

hat Norm eins, behält den ganzen ursprünglichen Uhrwürfel als Träger und erfüllt

\[
\langle\chi\rangle_{|h_\eta|^2}
=\frac{\eta}{2(1+\eta^2/8)}.
\]

Gemeinsame Multiplikation beider Eingänge mit \(h_\eta\) erhält ihre Orthogonalität durch disjunkte Dichtestrata. Die gewichtete skalare Eingangsnorm bleibt ebenfalls unverändert. Die Auswahl ist somit als Randzustand mathematisch möglich, ohne die Originalwirkung oder die Uhrmaße zu ändern.

**Status: OUTSIDE_FROZEN_CONTRACT, nicht übernommen.** Die konstanten Uhrpakete des eingefrorenen Experiments würden geändert. Es wurde kein \(\eta\) ausgewählt, optimiert oder numerisch integriert. Die Reflexion bildet \(\eta\) auf \(-\eta\) ab; die symmetrische Wirkung wählt kein Vorzeichen aus. Ein konkreter gerichteter Zustand kann physisch vorgegeben werden, benötigt dafür aber eine begründete Präparation. Die Konstruktion allein liefert weder Eigenzeit noch einen positiven Staubstrom, Masse oder eine physische Constraint-Paarung.

Auch ein nichtverschwindender Wirkungsstrom wurde **nicht** behauptet. Für eine Strominsertion folgt lediglich die exakte Zerlegung

\[
\mathcal A_J[h_\eta g]
=\frac{\eta}{2\sqrt{1+\eta^2/8}}
\mathcal A_{J\chi}[g].
\]

Der Integrand rechts ist unter Reflexion gerade; er kann trotzdem aus anderen Gründen verschwinden. Damit ist die mathematische Möglichkeit einer gerichteten Randpräparation gezeigt, und zugleich die Lücke zur physisch ausgewählten Quelle präzisiert. Innerhalb des eingefrorenen Vertrags bleibt der Nullsatz aus Abschnitt 1 bestehen.

## 3. Endrandgeometrie und alternativer positiver Quellenpatch

Die sechs rekonstruierten Historien haben denselben induzierten äußeren Rand und auf \(R=\{4,5\}\) jeweils dieselbe Zweier-Antikette. Deshalb ist **jede ausschließlich von der intrinsischen R-Ordnung abhängige Funktion** auf diesem Ensemble konstant. Dies ist ein begrenzter exakter Ausschluss einer solchen Geometrieauslese, kein Ausschluss von Geometrieobservablen der vollständigen Historie oder künftig hergeleiteten Randobservablen mit zusätzlichen Daten.

Die Enddichten bleiben in beiden skalaren Records atomar. Der Prüfer bestätigt zwölf Identitäten \(\partial_{T_4}S=\partial_{T_5}S=0\) nach \(r_4=r_5=0\). Terminale Uhrintegrale bleiben somit eins. Dowkers \(f_0/f_2\)-Paar ist eine echte neue kinematische **Materieauslese** am Endrand. Ohne zusätzlichen Adapter ist sie weder Arealradius, räumliches Volumen, Krümmung noch Energie. Der mit identischen beiden Eingängen verwendete R-Detektor hat laut seinem vor der Momentrechnung fixierten Vertrag einen neu berechneten Gain; der hier exakt nachgerechnete Majorant ist

\[
\frac{2\cdot4(3/5)^2(2257/16)(65+799)}{1024^2}
=\frac{548451}{1638400}<1.
\]

Dies prüft die algebraische Majorantenrechnung. Die Herleitung seiner Eingangs-/Ausgangsnormen und die neuen Momentamplituden liegen beim separaten Dowker-/Hilbert-Audit.

Der vorhandene positive kanonische Sechserpatch wurde als **getrennte Alternative** untersucht. Für seine eigene Ordnung und Uhrnormierung wurden \(C_4=C_5=0\), \(q_t=0\), \(q_u=Q\), beide vollständigen Schnittflüsse \(-Q\) und die legale Ladungsvariation \(Q_2/Q_1=16\) frisch symbolisch nachgerechnet. Ordnung und sämtliche Uhren bleiben bei dieser Variation gleich. Die alten rationalen Intervallzertifikate und ihre auf acht recorderhaltende konvexe Partitionen begrenzten Positivitätsausschlüsse werden ausdrücklich als vorhandene Evidenz wiederverwendet, nicht als neuer vollständiger Intervalllauf ausgegeben.

Diese Alternative liefert damit eine konkrete positive globale Ladung. Der negative vollständige Schnittfluss neben positivem \(J_{tu}\) verhindert jedoch die bereits geprüfte direkte lokale positive Stromidentifikation durch eine gemeinsame Orientierung; Betragnehmen zerstört die Innenbilanz. Auch liefert jede gleiche Zuordnung \(R_{\rm areal}=F(C,T)\), \(\tau=G(C,T)\) identische Kurven für \(Q\) und \(16Q\). Unter der **zusätzlich hypothetischen** Identifikation \(M=cQ\) reproduziert diese eingeschränkte Adapterklasse nicht die vorgegebene klassische nichttriviale Kollapsantwort mit Steigungsverhältnis vier. Andere hergeleitete Geometrieobservablen bleiben offen.

Die positive Ladung dieses anders normierten, anders präparierten Patches wird nicht in den Quantenpilot transplantiert. Sie löst dessen Quellen-, Uhr- oder Geometriekalibrierung nicht.

## 4. Ausgeführte Entscheidung zum Zwei-Quellen-Geometrievergleich

| Voraussetzung | Resultat dieses Prüflaufs | Geltungsbereich |
|---|---|---|
| Gleiches Instrument für beide Eingänge | Kinematisch deklariert; gemeinsame Majorante kleiner eins | Physische Detektorrealisierung und kohärente Paarung weiter bedingt |
| Zwei physisch zulässige, kalibrierte Quellen | Nicht hergeleitet | Frei stationäre positive A-Quelle ausgeschlossen; allgemeine Quantenrandquellen nicht ausgeschlossen |
| Relationale physische Uhr | Nicht hergeleitet | Relative Variable und unübernommene gerichtete Familie existieren; eingefrorene Ein-Strom-Insertionen exakt null |
| Geometrische Endobservable | Nicht hergeleitet | Intrinsische R-Ordnung konstant; zwei skalare Materierecords definiert |
| Skala und Verfeinerung | Nicht definiert | N=6, keine unabhängige räumliche Skala oder Verfeinerungsfamilie |
| Globaler Außenraum | Nicht definiert | Kein äußerer Anschluss im Vertrag |

Der Schritt wurde ausgeführt: **Ein physischer Zwei-Quellen-Geometrievergleich ist mit den vorhandenen kalibrierten Größen noch nicht ausführbar.** Es gibt null neue physische CST-Datenpunkte. Die endliche kohärente Instrumentdiagnose und der Vergleich zweier terminaler Materieausgänge bleiben ausführbare, klar begrenzte Ergebnisse. Sie sollten als solche abgeschlossen werden.

Die minimale nächste physische Arbeit ist ein gemeinsam begründeter Anschluss von Quellzustand, relativer Uhr und geometrischer Auslese innerhalb derselben Theorie. Eine bloße Wahl von \(\eta\), ein nachträglicher massenabhängiger Radius oder die Übernahme klassischer Zielkurven erfüllt diese Anforderung nicht. Solange dieser Anschluss fehlt, werden Historienzahl, Quadratur und Präzision nicht erhöht. Ein neues Modell müsste seine geänderten Randbedingungen und den beanspruchten Geltungsbereich vor der Auswertung erklären; für einen Kollapsanspruch kommen unabhängige Skala/Verfeinerung und ein geeigneter äußerer Anschluss hinzu.

Direkter Abgleich: Witten bestätigte die unveränderte Uhrparität und hält seine umgebungsabhängige Kohärenzannahme getrennt von den fehlenden physischen Adaptern. Dowker bestätigte die Trennung von Materie- und Geometrierecord, Hilberts unabhängiger Audit dieselbe Reichweite. Die exakten Aussagen stammen aus dem Originalvertrag und den hier nachgerechneten Identitäten. Quellpfade samt SHA256 stehen im maschinenlesbaren Ergebnis. Die unveränderten kanonischen Vorlagen liegen paketintern als `sources/prior_einstein_check.py`, `sources/prior_einstein_contract.json` und `sources/prior_einstein_calibration.json`; ihre Hashes sind im neuen Prüfer fest hinterlegt. Der alte Prüfer ist eine Provenienzkopie und ohne sein ursprüngliches Quellenpaket kein selbständiges Reproduktionsziel. Der neue `checks/physical_gate.py` benötigt ausschließlich Dateien dieses Pakets; er rechnet die genannten Identitäten selbst nach und verwendet nur die ausdrücklich ausgewiesenen alten Intervallzertifikate weiter.
