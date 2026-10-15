# Abnahme der Restpaaranalyse und der erweiterten Offline-Suite

15. Oktober 2026: **PASS** für die Implementierung
[`5eaffee5a594e2c2c5b86db28a1406dc29168087`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/5eaffee5a594e2c2c5b86db28a1406dc29168087).
Die nachfolgenden Evidenz- und Registercommits ändern weder die mathematischen
Prüfer noch das `REFERENCE_SOURCE_MANIFEST.json` dieser Implementierung.

| Prüfung | Ergebnis | Beleg |
| --- | --- | --- |
| Vier Restpaare und zwei Grenzfälle | 4/4 Primärpaare getrennt; n=7/n=8-Gegenbeispiele bestätigt | [Vollständige lokale Rechnung](evidence/local-results.json), [Wolfram-Ergebnis](evidence/wolfram-result.json) |
| Frischer sauberer Checkout ohne Site-Pakete | Neun Berichte; 26 übergreifende plus 17 Lorentz-Kontrollen | [Lokale Abnahme](evidence/fresh-checkout/acceptance.json), [CLI-Meldung](evidence/fresh-checkout/01-qualify.log) |
| Zehn zusätzliche Zurückweisungen über die gemeinsame CLI | Alle mit erwartetem Exit 1; insgesamt elf CLI-Schritte | Lokale Abnahme und sämtliche Logs unter `evidence/fresh-checkout/` |
| Zusätzliche Lorentz-CLI-Proben unter Python `-O` | Fehlendes Primärpaar und fälschlich als isomorph bezeichnetes n=8-Paar abgelehnt | [Fokussierte CLI-Abnahme](evidence/focused-cli-checks.json) |
| CI mit erzwungen getrenntem Netzwerk-Namespace | PASS, `network_namespace_isolated=true` | [CI-Abnahme](evidence/ci/acceptance.json), [Workflowbeleg](evidence/ci/workflow.json), [Lauf 38730788083](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/38730788083) |

Lokal: Python 3.12.14, Node 24.19.0. CI: Python 3.12.15, Node 24.21.0, Ubuntu 24.04.
GitHub prüfte den temporären Merge-Commit
`ecc85042e0cf18c57854bac96e261d688503659b` mit dem oben genannten PR-Head.
Beide Läufe erzeugten dieselbe vollständige Bundle-Prüfsumme:

`7ceef64b76c508229139b36ec2b883fb54b7e6cc9602e5dc3f2d92e402d69d4c`

Das lokale vollständige Bundle ist dauerhaft versioniert, einschließlich aller
neun Berichte und der Quellenbindungen. Mit unverändertem Quellenmanifest:

```sh
python3 -S -B x6.py reference verify research/lorentz_n6_residuals/evidence/fresh-checkout/run
```

Nach späteren Quelländerungen die oben genannte Implementierungsrevision
verwenden und das gespeicherte Bundle aus dieser Evidenzrevision bereitstellen.
Die historische Acht-Berichte-Abnahme unter `docs/reference-suite/` bleibt ihrem
früheren Quellencommit zugeordnet.

Der CI-Bericht wurde als vollständiger JSON-Block aus dem abgeschlossenen
Jobprotokoll extrahiert; nur Zeitstempel-Präfixe wurden entfernt. Das zusätzliche
GitHub-Artefakt bleibt 30 Tage verfügbar. Der lokale Bericht behauptet keine
erzwungene Netzwerktrennung; diese ist separat durch den CI-Lauf belegt.

Die [wissenschaftliche Anleitung](README.md) enthält Hypothese, Gültigkeitsgrenzen,
Literaturabgrenzung und die drei gespeicherten Wolfram-Versuche. Die zwei tatsächlich
fehlgeschlagenen Versuche werden bei jedem Replay weiterhin abgelehnt. Diese
Softwareabnahme ersetzt keine externe Begutachtung oder physische Validierung.
