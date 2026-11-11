# Validierungsplan und Quantensignaturen

## Ausgeführt versus geplant

Ausgeführt sind ausschließlich die kleinen Kontrollen in checks/run_checks.py.
Die untenstehenden Kampagnen sind NOT_RUN. Die in den Entwürfen genannten
Smoke-Test-Zahlen und Programme sind ohne Quellcode-/Datenprovenienz keine
Ergebnisse dieser Publikation. status.json trennt Software-Evidenz von
Modellannahmen und physikalischen Gates. Der Plan ist intern nach dem Review
formuliert, keine externe Präregistrierung und keine blinde Vorhersage.

## Vier Gitter

Die übermittelten Tripel werden unverändert erhalten:

| Stufe | erste Zahl | zweite Zahl | dritte Zahl |
|---|---:|---:|---:|
| G1 | 81 | 91 | 81 |
| G2 | 121 | 137 | 121 |
| G3 | 161 | 181 | 161 |
| G4 | 241 | 271 | 241 |

Arbeitskonvention dieses neuen Plans: (N_Q,N_φ,N_χ), einschließlich der
Endpunkte. Sie ist eine deklarierte redaktionelle Zuordnung, keine
Rekonstruktion verschwundener Original-Tabellenüberschriften. Vor einem Lauf
muss sie am tatsächlichen Solververtrag bestätigt und eingefroren werden.
Domäne, Randbedingungen, Anfangszustand, Parameter, Diskretisierung,
Linearsolver, Speicher-/Zeitschritte, Observablen und Toleranzen sind in
study_plan.json noch OPEN/null. Daraus darf kein PASS erzeugt werden.

Intervallzahlen sind N−1. Die Tripel bilden nicht überall eine exakt
homothetische Verfeinerung. Ein Vierpunktfit O(h)=O_*+c h^p ist nur zulässig,
wenn ein gemeinsamer effektiver h und kontrollierte Nebenfehler begründet
sind. Sonst Raum-, Materie- und Uhrschritt separat variieren. Auch Fernränder
und Modenabschneidung sind separat zu prüfen. Vier Werte und drei Fitparameter
lassen wenig Spielraum für einen Modelltest; paarweise und ausgelassene Stufen
sowie asymptotische Stabilität müssen dokumentiert werden. Keine Formel mit
festem Faktor 2 auf diese Gitter anwenden.

Zu messen sind Norm- und diskrete Energiedrift, gewichtete L²- und L∞-Reste
der rekonstruierten lokalen Norm-, Energie- und Impulsbilanzen, integrierter
Stratumtransfer, alle äußeren Flüsse und das geometrische Impulsbudget.
Physikalische Diagnosen: ⟨Q⟩, P_Q, N_0, Materieanregung, getrennte Kraftimpulse,
Wandkontakt, inverse Geometriemomente soweit definiert sowie Ereignis-/Recordgrößen.
Zeitfenster und Peak-Auswahl vorab festlegen. Lokale Kontinuumsreste sollen
mit ihrer nachgewiesenen Ordnung fallen; keine Maschinenpräzisionsforderung.
Globale Invarianten hängen auch vom Integrator ab: nahe Rundungsfehler nur,
wenn das konkrete diskrete Verfahren sie tatsächlich erhält. Erhaltung ist
keine Genauigkeitsbescheinigung. Vorzeichen und relative Änderungen benötigen
absolute Fehlergrenzen nahe null. Fehlende numerische PASS-Schwellen werden
nicht aus nachträglich günstigen Resultaten ergänzt.

## Gewichtete reduzierte Zustände

Für orthonormalisierte Gitteramplituden
A_sij=√w_Qi √w_φj ψ_sij gilt

$$\rho_{ss'}=\sum_{ij}A_{sij}A_{s'ij}^*,\quad N_s=\rho_{ss},
\quad C_{0+}=\rho_{0+}.$$

Bei normiertem Zustand sind Reinheit Trρ² und S=−Trρ logρ zu bestimmen.
Nur bei globaler Reinheit belegt gemischtes ρ_strat Verschränkung mit dem
Rest. Für Stratum-Materie-Verschränkung ist ρ_strat,φ=Tr_Qρ zu untersuchen;
positive Negativität ist ein hinreichender Zeuge, null kein allgemeiner Ausschluss.

$$[\rho_{\varphi|s}]_{jk}=N_s^{-1}\sum_i A_{sij}A_{sik}^*.$$

Bei N_s unter der vorab festgelegten Belegungsschwelle ist der konditionale
Record UNDEFINED, nicht null oder eins. Die quadrierte Uhlmann-Fidelität
F=(Tr√(√ρ_0 ρ_+ √ρ_0))² ist von einem Dichtevergleich zu unterscheiden.
Der quadrierte klassische Bhattacharyya-Überlapp der φ-Verteilungen ist eine
obere Schranke für F, kein identischer Wert (S8). Große Dichteüberlappung
schließt unterscheidbare phasenabhängige Records nicht aus.

Für eine deklarierte gemeinsame Referenzfrequenz ist
N_φ=⟨p_φ²/(2m_φ)+m_φ ω_ref² φ²/2⟩/(ℏω_ref)−1/2.
Dies ist keine basisunabhängig hergeleitete Teilchenzahl. Operator, Quadratur
und Randkonvention müssen zur Trajektorie passen.

## Keine notwendige Kohärenzschwelle des Stratumqubits

Die Baseline kann bei bestimmter kombinierter Parität kohärent transferieren
und verschränken, während C_0+=0 bleibt. QS-COHERENCE darf deshalb nicht als
notwendige Bedingung des Mechanismus verwendet werden. Untersucht werden
gemeinsame, φ-gewichtete Korrelationen und die integrierte Transferrate.
Auch gleiche ω_0=ω_+ schließen Materierecords nicht aus. Eine behauptete
Universalschwelle F<0.1 ist nicht fundamental und hier nicht als PASS eingefroren.

| Lauf | Änderung | Zulässige Folgerung |
|---|---|---|
| A | vollständiger deklarierter Operator | Hauptvergleich |
| B | g_1=0 | kein Transfer aus reinem Anfangskanal; Record des leeren Kanals undefiniert |
| C | konstantes g_1 | direkte Mischkraft null; indirekte diagonale Rückwirkung möglich |
| D | ω_0=ω_+ | keine Garantie identischer Records |
| E | strikte Projektion auf gemeinsamen Materiegrundzustand | P_vac φ P_vac=0; direkte lineare Mischung entfällt |
| F | Kopplung außerhalb des Paketbereichs | Restbeitrag durch Paketflanken quantitativ begrenzen |

QS-TRANSFER verlangt eine aufgelöste Belegung und geschlossene Flussbilanz.
QS-ENTANGLE muss seine Partition nennen; QS-MATTER seine Basis und Energie.
QS-RECORD braucht definierte konditionale Zustände; QS-CYCLE braucht
nachgewiesenen Zwischenpeak und Rückkehr. Ein Integral von J gleich null
allein kann auch überhaupt keinen Transfer bedeuten. Das Anfangszustands-Echo
ist eine Autokorrelation; ein Vergleich gekoppelt/Referenz verwendet
|⟨ψ_i|U_ref†U_full|ψ_i⟩|². Revivals können Boxeffekte sein.

## Ereignisse und Historien

POVMs auf einem Uhrschnitt ergeben p=⟨E⟩. Tatsächlich wiederholte Messungen
benötigen zusätzlich Instrumente für die Zustandsänderung. Für ungemessene
Historien werden zeitgeordnete relationale Klassenoperatoren und ein
vollständiges alternatives Ereignissystem definiert (S9).

$$C_B=P_{exp}(\chi_f)P_{min}(\chi_b)P_{con}(\chi_i),\quad
D(\alpha,\beta)=\langle\Psi|C_\beta^\dagger C_\alpha|\Psi\rangle.$$

Die P sind hier Heisenberg-/relationale Projektoren; im Schrödingerbild stehen
die Propagatoren dazwischen. Ein kleiner Q-Bereich ist kein Wendepunkt.
Kontraktion/Expansion dürfen nicht als Spektralprojektoren eines unzulässigen
gewöhnlichen Halbgeradenimpulses vorausgesetzt werden; zeitlich aufgelöste
Geometrieereignisse sind eine mögliche Alternative. Ergänzungen um Kanal und
Materierecord bei gleichem Uhrwert kommutieren bei getrennter Faktorwirkung.
Anfänglicher positiver Kanal und spätere Rückkehr müssen beide festgelegt sein.

Die Gegenalternative umfasst alle übrigen Historien. Bei Konditionierung auf
P_con ist die entsprechende Normierung separat zu führen. Für ein ausreichend
besetztes Paar ist |D(B,not B)|/√(D(B,B)D(not B,not B))≤ε_D eine hinreichende
Medium-Dekohärenzanforderung; seltene/Nullzweige brauchen eine absolute Kontrolle.
ε_D ist hier nicht festgelegt. Schwächere Konsistenzbedingungen sind möglich.
Eine einzelne ungestörte Trajektorie genügt nicht: projizierte Zweige müssen
weiterentwickelt werden. Ein erfüllter Klassenoperator trennt Wandbounce und
Mischkraft-Ursache nicht ohne das unabhängige Impulsbudget.
