# Zwei enduhrunabhängige Paarungen im kleinen CST-Uhrmodell

**18. November 2026.** Eine frühe Vorhersage kann im markierten Uhrmodell mit höchstens zwei inneren Ereignissen beim Verlängern des Zeitfensters stabil bleiben. Die Norm- und Schnittbedingungen lassen mehrere positive Paarungen zu. Sie liefern für dieselbe leere Anfangspräparation unterschiedliche Wahrscheinlichkeiten. Die Studie schliesst an den [Stand nach PR #303](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/2770f280ddcab063b925813170dc87c58a8b3821) an.

[Bericht (PDF, drei Seiten)](../reports/CST_DUST_Uhrpaarung_Erster_Lauf.pdf) · [Prüfpaket mit Bericht, Code und Eingabedaten (ZIP)](../packages/CST_DUST_Uhrpaarung_Erster_Lauf_Pruefpaket.zip)

| Wahl der Paarung | Keine Geburt bis Uhrmarke 1/4 | Keine Geburt bis Uhrmarke 1/2 |
| --- | ---: | ---: |
| β = 5/4 | 23/32 | 1/2 |
| β = 4/3 | 67/96 | 11/24 |

Bei festem β gilt jede Tabellenzeile für beide Enduhrwerte 1/2 und 1. Für jeden der zwei Primärfälle stimmen auf neun Uhrmarken alle 502 geprüften Unterteilungen über alle Endpunktpaare mit dem direkten Transport überein. Die Positivität im gesamten betrachteten Zeitfenster folgt zusätzlich aus der expliziten Formel. [Herleitung](theorie/befund.md) · [Solver und Prüfbereich](numerik/README.md) · [Exakte Solver-Ergebnisse](numerik/ergebnisse.json)

## Unabhängige Prüfung

Zwei präparierte Uhrpakete überlappen auf markierten Einerelement-Historien. Ein fester früher Record prüft diese Überlappung bei drei verschiedenen Enduhrwerten. Alle 108 direkten und verklebten Quadratformpaare stimmen überein. Der Unterschied der gemessenen komplexen Kreuzterme zwischen den beiden Paarungen ist (1 + i)/312. Die zwei eingebauten Auswertefehler wurden in allen neun Modell-Endwert-Paaren erkannt. Die kohärente Auslese betrifft die Präparation auf gemeinsamem Träger. Die Herleitung einer physikalischen Interferenz verschiedener Geometrievergangenheiten bleibt offen. [Audit und Auslese](audit/README.md) · [Exakte Auditergebnisse](audit/coherent_audit.json)

## N14 und der Pilot für M = 1

Die Endtypen 1790 und 5374 besitzen identische N13-Präfixspalten. Ihre Gewichte können innerhalb des positiven Zeugen gegeneinander verschoben werden. Der Wert dieses Orbittransfers ist unabhängig von der Wahl des Uhrparameters β physikalisch zu bestimmen. Für M = 1 wurde die klassische P3-Referenz mit 128 Zeitschritten neu integriert. Alle 20 archivierten Euler-Hüllen enthalten den analytischen Wert. **Dynamischer P3-Status: `HOLD_NOT_ELIGIBLE / NOT_RUN`, 0 von 524 physischen Vergleichen ausgeführt.** Die physikalische Paarung und Rückwirkung sowie die uniforme Kleinvolumen-Schranke bleiben offen. [Zusatzkontrollen mit Ergebnissen](zusatz.json) · [P3-Vertrag](../correspondence_v0_1/plan.json)

## Lokal wiederholen

Python 3.10 oder neuer und die Standardbibliothek genügen. Im ausgecheckten Repository startet folgender Befehl Theorieprüfung, Solver, Audit und Zusatzkontrollen. Die sieben geerbten Eingabedateien werden anhand ihrer SHA-256-Werte geprüft.

```sh
python3 -B research/rax_cqg/dust_collapse/clock_pairing_v0_1/start.py
```

Ohne Repository-Checkout das gewünschte Paket entpacken und in seinem eigenen Ordner `python3 -B start.py` ausführen.

- [Lokaler Vortest (ZIP)](../packages/CST_DUST_Lokaler_Vortest.zip) · Enumeriert mit dem archivierten Uhr-Replay Ordnungen bis N = 6. Bei N = 6 sind es 4.824 natürlich beschriftete Kausalordnungen. Der Lauf vergleicht sechs frisch erzeugte Ergebnisdateien byteweise mit dem Archiv und kontrolliert die bekannte Enduhrabhängigkeit.
- [Erster Paarungslauf (ZIP)](../packages/CST_DUST_Uhrpaarung_Erster_Lauf_Pruefpaket.zip) · Enthält die hier geprüften enduhrunabhängigen Varianten sowie die separaten N14-, N11-, Wirkungs-, Kleinvolumen- und klassischen Massenkontrollen. Die Quelldateien sind an den [Referenzstand gebunden](quellen.json).
