# Gemeinsame Offline-Referenzsuite

Die Suite verbindet die vorhandenen rationalen Graphprüfungen, vier eingefrorene
Wolfram-Pakete, den aktuellen Signal-Lab-Kern und den unabhängigen n=6-Prüfer. Hinzu kommt die gezielte Analyse der vier
n=6-Restkollisionen mit eingefrorener neuer Wolfram-Gegenprüfung.
Sie rechnet gespeicherte Ergebnisse lokal nach. Es gibt keine neuen Wolfram-Aufrufe,
keine Paketinstallation und keinen Download während der Prüfung.

## Ein Ablauf aus einem frischen Checkout

Voraussetzungen: **Linux/POSIX x86-64, Python 3.12 und Node.js 24** bereits auf dem
Rechner. Git wird nur zum Beziehen des Checkouts und für die zusätzliche
Checkout-Abnahme benötigt. Die Suite selbst braucht nur Python-Standardbibliothek
und Node. `setup`, NumPy, SciPy, Browser und Wolfram-Zugang sind nicht erforderlich.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-reference
cd x6-reference
python3 -S -B x6.py reference qualify --output /tmp/x6-reference-evidence
```

Nach dem Klonen kann das Netzwerk getrennt werden. Für denselben Quellenstand
den vollständigen Commit aus dem [Modulregister](MODULE_REGISTRY.md) auschecken.
Der Zielordner muss neu sein. `-S` deaktiviert Python-Site-Pakete;
die Checkout-Abnahme verlangt zusätzlich, dass keine `.venv` existiert.
Die Laufzeit hängt vom Rechner ab; die Checkout-Abnahme wiederholt die Suite mehrfach.

Erwartete Abschlussmeldung und Exitcode **0**:

```json
{
  "status": "PASS_OFFLINE_REFERENCE_REPLAY",
  "cases": 10,
  "negative_controls": 27
}
```

Die tatsächliche Meldung enthält zusätzlich Geltungsbereich und Runtime-Versionen.
`qualify` führt einen vollständigen Lauf aus, schreibt die Ergebnisse und prüft
diese durch einen erneuten Lauf derselben Prüfer. Ein Fehler beendet
den Befehl mit Exitcode **1** und `FAIL`; falsche CLI-Argumente haben Exitcode **2**.
Ein erwartetes fachliches `FAIL` innerhalb eines Referenzfalls ist kein Suitefehler.

## Was genau geprüft wird

| Bericht in `reports/` | Lokal ausgeführte Prüfung | Erwartung und Grenze |
| --- | --- | --- |
| `rational-graphs.json` | Bestehender `tests/python/independent_audit.py`, unverändert in temporärer Kopie; rationale Schur-Elimination | 5/5: Pfad, Dreieck, gewichtete Kante, gerundeter Signalpfad, unzusammenhängender Graph. Ungültige/strikte Grenzschranken werden abgelehnt. Keine Aussage über beliebige Signal-zu-Graph-Modelle. |
| `causal-n6.json` | Bytegleicher unabhängiger Prüfer und Atlas in `references/causal-order-n6/` | 318 nichtisomorphe Ordnungen, 4.824 natürlich beschriftete Ordnungen, 4.208 exakte Polynome. Klassen 286/314/285/318; offene Paare 37/4/33/0 für drei Spektren, Endpunkte, Quill-Basis und maximale Quills. Vollständige Kollisionslisten werden nachgerechnet. Endliche n=6-Aussage, kein allgemeiner Eindeutigkeitssatz. |
| `rax-w1.json` | Archiv `RAX_W1_Exakte_Gegenpruefung_v0_1_Paket.zip`: `verify_package.py` und `verify.py --output …` | Vollständiges Paketinventar; 44 Matrizen, 10 lumpable / 34 nicht lumpable, 20 Potenzprüfungen, 10 Verschiebekontrollen, 2 ungültige Matrizen. Alle 44 Detailzeilen und 10 Kontrollen werden gespeichert. Nur 44/160 veröffentlichte Matrizen; kein statistischer Erwerbs-Replay. |
| `wolfram-polarity.json` | Fall-2-Archiv: `verify.py --rerun`, einschließlich des archivierten Node-Kerns | 4 symbolische und 12 Metrikprüfungen; Identität PASS, Inversion und Nullsignal FAIL. Der anfänglich fehlgeschlagene Wolfram-Versuch bleibt nachgewiesen. |
| `current-polarity.json` | `tools/reference_current.cjs` mit **aktuellem** `app/signal-lab-core.js`, verglichen durch den archivierten Fall-2-Prüfer | Dieselben 12 Metriken, Masken, Undefined-Semantik und 33 Spektralbins innerhalb des eingefrorenen Vertrags. Vollständige neue Eingaben und Ergebnisse im Bericht. So erfasst die CI auch spätere Kernänderungen. |
| `wolfram-dependence.json` | Fall-4-Archiv: `verify.py` | 12 Wolfram-Prüfungen, 7 lokale Gegenrechnungen, exakte Wurzeleinschließung und 60-Dezimalstellen-Toleranz; ursprüngliches INCONCLUSIVE bleibt sichtbar. Konstruiertes Abhängigkeitsbeispiel, keine Prüfung echter Projektdaten. |
| `wolfram-causal3.json` | Fall-5-Archiv: `verify_release.py` | 16/16 Wolfram/Python, 6 charakteristische Polynome, 6 Permutationen. Isospektrale, nicht ordnungserhaltend isomorphe Dreierordnungen; ursprünglicher Vorzeichenfehler bleibt dokumentiert. |
| `lorentz-residuals.json` | [Restpaar-Prüfer](../research/lorentz_n6_residuals/README.md): 36 gespeicherte Wolfram-Polynome unabhängig gegenrechnen, alle n=6-Observablen und Höhe-zwei-n=7-Enumeration | Vier Paare getrennt; 17 zusätzliche interne Fehlerkontrollen. Zukunftsseparator scheitert bei n=7, volle Gradpaare plus Spektren bei einem verbundenen n=8-Dualpaar. Hypothese für beide Zählgrößen bei n=7/Höhe ≥3 offen. |
| `qe-graphs.json` | [X6-QE](../research/x6_qe/README.md): vier Graphen, drei bekannte Referenzen, exakte Adjazenz- und Ihara-Polynome mit unabhängigen Determinantenidentitäten | Stern ohne Zyklusfingerprint, primitiver Viererzyklus, Turmgraph/Shrikhande mit gleichem Spektrum und Zeta, aber K4=8/0. Zwölf Umbenennungen, 21 zusätzliche Fehlerkontrollen. Keine Quanten-, Gedächtnis- oder Arithmetikbehauptung. |
| `failure-controls.json` | 13 fachliche Mutationen plus 14 beschädigte/manipulierte Ausgaben | Alle 27 müssen abgelehnt werden. Akzeptiert ein Prüfer eine davon, scheitert die gesamte Suite. |

Die bisherigen 26 übergreifenden Fehlerkontrollen bleiben bestehen; ein neu gehashter
falscher QE-Motivbefund ergänzt sie auf 27. Zusätzlich enthalten die Berichte
`lorentz-residuals.json` 17 und `qe-graphs.json` 21 interne Fehlerkontrollen.
Die vier Original-ZIPs bleiben unverändert. Ihre Pfade und SHA-256-Werte stehen
in [REFERENCE_SOURCE_MANIFEST.json](../REFERENCE_SOURCE_MANIFEST.json).
Für n=6 dokumentiert [PROVENANCE.json](../references/causal-order-n6/PROVENANCE.json)
den ursprünglichen Branch, Commit und jedes kopierte Byteinventar. Übernommen sind
Prüfer, fester Atlas und historische Evidenz; der Atlasgenerator und die übrigen
Forschungsmodule des Branches bleiben dort. `ORIGINAL_README.md` beschreibt den
ursprünglichen Branch; dessen relative Generatorpfade sind keine neuen Suite-Einstiege.

## Gespeicherte Ausgabe prüfen

```sh
python3 -S -B x6.py reference verify /tmp/x6-reference-evidence
```

Der Ordner enthält genau **zehn Berichte und `complete.json`**. Letztere bindet
die vollständige Fallliste, alle Berichtslängen und SHA-256-Werte, den Geltungsbereich
und die Quellen. Sie wird erst nach erfolgreichen Rechnungen und Fehlerkontrollen
als letzte Datei geschrieben. Fehlende, zusätzliche, verlinkte, gekürzte oder
nichtkanonische Dateien, doppelte JSON-Schlüssel und nichtendliche Zahlen scheitern.

Die Prüfsummen sind nur die erste Stufe. `verify` erzeugt aus dem **vertrauenswürdigen
Checkout** alle Berichte neu und vergleicht deren vollständige kanonische Bytes.
Es führt keinen Code aus dem Ergebnisordner aus. Insbesondere reichen nachgezogene
Prüfsummen für eine falsche Graphschranke, eine entfernte Wolfram-Zeile, eine falsche
n=6-Anzahl oder eine erfundene PASS-Zusammenfassung nicht aus. Diese Angriffe sind
Teil jeder Ausführung; Graphschranke, Wolfram-Zeile und QE-Motivzahl werden zusätzlich über die öffentliche CLI
geprüft.

Die ursprünglichen fachlichen Toleranzen gelten beim Wolfram-Vergleich; Replay
fügt **keine zusätzliche Toleranz** hinzu. Lokale Python-/Node-Versionen werden nur
in der CLI-Meldung geführt; ausschließlich `local_python`, `python_version` und
`fresh_node` werden aus den betreffenden Archivberichten entfernt. Gespeicherte
Wolfram-Versionen, fachliche Werte und Einschränkungen bleiben enthalten.
Ein anderer Node-Patchstand oder eine andere Architektur kann letzte Gleitkommabits
ändern und damit einen alten Bericht beim strengen Replay ablehnen. Dann beide
Läufe mit derselben Runtime wiederholen; keine Resultate stillschweigend angleichen.

Die Vertrauenswurzel ist der überprüfte Checkout einschließlich Quellenmanifest.
Wer Prüfer und Quellenmanifest gemeinsam ändern kann, kann auch andere Regeln
definieren. Hashes und Replay beweisen weder Urheberschaft noch einen vergangenen
Ausführungszeitpunkt. Ein mathematisch identisches, neu erzeugtes Ergebnis ist
absichtlich gültig. Die Suite ist keine externe Begutachtung oder physische Abnahme.

## Frischen Checkout und Fehlereingaben abnehmen

```sh
python3 -S -B tests/reference/qualify_checkout.py --output /tmp/x6-reference-acceptance
```

Dieser zusätzliche Einstieg verlangt einen sauberen Git-Checkout ohne `.venv`,
ruft den dokumentierten CLI-Ablauf auf und prüft elf weitere Zurückweisungen:
Überschreiben, Python `-O`, drei neu gehashte Fälschungen (Graphschranke, Wolfram-Zeile, QE-Motivzahl), fehlender Fall,
doppelter JSON-Schlüssel, Symlink, veränderter aktueller Kern, beschädigtes
Wolfram-Archiv und fehlendes Node. Das sind **elf** Zurückweisungen plus der
erfolgreiche Qualifikationslauf, insgesamt zwölf protokollierte CLI-Schritte.
Er prüft außerdem, dass der Checkout unverändert bleibt. Das wiederprüfbare Bundle
liegt unter `run/`; `acceptance.json` und die Logs dokumentieren den Testlauf.

Die GitHub-Action **X6 Offline Reference Suite** läuft bei relevanten Pull Requests,
Pushes nach `main` und manuell. Nach Bereitstellung von Checkout, Python und Node
führt sie genau diese Abnahme mit `unshare --net` aus: ein eigener Netzwerk-Namespace
ohne Netzwerkanbindung, Python zusätzlich mit `-S`. Diese Bedingung wird mit
`--require-network-isolation` geprüft. Die Artefakte enthalten alle Ergebnisse
und Ablehnungsprotokolle. Ein normaler lokaler Lauf braucht keine
Namespace-Berechtigung und behauptet diese Isolation nicht.

## Änderungen pflegen

Relevante Prüfer, Archive, n=6-Quellen und Signal-Lab-Kern sind im Quellenmanifest
explizit gebunden. Nach einer beabsichtigten Änderung zuerst die wissenschaftlichen
Erwartungen und Fehlerfälle prüfen, dann die betroffenen Hashes bewusst aktualisieren:

```sh
python3 -B - <<'PY'
import hashlib, json
from pathlib import Path
p = Path('REFERENCE_SOURCE_MANIFEST.json')
d = json.loads(p.read_text())
d['files'] = {name: hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in d['files']}
p.write_text(json.dumps(d, indent=2) + '\n')
PY
```

Bei neuen Quellen auch die vollständige Dateiliste und CI-Pfadfilter ergänzen.
Anschließend die Repository-Inventare nach deren bestehenden Regeln aktualisieren,
frischen Checkout qualifizieren und Evidenz samt geprüfter Revision im Modulregister
nachführen. Automatisches Akzeptieren neuer Referenzwerte ist nicht vorgesehen.

Der [gespeicherte Abnahmebeleg](reference-suite/README.md) nennt den tatsächlich
geprüften Commit, den lokalen Lauf und den Netzwerk-isolierten CI-Lauf.

Die ursprüngliche Acht-Berichte-Abnahme unter `docs/reference-suite/` bleibt
historische Evidenz ihres dort genannten Commits. Die aktuelle Erweiterung und
ihre unveränderten Wolfram-Rohantworten stehen unter
[research/lorentz_n6_residuals/](../research/lorentz_n6_residuals/README.md).
Alte Bundles werden auf der zugehörigen alten Quellenrevision wiederholt,
nicht gegen das inzwischen erweiterte Zehn-Berichte-Inventar.

Die Zehn-Berichte-Erweiterung ist unter [X6-QE/Abnahme](../research/x6_qe/ACCEPTANCE.md)
dokumentiert. Frühere Acht-/Neun-Berichte-Bundles bleiben an ihre alten Quellenrevisionen gebunden.
