# CST-DUST: Zweiblock-Kopplung und gemeinsame Randreaktion v0.1

Die vorhandene Materiewirkung wird um einen zweiten Zukunftsblock ergänzt.
Überlappende Blöcke schließen durch Inklusion/Exklusion und die vollständigen
Kreuz-/Intervallkorrekturen. Auf einer Kette sind vier gemeinsame Elemente
minimal für eine korrigierungsfreie Verklebung bei beliebigen Felddaten;
diese Zahl gilt nicht für allgemeine Kausalsets.

Der eingefrorene Kragen aus PR 266 lässt keine gemeinsame innere stationäre
Lösung mit einem oder zwei zusätzlichen positiven Zukunftselementen zu.
Ein anderer, ausdrücklich konstruierter äußerer Kragen liefert dagegen eine
exakte Zweielement-Lösungsfamilie. Die getrennten Blockreaktionen sind dabei
nicht null, gleichen sich aber am gemeinsamen Element genau aus.

**Alle acht physikalischen Gates bleiben HOLD.** Der positive Zukunftsblock
ist kein physikalischer Vakuum-Außenraum. Die neuen Randdaten sind nicht
unabhängig physikalisch ausgewählt; äußere Reaktionen bleiben erforderlich.
Kein Bounce-Nachweis, kein n=5-Produktionslauf, keine kostenpflichtige Rechnung.

Basis: Main nach [PR 268](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/268),
`483358692a06cc1f17e12f9e392fad550a7494ca`. 8. November 2026 (Zürich).

## Unterlagen

- `CST_DUST_Zweiblock_Kopplung_Randreaktion_v0_1.pdf`: sechsseitiger Bericht.
- `DERIVATION.md`: vollständige Beweise, Domänen und Gültigkeitsgrenzen.
- `coupling_contract.json`: maschinenlesbare Annahmen und Status.
- `inputs/`, `provenance.json`: vier unveränderte Projektquellen plus Lizenz.

## Reproduktion

Python 3 mit Standardbibliothek genügt:

```sh
python3 -O -B verify_package.py
python3 -O -B replay.py
```

`analyze.py` erzeugt vier Ergebnisdateien. Rationale Arithmetik und der
exakte Zahlkörper Q(sqrt(305)) vermeiden Gleitkommatoleranzen.
`replay.py` reproduziert die Ergebnisse isoliert und bytegleich.
`package.py` baut das deterministische ZIP. Nur die optionale PDF-Neuerstellung
mit `build_report.py` benötigt ReportLab und DejaVu-Schriften.

Kontrollen: 50 natürliche Ordnungen, 3350 Überdeckungen, 6700 Materieidentitäten,
3350 gravitative Identitäten, 26388 Reaktionskomponenten, 95 Kettenüberlappungen,
81 eingefrorene Ein-Zukunfts-Fälle, ein analytischer Zwei-Zukunfts-Ausschluss,
27 exakte neue stationäre Fälle, 108 unabhängige Ableitungen,
432 Hesse-Komponenten und acht Negativkontrollen. Keine externe Replikation.
Plan nach analytischem Entwurf vor den endlichen Kontrollen gehasht;
keine externe Präregistrierung.

Nächster Schritt: die gemeinsam zulässigen Kragendaten klassifizieren und
unabhängige Randstörungen prüfen. Der neue Kragen ist ein Existenzzeuge,
noch keine physikalisch ausgewählte oder robuste Präparation.
