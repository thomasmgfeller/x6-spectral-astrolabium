# CST-Staubball: Abschluss des bisherigen Bounce-Kandidaten v0.1

**Entscheidung: `CLOSED_REJECTED_FOR_DOMINANT_BOUNCE`.** Der Kandidat mit 27 Entwicklungspfaden bzw. 17 disjunkten Prüfpfaden erreicht unter gleichen Amplitudenbeträgen, erhaltenen Endvolumenkanälen und beliebigen normierten passiven Zusatzzeigern höchstens `q_B = 1/2`. Die notwendige Bounce-Dominanz von `4/5` ist damit ausgeschlossen. Die Schranke ist eine obere Grenze, keine Erreichbarkeitsbehauptung.

Der Bericht enthält die vollständigen Voraussetzungen, den analytischen Beweis, beide konkreten Zeugen, die nachgerechneten numerischen Resultate und Wiederaufnahmekriterien. Der Satz war für die Entwicklungsfamilie bereits im Originalbericht zur Dichtespur enthalten. Der Abschluss konsolidiert ihn und zertifiziert die Voraussetzungen für beide Familien.

Der Abschlussstatus ersetzt keine historischen Gate-Entscheidungen. HOLD bei unzureichender Interferenzkontrolle bleibt HOLD; die 17 Prüfpfade ergeben im geprüften Kopplungsband für beide Messvarianten FAIL. Numerisches OPEN in schmalen Übergangsbändern bleibt sichtbar. Ein allgemeiner CST-Bounce und Singularitätsauflösung bleiben HOLD. N verneint nur das festgelegte Ereignis im festgelegten Zeitfenster.

## Quellenstand

Repository `thomasmgfeller/x6-spectral-astrolabium`, Main-Commit `5f7994400869c921dec5b335f04a384a713e5e64`, geprüft am 2026-11-05. Drei unveränderte Originalarchive aus PR 216, 219 und 220 liegen in `sources/`. Die Git-Blob-IDs wurden gegen den Commitbaum abgeglichen; SHA-256, interne Prüflisten und Konfigurationsdateien werden gesondert gebunden.

- `source_snapshot.json`: Originalarchive, Git-Pfade, Blob-IDs und SHA-256.
- `candidate_snapshot.json` und `CANDIDATE_SHA256`: deterministische Eingabebindung beider Familien, Gate, Wirkungsdaten und Messregeln.
- `verify_closure.py`: eigenständige rationale Zertifikate und Wiederholung der archivierten Auswertungen.
- `results/closure_result.json`: Abschlussentscheidung, Zertifikate, Statusübertragung und Prüfresultate.
- `results/scan.json`, `results/audit.json`, `results/replay.log`: erneute Ausgaben, inklusive offener Übergangsbereiche.
- `report.tex` und `CST_Staubball_Bounce_Kandidat_Abschluss_v0_1.pdf`: lesbarer Abschluss.
- `SHA256SUMS`: Integrität des vollständigen Abschlussverzeichnisses (ohne sich selbst).

## Reproduktion

Python 3.10 oder neuer ohne Zusatzpakete, mit aktivierten Assertions:

```sh
sha256sum -c SHA256SUMS
python3 verify_closure.py --out replay
```

Der Prüfer extrahiert Arbeitskopien in ein temporäres Verzeichnis, prüft 51 Original-Prüfsummen, zwei vollständige Träger und deren eindeutige Bounce-/isolierte Endkanalzeugen, wiederholt Scan, 120 direkte Zahlenvergleiche, Dichtespur und endliche Regularitätskontrollen und vergleicht acht Ergebnisdateien. Er verändert die Quellarchive nicht. Der universelle Messzeigersatz folgt aus der im Bericht formulierten Normzerlegung, nicht aus einer Stichprobe von Zeigern.

Die vollständige Kausalordnungs-Erzeugung, 18 ursprüngliche explizite Nachzählungen und 70 inverse Momentquadraturen wurden für diesen Abschluss nicht wiederholt. Es wurden keine Hardwaremessungen oder neuen statistischen Versuche ausgeführt. Lokale Hash-Siegel sind keine externe Präregistrierung. Diese retrospektive Auswertung darf nicht als neuer Holdout behandelt werden.

## Wissenschaftliche Konsequenz

Weitere Versuche, denselben Kandidaten allein durch passive Messkopplung über das 80-%-Gate zu bringen, werden beendet. Eine neue Kandidaten-ID verlangt eine unabhängig begründete Änderung ausschlussrelevanter Voraussetzungen sowie einen vorher festgelegten dynamischen und klassischen Referenztest. Das Ergebnis widerlegt weder die CST insgesamt noch jede andere Bounce-Definition. Der Bericht veranlasst keine Veröffentlichung, keine Änderung von GitHub-Issues und keine Beendigung anderer Programme.
