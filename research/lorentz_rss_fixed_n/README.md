# Roy–Sinha–Surya bei fester Punktzahl

Dieses Paket überträgt die Poisson-Kettenmomente auf n unabhängige,
bezüglich des physikalischen Volumens gleichverteilte Punkte. Es ergänzt den
[abgeschlossenen Krümmungsbenchmark](../lorentz_curvature/README.md).
Der frühere Negativbefund und die Grenze durch Dichtezwillinge bleiben erhalten.

**Vor dem Ziellauf:** [Prüfvertrag](contract.json), [Herleitung](DERIVATION.md),
exakte Kontrollen und Auswertung werden öffentlich fixiert. Der Vertrag legt
Budgets, Seeds und Entscheidungskriterien vorab fest. Kein Anspruch auf eine
unabhängige Präregistrierung oder externe Replikation.

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
python3 -B research/lorentz_rss_fixed_n/verify.py --replay
```

`verify.py --replay` benötigt das veröffentlichte Ergebnisarchiv und einen
vollständigen Git-Checkout einschließlich Quellencommit. Es prüft sämtliche
Relationen über SHA-256, alle Kettenzahlen exakt und die Gleitkomma-Ausgaben
mit deklarierten Toleranzen. Wissenschaftliche Nichtbestätigungen werden
nicht als Softwarefehler umgedeutet.

Absolute Krümmung benötigt eine unabhängige Skala. Die de-Sitter-Familie prüft
nur eine Ricci-Kombination. Allgemeine Krümmungsrekonstruktion, exakte
Unsicherheitsintervalle dafür und eine Überwindung der Dichtezwillinge sind
nicht nachgewiesen.
