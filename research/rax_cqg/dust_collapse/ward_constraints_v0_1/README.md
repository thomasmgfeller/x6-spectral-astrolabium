# CST-DUST: Uhrsymmetrie, Constraints und Atomgrenze v0.1

Die vorhandene Uhrverschiebungssymmetrie begründet den Variationsstrom, nicht
die binäre Sektorladung des zusätzlichen Referenzmodells. Im geankerten
Randmodell gilt am ersten freien Element C₁≥1; eine naive Übertragung der
klassischen Normierung auf Quantenzustände liefert keinen positiven ersten
Dichtesektor. Der regulierte Amplitudenkandidat leitet diese zusätzliche
Constraint-Quantisierung nicht her.

Für festes endliches n konvergiert die Materieamplitude bei starker Materiephase
zu 2^(-n), dem ursprünglichen Gewicht des Stratum mit ausschließlich verschwindenden
Dichtegewichten. Keine unendliche n-Summe, kein gravitativer oder physikalischer
semiklassischer Grenzwert ist damit kontrolliert. Alle acht physikalischen Gates
bleiben HOLD.

- `DERIVATION.md`: vollständige Beweise, Domainbedingungen und Primärquellen.
- `constraint_contract.json`: maschinenlesbarer Geltungsbereich und offene Physik.
- PDF: sechsseitiger Ergebnisbericht.
- `results/`: exakte kleine Kontrollen und rationale Funktions-Einschlüsse.
- `inputs/`, `provenance.json`: sechs gepinnte Quellen einschließlich Lizenz.

## Reproduktion

```sh
python3 -B verify_package.py
python3 -B replay.py
```

Nur Python 3 und die Standardbibliothek werden benötigt. Die isolierte
Nachrechnung verlangt Bytegleichheit von fünf Ergebnisdateien. Kein Netz,
keine Cloud und kein n=5-Produktionslauf. Das Kontrollgitter enthält höchstens
drei neue Elemente. Allgemeine Aussagen beruhen auf den ausgeschriebenen Beweisen.

Der Plan wurde nach analytischem Entwurf und Quellenprüfung vor den endlichen
Kontrollen eingefroren. Ein zusätzlicher rationaler Vergangenheitskragen ist
als nachträglicher analytischer Zeuge getrennt ausgewiesen; er erfüllt nur
die Normierung eines Elements, nicht dessen Uhrgleichung oder das Gesamtsystem.
Das Paket ist keine externe Replikation oder Beweisassistentenprüfung.

`build_report.py` benötigt optional ReportLab und DejaVu-Schriften.
`package.py` erzeugt aus der unveränderten PDF-Datei und dem expliziten Manifest
ein deterministisches ZIP; ein Neu-Rendern des PDFs kann Metadaten ändern.

## Wissenschaftliche Konsequenz

Zuerst sind Vergangenheitskragen, Randzustand, erlaubte Dichtevariation und
Quantisierungsregel gemeinsam physikalisch zu begründen. Kleine gewichtete
Constraint-Residuen genügen ohne Spektrallücke nicht zur Zustandsqualifikation.
Feste absolute Uhrboxen und mitverschobene relative Uhrfenster haben verschiedene
Randterme und dürfen nicht verwechselt werden.

Die analytische Dichteintegration war bereits im Vier-Element-Kern implementiert.
Dieses Paket beansprucht daraus keine neue Einsparung. Es enthält keinen
automatischen Produktionslauf und keinen Finanzierungsauftrag. Freiwillige
fachliche Prüfung oder Nachrechnung auf vorhandener Hardware begründet keinen
Anspruch auf Kostenerstattung durch Thomas Gfeller.

Basis: Main nach [PR 264](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/264),
Commit `0ee861d67f7d28e2c2762ef01e70f428796f1f53`. Lizenz: Apache-2.0.
