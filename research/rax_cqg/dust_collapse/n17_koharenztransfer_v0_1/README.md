# CST-DUST · Kohärente und zeitgemischte Uhr am N17-Zukunftsrand

22. November 2026. Auf zwei markierten Ordnungen verändert die kohärente Projektion einer früheren Uhr die bedingte Wahrscheinlichkeitsdifferenz zweier Pakete mit entgegengesetztem Anfangsstrom. In beiden Armen lautet die einzige Dichteauslese am Spätereignis (t>1/8). Der kohärente Arm konditioniert auf den konstanten Uhrmodus. Der zeitgemischte Arm summiert die Beiträge sämtlicher Uhrmodi. Jeder Arm wird pro Eingangspräparation einmal normiert.

| N15-Ausgangstyp | Vergleich | Rationale Einschliessung des Primärkontrasts für ganze Pakete |
|---|---|---|
| 375841 | Bekannter Anschluss, vollständiges ursprüngliches Paar | [−3,631; −3,116] × 10⁻²⁷ |
| 375841 | Dasselbe Verfahren, halbe Eingangsvariation | [−1,903; −1,472] × 10⁻²⁷ |
| 42429 | Vorab festgelegter Transfer, anderes Poset und anderes Paketpaar | [−2,639788; −2,639503] × 10⁻²³ |

Die Tabellengrenzen sind nach aussen gerundet. Der Primärkontrast ist der Unterschied zwischen dem Vorzeichenkontrast im kohärenten und im zeitgemischten Arm. Das Minuszeichen gibt seine Richtung an. Am neuen Typ liefert die unabhängige Zentrumsquadratur bereits bei scharfer Uhr einen positiven Vorzeichenkontrast von rund 3,6368451 × 10⁻²¹. Die kohärente Uhr verkleinert ihn auf rund 3,6104486 × 10⁻²¹. Die grössere absolute Zahl am zweiten Typ erlaubt keinen Vergleich der Empfindlichkeit der Geometrien, weil die Pakete verschieden sind.

## Herkunft und Zeitpunkt

- Die Dateien unter `basis/n17` stammen aus PR 349, der Einzelzeuge `basis/zeuge42429.py` aus der älteren Vorzeichenprüfung. Die mitgelieferten Quelldateien sind an den Git-Stand der [Vorgängerstudie](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/83b8a71bb96f2d794ecc35909f8102c20901f7f6) gebunden.
- Die Ausgänge auf 375841 sowie die N15-Einzelzeugen beider Vorzeichen auf 42429 waren bei der Planung bekannt. Der 42429-Typ wurde aufgrund seiner Struktur gewählt. Seine N17-Zieldichte blieb während der Zulassungsprüfung unausgewertet.
- Vor der ersten 42429-Zielauswertung wurde der [Prüfvertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7baa149a5c42de920d9249f30caeba6d527ebc9b/research/rax_cqg/dust_collapse/n17_koharenztransfer_v0_1/TRANSFER_42429.md) öffentlich festgehalten, aus dem Remote-Commit zurückgelesen und byteweise verglichen. Die Hypothese legte einen von null verschiedenen Kontrast fest. Beide Richtungen waren zugelassen. Der erste vereinbarte Rechenschritt mit 16 Teilintervallen und Taylorgrad 5 trennt das Ergebnis von null. Zulassung, exakte Auswertung und unabhängige Quadratur sind getrennte Programme. In `zulassung.json` bezeichnet `target: NOT_RUN` den früheren Status beim Abschluss der Zulassung. Die spätere Entscheidung steht in `transfer.json`.
- Die zusätzliche Rechnung zur markierten Masse auf Typ 2324 ist eine eigenständige, explorative Modellprüfung. Für alle 60 physikalischen P3-Punkte gilt weiterhin `NOT_RUN`.

## Ergebnisse im Einzelnen

[375841 · Zeitmischung auf ganzen Paketen und bedingte Erfolgsrate](KONTROLLE.md) · [Breitenkontrolle an den Zentren](QUADRATUR.md)

[42429 · Vorab veröffentlichter Vertrag](TRANSFER_42429.md) · [Zulassung und Ausgangsnormen](ZULASSUNG.md) · [Beweis der Transferschranke](TRANSFER_BEWEIS.md) · [Unabhängige Quadratur](TRANSFER_QUADRATUR.md)

[2324 · Zwei Ladungsmessungen und ein exaktes Gegenpaar zur Massenauslese](MASSENTEST.md)

## Offline nachrechnen

Im entpackten Verzeichnis mit Python 3.9 oder neuer ausführen.

```sh
python3 -B pruefen.py
python3 -B pruefen.py --gegenprobe
```

Die erste Zeile kontrolliert alle SHA-256-Einträge und reproduziert die rationalen Ergebnisse mit der Standardbibliothek. Die zweite ergänzt beide Zentrumsquadraturen und eine unabhängige komplex-rationale Matrixelimination. Getestet mit Python 3.12, mpmath 1.3.0 und SymPy 1.14.0. Die Quadraturwerte sind empirische Kontrollen. Für den 42429-Primärentscheid zählen die rationalen Intervallgrenzen.
