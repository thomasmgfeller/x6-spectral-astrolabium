# Datenschnittstellen v0.2 (Spezifikation, kein Extraktionsprogramm)

Diese Formate konkretisieren künftige Lieferungen. Ein NPZ allein ist keine
physikalische Provenienz. Ein JSON-Sidecar und SHA-256-Manifest sind erforderlich.
NPZ-Dateien sind ohne Pickle zu laden; Zahlen müssen endlich sein. Ein Leser
darf weder Maße fitten noch problematische Eigenwerte stillschweigend abschneiden.

## Gemeinsame Metadaten

dataset_id, producer_commit, action_version, regulator_definition, units,
hbar, clock_definition, boundary_class, gauge_quotient, boundary_conditions,
basis_order, basis_identification, cutoff, quadrature, precision,
tolerances, source_hashes und evidence_scope. Nicht bestimmte Werte bleiben
null und blockieren die davon abhängige Entscheidung. Mehrere Schritte und
Verfeinerungen sind eindeutig zu Paaren und Direktkompositionen zuzuordnen.

## Randkern

Erforderliche NPZ-Schlüssel: K, G_in, G_out, delta_chi. K hat Form
(d_out,d_in); Gram-Matrizen sind quadratisch, hermitesch innerhalb einer
deklarierten Toleranz und positiv auf dem begründeten Quotienten. Für einen
gewöhnlichen unitären Schritt ist ein gemeinsamer gleichdimensionaler Raum
mit dokumentierter Identifikation nötig. Nichtquadratische Kerne unterstützen
keinen gewöhnlichen Matrixlogarithmus.

Sidecar kernel_convention ist entweder covariant_matrix_elements oder
coefficient_map. Die Normierung ist entsprechend BRIDGE_CONTRACT verschieden.
Bei gleichem Kanalumfang: n_channels=2, states_per_channel=N und Gesamtgröße
2N. Das mehrdeutige historische Feld channel_dim wird nicht verwendet.
Reihenfolge: alle Nullatomzustände, danach alle positiven Zustände. Q- und
Materie-Unterordnung sowie mögliche Phasen müssen angegeben werden.

Optional: Q, phi, basis_transform_in, basis_transform_out. Arrays Q/phi allein
beweisen keine Tensorproduktstruktur. Für Gruppenprüfung zusätzlich direkte
Kerne bei Δχ_1+Δχ_2 und eine Folge kleiner Schritte. Für allgemein zeitabhängige
Dynamik chi_in/chi_out statt nur eines Differenzparameters.

Vorgesehene Ausgaben eines späteren Programms: K_tilde, Gram-Spektren und
Kondition, polar_unitary, polar_positive, H_full, H_unitary, beide Blockpaare,
Logzweig, absolute/relative Fehler und NICHT_AUSGEWERTET-Gründe. H_unitary ist
nur der Polardiagnostik zugeordnet; es darf H_full nicht still ersetzen.

## Trajektorie

psi: complex (Nt,2,NQ,Nphi); Q,phi,chi: streng geordnete reelle 1D-Arrays.
weights_Q,weights_phi: positive Quadraturgewichte. Bei nichtdiagonalem
Randprodukt ist eine explizite orthonormalisierende Basisabbildung erforderlich;
Tensor-Partialspuren sind nicht ohne begründete Faktorzerlegung zulässig.
Geometrie-Domäne, Dirichlet-Endpunkte und gespeicherte Randwerte sind eindeutig.

Zusätzlich hbar, M_Q, m_phi, omega_ref sowie alle für Kräfte/Energie benötigten
Koeffizienten oder der konkrete diskrete Hamiltonoperator. g1 allein genügt
nicht für das volle Impulsbudget. Variable Masse/Mode muss als Erweiterung
markiert werden. Der Integrator, Zeitschritt, Ausgabeschritt und Fehlerbudgets
sind getrennte Metadaten. Reduzierte Dichtematrizen werden mit den Gewichten
in VALIDATION.md gebildet. Die Nachweisgrenze für kleine Kanalbelegungen wird
vorher festgelegt.

Vorgesehene Ausgaben: Norm und Energie, Kanalbelegungen, kohärente gemeinsame
Korrelationen, Entropie/Reinheit, partitionierte Verschränkungszeugen,
Referenzanregung, definierte Records, Transfer- und Kraftimpulse,
Randflüsse, lokale Residuen. Historien benötigen zusätzlich einen reproduzierbaren
Propagator für projizierte Zweige; psi allein reicht dafür nicht.

## Ergebnisdateien und fehlende Implementierungen

Die vorhandene Datei results/checks.json enthält ausschließlich kleine
Kontrollbeispiele, keine Daten in den beiden obigen Formaten. Die im
Ausgangsentwurf benannten Programme randkern_hamilton_extraktion.py und
n0b_quantensignaturen.py werden hier nicht als vorhandene Implementierungen
ausgegeben. Ihre Quellcodes, Tests und Datensätze müssen gesondert geliefert
oder neu entwickelt und qualifiziert werden. Die Quelle des historischen
Solvers ist ebenfalls vor einer Wiederaufnahme zu identifizieren.
