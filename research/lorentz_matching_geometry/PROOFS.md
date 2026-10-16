# Knoten-Zuordnung und die gemeinsame mittlere Schicht

Dies sind Aussagen über endliche binäre Matrizen und spezifizierte Schichtungen.
Sie enthalten weder eine Geometrie- noch eine Neuheitsbehauptung. Die
[Zweischicht-Inversion aus PR #39](../lorentz_relational_boundary/PROOFS.md)
wird verwendet; der neue Punkt ist die explizite gemeinsame Zuordnung.

## 1. Nummerierungsunabhängige Entscheidung mit Zeugen

Seien A und B binäre m×u-Matrizen. Für eine bereits teilweise festgelegte
Zeilenbijektion p auf I betrachten wir die Multimengen der eingeschränkten
Spaltenvektoren:

\[
\{\!\{(A_{ij})_{i\in I}:1\le j\le u\}\!\}
=\{\!\{(B_{p(i)j})_{i\in I}:1\le j\le u\}\!\}.
\]

Diese Gleichheit ist notwendig für jede Fortsetzung zu einer Isomorphie.
Ebenso notwendig sind die erhaltenen Zeilengrade und die erhaltenen
paarweisen Schnittzahlen einschließlich ihrer Zeilenhistogramme. Die Suche
verwirft ausschließlich Verletzungen solcher notwendigen Bedingungen und
probiert alle verbleibenden Zeilenzuordnungen durch.

Bei I={1,…,m} ist die Multimengengleichheit auch hinreichend: Spalten mit
demselben vollständigen Vektor werden bijektiv gepaart, einschließlich
wiederholter und leerer Spalten. Damit entstehen explizite p und q mit
A[i,j]=B[p(i),q(j)] für sämtliche Einträge. Dieser gesamte Gleichheitstest
wird nach jeder positiven Entscheidung erneut ausgeführt.

Die Suche ist daher vollständig, **wenn sie ohne Ressourcenabbruch endet**.
Ein erschöpftes Suchbudget liefert `INCONCLUSIVE`, niemals `NONISOMORPHIC`.
Aus indizierten Schnittzahlen werden zunächst die Spaltenmultimengen durch
Möbius-Inversion rekonstruiert; derselbe Vergleich gilt anschließend für diese
Matrizen. Die Schnittdaten müssen vollständig sein, eine gültige Gradschranke
haben und Multiplizitäten einschließlich g(∅) enthalten.

Bei positiven Zweischichtenordnungen erkennt man untere und obere Seite an
den Vorgänger-/Nachfolgergraden. Der Zeuge wird auf die ursprünglichen
Knotenlabels zurückübersetzt und gegen die **vollständige gerichtete Relation**
geprüft. Isolierte Elemente sind im Matrixvergleich erlaubt; die automatische
Seitenerkennung des Ordnungsvergleichs lehnt sie ausdrücklich ab.

Dies ist ein exakter Referenzentscheider mit möglicher exponentieller Laufzeit,
keine kanonische Nummerierung und keine Lösung mit garantierter kurzer Laufzeit.
Bei Automorphismen können mehrere korrekte Zuordnungen existieren. Die Entscheidung
ist von der Nummerierung unabhängig; der ausgegebene einzelne Zeuge braucht es
nicht zu sein.

## 2. Warum zwei getrennte Rekonstruktionen nicht zusammenpassen müssen

Es seien L={l₁,l₂}, M={m₁,m₂}, U={u₁,u₂} angegeben, mit

\[
B=\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad
C=\begin{pmatrix}1&0\\1&1\end{pmatrix},\qquad
C'=\begin{pmatrix}1&1\\1&0\end{pmatrix}.
\]

B beschreibt L→M; C beziehungsweise C′ beschreibt M→U. In beiden Fällen
sei die vollständige Ordnung der transitive Abschluss dieser beiden Beziehungen.
Alle sechs Elemente liegen in den angegebenen positiven Schichten.

Die untere Beziehung B stimmt exakt überein. C und C′ stimmen nach Vertauschung
der mittleren Zeilen überein. Die beiden benachbarten Beziehungen sind deshalb
**jeweils einzeln isomorph**. Trotzdem ergeben sich für L→U die booleschen Produkte

\[
B\odot C=\begin{pmatrix}1&1\\1&1\end{pmatrix},\qquad
B\odot C'=\begin{pmatrix}1&1\\1&0\end{pmatrix}.
\]

Die vollständigen Ordnungen besitzen 3+3+4=10 beziehungsweise 3+3+3=9
strikte Relationen und sind daher nicht isomorph, auch ohne festgehaltene
Schichtlabels. Ein bloßes separates Zusammenpassen beider Seiten reicht
also nicht. Der Test prüft zusätzlich alle 6!=720 Knotenpermutationen.
Die Konstruktion wurde gezielt gewählt; globale Minimalität wird nicht behauptet.

## 3. Begrenzter Dreischicht-Rekonstruktionssatz

**Voraussetzungen.** L, M und U sind drei angegebene disjunkte Antiketten.
Es sind nur Beziehungen L→M und M→U als erzeugende Kanten erlaubt.
Die Ordnung ist genau deren transitiver Abschluss. Die Labels von L und U
bleiben erhalten. Für m∈M seien

\[
A_m=\{l\in L:l\prec m\},\qquad D_m=\{u\in U:m\prec u\}.
\]

Bekannt seien |M|, eine Schranke |Aₘ|+|Dₘ|≤d und sämtliche **gemeinsam
indizierten** Werte

\[
h(S,T)=\#\{m\in M:S\subseteq A_m,\ T\subseteq D_m\},
\quad S\subseteq L,\ T\subseteq U,\ |S|+|T|\le d.
\]

Nullwerte und h(∅,∅)=|M| gehören dazu. Die getrennten Randwerte h(S,∅)
und h(∅,T) allein sind nicht die hier vorausgesetzte Eingabe.

**Aussage.** Die Daten rekonstruieren die gesamte Ordnung bis auf **eine
gemeinsame Permutation der mittleren Elemente**, bei festen äußeren Labels.

**Beweis.** Da L und U disjunkt sind, kann man (S,T) als Teilmenge S∪T von
L⊔U auffassen. Die gesuchte Multiplizität jedes vollständigen Nachbarschaftspaars
(A,D) ist nach der Möbius-Inversion

\[
a(A,D)=\sum_{\substack{S\supseteq A,\ T\supseteq D\\|S|+|T|\le d}}
(-1)^{|S\setminus A|+|T\setminus D|}\,h(S,T).
\]

Man erzeugt a(A,D) mittlere Elemente mit genau diesen beiden Nachbarschaften.
Dies rekonstruiert beide angrenzenden Beziehungen mit derselben mittleren
Zuordnung. Nach Voraussetzung ist jede L→U-Relation genau dann vorhanden,
wenn mindestens eines dieser mittleren Elemente einen Weg vermittelt.
Ihr boolesches Produkt rekonstruiert deshalb auch die verbleibende Relation.
Weitere Relationstypen sind ausgeschlossen. Damit ist die gesamte Ordnung
bestimmt. ∎

Alternativ beschreibt die Matrix J=[B; Cᵀ] dieselbe Konstruktion: Ihre Zeilen
werden von L⊔U indiziert, ihre Spalten von M. Der Zweischicht-Matrixsatz auf J
rekonstruiert die **gepaarten** Nachbarschaften der mittleren Elemente.
Der Code prüft das vollständige Ergebnis für alle 16×16 Paare binärer
2×2-Matrizen, auch mit leeren Nachbarschaften bei vorgegebener Schichtzuordnung.
Diese Tests kontrollieren die Implementierung; den allgemeinen Satz trägt der Beweis.

### Voraussetzungen, die nicht entfallen dürfen

- **Direkte L→U-Verbindungen ohne mittleren Weg:** Sie sind aus h nicht
  erschließbar. Entweder werden sie ausgeschlossen, wie oben, oder zusätzlich
  als beschriftete Beziehung angegeben und beim Abschluss ergänzt.
- **Äußere Labels:** Ihre freie Zuordnung bleibt eine Isomorphieaufgabe mit
  erhaltener Aufteilung L/U. Der Satz löst sie nicht automatisch.
- **Gemeinsame statt getrennte Daten:** Die Kopplung von Aₘ und Dₘ ist notwendig;
  eine mittlere Multiplizität zählt das ganze Paar, nicht seine beiden Randwerte.
- **Speicher:** Bei r=|L|+|U| werden Σₖ₌₀ᵈ binomial(r,k) indizierte Einträge
  benötigt; im unbeschränkten Fall sind es 2ʳ. Kein allgemeiner Kompressionsvorteil.

Der Satz ist damit eine direkte endliche Anwendung klassischer Inversion,
kein Rekonstruktionssatz für beliebige Kausalmengen oder ihre Kontinuumsgeometrie.
