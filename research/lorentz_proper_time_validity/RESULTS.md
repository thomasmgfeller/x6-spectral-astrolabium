# Eigenzeit v0.2: Gültigkeitsbereich und Informationsbedarf

**Abgeschlossen: eine deterministische Gültigkeitskarte mit 1.176 Kombinationen.**
Die Rechnung bestätigt die endliche Absicherung innerhalb der jeweils
angenommenen Modellklasse und quantifiziert deren Versagen ausserhalb.
Sie qualifiziert keine reale Uhr und keinen allgemeinen Krümmungssensor.

![Überdeckung, falsche Präzisionsmeldungen und verbleibende Unsicherheit](results-overview.png)

## Vorab festgelegter Umfang

- Öffentlicher Quellenstand vor der ersten Zielauswertung: [`67dc770`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/67dc77089af09063e0f0069ad71e08aa622fef44).
- Erster Ziellauf: **18. Oktober 2026, 08:36:59 UTC / 10:36:59 Europe/Zurich**.
- 72 Geometrie-/Beobachtungsfälle, sieben beobachtete Punktzahlen von 256 bis 1.048.576 und die jeweils zulässigen Intervallvarianten ergeben 1.176 Zeilen.
- Bekannte flache Dimensionen d=2,3,4; de Sitter, Dichteänderung, Ausdünnen und Dichtezwillinge in d=4. Vier vorab bestimmte Eigenzeitwerte.
- Endliche Binomialausdrücke direkt ausgewertet, **keine neuen Punktwolken und keine Monte-Carlo-Erfolgsquoten**.
- Getrennte Integral-/CDF-Gegenprüfung sowie vollständiger Replay. Interne Reproduktion, keine externe wissenschaftliche Replikation.
- Beobachteter erster Ziellauf: rund 4,66 Sekunden und 85 MiB Peak-RSS; kein vergleichender Geschwindigkeitsbenchmark. Budget: 600 Sekunden und 2 GiB.

[Vertrag](contract.json) · [Herleitung](DERIVATION.md) · [Alle Daten](results.zip) · [Archivprüfung](ARCHIVE.json)

## Was als ausreichende Präzision zählt

Ein 95%-Intervall [L,U] erhält nur dann eine Präzisionsmeldung, wenn sein
relativer Radius (U−L)/(U+L) höchstens 10% ist. Der zugehörige Schätzwert ist
die harmonische Mitte 2LU/(L+U). Die ursprüngliche rohe Zählschätzung wird
getrennt mit Bias, RMSE und Erfolgswahrscheinlichkeit berichtet.
Eine Gitterzelle erfüllt die vorab festgelegten Kriterien nur bei gültigen
Modellannahmen, mindestens 95% Überdeckung und mindestens 90% Wahrscheinlichkeit
einer solchen Präzisionsmeldung. Die numerische Vergleichstoleranz beträgt 5e−10.

| Entscheidung | Kombinationen | Bedeutung |
|---|---:|---|
| MEETS_DECLARED_GRID_CRITERIA | 192 | Annahmen erfüllt; Überdeckung und Präzisionsverfügbarkeit genügen. |
| INSUFFICIENT_GRID_PRECISION | 522 | Annahmen erfüllt, gewünschte Präzision noch nicht verfügbar. |
| OUTSIDE_ASSUMED_CLASS | 462 | Geometrie oder Dichte liegt ausserhalb der Intervallannahmen; keine Freigabe. |

Alle **714** innerhalb ihrer Modellklasse liegenden Kombinationen haben numerisch mindestens **95.006076%** Überdeckung. Die grösste unbedingte Wahrscheinlichkeit einer falschen Präzisionsmeldung beträgt dort **1.818284%**. Diese Extremwerte beschreiben das festgelegte Gitter; die zugrunde liegende 95%-Aussage folgt aus der Herleitung unter ihren Voraussetzungen. Die Anzahl der Gitterzeilen ist keine Häufigkeit physikalischer Fälle.

## Wie viele beobachtete Punkte braucht die flache 4D-Referenz?

Kleinster erfolgreicher Wert **auf dem geprüften Gitter**, keine mathematisch
minimale Punktzahl und kein garantiertes sequenzielles Stoppbudget:

| Wahres τ/T | Uniformität bekannt, r=1 | Extern begrenzt: r ∈ [0,8; 1,25] | r ∈ [0,5; 2] |
|---:|---:|---:|---:|
| 0,1 | 1.048.576 | Keiner bis 1.048.576 | Keiner bis 1.048.576 |
| 0,2 | 65.536 | 262.144 | Keiner bis 1.048.576 |
| 0,4 | 4.096 | 16.384 | Keiner bis 1.048.576 |
| 0,7 | 256 | 1.024 | Keiner bis 1.048.576 |

Die Tabelle verwendet tatsächlich uniforme flache Daten und zeigt den Preis
einer vorsichtigeren Annahme über ihre Dichte. r ist die mittlere beobachtete
Intensität innen geteilt durch diejenige ausserhalb des inneren Intervalls.
Die Grenzen müssen unabhängig begründet sein. Bei τ/T=0,2 steigt der erste
passende Gitterwert von 65.536 auf 262.144. Bei der breiteren Dichteklasse
bleibt hier selbst im Grenzfall unendlich vieler Punkte ein relativer
Intervallradius von rund **17,13%**. Mehr Daten entfernen diese Unsicherheit nicht.

## Wenn viele Daten eine falsche Sicherheit erzeugen

Alle folgenden Beispiele haben d=4 und wahres τ/T=0,2. Die Auswahl erläutert
die Mechanismen; jede andere vorab festgelegte Zelle bleibt vollständig im Archiv.

| Modell / Intervall | Beobachtete m | Überdeckung | Präzision gemeldet | Präzision gemeldet und tatsächlich >10% Fehler |
|---|---:|---:|---:|---:|
| Uniform flach / nominal | 65,536 | 95.5167% | 100.0000% | 0.0126% |
| de Sitter h=0,5 / nominal | 1,048,576 | 59.8717% | 100.0000% | 0.0000% |
| Dichte β=4 / nominal | 65,536 | 45.6456% | 100.0000% | 5.7289% |
| Dichte β=12 / nominal | 65,536 | 0.1426% | 99.9999% | 88.5305% |
| Innen 50%, aussen 100% erfasst / nominal | 65,536 | 0.0022% | 99.9960% | 98.8089% |
| Gleiche selektive Erfassung / r ∈ [0,5; 2] | 65,536 | 97.7356% | 0.0000% | 0.0000% |

**Überdeckung und Genauigkeit sind unterschiedliche Fragen.** Im gezeigten
de-Sitter-Fall beträgt der relative Bias der rohen Schätzung nur rund 1,03%,
aber die nominellen 95%-Intervalle überdecken die Wahrheit nur noch mit
rund 59,87%. Trotzdem tritt dort praktisch kein Fehler über 10% auf.
Ein Scheitern des 95%-Intervalls ist daher nicht automatisch ein grosser Punktfehler.

Bei selektiv fehlenden Ereignissen ist das Problem stärker: Die ungeschützte
Präzisionsmeldung ist im gezeigten Fall mit rund 98,81% Wahrscheinlichkeit
falsch. Diese Zahl ist **keine Detektionsrate** und hat nichts mit der
früheren 506/512-Dichtewarnung zu tun. Das breite konservative Intervall
erhält in derselben Zelle rund 97,74% Überdeckung, verweigert aber die
10%-Präzision. Sein Nutzen ist hier eine begründete Enthaltung.

Uniformes unabhängiges Ausdünnen verändert die Zählwahrscheinlichkeit nicht,
wenn auf die beobachtete Punktzahl konditioniert wird. Es erhöht aber den
Akquisitionsaufwand: Bei 50% Erfassung braucht man im Mittel doppelt so viele
ursprüngliche Punkte. Selektive Erfassung verändert dagegen die Verteilung.

## Was damit mathematisch hinzugekommen ist

Für eine bekannte flache Geometrie und extern begrenzte relative Intensität
r_low≤r≤r_high wird das Binomialintervall monoton zu einem konservativen
Eigenzeitintervall erweitert. Der Beweis steht in der Herleitung und gilt
für jedes feste m unter iid-Beobachtungen. Er beseitigt keinen unbekannten
Geometrie-, Dimensions- oder Massstabsfehler. Eine statistische Datenprüfung
allein kann die externen Dichtegrenzen nicht bestätigen.

Die Dichtezwillinge behalten identische Zählwahrscheinlichkeiten und
Ordnungsgesetze bei unterschiedlicher wahrer Eigenzeit. Im gekrümmten Fall
wird die tatsächliche Eigenzeit aus dem bekannten Modell und einem
unabhängigen äusseren Massstab verwendet. Es gibt keine zirkuläre Kalibrierung
durch die flache Schätzformel.

## Verifikation und numerische Grenzen

- Alle 1.176 Überdeckungswerte wurden getrennt über ganzzahlige Binomial-Akzeptanzbereiche berechnet, ohne die inverse Betafunktion des Produzenten. Grösste Abweichung: **4,26e−12**.
- Adaptive Volumenintegration gegen feste Gauss-Legendre-Integration: grösste Wahrscheinlichkeitsabweichung **5,56e−17**.
- Unabhängige rationale Binomialkontrolle und numerische Tail-Inversion an anderen, nicht zum Zielgitter gehörenden Parametern. Drei absichtlich veränderte Resultate werden abgewiesen.
- Vollständiger Replay aller numerischen Felder und Planungsentscheidungen: **PASS_FULL_PROPER_TIME_VALIDITY_REPLAY**.
- Ausgelassene Binomialrandmasse: höchstens rund 2e−13 pro Zeile. Sie wird nicht renormalisiert; Fehlerbeiträge zu Bias/MSE stehen pro Zeile im Archiv.
- Float64, numerische Quadratur und Bibliotheksfunktionen: keine formal zertifizierte Rundungsfehlerrechnung. Auf vier Dezimalstellen gerundete 0% oder 100% sind keine Behauptung exakter Null/Eins.
- Die sechs eingefrorenen Forschungsdateien und die vier Originalausgaben bleiben unverändert. ZIP-Verpackung, Grafik, Bericht und Entpackhülle entstanden nach der Auswertung; keine Kriterienänderung oder Nachziehung.

[Vollständige Prüfwerte und Akzeptanzgrenzen](VERIFICATION.json). Der Runner
prüft CPU-/Adressraumbudget sowie die Laufzeit; der CI-Job besitzt zusätzlich
eine feste Zeitgrenze. Die GitHub-Prüfung wiederholt den vollständigen Lauf.

## Nächste fachliche Abnahme

1. Diese Referenz durch einen externen Rechenweg bzw. unabhängige Personen reproduzieren.
2. Dichte-/Erfassungsschranken für eine konkrete Datenquelle unabhängig begründen. Ohne diese Information bleibt die konservative Klasse nur eine Annahme.
3. Separat den Informationsbedarf einer eingeschränkten de-Sitter-Krümmungsschätzung aus der vollständigen Kettenkovarianz planen. Danach ein neuer Vertrag mit Zielgenauigkeit, Resttermkontrolle und frischen Daten.

Die bisherige negative Krümmungsstudie und das unerreichte RSS-Präzisionsziel
bleiben unverändert. Keine neue RSS-Inversion, keine frei unbekannte Raumzeit
und keine reale Planck-Uhr sind mit diesem Meilenstein qualifiziert.

## English summary

The publicly frozen deterministic study evaluates 1,176 model/budget/interval
combinations. All 714 in-class combinations retain at least 95% numerical
coverage; 192 also meet the declared precision-availability gate. Another
522 remain insufficiently precise, while 462 are outside the assumed class.
Selective missingness can produce narrow, systematically misleading intervals.
Externally bounded flat-space sampling-intensity ratios permit conservative
intervals, with an irreducible uncertainty floor. Complete internal replay
and independent geometry/CDF checks pass; there are no new Monte Carlo
clouds, physical measurements, external replication, general curvature
qualification or resolution of density twins.
