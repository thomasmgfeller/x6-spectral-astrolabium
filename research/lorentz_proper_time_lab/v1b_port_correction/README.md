# V1b: Python-Portkorrektur und erhaltener Fehlernachweis

Veröffentlicht am 20.10.2026. **Das Teilgate `corrected_port_matrix` besteht;
V1b insgesamt bleibt `NOT_PASSED`.**

[Vollständiger Bericht](V1b_PORTKORREKTUR.md) ·
[Originaler Ergebnisnachweis](results/port_verification.json) ·
[Publikationsprüfung](PUBLICATION.json) ·
[Erneuter lokaler Lauf](publication_replay/port_verification.json)

Im rekonstruierten alten Python-Port fehlte das äußere XOR der zweiten
PRNG-Mischoperation. `MissingXorRNG` reproduziert die 40 alten PRNG-Werte,
zwölf Zählwerte und den alten 64-Punkt-Fixture-Hash. `RNG` korrigiert diesen
Portierungsfehler. Der JavaScript-Kern wird unverändert vom Commit
`560f717c0e25c957bc58bb9df5ec5ac6ad23cad0` mitgeliefert.

Die erneute lokale Ausführung bestätigt sämtliche dokumentierten Ergebnisse:
40.000 PRNG-Werte exakt gleich; 4.000 Normalwerte mit maximaler absoluter
Abweichung 4,44·10⁻¹⁶; 196.608 Punkte mit maximalem Koordinatenfehler
1,67·10⁻¹⁶. Alle Zugehörigkeitsflags und zwölf Zählungen stimmen überein.
Die numerische Toleranz bleibt 10⁻¹² + 10⁻¹²·|Referenz|.

| Gate | Status |
| --- | --- |
| Herkunft der alten Ergebnisse | Fehlende-XOR-Variante reproduziert |
| Äquivalenz des alten Ports | FAIL |
| Korrigierter Port, deklarierte Matrix | PASS |
| Strikter innerer Support des nativen Samplers | FAIL_KNOWN_ZERO_INPUT |
| V1b-spezifischer Browser-/Export-Freeze | OPEN |
| V1b insgesamt | NOT_PASSED |

Seed `2463401483` erzeugt weiterhin zuerst U=0 und damit den Randpunkt
(-0,5,0,…,0). Die Forderung `abs(t)+norm(x)<0.5` scheitert.
Die Veröffentlichung repariert den nativen Sampler nicht. Ein grüner
Softwarejob für den Port ist keine Gesamtfreigabe für V1b.

## Reproduktion ohne Überschreiben der Originaldaten

Im Repository-Stamm, mit Node.js 24 und Python 3.12, ohne Zusatzpakete:

```sh
cd research/lorentz_proper_time_lab/v1b_port_correction
sha256sum -c SHA256SUMS
replay_dir="$(mktemp -d)"
node native_reference.cjs "$replay_dir/native_reference.json.gz"
python3 verify_port.py "$replay_dir"
```

`verify_port.py` ohne `-O` ausführen: Seine historischen Fixture- und
Herkunftsprüfungen verwenden Python-Assertions. Der Exitcode prüft das
Teilgate; den Gesamtstatus enthält `gates.overall_V1b`.
Die strenge alte Fixture-Prüfung kann andere Laufzeiten ablehnen.
Plattformübergreifende Bytegleichheit wird nicht zugesichert; auch die
korrigierten Python- und JavaScript-Fixtures sind nicht byteidentisch.

## Erhalt der Evidenz

Alle 16 Dateien des freigegebenen Pakets sind unverändert enthalten.
`SHA256SUMS` prüft seine 15 übrigen Dateien. Die ursprünglichen `results/`
wurden nicht mit dem neuen Lauf überschrieben. `PUBLICATION.json` bindet
das ursprüngliche ZIP über SHA-256 und dokumentiert den erneuten Vergleich.
Das Zusatzverzeichnis `publication_replay/` enthält dessen datierten Bericht.
Die laufende Repository-Quelleninventur erfasst auch diese Ergänzungen.

Der ursprüngliche Bericht beschreibt den Stand vor Veröffentlichung;
sein Schlusssatz zum damaligen Publikationsstatus ist historisch zu lesen.
Die dort erwähnte frühere native radiale Diagnostik wurde hier nicht erneut
ausgeführt. Es gibt keine neue statistische Freigabe und keine unabhängige
externe Replikation. Der nächste V1b-Schritt bleibt die explizite Behandlung
endlicher Randwerte mit anschließendem nativen Browser- und Exporttest.

English: The missing outer XOR in the reconstructed Python port is corrected.
The frozen finite comparison matrix passes. The original sampler's boundary
defect remains, and overall V1b qualification has not passed. Original evidence
is preserved byte for byte; the publication replay is recorded separately.
