# Unabhängige Bounce-Vorhersage: Referenzprüfung v0.1

**Ergebnis:** Alle zehn neuen Anfangszustände bestehen die vorher festgelegte Prüfung von Zeitpunkt und Minimum des mittleren Volumens im reduzierten Dirichlet-Modell. Ein eigenständiger physikalischer CST-Bounce und Singularitätsauflösung sind damit nicht bestätigt.

## Vorhersage und spätere Daten getrennt

`plan.json` wurde vor der späten Auswertung fixiert. `forecast.py` erzeugte anschließend ausschließlich aus den Anfangszuständen `forecast.json` und `FORECAST_SHA256`. Erst danach lief `verify.py` mit der getrennten Entwicklung in `propagate.py`. Der späte Löser erhält keine Forecast-Momente, Bounce-Zeit oder Sollkurve. Die Dateien und Toleranzen wurden nach Beobachtung der späten Ergebnisse nicht angepasst.

Die Eingaben sind acht neue Gaußpräparationen und zwei neue kohärente Überlagerungen. Sie wurden im vorherigen Klassiktest nicht verwendet. Dies ist eine getrennte rechnerische Gegenprüfung mit neuen synthetischen Anfangszuständen, keine neue physikalische Messung, externe Präregistrierung oder Replikation durch eine andere Forschungsgruppe.

## Referenzmodell

Es gilt q=sqrt(V)>0, kappa=1 in dimensionslosen Einheiten, H=hbar² d_qq und Dirichlet-Rand bei q=0. Das beschreibt die bereits gewählte homogene flache periodische Staubzelle, keinen vollständigen Staubball samt Außenraum und keine aus CST abgeleitete Quantentheorie.

Aus A=<q²>, J=2 hbar integral q Im(conj(psi)*psi_prime), E=hbar² integral |psi_prime|² folgt

```
<V(T)> = A - 2 J T + 4 E T²
T_b = J/(4 E)
V_b = A - J²/(4 E)
V_b >= hbar²/(4 E) > 0
```

Die Anfangsmomente werden durch Quadratur berechnet. Die späte Entwicklung verwendet einen zentralen räumlichen Differenzenoperator und Crank-Nicolson. Ein Gitterminimum und seine zwei Nachbarwerte bestimmen die späte Messgröße ohne Benutzung der frühen Prognose als Fitvorgabe. Eine zusätzliche Sinusentwicklung kontrolliert den Kontinuumskern an 50 Punkten.

## Ergebnisse

| Raumpunkte / Zeitschritt | Maximaler Zeitfehler | Maximaler Minimalvolumenfehler |
|---|---:|---:|
| 2048 / 0.005 | 10.2301 % | 18.4674 % |
| 4096 / 0.0025 | 2.4781 % | 5.1503 % |
| 8192 / 0.00125 | 0.6149 % | 1.3233 % |

Die vorher gesetzten Endtoleranzen sind 1 % und 3 %. Beide Fehler nehmen in jedem Fall bei jeder Verfeinerung ab. Der größte Normfehler beträgt 1.88e-12. Alle 30 Läufe, 7230 Ablesewerte und alle Fehler sind gespeichert. Raum- und Zeitfehler wurden gemeinsam, nicht separat, verfeinert. Dies sind Gleitkommaprüfungen, keine Intervallzertifikate.

## Kontrollen und Anspruchsgrenzen

- Dirichlet und Neumann liefern für zwei weit vom Rand präparierte Fälle innerhalb der Rechnung dieselben Volumen-Minima, aber unterschiedliche Randdichten. Sechs späte Neumann-Quadraturen prüfen die Momentkurve zusätzlich. Dies ist keine Prüfung sämtlicher Robin-Erweiterungen.
- Eine transparente volle q-Gerade hat ebenfalls ein Minimum von <q²>, obwohl der Schwerpunkt ins Negative läuft und nicht reflektiert wird. Negative q sind außerhalb der physikalischen Referenz; die Kontrolle zeigt nur, dass ein Volumenmittel allein Reflexion nicht identifiziert.
- Für alle acht Gauß-Bildzustände ist die Dirichlet-Randableitung zu jeder endlichen Zeit ungleich null. Damit divergiert <V^-2>, auch an der prognostizierten Umkehr. Das inverse Moment divergiert bei diesen Präparationen bereits anfangs; es wird kein Übergang von einem regulären zu einem singulären Zustand behauptet. Die beiden kohärenten Fälle werden durch den Einzel-Gauß-Beweis nicht zusätzlich klassifiziert.
- V^-2 wird nicht mit einem quantisierten Krümmungsoperator gleichgesetzt. Eine Singularitätsauflösung folgt nicht aus einem positiven Erwartungswertminimum.
- Der Begriff Bounce ist hier allein ein striktes Minimum des Volumenmittelwerts. Er ersetzt weder eine mehrzeitige Historienwahrscheinlichkeit noch das alte 80-%-Bounce-Gate.

Die volle CST-Prognose bleibt `HOLD_NOT_ELIGIBLE`: gekoppelter dynamischer Kern, physikalisches Maß, Vergröberung und der klassische Rückwirkungsnachweis fehlen. Der alte Kandidat bleibt `CLOSED_REJECTED_FOR_DOMINANT_BOUNCE`.

## Reproduzieren

```sh
python3 verify.py
python3 plot.py
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=results report.tex
```

`verify.py` überschreibt nur abgeleitete Ergebnisse im Ordner `results`. Die gespeicherten Prognosen bleiben unverändert und werden gegen neu berechnete Anfangsmomente geprüft. `forecast.py` verweigert das Überschreiben einer bestehenden Prognose. NumPy und SciPy sind nötig, Matplotlib nur für die Abbildung, LaTeX nur für den Bericht. Getestete Runtime-Versionen stehen in `results/verification.json`. Der Lauf dauert hier ungefähr 22 Sekunden; seine Zeitmessung ist maschinenabhängig.

`PLAN_SHA256`, `FORECAST_SHA256` und `provenance.json` sichern die verwendeten Daten. `SHA256SUMS` enthält die ausgelieferten Mitglieder ohne sich selbst. Es wurden keine neuen Kausalsets erzeugt, kein externes Rechenbudget verwendet und keine physikalischen Beobachtungen behauptet.

## Quellen

- Maeda, *Unitary evolution of the quantum universe with a Brown-Kuchar dust*: https://arxiv.org/abs/1502.06954
- Vorherige Klassik-/Rückwirkungsprüfung: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/236
- Historiengewichtung: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/235
- Frühere Regularitätsanalyse: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/rax_cqg/dust_collapse/reports/Staubball_Bounce_Regularitaet.pdf

Der bekannte Minisuperspace-Mechanismus wird hier anhand eines vorwärts gerichteten Prüfers nachvollzogen; es wird keine neue allgemeine Bounce-Theorie behauptet.
