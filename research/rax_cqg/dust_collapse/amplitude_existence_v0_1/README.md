# CST-DUST: Amplitudenexistenz v0.1

Schritt 3 schließt die Staubintegration und die Entfernung des inneren Skalar-Abel-Regulators für die **festgelegte endliche AA-Kontrollfamilie**. Es gibt eine explizite integrierbare Majorante, eine lineare Regulatorfehlerschranke und Gegenbeispiele gegen die bloß punktweise Anwendung des Nullraumkriteriums.

Die Staubboxen bleiben fest. Die physikalische CST-Amplitude, Historiengewichte und ein Kontinuumsgrenzwert sind nicht hergeleitet. Alle physikalischen Gates bleiben HOLD.

## Lesen

- `CST_DUST_Amplitudenexistenz_v0_1.pdf`: gesetzter Ergebnisbericht.
- `DERIVATION.md`: vollständige Definition, Beweise, Erweiterungssatz und Divergenzbeispiele.
- `existence_contract.json`: maschinenlesbarer Geltungsbereich.
- `results/existence_certificate.json`: 33 Blockzertifikate, Schranken und Gegenbeispiele.
- `provenance.json` und `inputs/`: eingefrorener Anschluss an PR #278–280.

## Offline prüfen

Mit Python 3.10+ und SymPy 1.14.0:

```sh
python verify.py
```

Der Prüfer verändert keine Referenzdaten. Er verlangt 22 bestandene Tests, vollständige Hashdeckung, unveränderte Herkunfts-Blobs und bytegleichen Ergebnis-Replay. Ein ZIP bitte **außerhalb** des entpackten Paketordners belassen; die Datei-Inventur ist absichtlich strikt.

## Ergebnisse und Bericht neu bauen

```sh
python existence.py
python make_report.py
python package.py
python verify.py
```

`package.py` ist ein bewusster Release-Bauer: er erneuert das Manifest und schreibt das ZIP in den übergeordneten Ordner. Er darf nicht anstelle des Integritätsprüfers auf ein fremdes Paket angewendet werden. Für den PDF-Bau zusätzlich ReportLab, Matplotlib und Pillow gemäß `environment.json` installieren. Das Ergebnis-JSON enthält keine numerisch berechnete physikalische Übergangsmatrix.

Lizenz: Apache-2.0. Herkunftsnachweis: `NOTICE` und `provenance.json`.
