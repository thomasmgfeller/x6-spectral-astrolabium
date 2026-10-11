# Ausgeführte Validierung v0.7

Ausgeführt am 11. Oktober 2026. Alle Ereignisse sind synthetisch. Es wurde
keine physische Messung an FPGA, Detektoren oder Optik durchgeführt.

| Prüfung | Ergebnis |
|---|---|
| VHDL-2008 Analyse/Compilation | PASS |
| 27 Klassifikator-Szenarien | PASS, einschließlich erwartetem Timeout ohne End-Watermark |
| Separater integrierter UART-Top-Level | PASS; zusammen 28 RTL-Szenarien |
| Alle 24 Zähler und Flags der abschließenden Klassifikator-Szenarien gegen unabhängiges Batch-Modell | PASS |
| Python: 17 Testmethoden mit Unterfällen | PASS |
| Alle 1952 Einzelbitänderungen eines 244-Byte-Frames | Zurückgewiesen |
| Sequenzlücken, Duplikate, Vertauschung, Trunkierung | Zurückgewiesen |
| Linux-Empfang über Pseudoterminal, stückweise Daten | PASS |
| Empfangstimeout mit Teilframe | Ungültig; empfangene Rohbytes erhalten |
| RTL → UART-Bits → Testbench-Empfänger → CRC/Sequenz → JSON → Statistik | PASS |
| RTL-Source-Loss → ungültiger Python-Bericht und Exitcode 2 | PASS |
| GHDL-Synthese für Kern, Framer, UART und Top-Level | PASS |
| Quartus Place-and-Route, Timing-Closure, physischer UART | NICHT DURCHGEFÜHRT |
| TDC, Detektoren, Optik, Klebe- und Umweltqualifikation | NICHT DURCHGEFÜHRT |
| Vollständige formale RTL-Verifikation | NICHT DURCHGEFÜHRT |

## Aussagekräftige Grenzfälle

Eine Milliarde leere 1-ns-Fenster benötigt im ausgeführten Kern-Test sechs
Steuerzyklen bis zum Snapshot, mit zwei weit auseinanderliegenden Klicks
14 Zyklen. Dies prüft die Sammelzählung und deren Zählergebnis. Daraus folgt
keine erreichte Taktfrequenz auf einem FPGA. Division und Multiplikation müssen
im Zielgerät noch zeitlich geschlossen werden.

Der 61-Repeat-Test zählt 61 Fenster mit je zwei A+-Ereignissen: 61
Wiederholungs-Trials, 61 zusätzliche Klicks, null Doppelport-Trials. Diese
Klassifikation identifiziert nicht die physikalische Ursache der Wiederholung.

Weitere Szenarien decken alle 16 Kanalbelegungen, halboffene Fenstergrenzen,
gleiche Zeitstempel, Nähe zur uint64-Grenze, Sättigung, ungültige Konfiguration,
Zeitreihenfolge, Kalibrierungswechsel, Erfassungsverlust und drei reproduzierbare
Zufallsfolgen ab. Die vollständige Liste steht in validation/test_summary.json.

Die Testbench prüft die Unveränderlichkeit fertiger Snapshots und die Stabilität
der Framer-Daten unter Rückstau. Der separate Top-Level-Test verwendet ein
50-MHz-Taktmodell und einen 1-Mbaud-UART, prüft die über START erfasste Sequenz
und verhindert eine zweite Übertragung ohne Reset. Das sind Simulationswerte.

## Statistik und Grenzen

Das synthetische CHSH-Beispiel liefert S_cond = −2.8253650438389006 und
S_all = −1.4125. Die Berichte führen physical_quantum_claim=NOT_ASSESSED.
Ein Ergebnis auf ausgewählten Koinzidenzen ist kein lückenfreier Bell-Test.
Annahmen der statistischen Grenzen stehen in docs/METROLOGY.md.

CRC32 und Sequenzkontrolle prüfen Transportintegrität; sie authentifizieren
keine Messung. Mit neu berechneter CRC manipulierte Zähler werden zusätzlich
durch semantische Prüfungen erkannt, soweit die definierten Identitäten sie
einschränken. Verschwiegene Erfassungsverluste kann Software nicht rekonstruieren.

Ausführungsumgebung, Quellenhashes, Testberichte und Syntheseprotokolle stehen
unter validation/. SHA256SUMS bezieht sich auf die ausgelieferten Dateien.
Endliche Tests und generische Synthese sind keine Serien- oder Hardwarefreigabe.
