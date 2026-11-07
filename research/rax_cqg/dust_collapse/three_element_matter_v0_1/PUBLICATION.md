# Kontinuierlicher Drei-Element-Sektor v0.1

Arbeitspaket vom 7. November 2026. Basis ist Main nach PR 255,
Commit `9869528d008966a88052b65216da14eafce8db6f`.

## Ergebnis und Geltungsbereich

Die kontinuierlichen Uhr- und Dichtemarken aller sieben natürlich
beschrifteten Drei-Element-Ordnungen sind im geerbten Referenzmaß integriert.
Die Dichteintegration erfolgt analytisch; die Uhrintegration verwendet
positive Gauß-Legendre-Quadratur mit rationalen Ableitungsgrenzen und
nach außen gerundeter 160-Bit-Intervallarithmetik. Quadratur- und
Arithmetikfehler werden getrennt eingeschlossen.

Die größte Einzelgeometrie-Quadraturgrenze ist kleiner als `6.50e-12`,
der größte eingeschlossene Arithmetik-/Funktionsrest kleiner als `1.61e-37`.
Das vorab erklärte Amplitudenziel `1e-10` wird in allen Fällen erreicht.
Die Rechnung umfasst 42 Geometrieamplituden und 36 kombinierte Parameterfälle.

Durch die vollständige Integration des Sektors n=3 sinkt die obere Schranke
für das Gewicht der noch unbekannten Phasensektoren je nach Uhrhorizont und
Zahlgewicht um **91.36 bis 99.44 Prozent**. Alle 36 neuen Zahlkanal-
Erfolgsintervalle liegen innerhalb der zuvor zertifizierten Intervalle.
Feldphasen ab n=4 bleiben offen. Ihre Unsicherheit wird durch exakte
Normmassen für n=4,...,6 und einen analytischen Rest für n>6 eingeschlossen.
Die angegebene n=3-Quadraturgenauigkeit ist nicht der Gesamtfehler der
unbegrenzten Elementzahlsumme.

Die sieben natürlichen Ordnungen dürfen hier nicht durch fünf gleichgewichtet
summierte Isomorphieklassen ersetzt werden: Die monotone Uhr und ihre Marken
gehören zu den Records. Die geerbte Auslese bleibt ein kohärenter Filter
innerhalb der Zahlsektoren. Ein bloßer Elementzähler bleibt phasenblind.

**MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben HOLD.** Das Dichtemaß, kohärenter Zugriff auf vollständige
Historien und die Endrandwahl sind weiterhin Annahmen. Ein physikalischer
Detektor, eine vierdimensionale CST-Dynamik, gravitative Rückwirkung, ein
Bounce und ein Innen-/Außenraumanschluss werden nicht hergeleitet.

## Artefakte

- [Bericht (PDF)](../reports/CST_DUST_Drei_Elemente_Kontinuierliche_Materiephase_v0_1.pdf)
- [Originales Prüfpaket (ZIP)](../packages/CST_DUST_Drei_Elemente_Kontinuierliche_Materiephase_v0_1_Pruefpaket.zip)
- [Vollständige Herleitung](DERIVATION.md)
- [Maschinenlesbarer Vertrag](three_element_contract.json)
- [Nachrechnung und Nutzung](README.md)
- [Ergebnisstatus](results/verification.json)
- [Restgrenzen und Intervallverbesserung](results/tail_reduction.json)

## Verifikation

3780 rationale Kontrollen prüfen die vollständige Wirkung und ihre Inkremente;
56 niedrige Momente stimmen auf geordneter Uhrdomäne und Würfel exakt überein.
Drei Methodenvergleiche bestätigen die Verbindung zu den früheren exakten
Ein- und Zwei-Element-Momentreihen. Legendre-Nullstellen, positive Gewichte
und Monomiale bis Grad 2q-1 sind eingeschlossen beziehungsweise geprüft.

Eine zusätzliche Negativkontrolle deckt einen normierungserhaltenden Fehler
auf: Ohne den gesamten Jacobian wäre das uniforme Würfelmaß ebenfalls
normiert, aber der erste Materiemoment der Antikette bei h=1/2 wäre
`-107/216` statt `-5/8`. Normierungsprüfungen allein genügen deshalb nicht.

Sechs Ergebnisdateien werden in einem frischen Verzeichnis bytegleich
reproduziert. Der Replay berechnet alle neuen Integrale erneut und benutzt
keine neuen Ergebnis-Caches. Dies ist Wiederholbarkeit derselben
Implementierung, keine externe Replikation oder formale Beweiszertifizierung.
Der Plan wurde nach analytischer Methodenplanung und vor der neuen
Integralrechnung lokal eingefroren; keine externe Präregistrierung wird behauptet.

Vom Repository-Stamm, Python 3.12 und nur Standardbibliothek:

```bash
python3 -O -B research/rax_cqg/dust_collapse/three_element_matter_v0_1/publication_check.py --replay
```

Der Prüfer verifiziert das unveränderte Originalarchiv, alle 35 Mitglieder,
34 Manifest-Prüfsummen, beide PDF-Kopien, den eingefrorenen Plan, acht
bytegleiche Repositoryquellen und die Aussagegrenzen. Der Workflow
`cst-dust-three-element-matter.yml` führt Integrität und Replay auf Pull
Requests und Main aus. Es werden keine neuen physikalischen Ensembles
oder bezahlten Rechenläufe gestartet.

| Objekt | SHA-256 |
|---|---|
| Original ZIP | `e4afc101569a203e335e1286a833fa5ce9c115ce62ae2cb9e6df5598c01b3a5f` |
| PDF | `eade58888523f3640ffc3a8aa70e935a53d7e7f4d0534c513d8bf5dedb654c01` |
| Plan | `a2fcfbfbcd5c283ceeb4df612caf5e7d1e719617042671373931f8ff3e2225ed` |

Alle Originaldateien bleiben unverändert. Publikationsnotiz, Repository-
Prüfer, CI und Index-/Integritätsdateien werden ergänzend aufgenommen.

## Nächste wissenschaftliche Grenze

Quantitativ ist n=4 nach einem vorab festgelegten Kostenbudget der nächste
Kandidat. Physikalisch bleibt die Begründung von Dichtemaß, kohärentem
Historienzugriff und Randwahl aus einer physikalischen CST-Amplitude offen.
