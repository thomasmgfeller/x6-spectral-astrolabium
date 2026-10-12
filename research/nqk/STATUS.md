# Ausgangsstand und offene Nachweise

**Stichtag: 12. Oktober 2026.** Quelle ist die unveränderte
[Forschungsfassung 2.0](baseline/NQK_Forschungsfassung_2_0.pdf), Abschnitte 2–16.
Dieses Roadmap-Dossier führt keine neuen wissenschaftlichen Produktionsläufe aus.

| Gegenstand | Vorhandene Evidenz | Grenze |
| --- | --- | --- |
| Historische Tests 001–013 | Originalartefakte nicht auffindbar | Unbestätigt; keine erfolgreiche historische Reproduktion |
| Mathematische Grundlagen | Log-Metrik-Bedingung, Gegenbeispiele, 20 Metrik- und 6 Einbettungstests | Bedingungen und Einbettung bleiben getrennt |
| Neue Serie N001–N013 | 3’812 synthetische Läufe | Teilweise abhängige Parameterfälle; bei grossen Netzen Tripelstichproben |
| Robustheit | 10’908 zusätzliche Läufe; 13 festgelegte Kriterien erfüllt | Bedingte interne Bestätigung; Schwellen sind modellabhängig |
| Quantenmodell | 454 Zustands-/Kanalfälle für 3–6 Qubits | Klassische Simulation; keine Hardwaremessung |
| Simulierte Messungen | 192 Datensätze unter idealisierten Annahmen | Bisher kein vollständiges SPAM-, Drift- oder Verlustmodell |
| Abschlussprüfung | 171 Konsistenz-/Archivprüfungen; 17 Dokumentseiten geprüft | Dokument- und Integritätsprüfung, keine zusätzliche Physik-Evidenz |
| Unabhängiges Review | Noch offen | Andere Seeds ersetzen keinen anderen Rechenkern oder Fachreview |
| Astrolabium-Integration | Zehn geplante Transferkandidaten | In diesem Auftrag keine NQK-Anwendungsfunktion implementiert |

## Aussagen, die die weitere Arbeit bestimmen

- `d = -ln(E)` garantiert nicht für beliebige Gewichte eine Metrik. Für normierte
  positive Gewichte hängt die Dreiecksrelation von `E_ij >= E_ik E_kj` ab;
  Symmetrie und Punkttrennung sind weitere Voraussetzungen.
- Clusterrekonstruktion kann erfolgreich sein, obwohl Metrikbedingungen verletzt
  werden. Eine hohe aggregierte Erfüllungsquote ersetzt keine vollständige Prüfung.
- Für Qubits mit `E_ij = I(i:j)/2` gilt die notwendige Schranke
  `E_ij + E_ik <= S(i) <= 1` für verschiedene i,j,k und Entropien in Bit.
  28 ausgewählte bisherige synthetische Matrizen verletzen sie. Der Befund
  betrifft diese Interpretation; er verwirft nicht sämtliche Quantenmodelle.
- GHZ und eine separable Mischung können dieselben Paarzustände besitzen.
  Paarmatrizen erfassen deshalb nicht allgemein die globale Verschränkung.
- Unter der festgelegten lokalen GHZ-Dephasierung bleiben Paargewichte konstant,
  während globale Kohärenz abnimmt. Der Kanalparameter ist keine gemessene Zeit.
- Symmetrische Distanzen liefern noch keine Kausalrichtung, Zeitseparation oder Dynamik.

## Publikationsumfang

Enthalten sind Forschungsbericht, Roadmap, Featurekatalog, vorgeschlagener
Schnittstellenvertrag, Quellen und ein Ausgangsregister. Die vollständigen
Referenzarchive werden über Dateinamen und SHA-256 identifiziert; sie sind in
dieser ersten GitHub-Veröffentlichung nicht enthalten. Die Übernahme in einen
aus einem Checkout ausführbaren Forschungsstand ist ausdrücklich Teil von M1.

Die Ergebnisse werden anhand des bestehenden Berichts eingeordnet. Diese
Veröffentlichung behauptet weder eine zusätzliche unabhängige Replikation noch
eine neue Fachbegutachtung oder eine qualifizierte NQK-Softwarefreigabe.
