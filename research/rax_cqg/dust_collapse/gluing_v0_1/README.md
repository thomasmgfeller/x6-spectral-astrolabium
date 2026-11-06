# CST-DUST-Verklebungsregel v0.1

Eine exakte Zerlegung der BDG-Wirkung, ein ausdrücklich bedingtes markiertes
Zählmaß, vollständige Amplitudenkerne und getrennte physikalische Entscheidungen.

**Physikalisches CST-Staub-Anschlussgesetz: HOLD_NOT_DERIVED. Globaler Bounce:
HOLD_NOT_RUN. Regularität und globale Fortsetzung: separat HOLD.**

Das Paket enthält konkrete mathematische Resultate, keine neue dynamische
Staubball-Simulation. Die 4473 endlichen Testordnungen sind nicht nach vierdimensionaler
Mannigfaltigkeitsnähe ausgewählt. Es werden keine externen Dienste oder bezahlten
Rechenläufe angesprochen.

## Reproduzieren

Im entpackten Paketverzeichnis mit Python 3.10 oder neuer (Referenzlauf 3.12.14):

```bash
python3 -O -B analyze.py
python3 -O -B verify_independent.py
```

Die numerische Prüfung braucht nur die Standardbibliothek. Optimierungsmodus
deaktiviert keine Prüfungen: Sie verwenden explizite Exceptions, keine asserts.
Alle Annahmen und Toleranzen stehen in plan.json, geschützt durch plan.sha256.
Alle Resultate werden in results/ deterministisch neu erzeugt. Der Manifestwert
python hängt absichtlich von der verwendeten Python-Version ab; dadurch ändern
sich bei anderen Versionen auch die davon abhängigen Hashfelder des P5-Datensatzes.
Die exakten mathematischen Resultate müssen identisch bleiben.

Erwartet: 130116 Wirkungs- und Stromprüfungen, 6372 verschmierte Prüfungen,
7998 Assoziativitätsprüfungen, 1549 markierte Bahnen, vier 2+2-Kerne und 32
Variationsidentitäten. 13 Strukturkontrollen und fünf separate synthetische
Gate-Kontrollen. Der unabhängige Algorithmus prüft dieselben 4473 Ordnungen und
130116 Zweiblockkorrekturen. Keine Toleranz ist ungleich null.

## Inhalt

- DERIVATION.md: vollständige Definitionen, Beweise, Gegenbeispiele und Grenzen.
- gluing.py: endliche Ordnungen, Intervallwirkung, Kopplung, Kerne, Symmetrien.
- analyze.py: vollständige Enumeration und unveränderter Model-Contract-Auditor.
- verify_independent.py: zweite Enumeration und unabhängige Intervallarithmetik.
- inputs/: unveränderte Vorarbeiten mit Commit- und Hashnachweis.
- results/: exakte CSV-/JSON-Resultate, Manifest und ein abgegrenzter P5-Datensatz.
- figures/: exaktes kleines Gegenbeispiel als Darstellungsbild.
- CST_DUST_Verklebungsregel_v0_1.pdf: lesbarer Ergebnisbericht.
- SHA256SUMS: Integrität des ausgelieferten Paketstands.

Die synthetischen Gate-Kontrollen sind keine physikalischen Nachweise. Der
übernommene Auditor kontrolliert Kategorien und Vollständigkeit, keine Beweise.

## Bericht neu erstellen

Optional: Matplotlib 3.10.8, ReportLab 4.4.9 und DejaVu-Sans-Schriften
in `/usr/share/fonts/truetype/dejavu` (Referenzumgebung).

```bash
python3 -B build_report.py
```

Der Bericht wird im Paket erzeugt. Die Abbildung ist nur eine Darstellung;
Beweise und exakte Resultate hängen nicht von Bildauflösung oder Plotbibliotheken ab.

Die Reproduktion überschreibt results/ und gegebenenfalls den Bericht.
`sha256sum -c SHA256SUMS` prüft den unveränderten gelieferten Stand; nach eigenen
Änderungen müssen erwartete Abweichungen von einer beschädigten Lieferung getrennt
werden. Lizenz: Apache-2.0 für eigenes Material; externe Arbeiten werden zitiert
und nicht als Volltext mitgeliefert.
