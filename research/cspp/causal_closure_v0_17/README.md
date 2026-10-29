# CSPP v0.17: Endliche aktive Hülle und Konvergenz der KG-History

Die gesamte aktive kausale Vergangenheit des unveränderten kompakten Detektors
liegt ab **H=21/4=5,25** im Diamanten Omega_H. Die unendliche Vergangenheit
betrifft damit die vorgeschriebene KG-History. Für die festgelegte glatte
kompakte Quelle wird ihre absolute Summierbarkeit und die fast sichere
Existenz der vollständigen Detektorantwort im Poisson-Modell hergeleitet.

**Der konkrete numerische Rest hinter Omega5 bleibt NOT_CERTIFIED.
METHOD_HOLD und G1 HOLD bestehen weiter.** Das Genauigkeitsziel 0,001 bleibt
unverändert. Keine neue Zufallswolke, kein neuer Seed und keine neue
statistische Freigaberegel wurden eingeführt. Die algebraischen Kontrollen
ersetzen keine unabhängige wissenschaftliche Prüfung des analytischen Beweises.

- [Bericht mit vollständiger Herleitung (PDF)](Aktive_Huelle_KG_History_v0_17.pdf)
- [Unverändertes Prüfpaket (ZIP)](Aktive_Huelle_KG_History_v0_17_Pruefpaket.zip)
- [Beweis als lesbarer Quelltext](causal_closure_v0_17/PROOF.md)
- [Rechenkontrollen und Ergebnisse](causal_closure_v0_17/results/ANALYTIC_CHECKS.json)
- [Protokoll und Aussagegrenzen](causal_closure_v0_17/PROTOCOL.json)

Der hinter Omega5 fehlende aktive Bereich hat exakt das Raumzeitvolumen
29*pi/1536. Seine zusätzliche Poisson-Punktzahl hat Mittelwert 29/512;
die Modellwahrscheinlichkeit für mindestens einen Punkt beträgt rund 5,51 %.
Das bestimmt keine konkrete Fortsetzung und erlaubt keinen Leernachweis.

## Reproduktion

```sh
python3 -m pip install python-flint==0.8.0
python3 -B research/cspp/causal_closure_v0_17/publication_check.py --replay
```

Python 3.12; keine Netzwerkzugriffe im Prüfer. Der Publikationsprüfer bestätigt
PDF, ZIP, alle 20 originalen Paketdateien und die 19 Paket-Prüfsummen.
Der isolierte Wiederholungslauf führt die 288 rationalen und intervallgestützten
Kontrollen aus und vergleicht sämtliche Ergebnisfelder exakt. Nur die
protokollierte Python-Patchversion darf sich unterscheiden und wird separat
angezeigt; python-flint bleibt auf 0.8.0 festgelegt. Der unveränderte ursprüngliche
Paketprüfer verlangt zusätzlich dieselbe Python-Patchversion für Bytegleichheit.

Der [GitHub-Workflow](../../../.github/workflows/cspp-causal-closure.yml)
führt diese Prüfung bei Änderungen auf PRs und auf main aus.
Die Quellseminormen sind noch nicht numerisch eingeschlossen; der korrelierte
aktive Transport und der endliche geometrische Rest benötigen weitere Kontrolle.

Basis: [v0.16 / PR #148](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/148),
Merge `5c075bfae81ee6ab5edea72a8ec9aa9ed3583b69`.
