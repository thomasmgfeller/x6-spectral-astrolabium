# CSPP v0.27 - Lokale Stabilität auf endlichen Zeitfenstern

Aufbauend auf v0.26, Main nach PR #159.

**Ergebnis:** Für Poisson-Kausalsets in 1+3 Minkowski-Raum und strikt kausale
Transfers mit `|K_ij| <= kappa/rho` gilt für eine feste passive Probe
`E G <= F(T)` und `P(G > 1+(F(T)-1)/delta) <= delta`, wobei
`F(T) = sum (8*pi*kappa)^k T^(4*k)/(4*k)!`.
Die Konstante ist bei festem q und endlichem T unabhängig von rho und der
räumlichen Erweiterung des Rechengebiets. Ein festes Detektormittel ist
eingeschlossen; das globale räumliche Maximum und T->infinity sind es nicht.

Eine eigene Schranke behandelt vorgeschriebene History ohne künstliche
History-zu-History-Propagation. Die Bedingung wird für die binomial geglättete
Intervallfamilie nachgewiesen. Die Konstanten sind für die ursprüngliche
Aufgabe noch grob. Die Genauigkeitsausschlüsse aus v0.25 gelten weiter.
METHOD und G1 bleiben HOLD.

## Reproduktion

```bash
python3 -B reproduce.py
python3 -O -B reproduce.py --check
```

Nur Python-Standardbibliothek erforderlich. Keine Netzabfragen, keine Seeds,
keine neuen Poisson-Wolken. 407 Ordnungen; 3256 Operatorfälle plus 3256
Fälle mit eingefrorener History; drei unabhängige rationale Lösungswege;
72 Integralidentitäten; sechs Negativkontrollen; drei Präzisionen.
Die endlichen Algebra-Kontrollen verwenden den rationalen Vorfaktor 1/7;
die physikalischen Zahlenbudgets werden getrennt eingeschlossen.

Die endlichen Kontrollen ersetzen keinen allgemeinen Beweis. Dieser steht
in PROOF.md. Keine Beweisassistent-Verifikation und kein externes Peer Review.

## Inhalt

- PROOF.md: Definitionen, vollständige Herleitungen, Quantoren und Grenzen.
- reproduce.py und results/RESULTS.json: reproduzierbare exakte Kontrollen.
- STATUS.json: getrennte Entscheidungen ohne physikalische Freigabe.
- evidence/: unveränderte, mit Git-Blob und SHA256 gesicherte Projektquellen.
- report/: PDF-Zusammenfassung und wissenschaftliche Abbildung.
- build_report.py: Berichtserstellung mit ReportLab und Matplotlib.
- SHA256SUMS: Integrität aller anderen Paketdateien.

Es wurde in diesem Entwicklungsschritt nicht neu auf GitHub veröffentlicht.

## Nächster präziser Auftrag

Die grobe Koeffizientenhülle durch kontrollierte Intervall- und signierte
Pfadabschätzungen ersetzen, mit gleicher Norm, festem Zeitfenster, explizitem
Ausfallbudget, vorgeschriebener History und unverändertem Detektor. Eine
Einzelpfadidentität ersetzt keine Kontrolle korrelierter Pfadpaare.
Der unabhängige Grad-5-Genauigkeitsauftrag bleibt offen.
