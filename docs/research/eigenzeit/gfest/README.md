# GFEST: Eigenzeit-Stabilität / proper-time stability

Veröffentlicht am 23. Oktober 2026. Forschungsentwürfe von und für das X6-Projekt;
keine unabhängige fachliche Begutachtung oder formale Beweisverifikation.

## An interessierte Physikerinnen und Physiker

Sie arbeiten an Causal Sets, Lorentz-Geometrie, statistischen inversen Problemen
oder diskreten d’Alembert-Operatoren? Wir laden Sie ein, die Voraussetzungen und
Beweise zu prüfen, die Rechnungen zu reproduzieren und Gegenbeispiele vorzulegen.
Die Leitfrage lautet: Wie stabil sind Operatorgewichte, wenn nur endlich viele,
möglicherweise korrelierte Kausalzählungen beobachtet werden?

| Dokument | Inhalt | Direkter Zugang |
| --- | --- | --- |
| GFEST v0.1, 11 Seiten | Bedingte Stabilitätssätze, Beweise, Fehlergrenzen und offene Beweispflichten | [PDF](General_Finite_Error_Stability_Theorem_v0_1.pdf) · [Original-Prüfpaket](GFEST_v0_1_Quellen_und_Pruefungen.zip) · [LaTeX und Code](v0.1/) |
| Ergänzung v0.2, 8 Seiten | Lichtkegelgrenzen, gemeinsame Bewegungen und rationales lokales Paarraumzertifikat | [PDF](GFEST_Stabilitaet_v0_2.pdf) · [Original-Prüfpaket](GFEST_Stabilitaet_v0_2_Pruefpaket.zip) · [LaTeX und Code](v0.2/) |

**Empfohlener Einstieg:** Lesen Sie zuerst die Zusammenfassung und den Status von
v0.2. v0.1 liefert die vollständigen Definitionen und den allgemeinen bedingten
Rahmen. v0.2 ergänzt v0.1; beide Fassungen bleiben separat zitierbar.

### Was gezeigt wird und was offen bleibt

- v0.1 formuliert ein Identifizierbarkeitskriterium auf einer kompakten Modellklasse
  und eine quantitative Schranke im vollständigen, beschrifteten Landmarkenmodell.
  Die Voraussetzungen müssen für eine Anwendung jeweils nachgewiesen werden.
- v0.2 gibt im deklarierten lokalen Modell um die archivierte Referenz `cloud_09`
  eine rationale Schranke: Sind die beiden vollständigen Beobachtungsgesetze
  jeweils höchstens `1e-5` in totaler Variation vom Referenzgesetz entfernt,
  ist die symmetrische relative Operatorgewichtsabweichung `g < 0.07`.
  Bekannte Dichte und Skala, das vollständige beschriftete Poisson-Landmarkenmodell
  und die weiteren Voraussetzungen des Berichts sind wesentlich.
- Das ist keine 7%-Genauigkeitsgarantie aus einer einzelnen Stichprobe.
  Der ursprüngliche allgemeine Claim `TV(Pθ,Pθ′) ≤ 1/4 ⇒ g ≤ 1/5` bleibt offen.
  Die 38 offenen Zellen aus [PR #122](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/122)
  werden durch die Ergänzung nicht geschlossen. Veröffentlichung bedeutet keine
  Zusammenführung dieses separaten Forschungs-PRs.
- Algebraische Kontrollen, numerische Diagnostik und lokale rationale Zertifikate
  sind im Material getrennt ausgewiesen. Keine formale Verifikation, kein
  unabhängiges Peer Review und kein Neuheitsanspruch werden behauptet.

### Unabhängig mitprüfen

Besonders hilfreich sind Prüfungen der Zielidentifizierbarkeit, der vollständigen
Beobachtungsmaske, der Rangbedingungen, der gemeinsamen Zählverteilung und der
Behandlung bewegter Landmarken. Auch ein reproduzierbares Scheitern ist ein Ergebnis.

[Fachliche Rückmeldung eröffnen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/issues/new?template=01-math.yml&title=GFEST%3A%20)
(GitHub-Konto erforderlich). Bitte nennen Sie Version, Satz/Gleichung oder Datei,
Annahmen, Reproduktionsschritte, Softwareversionen und das beobachtete Ergebnis.
Die Dokumente und Downloads sind ohne Anmeldung zugänglich.

### Reproduktion und Originaltreue

Die ZIP-Dateien werden unverändert veröffentlicht. `v0.1/` und `v0.2/` enthalten
ihre unverändert entpackten Inhalte einschließlich der ursprünglichen PDF-Dateien
und `SHA256SUMS`. In einer Arbeitskopie ausführen, da die Skripte `validation.json`
neu schreiben:

```sh
cd v0.1
python -m pip install -r requirements.txt
python verify_algebra.py
```

```sh
cd v0.2
python -m pip install -r requirements.txt
python verify_stability.py
```

Die separat bereitgestellten Lese-PDFs im übergeordneten Ordner sind ebenfalls
unveränderte Originale. Ihre Bytes unterscheiden sich von den PDF-Dateien in den
Archiven; der vollständige, mit `pdftotext -layout` extrahierte Text ist identisch.
Beide Varianten werden mit eigenen SHA-256-Werten in [PUBLICATION.json](PUBLICATION.json)
dokumentiert. Die ursprünglichen Archivprüfsummen bleiben erhalten.

Die Kontrollskripte wurden für diese Veröffentlichung in separaten Arbeitskopien
erneut ausgeführt. Das bestätigt die dokumentierten Rechenkontrollen und ersetzt
keine unabhängige fachliche Prüfung. Details: [PUBLICATION_CHECKS.json](PUBLICATION_CHECKS.json).

Frühere Ergebnisse bleiben nachvollziehbar:
[lokale Schranke, PR #99](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/99),
[zertifizierte Ausschlüsse im festen Suchraster, PR #108](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/108),
[Ergebnis und Grenzen des Poisson-Tail-Vergleichs](../../../../research/lorentz_local_dalembert/poisson_tail_obstruction/README.md).

## Invitation to physicists

Do you work on causal sets, Lorentzian geometry, statistical inverse problems or
discrete wave operators? We invite independent proof review, computational
reproduction and counterexamples. The PDFs are in German; the verification code,
requirements, archived results and source snapshots are available above.

Start with the v0.2 abstract and scope, then consult v0.1 for the full definitions
and conditional stability statements. The local `g < 0.07` certificate assumes
that each complete observation law is within TV `1e-5` of the archived reference,
under the declared complete labelled Poisson-landmark model with known density
and scale. It is not a statistical reconstruction guarantee from one sample.
The original general claim at pairwise TV `1/4` remains open, as do the 38 cells
referenced in PR #122. No independent expert review, proof-assistant verification
or novelty claim is asserted.

[Submit scientific feedback](https://github.com/thomasmgfeller/x6-spectral-astrolabium/issues/new?template=01-math.yml&title=GFEST%3A%20)
with the document version, theorem/equation or file, assumptions and reproducible
steps. Negative results and counterexamples are welcome. Reading and downloading
require no account; submitting an issue requires GitHub sign-in.

Original project contributions follow the repository's [Apache-2.0 license](../../../../LICENSE)
and [license scope](../../../../LICENSE_SCOPE.md); cited third-party works retain
their own terms. Publication is separate from scientific qualification.
