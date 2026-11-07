# CST-DUST: kontinuierlicher Vier-Element-Sektor v0.1

Vollständige Integration aller 40 natürlichen Vier-Element-Ordnungen im
geerbten kontinuierlichen Uhr-/Dichtemaß. Enthalten sind Kostenentscheidung,
beschleunigter Intervallkern, analytische Quadraturreste, 240 Geometrieamplituden
und 36 kombinierte Fälle mit getrenntem höherem Zahlrest.

**Alle acht physikalischen Gates bleiben HOLD.** Dichtemaß, kohärenter
Historienzugriff und Endrandwahl sind nicht physikalisch hergeleitet.
Feldphasen ab n=5 bleiben offen. Kein Bounce oder Junction Law wird behauptet.

## Nachrechnen

Voraussetzungen: Python 3.12 und `g++` mit C++17, signiertem `__int128` und
Überlauf-Builtins; für die wissenschaftliche Rechnung keine weiteren Pakete.
Der Compiler erzeugt nur eine vorübergehende lokale Binärdatei.

```sh
python3 -O -B analyze.py
python3 -O -B replay.py
python3 -B verify_package.py
```

Die vier nichttrivialen n=4-Konfigurationen brauchen insgesamt 1 305 984
Tensorpunkte und 31 343 616 Dichtefunktionsaufrufe. Je Konfiguration gilt
ein Timeout von 600 Sekunden. Kein bezahlter Rechendienst wird angesprochen.
Laufzeiten hängen vom Rechner ab. Bei fehlendem Compiler oder überschrittenem
Budget bricht die Rechnung mit Fehler ab.

Der Replay kompiliert und berechnet alle neuen Integrale erneut und verlangt
sechs bytegleiche Ergebnisdateien. Die zwölf gepinnten Vorgängerquellen bleiben
unverändert. Das belegt interne Wiederholbarkeit, keine externe Replikation.

## Dateien

- `DERIVATION.md`: Maß, Wirkung, Integrations- und Intervallbeweise, Grenzen.
- `plan.json`, `plan.sha256`: vor neuer Rechnung eingefrorener Plan.
- `native.py`, `kernel.cpp`: zertifizierte Eingaben und beschleunigte Intervalle.
- `analyze.py`: Kontrollen, neue Integrale und Fehlerfortpflanzung.
- `inputs/`: zwölf Quellen aus Main nach PR 256 mit Herkunftsbelegen.
- `results/`: rationale Ergebnisse, Kostenentscheidung, Zertifikate und Replay.
- `four_element_contract.json`: maschinenlesbare Aussagegrenzen.

PDF-Erzeugung: `python3 -B build_report.py`, zusätzlich ReportLab und DejaVu Sans.
Archiv-Erzeugung nach abgeschlossener Prüfung: `python3 -B package.py`.

Nächster sinnvoller Kandidat: die konservative höhere Normrestschranke
alpha-abhängig schärfen und erst danach den Nutzen weiterer Feldintegrationen
gegen ihren Rechenaufwand abwägen. Die physikalische Auswahl bleibt separat offen.
