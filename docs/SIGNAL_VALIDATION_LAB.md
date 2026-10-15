# X6 Signal Validation Lab

## Zweck und Einstieg

Gemeinsame Installation und lokaler Start: [X6 Integration](INTEGRATION.md).
`python3 x6.py serve` öffnet den gemeinsamen Einstieg. Native Lab-JSONs lassen
sich mit `x6.py import-signal` prüfen und in dasselbe Exportpaket wie lokale
CLI-Läufe übernehmen; die nativen Formate bleiben erhalten.

Das Signal Validation Lab ist eine eigenständig aufrufbare Erweiterung des X6
Spectral Astrolabium. Es prüft bekannte synthetische Signale, kontrollierte
Störungen und die tatsächlichen Ergebnisse von vier Verarbeitungsverfahren.
Der bestehende X6-Phasenfilter wird dabei mit denselben Referenzsignalen und
Kennzahlen bewertet wie die einfachen Vergleichsverfahren.

**Öffnen:** [Signal Validation Lab](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/signal-lab.html).
Die Startseite des Projekts enthält einen eigenen Lab-Einstieg. Innerhalb des
Labs führen Links zurück zum Projektportal und zum bestehenden Astrolabium.
Die Oberfläche bietet Deutsch, Englisch und Französisch.

Lokal lässt sich `app/signal-lab.html` direkt im Browser öffnen. Alternativ:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Dann `http://127.0.0.1:8000/app/signal-lab.html` aufrufen. Die Laufzeit benötigt
keine externen Frontendbibliotheken, Installation, Anmeldung oder Datenbank.
SHA-256-Exporte benötigen WebCrypto in einem unterstützten lokalen Dateikontext,
auf localhost oder über HTTPS.

## Ein sinnvoller erster Versuch

1. Die Standardparameter übernehmen und **Test ausführen** anklicken. Das Lab
   erzeugt Referenz, gestörten Eingang und die vier vollständigen Ausgaben.
2. In der Vergleichstabelle oder der Methodenauswahl zwischen **Identität**,
   **gleitendem Mittelwert**, **FFT-Tiefpass** und **X6-Phasenfilter** wechseln.
   Dieser Wechsel verändert nur die Darstellung des abgeschlossenen Versuchs.
3. Die Zeitkurven zusammen mit PSD, Kohärenz und Kreuzphase betrachten. Die
   Tabelle und die aufklappbaren Einzelkriterien verwenden dieselben Arrays.
4. Rauschstärke, Verstärkung, Phase, Zeitversatz, Clipping oder Quantisierung
   gezielt ändern und erneut ausführen. Bereits die Eingabeänderung verwirft
   die alten Ergebnisse und sperrt deren Export.
5. **Gegenbeispiele prüfen** ausführen. Ein bestandener Gegenbeispielfall
   bedeutet, dass der erwartete Befund gefunden wurde. Er bedeutet nicht,
   dass das verfälschte Signal als gut akzeptiert wurde.
6. JSON und bei Bedarf CSV exportieren. Der JSON-Bericht lässt sich im Lab
   importieren, prüfen und vollständig neu berechnen.

Der Standardfall ist ein Mehrtonsignal mit 32, 56 und 80 Hz, 1.024 Samples,
1.024 Hz Abtastrate, Seed 104729 und nominaler Rausch-Standardabweichung 0,15.
Diese Signalenergie liegt innerhalb der voreingestellten FFT-Tiefpassgrenze
von 128 Hz. Daraus folgt kein allgemeiner Vorteil dieses Tiefpasses: Bei anderen
Signalen kann er relevante Frequenzen abschneiden oder periodische Randeffekte
verursachen. Der X6-Standardwinkel um 0° kann hingegen schon einen sauberen
Sinus mit Fourierphase −90° entfernen. Das ist ein sichtbarer Prüfgegenstand.

## Signale, Störungen und Verfahren

Als Sollsignal stehen Sinus, fest definiertes Mehrtonsignal, linearer Chirp,
Gaußpuls und Nullkontrolle zur Verfügung. Die Referenz bleibt das analytische
Signal ohne die eingebrachten Störungen; sie wird nicht aus dem verrauschten
Ergebnis geschätzt oder geglättet.

Die Störungskette ist fest geordnet: Phasenfehler der schwingenden Komponenten,
Verstärkung, ganzzahliger Zeitversatz mit Nullauffüllung, weißes Gaußrauschen,
symmetrisches Clipping und vorzeichenbehaftete Quantisierung. Ein positiver
Zeitversatz bedeutet ein späteres Kandidatensignal. Phase ist für Puls und
Nullkontrolle nicht definiert; dort ist nur Phasenoffset null zulässig.

Die Rauschzahl ist die nominale Standardabweichung des Generatormodells.
Die konkrete endliche Stichprobe wird nicht nachträglich auf genau diese
Standardabweichung normiert. Gleiche Parameter und gleicher Seed erzeugen
wieder dieselbe Stichprobe.

| Verfahren | Genau geprüfte Verarbeitung | Wesentliche Einordnung |
| --- | --- | --- |
| Identität | Unveränderter gestörter Eingang | Zeigt die Ausgangsfehler ohne Verarbeitungsnutzen. |
| Gleitender Mittelwert | Zentriertes ungerades Fenster; verfügbare Randwerte werden neu normiert | Nichtkausaler Offlinevergleich; kann Details und Amplitude verlieren. |
| FFT-Tiefpass | Periodische Fourierdarstellung; Frequenzen über der angegebenen Grenze werden entfernt | Idealer Offlinefilter mit möglichen Rand- und Ringeffekten. |
| X6-Phasenfilter | Originalgetreue Winkelwahl der positiven Fourierkoeffizienten mit ihren konjugierten Paaren | Phasenselektion, kein gewöhnlicher Frequenz-Tiefpass; kann ein Sollsignal entfernen. |

`phaseWidthDeg` bezeichnet die **gesamte Winkelbreite**, nicht die Halbbreite.
Die Codearithmetik dieses Filters wird in den unabhängigen Tests direkt mit
dem aus `app/index.html` extrahierten Originalfilter verglichen.

## Ergebnisse richtig lesen

Das Lab gibt keine zusammengezogene Qualitätsnote aus. Es zeigt acht Kennzahlen:
RMSE, NRMSE, vorzeichenbehaftete RMS-Verstärkungsabweichung, Rekonstruktions-SNR,
relative PSD-Abweichung, gewichtete Kohärenz, Phasenfehler und geschätzten
Zeitversatz. Alle Zeitfehler werden **vor** einer Ausrichtung oder Skalierung
gemessen. Eine nachträgliche Korrektur versteckt die eingebrachten Fehler nicht.

Die sechs Akzeptanzprüfungen verwenden die im Formular sichtbaren Grenzen.
Ihre Startwerte sind veränderbare Kriterien für den aktuellen synthetischen
Versuch; sie sind keine allgemeine Qualitätsnorm oder Kalibriervorschrift.

| Ergebnisstatus | Bedeutung |
| --- | --- |
| `PASS` | Alle sechs ausdrücklich angegebenen Kriterien sind definiert und erfüllt. |
| `FAIL` | Mindestens ein definiertes Kriterium wurde verletzt. |
| `INCONCLUSIVE` | Kein definiertes Kriterium scheitert, aber mindestens eines bleibt unvollständig, undefiniert oder mehrdeutig. |
| `PARTIAL` bei einer Metrik | Nur ein Teil der relevanten Referenzleistung trägt zur Diagnose bei; ihr Kriterium kann nicht bestehen. |
| `AMBIGUOUS` bei Zeitversatz | Mehrere Korrelationsextrema oder ein Suchrand verhindern eine eindeutige Verzögerungsaussage. |
| `EXACT_MATCH` bei SNR | Ein nichtleeres Referenzsignal hat exakt null Stichprobenfehler; der mathematische SNR-Grenzwert ist unendlich. JSON enthält dafür `null` und den erklärenden Status. |
| `UNDEFINED` | Für die betreffende Größe fehlt die benötigte Information oder der numerisch darstellbare Nenner. Das ist kein günstiger Zahlenwert. |

Ein periodischer Sinus kann mit sich selbst in allen Samples übereinstimmen,
ohne dass aus der periodischen Form ein eindeutiger physischer Zeitversatz
ableitbar wäre. Das Lab hält diese Unterscheidung als `INCONCLUSIVE` fest.
Die Zeitversatzsuche ist auf höchstens ±64 Samples begrenzt. Über ihren Bereich
hinausgehende oder gebrochene Verzögerungen werden nicht allgemein identifiziert.

Welch-PSD und Kreuzspektren entfernen den Mittelwert jedes Segments. DC-Fehler
können deshalb im detrendeten Spektrum verschwinden; die ursprünglichen
Zeitmetriken behalten sie. Nullwerte erhalten keinen künstlichen logarithmischen
PSD-Wert. Undefinierte Kohärenz und Phase bleiben in den Diagrammen Lücken.

Zusätzlich begrenzt ein deklarierter numerischer Dynamikbereich die normierten
Diagnosen: Beide Binleistungen müssen mehr als `1e-24` des größeren PSD-Maximums
betragen; für Zeitversatz muss das Verhältnis der zentrierten Signalnormen über
`1e-12` liegen. Dadurch werden winzige Reste nach nahezu vollständiger
Signalentfernung nicht zu scheinbar aussagekräftiger Phase oder Korrelation
normalisiert. Auch eine mathematisch kohärente extreme Abschwächung kann deshalb
im Lab unbewertet bleiben. Diese Auswertungsgrenze ist keine physische
Rauschgrenze oder gemessene Dekohärenz. Roharrays, PSD/CSD und die ursprünglichen
Amplituden-/Rekonstruktionsfehler bleiben erhalten. Eine gemeinsame kleine
Skalierung beider Signale wird nicht allein wegen ihrer Größe ausgeschlossen.

Die vollständigen Formeln, Segmentparameter, Abdeckungsregeln und numerischen
Toleranzen stehen in [SIGNAL_LAB_METHODS.md](SIGNAL_LAB_METHODS.md).

## Acht feste Gegenbeispiele

Die Suite enthält Polaritätsumkehr, positiven und negativen Sieben-Sample-Versatz,
starkes Clipping, Nullsignal, unterschiedliche konstante DC-Pegel, periodische
Verzögerungsmehrdeutigkeit und die Entfernung eines sauberen Sinus durch den
X6-Phasenfilter. Sie umfasst 27 konkrete Befundprüfungen.

Bei Polaritätsumkehr (y=-x) bleiben PSD und Betragsquadrat-Kohärenz gleich,
während NRMSE 2 und der Phasenfehler 180° betragen. Die getrennten Kennzahlen
verhindern, dass das Lab eine solche Übereinstimmung im Spektrum als gelungene
Rekonstruktion ausgibt.

Jeder Fall enthält seine vollständigen Referenz- und Kandidatenarrays sowie die
feste Konstruktion. Die Suite wird über `runCounterexamples()` wiederholt.
Ihre einzelnen `parameters` beschreiben Abtastung und Kriterien; sie ersetzen
bei speziell konstruierten DC- oder vorgefilterten Kandidaten nicht das
Konstruktionsrezept. Eine allgemeine automatische Suche über beliebige
Fehlermodelle ist in dieser ersten Version nicht enthalten.

## Ergänzende Wolfram-Gegenprüfung vom 15. Oktober 2026

Die [veröffentlichte Gegenprüfung der Polaritätsumkehr](signal-lab/wolfram-polarity-v0.1/README.md)
bestätigt vier symbolische Identitäten und zwölf numerische Sollwerte mit einem
separaten Wolfram-Rechenweg. X6 weist das invertierte Signal korrekt zurück.
Prüfpaket, Rohantworten und die dokumentierte Präzisionskorrektur der Nullkontrolle
sind verfügbar. Dies ist eine begrenzte synthetische Rechenprüfung, keine externe
personelle Begutachtung oder physikalische Validierung.

## Export, Quellen und Wiederholung

Der JSON-Export verwendet `x6.signal-lab.evidence/1`. Er bewahrt:

- alle Parameter einschließlich Seed, Filterwerte und Akzeptanzgrenzen;
- vollständige Zeit-, Referenz-, Eingangs- und Ausgabearrays aller vier Methoden;
- Kennzahlen, Einzelkriterien, Welch-/Kreuzspektren und Verzögerungsdiagnostik;
- eine optional ausgeführte Gegenbeispielsuite einschließlich ihrer Arrays;
- Engineversion, Quellenhashes, deklarierten Erstellungszeitpunkt und Grenzen;
- SHA-256 über eine ausdrücklich definierte kanonische JSON-Darstellung.

Import akzeptiert nur endliche JSON-Werte innerhalb der Größen- und
Strukturlimits. Anschließend werden Hash, Schema, Version, Quellenstand und
unveränderbare Replay-Toleranzen geprüft. Das Lab generiert den Versuch aus
den Parametern neu und vergleicht **alle** Arrays und abgeleiteten Ergebnisse.
Bei enthaltenen Gegenbeispielen wird auch deren vollständige Suite neu berechnet.
Abgeleitete Zahlen dürfen um `5e-12 + 5e-10 × |Referenzwert|` abweichen.
Für Phase gilt stattdessen eine absolute Toleranz von `2e-6` Grad: Spektralphasen
werden zirkulär verglichen, RMS-Phasenfehler und ihr Kriterium gewöhnlich absolut.
Dies berücksichtigt die schlechte Konditionierung sehr schwacher Spektralbins
und die gleichwertigen Phasen ±180°. Im konkreten Chromium-/Node-Vergleich
betrug die gefundene Abweichung an einem schwachen, für den Phasengate
ausgeschlossenen Bin etwa `7.2e-8` Grad. Andere Toleranzen werden dadurch nicht
gelockert. Parameter, Feldstruktur, Status und Methodik müssen dem Vertrag entsprechen.

Ein gültiger Hash allein genügt daher nicht, um erfundene Kennzahlen mit einem
bekannten Versuch zu verbinden. Ein korrekt neu berechneter, anderer Versuch
ist dagegen ein anderer gültiger synthetischer Versuch. Weder Hash noch Replay
beweisen einen Autor, ein vertrauenswürdiges Aufnahme- oder Erstellungsdatum,
unveränderte Speicherung oder eine physische Herkunft.

Die Quellenangaben stammen aus `app/signal-lab-build.js`. Der Bundlehash
identifiziert die zugehörige Dateihash-Map; er ist kein Git-Commit und keine
Signatur. `base_commit` bezeichnet ausdrücklich den Projektstand **vor** der
Erweiterung. Die ausliefernde Git-Revision lässt sich dem Repository bzw.
CI-Lauf entnehmen. Ein Replay eines anderen Quellenstands verlangt dessen
passenden archivierten Build. Der Browser authentifiziert seinen eigenen
ausgeführten Code nicht; die separaten Quellprüfungen vergleichen die Dateien.

CSV enthält `index,time_s,reference,observed,identity,moving_average,fft_lowpass,x6_phase`
für jeden tatsächlich berechneten Sample. Für vollständige Nachvollziehbarkeit
den zugehörigen JSON-Bericht mit aufbewahren.

## Softwareprüfung reproduzieren

Python 3.12 und Node 22 oder neuer verwenden. NumPy/SciPy und Playwright werden
nur für die Entwicklerprüfungen benötigt, nicht zum Öffnen der Oberfläche:

```sh
python -m pip install -r tests/signal-lab/requirements.txt
npm install --prefix /tmp/x6-signal-lab-test --no-save --no-package-lock playwright@1.62.1
node /tmp/x6-signal-lab-test/node_modules/playwright/cli.js install chromium
NODE_PATH=/tmp/x6-signal-lab-test/node_modules python tests/signal-lab/qualify.py --output /tmp/x6-signal-lab-evidence
```

Der Ausgabeordner muss neu sein. Vorhandene Prüfbelege werden nicht überschrieben.
Die Qualifikation prüft Quellinventar und geschützten Forschungsstand, führt
Kern-, Evidenz-, Provenienz-, NumPy/SciPy- und Chromiumprüfungen aus und archiviert
Quellsnapshots, Laufzeitversionen, Logs, echte Browserexporte und Screenshots.
Fehlgeschlagene Prüfungen liefern einen Fehlerstatus und erhalten ihren Bericht.
Die Quellen dürfen sich während des Laufs nicht ändern.

Ein vorhandenes kompatibles Chromium kann über `X6_CHROMIUM_EXECUTABLE` angegeben
werden; die tatsächliche Browserversion wird im Bericht festgehalten.
Die einzelnen Prüfungen lassen sich auch getrennt ausführen:

```sh
python tools/build_signal_lab.py --check
node --test tests/signal-lab/test_core.cjs
node tests/signal-lab/test_evidence.cjs
python -m unittest discover -s tests/signal-lab -p 'test_provenance.py' -v
python tests/signal-lab/reference_validation.py
NODE_PATH=/tmp/x6-signal-lab-test/node_modules node tests/signal-lab/browser_test.cjs
```

Die unabhängige Referenz verwendet NumPy-FFT/Faltung und SciPy-Welch/CSD/Kohärenz
mit explizit angegebenen Parametern. Ein separater VM-Kontext führt den wirklichen
Originalfilter aus dem vorhandenen Astrolabium aus. Die Browserprüfungen bedienen
die Oberfläche, lesen die tatsächlichen Downloads und prüfen Sprache, mobile
Darstellung, lokale Dateiausführung, Fehlerzustände und asynchrone Verwerfung
veralteter Exporte. Das ist mehr als eine Prüfung des neu geschriebenen Kerns
gegen sich selbst; die browserinterne Wiederholung bleibt trotzdem eine
Wiederholung mit derselben Engine.

Der Workflow **X6 Signal Lab** läuft bei einschlägigen Pull Requests und
Änderungen an `main` sowie bei manueller Auslösung. Er besitzt keinen Zeitplan
und führt keine Forschungsagenten aus. Seine Artefakte werden 30 Tage behalten;
das ist kein unveränderliches Langzeitarchiv.

## Integration und bestehender Forschungsstand

Die Erweiterung verwendet eigene `signal-lab*`-Dateien. Der ursprüngliche
`app/index.html`-Hash bleibt
`f3795c05292b0fc6d144b7afcf7ef4a957d88ac38ab4fda0c1e985f4455eadb8`.
Die ursprünglichen Hashes der 17 App-/Agent-/Workflowdateien des Ausgangsstands
`1735a85dfd5bdb7a4b59e5c00595d2d300ce1e05` bleiben unter
`protected_research_baseline` erhalten. Am 13. Oktober 2026 hat der Maintainer
die Reparatur und Verlängerung des Betriebsfensters ausdrücklich autorisiert.
Genau fünf abweichende Dateien (drei Agentenworkflows, Mathematikkonfiguration,
Konfigurationsprüfung) sind nun mit separaten festen Hashes im Buildwerkzeug
zugelassen. Das aktuelle 17-Dateien-Inventar steht in `protected_research`.
Anwendung, Datenadapter und mathematische Algorithmen bleiben unverändert.
Keine weitere Änderung wird durch automatisches Neuschreiben freigezeichnet.
Siehe [Betriebsreparatur](AGENT_WINDOW_REPAIR_2026_10_13.md).

`python tools/build_signal_lab.py` erzeugt nach einer absichtlichen Labänderung
den Build und das eigene Inventar neu. Das Werkzeug aktualisiert außerdem nur
die drei ausdrücklich benannten Integrationseinträge für Portal, README und
Repositoryprüfer im vorhandenen Sagnac-Manifest. Andere Sagnac-/Photonicdateien
und die Forschungspins werden nicht automatisch freigezeichnet.

Bei der Integration fiel auf, dass das zuvor zusammengeführte isolierte
Evidenzmodul noch nicht im zentralen Quelleninventar erfasst war. Sein neuer
`EVIDENCE_CALIBRATION_SOURCE_MANIFEST.json` inventarisiert genau diese vorhandenen,
inhaltlich unveränderten Dateien. Die zentrale Prüfung behält ihre Ablehnung
unbekannter Dateien bei. Das Signal Lab übernimmt die ausdrückliche Kennzeichnung
synthetischer Evidenz und die Trennung von Inhaltshash und Tatsachennachweis;
sein browserfähiger Replayvertrag bleibt ein eigener, dokumentierter Vertrag.

## Grenzen der ersten Version

Die Ergebnisse betreffen die angegebenen synthetischen Modelle und endlichen
Testfälle. Es gibt noch keinen Eingang für unabhängig aufgenommene Messreihen,
keine vollständige Messunsicherheitsbilanz, keinen breit validierten Detektor
mit Fehlalarm-/Übersehensraten und keine Aussage zu allgemeiner Filterüberlegenheit.
Die feste Gegenbeispielsuite ersetzt keine offene adversarielle Forschung.
Frequenz-/Phasen- und Verzögerungsdiagnosen können bei kurzer Aufzeichnung,
schwacher Energie oder periodischen Signalen eingeschränkt sein.

Das Lab steuert keine Hardware und erzeugt weder Quanten-, Kalibrier- noch
kryptografische Qualifikation. Die bestehenden mathematischen Zertifikate des
Astrolabiums behalten ihren dort definierten Geltungsbereich; sie werden durch
einen bestandenen Signalvergleich nicht auf das Ursprungssignal übertragen.
