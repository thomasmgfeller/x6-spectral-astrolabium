# Warum höhere lokale Ordnung die fehlende Quelle nicht heilt

Diese analytische Einordnung ergänzt den Methodenvertrag. Sie verändert
weder den festgelegten Lauf noch dessen Fehlerbudgets und ist kein neuer
statistischer Test der acht Archivwolken.

Für den unveränderten Bump verschwinden außerhalb r<1/2 sämtliche lokalen
Ableitungen. Jede endliche lokale Taylor-History, die nur solche Jets am
jeweiligen ursprünglichen Knoten verwendet, erhält deshalb dort null.
Fehlt ein History-Knoten in der Quellstütze, enthält diese ganze
Adapterklasse keine Information über die Quelle. Auch H3 oder H5 kann
dieses Problem nicht allein durch höhere Ordnung beseitigen.

Im idealen homogenen Poisson-Modell lässt sich die Häufigkeit eines solchen
Informationsverlusts vor jeder Simulation berechnen. Die relevante Region
ist die Schnittmenge von Omega4, t<=-1 und r<1/2. Ihr Volumen ist

    V_history_source = 4*pi * integral_0^(1/2) r^2*(3-r) dr = 7*pi/16.

Mit Vol(Omega4)=512*pi/3 und nu=512 ist die erwartete Punktzahl darin

    lambda = nu * 21/8192 = 21/16.

Damit beträgt die Wahrscheinlichkeit einer leeren lokalen Quellhistory
im idealen Poisson-Modell exakt exp(-21/16), ungefähr 26,9 Prozent.
Das ist eine Modellrechnung, keine aus drei von acht Wolken geschätzte
Populationswahrscheinlichkeit und kein Beweis über den endlichen
binary64-Sampler. Es betrifft das Sampling des Adapters, nicht eine
universelle Quantengravitationsfluktuation.

Eine Forderung P(leer)<=delta verlangt für diesen lokalen Adapter bereits
nu >= (8192/21)*log(1/delta). Das ist ausschließlich eine notwendige
Quellverfügbarkeitsbedingung. Sie gibt keine ausreichende Dichte für
History-Genauigkeit, Operatorqualität, G1, Detektorintegration oder
physikalischen Fluktuationstransfer an. Die alten D20-Zulässigkeitsgrenzen
werden dadurch nicht verändert.

Ein weiterführender Adapter muss daher die Anfangsdaten über eine
ausdrücklich definierte räumlich nichtlokale Abbildung auf die vorhandenen
Knoten übertragen oder eine begründete andere diskrete Anfangswertformulierung
verwenden. Eine Möglichkeit zur Untersuchung ist eine konservative
Projektion mit Partition der Eins und kontrollierter Rekonstruktionsweite.
Sie müsste aus denselben f,g abgeleitet werden, Konstanten und relevante
Wellen kontrollieren und ihren Fehler bis T*h einschließen. Das wäre eine
neue Methodenentscheidung, noch kein in v0.10 getestetes Verfahren.

Insbesondere zählen das Verbreitern der physikalischen Quelle, das
unbemerkte Hinzufügen günstiger Knoten und das Nachziehen leerer Wolken
nicht als Lösung. Eine exakte Kontinuumshistory bleibt als Orakelvergleich
nützlich, beweist aber nicht die Existenz oder Güte einer eigenständigen
intrinsischen Anfangsdatenabbildung.
