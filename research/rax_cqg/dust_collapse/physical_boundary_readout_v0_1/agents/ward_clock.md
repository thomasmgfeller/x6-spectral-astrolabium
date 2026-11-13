# Kompakter Randvertrag: Ward-Identitäten, normierte Pakete und einseitiger Quelltest

**Zentraler neuer Befund:** Im bislang ausgewerteten N=11-Dirichletvertrag verändert eine ausschließlich am Vergangenheitsrand variierte Dichte die relativen Historienamplituden überhaupt nicht. Die zuvor beobachtete Antwort bei gemeinsam geändertem Randparameter stammt vollständig vom zugleich geänderten Zukunftsrand. Dieser begrenzte Gegenbefund ist algebraisch exakt und wurde durch einen getrennten Vier-Zellen-Rechenlauf bestätigt. Er ist kein allgemeines Verbot einer Antwort auf echte präparierte Anfangszustände.

Die tatsächlichen kompakten Maße liefern außerdem Schwinger-Dyson-/Integrationsidentitäten **mit Randtermen**, keinen homogenen Constraintprojektor. Normalisierte Randpakete können im erklärten Hilfsmaß ausdrücklich konstruiert werden; ihre kinematische Norm ist damit noch nicht als physikalisches Skalarprodukt ausgewählt.

## 1. Was aus dem Dichtemaß wirklich folgt

Das verwendete Maß ist

\[
d\nu(r)=\tfrac12\delta_0+\tfrac12\mathbf1_{(0,1)}(r)dr.
\]

Ein Zustand hat eine eigene Atomkomponente `f_a` und einen positiven Anteil `f_+(r)`. Der Atomwert ist nicht automatisch der Spurwert `f_+(0)`; mathematisch handelt es sich um eine direkte Summe. Definiere bei festgehaltenen übrigen Variablen

\[
A_C[f]=\tfrac12 f_a+\tfrac12\int_0^1 f_+(r)e^{-irC/2}dr.
\]

Auf dem positiven Anteil liefert Integration durch Teile für geeignete differenzierbare Testfunktionen exakt

\[
\frac12\int_0^1
\left[f_+'(r)-\frac{iC}{2}f_+(r)\right]e^{-irC/2}dr
=\frac{f_+(1)e^{-iC/2}-f_+(0)}2.
\]

Die Atomkomponente wurde nicht differenziert. Mit
`J_C[f_+']=1/2 integral f_+' exp(-irC/2)dr` lautet die entsprechende Gesamtidentität

\[
C A_C[f]=\tfrac C2 f_a
+i\left[f_+(1)e^{-iC/2}-f_+(0)\right]-2iJ_C[f_+'].
\]

Für konstante Gewichte gilt

\[
D(C)=\tfrac12+\frac{1-e^{-iC/2}}{iC},\qquad
C D(C)=\tfrac C2+i(e^{-iC/2}-1).
\]

Insbesondere ist `D(4*pi)=1/2` und `C D(C)=2*pi` dort ungleich null. Die kompakte Integration erzwingt daher kein `C=0`. Ein positiver frei variierter innerer klassischer Sattel verlangt weiterhin `C_j=0`; diese Eulerbedingung ist aber kein aus dem bisherigen Maß abgeleiteter Quantenprojektor. Bei positiven Testpaketen mit kompaktem Träger im offenen Intervall verschwinden zwar die positiven Randspuren, doch der Ableitungsterm bleibt. Auch daraus folgt nicht die punktweise Auslöschung von C.

Diese Aussagen erfordern weder eine geänderte Dichtevorzeichenklasse noch eine Integration über die gesamte reelle Multiplikatorachse. Eine solche Änderung wäre ein neuer Kandidat und müsste eigenständig begründet werden.

## 2. Uhr-Ward-Identität mit Boxrand

Im gegenwärtigen N=11-Vertrag ist `L=3/2` und `dλ(T)=dT/(2L)=dT/3` auf `[-L,L]`. Für `E_j=partial S/partial T_j` gilt

\[
\int_{-L}^{L}\left[\partial_{T_j}\psi+iE_j\psi\right]e^{iS}
\frac{dT_j}{2L}
=\frac{[\psi e^{iS}]_{-L}^{L}}{2L}.
\]

Die anderen Variablen und ihre Maße können anschließend gepaart werden. Bei konstantem Uhrpaket ist der Randfluss im Allgemeinen nicht null. Ein kompaktes inneres Testpaket beseitigt zwar die Spuren, führt aber dessen Ableitung in die Identität ein. Eine homogene Gleichung `integral E_j exp(iS)=0` darf deshalb nicht ohne Prüfung des Uhrzustands und der Randwerte eingesetzt werden.

Die vollständige Wirkung hängt nur von Uhrdifferenzen ab, daher gilt vor der Integration exakt `sum_all_j partial_Tj S=0`. Für den mit festen äußeren Uhren `T_B` definierten Kernel ergibt sich daraus jedoch

\[
\sum_{b\in B}\partial_{T_b}K(T_B)
=-\sum_{j\in I}\frac1{2L}
\int d\mu_{I\setminus j}\,
\left[e^{iS}\right]_{T_j=-L}^{T_j=L},
\]

mit zusätzlich vorhandenen Paketen entsprechend ihrer Produktregel. Der rechte Term ist eine echte Oberfläche des Integrationswürfels. Er kann nicht durch die Shift-Invarianz der Wirkung allein gestrichen werden.

Ein einfaches quadratisches Kontrollbeispiel zeigt die Nichtnulligkeit: Für
`S=-(t-tau)^2/2`, `L=3/2`, `tau=1/4` besitzt
`K(tau)=integral exp(iS)dt/3` die Ableitung

\[
K'(1/4)=\frac{e^{-49i/32}-e^{-25i/32}}3,
\qquad |K'(1/4)|=\frac23\sin(3/8)>0.
\]

Eine gemeinsame Verschiebung von **allen** Uhren, Integrationsgebieten und Paketen ergibt dagegen eine korrekte Kovarianz zwischen transportierten Verträgen. Das ist etwas anderes als eine Eichsymmetrie eines unveränderten Würfels mit festgehaltenen Dirichletwerten. Das Streichen einer Uhrvariablen durch `T0=0` wäre ohne Ableitung des transformierten Maßes, der Randdomäne und gegebenenfalls des Eichfaktors keine zulässige Folgerung.

## 3. Explizite normalisierte Randpakete im vorhandenen Hilfsmaß

Definiere die glatte kompakte Funktion

\[
b(u)=\begin{cases}e^{-1/(1-u^2)},&|u|<1,\\0,&|u|\ge1,\end{cases}
\qquad J=\int_{-1}^1 b(u)^2du>0.
\]

J ist ein fester, exakt definierter Normierungswert; es wird kein numerischer Näherungswert dafür benötigt. Für `0<epsilon<min(r0,1-r0)` ist

\[
f_{r_0,\epsilon}(r)=\sqrt{\frac2{\epsilon J}}\,
b\!\left(\frac{r-r_0}{\epsilon}\right),\qquad f_a=0
\]

genau auf eins normiert in ν. Es besitzt einen Träger strikt im positiven Sektor und Mittelwert `r0`. Der Atomanteil des Maßes wurde nicht entfernt; dieser Zustand hat dort lediglich Amplitude null.

Für `eta<L-|tau|` ist

\[
g_{\tau,\eta}(T)=\sqrt{\frac{2L}{\eta J}}\,
b\!\left(\frac{T-\tau}{\eta}\right)
\]

genau normiert in `dT/(2L)` und besitzt Mittelwert `tau`. Ein Faktor `exp(ip(T-tau))` ändert diese Norm nicht. Produkte dieser Dichte-/Uhrpakete mit normierten skalaren Gaußfunktionen liefern echte kinematische Randvektoren, keine Deltafunktionen an kontinuierlichen Koordinaten.

Als vollständig rationale Normkontrolle dient ergänzend das kompakte **C²**, nicht C∞, Profil `p(u)=(1-u²)^3` für `|u|<1`, außerhalb null. Hier gilt

\[
\int_{-1}^1p(u)^2du=\frac{2048}{3003},\quad
A_r^2=\frac{3003}{1024\epsilon},\quad
A_T^2=\frac{3003L}{1024\eta},\quad
\operatorname{Var}(r)=\frac{\epsilon^2}{15},\quad
\operatorname{Var}(T)=\frac{\eta^2}{15}.
\]

Diese Normen und Varianzen wurden exakt symbolisch geprüft. Eine konkrete gemeinsame Familie verwendet die Dichtemittelpunkte `1/8,1/4` und `epsilon=1/32`. Die beiden positiven Dichteträger sind disjunkt und damit im Hilfsmaß orthogonal. Für die affinen äußeren Uhrmittelpunkte `(j-5)Delta` ist `eta=1/16` vollständig innerhalb der gegenwärtigen Uhrbox zulässig. Derselbe Zukunftsrandzustand kann für beide Anfangspräparationen festgehalten werden.

**Grenze:** Die Konstruktion schließt die fehlende Normierbarkeit der Dirichlet-Auswertungen auf kinematischer Ebene. Sie beweist weder, dass das erklärte Produktmaß die physikalische Norm ist, noch dass diese Zustände sämtliche dynamischen Constraints erfüllen. Die neue vollständige Randpaket-Paarung wurde hier nicht mit der früheren Dirichletrechnung verwechselt oder als bereits ausgeführter höherdimensionaler Rechenlauf ausgegeben.

## 4. Tatsächlich ausgeführter einseitiger Quelltest

Das ursprüngliche Vollgewicht verwendete denselben Parameter rho an beiden äußeren Kragen. Jetzt werden ausdrücklich zwei Parameter getrennt:

\[
r_j=\rho_P\quad(j=0,1,2,3),\qquad
r_j=\rho_F\quad(j=7,8,9,10).
\]

Die äußeren Uhren bleiben affine Dirichletwerte; innere Uhrbox und Dichtemaß bleiben unverändert. Es wird keine Theta-Beschränkung eingeführt. Definiere

\[
B_P=\sum_{j=0}^3C_j,\qquad B_F=\sum_{j=7}^{10}C_j.
\]

Für beide Ordnungen ist unabhängig von sämtlichen inneren Uhren

\[
(C_0,C_1,C_2,C_3)=\left(1,\frac{20}{19},-\frac{16}{19},\frac{128}{19}\right),
\qquad B_P=\frac{151}{19}.
\]

Daher faktorisiert das vollständige neue Integral exakt:

\[
\begin{aligned}
W_c(\rho_P,\rho_F)
&=e^{iF_c}\left\langle e^{-\frac i2(\rho_PB_P+\rho_FB_F)}\prod_ID(C_j)\right\rangle_T\\
&=e^{-i151\rho_P/38}V_c(\rho_F).
\end{aligned}
\]

Somit gelten, wo das Verhältnis definiert ist,

\[
\partial_{\rho_P}\log W_c=-i\frac{151}{38},\qquad
\boxed{\partial_{\rho_P}\log\frac{W_1}{W_0}=0.}
\]

Der gemeinsame Phasenfaktor ändert weder relative kohärente Amplituden noch die Beträge einzelner Zweige. Bei gleicher rho-unabhängiger Skalarpaarung und festem gemeinsamen Readout bleibt auch jede daraus gebildete bedingte Randverteilung unverändert.

Der Vier-Zellen-Test wurde tatsächlich für `rhoP,rhoF in {1/8,1/4}` mit 128 und 160 Gaußknoten je innerer Uhr ausgeführt; die beiden partiellen Ableitungen wurden getrennt integriert. Alle acht Dichtestrata bleiben in `product D` enthalten.

| Vergangenheit rhoP | Zukunft rhoF | numerischer Betrag W1/W0 |
| --- | --- | --- |
| 1/8 | 1/8 | 1.605547530957258 |
| 1/4 | 1/8 | 1.605547530957258 |
| 1/8 | 1/4 | 1.869370056797860 |
| 1/4 | 1/4 | 1.869370056797860 |

Die numerischen Residuen der exakt verschwindenden vergangenen relativen Ableitung liegen bei etwa `10^-15`. Der Nullsatz folgt aus der Faktorisierung, nicht aus dieser kleinen numerischen Differenz. Die künftige relative Ableitung ist dagegen dieselbe nichttriviale Ableitung, die vorher entlang `rhoP=rhoF` gemessen wurde:

| Zukunft rhoF | partielle Ableitung nach rhoF von log(W1/W0) |
| --- | --- |
| 1/8 | 0.894388245208967 + 2.298401541807125 i |
| 1/4 | 1.499473042358319 + 1.726611722842165 i |

Damit ist die frühere Randantwort mathematisch nicht widerlegt, aber ihre Quellinterpretation präzisiert: **In diesem festen Dirichletvertrag war sie eine Antwort auf den mitveränderten Zukunftsrand. Sie ist kein Nachweis einer allein durch Anfangsdichte ausgelösten Geometrieänderung.**

Die frühere analytische W-Trunkationsschranke gilt auch hier, weil `rhoF<=1/4` und `rhoP` nur einen konstanten Faktor vom Betrag eins erzeugt. Float64-Rundung bleibt davon getrennt und nicht vollständig zertifiziert. Der Rechenlauf benötigt lokal wenige Sekunden.

## 5. Was der Nullsatz nicht behauptet

Die Faktorisierung benutzt die festgehaltenen frühen Uhren. Werden echte vergangene Uhrpakete gemeinsam mit Dichtepaketen integriert, ist der frühe Dichtefaktor eine Funktion dieser Uhren. Er kann dann unter derselben Integration mit dem zukunftsabhängigen Kernel gekoppelt sein. Die jetzige Rechnung schließt eine solche Präparationsantwort nicht aus. Ebenso wenig ist sie ein No-go für andere Kausalordnungen, Quellenräume oder physikalisch begründete Randmaße.

Für einen nächsten präparierten Quellvergleich müssen deshalb ein gemeinsamer festgehaltener Zukunftsrand und normierte vergangene Pakete Bestandteil desselben Tests sein. Erst danach darf eine verbleibende Antwort einem Anfangszustand zugeschrieben werden. Die oben konstruierten Pakete machen diesen Vertrag konkret; das physikalische Skalarprodukt und die darauf zulässigen Zustände bleiben eine getrennte Herleitungspflicht.

`checks/ward_clock/check.py` und `results.json` dokumentieren die exakten Maß- und Normidentitäten, den Shift-Randterm, die algebraische Quellfaktorisierung und den ausgeführten Vier-Zellen-Test. Der unabhängige Audit rekonstruiert die frühen Constraints und die Quelle/Zukunft-Trennung separat.
