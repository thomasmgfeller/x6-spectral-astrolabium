# CST-DUST: Positive Historien und Schnittkonsistenz v0.1

7. November 2026. Ein stark positives **Hilfs-Dekohärenzfunktional** ist mit
deklariertem Anfangszustand und positivem Randprodukt konstruiert. Das gemeinsame
relative Bra-/Ket-Uhrmaß und ein präzises Schnittkriterium sind hergeleitet.
Die physikalische Begründung von Randprodukt, Zustandsraum und Fortsetzung
bleibt offen.

**Neuer Befund:** Ein beschränkter roher Kern bei endlichem N, endlichen
Regulatoren und endlichen positiven Maßen ist Hilbert-Schmidt und kompakt.
Auf dem vollen unendlichdimensionalen L²-Eingangsraum kann er durch keine
einzige skalare Normierung isometrisch werden. Beschränkt äquivalente positive
Randnormen ändern das nicht. Eingeschränkte physikalische Zustandssektoren,
singuläre Kerne und kontrollierte Grenzprozesse sind nicht ausgeschlossen.

Das ist kein allgemeines No-go für CST. Der Satz zur Schnittkonsistenz setzt
eine bereits begründete lineare Fortsetzungsabbildung auf dem erreichbaren
Raum voraus; eine Markov-Fortsetzung auf bloßen CST-Randuhren wurde nicht
hergeleitet. **Alle acht physikalischen Audit-Gates bleiben HOLD.** Frühere
kandidatenspezifische FAILs bleiben bestehen.

[Bericht (PDF, sechs Seiten)](../reports/CST_DUST_Positive_Historien_Schnittkonsistenz_v0_1.pdf) ·
[Originales Prüfpaket (ZIP)](../packages/CST_DUST_Positive_Historien_Schnittkonsistenz_v0_1_Pruefpaket.zip) ·
[Vollständige Definitionen und Beweise](DERIVATION.md) ·
[Ergebnisse und Entscheidungen](results/verification.json)

## Ergebnisse und Reichweite

- Das verdoppelte Uhrmaß berücksichtigt die gemeinsame finale Uhr. Seine
  relativen Koordinaten haben E[rr′]=L²/3; ein unabhängiges Produkt der beiden
  marginalen Dreiecksmaße hätte null. 75 exakte Momentvergleiche bestätigen
  zwei unabhängige Herleitungen.
- Der geerbte Zweistellen-Kern ergibt für zwei normierte kontinuierliche
  Randfunktionen die zertifiziert verschiedenen Normfaktoren
  0.949281765835911… und 0.001646580694214… . Der numerische Zeuge verwendet
  ausdrücklich L=1; die frühere Hilfsbox L=4 bleibt unverändert.
- Drei Uhrintervalle erzeugen acht Ereignisse. Ihre positiven Diagonalen
  summieren sich zu etwa 0.333906725257478, während D(Ω,Ω)=1 gilt.
  Zertifizierte Interferenz verhindert ihre Interpretation als gewöhnliche
  Wahrscheinlichkeiten. Das sind keine physikalischen Bounce-Vorhersagen.
- 64 Hermitizitäts-, 432 Biadditivitäts-, eine Normierungs- und 64
  Grad-zwei-Identitäten sowie 64 positive quadratische Proben sind exakt
  ausgeführt. Die allgemeine starke Positivität folgt aus der Gramform,
  nicht aus endlich vielen Proben.
- 25 rationale Polynomvergleiche und 21 Schnittkontrollen ergänzen die
  Prüfung. Die unabhängige Quadratur umfasst 26 Vergleiche bei Ordnungen
  64 und 96; maximale Abweichung 4.45×10⁻¹⁶, ohne Intervallzertifizierung.
- Fünf exakte Ergebnisdateien werden isoliert bytegleich reproduziert.

Der Plan wurde lokal vor der Rechnung gehasht, ist aber keine externe
Präregistrierung oder blinde Vorhersage. `supplement_01.json` deklariert die
nach dem ersten Kernlauf ergänzten gemeinsamen Maßmomente und Quadraturen.
Der Entwicklungshinweis bleibt im Originalberichtspaket erhalten.

## Nachrechnung

Vom Repository-Stamm, Python 3.10+, nur Standardbibliothek:

```bash
python3 -O -B research/rax_cqg/dust_collapse/histories_v0_1/publication_check.py
python3 -O -B research/rax_cqg/dust_collapse/histories_v0_1/publication_check.py --replay
```

Die Prüfung pinnt das Original-ZIP, alle 29 Mitglieder, die PDF-Kopie, den
vollständigen Manifestinhalt, den Plan, fünf bytegleiche Vorgängertexte und
die abgegrenzten Entscheidungen. Der isolierte Replay regeneriert fünf
Ergebnisdateien aus Quellen und vergleicht alle Bytes und seine Quittung.
Die archivierte NumPy-Quadratur ist separat mit `verify_quadrature.py`
reproduzierbar; sie wird durch den Standardbibliothek-Replay nicht erneut
ausgeführt. Die CI prüft keine Beweise mit einem formalen Beweisassistenten.

`.github/workflows/cst-dust-histories.yml` führt die Integritätsprüfung und
isolierte Nachrechnung bei passenden Pull Requests und Änderungen auf Main aus.
Ein Software-PASS hebt keine physikalische HOLD-Entscheidung auf.

## Unveränderte Veröffentlichung

PDF, ZIP und alle 29 Originalmitglieder bleiben bytegleich. Nur diese
Übersicht und `publication_check.py` ergänzen den entpackten Komponentenordner.
Die fünf Herkunftstexte stimmen exakt mit den in `inputs/provenance.json`
gepinnten Repositorydateien überein. Frühere Eingabepräzisierungen bleiben
in den Originalquellen erhalten.

| Artefakt | SHA-256 |
|---|---|
| ZIP | `0abb7653154724bca81e850664db7f3015284416b6cacd5d69624438e89f0e28` |
| PDF | `b0db3a20fad2429921391694aac2b93182acf1a79b65061a77e4c26b5f50373c` |
| Plan | `1156cb82360481f8d3de1d4ba316e725157689babf9b578f8a689103c4538e55` |

Basis: Main `d9622fb0423725026fab73d6884a499322cb014f`, nach PR 247.
Keine neuen dynamischen 4D-Ensembles, keine gravitative Constraint-Herleitung,
kein physikalisches Junction-Gesetz und keine Singularitätsauflösung.
