# CST-DUST-Verklebungsregel v0.1 · Veröffentlichung

Die vollständige BDG-Wirkung lässt sich für jede endliche Ordnung exakt in zwei
induzierte Teilordnungen und Kopplungsbeiträge zerlegen. Dabei müssen sowohl
grenzüberschreitende Paare als auch Änderungen interner Intervallklassen erfasst
werden. Unter einem ausdrücklich angenommenen markierungstreuen Zählmaß ist auch
die Amplitudenkomposition geschlossen.

**Das physikalische CST-Staub-Anschlussgesetz bleibt HOLD_NOT_DERIVED. Ein globaler
Bounce bleibt HOLD_NOT_RUN. Regularität und globale Fortsetzung bleiben separat
HOLD.** Die Aussage bezieht sich auf einen neuen, abgegrenzten P5-Datensatz; sie
verändert frühere klassische Referenzentscheidungen nicht.

[Bericht (PDF, zehn Seiten)](../reports/CST_DUST_Verklebungsregel_v0_1.pdf) ·
[Originales Prüfpaket (ZIP)](../packages/CST_DUST_Verklebungsregel_v0_1_Pruefpaket.zip) ·
[Vollständige Beweise](DERIVATION.md) · [Exakte Ergebnisse](results/verification.json)

## Konkrete Ergebnisse

- Allgemeiner algebraischer Beweis einschließlich der Korrektur für interne
  Intervalle, deren Zwischenpunkte durch das Herausschneiden verändert werden.
- 130 116 vollständige Wirkungs- und ebenso viele Stromschnittprüfungen,
  6 372 rationale verschmierte Kontrollen und 7 998 Dreiblock-Assoziativitätsfälle.
- Zehn markierte Maßsektoren, 1 549 Bahn-Stabilisator-Prüfungen, vier vollständig
  bestimmte 2+2-Verklebungskerne und 32 endliche Variationsidentitäten.
- Explizites Gegenbeispiel: Zwei Dreierordnungen mit gleichem N, gleichem F4 und
  gleich vielen zulässigen Erweiterungen haben unterschiedliche Zukunftsamplituden.
  Der Zustand (N,F4) ist für diese exakte Fortsetzung nicht geschlossen.
- 13 Strukturkontrollen und fünf separate synthetische Gate-Negativkontrollen.
- Zweiter Generator über transitive Abschlüsse und Labelpermutationen sowie
  unabhängige mengenbasierte Intervallarithmetik: 4 473 Ordnungen und 130 116
  Kopplungskorrekturen stimmen vollständig überein.

Die Biaktionsidee stammt aus bestehender CST-Literatur, siehe die Primärquellen
im Bericht. Es wird kein neues universelles GHY- oder Israel-Gesetz beansprucht.
Die kleinen Ordnungen sind nicht nach vierdimensionaler Mannigfaltigkeitsnähe
ausgewählt. Zählgewichte und komplexe Phasensummen sind kein abgeleitetes
physikalisches Staubmaß und keine positiven Bounce-Wahrscheinlichkeiten.

## Reproduzieren

Vom Repository-Stamm aus, mit Python 3.10 oder neuer:

```bash
python3 -O -B research/rax_cqg/dust_collapse/gluing_v0_1/publication_check.py
python3 -O -B research/rax_cqg/dust_collapse/gluing_v0_1/publication_check.py --replay
```

Die Prüfung benötigt ausschließlich die Standardbibliothek. Sie kontrolliert
die Originalbytes von ZIP, PDF und allen 35 Archivmitgliedern, die vollständigen
SHA-256-Listen, unveränderte Vorgängereingaben, den vorab fixierten Plan, sämtliche
acht P5-Entscheidungen und den Quellenstand des ausgeführten Codes. Der Replay
entpackt isoliert, entfernt alle archivierten Ergebnisse und erzeugt die 14
Ergebnisdateien neu. Nur die Python-Versionsangabe im Manifest und ihr bereits
validierter abhängiger Datensatzhash dürfen sich zwischen Laufzeiten ändern.
Alle wissenschaftlichen Ergebnisse müssen unverändert bleiben.

`.github/workflows/cst-dust-gluing.yml` führt diese Prüfung auf Pull Requests
und nach Änderungen auf Main aus. Das Prüfen und Zusammenführen qualifiziert
die Softwareveröffentlichung; es stuft kein physikalisches Gate hoch.

Das ursprüngliche Prüfpaket und die darin enthaltenen Dateien bleiben bytegleich.
`PUBLICATION.md` und `publication_check.py` ergänzen nur die Repository-Einbindung.
Für den optionalen Berichtsbau gelten die Abhängigkeiten in der originalen README.

| Artefakt | SHA-256 |
|---|---|
| Original-ZIP | `83112d1528246189892e741e73cfc19ecc58b8cc7561421a9901b4d6ea836054` |
| Bericht | `59158543b05c4d533416b0190bb5dfefcaaf2f2204363f12a471684b1c0d5e76` |
| Vorab fixierter Plan | `67f4c8fad70b29f6ac745c6a05a45ff91510397d7ed0383d8d27c4cde6c81cb4` |

Projektbasis: Main-Commit `bc8c154be60c483c8a5a8f085c1b3b0668d8afa1` nach PR 243.

## Nächster physikalischer Engpass

Benötigt wird eine gemeinsame diskrete Staub-/Geometriedynamik mit begründetem
Maß und Zustand. An einer physikalisch abgeglichenen Familie müssen anschließend
effektive Wirkung und erste Randvariation im regulären klassischen Bereich
kontrolliert werden. Ein Wirkungsgrenzwert im Mittel allein genügt nicht.
Hochkrümmung, Dichte-/Krümmungsregularität, globale Fortsetzung und Bounce behalten
danach eigene Prüfungen. Keine neuen dynamischen CST-Ensembles wurden ausgeführt.
