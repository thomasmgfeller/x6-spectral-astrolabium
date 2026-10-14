# V1-Messprofil und ausführbarer Ergebnisvertrag — Version 0.1

Stand: 14.10.2026. Implementiert sind vier JSON-Schemas (Profil, Eingaben,
Ergebnis, Bewertung), lokale Vorprüfung, Ergebnisbewertung, synthetischer
Kontrollgenerator und Negativtests. Das ergänzt das industrielle
[Forschungsprogramm v0.2](../../docs/industrial-denoising/Astrolabium_Industrial_Denoising_Forschungsprogramm_v0_2.docx).

**Software implementiert; reale AP1-Freigabe NOT_READY.** Es fehlen konkrete
Maschinen-/Sensordaten, Rechtebelege, Referenz- und Labeldefinition, unabhängige
Datenaufteilung, Fallzahl-/Powerplanung, ausgewählte Verfahren und fachlicher
Protokollreview. Diese Tatsachen werden nicht erfunden. Die offenen Felder sind
im [ausführbaren Profil](V1_PROFILE_DRAFT.json) und im
[Vorprüfergebnis](examples/draft_readiness.json) einzeln ausgewiesen.

## Gewählter technischer Umfang

Erste Route ist **D: Diagnosequalität auf realen V1-Lagerdaten**. Zielgrösse
ist Sensitivitätsgewinn gegen eine vorher ausgewählte starke Baseline bei
begrenzter Fehlalarmrate. Q, E und ED benötigen eigene versionierte Verträge.
Der vorhandene X6-Chirp-Vertrag wird nicht umgedeutet oder überschrieben.
Das historische negative X6-Ergebnis bleibt unverändert.

| Festlegung | Version 0.1 |
|---|---|
| Aufnahme | 4 Kanäle, je 25'600 Samples/s, Float32 little endian, m/s² |
| Binärformat | Zeit zuerst, je Zeitpunkt 4 Kanäle; keine Kopfzeile |
| Datensatz je Einheit | Vorher ausgewählter 10-s-Ausschnitt, 256'000 Samples/Kanal |
| Streaming | Kausal, keine Vorschau; 256 Samples/Kanal je Block, also 10 ms Takt |
| Latenz | Höchstens 50 ms beobachtete Ende-zu-Ende-Latenz |
| Durchsatz | Mittlere Bedienzeit strikt <10 ms, empirisches p99 ≤10 ms |
| Ressourcenlauf | 6'000 aufeinanderfolgende Blöcke, 60 s Eingangsdauer |
| Zustand | Höchstens 8 MiB zusätzlicher Zustand; Messgrenze im Messbericht |
| Datenverlust | Keine verlorenen Blöcke, höchstens 4 wartende Blöcke, kein Rückstand nach Drain |
| Statistikeinheit | Ein vorab gewählter Ausschnitt pro unabhängigem physischem Lager |
| Hauptvergleich | Ein eingefrorener Kandidat gegen eine eingefrorene Baseline je Auswertung |

Die Aufnahmehardware, Kanalachsen/-orte, Sensorbandbreite, Analogfilter gegen
Aliasing, Messbereich, Kalibrierung, Drehzahl-/Lastbereich und Auswahlregel des
10-s-Ausschnitts müssen im referenzierten Aufnahmeprotokoll konkret stehen.
Die Diagnose erzeugt nach dem 10-s-Ausschnitt einen Score je Lager. Die
50-ms-Grenze betrifft die Streaming-Signalkette, nicht eine 10-s-Diagnose.
Initialisierung, Warmup, Messgrenzen, Last, Ausgabe-/Transportzeiten und
Messinstrumente werden im Ressourcenprotokoll festgelegt. Die Grenzwerte
sind Forschungsziele, keine bereits erfüllten Hardwareeigenschaften.

## Vorgeschlagene Schwellen und ehrliche Sperren

Zusätzlich zu den v0.2-Ressourcenzielen werden für diesen Entwurf vorgeschlagen:
S_min=0,80, positiver Sensitivitätsgewinn >0,05, Fehlalarmrate ≤0,01,
synthetischer Amplitudenfehler ≤5 %, Ereigniszeitfehler ≤2 Samples.
Sie sind **Entwurfsentscheidungen**, keine aus einer realen Maschine
abgeleiteten Anforderungen. Fachliche Begründung und Freigabe erfolgen im
`protocol_review`, bevor das Profil eingefroren wird.

Die Sentinel-Referenz im Entwurf ist ausdrücklich `DESIGN_ONLY` und blockiert.
Für einen Lauf sind materialisierte Float32-Referenzen mit eindeutigem Maximum
in vorher definierten Zeitfenstern nötig. Das Programm prüft Referenzmetadaten
gegen die Bytes und berechnet Maximalamplitude und Zeitpunkt aus den
Ausgangsarrays selbst. Keine nachträgliche Gain- oder Zeitausrichtung.
Mehrdeutige Spitzen liefern INVALID. Diese Prüfungen belegen nur die gewählten
synthetischen Schutzfälle; sie ersetzen weder reale Ereignislabels noch
ein messtechnisches Unsicherheitsbudget.

Der vollständige Sentinel-Plan muss saubere/kleine Impulse, Blockgrenzen,
Reset, Anlauf, Modulation und überlappende Störungen umfassen. Ein gültiger
Schemaeintrag allein beweist die fachliche Angemessenheit dieser Auswahl nicht.

## Daten und Prüfablauf

1. Development, Validation, Holdout und External werden im Eingabemanifest
   erfasst. Ein Lager darf hier nur eine Einheit liefern und in keinem anderen
   Split wiederkehren. Wiederholte IDs und identische Datenbytes sind gesperrt.
2. Labels `healthy`/`damaged` stammen aus einer unabhängigen, dokumentierten
   Referenz (z.B. Inspektion). Der Filter sieht keine Holdout-Labels.
3. Ein Score pro Lager und Verfahren wird nach der eingefrorenen Regel mit
   der auf Validation festgelegten Schwelle verglichen (`score >= threshold`).
   Die Score-Bildung gehört zum gehashten Algorithmusquelltext.
4. Das Ergebnis muss genau alle registrierten Holdout-Einheiten enthalten.
   Entfernen schwieriger Fälle und zusätzliche unregistrierte Fälle sind Fehler.
5. Alle referenzierten Bytes werden lokal geprüft. Eingabearrays müssen die
   vollständige Form haben und ausschliesslich endliche Float32-Werte enthalten.
6. Startzeit muss nach Protokoll-Freeze liegen. Profil, Eingabemanifest,
   Algorithmen und Ergebnis sind mit SHA-256 verbunden. Die Ausgabe enthält
   zusätzlich den Hash des ausgeführten Bewertungsprogramms.

Die Binomialauswertung setzt unabhängige, innerhalb der vorgesehenen
Population vergleichbare Lagerversuche voraus. Gemeinsame Maschinen-/Standort-
effekte können diese Annahme verletzen. Dann ist vor dem Test ein anderes
Samplingdesign oder ein Vertrag mit Clusterauswertung nötig. Tausende Fenster
eines Lagers ersetzen keine unabhängigen Lager. Hashes und angegebene Zeitstempel
beweisen weder Unabhängigkeit noch bisher unberührten Holdout-Zugang.

## Unsicherheiten und Entscheidung

Pro Anspruch gilt alpha=0,05/K, K=1 oder 2 vorher registrierte Ansprüche.
Sensitivität und Fehlalarmrate verwenden einseitige Clopper-Pearson-Grenzen.
Für den gepaarten Sensitivitätsgewinn wird W=P(Kandidat richtig, Baseline falsch)
und L=P(Kandidat falsch, Baseline richtig) auf beschädigten Lagern verwendet:

`untere Grenze = CP_lower(W, alpha/2) − CP_upper(L, alpha/2)`.

Die obere Grenze wird entsprechend gebildet. Per Vereinigungsabschätzung
hat jede gerichtete Differenzgrenze mindestens 1−alpha Abdeckung unter dem
Binomialmodell. Dieses Verfahren ist konservativ; es nutzt keine falsche
Unabhängigkeit zwischen Kandidat und Baseline. Alle Qualitätsgates müssen
gleichzeitig bestehen. Bonferroni über die K Ansprüche und die konjunktive
Entscheidung ersetzen keine fehlende Fallzahlplanung.

Bei null Fehlalarmen ist die obere Grenze positiv: `1−alpha^(1/n)`.
Für K=2 benötigt allein eine Grenze ≤1 % mindestens 368 unabhängige gesunde
Einheiten ohne Fehlalarm. Das ist keine Powerberechnung des Gesamtversuchs.
AP1 benötigt zusätzlich einen überprüften, auf ≥80 % Zielpower ausgerichteten
Plan mit Annahmen zu Sensitivität und gepaarten Diskordanzen. Das Programm
prüft dessen Bindung und Mindestfallzahlen, nicht die fachliche Güte des Texts.

| Status | Bedeutung |
|---|---|
| NOT_READY | Pflichtfestlegungen, Referenzen oder geplante Einheiten fehlen |
| INVALID | Schema, Hash, Bytes, Aufteilung oder Ergebnisvollständigkeit verletzt |
| INCONCLUSIVE | Gültige Beobachtungen entscheiden mindestens ein statistisches Gate nicht |
| FAIL | Deterministisches Gate verletzt oder Intervall vollständig auf der Ablehnungsseite |
| PASS | Alle registrierten Gates erfüllt; Aussage nur für Profil, Daten und Annahmen |
| READY_FOR_RESULT_REVIEW | Technische Vorprüfung bestanden, noch kein Leistungsurteil |

Die beiden ausgegebenen gerichteten Grenzen sind jeweils einseitig 1−alpha;
sie werden nicht als zweiseitiges 1−alpha-Intervall bezeichnet. Ressourcen-
und Sentinel-Grenzen beziehen sich auf beobachtete Werte, ohne allgemeine
statistische Garantie für beliebige zukünftige Messläufe.

Rekonstruktions-MSE und Energieersparnis sind hier ausdrücklich nicht verfügbar.
Ein `SYNTHETIC_CONTROL` kann nie `claim_supported=true` erhalten. Ein realer
PASS setzt zutreffende Messberichte und die fachlich geprüften Voraussetzungen
voraus; die Software attestiert weder Echtheit noch externe Replikation.

## Ausführen

Aus dem Repository-Hauptverzeichnis:

```sh
python -m pip install -r experiments/industrial-v1/requirements.txt
python experiments/industrial-v1/evaluate.py experiments/industrial-v1/V1_PROFILE_DRAFT.json --root experiments/industrial-v1 --output /tmp/v1-readiness.json
# Erwartet: NOT_READY, Exit-Code 3.
python experiments/industrial-v1/make_control.py /tmp/v1-control
python experiments/industrial-v1/evaluate.py /tmp/v1-control/profile.json --root /tmp/v1-control --inputs /tmp/v1-control/inputs.json --result /tmp/v1-control/result.json --output /tmp/v1-control/assessment.json
# Erwartet: INCONCLUSIVE, Exit-Code 4, SOFTWARE_CONTROL_ONLY.
python -m unittest discover -s experiments/industrial-v1/tests -v
```

Weitere Exit-Codes: PASS/READY=0, FAIL=1, INVALID=2. Referenzen sind relative
Dateien unter `--root`; Pfadausbrüche und symbolische Links werden abgelehnt.
Es gibt keine Netzwerkabfrage und keine Ausführung fremden Algorithmuscodes.
Der Kontrollgenerator erzeugt deklarierte Testwerte, keine simulierte
Industrievalidierung. Seine Timestamps sind feste Fixturewerte.

Dieses Paket ist ein Bewertungsadapter. Ein DSP-Runner für reale Filter,
JS/WASM-Portierung, GUI-Anbindung, Kalibrierung und Hardwaremessungen gehören
zu den folgenden Arbeitspaketen. Der vorhandene Edge-Runner unterstützt bisher
synthetische Signal-Lab-Aufträge; er behauptet keine V1-Kompatibilität.

## Primärquellen und Abgrenzung

- NIST, Exact Binomial Confidence Limits:
  https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbici.htm
- SciPy 1.17.0, Beta-Quantile für die Grenzen:
  https://docs.scipy.org/doc/scipy-1.17.0/reference/generated/scipy.stats.beta.html
- JSON Schema Draft 2020-12: https://json-schema.org/draft/2020-12

Die gepaarte konservative Kombination ist oben explizit hergeleitet;
Grenzwerte und Profilwahl sind eigene Entwurfsentscheidungen. Ein neuer
Entrauscher oder Neuheitsnachweis wurde mit diesem Paket nicht behauptet.
