# Durchsatzbudget – Annahmen getrennt von Messwerten

## Beobachteter digitaler Engpass

v0.6 zählte jedes leere Fenster einzeln. Bei W=1 ns wären bei einem leeren Lauf
10^9 Fensterschritte pro Sekunde Akquisitionszeit erforderlich. v0.7 ermittelt
die Anzahl zusammenhängender leerer Fenster rechnerisch und addiert sie zu
Maske0 und N. Ein belegtes Fenster wird separat geschlossen.

In GHDL gemessen: eine Milliarde leere Fenster → sechs Steuerzyklen vom Start
bis zum Snapshot; eine Milliarde Fenster mit zwei weit auseinanderliegenden
Treffern → 14 Zyklen. Das ist ein Test eines dünn besetzten Ereignisstroms und
keine Behauptung, eine Milliarde Detektorklicks in sechs Takten zu verarbeiten.
UART-Übertragungszeit ist in diesen Core-Zahlen nicht enthalten.

## Logische Obergrenze

ACQUIRE nimmt ein Ereignis an. Danach: gegebenenfalls belegtes Fenster
schließen, gegebenenfalls leere Fenster blockweise zählen, Abschlussbedingung
prüfen, Ereignis anwenden, zurück zu ACQUIRE. Maximal fünf Takte zwischen
Ereignisannahmen, solange keine Implementierung zusätzliche Pipeline-Stufen
einfügt. Der kombinatorische Pfad enthält konstante 64-Bit-Division und
Multiplikation. Quartus kann dafür einen anderen realisierbaren Takt ergeben;
die GHDL-Synthese liefert keine Fmax-Garantie.

**Beispielannahme** f_core=50 MHz: logisches Mindest-Servicebudget 10 Millionen
Elemente/s. Vier Kanäle mit je 100 kcps und 1000 Watermarks/s ergeben 401000
Elemente/s oder 4.01 % dieses bedingten Servicebudgets. Diese Zählraten sind
Entwurfsannahmen, keine gemessenen Quellraten.

## FIFO-Beispiel

Für eine vorgegebene Ankunftsschranke A(t)≤b+r*t und maximalen Servicestillstand T
gilt bei anschließend ausreichender Servicegeschwindigkeit als einfache
Pufferschranke b+r*T. Beispiel: b=512 Ereignisse, r=4 Millionen/s,
T=100 µs → 912 Einträge, gewählte Zweierpotenz 1024.
Bei 128 Bit je gepacktem Eintrag sind das 16 KiB Nutzspeicher, ohne Steuerlogik.

Ohne nachgewiesene Burst- und Stillstandsschranke ist 1024 keine Garantie gegen
Verlust. Quellen-, Kanal-Merge- und CDC-FIFOs müssen ihr eigenes Verlustflag
setzen. Der gegenwärtige Kern implementiert diese vorgelagerten FIFOs nicht.
Eine bloße niedrige mittlere Rate ersetzt keine Burst-Betrachtung.

## Hostbandbreite

Ein 244-Byte-Snapshot braucht bei 1 Mbaud und 8N1 etwa 2.44 ms, inklusive der
einen zusätzlichen Taktlücke pro Byte im implementierten Sender etwa 2.445 ms
bei 50 MHz. Es gibt keine Gleichsetzung zwischen dieser Bandbreite und dem
Detektoreingang. Hochratige Rohzeitstempel müssen separat aufgezeichnet werden.

Alle Beispielrechnungen sind mit `python3 host/budget.py` reproduzierbar.
`examples/design_budget.json` kennzeichnet sämtliche Frequenz-, Burst- und
Ratenannahmen ausdrücklich als nicht hardwarequalifiziert.
