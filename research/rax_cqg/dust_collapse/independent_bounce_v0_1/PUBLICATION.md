# Vorabprüfung einer Bounce-Vorhersage v0.1

**5. November 2026 · Zehn neue Referenzfälle bestanden; ein physikalischer CST-Bounce bleibt offen.**

Aus frühen Zustandsmomenten wurden Umkehrzeit und Minimalwert des mittleren Volumens bestimmt und vor der späten Zeitentwicklung gespeichert. Eine getrennte Crank–Nicolson-Rechnung mit acht neuen Gaußzuständen und zwei kohärenten Überlagerungen bestätigt diese Vorhersagen auf dem feinsten Gitter. Alle zehn Fälle erfüllen die vorher gesetzten Grenzen von 1 % Zeitfehler und 3 % Volumenfehler; beide Fehler sinken bei jeder der zwei Verfeinerungen. Die Maximalfehler betragen rund 0,615 % und 1,324 %.

- [Bericht (PDF, sechs Seiten)](../reports/CST_Staubball_Unabhaengige_Bounce_Vorhersage_v0_1.pdf)
- [Unverändertes Prüfpaket (ZIP)](../packages/CST_Staubball_Unabhaengige_Bounce_Vorhersage_v0_1_Pruefpaket.zip)
- [Festgelegter Plan](plan.json), [frühe Vorhersagen](forecast.json), [später Löser](propagate.py), [Prüfer](verify.py) und [Ergebnisse](results/verification.json)
- [Originalanleitung](README.md), [Herleitung](report.tex), [Abbildung](figures/prediction_test.png) und [Quellenbindung](provenance.json)

## Was unabhängig geprüft wurde

Die zehn synthetischen Anfangszustände wurden im vorherigen Klassiktest nicht verwendet. Der späte Löser erhält die Anfangszustände und Gitterdaten, aber weder die vorhergesagten Minima noch die Momentformel. 30 Entwicklungsläufe liefern 7230 Ablesewerte; 50 zusätzliche Sinuskontrollen prüfen den Kontinuumskern. Dies ist eine getrennte rechnerische Gegenprüfung innerhalb desselben angenommenen reduzierten Modells, keine unabhängige physikalische Messung, externe Präregistrierung oder Replikation durch eine andere Forschungsgruppe. Raum- und Zeitschritt wurden gemeinsam verfeinert; es liegen keine neuen Intervallzertifikate vor.

Das Referenzmodell bleibt die homogene flache periodische Staubzelle mit `q = sqrt(V) > 0`, direkter q-Quantisierung und gewähltem Dirichlet-Rand. Es beschreibt keinen vollständigen Staubball mit Außenraum und ist noch nicht aus der vierdimensionalen Kausalset-Summe abgeleitet.

## Aussagegrenzen der Umkehr

Dirichlet- und Neumann-Ränder geben bei zwei Kontrollen innerhalb der numerischen Genauigkeit dieselben mittleren Volumenminima, obwohl die Randdichten verschieden sind. Sechs späte Neumann-Quadraturen bestätigen die Momentkurve. Eine transparente volle q-Gerade zeigt ebenfalls ein Minimum von `⟨q²⟩`, obwohl der Schwerpunkt ins Negative läuft. Negative q liegen außerhalb der physikalischen Halbgeradenreferenz; diese Kontrolle zeigt die begrenzte Aussagekraft des Mittelwerts.

Bei allen acht Gauß-Bildzuständen divergiert `⟨V⁻²⟩` am vorhergesagten Minimum und bereits anfangs. Das positive Minimalvolumen beweist daher keine Singularitätsauflösung; es wird kein Übergang von einem regulären zu einem singulären Zustand behauptet. Diese Observable wird nicht mit einem Krümmungsoperator gleichgesetzt. Die beiden kohärenten Fälle werden durch den Einzel-Gauß-Beweis nicht zusätzlich klassifiziert.

Der Bounce-Begriff dieses Tests ist ein striktes Minimum des **mittleren** Volumens. Er ersetzt weder eine mehrzeitige Historienwahrscheinlichkeit noch die alte 80-%-Dominanzforderung. Der volle CST-Test bleibt `HOLD_NOT_ELIGIBLE`, Singularitätsauflösung `NOT_ESTABLISHED` und der alte Kandidat `CLOSED_REJECTED_FOR_DOMINANT_BOUNCE`.

## Veröffentlichung und Nachrechnung

Das ursprüngliche ZIP, seine 22 Mitglieder und der Bericht sind unverändert übernommen. Ergänzt wurden ausschließlich diese Veröffentlichungsübersicht, `publication_check.py` und `publication-requirements.txt`; CI rechnet in einer temporären Kopie nach und verändert die archivierten Ergebnisse nicht.

```sh
python3 -m pip install -r research/rax_cqg/dust_collapse/independent_bounce_v0_1/publication-requirements.txt
python3 research/rax_cqg/dust_collapse/independent_bounce_v0_1/publication_check.py --replay
```

Die Veröffentlichungskontrolle prüft alle Originalbytes, Plan- und Prognoseprüfsummen, die Bindung an die vorher publizierten Klassik- und Gewichtungsquellen sowie die wissenschaftlichen Entscheidungen. Die Ergebnisstruktur muss exakt übereinstimmen; numerische Werte werden mit `atol=2e-10`, `rtol=1e-10` verglichen. Laufzeit und Runtime-Metadaten dürfen abweichen. Zusätzlich gelten unverändert die ursprünglichen Akzeptanzkriterien aus `plan.json`. Beide CSV-Dateien werden ebenfalls mit den neu erzeugten Zahlen verglichen.

Keine neuen Kausalsets oder physikalischen Messungen. Der bekannte reduzierte Minisuperspace-Mechanismus wird nicht als neue allgemeine Bounce-Theorie ausgegeben. Projektbeiträge gemäß [Lizenzumfang](../../../../LICENSE_SCOPE.md).

