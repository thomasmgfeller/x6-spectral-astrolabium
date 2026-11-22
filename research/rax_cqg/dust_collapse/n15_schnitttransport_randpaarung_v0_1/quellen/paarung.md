# CST-DUST · Norm und Interferenz am gemeinsamen Zwischenrand

18. November 2026. Diese Untersuchung schliesst an [PR 307](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/307) an. Herleitung und Quellen stehen im [Bericht](../reports/CST_DUST_Zwischenrand_Norm_Interferenz.pdf). Die Einzelwerte, alle elf nicht absolut konvergenten Paare und die 33 partiellen Vorwärtsamplituden stehen in [ergebnis.json](ergebnis.json).

## Ergebnis

Die vollständige erweiterte Vorwärtsverklebung im festen Acht-Atom-/Grundpaketkanal ergibt ein positives Auslesegewicht von rund 3,27154 × 10⁻⁸. Zwischen den 33 linken Summanden steuern die Kreuzterme zusammen rund 2,27231 × 10⁻⁸ bei. Für die vollständige skalare Auslese wurden getrennt die 1.089 Vorwärts-/Konjugiert-Paare am gleichen Zwischenrand ausgewertet. Davon sind 1.078 absolut konvergent, vier besitzen einen endlichen Fresnel-Grenzwert, sieben wachsen mit der regulierten Feldlänge. Die Rechnung verbindet diese Ergebnisse durch die Frage nach dem Randprodukt. Beide Versuche haben verschiedene Präparationen und Auslesen.

Die Cauchy-Schwarz-Schranke im Bericht schliesst eine endliche positive Norm aus, sofern die bisherigen Testpaketnormen und sämtliche ursprünglichen Paarungen der Testpakete mit der kohärenten Geburtsantwort erhalten bleiben. Der einfache endliche Rest hat bereits auf zwei beschrifteten Summanden eine negative Determinante. Die physikalische Norm relativ zum leeren Zweig bleibt offen.

## Nachrechnung im Repository und offline

Die Hauptrechnung verwendet Python 3.10 oder neuer und seine Standardbibliothek. Sie kontrolliert die Git-Blob-IDs der archivierten Eingaben. Der Prüfwert der Grundpaketamplitude stammt aus dem veröffentlichten Arb-Intervall. Der vollständige Bericht kann aus der mitgelieferten TeX-Quelle mit pdfLaTeX gebaut werden.

Im Verzeichnis dieser Studie oder im entpackten [Offline-Prüfpaket](../packages/CST_DUST_Zwischenrand_Pruefpaket.zip) ausführen. Die Repository-Fassung liest die Eingaben aus den ursprünglichen Studien. Das Archiv enthält dieselben Eingaben für die lokale Nachrechnung.

```bash
python3 -B -O pruefung.py --out nachrechnung.json
cmp ergebnis.json nachrechnung.json
```

Der Bytevergleich ist in der Erstellungsumgebung geprüft. Andere Mathematikbibliotheken können die letzten Stellen von Gleitkommakontrollen ändern. Die Beweise und die rational bestimmte Einteilung hängen von diesen Stellen nicht ab.

Die separate Gegenprobe verwendet eine vorhandene NumPy-Installation. Sie rekonstruiert die 1.089 gemeinsamen Ordnungen direkt, berechnet die 33 linken Teilamplituden aus den Eigenwerten der komplexen Gesamtmatrix und integriert die kohärente skalare Antwort bei zwei Regulatorwerten auf dem gemeinsamen Feldgitter. Weitere Kontrollen verwenden die separate axiale Fresnel-Formel und die transversalen Einzelgewichte aus PR 307.

```bash
OPENBLAS_NUM_THREADS=1 python3 -B -O gegenprobe.py
```

## Geltungsbereich und Quellen

Die Ausgabe ist eine interne Modellrechnung. Der regulierte Vergleich auf der ausgehenden Staubatomkomponente genügt zum Ausschluss. Die anderen ausgehenden Dichtestrata werden für diese Schranke nicht numerisch integriert. Das aufgelöste Uhrrecord und das Dichteatom des zweiten Versuchs folgen PR 306, die erweiterte Vorwärtsverklebung dem ausdrücklich engeren Acht-Atom-Kontrollsektor. Der Faktor für die Geburtsnorm relativ zum leeren Zweig ist in keinem der beiden Verträge festgelegt. Der P3-Pilot für M = 1 bleibt auf seiner ersten Dichtestufe bei 0 von 38 physikalischen Vergleichen.

[quellen.json](quellen.json) führt für jede übernommene Datei den Originalpfad und die Git-Blob-ID im Commit bc13f4e7e1119d1afaeff62780a4081109af8f98 auf. [LICENSE](../amplitude_existence_v0_1/LICENSE) und [NOTICE](../extended_sewing_v0_1/NOTICE) gehören zu den übernommenen Projektquellen. Die neuen Programme und der Bericht stehen ebenfalls unter Apache-2.0.
