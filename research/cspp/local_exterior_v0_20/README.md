# CSPP v0.20: Lokale äußere History und exakte Überlappung

Eine geschlossene Lorentz-invariante Volumenformel verbindet die tatsächliche
Intervallüberlappung mit exakten Archivzählungen und lokalen KG-Werten.
Für den endlichen History-Wurzelbereich **P = [-6,-5] × [-2,2]³** wird der
vollständige Beitrag zum gemittelten Detektor einschließlich des Transports
über bekannte und unbekannte aktive Punkte eingeschlossen.

Die oberen bedingten Erwartungswertschranken liegen für vier Archive und
zwei Fenster ungefähr zwischen **0,004697 und 0,005799**. Das Ziel 0,001
bleibt unerreicht; der komplementäre Außenbereich wird hier nicht neu
integriert. Die globale v0.19-Restmajorante bleibt unverändert.
**METHOD_HOLD und G1 HOLD bleiben bestehen. Frische Bestätigung: NOT_RUN.**
Keine neue Wolke, keine neue Quelle, keine neue statistische Freigaberegel.

- [Bericht (PDF)](Lokale_aeussere_History_v0_20.pdf)
- [Unverändertes vollständiges Prüfpaket (ZIP)](CSPP_Lokale_aeussere_History_v0_20_Pruefpaket.zip)
- [Vollständige Herleitung und Aussagegrenzen](cspp_v020/PROOF.md)
- [Festgelegte Prüfstellen und Integrationsregion](cspp_v020/PROTOCOL.json)
- [Ergebnisse bei 192 Bit](cspp_v020/results/LOCAL_192.json)
- [Kontrollen und Gegenrechnungen](cspp_v020/results/CHECKS.json)
- [Reproduktionsnachweis](cspp_v020/REPLAY.json)
- [Offene nächste Arbeitsschritte](cspp_v020/NEXT_STEPS.json)

## Prüfung und Reproduktion

```sh
python3 -m pip install numpy==2.3.5 python-flint==0.8.0
python3 -B research/cspp/local_exterior_v0_20/publication_check.py --replay
```

Python 3.12. Die Publikationsprüfung kontrolliert PDF, ZIP, alle 53
ursprünglichen Paketdateien und 52 Paket-Hashes. Die isolierte vollständige
Neuberechnung bei 128/192 Bit muss alle 21 numerischen Ergebnisdateien
bytegleich reproduzieren. Enthalten sind 6.810 physikalische
Intervallvergleiche, 1.698 unabhängig durch Ganzzahldarstellung geprüfte
Archivzählungen, 55 separate validierte Kugelkappen-Quadraturen, 63 direkte
Poissonsummen mit Rest, 243 Kerntabellenkontrollen und drei Negativkontrollen.

Der [GitHub-Workflow](../../../.github/workflows/cspp-local-exterior.yml)
prüft den eingereichten Commit und `main`. Die ursprüngliche
`repository_publication: NOT_PERFORMED_FOR_V020`-Angabe in `cspp_v020/STATUS.json`
beschreibt den Stand des unveränderten Originalpakets vor dieser
Veröffentlichung. Aktuelle Publikationsmetadaten stehen separat in
[PUBLICATION.json](PUBLICATION.json).

## Aussagegrenze

Die 1.698 kausalen Prüfintervalle gehören zu acht festen mathematischen
Historyprüfstellen und 223 bekannten aktiven Archivpunkten; sie sind kein
neues Zufallsensemble. Die integrierte Patchschranke umfasst den ganzen
deklarierten vierdimensionalen Bereich und den vollständigen gemittelten
Detektor. Sie ist keine Realisierungsgenauigkeit und keine Zertifizierung
des gesamten äußeren Historybereichs. Eine obere Patchgrenze darf nicht
von einer oberen Gesamtgrenze abgezogen werden. Numerische und symbolische
Kontrollen ersetzen kein unabhängiges wissenschaftliches Review.

Basis: [v0.19 / PR #151](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/151),
Merge `b3e2c41bb32fec02a08432b40cc95acba013952a`.
