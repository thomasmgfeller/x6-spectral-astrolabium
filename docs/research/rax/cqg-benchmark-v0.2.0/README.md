# RAX-CQG Causal-Set Benchmark 0.2.0

**16. Oktober 2026 · Forschungssoftware-Prototyp · endliche Referenzprüfungen**

Diese Veröffentlichung stellt die reparierte, freigegebene Fassung als nachvollziehbares Rechenwerkzeug bereit. Sie ergänzt die [Forschungsarchitektur v0.1](../cqg-v0.1/README.md). Ihre Prüfungen sind keine Ausführung der gesamten dort geplanten CQG-01–08-Kampagne und keine Bestätigung einer Quantengravitationstheorie.

## Öffnen, herunterladen, prüfen

- [Causal-Set-Labor im Browser öffnen](../../../../app/rax-cqg-lab.html)
- [Vollständiges freigegebenes Paket als ZIP](RAX_CQG_Benchmark_v0_2_0.zip)
- [Quellcode und Reproduktionsanleitung](../../../../research/rax_cqg/benchmark-v0.2.0/README.md)
- [Mathematische Definitionen und Primärliteratur](../../../../research/rax_cqg/benchmark-v0.2.0/MODEL_CONTRACT.md)
- [Prüfbericht des freigegebenen Pakets](../../../../research/rax_cqg/benchmark-v0.2.0/VALIDATION.json)
- [Aussagenregister und offene Nachweise](../../../../research/rax_cqg/benchmark-v0.2.0/CLAIMS.json)
- [Dateiprüfsummen und Publikationsumfang](PUBLICATION.json)

Das ZIP und alle 28 daraus entpackten Dateien werden bytegleich veröffentlicht. Die Browserdatei ist ebenfalls bytegleich. Der enthaltene Bericht und der Satz, das Paket sei noch nicht hochgeladen, beschreiben den eingefrorenen Stand vor dieser Veröffentlichung. Aktuelle Publikationsprüfungen sind separat im [GitHub-Workflow](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/workflows/rax-cqg-benchmark.yml) nachvollziehbar.

## Was ist implementiert?

Korrekte transitive Ordnungen, sechs explizite Generatoren, offene Intervalle, die dimensionslose 4D-BDG-Kombination, tatsächliche Graphspektren, Bernoulli-Ausdünnung und JSON-Import/Export. Hinzu kommen ein stabiles **klassisches** Gaußfeld auf dem Vergleichbarkeitsgraphen und eine separat vorausgesetzte periodische Zweiqubit-Uhr.

Der gespeicherte interne Prüflauf umfasst 28 Python-Testmethoden, darunter alle 1.024 oberen DAGs auf fünf festen Labels, 28 Python/JavaScript-Vergleichsfälle, 16 UI-Logikprüfungen und die Wiederholung sämtlicher 240 Pilotläufe in 30 Gruppen. Die UI-Logikprüfungen liefen in Node; sie waren keine visuelle Browserprüfung. Der zusätzliche Publikationsworkflow prüft Dateigleichheit, wiederholt die Rechenprüfungen in einer temporären Kopie und enthält einen begrenzten Chromium-Smoke-Test für Bedienung, Export und zwei Ansichtsbreiten. Sein tatsächlicher Ausführungsstatus ist dem jeweiligen CI-Lauf zu entnehmen.

## Reproduktion

Aus einem Checkout dieses Repositorys, mit Python 3.12 und Node.js 24:

```sh
python3 tests/rax-cqg/verify_publication.py
cd research/rax_cqg/benchmark-v0.2.0
python3 -m venv .venv
# Die virtuelle Umgebung mit dem zur eigenen Shell passenden Befehl aktivieren.
python3 -m pip install -r requirements.txt
python3 validate.py
```

`validate.py` schreibt einen neuen lokalen Bericht und neue Logs. Der gespeicherte Originalbericht bleibt über den Git-Commit und das ZIP zugänglich. Für eine Veröffentlichung oder externe Gegenprüfung immer Commit, Laufzeitversionen und neu erzeugten Bericht angeben.

## Wissenschaftliche Grenze

Der Wachstumsindex ist keine kalibrierte physikalische Zeit. Die Zweiqubit-Uhr setzt Quantenmechanik voraus und ist nicht an den Poset-Generator gekoppelt. Nichtkommutativität klassischer Operationen ist kein Quantenbeleg. Nichtkommutatives QSG samt Kausalität/Kovarianz, KR-Unterdrückung, Hauptvermutung und Kontinuumsgrenze bleiben offen. Die ursprünglichen nicht lesbaren Gmail-Formelbilder wurden nicht als geprüfte Gleichungen übernommen.

Der praktische wissenschaftliche Nutzen liegt in offen nachrechenbaren Definitionen, endlichen Referenzen, Rohdaten und überprüfbaren Gegenbeispielen. Neuheit, physikalische Gültigkeit und personell unabhängige Replikation sind nicht nachgewiesen.

Originale Projektbeiträge: [Apache-2.0](../../../../LICENSE). Der PCG-Hinweis im Paket bleibt erhalten. Die frühere Architektur und vorhandene historische Evidenz werden nicht überschrieben.


## Abhängigkeitsprüfung vom 16.10.2026

Die [H7-Abhängigkeitsprüfung](../../../../research/lorentz_h7_dependency_audit/README.md) bestätigt an sechs bekannten Gegenbeispielmatrizen, dass die unveränderten Python- und JavaScript-Kerne volle Relationen behalten. Die Widerlegung von H7 erfordert hier keinen Rechenstopp. Spektren bleiben Diagnostik; eindeutige Rekonstruktion folgt daraus nicht. Das freigegebene ZIP und seine 28 Quelldateien bleiben unverändert.
