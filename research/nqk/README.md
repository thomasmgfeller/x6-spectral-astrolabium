# NQK — eigenständiger Forschungszweig

**Roadmap 0.1 · 12. Oktober 2026 · Forschungsplanung, keine Produktfreigabe**

NQK untersucht, welche Information aus endlichen Korrelationsnetzen rekonstruierbar
ist und welche zusätzlichen Strukturen für einen lorentzschen Anschluss nötig sind.
Ausgangspunkt ist die abgeschlossene Forschungsfassung 2.0 zu metrischer Konsistenz
und Quantenkorrelationen in endlichen Netzwerken.

NQK wird vorerst als eigenständiges Forschungsprogramm geführt. Dieser Git-Zweig
`research/nqk` und der Ordner `research/nqk/` beherbergen das Forschungsdossier.
Das gemeinsame Repository dient als Ablage; NQK ist derzeit kein Modul der
Astrolabium-Anwendung. Die Planung startet keine Agenten und steuert keine Hardware.

## Einstieg

| Dokument | Zweck |
| --- | --- |
| [ROADMAP.md](ROADMAP.md) | Meilensteine, Abhängigkeiten, Nachweise und Abbruchkriterien |
| [FEATURES_ASTROLABIUM.md](FEATURES_ASTROLABIUM.md) | Zehn mögliche spätere Funktionen und ihre jeweiligen Freigabebedingungen |
| [INTEGRATION_CONTRACT.md](INTEGRATION_CONTRACT.md) | Vorgeschlagene spätere Datenschnittstelle und Trennung der Evidenzklassen |
| [STATUS.md](STATUS.md) | Was bereits untersucht wurde und was noch offen ist |
| [REFERENCES.md](REFERENCES.md) | Fachliteratur und konkret geprüfter Astrolabium-Stand |
| [Forschungsfassung 2.0](baseline/NQK_Forschungsfassung_2_0.pdf) | Unveränderte 17-seitige wissenschaftliche Ausgangsfassung |
| [Maschinenlesbarer Ausgangsstand](baseline/baseline_summary.json) | Laufzahlen, Grenzen und Identität der bestehenden Prüfpakete |

## Drei Forschungsfragen

1. Welche geometrischen Eigenschaften und welche Information bewahrt eine
   Abbildung von Zuständen oder Daten auf Paargewichte?
2. Welche zusätzlichen Observablen unterscheiden Systeme, die dieselben
   Paarmatrizen oder dieselben Spektren besitzen?
3. Wie lassen sich explizite Kausalordnung, Zeitseparation und Quantenmodell
   kontrolliert zusammen untersuchen?

Die lorentzsche Richtung hat nach Absicherung der gemeinsamen Grundlagen
Forschungspriorität. Ein negatives Ergebnis oder ein reproduzierbares
Gegenbeispiel ist ein zulässiges Resultat.

## Verbindlicher Evidenzstatus

Die historischen Tests 001–013 bleiben unbestätigt. N001–N013 sind eine neue
synthetische Untersuchung. Die Quantenergebnisse stammen aus klassischen
Simulationen kleiner Systeme. Eine physikalische Theorie, Raumzeitentstehung,
ein vierdimensionaler Grenzwert oder ein Quantenvorteil sind nicht nachgewiesen.
Die Anzahl bestandener interner Prüfungen ersetzt keine unabhängige Begutachtung.

Dieses Dossier veröffentlicht die Roadmap und den Forschungsbericht. Die vier
vollständigen bisherigen Code-/Datenarchive sind hier noch nicht übernommen;
ihre Prüfsummen stehen im Ausgangsstand. Ihre kontrollierte Übernahme und
Ausführung aus einem frischen Checkout gehören zu M1. Der PDF-Bericht allein
ist daher noch kein ausführbares öffentliches Reproduktionspaket.

Die NQK-Dokumente wurden mit KI-Unterstützung erstellt. Externe Replikation,
fachliches Review und die Bewertung möglicher Neuheit bleiben offen.
Der bestehende [Lizenzstatus des Repositorys](../../README.md#license-status)
gilt weiter; dieses Dossier erteilt keine zusätzliche Nutzungslizenz.

## Nächster Arbeitsabschnitt

M1: vorhandene Referenzpakete zu einem unabhängig ausführbaren NQK-Kern
zusammenführen, Herkunft und erwartete Befunde festlegen und fremdimplementierte
Kontrollen ergänzen. Anschliessend M2 zum lorentzschen Anschluss bearbeiten.
Eine Übernahme einzelner Funktionen in Astrolabium wird erst nach ihren
separaten Freigaben beschlossen.
