# CST-DUST: gemeinsamer Rand- und Auslesevertrag v0.1

**Ergebnis:** Für das veröffentlichte N11-Paar ist ein gemeinsamer positiver
**bedingter skalarer Drei-Moden-Vertrag** konstruiert, einschließlich exakter
Normfaktoren, fortgesetzter Fresnelphasen und eines vollständigen lokalen
Messinstruments. Die ursprüngliche Gesamtwirkung wählt diesen Vertrag nicht
eindeutig aus. Die physikalische Geometriedynamik ist damit nicht geschlossen.

Stand: 13. November 2026. Ausgangspunkt: [PR #292](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/292),
Commit `06ca1444d582f2c3563e0be015b5ae7c3dbc9c49`.
Sechs Fachagenten und unabhängige algebraische Rekonstruktionen: interne
KI-gestützte Prüfung, keine externe Begutachtung.

## Was die ursprüngliche Wirkung entscheidet

- Die Skalar-Legendrematrix hat Rang 7 für C0 und Rang 6 für C1.
  C1 erzwingt je einen linearen Prä-/Postconstraint. Ein nichtverschwindender
  C1-Ausgang ist im ursprünglichen gemeinsamen `L²(R⁴,dq)` nicht normierbar.
- Der gemeinsame starke Constraintkern trägt C0 nicht: Der zurückgezogene
  Postconstraint hat mit dem Präconstraint die von null verschiedene
  physische Poissonklammer `−52625/(32β)`, `β=4/√6`.
  Dies schließt eine zusätzliche Projektion/Quotientierung nicht aus.
- Bei festen vergangenen Randuhren gilt exakt
  `Wc(ρP,ρF)=exp(−i151ρP/38) Wtilde_c(ρF)`.
  Eine isolierte Variation von ρP erzeugt keine relative Antwort. Der frühere
  diagonale Kontrast bei ρP=ρF ist innerhalb dieses Dirichletvertrags vollständig
  eine Zukunftsrandantwort. Integrierte Anfangs-Uhrpakete sind nicht erfasst.
- Die vollständige Uhr-/Dichte-Randrelation bestimmt die Zukunft unter den
  geprüften kanonischen Anfangsdaten nicht eindeutig. Für C1 existiert eine
  exakte Familie verschiedener künftiger Uhren mit denselben Anfangsdaten.

## Der konstruktive neue Vertrag

1. Gemeinsamer Quotient nach den C1-Randconstraints, **zusätzlich auch für C0**.
   Sektionen: eingangs q0=0, ausgangs q10=0. Kanonische CCR
   `[q,π]=i/β`, `π=p/β`, und positiver Raum `H3=L²(R³,dx)`.
2. Zwei exakt symplektische reduzierte Karten R0,R1. Der C0-Rigging-Sandwich
   benötigt den berechneten positiven Faktor `sqrt(2π·52625/(32β))`.
   Für C1 entsteht der exakt unitäre Deltakern mit Vorfaktor
   `92√2 β/(2π)`. Beide Kompositionsrichtungen sind geprüft.
   Die festgelegte Fourier-/Abelkonvention führt die relativen Phasen mit.
3. Gemeinsames Eingangspaket `(β/π)^(3/4) exp(−β|x|²/2)`.
   Lokaler Pointer `U=exp(−ig q7 p_y)` mit normierter Gaußpräparation.
   Die Krausdichte ist `M_y=(2πσ²)^(-1/4) exp[−(y−gq7)²/(4σ²)]`.
   Ihr Integral erfüllt `∫M_y†M_y dy=I`. Ein freies Klassen-γ wird ersetzt
   durch einen aus Zustand und Detektorkopplung berechneten Kreuzkern.
4. Deklarierte kohärente Kontroll-/Umweltpräparation mit festen positiven
   Gewichten `ω0+ω1=1`. Die akzeptierte Karte ist
   `K=Σωc Wc Vc`, mit `||K||≤1`. Das orthogonale Ancillakomplement liefert
   den Failure-Effekt `I−K†K`. Alle akzeptierten Pointerausgänge plus Failure
   summieren zu I. W enthält die Gravitationsphase bereits vollständig.

**Bedingte Referenzzahlen** bei g=σ=1: Pointervarianzen 21,55928 (C0) und
2,41176 (C1); `P(|y|≤1)` getrennt nach präpariertem Zweig 0,170520 und
0,480374. Das sind Modellvorhersagen der neuen gemeinsamen Reduktion,
keine gemessenen Zahlen und keine Fortsetzung der alten achtmodigen
Schwartz-Randpaarung bei unveränderter Präparation. Unterschiedliche
Zweigverteilungen sind keine perfekte projektive Messung der Historienklasse.
Die phasentreuen kohärenten Resultate stehen im Detektorbericht und dessen JSON.

## Präzise verbleibende Auswahl

Die neue gemeinsame Projektion, CCR-/Paarungswahl, Hilfsumweltdeutung,
Kontrollpräparation und der reale Detektoraufbau sind erklärte Zusatzannahmen.
Innerhalb dieses Vertrags werden Normierungen und Interferenz berechnet;
seine physikalische Geltung folgt nicht allein aus der ursprünglichen Wirkung.
Auch positive Kovarianz, exakte Präfixkomposition, klassische Markov-Normierung
und Bell-Kausalität erzwingen kein eindeutiges Historienmaß. Klassische
Wachstumswahrscheinlichkeiten sind nicht automatisch Quantenamplitudengewichte.

Das kompakte Atom-/Intervallmaß ist kein Constraint-Delta und trägt keine
unbeschränkte unitäre Dichtetranslation. Vollständig integrierte physikalische
Uhr-/Dichterandpakete, eine dadurch begründete Anfangsantwort sowie eine
vierdimensionale Staubball-/Verfeinerungsaussage bleiben offen.

Der nächste inhaltliche Test ist ein **einseitiges Anfangspräparationsexperiment**:
bei unverändertem späterem Instrument gemeinsame Uhr-/Dichtepakete und ihr
physisches Skalarprodukt festlegen, anschließend Quelle und Kontrollgewichte
getrennt variieren. Dies erfordert zuerst eine zusätzliche begründete
Randquantisierung; bloßes Nachintegrieren im bisherigen Hilfsmaß ersetzt sie nicht.

## Reproduktion

Python 3.12 wurde verwendet. Numerik: NumPy 2.3.5, SymPy 1.14.0, mpmath 1.3.0.

```bash
python -m pip install -r requirements.txt
python -B verify.py
```

Der Prüfer kontrolliert das vollständige SHA-256-Manifest, Elternprovenienz,
führt die angegebenen Rechnerskripte in einer isolierten Kopie aus und
vergleicht deren JSON-Ausgaben. Laufzeitmetadaten werden nicht verglichen;
Abhängigkeitshashes werden jeweils gegen die neu erzeugten Quelldateien geprüft.
Exakte algebraische Felder müssen identisch bleiben; Float64-/Dezimalauswertungen
werden mit einer absoluten und relativen Toleranz von je 5e-12 verglichen.
Assertions dürfen nicht über `python -O` deaktiviert sein.

Die Uhrintegrale verwenden n=128 und n=160 pro Achse, alle acht inneren
Dichtestrata und das ursprüngliche normierte Boxmaß. Die exakte Quellen-Nullantwort
beruht auf Algebra. Die Dezimalwerte der vollständigen Gewichte besitzen kein
vollständiges Intervallzertifikat für Rundungsfehler. Es ist kein großer
Community-Rechenlauf nötig.

PDF und Vergleichsabbildung lassen sich mit den zusätzlichen Paketen aus
`report/requirements.txt` durch `python -B report/build_report.py` erzeugen.
Die Report-Erzeugung ist getrennt von der wissenschaftlichen Regression.

## Dateien und Orientierung

- `contracts/boundary_readout_contract.json`: Status und zusätzliche Postulate.
- `agents/canonical_scalar.md`: Randconstraint, Reduktion, Quanten-Normierung.
- `agents/local_detector.md`: Apparat, tatsächliche Zweigzustände, kohärente Auslese.
- `agents/ward_clock.md`: einseitige Quelle, Randflüsse und Hilfspakete.
- `agents/variational_boundary.md`: kanonische Uhr-/Dichterelation.
- `agents/history_measure.md`: nicht eindeutige zulässige Gewichte.
- `agents/independent_audit.md`: unabhängige Rekonstruktion und Reichweite.
- `checks/`: eigenständig ausführbare Rechner und vollständige Ergebnisse.
- `sources/`: eingefrorene Elternverträge und Herkunft mit Hashes.

Die Primärliteratur dient der Einordnung, nicht als Beweis der neuen N11-Rechnung:
[Höhn, 1401.6062](https://arxiv.org/abs/1401.6062),
[Giulini, gr-qc/0003040](https://arxiv.org/abs/gr-qc/0003040),
[Rideout–Sorkin, gr-qc/9904062](https://arxiv.org/abs/gr-qc/9904062).
