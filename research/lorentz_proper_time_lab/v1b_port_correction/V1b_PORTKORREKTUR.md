# V1b — Ursache geklärt und Python-Port korrigiert

**Die Abweichung stammt vom fehlenden äußeren XOR im Python-Port.** Die rekonstruierte fehlerhafte Variante reproduziert alle 40 eingereichten PRNG-Referenzwerte, alle zwölf Zählwerte und den vollständigen 64-Punkt-Fixture-Hash exakt. Die korrigierte Variante besteht die hier ausgeführte Portprüfung gegen den unveränderten JavaScript-Kern.

Dies ist eine Ergänzung zum nativen Audit vom 20.10.2026. Die zuvor offene Zuordnung der Python-Ergebnisse ist damit auf Ebene der reproduzierten Rechenvorschrift geklärt. Der ursprüngliche temporäre Code und dessen Tool-Protokoll wurden nicht unabhängig eingesehen; Grundlage ist der neu übermittelte Text. Aus dessen Formatierungsverlusten wurden `232`/`231` als `2**32`/`2**31` und `init`/`call` als `__init__`/`__call__` gelesen. Ohne diese Normalisierung wäre der Text kein korrekt aufrufbarer Python-Port. Dass genau diese Rekonstruktion den alten Hash erzeugt, ist zusätzliche Evidenz für diese Lesart.

## 1. Die fehlerhafte Zeile

JavaScript führt aus:

```javascript
x ^= x + Math.imul(x ^ (x >>> 7), 61 | x);
```

Das bedeutet `x = x ^ (x + ...)`, einschließlich JavaScripts 32-Bit-Konversion am bitweisen XOR. Der eingereichte Python-Code hatte nur `x = x + ...` ausgeführt.

Korrigierte Fassung mit expliziter 32-Bit-Reduktion:

```python
mixed = imul(x ^ urshift(x, 7), 61 | x)
x = (x ^ ((x + mixed) & MASK)) & MASK
return ((x ^ urshift(x, 14)) & MASK) / 4294967296
```

Der letzte Rückgabeschritt ist danach gleich. Die `Math.imul`-Nachbildung war unter der obigen Formatierungslesart korrekt; das fehlende äußere XOR verändert bereits die PRNG-Ganzzahlen.

Für Seed 20261017:

| Rechenschritt | Wert |
|---|---:|
| Zustand nach Fortschaltung | 1851826830 |
| x nach erster imul-Operation | 125078561 |
| Zweite imul-Operation | 609831573 |
| Summe vor äußerem XOR | 734910134 |
| Korrektes Ergebnis des äußeren XOR, uint32 | 750344855 |
| Fehlerhafter finaler PRNG-Integer | 734886273 |
| Korrekter finaler PRNG-Integer | 750381170 |

Die ersten Ausgaben sind entsprechend 0.17110404395498335 (alter Port) und 0.17471173079684377 (korrigierter Port und Original-JavaScript).

## 2. Ausgeführte Prüfungen

Die Parameter und Toleranzen wurden in `protocol.json` vor der schichtweisen Vergleichsmatrix festgelegt. Die bereits bekannten ersten Vektoren und der reproduzierte Alt-Hash sind dort ausdrücklich benannt. Es handelt sich um eine gezielte Fehlersuche, nicht um ein blindes statistisches Experiment.

| Prüfung | Umfang | Ergebnis |
|---|---:|---|
| Rekonstruktion alter PRNG-Vektoren | 40 Werte, 4 Seeds | exakt reproduziert |
| Rekonstruktion alter Zählungen | 12 Läufe | exakt reproduziert |
| Rekonstruktion alter Fixture | 64 Punkte, d=4 | SHA-256 exakt reproduziert |
| Korrigierter PRNG gegen natives JS | 40000 Werte, 4 Seeds | exakt gleich |
| Korrigiertes normal() gegen natives JS | 4000 Werte | max. absoluter Fehler 4.4408920985006262e-16 |
| Korrigierte cloud() gegen natives JS | 196608 Punkte, d=2,3,4 | max. Koordinatenfehler 1.6653345369377348e-16 |
| Inside-Flags | 196608 Vergleiche | 0 Abweichungen |
| Zählwerte | 12 Vergleiche | exakt gleich |

Für die Gleitkommarechnungen galt `abs(Python - JS) <= 1e-12 + 1e-12 * abs(JS)`. Alle Vergleiche erfüllten diese Bedingung. PRNG-Werte, Inside-Flags und Zählwerte wurden exakt verglichen. Der Test kann nur die deklarierte Matrix bestätigen, nicht alle Seeds und alle endlichen Rechenpfade.

| d | Seed | Alter Port | Korrigierter Port | Original-JavaScript |
|---:|---:|---:|---:|---:|
| 2 | 0 | 4073 | 4078 | 4078 |
| 2 | 1 | 4125 | 4146 | 4146 |
| 2 | 20261017 | 4158 | 4054 | 4054 |
| 2 | 4294967295 | 4146 | 4082 | 4082 |
| 3 | 0 | 2032 | 1992 | 1992 |
| 3 | 1 | 2041 | 2045 | 2045 |
| 3 | 20261017 | 2011 | 2080 | 2080 |
| 3 | 4294967295 | 2077 | 2143 | 2143 |
| 4 | 0 | 973 | 1104 | 1104 |
| 4 | 1 | 1065 | 995 | 995 |
| 4 | 20261017 | 1033 | 1079 | 1079 |
| 4 | 4294967295 | 1029 | 1067 | 1067 |

## 3. JSON-Hashes und tatsächliche Gleitkommaunterschiede

Für alle hier aufgeführten 64-Punkt-Fixtures ist das Objekt ausdrücklich auf `points` und `inside` beschränkt. Python nutzt `json.dumps(..., separators=(',', ':'), allow_nan=False).encode('utf-8')`; JavaScript nutzt `JSON.stringify()`. Es gibt keinen abschließenden Zeilenumbruch.

- Alter Python-Port: `f1869f9749d3f1f2c8f6c2e9e677a1e657177a6f169dcdf2213ec4e543348781`
- Korrigierter Python-Port: `80c8d5b3e00046dafb59d9b59c447fe8894d2dcfccc7ce7a02fbe499067ca467`
- Original-JavaScript, gleiche Objektfelder: `58d2537e32e365043dcea2422e194f8d21b0e833273968281d5d510082d05297`

Die korrigierten Python- und JavaScript-Bytes sind nicht identisch. In der gesamten Wolkenmatrix unterschieden sich 111558 Koordinatenkomponenten bereits in ihrer binary64-Darstellung; die maximale absolute Differenz steht oben. Somit sind neben möglicher Textformatierung auch tatsächlich minimale Unterschiede der mathematischen Laufzeitfunktionen vorhanden. Das ist innerhalb der gewählten numerischen Portprüfung zulässig, liefert aber keine plattformübergreifende Bitidentität.

Der native Hash aus dem früheren Audit (`3e08353c...`) bezog sich auf das vollständige JavaScript-Rückgabeobjekt einschließlich Inferenzfeldern. Er ist deshalb kein Vergleichshash für das hier vereinheitlichte `points`/`inside`-Objekt.

## 4. Getrennte Gate-Entscheide

```yaml
V1b_OLD_RESULT_PROVENANCE: REPRODUCED_MISSING_XOR_VARIANT
V1b_OLD_PORT_EQUIVALENCE: FAIL
V1b_CORRECTED_PORT_MATRIX: PASS
V1b_NATIVE_STRICT_SUPPORT: FAIL_KNOWN_ZERO_INPUT
V1b_BROWSER_AND_EXPORT_FREEZE: OPEN
V1b_OVERALL: NOT_PASSED
```

Der korrigierte Python-Port übernimmt absichtlich das Verhalten des unveränderten Originalsamplers. Seed 2463401483 liefert weiterhin zuerst U=0 und danach den Punkt (-0.5,0,…,0). Damit scheitert die strikte Bedingung `abs(t)+norm(x)<0.5` weiterhin in allen drei Dimensionen. Eine Randwertkorrektur am Originalsampler ist in diesem Paket nicht enthalten.

Die alten Vektoren sind als Regression für die **fehlerhafte Variante** brauchbar. Sie dürfen nicht als Sollwerte des originalen JavaScript-Generators dienen. Dessen Integervektoren stehen in den nativen Ergebnissen. Für einen CI-Test sollte eine fehlgeschlagene Bedingung außerdem tatsächlich einen Fehler auslösen; `console.assert` allein ist kein zuverlässiger Testprozess-Abbruch.

Die frühere native radiale 4D-Diagnostik p≈0.01106 bleibt erhalten. Durch die Portkorrektur wurden weder Testseeds noch statistische Schwellen geändert oder ein neues statistisches PASS vergeben. Der analytische V1-Satz unter idealen unabhängigen kontinuierlichen Zufallszahlen wird von diesen Portierungs- und Randwertbefunden nicht widerlegt.

## 5. Quellstand und Reproduktion

Repository: https://github.com/thomasmgfeller/x6-spectral-astrolabium  
Commit: `560f717c0e25c957bc58bb9df5ec5ac6ad23cad0`  
Originalpfad des mitgelieferten `source/core.js`: `research/lorentz_proper_time_lab/core.js`  
Originalkern SHA-256: `5694637b2387bee6831008c53e86e1427bab341f4170648af8656181aee62795`  
Runtime JavaScript: Node.js v24.19.0, V8 13.6.233.17-node.51.  
Runtime Python: 3.12.14.  
Zeitpunkt Python-Prüfung: 2026-10-20T14:02:36.974892+00:00.

Die native Referenz kontrolliert den Git-Blob-Hash des Kerns anhand des vom früheren Audit übernommenen `source_manifest.json`. Dieses Manifest enthält zusätzlich die Herkunft von HTML und UI des früheren Audits; im vorliegenden Paket wird nur der unveränderte Kern benötigt und mitgeliefert. `normal()` wird für die isolierte Prüfung wortgetreu extrahiert, da es im Originalmodul nicht exportiert ist. Der vollständige Kern wird für PRNG und cloud() unverändert geladen.

Ausführen im entpackten Paket:

```bash
node native_reference.cjs
python3 verify_port.py
```

Es werden nur die Standardbibliotheken von Node.js und Python benötigt. Die Python-Prüfung liefert bei einer fehlgeschlagenen korrigierten Portprüfung einen Fehler-Exitcode. Ein erfolgreicher Exitcode betrifft ausdrücklich dieses Teilgate; der Gesamtstatus bleibt unter `gates.overall_V1b` separat sichtbar.

Dateien:

- `port.py`: korrigierte Variante und klar getrennte Rekonstruktion `MissingXorRNG`.
- `native_reference.cjs`: natives Referenzprogramm.
- `verify_port.py`: vollständiger Vergleich und Ursachennachweis.
- `results/port_verification.json`: maschinenlesbare Ergebnisse und Skripthashes.
- `results/native_reference.json.gz`: native Streams, Normalwerte, Wolken und Randfälle.
- `results/corrected_python_clouds.json.gz`: sämtliche korrigierten Python-Wolken.
- Die drei Fixture-JSON-Dateien: reproduzierte Alt-Fixture, korrigierte Python-Fixture und native Fixture.
- `SHA256SUMS`: Hashliste der Paketdateien.

Der ursprüngliche Repository-Code wurde nicht geändert oder veröffentlicht. Der nächste Implementierungsschritt ist die ausdrücklich definierte Behandlung endlicher Randwerte im Sampler, anschließend der erneute native Browser- und Exporttest.
