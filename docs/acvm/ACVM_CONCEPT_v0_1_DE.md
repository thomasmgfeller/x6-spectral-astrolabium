# Astrolabium Control and Validation Module

*Konzept für die Steuerung und Validierung*

**Kurzname ACVM · Konzeptversion 0.1 · 13. Oktober 2026**

Projektkontext Thomas Gfeller · Spektral Astrolabium

ACVM soll vorbereitete Versuchssequenzen ausführen, ihren tatsächlichen Ablauf erfassen und die Ergebnisse anhand offengelegter Kriterien prüfen. Der erste Zielpfad ist eine klassische FPGA Steuerungs- und Messkette. Ein photonischer Aufbau wird erst nach deren elektrischer Charakterisierung angeschlossen.

**Diese Fassung ist ein eigenständiger Konzeptentwurf. Sie legt Anforderungen und Prüfpläne fest. Es wurden dafür keine ACVM Software, keine FPGA Firmware und keine Geräteanbindung implementiert oder abgenommen.**

### Entscheidungen dieser Fassung

Der Name beschreibt die Funktion und hält den Anschluss an das Astrolabium. In einer künftigen Oberfläche lautet der deutsche Modulname „Steuerung und Validierung“. Als technischer Namensraum wird astrolabium.acvm vorgeschlagen. Die Bezeichnung ist keine geprüfte Marke und keine Behauptung technischer Neuheit.

Übernommen werden die Trennung von Host und zeitgebundener Ausführung, explizite Waveformbeschreibungen, unabhängige Validierung und nachvollziehbare Versuchsdaten. Die PMCS Bezeichnungen werden durch gewöhnliche Funktionsnamen ersetzt. Bekannte Fehler dienen als Ausgangspunkt für Regressionstests.

| **Bereich**                                 | **Status am 13. Oktober 2026**                         |
|---------------------------------------------|--------------------------------------------------------|
| Konzept und Anforderungen                   | In diesem Dokument ausgearbeitet                       |
| Übernahme ausführbaren PMCS Codes           | Nicht erfolgt und nicht als qualifiziert vorausgesetzt |
| Software und FPGA Nachweise                 | Für ACVM noch nicht erbracht                           |
| Elektrische und photonische Messungen       | Für ACVM noch nicht durchgeführt                       |
| Quantenoperation oder industrieller Einsatz | Eigene spätere Nachweise erforderlich                  |

Leseregel: „muss“ bezeichnet eine Anforderung an eine spätere Implementierung. Ein Prüfkriterium ist kein bestandenes Ergebnis. Die Statusangaben gelten für diesen Entwurf und dürfen nicht als vollständiger Bericht über alle früheren Astrolabium Arbeiten gelesen werden.

## 2 Übernahme und Herkunft

Die Übernahme erfolgt auf Ebene von Konzepten, Anforderungen und dokumentierten Gegenbeispielen. Der gelesene PMCS Prüfbericht betrifft v0.4.4; der zuletzt eingereichte Text beschreibt v0.1. Eine Identität ihrer Implementierungen ist nicht belegt. Der Bericht nennt seine geprüfte Eingabe und deren Hash. \[I1\]

| **Herkunft**         | **ACVM Baustein**                            | **Art der Übernahme**                                                       |
|----------------------|----------------------------------------------|-----------------------------------------------------------------------------|
| Schichtenarchitektur | Host, Compiler, Backend, Ausführung, Messung | Trennung übernehmen; Messrückweg ergänzen                                   |
| DEB                  | Ausführungsvertrag                           | Zeitbasis, Puffer, Fristen und Fehlerzustände neu spezifizieren             |
| WDBF                 | Versuchspaket                                | Metadaten und Nutzdaten mit vollständiger Inhaltsbindung neu festlegen      |
| PVF                  | Validierungsplan                             | Einzelmetriken, Referenzen, Unsicherheiten und Gültigkeitsbereich festlegen |
| PSE                  | Betriebsgrenzen und Datenintegrität          | Geräteschutz und Herkunftsprüfung getrennt behandeln                        |
| CMRF                 | Optionale Testsignalbibliothek               | Unregelmässige Folgen nur als deklarierte Testsignale prüfen                |
| PMCS Gegenbeispiele  | Regressionstestkatalog                       | Defekte als Testanforderungen konservieren; noch nicht portiert             |
| X6 Nachweisstatus    | Getrennte Evidenzanzeigen                    | Prüfumfang und offene Nachweise ausdrücklich anzeigen                       |

### Was die früheren Befunde tragen

Der PMCS Bericht dokumentiert unter anderem ungültige Zahlen mit scheinbar guten Kennwerten, falsche zyklische Phasenfehler, unvollständige komplexe Spektren, einen wirkungslosen Jitterparameter und unvollständige Bindung exportierter Daten an Signaturen. Seine Diagnoseprüfungen sind keine Freigabetests und beheben die Fehler nicht. \[I1, I2\]

Erfolgreiche MAT und HDF5 Rückleseprüfungen im Bericht stützen jeweils nur die geprüften Formatpfade unter den genannten Bedingungen. ACVM übernimmt deshalb das Prinzip unabhängiger Rückleseprüfungen; die Exportimplementierungen gelten dadurch nicht als übernommen oder qualifiziert. \[I1\]

### Grenze der Astrolabium Bestandsaufnahme

Der gelesene X6 v2.1 Audit dokumentiert abgegrenzte mathematische Referenztests und offene Prüfungen. Er beschreibt keinen heutigen Gesamtfreigabestand. Für ACVM werden deshalb keine bestehenden Geräteschnittstellen, Datenmodelle oder Browserpfade als kompatibel vorausgesetzt. Die Integration in Kapitel 3 ist ein Entwurf. \[I3\]

## 3 Architektur und Anschluss an Astrolabium

ACVM erhält einen eigenständig prüfbaren Kern. Astrolabium dient als Bedien- und Analyseoberfläche; ein lokaler Dienst verwaltet Gerätezugriffe. Eine Browseroberfläche darf keine präzise Ausführungszeit durch den Zeitpunkt eines Netzwerkaufrufs definieren. Zeitgebundene Ereignisse werden im unterstützten Gerät vorbereitet und ausgeführt.

| **Baustein**      | **Verantwortung**                                                 | **Prüfbare Ausgabe**               |
|-------------------|-------------------------------------------------------------------|------------------------------------|
| Experiment Plan   | Ziel, Kanäle, Sequenz, Grenzen und Abnahme vor dem Lauf festlegen | Versionierter Plan                 |
| Sequence Compiler | Plan in Zeitmarken und numerische Ausgabewerte übersetzen         | Execution Image mit Hash           |
| Device Backend    | Gerätefähigkeiten prüfen; laden, starten und Status erfassen      | Geräteantworten mit Run ID         |
| FPGA Sequencer    | Vorbereitete Ereignisse auf definierter Uhr ausführen             | Ereignis- und Fehlerprotokoll      |
| Acquisition       | Elektrische oder optische Wirkung erfassen                        | Rohdaten mit Zeitbasis             |
| Validation Engine | Unabhängige Referenz mit Messung vergleichen                      | Einzelprüfungen und Unsicherheiten |
| Run Archive       | Plan, Builds, Rohdaten und Auswertung zusammenhalten              | Vollständiges Versuchspaket        |

### Vorgeschlagener Integrationsvertrag

Astrolabium übergibt einen gespeicherten Experiment Plan an ACVM und erhält getrennt den Compilerbericht, den Ausführungsstatus und den Validierungsbericht zurück. Schema und Hauptversion müssen explizit übereinstimmen. Unbekannte Hauptversionen werden abgewiesen. Der Adapter darf keine Einheiten stillschweigend umdeuten.

Im ersten Integrationsschritt werden Pakete exportiert und wieder importiert. Der Gerätebetrieb kommt erst nach einer Prüfung des aktuellen Astrolabium Codes und eines konkret ausgewählten Backends hinzu. Ein künftiger Signal Validation Lab Adapter ist gegen dessen dann festgelegte Schnittstelle zu testen; seine Existenz oder Kompatibilität wird hier nicht behauptet.

### Gemeinsame und getrennte Aufgaben

Signalmetriken sollen nach ihrer Qualifizierung aus einer gemeinsamen, versionierten Bibliothek stammen. Backend, Sequencer und Fehlerüberwachung bleiben von Darstellung und wissenschaftlicher Auswertung getrennt. Rechenintensive Astrolabium Analysen dürfen die zeitkritische Ausführung nicht blockieren.

ARTIQ zeigt die technische Tragfähigkeit gepufferter, zeitgestempelter FPGA Ereignisse; QICK ist ein Referenzpunkt für die gemeinsame Charakterisierung digitaler und analoger Qubitsteuerung. Beide sind Vergleichssysteme. Ihre Leistungswerte sind keine ACVM Spezifikationen. \[R1, R2\]

## 4 Ausführungsvertrag und Gerätezustände

ACVM startet mit vollständig vorgeladenen, endlichen Sequenzen. Streaming und schnelle Rückkopplung bleiben eigene Erweiterungen, weil sie zusätzliche Bandbreiten- und Fristnachweise benötigen. FPGA, DAC, ADC und Detektoreingänge können verschiedene Uhrdomänen besitzen; jeder Übergang muss beschrieben und geprüft werden.

| **ID** | **Verbindliche Anforderung**                                                                                                                                    |
|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ACV 01 | Nur endliche, dimensionsrichtige Parameter innerhalb des Geräteprofils zulassen. NaN und Infinity führen zu INVALID.                                            |
| ACV 02 | Experimentzeit in ganzzahligen Ticks mit dokumentierter Dauer und Epoche führen. Bei JSON grosse Zähler als Dezimalstrings kodieren; kein Verlust oberhalb 2⁵³. |
| ACV 03 | Vor dem Start Pufferbedarf, Kanalbelegung, minimale Ereignisabstände, Zählerüberlauf und Startvorlauf prüfen.                                                   |
| ACV 04 | Zeitgebundene Ausgabe erst nach vollständigem Laden und bestätigter Gerätebereitschaft erlauben. Keine stille Zeitverschiebung verspäteter Ereignisse.          |
| ACV 05 | Fehlende Takte, Pufferfehler, Datenverlust und Kommunikationsabbruch erfassen. Reaktion und Ausgangszustand pro Geräteprofil festlegen.                         |
| ACV 06 | Jeden Befehl an Run ID, Sequenznummer und Execution Image Hash binden. Wiederholungen dürfen keinen zweiten Start auslösen.                                     |
| ACV 07 | Rohdaten und Fehlerzustände bleiben erhalten. Nach einem Fehler muss ein neuer Lauf eine neue Gültigkeitsbewertung erhalten.                                    |

| **Zustand**          | **Bedeutung und zulässiger Übergang**                                                                      |
|----------------------|------------------------------------------------------------------------------------------------------------|
| IDLE und LOADED      | Gerät im festgelegten Ruhezustand; danach Paket prüfen und laden.                                          |
| ARMED                | Geladene Daten, Uhr und Betriebsgrenzen bestätigt; Start nur für diesen Run.                               |
| RUNNING und COMPLETE | Sequenz ausführen; COMPLETE erst nach Abschlussbestätigung und Datenerfassung.                             |
| ABORTED und FAULT    | Abbruch oder Gerätefehler; keine automatische Fortsetzung. Erneutes Laden nach dokumentierter Rücksetzung. |

Eine Empfangsbestätigung ist keine Ausführungsbestätigung. Bei unklarem Verbindungszustand wird der Lauf als UNKNOWN behandelt; ein erneuter Start erfolgt erst nach Zustandsabfrage und eindeutiger Zuordnung. Der sichere Ausgangszustand kann je nach Aktuator von null Volt abweichen.

Physische Grenzwerte müssen soweit erforderlich auch unabhängig von der Benutzeroberfläche durchgesetzt werden. Die konkrete Schutzschaltung und ihre Prüfung gehören zum ausgewählten Geräteprofil, nicht zu einer pauschalen Softwaregarantie.

## 5 Versuchspaket und Datenintegrität

ACVM verwendet zunächst ein transparentes Verzeichnis mit JSON Metadaten und getrennten Nutzdaten. Ein neues universelles Binärformat ist für den ersten Meilenstein nicht erforderlich. Das Paket beschreibt die tatsächlichen Bytes und die zugehörige physikalische Bedeutung.

| **Objekt**                     | **Pflichtinhalt**                                                                                                           |
|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| plan.json                      | schema_version, run_id, evidence_kind, Versuchsziel, Kanäle, Einheiten, Sequenz, Abnahmeplan und dessen Hash                |
| device_profile.json            | Gerätekennung, Kanalfähigkeiten, Pegel, Taktquellen, Puffer, Grenzen, Reaktion auf Fehler, Kalibrierbezüge                  |
| execution.json und samples.bin | Zeitmarken, Kanalreihenfolge, Abtastrate, Samplezahl, Datentyp, Byte-Reihenfolge, Skalierung, Compiler- und Firmwarekennung |
| raw und events                 | Unveränderte Erfassungsdaten, Trigger, Gerätezeit, Verluste, Fehlermeldungen und explizite Lücken                           |
| calibration und validation     | Gültige Kalibrierung, Auswerteversion, Referenz, Unsicherheiten, Einzelentscheidungen und Begründungen                      |
| manifest.json                  | Dateiliste, Bytegrössen und SHA-256 aller einbezogenen Dateien; Erstellungs- und Finalisierungsstatus                       |

### Numerische und zeitliche Semantik

Das erste numerische Profil definiert genau einen Nutzdatentyp pro Datei, etwa little endian int16 für DAC Codes. Zuordnung zu Volt, Übersteuerung und Kanalanordnung sind festzulegen. Komplexe Werte benötigen eine explizite Abbildung auf reale I/Q Kanäle. Float Referenzdaten und DAC Codes bleiben getrennt. Gerundete CSV Exporte sind Ansichtskopien, sofern kein eigener Genauigkeitsvertrag besteht.

Bei Zufallssignalen werden Algorithmus, Implementierungsversion, Seed, Initialzustand und Ziehungsreihenfolge festgehalten. Bei chaotischen Testfolgen kommen Integrator, Schrittweite und Zahlenpräzision hinzu. Hardwaremessungen sind statistisch reproduzierbar; derselbe Seed erzeugt keine identischen Photodetektorereignisse.

### Integrität und Herkunft

Das Manifest wird nach Abschluss der Messung eingefroren und bei jeder Auswertung geprüft. Es listet sich selbst und seine abgetrennte Signatur nicht rekursiv. Eine optionale Signatur schützt seine exakt festgelegten Bytes; eine Kanonisierung muss vor Verwendung eindeutig spezifiziert werden. Ein Hash erkennt Inhaltsänderungen, bestätigt aber weder Messrichtigkeit noch Urheberschaft.

Bei Signaturen werden Schlüsselvertrauen, Widerruf und Prüffehler getrennt vom mathematischen Prüfergebnis angezeigt. Fehlende Vertrauensinformation ergibt UNKNOWN. Private Testschlüssel in einem Browser sind keine qualifizierte Schlüsselverwaltung. Eine neue Auswertung erhält eine neue Kennung und überschreibt die Rohdaten nicht.

## 6 Modell für Zeit Verlust und Drift

Die folgenden Gleichungen sind ein vorgeschlagenes Modellgerüst. Parameter müssen gemessen oder ausdrücklich als synthetische Annahmen markiert werden. Schnelle Samplezeit und langsame Versuchszeit werden beide in Sekunden geführt; ihre Zuordnung ist Teil des Plans.

### Zeitpunkte und Uhrabweichungen

$$
t_{c,n}=t_0+nT_s+b_c+d_c(nT_s)+\varepsilon_{c,n}
$$

c bezeichnet den Kanal, n den Sampleindex, Ts die nominelle Sampleperiode, bc einen konstanten Versatz, dc die langsame Uhrdrift und εc,n den verbleibenden zeitlichen Fehler. Auflösung, systematischer Versatz, Jitter und Messunsicherheit sind getrennte Angaben. Korrelationen zwischen Kanälen bleiben erhalten; ein unabhängig gezogener Zufallsterm ist keine universelle Jitterbeschreibung.

### Elektrische Übertragung

$$
v_c(t)=(h_c\ast u_c)(t)+v_{\mathrm{bias},c}(t)+\nu_c(t)
$$

uc ist die aus DAC Codes und tatsächlichen Ausgabezeitpunkten rekonstruierte Eingangsspannung. hc ist die im betrachteten Bereich angenommene lineare Impulsantwort, vbias,c die Biasdrift und νc ein Störterm. Sättigung, Slew Rate und relevante Nichtlinearitäten benötigen zusätzliche Modelle. Jitter muss die Zeitpunkte und dadurch das Signal verändern.

### Beispiel für einen Intensitätsmodulator

$$
T(t)=\eta(t)\cos^2\!\left(\frac{\varphi_{\mathrm{bias}}(t)+\pi v(t)/V_\pi}{2}\right)
$$

T ist die Leistungstransmission eines idealisierten Mach Zehnder Modulators. η enthält die zusätzlichen Verluste, Vπ folgt der angegebenen Ansteuerkonvention. Diese statische Kennlinie ist nur für ein passendes Bauteil und einen geprüften Arbeitsbereich anwendbar. Bandbreite, Wellenlänge, Polarisation, Extinktion und Hysterese sind gesondert zu charakterisieren. Für andere Aktuatoren wird sie ersetzt.

$$
\eta_{\mathrm{ges}}=10^{-L_{\mathrm{ges}}/10},\qquad 0\leq\eta_{\mathrm{ges}}\leq 1
$$

Lges ist der gesamte Leistungsverlust in dB. Beiträge dürfen nur bei konsistenten Bezugsebenen addiert werden; für ein Feld beträgt der zugehörige Amplitudenfaktor die Quadratwurzel der Leistungstransmission. Gemessene gekoppelte Drift und Verluste dürfen nicht ohne Prüfung als unabhängig modelliert werden.

Das Modell liefert zunächst klassische Vorhersagen. Ein Quantenzustandsmodell muss zusätzlich Moden, Verlustkanäle und Detektion abbilden. Parameter werden an Kalibrierdaten angepasst und an getrennten Messläufen geprüft. \[R3\]

## 7 Metriken und wissenschaftliche Entscheidung

ACVM berichtet Einzelgrössen mit Einheiten, Messbedingungen und Unsicherheiten. Ein zusammengefasster Qualitätsscore ist kein Freigabekriterium. Ein Lauf kann technisch abgeschlossen sein und wissenschaftlich dennoch INVALID oder INCONCLUSIVE bleiben.

### Signalfehler und Phase

$$
\Delta\varphi_n=\operatorname{atan2}\!\left(\sin(\varphi_{m,n}-\varphi_{r,n}),\cos(\varphi_{m,n}-\varphi_{r,n})\right)
$$

m bezeichnet Messung und r Referenz. Phasenwerte bei zu kleiner Amplitude werden anhand einer vorab festgelegten Schwelle ausgeschlossen und als undefiniert gezählt. Zeit-, Phasen- oder Verstärkungsabgleich ist nur zulässig, wenn seine Freiheitsgrade vorab festgelegt sind. Rohfehler, korrigierter Fehler und geschätzte Korrekturen werden gemeinsam berichtet.

$$
E_{\mathrm{rel}}=\frac{\lVert x_m-x_r\rVert_2}{\lVert x_r\rVert_2}
$$

Der relative komplexe RMS Fehler ist nur für einen von null verschiedenen Referenznormwert definiert. Er ist keine Quantengatterfidelität. Eine EVM Bezeichnung setzt zusätzlich eine festgelegte Symbolreferenz und Auswertekonvention voraus.

### Spektrum und zeitliche Messung

Komplexe Basisbandsignale benötigen positive und negative Frequenzen. Eine PSD muss Abtastrate, Fenster, Normierung, Mittelung und Einheit angeben, etwa V²/Hz für Spannung. Zeitauflösung, Triggerabweichung, Kanalversatz, beobachtete Extremwerte, Quantile und Messdauer werden separat ausgewiesen. Ein beobachtetes Maximum beweist keine absolute Worst Case Grenze.

### Unsicherheit und Entscheidungsregel

Kalibrierunsicherheit, Auflösung, Drift, Wiederholstreuung und Korrelationen werden für die jeweilige Messgrösse bilanziert. Messmodell, Kovarianzen und verwendete Näherungen müssen nachvollziehbar sein. Bei nichtlinearen oder korrelierten Daten sind geeignete Fortpflanzung oder modellbasierte Simulationen zu begründen. JCGM Dokumente dienen als metrologischer Bezug, ohne eine Konformitätsbehauptung für ACVM. \[R4\]

Für eine obere Fehlergrenze B kann konservativ gelten: PASS, wenn das gesamte ausgewiesene Unsicherheitsintervall unter B liegt; FAIL, wenn es vollständig darüber liegt; sonst INCONCLUSIVE. Intervallart und Abdeckung werden angegeben. Fehlende erforderliche Rohdaten führen zu INVALID, nicht zu einem kleinen Fehlerwert.

Jede Entscheidung trägt Kriterium, Messbereich, Datenhash und Auswerteversion. Simulationsbefunde, elektrische Messungen und Quantenbefunde besitzen getrennte Evidenzkennzeichen. Koinzidenzauswahl, Hintergrundkorrektur und weitere Postselektion sind Teil des Auswerteplans.

## 8 Prüfplan und Rückverfolgbarkeit

Alle folgenden ACVM Prüfungen stehen auf NOT RUN. Die Grenzwerte für reale Hardware werden erst aus dem gewählten Versuchs- und Geräteprofil abgeleitet und vor der Messung eingefroren. Die hier festgelegten Negativtests lassen sich bereits für den Softwarekern konkretisieren.

| Test | Prüffall | Abnahmekriterium |
| --- | --- | --- |
| V01 / ACV 01 | NaN, Infinity, falsche Einheiten und unzulässige DAC Parameter | Abweisung vor Ausgabe; keine alten PASS Anzeigen oder Artefakte dem neuen Lauf zuordnen |
| V02 | Phasen 0 und 2π; kleine negative Phase um null; Nullamplitude | Zyklischer Fehler numerisch korrekt; vorgeschlagene absolute Toleranz 10⁻¹² rad für diese Float64 Fälle; Phase bei Nullamplitude undefiniert |
| V03 | Gezielte Zeitverschiebung einer nichtperiodisch symmetrischen Referenz | Unalignierter Fehler wird erkannt; erlaubter Abgleich meldet den Versatz separat |
| V04 | Komplexe Töne mit positiven und negativen Frequenzen | Peaks an erwarteten FFT Bins; Leistung stimmt mit unabhängiger Referenz innerhalb festgelegter Numeriktoleranz überein |
| V05 | Änderung eines Samples nach Index 256; Kürzung; falsche Bytezahl | Inhaltsprüfung schlägt fehl; keine Teilsample Prüfsumme als Vollschutz akzeptieren |
| V06 / ACV 02 und 03 | Zählerüberlauf, ungültige Reihenfolge und volle Puffer | Definierte Ablehnung oder protokollierte Fehlerreaktion; keine stille Datenlücke |
| V07 / ACV 04 bis 07 | Doppelter Start, Verbindungsabbruch und Verlust der Taktreferenz | Kein doppelter Lauf; Geräteprofil bestimmt Reaktion; Ergebnis bleibt eindeutig zugeordnet |
| V08 | Jitter und Drift an einer zeitlich veränderlichen synthetischen Referenz variieren | Zeitpunkte und Signal ändern sich konsistent; Nullstörung reproduziert Referenz innerhalb Numeriktoleranz |
| V09 | DAC Ausgang unabhängig elektrisch erfassen | Zeit- und Signalfehler samt Unsicherheit erfüllen die eingefrorenen Profilgrenzen |
| V10 | Modell an Kalibrierdaten anpassen und an neuen Daten prüfen | Vorhersagefehler, Drift und Verluste erfüllen vorab definierte Kriterien; Gültigkeitsbereich bleibt begrenzt |

V02 bis V05 und V08 greifen dokumentierte PMCS Fehlerklassen auf. Die Prüfungen verwenden unabhängige Referenzberechnungen; ein Vergleich zweier Aufrufe desselben fehlerhaften Kerns genügt nicht. Ein erfolgreiches synthetisches Ergebnis schliesst V09 oder V10 nicht ab. \[I1, I2\]

## 9 Erster Versuchsablauf und Quantenpfad

### D01 Software Referenzversuch

Eine endliche Sequenz enthält Gleichanteil, Sinus, einen negativen komplexen Frequenzton und eine eindeutige Zeitmarke. Der Compiler erzeugt eine feste Ausgabedatei. Ein unabhängig implementierter Leser rekonstruiert Referenz und Metadaten. V01 bis V08 prüfen Normalfälle und gezielt gestörte Kopien. Der Ergebnisstatus lautet SIMULATED; eine Hardwareausführung wird nicht suggeriert.

### E01 Elektrische Schleifenmessung

Nach Wahl eines Geräteprofils wird zunächst ein Ausgangskanal auf einen geeigneten unabhängigen Messeingang geführt. Der Plan legt Dauer, Bandbreite, Amplitude, Samplezahl, Trigger und Fehlergrenzen fest. Rohdaten umfassen auch Einschwingverhalten, Übersteuerung und Datenlücken. Wenn Generator und Messgerät dieselbe Uhr nutzen, wird die eingeschränkte Aussage zur absoluten Zeitgenauigkeit ausgewiesen.

Die Prüfung umfasst Wiederholungen und einen festgelegten längeren Lauf zur Driftbeobachtung. Anzahl und Dauer folgen aus der gewünschten Aussage und Autokorrelation. Null beobachtete Fehler allein belegt keine Fehlerfreiheit; eine Fehlerratengrenze erfordert ein geeignetes statistisches Modell. Messmittelauflösung und Kalibrierung müssen zur geforderten Grenze passen.

### P01 Photonische Charakterisierung

Erst danach wird ein kompatibler Aktuator mit geeigneter optischer Messung untersucht. Bestimmt werden mindestens statische Kennlinie, nutzbarer Arbeitsbereich, Verlust, Biasdrift und zeitliche Antwort. Der Vergleich mit einem ungeregelten Referenzlauf zeigt, ob eine langsame Stabilisierung unter denselben Bedingungen nützt. TFLN bleibt eine Option; Bauteilauswahl und Ansteuerung folgen dem konkreten Versuchsbedarf. \[R6, R7\]

### Q01 Charakterisierung einer Quantenoperation

Ein späterer Sagnac Versuch muss zuerst Kodierung, Zielzustand, Messbasen und beabsichtigte Operation festlegen. Bei Polarisationsqubits ist eine gemeinsame konstante Phase physikalisch wirkungslos für das Polarisationsqubit; eine relative Phase zwischen H und V kann relevant sein. Zeitabhängige Modulation kann zusätzliche Moden verändern. Das erforderliche Modell hängt vom optischen Aufbau ab. \[R3\]

Eine gute klassische Waveform oder Interferenzsichtbarkeit bestätigt noch keine Prozessfidelität. Geeignete Zustands- beziehungsweise Prozesscharakterisierung muss Präparations- und Messfehler, Verluste und Postselektion ausweisen. Konditionierte Güte und Erfolgswahrscheinlichkeit werden getrennt berichtet. ACVM allein erzeugt weder Verschränkung noch einen universellen Quantencomputer.

Für spätere ereignisabhängige Steuerung zählt die gesamte Kette aus Detektor, Eingang, Logik, Ausgang, Treiber und Aktuator. Deren Latenz mit Schwankungen und Reserve muss in das physikalisch verfügbare Zeitfenster passen. Der Host verbleibt ausserhalb dieser schnellen Reaktionskette.

## 10 Entwicklungsstufen und offene Entscheidungen

| Stufe | Liefergegenstand | Voraussetzung für Abschluss |
| --- | --- | --- |
| 0.1 / Konzept | Dieses Dokument mit Übernahmeplan und Nachweisgrenzen | Konzeptprüfung; keine technische Freigabe |
| 0.2 / Referenzkern | Paketformat, Compiler, unabhängiger Leser und Modellprüfungen V01 bis V08 | Reproduzierbare Softwareberichte mit geprüften Referenzen |
| 0.3 / FPGA Backend | Ein Geräteprofil, Sequencer und elektrische Schleifenmessung | V09 sowie V06 und V07 an realer Hardware |
| 0.4 / Photonischer Pfad | Ein kalibrierter Aktuator und das angepasste Modell | V10 mit getrennten Kalibrier- und Prüfdaten |
| 1.0 / Definierte Modulfreigabe | Stabile Schnittstellen, Regressionen, Anleitung und begrenzter Betriebsbereich | Alle Pflichtkriterien für den genannten Umfang erfüllt; offene Grenzen publiziert |

Die Versionsnummer allein bezeichnet keinen Reifegrad. Quantencharakterisierung, Mehrkanalbetrieb, Streaming, industrielle Qualifikation und Hochgeschwindigkeits TFLN sind getrennte Erweiterungen. Für sie werden eigene Profile und Abnahmen benötigt.

### Entscheidungen vor der Implementierung

| **Entscheidung**                      | **Bis zur Klärung geltende Regel**                                              |
|---------------------------------------|---------------------------------------------------------------------------------|
| FPGA Board und Wandler                | Keine Bandbreite, Latenz oder Analogauflösung als verfügbar behaupten           |
| Erster Messzweck und Fehlergrenzen    | Zuerst elektrischen Einzelkanal qualifizieren; Grenzwerte vor Messung festlegen |
| Uhr und Messmittel                    | Referenz, Trigger und Kalibrierung vollständig erfassen                         |
| Astrolabium Zielversion               | Aktuellen Code und Datenvertrag prüfen; danach separaten Adapter testen         |
| Photonenwellenlänge und Aktuator      | Keine Kompatibilität aus Materialtransparenz oder Produktfamilie ableiten       |
| Wiederverwendung vorhandener Software | Quellstand, Lizenz, Schnittstelle und Tests pro Baustein dokumentieren          |

### Wissenschaftlich prüfbarer Nutzen

Die erste Forschungsfrage lautet, wie genau sich aus einem gespeicherten Plan der tatsächlich gemessene Verlauf vorhersagen lässt. Weitere Fragen betreffen die Übertragung von Zeitfehlern auf Signalfehler, die Gültigkeitsdauer einer Kalibrierung und den Nutzen einer Driftregelung. Vergleichsläufe benötigen gleiche Randbedingungen, vorab definierte Auswertung und berichtete Unsicherheit.

Ein späterer Beitrag zur Wissenschaft wäre ein nachvollziehbarer Datensatz samt geprüftem Modell und offenem Fehlerbudget. Neue Physik, Quantenvorteil oder eine industrielle Plattform sind kein Ergebnis dieser Konzeptfassung.

## 11 Quellen und Evidenzregister

Interne Dokumente wurden als vorhandene Nachweise gelesen; frühere Tests wurden für diesen Konzeptauftrag nicht erneut ausgeführt. Die externen Quellen begründen einzelne Methoden und Vergleichspunkte. Sie validieren ACVM nicht.

### Interne Ausgangsartefakte

\[I1\] PRUEFBERICHT_DE.md, „PMCS v0.4.4 – technische und wissenschaftliche Prüfung“, 12.10.2026. Status im Bericht: BLOCKED_FOR_SCIENTIFIC_OR_SECURITY_RELEASE. Umfang: synthetische Diagnose, Export- und Kryptographiegegenproben. Der Bericht beschreibt die geprüfte Eingabe mit SHA-256:

c1b6618821ebfa6cc535f3052c104f154f4c92b2f2c37b37b8130e2850d47ce8

\[I2\] reference_results.json, 12.10.2026. Gelesene Diagnoseeinträge zu den in \[I1\] beschriebenen Fehlerklassen. Status: DIAGNOSTIC_OBSERVATIONS_CONFIRMED_NOT_RELEASE_PASS. Keine neue ACVM Testausführung.

\[I3\] X6_v2_1_AUDIT.md, 09.10.2026. Abgegrenzte analytische und numerische Referenzfälle mit ausdrücklich offenen Prüfungen. Historischer Audit, kein Nachweis des aktuellen Gesamtzustands von Astrolabium.

\[I4\] Vom Nutzer bereitgestellter PMCS v0.1 Auszug im Gespräch vom 13.10.2026. Enthält Roadmap und Architekturbegriffe; keine vollständige Implementierung und keine zugeordneten Hardwaremessdaten.

### Externe Primärquellen und Dokumentation

\[R1\] M Labs, ARTIQ Real Time I/O concepts. Referenz für gepufferte Ereignisse, Uhrdomänen und Ausführungsfehler.

https://m-labs.hk/artiq/manual/rtio.html

\[R2\] Stefanazzi et al., The QICK Quantum Instrumentation Control Kit, arXiv:2110.00557. Referenz für FPGA basierte Qubitsteuerung und Charakterisierung.

https://arxiv.org/abs/2110.00557

\[R3\] Capmany und Fernandez Pousa, Quantum Modelling of Electro Optic Modulators, arXiv:1103.4747. Bezug für modenspezifische Quantenbeschreibung.

https://arxiv.org/abs/1103.4747

\[R4\] JCGM, Publikationsverzeichnis beim BIPM, insbesondere GUM und ergänzende Dokumente. Bezug für Messmodelle und Unsicherheiten.

https://www.bipm.org/en/committees/jc/jcgm/publications

\[R5\] Feasibility Study for a Python Based Embedded Real Time Control System, Electronics 12, 1426, 2023. Untersuchte Echtzeitbedingungen sind nicht universell übertragbar.

https://www.mdpi.com/2079-9292/12/6/1426

\[R6\] LIGENTEC, TFLN Modulator Technical Specifications. Herstellerangaben auf Plattformebene; detaillierte Gerätequalifikation bleibt erforderlich.

https://www.ligentec.com/wp-content/uploads/2025/09/TFLN-Modulator-Technical-Specifications.pdf

\[R7\] Yamaguchi et al., OFC 2025, Th4D.4. Zugänglicher Abstract zu einem speziellen TFLN Kommunikationsmodulator; keine Quantenvalidierung von ACVM.

https://doi.org/10.1364/OFC.2025.Th4D.4

Quellenzugriff 13.10.2026. \[R5\] bis \[R7\] wurden im unmittelbar vorausgehenden Prüfauftrag ausgewertet. Die Aussagen dieses Konzepts übernehmen daraus keine Leistungszusage. Verifikation bedeutet Prüfung einer Implementierung gegen ihre Spezifikation; physikalische Validierung bedeutet Prüfung ihrer Vorhersagen im angegebenen Messbereich.
