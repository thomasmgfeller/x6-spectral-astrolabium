# Datenformat und Prüfregeln v0.1

## Quellen

Die NPZ-/JSON-Dateien in inputs/ sind unveränderte v0.2-Quellen. label_quotient.json ist der unveränderte m=0,1,2-Quotientenbericht aus dem Benchmark. Commit, Git-Blob und lokale Pfade stehen in provenance.json; der Paketprüfer kontrolliert jeden Quellblob.

Der Generator ist auf diesen endlichen **z=1-Kontrollfall** begrenzt. Er ist kein generischer Importer beliebiger Randamplituden. Die Eingabe muss Rolle GEOMETRY_SPECTATOR_CONTROL, Konvention coefficient_map, diagnostische Produkte I8 und die acht eindeutigen Basislabels besitzen. Eine explizit deklarierte Permutation wird nach gemeinsamer Prüfung von Matrix, Gram und Indexlabels kanonisiert. Eine falsch bezeichnete kanonische Basis wird zurückgewiesen.

## NPZ-Ausgabe

Alle Archive sind ohne Pickle lesbar: numpy.load(..., allow_pickle=False).

| Feld | Form | Bedeutung |
|---|---|---|
| A_source_orthonormal | 8×8 | Quell-Koeffizientenabbildung in kanonischer formaler Testbasis |
| A_indicator | 8×8 | Koeffizientenabbildung der gewählten Zuordnung in Indikatoren |
| B_indicator | 8×8 | Kovariante Matrixelemente derselben Zuordnung, $B=GA$ |
| normalized_from_coefficients | 8×8 | $G^{1/2}AG^{-1/2}$ |
| normalized_from_covariant | 8×8 | $G^{-1/2}BG^{-1/2}$; muss numerisch übereinstimmen |
| G_selected_aux | 8×8 | Positive ausgewählte Hilfs-Gram |
| G_parent_aux | 14×14 | Sieben Quellorbits × externes Testlabel |
| embedding_indicators | 14×8 | Auswahl E |
| embedding_orthonormal | 14×8 | Normierte Einbettung J |
| defect_diagnostic_I8 | 8×8 | $U^\dagger U-I_8$ der deklarierten Testabbildung |
| basis, mode, role, z | Labels/Skalare | Eindeutige Zuordnung und Kontrollphase |

G_selected_aux heißt bewusst nicht physikalisches Ein-/Ausgangsprodukt. Das NPZ enthält keine Uhrschrittweite und keine aus einer Materiewirkung hergeleiteten Moden.

Die JSON-Datei führt Quellen-/Generator-/NPZ-Hashes, Auswahl, numerische Identitätsresiduen, Singularwerte, Spektral- und Frobeniusdefekte sowie den physikalischen Status. Die Aussage isometry_of_declared_test_map=FAIL ist auf die jeweilige Hilfszuordnung beschränkt und setzt das physikalische Gate MODEL nicht auf FAIL; dieses bleibt HOLD.

## Numerische und exakte Prüfungen

Komplexe Matrizen werden als complex128 berechnet. Die Gramprüfung verwirft nichtendliche, nichtquadratische und deutlich nicht-Hermitesche Matrizen. Erst nach erfolgreicher Prüfung darf ein Rundungsrest bis $10^{-12}\max(1,\|G\|_2)$ symmetrisiert werden; der gemessene Rest wird protokolliert. Eigenwerte müssen strikt größer als $10^{-12}\max(1,\lambda_{\max})$ sein. Es gibt kein Abschneiden negativer Eigenwerte und keine automatische Regularisierung.

Identitätsresiduen müssen die dokumentierte numerische Toleranz $10^{-12}$ erfüllen; sie sind keine physikalischen Fehlerbudgets. Vor dem Schreiben werden sämtliche Pflichtkontrollen und die strikte JSON-Serialisierung durchgeführt. Ungültige Eingaben führen zu einem von null verschiedenen Prozessstatus.

results/exact_certificates.json verwendet rationale Arithmetik für Singularwertpolynome, Frobenius-Normquadrate und die positiven Koeffizienten der diagonalen Produktobstruktion. Die dezimalen NPZ-/JSON-Matrizen bleiben Gleitkommadaten; sie werden nicht als symbolisch exakt bezeichnet.

Deterministische NPZ-/ZIP-Archive verwenden sortierte Einträge, feste Zeitstempel und unkomprimierte Nutzdaten. SHA256SUMS.json umfasst alle Paketdateien außer sich selbst und dem äußeren ZIP. Der Prüfer vergleicht das äußere ZIP, falls vorhanden, mit einer neu aufgebauten Bytefolge. Deshalb lässt sich auch das entpackte Paket unabhängig prüfen.
