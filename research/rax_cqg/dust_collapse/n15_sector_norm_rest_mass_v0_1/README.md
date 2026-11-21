# CST-DUST · Relative Sektornorm und Ruhemasse

**21. November 2026 · N15 · Stand nach dem Kovarianztest**

**Die heutige Randpaarung bestimmt kein physikalisches Verhältnis c₊/c₋. Die physischen P3-Daten liefern keinen Umrechnungsfaktor von der Stromladung zur Ruhemasse.** Eine einmalige Eichung der markierten endlichen Referenz besteht die Dosisänderung bei festem Uhrprofil. Zwei Profilwechsel verfehlen mit demselben Faktor die Massentoleranz. Auf einer zweiten Ordnung liefern zwei verschiedene markierte Massen sogar dieselbe exakt positive Einzelladung.

Die Eingaben stammen vom zusammengeführten Stand von PR #338. Der [Prüfvertrag](pruefvertrag.json) wurde vor der neuen Rechnung lokal mit SHA-256 festgehalten. Die früheren Ergebnisse aus PR #334 und #338 waren bei der Versuchsplanung bekannt. [GitHub-Stand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/397f867ba5318127cd9f7fbefbb0b388c8cdae05)

## 1. Sektornorm

Aus den publizierten komplexen 6×6-Matrizen wurden beide Vorzeichenzweige kohärent gebildet. Dazu werden auch die Nebendiagonaleinträge innerhalb jedes Vorzeichens mit aufsummiert. Über alle zwölf Kombinationen aus Masse, Dichtezentrum und Gewichtsverhältnis liegt der normierte Betrag des Überlapps im H₃-Raum zwischen 0,01129561 und 0,07695715. Die zwölf Werte stimmen mit der archivierten Vergleichstabelle überein.

Die Algebra der Umskalierung ist exakt. Für Nichtnullvektoren und positive a und b gilt

    |⟨aψ₊, bψ₋⟩| / (‖aψ₊‖ ‖bψ₋‖) = |⟨ψ₊,ψ₋⟩| / (‖ψ₊‖ ‖ψ₋‖).

Auf der geöffneten Zukunftsbox des Einzeltyps 375841 sind die zwei Paketbilder derselbe Vektor v mit γ = ‖v‖² > 0. In der reskalierten Paketbasis hat die Gram-Matrix die Form γ [[a²,ab],[ab,b²]]. Ihre Nullrichtung ist (1/a,−1/b). Ihr positiv selektierter Anteil hat das Normquadrat γ. Der scharfe Selektor bleibt damit auf dem Quotienten dieser Paarung für jedes positive a und b undefiniert.

Eine relative Norm setzt physikalisch begründete Sektoren und interne Paarungen voraus. Selbst dann bedarf es einer sektorübergreifenden Normierungsbedingung. Gäbe es beispielsweise zwei aus der Dynamik bestimmte, physikalisch adjungierte Übergänge B von minus nach plus und A von plus nach minus, müsste für geeignete Zustände u und v gelten

    c₊ ⟨u, Bv⟩₊ = c₋ ⟨Au, v⟩₋.

Für eine Bestimmung müssten die Vergleichswerte ungleich null sein und für alle zugelassenen Vergleichspaare dasselbe positive Verhältnis ergeben. Die gegenwärtige Rechnung setzt keinen solchen Übergang voraus. [Ensembleprüfung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/397f867ba5318127cd9f7fbefbb0b388c8cdae05/research/rax_cqg/dust_collapse/n15_charge_interval_record_v0_1) · [Randtest](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/397f867ba5318127cd9f7fbefbb0b388c8cdae05/research/rax_cqg/dust_collapse/n15_future_boundary_v0_1)

## 2. Eine Eichung, vier Transfers

Auf Typ 2324 verläuft der markierte Fluss entlang 3 → 4 → 13 → 7. Seine bekannte Referenzmasse M wird am Anfangsschnitt durch Zählen der Markierung bestimmt. Die vorgegebene Verweildauerregel ergibt auf den zwei besetzten inneren Ereignissen die Dichten MD/4 und 3MD/4, auch beim Profilwechsel. Die Ladung wird separat durch eine symmetrische Differenz der Wirkung bei verschobenen Anfangsuhren und festgehaltenen Dichten bestimmt. Als Auslese dient das diagonale Mittel über die zwei vollständigen Randuhrfenster aus PR #334. Sowohl der ursprüngliche Rand mit leerem Inneren als auch eine vollständig staubfreie Kontrollbelegung liefern p = 0.

Die einzige Eichung verwendet M = 1/4 und k = 1/3. Sie ergibt ⟨p⟩ ≈ 0,07097231331 und g = M/⟨p⟩ ≈ 3,522500372 in markierten Referenzeinheiten. Nullpunkt und g bleiben für jede folgende Zeile fest.

| Markierte Prüfmasse | Inneres Uhrprofil k | Gemittelte Ladung | Masse aus g⟨p⟩ | Relativer Fehler | ±2 % |
|---:|---:|---:|---:|---:|---|
| 1/2 | 1/3 | 0,14194463 | 0,50000000 | exakt 0 | PASS |
| 1/2 | 3/8 | 0,15515651 | 0,54653886 | +9,3078 % | FAIL |
| 1 | 1/3 | 0,28388925 | 1,00000000 | exakt 0 | PASS |
| 1 | 11/24 | 0,36316055 | 1,27923317 | +27,9233 % | FAIL |

Die Halbdosis und das Profil 3/8 wurden als neue Prüffälle festgelegt. Die Einheitsdosis und die zwei äusseren Profilwerte waren publiziert. Keine der vier Zeilen floss in die Eichung ein. Der exakte Transfer bei festem Profil folgt aus der Linearität der bedingten Ladung in der Markermasse. Der Profilwechsel prüft, wie weit die so gewonnene Kalibrierung übertragbar ist.

Der Prüfer rekonstruiert die Relation, die Intervallkoeffizienten und die Quellenvariation. In θ = δ/Δ ist p quadratisch. Die drei aus den Wirkungsdifferenzen gewonnenen Koeffizienten stimmen rational exakt mit M(4−θ)[1−23θ+3k(4−θ)]/76 überein. Die beiden gleich gewichteten Fenster liefern E[δ] = 0 und E[δ²] = 13/3072. Für Δ² = √(3/722) wird eine rationale Einschliessung der Breite 10⁻⁴⁰ verwendet. Die Statuswerte beruhen auf den vollständigen Fehlerintervallen der endlichen Modellrechnung. [Schnittmasse und Stromladung, PR #334](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/334)

## 3. Zwei verschiedene Markermassen mit identischer positiver Ladung

Der zweite Versuch nutzt Typ 375841 in der synchronisierten Präparation. Geometrie, Uhren, äusserer Rand, Dichtezentrum und Ausleseregel bleiben fest. Bei e = −1/4 sind f das normierte Verweildichteprofil und d die veröffentlichte Dichteverschiebung. Auf der Strecke zwischen den beiden Paketzentren gilt

    x(λ) = f + (2λ−1)d,      w = M Δ(4−e)x(λ),      0 ≤ λ ≤ 1.

Die normalisierten Dichten summieren sich zu 1. Für beide Marken liegen die verwendeten Dichten strikt im ±1-%-Band der Präparation und erfüllen 0 < w < 1. Die Summe der sieben inneren Dichten geteilt durch die Verweildauer ergibt an diesen Punkten die vorgegebene Markermasse. Verwendet wird das ganze zugelassene Dichteband. Die interpolierten Punkte liegen im Allgemeinen ausserhalb der beiden kleinen Vorzeichen-Testzellen.

Die feine Ladung ist bei festen Uhren affin in λ. Das folgt aus der Linearität der Wirkung in den Dichten. Der Prüfer hat sie an allen vier angegebenen Punkten durch symmetrische Wirkungsdifferenz nachgerechnet. Die Endwerte von p/M sind 1429581/190000000 und −1004581/190000000.

| Markierte Masse | λ | Exakte Modellladung p |
|---:|---:|---:|
| 1/4 | 84093/143186 | 0 |
| 1 | 84093/143186 | 0 |
| 1/4 | 84093/286372 | 1429581/1520000000 |
| 1 | 588651/1145488 | 1429581/1520000000 |

Schon bei einem strikt positiven p würde eine Abbildung M = F(p) denselben Wert für zwei verschiedene Markermassen liefern müssen. Eine punktweise Rekonstruktion allein aus der Ladung scheitert damit auf dieser Familie. Über die Eignung eines Schätzers aus der gesamten Ladungsverteilung oder zusätzlichen Observablen entscheidet dieser Test nicht. [Synchronisierte Präparation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/397f867ba5318127cd9f7fbefbb0b388c8cdae05/research/rax_cqg/dust_collapse/synchronized_distributed_dust_v0_1)

## 4. Physikalische Ruhemasse und ausstehender Transfertest

Alle 60 physischen P3-Datensätze stehen auf NOT_RUN, darunter alle zwölf Einträge am Anfangsschnitt. Die Massen in ihren Kontextfeldern sind Sollwerte. Es fehlen ein unabhängig bekannter positiver physikalischer Massenstandard mit gemessener Ladung derselben Präparation sowie ein mit diesem Messprotokoll überprüfter physikalischer Nullpunkt.

Für den physikalischen Transfer sieht der Vertrag folgende Auswertung vor.

1. Physikalische Paarung oder Messinstrument, Ladungsstatistik, Präparationsvorschrift und Unsicherheitsmodell vor der Auswertung festlegen. Den Nullpunkt mit der zugehörigen Vakuumkontrolle prüfen.
2. Beim unabhängig begründeten linearen Ansatz M = g p ausschliesslich das positive Referenzpaar bei M = 1/4 für g verwenden. Das Ladungsintervall muss eine positive Verstärkung zulassen und von null getrennt sein.
3. Mit festem g die Ladungen bei den unabhängigen Prüfmassen 1 und 4 auswerten. Zuerst dieselbe Präparationsvorschrift mit geänderter Masse verwenden, dann zulässige Profiländerungen prüfen. Das gemeinsame Unsicherheitsbudget muss Standard, g, neue Ablesung und ihre Korrelationen erfassen.
4. Das vollständige simultane relative Fehlerintervall mit dem geerbten ±2-%-Band vergleichen. Ein enthaltenes Intervall ergibt PASS, ein disjunktes FAIL, eine teilweise Überdeckung oder ein unvollständiges Budget HOLD.

Der physikalische Transfer steht auf NOT_RUN. [P3-Vertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/397f867ba5318127cd9f7fbefbb0b388c8cdae05/research/rax_cqg/dust_collapse/correspondence_v0_1/plan.json)

## Offline wiederholen

Python 3.9 oder neuer mit aktivierten Assertions genügt. Alle Eingaben liegen bei. Der Prüfer kontrolliert ihre Git-Blob-Identitäten und den Prüfvertrag.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py > wiederholung.json
cmp ergebnis.json wiederholung.json
```

Die rationalen Intervalle, alle zwölf Überlappwerte und die Ladungszeugen stehen in [ergebnis.json](ergebnis.json). [Herkunft der Eingaben](quellen.json)
