# Mathematischer Rahmen des 4D-Poisson-Piloten

Alle Aussagen beziehen sich auf flache 3+1-Minkowski-Geometrie mit c=1,
fünf festgelegten affinen Landmarken, bekannter Dichte und zwei Stützpunkten.

## 1. Exakte disjunkte Bereiche einer Kette

Seien e0 < e1 < ... < e6 streng zeitartig geordnet. Schreibe
I(i,j)=I(ei,ej), V(i,j)=Vol(I(i,j)); für i>=j setze I leer und V=0.
Im äusseren Intervall I(0,6) definiere für i<j

    A(i,j) = I(i,j) \ ( I(i+1,j) union I(i,j-1) ).

Für jeden Hintergrundpunkt x in I(0,6) ist i der grösste Kettenindex mit
ei < x und j der kleinste Index mit x < ej. Wegen der Transitivitität ist
i<j. Genau diese beiden Indizes ordnen x eindeutig A(i,j) zu. Grenzen
haben bezüglich des 4-Volumens Mass null. Die 21 Mengen A(i,j) bilden
folglich eine disjunkte Zerlegung des äusseren Intervalls.

Aus der Kettenordnung folgt

    I(i+1,j) intersection I(i,j-1) = I(i+1,j-1).

Inklusion-Exklusion liefert deshalb exakt

    v(i,j) = V(i,j)-V(i+1,j)-V(i,j-1)+V(i+1,j-1).

Insbesondere ist v(i,j)>=0. In vier Dimensionen gilt

    V(i,j) = (pi/24) * tau(i,j)^4 = (pi/24) * s(i,j)^2,

wobei s<0 das vorzeichenbehaftete Intervallquadrat ist. Die Koordinaten
dieses Experiments sind rational; s^2 und alle Bereichsvolumina nach
Division durch pi/24 werden exakt rational berechnet. Bei vorgegebenem
M=E[N(0,6)] ist der Bereichsmittelwert

    lambda(i,j) = M * v(i,j)/V(0,6).

Der gemeinsame Faktor pi/24 fällt heraus. Es gibt keine angenäherte
Überlappungsintegration und kein Histogramm als Ersatz des Raumzeitmodells.

Für einen homogenen Poisson-Prozess sind die Zählungen Y(i,j) der disjunkten
Bereiche unabhängig mit Mittelwert lambda(i,j). Dann sind die
Intervallzählungen exakt

    N(a,b) = sum_{i>=a, j<=b, i<j} Y(i,j).

Für zwei Intervalle ergibt sich insbesondere

    Cov(N(a,b),N(c,d)) = rho * V(max(a,c),min(b,d)).

Das folgt entweder aus der gemeinsamen Bereichssumme oder direkt aus der
Poisson-Zählmasse der Schnittmenge. Die implementierten rationalen
Kontrollen prüfen diese Identität für sämtliche 21x21 Paare jeder Geometrie.
Die erzeugten primären Zählungen haben somit analytisch das vollständige
gemeinsame Gesetz des deklarierten Hintergrundprozesses. Software zieht
Poisson-Zufallszahlen mit Float64-Mittelwerten; dies ist keine formale
Verifikation der PRNG-Implementierung oder der Rundung.

Fest eingefügte Landmarken sind nicht Teil dieses zufälligen Hintergrunds.
In einer Rohzählung einschliesslich aller eingefügten Kettenereignisse gilt
N_raw(i,j)=N(i,j)+(j-i-1). Eine datenabhängige Auswahl von Landmarken aus
demselben Prozess fällt nicht ohne Weiteres unter diesen Satz.

## 2. Rekonstruktion aus 20 Intervallzählungen

Die beobachtete Maske enthält alle zehn Landmarken-Landmarken-Intervalle
und alle zehn Landmarken-Stützpunkt-Intervalle. N(p,q) ist zurückgehalten.
Für jedes verwendete zeitartige Intervall wird

    s_hat(i,j) = -sqrt(24 N(i,j)/(pi rho))

gebildet. Daraus folgen für i,j=1,...,4

    G_hat_ij = (s_hat(0,i)+s_hat(0,j)-s_hat(i,j))/2,
    d_hat_i = (s_hat(0,p)-s_hat(i,p)-s_hat(0,q)+s_hat(i,q))/2.

Für exakte Eingaben gilt G=E^T eta E mit den affinen Landmarkendifferenzen
als Spalten von E. Bei vollem Rang folgt

    tau(p,q)^2 = -d^T G^(-1) d.

Dies definiert den Plug-in-Schätzer. Nur ein negatives und drei positive
Eigenwerte, hinreichende numerische Nichtsingularität und eine positive
endliche Eigenzeitschätzung werden akzeptiert. Eine verworfene Schätzung
zählt im Genauigkeits-Gate als Ausfall. Die Signatur wird nicht durch
Ersetzen von Eigenwertvorzeichen erzwungen.

## 3. Simultane Poisson-Mittelwertregion

Für jede der m=20 marginalen Beobachtungen k benutze zentrale
Garwood-Grenzen mit alpha=0.05 und a=alpha/(2m):

    L(k) = 0                         für k=0,
    L(k) = chi2_quantile(a,2k)/2      für k>0,
    U(k) = chi2_quantile(1-a,2(k+1))/2.

Jedes Mittelwertintervall hat mindestens 1-alpha/m Überdeckung. Die
Vereinigungsabschätzung garantiert mindestens 1-alpha gemeinsame
Überdeckung, unabhängig von den Abhängigkeiten der Zählungen. Dabei ist
die Beobachtungsmaske fest und die Dichte bekannt.

Die monotone Transformation s=-sqrt(24 lambda/(pi rho)) liefert gleichzeitig
gültige Intervalle [s_lo,s_hi]. Um den Punktschätzer setze

    e_s = max(abs(s_hat-s_lo),abs(s_hi-s_hat)).

Da G und d lineare Funktionen von s sind, ergeben Dreiecksungleichungen
komponentenweise Radien E_ij und e_d_i. Für die Diagonale ist E_ii=e_s(0,i),
für Nebendiagonalen die halbe Summe der drei beteiligten Radien; für d_i
die halbe Summe der vier Radien. Korrelationen werden für die Gültigkeit
der Region nicht ignoriert, aber ihre Struktur wird zur Verengung dieser
rechteckigen Region nicht ausgenutzt.

## 4. Explizite Fehlerfortpflanzung und ihre Grenzen

Diagonalisiere die symmetrische beobachtete Matrix G_hat=Q Lambda Q^T.
Für invertierbares G_hat sei T=Q |Lambda|^(-1/2). Dann ist
T^T G_hat T=J eine Diagonalmatrix aus Vorzeichen mit ||J^-1||_2=1.
Die nachfolgende Transformation hängt nur von den Beobachtungen ab.

Für jede in der gemeinsamen Region enthaltene wahre Matrix gilt

    ||T^T (G-G_hat) T||_2 <= || |T|^T E |T| ||_F = epsilon.

Mit d_bar=T^T d_hat, D=||d_bar||_2 und
delta=|| |T|^T e_d ||_2 gilt zugleich
||T^T(d-d_hat)||_2<=delta. Falls epsilon<1, liefert die Neumann-Schranke

    ||(T^T G T)^-1||_2 <= 1/(1-epsilon),
    ||(T^T G T)^-1-J^-1||_2 <= epsilon/(1-epsilon).

Für q=tau^2 und q_hat=-d_hat^T G_hat^-1 d_hat folgt daraus

    |q-q_hat| <= B,
    B = (D^2 epsilon + 2 D delta + delta^2)/(1-epsilon).

Der Beweis zerlegt die Differenz der quadratischen Formen in eine Änderung
der inversen Matrix bei festem d_bar und die beiden linearen sowie den
quadratischen Term der Vektoränderung. Operatornorm und Cauchy-Schwarz
liefern die drei Summanden. Diese Argumentation gilt deterministisch für
jeden Punkt der simultanen Eingaberegion, auch bei datenabhängigem T.

Für positive wahre Eigenzeit ist folglich

    tau in [sqrt(max(0,q_hat-B)), sqrt(q_hat+B)]

sofern die obere Wurzel definiert ist. Falls die ausreichenden Voraussetzungen
nicht geprüft werden können, wird [0,+infinity] ausgegeben. Dies erhält die
Überdeckung, liefert aber kein endliches Präzisionszertifikat.

Ein Intervall [l,u] mit l>0 zertifiziert höchstens 10% relativen Fehler des
Punktschätzers, wenn

    l >= tau_hat/1.1  und  u <= tau_hat/0.9.

Das mathematische Überdeckungsargument setzt exakte Quantile und Normen
voraus. Die vorliegenden Auswertungen verwenden Float64 und sind keine
nach aussen gerundeten numerischen Beweise. Kein Lauf erfüllt die
10%-Zertifikatsbedingung; es wird folglich auch kein solches numerisches
Zertifikat als gesichert ausgegeben.

## 5. Was das bestandene Genauigkeits-Gate bedeutet

Die Erfolgswahrscheinlichkeit wird bei jeder Geometrie durch 512 unabhängige
Hintergrundprozesse geprüft. Der Erfolg ist vorab als gemeinsames Ereignis
aus Struktur-, Mindestzähl- und 10%-Genauigkeitskriterium definiert. Bei K
Erfolgen aus n Wiederholungen lautet die einseitige Untergrenze

    p_lower = Beta_quantile(0.05/20; K, n-K+1),

mit p_lower=0 bei K=0. Bonferroni sichert die 20 Aussagen gleichzeitig mit
mindestens 95% Konfidenzniveau. Primär ist ausschliesslich die zuvor
festgelegte höchste Dichte; es wurde nicht nach dem besten getesteten
Dichteniveau gewählt. Die kleinste Untergrenze 0.98407348 erfüllt die
geforderte Schwelle 0.9.

Das ist eine statistische Aussage über wiederholte Versuche an diesen
festen Geometrien unter dem festgelegten Modell. Sie ist weder eine
beobachtungsspezifische Fehlergrenze für eine einzelne unbekannte Geometrie
noch eine Aussage über eine beliebige Population neuer Geometrien.

## 6. Fachliche Konsequenz

Die Ergebnisse rechtfertigen weitere Arbeit an der 3+1-Rekonstruktion.
Sie belegen noch keinen nutzbaren zertifizierten 4D-Operator. Das exakte
gemeinsame Zählgesetz eröffnet jetzt eine konkrete Prüfung, ob eine
gemeinsame Konfidenzregion samt geometrischer Konsistenzbedingungen die
rechteckigen Eingabebereiche hinreichend schärfen kann. Dafür müssen neue
Akzeptanzkriterien vor weiteren Versuchsläufen festgelegt werden.
