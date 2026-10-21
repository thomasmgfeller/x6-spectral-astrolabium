# Begrenzte Eigenzeit-Qualifikation V1b, Version 2

**Ergebnis: PASS im festgelegten Bereich — 52/52 Prüfungen bestanden.**
Der einmalige Versuch umfasst 24.576 neue native Wolken mit insgesamt
**100.663.296 Punkten**. Beide absichtlich fehlerhaften Kontrollen wurden erkannt.
Der historische V1b-Status bleibt **NOT_PASSED**, Phase 3 bleibt **HOLD_PHASE3**.

## Die drei ausgeführten Schritte

1. **Fehlergrenzen abgeleitet.** Das bestehende 10%-Eigenzeitziel wird in
   eine direkte Überdeckungs-/Präzisionsforderung und eine vorab gewählte
   2%-Reserve für den Skalenbias des mittleren Zählanteils übersetzt.
   [Vollständige Ableitung und Quellen](DERIVATION.md).
2. **Versuch vor neuen Daten veröffentlicht.**
   [Commit fbb7cdf](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/fbb7cdf01aa0787e9e2d95d05451177bcee88b31)
   vom 21.10.2026, 07:29:00 UTC enthält
   [Protokoll](protocol.json), [analytische Budgetplanung](planning.json),
   [Seeds](seeds.json), Erfassung und Auswertung.
   [Quellbindung](freeze.json): keine Änderung dieser Dateien nach dem Einfrieren.
3. **Einmalig ausgeführt und entschieden.** Datenerzeugung ab
   07:29:35.806 UTC, Laufzeit 233,363 Sekunden, ohne zusätzliche Seeds,
   Ersatzwolken oder Schwellenänderungen.
   [Maschinenlesbare Entscheidung](results/decision.json),
   [Rohbeobachtungen](results/raw/manifest.json),
   [erfolgreiche erneute Auswertung derselben Daten](results/verification.json).

## Was genau bestanden ist

Die neue Referenzfunktion [`qualifiedInterval`](qualified.cjs) erweitert das
native Intervall [L,U] zu [L/1,02; U/0,98]. Ihr harmonischer Mittelpunkt ist
die hier geprüfte Eigenzeitausgabe. Der Nachweis gilt für:

- bekannte flache Minkowski-Geometrie, zentrale innere Diamanten, T=1;
- d∈{2,3,4}, **genau m=4096**, **genau θ∈{0,4;0,7}**;
- unabhängig gleichverteilt aus der vorab definierten Population gezogene
  32-Bit-Startseeds; diese Eigenschaft der Betriebssystemquelle ist eine Annahme;
- keine Unabhängigkeitsannahme für Punkte innerhalb einer Wolke.

Die vorhandene Browserfunktion und deren Intervall bleiben unverändert.
Dieses PASS qualifiziert die neue Referenzfunktion in den sechs geprüften
Zellen. Es ist keine pauschale Freigabe aller Browserparameter oder aller Seeds.

Alle 52 Konfidenzaussagen sind mit Bonferroni auf ein gemeinsames
Fehlerniveau von 5 % abgesichert. Die folgende Untergrenze betrifft die
Wahrscheinlichkeit, dass das Intervall die Wahrheit überdeckt **und** einen
relativen Präzisionsradius ≤10 % hat. Damit liegt der harmonische Mittelpunkt
auch innerhalb von 10 % der wahren Eigenzeit. Gefordert waren mindestens 90 %.
Die gesonderte Mindestüberdeckung von 95 % ist ebenfalls in allen Zellen erfüllt.

| Dimension | θ | Konfidenzbereich des Skalenbias im mittleren Zählanteil | Gemeinsame Erfolgswahrscheinlichkeit, Untergrenze | Ergebnis |
|---|---:|---:|---:|---|
| 2 | 0,4 | −0,2033 % bis +0,4011 % | 99,5687 % | PASS |
| 2 | 0,7 | −0,1213 % bis +0,1104 % | 99,9067 % | PASS |
| 3 | 0,4 | −0,1569 % bis +0,6871 % | 99,5185 % | PASS |
| 3 | 0,7 | −0,0885 % bis +0,1266 % | 99,9067 % | PASS |
| 4 | 0,4 | −0,2074 % bis +1,1505 % | 99,3571 % | PASS |
| 4 | 0,7 | −0,0860 % bis +0,1313 % | 99,9067 % | PASS |

Die Biasgrenzen sind nach außen gerundet; die Erfolgsuntergrenzen abgerundet.
Die Biasforderung war ±2 %. Sie bezieht sich auf
`(E_seed[K/m] / θ^d)^(1/d) − 1`, nicht auf den endlichen Schätzerbias.
Letzterer steht separat im vollständigen Ergebnisbericht.

## Ergebnis zur radialen 4D-Auffälligkeit

Die drei neuen, vorab festgelegten radialen CDF-Prüfungen sind bestanden.
Die Konfidenzbereiche für die Abweichung vom idealen CDF-Wert liegen an
allen drei Sonden innerhalb von **±0,137 Prozentpunkten**; erlaubt waren
±0,5 Prozentpunkte. Das sind Grenzen an diesen Sonden, keine globale KS-Grenze.

| Radiale CDF-Schwelle | Beobachteter Anteil | Abgesicherte Abweichung in Prozentpunkten | Ergebnis |
|---:|---:|---:|---|
| 0,25 | 0,2499458194 | −0,0852 bis +0,1252 | PASS |
| 0,50 | 0,4999343753 | −0,1198 bis +0,1066 | PASS |
| 0,75 | 0,7499294579 | −0,1369 bis +0,0719 | PASS |

Zusammen mit der [vorherigen Ursachenlokalisierung](../v1b_radial_audit/README.md)
ergibt das einen neuen, begrenzten Nutzbarkeitsnachweis. Die alte
Vier-Seed-KS-Prüfung mit p=0,0110616450 wird nicht umgedeutet, entfernt oder
durch eine nachträglich angepasste Schwelle bestanden erklärt. Der
Sampler ist unverändert. Ein bestimmter Mechanismus für den historischen
Ausschlag oder globale Gleichverteilung ist damit nicht bewiesen.

## Kontrollen, technische Prüfung und ausgeschlossener Bereich

- Falsche Radiuspotenz: mindestens eine radiale Prüfung erkennt den Fehler.
- Wiederholter Einzelpunkt: beide 4D-Überdeckungsprüfungen erkennen die
  unbrauchbare Wolkenabhängigkeit.
- Alle nativen Punkte liegen strikt im äußeren Diamanten; keine Verwerfungen
  oder Nullradien traten auf. Größter Transformationsfehler:
  7,55·10⁻¹⁴, unter der festen Grenze 10⁻¹².
- Native Intervalle und unabhängige SciPy-Berechnung stimmen bis
  7,85·10⁻¹³ überein; feste Toleranz 2·10⁻¹⁰.
- Die [bekannten Seed-Fixtures](results/fixtures/manifest.json) prüfen vor dem
  Versuch volle Koordinaten und Zählungen gegen `cloud()`.
- Die früheren 88 Radial-Archivprüfsummen und Originalquellen wurden erneut
  ohne Änderung geprüft. Vorhandene Browser-/Export-Evidenz bleibt gültig.

Die zusätzlich protokollierten θ=0,1 und θ=0,2 sind ausdrücklich nicht
qualifiziert. Bei θ=0,1 erreicht keine beobachtete Wolke den 10%-Präzisionsradius.
Bei θ=0,2 erreichen ihn in 2D 87,22 %, in 3D und 4D 0 %. Das feste Budget
genügt dort nicht für das 90%-Ziel. Keine Freigabe anderer m-Werte,
verschobener/boosted Intervalle, adaptiver Messungen, unbekannter Skala oder
Dimension, gekrümmter Raumzeit oder physikalischer Eigenzeitmessung.

## Reproduzierbare Prüfung

```sh
python -m pip install -r research/lorentz_proper_time_lab/v1b_boundary/requirements.txt
python research/lorentz_proper_time_lab/v1b_qualification_v2/verify.py
```

Die [CI](../../../.github/workflows/lorentz-v1b-qualification.yml) prüft den
öffentlichen Vorab-Commit, alle eingefrorenen Quellen, die archivierten
Wolkenbeobachtungen und die vollständige Entscheidung. Sie wiederholt keine
neue statistische Stichprobe. Gleitkomma-Abweichungen beim Replay sind bis
1e−12 absolut plus 1e−12 relativ zulässig; Entscheidungen und Zählungen müssen
exakt übereinstimmen.

Archiviert sind alle Wolkenstatistiken und die Hashes der geordneten
Koordinaten, nicht alle 100,7 Millionen Koordinaten als Dateien.
[SHA-256-Inventar](results/SHA256SUMS). Code: Apache-2.0.
