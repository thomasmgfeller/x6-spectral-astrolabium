# CST-DUST: Präparation, Rückkehrtest und Fehlerbudget v0.1

7. November 2026. Grundlage: Main nach PR 260,
`c04214b9b6397abe9384bbcd728998b5c6b75173`.
Die fünf übernommenen Quellen sind in `provenance.json` bytegenau bezeichnet.

## 1. Aufgabe und Ergebnis

Der vorherige Maßvergleich unterscheidet bereits verschiedene Präparationen
von einer Änderung der L²-Darstellung. Hier wird die verbleibende
operationale Auswahl ausdrücklich untersucht. Das Ergebnis hat drei Teile:

1. Selbst die **vollständige klassische Recordverteilung**, nicht nur zwei
   Momente, legt die kohärente Präparation und Auslese nicht fest.
2. Ein als Rang-eins-Projektor qualifizierter Rückkehrdetektor und perfekte
   phasenfreie Kalibrierung erzwingen eine passende reine Präparation.
   Zusammen mit einer vorgegebenen vollständigen klassischen Recordverteilung
   folgt daraus die bisherige Referenzsichtbarkeit, unabhängig von der
   Wellenfunktionsphase und der äquivalenten Maßdarstellung.
3. Für begrenzte Kalibrier-, Effekt- und Verteilungsfehler wird eine
   explizite Wahrscheinlichkeitsfehlerschranke bewiesen.

Dies ist ein **bedingter operationaler Abschluss** der Referenzauslese.
Die benötigte Rang-eins-Messung, ihre physikalische Kopplung, der Dichteprior,
die Zahlgewichte und die CST-Dynamik werden nicht aus der Gravitation
abgeleitet. Alle acht physikalischen Gates bleiben HOLD. Ein mathematisch
gültiges Instrument ist noch kein physikalisch verfügbares Instrument.

## 2. Darstellungsunabhängiger Vertrag für Zustände und Instrumente

Sei H ein erklärter Historien-Hilbertraum bei festem Enduhrwert. Ein Zustand
ist ein positiver Spurklasseoperator ρ mit Tr ρ=1. Ein diskretes Instrument
wird durch Krausoperatoren K_(j,a) beschrieben:

\[
 \mathcal I_j(\rho)=\sum_a K_{j,a}\rho K_{j,a}^\dagger,
 \qquad E_j=\sum_a K_{j,a}^\dagger K_{j,a},
 \qquad\sum_jE_j=I.
\]

Für unendlich viele Ausgänge sind die üblichen starken bzw. Spurklassen-
Konvergenzen vorausgesetzt. Die folgenden Kontrollen verwenden endliche
Instrumente. Aus der Krausform folgt vollständige Positivität auch bei
Tensorierung mit einem beliebigen Hilfssystem; die Vollständigkeit macht
den nichtselektiven Kanal spurtreu. Der unnormierte selektive Ausgang wird
erst nach Berechnung seiner Wahrscheinlichkeit konditioniert. Ein Ausgang
mit Wahrscheinlichkeit null wird nicht durch Division künstlich erzeugt.

Für eine unitäre Darstellungsabbildung U:Hθ→H0 sind gemeinsam zu setzen:

\[
 \rho_\theta=U^\dagger\rho_0U,\quad
 E_{j,\theta}=U^\dagger E_{j,0}U,\quad
 K_{j,a,\theta}=U^\dagger K_{j,a,0}U,\quad
 D_\theta=U^\dagger D_0U.
\]

Dann stimmen die Wahrscheinlichkeiten Tr(E DρD†), die unnormierten
Zustandsupdates und alle zeitlich geordneten Produkte festgelegter
Instrumente unter U überein. Dies folgt durch Einsetzen und UU†=I;
Zwischenfaktoren heben sich in jedem Produkt auf, die Spur bleibt gleich.
Bei einem Maßwechsel ist U die Multiplikation mit der Quadratwurzel der
Radon-Nikodym-Dichte. Am diskreten Nullatom bleibt ihr Verhältnis eins.
Die Phase D=exp(iS) kommutiert mit dieser Multiplikation.

In einer endlichen gewichteten Koordinatendarstellung mit Metrik G=U†U
lautet der Adjungierte A♯=G^(-1)A†G. Die Simulation kontrolliert genau diese
Identität; sie verwechselt den gewichteten Adjungierten nicht mit dem
gewöhnlichen euklidischen Transponiert-Konjugierten.

Dieser Darstellungstransport ist kein neues Eichgesetz der Gravitation und
keine Herleitung einer CST-Zeitentwicklung. Physikalische Beschränkungen
an erlaubte Zustände oder Kopplungen müssten gesondert nachgewiesen werden.

## 3. Gleiche gesamte klassische Daten, verschiedene kohärente Ausgänge

Wir verwenden ausschließlich den vorhandenen bedingten n=1-Sektor:

\[
 H=L^2(dx\,\nu_0(dw)),\quad x\in(0,1),\quad
 \nu_0=\tfrac12\delta_0+\tfrac12\mathbf1_{(0,1)}dw,
 \quad D_\mu=\exp[-i\mu w(\tfrac12+4h^2x^2)].
\]

Die normierten orthogonalen Vektoren
|a>=√2·1_(w=0) und |c>=√2·1_(0<w<1) sind in x konstant.
In ihrem zweidimensionalen Spannraum definieren wir für η,κ∈[-1,1]

\[
 \rho_\eta=\tfrac12\begin{pmatrix}1&\eta\\\eta&1\end{pmatrix},
 \qquad E_\kappa=\tfrac12\begin{pmatrix}1&\kappa\\\kappa&1\end{pmatrix}.
\]

Beide werden durch null auf das orthogonale Komplement fortgesetzt.
Die Eigenwerte (1±η)/2 bzw. (1±κ)/2 zeigen ρ≥0, Trρ=1 und 0≤E≤I.
{Eκ,I−Eκ} ist eine gültige Zweiausgangs-POVM. Eine abstrakte Krausrealisierung
ist {√Eκ,√(I−Eκ)}; eine physikalische Kopplung wird damit nicht hergeleitet.

Für jede beschränkte diagonale Recordfunktion f(x,w) gilt
<a|f|c>=0 wegen disjunkter Träger. Daher ist für **jedes** η

\[
 \operatorname{Tr}(\rho_\eta M_f)
 =\tfrac12\langle a|M_f|a\rangle+
  \tfrac12\langle c|M_f|c\rangle
 =\int f(x,w)\,dx\,d\nu_0(w).
\]

Alle klassischen Recordwahrscheinlichkeiten und alle existierenden Momente
der Materiewirkung stimmen überein. Dies ist stärker als der vorherige
Zwei-Moment-Vergleich. Dennoch sind die kohärenten Ausgänge verschieden.
Es wird nur die Kohärenz **zwischen Atom und kontinuierlichem Anteil**
variiert; die Kohärenz innerhalb des kontinuierlichen Anteils und der
Uhren bleibt fest. Insbesondere ist ρη=0 keine vollständige Dephasierung
eines kontinuierlichen Records und kein hypothetischer spurklassiger
kontinuierlicher Diagonaloperator.

Mit

\[
 B(h,\mu)=\int_0^1\!dx\int_0^1\!dw\,
 e^{-i\mu w(1/2+4h^2x^2)}
\]

folgt durch die vier Matrixelemente exakt

\[
 P_{\eta,\kappa}(h,\mu)
 =\operatorname{Tr}(E_\kappa D_\mu\rho_\eta D_\mu^\dagger)
 =\frac{1+|B|^2+2\eta\kappa\operatorname{Re}B}{4}.
\]

D|c> muss nicht im zweidimensionalen Spannraum liegen. Die Formel enthält
die Projektion auf diesen Raum; die fehlende Masse gehört zum vollständigen
Ausfall-Effekt I−Eκ. Es wird kein normierter Nachmesszustand vorweggenommen.

Bei μ=0 ist B=1 und P=(1+ηκ)/2. Bei festem κ=1 durchläuft P das ganze
Intervall [0,1], obwohl sämtliche klassischen Recorddaten gleich bleiben.
Die Familie ist keine neue Lösung der CST-Constraints; sie beweist die
Unterbestimmtheit allein der hier erklärten kinematischen Daten.

Zugleich kann selbst ein vollständiger Scan dieser P(h,μ) nur das Produkt
ηκ bestimmen. Beispielsweise geben (η,κ)=(1,1/2) und (1/2,1) dieselben
Werte. Ohne unabhängige Qualifizierung von Präparation oder Detektor ist
die Aufteilung dieser Kohärenz nicht identifizierbar.

### Exakte endliche Kontrollen

Für U=w(1/2+4h²x²) unter dem kontinuierlichen Produktmaß gilt

\[
 E U^k=\frac1{k+1}\sum_{j=0}^k {k\choose j}
 \frac{(1/2)^{k-j}(4h^2)^j}{2j+1}.
\]

Re B=E cos(μU) und |B|²=E cos[μ(U−U′)] werden bis Grad 24 aus diesen
rationalen Momenten berechnet. Weil 0≤U≤A=1/2+4h², ist jeder Rest höchstens
r=(|μ|A)^26/26!. Für P ist der Rest deshalb höchstens
(1+2|ηκ|)r/4. Das Kosinuspolynom stimmt mit dem Grad-25-Taylorpolynom
überein; dessen Grad-26-Rest liefert die genannte Schranke.

Der eingefrorene Plan enthält h=1/4,1/2, μ=0,1/4,1 und jeweils fünf
η- und κ-Werte. Insgesamt werden 150 Fälle eingeschlossen. Bei η=κ=1
wird P=|1+B|²/4 exakt zur alten Referenzsichtbarkeit. Für die vier
nichttrivialen (h,μ)-Fälle stimmt sogar der rationale Polynommittelpunkt
mit der bereits veröffentlichten unabhängigen Mischmaßrechnung überein.

## 4. Bedingter Eindeutigkeitssatz für einen abgestimmten Rückkehrtest

**Zusatzbedingungen:**

- Der erklärte Erfolgs-Effekt ist ein **bekannter Rang-eins-Projektor**
  E=|φ><φ| mit ||φ||=1; Ausfall I−E wird mitgezählt.
- Die phasenfreie Kalibrierung erfüllt Tr(Eρ)=1.
- Die vollständige klassische Recordverteilung von φ ist vorgegeben:
  dλ=|φ(Y)|²dν(Y), einschließlich gemeinsamer Abhängigkeiten.
- D ist die unveränderte Multiplikation mit exp(iS(Y)) im gewählten
  Referenzmodell. Diese Bedingung ist keine Bewegungsgleichung.

Dann gilt **ρ=E** und

\[
 P(S)=\operatorname{Tr}(ED\rho D^\dagger)
 =|\langle\phi|D|\phi\rangle|^2
 =\left|\int e^{iS(Y)}d\lambda(Y)\right|^2.
\]

Beweis der ersten Aussage: Tr[(I−E)ρ]=0. Für ρ≥0 ist dies
|| (I−E)√ρ ||²_HS=0. Also liegt der Träger von ρ im eindimensionalen
Bild von E. Die Spur eins erzwingt ρ=E. Die restlichen Gleichungen folgen
direkt aus dem Rang-eins-Ausdruck und der Multiplikationsform von D.

Eine verbleibende Wellenfunktionsphase φ→e^(if(Y))φ hebt sich im
abgestimmten Rückkehrtest auf, weil sie mit D kommutiert. Bei äquivalenten
Maßdarstellungen werden φ und E gemeinsam transportiert; λ und P bleiben
unverändert. **Diese Eindeutigkeit betrifft die Erfolgsvorhersage unter
den Zusatzbedingungen, nicht alle Zustände oder alle Messinstrumente.**

Ein perfekter phasenfreier Test allein genügt ausdrücklich nicht:
E=I besteht ihn für jeden Zustand und liefert auch nach jeder Phase Erfolg
eins. Die Rang-eins-Eigenschaft muss deshalb unabhängig begründet oder
qualifiziert werden. Ebenso reicht eine endliche Momentliste nicht, um
λ festzulegen; der vorherige Maßvergleich liefert dafür Gegenbeispiele.

### Das Instrument bleibt eine zusätzliche Festlegung

Für eine konkrete Fortsetzung nach der Messung kann man als **Referenz**
das Lüders-Instrument K_ok=E, K_fail=I−E wählen. Dies ist eine Festlegung,
keine Folgerung allein aus E. Im Zwei-Record-Modell sei E=|+><+|,
Z=diag(1,−1). Die Krausoperatoren ZE und Z(I−E) haben dieselben Effekte,
aber der Erfolg bei Eingang |+> hinterlässt |−> statt |+>. Ein zweiter
E-Test gibt dann null statt eins. Die erste Erfolgswahrscheinlichkeit
identifiziert den Nachmesszustand somit nicht. Die Wahl eines Updates
braucht bei sequentiellen Aussagen eine eigene physikalische Rechtfertigung.

## 5. Fehlerschranke ohne perfekte Kalibrierung

Sei E=|φ><φ| das qualifizierte ideale Ziel und \(\widetilde E\) ein tatsächlicher
Effekt mit 0≤\(\widetilde E\)≤I und ||\(\widetilde E\)−E||≤τ. Die phasenfreie
Erfolgswahrscheinlichkeit erfülle Tr(\(\widetilde E\)ρ)≥1−ε. Dann gilt
Tr(Eρ)≥1−ε−τ und

\[
 T(\rho,E):=\tfrac12\|\rho-E\|_1
 \le\sqrt{1-\operatorname{Tr}(E\rho)}
 \le\sqrt{\min(1,\epsilon+\tau)}.
\]

Ein elementarer Beweis der ersten Schranke: Schreibe
ρ=Σ_j p_j|ψ_j><ψ_j|. Für zwei reine Zustände ist die Spurweite genau
√(1−|<φ|ψ_j>|²), wie die beiden nichtverschwindenden Eigenwerte ihrer
Differenz zeigen. Dreiecksungleichung und Konkavität der Quadratwurzel
ergeben T(ρ,E)≤Σp_j√(1−|<φ|ψ_j>|²)≤√(1−<φ|ρ|φ>).
Dies gilt auch für eine abzählbare spektrale Zerlegung eines
Spurklassezustands. Ein Effekt trennt zwei Zustände höchstens um ihre
Spurweite; unitäre Konjugation erhält diese.

Sei außerdem δ=TV(λφ,λ_ref) für die **vollständige gemeinsame** klassische
Recordverteilung, mit TV=1/2·||λφ−λ_ref||_var. Da |exp(iS)|=1,
unterscheiden sich die Amplituden um höchstens 2δ und ihre quadrierten
Beträge um höchstens 4δ. Daher folgt die kombinierte Grenze

\[
 \boxed{\left|\operatorname{Tr}(\widetilde E D\rho D^\dagger)
 -\left|\int e^{iS}d\lambda_{ref}\right|^2\right|
 \le\min\{1,\tau+\sqrt{\min(1,\epsilon+\tau)}+4\delta\}.}
\]

ε,τ und δ sind voneinander verschiedene Fehlerquellen. Eine obere
Konfidenzgrenze für einen Kalibrierfehler kann als ε eingesetzt werden;
die mathematische Schranke erzeugt diese experimentelle Grenze nicht.
τ setzt eine unabhängige Effektqualifizierung voraus. δ darf weder
durch zwei Momentfehler noch durch einzelne Marginalfehler ersetzt werden.
Der Beweis gilt nur bei gleichem erklärtem D; Modell- oder Dynamikfehler
sind nicht in dieser Bilanz enthalten.

Die drei ausgewiesenen Budgets sind rein diagnostisch, nicht gemessen:

| ε | τ | δ | obere Wahrscheinlichkeitsabweichung |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 10^-4 | 0 | 0 | 0,01 |
| 9·10^-6 | 10^-6 | 10^-5 | 0,003203277661 |

Der letzte Wert ist nach oben gerundet. Die Auswertung verwendet eine
ganzzahlige Quadratwurzeleinschließung. 208 exakte endliche Matrixfälle
kontrollieren zusätzlich die reine Kalibrierschranke (τ=δ=0); der
allgemeine kombinierte Satz wird durch den obigen Beweis getragen.

### Übernahme in die vorhandenen Zahlkanäle

Der Satz kann bei festem Endhorizont getrennt in jedem n-Sektor verwendet
werden. Die Zahlgewichte p_n bleiben eine zusätzliche Wahl. Sind β_n
die jeweiligen Fehlergrenzen, so ist der Fehler des Zahlkanal-Erfolgs
höchstens Σ_n p_nβ_n. Für bekannte Normmassen bis K und unbekannte
Restmasse s≤R folgt mit β_n≤1:

\[
 |\Delta P_{count}|\le
 \frac{\sum_{n\le K}c_n\beta_n+R}{Z_K+R}.
\]

Der Beweis ist die Monotonie von (B+s)/(Z_K+s) bei B≤Z_K.
Damit lässt sich das vorhandene Normrestbudget nutzen, ohne n=5 zu
integrieren. Für eine kohärente Auslese über verschiedene Elementzahlen
muss dagegen der gesamte Zustand samt solcher Kohärenzen qualifiziert
werden; getrennte Sektorkalibrierungen reichen dafür nicht.

## 6. Prüfung, offene Physik und nächste Entscheidung

Der Plan wurde nach dem algebraischen Entwurf und vor den endlichen
Rechnungen eingefroren. Dies ist keine externe Präregistrierung.
Geprüft sind 150 kontinuierliche Auslesefälle, vier Wiedergewinnungen
publizierter Referenzpolynome, 108 Produktentartungen, 300 gewichtete
Wahrscheinlichkeitsvergleiche, 240 sequentielle Instrumentvergleiche,
208 Kalibrierschranken und acht Negativkontrollen. Die kleinen
Matrixmodelle sind algebraische Kontrollen, keine Quadratur der CST.

Die Negativkontrollen erfassen die behauptete Eindeutigkeit aus klassischen
Daten, den unqualifizierten Identitätsdetektor, das Verwechseln von Effekt
und Update, die getrennte Identifikation von η und κ, fehlenden
Effekttransport, einen falschen Adjungierten, unzulässige Kohärenzparameter
und veränderte Quellbytes. Die allgemeingültigen Aussagen beruhen auf den
ausgeschriebenen Beweisen, nicht auf endlichen Tests.

**Nächste physikalische Entscheidung:** Entweder eine aus dem CST-Materie-
und Randmodell abgeleitete Wechselwirkung liefert den qualifizierten
Rückkehrdetektor und die vorgeschriebene Recordverteilung, oder die
Sichtbarkeit bleibt eine konditionale Referenzobservable. Eine weitere
Präzisierung derselben großen Integration entscheidet diese Auswahl nicht.

Ein präzises Übergabekriterium dafür steht in `operational_contract.json`:
Raum und Symmetrien, Zustandsquelle, vollständige Recordverteilung,
Detektor-Effekt samt Kopplung, Nachmesskanal, Kalibriergrenzen und
Rückwirkung müssen separat belegt werden. **Keiner dieser physikalischen
Nachweise wird durch die vorliegende algebraische Zertifizierung ersetzt.**

MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben HOLD. Kein n=5-Produktionslauf, keine kostenpflichtige
Rechenleistung, keine neue Community-Zusage und kein Messdatensatz.

## Primärquellen und Provenienz

- Projektbasis: [PR 260](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/260)
  und die in `provenance.json` gepinnten früheren Herleitungen.
- John Preskill, *Quantum Information*, Kapitel 3, insbesondere 3.1.2,
  3.2.1 und 3.2.6: https://www.preskill.caltech.edu/ph219/chap3_15.pdf .
  Kontext zu Instrumenten und vollständiger Positivität; kein CST-Auswahlgesetz.
- Matteo G. A. Paris, *The modern tools of quantum mechanics*,
  https://arxiv.org/abs/1110.6815v2 . Kontext zu Zuständen, Effekten und
  Operationen. Die hier verwendeten Familie, Schranken und Bedingungen
  sind oben selbstständig hergeleitet. Externe Volltexte werden nicht verteilt.
