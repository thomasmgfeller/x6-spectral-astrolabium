# CST-DUST · Was vom frühen Messbit im Uhrfenster bleibt

23. November 2026 · N15-Typ 2097151 · markierte Dosis 1 · Referenz e=1/4

Die vorangegangene Fourier-Messung der Staubuhr 5 verschiebt 29,73576 % der Hilfsnorm aus den beiden präparierten Paketen. Davon liegen 27,21565 Prozentpunkte in 14 weiteren Paketen innerhalb des ursprünglichen N15-Uhrfensters und 2,52011 Prozentpunkte ausserhalb. Im Inneren lässt sich der Transport mit der vorhandenen Wirkung bis hinter 12 berechnen. Eine optimale Auslese kann 97,41474 % des akzeptierten Anteils fehlerfrei dem früheren Bit zuordnen, wenn sie bei den übrigen Fällen „unentschieden“ melden darf.

| Frage | Ergebnis |
|---|---|
| Wie gut ist ein zwingend binärer Vergleich hinter 12? | Auf dem akzeptierten Anteil erreicht die Wiederholung des ursprünglichen Impulsfilters 98,70737 % richtige Antworten. Die optimale binäre Auslese erreicht 99,98329 %. |
| Gibt es einen Vergleichsdetektor für das ursprüngliche Uhrfenster? | Ein endlicher Translationsoperator mit offenen Enden liefert zwei orthogonale Ergebnisräume, die sich bis hinter 12 exakt weitertragen. Die gewählten Dichtefenster werden mit 50,00004648 % Trefferquote unterschieden. |
| Wie ändert sich die späte Interferenz hinter 13? | Beim fensterinternen Detektor verbleiben 57,09003 % des pulsfreien Kontrasts. Beim akzeptierten Zweig der Messung auf der Geraden sind es 99,99999999794 %. |
| Liefert die Staubwirkung den nötigen Übergang? | Unter feldunabhängigen starren Translationen ist nur die gemeinsame Verschiebung aller 15 Uhren eine Symmetrie. Sie lässt die relative Koordinate u₅ unverändert. Der endliche Translationsoperator bleibt eine zusätzliche Annahme. |
| P3 | 60 × NOT_RUN. Die Rechnungen verwenden die deklarierte positive Hilfsnorm. Eine physische Randkopplung, ihr Skalarprodukt und die unabhängige positive Masseneichung stehen aus. |

## Reproduktion

Alle Rechnungen laufen lokal auf der CPU. Für die Fenster-, Symmetrie- und Intervallbeweise genügt die Standardbibliothek von Python. Die unabhängigen Matrix- und Quadraturprüfungen in schnitt.py verwenden NumPy.

```sh
sha256sum -c SHA256SUMS
python3 -B fenster.py
python3 -B endintervall.py
OPENBLAS_NUM_THREADS=1 python3 -B schnitt.py
```

HERLEITUNG.md enthält die Normierung, den Transportbeweis, die optimalen Fehlergrenzen sowie den Vergleich mit dem endlichen Detektor. fenster.json und endintervall.json enthalten nach aussen gerundete rationale Zertifikate. schnitt.json enthält die Vierphasenauslese, die Wiederholungsprüfungen, den Vergleich von 144 Verklebungen und drei Pulswahlen. Die Quellen sind durch Git-Blob und SHA-256 bzw. bei Vorstudien durch SHA-256 identifiziert. Der Hauptplan und die drei Ergänzungen wurden lokal vor ihren jeweiligen Auswertungen gehasht. Es gab keinen externen Zeitstempel oder Blindtest.

[Geprüfter Stand des Forschungsprogramms](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/f6d78fd5ef60b120da406a92b65b847494fa9cdf/research/rax_cqg/dust_collapse)
