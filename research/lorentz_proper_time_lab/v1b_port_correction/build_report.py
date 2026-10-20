from pathlib import Path
import hashlib
import json
import zipfile

R=Path(__file__).resolve().parent
r=json.loads((R/'results/port_verification.json').read_text())
normerr=max(x['max_absolute_error'] for x in r['normal_results'])
clouderr=max(x['max_absolute_error'] for x in r['cloud_results'])
different=sum(x['different_binary64'] for x in r['cloud_results'])
countrows='\n'.join(f"| {x['d']} | {x['seed']} | {x['old_count']} | {x['corrected_count']} | {x['native_count']} |" for x in r['cloud_results'])
text=f'''# V1b — Ursache geklärt und Python-Port korrigiert

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
| Zustand nach Fortschaltung | {r['first_step_trace']['advanced_state_uint32']} |
| x nach erster imul-Operation | {r['first_step_trace']['left_x_signed']} |
| Zweite imul-Operation | {r['first_step_trace']['second_imul_signed']} |
| Summe vor äußerem XOR | {r['first_step_trace']['sum_before_outer_xor']} |
| Korrektes Ergebnis des äußeren XOR, uint32 | {r['first_step_trace']['correct_outer_xor_uint32']} |
| Fehlerhafter finaler PRNG-Integer | {r['first_step_trace']['missing_xor_final_uint32']} |
| Korrekter finaler PRNG-Integer | {r['first_step_trace']['corrected_final_uint32']} |

Die ersten Ausgaben sind entsprechend 0.17110404395498335 (alter Port) und 0.17471173079684377 (korrigierter Port und Original-JavaScript).

## 2. Ausgeführte Prüfungen

Die Parameter und Toleranzen wurden in `protocol.json` vor der schichtweisen Vergleichsmatrix festgelegt. Die bereits bekannten ersten Vektoren und der reproduzierte Alt-Hash sind dort ausdrücklich benannt. Es handelt sich um eine gezielte Fehlersuche, nicht um ein blindes statistisches Experiment.

| Prüfung | Umfang | Ergebnis |
|---|---:|---|
| Rekonstruktion alter PRNG-Vektoren | 40 Werte, 4 Seeds | exakt reproduziert |
| Rekonstruktion alter Zählungen | 12 Läufe | exakt reproduziert |
| Rekonstruktion alter Fixture | 64 Punkte, d=4 | SHA-256 exakt reproduziert |
| Korrigierter PRNG gegen natives JS | 40000 Werte, 4 Seeds | exakt gleich |
| Korrigiertes normal() gegen natives JS | 4000 Werte | max. absoluter Fehler {normerr:.17g} |
| Korrigierte cloud() gegen natives JS | 196608 Punkte, d=2,3,4 | max. Koordinatenfehler {clouderr:.17g} |
| Inside-Flags | 196608 Vergleiche | 0 Abweichungen |
| Zählwerte | 12 Vergleiche | exakt gleich |

Für die Gleitkommarechnungen galt `abs(Python - JS) <= 1e-12 + 1e-12 * abs(JS)`. Alle Vergleiche erfüllten diese Bedingung. PRNG-Werte, Inside-Flags und Zählwerte wurden exakt verglichen. Der Test kann nur die deklarierte Matrix bestätigen, nicht alle Seeds und alle endlichen Rechenpfade.

| d | Seed | Alter Port | Korrigierter Port | Original-JavaScript |
|---:|---:|---:|---:|---:|
{countrows}

## 3. JSON-Hashes und tatsächliche Gleitkommaunterschiede

Für alle hier aufgeführten 64-Punkt-Fixtures ist das Objekt ausdrücklich auf `points` und `inside` beschränkt. Python nutzt `json.dumps(..., separators=(',', ':'), allow_nan=False).encode('utf-8')`; JavaScript nutzt `JSON.stringify()`. Es gibt keinen abschließenden Zeilenumbruch.

- Alter Python-Port: `{r['fixtures']['missing_xor']['sha256']}`
- Korrigierter Python-Port: `{r['fixtures']['corrected']['sha256']}`
- Original-JavaScript, gleiche Objektfelder: `{r['fixtures']['native_points_inside_only']}`

Die korrigierten Python- und JavaScript-Bytes sind nicht identisch. In der gesamten Wolkenmatrix unterschieden sich {different} Koordinatenkomponenten bereits in ihrer binary64-Darstellung; die maximale absolute Differenz steht oben. Somit sind neben möglicher Textformatierung auch tatsächlich minimale Unterschiede der mathematischen Laufzeitfunktionen vorhanden. Das ist innerhalb der gewählten numerischen Portprüfung zulässig, liefert aber keine plattformübergreifende Bitidentität.

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
Commit: `{r['git_commit']}`  
Originalpfad des mitgelieferten `source/core.js`: `research/lorentz_proper_time_lab/core.js`  
Originalkern SHA-256: `{r['source_sha256']}`  
Runtime JavaScript: Node.js {r['runtimes']['native']['node']}, V8 {r['runtimes']['native']['v8']}.  
Runtime Python: {r['runtimes']['python']}.  
Zeitpunkt Python-Prüfung: {r['timestamp_utc']}.

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
'''
(R/'V1b_PORTKORREKTUR.md').write_text(text)
files=[p for p in sorted(R.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS']
(R/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix()+'\n' for p in files))
files.append(R/'SHA256SUMS')
archive=R.parent/'V1b_Portkorrektur_2026-10-20.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in files:z.write(p,'V1b_Portkorrektur/'+p.relative_to(R).as_posix())
print(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,'files':len(files)}))
