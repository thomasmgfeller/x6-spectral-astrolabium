# Übernahme- und Behauptungsregister

Die maschinenlesbare Herkunft und SHA-256-Werte stehen in
[`adoption_manifest.json`](../adoption_manifest.json). Dateien werden nur in dem
hier genannten Umfang als Referenz genutzt. Gleichheit eines Hashes belegt
Identität, keine unabhängige fachliche Begutachtung.

| Artefakt | Herkunft / Übernahme | Vertretbare Verwendung / Grenze |
|---|---|---|
| Sagnac v0.7 Schnittstellen- und Transportvertrag | Geerbte Repository-Dateien unter `experiments/photonic-two-qubit/reference/sagnac_v0_7`; unverändert, MIT | uint64-Zeitstempel, vollständige 16 Masken/24 Zähler, Watermarks, Integritätsflags, SGNCv007; keine analoge Präzisionszusage |
| Sagnac Batchreferenz und Hostdecoder/-validator | Unverändert geerbt, direkt gegen neuen Zähler-/Frameexport getestet | Alternative digitale Implementierung; nicht eine Replikation durch eine unabhängige Forschungsgruppe |
| Sagnac VHDL und Testbench | Unverändert geerbt; optional in temporärer Kopie mit GHDL ausgeführt | Funktionale RTL-Simulation; keine neue Timing-Closure, Hardwaremessung oder verteilte FPGA-Implementierung |
| `SCIENTIFIC_STATUS.md` und `LAB_PROTOCOL.md` | Geerbtes Photonikprojekt | Begrenzung von CHSH-/Postselektionsaussagen, Rohdaten- und Kalibrierdisziplin; keine pauschale Freigabe aller früheren Zahlen |
| NQK `tests/reference/quantum_core.py` | Bytegleiche Kopie aus NQK 0.4.0, Site-Source-Commit `9fdf357d5bb8d1244f13d208f8f9c6f2dfe345d7`; `vendor/nqk` enthält LICENSE und NOTICE | Gegenprüfung von Dichtematrixgültigkeit, Negativität und Dephasierungs-Krauskanälen. Andere enthaltene NQK-Funktionen sind nicht Gegenstand dieser Validierung |
| Astrolabium-Repositorystruktur und Apache-Lizenz | Branch-Basis `132f1df9cc8b97c29d8a8cebb86a17061a2714ce` | Reproduzierbare neue Forschungsfläche; daraus folgt keine Übertragung sonstiger Astrolabium-Ergebnisse auf Quantenoptik |

## Nicht übernommene Behauptungen

| Frühere Behauptung | Entscheidung und Begründung |
|---|---|
| Geometrische/Berry-Phase macht den Kanal allgemein verlust- und driftimmun | Verworfen. Geometrie ist ohne spezifischen Hamiltonian, Rauschmodell und Schutzmechanismus kein allgemeiner Robustheitsbeweis; siehe R6 |
| `acos(sqrt(p_A+))` rekonstruiert zwei-Qubit-Geometrie oder erkennt jeden Angriff | Verworfen. Ein Marginalwert bestimmt keine Dichtematrix, Fisher-Information oder Holonomie. Separables Gegenbeispiel als Regressionstest |
| Summe von vier solchen Abständen muss pi/4 sein | Keine hergeleitete Invariante. Die ursprünglich angegebenen Zahlen liefern pi/2 |
| Faserrotation zerstört stets instantane Verschränkung | Korrigiert. Lokale unitäre Rotation erhält Verschränkung; zeitliche Mittelung und weitere Kanäle sind gesondert zu prüfen |
| FPGA-Ereigniszeitstempel messen die optische Pump- oder Berry-Phase | Verworfen. Die vorhandene digitale Schnittstelle spezifiziert Ereigniszeiten, keine solche Phasenmessung |
| Korrelationszählung ergibt einen abhörsicheren Kanal / BBM92 ist bereits gelöst | Verworfen. Protokoll, Authentisierung, Nachverarbeitung, Gerätemodell und endliche Sicherheitsanalyse fehlen |
| Zwei Paarquellen sind für jeden elementaren Link nötig | Korrigiert. Eine Paarquelle und zwei Messstationen reichen für den hier modellierten elementaren Link |
| Alle drei fehlenden Ingenieursbausteine schließen die Brücke lückenlos | Nicht haltbar. Weitere Quell-, Detektor-, Kalibrier-, Datenintegritäts- und Protokollanforderungen bleiben |

Die Ablehnung einer Schutzbehauptung verwirft nicht die sinnvolle Forschung an
geometrischen Diagnostikgrößen. Eine solche Erweiterung muss messbar definiert
und gegen einfachere Diagnostik geprüft werden.
