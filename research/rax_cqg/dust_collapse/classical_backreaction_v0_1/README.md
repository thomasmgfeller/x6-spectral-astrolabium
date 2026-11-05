# CST Staubball: Klassik und gravitative Rückwirkung v0.1

Die reduzierte Einstein-Staub-Referenz reproduziert den klassischen Kollaps und seine Massenabhängigkeit. Der normierte Quantenkern besitzt im geprüften Fenster den passenden semiklassischen Grenzfall. Die Ableitung dieses Verhaltens aus einer vollständigen 4D-Kausalset-Summe bleibt **HOLD**.

## Physikalischer Vertrag

Es gilt c=1, Signatur (-+++), Lambda=0, irrotationaler druckloser Staub. Die homogene Reduktion benutzt eine räumlich flache periodische Zelle mit V=V0 a^3, q=sqrt(V), kappa=3 pi G/2. Sie beschreibt weder den Rand eines Staubballs noch dessen Außenraum. Die Einstein-Hilbert-Wirkung, Staubwirkung und der nötige metrische Randterm werden vor Einsetzen der Zwangsbedingungen variiert.

- Staubfluss: u^a u_a=-1, div(rho u)=0, geodätische Bewegung.
- Quellgleichung: G_ab=8 pi G rho u_a u_b.
- Reduzierter Zwang: p_T-kappa p_q^2=0, M=p_T>0.
- Staubzeit-Hamiltonian: H=-kappa p_q^2, q(T)=q_i-2 sqrt(kappa M)(T-T_i).
- Daraus: H_a^2=8 pi G rho/3, a_ddot/a=-4 pi G rho/3, rho=M/V.

Das Maß dq=dV/(2 sqrt(V)) allein erzwingt diese Wirkung oder ihre physikalische Herkunft nicht. Die Quantenreferenz benutzt die vorher festgelegte direkte q-Quantisierung und Dirichlet-Randbedingung bei q=0.

## Ausgeführt

1. Exakte rationale erste Variation der diskreten reduzierten Wirkung auf einem ungleichmäßigen Zeitgitter, drei Massen, lokale quadratische Variationskontrolle.
2. Unabhängige RK4-Integration der Beschleunigungsgleichung in a, drei Massen und 20/40/80 Schritte, Vergleich mit analytischer q-Bewegung und Zwangserhaltung.
3. 90 Spektralauswertungen: drei zentrale Massen, drei hbar-Werte, fünf Zeiten, zwei Ortsgitter. Vergleich mit der unabhängigen exakten Halbgeraden-Bildlösung, Norm, Masse- und Volumenmomenten. Das Vergleichsfenster bleibt mindestens zehn Paketbreiten vom Rand entfernt.
4. Audit der unveränderten 27 Entwicklungs- und 17 Prüfpfade. Ihre frühen Werte implizieren T*=1.4061817645901094, während die positive Pfadfamilie bis T=1.6 reicht. Kein vollständiger klassischer Vergleich über dieses ganze Fenster ist zulässig. Einzelne nichtstationäre Pfade sind kein Ausschlusssatz für ein Quantenpfadintegral.
5. Unabhängige Gleitkomma-Gegenrechnung der archivierten Massenantwort von Randfamilie C unter drei Maßen, drei Massen und voller, gravitationsphasenfreier bzw. massenblinder Kontrolle. Vergleich mit archivierten Intervallmittelpunkten; die alte Intervallzertifizierung wird nicht neu durchgeführt.

## Zustands- und Einheitenhinweise

Die numerische Referenz setzt dimensionslos kappa=1, V0=1, q0=4. M in den Testtabellen bezeichnet die **zentrale klassische Masse**. Für sigma_q^2=hbar/2 ist der Erwartungswert der Quantenmasse M+hbar/2 bis auf exponentiell kleine Bildkorrekturen. Diese lokalisierten Zustände haben eine endliche Massenstreuung, die im betrachteten semiklassischen Grenzfall verschwindet. Die hbar-Reihe ist kein neuer physikalischer Kopplungsscan.

Die Anfangszwangsgleichung verbindet Masse und Gravitationsimpuls. Vierfache Masse bei gleichem Anfangsvolumen erfordert den doppelten Betrag von q_dot. Die Masse bei unverändertem Gravitationsimpuls zu ändern wäre im flachen Referenzmodell keine zulässige Anfangsdatenvariation.

Die C-Kontrolle `g_zero` entfernt einen Gravitationsphasenfaktor. Sie ist **nicht** der Grenzfall G->0, denn der physikalische BD-Koeffizient skaliert bei festem ell und hbar wie 1/G. Massenabhängige Endamplituden beweisen ohne kalibrierte mehrzeitige Volumina und konsistenten gekoppelten Kern keine gravitative Rückwirkung.

## Reproduktion

```sh
python3 verify.py
python3 plot.py
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=results report.tex
```

`verify.py` benötigt NumPy und SciPy; `plot.py` zusätzlich Matplotlib. Die Tests liefen mit Python 3.12.14, NumPy 2.3.5 und SciPy 1.17.0; die tatsächlich gemeldeten Versionen stehen in `results/verification.json`. Die Verwendung neuerer kompatibler Versionen kann letzte Gleitkommastellen ändern. `report.tex` benötigt eine LaTeX-Installation. Der Prüflauf erzeugt die JSON- und CSV-Dateien in `results/` neu. Ergebnisse sind numerische Diagnostik, keine neuen Intervallzertifikate.

`plan.json` ist eine vor dem neuen Lauf fixierte lokale Spezifikation, keine externe Präregistrierung. Der Plan enthält den Ausgangsstatus; die ausgeführten Entscheidungen stehen in `results/verification.json`. `PLAN_SHA256` schützt den Plan, `provenance.json` schützt die kopierten Quelldateien und verzeichnet den geprüften Main-Commit. `SHA256SUMS` enthält die ausgelieferten Dateien ohne sich selbst.

## Entscheidung

| Teilprüfung | Status |
|---|---|
| G4-REF: klassische und semiklassische reduzierte Referenz | PASS, unter angegebenen Voraussetzungen |
| Massenantwort derselben gekoppelten Referenz | PASS, unter angegebenen Voraussetzungen |
| G4-CST: Herleitung aus der vollständigen diskreten Summe | HOLD |
| Einstein-Staub-Rückwirkung aus den vorhandenen CST-Endamplituden | HOLD |
| Neue Bounce-Prüfung | NOT_RUN |
| Singularitätsauflösung | Nicht nachgewiesen |

Die vorgängige Entscheidung `CLOSED_REJECTED_FOR_DOMINANT_BOUNCE` wird nicht verändert. Es wurden keine neuen CST-Geometrien, neuen Sprinkling-Daten oder kostenpflichtigen Rechenläufe erzeugt. Der Bericht legt die noch erforderliche Verbindung zum dynamischen CST-Kern ausdrücklich offen.

## Quellen

- Brown/Kuchař, *Dust as a Standard of Space and Time in Canonical Quantum Gravity*: https://arxiv.org/abs/gr-qc/9409001
- Benincasa/Dowker, *The Scalar Curvature of a Causal Set*, korrigierte Fassung v4: https://arxiv.org/abs/1001.2725
- Historiengewichtung: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/235
- Zwei-Massen-Test Randfamilie C: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/214

Die Testimplementierung und die homogene Ableitung sind Teil dieses Arbeitsdokuments. Es wird keine zusätzliche Literaturbehauptung über eine bewiesene allgemeine CST-Klassik oder eine Singularitätsauflösung erhoben.
