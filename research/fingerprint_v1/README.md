# X6: Messpipeline und mehrschichtiger Fingerprint v1.0.0

**Ziel:** X6 sammelt definierte Observablen, erkennt verbleibende Mehrdeutigkeit und wählt eine weitere zulässige Beobachtung. Das Ergebnis ist ein nachvollziehbarer Trennungsbefund innerhalb eines registrierten Vergleichsraums. Ein ungelöster Fall ist ein gültiges Ergebnis.

Diese Lieferung enthält die Messspezifikation, zwei JSON-Schemas, einen Validator, zwei aus dem vorhandenen n=6-Atlas erzeugte Fingerprints, deren überprüfbares Vergleichsereignis und einen ausdrücklich ungemessenen Laborplan. Automatische Sensorsteuerung, ein empirischer Entscheidungsalgorithmus und physikalische Validierung sind noch nicht implementiert.

## 1. Zwei Ausführungsprofile

| Profil | Eingabe | Minimale Sensorik | Zulässiger Befund |
|---|---|---|---|
| `CAUSAL_ORDER_EXACT` | Strikte transitive Kausalmatrix C, Operatorrezepte, Vergleichskorpus | **Keine physischen Sensoren**; exakte Rechenoperatoren sind die virtuellen Messkanäle | Gleichheit oder Trennung registrierter Invarianten endlicher Ordnungen |
| `SIGNAL_SINGLE_POINT` | Eine kalibrierte Zeitreihe | **1 Antwortsensor + getakteter ADC** mit Anti-Aliasing | Lokales Leistungsspektrum und zeitliche Autokorrelation; eingeschränkte Identifizierbarkeit |
| `MODAL_2R1F` | a₁(t), a₂(t), F(t), gemeinsame Zeitbasis, bekannte Positionen und Achsen | **2 Beschleunigungssensoren + 1 Kraftsensor; 3 synchrone ADC-Kanäle**; kontrollierte Anregung | Räumlich abgetastete Antwort, Kreuzkorrelation, Übertragungsfunktionen und eingeschränkte Modenhinweise |
| `DISPERSION_SPATIAL` | Antworten an mehreren bekannten Positionen, Anregungsreferenz und Ausbreitungsmodell | Für den vorgesehenen Ausbau **mindestens 3 räumliche Antwortpositionen + Kraftreferenz**, also 4 synchrone Kanäle bei fester Bestückung | Modellgebundene Schätzung eines Ausbreitungszweigs, sofern räumliches Aliasing und Reflexionen beherrscht werden |

Die letzte Zeile ist ein Entwurf für einen eindimensionalen, dominanten Ausbreitungszweig, kein allgemeiner Vollständigkeitssatz. Zwei Positionen können unter starken Vorannahmen genügen, lassen die Phase aber zunächst modulo 2π offen. Auch drei Positionen garantieren bei mehreren Zweigen oder Reflexionen keine eindeutige Dispersion. Ein versetzbarer Antwortsensor spart Hardware, verlangt jedoch reproduzierbare Anregung, eine feste Referenz und kontrollierte Zustandsänderungen.

Für den ersten physischen Trennungsversuch ist **MODAL_2R1F** die vorgeschlagene Mindestkonfiguration. Ein einzelner triaxialer Sensor liefert mehrere Richtungen am selben Ort und ersetzt keine zwei räumlichen Positionen. Ein Shaker oder instrumentierter Impulshammer stellt die Anregung bereit; der Kraftkanal misst den tatsächlich eingebrachten Eingang. Drehzahlsensoren werden erst für Winkel-/Ordnungsanalyse an rotierenden Systemen notwendig, Temperaturkanäle bei einer entsprechenden Drift- oder Zustandsfrage.

Die NI-Dokumentation beschreibt die experimentelle Modalprüfung über gemessene Anregung und Antwort sowie die Ableitung von Frequenz, Dämpfung und Modenform aus Übertragungsfunktionen [1]. Die hier gewählte Kanalzahl ist ein begrenzter X6-Pilotentwurf und keine Zusicherung, alle Moden beobachten zu können.

## 2. Die konkrete Messschleife

| Schritt | Operation | Ergebnis und Gate |
|---|---|---|
| 0 — Registrieren | Objekte, Hypothesen/Kandidaten, Operatoren, Einheiten, Zustand, Geometrie, Invarianzen, Bandbreite und Budget festlegen. Vergleichsprotokoll versionieren und hashen. | Derselbe Definitionsraum für beide Objekte; sonst `INCOMPARABLE` im Steuerungsablauf, kein Vergleichsereignis mit Trennungsurteil. |
| 1 — Erfassen | Exakt: C einlesen. Physisch: rohe synchrone Kanäle, Kalibrierung, Positionen, Anregung und Betriebszustand sichern. | Unveränderte Rohdaten und Quellartefakte mit SHA-256; Hash belegt Inhaltsbindung, keine Echtheit. |
| 2 — Qualität prüfen | Exakt: binär, irreflexiv, transitiv, richtige Dimension; unabhängige Rechenprüfung. Physisch: Clipping, Ausfälle, Zeitversatz, Kalibrierung, Anti-Aliasing, Eingangssignal und Wiederholbarkeit prüfen. | `PASS` erlaubt Merkmalsextraktion. Fehlende Voraussetzung führt zu `INVALID` oder `NOT_MEASURED`, niemals zu Nullwerten. |
| 3 — Basismessung | Zunächst Spectrum; Degeneracy daraus ableiten, soweit bestimmt. | Ein vollständiger Fingerprint enthält alle sieben Ebenen, einschliesslich ihrer Verfügbarkeitsstatus. |
| 4 — Mehrdeutigkeit erkennen | Exakt definierte Merkmalswerte vergleichen; bei empirischen Daten den registrierten Abstand samt Unsicherheit auswerten. | `EXACT_COLLISION`, `OBSERVATIONALLY_UNRESOLVED`, `SEPARATED` oder `INCONCLUSIVE`, jeweils relativ zum Merkmalsumfang. |
| 5 — Nächste Observable wählen | Nur anwendbare, noch nicht gemessene Kandidaten zulassen. Erwartete Verringerung ungetrennter Paare durch Kosten teilen. Ohne belastbares Vorhersagemodell eine vorab festgelegte günstige Reihenfolge verwenden. | Auswahlgrund, erwarteter Nutzen, Kosten und Voraussetzungen protokollieren. Eine gewählte Observable muss nicht trennen. |
| 6 — Nachmessen und verfeinern | Weitere Berechnung oder registrierte Messkonfiguration ausführen. Alte Evidenz behalten, neue hinzufügen. | Kumulativer Umfang Fₜ₊₁ = Fₜ ∪ {Oₜ₊₁}; jeder bestätigte Trennungsbefund nennt eine konkrete Zeugenobservable. |
| 7 — Bestätigen und stoppen | Exakt: unabhängige Berechnung bzw. überprüfte Quelle. Empirisch: nach der adaptiven Auswahl unberührte Bestätigungsdaten und registrierte Fehlerkontrolle. | Stopp bei Trennung im definierten Raum, Budgetende oder fehlender zulässiger Observable. Physikalische Äquivalenz bleibt `NOT_ASSESSED`. |

Rechenzeit, Messdauer und Umbaukosten werden vor Auswahl in einer gemeinsamen Kostenfunktion gewichtet. Ohne solche Gewichte ist ein angeblich „optimaler“ nächster Sensor nicht begründet. Das Beispiel verwendet eine feste Reihenfolge und erhebt keinen Anspruch auf optimale adaptive Auswahl.

Bei einem **exakten** Merkmalsvektor definiert Gleichheit eine Äquivalenzrelation und zusätzliche Observablen verfeinern deren Klassen. Die Regel „Abstand ≤ ε“ ist im Allgemeinen nicht transitiv. Empirische Ununterscheidbarkeit wird deshalb als Paarbefund mit Unsicherheit geführt, nicht als automatisch wohldefinierte Äquivalenzklasse. Ein empirischer Algorithmus darf Kandidaten revidieren; monotone Klassenverfeinerung gilt unmittelbar nur für fehlerfrei bestimmte Invarianten.

## 3. Minimal notwendige Messgrössen je Ebene

| Ebene | Exakter Lorentz-Pfad | Physischer Pilot | Voraussetzung / Grenze |
|---|---|---|---|
| **Spectrum** | Vollständige charakteristische Polynome von S=C+Cᵀ, A=C−Cᵀ, K=SA−AS, später S₂=C²+(C²)ᵀ; dimensionslos | Einseitige PSD Gₐᵢₐᵢ(f), Einheit (m/s²)²/Hz; Resonanzen f in Hz | Operator, Normierung bzw. Fenster, Spektralschätzer, Band und Auflösung müssen feststehen. Eine PSD ist kein vollständiges Operatorspektrum. |
| **Degeneracy** | Algebraische Vielfachheiten sind bereits im vollständigen charakteristischen Polynom enthalten | Nur auflösbare Mehrfachmoden unter einem identifizierbaren Modalmodell | Zwei Peaks oder ein breiter Peak beweisen keine exakte Entartung. Nicht doppelt als unabhängige Evidenz zählen. Kollision verschiedener Objekte ist ein separates Vergleichsereignis. |
| **Sector** | Z. B. minimale/maximale Elemente, Isolierte, gepaarte gerichtete Gradverteilung | Vorab definierte Symmetrie, Polarisation oder Anregungs-/Antwortklasse | Kein zusätzlicher Universalsensor. Strukturmerkmale sind keine automatisch bestätigten physikalischen Symmetriesektoren. |
| **Mode structure** | Projektorinvarianten, z. B. tr(PλQμ) für zwei festgelegte Operatoren | Komplexe relative räumliche Antwort oder abgetastete Modenform mit Sensorpositionen; dimensionslos nach deklarierter Normierung | Eigenvektorvorzeichen, Phasen und Basen in entarteten Unterräumen sind nicht eindeutig. Zwei Positionen liefern keine vollständige Modenform. |
| **Correlation** | Definierte Feld-/Strukturobservablen und Zustand/Ensemble erforderlich | R₁₂(τ), Kreuzspektrum G₁₂(f), Kohärenz γ²(f); τ in s, Kohärenz dimensionslos | Mittelwertabzug, Ensemble, Stationarität und Schätzer deklarieren. Klassische Sensorkorrelation ist keine Wightman-Funktion. |
| **Dispersion** | Nur mit zusätzlicher Geometrie-/Impulsdefinition und Ausbreitungsmodell | k(f) in rad/m und ω=2πf in rad/s; ggf. Phasen-/Gruppengeschwindigkeit in m/s | Ein Resonanzpeak ergibt keine Dispersion. Geometrie, Zweig, Phasenentfaltung, Reflexionen und räumliches Aliasing prüfen. |
| **Dynamics** | Definierter Evolutionsoperator, Anfangs-/Randbedingungen oder ausdrücklich kombinatorisches Probeverfahren | Hᵢ(f)=G_Faᵢ/G_FF in (m/s²)/N, Impulsantwort, Abklingrate in 1/s und Dämpfungsverhältnis | Gemessener Eingang und ausreichende Anregung nötig. Eine Quill-Anfügung ist eine kombinatorische Intervention und keine nachgewiesene physikalische Zeitentwicklung. |

Für Projektoren muss die Konstruktion unter gemeinsamer Umnummerierung invariant sein. Bei numerisch beinahe entarteten Eigenwerten wird zunächst die Cluster-/Unterraumdefinition festgelegt; ein Solver-Basiswechsel gilt nicht als Trennung. Für empirische Modenvergleiche müssen Messpositionen, Referenzphase und inneres Produkt übereinstimmen.

Die Lorentz-Literatur untersucht Spektren mehrerer Operatoren und Invarianten kleiner Anfügungen zur Unterscheidung endlicher Kausalordnungen [3]. Eine generische endliche Ordnung besitzt jedoch keine automatisch ausgewiesene Raumkoordinate oder Impulsachse. Beispielsweise werden Dispersionsaussagen für verallgemeinerte kausale d'Alembertians unter ausdrücklich eingeführten Kontinuums- und Ebenenwellenannahmen untersucht [4].

## 4. Startrezept für den physischen Pilot

Dies sind **zu qualifizierende Entwurfswerte**, keine Messergebnisse und keine universellen Grenzwerte. Sie bilden ein eigenes Profil; der bestehende Industrial-V1-Vertrag mit vier Beschleunigungskanälen wird dadurch nicht verändert.

1. Zwei einachsige Beschleunigungssensoren an verschiedenen bekannten Positionen, ein Kraftsensor am Eingang; drei simultane Kanäle mit gemeinsamer Zeitbasis. SI-Einheiten m/s², N, s, m. Sensorempfindlichkeit, Frequenzgang, Ausrichtung und Kalibrierunsicherheit dokumentieren.
2. Zielband 20–2000 Hz, Abtastrate 25,6 kHz, zehn Sekunden pro Aufnahme: 256 000 Werte je Kanal. Analoge Anti-Aliasing-Übertragung muss den verwendeten Messbereich absichern; Abtastrate allein genügt nicht. Vorgeschlagenes maximales Kanal-Skew: 1 µs; bei 2 kHz entspricht dies 0,72° Phasenfehler, ohne weitere Sensor-/Filterfehler.
3. Stationäre breitbandige Anregung im vorab geprüften linearen Amplitudenbereich. Pro Objekt/Konfiguration fünf unabhängige Entdeckungsaufnahmen, anschliessend fünf neue Bestätigungsaufnahmen. Die Anzahl ist ein Pilotansatz, keine nachgewiesene statistische Teststärke. Wiederholte Fenster desselben Records sind keine unabhängigen Objekte.
4. Mittelwert entfernen; Welch mit Hann-Fenster, 16 384 Samples und 50 % Überlappung. Frequenzraster 1,5625 Hz; dies ist nicht gleich garantierter Modenauflösung. Konvention G_xy=⟨conj(X)Y⟩, H₁,i=G_Faᵢ/G_FF. Rohdaten bleiben erhalten; keine unabhängige automatische Zeitverschiebung der Kanäle.
5. Qualitätsmaske: keine abgeschnittenen/fehlenden Samples, Eingang über einem vorab aus dem Rauschen bestimmten Mindestniveau, dokumentierter Zeitversatz. Kohärenz ≥0,9 ist eine vorgeschlagene Nutzungsbedingung je Frequenzbin. Sie beweist weder Linearität noch physikalische Identität. Kohärenz aus nur einer ungemittelten Realisierung ist keine belastbare Qualitätsprüfung [2].
6. Vor Bestätigung festlegen: Vergleichsgrösse, praktisch relevanter Unterschied δ, Unsicherheitsmethode und gemeinsames Fehlerbudget über alle getesteten Merkmale. Trennung nur, wenn ein entsprechend kontrolliertes Konfidenzintervall der Differenz vollständig ausserhalb [−δ,+δ] liegt. Sonst ungelöst oder unzureichende Evidenz. Eine behauptete Näherungsäquivalenz benötigt ihr eigenes vorab definiertes Äquivalenzverfahren.
7. Maximal drei zusätzliche registrierte Messkonfigurationen pro Objekt; mögliche nächste Schritte sind weitere Position, andere Anregungsrichtung oder ein anderer kontrollierter Zustand. Unberührte Bestätigungsdaten reservieren. Fehlende Kalibrierung, Geometrie oder Fehlerkontrolle blockieren eine physikalische Trennungsentscheidung.

## 5. Schema und Datensemantik

- [x6-fingerprint.schema.json](x6-fingerprint.schema.json): geschlossenes JSON Schema Draft 2020-12 [5]. Alle sieben Ebenen sind Pflichtfelder; jede hat `AVAILABLE`, `NOT_MEASURED`, `NOT_APPLICABLE` oder `INVALID`.
- Bei `AVAILABLE` sind Merkmalsdefinition, Einheit, Herkunft, Abhängigkeiten, Annahmen, typisierter Wert und Unsicherheit erforderlich. Nicht verfügbare Ebenen benötigen einen Grund und dürfen keine Ergebniswerte enthalten.
- Exakte Ganzzahlen werden als Dezimalstrings gespeichert, um grosse charakteristische Koeffizienten auch in JavaScript verlustfrei zu erhalten. `EXACT_COMPUTATION` darf keine gerundeten Gleitkommazahlen als exakte Werte ausgeben.
- Unsicherheit: `EXACT`, `BOUNDED`, `INTERVAL`, `ARTIFACT` oder begründetes `UNKNOWN`. Einheiten entsprechen der Messgrösse; Intervall-/Artefaktmethoden müssen im Protokoll erklären, ob marginale oder simultane Abdeckung gemeint ist.
- `depends_on` macht abgeleitete Evidenz erkennbar. Die Degeneracy-Zeile des Beispiels verweist auf die Spektren; sie stellt keinen zweiten unabhängigen Test dar.
- Kontext enthält Modell, Zustand/Ensemble, Geometrie, Skala und Invarianzen. Nicht definierte Grundlagen werden explizit ausgewiesen. Physische Rohdaten, Kalibrierung und Qualitätsbericht sind bei abgeschlossener physischer Erfassung obligatorisch.
- [comparison-event.schema.json](comparison-event.schema.json) speichert das **Vergleichsereignis** getrennt vom Objekt-Fingerprint. Es bindet zwei Fingerprints über Dateihashes und nennt kumulative Merkmalsmengen sowie trennende Zeugen. Keine zyklische Selbsthash-Abhängigkeit.
- Benannte Ebenen (`spectrum`, `mode_structure` usw.) sind keine Rangnummern. Nur die kumulativen Schritte im Ereignis bilden eine Leiter. Höherer kumulativer Schritt kann eine zuvor gefundene exakte Trennung nicht zurücknehmen.
- `physical_equivalence` ist in dieser Version fest `NOT_ASSESSED`. Formatgültigkeit und Dateihashes beweisen weder Kalibrierung noch Wahrheit eines gemeldeten Experiments.

Der ergänzende [Validator](validate.py) prüft neben dem Schema: lokale SHA-256-Bindung, sichere relative Pfade, eindeutige IDs, Referenzen, Datentypen, Polynomgrad, Reihenlängen, Evidenzherkunft und azyklische Ableitungen. Exakte Vergleichsereignisse werden aus den gespeicherten Werten erneut ausgewertet; Definitions- oder Kontextwechsel werden abgelehnt. Empirische Vergleichsereignisse sind im Format vorgesehen, werden vom Referenzvalidator aber ausdrücklich als noch nicht implementiert zurückgewiesen. Ein statistischer Assessor muss separat ergänzt werden.

**Grenze des Validators:** Er berechnet nicht jedes übergebene Polynom aus der Rohmatrix neu und prüft keine Laborgeräte. Der mitgelieferte Atlas hat einen separaten unabhängigen algorithmischen Prüflauf. Die Ereignisprüfung sichert den Vergleich der gebundenen Datensätze; sie ersetzt nicht deren fachliche Erzeugung und Prüfung.

## 6. Konkrete Trennung: n6-0073 und n6-0181

| Kumulativer Schritt | Hinzugefügte Observable | Ergebnis |
|---|---|---|
| 0 | Vollständiges Spektrum von S | Exakte Kollision |
| 1 | Spektren von A und K | Exakte Kollision bleibt |
| 2 | Anzahl minimaler, maximaler, isolierter Elemente: (3,3,0) | Exakte Kollision bleibt |
| 3 | Multimenge gepaarter (Vergangenheitsgrösse, Zukunftsgrösse) | **Exakt getrennt** |

Beide besitzen χ_S(x)=x⁶−5x⁴+4x². Ihre gerichteten Gradmultimengen unterscheiden sich:

- n6-0073: {(0,1)×2, (0,3), (1,0)×2, (3,0)}.
- n6-0181: {(0,1), (0,2)×2, (1,0), (2,0)×2}.

Gezählt werden alle Kausalrelationen, nicht nur die Hasse-Kanten. Die Paare und ihre Vielfachheiten bleiben erhalten. Dies ist ein tatsächlicher Strukturseparator für dieses Paar; eine Trennung über Modenstruktur wird hier nicht behauptet.

Dateien: [Fingerprint A](examples/n6-0073.json), [Fingerprint B](examples/n6-0181.json), [Vergleichsereignis](examples/separation-event.json), [physischer Entwurfsdatensatz](examples/physical-pilot-plan.json). Der physische Datensatz enthält keine vorgetäuschten Messwerte; seine Positionen sind ausdrücklich Planungsplatzhalter.

## 7. Ausführen

Vom Repository-Stamm mit den bereits für die Arbeitspakete gepinnten Python-Abhängigkeiten:

```bash
python -m pip install -r experiments/industrial-v1/requirements.txt
python research/fingerprint_v1/build_schema.py
python research/fingerprint_v1/make_examples.py
python research/fingerprint_v1/validate.py research/fingerprint_v1/examples/n6-0073.json research/fingerprint_v1/examples/n6-0181.json research/fingerprint_v1/examples/separation-event.json research/fingerprint_v1/examples/physical-pilot-plan.json
python -m unittest discover -s research/fingerprint_v1/tests -v
```

Die Beispielerzeugung ist lokal und führt keine Sensormessung oder Netzwerkanfrage aus. Sie erneuert Zeitstempel und deshalb die gebundenen Fingerprint-Hashes. Die Quellinventare eines veröffentlichten Commits müssen nach beabsichtigten Änderungen separat neu erstellt werden; ein unveränderter publizierter Datensatz wird nur validiert.

## Quellen

1. NI, [Modal Analysis in LabVIEW](https://www.ni.com/en/shop/labview/modal-analysis-in-labview.html): Anregung, Antwort und experimentelle Modalparameter.
2. NI, [LabVIEW Analysis Concepts](https://download.ni.com/support/manuals/370192c.pdf), Abschnitt Coherence Function: Kreuz-/Autospektren und Mittelung.
3. Yazdi, Letizia, Kempf, [Lorentzian spectral geometry with causal sets](https://www.to.infn.it/~mussod/Yazdi_2021_Class._Quantum_Grav._38_015011.pdf), CQG 38 (2021) 015011, DOI 10.1088/1361-6382/abc3f8.
4. Aslanbeigi, Saravani, Sorkin, [Generalized Causal Set d'Alembertians](https://arxiv.org/abs/1403.1622), JHEP 06 (2014) 024.
5. [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12).
