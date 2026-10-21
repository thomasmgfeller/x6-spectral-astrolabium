# V1b: begrenzte Eigenzeit-Qualifikation, Version 2

Dieses Dokument, der Code, die analytische Planung und die Seed-Liste werden
vor der Erzeugung neuer Zielwolken gemeinsam in einem öffentlichen Commit
festgeschrieben. Der Commit wird anschließend in `freeze.json` referenziert.
Version 2 ist eine neue, enger definierte Qualifikation. Der historische
V1b-Status **NOT_PASSED** und **HOLD_PHASE3** bleiben bestehen.

## 1. Vom Eigenzeit-Ziel zu prüfbaren Grenzen

Das bestehende Ziel steht in
[`../../lorentz_proper_time_validity/contract.json`](../../lorentz_proper_time_validity/contract.json):
relativer Präzisionsradius höchstens 0,10, Wahrscheinlichkeit einer ausreichend
präzisen Ausgabe mindestens 0,90, nominelle Überdeckung mindestens 0,95.
Für ein Intervall [L,U] gelten harmonischer Mittelpunkt H=2LU/(L+U) und
R=(U−L)/(U+L). Wenn die wahre Eigenzeit im Intervall liegt, ist
|H/τ−1|≤R. Die Prüfung verlangt deshalb zusätzlich direkt
P(überdeckt UND R≤0,10)≥0,90; dies ist stärker als die getrennte Präzisionsforderung.

Die neue technische Budgetentscheidung reserviert **2 %** für eine
systematische Skalenabweichung des mittleren Zählanteils. Diese Aufteilung
ist vorab gewählt, nicht aus der alten Auffälligkeit geschätzt.
Mit θ=τ/T, p=θ^d und q=E_seed[K/m] lautet die Äquivalenzforderung exakt:

    p(1−0,02)^d ≤ q ≤ p(1+0,02)^d.

Sie bedeutet |(q/p)^(1/d)−1|≤0,02. Sie ist keine Aussage über den
Jensen-Bias E[(K/m)^(1/d)] und impliziert keine Binomialverteilung von K.
Beide Aspekte werden getrennt behandelt: endlicher Schätzerbias wird
berichtet, tatsächliche Intervallüberdeckung wird über neue Seeds geprüft.

Die unveränderte native 95%-Clopper-Pearson-Inferenz liefert [L,U]. Eine neue
Referenzfunktion `qualifiedInterval` erweitert sie zu

    L* = L/1,02,   U* = U/0,98.

Diese Transformation folgt direkt aus der obigen multiplikativen Abweichung.
Sie besitzt unter dem idealen Binomialmodell eine entsprechende robuste
Interpretation. Für den endlichen Generator nehmen wir dieses Modell nicht
als bewiesen an: P_seed(τ∈[L*,U*])≥0,95 und
P_seed(τ∈[L*,U*] UND R*≤0,10)≥0,90 werden eigenständig getestet.
Die vorhandene Browser-Anzeige bleibt unverändert. Nur die neue
Referenzfunktion ist Gegenstand dieses begrenzten Nachweises.

## 2. Vorab gewählter Gültigkeitsbereich und Budget

- Unverändertes `core.js`, Version 1.1, flache Minkowski-Geometrie.
- Bekannte Dimension d∈{2,3,4}, zentrale ineinander liegende Diamanten.
- Genau m=4096, θ∈{0,4; 0,7}, T=1. Homogene Skalierung mit bekanntem T
  ist algebraisch; numerische Tests erfolgen bei T=1.
- Zusätzlich θ=0,1 und 0,2 als veröffentlichte Budgetdiagnostik; keine
  Freigabe dieser kleineren Intervalle und keine Interpolation zwischen θ-Werten.
- R=8192 vollständige Wolken je Dimension: **100 663 296 native Punkte**.
- Zwei positive Kontrollen in 4D mit je 512 Seeds: falscher Radius
  (2 097 152 Punkte) und Wiederholung eines einzigen Punkts pro Wolke
  (512 erzeugte Punkte; logische Wolkengröße weiterhin 4096).
- Ein Durchlauf, feste Reihenfolge, maximal 1200 Sekunden Datenerzeugung.
  Keine Erweiterung des Budgets nach Einsicht in Ergebnisse.

`planning.json` berechnet die ideale Binomial-Überdeckung, Präzision und
Erfolgswahrscheinlichkeit der Überdeckungsprüfungen ohne neue Zufallsdaten.
Für alle sechs primären Zellen müssen die idealen Prüf-Powers mindestens
0,90 sein. Die Äquivalenzprüfung verwendet beobachtete Varianz; ihre
Gültigkeit benötigt keine angenommene Binomialvarianz. Eine universelle
Power für beliebige defekte Generatoren wird nicht behauptet.

## 3. Unabhängige Einheit: der zufällig gewählte Startseed

`secrets.randbits(32)` wählt Seeds aus der Betriebssystem-Zufallsquelle.
Die Annahme ist eine unabhängige Gleichverteilung dieser Ziehungen. Die
fest archivierten früheren 128 Kontrollseeds sowie 0, 1, 20261017,
4294967295 und der Randfallseed 2463401483 werden allein anhand ihrer
Identität ausgeschlossen; jeder Ausschluss wird vorab in `seeds.json`
veröffentlicht. Weitere frühere Arbeiten können Seeds aus dieser Population
benutzt haben; eine vollständige historische Seed-Inventur wird nicht behauptet.
Es gibt keine Auswahl anhand der neuen Ergebnisse.

Unter den neuen Ziehungen bleiben Duplikate erhalten (mit Zurücklegen).
Die Zustandsfenster dürfen sich überlappen. Ein deterministischer Funktionswert
f(seed) aus unabhängig gewählten Seeds bleibt eine unabhängige Stichprobe
aus der Verteilung über Seeds; überlappende Zustandsfenster ändern diesen
Sachverhalt nicht. Nach dem Einfrieren sind die Daten deterministisch
reproduzierbar. Die frequentistische Aussage bezieht sich auf das vorher
definierte Seed-Ziehexperiment, nicht auf zusätzliche Zufälligkeit beim Replay.

Innerhalb einer Wolke wird **keine Unabhängigkeit** vorausgesetzt.
Die Qualifikation betrifft die endliche, explizit definierte Seedpopulation,
nicht jeden einzelnen Seed. Die Betriebssystemquelle wird nicht physikalisch
auditiert. Die Sensitivitätskontrolle mit wiederholtem Einzelpunkt soll gerade
einen Fall erkennen, in dem richtige Einzelpunkt-Marginalen unbrauchbare
Wolken erzeugen.

## 4. Endliche Konfidenzgrenzen auf Wolkenebene

Für jeden mittleren Zählanteil sind X_i=K_i/m unabhängige Werte in [0,1].
Setze vorab a=max(0,p−8√(p(1−p)/m)), b=min(1,p+8√(p(1−p)/m)) und
Y_i=clip(X_i,a,b). Die ideale Binomialvarianz legt hier ausschließlich die
festen Clippinggrenzen fest; Ausreißer werden nicht verworfen.

Für jeden Ausgang X∈[0,1] gilt punktweise:

    Y − a·1{X<a} ≤ X ≤ Y + (1−b)·1{X>b}.

Damit ergibt sich ein gültiges Intervall für EX aus einem Intervall für EY
und zwei oberen Grenzen für die Tail-Wahrscheinlichkeiten. Für jede der
beiden Seiten von EY verwenden wir Theorem 4 von Maurer und Pontil (2009),
mit dem üblichen unverzerrten Stichprobenvarianzschätzer s_Y²:

    radius = √(2 s_Y² log(8/α_g)/R)
             + 7(b−a) log(8/α_g) / [3(R−1)].

Jede Seite erhält Fehlerbudget α_g/4. Die beiden Tail-Obergrenzen u_lo und
u_hi sind einseitige exakte Clopper-Pearson-Grenzen mit demselben Budget.
Das gesamte Konfidenzintervall lautet:

    [max(0, mean(Y)−radius−a u_lo),
     min(1, mean(Y)+radius+(1−b)u_hi)].

Die Vereinigungsabschätzung der vier Ereignisse begrenzt den Fehler auf α_g.
Für Überdeckung und gemeinsame Überdeckung/Präzision verwenden wir direkt
zweiseitige Clopper-Pearson-Grenzen über die 8192 Bernoulli-Wolkenergebnisse.
Die vier Bonferroni-Teilbudgets werden nicht nach beobachteten Tails umverteilt.

## 5. Die 52 vorab festgelegten primären Prüfungen

**18 Eigenzeitprüfungen:** sechs (d,θ)-Zellen, jeweils Äquivalenz des
mittleren Zählanteils, Mindestüberdeckung 0,95 und gemeinsame
Überdeckung/Präzision mindestens 0,90.

**34 Marginalprüfungen:** je Dimension zeitliches Z=(1−2|t|)^d und radiales
W=(r/(0,5−|t|))^(d−1) an den Schwellen 0,25, 0,50 und 0,75 (18 Prüfungen).
Zusätzlich Vorzeichen der einen Raumrichtung in 2D (1); in 3D je
Richtungskomponente Schwellen −1/√2, 0, +1/√2 (6); in 4D je Komponente
−0,5, 0, +0,5 (9). Ideale CDF-Werte sind jeweils 0,25/0,50/0,75,
in 2D nur 0,50. Der vorab gewählte zusätzliche technische Toleranzbetrag
ist 0,005 absolut. Diese wenigen Sonden sind keine globale CDF-Grenze und
beweisen weder Unabhängigkeit noch vollständige Winkelisotropie.
Ihre Toleranz allein garantiert keine Eigenzeitgenauigkeit; dafür stehen
die direkten Eigenzeitprüfungen.

Familienfehler α_F=0,05, gleichmäßig α_g=0,05/52 je Prüfung. Die
Unabhängigkeit verschiedener Prüfungen ist für Bonferroni nicht erforderlich.
Das Familienniveau betrifft diesen neuen, vorab definierten Versuch;
es wird nicht rückwirkend mit früheren Prüfungen kombiniert.

Äquivalenz: PASS, wenn das Konfidenzintervall vollständig im Toleranzbereich
liegt; FAIL, wenn beide disjunkt sind; sonst UNENTSCHIEDEN.
Mindestleistung: PASS, wenn die Untergrenze mindestens das Ziel erreicht;
FAIL, wenn die Obergrenze unter dem Ziel liegt; sonst UNENTSCHIEDEN.
Gesamt-PASS erfordert alle 52 PASS, vollständige Daten, Quellidentität,
strikte Stütze, Transformationsfehler ≤1e−12 und bestandene positive Kontrollen.
Eine falsche Radiuspotenz muss mindestens eine radiale Prüfung verfehlen;
die Einzelpunktwiederholung muss beide 4D-Überdeckungsprüfungen verfehlen.
Ein fehlgeschlagener harter Nachweis ergibt FAIL, ein unvollständiger Lauf
UNENTSCHIEDEN. Ein neuer Lauf zur Ergebnisverbesserung ist nicht zugelassen.

## 6. Technische Evidenz und Grenzen

Die frühere technische V1b-Evidenz und Radialdiagnose werden über ihre
unveränderten Quellen und Archivprüfungen weiterverwendet. Die neue
Erfassung prüft auf bekannten Seeds 0 und 1 die vollständigen Koordinaten
und Zählungen gegen `cloud()`, bevor neue Seeds ausgewertet werden.
Native und unabhängige SciPy-Intervallgrenzen werden für alle tatsächlich
vorkommenden K verglichen (absolute Toleranz 2e−10).

Archiviert werden alle Wolken-Zählungen, Marginalzählungen, Seedidentitäten,
Transformationsmaxima, Ablehnungen und SHA-256-Hashes der geordneten
IEEE-754-Koordinaten (Little Endian). Die vollständigen Koordinaten sind
reproduzierbar, aber nicht als Rohdateien archiviert. Kein Ausreißer wird entfernt.
Die CI analysiert diese identischen Beobachtungen erneut; dies ist kein
weiterer statistischer Versuch. Rechenergebnisse dürfen beim Replay nur
um 1e−12 absolut plus 1e−12 relativ abweichen; Entscheidungen bleiben exakt.

Keine Aussage zu gekrümmter Raumzeit, adaptiven Messungen, anderen Budgets,
unbekannter Skala/Dimension, physikalischer Validierung oder Phase-3-Freigabe.

## Primärquellen

- [Bestehender Genauigkeitsvertrag](../../lorentz_proper_time_validity/contract.json).
- [Maurer & Pontil (2009), Theorem 4](https://www.cs.mcgill.ca/~colt2009/papers/012.pdf).
- [NIST: exakte Binomial-Konfidenzintervalle](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbici.htm).
- [Python: secrets und Betriebssystem-Zufallsquelle](https://docs.python.org/3/library/secrets.html).
