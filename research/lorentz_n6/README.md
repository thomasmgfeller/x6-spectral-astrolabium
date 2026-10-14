# Exakter Lorentz-Kollisionsatlas n=6 — Version 0.1

Stand: 14.10.2026. Ausgeführte endliche Replikation, keine allgemeine
Rekonstruktionsaussage, kein Kontinuums- oder Physiknachweis.

## Ergebnis

| Verfahren | Klassen aus 318 Ordnungen | Ungelöste Paare |
|---|---:|---:|
| Drei Spektren S, A, SA−AS | 286 | 37 |
| Zusätzlich geordnetes Paar (Minima, Maxima) | 314 | 4 |
| Quill-Vergleichsbasis: S, S2, Minima, Maxima, Isolierte | 285 | 33 |
| Vergleichsbasis und maximale Quill-Antworten | 318 | 0 |

S=C+Cᵀ, A=C−Cᵀ, S2=C²+(C²)ᵀ. C² zählt zweigliedrige
Relationspfade; es ist keine boolesche Abschlussoperation.
Die beiden Vergleichsbasen sind verschieden. 33 ist nicht die Zahl der
Kollisionen aus den drei Spektren. Gruppen, Paare und Anzahl zusätzlicher
Elemente innerhalb einer Klasse werden getrennt ausgewiesen.

Literatur: Yazdi, Letizia, Kempf, *Lorentzian Spectral Geometry with Causal Sets*,
Class. Quantum Grav. 38 (2021) 015011,
https://doi.org/10.1088/1361-6382/abc3f8, Tabellen 1–2 (C-Spalten), Tabelle 4,
Abschnitt 4.2. Repliziert ist hier ausschliesslich n=6. Die Arbeit untersuchte
auch grössere Ordnungen; daraus wird kein eigener Neuheitsanspruch abgeleitet.

## Vollständigkeit und exakte Arithmetik

`atlas.py` untersucht alle 32'768 oberen binären Dreiecksmatrizen. 4'824
sind transitiv. Jede endliche Ordnung besitzt eine topologische Beschriftung,
also ist diese Enumeration vollständig. Umkehrordnungen werden nur dann
identifiziert, wenn sie tatsächlich isomorph sind.

Die kanonische Kodierung ordnet Zellen nach (Eingangs-, Ausgangsgrad) und
probiert jede Permutation innerhalb der Zellen. Isomorphismen erhalten diese
Zellen; damit bleibt die Reduktion exakt. Alle 318 Repräsentanten,
Beschriftungsmultiplizitäten, Polynome und Kollisionsgruppen stehen in
[`results/atlas_n6.json`](results/atlas_n6.json).
Python-Ganzzahlen und Faddeev–LeVerrier bestimmen die charakteristischen
Polynome. Gleitkomma-Eigenwerte und Hashes entscheiden keine Spektralgleichheit.

Eine zukünftige Quill an v fügt ein neues Element z mit v≺z hinzu und
übernimmt alle Vorgänger von v. Die Vergangenheit wird dual konstruiert.
Die alte Ordnung bleibt als induzierte Teilordnung erhalten. Im Hasse-Diagramm
entsteht genau eine neue Verbindung. Jeder maximale Anker wird einzeln
perturbiert. Das sortierte **Multiset gepaarter** Polynome (S,S2) ist die
Antwort; Multiplizitäten und die Zuordnung beider Spektren bleiben erhalten.
Vergangenheitsquills an allen Minima sind ebenfalls gespeichert, aber für
den n=6-Nachweis aus Tabelle 4 nicht nötig.

## Unabhängiger Rechenweg

`verify.py` importiert weder Atlas- noch Agentenalgorithmen. Es erzeugt
Ordnungen rekursiv durch Hinzufügen eines maximalen Elements mit einem
Ordnungsideal als Vergangenheit. Gerichtete Backtracking-Bijektionen prüfen
Vollständigkeit und Nichtisomorphie. Bareiss-Determinanten an ganzzahligen
Stützstellen mit rationaler Newton-Interpolation prüfen alle 4'208 Polynome.
Quills werden über einen separat implementierten transitiven Abschluss geprüft.
Kollisionsgruppen werden vollständig neu berechnet.

Das ist algorithmische Gegenprüfung innerhalb dieses Projekts, keine externe
Begutachtung. Die Null-Kollisions-Aussage gilt für diesen endlichen Korpus.

## Reproduktion

Aus dem Repository-Hauptverzeichnis, Python 3.12 und NumPy 2.3.5:

```sh
python research/lorentz_n6/atlas.py --output /tmp/atlas_n6.json
python research/lorentz_n6/verify.py /tmp/atlas_n6.json --output /tmp/atlas_check.json
python -m unittest tests/python/test_lorentz_n6.py -v
```

Die vollständige Ausgabe ist deterministisch. `--seconds` begrenzt den
Atlaslauf; n>6 wird absichtlich zurückgewiesen. Ein Abbruch produziert keinen
als vollständig deklarierten Atlas. Der unabhängige Prüfer benötigt nur die
Python-Standardbibliothek. Der bestehende zeitgesteuerte n=3..5-Agent und
sein genehmigtes Zeitfenster werden durch dieses eigenständige Paket nicht verändert.

## Nächster Forschungsentscheid

Die vier Kollisionspaare nach Endpunktanreicherung sind explizite Ansatzpunkte
für Strukturfragen. Vor einer Erweiterung auf n=7 stehen Literaturabgrenzung,
Laufzeitbudget und die genaue neue Hypothese. Das blosse Wiederholen dieses
festen Atlas erzeugt zusätzliche Regressionsevidenz, keine neuen Ordnungen.
