# CSPP v0.7: Anfangsdatenadapter und skalare Propagation

28. Oktober 2026. **Der skalare Benchmark besitzt jetzt einen ausdrücklich
definierten Anfangsdatenadapter und getrennte Fehlerkontrollen bis zu den
Messwerten. Eine Genauigkeitsfreigabe folgt daraus nicht: Alle 1.554 geprüften
Feld-/Adapterfälle überschreiten 10 % relativen RMS.** G1 bleibt HOLD,
G2/G3 NOT_RUN. Es wurde keine neue Zufallswolke erzeugt.

## Was hinzugekommen ist

Die bisherigen 64 Archivwolken werden für m=1 und die festen Wellenzahlen
k=0,2,4,8 erneut verwendet. Die Quelle beginnt weiterhin bei t=-1.
Ein linearer Adapter H1 und ein kubischer Adapter H3 setzen die vorgegebenen
Cauchy-Daten f,g in die benötigte diskrete Vergangenheit fort:

\[
H_1=f+\tau g,\qquad
H_3=f+\tau g+\tfrac12\tau^2(\Delta-m^2)f
+\tfrac16\tau^3(\Delta-m^2)g,\quad\tau=t+1.
\]

Es werden keine neuen Anfangsflächenpunkte eingefügt. Beide Adapter verwenden
die vorhandenen History-Knoten bei t<=-1. Sie benötigen analytisch bekannte
f,g und Laplacians; ein Verfahren zum Rekonstruieren dieser Ableitungen aus
verrauschten diskreten Messdaten ist damit noch nicht gegeben.

Zusätzlich bleibt der kompakte Bump mit Radius 1/2, Trägerwellenzahl 4 und
verschwindender Anfangsgeschwindigkeit fest. Auf der vorab gewählten Wolke
**d0_r00** werden alle drei Massen m=0,1,2 vollständig untersucht. Dazu
kommen **1.341 neue Kontinuumseinschließungen an 447 aktiven Knoten** pro
Präzisionsstufe hinzu. Die 84 bereits eingeschlossenen Probe/Masse-Werte
aus v0.3/v0.5 bleiben erhalten.

| Teil des Benchmarks | Umfang |
|---|---:|
| Exakte homogene Wellenkontrollen | 64 Wolken × 3 Glättungen × 4 Wellenzahlen × 2 Adapter = 1.536 Fälle |
| Kompakte Quelle | 1 feste Wolke × 3 Glättungen × 3 Massen × 2 Adapter = 18 Fälle |
| Beobachtungen je Fall | 28 unveränderte Punktproben |
| Zusätzliche Beobachtung | Gewichtete Intensität an den sieben Detektorpunkten |

Die neue Punktintensität ist eine eindeutig definierte skalare Diagnose.
Sie ist **keine räumliche Detektorintegration und keine Wahrscheinlichkeit**.
Die noch zu breiten räumlichen Einschließungen aus v0.5 bleiben offen.

## Die Fehler werden bis zur Beobachtung getrennt

Jeder Ergebnisdatensatz enthält vier Beiträge:

1. **Operator und endliches Gebiet:** diskrete Lösung mit eingeschlossener
   Kontinuumshistorie minus Kontinuumsreferenz. Lokale Defekte an sämtlichen
   aktiven Knoten werden zusätzlich bis zu den Proben fortgepflanzt.
2. **Anfangsdatenfortsetzung:** Lösung mit exakt ausgewertetem H1/H3 minus
   der Orakellösung. Der Orakelwert ist nur eine Kontrolle, kein Adaptereingang.
3. **Anfangsdatenauswertung:** Fehler der tatsächlich gerundeten History-Werte,
   bis zu den Proben durch das exakte diskrete System fortgepflanzt.
4. **Numerische Lösung und Koeffizientenrechnung:** Float-Ergebnis minus
   eingeschlossener exakter diskreter Lösung bei denselben gerundeten Eingaben.

Die signierten Beiträge summieren sich zum Gesamtfehler. Für die Punktintensität
werden dieselben vier Stufen mit eigener absoluter Störungsschranke ausgewiesen.
Die Beiträge werden nicht als unabhängige Zufallsvarianzen behandelt.

Eine eingeschlossene Verstärkungsschranke gilt außerdem für **jede**
History-Störung, nicht nur für eine einzelne konstante Teststörung. Die
[Herleitung](METHODS.md) zeigt ausdrücklich, wie Unsicherheiten von f,g und
deren Laplacians dadurch bis zu den Beobachtungsgrößen weitergegeben werden.

## Ergebnis und Bedeutung

Keiner der 1.554 Fälle erreicht den 10-%-Screen. Die maximalen eingeschlossenen
absoluten RMS-Beiträge aus der numerischen Lösung liegen unter **7,285 × 10^-10**,
die aus der Anfangsdatenauswertung unter **8,248 × 10^-10**. Die größten
Komponentenradien der eingeschlossenen Adapterlösungen sind kleiner als
**5,001 × 10^-22**. Die großen physikalischen Vergleichsfehler lassen sich
somit nicht durch eine ungenaue Dreieckslösung erklären.

Ein fester Ausschnitt illustriert die Trennung: nu=4096, epsilon=1/16,
jeweils RMS über die 16 Archivwolken und 28 Proben. Bei diesen Wellen ist
der Referenz-RMS eins, sodass die Werte zugleich relative RMS sind.

| k | Adapter | Operator/Gebiet | History-Fortsetzung | Gesamt |
|---:|---|---:|---:|---:|
| 0 | H1 | 0,9183 | 0,3462 | 0,9775 |
| 0 | H3 | 0,9183 | 0,07169 | 0,9288 |
| 8 | H1 | 1,1226 | 2,8636 | 3,0219 |
| 8 | H3 | 1,1226 | 58,3407 | 58,3330 |

Die höhere Taylorordnung hilft hier der langsamsten Mode, verschlechtert
aber die kurze Welle stark. Auf einem langen History-Streifen reicht das
korrekte Treffen von f und g auf der Anfangsfläche offenbar nicht aus.
Zugleich bleibt der Operator-/Gebietsfehler schon bei Orakelhistorie groß.
Die Tabelle ist ein ausgewiesener Ausschnitt; sämtliche Zellen und Fälle
stehen in den Ergebnisdateien. Es gibt keine Auswahl erfolgreicher Wolken.

Die größte ausgewertete obere History-Verstärkung liegt bei etwa
8,59 × 10^5. Dies ist eine konservative Normobergrenze, kein gemessener
typischer Verstärkungsfaktor und kein Instabilitätsbeweis. Die direkte
eingeschlossene Fehlerfortpflanzung ist wesentlich genauer.

**Folgerung:** H1 und H3 sind jetzt vollständig beschriebene und überprüfbare
Adapter dieses endlichen Benchmarks, erfüllen aber das gewünschte Fehlerziel
nicht. Ein produktiver Propagationslauf wird dadurch nicht freigegeben.
Die nächste Adapterentwicklung muss ihre Konsistenz auf dem benötigten
History-Bereich und die verbleibenden Operatorfehler gemeinsam berücksichtigen.
Eine bloße Erhöhung der Taylorordnung oder der CPU-Präzision löst das
gezeigte Problem nicht.

## Vollständige CPU-Kausalitätsprüfung

Der neue Kern entscheidet alle benötigten Relationen der gespeicherten
binary64-Koordinaten mit nach außen gerundeten Intervallen. Unsichere Fälle
werden mit exakten rationalen Zahlen entschieden; exakt nullartige Paare
sind gemäß der strikten Ordnung ausgeschlossen. Eine plattformabhängige
long-double-Nachrechnung ist nicht mehr die letzte Entscheidungsinstanz.

In beiden CPU-Konfigurationen müssen sämtliche Wolke/Wolke- und
Wolke/Probe-Bitfelder, Intervallzahlen, History-/Aktivmasken sowie exakten
Gebiets- und Schalenmitgliedschaften übereinstimmen. Dies umfasst alle
64 ursprünglichen inneren Wolken und acht äußeren Erweiterungen.
Archiv- und RNG-Ausgabehashes bleiben exakt. Das behauptet weiterhin keine
allgemeine bitweise Reproduzierbarkeit regenerierter Koordinaten und keinen
Beweis über ideal reelle Zufallskoordinaten.

Beide CPU-Prüfungen sind bestanden. Ohne AVX-512 weichen regenerierte
Koordinaten höchstens um 8,882 × 10^-16 L0 ab; sämtliche benötigten
Relationen und Mitgliedschaften bleiben exakt gleich. Die maximale
Abweichung der numerischen Propagationswerte beträgt 2,329 × 10^-10
und erfüllt die unveränderte kombinierte absolute/relative Toleranz.
Die vollständige Produktion einschließlich beider CPU-Prüfungen dauerte
767,23 Sekunden; der maximale gemessene Prozessspeicher lag bei 771,55 MiB.

## Dateien und Reproduktion

- [METHODS.md](METHODS.md): Definitionen, Fehleridentität, Störungsnormen,
  exakte CPU-Prädikate, Referenzfehler und Aussagegrenzen.
- [PROTOCOL.json](PROTOCOL.json), [FREEZE.json](FREEZE.json),
  [Amendment 01](amendment_01/AMENDMENT.json): vollständige Festlegung und
  dokumentierte Unsicher-Null-Korrektur vor abgeschlossener Produktion.
- [SUMMARY.json](results/SUMMARY.json): alle 114 aggregierten Zellen und
  getrennte Fehlerbeiträge; keine statistische Bestätigungsfreigabe.
- [BENCHMARK_128.json.gz](results/BENCHMARK_128.json.gz) und
  [BENCHMARK_192.json.gz](results/BENCHMARK_192.json.gz): sämtliche 201
  Wolken-/Operatorzellen mit insgesamt 1.554 Feld-/Adapterfällen.
- [SOURCE_NODES_128.json.gz](results/SOURCE_NODES_128.json.gz) und
  [SOURCE_NODES_192.json.gz](results/SOURCE_NODES_192.json.gz): alle 1.341
  neuen Referenzwerte je Präzisionsstufe.
- [AUDIT.json](results/AUDIT.json), [CPU_DEFAULT.json](results/CPU_DEFAULT.json),
  [CPU_BASELINE.json](results/CPU_BASELINE.json), [COMPUTE.json](results/COMPUTE.json).

Die `real_ball`-/`imag_ball`-Strings tragen die Einschließungen. Die zusätzlichen
Display-Zahlen sind gerundete Anzeigen. Frühere Prüfpakete werden nicht verändert.

Aus der Repository-Wurzel, Python 3.12 und g++:

```bash
python -m pip install -r research/cspp/scalar_propagation_v0_7/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -O -B \
  research/cspp/scalar_propagation_v0_7/verify_publication.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B \
  research/cspp/scalar_propagation_v0_7/verify_publication.py --replay
```

Der vollständige Replay berechnet alle Einschließungen und beide CPU-Prüfungen
in temporären Dateien neu. Präzisionsüberlappung ist ein Implementierungstest;
die Begründung der Fehlergrenzen sind die eingeschlossenen Formeln und
Rekursionen. Allgemeine nichtlokale Cauchy-Wohlgestelltheit, eine vollständige
räumliche Detektorreferenz sowie Dirac-/Flavor-Propagation bleiben offen.
