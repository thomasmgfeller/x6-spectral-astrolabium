# CST-DUST: Kohärente Randauslese und Dekohärenz v0.1

Arbeitspaket vom 7. November 2026, aufgebaut auf Main nach PR 253
(`36afc462dc5a9503616e9b016481e3b441b7c123`).

**Ergebnis:** Zwei ausdrücklich gewählte, beschränkte kohärente Endauslesen
sind mit dem Referenztransport vereinbar. Ihr Rücktransport stimmt ohne
nachträgliche Normierung an verschiedenen Zeitschnitten überein.
Eine Rang-eins-Auslese kann bei reinem Anfangszustand keine exakt
mittel-dekohärente Partition mit mehreren positiven Historienatomen tragen.
Getrennte Elementzahlkanäle erhalten Interferenz innerhalb jeder Zahl und
liefern eine konsistente Verteilung der terminalen Zahl-Ausgänge.

Das ist ein mathematisch geprüftes Referenzinstrument, keine physikalisch
ausgewählte CST-Randbedingung. **Alle acht physikalischen Gates bleiben HOLD.**
Kein Bounce, keine Singularitätsauflösung und kein allgemeines CST-No-go.

## Inhalt

- `DERIVATION.md`: Definitionen, Beweise, Geltungsgrenzen und Primärquellen.
- `boundary_contract.json`: maschinenlesbarer Status.
- `CST_DUST_Kohaerente_Randauslese_Dekohaerenz_v0_1.pdf`: kompakter Bericht.
- `plan.json`, `plan.sha256`: vor Enumeration lokal eingefrorener Prüfplan.
- `inputs/provenance.json`: sechs bytegleiche Eingaben mit Commit und Blob-SHA.
- `results/`: sechs exakte Ergebnisdateien plus isolierter Replay-Nachweis.

## Nachrechnen

Python 3.10 oder neuer; Analyse und Replay verwenden nur die Standardbibliothek.

```bash
python3 -O -B analyze.py
python3 -O -B replay.py
python3 -B verify_package.py
```

Der kontinuierliche Gravitationstest integriert Uhr/Dichte bei Materiekopplung
null exakt und begrenzt den Rest über zusätzliche Elementzahlen. Der gesonderte
atomare Test kontrolliert beide Wirkungsphasen an 921 Endrecords; er ist keine
zertifizierte Quadratur des kontinuierlichen Materieintegrals.
6.240 Rücktransportgleichheiten und 72 Vergleiche fester vergangener Ereignisse
werden mit rational-komplexer Arithmetik geprüft. Kein Monte Carlo oder
physikalisches 4D-Ensemble. Die Nachrechnung ist Wiederholbarkeit derselben
Implementierung, keine unabhängige wissenschaftliche Replikation.

`build_report.py` benötigt ReportLab und DejaVu Sans. `package.py` erzeugt nach
Sichtprüfung des Berichts ein deterministisches Archiv mit SHA-256-Manifest.
Das ausgelieferte Originalarchiv bei eigener Neuverpackung als Referenz behalten.

## Interpretationsgrenze

Erfolgs-/Ausfallwahrscheinlichkeiten des angegebenen Instruments sind gültig.
Normierte Diagonalen eines interferierenden Dekohärenzfunktionals sind dagegen
nicht automatisch klassische Historienwahrscheinlichkeiten: die Negativkontrolle
liefert für ein Atom den Wert 4. Die terminale Elementzahlpartition dekohäriert
bei der Kanalauslese exakt; die geprüfte frühere Partition tut dies nicht.
Eine kophasiert mitbewegte Endauslese entfernt den Interferenzeffekt vollständig.
Randwahl, Zahlgewichtung und Enduhrwert bleiben physikalisch zu begründen.
