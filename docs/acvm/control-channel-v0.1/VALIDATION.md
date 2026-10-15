# ACVM C1: ausgeführte Prüfung und verbleibende Nachweise

**Gesamtergebnis: SOFTWARE_PASS_HARDWARE_OPEN.**

Der Softwarekanal wurde implementiert und über eine virtuelle serielle
Verbindung vollständig ausgeführt. Die reale elektrische und optische
Ansteuerung ist damit noch nicht nachgewiesen. Es war kein Pico/DAC-Aufbau
angeschlossen; Pico SDK und Arm-Toolchain standen nicht bereit. Deshalb wurde
kein UF2 gebaut und keine reale Spannung als gemessen ausgegeben.

## Ausgeführte Prüfungen

| Prüfung | Ergebnis | Beleg |
| --- | --- | --- |
| 27 C++-Gerätekernfälle mit kontrollierter Zeit | PASS | [Kernprotokoll](evidence/firmware-core-tests.log) |
| 18 Python-/Transportfälle, einschließlich echter POSIX-Pseudoterminals | PASS | [Hostprotokoll](evidence/host-tests.log) |
| 384 einzelne Bitfehler im 48-Byte-Frame | Alle abgewiesen; Teil eines Kernprüffalls | Kernprotokoll und `core_tests.cpp` |
| Stufenfolge mit sechs Punkten und abschliessendem Nullzustand | PASS gegen unabhängig gelesenen Binärplan | [Rohdaten und Ergebnis](evidence/model-run/result.json) |
| Export und erneutes Einlesen | PASS | [Qualifikation](evidence/qualification.json) |
| Fünf Manipulationsklassen | Alle abgewiesen | Qualifikation |
| Frischer Git-Checkout: neun dokumentierte Schritte | PASS | [Checkout-Beleg](evidence/fresh-checkout/fresh-checkout.json) |
| 12 bestehende X6-Integrationstests im frischen Checkout | PASS | [Regressionen](evidence/fresh-checkout/09.log) |

Die fünf Manipulationsklassen sind: beschädigtes Exportpayload, gefälschter
Antwortwert im Ergebnis, Umdeklaration eines Modelllaufs zu Hardware,
veränderter Plan mit erneuerten Dateihashes und veränderte Modellereignisse
mit erneuertem Dateihash. Diese Tests belegen die geprüften Konsistenzregeln;
sie liefern keine kryptografische Authentizität vollständig neu erfundener Daten.

Die Fehlerprüfungen umfassen doppelte Starts, verlorenes Start-ACK, Stop bei
Sequenzlücken, falsche Session, ungeordnete Befehle, unvollständige Pläne,
Bereichs-/Puffergrenzen, eine volle 64-Punkte-Sequenz, Zeitüberschreitung,
rückwärts laufende Uhr, Überschreiten der 32-Bit-Millisekundengrenze,
beschädigte/fragmentierte Pakete sowie ausbleibende Lebenszeichen und das
Schliessen der virtuellen seriellen Verbindung. Der Modell-Gerätekern läuft
nach dem Verbindungsabbruch bis zur Lease-Fehlerreaktion weiter.

## Reproduzierbarkeit

Ausführbarer Implementierungsstand: Git-Commit
`7f20fbc7e55aea371614e9832570c91b45243a04`, basierend auf veröffentlichtem
`76f70c0be27ba3b2403d3027b71435c326590442`.
Spätere Lieferänderungen ergänzen Berichte und das Quellpaket; die tatsächlich
geprüften Quelldateien sind in `evidence/qualification.json` einzeln gehasht.

Umgebung: Linux x86_64, Python 3.12.14, g++ 13.3.0. Native C++-Builds verwenden
`-std=c++17 -O2 -Wall -Wextra -Werror -pedantic`. Der Softwareablauf benötigt
keine zusätzlichen Python-Pakete. Die bestehende X6-Kernumgebung wurde nur
für die zusätzlichen Integrationstests eingerichtet.

Im frischen Checkout wurden Voraussetzungen, Compiler, Demo, unabhängige
Verifikation, Export, vollständige C1-Qualifikation, Repository-Inventar,
X6-Kerninstallation und die bestehenden Integrationstests ausgeführt.
Das Quellpaket ist zusätzlich mit `python3 -m experimental.control_channel`
ohne X6-Launcher ausführbar. Die [Anleitung](README.md) enthält die Befehle.

Zeitwerte der Modellereignisse stammen aus einer Softwareuhr. Sie sind keine
Oszilloskopmessung, kein Nachweis der USB-/SPI-Latenz und keine Garantie für
einen späteren optischen Aktuator. Der Paketexport und SHA-256 sichern die
aufgezeichneten Bytes; eine externe Begutachtung wurde nicht durchgeführt.

## Offene Gates

1. Flashen und Identifizieren des konkreten Boards. Der
   [RP2040-Zielbuild samt UF2-Identifikation](../c1-e01-target-build/README.md)
   ist inzwischen ausgeführt; die unten stehenden physischen Gates bleiben offen.
2. Reale USB-/SPI-Verbindung und unabhängige Spannungs-/Timingmessung nach
   [E01](HARDWARE.md), einschließlich Fehler- und Abschaltversuchen.
3. Auswahl eines konkreten optischen Treibers, bestätigte elektrische
   Schnittstelle, Kalibrierung und getrennte optische Prüfdaten.

Der Status der umfassenden ACVM-Prüfungen V01–V10 wird durch C1 nicht pauschal
auf PASS gesetzt. C1 deckt Teilanforderungen zu Eingaben, Dateiintegrität,
Reihenfolge und Fehlerbehandlung ab. Die ursprünglichen Signalmodelle,
FPGA-Sequencer, optische Regelung und schnelle Feed-forward-Kette bleiben
separate Arbeitsschritte. Es besteht keine Hardware- oder Quantenfreigabe.
