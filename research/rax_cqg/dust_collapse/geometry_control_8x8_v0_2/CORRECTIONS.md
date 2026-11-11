# Korrekturen gegenüber dem eingereichten 8×8-Artefakt

| Punkt | Korrektur | Prüfung |
|---|---|---|
| „Einzig evidenztreue Erweiterung“ | Identität auf vier Zusatzlabels als zusätzliche Kontrollannahme kenntlich gemacht | JSON-Rolle und physikalische Statuswerte |
| Geometrie zuerst geordnet | Gemeinsame Zeilen-/Spaltenpermutation zu Stratum/Geometrie/Materielabel | Exakte Rückpermutation und ursprünglicher Geometrieblock 26 I4 |
| `channel_dim=2` | `n_channels=2`, `states_per_channel=4`, explizite Basis und Indexarrays | Metadaten-/NPZ-Test |
| Tensorrest als Mischungsnorm bezeichnet | Tensorrest, echte Stratum-, Materie- und kombinierte Labelmischung getrennt | Diagonal- und Geometrieänderungen ergeben keine falsche Labelmischung |
| Mischblöcke nicht unabhängig geprüft | Tatsächliche Masken aus den Kanal-/Materieindizes verwendet | Eingefügte Stratum- bzw. Materiemischung wird erkannt |
| Falsche Kontrollen nur als Boolean ausgegeben | Pflichtkontrollen lösen einen Fehler aus; CLI endet mit Code 2 | Eingespeiste Quellen- und Strukturfehler erzeugen keine Dateien |
| NaN/Inf wurden exportiert | Endliche Eingaben, Matrizen, Diagnostik und striktes JSON vorgeschrieben | CLI-Negativkontrollen und nichtendliche Matrix |
| Gleitkommadeterminante als exaktes Resultat missverständlich | Gaußsche Ganzzahlarithmetik an 1,−1,i; allgemeines z bleibt complex128 | det(1)=24, det(−1)=−12, det(i)=70+6i |
| Implizites physikalisches Produkt | I8 nur als deklarierte diagnostische Basisnormierung | Physikalisches Produkt und Uhr bleiben null/offen |
| Mehrdeutige Eingabemodi | Phase, κ und direktes z schließen sich gegenseitig aus | CLI-Konflikttest |
| Reproduktion nur über Wertevergleich | Deterministisches NPZ/JSON und isolierter Replay | Sieben Dateien bytegleich |

Nullmischung im Kontrollkern ist konstruktionsbedingt. Weder Superselektion noch
ein physikalischer Stratumwechsel werden daraus abgeleitet. Die frühere
Quellenmatrix im [Randkern-Benchmark](../boundary_kernel_benchmark_v0_1/README.md)
und deren wissenschaftliche Aussagegrenzen bleiben unverändert.
