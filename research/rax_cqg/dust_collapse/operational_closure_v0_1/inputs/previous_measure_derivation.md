# CST-DUST: Maßabhängigkeit und Zustandstransport v0.1

7. November 2026. Basis: PR 258 / Main
`3177458a7f8545f845054e235cd3dcd7e829eff3`.
Vier verwendete Rechenmodule sind byteidentisch gepinnt; `provenance.json`
nennt ihre ursprünglichen Pfade und Git-Blob-Identitäten.

## 1. Frage, Vergleich und Reichweite

Der große n=5-Lauf ist nicht erforderlich, um die folgende Frage zu prüfen:
Bestimmen Normierung, Nullanteil, Mittelwert und Varianz des Materiemaßes
die kohärente Auslese der bisherigen Referenzkonstruktion eindeutig?

Wir halten Uhrmaß, geankerte Kausalordnungen, Wirkung, Kopplungen, α-Gewichte
und die **Vorschrift konstanter normierter Randvektoren** fest. Variiert wird
das unabhängige, an jedem neuen Element gleiche Dichtemaß. Dies ist zunächst
ein Vergleich mathematischer Referenzvorschriften, keine Identifikation
derselben physikalischen Präparation in verschiedenen Darstellungen.

Ergebnis: Die konstante Randvorschrift ist unter diesen Momentbedingungen
nicht invariant. Bereits im bedingten Ein-Element-Kanal liegen acht exakte
Differenzintervalle vollständig außerhalb von null. Zugleich gilt ein
exakter Darstellungssatz: Werden beide Randvektoren mit dem Maß transportiert,
bleiben die betrachteten Matrixelemente unverändert. Die Interpretation ist
daher eine offene Auswahl von **Maß, Zustand und Auslese gemeinsam**.

Gleiche erste zwei Momente sind kein Beweis gleicher klassischer Dynamik,
gleicher gravitativer Rückwirkung oder physikalischer Zulässigkeit aller
Vergleichsmaße. Alle acht physikalischen Gates bleiben HOLD.

## 2. Positive Familie mit gleichen ersten beiden Momenten

Für -1≤θ≤1 setze auf [0,1]

\[
 q(w)=20w^3-30w^2+12w-1=P_3(2w-1),\qquad
 \nu_\theta=\tfrac12\delta_0+
 \tfrac12[1+\theta q(w)]\mathbf1_{(0,1)}(w)dw.
\]

Die Legendre-Bezeichnung ist eine Einordnung; die folgenden elementaren
Identitäten tragen den hier benötigten Beweis:

\[
 q(w)+1=2w[10(w-3/4)^2+3/8],\qquad
 1-q(w)=2(1-w)[10(w-1/4)^2+3/8].
\]

Auf [0,1] sind beide rechte Seiten nichtnegativ; im Innern sind sie positiv.
Also |q|≤1 und |q|<1 im Innern. Damit ist die kontinuierliche Dichte für
|θ|≤1 nichtnegativ und im Innern positiv. Der diskrete Nullanteil bleibt
exakt 1/2. Direkte Integration liefert für jedes ganzzahlige k≥0

\[
 I_k:=\int_0^1w^kq(w)dw
 =\frac{20}{k+4}-\frac{30}{k+3}+\frac{12}{k+2}-\frac1{k+1}
 =\frac{k(k-1)(k-2)}{(k+1)(k+2)(k+3)(k+4)}.
\]

Die letzte Identität folgt durch gemeinsamen Nenner und Ausmultiplizieren.
Somit m_0=1, m_1=1/4, m_2=1/6 und Var(w)=5/48 für alle θ. Für k≥1 ist
m_k(θ)=1/[2(k+1)]+θ I_k/2. Insbesondere

\[
 m_3(\theta)-m_3(0)=\theta/280,\qquad
 m_4(\theta)-m_4(0)=\theta/140.
\]

Die Familie bleibt an allen Elementen identisch und unabhängig. Damit wird
keine Beschriftung bevorzugt. Die vorhandenen Uhrsymmetrien werden durch
diesen reinen Dichtewechsel nicht zusätzlich gebrochen; daraus folgt keine
neue Aussage über physikalische Eichquantisierung.

## 3. Erhaltene Wirkungs-Momente und Normreste

Für feste Geometrie und Uhren hat die geerbte Materiewirkung die Form

\[
 S_d=-\sum_jw_ja_j,\qquad
 a_j=\tfrac12+4h^2\sum_{y\prec j} B_{k(y,j)}(x_j-x_y)^2,
 \quad B=(1,-9,16,-8),\quad B_{k\ge4}=0.
\]

Der Anker x=0 gehört zur Summe. Aus Unabhängigkeit folgt für beliebige
endliche Elementzahl, ohne numerische Integration:

\[
 E_\theta S_d=-m_1\sum_j a_j,\qquad
 E_\theta S_d^2=m_2\sum_j a_j^2+
 2m_1^2\sum_{i<j}a_ia_j.
\]

Beide Ausdrücke sind θ-unabhängig. Dasselbe gilt nach Integration über das
unveränderte Uhrmaß. Auch die ersten beiden Momente einer vollständigen
Wirkung mit festem geometrischem Beitrag bleiben gleich. Die Gültigkeit
dieser Identitäten ist nicht gleichbedeutend mit einer Bewegungsgleichung.

Da jedes νθ normiert ist, bleiben die Sektornormmassen
c_n=N_n h^n/n! · 2^[-α n(n-1)/2] unverändert. Daher gelten die bereits
bewiesenen kombinatorischen Normrestschranken weiter. Diese Invarianz der
Normierung darf nicht mit Invarianz kohärenter Auslesewahrscheinlichkeiten
bei konstanten Randvektoren verwechselt werden.

## 4. Exakter Ein-Element-Gegenvergleich

Bei einem neuen Element und x gleichverteilt auf [0,1] ist
a(x)=1/2+4h²x² positiv. Setze U=w a(x). Die konstante Randvorschrift liefert
Aθ=Eθ exp(-iμU), Vθ=|Aθ|². Die Gravitationsphase ist hier trivial (G=0);
auch ein gemeinsamer reiner Phasenfaktor würde V nicht ändern. V ist der
**bedingte n=1-Kanal**, nicht die gesamte unbegrenzte Zahlkanalwahrscheinlichkeit.

Die Uhrmomente sind exakt

\[
 M_k(h)=E[a(x)^k]=\sum_{j=0}^k {k\choose j}
 \frac{(1/2)^{k-j}(4h^2)^j}{2j+1},\qquad E_\theta U^k=m_k(\theta)M_k(h).
\]

Aus der Potenzreihe folgt

\[
 A_\theta-A_0=i\theta\mu^3M_3/1680+O(\mu^4),
\]

\[
 V_\theta-V_0=\theta\mu^4
 \frac{2M_4-M_1M_3}{3360}+O(\mu^6).
\]

Der Koeffizient ist positiv: Für die positive Zufallsvariable a ist
Cov(a,a³)≥0, denn mit einer unabhängigen Kopie a′ gilt
2 Cov(a,a³)=E[(a-a′)(a³-a′³)]≥0. Also M_4≥M_1M_3 und
2M_4-M_1M_3≥M_4>0. Dies beweist bereits einen Unterschied für hinreichend
kleine, von null verschiedene μ und festes θ≠0.

Die vorher festgelegten endlichen Werte werden ohne asymptotische
Fehlerschätzung eingeschlossen. Mit einer unabhängigen Kopie U′ gilt

\[
 V_\theta=E\cos[\mu(U-U')],\quad
 D_{2k}=E(U-U')^{2k}=
 \sum_{j=0}^{2k}(-1)^j{2k\choose j}E U^{2k-j}E U^j.
\]

Alle Momente sind rationale Zahlen. Da 0≤U≤a_max=1/2+4h², gilt
|U-U′|≤a_max. Das Kosinuspolynom bis Grad 24 hat daher den Rest

\[
 \left|V_\theta-\sum_{k=0}^{12}
 \frac{(-1)^k\mu^{2k}D_{2k}}{(2k)!}\right|
 \le\frac{(|\mu|a_{max})^{26}}{26!}.
\]

Die Grad-25-Taylorform hat denselben polynomialen Teil; ihr Lagrange-Rest
liefert die angegebene Grad-26-Grenze, weil alle reellen Kosinusableitungen
Betrag höchstens eins haben. Ein unabhängiges Amplituden-Taylorpolynom mit
Rest (|μ|a_max)^25/25! kontrolliert den Sichtbarkeitseinschluss zusätzlich.
Die Koeffizienten werden außerdem exakt durch die Faltung A·conj(A) geprüft.

| h | μ | V(+1)-V(0), ungefähr | V(-1)-V(0), ungefähr |
|---|---|---:|---:|
| 1/4 | 1/4 | +1.55596214e-7 | -1.55588700e-7 |
| 1/4 | 1 | +3.90460795e-5 | -3.90156528e-5 |
| 1/2 | 1/4 | +1.35418804e-6 | -1.35407273e-6 |
| 1/2 | 1 | +3.22433506e-4 | -3.21985807e-4 |

Alle acht rationalen Differenzintervalle schließen null aus. Die größte
Intervallbreite ist kleiner als 3.757e-22; dies ist die Breite der exakten
mathematischen Taylor-Einschließung, keine experimentelle Messunsicherheit.
Die vollständigen Brüche stehen in `results/one_element_witnesses.json`.

## 5. Darstellungssatz: Maß und Randvektoren gemeinsam transportieren

Dieser Abschnitt ist eine ausdrücklich dokumentierte Ergänzung nach
Einfrieren des ursprünglichen Plans und Start der Rechnung (`supplement.json`).
Vergleichsparameter und Fehlerordnung wurden nicht geändert.

Alle νθ sind zueinander äquivalent. Relativ zu ν0 lautet die
Radon-Nikodym-Dichte rθ am **Atom w=0 exakt 1**, im kontinuierlichen Innern
rθ(w)=1+θq(w)>0. Der Wert der kontinuierlichen Formel am Rand ersetzt nicht
das atomare Verhältnis. Für |θ|=1 sind die möglichen Nullstellen nur
Lebesgue-Nullmengen; zwischen den gewichteten Hilberträumen bleibt der
folgende Operator unitär:

\[
 U_\theta:L^2(\nu_\theta)\longrightarrow L^2(\nu_0),\qquad
 f\longmapsto\sqrt{r_\theta}\,f.
\]

Beweis: ||Uθ f||²_ν0=∫rθ|f|²dν0=||f||²_νθ. Für jedes g∈L²(ν0)
ist f=g/√rθ in L²(νθ) und Uθ f=g. Das beweist Isometrie und Surjektivität.
Die punktweise möglicherweise unbeschränkte inverse Funktion an Randnähe
ist kein Problem für die Norm zwischen diesen beiden gewichteten Räumen.

Die betrachtete Wirkung wirkt als Multiplikation mit exp(iS); sie kommutiert
mit diesem Dichtefaktor. Für mehrere Elemente ersetzt man rθ durch
Rθ=∏j rθ(w_j). Uhrmaß, Geometriesumme und Sektorgewichte bleiben unverändert.
Für jedes endliche n gilt deshalb:

\[
 \langle R_\theta^{-1/2},e^{iS}R_\theta^{-1/2}\rangle_{\nu_\theta^{\otimes n}}
 =\int e^{iS}d\nu_0^{\otimes n}.
\]

Beide transportierten Vektoren haben Norm eins. Die Präparation und die
Auslese müssen beide transformiert werden; ein einzelner Faktor würde nur
√Rθ kompensieren. Nach einer kontrolliert konvergenten Sektorsumme bleibt
die Gleichheit erhalten; bei α≥1 und endlichem h sichert die vorhandene
positive Normrestmajorante die erforderliche absolute Domination.

| Vergleich | Zustand/Auslese im gemeinsamen ν0-Raum | Ergebnis |
|---|---|---|
| In jedem νθ konstante Randvektoren 1 | √Rθ statt 1 | Verschiedene Referenzpräparationen; Gegenbeispiel gilt |
| Beide Randvektoren Rθ^(-1/2) in νθ | Dieselben Vektoren 1 | Matrixelemente exakt identisch |

Das ist keine Herleitung einer unitären CST-Zeitentwicklung, kein
gravitatives Eichgesetz und keine Auswahl eines physikalischen Zustands.
Es verhindert, dass eine bloße Änderung der Darstellung als neue Physik
ausgegeben wird. Der beobachtete Referenzunterschied kann im gemeinsamen
Raum vollständig als geänderte Präparation und Auslese dargestellt werden.

## 6. Belastbare Änderungsschranke für die konstante Randvorschrift

Definiere χθ(t)=∫exp(-itw)dνθ(w). Wegen I_0=I_1=I_2=0 verschwinden die
ersten drei Terme der Differenz. Der Taylor-Rest dritter Ordnung und |q|≤1
liefern für alle reellen t und θ,η∈[-1,1]

\[
 |\chi_\theta(t)-\chi_\eta(t)|
 \le \frac{|\theta-\eta||t|^3}{12}\int_0^1w^3|q(w)|dw
 \le\frac{|\theta-\eta||t|^3}{48}.
\]

Zusätzlich gilt |χθ-χη|≤|θ-η|/2 aus der totalen Variation. Alle χ sind
charakteristische Funktionen positiver normierter Maße und haben Betrag
höchstens eins. Eine teleskopierende Produktdifferenz ergibt daher

\[
 |A_{p,\theta}-A_{p,\eta}|
 \le D_p:=\min\left\{2,\frac{n|\theta-\eta|}{2},
 \frac{|\theta-\eta||\mu|^3}{48}\sum_jE_x|a_j|^3\right\}.
\]

Der Betrag zwei ist die allgemeine Schranke zwischen Einheitskreispunkten.
Für jedes a_j wird sein Bereich mit rationalen Bernstein-Koeffizienten
eingeschlossen. Ist das Vorzeichen fest, wird E|a_j|³ exakt polynomial
integriert. Andernfalls gilt E|a_j|³≤M_j E a_j² mit M_j≥sup|a_j|. Diese
Rechnung verwendet nur niedrige Polynom-Momente, keine Feldquadratur.

Für den geometrisch kohärenten Sektor ist D_n der Mittelwert der D_p, da
die unveränderten Gravitationsphasen Betrag eins besitzen. Die Änderung
der Sektorsichtbarkeit ist höchstens min(1,2D_n).

Zur unbegrenzten Zahlensumme setzen wir K=4,
R=c_5+c_6+Δ_6, Zmax=Z_4+R und K_v=Σ_(n≤4)c_n min(1,2D_n), D_0=0.
Der tatsächliche unbekannte Rest s liegt zwischen 0 und R. Da K_v≤Z_4,
ist (K_v+s)/(Z_4+s) monoton wachsend in s. Es folgt

\[
 |P_{count,\theta}-P_{count,\eta}|
 \le \frac{K_v+R}{Z_{max}}.
\]

Analog ergibt sich für die kohärente Gesamtsichtbarkeit

\[
 |P_{coh,\theta}-P_{coh,\eta}|\le
 \min\left(1,2\frac{\sum_{n\le4}c_nD_n+2R}{Z_{max}}\right).
\]

Die Monotonie benutzt hier Σc_nD_n≤2Z_4. Alle Größen sind exakt rational.
Die acht berechneten Parametersätze gelten für |θ-η|=1, beliebiges g und
die konstante Randvorschrift. Es sind obere Grenzen, keine tatsächlich
beobachteten Änderungen des unendlichen Kanals. Für μ=0 sind alle Änderungen
exakt null; für den kovariant transportierten Vergleich aus Abschnitt 5
ebenfalls für jedes μ. Die großen konservativen Schranken ersetzen keine
physikalische Auswahlregel.

## 7. Prüfungen, Reproduktion und Urteil

Der eingefrorene Plan enthält θ=-1,0,1; h=1/4,1/2; μ=1/4,1; Grad 24.
Die Familie und der führende Gegenbeispielterm wurden vorher algebraisch
hergeleitet. Es gibt weder eine externe Präregistrierung noch eine blinde
Vorhersage. Der Darstellungstransport ist als spätere Ergänzung offengelegt.

Geprüft werden 33 exakte Momentformeln; 12 Sichtbarkeitsfälle mit acht
getrennten Gegenvergleichen; 100 Vollwirkungs-/Inkrementkontrollen;
100 Geometrie-/Uhrfälle mit gleichen Momenten bis Grad zwei; 100 geometrische
Änderungsbudgets und acht unbegrenzte Parameterschranken. Sechs negative
Kontrollen verwerfen Vorzeichenfehler, fehlenden Halb-Faktor, falsche
Normierung, unzulässiges θ, einen falschen Nullunterschied und veränderte
Quellbytes. Die Ergänzung kontrolliert 175 polynomiale Matrixelemente,
245 Produktfälle, die falsche Atomformel und einseitigen Randtransport.

`python3 -B analyze.py` erzeugt fünf Ergebnisdateien.
`python3 -B transport_controls.py` erzeugt die sechste.
`python3 -B replay.py` erzeugt sie in einem frischen Verzeichnis erneut und
verlangt Bytegleichheit. Python-Standardbibliothek genügt. Das ist
Reproduzierbarkeit derselben Implementierung, keine externe Replikation
oder formale Prüfung mit einem Beweisassistenten.

**Urteil:** Die ersten beiden Materiemomente wählen die Referenzpräparation
nicht eindeutig aus. Ein Maßwechsel allein ist aber kein Nachweis neuer
Physik: Bei transportierten Zuständen/Auslesen ist die untersuchte Familie
darstellungsäquivalent. Der nächste wissenschaftliche Engpass ist eine
physikalische, darstellungsunabhängige Festlegung von Zustand und Messauslese.

MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben HOLD. Der n=5-Community-Auftrag bleibt die Berechnung des
ursprünglichen ν0-Referenzfalls. Es wurde keine kostenpflichtige Rechenleistung
beauftragt und kein n=5-Produktionslauf gestartet.

## 8. Primärquellen

- [PR 258](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/258)
  und die in provenance.json gepinnten Quellen: Modell, Wirkung und Normreste.
- [NIST DLMF 18.3](https://dlmf.nist.gov/18.3): Einordnung der klassischen
  orthogonalen Polynome einschließlich Legendre.
- [NIST DLMF 18.5](https://dlmf.nist.gov/18.5): explizite Darstellungen.
  Die hier verwendete kubische Formel, ihre Positivität und sämtliche
  Momentidentitäten sind oben unabhängig und vollständig ausgeführt.

Der gewichtete L²-Transport wird hier unmittelbar durch Normidentität und
Surjektivität bewiesen; es wird daraus keine zusätzliche CST-Physik zitiert.
