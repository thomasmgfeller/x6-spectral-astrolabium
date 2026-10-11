# Optischer Funktionsentwurf

**Designwerte, keine bestätigten Betriebsparameter.** Grundlage: Kim, Fiorentino und Wong (2006), siehe [Quellen](SOURCES.md). Der veröffentlichte Literaturaufbau ist nicht mit unserem noch unqualifizierten Aufbau gleichzusetzen.

Ein nominaler 405-nm-Pumpstrahl soll einen Typ-II-ppKTP-Kristall in zwei gegenläufigen Wegen eines Polarisations-Sagnac-Interferometers anregen. Die beiden Erzeugungsalternativen müssen räumlich, spektral und zeitlich hinreichend ununterscheidbar sein. Relative Amplitude und Phase bestimmen den Zustand. 810 + 810 nm ist die geplante degenerierte Wellenlängenkombination; Temperatur, Polungsperiode und tatsächliche Phasenanpassung sind noch festzulegen. Ein gewünschter Singlet-Zustand entsteht nicht allein durch Einsetzen des Kristalls.

Nach Pumpunterdrückung und geeigneter Auskopplung besitzt jeder der zwei Messarme einen Polarisationsanalysator. Je ein QWP/HWP/PBS-System soll die Analysebasis einstellen und die Ausgänge auf A+/A− bzw. B+/B− führen. Optikreihenfolge, Achsenkonventionen und tatsächliche Stellwinkel sind experimentell zu kalibrieren. Die Winkel 0°, 45°, +22,5°, −22,5° in der CHSH-Referenz sind Analyseachsen, keine ungeprüft übertragbaren Motor- oder Wellenplattenwinkel.

## Vor einer Beschaffung zu schließen

| Baugruppe | Vorgesehene Funktion | Noch zu spezifizieren / nachzuweisen |
|---|---|---|
| Pumpquelle | Nominal 405 nm, geeignete Polarisation und Kohärenz | Modell, Leistung, Bandbreite, Strahlprofil, Stabilität und Laserschutzkonzept |
| Nichtlinearer Kristall | Ein Typ-II-ppKTP, nominal degenerierte SPDC | Länge, Apertur, Polungsperiode, Beschichtungen, Temperaturbereich und Halter |
| Sagnac-Optik | Gegenläufige Pumpwege und Rekombination | Tatsächliche Strahlgeometrie, PBS, Spiegel, duale Wellenlängenanforderungen, Phasen-/Balancekontrolle |
| Auskopplung und Filter | Zwei Photonenarme, starke Pumpunterdrückung | Dichroika/Filter, Bandbreite, Transmission, Faser- oder Freistrahlkopplung, Streulicht |
| Analysatoren | Zwei QWP, zwei HWP, zwei analysierende PBS als Funktionsbedarf | 810-nm-Spezifikation, Achsen/Retardanz, Nullpunkte und Detektorkanalzuordnung |
| Detektoren | Vier zeitaufgelöste Ausgänge | Modellvariante, Effizienz, Dunkelrate, Jitter, Totzeit, Nachpulse, Versorgung und Abschlüsse |
| Zeitmessung | Gemeinsame Zeitbasis für vier Kanäle | Kalibrierung, Skalenfehler, Kanalversatz, DNL/INL soweit relevant, Überlauf- und Verlustnachweis |
| Digitalteil / Host | Geordnete Ereignisse → Fensterzähler → SGNCv007 → X6 | TDC/FPGA-Adapter, FIFO/CDC, Board-Pinmap, sichere Pegel und Ende-zu-Ende-Prüfung |
| Mechanik | Stabiler Quellenaufbau; Jig für qualifizierten Montageprozess | Frei zugängliche Strahlwege, Drift, Klebefuge, thermische und mechanische Toleranzen |

Diese Liste ist ein Funktionsbedarf, keine vollständige Bestellstückliste. Konkrete elektrische Kandidaten und offene Schnittstellen sind im [Hardwareplan v0.7](reference/sagnac_v0_7/docs/HARDWARE.md) dokumentiert. Ein kalibrierter externer Time-Tagger ist eine mögliche erste Referenz; die eigene TDC-Entwicklung bleibt separat zu qualifizieren. Kaufmodule und der v0.2-SPAD-Eigenbau sind Alternativen mit unterschiedlichen Entwicklungsrisiken.

Der Jig ist ein Montagehilfsmittel. Seine 6-DOF-Kinematik ersetzt keine Polarisationsoptik, Phasenregelung oder Quantenoperation. Das Astrolabium übernimmt in diesem Stand Import, Kontrolle und Darstellung von Zähldaten; eine geschlossene Quantenregelung ist nicht implementiert.
