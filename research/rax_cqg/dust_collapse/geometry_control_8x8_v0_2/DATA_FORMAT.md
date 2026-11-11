# Ausgabeformat v0.2

Eigener Datensatztyp `GEOMETRY_SPECTATOR_CONTROL`, ausdrücklich kein vollständig
qualifizierter physikalischer Randkerndatensatz nach N0B-2C-MF. NPZ ohne Pickle,
JSON ohne NaN/Infinity. Basisnamen sind Testlabels, keine hergeleiteten Moden.

## Basis und Permutation

Die Originalreihenfolge war Geometrie/Stratum/Materielabel. Die neue Reihenfolge ist

| Index | Label |
|---|---|
| 0 | A, 0, 0m |
| 1 | A, 0, 1m |
| 2 | K, 0, 0m |
| 3 | K, 0, 1m |
| 4 | A, +, 0m |
| 5 | A, +, 1m |
| 6 | K, +, 0m |
| 7 | K, +, 1m |

A und K bezeichnen Zweierantikette und Zweierkette. Mit p=(0,1,4,5,2,3,6,7) gilt

$$K_{\rm neu}=K_{\rm alt}[p,p]
=I_{\rm stratum}\otimes K_{\rm geom}\otimes I_{\rm matterlabel}.$$

`original_to_output_indices` speichert p im Sinn: Ausgabeposition i liest
Originalposition p[i]. Zeilen und Spalten werden beide permutiert. Dasselbe
müsste mit jedem dazugehörigen Produkt oder Observable geschehen.

## NPZ-Felder

| Feld | Bedeutung |
|---|---|
| `z` | Endlicher komplexer Laurent-Parameter, ungleich null |
| `K_geom`, `K` | 2×2- bzw. 8×8-Zahlenmatrix |
| `basis`, `basis_layout` | Acht Labels; `stratum_geometry_matter` |
| `n_channels`, `states_per_channel` | 2 Strata, je 4 Testzustände |
| `n_geometry_states`, `n_matter_labels` | Je 2 |
| `stratum_index`, `geometry_index`, `matter_index` | Explizite Indizes pro Basisposition; positives Stratum als 1 codiert |
| `original_to_output_indices` | Gemeinsame Basispermutation |
| `role` | `GEOMETRY_SPECTATOR_CONTROL` |
| `diagnostic_operator_convention` | `coefficient_map`, ausschließlich für die formale Testinterpretation |
| `G_in_diagnostic`, `G_out_diagnostic` | Gewählte I8-Produkte der formalen Testbasis |
| `defect_diagnostic_I8` | K†K−I8 in dieser Basis |

Die Felder `channel_dim`, `G_in`, `G_out` und `delta_chi` werden nicht als
NPZ-Eingaben eines physikalischen Extraktors ausgegeben. Im Sidecar bleiben
physikalisches Produkt, physikalische Kernkonvention und Uhr einschließlich
`delta_chi` ausdrücklich null. Eine vorhandene Zahlenmatrix erlaubt keine
automatische Hochstufung des Datensatztyps.

## JSON und Messgrößen

Das Sidecar dokumentiert Quellcommit, Quellhash, Generatorhash, NPZ-Hash, Basis,
Testannahmen, alle drei Quellenkontrollen und die getrennten physikalischen
Statuswerte. Für z∈{1,−1,i} liegen exakte Gaußsche Ganzzahlen als Paare [Re,Im]
sowie exakte Determinanten und Defekt-Normquadrate vor. Der Frobeniusnormwert ist
daneben eine Gleitkommaanzeige. An anderen z ist `exact_source_phase_data=null`.

Die Mischungsnormen summieren die tatsächlich ausgewählten Einträge mit
unterschiedlichen Stratum- bzw. Materielabels, jeweils in beiden Richtungen.
`either_label_mixing_fro` benutzt die Vereinigung beider Masken ohne doppelte
Zählung. `tensor_residual_fro` ist separat der Rest zum deklarierten Tensorprodukt.
Eine Geometrieänderung bei unveränderten Zusatzlabels ist keine Labelmischung.

Für eine künftige physikalische Matrix sind Zustandsfunktionen, Quotientabbildung,
Maße, Uhr, Variationsraum und Materiewirkung unabhängig zu begründen. Bei
kovarianten Matrixelementen ist die Gram-Normalisierung anders als bei einer
Koeffizientenabbildung; siehe den [Brückenvertrag](../n0b_2c_mf_v0_2/BRIDGE_CONTRACT.md).
