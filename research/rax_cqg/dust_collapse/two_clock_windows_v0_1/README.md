# CST-DUST · Zwei Uhrfenster am verklebten Rand

[Bericht (PDF)](../reports/CST_DUST_Zwei_Uhrfenster_Am_Verklebten_Rand.pdf) · [Offline-Prüfpaket (ZIP)](../packages/CST_DUST_Zwei_Uhrfenster_Pruefpaket.zip) · [Normierung der Null- und Ein-Ereignis-Antwort](../zero_one_pairing_v0_1/README.md)

Die Studie prüft, wie frühere Geburtszeiten in einer späteren Messung derselben diskreten Wirkung unterschieden werden können. Sie schliesst an die gemeinsame Normierung von null und einem inneren Ereignis in [PR 309](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/309) an. Eine Hälfte enthält 33 beschriftete Ordnungen. Der zweite Gebietsschnitt verklebt alle 1 089 Paare. Dichte und Uhr des späteren inneren Ereignisses bleiben als gemeinsames Record erhalten. Die frühere innere Dichte wird vollständig integriert. Der gewählte Produktraum am späteren Record und die äusseren Skalarpakete sind Teil des Versuchs.

## Ergebnisse

- Der direkte Uhrenkopplungsterm hat in 702 Ordnungen Koeffizient −9, in 338 Koeffizient null und in 49 Koeffizient 16.
- Am Mittelschnitt des Fensters (0, 1/8) macht der reale Kreuzterm einschliesslich des konjugierten Terms numerisch 49,908831724 % des kohärenten Gesamtgewichts aus. Die beiden Teilfenster bleiben stark kohärent.
- Das Gesamtgewicht wächst für kurze Fenster quadratisch. Positiver Anfangskoeffizient und endliche obere Schranke werden mit rationalen Intervallen nachgewiesen. Für die vereinbarten Referenzuhren bleibt die bedingte Verteilung des Geburtszeitpunkts bei genau einer Geburt gleichförmig, während die beiden linearen Gesamtgeburtsraten verschieden sind. Die physikalische Normierung bleibt offen.

## Nachrechnung

Die rationale Fensterrechnung und das Zertifikat für die positive Untergrenze benötigen nur Python 3.10 oder neuer. Die numerische Verklebung und ihre Gegenprobe nutzen zusätzlich NumPy. Geprüft mit Python 3.12.14 und NumPy 2.3.5. Es werden weder Netzwerkzugang noch Zufallszahlen benötigt. Im Verzeichnis dieser Studie oder im entpackten Prüfpaket ausführen. Die Repository-Fassung liest ihre Eingaben aus den verknüpften Vorstudien. Im entpackten Paket prüft zusätzlich `sha256sum --check SHA256SUMS` alle mitgelieferten Dateien.

```sh
python3 -B schnitt.py --out schnitt_replay.json
cmp schnitt.json schnitt_replay.json
python3 -B anfangsgrenze.py --out anfangsgrenze_replay.json
cmp anfangsgrenze.json anfangsgrenze_replay.json
OPENBLAS_NUM_THREADS=1 python3 -B verklebung.py --out verklebung_replay.json
cmp verklebung.json verklebung_replay.json
OPENBLAS_NUM_THREADS=1 python3 -B gegenprobe.py
```

Der Bytevergleich der numerischen Ausgabe bezieht sich auf die Referenzumgebung. Die Gegenprobe verwendet direkte Gesamtordnungen, Eigenwerte der vollen Wirkungs-Matrizen, eine zusammengesetzte Quadratur und explizite Toleranzen. Die beiden rationalen Rechnungen verwenden nach aussen gerundete Intervalle. Die Prüfungen sind interne Nachrechnungen.

| Datei | Inhalt |
|---|---|
| [Bericht](../reports/CST_DUST_Zwei_Uhrfenster_Am_Verklebten_Rand.pdf), `bericht.tex` | Vollständige Herleitung und Geltungsbereich |
| `schnitt.py`, `schnitt.json` | Zwei reduzierte Randprodukte, Schnitte bei 1/3, 1/2 und 2/3 des Fensters, exakte Präfixformeln und Ranggrenzen |
| `verklebung.py`, `verklebung.json` | 1 089 gemeinsame Wirkungen, 17 Uhrkoeffizienten-Muster, zwei Zeitteilungen, reeller und imaginärer Kreuzterm |
| `anfangsgrenze.py`, `anfangsgrenze.json` | Direkte Rekonstruktion der 1 089 Ordnungen, Intervallrechnung der skalaren Amplituden, positive Untergrenze |
| `gegenprobe.py` | Unabhängige Eigenwert- und Quadraturkontrolle der beiden Verklebungsmatrizen und der Anfangsnorm |
| `quellen.json` | Herkunft und Git-Kennungen der ursprünglichen Dateien. Die Quellen und die [Lizenz](../amplitude_existence_v0_1/LICENSE) liegen dem Prüfpaket bei. |
| `SHA256SUMS` im Offline-Paket | Prüfsummen aller mitgelieferten Dateien ausser der Prüfsummendatei |

[Quellenstand nach PR 309](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/f461985f67aa0c1aef972d529a9b09575fe8df77/research/rax_cqg/dust_collapse)
