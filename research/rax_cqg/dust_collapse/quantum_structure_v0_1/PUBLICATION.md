# CST-DUST: Zustandsraum und Constraints v0.1 · Veröffentlichung

Ein positiver Hilfshistorienraum, sein Testbereich, die vollständige
Umbenennungsdarstellung und die zugehörigen Constraints sind explizit definiert.
Die Gruppenmittelung liefert ein positives Quotientskalarprodukt. Diese
Reduktion entfernt Labels; sie ist noch keine gravitative dynamische Reduktion
und kein nachgewiesen vollständiger physikalischer Randzustandsraum.

**Der vollständige physikalische CST-Zustandsraum und seine Dynamik bleiben
HOLD.** Aus der gemeinsamen Geometrie-Materie-Amplitude müssen dynamische
Constraints samt physikalischem Skalarprodukt, ein relationaler Hamiltonoperator
oder eine konsistente kovariante Historiendynamik erst gewonnen werden.

[Bericht (PDF, neun Seiten)](../reports/CST_DUST_Zustandsraum_Constraints_v0_1.pdf) ·
[Originales Prüfpaket (ZIP)](../packages/CST_DUST_Zustandsraum_Constraints_v0_1_Pruefpaket.zip) ·
[Definitionen, Beweise und Primärquellen](DERIVATION.md) ·
[Exakte Ergebnisse](results/verification.json)

## Ergebnisse und Reichweite

- 3 671 markierte Zustände, 85 035 Gruppenwirkungen, 234 Orbits und 4 817
  gemeinsame Geometrie-/Feldumbenennungen bestätigen die endliche Labelreduktion.
- Die direkte Staub-Eulerbedingung als Multiplikationsconstraint hat im gewählten
  gewöhnlichen L²-Raum auf jedem nichtleeren Staubstratum nur den Nullzustand.
  Der Beweis gilt bei frei kontinuierlichen Uhren vor Randkonditionierung;
  7 249 Polynomkontrollen illustrieren ihn. Distributionelle Konstruktionen und
  anders hergeleitete dynamische Constraints sind damit nicht ausgeschlossen.
- Für den unveränderten Zweistellen-Kern wird zusätzlich die Identifikation der
  Uhrlabels (0,1) und (2,3) durch Translation festgelegt. **Kein gemeinsames
  positives Hermitesches M** erfüllt dann K†MK = cM mit c > 0. Das notwendige
  reelle Spektralkriterium scheitert: Im[(tr K)²/det K] liegt zertifiziert bei
  etwa −2,45273. Dies schließt weder unabhängig begründete unterschiedliche
  Randprodukte noch vollständige Randräume, Constraint-Deutungen oder
  kontrollierte Verfeinerungsfamilien aus.
- Eine vollständig lösbare distributionelle Constraint-/Evolutionsreferenz
  besitzt ein positives physikalisches Produkt, vier exakte Unitaritäts- und
  16 Kompositionskontrollen. Ihr Hamiltonoperator ist **nicht aus CST abgeleitet**.

Zwei neue, getrennte P1-Datensätze: `CST-DUST-QS1-RELABEL` hält alle acht
physikalischen Entscheidungen offen; `CST-DUST-V1-RAW-K-COMMON-M` ergibt
MODEL=FAIL für die ausdrücklich gemeinsame-M-Interpretation und sieben HOLD.
Die früheren Datensätze bleiben unverändert. **Junction-Gesetz, gemeinsamer
Außenraum, Regularität und globaler Bounce bleiben offen.** Keine neuen
physikalischen 4D-Ensembles, Sprinklings, Zufallsdaten oder bezahlten Läufe.
Strukturelle Hindernisse waren vor der numerischen Zertifizierung erwartet;
der lokale Plan ist keine externe Präregistrierung oder blinde Vorhersage.

## Reproduzieren

Vom Repository-Stamm aus, Python 3.10 oder neuer, ausschließlich Standardbibliothek:

```bash
python3 -O -B research/rax_cqg/dust_collapse/quantum_structure_v0_1/publication_check.py
python3 -O -B research/rax_cqg/dust_collapse/quantum_structure_v0_1/publication_check.py --replay
```

Die Prüfung kontrolliert die Originalbytes von ZIP, PDF und allen 34
Archivmitgliedern, das vollständige SHA-256-Manifest, Vorgängereingaben,
Plan und ausgeführte Quellen. Beide P1-Datensätze werden erneut mit dem
unveränderten geerbten Gate auditiert.

Der Replay entpackt isoliert, löscht die archivierten Ergebnisse und erzeugt
alle 13 Ergebnisdateien neu. Nur die Python-Version im Laufmanifest und die
davon abhängigen, separat geprüften Manifestverweise der beiden Datensätze
dürfen zwischen Laufzeiten abweichen. Wissenschaftliche Ergebnisse und
Entscheidungen müssen gleich bleiben. Der ursprüngliche Lauf unter Python
3.12.14 wurde vollständig bytegleich reproduziert.

`.github/workflows/cst-dust-quantum-structure.yml` prüft Pull Requests und
Änderungen auf Main. Software-PASS bestätigt die Reproduktion dieser
abgegrenzten Ergebnisse; es hebt keine physikalische HOLD-Entscheidung auf.
Originalpaket und Inhalt bleiben bytegleich. Nur `PUBLICATION.md` und
`publication_check.py` ergänzen hier die Repository-Einbindung.

| Artefakt | SHA-256 |
|---|---|
| Original-ZIP | `734d37c423208a0362d5ef1997364ae178be30b5e9c64b657006261592695624` |
| Bericht | `3242dcacd9251eb1b653690fa57d6e7418616fee225de05f29c1df514aaf3712` |
| Fixierter Plan | `95412203ca3292d9dfb51d8b7e0628230c0cb783ff174e2a98668a5c6a22fa3e` |

Projektbasis: Main-Commit `3595df81b8655a5183cdbf5c5da077aef51e4259` nach PR 245.
