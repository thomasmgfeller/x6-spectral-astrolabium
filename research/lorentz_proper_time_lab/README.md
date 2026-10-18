# Eigenzeit-Labor: Notebook und interaktiver Demonstrator

Ein ausführbares Lehr- und Forschungswerkzeug zur vorhandenen, bedingten
Eigenzeitreferenz. Es ergänzt deren Erklärung und Bedienung; es ist kein
neuer vorab festgelegter Wirksamkeitsversuch.

- **[Demonstrator öffnen](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/proper-time.html)** — ohne Installation, auch auf dem Smartphone.
- **[Jupyter-Notebook](eigenzeit.ipynb)** — eigenständig ausführbar, mit gespeicherten Beispielausgaben.
- [Abhängigkeiten](requirements.txt) und [numerischer Prüfbericht](verification.json).
- [Bestehender Gültigkeitsvertrag](../lorentz_proper_time_domain/README.md).

## Bedienung

1. Raumzeitdimension, Hintergrundbudget und wahre normierte Eigenzeit einstellen.
2. Türkise Punkte liegen im inneren Intervall zwischen p und q. K zählt alle
   Hintergrundpunkte in diesem Intervall; die Darstellung zeigt höchstens 1.400 Punkte.
3. Schätzung und 95%-Intervall mit der bekannten Simulatorwahrheit vergleichen.
4. 200 unabhängige Zählversuche starten. Überdeckung, deren Unsicherheit, Bias
   und RMSE werden für alle 200 berichtet; der Plot zeigt die ersten 40 ohne Auswahl.
5. Versuch als JSON exportieren und optional im Notebook unabhängig nachzählen.

Die Beispiele „Kaum Ereignisse“, „Mehr Information“ und „1 + 1 Dimensionen“
helfen beim Einstieg. Eine längste innere Kette wird für K≤256 angezeigt;
oberhalb dieser Grenze wird nur diese Zusatzberechnung ausgelassen.
Das 4D-Modell bleibt vierdimensional, obwohl die Grafik nur t und x₁ zeigt.

Der Browser rechnet lokal und lädt keine Laufzeitbibliotheken nach.
**Demonstrator offline** speichert eine eigenständig ausführbare HTML-Datei.
Ihre Berechnungen benötigen kein Netz; Dokumentationslinks verweisen weiter
auf die veröffentlichten Quellen. Der Browser speichert Versuche nicht
automatisch über das Schliessen der Seite hinaus; dafür gibt es den JSON-Export.

## Notebook starten

Python 3.12, in einer eigenen Umgebung:

```sh
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell stattdessen: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install jupyterlab
python -m jupyterlab eigenzeit.ipynb
```

Notebook und requirements.txt zusammen herunterladen. Alternativ funktioniert
ein bestehender Jupyter-Editor mit den genannten Python-Paketen. **Kernel neu
starten → Alle Zellen ausführen**; anschliessend Parameter in Abschnitt 1
ändern und alle folgenden Zellen erneut ausführen. Die Berechnung selbst
braucht keinen Netzwerkzugriff und keinen Repository-Checkout.

## Mathematischer und statistischer Vertrag

Bekannte flache Minkowski-Raumzeit, d=2,3,4, c=1. Die maximale Eigenzeit
zwischen den zentralen Endereignissen ist τ=Tθ; T ist eine externe Vorgabe.
Genau m unabhängige uniforme Hintergrundpunkte werden im äusseren Diamanten
gezogen. Die Endereignisse sind vorab festgelegt, werden nicht mitgezählt,
und das innere Intervall ist vollständig enthalten.

K~Binomial(m,θ^d), τ̂=T(K/m)^(1/d). Das 95%-Intervall transformiert die
zweiseitigen Clopper–Pearson-Grenzen monoton. Die Schätzung ist endlich im
Allgemeinen nach unten verzerrt. K=0 lässt eine positive obere Grenze stehen.
Bei 200 Wiederholungen wird zusätzlich ein Clopper–Pearson-Intervall für die
unbekannte Überdeckungsrate berichtet; eine empirische Rate unter 95% allein
ist noch keine Widerlegung des theoretischen Verfahrens.

Feste Gesamtzahl m ist nicht dasselbe Experiment wie eine unbedingte
Poissonzahl bei bekannter Intensität. Der feste Versuch ist aber die bedingte
Version einer homogenen Poisson-Beprobung. Die Darstellung nennt deshalb
m und keine fälschlich garantierte physische Ereignisdichte.

Keine Absicherung optionalen Stoppens oder einer nach Datenansicht
ausgewählten Familie von Versuchen. Dafür existiert die separate
[sequenzielle Referenz](../lorentz_proper_time_sequential/README.md).
Keine unbekannte Dichte, Krümmung, Randmasken, Abhängigkeiten oder fehlerhaften
Relationen im Gültigkeitsbereich. Die Kettenansicht kalibriert keine zweite
Uhr. Absolute Zeit- oder Planck-Messfähigkeit wird nicht behauptet.

## Implementierung und Gegenprüfung

- `core.js`: Sampler, Zähler, Clopper–Pearson-Inversion, Kettenpfad,
  endliche Binomialsummen für Bias/RMSE. Der Schätzer erhält keine Wahrheit.
- `ui.js`, `style.css`, `web.html`: Oberfläche; `build.py` erzeugt die
  einzelne Datei `app/proper-time.html` ohne externe Abhängigkeiten.
- `create_notebook.py`: nachvollziehbare Erstellung des eigenständigen Notebooks.
- `verify.py`: JavaScript gegen die bestehende Python-Referenz, Grenzfälle,
  Geometrie-/Relationszähler, Kettenkontrollen, gültige Notebook-Struktur
  und optional ein echter Jupyter-Kernel-Lauf aller Codezellen.
- `browser_test.cjs`: Bedienung, reproduzierbare Seeds, mobile Breiten,
  JSON-Export, Notebook-Link und Offline-HTML; Screenshots in den CI-Artefakten.

Vom Repository-Stamm:

```sh
python -m pip install -r research/lorentz_proper_time_lab/requirements.txt
python research/lorentz_proper_time_lab/build.py --check
python research/lorentz_proper_time_lab/verify.py --execute
```

Zum Neuaufbau der gespeicherten Notebook-Ausgaben:

```sh
python research/lorentz_proper_time_lab/create_notebook.py
python research/lorentz_proper_time_lab/verify.py --save-notebook
```

`--in-process` führt bei gesperrten lokalen Sockets die gewöhnlichen Python-Zellen
direkt aus; dieser Modus wird ausdrücklich getrennt vom Jupyter-Kernel-Lauf
berichtet. Die gespeicherten Ausgaben wurden so lokal erzeugt; CI führt
dieselben Zellen zusätzlich mit einem echten Jupyter-Kernel aus.
Python nutzt NumPy-PCG64 mit getrennten SeedSequence-Streams; der Browser
Mulberry32 mit separat abgeleitetem Wiederholungsseed. Gleiche Seed-Zahlen
sind **keine** Zusage identischer Wolken zwischen den Sprachen. Die
numerische Gegenprüfung vergleicht identische Zählwerte und gespeicherte
Koordinaten. Endliche Pseudozufallszahlen und float64 approximieren das
kontinuierliche Modell. Numerische Toleranz der JavaScript-Gegenprüfung:
2·10⁻¹⁰ bei T=1; kein formal verifizierter Rundungsfehlerbeweis.

Die ursprüngliche Referenz und ihre Ergebnisarchive bleiben unverändert.
Ein erfolgreicher Softwaretest ist keine unabhängige wissenschaftliche Replikation.

## Quellen

- [X6: Gültigkeitsvertrag und Python-Referenz, Commit abf1423](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/abf1423c985606f5c514ea1bfd2aa48a260ad2bf/research/lorentz_proper_time_domain).
- [NIST: Exact binomial confidence limits](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbici.htm).
- [SciPy: binomtest und exakte proportion_ci](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html).

English: This German-language notebook and browser demonstrator explain the
existing fixed-budget proper-time reference. They assume a known flat model,
uniform independent sampling, known dimension and an external time scale.
They do not add a curvature detector or an anytime-valid inference claim.

Code licence: Apache-2.0.

## Weiterführend: Eigenzeit v0.2

Die [Gültigkeitskarte und Budgettabelle](../lorentz_proper_time_validity/RESULTS.md)
prüfen bekannte Krümmung, Dichteänderungen und fehlende Beobachtungen.
Vorab begrenzte Dichteunsicherheit ermöglicht konservativere Intervalle
im flachen Modell. Diese Erweiterung ist separat dokumentiert; der
Browser-Demonstrator verwendet weiterhin seine ursprünglichen festen
Stichproben und uniformen flachen Modellannahmen.
