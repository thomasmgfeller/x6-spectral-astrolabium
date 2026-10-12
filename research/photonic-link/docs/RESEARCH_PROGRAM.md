# Forschungsprogramm PLVL 0.1

## Gegenstand und zulässiger Anspruch

Untersucht wird, wie gemeinsame Verlust-, Polarisations- und Zeitfehler die
Verlässlichkeit einer Messkette für verteilte Photonenpaare begrenzen. Das
angestrebte Ergebnis ist ein überprüfbares Modell mit kalibrierten Parametern,
offenen Rohdaten und dokumentierten Vorhersagefehlern. Die industrielle
Arbeitshypothese ist ein möglicher Nutzen für Inbetriebnahme, Fehlersuche und
vergleichende Bewertung solcher Messketten. Ob dieser Nutzen gegenüber
vorhandenen Werkzeugen besteht, ist offen.

Ein eigener Forschungszweig ist eine organisatorische Entscheidung, kein
Neuheitsnachweis. Simulation, unabhängige Implementierungsprüfung,
Laborvalidierung und Replikation werden als verschiedene Evidenzstufen geführt.
Der aktuelle Stand erreicht nur die im Prüfbericht tatsächlich ausgeführten
Software- und Simulationsprüfungen. Hardware- und Sicherheitsfelder stehen
weiter auf `NOT_ASSESSED`.

## Forschungsfragen und Widerlegungsmöglichkeiten

| ID | Prüffrage | Vergleich / Messgröße | Wann die Hypothese verworfen oder eingeschränkt wird |
|---|---|---|---|
| H1 | Reicht skalarer, bedingt unabhängiger Verlust für den gewählten Aufbau? | Einzelraten, Paarüberleben, port- und basisaufgelöste Raten gegen kalibrierte eta | Reproduzierbare basisabhängige Transmission, nicht erklärte Kovarianz oder Residuen außerhalb der vorher festgelegten Unsicherheit erfordern PDL-/Quellmodell-Erweiterung |
| H2 | Erklären lokale Rotationen die beobachtete Polarisationsdrift? | Zeitaufgelöste, ausreichend vollständige Polarimetrie/Tomografie; unitäres Modell gegen Modell mit Mischung | Driftbedingte Daten lassen sich auch mit kalibrierten lokalen Rotationen nicht vorhersagen; Dephasierung/PMD/Quelle müssen separat geprüft werden |
| H3 | Reicht eine affine Zeitabbildung im vorgesehenen Kalibrierintervall? | Zurückgehaltene Referenzpulse; Referenz gegen Offset-only- und affines Modell | Systematische Krümmung, Ausläufer oder Transferfehler überschreiten das vorab festgelegte Restfehlerbudget |
| H4 | Verbessert ein gemeinsamer Umweltprozess die Vorhersage gegenüber getrennten Fehlerbudgets? | Paarige Vorhersagefehler auf neuen Zeitblöcken und Tagen; gekoppelt gegen faktorisiert | Kein stabiler Zusatznutzen nach Berücksichtigung zusätzlicher Parameter; einfacheres Modell bleibt bevorzugt |
| H5 | Liefern geometrische Zustandsmerkmale zusätzliche diagnostische Information? | Vorab definierte Merkmale gegen direkte Polarisations-, Rate- und Timingdiagnostik auf zurückgehaltenen Daten | Gleiche oder schlechtere Vorhersage, mangelnde Identifizierbarkeit oder Instabilität; Ergebnis als Negativbefund publizieren |

H5 ist ein späterer explorativer Strang. Berry-Phasen, Fubini-Study-Abstände und
Fisher-Information benötigen jeweils ein definiertes Zustands-/Parametermodell
und passende Messungen. Sie sind keine voreingestellten Schutzmechanismen.
Die Funktionen des früher vorgeschlagenen Marginalzählers erfüllen diese
Anforderungen nicht; ihre Fehlklassifikation ist jetzt ein Regressionstest.

## Arbeitspakete und Entscheidungstore

| Tor | Arbeit / erforderliche Artefakte | Annahmekriterium | Stand dieser Version |
|---|---|---|---|
| G0: digitale Referenz | Einheiten, Annahmen, Quellen, Herkunft, Tests, vollständige Zählbilanz | Analytische Grenzfälle, differenzielle Referenzprüfungen und Fehlerpfade bestehen; keine unbelegten Statusfelder | siehe ausführbares Prüfprotokoll |
| G1: Messfähigkeit | Detektor-/TDC-Kalibrierung, DNL/INL, Jitter, Totzeit, Dunkelzählungen, Verlustbilanz, Zeitepochen | Getrennte Kalibrier- und Prüfdaten; rückführbare Referenzen mit Unsicherheit; Bilanz aller Flags und verworfenen Ereignisse | nicht ausgeführt |
| G2: lokaler Link | Eine Quelle, zwei Stationen; kontrollierte Dämpfung, bekannte Rotationen und Zeitfehler | Modellparameter ausschließlich aus Trainingsdaten; Vorhersageintervalle decken zurückgehaltene Kontrollmessungen wie geplant ab; Residuen ohne unmodellierte Struktur | nicht ausgeführt |
| G3: Faserspule / reale Strecke | Messplan über mehrere Tage, Umweltsensorik, Zustands-/Timingdiagnostik, Ausfallprotokoll | Vorab definierte Einsatzanforderungen an Rate, Fehleranteil, Restjitter und Verfügbarkeit werden mit Unsicherheiten erfüllt | nicht ausgeführt |
| G4: unabhängige Replikation / Nutzen | Zweiter Aufbau oder unabhängige Gruppe; Vergleich gegen Referenzmesskette | Reproduktion wesentlicher Ergebnisse; messbarer Nutzen bei gleichem Zeit-, Kosten- und Gerätebudget | nicht ausgeführt |
| G5: mögliche QKD-Erweiterung | Eigenes Bedrohungsmodell, Geräteannahmen, zufällige Basen, Authentisierung, Fehlerkorrektur, Privacy Amplification, endliche Schlüsselanalyse | Fachlich geprüfter Sicherheitsbeweis und Implementierungsprüfung; positive geheime Schlüsselrate unter angegebenen Annahmen | eigener späterer Forschungsauftrag |

G2 kann zunächst lokal bei einer zur verfügbaren Quelle und Detektion passenden
Wellenlänge stattfinden. Ein Wechsel auf 1550 nm ist eine gesonderte Optik- und
Detektorentscheidung. Standard-Telekomfaser ist bei 810 nm nicht automatisch
im garantierten Singlemode-Bereich. Dämpfung, Modenführung und Detektion müssen
für die konkrete Stückliste geprüft werden. Ein White-Rabbit-Netz ist eine
mögliche Zeitreferenz, keine Voraussetzung dieses Modells und kein implementierter
Bestandteil. Klassische Uhrsynchronisation ist keine optische Phasenreferenz.

## Versuchsplan vor neuer Datenerhebung

1. **Modell und Messgrößen einfrieren.** Commit, Konfiguration, Referenzkalibrierungen,
   Fensterbreite, Vorzeichenkonventionen, Ausschlussregeln und primäre Endpunkte
   versionieren. Dieses Dokument ist ein Entwurf einer Präregistrierung, keine
   bereits erfolgte externe Präregistrierung.
2. **Kontrollen messen.** Quelle blockiert; beide Arme einzeln blockiert; bekannte
   Dämpfung; bekannte Analysatorrotation; bewusst eingefügter Offset/Skew;
   Referenzsignal ohne Faser. Dunkel- und Verzögerungskontrollen gesondert halten.
3. **Parameter identifizieren.** Geeignete unabhängige Referenzen verwenden.
   Nicht identifizierbare Produkte nicht in einzelne angeblich gemessene
   Effizienzen zerlegen. Gemeinsame Fehlerquellen in der Kovarianz berücksichtigen.
4. **Vorhersagen prüfen.** Kalibrierblöcke, zeitlich getrennte Prüfblöcke und einen
   anderen Tag unterscheiden. Fensterbreite und Ausreißerregeln anhand der
   Trainingsdaten festlegen und danach sperren. Identische Rohdaten für beide
   Modellalternativen verwenden.
5. **Unsicherheit und Stichprobe planen.** Pilotdaten dienen der Varianz- und
   Autokorrelationsschätzung. Danach wird eine praktisch relevante Differenz
   definiert und die Zahl unabhängiger Blöcke geplant. Für einen annähernd
   normalverteilten Mittelwert unabhängiger Blockdifferenzen kann
   n≈((z_(1-alpha/2)+z_(1-beta))*s_D/Delta)^2 als Startwert dienen; bei
   Autokorrelation/seltenen Ereignissen per Simulation planen. Es gibt hier
   noch keine datengestützte Power-Behauptung und kein optionales Stoppen bei
   einem günstigen p-Wert.
6. **Alle Ergebnisse erhalten.** Nullbefunde, Integritätsfehler, Totzeitverluste,
   Multiklicks und Ausfälle berichten. Ein Datenverlustflag macht eine physikalische
   Bewertung ungültig; es wird nicht durch Hintergrundabzug geheilt.

## Vergleichsmaßstäbe und Abbruchregeln

Die erste Softwarebaseline verwendet eingefrorene Polarisation, konstante
Dämpfung und ideale/affine Uhren. Weitere Vergleiche entfernen jeweils eine
Kopplung. Geometrische Merkmale werden nur gegen bereits verfügbare direkte
Diagnostik bewertet. Ein Vergleich gegen eine Fachpublikation darf deren
Quellhelligkeit, Detektortechnik und Fasertopologie nicht ignorieren.

Wenn die reale Kalibrierung keine Trennung der Parameter erlaubt, wird der
Anspruch auf die identifizierbare Kombination begrenzt. Wenn nichtmodellierte
Effekte die Unsicherheit dominieren, stoppt die Extrapolation auf größere
Strecken. Eine physikalisch nötige Erweiterung erhält eigene Tests und eine neue
Modellversion. Ein nicht erreichter Anwendungsvorteil ist ein zulässiges Ergebnis.

## Liefergegenstände dieses Zweigs

Python-Modell, strenge Konfiguration, synthetische Rohereignisexporte,
SGNCv007-Zählerexport, analytische Vergleichsfälle, Monte-Carlo-Wiederholungen,
Hashinventar, getestete Referenzübernahme, CI sowie dieses Forschungsprogramm.
Die erste spätere Laborlieferung wäre ein unverändertes Rohdatenpaket mit
Kalibrierprotokoll und vorab festgelegter Analyse, nicht eine neue Schutzbehauptung.
