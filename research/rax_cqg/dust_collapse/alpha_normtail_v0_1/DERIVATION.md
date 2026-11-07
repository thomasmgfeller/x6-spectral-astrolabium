# CST-DUST: α-abhängige Normrestschranke v0.1

7. November 2026. Ausgangsbasis: Main nach PR 257,
`0067da907da4ea8df5b625ea9f8f99ce1527e9ed`.
Acht Quellen sind in `inputs/` byteidentisch mit Git-Blob-Identitäten gepinnt.

## 1. Präzise Fragestellung und Geltungsbereich

Die kontinuierliche Materiephase ist im Referenzmodell bis n=4 integriert.
Die Normmassen sind bis n=6 exakt bekannt. Der Vier-Element-Stand benutzte
für den restlichen Normierungsbeitrag nur

\[
 \Delta_K^{old}=\frac{h^{K+1}}{(K+1)!}\frac1{1-h/(K+2)},\qquad h<K+2.
\]

Diese Grenze verwirft die zusätzliche Unterdrückung durch α>1 und die
bereits exakt gezählten Ordnungen. Hier werden beide Informationen genutzt.
Das Referenzmaß, die kontinuierlichen Materieintegrale, die Kopplungen,
die Auslese und die physikalischen Aussagen bleiben unverändert.

Die Produktion bleibt bei K=6 und integriert weiterhin nur n≤4.
Die vollständige Enumeration bis n=7 dient als unabhängige endliche
Kontrolle des Beweises, nicht als neuer Feldphasensektor oder als Erhöhung
des Produktions-Normierungscutoffs. Die tatsächlich bekannte n=7-Normmasse
wird im Produktionsrest weiterhin konservativ mit eingeschlossen.

Der lokale Plan wurde nach symbolischer Beweisplanung, aber vor den neuen
numerischen Restwerten und der Implementierung eingefroren. Das ist keine
externe Präregistrierung oder blinde Vorhersage.

## 2. Kombinatorisches Lemma

N_n zählt die natürlich durch die monotone Uhr beschrifteten Ordnungen
auf n neuen Elementen. Der fest vorgegebene Anfangsanker wird nicht mitgezählt.
N_0=1. Ein neues letztes Element hat als Vergangenheit ein Ordnungsideal
seiner n Vorgänger. Es gibt höchstens 2^n Teilmengen, also

\[
 N_{n+1}=\sum_{p\in\mathcal P_n}|\mathcal I(p)|\le 2^n N_n.
\]

Die Gleichheit folgt aus einer Bijektion: Jede neue natürliche Ordnung
besitzt genau ein Präfix p und genau ein letztes Vergangenheitideal.
Transitivität ist genau die Forderung, dass diese Vergangenheit ein Ideal
ist. Damit gilt für jedes n≥K:

\[
 N_n\le N_K\,2^{\binom n2-\binom K2},\qquad
 N_n\le 2^{\binom n2}.
\]

Die zweite Ungleichung kann auch direkt durch Einbettung in die Menge aller
oberen Dreiecksrelationen gewonnen werden. Es werden keine unbeschrifteten
Isomorphieklassen gleichgewichtet anstelle der natürlichen Ordnungen verwendet.

Zwei vollständige Enumerationswege, Rekursion über Ideale und ein unabhängiger
Transitivitätsfilter auf Dreiecksrelationen, liefern

| n | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| N_n | 1 | 1 | 2 | 7 | 40 | 357 | 4824 | 96428 |

Diese Zahlen werden berechnet, nicht aus einer externen Zähltabelle übernommen.
Die endlichen Vergleiche kontrollieren die Implementierung; die Bijektion
und die Schranke auf alle Teilmengen tragen den unendlichen Beweis.

## 3. α-abhängiger Satz für den Normrest

Die im Referenzmodell geerbte Sektormasse ist

\[
 c_n=N_n\frac{h^n}{n!}\,2^{-\alpha\binom n2},\qquad h\ge0,\quad\alpha\ge1.
\]

Weder Materie- noch Gravitationsphasen ändern diese Normmassen. Aus dem Lemma
folgt ohne Division durch möglicherweise verschwindende c_n:

\[
 c_{n+1}\le r_n c_n,\qquad
 r_n=\frac h{n+1}\,2^{-(\alpha-1)n}.
\]

Der Faktor α-1 ist wesentlich: Das maximale Verzweigungswachstum 2^n
kompensiert genau einen der α-Faktoren der Gewichtung. Für α≥1 ist r_n
monoton fallend. Setze q_K=r_{K+1}. Falls q_K<1, gilt daher

\[
 \sum_{n>K}c_n\le
 \frac{c_K r_K}{1-q_K}
 =\frac{N_K}{2^{\binom K2}}
 \frac{h^{K+1}2^{-(\alpha-1)\binom{K+1}2}}
      {(K+1)!\,[1-h\,2^{-(\alpha-1)(K+1)}/(K+2)]}
 =:\Delta_K^{anch}.
\]

Beweis: Der erste ausgelassene Beitrag ist höchstens c_K r_K.
Alle nachfolgenden Quotienten sind höchstens q_K; die positiven Beiträge
werden durch eine geometrische Reihe dominiert. Deren Summe ist
`first/(1-q_K)`. Die elementare endliche Summenidentität ist beispielsweise
in [NIST DLMF 1.2.11](https://dlmf.nist.gov/1.2.E11) dokumentiert; ihr Grenzwert
für |q_K|<1 liefert den Nenner. Das kombinatorische Lemma und seine Anwendung
auf dieses Referenzmaß werden hier vollständig hergeleitet.

Ohne den exakten Präfixzähler ergibt sich die universelle α-Grenze
\(\Delta_K^{univ}\) durch Ersetzen von `N_K/2^(K choose 2)` durch eins.
Für den gemeinsamen Geltungsbereich h<K+2 folgt

\[
 0\le\Delta_K^{anch}\le\Delta_K^{univ}\le\Delta_K^{old}.
\]

Bei α=1 ist nur der kombinatorische Gewinn wirksam. Für K=6 lautet sein
Faktor exakt `4824/32768 = 603/4096`, also eine Reduktion der Normrestschranke
um `3493/4096 = 85,2783203125 %`. Bei α=2 kommt im ersten ausgelassenen
Term zusätzlich `2^(-21)` hinzu; auch der geometrische Nenner verbessert sich.

Der Satz gilt für reelle α≥1. Die nachrechenbare Implementierung verwendet
nur ganzzahlige α≥1, damit alle Resultate ohne Gleitkomma exakt rational sind.
Die Produktionswerte sind α=1,2. α<1 ist von diesem Zertifikat nicht abgedeckt;
es wird daraus keine Divergenzaussage für alle α<1 abgeleitet. Bei q_K≥1
liefert die verwendete geometrische Formel keine gültige endliche Grenze
und muss zurückgewiesen werden. Für α≥1 existiert zu jedem endlichen h ein
hinreichend großer Cutoff mit q_K<1; es folgt keine Aussage über h→∞.

## 4. Übertragung auf die bestehenden Ausleseintervalle

Unverändert bleiben `Z4=sum_(0..4)c_n`, `Z6=sum_(0..6)c_n`, die eingeschlossenen
Amplituden t_n mit Fehler ε_n und die Sichtbarkeitsintervalle [v_n^-,v_n^+].
Mit der neuen Grenze gelten

\[
 Z_{max}=Z_6+\Delta_6^{anch},\quad
 R_{max}=Z_6-Z_4+\Delta_6^{anch},\quad p_{max}=R_{max}/Z_{max}.
\]

`Z6-Z4` ist die exakte Normmasse der weiterhin unbekannten Feldphasensektoren
n=5,6. Sie darf nicht mit dem Normrest für n>6 verwechselt oder entfernt werden.
`p_max` ist eine obere Schranke, keine gemessene tatsächliche Restwahrscheinlichkeit.

Setze S_±=sum_(n=0..4)c_n v_n^±. Für den Zahlkanal bleibt die geerbte Formel

\[
 P_{count}\in[S_-/Z_{max},\ \min(1,(S_++R_{max})/Z_{max})].
\]

Monotonie zeigt die Verbesserung: Die Untergrenze steigt beim Absenken von
Zmax. Die Obergrenze ist `1-(Z4-S_+)/Zmax`, mit `S_+≤Z4`, und fällt daher.
Das folgt auch direkt aus einem unbekannten Restbeitrag zwischen null und
der jeweiligen Restnorm. Alle 36 neuen Intervalle werden zusätzlich exakt
auf Einschluss in ihre Vorgänger geprüft.

Für die kohärente Summe ist die Änderung gegenüber der normierten n≤4-Summe
im komplexen Absolutwert höchstens `2*p_max`, da sowohl der bekannte als auch
der unbekannte normierte Summand Betrag höchstens eins besitzen. Mit

\[
 t=\frac{\sum_{n=0}^4c_n t_n}{Z_4},\qquad
 \epsilon=\frac{\sum_{n=0}^4c_n\epsilon_n}{Z_4}+2p_{max}
\]

folgt ein Sichtbarkeitsfehler von höchstens `2ε+ε²` um |t|². Bei Zmax<2
bleibt die Vakuum-Untergrenze `(2/Zmax-1)^2` gültig. Rohintervall und Schnitt
mit der gültigen Vorgängergrenze werden getrennt gespeichert. Beide
Einschlussprüfungen bestehen in allen 36 Fällen. Bei g=μ=0 bleibt das Ergebnis
exakt eins. Die 180 bedingten Ausleseintervalle für n=0,...,4 verbessern sich
ebenfalls; ihr positiver Nenner ist durch den Vakuumbeitrag gesichert.

## 5. Resultate: Normrest und gesamter Phasenrest trennen

| h | α | alte Normrestgrenze, ungefähr | neue Normrestgrenze, ungefähr | Reduktion der gesamten Phasenrest-Gewichtsschranke |
|---|---:|---:|---:|---:|
| 1/4 | 1 | 1,25008e-8 | 1,84033e-9 | 0,36765 % |
| 1/4 | 2 | 1,25008e-8 | 8,50321e-16 | 81,84897 % |
| 1/2 | 1 | 1,65344e-6 | 2,43414e-7 | 1,47425 % |
| 1/2 | 2 | 1,65344e-6 | 1,08868e-13 | 94,90531 % |

Die dezimalen Zahlen hier sind Zusammenfassungen; maßgeblich sind die exakten
rationalen Werte in `results/`. Bei α=2 sinkt die Normrestschranke allein um
mehr als 99,99999 %, aber die gesamte Phasenrestschranke nicht in diesem
Umfang: Die unbekannten n=5,6-Phasen bleiben enthalten.

Nach der Korrektur stammen je nach Parameterfall etwa 96,35 bis 99,95 % der
verbleibenden oberen Restmasse aus der exakt bekannten n=5-Normmasse. Dies
ist eine Aussage über die konservative Unsicherheitsbilanz, keine gemessene
Elementzahlverteilung. Der quantitative Engpass liegt nun im unbekannten
n=5-Feldintegral. Vor dessen Auswertung ist ein neues Kosten-/Fehlerbudget
erforderlich. Weitere Normrestverschärfung ist möglich, verspricht hier aber
deutlich weniger Gewinn als zuvor.

## 6. Kontrollen, Nachrechnung und Grenze

Der eingefrorene Kontrollplan umfasst 168 rationale Parameter-/Cutoff-Fälle:
157 liegen im Geltungsbereich, 11 mit q_K≥1 werden zurückgewiesen. Insgesamt
7536 Majorantenschritte prüfen Rekurrenz, monotone Quotienten und geometrische
Domination. Die positive, tatsächlich enumerierte Restmasse bis n=7 liegt
in allen 157 gültigen Fällen unter der analytischen Grenze.

Zwei numerische Negativkontrollen sind besonders wichtig: Ersetzt man im
Verzweigungsquotienten α-1 fälschlich durch α, oder lässt man den Faktor N6
weg, fällt die vermeintliche Grenze im gewählten Kontrollfall bereits unter
die exakt gezählte n=7-Masse. Beide Varianten werden zurückgewiesen.
Zusätzlich werden α<1, negatives h, negativer Cutoff und q_K=1 abgewiesen.

Der isolierte Replay erzeugt fünf neue Ergebnisdateien aus den acht gepinnten
Quellen, dem Plan und dem neuen Python-Code bytegleich. Er benutzt keine
neuen Ergebnis-Caches und führt keine Feldintegration durch. Endliche Tests
ersetzen weder den obigen unendlichen Beweis noch externe Replikation oder
eine formale Beweisassistenzprüfung.

**Alle acht physikalischen Gates bleiben HOLD:** MODEL, CURRENT,
CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION.
Das Dichtemaß, der kohärente Zugriff auf Historien und die Endrandwahl bleiben
physikalisch unbegründete Referenzannahmen. Keine vollständige 4D-CST-Dynamik,
Rückwirkung, Singularitätsauflösung, Bounce oder Junction werden hergeleitet.

Quellen: [PR 257](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/257),
die acht gepinnten Dateien mit Herkunft in `inputs/provenance.json`,
[NIST DLMF 1.2.11](https://dlmf.nist.gov/1.2.E11) für die geometrische
Summenidentität. Die aktuelle Aussage ist eine neue Schranke innerhalb
des erklärten Referenzmodells, keine behauptete neue physikalische Theorie.
