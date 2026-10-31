# CSPP v0.26 - Uniforme Stabilität: Grenze und Pfadkriterium

Ausgeführt am 31. Oktober 2026, auf Basis von Main nach PR #158.

**Ergebnis:** Nichttriviale, realisierungsunabhängige Intervallkerne besitzen
keine deterministische l-infinity-Verstärkungsschranke über alle endlichen
Kausalsets. Eine exakte, Minkowski-realisierbare Fächerfamilie erreicht
`||(I-K)^(-1)|| = 1 + M |t(r)|`. Der Ausschluss umfasst alle
nichtsingulären Parameter der v0.25-Familie. Er betrifft ausdrücklich
Worst-Case-Stabilität, nicht typische zeitliche Dynamik oder den KG-Detektor.

Ein hinreichender Satz nach exakter interner Pfadelimination und eine
analytisch lösbare Zellenfamilie liefern eine positive Gegenkontrolle.
Der positive Satz ist noch nicht auf eine physikalisch qualifizierte
GCB-Familie angewandt. METHOD und G1 bleiben HOLD.

## Dateien

- `PROOF.md`: vollständige Definitionen, Beweise, Quantoren und Grenzen.
- `reproduce.py`: exakte endliche Kontrollen, nur Python-Standardbibliothek.
- `results/RESULTS.json`: rationale Ergebnisse und eingeschlossene Konstanten.
- `evidence/`: unveränderte Projektquellen mit Git-Blob- und SHA256-Prüfung.
- `STATUS.json`: getrennte Entscheidungen und offene Aufgaben.
- `report/`: PDF-Zusammenfassung und Visualisierung.

## Reproduktion

```bash
python3 reproduce.py
python3 reproduce.py --check
```

Die erste Ausführung erzeugt das Ergebnis; `--check` vergleicht es bytegenau.
Der PDF-Bericht benötigt zusätzlich ReportLab und Matplotlib; die mathematischen
Kontrollen benötigen beide nicht. Es werden keine Netzabfragen vorgenommen.

Die endlichen Tests sind keine formale Verifikation des allgemeinen Beweises.
Kein externes Peer Review, keine Prioritätsbehauptung, keine neuen Poisson-Wolken.
Die Grad-5-Kandidatenentwicklung und probabilistische Stabilitätsprüfung bleiben offen.
