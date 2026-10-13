# ACVM Experiment Records

*Konzept 0.1*

**Experimentakten und Provenienz für das Astrolabium Control and Validation Module**

Thomas Gfeller · 13. Oktober 2026 · Dokumentkennung ACVM ER C01

ACVM Experiment Records konkretisiert das Run Archive des ACVM-Konzepts 0.1. Es soll Versuchsplan, übersetzte Ansteuerungsdaten, Ausführungsprotokoll, Rohdaten und Auswertung so verbinden, dass jede Aussage auf ihre Eingaben und Prüfkriterien zurückgeführt werden kann. Der erste Entwicklungsgegenstand ist ein portables Versuchspaket mit unabhängigem Leser.

Die Experimentakte bewahrt den Unterschied zwischen geplanter Wirkung, gemeldetem Geräteablauf und tatsächlich gemessener Wirkung. Sie unterstützt die Prüfung einer Aussage; die wissenschaftliche Begründung entsteht durch passende Modelle, Messungen und Auswertungen.

| **Gegenstand**                    | **Status dieser Fassung**                                                 |
|-----------------------------------|---------------------------------------------------------------------------|
| Architektur und Datenvertrag      | Konzept und Anforderungen ausgearbeitet                                   |
| Schema und Implementierung        | Vorgeschlagen; noch nicht als ausführbares Schema oder Software geliefert |
| Adapter zu bestehenden Modulen    | Entworfen; technische Kompatibilität noch zu prüfen                       |
| Prüfungen ER01 bis ER14           | NOT_RUN                                                                   |
| Elektrische oder optische Abnahme | Für diese Erweiterung nicht durchgeführt                                  |

**Leseregel: „muss“ bezeichnet eine Anforderung an die künftige Implementierung. Anforderungen, Beispieldaten und Prüfpläne sind keine bestandenen Nachweise. Frühere Resultate anderer Module behalten ausschliesslich ihren dokumentierten Geltungsbereich.**

### Umfang und Orientierung

Kapitel 2 bis 6 legen Anschluss, Objekte, Paketstruktur, Zustände und Messsemantik fest. Kapitel 7 bis 9 beschreiben Entscheidungen, Integrität und Adapter. Kapitel 10 und 11 enthalten die prüfbaren Anforderungen. Kapitel 12 definiert den ersten Umsetzungsschritt und die offenen Entscheidungen; Kapitel 13 dokumentiert die Quellen.

## 2 Anschluss an die bisherigen Arbeiten

Der Anschluss erfolgt an ACVM 0.1, insbesondere dessen Architektur in Kapitel 3, Ausführungsvertrag in Kapitel 4 und Versuchspaket in Kapitel 5. Experiment Records ist die Daten- und Nachweisschicht des dort vorgesehenen Run Archive. Sequence Compiler, Device Backend, FPGA Sequencer, Acquisition und Validation Engine behalten ihre Aufgaben. \[I1\]

| **Bestandsarbeit**                     | **Übernommener Vertrag**                                                   | **Anschluss dieser Erweiterung**                                           |
|----------------------------------------|----------------------------------------------------------------------------|----------------------------------------------------------------------------|
| ACVM 0.1                               | Experiment Plan, Execution Image, Run ID, Rohdaten und getrennte Prüfungen | Objektidentitäten, Paketversionen und Referenzen präzisieren               |
| Signal Validation Lab                  | Synthetische Referenzen, getrennte Metriken, archivierter Quellenstand     | Unveränderten Export einbetten; synthetische Herkunft erhalten             |
| Sagnac Integration 0.1                 | SGNCv007-Snapshots, exakte Zähler, Originalbytes und deklarierte Herkunft  | Originalformat separat prüfen; Importbefund und Analyse getrennt speichern |
| Photonischer Zwei-Qubit-Versuchsaufbau | Optischer Entwurf, digitale Referenzen und offene Labornachweise           | Pläne und spätere Messungen einem konkreten Aufbau zuordnen                |

Die Referenzstände sind durch den Git-Commit c20c2b306e8785f79a431bdd9becec57acb95cec festgelegt. Die Anschlussbewertung stützt sich auf deren Dokumentation. Bestehende Prüfungen wurden für dieses Dokument nicht wiederholt. \[I1–I4\]

### Verantwortung und Ausführungsgrenze

Astrolabium erstellt oder wählt einen Plan. Der Compiler liefert ein Execution Image samt Übersetzungsbericht. Das Backend meldet Geräteereignisse, Acquisition liefert Erfassungsdaten, und die Validation Engine erzeugt kriterienspezifische Befunde. Experiment Records ordnet diese Objekte zu, prüft ihre strukturelle Konsistenz und archiviert Versionen.

Die Archivierung bestimmt keine Gerätezeit. Datenbankzugriffe, Berichterstellung und Agenten bleiben ausserhalb zeitkritischer FPGA-Abläufe. Ein für die Messung nötiger lokaler Recorder benötigt ein eigenes Speicher- und Durchsatzbudget. Bei drohendem Datenverlust gilt die vorab festgelegte Fehlerreaktion des Geräteprofils.

### Abgrenzung der Erweiterung

Das Konzept spezifiziert keine neue Aktuatorsteuerung, keine neue Quantenoperation und kein allgemeines Binärformat. Die erste Speicherung erfolgt in Dateien. Eine spätere Datenbank dient als durchsuchbarer Index; die exportierbare Experimentakte bleibt der nachvollziehbare Datenbestand.

## 3 Identitäten und Beziehungen

Eine Experimentakte beschreibt eine Fragestellung mit einem oder mehreren Läufen. Ein Lauf ist ein einzelner Ausführungsversuch oder eine ausdrücklich deklarierte Simulation. Eine neue Analyse desselben Laufs erzeugt eine neue Analysekennung. Identität, Revision und Inhaltsbindung erfüllen unterschiedliche Aufgaben.

| **Objekt oder Feld**               | **Verbindliche Bedeutung**                                                                                                            |
|------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| experiment_id                      | Gruppiert die Forschungsfrage und ihre Läufe; ist kein Gütesiegel.                                                                    |
| plan_id und plan_revision          | Identifizieren einen gespeicherten Planstand mit Annahmen und Akzeptanzkriterien.                                                     |
| run_id                             | Kennzeichnet genau einen Versuch. Ein echter Neustart erhält eine neue Kennung; die Wiederholung derselben Übertragungsanfrage nicht. |
| artifact_id und sha256             | Identifizieren ein Datenobjekt und dessen konkrete Bytes. Rollen, Einheiten und Referenzen werden gesondert gebunden.                 |
| analysis_id und review_id          | Kennzeichnen eine Auswertung beziehungsweise Bewertung mit ihren Eingaben und Versionen.                                              |
| package_id und parent_package_hash | Kennzeichnen einen eingefrorenen Paketstand und gegebenenfalls dessen Vorgänger.                                                      |

### Planbindung ohne Zirkelschluss

Ein wiederverwendbarer Planentwurf wird vor dem Lauf als run-spezifische plan.json eingefroren. Damit bleibt die in ACVM 0.1 verlangte run_id im Plan erhalten. Änderungen nach Beginn erhalten eine neue Planrevision und eine begründete Abweichungsnotiz; der tatsächlich verwendete Plan bleibt unverändert verfügbar.

Jeder Befund verweist auf die konkreten Eingabeartefakte und den Kriterienstand. Eine Ableitung darf keine Zyklen enthalten. Externe Referenzen benötigen stabile Identität, Inhaltsbindung und Verfügbarkeitsstatus. Ein fehlendes erforderliches Objekt verhindert die betreffende Prüfung; ein Dateiname allein genügt nicht.

### Herkunft und Evidenzart

evidence_kind wird aus dem ACVM-Vertrag übernommen und je Datenobjekt konkretisiert. Vorgeschlagene Werte sind SIMULATED, SOFTWARE_TEST, ELECTRICAL_MEASUREMENT und OPTICAL_MEASUREMENT. Ein gemischtes Paket enthält mehrere Arten; es wird nicht durch eine einzige Herkunftsangabe aufgewertet. Die Domäne „Quantenexperiment“ wird zusätzlich beschrieben und belegt noch keine Quantenbehauptung.

Die Herkunftsdeklaration nennt, wer sie abgegeben hat und worauf sie beruht. Import, Umbenennung oder Signatur ändern die Evidenzart nicht. Eine beobachtete Inkonsistenz führt zu einem neuen Befund, während die ursprüngliche Deklaration erhalten bleibt. Eine intern konsistente falsche Herkunftsangabe lässt sich durch Schema- und Hashprüfung allein nicht erkennen.

Provenienz wird als Beziehung zwischen Datenobjekten, Verarbeitungsschritten und verantwortlichen Akteuren geführt. Dies ist an W3C PROV anschliessbar; eine formale PROV-Konformität ist noch nicht nachgewiesen. \[R1\]

## 4 Portables Versuchspaket

Die Dateistruktur erweitert das in ACVM 0.1 vorgeschlagene Versuchspaket. Pflichtobjekte hängen vom Paketprofil ab: Ein Entwurf braucht keine erfundenen Messdaten. Ein gemessener Lauf benötigt seine Originaldaten. Nicht anwendbare Objekte werden mit Begründung ausgewiesen. \[I1\]

| **Datei oder Verzeichnis**     | **Inhalt und Bindung**                                                                                     |
|--------------------------------|------------------------------------------------------------------------------------------------------------|
| record.json                    | Schema, Profil, Objektkennungen, Paketstatus, Herkunftsdeklarationen und referenzierte Teilobjekte         |
| plan.json                      | Run-spezifischer Plan, Zielgrössen, Annahmen, zulässige Korrekturen und vorab gespeicherter Kriterienstand |
| device_profile.json            | Bei Gerätebezug: Fähigkeiten, Grenzwerte, Uhrdomänen, Fehlerreaktionen und Kalibrierreferenzen             |
| execution.json und samples.bin | Bei Kompilierung: Zeitraster, Kanalabbildung, Datentyp, Skalierung, Compilerstand und exakte Nutzdaten     |
| build/ und events/             | Übersetzungsbericht, Quellen- und Laufzeitstände sowie unveränderte Geräte- und Erfassungsereignisse       |
| raw/ und calibration/          | Originalmessdaten oder deklarierte Simulationsdaten; gültigkeitsbezogene Kalibrierdatensätze               |
| validation/ und reviews/       | Versionierte Auswertungen, Einzelentscheidungen, Prüfprotokolle und fachliche Bewertungen                  |
| manifest.json                  | Dateipfade, Bytegrössen, SHA-256, Rollen und Paketprofil; nach Abschluss eingefroren                       |

### Vorgeschlagener Schemakontrakt

Für record.json werden schema_id = astrolabium.acvm.records und schema_version = 0.1.0 vorgeschlagen. Der Namensraum erweitert astrolabium.acvm. Die Konzeptversion 0.1 ist keine Softwareversion. Vor Implementierung sind JSON Schema, zulässige Werte, Referenzregeln und Testvektoren vollständig festzulegen.

Der erste Leser akzeptiert nur ausdrücklich unterstützte Schema- und Profilversionen. Erweiterungsfelder liegen in einem eigenen Namensraum. Unbekannte Pflichtmerkmale werden abgewiesen. Eine Migration erzeugt ein neues Artefakt mit Werkzeugversion und Änderungsprotokoll; das Original bleibt erhalten.

### Importgrenzen

Relative Pfade müssen eindeutig sein. Absolute Pfade, übergeordnete Pfadsegmente, doppelte Einträge und Symlinks werden im ersten Profil abgewiesen. Dateizahl, entpackte Grösse und Verschachtelung erhalten begründete Grenzen. Eingebetteter Code wird beim Lesen nicht ausgeführt. Ein vollständig portables Paket enthält alle für die beanspruchte Prüfung erforderlichen Daten.

## 5 Laufzustände und Fehlerbehandlung

Gerätezustand, Paketabschluss und Prüfentscheidung werden in getrennten Feldern geführt. COMPLETE beschreibt den im ACVM-Ausführungsvertrag bestätigten Abschluss einschliesslich der dort geforderten Erfassung. Daraus folgt kein wissenschaftliches PASS. \[I1\]

| **Ebene**              | **Zustände und Bedeutung**                                                                                         |
|------------------------|--------------------------------------------------------------------------------------------------------------------|
| Geräteausführung       | IDLE, LOADED, ARMED, RUNNING, COMPLETE, ABORTED, FAULT; UNKNOWN bei ungeklärter Ausführungslage                    |
| Paketbearbeitung       | DRAFT für Entwurf, OPEN während Ergänzung, SEALED nach Inhaltsbindung; neue Inhalte erzeugen eine neue Revision    |
| Datenvollständigkeit   | COMPLETE, PARTIAL oder UNKNOWN relativ zur eingefrorenen Inventar- und Erfassungsvorgabe                           |
| Einzelprüfung          | NOT_RUN, PASS, FAIL, INVALID, INCONCLUSIVE; NOT_APPLICABLE nur mit sachlicher Begründung                           |
| Herkunft und Vertrauen | Deklaration, Integritätsbefund, Signaturbefund und Schlüsselvertrauen separat; fehlende Bewertung als NOT_ASSESSED |

### Eindeutigkeit unter Störungen

Lade-, Start- und Abbruchereignisse werden an run_id, Befehlssequenz und Execution-Image-Identität gebunden. Ein erneut übertragenes Startkommando darf keinen zweiten Start auslösen. Nach Verbindungsverlust muss zuerst die Ausführungslage geklärt werden. Solange dies nicht gelingt, bleibt sie UNKNOWN; ein vermuteter Erfolg wird nicht eingetragen.

Empfang, Annahme, Start und Abschluss sind unterschiedliche Ereignisse. Hostzeit und Gerätezeit werden jeweils mit ihrer Quelle gespeichert. Die Reihenfolge wird innerhalb einer Quelle durch Sequenznummern bestimmt. Eine globale Reihenfolge darf nur behauptet werden, wenn der Synchronisationsvertrag sie trägt.

### Erhaltung fehlgeschlagener Läufe

Bei Abbruch oder Fehler bleiben bereits gespeicherte Rohbytes, Lücken und letzte bekannte Zustände erhalten. Auch ein PARTIAL-Paket kann eingefroren werden; seine Unvollständigkeit bleibt Bestandteil der Akte. SEALED bestätigt nur einen abgeschlossenen Paketstand, keine vollständige oder gültige Messung.

Neue Eingaben dürfen alte PASS-Anzeigen nicht übernehmen. Auswertungen binden ihre Ergebnisse an die tatsächlich geprüften Eingaben. Eine spätere Korrektur erzeugt eine neue Bewertung mit Verweis auf die ersetzte; der frühere Befund bleibt einsehbar.

Die Reaktion auf Datenträgerfehler, volle Puffer oder unterbrochene Erfassung wird vor dem Lauf im Geräte- und Erfassungsprofil festgelegt. Experiment Records implementiert keine universelle sichere Ausgangsspannung und ersetzt keine gerätespezifische Schutzfunktion.

## 6 Numerik Zeit und Kalibrierung

### Numerische Bedeutung

Jede numerische Nutzdatei deklariert Datentyp, Byte-Reihenfolge, Dimensionen, Kanalreihenfolge, Samplezahl und Einheit. Ganzzahlige DAC-Codes und physikalische Referenzwerte bleiben getrennte Objekte. Skalierung, Offset, Lastkonvention und Übersteuerungsverhalten gehören zur Abbildung. Komplexe Werte erfordern eine explizite I/Q- oder andere Kanalzuordnung.

JSON-Metadaten werden als UTF-8 geführt. Nicht endliche numerische Werte und doppelte Objektschlüssel werden im Profil abgewiesen. Nicht definierte Messgrössen erhalten einen Status mit Begründung, keinen Ersatzwert 0. Grosse Zähler und Gerätezeitmarken werden wie in ACVM 0.1 als Dezimalstrings gespeichert; Präzision darf beim Import nicht verloren gehen. \[I1, R5\]

### Zeitbasis und Beobachtungsbereich

Gerätezeit wird in ganzzahligen Ticks mit exakt beschriebener nominaler Tickdauer, etwa als rationalem Wert in Sekunden, geführt. Zusätzlich werden Uhrkennung, Epoche beziehungsweise Resetbezug, Zählerbreite, Überlaufbehandlung und Synchronisationsmethode erfasst. Die nominale Tickdauer ist von gemessener Frequenzabweichung und Kalibrierunsicherheit zu unterscheiden.

UTC-Zeitstempel mit expliziter Zeitzone beschreiben Archiv- und Bedienereignisse. Sie ersetzen keine präzise Gerätezeit. Gemeinsame Referenzuhren, Kanalversatz, Drift, Jittermodell und Zeitauflösung werden dokumentiert. Fehlende Synchronisation bleibt sichtbar; aus unsynchronisierten Zeitstempeln wird keine scheinbar genaue Latenz berechnet.

### Kalibrierbezug und Modellparameter

Ein Kalibrierobjekt benennt Messgrösse, Methode, Referenz, Gerät und Konfiguration, Zeitpunkt, Gültigkeitsbedingungen, Unsicherheiten und Originaldaten. Ein Kalibrierbezeichner allein belegt weder Gültigkeit noch metrologische Rückführbarkeit. Die Zuordnung wird für den Zeitpunkt und Betriebsbereich des Laufs geprüft.

Die Zeit-, Übertragungs-, Verlust- und Driftmodelle aus ACVM 0.1 werden durch Modellkennung, Version und Parameterreferenzen eingebunden. Jeder Parameter trägt Einheit, Herkunft, Gültigkeitsbereich und gegebenenfalls Kovarianzen. Gemessene Parameter und synthetische Annahmen bleiben unterscheidbar. Es wird kein konkurrierendes physikalisches Modell eingeführt. \[I1\]

Kalibrierdaten und Daten zur unabhängigen Prüfung müssen getrennt bezeichnet werden. Eine nachträgliche Anpassung an Prüfdaten wird als explorative Neuauswertung protokolliert. Unsicherheitsmodelle berücksichtigen auch systematische Beiträge und relevante Abhängigkeiten. Eine geforderte Abdeckung oder Rückführbarkeit benötigt passende Nachweise. \[R3, R4\]

## 7 Prüfentscheidungen und Aussagegrenzen

Jede Prüfung beantwortet eine begrenzte Frage. Strukturelle Gültigkeit, Datenintegrität, Reproduzierbarkeit einer Berechnung, Geräteverhalten und wissenschaftliche Aussage werden separat berichtet. Ein globaler Qualitätsscore darf keinen fehlenden Pflichtnachweis ausgleichen. \[I1\]

| **Prüfbericht enthält**   | **Bedeutung**                                                                         |
|---------------------------|---------------------------------------------------------------------------------------|
| claim_id und criterion_id | Konkrete Aussage und zuvor festgelegtes Kriterium mit Versionsbezug                   |
| scope und input_refs      | Geltungsbereich sowie Identität und Hash aller verwendeten Eingaben                   |
| method und implementation | Methode, Softwarestand, Laufzeitumgebung und verwendete Referenz                      |
| result und uncertainty    | Wert mit Einheit; Intervallart, Abdeckung und Unsicherheitsannahmen, soweit anwendbar |
| decision und reason       | Einzelstatus, Entscheidungsregel, Abweichungen und Einschränkungen                    |
| execution_record          | Ausführungszeit, Protokoll und Identität des Prüfprozesses                            |

### Entscheidungsregeln

PASS setzt gültige Pflichtdaten und die Erfüllung des konkreten Kriteriums voraus. FAIL bezeichnet dessen nachgewiesene Verletzung. INVALID bezeichnet fehlende Voraussetzungen, beispielsweise unlesbare Pflichtdaten oder einen ungeklärten Einheitenvertrag. INCONCLUSIVE bezeichnet einen mit zulässigen Daten nicht eindeutigen Befund. NOT_RUN darf niemals als bestanden gezählt werden.

Für eine obere Fehlergrenze kann die in ACVM beschriebene konservative Regel verwendet werden: PASS, wenn das gesamte deklarierte Unsicherheitsintervall unterhalb der Grenze liegt; FAIL, wenn es vollständig oberhalb liegt; sonst INCONCLUSIVE. Der Umgang mit Gleichheit, Intervallart und Abdeckung wird vorab festgelegt. Andere Regeln benötigen eine ausdrückliche Begründung. \[I1\]

### Reproduktion und unabhängige Referenz

Ein numerisches Replay benennt Quellenstand, Abhängigkeiten, Zufallsalgorithmus, Seed, Initialzustand und Ziehungsreihenfolge. Bitidentische Wiederholung und Übereinstimmung innerhalb einer Numeriktoleranz sind verschiedene Verträge. Stochastische Hardwareereignisse werden nicht durch einen Softwareseed reproduziert.

Eine unabhängige Referenz benötigt ein begründetes Mass an methodischer oder implementativer Unabhängigkeit, etwa eine analytische Lösung oder einen separat implementierten Leser. Zwei Aufrufe desselben Kerns sind kein unabhängiger Gegencheck. Ein erfolgreiches Replay kann einen Modellfehler wiederholen.

Ein Referenzpaket stützt nur die geprüften Aussagen unter seinen Bedingungen. Eine klassische Signalmessung liefert keine Quantengatterfidelität. Die Bewertung von Verschränkung oder Quantenoperationen benötigt einen eigenen Mess- und Auswerteplan. Validierung bleibt an einen vorgesehenen Einsatz gebunden. \[R3\]

## 8 Integrität Provenienz und Archivierung

### Vollständige Inhaltsbindung

Das Manifest erfasst alle für den jeweiligen Paketstand einbezogenen Dateien mit relativen Pfaden, Grössen, Rollen und vollständigen SHA-256-Werten. Es wird nach der finalen Speicherung erzeugt und dann eingefroren. Es listet sich selbst und eine abgetrennte Signatur nicht rekursiv. Beim Lesen werden alle erforderlichen Dateien vollständig geprüft.

Execution Image und Auswertung brauchen ebenfalls vollständige Inhaltsbindung: Metadaten, Skalierungen, Kanalabbildung und Nutzdaten gehören zusammen. Für ein mehrteiliges Image wird ein eigenes Manifest über genau diese Bestandteile gebildet. Sein Bytehash ist die Execution-Image-Identität; es enthält diesen eigenen Hash nicht. Geräteberichte verweisen auf die Identität oder dokumentieren die begrenzte Bindungsmöglichkeit des Backends.

Der Paketstand wird durch den Hash der exakten manifest.json-Bytes referenziert. Umformatierung erzeugt andere Bytes und damit einen neuen Stand. Ein optionaler Signaturmechanismus bindet genau diese Bytes. Vor seinem Einsatz sind Algorithmus, Schlüsselzuordnung, Schlüsselverwaltung, Widerruf und Prüffehler festzulegen. Integrität ist kein Beweis der Messwahrheit. \[R6\]

### Nachvollziehbare Änderungen

Spätere Analysen oder Reviews erzeugen eine neue versiegelte Paketrevision oder einen separat gebundenen Ergänzungsdatensatz. Vorgängerhash und Änderungsgrund bleiben erhalten. Ein Dateisystem oder eine Datenbank kann Änderungen technisch weiterhin erlauben; die Bezeichnung SEALED allein macht einen Speicher nicht unveränderlich.

Hashketten können Änderungen relativ zu einer erhaltenen Referenz sichtbar machen. Ohne unabhängig bewahrten Bezug verhindern sie keine vollständige Umschreibung der Historie. Der erste Entwicklungsumfang zielt auf das Erkennen versehentlicher Beschädigung und Zuordnungsfehler; Schutz gegen böswillige Änderung benötigt ein gesondertes Bedrohungsmodell und passende Kontrollen.

### Dauerhafte Verfügbarkeit

Ein Paket wird zunächst in einem temporären Ziel vollständig geschrieben, geprüft und erst danach als geschlossen veröffentlicht. Ein unterbrochener Schreibvorgang bleibt erkennbar offen. Der Index darf aus den Paketen neu aufgebaut werden. Wiederherstellung aus einer getrennten Sicherung muss die erwarteten Dateien und Hashwerte reproduzieren.

Originaldaten werden nicht durch gerundete Ansichten ersetzt. Aufbewahrungsdauer, Speicherbedarf, Zugriffsrechte und Exportumfang sind pro Betrieb festzulegen. Für öffentliche Pakete werden Rechte und notwendige personenbezogene Angaben geprüft. Eine bereinigte Veröffentlichung erhält eine eigene Ableitung mit dokumentierten Auslassungen.

Ein späterer Export nach Workflow Run RO-Crate kann Eingaben, Ausgaben und Verarbeitungsschritte beschreiben. Profilversion und Validierung dieses Exports sind eigene Implementierungsaufgaben; die erste ACVM-Akte behauptet keine automatische RO-Crate-Konformität. \[R2\]

## 9 Adapter Auswertung und Review

### Importadapter als getrennte Komponenten

Ein Adapter erhält ein Originalartefakt, dokumentiert Quellformat und Quellversion, prüft dessen vereinbarte Regeln und erzeugt eine neue Zuordnung. Originalbytes, Parser-Version, Warnungen und Adapterbericht bleiben erhalten. Eine Übersetzung von Feldern enthält eine explizite Zuordnungstabelle; nicht verlustfrei darstellbare Information wird als Original mitgeführt.

Für das Signal Validation Lab bleibt die synthetische Herkunft erhalten. Ein dort berichteter Replaybefund wird als Quellbefund importiert. Die Erweiterung erklärt ihn erst nach einer eigenen ausgeführten Prüfung zum eigenen Ergebnis. Quellenstand, vollständige Daten und die jeweils gültigen Numeriktoleranzen müssen zusammenpassen. \[I2\]

Für Sagnac bleibt SGNCv007 ein Snapshotformat. Ein Record-Adapter ergänzt weder Einzelphoton-Zeitmarken noch einen Aktuatorvertrag. Exakte Zähler, Sequenz- und Fehlerangaben, Kalibrierbezug und Originalbytes werden erhalten. Der Herkunftswert „hardware“ bleibt eine Deklaration. CHSH-Annahmen und die Trennung bedingter von allen Versuchen werden übernommen; eine physikalische Quantenbehauptung bleibt ohne eigenen Nachweis NOT_ASSESSED. \[I3, I4\]

### Faire Vergleiche und Auswertungsplanung

Benchmarks speichern Aufgabe, Datenaufteilung, Vergleichsverfahren, Metriken, Parameterwahl und Rechenbudget. Explorative Optimierung und anschliessende Prüfung werden getrennt. Alle gemäss Plan relevanten Läufe einschliesslich Abbrüchen und negativen Befunden bleiben verfügbar. Änderungen von Ausschlussregeln und Mehrfachvergleiche werden offengelegt.

Ein Benchmarkbericht beschreibt den tatsächlich untersuchten Bereich. Ein günstiger Einzelfall belegt keine allgemeine Überlegenheit. Unterschiede zwischen Geräten, Kalibrierungen oder Stichproben werden nicht durch einen gemeinsamen Rangwert verdeckt.

### Automatisierte Hilfe und fachliche Verantwortung

Deterministische Prüfer können Schemas, Referenzen und definierte Gegenbeispiele prüfen. Sprachmodellgestützte Agenten können Befunde erläutern oder Hinweise vorschlagen. Ihre Ausgaben werden als eigene Reviewobjekte mit Modellkennung, Zeitpunkt, relevanten Eingaben und Werkzeugprotokollen gespeichert. Vertrauliche Inhalte werden nicht allein zur Vollständigkeit öffentlich exportiert.

Ein Agentenkommentar setzt keinen Prüfstatus auf PASS und löst keinen Gerätebefehl aus. Ausgeführte Tests stammen aus einem benannten Prüfprozess. Ein fachlicher Review nennt die geprüften Aussagen, Einwände und die verantwortliche Instanz. Mehrere Agenten gelten ohne begründete Unabhängigkeit nicht als unabhängige Gutachten.

Berichte werden aus einem festgelegten Paketstand erzeugt. Tabellenwerte und Aussagen müssen auf konkrete Befunde zurückführen. Ein exportierter Bericht ist ein überprüfbares Arbeitsprodukt; wissenschaftliche Begutachtung oder industrielle Freigabe sind damit nicht erteilt.

## 10 Anforderungen und Abnahme der Datenkette

ER R01 bis ER R14 sind Anforderungen dieser Erweiterung. ER01 bis ER14 sind die zugehörigen geplanten Abnahmeprüfungen. Alle stehen auf NOT_RUN. Die ACVM-Prüfungen V01 bis V10 behalten ihre Kennungen und ihren eigenen Geltungsbereich. Records-Prüfungen ersetzen keine Geräteprüfung. \[I1\]


| Anforderung und Test | Prüffall | Erwarteter Befund |
| --- | --- | --- |
| ER R01 / ER01 / Schema und Profil | Unbekannte Version, fehlende Pflichtfelder, unbekanntes Pflichtmerkmal und doppelte JSON-Schlüssel | Definierte Abweisung; kein stilles Auffüllen oder Umdeuten. |
| ER R02 / ER02 / Numerik und Einheiten | Zähler 9007199254740993; falsche Einheit; nicht endlicher Wert; fehlender Messwert | Zähler bleibt exakt; unzulässige Daten sind INVALID; fehlend wird nicht als 0 behandelt. |
| ER R03 / ER03 / Identität und Herkunft | Im bekannten Testpaket Skalierung oder Evidenzart ändern; fremde run_id eintragen | Geänderte Semantik verändert Bindung; Konflikte zur Referenz werden sichtbar; keine automatische Aufwertung. |
| ER R04 / ER04 / Vollständige Bindung | Ein Sample nach Index 256 ändern; Metadatum ändern; Datei kürzen oder entfernen | Gesamte betroffene Inhaltsbindung schlägt fehl; ursprüngliches PASS wird nicht weiterverwendet. |
| ER R05 / ER05 / Unabhängiges Lesen | Referenzpaket mit separat implementiertem Leser öffnen und Daten rekonstruieren | Identitäten, Einheiten, Reihenfolge und Nutzdaten stimmen mit festgelegter Referenz überein. |
| ER R06 / ER06 / Laufzuordnung | Doppelten Start, verspätete Antwort, Abbruch und unklare Geräteverbindung nachstellen | Kein doppelter Lauf; keine falsche COMPLETE-Zuordnung; Teilinformationen bleiben erhalten. |
| ER R07 / ER07 / Uhren und Lücken | Uhrreset, Zählerüberlauf, Sequenzlücke und zwei unsynchronisierte Quellen | Lücke oder Unsicherheit ausgewiesen; keine erfundene Reihenfolge oder präzise Latenz. |


### Prüfaufbau und Nachweise

Testvektoren, erwartete Befunde und ausführende Versionen werden vor dem Lauf gespeichert. Fehler werden an Kopien absichtlich eingebracht. Ein erfolgreicher Negativtest bedeutet, dass der Fehler erkannt wurde. Er bedeutet nicht, dass das beschädigte Paket als gültig angenommen wurde.

ER06 prüft zuerst die Zuordnungslogik mit einem Gerätemodell. Der Nachweis am wirklichen Backend bleibt Bestandteil der ACVM-Prüfungen V06 und V07. Protokolllogik, Softwaretest und physischer Geräteversuch werden getrennt berichtet.

## 11 Anforderungen an Entscheidung und Betrieb


| Anforderung und Test | Prüffall | Erwarteter Befund |
| --- | --- | --- |
| ER R08 / ER08 / Kalibriergültigkeit | Falsches Gerät, unpassender Betriebsbereich oder fehlende Kalibrierunterlage | Kalibrierabhängige Entscheidung wird blockiert oder INVALID; Originaldaten bleiben erhalten. |
| ER R09 / ER09 / Entscheidungssemantik | Grenzfall am Limit, überlappendes Intervall, fehlende Pflichtdaten, NOT_RUN | Erwartete Einzelstatus; keine Zusammenfassung, die eine fehlende Prüfung als Erfolg zählt. |
| ER R10 / ER10 / Rechenreproduktion | Festgelegter Lauf mit archiviertem Build; danach gezielt andere Implementierung oder Parameter | Passender Replayvertrag erfüllt; Abweichung oder unpassender Stand ausdrücklich gemeldet. |
| ER R11 / ER11 / Unveränderte Quellen | Quellpaket importieren, erneut ausgeben und neue Auswertung ergänzen | Originalbytes unverändert; neuer Analyse- und Paketstand mit vollständigen Referenzen. |
| ER R12 / ER12 / Abbruch und Restore | Schreibvorgang unterbrechen, Sicherung wiederherstellen, Index neu erzeugen | Offenes Paket wird nicht SEALED; Restore stimmt mit Referenzinventar überein. |
| ER R13 / ER13 / Begrenzter Import | Pfadtraversierung, doppelte Pfade, übergrosse Datei und eingebettete ausführbare Inhalte | Abweisung innerhalb definierter Ressourcenlimits; keine Codeausführung oder Schreibwirkung ausserhalb des Ziels. |
| ER R14 / ER14 / Review und Bericht | Agententext fordert PASS; Bericht stammt aus alter Revision; Quelldaten fehlen | Kein unbegründeter Statuswechsel; Revision sichtbar; fehlende Belege und Einschränkungen werden mit exportiert. |


### Zuordnung zum ACVM-Prüfplan

ER01 bis ER04 und ER07 konkretisieren Datenaspekte von ACV 01 bis ACV 03 sowie V01, V05 und V06. ER06 ergänzt die Protokollierung von ACV 04 bis ACV 07 und V07. ER08 und ER09 bewahren Voraussetzungen und Grenzen von V09 und V10. ER10 unterstützt die dokumentierte Wiederholung der einschlägigen Software- und Modellprüfungen. Keine dieser Beziehungen überträgt ein PASS von einem Test auf einen anderen.

### Abnahmeumfang

Der erste Softwaremeilenstein verlangt ER01 bis ER14 für das festgelegte Offlineprofil. Tests mit Gerätebezug verwenden dort ein ausdrücklich bezeichnetes Gerätemodell. Eine Freigabe nennt Paketprofil, Implementierungsstand, Umgebung, tatsächlich ausgeführte Fälle und Restgrenzen.

Eine spätere Signaturfunktion erhält zusätzlich eigene kryptografische Testvektoren und Fehlerfälle für falsche, unbekannte oder widerrufene Schlüssel. Mehrbenutzerbetrieb, Nebenläufigkeit, Langzeitverfügbarkeit und echte Hardware benötigen erweiterte Abnahmepläne. Sie sind durch den ersten Offlineumfang nicht abgedeckt.

## 12 Erster Referenzlauf und Umsetzung

### Pilot als Erweiterung von D01

Der erste Records-Pilot dokumentiert den in ACVM 0.1 vorgesehenen Software-Referenzversuch D01. Die Sequenz enthält die dort beschriebenen Referenzanteile und eine eindeutige Zeitmarke. Das Pilotprofil bleibt SIMULATED und benötigt zunächst kein Board. \[I1\]

- Vorbereiten: Plan, Kriterien, Compilerkonfiguration und Referenzverfahren versionieren. Eingaben und erwartete Negativbefunde vor der Prüfung speichern.

- Erzeugen: Execution Image und Compilerbericht erstellen; Originaldaten und Metadaten vollständig an den Lauf binden.

- Prüfen: Einen unabhängigen Leser einsetzen, ER01 bis ER14 ausführen und gezielt beschädigte Kopien als Negativfälle verwenden.

- Reproduzieren: Paket in einer frischen, dokumentierten Umgebung lesen; Ergebnisse nach dem vereinbarten numerischen Vertrag vergleichen.

- Archivieren: Einen abgeschlossenen und einen absichtlich abgebrochenen Lauf exportieren, wiederherstellen und mit allen Einschränkungen berichten.

**Für diesen Konzeptauftrag wurde dieser Pilot nicht ausgeführt. Ein späterer Bericht muss seine tatsächlichen Ergebnisse enthalten; die hier beschriebenen Erwartungen dürfen nicht als Mess- oder Testergebnis übernommen werden.**

### Entwicklungsstufen mit Abschlussbedingungen

| **Stufe**            | **Liefergegenstand**                                         | **Abschlussbedingung**                                                |
|----------------------|--------------------------------------------------------------|-----------------------------------------------------------------------|
| Konzept 0.1          | Dieses Daten- und Nachweiskonzept                            | Fachliche Prüfung; keine Softwarefreigabe                             |
| Offlineprofil        | Schema, Beispieldaten, Writer, unabhängiger Leser und Prüfer | Dokumentierte Ergebnisse ER01–ER14 für den definierten Umfang         |
| Bestandsadapter      | Je ein Importpfad für Signal Lab und Sagnac                  | Originalerhalt, explizite Feldzuordnung und separat geprüfte Semantik |
| Gerätebetrieb        | Ein ausgewähltes Backend mit echter Erfassung                | ACVM V09 sowie relevante Fehlerprüfungen an der Hardware              |
| Photonischer Betrieb | Passende Kalibrierung, Modell und neue Messläufe             | ACVM V10 und ein begrenzter, belegter Gültigkeitsbereich              |

Vor der Implementierung bleiben konkret festzulegen: das erste Nutzdatenprofil, Kennungsvergabe, Numeriktoleranzen, Importlimits, Aufbewahrungsdauer und Referenzumgebung. Für Hardware kommen Board, Uhr, Messmittel und Fehlergrenzen hinzu. Diese offenen Parameter dürfen nicht durch frei gewählte Leistungszusagen ersetzt werden.

Der Nutzen wird am Aufwand für Wiederholung, Vollständigkeit der Datenzuordnung und Erkennung gezielt eingebrachter Fehler geprüft. Eine neue Physik, ein Quantenvorteil oder industrielle Betriebsreife wird aus der Dokumentationskette nicht abgeleitet.

## 13 Quellen und Dokumentkontrolle

Interne Referenz: Repository x6-spectral-astrolabium, Commit c20c2b306e8785f79a431bdd9becec57acb95cec. Die folgenden Links zeigen auf diesen eingefrorenen Stand. Die Dokumente begründen den Anschluss; frühere Ergebnisse werden nicht als neue Records-Abnahme übernommen.

[\[I1\] Astrolabium Control and Validation Module, Konzept 0.1. Kapitel 3 bis 10: Architektur, Paket, Modell und Prüfplan.](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c20c2b306e8785f79a431bdd9becec57acb95cec/docs/acvm/ACVM_CONCEPT_v0_1_DE.md)

[\[I2\] Signal Validation Lab. Datenexport, Reproduktion und Grenzen synthetischer Signalvergleiche.](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c20c2b306e8785f79a431bdd9becec57acb95cec/docs/SIGNAL_VALIDATION_LAB.md)

[\[I3\] Sagnac Integration 0.1. SGNCv007, Erfassung, Deklarationen und offene Gerätequalifikation.](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c20c2b306e8785f79a431bdd9becec57acb95cec/docs/SAGNAC_INTEGRATION.md)

[\[I4\] Photonischer Zwei-Qubit-Versuchsaufbau. Entwurf, digitale Referenzen und Status der Labornachweise.](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c20c2b306e8785f79a431bdd9becec57acb95cec/experiments/photonic-two-qubit/README.md)

### Externe methodische Referenzen

[\[R1\] W3C, PROV-DM, Recommendation vom 30. April 2013. Begriffe für Entitäten, Aktivitäten, Ableitungen und Verantwortlichkeit.](https://www.w3.org/TR/2013/REC-prov-dm-20130430/)

[\[R2\] Workflow Run RO-Crate Profile Collection. Profile für Provenienz von Rechenläufen; mögliche Exportanbindung.](https://www.researchobject.org/workflow-run-crate/profiles/)

[\[R3\] JCGM 200:2012, International Vocabulary of Metrology. Insbesondere Unsicherheit, Kalibrierung, Verifikation und Validierung.](https://www.bipm.org/documents/20126/2071204/JCGM_200_2012.pdf)

[\[R4\] JCGM, Guide to the Expression of Uncertainty in Measurement und ergänzende Publikationen. Bezug für Messmodelle und Unsicherheitsbilanz.](https://www.bipm.org/en/committees/jc/jcgm/publications)

[\[R5\] IETF, RFC 8259, Dezember 2017. JSON-Syntax und Grenzen interoperabler numerischer Darstellung. Das Records-Profil legt zusätzliche Ablehnungsregeln fest.](https://www.rfc-editor.org/rfc/rfc8259)

[\[R6\] NIST, FIPS 186-5, Digital Signature Standard, 2023, mit veröffentlichten Korrekturhinweisen. Bezug für den begrenzten Zweck digitaler Signaturen.](https://csrc.nist.gov/pubs/fips/186-5/final)

Quellenzugriff und Dokumentstand: 13. Oktober 2026. Die methodischen Referenzen belegen keine Konformität oder Zertifizierung dieser Erweiterung. Ein späterer standardbezogener Export oder Signaturdienst benötigt eine eigene Spezifikation und Prüfung.

### Änderungskontrolle

Dokumentkennung ACVM ER C01 · Konzeptversion 0.1 · Erste Fassung. Der technische Namensraum ist vorgeschlagen. Änderungen an Objektsemantik, Statusbedeutung oder Pflichtfeldern erfordern eine neue dokumentierte Revision und passende Migrationstests. Die ACVM-Basisfassung bleibt als eigenständige Referenz erhalten.
