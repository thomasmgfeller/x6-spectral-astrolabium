X6 Detektionsqualifikation v0.1 — 2026-11-05

Status: DESIGNAUSWERTUNG / PRÜFVORBEREITUNG. Hardware NOT_RUN. BOM HOLD.
Die Referenzdetektion, das Niedervolt-Eigenfrontend und der spätere vollständige
APD-Detektor haben getrennte Freigaben. Es werden keine Geräte angesteuert.

Start mit X6_Detektionsqualifikation_v0_1.pdf und Referenzvertrag.json.
Referenzmessung.template.json kopieren, reale Identität/Konfiguration/Grenzen
und Belege eintragen. Leere Felder sind unbekannt, niemals Nullmessungen.
Alle Bedingungen gelten für sämtliche vorgesehenen Lasten/Temperaturen;
Grenzen sind konservative Hüllen inklusive dokumentierter Unsicherheit.
Bei |Offset| und |Drift| den Betrag plus Unsicherheitsgrenze liefern.
Zählgrößen müssen exakte ganze Zahlen sein, keine gerundeten Schätzwerte.

Python >=3.10; Auswertung und Tests benötigen nur die Standardbibliothek:
  python3 -m unittest discover -s . -p 'test_*.py' -v
  python3 analysis.py design
  python3 analysis.py reference Referenzmessung.template.json --evidence-root .
  python3 analysis.py timing messung_timing.json
  python3 analysis.py coincidences messung_koinzidenzen.json
  python3 verify_package.py

Der Referenzscreen erwartet konservative Intervallgrenzen aus geprüften
Messungen. Er extrahiert keine Oszillogramme, berechnet keine Messunsicherheit
und beglaubigt keine Kalibrierung. Reviewer, lokale Belegdateien und deren
SHA-256 müssen angegeben werden. Vollständige synthetische Daten führen nur
zu SYNTHETIC_ONLY. Selbst ein NUMERICAL_SCREEN_PASS realer Daten verlangt eine
unabhängige physische Freigabe und lässt die BOM auf HOLD.
Die Test-Fixture ist explizit synthetisch und erzeugt keine Produktnachweise.

Das Paket enthält keinen fertigen Swabian-.ttbin-Konverter. R10 bleibt bis zur
validierten Implementierung und Prüfung der konkreten SDK-Kette offen.
Konfigurationsfelder sind der abstrakte Prüfvertrag, keine SDK-Methodennamen.
Originale readback/configuration Dumps unverändert archivieren.

Timing: Alle sechs Kanalpaare, vollständige Verteilung; vor Statistik werden
integer-ps-Zeitmarken subtrahiert. Keine Nachzentrierung und kein Beschneiden
auf das Koinzidenzfenster. Confidence/Uncertainty nicht automatisch berechnet.
Koinzidenzen: maximal 100000 Tags und 500000 Kanten, nur Diagnose kleiner
Datensätze. Bipartite Komponenten zählen eindeutige 1:1-Paare, mehrdeutige
Komponenten und ungepaarte Singles. Nicht die Streaming-CHSH-Primärpipeline.
PDE-/Afterpulse-Funktionen liefern nur modellbedingte Punktwerte.
Poisson-Grenzen gelten nur bei geeigneter Stationaritäts-/Zählmodellannahme.

Quellen.json verlinkt Herstellerunterlagen; keine fremden PDFs im Paket.
Systemziele_Basis.json ist eine unveränderte lokale Projektkopie des
veröffentlichten Vertrags. Neue Entwicklungsziele sind ausdrücklich markiert.
Eigene Beiträge: Apache-2.0 entsprechend X6-Projektumfang.
