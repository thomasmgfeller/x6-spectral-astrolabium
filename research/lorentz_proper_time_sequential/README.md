# Sequenzielle Eigenzeit und bedingte Kettendiagnostik

Implementierte Forschungsreferenz im bekannten flachen Diamanten. Anschluss
an [Einschluss und Feststichprobe](../lorentz_proper_time_domain/README.md).
Das Paket erlaubt datenabhängiges Stoppen bei festem Stichprobengesetz und
eine einmalige Diagnose der inneren Ordnung. Es enthält **keinen
Krümmungsschätzer und keinen topologischen Kontinuumsnachweis**.

## 1. Beobachtungs- und Fehlervertrag

Referenzdiamant D, seine bekannte Zeitdauer S, Dimension d und markierte
Endpunkte p<<q sind vor der Bestätigungsstichprobe festgelegt; I(p,q) ist
vollständig in D enthalten. Die unabhängigen uniformen Punkte X_i liefern
Y_i=1{p<<X_i<<q}. Bedingt auf die gewählten Endpunkte gilt

\[
\mathbb E[Y_i\mid\mathcal F_{i-1}]=a=(\tau/S)^d.
\]

Anpassbar ist die Zahl frischer Beobachtungen. Eine Erhöhung der Ankunftsrate
bei unveränderter räumlicher Verteilung verletzt dieses Modell nicht.
Ein Wechsel der Region, Markierungen, Zeitkalibrierung oder räumlichen
Auswahlwahrscheinlichkeiten wird jedoch nicht durch dieselbe Konfidenzfolge
abgesichert. Eine unabhängige Pilotphase kann die feste Region bestimmen;
anschließend beginnt eine neue, separat budgetierte Bestätigungsstichprobe.
Beliebig viele Neustarts, Paare oder Regionen benötigen eine gemeinsame
Fehlerallokation. Metadaten prüfen keine physikalischen Stichprobenannahmen.

Im vorab fixierten Vertrag ist alpha_total=0,05, aufgeteilt in alpha_time=0,025
und alpha_chain=0,025. Die Zeitkonfidenzfolge hat daher mindestens 97,5%
simultane Deckung; die einmalige Diagnose hat höchstens 2,5% Fehlalarm unter
dem flachen Nullmodell. Unter diesem gemeinsamen Modell beträgt die
Wahrscheinlichkeit mindestens eines dieser beiden Fehlereignisse höchstens
5%. Nichtverwerfen der Diagnose beweist die Modellannahmen nicht.

## 2. Howard-Konfidenzfolge mit endlicher LIL-Rate

Wir verwenden Howard et al., Theorem 4 (empirical Bernstein), kombiniert mit
der gestitchten sub-Gamma-Grenze aus Theorem 1, Gleichung (8). **Nicht**
verwendet werden nachträglich eingesteckte Stichprobenvarianzen in einer
normalverteilungsbasierten Feststichprobengrenze oder gerundete Beispielkonstanten.

Vor jedem festen Beobachtungsblock wird die Prognose q_i auf den bisherigen
kumulierten Erfolgsanteil gesetzt; vor dem ersten Block gilt q_i=0. Innerhalb
des Blocks bleibt sie konstant. Damit ist q_i vorhersehbar bezüglich der
Beobachtungsfiltration und liegt in [0,1]. Definiere

\[
K_n=\sum_{i=1}^nY_i,\quad
\widehat V_n=\sum_{i=1}^n(Y_i-q_i)^2.
\]

Für einen Block mit b Beobachtungen und k Erfolgen ist der exakte Zuwachs
k(1-q)^2+(b-k)q^2. Die Prognose wird **vor** dem Einlesen dieses Blocks
festgelegt. Deshalb sind aggregierte binomiale Blockzählungen ausreichend;
die Reihenfolge innerhalb des Blocks wird nicht nachträglich ausgewählt.

Parameter: eta=2, s=1,4, v_min=1, c=1 und alpha_side=alpha_time/2.
Seien Z_s=sum_{j>=1} j^(-s), w=max(v,v_min) und

\[
\ell(w)=\log\frac{Z_s}{\alpha_{\rm side}}
 +s\log\left(1+\frac{\log(w/v_{\min})}{\log\eta}\right),
\]
\[
k_1=(\eta^{1/4}+\eta^{-1/4})/\sqrt2,\qquad
k_2=(\sqrt\eta+1)/2,
\]
\[
u(v)=\sqrt{k_1^2w\ell(w)+k_2^2c^2\ell(w)^2}+k_2c\ell(w).
\]

Hier ist h(k)=Z_s(k+1)^s steigend und sum_{k>=0}1/h(k)=1. Die
sub-exponentielle Funktion aus Theorem 4 wird bei c=1 durch die
sub-Gamma-Funktion lambda²/[2(1-lambda)] dominiert: Dies folgt für
0<=lambda<1 durch Vergleich der Potenzreihen von -log(1-lambda)-lambda.
Damit ist die obige Grenze auf Theorem 4 anwendbar.

Für alle n gleichzeitig gilt mit Wahrscheinlichkeit mindestens 1-alpha_time:

\[
a\in C_n=[K_n/n-u(\widehat V_n)/n,
          K_n/n+u(\widehat V_n)/n]\cap[0,1].
\]

Die LIL-Rate bezieht sich auf das asymptotische Wachstum der Schranke:
u(v)=O(sqrt(v log log v)+log log v). Ihre endliche Gültigkeit stammt aus dem
genannten Satz, nicht aus einer asymptotischen Normalapproximation.
Die laufende Schnittmenge bisheriger C_n bleibt gültig, weil a konstant ist.
Die Software prüft feste Batch-Endpunkte; der zugrunde liegende Satz gilt
auch für die darin enthaltene vollständige Beobachtungsfolge.

Durch die monotone Transformation entstehen Zeitgrenzen
L_n=S*lower(C_n)^(1/d), U_n=S*upper(C_n)^(1/d). Bei variierendem
Stichprobengesetz würde Theorem 4 nur eine durchschnittliche bedingte
Erfolgswahrscheinlichkeit überdecken; deren Wurzel wäre im Allgemeinen
**keine** Eigenzeit. Das wird nicht als unterstützte Adaptivität ausgegeben.

Die Implementierung verwendet float64 und eine kleine nach außen gerichtete
numerische Reserve. Sie ist kein formal verifizierter Intervallarithmetik-Beweis.

## 3. Stoppregel und richtige Bedeutung der Garantie

Für 0<L<=U setze

\[
\widetilde\tau=\frac{2LU}{L+U},\qquad
r=\frac{U-L}{U+L}.
\]

Für **jeden** Wert tau in [L,U] gilt
|tilde_tau/tau-1|<=r. Das Maximum liegt an einem der beiden Endpunkte und
ist dort gleich groß. Die Ausgabe ist daher der harmonische Mittelpunkt,
nicht zwingend die bisherige Volumen-Punktschätzung S(K/n)^(1/d); letztere
wird zusätzlich unverändert als `raw_volume_estimate` berichtet.

Die Software stoppt am ersten Batch-Endpunkt mit L>0 und r<0,1. Andernfalls
meldet sie bei ausgeschöpftem Budget `BUDGET_EXHAUSTED`; eine leere
Schnittmenge führt zu `EMPTY_CONFIDENCE_SEQUENCE` und keiner Zeitfreigabe.
Kein Seed wird ersetzt, kein Fehlpfad still verworfen.

Die genaue Aussage ist

\[
\Pr\{\text{Präzision gemeldet und }|\widetilde\tau/\tau-1|>0.1\}
\le\alpha_{\rm time}.
\]

Bei einem endlichen Budget ist dies **nicht** automatisch dieselbe Aussage
bedingt auf die Teilmenge erfolgreicher Stopps. Es gibt keinen garantierten
endlichen Beobachtungsbedarf; bei a=0 kann relative Präzision grundsätzlich
nicht erreicht werden. Die Nullstrom-Kontrolle ist ein statistischer
Grenzfall, keine Behauptung über zeitartig getrennte physikalische Endpunkte.

## 4. Kettenhöhe als bedingte Ordnungsdiagnostik

H ist die maximale Zahl strikter innerer Knoten auf einer Kette. Mit den
beiden Endpunkten hätte eine maximale Kette H+2 Knoten beziehungsweise H+1
Kanten. Diese Konvention ist über Referenz und Beobachtung identisch.

Wir verwenden **keinen** asymptotischen Faktor gamma_d zur Zeitkalibrierung.
Stattdessen wird H bei der tatsächlich beobachteten inneren Punktzahl K mit
unabhängigen uniformen K-Punkt-Ordnungen eines flachen d-Diamanten verglichen.
Lorentztransformation und Skalierung erklären die Unabhängigkeit dieses
bedingten Nullgesetzes von tau, Lage und Boost des inneren Intervalls.

Für B=255 unabhängige Referenzhöhen sind die beiden Rang-p-Werte
(1+#H_ref<=H_obs)/(B+1) und (1+#H_ref>=H_obs)/(B+1). Ihr doppeltes Minimum,
auf 1 begrenzt, ist ein konservativer zweiseitiger p-Wert; Bindungen zählen
mit. Austauschbarkeit liefert die einseitigen Ranggarantien, ein Union Bound
die zweiseitige Garantie. Die kleinste mögliche Ausgabe beträgt 2/256.

Ein einmaliger Test am count-basierten Stoppzeitpunkt ist zulässig: Die
Stoppregel verwendet nur Intervallindikatoren, keine inneren Koordinaten oder
Höhen. Bedingt auf diese Indikatoren und K bleiben die inneren Punkte uniform.
Die Referenzbank wird unabhängig erzeugt. Wiederholte Tests, Auswahl von
Paaren anhand ihrer Höhe oder Wahl eines günstigen Referenz-Seeds sind nicht
abgesichert. Die integrierte Schnittstelle erlaubt eine Diagnose pro Stream
und prüft K gegen die übergebene innere Matrix. K außerhalb [8,512] wird als
nicht im Diagnosebudget gemeldet; keine heimliche Extrapolation.

Eine Warnung heißt `FLAT_MODEL_DEVIATION` und setzt die wissenschaftliche
Zeitfreigabe auf `WITHHELD_MODEL_WARNING`. Ursachen können Stichprobendichte,
Randabschneidung, falsche Dimension, Relationsfehler oder Geometrie sein.
`NO_DEVIATION_DETECTED` ist keine Bestätigung, dass all diese Fehler fehlen.
Die Kettenhöhe ist eine Ordnungsstatistik, kein hier bewiesenes topologisches
Invarianten- oder Krümmungszertifikat.

**Grundsätzliche Verwechslungsmöglichkeit:** Für g'=Omega²g bleibt die
chronologische Relation unverändert, während dV_g'=Omega^d dV_g gilt.
Uniforme Volumenbeprobung in einer entsprechend gekrümmten konformen Metrik
hat damit dasselbe Ordnungsgesetz wie passende inhomogene Beprobung im
flachen Raum. Ohne unabhängige Information über die Beprobung kann kein
reiner Ordnungstest diese Ursachen eindeutig auseinanderhalten.

## 5. Begrenzte Prüfung, Ergebnisse und Bedienung

[contract.json](contract.json) fixiert vor neuen Zielziehungen drei positive
Zählmodelle mit je 1.024 Läufen, einen Nullstrom mit 64 Läufen, vier bedingte
Kettentests mit je 128 unabhängigen Beobachtungs-/Referenzgruppen sowie
einen tatsächlichen lokalen 4D-Geometrielauf mit integrierter Stoppdiagnose.
Die Nulltests besitzen getrennte Referenzbanken; ihr Fehlalarmanteil wird
nicht fälschlich als unabhängige Binomialzählung bei gemeinsamem Bankfehler
behandelt. Acht festgelegte Implementierungsgates verwenden Bonferroni 1%.

Gezielte Fehlkontrollen: vollständige Ketten, Antiketten, räumlich komprimierte
Punktwolken **bei weiterhin flacher Metrik**, und absichtlich abhängige
Bernoulli-Ströme. Dies sind Gegenbeispiele für unberechtigte Modellübertragung,
keine positiven Krümmungstests. Eine quantitative Empfindlichkeit gegenüber
bestimmten gekrümmten Geometrien ist weiterhin nicht etabliert.

```sh
python research/lorentz_proper_time_sequential/verify.py --design-only
python research/lorentz_proper_time_sequential/run.py
python research/lorentz_proper_time_sequential/verify.py
```

Runner und Prüfer akzeptieren einen anderen Ergebnisverzeichnispfad als
erstes Argument. Der Runner überschreibt keine vorhandenen Ergebnisse.
Er schreibt die Quellenhashes vor der ersten Zielziehung; diese lokale
Fixierung ist keine externe Präregistrierung. `batch_counts.npz` enthält
sämtliche Blockzählungen, `summary.json` alle Referenzhöhen und Stoppausgaben.

[Ergebnisbericht](results/RESULTS.md), [Prüfbericht](results/verification.json),
[Geometrischer Integrationslauf](results/integration_demo.json).

## Quellen

- Howard et al., [Time-uniform, nonparametric, nonasymptotic confidence sequences](https://arxiv.org/html/1810.08240v9),
  Annals of Statistics 49(2), 1055–1080 (2021), Theoreme 1 und 4, Gleichung (8).
- Brightwell und Gregory, [The structure of random discrete spacetime](https://ntrs.nasa.gov/api/citations/19900019113/downloads/19900019113.pdf),
  PRL 66,260 (1991): Ketten und asymptotische Zeitabstände. Die hier
  implementierte endliche Rangdiagnose wird nicht dieser Arbeit zugeschrieben.
- Ilie, Thompson und Reid, [A numerical study of the correspondence between paths in a causal set and geodesics in the continuum](https://arxiv.org/abs/gr-qc/0512073),
  CQG 23 (2006) 3275–3286: numerische Pfad-/Geodätenbeziehung. Kein Beleg für
  eine eindeutige Krümmungsdiagnose aus einer einzelnen Kettenhöhe.

Keine neue mathematische Priorität, Universalität oder industrielle
Überlegenheit wird beansprucht. Die wissenschaftliche Ergänzung ist die
explizite Verbindung eines bekannten sequenziellen Satzes mit dem bisherigen
Geometrievertrag und einer abgegrenzten endlichen Modelldiagnostik.
