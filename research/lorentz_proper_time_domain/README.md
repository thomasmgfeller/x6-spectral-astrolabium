# Eigenzeit: Einschluss, endliche Ordnung und bedingte Fehlergrenzen

Dieses abgeschlossene, begrenzte Arbeitspaket ergänzt die vorhandene
[1+1-Referenz](../lorentz_proper_time/README.md). Es formuliert den bekannten
flachen Zusammenhang für d Dimensionen und prüft seine Implementierung für
d=2,3,4. Es begründet weder einen universellen Eigenzeitschätzer noch neue
Kontinuumsrekonstruktions- oder Kausalitätssätze.

## 1. Satz mit expliziten Einschlussbedingungen

Sei d>=2 eine bekannte **Raumzeitdimension**, c=1 und
M=R^d mit Minkowski-Metrik g=-dt²+dx_1²+...+dx_(d-1)². Für Ereignisse x,y sei

\[
x\ll y\quad\Longleftrightarrow\quad
y^0-x^0>\|\mathbf y-\mathbf x\|_2.
\]

Wir verwenden die strikte **chronologische** Relation. Nullgetrennte Punkte
sind nicht vergleichbar. Bei kontinuierlichen iid-Volumenstichproben ist
exakte Nulltrennung ein Nullereignis; für Messdaten darf das nicht einfach
vorausgesetzt werden.

Seien A<<B fest, T=tau(A,B)>0 bekannt, und
D=I(A,B)={x:A<<x<<B} der gesamte äußere Diamant. Die markierten Endpunkte
erfüllen **A<<p<<q<<B**. Sie werden entweder fest vorgegeben oder unabhängig
von den anschließend erzeugten Hintergrundpunkten gewählt. Es erfolgt keine
nachträgliche Auswahl nach K oder nach der Hintergrundordnung.

Dann folgt aus Transitivität für jedes z mit p<<z<<q:
A<<p<<z<<q<<B. Also ist

\[
I(p,q)\subset D.
\]

Es wird das volle innere Intervall gezählt: keine Beobachtungsmaske, kein
zeitlicher Ausschnitt, keine ausgelassenen Ereignisse, kein Relationsfehler.
Eine Hasse-Matrix darf nicht als vollständige Relationsmatrix interpretiert
werden. Ihre transitive Hülle wäre ein ausdrücklich getrennter Adapter.

Die Zielgröße ist theta=tau(p,q)/T, wobei tau die maximale Eigenzeit zwischen
den Endpunkten (hier die geradlinige zeitartige Verbindung) bezeichnet. Die
Eigenzeit einer beliebig beschleunigten Weltlinie folgt daraus nicht.

**Volumenrechnung.** Im Ruhesystem eines Diamanten mit Zeitdauer s ist sein
räumlicher Querschnitt zur Zeit t eine (d-1)-Kugel mit Radius s/2-|t|. Daher

\[
V_d(s)=2\omega_{d-1}\int_0^{s/2}(s/2-t)^{d-1}\,dt
=c_d s^d,\qquad c_d=\frac{\omega_{d-1}}{d2^{d-1}},
\]

mit omega_n=pi^(n/2)/Gamma(n/2+1). Insbesondere c_2=1/2 und c_4=pi/24.
Translation und Lorentztransformation erhalten das Volumen. Deshalb gilt
auch für verschobene und geboostete innere Intervalle

\[
\frac{V(I(p,q))}{V(D)}=\left(\frac{\tau(p,q)}T\right)^d=\theta^d.
\]

Nun seien X_1,...,X_m iid mit Verteilung dV/V(D). K zählt die X_i in I(p,q),
ohne die markierten Endpunkte; N=m+2. Bedingt auf p,q gilt

\[
K\sim\operatorname{Binomial}(m,\theta^d),\qquad
\widehat\theta=(K/m)^{1/d}.
\]

Dies beweist das endliche Zählmodell. Die Punktschätzung ist wegen der
konkaven Wurzel im Allgemeinen nach unten verzerrt. Für festes theta folgt
Konsistenz aus dem Gesetz der großen Zahlen, aber keine endliche exakte
Rekonstruktion aus einer einzelnen Ordnung. Die Vollständigkeit der Daten
und das Stichprobengesetz sind Annahmen, die ein Poset allein nicht beweist.

## 2. Fehlergrenze ohne Monte-Carlo-Näherung

Für beobachtetes k sind L_k,U_k die zweiseitigen Clopper-Pearson-Grenzen für
a=theta^d beim Konfidenzniveau 1-alpha:

\[
L_0=0,\quad L_k=B^{-1}_{\alpha/2}(k,m-k+1)\ (k>0),
\]
\[
U_m=1,\quad U_k=B^{-1}_{1-\alpha/2}(k+1,m-k)\ (k<m).
\]

Damit gilt unter den genannten Bedingungen für jedes feste Endpunktpaar

\[
\Pr\{\theta\in[L_K^{1/d},U_K^{1/d}]\mid p,q\}\ge1-\alpha.
\]

Dies ist eine häufigkeitsstatistische Deckungsgarantie für das Verfahren,
keine nachträgliche 95%-Wahrscheinlichkeit für einen festen Parameter.
Die Gültigkeit folgt analytisch; eine Simulation kontrolliert nur die
numerische Implementierung an ausgewählten Fällen. Sie beweist keine
gleichmäßige Gültigkeit über nicht getestete Modelle.

Für k=0 ist die obere Grenze
[1-(alpha/2)^(1/m)]^(1/d), nicht null. Weiter gilt
P(K=0)=(1-theta^d)^m. Mindestens einen Punkt mit Wahrscheinlichkeit 1-delta
zu sehen erfordert

\[
m\ge\left\lceil\frac{\log\delta}{\log(1-\theta^d)}\right\rceil.
\]

Das ist nur eine Nachweis-/Auflösungsbedingung, keine Genauigkeitsgarantie.
RMSE und Bias werden separat durch endliche Binomialsummen ausgewertet.
Die Formeln sind exakt; die gespeicherten Zahlen sind float64-Auswertungen.

**Bedingte Erweiterung bei bekanntem Modellfehler:** Bleiben die
Intervallindikatoren iid Bernoulli mit Erfolgswahrscheinlichkeit a, und liegt
eine unabhängig begründete Schranke |a-theta^d|<=epsilon_a vor, so überdeckt

\[
[\max(0,L_K-\epsilon_a)^{1/d},
 \min(1,U_K+\epsilon_a)^{1/d}]
\]

theta ebenfalls mit mindestens 1-alpha. Die Aussage folgt durch Einschluss
der möglichen theta^d-Werte. Für unbekannte Dichte, Krümmung, Randabschneidung
oder abhängige Punkte wird hier **keine solche Schranke behauptet**. Bei
Abhängigkeiten gilt zudem die Binomialinversion nicht ohne neuen Nachweis.

## 3. Konkreter Kausalitäts- und Datenintegritätstest

`validate_order` verarbeitet eine vollständige binäre Relation und prüft:

1. Irreflexivität: kein C_ii=1.
2. Asymmetrie: keine gegenseitigen Relationen.
3. Azyklizität durch topologisches Entfernen, einschließlich längerer Zyklen.
4. Transitivität: C_ij=C_jk=1 verlangt C_ik=1; Fehler liefern ein Gegenbeispiel.
5. Der Zähladapter verlangt zusätzlich gültige, geordnete Markierungen.

Es erfolgt keine automatische Reparatur. Ein Zyklus in gelieferten Daten ist
zunächst ein Widerspruch zur angenommenen Ordnungsdarstellung, kein Nachweis
physikalischer Zeitreisen. Eine nichttransitive Hasse-Matrix kann lediglich
eine andere Darstellung sein; deshalb ist das Eingabeformat entscheidend.

Mit **unabhängig bekannten Koordinaten und Metrik** prüft `embedding_audit`
zusätzlich jede Relation gegen den Kegeltest. Ohne diese Zusatzdaten können
falsche, aber weiterhin transitive Relationen unbemerkt bleiben. Identische
endliche Vergangenheits-/Zukunftsprofile zweier Knoten werden ausdrücklich
nicht als Verletzung der Kontinuumsunterscheidbarkeit gewertet.

**Keine Minguzzi-Zertifizierung:** K-Kausalität, stabile Kausalität,
Reflektivität und kausale Kontinuität beziehen sich auf eine Raumzeit mit
topologischer und kausaler Struktur. Ein endlicher azyklischer Graph oder
eine endliche topologische Sortierung beweist diese Eigenschaften einer
unbekannten Raumzeit nicht. Die Diskretisierung der Topologie würde gerade
die relevanten Kontinuumsabschlussbedingungen verlieren.

Für die hier bekannte Minkowski-Geometrie ist stabile Kausalität analytisch
gesichert: t besitzt einen überall zeitartigen Gradienten; auch eine feste
Verbreiterung der Lichtkegel lässt t entlang zukunftsgerichteter kausaler
Kurven strikt wachsen. Der Computertest prüft, ob die diskreten Daten zu
dieser bekannten Geometrie passen. Er entdeckt keine allgemeine
Kontinuumseigenschaft aus unbekannten Daten.

## 4. Begrenzte numerische Kontrolle

[contract.json](contract.json) fixiert d=2,3,4; m=256,1024; theta=0.1,0.5;
zentrale sowie verschobene/geboostete Intervalle; 2.048 neue Wolken je Zelle.
Die Endpunkte sind vorab fest und das gesamte Intervall bleibt eingeschlossen.
Insgesamt 24 Zellen und 49.152 Wolken. Das Ergebnis gilt bedingt auf diese
festen theta-Werte; es ist nicht direkt mit der über zufällige Endpunkte
gemittelten RMSE der ursprünglichen Studie vergleichbar.

Der gleichmäßige Diamantsampler zieht eine Zeitscheiben-Halbbreite
A=(T/2)U^(1/d), ein unabhängiges Vorzeichen und t=sign*(T/2-A). Anschließend
wird eine gleichmäßige (d-1)-Kugel mit Radius A beprobt. Die Zeitdichte ist
damit proportional zum räumlichen Querschnitt; sie ist nicht uniform in t.

Zwei vorab gewählte Binomialtests je Zelle prüfen die Summe der K-Werte und
die beobachtete Deckung gegen die jeweiligen exakten Modellverteilungen.
Bonferroni kontrolliert das gemeinsame Fehlalarmniveau auf 1%. Ein
Nichtverwerfen beweist das Modell nicht. Bias/RMSE sind beschreibende
Kontrollen; es wird keine Mindestleistung nachträglich ausgewählt.

Die K-Werte aller Replikate werden gespeichert. Zwölf vollständige
Relationsmatrizen prüfen zusätzlich den Datenweg vom bekannten Raumzeitmodell
über die Relation zum Intervallzähler und zum bisherigen Merkmalsextraktor.
Aufbau und Analyse aller vollständigen Matrizen sind nicht Teil dieses
Laufzeitbudgets. Seeds und feste Softwareversionen erlauben die Wiederholung;
gleiches Ergebnis ist keine unabhängige Replikation.

## 5. Reproduktion und Ergebnis

Vom Repository-Stamm, mit installierten Versionen aus requirements.txt:

```sh
python research/lorentz_proper_time_domain/run.py
python research/lorentz_proper_time_domain/verify.py
```

Der Runner überschreibt keine Ergebnisse. Ein Wiederholungslauf erhält einen
neuen Pfad, beispielsweise als zweites CLI-Argument ` /tmp/x6-domain-replay`.
Der Prüfer akzeptiert denselben Ergebnisverzeichnispfad als Argument.
`freeze.json` wird vor der ersten Zielziehung geschrieben; dies ist lokale
Quellenfixierung, keine externe Präregistrierung.

[Ergebnisbericht](results/RESULTS.md), [vollständige Zusammenfassung](results/summary.json),
[Rohzählungen](results/counts.json), [Gegenprüfung](results/verification.json).

## 6. Quellen und Anspruchsgrenzen

- [NIST: Exact binomial confidence limits](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbici.htm).
  Grundlage der Intervallinversion; Anwendung auf theta erfolgt durch die
  hier begründete monotone Transformation.
- E. Minguzzi, [Lorentzian causality theory](https://doi.org/10.1007/s41114-019-0019-x),
  Living Reviews in Relativity 22,3 (2019), insbesondere der Kausalitätsleiter
  und der Äquivalenz von K-Kausalität und stabiler Kausalität (Theorem 4.99).
- M. Braun, [Spacetime reconstruction by order and number](https://arxiv.org/html/2507.01907v1),
  Theorem 1.4. Seine Aussagen über Verteilungen aller endlichen
  Stichprobengrößen, bei zusätzlichen geometrischen Voraussetzungen und
  gleichem Gesamtvolumen, werden hier nicht als endlicher Fehlersatz benutzt.

Eigener Beitrag dieses Pakets: expliziter Gültigkeitsvertrag, nachvollziehbare
Anwendung bekannter Statistik, endliche Integritätsprüfungen mit Gegenbeispielen
und begrenzte numerische Reproduktion. Kein mathematischer Prioritätsanspruch.
