# CST-DUST: Messmodell und kontinuierliche Materiephase v0.1

Arbeitspaket vom 7. November 2026, auf Main nach PR 254 aufgebaut
(`35a0d886c4a7ca1d639f09b2933ffeb6c255ad9e`).

**Ergebnis:** Ein explizites unitäres Hilfssystem realisiert Zahlkanäle mit
kohärentem Filter. Ein reiner Elementzähler ist phasenblind und genügt dafür
nicht. Die kontinuierliche Materiephase ist für n=0,1,2 mit exakten rationalen
Momenten und einer maximalen Einzelamplituden-Restschranke unter 1,65e-14
integriert. Nicht integrierte n≥3-Feldphasen und die Normmasse oberhalb n=6
werden getrennt eingeschlossen. Alle acht physikalischen Gates bleiben HOLD.

## Lesen

- `DERIVATION.md`: Definitionen, Beweise, Ergebnisse und Geltungsgrenzen.
- `operational_contract.json`: maschinenlesbarer Status.
- `CST_DUST_Messmodell_Kontinuierliche_Materiephase_v0_1.pdf`: kompakter Bericht.
- `plan.json`, `plan.sha256`: lokal eingefrorener Prüfplan.
- `inputs/provenance.json`: sechs unveränderte Quellen mit Commit und Git-SHA.
- `results/`: sechs exakte Ergebnisdateien und Replay-Nachweis.

## Nachrechnen

Python 3.10 oder neuer; Analyse und Replay verwenden nur die Standardbibliothek.

```bash
python3 -O -B analyze.py
python3 -O -B replay.py
python3 -B verify_package.py
```

36 Kopplungs-/Gewichts-/Uhrdauerfälle, 390 Prüfungen der Wirkungsformeln,
16 unabhängige Kontrollen niedriger Momente sowie eine exakte 16×16-unitäre
Messkopplung. Der Replay erzeugt die sechs Ergebnisdateien aus den Eingaben
in einem frischen Verzeichnis und fordert Bytegleichheit. Dies ist
Wiederholbarkeit derselben Implementierung, keine externe wissenschaftliche
Replikation oder formale Beweiszertifizierung.

`build_report.py` benötigt zusätzlich ReportLab und DejaVu Sans.
`package.py` erzeugt nach visueller Berichtskontrolle ein deterministisches
Archiv mit vollständigem SHA-256-Manifest. Das Originalarchiv bei eigener
Neuverpackung als Referenz behalten.

## Interpretationsgrenzen

Die unitäre Messrealisierung setzt kohärenten Zugriff auf vollständige
Historien voraus. Sie beweist nicht, dass ein solcher Detektor physikalisch
existiert oder die Kosmologie ihn auswählt. Ein ignorierter Messausgang
erhält die Elementzahlverteilung, muss aber den Geometriezustand innerhalb
eines Zahlsektors nicht erhalten. Die Funktionalidentität des Vorgängers
ist deshalb nicht als Identität des nichtselektiven Zustandskanals zu lesen.

Die kontinuierlichen Integrale werden vollständig nur bis n=2 behandelt.
Die unbegrenzten Erfolgsintervalle sind gültige konservative Schranken;
die fehlenden n≥3-Feldphasen sind nicht heimlich auf null gesetzt.
Keine physikalischen Kopplungen, keine 4D-Quantendynamik und kein Bounce
werden ausgewählt. Keine neuen physikalischen Ensembles und keine bezahlten Läufe.
