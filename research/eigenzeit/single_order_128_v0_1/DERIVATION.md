# Einzelordnungen im vollständigen 4D-Kausaldiamanten

## Experiment und Beobachtung

Im konformen Diagramm sei a=1/2, D={|t|+|x|<a}, mit x in drei Raumdimensionen.
Verglichen werden g_h=(1-h t)^(-2) η bei h=0,1/4,1/2. Für h>0 ist dies de Sitter
im flachen konformen Ausschnitt. R=12h², die Eigenzeit der Spitzen ist
T=2 atanh(h/2)/h mit stetigem Wert 1 bei h=0. Der dimensionslose Parameter ist
q=RT²=48 atanh(h/2)². Ein Versuch besteht aus exakt N=128 unabhängig nach
normiertem physischem Volumen gezogenen Ereignissen. Die strikte Ordnung wird
anschließend zufällig umnummeriert. Die Spitzen sind keine zusätzlichen Ereignisse.
Es stehen weder Koordinaten noch Dichte- oder Zeitskalenmessungen zur Verfügung.
Bei festem N geht die Information aus der absoluten Zahl eines unbedingten
Poisson-Prozesses verloren. Der Satz gilt nur für das hier festgelegte Experiment.

## Kalibrierung und Entscheidung

Der Statistikwert C2 ist die Zahl vergleichbarer ungeordneter Paare, also die
Eintragssumme der strikten transitiven Ordnungsrelation. Der Nenner für U ist
8128. Überlappende Paare sind abhängig. Für jeden Kandidaten wurden m=1999
ganze unabhängige Ordnungen erzeugt. Akzeptiert wird das einschließlich beider
Grenzen geschlossene Band vom 50. bis 1950. sortierten C2-Wert. Der Test sieht
pro Entscheidung eine Ordnung. Er gibt eine Teilmenge des festen Dreipunktrasters aus.

Unter dem wahren Modell sind die m Kalibrierwerte und der neue Wert austauschbar.
Bei zufälliger Auflösung von Bindungen ist der Rang gleichverteilt auf 1 bis
2000. Die höchstens 50 unteren und 50 oberen Ränge erzeugen eine Ablehnung;
der inklusive Test ohne Auflösung von Bindungen verwirft nur eine Teilmenge
dieser Ereignisse. Die Wahrscheinlichkeit, den wahren Rasterpunkt zu behalten,
beträgt mindestens 0,95, gemittelt über neue Beobachtung und zufällige Kalibrierung.
Die Prüfung der anderen Kandidaten verbraucht für diese Überdeckung kein
zusätzliches Fehlerbudget. Sie gibt keine simultane Garantie über viele
künftige Entscheidungen und keine bedingte Sicherheit unter Einzelmeldungen.

Bei festgehaltener Bank bewerten 4096 neue Ordnungen je Wahrheit die Einschluss-
und Ausschlussraten. Jedes Ereignis bezieht sich auf eine ganze Ordnung.
Die neun binomialen Clopper-Pearson-Intervalle haben je Rand 0,05/18 Fehlerbudget.
Ihre gemeinsame nominale Sicherheit ist mindestens 95 %. Dieselben Wolken dürfen
verschiedene Spalten bedienen, da die Bonferroni-Schranke keine Unabhängigkeit
zwischen den Spalten verlangt. Die Diagonale prüft Einschluss. Außerhalb der
Diagonale prüft die Tabelle Ausschluss einschließlich leerer Rückgaben. Für
eine Auflösung sind in beiden Richtungen mindestens 80 % gefordert. Dies war
vor der Erzeugung im Vertrag festgelegt. Die Simulationsaussagen setzen die
übliche Modellierung getrennter Pseudozufallsströme als unabhängige Zufallszüge voraus.

## Obergrenze für jeden Test der Ordnung

**Gemeinsame Koordinaten.** Schreibe u=t-r, v=t+r mit r=|x| und behalte die
Raumrichtung bei. Das konforme Diagramm ist -a≤u≤v≤a. Die steigende Funktion
f(s)=(s+k a²)/(1+k s) fixiert beide Enden. Ihre Anwendung auf u und v ist
ein bijektiver, zukunftserhaltender konformer Automorphismus des Diamanten.
Tatsächlich gilt f'(u)f'(v)=Ω² und (f(v)-f(u))/(v-u)=Ω mit
Ω=(1-a²k²)/[(1+k u)(1+k v)]. Das flache Linienelement
-du dv + ((v-u)/2)² dΩ₂² erhält damit denselben Faktor in beiden Termen.
Am räumlichen Ursprung folgt die Fortsetzung durch Stetigkeit (die kartesische
Form ist glatt). Also bleibt die beobachtete Kausalrelation in jeder Punktwolke
erhalten. Die Abbildung dient allein dem Vergleich der Wahrscheinlichkeitsgesetze.

Wähle k=h/[1+√(1-a²h²)]. Der konforme Faktor der zurückgezogenen Metrik ist
Ω/[1-h(f(u)+f(v))/2]=(1+a²k²)/(1-k²uv). Dabei verschwindet der lineare
Term wegen 2k=h(1+a²k²). In normierten Nullkoordinaten U=u/a,V=v/a,
S=UV und δ=a²k² ist die normierte Punktdichte relativ zum flachen Volumen

    pδ(S)=(1-δS)^(-4) / E₀[(1-δS)^(-4)].

Die faktorunabhängige Winkelverteilung bleibt unverändert. Die Ordnung wird
auf diesem gemeinsamen Koordinatenraum für alle h mit derselben Abbildung gelesen.
Ein beliebiges, sogar labelinvariantes Merkmal kann also die Totalvariation
des Experiments mit vollständigen ausgerichteten Koordinaten nicht vergrößern.

**Momente.** Das radiale Volumenelement ist proportional zu (V-U)² dU dV.
Für Funktionen von S gestattet Symmetrie die Integration über das ganze
Quadrat [-1,1]² mit normiertem Gewicht 3(V-U)²/8. Schreibe
a_j=0 für ungerades j, a_j=1/(j+1) für gerades j. Durch Ausmultiplizieren folgt

    m_j=E₀[S^j]=3(a_(j+2) a_j - a_(j+1)²).

**Affinität und Fehlergrenze.** Setze F_ij=E₀[(1-δ_i S)^(-2)(1-δ_j S)^(-2)].
Die Einpunkt-Affinität A_ij=∫√(p_i p_j) ist F_ij/√(F_ii F_jj).
Für N unabhängige Punkte ist die Affinität A_ij^N. Cauchy-Schwarz auf
|√p-√q|(√p+√q)/2 gibt TV≤√(1-A_ij^(2N)). Für die Ordnung und alle ihre
randomisierten Tests folgt

    P_j(verwirft i) ≤ P_i(verwirft i) + TV(P_i^Ordnung,P_j^Ordnung)
                    ≤ α + √(1 - A_ij^(2N)),

sobald P_i(verwirft i)≤α. Unabhängige Kalibrierdaten mit derselben Verteilung
unter beiden Hypothesen ändern die Schranke nicht. Damit gilt sie auch für
das marginal kalibrierte Rangverfahren. Es ist keine obere Schranke auf die
Trennleistung einer Bank, deren tatsächlicher Fehlalarm größer als α ist.
Die Affinität liefert eine obere Schranke, nicht den exakten optimalen Test.

**Numerische Einschließung.** Jede Wurzel in δ wird rational eingeschlossen.
Für F_ij ist der Koeffizient von m_n gleich Σ_(l=0)^n (l+1)(n-l+1) δ_i^l δ_j^(n-l).
Es werden alle Terme bis n=12 mit rationalen Endpunkten ausgewertet und die
Vorzeichen von m_n berücksichtigt. Für d=max(δ_i,δ_j) nach oben gerundet ist
der Betrag des Restes ab J=13 höchstens

    binom(J+3,3) d^J / [1 - d (J+4)/(J+1)].

Dies folgt aus |S|≤1, der Vandermonde-Summe und fallenden Quotienten der
Majorante. F_ij,lo²/(F_ii,hi F_jj,hi) ist somit eine untere Schranke L für A².
Die obere TV-Schranke √(1-L^N) wird auf 10^-6 nach oben gerundet. Alle drei
Zahlen wurden zusätzlich numerisch in den ursprünglichen Koordinaten gegengeprüft.

**Nachträglich abgeleitete Budgetfolge.** Damit 80 % Ausschluss bei 5 % Fehler
überhaupt möglich sind, muss L^N≤1-(0,80-0,05)²=7/16 gelten. Ein Abrunden
von L auf 30 Dezimalstellen und gerichtete Intervall-Potenzierung in audit.py
zertifizieren bis einschließlich N=8998 für flach gegen h=1/2, N=15774 für
h=1/4 gegen 1/2 und N=150271 für flach gegen h=1/4 die Unmöglichkeit.
Die jeweils folgende Elementzahl ist notwendig, ihre Hinlänglichkeit ist offen.
Dies ist eine deterministische Folge des vorab festgelegten Informationsvergleichs,
keine zusätzliche Simulation und keine universelle Grenze für andere Regionen.

## Exakte Dichtezwillinge

Interpretiert man dieselben Punkte im ursprünglichen konformen Diagramm mit
flacher Metrik und räumlich-zeitlich veränderlicher Beprobung proportional zu
(1-ht)^(-4), so ist ihr gemeinsames Koordinatengesetz genau das des gekrümmten
volumengleichmäßigen Falls. In beiden Fällen ist die chronologische Relation
dieselbe. Die gekoppelten Ordnungen stimmen somit punktweise überein. Diese
zusätzliche Kontrolle liegt außerhalb der homogenen Drei-Kandidaten-Klasse.
Sie ist qualitativ strenger als die nahe beieinanderliegenden Gesetze im Haupttest.
