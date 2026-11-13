# CST-DUST: Interferenz, Randantwort und Dynamikprüfung v0.1

Die drei Anschlussaufgaben zum stationären N11-Paar sind bearbeitet: das vollständige **innere** Uhr-/Dichtegewicht unter einem expliziten Dirichlet-/Boxvertrag, eine Familie konsistenter bedingter Auslesemodelle und die exakte Zusammensetzung mit vollständiger Schnittinformation. Die physikalische Geometriedynamik ist weiterhin **NOT_DERIVED**.

Ausgangspunkt: [stationärer Geometriekandidat, PR 291](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/291), main-Commit `da48df345a20b3922b5764ad795e3bf2444d9bb4`. Die Wirkung bleibt unverändert; der zuvor optionale gemeinsame Uhrträger `[-3/2,3/2]` wird hier mit normiertem Maß gewählt. Keine zusätzliche Theta-Bedingung auf Uhrmonotonie. Die ursprünglichen acht Atom-/Positivkombinationen der drei inneren Dichten bleiben erhalten. Feste äußere Uhren und Dichten sind Dirichletdaten, keine hergeleiteten normierten physischen Randpakete.

## Neue Ergebnisse

1. Alle drei inneren Uhren und acht Dichtestrata integriert, einschließlich aller äußeren Wirkungsterme. Die volle Amplitude lautet `a_c=omega_c*W_c*g_c`; W enthält bereits die Gravitationsphase. **Kein zusätzlicher Faktor exp(iS_on).**
2. `|W1/W0|` verändert sich bei `rho=1/8 -> 1/4` von `1.60554753` auf `1.86937006`. Die logarithmische Quellenableitung ist `0.894388+2.298402i` beziehungsweise `1.499473+1.726612i`, nicht bloß `i*23/19`.
3. Bei ausdrücklich gleichen festen Historiengewichten verändert sich die komplexe Rand-Einsetzung `q0*q10` von `0.04695082+0.02516108i` auf `0.01725347+0.08261839i`. Das ist keine positive Messkovarianz.
4. Das Record-Gram-Modell ist stark positiv und lässt sich bei zusätzlich deklariertem endlichen Eingangsraum zu vollständigen CP-Instrumenten ergänzen. Die Rechnung beweist zugleich die Unterbestimmtheit durch freie Recordüberlappungen und Historiengewichte.
5. 22 Präfixidentitäten, vier Schnittidentitäten und dreiteilige Assoziativität schließen die Zusammensetzung mit voller Erinnerung. Das naive Produkt ohne Kreuzbeiträge scheitert an allen vier Schnitten.
6. Die intrinsische Geometriegröße vergleichbarer Innenpaare hat Werte 3 und 1. Im **separaten aufgelösten Recordvertrag**, bei gleichen Gewichten, lautet ihr bedingter Mittelwert `2.47359382 -> 2.34746389`. Dieser Quellenvergleich verändert auch den späteren Dirichletrand; er ist keine Zeitentwicklung und keine isolierte Anfangsstörung.

## Fehler und Aussagegrenzen

Die drei Uhrintegrale wurden mit Gauß-Legendre-Tensorquadratur `n=64,96,128,160` berechnet. Analytische Bernstein-/Chebyshev-Restschranken für `0 <= rho <= 1/4` sind unabhängig und rein rational gegengeprüft. Bei n=160 liegen die W-Reste unter `1.2e-25` und `1.6e-32`. **Diese Grenzen enthalten nicht die Float64-Knoten-, Funktions- und Summationsrundung.** Die numerischen Ergebnisse sind keine vollständigen Intervallzertifikate. Die 128/160-Abweichungen betragen etwa `1e-15` bei W und `1e-14` bei W'.

Die skalare Gaußphase ist durch unabhängige Fresnel- und Fourier-Delta-Auswertung kontrolliert. Hohe Rechenpräzision wird auch dort nicht als Intervallbeweis ausgegeben.

Kein bevorzugtes physisches Historienmaß, keine physikalische Uhr-/Staub-Randpaarung, kein hergeleiteter Detektor und keine kalibrierte vierdimensionale Staubball-Dynamik werden behauptet. Dies ist ein endlicher vollständiger Prüfstein für künftige physikalische Verträge, kein allgemeiner Unmöglichkeitssatz.

## Reproduktion

Python 3.12 wurde verwendet; die numerischen Abhängigkeiten sind fixiert:

```bash
python -m pip install -r requirements.txt
python -B verify.py
```

Der Prüfer kontrolliert das Manifest, kopiert das Paket in ein temporäres Verzeichnis und führt acht Programme aus. Er vergleicht alle erzeugten JSON-Ergebnisse, exakt für algebraische Angaben und mit `abs_tol=5e-12`, `rel_tol=5e-12` für Floatwerte. Laufzeitangaben werden vom Vergleich ausgenommen. Eingebettete Quellhashes werden jeweils gegen die tatsächlichen Quelldateien des Originals und des Replays geprüft: durch neue Laufzeitmetadaten ändern sich deren Bytes, während numerische Inhalte separat verglichen werden. Diese Toleranz prüft Reproduzierbarkeit, sie ist keine neue physikalische oder rigorose numerische Fehlerschranke. Der Prozess verändert keine archivierten Ergebnisse.

PDF erneut erzeugen: `python -m pip install -r report/requirements.txt` und `python report/build_report.py`. Das PDF enthält sechs Seiten; seine Dateibytes können durch Erstellungszeitstempel variieren und sind kein numerischer Replay-Ausgang.

## Inhalt

| Pfad | Zweck |
| --- | --- |
| `contracts/interference_contract.json` | Gemeinsamer Rand-/Maßvertrag und explizite Grenzen |
| `agents/` | Sechs Fachberichte mit Herleitungen und unabhängiger Kritik |
| `checks/full_weight/` | Drei Uhren, acht Strata, Quellableitungen, Quadraturrest |
| `checks/scalar_response/` | Exakte Determinanten, Abel/Fresnel-Zweig, Randinsertionen |
| `checks/physical_readout/` | Positive Recordmodelle, CP-Vervollständigung, Unterbestimmtheit |
| `checks/composition/` | Präfixe, Schnitte, Assoziativität, Gedächtnisvertrag |
| `checks/geometry_response/` | Invariante Geometriegröße, aufgelöster Kontrast und Ablationen |
| `checks/independent_audit/` | Unabhängige Algebra und rationale Restzertifikate |
| `checks/combined_response/` | Zusammensetzung der berechneten Amplituden und Randantwort |
| `sources/` | Drei gehashte Quelldateien des Ausgangsstands |
| `report/` | Bericht und PDF-Generator |

Primärliteratur zur Einordnung: [Giulini (2000)](https://arxiv.org/abs/gr-qc/0003040), [Dowker, Johnston, Surya (2010)](https://arxiv.org/abs/1007.2725). Die neuen endlichen Ergebnisse sind eigene Ableitungen; ihre Belege liegen im Code und in den Fachberichten. Sechs KI-Fachagenten unterstützten die Bearbeitung, keine externe Begutachtung wird behauptet.
