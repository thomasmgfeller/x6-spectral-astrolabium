# Kalibrierung und Messabnahme

Alle Zahlen unten sind **vorab gewählte Arbeitskriterien**, keine bereits
erreichten Gerätespezifikationen. Bei abweichender Hardware ein neues Profil
vor den Prüfmessungen festschreiben. Rohdaten, Seriennummern, Gerätekonfiguration,
Wellenlänge, Temperatur, Zeitbasis, Unsicherheitsbudget und Quellcode-Hash sichern.
Kalibrierung und Prüfung sind getrennte Aufnahmeblöcke, keine zufällig geteilten
Einzelsamples aus demselben Driftverlauf.

## K01 – Motor und Koordinaten

1. Ohne freigegebenen Laserstrahl jeden Motor einzeln mit Herstellerbedienung
   referenzieren; Busadressen eindeutig vergeben. Die neue Software führt kein
   automatisches Homing oder Änderung persistenter Einstellungen aus.
2. `in`-Antwort, Seriennummer, Firmware und Encoderfeld protokollieren.
   Mit unabhängigem Winkelmaß mindestens 0°, 22.5°, 45° und Rückfahrt messen.
   Daraus Impulse/Grad und Bewegungsrichtung bestimmen; Fehler über mindestens
   drei Hin-/Rückläufe berichten. Erst dann `pulses_per_degree` eintragen.
3. Arbeitsbereich zunächst 0–90° Motorwinkel, falls mechanisch zulässig.
   Berichtsgrenze 0.05° ist ein einstellbarer Soll-/Geräterückmeldungsvergleich,
   keine Aussage über die absolute Winkelgenauigkeit. Optische Achsnull separat.
4. Port/Seriennummer vertauschen, Kabel abziehen und unerreichbaren Zielwinkel
   testen. Kein erneutes `ma`, keine automatische Wiederaufnahme. `st` und
   Parkstellung sind Best-Effort; unabhängigen Strahlverschluss prüfen.

## K02 – HWP/PBS-Intensitätskennlinie

Lineares 810-nm-Referenzlicht, nachgemessener Polarisationszustand, Pumpe aus.
PM100D/S120C nullen, Seriennummer und Sensorkalibrierung sichern. Wellenlänge
einstellen; hinter dem PBS messen und den verworfenen Port auffangen.

- Drei Kalibrierläufe: 0–85° in 5°-Schritten; Hin-/Rückrichtung abwechseln.
  Je Stellung nach vollständiger Bewegung mindestens 0.5 s warten, tatsächlich
  erforderliches Einschwingen in K04 bestimmen. Drei Messwerte und passende
  Referenzleistung pro Stellung erfassen. Reihenfolge und Zeitstempel erhalten.
- JSON-Zeilenfelder des Fits: `angle_deg`, `power_w`, `reference_w`, `dark_w`.
  `fit-hwp` passt `(P−Pdark)/Pref = a+b cos(4θ)+c sin(4θ)` an. Ergebnis:
  Nullwinkel modulo 90°, Sichtbarkeit und sämtliche Residuen. Ein Fit ersetzt
  keine Unsicherheitsschätzung aus unabhängigen Läufen.
- Für den Stellkanal nur einen monotonen Ast wählen, bevorzugt mit Transmission
  0.05–0.95. Eine dicht genug gemessene Tabelle `fraction → motor_deg` anlegen;
  Interpolation durch zusätzliche Zwischenwinkel prüfen. Außerhalb der Tabelle
  verweigert die Software die Ausgabe. Flache Endbereiche vermeiden.
- Drei **neue** Prüfläufe mit vorher festgelegten Zwischenwinkeln. Grenze für
  absolute Transmissionsvorhersage zunächst 0.02 einschließlich Unsicherheit.
  Temperatur-/Ausrichtungsänderung erfordert neue Kalibrier-ID.

`calibration-simulated.json` zeigt das Datenformat, enthält aber fiktive Werte.
`MEASURED` erst für reale Daten verwenden, nicht durch Umbenennen des Beispiels.
Absolute PM100D-Leistung, Referenznormierung, Nullpunktfehler und gemeinsame
Sensorkalibrierung sind korreliert; Messpunkte nicht als unabhängige Zertifikate
zählen. Diese Version automatisiert den Fit und die Regelung, noch keinen
kompletten motorisierten Kalibrierscan mit Referenzmonitor.

## K03 – Analyse und relative Phase

Bekannte H/V/D/A/R/L-Eingänge bei tatsächlicher Wellenlänge verwenden. QWP-
Retardanz und Achsnull aus allen Zuständen gemeinsam bestimmen; HWP-Null aus
K02 ergänzen. QWP/HWP/PBS-Reihenfolge, Richtung und Detektorlabels festhalten.
Für CHSH sind 0°, 45°, ±22.5° **Analyseachsen**, nicht ungeprüfte Motorwerte.

Für QHQ: Q1 und Q2 optisch auf 45°; HWP-Winkel θ ergibt im implementierten
Jones-Konventionssystem relative Phase `φ = π + 4θ (mod 2π)` zwischen V und H.
Die Software prüft diesen Zusammenhang analytisch. In der realen Kalibrierung
Retardanzen und Achsnullen eintragen; alle drei Achsen sind seriell identifiziert.
Der begrenzte ideale Lösungsansatz wird bei zu großem kalibriertem Restfehler
oder Polarisationsübersprechen verworfen. Er ist kein allgemeiner Optimierer.

Abnahme an **neuen** Phasen 0, π/4, π/2, 3π/4, π über D/A- und R/L-Analyse.
Kreisförmiger Phasenfehler, Transmission und Unsicherheit gemeinsam berichten;
bei zu kleiner Amplitude Phase undefiniert lassen. Anfangskriterien: 0.02 rad
Phasenrestfehler und 0.01 Jones-Übersprechamplitude sind Modellfilter,
keine bestätigte optische Genauigkeit. Gemeinsame globale Phase ist unbeobachtbar.

## K04 / V10 – langsamer geschlossener Regelkreis

Zuerst Sprungantworten für beide Stellrichtungen aufnehmen. Die Wartezeit nach
Abschluss jeder Bewegung muss die beobachtete Einschwingzeit mit Reserve
übersteigen; Startwert 1 s ist nur ein Versuchswert. Hostzeiten begrenzen ein
Anfrageintervall, sie sind keine Zeitstempel aus dem optischen Sensor.

Vor Prüfung Profil, Kennlinie, PI-Gewinne, Ziel 0.5 mW und Datenfenster einfrieren.
Je mindestens fünf getrennte Läufe mit Regelung und fünf mit festem kalibriertem
Stellwert, Reihenfolge blockweise randomisieren; gleiche Laufdauer und Zahl der
Messungen. Einen zweiten Sensor oder wiederholte unabhängige Kontrollmessungen
verwenden, damit das Messgerät nicht allein seine eigene Regelung bestätigt.
Verlust und Drift ebenfalls aufnehmen; sämtliche Anlaufwerte exportieren.

Vorläufige Kriterien: nach dem eingefrorenen Anlaufzeitfenster RMSE mit Regelung
<50% des festen Stellwerts, mittlere absolute Leistung innerhalb 2% des Ziels
zuzüglich Unsicherheitsentscheidung, keine Sättigung/fehlende Messung, kein
ungeklärter Abbruch. Ergebnisse pro Lauf berichten; kein Standardfehler aus
autokorrelierten Einzelpunkten. Bei Grenzüberlappung INCONCLUSIVE.

`assess-optical` prüft ein **lokales lineares Transfermodell**, disjunkte Lauf-IDs,
Kalibrierbereich, Vorhersageresiduen, Residuen-Spannweite und Verlust. Es ist kein
allgemeiner Sagnac-, Jones- oder Reglerqualifizierer. Seine konservative empirische
Kalibrierhülle ist kein statistisch bewiesenes Konfidenzintervall. Unzulässige
Daten ergeben keinen PASS. Ein Kriterien-Hash belegt allein keine Vorregistrierung.

## V09 – unabhängiger elektrischer Nachweis des C1-Ausgangs

Nach Pico-Zielbuild und Verdrahtungsprüfung: GP2-Startmarker und DAC-Ausgang mit
kalibriertem Oszilloskop unabhängig aufnehmen. VREF messen. C1-Plan mit Codes
0, 819, 1638, 2457, 3276 und Rückkehr zu 0 verwenden; mindestens drei getrennte
Läufe, tatsächliche Dauer und Zeitbasis dokumentieren. Spannungsziel aus
gemessener VREF und `code/4096`; Messfenster fern der Sprungflanken und separat
Einschwingzeit/Überschwingen bestimmen. Zeitpunktdefinition vorab festlegen.

Vorläufige Grenzen: 10 mV absoluter Spannungsfehler und 1 ms Ereigniszeitfehler,
jeweils einschließlich Unsicherheit. `assess-electrical` vergleicht absolute
Soll-/Messwerte ohne Gain-/Offset-Fit; Fehler können nicht wegkalibriert werden.
Gemeinsame Zeitbasis erlaubt nur relative Timingbehauptungen. Rohwellenformen
und Gerätekalibrierung separat sichern; die JSON-Auswertung ersetzt sie nicht.
STOP, Hostverlust, Reset, Versorgungsausfall und unerwartete Last separat messen.

## K05 – Sagnac-Quelle

Herstellerbestätigtes O02-K1-Kristallprofil und Ofen zuerst abschließen.
Einzelrichtung CW/CCW getrennt charakterisieren (Spektrum, Polarisation,
Kopplung, Dunkelrate, Zählrate). Dann beide Wege und Modenüberlappung einstellen.
Temperatur-/Pumpenwellenlängenscan nur innerhalb der konkreten Bauteilgrenzen.
Koinzidenzfenster und Detektoroffsets aus separater Kalibrierung einfrieren.

Neue Prüfblöcke in H/V, D/A, R/L und den vorgesehenen CHSH-Basen aufnehmen;
Rohzählungen, Unfallkoinzidenzen, Verluste und Unsicherheit berichten. Koinzidenzen
oder klassische Sichtbarkeit allein sind kein Nachweis einer Quantenoperation.
Der vorhandene SGNCv007-Bridge bleibt ein Snapshot-Leser; Rohzeitstempel und
unabhängige Referenzmessung müssen aus der realen Erfassung kommen.
