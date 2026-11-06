# Physikalische Historiengewichtung v0.1

**5. November 2026 · Bedingte Referenzherleitung; vollständiges CST-Maß offen.**

Die bisherige Gleichgewichtung der 27 Entwicklungs- und 17 Prüfpfade wird als Modellannahme eingeordnet. Für die ausdrücklich reduzierte flache homogene Staubzelle in Staubzeit ergibt die direkte kanonische Quantisierung in `q = sqrt(V)` das Integrationsmaß `dq = dV/(2 sqrt(V))`. Diese Referenz liefert noch keine eindeutige Gewichtung der vollständigen vierdimensionalen Kausalset-Summe.

- [Bericht (PDF, neun Seiten)](../reports/CST_Staubball_Historiengewichtung_v0_1.pdf)
- [Unverändertes Prüfpaket (ZIP)](../packages/CST_Staubball_Historiengewichtung_v0_1_Pruefpaket.zip)
- [Lesbarer Prüfer](verify.py), [Ergebnisse](results/verification.json), [Vertrag](contract.json) und [Quellenbindung](provenance.json)
- [Ursprüngliche Anleitung](README.md) und [bearbeitbare Herleitung](report.tex)

## Was begründet und geprüft ist

Die Ausarbeitung trennt Wirkungsphase, Integrationsmaß, Zustandskoeffizienten und klassische Wahrscheinlichkeiten. Der Faktor `1/|Aut(C)|` folgt aus einer gleich gewichteten beliebig beschrifteten Ausgangssumme nach Division durch die erlaubte Permutationsgruppe. Diese Ausgangsmaßwahl bleibt eine Annahme. Natürliche Beschriftungen enthalten die zusätzliche Vielfachheit der linearen Erweiterungen; physikalische Randmarken verkleinern die zulässige Gruppe. Kovarianz allein bestimmt daher kein eindeutiges Maß.

Der Prüfer zählt alle 87 unbeschrifteten Ordnungsklassen mit einem bis fünf Elementen und kontrolliert die Orbitgrößen sowie die Korrektur natürlicher Beschriftungen exakt. Ein endlicher Sinusraum mit 16 beziehungsweise 32 Moden besteht die Kontrollen für Normerhaltung und Zusammensetzung. Die unabhängige Koordinatenquadratur bestätigt das transformierte Maß. Das absichtlich falsche Volumenmaß verletzt die Zusammensetzung. Vier rationale Zeitpunkte prüfen den klassischen kontrahierenden Staubzweig.

## Grenzen und erhaltene Entscheidungen

Der vollständige CST-Träger, die Sektorgewichte bei variabler Elementzahl, Materie- und Randdaten, Vergröberungsfasern und ein konsistenter CST-Übergangskern bleiben offen. Der Dirichlet-Rand der Referenz ist eine Quantisierungsentscheidung und kein CST-Nachweis. Die endliche Spektralprüfung ist weder eine 4D-Konvergenzprüfung noch eine rigorose Intervallzertifizierung ihrer Gleitkommawerte.

Die archivierten 27/17 Volumenpfade sind keine nachgewiesene Quadratur dieses Pfadintegrals und werden nicht nachträglich mit dem neuen Referenzmaß gewichtet. Der bisherige Abschluss `CLOSED_REJECTED_FOR_DOMINANT_BOUNCE` bleibt erhalten. Die verallgemeinerte notwendige Schranke für ungleiche Amplituden wird nicht als Vorschrift zur Bevorzugung einer Umkehr benutzt. Neuer Bounce-Test: `NOT_RUN`; allgemeiner CST-Bounce und Singularitätsauflösung: `HOLD`.

## Veröffentlichung und Nachrechnung

Das ursprüngliche ZIP und alle zwölf Mitglieder sind bytegleich übernommen. Die PDF-Kopie im Berichtsverzeichnis ist identisch. `PUBLICATION.md` und `publication_check.py` sind ergänzende Veröffentlichungshilfen. Aussagen im ursprünglichen Bericht und README, wonach das Paket selbst keine GitHub-Veröffentlichung erzeugt, beschreiben seinen damaligen Lieferumfang; die Veröffentlichung wird durch den Git-Verlauf dokumentiert. Der Quellenstand `60de9ac01bacc0f86dc68adc8e5784c08338df87` bleibt erhalten.

```sh
python3 research/rax_cqg/dust_collapse/history_weighting_v0_1/publication_check.py --replay
```

Python ab 3.10, nur Standardbibliothek. Die Kontrolle prüft Archivintegrität, alle zwölf Mitglieder, die PDF-Kopie sowie die Bindung beider Tabellen an das bereits veröffentlichte Kopplungsscan-Archiv und den Kandidatensnapshot. Die Nachrechnung läuft in einer temporären Kopie. Sie vergleicht die strukturellen und exakten Resultate mit dem Berichtspaket; numerische Werte werden mit ausgewiesener Toleranz verglichen. Archivierte Resultate bleiben unverändert.

Die vollständige Neuerzeugung der Kausalordnungen, der alte Kopplungsscan und die inversen Volumenmomentrechnungen werden nicht erneut ausgeführt. Keine neue physische Messung, externe Präregistrierung oder Veröffentlichung fremder Artikelvolltexte. Projektbeiträge gemäß [Lizenzumfang](../../../../LICENSE_SCOPE.md).
