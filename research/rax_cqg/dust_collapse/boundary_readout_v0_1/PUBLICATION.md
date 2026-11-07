# Kohärente Randauslese und Dekohärenz v0.1

Arbeitspaket vom 7. November 2026. Basis ist Main nach PR 253,
Commit `36afc462dc5a9503616e9b016481e3b441b7c123`.

## Ergebnis und Voraussetzungen

Zwei ausdrücklich gewählte, beschränkte kohärente Endauslesen ergänzen den
Referenztransport vollständiger Historien. Der feste Randbezug ist der
normierte, phasenfrei entwickelte leere Anfangsrecord. Sein Rücktransport
stimmt zwischen den Zeitschnitten überein, wenn derselbe Enduhrwert, dieselben
Zahlgewichte und dieselbe Regulatorwahl beibehalten werden. Zurücktransportierte
Randvektoren dürfen nicht nachträglich normiert werden.

Bei reinem Anfangszustand ist der Rang einer Historien-Atommatrix durch den
Effektrang begrenzt. Eine Rang-eins-Endauslese erlaubt deshalb höchstens ein
positives Atom in einer exakt mittel-dekohärenten Partition. Normierte
Diagonalen eines interferierenden Funktionals sind keine gewöhnlichen
Historienwahrscheinlichkeiten: eine Negativkontrolle liefert den Wert 4.
Ein vollständig dunkler Ausgang darf nicht normiert werden.

Getrennte Elementzahlkanäle erhalten dagegen Interferenz zwischen Geometrien
innerhalb derselben Zahl und liefern eine normierte Verteilung ihrer
terminalen Zahl-Ausgänge. Die frühere Historienpartition dekohäriert dadurch
nicht automatisch; in allen zwölf geprüften atomaren Fällen bleibt sie
bei beiden Auslesen nicht mittel-dekohärent. Unbeobachtete Ausleseergebnisse
geben die phasenblinde ursprüngliche Recordverteilung zurück.

Ein kontinuierlich integrierter Gravitationstest zeigt exakte Interferenz.
Bei Zahlgrenze 2, alpha=1, h=1/2 und Materiekopplung null ergibt g=pi/9
für die Zahlkanäle einen Gesamterfolg 12/13 und die bedingte Verteilung
(2/3,1/3,0). Die Enumeration bis n=6 besitzt die analytische
Zustandssummen-Restschranke 1/604800. Das kontinuierliche Integral bei
nichtverschwindender Materiekopplung wurde nicht ausgewertet. Die gesonderten
atomaren Kontrollen beider Wirkungsphasen sind keine zertifizierte Quadratur.

**MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben HOLD.** Die Randwahl, Zahlgewichtung und der Enduhrwert
sind physikalisch nicht ausgewählt. Insbesondere ist der Referenzeffekt
kein abgeleitetes Innen-/Außenraum-Junction law. Kein Bounce, keine
Singularitätsauflösung und kein allgemeines CST-No-go werden behauptet.

## Artefakte

- [Bericht (PDF)](../reports/CST_DUST_Kohaerente_Randauslese_Dekohaerenz_v0_1.pdf)
- [Originales Prüfpaket (ZIP)](../packages/CST_DUST_Kohaerente_Randauslese_Dekohaerenz_v0_1_Pruefpaket.zip)
- [Vollständige Herleitung und Geltungsgrenzen](DERIVATION.md)
- [Maschinenlesbarer Auslesevertrag](boundary_contract.json)
- [Nachrechnung und Nutzung](README.md)
- [Ergebnisse und Status](results/verification.json)

## Verifikation

Geprüft sind 921 atomare Endrecords, 6.240 Rücktransportgleichheiten und
72 Vergleiche derselben vergangenen Ereignisfunktionale. Die Prüfung umfasst
positive Kontraktionen, Erfolgs-/Ausfallvollständigkeit, Hermitizität,
starke Positivität, Ereignisadditivität und die Grad-zwei-Regel.
Sechs Ergebnisdateien werden in einem frischen Verzeichnis bytegleich
reproduziert. Das ist Wiederholbarkeit derselben Implementierung,
keine unabhängige wissenschaftliche Replikation oder formale Beweiszertifizierung.

Vom Repository-Stamm, Python 3.10 oder neuer, nur Standardbibliothek:

```bash
python3 -O -B research/rax_cqg/dust_collapse/boundary_readout_v0_1/publication_check.py --replay
```

Der Publikationsprüfer kontrolliert das unveränderte Originalarchiv,
alle 30 Mitglieder, 29 Manifest-Prüfsummen, beide PDF-Kopien, den
eingefrorenen Plan, sechs bytegleiche Repositoryquellen und die
Ergebnisgrenzen. Der Workflow `cst-dust-boundary-readout.yml` führt
Integritätsprüfung und isolierten Replay auf Pull Requests und Main aus.
Keine neuen physikalischen 4D-Ensembles und keine bezahlten Läufe.

| Objekt | SHA-256 |
|---|---|
| Original ZIP | `f4ae8ff4b00a07eb2fd398d9a45cb421fb9fa121835a92df495258eb6c6183a0` |
| PDF | `a1fdb8fde19e8b744508930689523e0d975ffebdcc6ef7c2fd5e224c7c97e43a` |
| Plan | `01597b51c463b22c0f4302676009d2563966ba2ac7f900c4c9238b413fa82a83` |

Alle Originaldateien bleiben unverändert. Publikationsnotiz, Repository-Prüfer,
CI und Index-/Integritätsdateien werden separat ergänzt.

## Nächster Entscheidungspunkt

Die Rand-Auslese und die dazu passende Ereignisalgebra operational oder
dynamisch begründen. Anschließend die kontinuierliche Materiephase mit
kontrollierten Integrationsfehlern sowie Robustheit gegen Zahlgewichtung
und Enduhrwert prüfen. Eine neue Randannahme bleibt als Modellentscheidung
auszuweisen; sie wird nicht durch eine weitere Normierung physikalisch hergeleitet.
