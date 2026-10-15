# Ausgeführte Abnahme der Offline-Referenzsuite

**15. Oktober 2026 · PASS.** Geprüfte Implementierung:
[`7c35b591f77ab1c123ee9795ea6978d1681d59bb`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/7c35b591f77ab1c123ee9795ea6978d1681d59bb).
Die nachfolgenden Evidenz- und Registercommits ändern diese Prüfer und ihre
Quellenbindungen nicht. Die [Anleitung](../OFFLINE_REFERENCE.md) beschreibt den
einzigen gemeinsamen Einstieg und die Grenzen jedes Falls.

| Abnahme | Ergebnis | Beleg |
| --- | --- | --- |
| Sauberer neuer Checkout ohne `.venv` und Python-Site-Pakete | PASS; 8 Berichte, 26 interne Fehlerkontrollen | [Lokaler Bericht](local/acceptance.json), [CLI-Ausgabe](local/01-qualify.log) |
| Öffentliche CLI gegen falsche und unvollständige Ausgaben | 10 erwartete Zurückweisungen mit Exit 1; darunter zwei Fälschungen mit neu berechneten Prüfsummen | Elf Schritte im lokalen Bericht und zugehörige Logs |
| Zweiter vollständiger Rechenlauf | PASS_OFFLINE_REFERENCE_REPLAY | [Vollständiges Bundle](local/run/complete.json), alle acht Berichte in `local/run/reports/` |
| CI im getrennten Netzwerk-Namespace | PASS; `network_namespace_isolated: true`, Site-Pakete deaktiviert | [CI-Abnahme](ci/acceptance.json), [beobachteter Workflow](ci/workflow.json), [GitHub-Lauf](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/38720405798) |

Lokal liefen Python **3.12.14** und Node **24.19.0**. Die GitHub-Abnahme verwendete
Python **3.12.15** und Node **24.21.0** auf Ubuntu 24.04 x86-64. GitHub prüfte den
temporären PR-Merge-Checkout `3196bc85f73f32ba6e1ca7347294b08acf88006a` mit
PR-Head `7c35b591f77ab1c123ee9795ea6978d1681d59bb`; beide sind im CI-Beleg getrennt
ausgewiesen. Der lokale und der CI-Lauf erzeugten dieselbe SHA-256-Prüfsumme
für `complete.json`:

`6c6f28f42a0b61120180db3cb8de90decb13bc1068cd089494ff6d5e5f051599`

Das bindet dieselben vollständigen Berichtsinventare und Quellen. Die
Versionsangaben in der informativen CLI-Meldung unterscheiden sich erwartungsgemäß.
Dieser konkrete Vergleich qualifiziert nicht beliebige weitere Runtime-Versionen.

Die CI-Abnahme wurde als JSON-Block aus dem abgeschlossenen GitHub-Jobprotokoll
übernommen; ausschließlich die Zeitstempel-Präfixe wurden entfernt. Die kompletten
CI-Bundles und Logs liegen zusätzlich im Workflow-Artefakt
`x6-offline-reference-evidence` (30 Tage Aufbewahrung). Das lokale Bundle und seine
Logs sind hier dauerhaft versioniert. Der lokale Host erlaubte keinen eigenen
Netzwerk-Namespace; deshalb weist sein Bericht diesen Wert korrekt als `false`
aus. Die erzwungene Netzwerktrennung ist separat durch den erfolgreichen CI-Lauf
belegt.

Aus einem Checkout mit unverändertem `REFERENCE_SOURCE_MANIFEST.json`:

```sh
python3 -S -B x6.py reference verify docs/reference-suite/local/run
```

Bei späteren Quelländerungen kann dieses historische Bundle absichtlich an der
Quellenbindung scheitern. Dann den oben genannten Commit verwenden und das Bundle
aus der neueren Evidenzrevision als Eingabe bereitstellen. Die Suite bewertet
endliche Rechnungen und Ablehnungsregeln; sie bestätigt keine physische Messung,
keine Urheberschaft und keine externe Begutachtung.
