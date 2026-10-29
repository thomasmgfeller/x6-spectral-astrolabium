# CSPP v0.6: Dichte, Nichtlokalität und Gebietsgröße gemeinsam planen

28. Oktober 2026. **Entscheidung: Unter dem bisherigen Budget keinen neuen
Sprinkling-Lauf für das 10-%-Fehlerziel starten.** Alle 320 deklarierten
Kombinationen aus 20 Nichtlokalitätslängen und 16 Gebietsgrößen scheitern
bereits an notwendigen Bedingungen. Die Dichte wird für jedes Paar analytisch
über ihr gesamtes zulässiges Budgetintervall geprüft.

Als Budget wurden die bisherigen **20.000 erwarteten Punkte pro Wolke**
übernommen; es liegt keine neue numerische Budgetvorgabe vor. Die bisherigen
Ressourcengrenzen sind 4 GiB und 21.600 Sekunden. Quelle, Detektor, Feldlänge
und physikalische Wellenzahlen bleiben unverändert. Kein Zufallslauf wurde
gestartet, kein Bestätigungsseed verwendet. G1 bleibt **HOLD**, G2/G3 **NOT_RUN**.

## Was gegenüber D20 verbessert wurde

Eine neue vorzeichenbehaftete Randeinschließung berücksichtigt die Auslöschung
der Schichtgewichte. Sie ersetzt für diese Planung die bisherige grobe
Betragshülle. Dadurch können kleinere Gebiete geprüft werden, ohne das
Gauß-Feld oder seine physikalischen Wellenlängen mitzuskalieren.

Die ursprünglichen **85.786.423,394 erwarteten Punkte** folgen unverändert aus
`rho >= ell_k^-4` bei `ell_k=1/8` und `Vol(D20)=pi*20^4/24`.
Eine bessere Varianzschranke ändert diese Zulässigkeitsgrenze nicht.
Die folgenden kleineren Zulässigkeitszahlen entstehen durch die gemeinsame
Änderung von `ell_k` und `H`.

Unter den 115 Paaren, die die getrennten systematischen Allokationen von
5 % Nichtlokalitätsbias und 1 % Randfehler erfüllen, liefert dasselbe Rasterpaar
die kleinste ausgewertete notwendige und hinreichende Punktzahl:

\[
\ell_k=37/256=0{,}14453125,\qquad H=11/4=2{,}75.
\]

Hier sind `rho_admiss = 2291,674673`, relativer Nichtlokalitätsbias
4,946659 %, relativer Randbeitrag 0,876929 % und tatsächlicher endlicher
Bias 5,823588 %. Die notwendige Dichte für die 7-%-Streuungsallokation ist
mindestens `rho = 2,3718587e7`.

| Erwartete Punkte | Nur Operatorgebiet D_H | Gebiet Omega_H mit Quelle und Detektor |
|---|---:|---:|
| Zulässigkeit des Operators | 17.156,25 | 622.739,89 |
| Notwendige Untergrenze für die Fehlerallokationen | 1,7756535 × 10^8 | 6,4452911 × 10^9 |
| Hinreichende, sehr konservative Obergrenze für den einzelnen Gauß-Zeugen | 2,6578251 × 10^20 | 9,6474095 × 10^21 |

**Die notwendige Untergrenze ist kein erreichbares Budget.** Die hinreichende
Obergrenze ist keine Schätzung des Minimums und qualifiziert nur diesen
einzelnen Zeugen, nicht die vollständige Feldfamilie oder die E4-Pipeline.
Zwischen den Schranken bleiben mehr als zwölf Größenordnungen offen.

`D_H = I((-H,0),(0,0))` endet am Operatorprüfpunkt. Es enthält keinen Detektor
bei `t=1`. Deshalb wird zusätzlich
`Omega_H = I((-H,0),(4,0))`, Volumen `pi*(H+4)^4/24`, ausgewiesen.
Die Zukunftsspitze 4 bleibt fest. Für alle geprüften `H >= 2` enthält dieses
Gebiet Quelle, Detektor und den gesamten kausalen Quellensupport bis `t=1`
mit mindestens 1/2 Nullkoordinatenabstand zum Rand. Seine Vergangenheit am
Prüfpunkt ist genau D_H. Beide Spalten verwenden dieselbe Dichte.

## Warum auch eine günstigere Fehleraufteilung keinen Lauf freigibt

Die Prüfung beschränkt sich nicht darauf, die getrennten 5/1/7-%-Allokationen
zu verlangen. Für jedes Paar wird auch direkt der gesamte relative RMS-Fehler
gegen 10 % geprüft:

| Ausschlussgrund beim Budget 20.000 in D_H | Paare |
|---|---:|
| Keine zulässige Dichte innerhalb des Budgets | 197 |
| Untergrenze des gesamten Gauß-RMS über 10 % | 122 |
| Weitere unveränderte Kalibriermode hat Bias über 10 % | 1 |
| Nicht entschieden | 0 |

Der letzte Fall ist wichtig: Bei `ell_k=1,5`, `H=2` ergibt die Auslöschung
von Nichtlokalitäts- und Randbeitrag beim unmodulierten Gauß-Feld nur 3,51887 %
Bias. Die unveränderte zeitliche Mode `omega=1/4, k=0` hat aber **22,41334 %**
Bias, unabhängig von der Dichte. Sie schließt diesen scheinbaren Ausweg aus.
Für dieses Paar wurden alle vier bisherigen Kalibriermoden eingeschlossen.

Selbst ohne getrennte Teilallokationen liegen die kleinsten notwendigen
10-%-Gesamtbudgets im Raster, nach Ausschluss dieses Gegenbeispiels, bei
26,626 Millionen Punkten in D_H (`ell_k=3/16, H=11/4`) beziehungsweise
859,248 Millionen in Omega_H (`ell_k=3/16, H=3`). Auch dies sind lediglich
notwendige Schranken, keine nachgewiesenen durchführbaren Kombinationen.

## Konsequenz für den nächsten Lauf

Für die untersuchte Operator-, Feld- und Gebietsfamilie gibt es bei 20.000
erwarteten Punkten keinen begründeten Kandidaten für einen neuen Genauigkeitslauf.
Weitere Wolken bei diesem Budget würden den nachgewiesenen Ausschluss nicht
beseitigen. Die Rasterrechnung ist **kein globaler Unmöglichkeitssatz** über
alle kontinuierlichen Werte von `ell_k,H`, andere Gebiete oder Operatoren.

Der nächste sinnvolle Rechenschritt ist eine deterministische Verfeinerung
der Varianzrechnung: die räumlichen gemeinsamen Intervallbeiträge aus v0.4
enger integrieren und die erste Chaos-Norm umfassender einschließen. Vor einem
größeren Sprinkling müssen ein verbleibender Parameterbereich, die übrigen
festen Testfelder und ein ausführbarer Zählalgorithmus zusammen qualifiziert
werden. Das Paar `37/256, 11/4` ist ein Vergleichspunkt dafür, kein freigegebener Lauf.

Der vorhandene Zählkern hält mindestens `(17/4)*N^2` Bytes gleichzeitig.
Schon bei der notwendigen Punktzahl des Vergleichspaars beträgt die
Speicher-Untergrenze im Erwartungswert etwa 1,25 × 10^8 GiB für D_H und
1,64 × 10^11 GiB für Omega_H. Das sind Untergrenzen, keine Spitzenlastprognosen.
Eine Laufzeit für diese Größen wurde nicht extrapoliert.

Ein tatsächlicher Deckel von 20.000 Punkten ist zudem nicht dasselbe wie
20.000 erwartete Punkte. Für hypothetische 16 Wolken und eine eigene
1-%-Ressourcenüberschreitungsallokation zertifiziert die Chernoff-/Unionsschranke
höchstens den ganzzahligen Mittelwert **19.462**. Eine Überschreitung würde als
`RESOURCE_HOLD` mit erhaltener Versuchsidentität vermerkt; kein Neuziehen.
Diese Ressourcenrechnung ist keine wissenschaftliche Konfidenzaussage.

## Nachweise und Reproduktion

- [Herleitung und Grenzen](METHODS.md), [festes Protokoll](PROTOCOL.json),
  [Entscheidung](results/DECISION.json), [Ressourcen](results/RESOURCES.json).
- Alle 320 Datensätze: [128 Bit](results/SCAN.json.gz) und
  [192 Bit](results/SCAN_192bit.json.gz). Die Dezimal-Balls sind die
  Einschließungen; `display_midpoint` und `display_radius` dienen nur der Anzeige.
- [Audit](results/AUDIT.json): 31 exakte Momentidentitäten, 51 unabhängige
  Gamma-Rekurrenzvergleiche, drei eingeschlossene doppelte Randintegrale,
  vier zusätzliche Modenregressionen, Geometrie-, Vorzeichen- und Negativkontrollen.
- Der [Freeze](FREEZE.json) erfolgte nach explorativen Vorrechnungen und vor
  der gespeicherten Produktion. Dies ist deterministische Entwicklungsplanung,
  keine statistische Bestätigung. Frühere Prüfpakete bleiben unverändert.

Aus dem Repository-Wurzelverzeichnis, Python 3.12:

```bash
python -m pip install -r research/cspp/joint_budget_v0_6/requirements.txt
python -O -B research/cspp/joint_budget_v0_6/verify_publication.py
python -B research/cspp/joint_budget_v0_6/verify_publication.py --replay
```

Der Replay schreibt in ein temporäres Verzeichnis. Die mathematischen
Ungleichungen begründen die Einschließungen; die 128/192-Bit-Übereinstimmung
prüft ihre Implementierung. Die gespeicherte Produktion dauerte etwa 8,24 s.
Die massive Punktreferenz aus v0.5 bleibt erhalten; ihre noch zu breiten
räumlichen Detektoreinschließungen sowie Dirac-/Flavor- und globale
Lösungsfehler werden durch diese Planung nicht geschlossen.
