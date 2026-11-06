# Regularität v0.2 - eigenständiges Prüfpaket

Die wissenschaftliche Entscheidung steht in DERIVATION.md und im PDF.
Status: CST-Singularitätsauflösung HOLD. Neuer anfangs momentenregulärer
kontrahierender Gegenbeispielzustand; uniformes Tail-Kriterium;
bedingter Ausschluss des glatten Schwarzschild-Anschlusses der effektiven Bounce-Metrik.

## Reproduktion

```sh
sha256sum -c SHA256SUMS
python3 verify.py
```

NumPy und SciPy werden benötigt. Der Prüfer regeneriert Ergebnisse und kontrolliert
exakte rationale Identitäten sowie numerische Referenzvergleiche. Numerische
Kontrollen sind keine rigorosen Intervallzertifikate. Die Divergenz und der
Anschlussausschluss werden analytisch im Bericht bewiesen.

`make_report.py` erzeugt zusätzlich Abbildungen und PDF mit Matplotlib und ReportLab.
Dateien in `results/` sind synthetische mathematische Referenzrechnungen.
Es wurden keine neuen CST-Ensembles erzeugt und keine Horizontereignisse berechnet.

Parameter und Grenzen wurden nicht zur Erzeugung eines positiven Regularitätsbefunds angepasst.
Dieses Paket dokumentiert eine analytische Untersuchung, keine externe Präregistrierung.
