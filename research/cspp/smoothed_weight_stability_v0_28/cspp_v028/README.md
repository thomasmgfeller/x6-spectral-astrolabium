# CSPP v0.28 - Geglättete Intervallgewichte und schärfere Stabilitätsbudgets

1. November 2026, Basis Main nach PR #160.

**Ergebnis:** Der Maximalbetrag der tatsächlichen binomial geglätteten
Intervallgewichte ersetzt die grobe Hülle max|c_k| aus v0.27. Eine exakte
Binomialkomposition überträgt den Nachweis auf sämtliche höheren Dichten.
Die unendlich vielen Intervallzahlen werden durch vollständige rationale
Prüfung eines Anfangsbereichs und einen analytischen monotonen Rest erfasst.

Für theta=21 sinkt bei festem q, T=9/4, H=4, delta=0.01 und rho>=3/pi
die gemeinsame hinreichende 99-Prozent-Verstärkungsobergrenze von etwa
225.5 Millionen auf etwa 82030 (Faktor 2749). Bei exakter History sinkt
die aktive Grenze von etwa 89858 auf etwa 585.

Das ist keine gemessene Fehlerreduktion. Der theta=21-Genauigkeitsausschluss,
METHOD=HOLD und G1=HOLD bleiben bestehen. Langzeitstabilität, unendliche
History und signierte Aufhebung zwischen unterschiedlichen Pfaden sind
weiterhin offen. Die neue Hülle gilt ab der ausgewiesenen Dichteuntergrenze.

## Reproduktion

```bash
python3 -B reproduce.py
python3 -I -O -B reproduce.py --check
```

Nur Python 3.12 und Standardbibliothek; keine Netzzugriffe oder Zufallswolken.
Sechs globale Gewichtszertifikate, 1782 ganzzahlige Gewichte auf drei
Rechenwegen, 648 Binomialkompositionen, 2442 Operatorfälle und ebenso viele
History-Kontrollen, sechs Negativkontrollen, zehn Budgetzeilen in drei
Präzisionen sowie Abgleich mit den archivierten v0.27-Intervallen.

Die endlichen Graphkontrollen verwenden einen rationalen Vorfaktor 1/7;
die tatsächlichen physikalischen Konstanten werden separat eingeschlossen.
Fünf Quellen sind durch Git-Blob und SHA256 gesichert. Die unveränderte
v0.27-Reproduktion liefert ausgewiesene gemeinsame Prüfroutinen.

## Dateien

- `PROOF.md`: vollständige Definitionen, Beweise, Quantoren und Grenzen.
- `reproduce.py`, `results/RESULTS.json`: exakte Zertifikate und Zahlenintervalle.
- `STATUS.json`: getrennte Entscheide und offene Aufgaben.
- `evidence/`: unveränderte Projektquellen und Hashprovenienz.
- `report/`: PDF-Zusammenfassung und wissenschaftliche Abbildung.
- `build_report.py`, `requirements-report.txt`: Berichtserstellung.
- `SHA256SUMS`: Integrität aller übrigen Paketdateien.

Keine Beweisassistent-Verifikation, kein externes Peer Review und kein
Neuheitsanspruch. GitHub-Publikation ist nicht Teil dieses Entwicklungsschritts.

Der nächste Auftrag ist eine Intervallvolumen-abhängige Pfadmajorante unter
Poisson, mit weiterhin expliziter History- und Detektorkopplung. Die
Unabhängigkeit disjunkter Einzelkettenintervalle darf dabei nicht auf
überlappende Pfadpaare übertragen werden. Die Grad-5-Genauigkeit bleibt separat offen.
