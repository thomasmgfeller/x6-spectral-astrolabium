# CST-DUST: kanonische Randrelation und lokale Reduktion v0.1

Aus der vorhandenen Wirkung folgt im positiven inneren Dichtesektor eine
vierdimensionale lagrangesche Randrelation über einer explizit parametrisierten
zweidimensionalen Momentfläche. Die zusätzliche lokale Dirac-Reduktion ist
mathematisch konsistent, legt aber weder eine physikalische Präparation noch
einen Hamiltonian fest. Der frühere nichtverschwindende Kommutator bleibt
im dort geprüften Operatoransatz richtig. Formale vollständige
Gradienten-Graphoperatoren kommutieren; das allein ist keine physikalische
CST-Constraintalgebra.

Der Dichte-Atomzweig bleibt getrennt und erlaubt mehr Randdaten als der
positive stationäre Zweig. Der exakte Maßtransport bewahrt die Atommasse
und positiven Momente; ein endliches Dichteintegral wird keine Delta-Projektion.

**Alle acht physikalischen Gates bleiben HOLD.** Kein Bounce-Nachweis,
kein physikalischer Außenraum, kein n=5-Produktionslauf, keine kostenpflichtige
Rechnung. Keine externe Replikation.

Basis: Main nach [PR 267](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/267),
`a373f318e4a99bf1e2496f4d5bc674da6f6ea59c`. 8. November 2026 (Zürich).

## Unterlagen

- `CST_DUST_Kanonische_Randrelation_Reduktion_v0_1.pdf`: sechsseitiger Bericht.
- `DERIVATION.md`: vollständige Formeln, Beweise, Domänen und Grenzen.
- `canonical_contract.json`: maschinenlesbarer Status.
- `inputs/`, `provenance.json`: vier unveränderte Projektquellen, dazu die Lizenz.

## Nachrechnen

Python 3, nur Standardbibliothek für die wissenschaftlichen Prüfungen:

```sh
python3 -O -B verify_package.py
python3 -O -B replay.py
```

`analyze.py` erzeugt drei deterministische Ergebnisdateien. `replay.py`
vergleicht sie bytegenau in einem isolierten Verzeichnis. `package.py`
erzeugt das deterministische ZIP. Nur die optionale PDF-Neuerstellung mit
`build_report.py` benötigt ReportLab und DejaVu-Schriften.

Kontrollen: 36 symbolisch verschwindende Graphklammern, vier nichtverschwindende
naive Klammern samt vollständiger Aufhebung durch den ergänzten Impuls,
15 rationale Flächen-/Coarea-Fälle, 135 stationäre Reaktionsfälle,
45 Kotangentialtransporte, vier Dirac-Umdefinitionen, fünf positive
Dichtemomente und acht Negativkontrollen. Der Kontrollplan wurde nach
analytischem Entwurf vor Ausführung gehasht; keine externe Präregistrierung.

Nächster konkreter Test: einen zweiten Rand-/Außenblock aus derselben
Materiewirkung koppeln und gemeinsame Impulsbilanz sowie alle neuen oder
umklassifizierten Kausalintervalle prüfen. Die vorliegende Relation ist
noch kein solcher Außenblock und kein physikalisches Junction-Gesetz.
