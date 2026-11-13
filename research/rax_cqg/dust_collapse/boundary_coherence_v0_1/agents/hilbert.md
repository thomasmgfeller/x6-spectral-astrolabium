# Hilbert-Perspektive: unabhängige mathematische Gegenprüfung

KI-Prüfperspektive, keine Aussage einer realen Person. Ergebnis: **Die beschränkte Zwei-R-Studie ist als neues endliches, bedingtes Instrument konsistent. Der physikalische Schluss bleibt HOLD.** Das neue Randexperiment liefert mehr als eine umbenannte Klassenflag-Messung, weil tatsächlich zwei orthogonale terminale Materiezustände konstruiert wurden. Es liefert noch keine geometrische Messgröße.

## Unabhängigkeit und geprüfte Voraussetzungen

`checks/hilbert_audit.py` rekonstruiert aus den erzeugenden Relationen des eingefrorenen Piloten alle sechs Historien, die Intervallgewichte, skalaren Hesse-Matrizen und Gaußmomente. Es verwendet ausschließlich rationale Arithmetik im Körper `Q(i sqrt(6))`; Dowkers Matrizen und dessen symbolische Inversion werden nicht importiert. Auch die Paketnormen werden unabhängig durch rationale Gaußmomente berechnet. Die erhaltenen Faktoren stimmen exakt überein.

Die originalen Dateien bleiben unverändert. Die Hashes des Piloten und der übernommenen Amplitudenboxen stimmen. Der Audit überprüft zusätzlich die neuen Momentintervalle durch exaktes Quadrieren ihrer rationalen Grenzen. Die anschließend propagierten Wahrscheinlichkeiten bleiben von der Richtigkeit der geerbten Amplitudeneinschlüsse abhängig; deren ursprüngliche Quadratur wurde hier nicht erneut bewiesen oder gerechnet.

## Was die kohärente Ergänzung mathematisch ändert

Das klassische Weglassen der Klasse ergibt `sum_c |a_cs|^2`. Der Phasenfaktor `exp(i F_c)` fällt heraus. Ein kohärentes Messinstrument muss dagegen bereits vor der irreversiblen Klassenauslese spezifiziert werden. Für den Diagnoseanalysator gilt

\[
M_{\pm,s}=\frac{\lambda}{\sqrt2}(a_{1s}\pm e^{i\theta}a_{2s}),\qquad
\sum_{\pm,s}M_{\pm,s}^{\dagger}M_{\pm,s}=Q_{\rm old}.
\]

Damit bleiben der alte Gesamterfolg und die alte Failure erhalten. Nur die aufgelösten Ports enthalten den Kreuzterm. Diese Identität gilt auf ganz `E`, nicht nur für die beiden getesteten Basiszustände. Die separaten exakten Identitäten sind die Begründung; ein numerisches Differenzintervall, das Null enthält, ist lediglich ein Konsistenzcheck.

Die direkte Randfusion `C_s=lambda(a_1s+a_2s)` ist ein anderes Instrument. Sie entspricht `sqrt(2)` mal dem Plusport und benötigt eine neue Failure. Wittens Schranke `Q_direct <= 2 Q_old < 0.404 I_E` stimmt für das alte terminale Paket `f0`.

Für nicht beobachtete Umgebungsmarker multipliziert `gamma_s=<e_2s|e_1s>` den Kreuzterm. Die verwendete Gram-Matrix und Phasenorientierung stimmen. Normierte Marker existieren für jedes `|gamma_s|<=1`, und ihre Wahl muss vom Eingabezustand unabhängig sein. Eine anschließende Klassenmessung liefert für alle diese Marker dieselben alten Klassenwahrscheinlichkeiten. Die neuen kohärenten Vorhersagen unterscheiden sich: Die zertifizierten Realteile der Kreuzsummen sind für beide Testzustände negativ. Damit ist die fehlende Identifizierbarkeit von `gamma_s` anhand der alten Instrumentdaten konstruktiv belegt.

Rephasierung `a_cs -> exp(i chi_cs) a_cs` muss durch entsprechende Überlappungs- oder Detektortransformation kompensiert werden. Für festgehaltenes `gamma` lautet der Phasentransport `theta_s -> theta_s + chi_1s - chi_2s`. Ohne diesen Transport ändert sich das gewählte Instrument.

## Zwei konkrete terminale Materie-Records

Die neue, vor ihren Momentwerten fixierte Wahl lautet

\[
f_2=\frac{(q_4+q_5)^2-1}{\sqrt2}f_0.
\]

Der Zustand ist normiert, orthogonal zu `f0`, invariant unter dem Tausch der terminalen Labels und gerade unter globaler skalarer Parität. Die kinematische Gram-Matrix ist `I_2`. Die gewichtete Gram-Matrix ist dagegen

\[
\begin{pmatrix}65&98\sqrt2\\98\sqrt2&799\end{pmatrix}.
\]

Die Unterscheidung ist wesentlich: Kinematische Orthogonalität impliziert keine Orthogonalität in der gewichteten Norm, aus der der Instrumentbound folgt.

Mit `ell=(0,0,0,0,1,1)` und `Q_C=diag(1,1,1,0,1,1)-iH_C` ergibt die Gaußquellenidentität

\[
Z_C(J)=Z_C(0)\exp\left(\tfrac12J^2\ell^TQ_C^{-1}\ell\right)
\]

die exakte Relation

\[
a^{(f_2)}_{cs}=\eta_c a^{(f_0)}_{cs},\quad
\eta_c=\frac{\ell^TQ_C^{-1}\ell-1}{\sqrt2}.
\]

Unabhängig bestätigt:

\[
\eta_1=-\frac{64430531\sqrt2}{771663506}
-i\frac{8175324\sqrt3}{385831753},\qquad
\eta_2=-\frac{539495737\sqrt2}{10449188518}
-i\frac{47339214\sqrt3}{5224594259}.
\]

Alle sechs durch Randintegration gebildeten Schur-Komplemente besitzen einen strikt positiven rationalen Realteil. Die Polynomeinfügung multipliziert den geerbten Abel-Grenzwert; es wird keine neue Determinantenwurzel oder Fresnelphase gewählt. Alle bisherigen Uhren-, Dichte-, Quotienten- und Historiengewichte bleiben erhalten, weil `f2` allein die skalaren terminalen Variablen ändert und die Wirkung keine direkte Skalar-Staub-Kopplung enthält. **Neue Uhrenquadraturen: null.**

Weil `eta1 != eta2` und der geerbte positive-Stratum-Minor nullfrei ist, besitzt die kohärente Eingabe-zu-`(f0,f2)`-Karte auf `E` Rang zwei. Die alten Matrixelemente mit einzigem `f0` allein hätten diesen zweiten Record nicht bestimmt; zusätzlich wurde die bereits deklarierte quadratische Wirkung ausgewertet.

## Norm, Completion und endlicher Geltungsbereich

Das alte Gain `1/256` darf nicht mit seiner alten Vorabgarantie auf beide terminalen Pakete übertragen werden: Der entsprechende separate Majorant wäre `2.6779833984375`. Ein Majorant über eins beweist **keine** tatsächliche Nichtkontraktivität; er liefert nur keine Garantie.

Das deshalb vor den neuen Antwortwerten fixierte `lambda_R=1/1024` ergibt für die direkte kohärente Klassenfusion

\[
Q_R\le
\frac{2\cdot4(3/5)^2(2257/16)(65+799)}{1024^2}I_E
=\frac{548451}{1638400}I_E
=0.3347479248046875\,I_E.
\]

Folglich ist `I_E-Q_R` strikt positiv. `M_F=(I_E-Q_R)^(1/2)` mit eigenem Failure-Flag vervollständigt die CP-Karte für jeden Eingabezustand auf `E`. Weder ein globales `K†K` noch ein physikalisches Historien-Skalarprodukt wird hierfür vorausgesetzt.

Die orthogonalen terminalen Projektoren `|f0><f0|` und `|f2><f2|` sind kinematische Materieprojektoren. Das vollständige Instrument mit Innerstratum und Failure wird auf `E` separat konstruiert; daraus folgt keine bereits hergeleitete physikalische Endrand-PVM.

## Zertifizierter begrenzter Befund

Roots unabhängige rationale Intervallpropagation liefert für die direkt kohärente Zwei-R-Karte:

| Größe | Einschluss |
|---|---|
| `P(f2 | success,g0)` | `[0.01588643892758915, 0.01588644174367168]` |
| `P(f2 | success,gplus)` | `[0.01588896120528318, 0.01588896281716421]` |
| Differenz `gplus-g0` | `[2.51946161151096e-6, 2.52388957504805e-6]` |

Der Unterschied ist innerhalb der übernommenen Fehlerannahmen nullfrei. Er ist eine bedingte Materiemoden-Wahrscheinlichkeit. Der unbedingte Erfolg liegt bei ungefähr `3.59e-10` beziehungsweise `9.35e-10`; die hohe Failure-Wahrscheinlichkeit muss zusammen mit bedingten Zahlen berichtet werden. Gain und Erfolgsrate sind Eigenschaften des deklarierten Hilfsinstruments, kein kalibriertes Laborprotokoll.

Auch das dephasierte Zwei-R-Instrument besitzt bereits einen Präparationskontrast von ungefähr `2.339e-6`. Ein nullfreier Präparationskontrast allein ist daher kein Interferenznachweis. Der getrennte Gamma-Vergleich verändert die terminalen Verteilungen nullfrei. Entfernt man außerdem nur die `F4`-Phasen als kontrafaktische Wirkungskontrolle, ändert sich der Präparationskontrast um `[-1.074949651e-6,-1.066533590e-6]`. Der exakte rationale Taylor-Einschluss dieser Kontrolle und die Intervallrechnung stimmen überein. Das belegt die Phasenabhängigkeit innerhalb des bedingten Instruments, keine reale Variation der Gravitation im Labor.

## Freigabe- und Blocker-Ledger

| Punkt | Urteil | Grenze |
|---|---|---|
| Klassische Grobkörnung versus kohärente Fusion | PASS | Kohärenz ist neue Instrumentannahme. |
| Gamma-Modell, Phasenkovarianz, vollständige Effekte auf `E` | PASS | Alte Daten identifizieren Gamma nicht. |
| Zwei normierte invariante terminale Pakete und exakte Momente | PASS | Materie-, keine Geometriemoden. |
| Neue Gain-/Failure-Konstruktion auf ganz `E` | PASS | Alte Failure wird nicht übertragen. |
| Fehlerfortpflanzung und nullfreier Zwei-R-Kontrast | PASS, bedingt | Geerbte Amplitudenboxen; keine neue Integrationszertifizierung. |
| Physische Umgebung, Phasenreferenz, Historienmaß | HOLD | Gemeinsame Randordnung allein reicht nicht. |
| Geometrischer Endrand-Detektor oder Gravitations-Backreaction | HOLD | Keine Masse-, Uhr-, Radius- oder Krümmungskalibrierung. |

Der alte fixe terminale Projektor hat Rang eins **im terminalen Raum**; die gesamte alte Klassen-/Stratum-Instrumentkarte hat bereits Rang zwei auf `E`. Die Rang-eins-Aussage ist daher weder eine globale Aussage über das alte Instrument noch ein Unmöglichkeitssatz für erweiterte Theorien.

Weiterarbeit ist sinnvoll, wenn als nächster unabhängiger Eingang ein gemeinsamer physischer Detektor/Umgebungszustand und eine konkrete Messgröße begründet werden. Zusätzliche Phase-, Gain- oder Paketoptimierungen ersetzen diesen Eingang nicht. Die klaren Stopkriterien sind: kein fitabhängiges Gamma, keine Übertragung einer alten Failure auf neue Akzeptanzoperatoren, keine Interpretation der Hermite-Labels als Radius/Krümmung und kein physikalischer Backreaction-Schluss aus dem bedingten endlichen Kontrast.
