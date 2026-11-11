# Vollständige Asymmetrieprüfung (2,3) v0.1

Die feste Klasse mit zwei und drei Astereignissen, vier festen äußeren
Dichte-Nullzeilen und frei variiertem positivem Endpunkt besitzt keine
vollständige innere stationäre Lösung. Der besondere Kragenfall P=0 wird
ausdrücklich mitbehandelt. Unter einer notwendigen Teilmenge der Gleichungen
gilt C_j > 1 + 87(h-g)^2/32, während die Endpunkt-Dichtevariation C_j=0 fordert.
Die Aussage überträgt sich durch Asttausch auf (3,2).

[Bericht](CST_DUST_Vollstaendige_Asymmetriepruefung_2_3_v0_1.pdf) ·
[Herleitung](DERIVATION.md) · [Prüfvertrag](stationarity_contract.json) ·
[Ergebnisse](results/) ·
[Prüfpaket](CST_DUST_Vollstaendige_Asymmetriepruefung_2_3_v0_1_Pruefpaket.zip)

Alle sechs Norm- und sechs Uhrgleichungen sind enthalten. 26 symbolische
Identitäten, 1.458 Profile und je 8.748 unabhängige Uhr-/Dichteableitungen
sind exakt geprüft. Neun bedingte Zeugen sind ausdrücklich keine vollständigen
Lösungen. Vier Ergebnisdateien sind isoliert bytegleich reproduzierbar.

```sh
python3 -O -B verify_package.py
python3 -O -B replay.py
```

Die Rechnung benötigt nur Python 3 und die Standardbibliothek.
`build_report.py` benötigt zusätzlich ReportLab und DejaVu-Schriften.
`package.py` erzeugt das Manifest und ein deterministisches ZIP.

Alle acht physikalischen Gates bleiben HOLD. Kein allgemeines CST-Verbot,
kein physikalischer Außenraum oder Bounce, kein kostenpflichtiger Lauf,
keine externe Replikation. Die Schranke behandelt exakt erfüllte
Teilgleichungen; ein Budget für Näherungsreste ist nicht abgeleitet.

Quelle: Main `c544521e4db792b9d01b083378a2cba5879a8a59`, PR 272.
Der Plan wurde nach dem analytischen Erstentwurf vor den endlichen Kontrollen
fixiert, ohne externe Präregistrierung. Nächste konkrete offene Klasse: (1,4).
