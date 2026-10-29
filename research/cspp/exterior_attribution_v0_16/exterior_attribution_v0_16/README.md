# CSPP v0.16: Aeussere Forcierung und endliche Fehlerzuordnung

Die vier vorhandenen Paare Omega4/Omega5 werden fuer den unveraenderten
kompakten KG-Detektor ausgewertet. Es werden vollstaendige diskrete
Gebietserweiterung und vorgeschriebene KG-Aussenwerte getrennt berechnet.

**METHOD_HOLD und G1 HOLD bleiben bestehen.** Die gesamte unendliche
Vergangenheit ist nicht zertifiziert. Die endliche Omega5-Restabweichung
ist kein isolierter intrinsischer Operatorbias.

* `METHODS.md`: Herleitung, lokale Supportaussage und konditionales Restlemma.
* `PROTOCOL.json`: Entwicklungsplan, feste Quelle, Fenster, Gitter und Grenzen.
* `results/COEFFICIENTS_192.json.gz`: validierte volle Detektorkoeffizienten.
* `results/ATTRIBUTION_128.json.gz`, `_192.json.gz`: Aussenhistory,
  diskrete Aussenwerte, signierte Transfers und Fehlerintervalle.
* `results/CHECKS.json`: Intervallvergleich, unabhängige rationale
  Kausalzaehlungen und Negativkontrollen.
* `AMENDMENT_01.json`, `development_initial/`: erhaltene erste Auswertung
  vor einer rein algebraischen Schaerfung der Intervallauswertung.
* `PUBLIC_SOURCE_TREE.json`: Quelldateien gegen den oeffentlichen Git-Stand.

Aus dem Paketwurzelverzeichnis, Python 3.12 und C++17-Compiler:

```bash
python3 -m pip install -r exterior_attribution_v0_16/requirements.txt
python3 -B exterior_attribution_v0_16/exterior.py solve --bits 128
python3 -B exterior_attribution_v0_16/exterior.py solve --bits 192
python3 -B exterior_attribution_v0_16/verify.py
```

Diese Wiederholung verwendet die mitgelieferten, gehashten Detektorkoeffizienten.
Ihre vollstaendige Neuberechnung ist mit `python3 -B
exterior_attribution_v0_16/exterior.py coefficients` moeglich. Vorher das Paket
kopieren, damit die veroeffentlichten Ergebnisse erhalten bleiben.
Die einmalige 192-Bit-Raumquadratur wird von beiden Loesungsrechnungen
gemeinsam verwendet; 128/192 Bit sind keine zwei unabhaengigen Raumquadraturen.

Keine Zufallsaufrufe, keine neue Bestaetigungsstichprobe, kein geaendertes
Fehlerziel. Der Ausschluss einer endlichen Konfiguration darf nicht als
Ausschluss aller Gebiete oder der gesamten Operatorfamilie ausgegeben werden.
