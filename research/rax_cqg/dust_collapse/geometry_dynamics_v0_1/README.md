# CST-DUST: stationärer Geometriekandidat v0.1

13. November 2026. Anschluss an PR 290 / Commit `f5ee44d7cb4dc1f924eee580f1eaf0cfcb4a5bc6` in `thomasmgfeller/x6-spectral-astrolabium`.

**Neuer Befund:** Zwei verschiedene Kausalordnungen mit elf Ereignissen besitzen unter denselben festen äußeren Randdaten positive stationäre innere Staubquellen und gerichtete Uhren. Die unveränderte Wirkung liefert

\[
S_0=10-151\rho/38,\qquad S_1=18-105\rho/38,\qquad
\Delta S=8+23\rho/19,\quad 0<\rho<1/2.
\]

Dies ist ein stationärer quellenabhängiger geometrischer Wirkungsvergleich. Physikalische Geometriedynamik, Übergangswahrscheinlichkeiten, Einstein-Korrespondenz und Singularitätsauflösung sind damit **nicht hergeleitet**.

## Konstruktion

Der feste äußere Kragen ist B={0,1,2,3,7,8,9,10}, das Innere I={4,5,6}. C0 ist die vollständige Kette. C1 entfernt nur (4,5) und (5,6), behält (4,6). Alle äußeren und B–I-Relationen bleiben gleich. Der innere Relationszähler ist 3 beziehungsweise 1 und unterscheidet die Geometrien invariant unter gemeinsamer Umnummerierung.

Mit β=4/√6, Δ²=2/(19β), u=T/Δ+5, festen u_j=j und r_j=ρ auf B sind die inneren stationären Werte:

| | C0 | C1 |
| --- | --- | --- |
| u_I | (4,5,6) | (4,4,5) |
| r_I/ρ | (1,1,1) | (2,1,1) |
| q_I am klassischen Punkt q_B=0 | (0,0,0) | (0,0,0) |
| F4 | 10 | 18 |

Alle freien Euler-Gleichungen stammen aus der vollen Wirkung einschließlich der Beiträge des Zukunftskragens. Die innere Staub-Hesseform ist regulär. Bei C1 ist eine innere Skalarmode singulär, aber randgekoppelt: H[:,I] hat Rang drei. Mit demselben Gaußtestgewicht auf allen acht äußeren Skalarvariablen existiert der gemeinsame Abel-Grenzwert. Ein zunächst untersuchter N10-Fork scheitert dagegen an einer vollständig entkoppelten skalaren Nullmode.

## Was sich gegenüber PR 290 ändert

Die Wirkung und ihre Koeffizienten bleiben gleich; die Historienfamilie, stationäre positive Kragenquelle und Uhrauswahl sind neu. Für den affinen N11-Vergleich wird die Uhrbox ausdrücklich auf [-3/2,3/2] erweitert: max|T_B|=5Δ≈1,26945. Eine normierte gleichförmige Uhrintegration hätte dann dt/3 statt dt/2. Hier wird keine solche neue Uhrquadratur berechnet.

Der klassische Randpunkt q_B=0 wird von der anschließend integrierten Skalar-Testpaarung unterschieden. Weder Dirichlet-Punkte noch die reguläre Coarea-Konditionierung werden als bereits hergeleitete physikalische Zustände ausgegeben. Das ursprüngliche Atom-/Positiv-Dichtemaß erzeugt weiterhin D(C)=1/2+i(exp(-iC/2)-1)/C, keinen Delta-Constraint.

Der neue Vergleich ist explorativ. Die sechs kleinen Ordnungsfälle wurden nach struktureller Zulässigkeit geprüft; es wird keine blinde Preregistrierung behauptet. Minimalität betrifft nur die erklärte Cover-Löschungsfamilie mit vierlagigem Kragen.

## Zusätzliche Ergebnisse

- Ein algebraisch zertifizierter regulärer N10-Materiesattel passt sogar in die ursprüngliche Uhrbox [-1,1]. Dazu wird eine neue feste Kragenpräparation gewählt.
- Die direkt aus der Wirkung folgende affine Uhrrekursion ist vorwärts instabil: ein reeller Multiplikator liegt in (-6,-5). Der Randwertkandidat ist deshalb keine stabile Cauchy-Dynamik.
- Vollständige kausale Präfixzerlegung und Quellen-Ableitung der stationären Wirkung sind exakt geprüft.
- Der frühere Sechshistorienpilot besitzt intrinsische Geometrieverläufe, aber seine kohärenten akzeptierten Klassenäste sind nicht additiv. Alte enge Hindernisse werden weder verallgemeinert noch stillschweigend aufgegeben.

## Reproduktion

Python 3.12 und SymPy 1.14.0. Die Rechner verwenden keine Netzwerkzugriffe und keine großen Integrationen.

```sh
python -m pip install -r requirements.txt
python -B verify.py
```

`verify.py` prüft das Manifest, kopiert ausschließlich die Prüfdateien in ein isoliertes Verzeichnis, führt neun Programme aus und verlangt bytegleiche JSON-Ergebnisse. Der PDF-Generator wird nicht ausgeführt. Zusätzliche PDF-Abhängigkeit: `report/requirements.txt`.

- `report/`: siebenseitiger Ergebnisbericht und Generator.
- `contracts/geometry_candidate.json`: vollständiger neuer Kandidatenvertrag mit offenem physikalischem Schluss.
- `agents/`: sechs Fachberichte mit gegenseitigen Gegenprüfungen; KI-Arbeit, kein externes Peer Review.
- `checks/`: neun ausführbare Prüfer, Ergebnisse und relevante gehashte Quellen.
- `MANIFEST.json`: SHA-256 und Größen aller Paketdateien außer dem Manifest selbst.

## Nächster entscheidender Schritt

Für das jetzt explizite Geometriepaar muss eine gemeinsame physikalische Paarung bzw. konsistente Historiendeutung aus Wirkung, Maß und Schnittinformation begründet werden. Atom- und Randterme dürfen dabei nicht verschwinden. Erst daraus können normierte Geometrieverläufe folgen. Eine frei gewählte Normierung, ein ad-hoc-Hamiltonoperator oder die erneute Vergrößerung der Historienfamilie lösen diese Frage nicht.

Die Quellen-/Uhr-/Radiuskalibrierung, vierdimensionale Korrespondenz und globale Staubball-Dynamik bleiben zusätzlich offen. Diese Untersuchung verändert keine GitHub-Inhalte. Die ausführlichen Primärquellen stehen im Bericht und den Fachtexten; sie ersetzen keine Prüfung der neuen Rechnungen.
