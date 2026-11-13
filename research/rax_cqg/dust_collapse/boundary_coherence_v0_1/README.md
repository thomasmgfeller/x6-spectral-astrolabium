# CST-DUST: kohärente Endrandmessung v0.1

Ausführung der fünf vereinbarten Schritte, 13. November 2026. Ein begrenzter
Nachfolger des veröffentlichten Sechshistorienpiloten. Kein neuer großer
Integrationslauf, keine Änderung der früheren Ergebnisse.

## Ergebnis

Eine klassenblinde kohärente Auslese kann innerhalb des ausdrücklich deklarierten
endlichen Hilfsmodells die relative Gravitationsphase in tatsächliche terminale
Skalarmodenwahrscheinlichkeiten überführen. Dafür wurden zwei normierte,
orthogonale, unter Endknotenvertauschung invariante Pakete konstruiert:

\[
f_0=R_f,\qquad f_2=((q_4+q_5)^2-1)f_0/\sqrt2.
\]

Ihre neuen Amplituden sind analytische Gaußmomente der ursprünglichen Wirkung:
\(a^{(2)}_{c,s}=\eta_c a^{(0)}_{c,s}\). Die Faktoren unterscheiden sich zwischen
den Klassen. Es wird weder ein Skalarmodus als Radius bezeichnet noch ein
physischer Gravitationsdetektor behauptet.

Bei der expliziten idealen Kohärenzannahme γ=1, ursprünglicher Wirkung κ=1 und
dem vor den neuen Randwerten festgelegten Gain 1/1024 liegt der bedingte
Unterschied P(f2|Erfolg,g+)−P(f2|Erfolg,g0) in
\([2.5194616115,2.5238895751]\times10^{-6}\).
Erfolgswahrscheinlichkeiten sind nur etwa 3.58872e−10 und 9.34809e−10;
Failure ist vollständig berücksichtigt. Diese Größen sind Hilfsmodellwerte,
keine Zählraten eines gebauten Detektors.

Das dephasierte Instrument hat bereits eine kleine Quellenantwort. Deshalb
werden zusätzlich kohärent/dephasiert und die kontrafaktische Entfernung allein
der F4-Phasen verglichen. Erst diese Kontrollen identifizieren den zusätzlichen
Interferenzbeitrag innerhalb des Modells. κ=0 ist kein physischer G-Stellknopf.

## Fünf Schritte und Reichweite

| Schritt | Ausgeführt | Status |
|---|---|---|
| 1 | Gemeinsamer Recordvertrag, komplexer Umweltüberlapp, CP-Instrument und Nichtidentifizierbarkeit aus alter Klassenmessung abgeleitet | Bedingte Existenz; physische Kohärenz offen |
| 2 | Alte Amplitudenintervalle auf ±-Auslese, direkten Kanal und sämtliche Failure-Wahrscheinlichkeiten fortgepflanzt | PASS unter übernommenen Einschließungen |
| 3 | Zwei echte terminale Materiemoden, exakte Gaußmomente, neue Normschranke und Randwahrscheinlichkeiten konstruiert | PASS als endliches Hilfsinstrument |
| 4 | Quellenbedingungen, Strombilanzen und Uhrreflexion erneut exakt geprüft; glatter orientierter Uhrkandidat untersucht | Begrenzte Hindernisse bestätigt; Kandidat nicht übernommen |
| 5 | Voraussetzungen eines physischen Zwei-Quellen-Geometrievergleichs geprüft | HOLD: nicht definiert; keine physische Kollapskurve berechnet |

Die Quellenbedingung C_A≥1 schließt frei variierte positive stationäre
A-Dichten aus, aber nicht allgemein Quantenrandzustände. Einzelne orientierte
Strominsertionen verschwinden unter den vorhandenen reflektionsgeraden
Uhrpaketen. Beide R-Geometrien sind dieselbe Zweierantichain. Keine dieser
Aussagen ist ein allgemeines Verbot einer anderen CST-Konstruktion.

## Reproduktion

Python 3.12.14, mpmath 1.3.0, SymPy 1.14.0 und NumPy 2.3.5 wurden verwendet.
Der PDF-Generator benötigt zusätzlich reportlab; er ist keine Voraussetzung
für die wissenschaftlichen Checks.

```bash
python checks/run_all.py
```

Der Aufruf funktioniert auch über den absoluten Pfad zum Skript. Alle benötigten
Daten liegen in `sources/`; das alte große Prüfpaket ist nicht erforderlich.
`sources/prior_einstein_check.py` ist ausschließlich eine historische Quelle,
kein Einstiegspunkt dieses Pakets. Ihr ursprünglicher Kontext ist im früheren
veröffentlichten Prüfpaket enthalten.

Die unabhängigen rationalen Auditoren verwenden exakt die gespeicherten
Amplitudenrechtecke; sie wiederholen deren Quadratur nicht. Der zweite Audit
kontrolliert die F4-Phasenentfernung zusätzlich mit rationalen Taylorpolynomen
und reellem Lagrangerest. Hilbert rekonstruiert die neuen Gaußmomente unabhängig
aus den Ordnungsrelationen mit rationaler Algebra in Q(i√6).

## Dateien und Provenienz

- `contracts/`: Annahmen, unveränderte Eingaben und vor neuer Auswertung festgelegte R-Pakete/Gain.
- `checks/`: ausführbare Rechnungen und nach außen gerundete Ergebnisse.
- `agents/`: fünf fachliche Ableitungen und gegenseitige Prüfung; die Namen bezeichnen KI-Arbeitsperspektiven.
- `sources/`: unveränderte, gehashte Ausgangsdaten und begrenzte historische Quellen.
- `report/`: zusammengefasster Bericht und Erzeugungscode.
- `MANIFEST.json`: Dateigrößen und SHA-256-Werte, ohne sich selbst und ohne Laufzeit-Caches.

Ursprünglicher Wirkungsstand: 338a3ebb28507790fe916ae577920d0c264acab9.
Veröffentlichter Sammelstand: 9f31ae8034c398efc979e47d7fa5b66b61e13517.
Pilotvertrag: 442cc81227921135ccb046cdc238f8c2d9cae88f2082614490e59cfceba77ba3.
Geerbte Amplituden: 5085b0f3d5bf2d9a70a184853c9d236fc2d41d7d2f7003b9c57ad980bdb34eae.

Die frühere θ=0-Diagnose war bereits bekannt; es wird keine neue blinde
Vorhersage behauptet. Die neue f2-Wahl ist durch den niedrigsten geraden
symmetrischen Hermitemodus motiviert; Paket und Gain wurden vor ihren neuen
Antwortwerten festgelegt. Der frühere held-out Status von g+ wird nicht als
unabhängige neue Validierung dieses späteren Entwurfs ausgegeben.

Abbruchregel: Weitere Historien oder höhere Präzision ersetzen keine physische
Constraintpaarung, Quellen-/Uhrkalibrierung und geometrische Observable. Diese
Ausführung veröffentlicht oder verändert keine GitHub-Inhalte.

Methodischer Literaturanschluss: A. Mozota Frauca und R. D. Sorkin,
*How to Measure the Quantum Measure*, https://arxiv.org/abs/1610.02087.
Die Literatur validiert nicht die physische Realisierbarkeit dieses Instruments.
