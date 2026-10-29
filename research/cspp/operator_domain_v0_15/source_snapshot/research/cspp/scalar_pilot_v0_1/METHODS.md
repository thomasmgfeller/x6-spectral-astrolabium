# CSPP scalar pilot v0.1 — Methode und Geltungsbereich

Dieser Entwicklungspilot führt Schritt 2 des E4-Plans aus. Er prüft einen
konkreten skalaren Operator, bevor Dirac-, Flavor- oder Kohärenzaussagen
zugelassen werden. Das frühere E4-Dokument bleibt ein unveränderter Entwurf.
`FREEZE.json` bezeichnet ausschließlich die lokale Sperre der Pilotquellen,
keine Freigabe des E4-Bestätigungsexperiments. Die dokumentierte Korrektur in
[Amendment 01](amendment_01/README.md) erfolgte nach der ersten Auswertung.

## Geometrie und Reproduzierbarkeit

Einheiten: c=ℏ=L0=1, Koordinaten (t,x,y,z), Metrik diag(-1,1,1,1).
Die offene Region Ω4 erfüllt |t|+r<4; V4=512π/3. Gescannt wird die
dimensionslose erwartete Punktzahl ν=ρV4, nicht eine einheitenlose Dichte.
Vier unabhängige Zellen ν=(512,1024,2048,4096), je 16 Poisson-Sprinklings.
Die drei Glättungen ε=(1,1/4,1/16) benutzen jeweils dieselbe Wolke.

N~Poisson(ν). Bedingt auf N: unabhängiges Vorzeichen für t,
|t|=H(1-U^(1/4)), r=(H-|t|)W^(1/3), gleichverteilte räumliche Richtung.
Damit ist die Zeitdichte 2(H-|t|)^3/H^4 und das bedingte Raummaß das
Volumenmaß der dreidimensionalen Kugel. Die abschließende Zeitsortierung
verändert die Punktmenge nicht. PCG64DXSM und SeedSequence erhalten die
ganzzahligen Identitäten aus `PROTOCOL.json`. Rohkoordinaten bleiben gespeichert.
Kein globaler RNG, kein Python-hash, keine ausgesuchten erfolgreichen Wolken.

Strikte Kausalordnung: Δt>0 und (Δt)^2>|Δx|². Der C++-Kern zählt die
Elemente im offenen Intervall durch Schnitt von Vergangenheits- und
Zukunftsbitmengen. Die zusätzlichen Messpunkte sind keine gesprenkelten
Elemente. Nahe Nullabstände werden in long double erneut berechnet; ein
weiterhin unsicherer Vergleich blockiert den Lauf. Exakte rationale Tests
prüfen den Kern auf kleinen Kontrollmengen. Das ist **keine allgemeine
Intervallarithmetik-Zertifizierung aller Produktionskoordinaten**.

## Operator und analytische Felder

Es gilt □=-∂t²+∇². Verwendet wird der vierdimensionale geglättete
Benincasa–Dowker-Operator [1, Gleichungen 110–111]:

\[
B_\epsilon\phi(x)=\frac{4\sqrt{\epsilon\rho}}{\sqrt6}
\left[-\phi(x)+\epsilon\sum_{y\prec x} f(n(y,x),\epsilon)\phi(y)\right],
\qquad
f(n,\epsilon)=\sum_{k=0}^3 c_k{n\choose k}\epsilon^k(1-\epsilon)^{n-k},
\]

mit c=(1,-9,16,-8), ℓ=ρ^(-1/4), ℓk=(ερ)^(-1/4).
ε=1 wird durch den exakten endlichen Grenzfall ausgewertet.
Die Summe enthält nur Elemente der festgelegten endlichen Region.
Die bekannte Korrespondenzaussage für den Mittelwert [1] ersetzt weder
eine Varianzkontrolle noch eine Stabilitätsprüfung der Propagation [2].

Alle Testfelder tragen denselben glatten Abschneider χ(t,r)=h(|t|)h(r):
h(q)=1 für q≤1, h(q)=0 für q≥3, sonst
h(q)=logistic(1/s−1/(1−s)), s=(q−1)/2.
Felder: χ, χt, χz, χt², χz², χtz und
χ exp(i(kz−√(k²+1)t)) für k=(0,2,4,8).
`fields.py` berechnet □φ analytisch einschließlich aller Abschneiderterme.
Der Abschneider ist nicht vollständig innerhalb von Ω4 getragen; der
endliche Außenrand gehört deshalb ausdrücklich zur Fehlerdiagnose.

Primär werden 21 feste Einbettungskoordinaten ausgewertet: t=(-.5,0,.5),
jeweils Raumursprung und sechs Achsenpunkte mit Radius .5.
Zusätzlich: sieben Detektorproben bei t=1 und vier Randproben, gemäß Protokoll.
Die Detektorproben sind **keine numerische Integration des E4-Detektors**.

Für Feld j ist der Nenner
s_j=max(RMS_P(φ_j)/L0²,RMS_P(□φ_j)). Alle primären Nenner sind positiv.
Der dimensionslose Fehler ist (Bφ−□φ)/s_j. RMSE wird über die 16 Wolken
und 21 festen Proben gemittelt. Die Proben werden statistisch nicht als
unabhängige Sprinklings behandelt. Zusätzlich speichern wir den räumlichen
RMS des Ensemble-Bias und der Stichprobenstandardabweichung (ddof=1).
RMSE²=Bias_RMS²+(15/16)SD_RMS² wird rechnerisch kontrolliert.
Das Maximum über die zehn Felder dient nur dem vorläufigen 0,1-Screening.
Eine Identität des maximalen Feldes über Dichten wird nicht vorausgesetzt.

## Propagation und getrennte Kontrollen

Für (Bε−m²)φ=J ist die Diagonale -(a+m²), a=4√(ερ)/√6.
Das System ist nach Zeitsortierung dreieckig. Auf t≤−1 werden alle
kontinuierlichen Vergangenheitswerte vorgegeben. Die Lösung lautet rekursiv
φ_i=(aεΣ_j f(n_ji,ε)φ_j−J_i)/(a+m²).
Dies ist eine **Diagnose mit vorgegebener Kontinuumsvergangenheit**,
kein qualifizierter Adapter für ausschließlich lokale Cauchy-Daten.
Eine endliche kausale Matrix allein löst das nichtlokale Anfangswertproblem nicht.

Vier analytische Kontrollen: die kompakten Wellenfelder mit m=1 und
exaktem J=(□−1)φ. Die exakte Referenz ist hier unabhängig von einem
numerischen Fourier-Löser. Propagationsfehler werden über 28 feste
Proben bei t=(-.5,0,.5,1) als relative RMS-Fehler angegeben.

Drei zusätzliche Quellendiagnosen: der E4-Bump mit Radius .5, Trägerwelle
k0=4, φ(-1)=f, ∂tφ(-1)=0 und m=(0,1,2). Eine periodische Fourier-Rechnung
auf einer Box der Länge 12 verwendet den Faktor cos(√(p²+m²)(t+1)).
Es werden 64³/dt=.125 und 128³/dt=.0625 verglichen. Räumlich wird
trilinear, zeitlich linear interpoliert. Die Kontinuumsstütze kann im
Zeitfenster [-4,1] die periodische Boxgrenze nicht erreichen; daraus folgt
**keine** Schranke für Diskretisierungs-, Fourier- oder Interpolationsfehler.
Die feinere Rechnung liefert nur eine diagnostische Referenz und Historie.
Die Differenz beider Auflösungen ist kein zertifizierter Restfehler.
REFERENCE_HOLD bleibt daher unabhängig vom Operator-Screening bestehen.

Der algebraische Rückwärtsfehler ist max |Aφ−b|/(|A||φ|+|b|), mit
einem Maschinenminimum im Nenner. Eine kleine Zahl belegt eine genaue
Lösung des diskreten Gleichungssystems, keine Kontinuumsnähe und keine
obere Vorwärtsfehlerschranke. Separat wird die Antwort auf eine konstante
Einheitsänderung der vorgeschriebenen Historie bei m=1, J=0 gespeichert.
Dies testet eine Richtung; es ist keine induzierte Operatornorm.

## Rand, Statistik und Entscheidung

Für je vier Wolken bei ν=512 und 4096 wird dieselbe innere Punktmenge
um ein unabhängiges Poisson-Sprinkling in Ω5\Ω4 bei gleicher ρ ergänzt.
Der Operator wird an denselben Proben erneut gemessen. Es ändern sich
weder Feld noch innere Wolke; zusätzliche Elementzahlen werden nicht als
höhere innere Dichte ausgegeben. Die gepaarte Differenz diagnostiziert
Außengebietssensitivität. Sie beweist keine Randkonvergenz.

Das feste M=16 liefert deskriptive Mittelwerte, Streuungen und RMS-Fehler.
Es gibt keine Bestätigungs-Konfidenzintervalle, keine adaptive Stoppregel,
keinen Potenzgesetzfit und keine Auswahl eines Siegers für eine Physikaussage.
Zwölf vollständige Zellen werden berichtet. Ein Rechenfehler oder Ressourcen-
abbruch würde die Freigabe blockieren und seinen Lauf nicht aus dem Ensemble
entfernen. Hier konnten alle 64 Hauptläufe berechnet werden.

G1 bleibt HOLD. G2 (Dirac), G3 (gemeinsame Geometrieregion) sowie Flavor
und Kohärenz werden nicht ausgeführt. Die beabsichtigte spätere Trennung
von Geometrie, Operator und Statistik ist mit dieser Diagnose vorbereitet,
aber quantitativ noch nicht vollständig zertifiziert.

## Primärquellen

1. A. Belenchia, D. M. T. Benincasa, F. Dowker, *The continuum limit of a
   4-dimensional causal set scalar d'Alembertian*,
   [arXiv:1510.04656v2](https://arxiv.org/abs/1510.04656v2),
   [Volltext, insbesondere Abschnitt zum geglätteten Operator](https://arxiv.org/html/1510.04656v2).
2. S. Aslanbeigi, M. Saravani, R. D. Sorkin, *Generalized Causal Set
   d'Alembertians*, [arXiv:1403.1622](https://arxiv.org/abs/1403.1622).
   Die dortigen Stabilitätsergebnisse betreffen die untersuchten Operatoren;
   unser kleiner Pilot beweist weder deren asymptotisches Verhalten noch
   ein allgemeines Scheitern von Causal-Set-Propagation.
