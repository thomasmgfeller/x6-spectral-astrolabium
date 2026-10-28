# CSPP v0.10: Detektorintegration und Anfangsdatenfehler

Entwicklungsbenchmark für die nächsten beiden offenen Methodenfragen aus
[v0.9](../detector_transfer_v0_9/NEXT_STEP.md): analytisches Zeitintegral
mit vollständiger Kugelintegration sowie getrennte H1-/H3-Fehlerobergrenzen
bis zur endlichen Detektorantwort.

Dieselben acht bekannten Archivwolken, dieselben Quellen und Detektoren.
Keine neuen Sprinklings und keine unabhängige Bestätigung. Die Rechenquellen
wurden vor dieser neuen Integration öffentlich festgelegt.

**Ergebnis: METHOD_HOLD.** Die 74 nichttrivialen ursprünglichen Intervalle
sind etwa 5- bis 6-mal enger; 11/80 statt 6/80 H1-Integrationsbudgets bestehen.
Darunter sind fünf nichtverschwindende kompakte Signale. Alle Wellen bleiben
über dem Ziel. Die getrennten kompakten Anfangsdatenobergrenzen qualifizieren 0/32 Fälle.
Höhere lokale Taylor-Ordnung behebt fehlende Quellstützpunkte grundsätzlich nicht.

- [Protokoll](PROTOCOL.json)
- [Herleitung und Grenzen](METHODS.md)
- [Analytische Kontrollen](audit10.py)
- [Ergebnisse und Anschlussentscheidung](RESULTS.md)
- [Strukturelle Grenze des lokalen Adapters](ADAPTER_OBSTRUCTION.md)
- [Reproduktionsprüfung](results/CHECKS.json)

Reproduktion mit den fixierten Abhängigkeiten:

```sh
python -m pip install -r research/cspp/detector_methods_v0_10/requirements.txt
python -O -B research/cspp/detector_methods_v0_10/verify10a.py
python -B research/cspp/detector_methods_v0_10/verify10a.py --replay
```

G1 bleibt HOLD; G2/G3 NOT_RUN. Ein engeres Integral allein begründet noch
kein physikalisches Fluktuationsmodell.

Der nach dem Lauf korrigierte Prüfeinstieg ist `verify10a.py`;
[Prüfkorrektur und unveränderte Produktionsquellen](VERIFICATION_AMENDMENT.json).
