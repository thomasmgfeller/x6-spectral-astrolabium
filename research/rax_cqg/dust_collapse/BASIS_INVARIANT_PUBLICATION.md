# Portable Reproduktion des basisunabhängigen Kopplungsbefunds

Der Bericht und das 28-Dateien-Prüfpaket v0.1 bleiben unverändert. Der lokale Original-Replay war für alle drei numerischen Dateien bytegleich.

Beim GitHub-Lauf erzeugte die numerische Bibliothek geringfügig andere Vorschlagsvektoren für die zusätzliche Rayleigh-Prüfung. Dieselbe Variation wurde lokal durch einen anderen OpenBLAS-Rechenkern reproduziert. Die vollständigen Amplitudenblöcke, ihre Fehlereinschließungen, die zertifizierten Singularwerte und die festen unabhängigen Schranken änderten sich nicht.

Die Veröffentlichungsprüfung führt deshalb aus:

```sh
python -B research/rax_cqg/dust_collapse/verify_basis_invariant_publication.py
```

Sie verlangt unveränderte Paket-Hashes, bytegleiche Quadraturdaten und exakte Gleichheit aller weiteren wissenschaftlichen Daten einschließlich Sylvester-Determinanten. Ausschließlich die Felder `trial_vector` und `Rayleigh_lower` der zusätzlichen unabhängigen Zertifikate dürfen zwischen Rechenkernen variieren. Die ursprünglichen und die neu vorgeschlagenen Vektoren müssen die angegebenen unteren Grenzen jeweils erneut in 192-Bit-Intervallarithmetik beweisen. Auch alle oberen Grenzen werden erneut durch positive Hauptminoren geprüft. Dadurch entstehen 40 erneut validierte Einzelzertifikate. Die ursprünglichen 13 Kontrollgruppen laufen vollständig.

Drei gezielte Negativkontrollen verlangen die Zurückweisung eines veränderten Amplitudeneintrags, eines Nullvektors als unterem Zeugen und einer zu kleinen oberen Normgrenze. Es gibt keinen allgemeinen Toleranzvergleich und keine Ausnahme für veränderte Amplituden oder Singularwerte.

Das ursprüngliche `verify.py` bleibt als strikter Byte-Replay für die aufgezeichnete numerische Umgebung erhalten. Die portable Prüfung ergänzt den Rechnerwechsel; sie verändert weder das mathematische Fehlerbudget noch den Geltungsbereich des endlichen E→F′-Befunds.
