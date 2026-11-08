# CST-DUST: Zulässige Randdaten und Störungsgrenzen v0.1

Die Zweiblock-Lösung aus PR 269 ist innerhalb der festen Sechserkette mit
vier geordneten äußeren Uhren und zwei freien positiven Materiezeilen
vollständig klassifiziert. Notwendig und hinreichend sind zwei Gleichheiten
E=F=0 und die beiden strikten Ungleichungen t_*>d, P<0.

Die zulässigen äußeren Daten bilden eine glatte zweidimensionale Fläche.
Sie lassen sich durch eine Form und eine gemeinsame Uhrverschiebung
parametrisieren. Zwei positive Dichtegewichte bleiben frei. Die äußere
Reaktion ist explizit bestimmt und verschwindet nicht.

Unabhängige Randstörungen können die Fläche verlassen. Dann hilft auch
eine Neuwahl sämtlicher innerer Variablen nicht. Eine gemeinsame Verschiebung
und andere korrelierte Änderungen entlang der Fläche erhalten dagegen
Lösungen. Notwendige Restfehlergrenzen machen diese Prüfung für Rechnungen
mit endlichen Toleranzen nutzbar; sie benötigen einen Dichteboden und eine
Obergrenze für den Zukunftsabstand.

**Alle acht physikalischen Gates bleiben HOLD.** Das ist eine Klassifikation
der erklärten endlichen Kettenklasse, keine physikalische Randpräparation,
kein Vakuum-Außenraum, keine dynamische Stabilitätsaussage und kein Bounce.
Kein n=5-Produktionslauf, keine kostenpflichtige Rechnung.

Basis: [PR 269](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/269),
Main `adb6ea2de0dc56417da3493e8aabf8903981090f`.
Datum: 8. November 2026 (Zürich).

## Unterlagen

- `CST_DUST_Randdaten_Klassifikation_Stoerungsgrenzen_v0_1.pdf`: sechsseitiger Bericht.
- `DERIVATION.md`: vollständige Beweise und Gültigkeitsgrenzen.
- `classification_contract.json`: Annahmen und maschinenlesbare Grenzen.
- `inputs/`, `provenance.json`: unveränderte Quellen aus PR 269.

## Reproduktion

Python 3 und Standardbibliothek genügen:

```sh
python3 -O -B verify_package.py
python3 -O -B replay.py
```

16 symbolische Identitäten, 21 Kragen, 108 stationäre Fälle, 168 unabhängige
Randableitungen, 24 Einzelstörungen, 432 Restfehlerbudgets, 108 gemeinsame
Verschiebungen und sechs Negativkontrollen bestehen exakt. Vier Ergebnisdateien
werden isoliert bytegleich reproduziert. `package.py` erzeugt ein
deterministisches ZIP. Nur die optionale PDF-Neuerstellung benötigt ReportLab
und DejaVu-Schriften.

Der Plan wurde nach analytischem Entwurf vor dem endlichen Kontrolllauf
gehasht; keine externe Präregistrierung oder externe Replikation.

Nächster Schritt: einen kleinen verzweigten Rand-/Zukunftsblock vorab
definieren und seine Randbedingungen sowie vollständige Intervallkopplung
ableiten. Die gefundene Kragenfläche allein begründet keine physikalische
Auswahl der darauf liegenden Randdaten.
