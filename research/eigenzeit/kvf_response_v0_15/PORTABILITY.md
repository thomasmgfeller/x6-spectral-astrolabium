# Numerische Reproduktion auf verschiedenen Plattformen

Der ursprüngliche lokale Lauf und sein sauberer Reproduktionslauf waren
bytegleich. Der erste GitHub-Actions-Lauf unter Python 3.12.15 bestand
den Vergleich aller sechs JSON-Ergebnisse und scheiterte am strengeren
Bytevergleich von M0.npy:
https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/41325551714 .

Ein lokaler Kontrolllauf mit unveränderten Programmen, Seeds und
Abhängigkeiten, aber OPENBLAS_CORETYPE=Haswell statt des automatisch
gewählten SkylakeX-Pfads, reproduzierte den Unterschied:

| Datei | Größte absolute Wertabweichung |
|---|---:|
| M0.npy, M1.npy | 2.220446049250313e-16 |
| M0_blocks.npy, M1_blocks.npy | 1.1102230246251565e-16 |
| endpoint_M0.npy, endpoint_M1.npy | 0 |

Das Originalarchiv, beide Fixierungen, Programme, Daten, PDF und der
ursprüngliche strenge Reproduktionsweg bleiben unverändert.

## Zwei explizite Prüfarten

- publication_check.py --replay verwendet den ursprünglichen Bytevergleich.
- publication_check.py --portable-replay verwendet zusätzlich eine
  offengelegte numerische Vergleichsregel für Rohdaten. Diese ist der
  Einstieg der plattformübergreifenden CI.

Die neue Regel verlangt identische Dateiinventare, Arrayformen und
float64-Datentypen sowie ausschließlich endliche Werte. Für jede
Rohdatendatei gilt rtol=0 und

absolute Toleranz = 8 * eps(float64) * max(1, max(abs(Originalwerte))).

Die größte tatsächliche Abweichung und Bytegleichheit werden für jede
Datei ausgegeben. Die Regel kann daher keinen bytegleichen Lauf vortäuschen.
Die JSON-Werte werden weiterhin mit dem unveränderten Vergleich des
Originalpakets geprüft (rtol=2e-10, atol=2e-12); Kategorien und Text
müssen exakt übereinstimmen. Die Zähler liegen weit unter einer Größe,
bei der diese Toleranz einen Unterschied von einem Treffer zulassen würde.

Der separate Audit wird auf den neu erzeugten Blockdaten mit seinen
fixierten Seeds und Radien erneut ausgeführt und mit dem Originalergebnis
verglichen. Die numerischen Toleranzen sind keine Messunsicherheiten.

Negative Kontrollen des Rohdatenvergleichs müssen eine Veränderung um
1e-9, eine Umordnung, einen Datentypwechsel, eine fehlende Zeile und
einen NaN-Wert zurückweisen. Ein einzelner benachbarter float64-Wert
bleibt innerhalb der ausdrücklich ausgewiesenen Rundungstoleranz.
