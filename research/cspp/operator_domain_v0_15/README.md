# CSPP v0.15: Operator, Gebiet und Randbehandlung

**Ergebnis:** Bei `rho=3/pi` und `epsilon=1/16` kann eine reine Vergrösserung
des vergangenen Diamantgebiets die bisherige Operatorzelle nicht qualifizieren.
Für den vorhandenen Gauß-Kontrolltest bleibt der relative Mittelwertfehler für
jedes reelle `H>=4` nachweislich über **41,70 %**; im unbegrenzten Gebiet
beträgt er **68,49 %**. Der Ausschluss verwendet validierte Quadratur,
eine Ableitungsschranke zwischen 129 Stützstellen und eine analytische Resthülle.

Diese Prozentwerte gelten für das Kontrollfeld. Die vollständige Aufteilung
des Fehlers des ursprünglichen kompakten Detektormodells zwischen Operator und
fehlender äusserer Vergangenheit bleibt offen. **METHOD_HOLD und G1 HOLD
bleiben bestehen.** Kein neuer Kandidat, kein neues Ensemble und kein
Ausschluss der gesamten Operatorfamilie.

## Bericht und reproduzierbares Paket

- [Bericht als PDF](Operator_Gebietsfehler_v0_15.pdf)
- [Vollständiges Prüfpaket als ZIP](Operator_Gebietsfehler_v0_15_Pruefpaket.zip)
- [Herleitung und wissenschaftliche Grenzen](operator_gebiet_v0_15/README.md)
- [Prüfergebnisse](operator_gebiet_v0_15/results/CHECKS.json)
- [Kontinuierlicher Gebietsausschluss, 192 Bit](operator_gebiet_v0_15/results/DOMAIN_CERTIFICATE_192.json)
- [Vollständige Fehlerdiagnose, 192 Bit](operator_gebiet_v0_15/results/DIAGNOSIS_192.json)
- [Verstärkung der Operatordefekte zum Detektor](operator_gebiet_v0_15/results/RESIDUAL_GAIN_192.json)

38 Kontrollen, 659 überlappende Intervalle gleicher exakter Zielgrössen,
32 unabhängige rationale Kausalzählungen und neun Gegenrechnungen in anderen
Integrationskoordinaten sind bestanden. Präzisionsabhängige Endpunktschranken
werden getrennt behandelt und nicht als identische exakte Zielwerte ausgegeben.

Vier vorhandene Archivpaare erlauben die signierte Trennung von Randbias und
Realisierungsabweichung am Kontrollfeld. Acht bekannte Wolken dienen der
History- und Verstärkungsdiagnose am ursprünglichen Detektor. Quelle,
Detektorfenster und Kontinuumsreferenz bleiben unverändert.

## Reproduktion

Aus dem Repositorywurzelverzeichnis, mit Python 3.12 und einem C++17-Compiler:

```bash
python3 -m pip install -r research/cspp/operator_domain_v0_15/operator_gebiet_v0_15/requirements.txt
python3 -B research/cspp/operator_domain_v0_15/publication_check.py --replay
```

Der Prüfer kontrolliert die unveränderten Datei- und Archivhashes, entpackt in
ein temporäres Verzeichnis, wiederholt alle drei Rechnungen bei 128 und 192 Bit
und vergleicht die neuen Intervalle mit den veröffentlichten Ergebnissen.
Die ursprünglichen Dateien bleiben erhalten. Der eingefrorene `source_snapshot`
ist Bestandteil des Standalone-Pakets; er verhindert Abhängigkeiten von späteren
Änderungen an Vorgängerversionen.

Die Basis ist [PR #146](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/146)
mit Commit `56207e7d36be4cddc897edf01a613c0be8837b86`. Diese Veröffentlichung
führt die noch offenen Vorgänger-PRs nicht automatisch in `main` zusammen.
