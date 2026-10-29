# Unabhängige Transferprüfung v0.14: Zulassungsentscheidung

**Entscheidung: Das konkrete Transfermodell v0.13 wird in seinem jetzigen
Stand nicht zu einem frischen Bestätigungsensemble zugelassen.**
`REJECTED_FOR_CONFIRMATORY_RUN`; Gesamtstatus `METHOD_HOLD`, G1 `HOLD`.

Die verlangte Vorprüfung ist abgeschlossen. Ein unabhängiger Datentest ist
**nicht durchgeführt**: Die vorgeschaltete Methodenkontrolle scheitert.
Das ist eine begründete Zurückweisung der Testfreigabe, keine statistische
Widerlegung der gemeinsamen Momentenformel durch neue Daten.
Neue Parameter, Stichprobengröße, Fehlerbudgets, Signifikanzniveau,
Powerziel, Ressourcenlimits, Seeds und statistische Abbruchregeln bleiben
unfestgelegt. Es gibt **null neue Wolken und null neue Zufallsaufrufe**.

## 1. Welches Modell wird beurteilt?

Basis ist der veröffentlichte v0.13-Commit
`1995b37260806841a9b084703e5636793fa7e5a0` aus
[PR #145](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/145).
Seine eigene GitHub-Reproduktionsprüfung
[40770345822](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/40770345822)
ist bestanden. Die lokalen Kontrollnachweise umfassen 27 Tests und
105 Intervallvergleiche. Ein bestandener Softwarelauf ist jedoch keine
unabhängige Bestätigung der ursprünglichen Detektorvorhersage.

Beurteilt werden die unveränderten Modelle mit lokalem H1- und nichtlokalem
PU-H1-Adapter, getrennt voneinander. Es gelten weiterhin

\[
 \Omega_4=\{(t,x):|t|+|x|<4\},\quad
 \rho=3/\pi,\quad \mathbb EN=512,\quad \epsilon=1/16,\quad m=1.
\]

Quelle, History bis t=-1, Detektorball mit Zentrum (0,0,3/2) und Radius 1/2
sowie die vollständigen Fenster [3/4,1] und [1,5/4] bleiben unverändert.
Beide komplexen Antworten werden durch die bisherige Feldskala A/e
normiert. Die vierdimensionale Poisson-Intervallkontrolle und der
Oszillator sind Methodenprüfungen; sie werden nicht an die Stelle dieses
Quell-/Detektormodells gesetzt.

## 2. Methodenkontrolle vor jedem neuen Testdesign

| Voraussetzung | Lokales H1 | Nichtlokales PU-H1 |
|---|---|---|
| Reproduzierte Kontrollmodelle | bestanden | bestanden |
| Abbildung auf allen Ensemblefällen | definiert | nicht vollständig definiert |
| Ausgewertete gemeinsame Originalmomente | fehlen | fehlen |
| Vierte Momente oder geeignete Schwanzgrenzen | grobe Schranke bewiesen | nicht zertifiziert |
| Ensembleweite numerische Fehlerbilanz | fehlt | fehlt |
| Abgleich von Vorhersage- und Abtastgesetz | fehlt | fehlt |
| Zulassung zum Bestätigungslauf | zurückgewiesen | zurückgewiesen |

Die ausgeführten Kontrollmodelle belegen die gemeinsame Behandlung von
Überlappungen, Palm-Einfügungen, Operatorzufälligkeit und Historykorrelation.
Es fehlen dagegen Zahlen mit Fehlergrenzen für den Mittelwert und die
vollständigen Kovarianz-/Relationsmatrizen des ursprünglichen Detektors.
Die bloße Pfadmomentenformel und kleine Abschneidereste ersetzen deren
räumlich-zeitliche Integrale nicht.

Der nichtlokale Adapter ist schon auf Wolken mit weniger als vier
History-Knoten nicht definiert. Außerdem fehlen Schranken für nahezu
entartete Geometrien. Eine Behandlung dieser Fälle würde das Modell
vervollständigen oder ändern und muss vor einer erneuten Vorprüfung
festgelegt werden. Verwerfen, Nachziehen, Nullsetzen oder stilles
Konditionieren ist keine zulässige Fehlerbehandlung für das unveränderte
unbedingte Ensemble.

Eine Rechnung auf gespeicherten dyadischen Koordinaten kontrolliert deren
exakte Geometrie. Sie zertifiziert nicht automatisch den Abstand zum
idealen kontinuierlichen Poisson-Gesetz. Vor einem späteren Test muss die
gemeinsame Zielverteilung eindeutig sein: mit begrenztem Rundungs-/Sampler-
Beitrag oder ausdrücklich auf das tatsächlich deklarierte diskrete Gesetz
bezogenen Vorhersagen. Die übliche Annahme unabhängiger Pseudozufallsströme
ist davon zu unterscheiden; sie wird nicht als mathematischer Beweis
physischer Zufälligkeit ausgegeben.

## 3. Getrennte Entscheidungen

**Fluktuationen:** `NOT_TESTED_METHOD_GATE_FAILED`. Es gibt keinen neuen
p-Wert und keinen statistischen PASS/REJECT-Befund für die ursprünglichen
Momentenvorhersagen. Das Modell ist für diesen Test noch nicht auswertbar.

**Makroskopischer Ensemble-Mittelwert:** `NOT_ESTABLISHED`. Ob der mittlere
Originaldetektor innerhalb einer noch festzulegenden Populationsmarge mit
der Kontinuumsantwort übereinstimmt, ist nicht nachgewiesen und hier nicht
statistisch verworfen.

**Makroskopische Einzelrealisierungen beim lokalen Adapter:** Eine
fast-sichere Garantie der bisherigen Genauigkeit 0.001 ist analytisch
widerlegt. Der Fehler übersteigt diese Toleranz in beiden Fenstern gemeinsam
mit mindestens 26.91463487 % Wahrscheinlichkeit. Eine solche universelle
Garantie war kein vorregistrierter Populationstest; der Befund darf nicht
in einen erfundenen statistischen Test umetikettiert werden.

**Populations-RMS beim lokalen Adapter:** Es gelten rigorose Untergrenzen
0.0107911599 und 0.0045552310. Es wird kein neuer RMS-Zielwert gewählt.
Die bisherige Einzelrealisierungs-Toleranz wird nicht nachträglich zum
RMS-, Mittelwert- oder Quantilziel erklärt.

**Vorherige G1-Prüfung:** Die unveränderte Operatorzelle nu=512,
epsilon=1/16 war bereits in v0.8 wegen neun von zehn Feldtests
zurückgewiesen worden. Das ist bekannte, separate Evidenz für eine
notwendige lokale Operatorbedingung. Sie ist kein frischer Test der
Detektorkovarianz und wird nicht erneut als unabhängige Bestätigung gezählt.

Eine zutreffende Fluktuationsvorhersage kann die Streuung eines ungenauen
Operators richtig beschreiben. Daher kann ein späterer Fluktuations-PASS
mit einem makroskopischen REJECT zusammentreffen. Beide Entscheidungen
bleiben in den Ergebnisdateien eigenständig.

## 4. Unabhängig nachgerechnete strukturelle Schranken

### 4.1 Gemeinsamer Nullanteil und Referenzfehler

Der Schnitt von Quellstütze und History hat Volumen

\[
 |S|=4\pi\int_0^{1/2}r^2(3-r)\,dr=7\pi/16,
 \qquad \lambda_S=\rho|S|=21/16.
\]

Mit Wahrscheinlichkeit \(p_0=e^{-21/16}\) fehlt jeder lokale Quellknoten.
Dann ist die gesamte lokale H1-History null; die homogene retardierte
Dynamik und beide vollständigen Detektorintegrale bleiben exakt null.
Die Kontinuumsreferenzen aus v0.12 haben Beträge etwa 0.02080050516 und
0.00878043762, beide sicher größer als 0.001. Somit

\[
 \mathbb P(|A_1-c_1|>0.001,\ |A_2-c_2|>0.001)\ge p_0,
\]
\[
 \mathbb P(\text{beide Fenster innerhalb der Toleranz})\le1-p_0
 =0.730853651270816\ldots .
\]

Für einen hypothetischen festen Umfang n unabhängiger Wolken ist deshalb
die Wahrscheinlichkeit, dass alle Wolken beide Toleranzen einhalten,
höchstens \((1-p_0)^n\). Das ist eine analytische Beziehung, keine gewählte
Ensemblegröße oder neue statistische Entscheidungsregel.

Mit \(\mu=\mathbb EA\), \(\Sigma=\operatorname{Cov}(A)\) gilt in der
Ordnung positiv semidefiniter Matrizen

\[
 \mathbb E[(A-c)(A-c)^*]
 =\Sigma+(\mu-c)(\mu-c)^*\succeq p_0cc^*,
 \qquad \Sigma\succeq\frac{p_0}{1-p_0}\mu\mu^*.
\]

Die erste Ungleichung folgt durch Einschränkung des nichtnegativen
quadratischen Ausdrucks auf das Nullereignis. Für die zweite wendet man
Cauchy-Schwarz auf dessen Komplement an. Beide erlauben einen korrekten
Ensemble-Mittelwert trotz großer Streuung. Die RMS-Untergrenzen sind
\(\sqrt{p_0}|c_r|\). Die Unsicherheit der Kontinuumsreferenz bleibt in der
neuen Nachrechnung enthalten. Die angegebenen Dezimal-Untergrenzen sind
nach unten gerundet. Keine dieser lokalen Quellverlustschranken wird auf
den nichtlokalen Adapter übertragen.

### 4.2 Nichtlokale Definitionslücke

Das volle Historyvolumen ist
\(4\pi\int_0^3s^3ds/3=27\pi\), also \(\mathbb EN_H=81\). Daher

\[
 \mathbb P(N_H<4)=e^{-81}\sum_{j=0}^3\frac{81^j}{j!}
 \simeq6.10425363021\,10^{-31}>0.
\]

Der kleine Wert beseitigt die Definitionslücke nicht. Er ist nur eine
Untergrenze der problematischen Fälle, keine vollständige Ausfallquote.
Ohne Fehlerbeitrag dieser Fälle darf daraus keine Ensembleapproximation
mit kontrollierten Momenten abgeleitet werden.

### 4.3 Neue vierte Momentenschranke für das lokale Modell

Die unabhängige Rechnung prüft alle Schichtgewichte bis n=127 als rationale
Zahlen. Für n>=128 begrenzt eine fallende Polynom-mal-Exponential-Hülle
den Rest. Daraus folgt global \(|w(n)|<2\). Mit

\[
 a=4\sqrt{\rho/96},\quad \beta=\frac{a}{16(a+1)},\quad b=2\beta
\]

und \(|h|\le1\) liefert die Anzahl geordneter kausaler Pfade

\[
 |A_r|\le\sum_{j=1}^N\binom Nj b^j=(1+b)^N-1.
\]

Der passive Detektor fügt keinen zufälligen Lösungszustand hinzu. Bei der
normierten räumlich-zeitlichen Mittelung bleibt die Schranke erhalten.
Für \(N\sim\mathrm{Poisson}(512)\) folgt für jedes positive ganzzahlige p

\[
 \mathbb E|A_r|^p\le M_p
 :=\exp\{512[(1+b)^p-1]\}.
\]

Hier sind \(M_2\simeq1.36551821184\,10^{16}\) und
\(M_4\simeq2.76338081764\,10^{33}\). Das beweist Endlichkeit geeigneter
Momente des lokalen Modells. Es sind sehr grobe Obergrenzen, keine
Vorhersagen der tatsächlichen Varianz und keine Aussage, dass jede
mögliche Testmethode unbezahlbar wäre.

## 5. Bedingte Statistik für eine spätere reife Modellversion

Dieser Abschnitt leitet Werkzeuge her; er registriert **keine Kampagne**.
Numerische Werte für alpha, beta, n, Toleranzen und Fehlermargen werden
erst nach bestandener Methodenkontrolle gewählt. Die Formeln setzen
unabhängige, gleich verteilte vollständige Wolken voraus. Orte und Zeiten
innerhalb einer Wolke bleiben korreliert.

### 5.1 Vollständige gemeinsame Momentenziele

Setze \(Z=(\Re A_1,\Re A_2,\Im A_1,\Im A_2)\). Die 14 reellen
Observablen sind vier Komponenten \(Z_i\) und die zehn Produkte
\(Z_iZ_j\), \(i\le j\). Ihr Mittelwertvektor bestimmt alle vier
Mittelwerte und die reelle symmetrische Kovarianzmatrix.

Mit \(m_i=\mathbb EZ_i\), \(M_{ij}=\mathbb EZ_iZ_j\) und
\(C=M-mm^T\) ergeben sich für r,s=1,2

\[
 \mu_r=m_r+i m_{r+2},
\]
\[
 \Sigma_{rs}=C_{rs}+C_{r+2,s+2}+i(C_{r+2,s}-C_{r,s+2}),
\]
\[
 \Pi_{rs}=C_{rs}-C_{r+2,s+2}+i(C_{r,s+2}+C_{r+2,s}).
\]

Die Relationsmatrix bleibt enthalten. Ein bloßer Vergleich zweier
Fenstervarianzen wäre keine Prüfung des gemeinsamen Fluktuationstransfers.
Auch ein PASS dieser Momente validiert nicht die gesamte Verteilung oder
eine unbeobachtete mikroskopische Raumzeit-Kovarianz.

### 5.2 Endliche Konfidenz ohne Gauß-Annahme

Für jede Observable W_j brauche man eine vorab gültige Schranke
\(\operatorname{Var}(W_j)\le V_j\). Dann folgt aus Tschebyscheff

\[
 \mathbb P(|\overline W_j-\mathbb EW_j|>s_j)\le\alpha_j,
 \quad s_j=\sqrt{V_j/(n\alpha_j)}.
\]

Für das lokale Modell kann man konservativ V_j=M_2 für die linearen und
V_j=M_4 für die quadratischen Observablen verwenden. Für Produkte folgt
dies aus Cauchy-Schwarz. Die Kovarianz einer Kovarianzschätzung benötigt
somit höhere Momente; aus \(\Sigma\) allein folgt ihre Unsicherheit nicht.

Enthält jede berechnete Observable ihren exakten Wert mit Radius a_kj,
so gilt für den Stichprobenmittelwert der numerische Radius
\(e_j=n^{-1}\sum_k a_{kj}\). Mit berechnetem Zentrum \(\widehat w_j\)
ist

\[
 I_j=[\widehat w_j-e_j-s_j,\widehat w_j+e_j+s_j]
\]

ein gültiges Konfidenzintervall. Unter \(\sum_j\alpha_j\le\alpha\)
sind alle 14 Intervalle gleichzeitig mit mindestens 1-alpha gültig;
Unabhängigkeit der 14 Komponenten wird nicht benötigt. Die Intervall-
Transformation der gemeinsamen Rohmomente kontrolliert anschließend
\(\mu,\Sigma,\Pi\). Vorhersage-, Quadratur- und Linearisierungsreste
gehen in die theoretischen Zielintervalle T ein, nicht in eine nachträglich
aufgeweitete empirische Toleranz.

Für eine vorab festgelegte Äquivalenzmarge tau wird ein skalarer bzw.
komplexer Vergleich anhand des Differenzintervalls I-T entschieden:

- PASS, wenn dessen maximaler Betrag höchstens tau ist.
- REJECT, wenn dessen minimaler Betrag größer als tau ist.
- Sonst INCONCLUSIVE.

Alle vorgesehenen Komponenten müssen die jeweilige PASS-Bedingung erfüllen;
ein sicherer Verstoß verwirft die entsprechende Gesamtbehauptung. Die
bloße Überlappung von Konfidenz- und Vorhersageintervall ist kein PASS.
Diese nichtasymptotische Konstruktion ist konservativ. Sie behauptet
keine Normalität und setzt keine Stichprobenvarianz als bewiesene
Populationsschranke ein.

### 5.3 Aussagekraft, numerische Margen und Rechenbudget

Für eine skalare Größe seien r der Theorieradius und a eine vorab gültige
Obergrenze des numerischen Mittelwertfehlers. Eine vorgegebene Alternative
liege um Delta außerhalb der Äquivalenzgrenze; für eine positive
Bestätigung liegt sie entsprechend um Delta innerhalb. Falls V auch
unter dieser Alternative gilt, ist für eine Entscheidung mit
Wahrscheinlichkeit mindestens 1-beta hinreichend:

\[
 \Delta>r+2a,\qquad
 n\ge\frac{V(\alpha_j^{-1/2}+\beta^{-1/2})^2}
                 {(\Delta-r-2a)^2}.
\]

Hier bezeichnet beta das statistische Fehlerrisiko, nicht den
Kantenkoeffizienten aus Abschnitt 4.3. Begründung: Für V>0 liegt der
Stichprobenmittelwert unter der Alternative mit Wahrscheinlichkeit
mindestens 1-beta um weniger als \(\sqrt{V/(n\beta)}\) vom wahren Mittel
entfernt. Bei V=0 ist der exakte Stichprobenmittelwert deterministisch.
Zur benötigten Marge
kommen der Konfidenzradius, der Theorieradius und zweimal der numerische
Fehler. Für eine gemeinsame positive Bestätigung sind die beta-Anteile
über die verlangten Größen ebenfalls zu kontrollieren.

Diese n-Schranke ist **hinreichend für dieses Verfahren**, keine notwendige
Stichprobengröße und keine allgemeine Unmöglichkeitsgrenze. Der Code
prüft die Algebra an deterministischen Einheitsbeispielen; deren Werte
sind keine CSPP-Testparameter. Nichtschrumpfende Integrationsfehler lassen
sich durch größere Ensembles nicht beheben.

Erst wenn die Modell- und Fehlerzertifikate vorliegen, werden endliche
Alternativen, akzeptable Abweichungen und simultane Irrtumsbudgets
gewählt. Danach ist ein ausreichend konservativer Laufzeit-/Speicherplan
auf bekannten Entwicklungsfällen zu messen. Er muss Vorhersageintegrale,
Geometrie, History, Lösung, vollständige Detektorintegration, Zertifikate
und Nachprüfung enthalten. Die Zeiten der vierzuständigen Kontrolle oder
der lokalen v0.8-Operatorprüfung dürfen nicht als Kosten des vollständigen
neuen Detektorlaufs eingesetzt werden.

Im jetzigen Stand lautet die Budgetentscheidung daher
`NOT_DESIGNED_METHOD_GATE_FAILED`, nicht etwa bewiesene Unbezahlbarkeit.
Es gibt keinen fachlich begründeten frischen Lauf, dessen Ressourcen
freigegeben werden könnten.

## 6. Unabhängigkeit und spätere Abbruchregeln

Alle bisherigen Entwicklungs- und v0.8-Daten sind bekannt. Ihre erneute
Auswertung, ein anderer Präzisionslauf oder andere Fensterausschnitte
erzeugen keine unabhängigen Daten. Nach einer verbesserten Modellversion
müssten Methode, Vorhersageintervalle, Parameter, n, Fehlerbudgets,
statistische Ziele und konkrete Ressourcen-/Abbruchregeln vor dem ersten
neuen Zufallsaufruf öffentlich eingefroren werden.

Ein späterer Entwurf muss mindestens gewährleisten: disjunkte deklarierte
Validierungsströme; kein Zugriff auf den reservierten E4-Bestätigungsstrom;
keine Aussonderung ungünstiger Wolken; keine Ersatzziehung; keine Änderung
von n nach Zwischenbefunden. Bei Modell-, Integritäts- oder Ressourcenfehlern
ist ohne eigens hergeleitete Ausfallmethode keine positive Freigabe möglich.
Gerade bei unbeschränkten Momenten ist das Nullsetzen fehlender Antworten
keine konservative allgemeine Korrektur. Diese Anforderungen sind noch
keine numerisch festgelegte Abbruchregel einer gestarteten Kampagne.

Die spätere makroskopische Entscheidung muss ihr Ziel benennen: mittlere
Antwort, Populations-RMS oder Toleranzwahrscheinlichkeit. Beispielsweise
\(\mathbb E|A_r-c_r|^2=\Sigma_{rr}+|\mu_r-c_r|^2\) trennt Streuung
von Mittelwertfehler. Ein besserer Fluktuationsfit darf ein makroskopisches
Scheitern nicht überschreiben; ein makroskopischer PASS darf eine falsche
Kovarianzvorhersage nicht verdecken.

## 7. Reproduktion und Abschluss

17 neue analytische Tests sind bestanden; beide Entscheidungen werden
bei 128 und 192 Bit reproduziert. Die Tests decken Quellengeometrie,
globale Gewichtsschranke, vierte Momente, gemeinsame komplexe Momente,
Intervallentscheidungen, exakte Binomialkontrolle der Tschebyscheff-Grenze,
bedingte Powerformel und die gesperrte Testfreigabe ab. Kein Test erzeugt
ein zufälliges CSPP-Ensemble.

```bash
python -m pip install -r research/cspp/independent_transfer_v0_14/requirements.txt
python -B research/cspp/independent_transfer_v0_14/verify.py
```

`PROTOCOL.json` dokumentiert die Reihenfolge und die bewusst leeren
Designfelder. `FREEZE.json` bindet Code und relevante Vorgängerevidenz.
`admission.py` berechnet die Entscheidung, `inference.py` die bedingten
Statistikwerkzeuge. `results/DECISION_128.json`, `results/DECISION_192.json`
und `results/CHECKS.json` enthalten Rohintervalle und getrennte Statuswerte.
Die CI wiederholt die Vorprüfung ohne neue Zufallsdaten. Lokales Einfrieren
dieser Vorprüfung ist keine öffentliche Vorregistrierung eines Experiments.

Die Zurückweisung gilt für diesen konkreten Modellstand. Eine erneute
Zulassungsprüfung erfordert vollständige Originalmomente, eine totale
Adapterabbildung, ausreichende Moment-/Schwanzkontrolle und eine gemeinsame
numerische Ensemblebilanz einschließlich des Abtastgesetzes. Erst dann
beginnt die Festlegung einer unabhängigen Kampagne.

### Quellen und Evidenz

1. Eigene eingefrorene Projektquellen: v0.13 `README.md`, `PROTOCOL.json`
   und Ergebnisdateien; v0.12 vollständige Kontinuumsreferenz; v0.11
   nichtlokaler Adapter; v0.8 unabhängige lokale Operatorprüfung.
   Die Hashes der verwendeten Eingaben stehen in `FREEZE.json`.
2. Yen-Chi Chen, *STAT 512, Lecture 3*, Abschnitt 3.3.1: Tschebyscheff
   und Varianz des Mittels unabhängiger Beobachtungen.
   <https://faculty.washington.edu/yenchic/20A_stat512/Lec3_Expectation.pdf>
3. J. H. Yen, D. D. Leber, L. S. Pibida, *Comparing Instruments*, NIST TN 2106
   (2020): Vergleichs- und Äquivalenztests.
   <https://www.nist.gov/publications/comparing-instruments>

Die Intervallregel und die Powerformel sind hier ausdrücklich hergeleitet.
Die externen Quellen belegen statistische Grundlagen, keine Qualifikation
des CSPP-Modells.
