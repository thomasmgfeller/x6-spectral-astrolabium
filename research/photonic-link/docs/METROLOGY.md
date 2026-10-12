# Messplan und Unsicherheitsbudget

## Parameter, die eine reale Messung benötigt

| Größe / Einheit | Unabhängige Bestimmung | Wesentliche Verwechslungsmöglichkeit |
|---|---|---|
| R, erzeugte Paare/s | Quellcharakterisierung mit gesonderter Effizienz-/Mehrpaaranalyse | Helligkeit, Kopplung und Detektoreffizienz sind aus Einzelraten allein nicht getrennt bestimmbar |
| alpha L + Einfügedämpfung, dB | Kalibrierte Transmissionsmessung bei tatsächlicher Wellenlänge und Polarisation | Steckerverluste, PDL, Quellenänderung und Messleistungsdrift |
| Kopplung und Detektoreffizienz | Getrennte optische Referenz und Detektorkalibrierung mit Unsicherheit | Nur ihr Produkt ist im skalaren Zählmodell sichtbar |
| Dunkelzählrate pro Port, Hz | Quelle blockieren; gleiche Temperatur und Detektoreinstellungen | Raman-/Streulicht ist nicht notwendig dieselbe Statistik wie Dunkelrauschen |
| Totzeit, s | Interarrival-Histogramme und kontrollierte Ratenvariation pro Kanal | Nicht-/paralysierbare Totzeit, Nachpulse und Sättigung |
| Jitterverteilung, s | Gemeinsame kalibrierte Impulse; pro Kanal und Rate | Referenzpulsbreite, Quantisierung, DNL/INL, echte nichtgaußförmige Ausläufer |
| U_i(t), dimensionslose Winkel | Mindestens ausreichende nichtkommutierende Polarisationsmessungen; für allgemeine Zustände informationsvollständige Tomografie | Eine Eingabepolarisation bestimmt keine allgemeine SU(2)-Transformation |
| Zeitoffset, Skew und Drift | Zweiweg-/gemeinsame Referenz oder anderweitig bekannte Laufzeit; geprüfter Transfer | Einseitig gemessen sind Offset und Laufzeit nicht getrennt identifizierbar |
| Gemeinsamer Umwelteinfluss | Synchrone externe Sensoren und wiederholte Störungen | OU-Koeffizienten beschreiben zunächst ein statistisches Modell, keine gemessene Materialkonstante |

## Unsicherheiten weitergeben

Für eta=c*eta_det*10^(-ell/10) ist
d ln(eta)=d ln(c)+d ln(eta_det)-(ln(10)/10)d ell. Mit Parameterkovarianz Sigma
ergibt die lokale lineare Näherung u²(ln eta)=J Sigma Jᵀ. Korrelationen zwischen
Armen und Kalibrierungen dürfen nicht weggelassen werden. Diese Näherung ist
bei großen/asymmetrischen Unsicherheiten und nahe Parametergrenzen durch
Monte-Carlo-Propagation mit physikalisch zulässigen Verteilungen zu ersetzen.

Für eine Differenzzeit gilt grundsätzlich
Var(tA-tB)=Var(tA)+Var(tB)-2Cov(tA,tB). Ein gemeinsamer Takt ist deshalb anders
zu behandeln als unabhängige Uhren. Die aktuelle Simulation enthält unabhängigen
Detektorjitter und eine gemeinsame Pfadstörung; sie bildet nicht jede Form
korrelierten Taktjitterrauschens ab. Reale TDC-Kalibrierunsicherheit kommt hinzu.

Die Datei `evidence/experiments.json` zeigt Wiederholungsstreuung und Standardfehler
von Mittelwerten über unabhängige synthetische Seeds. Das ist **Monte-Carlo-
Unsicherheit unter festen Modellparametern**, keine Unsicherheit des realen
Aufbaus. Die Datei gibt keine QKD-Konfidenz oder geräteunabhängige Aussage aus.
Innerhalb eines Laufs können Fenster zeitlich korreliert sein.

Reale Daten erfordern geeignete unabhängige Blöcke bzw. einen validierten
zeitabhängigen Likelihoodansatz. Blockbootstrap ist erst nach Prüfung der
Blocklänge und Abhängigkeit sinnvoll. Ein naiver Binomialfehler über alle
Fenster oder eine iid-Hoeffding-Schranke über Driftblöcke ist nicht automatisch
gerechtfertigt. Kalibrierunsicherheit und systematische Modellabweichung werden
zusätzlich zu Zählstatistik berichtet.

## Gemeinsame Hardware-Datensätze

Jeder spätere Lauf benötigt mindestens: unveränderte lokale Tags je Station,
Port-ID, Zeit-Epoche/Einheit, tatsächliche Quantisierung, Kalibrier-ID,
Referenzpulse, Basisprotokoll, Temperatur-/Regelungsdaten, FIFO-/TDC-Fehler,
Start/Stop, Garantie zur Vollständigkeit, Prüfsummen und Geräte-/Firmwarestände.
Rohdaten werden nicht allein durch 24 Snapshot-Zähler ersetzt. Aus bereits
aggregierten Fenstern kann ein später gefundener Uhrfehler nicht allgemein
rückgängig gemacht werden.

Ein Kalibrierwechsel trennt Läufe oder erhält einen expliziten Transformations-
und Unsicherheitsvertrag. Ungültige TDC-Bins dürfen nicht unsichtbar ausmaskiert
werden: Anzahl, Ursache und Selektionsabhängigkeit müssen erhalten bleiben.
Ein ungültiger Integritätsstatus blockiert die physikalische Bewertung.

## Geplante Kontrollen der Diskretisierung

Die Zellenbreite h ist unabhängig von der Auswertefensterbreite W. Eine kleinere
Fensterbreite erhöht nicht die physikalische Zeitauflösung. Für einen glatten
deterministischen Driftpfad werden h, h/2 und h/4 gegen eine feinere Referenz
verglichen. Für OU-Pfade braucht ein pfadweiser Vergleich konsistent gekoppelte
feine und grobe Realisierungen; einfach denselben Seed bei anderer Schrittzahl
zu verwenden liefert nicht denselben Pfad. Alternativ sind Ensembleverteilungen
mit ausgewiesener Monte-Carlo-Unsicherheit zu vergleichen.

Die mitgelieferte Konvergenzprüfung behandelt den deterministischen Anteil.
Eine allgemeine OU-Konvergenzstudie und Parameterinferenz aus Hardwaredaten
sind offene Aufgaben vor G2/G3. Die Simulatorgrenzen von maximal 2 Millionen
erwarteten Ankünften, 10 Sekunden Laufzeit und 10000 Zellen sind Ressourcen-
und Präzisionsgrenzen dieser Version, keine Grenzen eines physikalischen Links.
