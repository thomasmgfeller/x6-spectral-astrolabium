# Vorregistrierter Staubuhrtest · Präfix 1564

Stand bei Erstellung: **REGISTERED / NOT_RUN**. Protokoll.md beschreibt genau eine Vorhersage, ihre Herleitung und die bindende spätere Entscheidung. registration.json bindet Protokoll, Prüfprogramme und das unveränderte Referenzpaket per SHA-256. Die im PDF und im Chat angegebene Prüfsumme bezieht sich auf die exakten Bytes dieser Registrierung. Die Registrierung ist in dieser Fassung datiert. Eine öffentliche Registereintragung ist ein eigener Veröffentlichungsschritt.

## Jetzt nachprüfbar

Im entpackten Verzeichnis ausführen. Der erste Befehl prüft die Prüfsummen. Der zweite prüft den vorab hergeleiteten Grenzwert und synthetische Polynomkontrollen. Die physikalische Zielintegration wird dabei vollständig durch eine Testfunktion ersetzt. Der dritte Befehl gibt die rationale Vorabschätzung aus den Referenzdaten nochmals aus.

~~~sh
sha256sum -c SHA256SUMS
python3 -B verify_registration.py
python3 -B baseline.py
~~~

## Separater Folgelauf

Für den später beauftragten Test sind die folgenden Befehle vorbereitet. Im versiegelten Paket sind keine Zielwerte hinterlegt. Bei Wiederholungen ist eine neue Ausgabedatei zu wählen.

~~~sh
python3 -B run_later.py target_run_001.json
python3 -B score.py target_run_001.json
~~~

Die Ordner im inneren Referenzarchiv enthalten Quell- und Lizenzangaben des Forschungsprojekts. Verwendete Umgebung für die Referenz- und Designkontrollen: Python 3.12, NumPy 2.3.5, SymPy 1.14.0 und mpmath 1.3.0. Der künftige Evaluator benötigt keinen Netzzugang und keinen externen Rechenauftrag. Seine Laufzeit auf dem neuen Paket wurde bei der Registrierung nicht gemessen.
