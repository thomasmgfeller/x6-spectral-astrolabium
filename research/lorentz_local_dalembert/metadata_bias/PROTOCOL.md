# Metadatenabhängige Bias-Korrektur: vorab festgelegter Pilot

Die früheren 64 Wolken sind Training (60 bisher nutzbar), die früheren 32
Wolken werden ausdrücklich Entwicklung/Residualkalibrierung (30 nutzbar).
Sie sind keine unabhängige Bestätigung der neuen Methode. 32 neue Seeds
70210000–70210031 sind ausschließlich Test. Kein Ersatz ausgefallener Wolken.
Alle Felder einer Wolke bleiben in derselben CV-Falte; Bootstrap zieht Wolken,
nicht Feldantworten. Sechs Trainingsfelder und vier neue Transferfelder sind
vorab in contract.json festgelegt. Transferfelder werden vor dem Freeze nicht
ausgewertet. Dichte, flaches 2+1-Modell und IID-Feldrauschen bleiben fest.

## Warum kein pauschaler Biasvektor?

Ein feldunabhängiger additiver Offset zerstört Linearität und den Nullwert auf
konstanten Feldern. Deshalb untersuchen wir eine explizit eingeschränkte Variante:
metadatenabhängige, **feldlineare** Korrektur ausschließlich im Nullraum der neun
rekonstruierten linearen/quadratischen Momentbedingungen. Das ist eine Änderung
der Operatorgewichte, keine Verbesserung der rekonstruierten Koordinaten.

Für jeden der zwei bisherigen Geometriearme sei D die Momentmatrix, a der
unveränderte Minimum-Rausch-QP-Vektor und H=I+11ᵀ. Zwei vorab gewählte kubische/
quartische Formvektoren werden auf ker(D) projiziert und in H orthonormalisiert:
DQ=0, QᵀHQ=I. Dann a'=a−sqrt(aᵀHa) Q alpha(m). alpha ist eine Ridge-Regression
mit höchstens acht Koeffizienten je Arm (zwei Formen mal Intercept/drei Merkmale).
Die Koeffizientenauswahl verwendet nur Trainingswolken, fünf Wolkenfalten und
den deklarierten Ridge-Raster. Eine Metadaten-freie Variante mit zwei Koeffizienten
dient als Ablation. Sie wird separat über denselben Raster ausgewählt.

Da a die bedingte Rauschvarianz minimiert, ist aᵀHQ=0. Somit wächst die Varianz
um den Faktor 1+||alpha||². Normbegrenzung auf sqrt(0.25) begrenzt den Faktor auf
1.25; eine unabhängige direkte Nachrechnung prüft dies. Außerhalb des komponenten-
weisen Trainingsbereichs der Metadaten wird a unverändert verwendet. Konstanten,
Linearität und die rekonstruierten quadratischen Momente bleiben erhalten.
Das ist keine Garantie für Momente in den unbekannten wahren Koordinaten.

## Getrennte Unsicherheit und Vergleich

Sechs Arme: ursprünglicher QP, Metadatenkorrektur, bisherige euklidische Relations-
projektion, Projektion+Metadatenkorrektur sowie je eine Metadaten-freie Ablation.
**Die Projektion ist die bisherige, keine neue kovarianzgewichtete Projektion.**
Weder Referenz noch Kandidat erhält einen nachgelagerten globalen Feld-Offset;
der Vergleich betrifft lineare Operatoren. Daher sind die Posteriorzahlen nicht
identisch definiert wie im früheren Ein-Feld-Piloten.

Alle sechs Gewichte werden VOR Kenntnis der Feldwerte/Simulationswahrheit fixiert.
N(C)=sigma² B Bᵀ wird danach mit den tatsächlich verwendeten Gewichten neu
gerechnet, einschließlich Root und sämtlicher Kreuzterme. Die saubere Residual-
kovarianz G und der Residualmittelwert mu werden separat auf den früheren 32
Wolken und den sechs Trainingsfeldern geschätzt. Als konservativer Arbeitswert
für den skalaren Ein-Schritt-Filter dient R=G+mu muᵀ+N(C), also ein zweites
Fehlermoment, keine als exakt behauptete bedingte Kovarianz. Die Residualmittel
werden NICHT abgezogen; Kalibrier-/Modellparameterunsicherheit ist nicht vollständig
erfasst. Keine erneute Addition bereits verrauschter Streuung. Kein gemeinsamer
Fusionsgewinn wird in diesem Pilot beansprucht.

Primär: saubere RMSE auf vier neuen Transferfeldern; zusätzlich Bias, zentrierte
Streuung, Einzel-Feld-Werte, verrauschte RMSE, Posterior-RMSE, nominelle Überdeckung,
vorab über Trainingsquantile definierte Rauschgruppen, Ausfall-/OOD-Quote und Budget.
Alle Mittel gewichten jede Wolke gleich. Felder sind keine unabhängigen Replikate.
Bootstrap konditioniert auf die eingefrorene Kalibrierung und belegt keine Garantie.
Prädiktionsfehler und Feldrauschen sind synthetisch und unabhängig erzeugt.

## Abbruch und Grenzen

Der vollständige Code, Vertrag und gefittete Parameter werden vor Generierung
neuer Testwolken committed und veröffentlicht. Laufprogramme prüfen diese Bindung.
Die Kriterien aus contract.json bleiben bei negativem Ergebnis unverändert.
Quellartefakte, Archive und Ausführungsprotokolle werden mit SHA256 gebunden.

Einbettungskovarianz fehlt weiterhin: wechselnde Stützmengen, gemeinsame
Intervallzählungen, gewählter Lorentz-Bezugsrahmen, diskrete Auswahl und aktive
Relationsbedingungen verhindern die Identifikation mit der bisherigen 2×2-
Operatorfehlerkovarianz. Der nächste dafür notwendige Schritt wäre eine separat
definierte, bezugsrahmenbereinigte Koordinatenfehler-Kalibrierung und unabhängige
Validierung. Eine heuristische Skalierung hebt diese Blockade nicht auf.
Gemeinsame Geometrie-/Bias-Schätzung bleibt bis zu einem Identifizierbarkeitsnachweis
zurückgestellt. Zukunftsstützen bleiben vorhanden: keine Online-Freigabe.
