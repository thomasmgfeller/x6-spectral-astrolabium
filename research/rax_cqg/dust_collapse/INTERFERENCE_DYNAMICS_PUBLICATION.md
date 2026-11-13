# Interferenz, vollständige innere Randamplitude und Dynamikprüfung v0.1

13. November 2026 · Anschluss an den [stationären Geometriekandidaten](GEOMETRY_DYNAMICS_PUBLICATION.md), PR 291 / `da48df345a20b3922b5764ad795e3bf2444d9bb4`.

**Die vollständigen inneren Uhr-/Dichtegewichte des N11-Paars sind unter einem gemeinsamen, ausdrücklich gewählten Dirichlet-/Boxvertrag berechnet. Sie verändern Betrag und Phase der relativen Amplitude. Bedingte Auslesemodelle und die Zusammensetzung mit voller Schnittinformation sind konsistent konstruiert; physikalische Geometriedynamik bleibt NOT_DERIVED.**

[Bericht (PDF)](reports/CST_DUST_Interferenz_Dynamik_v0_1.pdf) · [Originalprüfpaket (ZIP)](packages/CST_DUST_Interferenz_Dynamik_v0_1_Pruefpaket.zip) · [Quellen und Reproduktion](interference_dynamics_v0_1/README.md) · [Rand- und Maßvertrag](interference_dynamics_v0_1/contracts/interference_contract.json) · [Publikationsnachweis](interference_dynamics_publication.json)

## Drei ausgeführte Aufgaben

| Aufgabe | Ergebnis | Reichweite |
| --- | --- | --- |
| Vollständiges relatives Gewicht | Drei innere Uhren und alle acht Atom-/Positivdichtestrata integriert, sämtliche Randwirkungsterme erhalten | Gewähltes gemeinsames Uhrmaß; äußere Uhr-/Dichtewerte bleiben Dirichletdaten |
| Auslese begründen | Stark positive endliche Recordmodelle und unter zusätzlichen Eingangsannahmen vollständige CP-Instrumente konstruiert | Historiengewichte, Recordüberlapp und physische Randpaarung nicht aus der Wirkung ausgezeichnet |
| Dynamik prüfen | 22 Präfixidentitäten, vier Schnittprüfungen und dreiteilige Zusammensetzung exakt geschlossen | Volle Schnittinformation; keine reduzierte physische Zeitentwicklung hergeleitet |

Die Wirkung bleibt unverändert. C₀ ist die elfgliedrige Kette; C₁ entfernt (4,5) und (5,6), behält (4,6). Für die drei inneren Uhren wird die zuvor vorbereitete gemeinsame Box `[-3/2,3/2]` mit `dT/3` gewählt. Die ursprüngliche innere Dichtemischung `(δ₀+1_(0,1)dr)/2` bleibt erhalten. Es wird **keine zusätzliche Beschränkung auf monotone Uhren** eingeführt.

Die exakte Faktorisierung lautet `a_c = omega_c W_c(rho) g_c`. W enthält bereits `exp(iF_c)` und die vollständige Staub-/Uhrphase. **Ein zusätzlicher Faktor exp(iS_on) würde die Wirkung doppelt zählen.** Der skalare Quotient wird erst nach gemeinsamer Schwartz-Randpaarung gebildet; der singuläre Innenblock der zweiten Ordnung wird distributionell behandelt.

| Numerische Diagnose | ρ=1/8 | ρ=1/4 |
| --- | --- | --- |
| Betrag des vollständigen inneren Gewichtsverhältnisses \|W₁/W₀\| | 1,60554753 | 1,86937006 |
| Komplexe Einsetzung q₀q₁₀ bei gleichen festen Historiengewichten | 0,04695082 + 0,02516108 i | 0,01725347 + 0,08261839 i |
| Bedingter Mittelwert der vergleichbaren Innenpaare beim getrennten aufgelösten Recordvertrag | 2,47359382 | 2,34746389 |

Die Rand-Einsetzung ist keine positive Messkovarianz. Der aufgelöste Recordvertrag ist ein anderes Experiment als die kohärente gemeinsame Auslese. Die geometrische Observable hat die invarianten Werte 3 und 1; sie ist kein Radius oder räumliches Volumen. **ρ verändert sowohl den vergangenen als auch den zukünftigen Dichtekragen.** Der Vergleich ist eine beidseitige Randparameterantwort, keine Zeitentwicklung und keine isolierte Anfangsstörung bei festem späteren Filter.

Die Unterbestimmtheit ist konkret: Bei gleichen Wirkungsamplituden verändern zusätzliche Recordüberlappungen und Historiengewichte die bedingten Vorhersagen. Positive endliche Modelle sind möglich, werden aber durch die vorliegenden Daten nicht eindeutig ausgewählt. Das ist kein allgemeiner Unmöglichkeitssatz für CST-Dynamik.

## Fehlerkontrolle und unveränderte Originale

Die Uhrquadraturen mit 64, 96, 128 und 160 Knoten pro Achse besitzen unabhängig hergeleitete Bernstein-/Chebyshev-Restschranken für `0≤ρ≤1/4`. Bei n=160 liegen die W-Reste unter `1,2×10^-25` bzw. `1,6×10^-32`; ein unabhängiger rationaler Taylor-Audit bestätigt die Obergrenzen. **Diese Schranken enthalten nicht die Rundungsfehler der Float64-Auswertung.** Die Zahlen sind kontrollierte Näherungen, keine vollständigen Intervallzertifikate.

Alle 37 Dateien des Originalpakets, das ursprüngliche ZIP und der separate Bericht werden unverändert veröffentlicht. Der separate Bericht stimmt bytegleich mit dem eingebetteten PDF überein. Die sechs Fachberichte dokumentieren KI-gestützte interne Gegenprüfungen, keine externe Begutachtung.

```sh
python -m pip install -r research/rax_cqg/dust_collapse/interference_dynamics_v0_1/requirements.txt
python -B research/rax_cqg/dust_collapse/verify_interference_dynamics_publication.py
```

Die Publikationsprüfung kontrolliert Dateigrößen, SHA-256, vollständige ZIP/Quellcode-Parität und beide PDF-Kopien. Anschließend laufen acht Programme isoliert; neun JSON-Dateien werden reproduziert. Algebraische Angaben stimmen exakt, Floatwerte innerhalb `abs_tol=rel_tol=5e-12`; Laufzeiten werden ausgenommen, Quellhashes gegen die jeweiligen Original-/Replaydateien validiert. Diese Reproduktionstoleranz ist keine wissenschaftliche Fehlerschranke.

Die auf diese Veröffentlichung begrenzte CI wiederholt nur die kleinen Rechnungen dieses Pakets. Angaben zum früheren Publikationsstatus in den Originaldateien beschreiben den Stand vor dieser Veröffentlichung.

English: the complete inner dust/clock amplitudes for the finite N11 pair are evaluated under a declared common Dirichlet/box contract, retaining all eight density strata. Their source response changes modulus as well as phase. Conditional positive readouts and full-memory composition are constructed, while physical history weights, boundary pairing and calibrated four-dimensional geometric evolution remain unestablished. Original artifacts are preserved; eight isolated programs reproduce nine JSON outputs with explicitly separated algebraic and numerical checks.
