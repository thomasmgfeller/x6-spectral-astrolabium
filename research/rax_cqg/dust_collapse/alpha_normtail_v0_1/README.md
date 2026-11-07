# CST-DUST: α-abhängige Normrestschranke v0.1

Das Paket schärft den Normrest des veröffentlichten Vier-Element-Referenzmodells
durch α und die exakt bekannten 4824 Sechs-Element-Ordnungen. Es berechnet
keine neuen Feldintegrale. Alle acht physikalischen Gates bleiben HOLD.

- `DERIVATION.md`: vollständiger unendlicher Beweis, Ergebnisse und Grenzen.
- `bounds.py`: exakte rationale Majoranten.
- `analyze.py`: zwei Enumerationen, Negativkontrollen und 36 Intervallverfeinerungen.
- `inputs/`: acht unveränderte Quellen aus Main nach PR 257.
- `results/`: fünf exakte Ergebnisdateien und Replay-Beleg.
- `alpha_normtail_contract.json`: maschinenlesbarer Aussageumfang.

Python 3.12 und ausschließlich die Standardbibliothek genügen zur Nachrechnung:

```bash
python3 -B analyze.py
python3 -B replay.py
python3 -B verify_package.py
```

Der Replay setzt das festgelegte Zeitlimit von 180 Sekunden durch. Er benötigt
keinen C++-Compiler und ruft den nativen Integralkern des Vorgängers nicht auf.
Die acht gepinnten Quellen enthalten ausdrücklich die bereits zertifizierten
Amplituden und ihre Fehler. Diese werden übernommen und nicht neu zertifiziert.
Ein Neubau des Berichts mit `build_report.py` benötigt zusätzlich ReportLab
und die DejaVu-Schriftfamilie. `package.py` erstellt das deterministische ZIP.

Normierungssumme bis n=6; Feldintegration weiterhin bis n=4. Die n=7-Enumeration
dient ausschließlich der endlichen Validierung. Für α<1 wird kein gültiges
Zertifikat oder Divergenzsatz behauptet. Die ausführbare Implementierung
beschränkt sich für exakte rationale Potenzen auf ganzzahlige α≥1.

Interne bytegleiche Wiederholbarkeit ist keine externe Replikation und keine
formale Verifikation. Das physikalische Maß, die Auslese und die Randwahl
bleiben offen; ein Bounce ist nicht hergeleitet.
