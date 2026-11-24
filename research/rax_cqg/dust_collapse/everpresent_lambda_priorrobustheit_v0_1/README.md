# Everpresent Λ auf DESI DR2 und Pantheon+ · Replikation und Materieprior

24. November 2026. Für das publizierte Modell 2 beträgt das gemeinsame Evidenzverhältnis gegenüber flachem ΛCDM im präziseren Kontrolllauf **0,06185 ± 0,00134** mit der ursprünglichen Historienverteilung und **0,12484 ± 0,00261** mit einem für beide Modelle gleichen flachen Prior des heutigen Materieanteils. Die Kehrwerte betragen 16,17 und 8,01. Alle Fehlerangaben sind einfache numerische Standardfehler der Integration. Die Daten und ihre Messunsicherheiten gehen über die Likelihood in die Evidenzen ein.

[Kurzbericht](Kurzbericht.pdf) · [Sobol-Ergebnisse](resultate/ergebnis.json) · [Kontrolllauf für seltene Historien](resultate/importance.json) · [Festlegung vor dem Hauptlauf](protokoll.txt) · [Festlegung vor dem Zusatzlauf](zusatzprotokoll.txt)

## Ergebnisse mit denselben Himmelsdaten

Der Zähler ist jeweils die Evidenz der angegebenen Everpresent-Λ-Variante. Der Nenner ist immer die Evidenz derselben flachen ΛCDM-Referenz. Für beide Modelle ist die BAO-Skala h r_d auf [10, 1000] Mpc gleichverteilt. Ein freier Supernova-Nullpunkt wird ausintegriert, gemeinsame Normierungsfaktoren kürzen sich. Die Auswertung nutzt 13 DESI-DR2-BAO-Grössen und 1590 unkalibrierte Pantheon+-Lichtkurven mit zHD > 0,01 und den vollständigen ausgewählten Kovarianzen. Eine einzige Historie gilt jeweils für beide Datensätze.

| Rechnung und Prior des heutigen Materieanteils | DESI allein | DESI und Pantheon+ |
|---|---:|---:|
| Erstlauf PR 365, ursprüngliches Modell | 0,22286 ± 0,01506 | 0,08446 ± 0,01294 |
| Sobol, ursprüngliches Modell | 0,24305 ± 0,00872 | 0,05404 ± 0,00523 |
| Sobol, gleichförmiger Prior direkt gezogen | 0,48052 ± 0,01613 | 0,12600 ± 0,01061 |
| Gewichteter Zusatzlauf, ursprüngliches Modell | 0,23477 ± 0,00569 | 0,06185 ± 0,00134 |
| Gewichteter Zusatzlauf, nur Intervall eingeschränkt | 0,47513 ± 0,01151 | 0,12518 ± 0,00272 |
| Gewichteter Zusatzlauf, gleichförmiger Prior | 0,47877 ± 0,01153 | 0,12484 ± 0,00261 |

## Was die Änderung des Priors bewirkt

Das untersuchte Prozessmodell setzt m = Ωm0 = 1 − tanh g(0). Die Koeffizienten sind im Original unabhängig standardnormal, also ist g(0) normalverteilt mit Standardabweichung σ = ‖b(0)‖ = 0,8824 auf Maschinenpräzision. Für 0 < m < 2 folgt durch Variablentransformation

    g = artanh(1 − m)
    p(m) = exp[−g²/(2σ²)] / [√(2π) σ m(2−m)].

Das Intervall I = [0,01, 0,99] trägt die ursprüngliche Priorwahrscheinlichkeit P(I) = 0,49412619. Drei Ensembles machen den Einfluss des Priors messbar.

1. **Ursprünglich.** Jeder Pfad erhält sein ursprüngliches Wahrscheinlichkeitsgewicht.
2. **Konditioniert.** Nur m in I zulassen und das Gewicht durch P(I) teilen. Für die hier integrierte gemeinsame Likelihood ist der Beitrag ausserhalb von I numerisch vernachlässigbar. Der gemessene Faktor 2,02377 entspricht 1/P(I). Die Rechnung liefert keine analytische obere Schranke für ungezogene Pfade.
3. **Gleicher flacher Prior.** Innerhalb von I die Randdichte durch 1/0,98 ersetzen, bei gleicher bedingter Pfadverteilung für jedes m. Der zusätzliche Faktor im präziseren Lauf beträgt 0,99730 ± 0,00144. Beide Änderungen zusammen ergeben 2,01830 ± 0,00291. Die Fehler für die Faktoren nutzen die Korrelationen der Strommittel. Sie beziehen sich auf die Integrationspräzision innerhalb dieser Stichprobe.

Für die direkte Ziehung verwenden wir eine orthogonale Transformation der 18 Koeffizienten. Ihre erste Koordinate entspricht g(0)/σ. Setzt man diese Koordinate auf artanh(1−m)/σ und zieht die übrigen 17 unabhängig standardnormal, bleibt das ursprüngliche bedingte Prozessgesetz bei festem m erhalten. Die Gegenrechnung verwendet stattdessen ursprüngliche Pfade mit Gewicht 1_I(m)/[0,98 p(m)]. Der angeglichene Prior definiert eine eigene Sensitivitätsvariante. Der Projektstand leitet keinen der beiden Priors aus N15 her.

## Zwei Integrationsverfahren

**Festgelegter Hauptlauf.** 16 unabhängig gescrambelte 18-dimensionale Sobol-Netze mit je 16 384 Punkten. Dieselben Punkte speisen beide Priorvarianten, mit 262 144 ausgewerteten Historien je direkter Variante. Die Zwischengrössen 4096 und 8192 sind verschachtelte Teilnetze. Standardfehler werden aus der Streuung der 16 unabhängigen Netzmittel berechnet. Die Differenz der nativen Schätzung zum Erstlauf beträgt 2,18 kombinierte Standardfehler. Direkte und umgewichtete Gleichverteilung unterscheiden sich um 1,14 gepaarte Standardfehler. Alle acht vorab genannten Kriterien sind erfüllt.

**Zusatzlauf nach Sicht auf diese Abweichung.** 131 072 neue PCG64-Ziehungen in 16 unabhängigen Strömen. Ein Achtel der Ziehungen stammt aus dem ursprünglichen Normal-Prior. Zwei Student-Verteilungen in den ersten vier Koeffizienten konzentrieren die übrigen Ziehungen auf Regionen hoher Likelihood. Für die Schätzung ihrer Lage und Streuung dienten die eingefrorenen Historien des Erstlaufs. Die Mischdichte ist analytisch normalisiert und überall positiv. Jede Likelihood wird mit dem exakten Faktor p/q gewichtet. Die drei Stichprobenumfänge je Strom sind im Verhältnis 1:2:5 fixiert. Die Evidenz wird mit dem gewöhnlichen arithmetischen Mittel dieser korrigierten Beiträge integriert. Es findet keine Selbstnormalisierung und keine Zusammenlegung mit einem vorigen Lauf statt. Die 14 übrigen Koeffizienten folgen weiter ihrem ursprünglichen Gesetz.

Das mittlere Vorschlagsgewicht ist 1,00026 ± 0,00257, bei theoretischem Sollwert 1. Die Gewichtskonzentration der gemeinsamen Evidenz entspricht rund 3193 (ursprünglich) bzw. 3353 (gleichförmig) gleich gewichteten Beiträgen. Diese Grössen dienen als Konzentrationsdiagnostik. Die berichteten Fehler stammen aus den unabhängigen Strommitteln. Die Ergebnisse weichen vom direkten Sobol-Lauf um 1,45 bzw. 0,11 kombinierte Standardfehler ab. Alle fünf Kriterien des Zusatzprotokolls sind erfüllt. Die nachträgliche Entscheidung für diesen Zusatzlauf begrenzt seine Interpretation als vorab geplante Replikation. Beide Verfahren verwenden dieselbe Likelihood und dieselben Himmelsdaten.

**Numerische Kontrollen.** Die erneut berechneten ΛCDM-Log-Evidenzen stimmen in dieser Softwareumgebung mit dem Archiv überein. Eine separate 48-Punkt-Gauss-Legendre-Integration reproduziert die transversalen und radialen Distanzen an den vier festgelegten Kontrollhistorien mit relativer Abweichung unter 2,7 × 10⁻¹⁰. Die Bezugsdateien und die vier Eingabedateien werden per SHA-256 geprüft. Die Protokollhashes sind lokale Inhaltsnachweise. Externe Zeitstempel fehlen.

## Nachrechnung

Die mitgelieferten Ergebnisse, Prüfentscheidungen und die Randverteilung lassen sich offline mit Python 3.11+ prüfen. Aus dem Studienverzeichnis:

```sh
python -B pruefen.py
```

Für den vollständigen Rechenlauf werden zusätzlich NumPy und SciPy benötigt. Verwendet wurden NumPy 2.3.5 und SciPy 1.17.0. Ein vorhandener Datenordner mit den vier Originaldateien kann übergeben werden. Bei leerem Cache lädt die Referenzpipeline die im Quellenregister festgeschriebenen Versionen. Die mitgelieferte Vorschlagsdatei reicht für den vollständigen Zusatzlauf aus.

```sh
python -B priorlauf.py --cache cache --out nachrechnung
python -B seltene_historien.py --cache cache --out nachrechnung
```

Der Zusatzlauf nutzt für seine Vergleichskennzahlen das eingefrorene Sobol-Ergebnis aus `resultate/ergebnis.json`. Beide Hauptschätzer werden aus den Originalmessdaten neu berechnet. Die 48 Zeilen in `netze.csv` und die 16 Zeilen in `importance_stroeme.csv` dokumentieren die Mittelwerte je Folge. Einzelpfade können mit den angegebenen Seeds, Softwareversionen und Generatoren regeneriert werden. Zum optionalen Wiederaufbau von `vorschlag.json` aus der Originaldatei `resultate/historien.npz` des Erstlaufs:

```sh
python -B seltene_historien.py --train /pfad/zum/historien.npz --proposal vorschlag_kontrolle.json
```

[Originalcode und Trainingsarchiv am verwendeten Commit](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/d00c21965fd37f08d4979653ef6e5ad96e5a785a/research/rax_cqg/dust_collapse/everpresent_lambda_dr2_pantheon_v0_1) · [Quelldaten und Prüfsummen](basis/pipeline/quelldaten.json) · [Modell 2, Gleichungen 2.9 und 2.10 und Tabelle 1](https://arxiv.org/abs/1703.06265) · [DESI DR2](https://arxiv.org/abs/2503.14738) · [Pantheon+](https://arxiv.org/abs/2202.04077)

Der Vergleich gilt für das festgelegte phänomenologische Hintergrundmodell mit α = 0,8824 und μ = 0,9804. Eine Zuordnung vom lokalen N15-Staubball zu einer Verteilung kosmologischer H(z) ist weiterhin offen. Die 60 physikalischen P3-Prüfpunkte stehen auf NOT_RUN.
