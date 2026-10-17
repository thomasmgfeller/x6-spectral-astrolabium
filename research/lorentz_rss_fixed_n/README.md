# Roy–Sinha–Surya bei fester Punktzahl

Dieses Paket überträgt die Poisson-Kettenmomente auf n unabhängige,
bezüglich des physikalischen Volumens gleichverteilte Punkte. Es ergänzt den
[abgeschlossenen Krümmungsbenchmark](../lorentz_curvature/README.md).
Der frühere Negativbefund und die Grenze durch Dichtezwillinge bleiben erhalten.

**Abgeschlossen:** Die bedingten Formeln sind hergeleitet; 24.576 unabhängige
Punktwolken sind ausgewertet und vollständig intern reproduziert. Das gemeinsame
±5%-Präzisionsziel für die drei führenden Koeffizienten ist **nicht erreicht**.
Die unabhängige Zweierketten-Integration stützt die korrigierte Vorhersage;
die untersuchte allgemeine lineare Krümmungsrekonstruktion streut bei N=64/128
sehr stark.

[Ergebnisse und Grenzen](RESULTS.md) · [Prüfvertrag](contract.json) ·
[Herleitung / mathematical derivation](DERIVATION.md) · [Rohdaten](results/) ·
[Vollständiger Replay](replay.log)

Der [öffentliche Quellenstand 485d866](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/485d8663391966458965b6c282ef4add4eafdd46)
fixierte Budgets, Seeds und Kriterien vor dem ersten Ziellauf. Kein Anspruch
auf eine unabhängige Präregistrierung oder externe Replikation.

![Erwartungswerte, Näherungsfehler und Rauschen](results-overview.png)

Die wesentliche Formel lautet mit F_k=C_k/binom(n,k):

\[
E[F_k\mid n]=k!\chi_k[1+(\alpha_k-k\alpha_1)RT^2+
(\beta_k-k\beta_1)R_{00}T^2+\cdots].
\]

Die Konditionierung berücksichtigt die exakte Kombinatorik und das gekrümmte
normierende Volumen. Die Kovarianz ergibt sich aus überlappenden Teilmengen;
Kettenzahlen sind keine unabhängigen Poisson-Zählwerte.

## Reproduktion

Python 3.12, Linux/POSIX; Befehle vom Repository-Stamm:

```sh
python3 -m pip install -r research/lorentz_rss_fixed_n/requirements.txt
python3 -B research/lorentz_rss_fixed_n/selftest.py
python3 -B research/lorentz_rss_fixed_n/reproduce.py
```

`reproduce.py` benötigt das veröffentlichte Ergebnisarchiv und einen
vollständigen Git-Checkout einschließlich Quellencommit. Es prüft sämtliche
Relationen über SHA-256, alle Kettenzahlen exakt und die Gleitkomma-Ausgaben
mit deklarierten Toleranzen. Wissenschaftliche Nichtbestätigungen werden
nicht als Softwarefehler umgedeutet.

Erwartet: `PASS_FULL_RSS_FIXED_N_REPLAY` bei unverändertem wissenschaftlichem
Status `FORWARD_SLOPE_NOT_RESOLVED`. Nur Archiv prüfen:
`python3 -B research/lorentz_rss_fixed_n/reproduce.py --archive-only`.
Abbildung neu erzeugen: `python3 -B research/lorentz_rss_fixed_n/draw.py`.

**Transparenter Nachtrag:** Der erste direkte Aufruf des eingefrorenen
`verify.py` scheiterte an einem Import-Namenskonflikt mit dem älteren Paket.
`reproduce.py` lädt die richtigen Prüfmodule vorab und führt den unveränderten
Prüfer aus. Alle eingefrorenen Dateien, Rohdaten, Kriterien und Toleranzen
sind unverändert; Details stehen im Ergebnisbericht.

Absolute Krümmung benötigt eine unabhängige Skala. Die de-Sitter-Familie prüft
nur eine Ricci-Kombination. Allgemeine Krümmungsrekonstruktion, exakte
Unsicherheitsintervalle dafür und eine Überwindung der Dichtezwillinge sind
nicht nachgewiesen.
