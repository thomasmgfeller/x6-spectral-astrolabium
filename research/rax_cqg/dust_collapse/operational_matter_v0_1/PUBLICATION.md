# Messmodell und kontinuierliche Materiephase v0.1

Arbeitspaket vom 7. November 2026. Basis ist Main nach PR 254,
Commit `35a0d886c4a7ca1d639f09b2933ffeb6c255ad9e`.

## Ergebnis und Voraussetzungen

Ein explizites unitäres Hilfssystem realisiert die Elementzahlkanäle mit
kohärentem Filter. Ein bloßer Elementzähler ist gegenüber der Wirkungsphase
blind und genügt dafür nicht. Kohärenter Zugriff auf vollständige Historien
bleibt eine zusätzliche, physikalisch nicht hergeleitete Modellannahme.
Die endliche Kontrolle prüft eine rationale 16×16-unitäre Kopplung und
alle vier vollständigen Krausausgänge. Sie ist kein Hardwareentwurf und
keine Quadratur eines kontinuierlichen Zahlsektors.

Die kontinuierlichen Uhr- und Dichtemarken sind für n=0,1,2 mit exakten
rationalen Momenten bis Ordnung 48 integriert. Die größte analytische
Einzelamplituden-Restschranke der geprüften Fälle ist `10^49/49! < 1.65e-14`.
Die geerbten Wirkungsformeln werden an 390 rationalen Punkten geprüft;
16 niedrige Momente stimmen mit einem zweiten Integrationsweg überein.
Der Scan umfasst 36 Gewichts-/Uhrdauer-/Kopplungsfälle.

Bei h=1/2, g=pi/9 und mu=1 wird der bei mu=0 vollständig dunkle
Zwei-Geometrien-Ausgang positiv: Die Sichtbarkeit ist sicher zwischen
0.053484072766766 und 0.053484072766800 eingeschlossen. Dies ist ein
kontrollierter Effekt des erklärten Referenzinstruments und der Präparation,
kein Nachweis gravitativer Rückwirkung oder eines Bounce.

Feldphasen ab n=3 sind noch nicht ausgewertet. Ihre möglichen Beiträge
werden durch exakte Normmassen bis n=6 und einen analytischen Rest für
n>6 eingeschlossen. Der Fehler der n≤2-Integration ist ausdrücklich nicht
der Gesamtfehler der unbegrenzten Summe. Bei festem Uhrhorizont sind die
angegebenen unbegrenzten Erfolgsintervalle konservative Zertifikate.

Ein ignorierter Messausgang erhält in diesem Instrument die Elementzahl,
kann jedoch den Geometriezustand innerhalb eines Zahlsektors verändern.
Die Funktionalidentität des Vorgängers für vor der Endauslese definierte
Historienfragen ist nicht als Identität des nichtselektiven Nachmesskanals
zu lesen. Die normierten Zahlfilter sind bei festem n und h unabhängig
von alpha; alpha verändert die Präparationsgewichte zwischen den Zahlen.

**MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben HOLD.** Ein physikalischer Detektor, eine kosmologische
Endrandbedingung, eine vierdimensionale Quantendynamik und ein Junction law
sind nicht ausgewählt oder hergeleitet. Keine Singularitätsauflösung wird behauptet.

## Artefakte

- [Bericht (PDF)](../reports/CST_DUST_Messmodell_Kontinuierliche_Materiephase_v0_1.pdf)
- [Originales Prüfpaket (ZIP)](../packages/CST_DUST_Messmodell_Kontinuierliche_Materiephase_v0_1_Pruefpaket.zip)
- [Vollständige Herleitung und Geltungsgrenzen](DERIVATION.md)
- [Maschinenlesbarer Vertrag](operational_contract.json)
- [Nachrechnung und Nutzung](README.md)
- [Ergebnisse und Status](results/verification.json)

## Verifikation

Sechs Ergebnisdateien werden aus Quellen, Plan und gepinnten Eingaben in
einem frischen Verzeichnis bytegleich reproduziert. Dies ist Wiederholbarkeit
derselben Implementierung, keine externe wissenschaftliche Replikation oder
formale Beweiszertifizierung. Der Plan wurde lokal vor Implementierung
eingefroren; keine externe Präregistrierung wird behauptet.

Vom Repository-Stamm, Python 3.10 oder neuer, nur Standardbibliothek:

```bash
python3 -O -B research/rax_cqg/dust_collapse/operational_matter_v0_1/publication_check.py --replay
```

Der Publikationsprüfer kontrolliert das unveränderte Originalarchiv,
alle 31 Mitglieder, 30 Manifest-Prüfsummen, beide PDF-Kopien, den
eingefrorenen Plan, sechs bytegleiche Repositoryquellen und die
Ergebnisgrenzen. Der Workflow `cst-dust-operational-matter.yml` führt
Integritätsprüfung und isolierten Replay auf Pull Requests und Main aus.
Keine neuen physikalischen 4D-Ensembles und keine bezahlten Läufe.

| Objekt | SHA-256 |
|---|---|
| Original ZIP | `c5029b9d6dd5d32f0902ae2d57db8e73c2136f22a72b3b61aceb0690bc6fe681` |
| PDF | `d9f0ed39817d7bfc3b11bed29b8b8351122061514cf999e82c4dbb157cc79f31` |
| Plan | `386387f9d0c5db4c037ee6b6a678ed1bfcef83f6a01b47067f6d003b4c31e024` |

Alle Originaldateien bleiben unverändert. Publikationsnotiz, Repository-Prüfer,
CI und Index-/Integritätsdateien werden separat ergänzt.

## Nächste wissenschaftliche Grenze

Quantitativ ist die kontrollierte Feldphasenintegration ab n=3 der nächste
Ausbau. Physikalisch bleibt die Begründung kohärenten Historienzugriffs,
des Dichtepriors und der Endrandwahl offen. Eine unitäre Messdilatation
ersetzt diese Auswahl nicht.
