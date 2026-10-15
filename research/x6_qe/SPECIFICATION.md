# Wissenschaftlicher Vertrag und Grenzen

Version 0.1.0, 15. Oktober 2026. Maßgebliche ausführbare Angaben: `contract.json`
und `inputs.json`. Die fehlenden Formeln des ursprünglichen Ideentextes wurden
nicht als vorliegende Spezifikation behandelt. Dieses Modul definiert einen
neuen, ausdrücklich beschränkten Referenzumfang.

## Fragestellung

Welche vorab festgelegten relationalen Merkmale unterscheiden endliche Graphen,
die von bestimmten spektralen Observablen nicht unterschieden werden?

Spektrale Universalität (Levelstatistik), Quanten-Ergodizität (Dichte-eins-
Gleichverteilung), QUE und vollständige Isospektralität sind verschiedene Begriffe.
Hier wird ausschließlich endliche Isospektralität untersucht. Es wird kein
semiklassischer Grenzübergang, keine Dynamik und keine zunehmende Universalität
simuliert. Die Information eines unitär entwickelten Gesamtzustands wird nicht
als vernichtet bezeichnet.

## Objekte und Konventionen

Endliche einfache ungerichtete ungewichtete Graphen, Knoten 0 bis n−1,
symmetrische Adjazenzmatrix A, Null-Diagonale. Gespeicherte Kanten sind eindeutige,
lexikographisch sortierte Paare u<v. Negative Indizes, Boolesche Zahlen-Aliase,
Schleifen, Mehrfachkanten und unbekannte Felder sind unzulässig.

Stern: Zentrum 0, Blätter 1,…,6. C4: Ring 0–1–2–3–0.
Die beiden 16-Knoten-Graphen haben Knoten (i,j) in Z4×Z4, Index 4i+j.
Im Turmgraphen sind verschiedene Knoten benachbart, wenn eine Koordinate gleich
ist. Im Shrikhande-Graphen liegen die Differenzen in
{(±1,0),(0,±1),(1,1),(−1,−1)} modulo 4.

Das Adjazenzpolynom ist det(tI−A), Koeffizienten absteigend, monisch.
Es ist kein Graph-Laplacian und kein Lorentz-Operator. Ein späterer PDE-Solver
muss seine eigene Diskretisierung samt Massenmatrix und Randbedingungen prüfen.

Für orientierte Kanten (u,v), (x,y) gilt T[(u,v),(x,y)]=1 genau dann, wenn v=x
und y≠u. Verwendet wird

\[
Z_G(u)^{-1}=\det(I-uT)
=(1-u^2)^{m-n}\det(I-uA+u^2(D-I)).
\]

Gespeichert wird das reziproke Zeta-Polynom in aufsteigender Reihenfolge,
ohne abschließende Nullkoeffizienten. Primitive Zyklen haben keine unmittelbare
Umkehr, auch nicht am Zusammenschluss, und sind keine Wiederholungen kürzerer
geschlossener Wege. Zyklische Startpunktverschiebungen werden identifiziert,
entgegengesetzte Orientierungen nicht. Die explizite Zyklusaufzählung ist auf
Stern/C4 und Längen 1 bis 8 begrenzt. Im C4 sind nur die beiden Orientierungen
der Länge 4 primitiv; eine doppelte Umrundung der Länge 8 ist nicht primitiv.

Für d-reguläre Graphen folgt aus D=dI, dass Z durch das vollständige
Adjazenzspektrum bestimmt ist. Damit ist Z keine allgemein unabhängige
Informationsschicht. Der K4-Separator ist ein kombinatorisches Merkmal; er
beweist weder topologische Schutzwirkung noch Gedächtnis.

## Exaktheit und Gegenprüfung

Zwei Polynome vom Grad höchstens d stimmen identisch überein, wenn sie an d+1
verschiedenen Punkten übereinstimmen. Die Bareiss-Prüfung nutzt n+1 Punkte für
das Adjazenzpolynom, 2m+1 für die Ihara-Bass-Identität bei m≥n. Beim Stern wird
die Gleichung mit (1−u²) multipliziert und an max(2m,2n)+1 Punkten geprüft;
so wird auch bei u=1 keine Division durch null vorgenommen. Dies ist ein
exaktes Polynomzertifikat, kein numerischer Stichprobentest.

Für die regulären Graphen liefert A²=4I+2J zusammen mit Grad 6 und Spur 0 das
Spektrum 6 (einmal), 2 (sechsmal), −2 (neunmal). Positive Nebendiagonale von
A² stellt Zusammenhang sicher. Das K4-Zählen nutzt zusätzlich
sum_v tr(A[N(v)]³)/24: jedes K4 wird viermal mit sechs Dreiecksorientierungen
gezählt. Diese Referenzen waren vor der Implementierung bekannt.

## Schlussfolgerungen

Die drei festgeschriebenen Ergebnisse sind Replikationen mathematischer
Referenzen. Software-PASS bedeutet korrekte Reproduktion einschließlich
erwarteter Grenzen. Die ursprünglichen U/B/T/A-Hypothesen sind NOT_TESTED.
U→B→T→A darf später eine Arbeitsreihenfolge bezeichnen, keine Kausalkette und
keine garantierte Zerlegung unabhängiger Informationen.

Wenn Primzahlstatus P(k) allein aus dem Grad k berechnet wird, liefert P(k)
bedingt auf vollständig bekanntem k keine zusätzliche Information. Ein späterer
Primzahltest muss daher einen ausdrücklich begrenzten Vorhersagevergleich gegen
vorab festgelegte Modelle definieren. Ihara-primitiv ist nicht zahlentheoretisch
prim. Ein nichtsignifikanter Test beweist kein Nichtvorhandensein eines Effekts.
