# Everpresent Λ auf DESI DR2 und Pantheon+

Erster kosmologischer Modelllauf des CST-DUST-Projekts · 24. November 2026

Für das phänomenologische Everpresent-Λ-Modell 2 mit festem α = 0,8824 und μ = 0,9804 ergibt sich aus beiden Datensätzen ein Evidenzverhältnis von 0,0845 ± 0,0129 (Everpresent Λ geteilt durch flaches ΛCDM, einfacher Monte-Carlo-Standardfehler). 50 der 131 072 gezogenen Historien erreichen oder unterschreiten das beste χ² der Referenz. Die Schlussfolgerung gilt für die gewählte Verteilung der Expansionsgeschichten, die angegebenen Priors und die geometrischen Daten. Eine Abbildung vom lokalen N15-Kollaps auf einen kosmologischen Hintergrund ist im Projekt offen.

[Kurzbericht mit Abbildung](Kurzbericht.pdf) · [Hauptergebnis](resultate/ergebnis.json) · [Unabhängige Gegenrechnung](resultate/kontrollen.json) · [Skalenfreier Distanzvergleich](resultate/DESI_skalenfrei.csv)

## Was vor dem Lauf feststand

Die mathematische Vorschrift, die beiden Parameter, der Zufallsstart, die Anzahl der Ziehungen, der primäre Vergleich und die Vergleichsschwellen wurden im [Laufprotokoll](protokoll.txt) vor der Auswertung festgelegt. Die lokale Prüfsumme dokumentiert den Inhalt. Ein externer Zeitstempel liegt nicht vor. Die Literatur und der frühere ΛCDM-Lauf waren bekannt. Dies ist eine Anwendung auf bereits veröffentlichte Daten. Andere Autoren haben Modell 2 ebenfalls an DESI DR2 und Pantheon+ untersucht, unter anderem mit eigenem Schallhorizont und BBN-Prior. Deren Zahlen sind wegen der abweichenden Modellierung nicht direkt mit diesem Lauf vergleichbar. [Zwane, Afshordi und Sorkin, Gl. 2.9–2.10 und Tabelle 1](https://arxiv.org/pdf/1703.06265) · [Frühere Untersuchung von Dat Tan Nguyen](https://synapsesocial.com/papers/6ac1ec6de428693a5716e757)

## Vom Modell zur Distanz

1. Für x = ln a wird ein mittelwertfreier Gaussprozess g mit Kovarianz K(x,y) = α² exp[−μ(x−y)²/2] gezogen. Die zeitabhängige Dunkelenergiefraktion ist Ωde(x) = tanh g(x). Wir verwenden die gedruckte Realraum-Kovarianz aus Gl. 2.9. Die 2018 bestimmten Hyperparameter sind ein publizierter Beispielpunkt mit älteren CMB- und BAO-Daten. Die spezifische damals angepasste Historie wird nicht übernommen. Alle neuen Historien erhalten das gleiche Prior-Gewicht. Die Ziehung ist unbedingt, auch negative heutige Ωde-Werte sind zulässig.
2. In der flachen, räumlich homogenen Hintergrundrechnung mit erhaltener nichtrelativistischer Materie und vernachlässigter Strahlung gilt Ωm0 = 1 − Ωde(0) und E²(z) = H²(z)/H₀² = (1+z)³ Ωm0 / [1 − Ωde(−ln(1+z))]. Kein zusätzlicher Ωm0-Fit für eine gezogene Historie. Die Annahmen gelten im untersuchten späten Fenster bis z = 2,33. Es wird keine Frühzeitkalibrierung des Schallhorizonts berechnet.
3. Mit I(z) = ∫₀ᶻ dz′/E(z′) und s = h r_d in Mpc ergeben sich D_M/r_d = 2997,92458 I(z)/s, D_H/r_d = 2997,92458/[s E(z)] und D_V/r_d = [z (D_M/r_d)² D_H/r_d]^(1/3). Das Supernovamodell lautet m_b = 5 log₁₀[(1+zHEL) I(zHD)] + ℳ. Jede Historie sagt damit die Distanzform bereits vor der Anpassung der Skalen voraus.
4. Das direkt beobachtbare Verhältnis F_AP = D_M/D_H = E(z) I(z) enthält weder H₀ noch r_d. Die sechs anisotropen DESI-Bins erlauben eine Darstellung. Die 68%-Fehler der gemessenen Verhältnisse folgen hier näherungsweise aus linearer Fehlerfortpflanzung mit dem zugehörigen 2×2-Kovarianzblock. Der Originalfit benutzt die 13 ursprünglichen Observablen, einschliesslich D_V bei z = 0,295, mit der vollständigen 13×13-Kovarianz. Die Quotienten dienen allein der Illustration.

## Identische Datenbehandlung

Der Lauf importiert die Datenprüfung, Redshift-Auswahl und Kovarianzaufbereitung aus dem bereits geprüften Referenzcode. Bei Pantheon+ bleiben 1 590 von 1 701 Lichtkurven nach zHD > 0,01. Die ausgewählten Zeilen und Spalten der STAT+SYS-Kovarianz werden gemeinsam übernommen. Die Rotverschiebung in der Distanzintegration ist zHD, im Vorfaktor zHEL. Es gibt keine Cepheiden-Verankerung. DESI und Pantheon+ gelten bei gegebenen Parametern und derselben Historie als bedingt unabhängig. [Pipeline im verwendeten Git-Stand af54400](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/af544001af7475b14a753d26b6733dfbac66de10/research/rax_cqg/dust_collapse/n15_uhr5_vierphasentest_v0_1/daten) · [DESI DR2](https://arxiv.org/abs/2503.14738) · [Pantheon+](https://arxiv.org/abs/2202.04077) · [Eingabedateien und SHA-256](pipeline/quelldaten.json)

## Anpassung und Evidenz

Für jede Theorie gilt derselbe flache Prior für s = h r_d auf [10,1000] Mpc. Der freie Supernova-Nullpunkt wird analytisch integriert. Sein konstanter Normierungsfaktor ist für beide Modelle identisch und kürzt sich im Vergleich heraus. Die in der JSON-Datei archivierten log Z sind bis auf gemeinsame Normierungskonstanten definiert. Die Referenz integriert zusätzlich mit flachem Ωm-Prior auf [0,01,0,99]. Der Materieanteil in Modell 2 folgt dagegen aus der positiven oder negativen Dunkelenergiefraktion der jeweiligen Ziehung. Die beiden Verteilungen für Ωm0 unterscheiden sich wesentlich. Eine Änderung dieser Priors, eine Konditionierung auf den heutigen Materieanteil oder andere Hyperparameter verlangt eine neue Berechnung.

Für die profilierte χ²-Angabe wird die beste BAO-Skala bestimmt. Für die Evidenz wird die Likelihood über den gesamten vorgegebenen Skalenprior integriert. In der inversen Skala v=1/s ist die BAO-Likelihood eine Gaussfunktion mit Krümmung C>0. Die Integration berücksichtigt den Jacobi-Faktor v⁻². Das standardisierte Integrationsintervall wird bei ±14 Standardabweichungen abgeschnitten. Eine direkte adaptive Integration in s prüft die Genauigkeit für drei Historien. Für ΛCDM ergibt eine zusätzliche zweidimensionale Integration mit dem ursprünglichen Quadraturgitter denselben log-Z-Wert.

| Auswertung | Ergebnis |
|---|---:|
| DESI allein, Evidenzverhältnis Modell 2 / ΛCDM | 0,2229 ± 0,0151 |
| DESI und Pantheon+, gleiches Verhältnis | 0,0845 ± 0,0129 |
| Zusätzlicher relativer Vorhersagefaktor für Pantheon+ nach DESI | 0,3790 |
| Effektive Zahl gewichteter Historien für die gemeinsame Evidenz | 42,6 |
| Δχ² ≤ 0 gegenüber dem globalen ΛCDM-Minimum | 50 von 131 072 |
| Δχ² ≤ 4 gegenüber dem globalen ΛCDM-Minimum | 113 von 131 072 |

Der dritte Wert ist das gemeinsame Evidenzverhältnis geteilt durch das DESI-Evidenzverhältnis. Eine gemeinsame, unkalibrierte Supernova-Nullpunktkonstante fällt im modellvergleichenden Quotienten weg. Die angegebenen ±-Werte sind je ein Standardfehler der arithmetischen Monte-Carlo-Mittel aus unabhängigen Historien. Die alternative Streuung der 16 Blockmittel liefert 0,0099 für das gemeinsame Verhältnis. Die einzelnen Blöcke ergeben 0,0207 bis 0,1612. Die geringe effektive Stichprobe begrenzt die Präzision. Der Kehrwert des gemeinsamen Punktschätzers beträgt 11,84. Modellwahrscheinlichkeiten würden zusätzlich vorherige Modellgewichte benötigen.

| Behandlung | χ² DESI | χ² Pantheon+ | χ² gesamt |
|---|---:|---:|---:|
| ΛCDM, Ωm und Skalen angepasst | 10,870 | 1405,269 | 1416,139 |
| Erster im Protokoll festgelegter Zug, nur Skalen angepasst | 512,896 | 1574,843 | 2087,739 |
| Kleinster Wert unter 131 072 Zügen, nach Datensicht ausgewählt | 7,868 | 1402,885 | 1410,754 |

Die seltene beste Ziehung ist ein Beispiel dafür, dass das Modell passende Kurven erzeugen kann. Ihr χ² ist als ausgewähltes Minimum ungeeignet, um die Modellgüte des ganzen Ensembles oder eine Entdeckungswahrscheinlichkeit abzuleiten. Die Schwellenzählungen sind Prior-Anteile des gewählten Modells, keine p-Werte.

## Numerik und Nachrechnung

Die 16 unabhängigen Zufallsströme verwenden PCG64 mit SeedSequence(20261124) und je 8 192 Ziehungen. Die 18 Koeffizienten je Historie parametrisieren die konvergente Reihe des exakten Kerns um die Mitte des logarithmischen Zeitfensters. Mit t = √μ (x + ln(3,33)/2) lautet sie g(x) = α exp(−t²/2) Σ ξₖ tᵏ/√(k!), k=0,…,17. Die ξₖ sind unabhängig standardnormal. Der nicht berücksichtigte Rest hat an jedem einzelnen Punkt eine Standardabweichung unter 10⁻¹². Diese punktweise RMS-Schranke folgt aus dem exponentiellen Reihenrest und ist keine uniforme Pfadfehlerschranke. Für die Hauptrechnung werden eine kumulative Simpson-Integration und kubische Hermite-Auswertung der Stammfunktion auf 513 logarithmischen Stützstellen verwendet.

Die getrennte Gegenrechnung integriert bei den originalen Rotverschiebungen mit 48-Punkt-Gauss-Legendre, direkter Polynomauswertung und separater Kovarianzlösung. Beim ersten, zweiten und nachträglich besten Zug blieb die Summe der absoluten Differenzen der zwei χ²-Beiträge unter 1,1×10⁻⁶. Die 131 072 Verläufe, ihre Skalen und χ²-Beiträge sind im Paket enthalten. CSV-Spalten namens first beziehen sich auf die vorher festgelegte Historie 0, best_draw auf die anhand der Daten ausgesuchte Historie 13690. Bei DESI_vorhersagen.csv und Pantheon_vorhersagen.csv sind die beiden Skalen an die jeweiligen Daten angepasst. erste_distanzkurve.csv und DESI_skalenfrei.csv dokumentieren auch skalenfreie Vorhersagen.

Erforderlich sind Python 3.11 oder neuer, NumPy und SciPy (Originalversionen im Ergebnis). Alle archivierten Resultate können offline gelesen werden. Für eine Neuberechnung müssen die vier veröffentlichten Eingaben einmalig von ihren fixierten URLs bezogen werden. Ein vorhandener Datenordner lässt sich mit --cache übergeben. Aus dem entpackten Studienordner:

```sh
sha256sum -c SHA256SUMS
python -B lauf.py --out vergleich
python -B gegenprobe.py --out vergleich
```

Beim Start prüft das Programm die vier Eingaben gegen ihre SHA-256-Prüfsummen. Die ZIP-Datei enthält den Referenzcode mit Lizenz und Herkunft, die vollständigen Modellziehungen und Ergebnisdateien. Im Archiv für die Historien stehen rows und coefficients in derselben Reihenfolge. Die IDs sind nullbasiert. Das Feld log_scale_integral erfasst den Skalenintegralfaktor ohne das profilierte χ². Die Likelihoodgewichte erhält man als exp(log_scale_integral − (chi2_bao+chi2_sn)/2) mit der üblichen numerischen Log-Sum-Exp-Stabilisierung.

## Bezug zu CST-DUST

Die N15-Studien untersuchen lokalen Staubkollaps. Für eine eigenständige Vorhersage des Staubballs braucht es eine vom kosmologischen Datensatz unabhängig begründete Abbildung vom mikroskopischen Zustandsensemble auf eine Expansionsgeschichte oder ihre Verteilung. Weder α und μ noch eine der hier gezogenen Historien wurden aus N15 hergeleitet. Der vorliegende Test betrifft die kosmologische Hintergrundgeometrie des publizierten Modell-2-Ansatzes. Der P3-Status des Staubballs bleibt offen.
