# Eigenzeit v0.11 · Wie lässt sich die 20-ppm-Driftgrenze prüfen?

Der Prüfling und ein unabhängig kalibrierter Referenzstandard beobachten dieselben markierten Ereignisse. In jeder der 16 Zellen werden zwei Betriebszustände geprüft. Systematische Unsicherheiten dürfen zusammen höchstens 6 ppm beanspruchen. Die Häufigkeit ungleicher Paarantworten prüft die verbleibenden 14 ppm. Damit lässt sich eine Eingangsbedingung der Krümmungsschätzung aus v0.10 absichern. [Bericht (PDF)](Eigenzeit_Referenzaudit_v0_11.pdf) · [Herleitung](BEWEIS.md) · [Originales Prüfpaket (ZIP)](Eigenzeit_Referenzaudit_v0_11_Pruefpaket.zip)

| Größe | Ergebnis unter den Modellannahmen |
|---|---:|
| Umfang für einen positiven Audit | 32 Messpunkte × 3.300.000 Paare |
| Höchste zulässige Zahl ungleicher Antworten je Messpunkt | 25 |
| Wahrscheinlichkeit, eine tatsächlich verletzte Driftgrenze zu akzeptieren | höchstens 0,04778 % |
| Wahrscheinlichkeit einer falschen physischen Freigabe mit v0.10 | höchstens 0,98379 % |
| Unbedingte Überdeckung des Krümmungsintervalls einschließlich HOLD | mindestens 95,10 % |

Sobald am selben Messpunkt die 26. Diskordanz auftritt, endet der Audit negativ. Eine positive Zählentscheidung benötigt alle 105,6 Millionen Paare. Im synthetischen Pilot bestanden bei 3 ppm Paarabweichung an allen Messpunkten 39.979 von 40.000 Kampagnen. Bei einem gemeinsamen Zielversatz von 50 ppm erfüllten beide Kanäle die Zählbedingung in allen 40.000 Kampagnen. Dieser Gegenfall zeigt, weshalb der Standard eine unabhängige Kalibrierung braucht. [Zertifikat](certificate.json) · [Ergebnisse der fünf Szenarien](pilot.json) · [Gegenrechnungen](controls.json)

**Für reale Messungen gilt HOLD_EVIDENCE.** Es fehlen der Nachweis des Zielbezugs des Vergleichsstandards, unabhängige Belege für die Übertragung in den Betriebsbereich und markierte Paardaten einer Anlage. Der Feldprüfer unterscheidet fehlende Nachweise, widersprüchliche Zählungen und erfüllte Zählbedingungen. Das Feldprotokoll beschreibt die fachliche Prüfung und die Übergabe an v0.10. [Feldprotokoll](FELDPROTOKOLL.md) · [Feldvorlage](examples/field_worksheet.json) · [Vorstudie v0.10](../drift_reserve_v0_10/README.md)

## Ausführen

Im Verzeichnis dieser Studie benötigen die beiden folgenden Befehle nur Python ab 3.11. Die leere Feldvorlage ergibt `HOLD_EVIDENCE`. Der zweite Aufruf zeigt den Abbruch am ersten Messpunkt nach 26 ungleichen Antworten.

```sh
python -B audit.py examples/field_worksheet.json
python -B screen.py examples/prefix_26.json
```

Für die vollständige Reproduktion im Wurzelverzeichnis des Repositorys mit Python 3.12 ausführen.

```sh
python -m pip install -r tools/workflow/requirements-research.txt
python -B research/eigenzeit/reference_audit_v0_11/publication_check.py --replay
```

Der Prüflauf vergleicht die Originaldateien, die internen Prüfsummen und vier übernommene Dateien mit dem veröffentlichten v0.10-Archiv. Anschließend erzeugt er das Zertifikat, den synthetischen Pilot mit fünfmal 40.000 Kampagnen, die unabhängigen Prüfungen und die ergänzenden Kontrollen neu und vergleicht alle vier Protokolle byteweise. [Prüfprotokoll](verification.json) · [Veröffentlichungsnachweis](PUBLICATION.json)

Die Folgestudie definiert die Messgröße am ersten Referenzpunkt C01 und rechnet die Unsicherheitsbilanz sowie die gesonderte 2-ppm-Entscheidung an einem synthetischen Beispiel durch. [C01 und die GUM-Bilanz v0.12](../c01_gum_v0_12/README.md)
