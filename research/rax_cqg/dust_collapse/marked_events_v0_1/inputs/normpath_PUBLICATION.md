# CST-DUST: Normpfad und kohärenter Quotient v0.1

7. November 2026. Positive diagonale, feldunabhängige Hilfsnormpfade für die
vollständige Vergangenheit sind durch h(P)=e(P)²μ(P) klassifiziert. μ ist ein
konsistentes positives Zylindermaß, e(P) die Zahl linearer Erweiterungen.
Eine bekannte transitive Perkolationsfamilie liefert allstufige Beispiele,
ohne die ursprünglichen Fortsetzungsamplituden zu verändern. Positivität
und Isomorphieinvarianz wählen keine eindeutige physikalische Norm aus.

**Neue Grenze:** Unter h₀=1 besitzt die unveränderte kohärente Endsumme auf
den vollständigen Räumen dieser diagonalen Klasse keine gemeinsame
Operatornormschranke über die Elementzahl. Der allgemeine Beweis verwendet
Cauchy-Schwarz und eine Zweischicht-Zählabschätzung; er beruht nicht auf einer
Extrapolation der endlichen Kontrollen.

[Bericht (PDF, sechs Seiten)](../reports/CST_DUST_Normpfad_Kohaerenter_Quotient_v0_1.pdf) ·
[Originales Prüfpaket (ZIP)](../packages/CST_DUST_Normpfad_Kohaerenter_Quotient_v0_1_Pruefpaket.zip) ·
[Vollständige Herleitung](DERIVATION.md) ·
[Normvertrag](norm_contract.json) ·
[Ergebnisse und Entscheidungen](results/verification.json)

## Ergebnisse und Geltungsbereich

- Bei passender terminaler Wahl sind die Perkolations-Hilfsnormen exakt
  unabhängig vom Endhorizont. Die untersuchten Parameter 1/4, 1/2 und 3/4
  ergeben verschiedene relative Normen; kein physikalisches p wird gewählt.
- Für die unveränderte kohärente Endkontraktion gilt auf der erklärten
  diagonalen Normklasse
  `||ell_m|| >= sum_P 1/e(P) >= 2^(floor(m/2)*ceil(m/2))/m! -> infinity`.
  Eingeschränkte physikalische Räume, distributionelle Endzustände sowie
  nichtdiagonale oder feldabhängige Produkte sind dadurch nicht ausgeschlossen.
- Im **unmarkierten Geometrie-Referenzsektor** ist die kohärente
  Labelidentifikation algebraisch mit der Fortsetzung verträglich. Eine
  Zweierkette und eine Zweierantikette tragen zum selben Kindtyp bei. Der
  erzwungene Kreuzterm `4*d/9 > 0` verhindert Isometrie mit positiven
  diagonalen Produkten auf dem ganzen Elternraum.
- Nichtdiagonale positive Produkte lassen sich über eine explizite
  Linksinverse konstruieren. Komplementprodukt, physikalische Ereignisse und
  gleichmäßige Schranken bleiben frei beziehungsweise offen. Der vollständige
  markierte Feldquotient ist nicht konstruiert.
- Ein abstrakter Hilbert-Induktivgrenzraum qualifiziert weder die ursprüngliche
  kohärente Endsumme noch die Fortsetzung ihres quantalen Vektormaßes.

Die unabhängige Vergleichsroute enumeriert 33.868 natürliche gerichtete
azyklische Graphen und bildet deren transitive Hülle. 15.696 rationale
Wahrscheinlichkeitsvergleiche, jeweils 1.224 Zylinder- und Normrekursionen
sowie 17.118 exakte Horizontvergleiche sind ausgeführt. Der Quotiententest
umfasst 88 Isomorphietypen einschließlich des leeren Typs, 51
Vertreterkontrollen und 87 erhaltene Endkoeffizienten. Acht rekursiv
konstruierte Produkte und eine zusätzliche 5×5-Matrix haben positive
rationale LDL-Zerlegungen.

**Alle acht physikalischen Gates bleiben HOLD:** MODEL, CURRENT,
CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION.
Kein allgemeines No-go für CST, keine physikalische Parameterwahl, kein
neues dynamisches 4D-Ensemble, kein Junction-Gesetz und keine
Singularitätsauflösung. Historische kandidatenspezifische FAILs bleiben bestehen.

## Nachrechnung

Vom Repository-Stamm, Python 3.10+, nur Standardbibliothek:

```bash
python3 -O -B research/rax_cqg/dust_collapse/normpath_v0_1/publication_check.py
python3 -O -B research/rax_cqg/dust_collapse/normpath_v0_1/publication_check.py --replay
```

Die Prüfung pinnt das Original-ZIP, alle 28 Mitglieder, die PDF-Kopie, den
vollständigen Manifestinhalt, den lokalen Plan und sechs bytegleiche
Vorgängerquellen. Die isolierte Nachrechnung erzeugt fünf Ergebnisdateien
aus Quellen und vergleicht sämtliche Bytes sowie die Replay-Quittung.
`.github/workflows/cst-dust-normpath.yml` führt diese Kontrollen bei passenden
Pull Requests und Änderungen auf Main aus. Ein Software-PASS hebt keine
physikalische HOLD-Entscheidung auf.

Der Plan wurde lokal vor Implementierung und Auswertung gehasht. Die
Mechanismen waren vorher durchdacht; dies ist keine externe Präregistrierung
oder blinde Vorhersage. Allgemeine Beweise sind ausgeschrieben, nicht mit
einem formalen Beweisassistenten zertifiziert.

## Unveränderte Veröffentlichung

PDF, ZIP und alle 28 Originalmitglieder bleiben bytegleich. Nur diese
Übersicht und `publication_check.py` ergänzen den entpackten Komponentenordner.

| Artefakt | SHA-256 |
|---|---|
| ZIP | `64f615f4db62231db334817652dd7d5da7b291e7a1cbc9e49540bc8a26f51c60` |
| PDF | `541ca9e30ebdd9ee5abd39d6d5a53375d65fd84d1eed389a768a623caed7d428` |
| Plan | `91d43a2e7a0a5e457546ac42d7f6b284baca9c88b05716babe40d209b1450818` |

Basis: Main `573084d007ae96d82eb6c241df6ae1d572523418`, nach PR 249.
Nächster wissenschaftlicher Schritt: physikalische Zustände, Ereignisse und
Endkontraktion gemeinsam mit begründeten Auswahlkriterien festlegen.
