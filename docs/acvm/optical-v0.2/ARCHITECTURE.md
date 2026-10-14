# Implementierte Architektur und Nachweisgrenzen

## Drei getrennte Ausführungspfade

1. **D01 / SIMULATED:** Plan → strenger Compiler → komplexes Sample-Image →
   unabhängiger Leser → Referenz-Zustandsautomat → vollständiges Archiv.
   Virtuelle Zeit; keine FPGA-Synthese, keine DAC-Ausgabe.
2. **C1:** bestehender endlicher Host-/Pico-Befehlskanal mit C++-Kern,
   Geräte-Lease und expliziter Kanalprofilgrenze. Native/PTY-Ausführung geprüft;
   Pico-Target und elektrische Wirkung weiterhin unqualifiziert.
3. **O02 / DEVICE_REPORTED:** explizites Geräteprofil → ELL14/PM100D-Adapter →
   endliche langsame Regelung → Rohprotokolle und Ergebnis. Diese Implementierung
   ist mit Protokollmodellen und virtueller serieller Schnittstelle geprüft.
   Kein angeschlossenes Gerät hat den hier veröffentlichten Nachweis geliefert.

Diese drei Pfade werden nicht gegenseitig als Hardwarebeleg verwendet.
Der D01-Zustandsautomat enthält Clock-valid-/Disconnect-Fehlerinjektion; das
fügt dem C1-Pico nicht nachträglich einen gemessenen Referenztakt-Eingang hinzu.

## Formate

`acvm.d01.plan/1`: eindeutige Run-ID, `normalized_IQ`, integer `tick_ns`,
`duration_ticks`, 1–4096 Samples mit `tick`, `i`, `q`. IQ je −1 bis +1,
erstes Sample bei Tick 0, streng steigende Reihenfolge, endliche Dauer.
Zeitprodukte dürfen 64 Bit nicht überlaufen; JSON-Integer bleiben exakt unter
2^53. Andere Einheiten, Zusatzfelder, NaN/Inf und boolesche Zahlen werden abgewiesen.

Binärimage: 24-Byte-Header (`ACVMD01\0`, uint32 Anzahl, uint32 Tick-ns,
uint64 Dauer), dann je Sample uint64 Tick + Float64 I + Float64 Q,
little-endian. Vollständiger SHA-256 im Archiv, kein Präfixhash. Der unabhängige
Leser importiert weder Compiler noch dessen Structs. Zustandsautomat bindet
Run-ID und Imagehash; doppelte STARTs führen nicht zu einer zweiten Ausführung.
Verpasste Samples werden nicht verspätet als Burst nachgeholt.

`acvm.archive/2`: `plan.json`, `samples.bin`, `execution.json`, `manifest.json`.
Leser prüft Bytezahl, Werte, Ordnung, Planvergleich, sämtliche Events, Endzustand
und Modellklasse. Das Manifest ist ausgenommen von seinem eigenen Hash.
Archivformat ist begrenzt auf D01, nicht die vollständige generische Records-
Konzeptarchitektur. Elektrische/optische Messdaten werden in getrennten Formaten
mit nachvollziehbaren Aufnahmeblöcken ausgewertet.

`acvm.optical.calibration/1`: Kennlinie eines monotonen Intensitätsasts,
Seriennummer, Wellenlänge, Kalibrier-ID, Lauf-IDs, Einschwingzeit und Leistungsgrenze.
Ein Phasenprofil hat zusätzlich drei Achsnullen/-richtungen und Retardanzen.
Vorlagen und Simulationen können den Live-Regler nicht aktivieren.

## Geräteadapter

ELL14: 9600/8N1, expliziter exklusiver serieller Port, Antwortende CR/LF,
begrenzte Antwortlänge und Zeit. Modell/Seriennummer/Adresse müssen stimmen.
`ma` wird bei verlorener Antwort nicht wiederholt. GS09 ist BUSY, GS00 allein
ist keine Position. Erst passende PO-Antwort bestätigt eine gemeldete Stellung.
Fehler verriegeln den Adapter; STOP nur bestmöglich. Das Herstellerprotokoll
beschreibt `st` für kontinuierliche Bewegung/Optimierung; ein sicherer Abbruch
einer laufenden Absolutbewegung wird hier ausdrücklich nicht vorausgesetzt. Es
hat keinen ACV1-CRC und keine unseren C1-Sessions entsprechende Authentifizierung.

PM100D: explizite VISA-Ressource, 1 s I/O-Zeitlimit, Zeilenabschluss LF, Identität
von Konsole und Sensor, Watt-Einheit bei jeder Abfrage, Wellenlängenrücklesen,
Fehlerqueue und Bereichsprüfung. NaN/Inf, Überlaufwerte und negative Leistungen
werden abgewiesen. Kommunikation und Rückgaben werden vollständig protokolliert.
Ein beliebig großer endlicher Wert wird nicht als gültige Messung behandelt.

Die Parkstellung ist ein kalibriertes geringes Transmissionsniveau, kein
garantiertes Nulllicht. ELL14/PM100D besitzen hier keine vom Host unabhängige
Gesamtregelung; ein Hardwarestrahlverschluss bleibt Teil des Laboraufbaus.

## Schnelles Feed-forward

Der implementierte Motor-/USB-Pfad ist dafür ungeeignet. Benötigt wird ein
gesonderter schneller Kanal: Detektor → konditionierter Eingang → deterministische
FPGA-/Logikentscheidung → Ausgang → passender Treiber → 810-nm-EOM/Pockelszelle.
Photonenverzögerung/optischer Weg muss den vollständigen Zeitbedarf abdecken.
Ereignis-Pulsbreite, Doppeltreffer, Totzeit, Fehltrigger und Ausgangspulsbreite
sind Teil desselben Experiments, nicht nur eine minimale Logiklatenz.

Der ausführbare Budgetprüfer verlangt alle sechs Stufen, explizite Reserve und
je Stufe Latenz, Jitterobergrenze und Herkunft. Obergrenzen werden summiert,
keine unabhängigen Fehler unterstellt. Die Beispieldatei enthält ausschließlich
Entwurfszuweisungen: 280 ns Latenzen + 70 ns Jitter + 100 ns Reserve = 450 ns
bei angenommenen 500 ns verfügbarem Fenster. Ergebnis nur
`CONDITIONAL_BUDGET_FITS`, **niemals** „Feed-forward demonstriert“.

Physische Abnahme: Trigger und tatsächliche optische Umschaltung gleichzeitig
mit unabhängiger Zeitreferenz messen; vorab gewählte Eingangsraten und lange
Läufe einschließlich Grenzabständen, fehlendem Takt und Doppelereignissen.
Ein beobachtetes Maximum beweist keine Worst-Case-Garantie. Erforderlich sind
Hardwareaufbau, FPGA-Zielimplementierung/Timingabschluss und optische Messung.
Diese Version enthält keine neue RTL- oder EOM-Hardwareimplementierung.

## Aussagegrenze

Klassische Leistung/Phasengenauigkeit ist keine Quantenprozessfidelity.
Motorisch erzeugte relative H/V-Phase ist keine demonstrierte photonische
Feed-forward-Operation. Ein erfolgreicher Modelllauf validiert die spezifizierte
Rechenregel und Fehlerbehandlung innerhalb seiner Tests, nicht den Modellbezug
zur realen Anlage. Keine Quantenrechner-, Vorteil- oder Neuphysikbehauptung.
