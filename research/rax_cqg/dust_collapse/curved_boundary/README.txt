DER GEKRÜMMTE RANDTERM  |  REPRODUKTION
2. November 2026. Paket zum Bericht CST_Staubkollaps_Gekruemmter_Randterm.pdf.

Alle Befehle im entpackten Verzeichnis ausführen. Getestet mit Python 3.12,
NumPy 2.3.5 und SciPy 1.17.0 unter Linux. Es sind keine externen Daten nötig.
Für die Präzisionsprüfung benötigt numpy.longdouble mehr Mantissenbits als
float64, wie beim verwendeten Linux-x86-System. Der Haupttest nutzt float64.

Hauptprüfung in dieser Reihenfolge
  python3 coefficient_checks.py
  python3 prediction.py
  python3 reference.py
  python3 evaluate.py

Zusatzprüfung des logarithmischen Koeffizienten
  python3 logcheck.py
  python3 logcheck_precise.py
  python3 ray_audit.py

design.json hält Fenster, Dichten und Regeln der Hauptprüfung fest. Die Parameter
wurden im Ablauf vor den neuen Flussauswertungen gesetzt. Es gibt keine externe
Vorregistrierung. logcheck_design.json wurde für eine separate spätere Gegenprobe
angelegt. Die ersten beiden Quadraturverfahren konnten die numerische Steigung
beim höchsten Dichtepaar in ihren groben Auflösungen nicht ausreichend stabil
bestimmen. precision.py und ray_audit.py prüfen Rundung und zeitliche Auflösung
gesondert. Die Daten dieser Versuche sind vollständig enthalten.

Vorhersagen benötigen nur die Schnittlage, die Restzeit zum bekannten klassischen
Singularitätszeitpunkt, Fensterbreiten und Beprobungsdichte. common.py beschreibt
das exakte homogene Referenzmodell. prediction.py berechnet die Mellin-Koeffizienten
ohne Zugriff auf die Flussreferenz. Die sechsfache Tabelle der Fensterkoeffizienten
und ihre Variationen stehen in predictions.csv. coefficient_checks.py verifiziert
lokale rationale Koeffizienten und den unabhängig bekannten flachen Randterm.

reference.py integriert den endlichen Poisson-Erwartungswert. lens_reference.py
ist die separate Kugelschnitt-Implementierung aus der früheren Kalibrierung.
previous_design.json gehört zu deren Import. Die Hauptreferenz ist in reference.csv
gespeichert. holdout.csv enthält alle 24 Vergleiche einschliesslich des einzigen
Überschreitens der 10-Prozent-Grenze. holdout.log enthält die Zusammenfassung.

logcheck_values.csv, logcheck_slopes.csv, logcheck_precision.csv,
logcheck_precision_slopes.csv und ray_audit.csv dokumentieren die Stufen der
ergänzenden Prüfung. ray_audit.log enthält die Steigungen aus dem feinen
Strahlenintegral. Die Daten sind deterministische Erwartungswerte, es wurden keine
neuen einzelnen Kausalordnungen simuliert oder Zufallszahlen verwendet.
SHA256SUMS.txt enthält die Prüfsummen der übrigen Paketdateien.
