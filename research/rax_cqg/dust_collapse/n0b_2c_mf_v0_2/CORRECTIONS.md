# Korrekturregister zur v0.1-Entwurfsfamilie

Diese Tabelle ist eine redaktionelle Zusammenfassung, keine wörtliche
Transkription verlorener Formeln. Auch die später gelieferten Ergänzungen
werden berücksichtigt: beide Oszillatorrichtungen, der p_φ-Term und der
Propagatorvergleich sind im Entwurf vorhanden und werden ausdrücklich übernommen.

| ID | Ausgangsaussage / Problem | Korrigierte Behandlung | Nachweis / Ort |
|---|---|---|---|
| C01 | Vollständige physikalische CST-Theorie | Bedingtes reduziertes Modell; CST-Herleitung HOLD | MODEL, BRIDGE_CONTRACT |
| C02 | Nullatom als gewöhnlicher identischer Kanal | Herkunft und Trägerabbildung offen; Atom nicht wegquotientieren | Vorgänger, SOURCE S-P1 |
| C03 | Lineares Uhrconstraint aus Spektralstütze | Stütze, Gewicht und Sektorauswahl gemeinsam prüfen | CLOCK-SUPPORT |
| C04 | Dirichlet allein beweist Selbstadjungigkeit | Geschlossene Form und global kontrollierte Koeffizienten | MODEL §3, S1 |
| C05 | dP_Q/dχ=−⟨∂_Q V⟩ | Wand- und weitere Randimpulse ergänzen | WALL-* |
| C06 | Norm-/Energieerhaltung beweist Genauigkeit | Lokale Residuen, Fernränder und Konvergenz separat | VALIDATION |
| C07 | Lokale Energie ist schon Raumzeitstrom | Konfigurationsraum-Bilanz; physikalischer Tensor offen | BALANCES |
| C08 | G=0 impliziert Superselektion | Dynamische Entkopplung; zulässige Observable-Algebra zusätzlich nötig | MODEL §5, S4 |
| C09 | Nichtnull C_0+ notwendige Quantensignatur | Bestimmte kombinierte Parität erlaubt C_0+=0 bei Transfer/Entanglement | QS-*, SYM-* |
| C10 | Gleiche Frequenzen verhindern Records | Kein allgemeiner Schluss | QS-RECORD |
| C11 | Dichteüberlapp ist Uhlmann-Fidelität | Klassischer quadrierter Bhattacharyya-Überlapp nur obere Schranke | VALIDATION, S8 |
| C12 | Leerer Kanal besitzt konditionalen Record | Bei zu kleiner Belegung UNDEFINED | DATA_CONTRACT |
| C13 | Reine Präzession exakt für reduzierten Blochvektor | Exakt gemeinsamer Erwartungswert; Faktorisierung bedingt | MODEL §6 |
| C14 | Kleiner Unitaritätsdefekt bei kleinem Schritt genügt | Fehler pro Zeit und Generatorgrenzwert kontrollieren | UNITARITY-RATE |
| C15 | Drei Schrittweiten bestimmen den Logzweig | Spektralfenster oder weitere kontrollierte Fortsetzung | BRANCH-ALIAS |
| C16 | K_0+=0 an einem Schritt schließt Mischung aus | Revivals prüfen; Generator/ganze Familie nötig | KERNEL-REVIVAL |
| C17 | Polarer Generator ist automatisch physikalisch | Diagnose des projizierten unitären Anteils | BRIDGE_CONTRACT |
| C18 | Retardierte Matrix direkt als reelle quadratische Wirkung | Variation liefert symmetrischen Anteil | ACTION-SYMMETRIZATION |
| C19 | Schur-Komplement ist gesamte Quantenamplitude | Determinante, Phase, Maß und Nullmoden ergänzen | SCHUR-STATIONARY, GAUSSIAN-FACTOR |
| C20 | Randhessian-Eigenwert/m ist automatisch Frequenz² | Relationale kinetische Form und Potential identifizieren | MODE-FREQUENCY-TRAP |
| C21 | ε_mode ist sichere Fehlergrenze | Normalisierte erste Ordnung; direkte Unterraumfehler/Schranken nötig | MODE-FALSE-PASS |
| C22 | Quadratische Materiewirkung erlaubt sicher g_1φ | Kanalneutrale ungebrochene Feldumkehr kann linearen Term ausschließen | SYM-MATTER-ODD |
| C23 | Nur Δn=±1 und eine Bandrichtung identifizieren φ | Beide Richtungen, Phasen, weitere Bänder und Q-Lokalität | OP-UP-DOWN-*, OP-HERMITIAN-TRAP |
| C24 | Kleiner Kopplungsrest kontrolliert Mischkraft | Ableitungen oder Kraftimpuls separat prüfen | FORCE-REST |
| C25 | m_φ(Q) ändert keine Kraftformel | Materiekinetik liefert zusätzlichen Beitrag | MASS-BACKREACTION |
| C26 | H-Kompression allein beweist dynamische Konvergenz | Vorhandenen Propagatorvergleich mit Isometrie/Zeitscope präzisieren | REFINE-LEAKAGE |
| C27 | N-Gitter sind homothetisch/Faktor 2 | Intervallzahlen und getrennte Regulatoren verwenden | GRID-NONHOMOTHETIC |
| C28 | Historiennamen genügen für Bounce-Wahrscheinlichkeit | Ereignisse, Gegenalternative, Konditionierung und Dekohärenz explizit | VALIDATION |
| C29 | Tools und Smoke-Test bereits verifiziert | Ohne entsprechende Quellen/Daten nicht als Implementierung/Ergebnis übernehmen | status.json |

Die kleinen Kontrollen widerlegen jeweils eine zu starke Schlussfolgerung
oder bestätigen eine abgegrenzte Identität. Sie entscheiden keine globale
CST-Physik. Ihre Voraussetzungen und erwarteten Gegenresultate wurden während
des Reviews entwickelt; es wird kein unabhängiger Blindtest beansprucht.
