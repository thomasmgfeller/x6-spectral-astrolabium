# Gemeinsamer minimaler Skalarwirkungsansatz v0.1

**Schritt 1:** Ein expliziter Kandidat für Geometrie, den bestehenden
wirbelfreien Staub und ein zusätzliches reelles Skalarfeld.

Modell-ID: `CST-DUST-KG-MIN-v0.1`. Datum: 11. November 2026.
Anschluss: [PR 278](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/278),
Commit `4fed3a2fd0c5050af8e5b6dab6e6311fe7f4fd83`.

## Ergebnis

Für den deklarierten Kandidaten sind Feldinhalt, Einheiten, endliche Wirkung,
Hesse-Matrix, skalare Randreaktion und klassische Zielgleichungen explizit
ausgearbeitet. Das zusätzliche Feld ist **nicht** die Staubuhr und keine
unkonditionierte Staubuhrstörung. Es koppelt über die gemeinsame Geometrie;
eine direkte Staub-Skalar-Kopplung wird auf null gesetzt.

Der Bericht `CST_DUST_Gemeinsamer_Skalarwirkungsansatz_v0_1.pdf` enthält die
Herleitung, ihre Voraussetzungen und Primärquellen. `report.tex` ist die
vollständige editierbare Quelle. Der maschinenlesbare Vertrag steht in
`action_contract.json`.

Die 33 abgedeckten AA-Kontrollhistorien besitzen bei festem `ell > 0` und
`mu^2 >= 0` einen invertierbaren inneren Skalarblock:

    H_II = -v * (a*(p+q)/2 + mu^2)
    abs(H_II) >= v*(a + mu^2) > 0
    a = 4/(sqrt(6)*ell^2), v = ell^4

Das ist ein endliches algebraisches Resultat. Die Schranke ist **nicht**
gleichmäßig im Kontinuumsgrenzwert `ell -> 0`. Sie gilt auch nicht für
beliebige Kettenränder. Die Fünferkette liefert das enthaltene Gegenbeispiel.

## Reproduktion

Python 3.10 oder neuer und die in `requirements.txt` angegebene SymPy-Version
genügen. Die Kontrollfamilien sind klein; keine Produktionssimulation,
kein Cloudkonto und kein externer Datendownload werden benötigt.

```bash
python -m pip install -r requirements.txt
python verify.py
```

`verify.py` prüft den Paketinhalt und die mitgeführten Repository-Eingaben
gegen ihre Hashwerte, führt die 25 exakten Tests aus und vergleicht beide
neu erzeugten Ergebnisdateien bytegenau mit den ausgelieferten Dateien.
Es greift nicht auf das Netzwerk zu und verändert die Referenzergebnisse nicht.

Für eine bewusste Neuberechnung der Resultate:

```bash
python build_evidence.py
```

Für die PDF-Erzeugung in einer regulären TeX-Live-Installation mit
Latin Modern, Babel, AMS, booktabs, geometry, hyperref, fancyhdr und microtype:

```bash
pdflatex -interaction=nonstopmode -halt-on-error report.tex
pdflatex -interaction=nonstopmode -halt-on-error report.tex
```

Die PDF-Metadaten können sich zwischen TeX-Builds ändern; eine byteidentische
PDF-Neuerzeugung ist nicht Teil des Reproduktionsversprechens. Für ein neues
Release die resultierende `report.pdf` unter den oben genannten PDF-Namen
kopieren und erst danach `python package.py` ausführen. Der Paketbau setzt
die Prüfsummen auf den aktuellen Inhalt; er ist **kein** Ersatz für die
vorherige Prüfung eines empfangenen Pakets mit `verify.py`.

## Dateien und Konventionen

- `model.py`: unabhängige Produkt- und Inzidenzform der skalaren Wirkung.
- `test_model.py`: 25 exakte algebraische und klassische Zielkontrollen.
- `results/checks.json`: Testumfang und wissenschaftliche Aussagegrenzen.
- `results/aa_hessians.json`: 33 rationale masselose Matrizen `H0`;
  physikalische Skalierung `H = v*a*(H0 - u*I5)`, `u = mu^2/a`.
- `provenance.json`: Repository-Pfade, Commit, Git-Blob- und SHA-256-Werte.
- `inputs/`: unveränderte benötigte Eingaben des bisherigen Programms.
- `MANIFEST.sha256.json`: Hashwerte des ausgelieferten Paketinhalts.
- `environment.json`: Umgebung der ausgeführten Kontrollen.

Elementreihenfolge: `(0,1,2,3,4)`, inneres Element `2`.
Gaußadapter: `(0,1,3,4,2)` = Eingang, Ausgang, Inneres.
Die vorherige achtgliedrige Zustandsbasis bleibt **Strata zuerst**, mit
Zeilen ausgehend und Spalten eingehend. Carrier-Namen nennen Eingang vor Ausgang.
Die neue Fünfer-Hesse-Matrix ist keine physikalische 8x8-Übergangsmatrix.

## Aussagegrenzen

Minimalität, `xi=0`, fehlende Selbstwechselwirkung und fehlende direkte
Staub-Skalar-Kopplung sind deklarierte Modellentscheidungen. Andere endliche
Wirkungen mit demselben führenden klassischen Zielgrenzfall sind möglich.
Die physikalische gravitative Randwirkung bleibt unbestimmt; der übernommene
Kontrollwert null ist kein hergeleitetes Junction-Gesetz.

Die klassische Zielwirkung liefert analytisch die Klein-Gordon-Gleichung,
Staubnorm, Staubkontinuität und den gemeinsamen Stresstensor. Dass die
diskrete gemeinsame Wirkung und ihre Variationen dorthin konvergieren,
ist **nicht bewiesen**. Physikalische Historiengewichte, Randzustände, Maße,
Regulatorgrenzwerte, Stabilität und Fehlerbudget sind weiterhin offen.

**Alle acht physikalischen Gates bleiben HOLD.** Die physikalische Materiematrix
ist `NOT_CONSTRUCTED`; `K_0plus` wurde nicht berechnet. Die 25 bestandenen
Tests sind kein Nachweis von Singularitätsauflösung oder Bounce.

Der nächste Anschluss ist der physikalische Rand- und Zustandsvertrag für
diesen ausdrücklich benannten Wirkungskandidaten.

## Lizenz und Quellen

Apache-2.0, siehe `LICENSE` und `NOTICE`. Die mitgeführten früheren Quellen
sind in `provenance.json` festgehalten. Externe Fachartikel werden zitiert,
nicht mitverteilt. Ihre Verwendung ist im PDF auf die jeweils benötigte
mathematische beziehungsweise klassische Aussage begrenzt.
