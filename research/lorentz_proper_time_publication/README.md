# Eigenzeit: Ergebnisse, Gültigkeit und reproduzierbarer Einstieg

Stand: 17. Oktober 2026. **Die statistische Eigenzeitschätzung ist innerhalb
des deklarierten flachen Stichprobenmodells qualifiziert.** Jetzt sind auch
endliche Fehlerintervalle, datenabhängiges Nachbeproben und eine begrenzte
Ordnungsdiagnostik implementiert und intern geprüft. Eine Anwendung auf
unbekannte Geometrien oder reale Messdaten ist damit nicht qualifiziert.

## Drei aufeinander aufbauende Ergebnisse

| Paket | Tatsächlich geprüft | Befund und Grenze |
|---|---|---|
| [Ursprüngliche 1+1-Referenz](../lorentz_proper_time/RESULTS.md) | 6.912 Ordnungen, 27.648 Vorhersagen; vorab festgelegter Hauptvergleich | `QUALIFIED_IN_DECLARED_MODEL`; RMSE 0,031614 gegenüber 0,177785 für die Dichte-/Höhenregression. Größte exakt abgeglichene Zusatzkontrolle: nur 63 statt 128 Paare, daher keine Leistungsbewertung. |
| [Gültigkeitsbereich und Fehlergrenzen](../lorentz_proper_time_domain/results/RESULTS.md) | 49.152 unabhängige Punktwolken, 24 Zellen in d=2,3,4; zwölf volle Relationsgegenprüfungen | `CONDITIONAL_FLAT_MODEL_CHECK_PASSED`; exaktes Binomialmodell und konservative 95%-Intervalle. Gute Deckung bedeutet bei kleinen Intervallen keine gute Auflösung. |
| [Sequenzielle Referenz](../lorentz_proper_time_sequential/results/RESULTS.md) | Drei positive Zählmodelle mit je 1.024 Läufen, 64 Nullströme, vier Kettendiagnosen mit je 128 Nullbeispielen; ein tatsächlicher Geometrielauf | `DECLARED_SEQUENTIAL_REFERENCE_CHECK_PASSED`; zeituniforme Absicherung und einmalige bedingte Ordnungsdiagnose. Die Hauptsimulation verwendet Zählblöcke, keine vollständigen Punktwolken. |

Die RMSE des ersten Versuchs mittelt über zufällig gewählte Endpunkte. Die
Folgestudie untersucht feste normierte Abstände. Diese RMSE-Werte sind keine
direkten Leistungsranglisten. Keine dieser Prüfungen ist externe Replikation,
ein Hardwarebenchmark oder ein Nachweis von Quantenvorteil.

## Wann die Aussage gilt

Bekannt sein müssen die Raumzeitdimension d, ein flacher Minkowski-Diamant
D=I(A,B), sein Zeitmaßstab S und vollständig eingeschlossene, vor der
Bestätigungsstichprobe bestimmte Endpunkte A≪p≪q≪B. Gezählt werden frische,
unabhängige und bezüglich des Volumens uniforme Hintergrundpunkte. Es gibt
keine Beobachtungsmaske und keine Relationsfehler. Die beiden Markierungen
zählen nicht zu den m Hintergrundpunkten.

Dann gilt K ~ Binomial(m, (τ/S)^d) und die rohe Volumenschätzung ist
τ̂=S(K/m)^(1/d). τ bezeichnet die maximale Eigenzeit zwischen den Endpunkten,
nicht die Zeit entlang einer beliebig beschleunigten Weltlinie. Ohne bekannten
Maßstab S oder eine geeignete Dichtekalibrierung liefert die Ordnung keine
absolute Zeit. Herleitung, Einschlussbeweis, Nullzählungen und endliche
Poset-Kontrollen stehen im [mathematischen Vertrag](../lorentz_proper_time_domain/README.md).

**Versagen und verweigerte Freigabe gehören zum Ergebnis:** falsche Dimension,
abgeschnittene Intervalle, unbekannte Dichte, abhängige Beobachtungen und
nachträglich ausgewählte Endpunkte können die Statistik ungültig machen.
Ein endlicher azyklischer transitiver Graph zertifiziert keine
Minguzzi-Kausalitätsbedingung im Kontinuum. Bei zu kleinem Budget lautet der
sequenzielle Ausgang `BUDGET_EXHAUSTED`, nicht „präzise“.

## Unter 10% relativer Fehler: drei verschiedene Fragen

Für d=4 und τ/T=0,1 trifft ein globaler Punkt das innere Intervall nur mit
Wahrscheinlichkeit 0,0001. Bei m=256 bleibt K mit etwa 97,47% Wahrscheinlichkeit
null. Ein Filter erzeugt keine zusätzlichen unabhängigen Beobachtungen.

Die folgenden **Feststichprobenbeispiele** betreffen
P(|τ̂/τ−1|<0,1), nicht die Breite eines beobachteten Konfidenzintervalls.
Sie setzen den Planungswert τ/T=0,1 voraus und sind keine geschätzten
Minimalbudgets. Die lokale Variante verlangt einen bereits bekannten,
vollständig einschließenden Diamanten mit S=0,2T und frische uniforme Punkte
in diesem Diamanten. Dessen Volumen ist 1/625 des äußeren Volumens.

| Beprobung | m | E[K] | Erfolgswahrscheinlichkeit aus Binomialformel |
|---|---:|---:|---:|
| Global, S=T | 300.000 | 30 | 96,83996% |
| Lokal, S=0,2T | 480 | 30 | 97,33867% |
| Global, konservatives Budget | 550.000 | 55 | 99,51818% |
| Lokal, konservatives Budget | 880 | 55 | 99,62690% |

Für E[K]=30 ist der akzeptierte ganzzahlige Bereich K=20,…,43.
Die Werte sind numerische Auswertungen exakter Binomialausdrücke, keine
Simulation und keine formal gerundete Intervallarithmetik. Wegen der
ganzzahligen Akzeptanzgrenzen muss die exakte Erfolgswahrscheinlichkeit bei
kleinen Änderungen von m nicht monoton sein.

Eine konservative analytische Planung folgt aus der Chernoff-Schranke.
Mit λ=E[K], r₋=0,9⁴, r₊=1,1⁴ und h(r)=r ln(r)−r+1 gilt für die
Fehlerwahrscheinlichkeit höchstens exp(−λh(r₋))+exp(−λh(r₊)). Für λ≥55 ist
dies höchstens 0,030224, also weniger als 5%. Die Schranke gilt für das
deklarierte Binomialmodell sowie für eine Poisson-Zählung mit bekannter
Intensität und entsprechendem Volumenschätzer. Sie beseitigt keinen
systematischen Modellfehler. [Rechnung](planning.py) · [Zahlen](planning.json).

**Sequenzielles Stoppen** beantwortet eine andere Frage. Hier darf nach jedem
Block geprüft und bei hinreichend enger Konfidenzfolge gestoppt werden. Für
das Zeitfehlerbudget 2,5% verwenden wir die explizite gestitchte
Empirical-Bernstein-Schranke nach Howard et al. Bei Intervall [L,U], L>0,
verwenden wir die harmonische Mitte 2LU/(L+U). Deren maximaler relativer Fehler
über dieses Intervall beträgt (U−L)/(U+L). Gestoppt wird bei einem Wert <0,1.

Unter den Annahmen ist P(Präzision gemeldet UND relativer Fehler >0,1) ≤2,5%.
Das ist bei endlichem Budget keine automatische bedingte Garantie nur unter
den erfolgreichen Stopps. Es gibt kein garantiert ausreichendes endliches
Budget. In den gespeicherten Läufen lag der Median bei 2.592 lokalen bzw.
1.673.216 globalen Beobachtungen; alle je 1.024 positiven 4D-Läufe erreichten
das Ziel. Diese Mediane sind Beobachtungen, keine Budgetgarantien. Andere
Batchgrößen und das strengere, zeituniforme Intervall erklären den Abstand
zu den Feststichprobenbeispielen.

## Was die längste Kette zusätzlich leistet

Die längste Kette wird bei der beobachteten inneren Punktzahl K gegen frische
flache Referenzordnungen verglichen. Diese Diagnose nutzt Forminformation,
die K allein nicht enthält. Im uniformen flachen Diamanten ist die Verteilung
der inneren Ordnung **bedingt auf K unabhängig von τ**: Translation,
Lorentztransformation und Skalierung führen auf denselben Einheitsdiamanten.
Deshalb bringt diese innere Ordnung dort keine zusätzliche Zeitmaßinformation
über K hinaus. Bei K=0 kann auch keine Kette die fehlenden Punkte ersetzen.
Das behauptet weder Optimalität der rohen Wurzelschätzung noch dass sämtliche
Relationen zu äußeren Punkten informationslos wären.

Die einmalige Diagnose hat unter dem gemeinsamen Nullmodell höchstens 2,5%
Fehlalarm; zusammen mit dem Zeitfehlerbudget sind beide Fehlerereignisse per
Union Bound durch 5% begrenzt. Ein nicht auffälliger Test beweist die
Modellannahmen nicht. Eine Warnung setzt die wissenschaftliche Zeitfreigabe
auf `WITHHELD_MODEL_WARNING`.

Die gespeicherten Kontrollen meldeten 5/512 Warnungen im flachen Nullmodell
und 506/512 bei absichtlich räumlich komprimierten Stichproben in weiterhin
flacher Metrik. Letzteres zeigt ausdrücklich eine Dichtestörung, **keine
Krümmung**. Eine unbekannte Beprobungsdichte und eine konforme Metrikänderung
können dasselbe Ordnungsgesetz erzeugen. Die
[Herleitung und Testregeln](../lorentz_proper_time_sequential/README.md)
verhindern diese Verwechslung.

## Reproduktion und Herkunft

Voraussetzungen: Git, Python 3.12, NumPy 2.3.5 und SciPy 1.17.0. Abhängigkeiten
benötigen einmalig Netzwerk oder vorbereitete Wheels; die Rechnungen danach
keinen externen Dienst. Aus dem Repository-Wurzelordner:

```sh
python3 -m pip install -r research/lorentz_proper_time_sequential/requirements.txt
python3 -B research/lorentz_proper_time_publication/replay.py
python3 research/lorentz_proper_time_publication/planning.py
```

Der Replay prüft beide Archive, wiederholt die beiden vollständigen neuen
Versuche in temporären Verzeichnissen und vergleicht Rohzählungen sowie alle
wissenschaftlichen Zusammenfassungen. Nur Laufzeit und Laufzeitumgebung
werden aus dem deterministischen Vergleich ausgeschlossen. Er prüft auch
den dokumentierten technischen Reparaturverlauf. Historische Dateien werden
nicht überschrieben. Der vorhandene 1+1-Lauf behält seinen
[eigenen Reproduktionsweg](../lorentz_proper_time/README.md).

Die beiden neuen Versuche wurden lokal vor ihren Zielziehungen fixiert und
werden **erst nach Ausführung veröffentlicht**. Das ist keine öffentliche
Präregistrierung. Beim sequenziellen Erstlauf scheiterte das Schreiben eines
NumPy-Integerwerts in JSON; die gezielte Typkonvertierung und identische
Wiederholung mit denselben Seeds sind im
[Ausführungsverlauf](../lorentz_proper_time_sequential/EXECUTION_HISTORY.md)
dokumentiert. Originalcode, erste Quellenfixierung und erste Rohzählungen
bleiben erhalten. Weder dieser Reparaturlauf noch CI ist externe Replikation.

Der wissenschaftlich abgeschlossene Umfang lautet: **bedingte
Eigenzeit-Referenz mit expliziter Unsicherheit und Abbruchregeln im bekannten
flachen Modell**. Eine Erweiterung braucht eine bestimmte Geometrie- und
Beprobungsklasse, unabhängige Zeit-/Dichtekalibrierung und eigene
Fehlerkontrolle. Weitere Stichproben im selben Modell ersetzen das nicht.

## Primärquellen

- Howard et al., [Time-uniform, nonparametric, nonasymptotic confidence sequences](https://doi.org/10.1214/20-AOS1991), Annals of Statistics 49 (2021), 1055–1080; [Volltext](https://arxiv.org/html/1810.08240v9), Theoreme 1 und 4, Gleichung (8).
- Brightwell und Gregory, [The structure of random discrete spacetime](https://doi.org/10.1103/PhysRevLett.66.260), PRL 66 (1991), 260–263. Historischer Kettenansatz; die endliche Rangdiagnose hier ist kein daraus übernommener Krümmungssatz.
- Minguzzi, [Lorentzian causality theory](https://doi.org/10.1007/s41114-019-0019-x), Living Reviews in Relativity 22 (2019). Kontinuumsbedingungen sind von endlicher Poset-Validierung zu unterscheiden.

## Weiterführend: Eigenzeit v0.2

Die [Gültigkeitskarte und Budgettabelle](../lorentz_proper_time_validity/RESULTS.md)
prüfen bekannte Krümmung, Dichteänderungen und fehlende Beobachtungen.
Vorab begrenzte Dichteunsicherheit ermöglicht konservativere Intervalle
im flachen Modell. Diese Erweiterung ist separat dokumentiert; der
Browser-Demonstrator verwendet weiterhin seine ursprünglichen festen
Stichproben und uniformen flachen Modellannahmen.
