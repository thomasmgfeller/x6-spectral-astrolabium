# Umsetzung der beiden Forschungsarbeitspakete

Stand 14.10.2026. Ausgangscommit:
`7ac131bcfbabd658b38fb1c97686325ac47fa081`.

## Arbeitspaket 1 — abgeschlossen im Umfang n=6

Der [exakte Atlas](../research/lorentz_n6/README.md) enthält alle 318
nicht isomorphen Sechserordnungen. Die separate Gegenprüfung deckt sämtliche
4'824 natürlich beschrifteten Ordnungen und 4'208 charakteristische Polynome ab.
Die Werte 286 bzw. 314 Klassen replizieren die Literatur. Maximale
Quill-Antworten lösen alle 33 Paare der dafür definierten Vergleichsbasis auf.
Vollständige Repräsentanten und Kollisionsmitgliedschaften sind gespeichert.

Das ist eine nachgerechnete endliche Replikation. Allgemeine Eindeutigkeit,
neue Mathematik, Kontinuumskonvergenz und physikalische Evidenz sind nicht belegt.
Der unabhängige Rechenweg ist projektintern und keine externe Begutachtung.

## Arbeitspaket 2 — Software umgesetzt, reale AP1-Freigabe offen

Der [V1-Vertrag](../experiments/industrial-v1/README.md) konkretisiert die
Diagnoseroute D: Aufnahmeformat, Einheit, kausale Verarbeitung, Entscheidungs-
schwellen, statistische Einheit, Ergebnisstruktur, Intervallberechnung,
Signalerhalt, Durchsatz, Latenz, Speicher und Fehlerstatus.

Vier geschlossene JSON-Schemas und ein Kommandozeilenprogramm prüfen den
Vertrag. Die Bewertung errechnet Qualitätsgrenzen aus einzelnen Lagerentscheidungen,
Schutzmetriken aus Float32-Ausgangsarrays und Ressourcenmetriken aus
Blockbeobachtungen. Hashbindungen, Daten-Dubletten, unvollständige Ergebnisse
und unzulässige Evidenzaufwertung werden geprüft.

Die realen Angaben zu Maschine/Sensor, Kalibrierung, Datenrechten, Labels,
Aufteilung, Zugang, Fallzahl/Power, Algorithmen und fachlichem Review stehen
weiterhin aus. Die vorgesehenen Referenz-Sentinels sind noch zu materialisieren.
Der dokumentierte Entwurf bleibt daher **NOT_READY**. Das ist ein tatsächlicher
offener Abschluss von AP1 im industriellen Programm, keine bereits erfolgte
Studienfreigabe. Die Software kann diese Angaben prüfen, aber nicht erzeugen.

S_min=0,80, Mindestgewinn 5 Prozentpunkte, 5 % Amplitudengrenze und 2 Samples
Zeitfehler sind begründungsbedürftige Entwurfsschwellen. Hardwarewerte stammen
aus dem vorhandenen Programm. Eine Maschine hat diese Ziele noch nicht erfüllt.
Der kleine synthetische Kontrolllauf endet erwartungsgemäss INCONCLUSIVE und
`claim_supported=false`; er ist kein Filterbenchmark.

## Ausgeführte Prüfung

Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, jsonschema 4.25.1.

| Prüfung | Ergebnis |
|---|---|
| Lorentz n=6, bisherige Lorentz- und Math-Agent-Regression | 28/28 |
| V1-Vertrag inklusive Binomial-/Multinomial-Gegenprüfung | 25/25 |
| Bestehende Provenienzschutztests | 16/16 |
| Bestehende Edge-Referenztests | 11/11 |
| Signal-Lab-Quellinventar | PASS |
| Kommandozeile: realer Entwurf | NOT_READY, erwarteter Exit-Code 3 |
| Kommandozeile: synthetische Kontrolle | INCONCLUSIVE, erwarteter Exit-Code 4 |

Damit bestehen 80 Tests und die zusätzlichen Integrationskontrollen.
Ein erwarteter NOT_READY/INCONCLUSIVE-Status wird ausschliesslich als korrekte
Softwareentscheidung gezählt, nicht als positiver Forschungsbefund.
[Maschinenlesbarer Bericht und Logs](../evidence/workpackages-2026-10-14/qualification.json).

Reproduktion: `python tools/qualify_workpackages.py --output /tmp/x6-wp-check`.
Der neue GitHub-Workflow läuft bei Änderungen oder manuell, hat keinen Zeitplan
und startet keine neuen dauerhaften Agenten. Bestehende Agentenquellen,
App-Hash und Zeitfenster bleiben unverändert. Das neue Quellinventar ergänzt
die bisherige strikte Manifestprüfung; bestehende Hash-Sperren bleiben aktiv.

## Nächste sachliche Voraussetzungen

Für Lorentz ist nun die genaue Struktur der verbleibenden Kollisionen vor
Quill-Anreicherung untersuchbar. Für V1 muss ein konkreter Mess-/Datenpartner
oder ein hinreichender Datensatz mit den erforderlichen unabhängigen Einheiten
benannt und der Entwurf fachlich geschlossen werden. Erst dann beginnen
Baseline-Runner, Kandidatenentwicklung und ein bestätigender Datenlauf.
