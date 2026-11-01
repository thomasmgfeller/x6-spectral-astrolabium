# Zwei Schlüssel für einen späteren Laborvertrag

Alle folgenden Gerätebelege fehlen. Die vorliegenden Dateien steuern
keine Apparatur. Das Quellen-/Sondenmodell ist eine mathematische
Referenz mit einem freien Skalarfeld und kein elektrooptischer Aufbau.

| Schlüssel | Erforderlicher Beleg | Weshalb er benötigt wird | Status |
|---|---|---|---|
| Metrologie | Tatsächliche Kopplung von Quelle, Feld und ADC einschließlich Vorzeichen, Einheit, Verstärkung und linearer Betriebsgrenze | Zuordnung des Kontrasts zur Feldantwort | HOLD |
| Metrologie | Raumzeitliche Gewichte, Timing und räumliche Ausdehnung samt nachgewiesenen Ausläufern | Die strikten Nullstellen setzen kompakte oder quantitativ begrenzte Träger voraus | HOLD |
| Metrologie | Rest des vorzeichenabhängigen Übersprechens für jede Einstellung unabhängig begrenzen | Eine Referenzsubtraktion allein begrenzt den Unterschied zwischen den Kanälen nicht | HOLD |
| Metrologie | Nullpunkte, nichtlineare Drift, Rausch-Kreuzterme und gemeinsame Kalibrierkovarianz | ABBA entfernt nur die im Vertrag genannten Beiträge | HOLD |
| Statistik | Begründete Anzahl unabhängiger oder ausdrücklich modelliert abhängiger Blöcke | Marginale Streuung allein genügt nicht für das Budget | HOLD |
| Physik | Reale Materialantwort, Zustand, Rückwirkung und gewöhnliche Übertragungswege | Ein skalares Vakuummodell ist noch keine Kristall-/Photonikvorhersage | HOLD |
| Physik | Vorab festgelegter Test gegen relevante klassische Alternativen | Klassische Klein-Gordon-Dynamik hat dieselbe Antwort | HOLD |

## Nächster konkreter Versuchsauftrag

1. Quelle und Detektor auf eine reale Plattform festlegen; messbare Einheit
   und Zeit-/Längenskala angeben. Es wird hier keine Bauteilbestellung ausgelöst.
2. Ein unabhängiges Referenzverfahren für den ungeraden Rest entwickeln.
   Sinnvolle getrennte Kontrollen sind gesperrter Feldweg bei aktiver
   Elektronik, vertauschte Messpfade, gleichwertige Abschlüsse und mehrere
   Quellamplituden einschließlich null. Jede davon hat Modellannahmen;
   keine einzelne Kontrolle beweist automatisch die benötigte Schranke.
3. Den ursprünglichen und den Referenzkanal vollständig aufzeichnen.
   Dunkel-/Nullmessungen charakterisieren die passive Rauschkovarianz,
   ersetzen aber keine Kontrolle quellenabhängiger Störungen.
4. Auf Entwicklungsdaten ein Modell für Drift, Ausläufer, Verlust und
   zeitliche Abhängigkeit bestimmen. Danach einen neuen unabhängigen
   Testvertrag einfrieren. Die Zahl 2048 wird erst nach erfolgreicher
   Übertragung der Rausch- und Kalibriergrenzen neu bewertet.

Die Referenz aus v0.14 und der Antwortkanal aus v0.15 sind zwei
unterschiedliche Messkonfigurationen. Ihre Ergebnisse werden nicht als
statistisch unabhängige Doppelbestätigung oder als fertiger gemeinsamer
experimenteller KVF ausgegeben. Dafür fehlen gemeinsame reale Messdaten.
