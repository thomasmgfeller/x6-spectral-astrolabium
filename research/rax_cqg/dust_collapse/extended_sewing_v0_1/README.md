# CST-DUST: Erweiterte Verklebungsregel v0.1

Der erweiterte Randvertrag rekonstruiert die gemeinsame Gravitation-, Staub- und Skalarwirkung aus serialisierten lokalen Paketen. Alle 1.089 minimalen transitiven Verklebungen der bisherigen 33 × 33 AA-Historien stimmen exakt mit der unabhängigen gemeinsamen Rechnung überein.

Die Schnittdaten enthalten die kausalen Fußabdrücke, nach Fußabdruck gruppierte Intervallzähler, frühere Uhr- und Feldvariablen sowie die späteren Dichten. Die bedingten Amplituden und ihre Korrelationen bleiben erhalten, bis die Kreuzwirkung eingefügt ist. Der zusätzliche Faktor lautet

`I_epsilon = 2 exp(i (Delta S - S_seam)/hbar) exp(-epsilon (q3^2+q4^2)/2)`.

Für das bekannte geschichtete Beispiel ergeben sich dieselben fünf Kreuzterme, `Delta F4=16`, `F4_joint=88`. Die zusätzliche Phase enthält `14*kappa`, weil die Schnittgravitation einmal abgezogen werden muss. Der Faktor zwei korrigiert das bisherige quotientierte Schnittmaß.

## Ausführen

Python 3.11 oder neuer; `sewing.py` braucht nur die Standardbibliothek. Aus dem Paketverzeichnis:

```bash
python sewing.py examples/left.json examples/right.json --fields examples/fields.json --output /tmp/joined.json
python -m pip install -r requirements.txt
python analysis.py
python -m unittest discover -s . -p 'test_*.py' -v
python verify.py
```

Die Rekonstruktion liest keine globale Ordnung. Lokale Relationstabellen werden zur unabhängigen Prüfung der gespeicherten Profile benutzt. Das Ausgabe-JSON liefert die gemeinsame Wirkung und die zusätzliche Schnittphase in exakten rationalen Koeffizienten von `kappa`, `1` und `beta=4/sqrt(6)`. Es ist kein numerischer Löser für beliebige Eingangs-Wellenfunktionen.

Mit zusätzlichem `--epsilon 1/7` wertet der CLI-Aufruf das Einflussfunktional an den gebundenen Feldern auch als komplexe Zahl aus. Diese optionale Ausgabe nutzt gewöhnliche Gleitkommaarithmetik; ihre Zahlen sind kein Arb-Zertifikat. Frühere Dichten bleiben im unverkleinerten Beispiel explizit als lokale Hilfsvariablen gebunden, obwohl die Kreuzwirkung sie nicht benötigt.

`analysis.py` erzeugt die globalen Ordnungen als unabhängige Referenz, vergleicht sämtliche Wirkungskoeffizienten und berechnet die vollständige 1.089er-Summe im explizit eingeschränkten Acht-Atom-/Gauß-Kontrollsektor mit Arb. Positive Dichtesektoren sind durch die exakte Wirkungsidentität abgedeckt, aber nicht zusätzlich numerisch integriert.

## Wissenschaftlicher Status

- **FINITE_EXTENDED_SEWING_PASS:** 1.089 exakte Wirkungsidentitäten; 2.178 zertifizierte Kontrollen der Integrationsreihenfolge bei positivem Regulator.
- 32 innere Skalarblöcke haben Rang drei. Alle Nullmoden koppeln an die Randfelder. Der Abel-Grenzwert ist deshalb auf dem deklarierten Schwartz-Testraum als Distribution definiert.
- Die 1.089er-Summe im Acht-Atom-/Grundpaketsektor beträgt im Abel-Grenzwert `-0.000069112936 + 0.000167149114 i`; Fehler je angezeigter Komponente kleiner als `1e-12`.
- Die minimale transitive Hülle ist eine ausdrückliche Abschlussregel. Zusätzliche globale Schnittumgehungen können dieselben lokalen Restriktionen haben und benötigen eigene Daten.
- **PHYSICAL_CST_EVOLUTION_NOT_CONSTRUCTED:** Keine neue L²-Evolution, Unitarität, allgemeine Junction-Dynamik oder Bounce-Vorhersage. Der frühere Definitionsbereichsbefund bleibt bestehen.

## Dateien und Reproduzierbarkeit

Die vollständige Herleitung und der Zustands-/Fehlerbegriff stehen in `DERIVATION.tex` und `CST_DUST_Erweiterte_Verklebungsregel_v0_1.pdf`. `contract.json` fixiert den Geltungsbereich. `examples/` enthält vollständige Eingangspakete, `results/` die rekonstruierte Wirkung, sämtliche Historienkennzahlen, Nullmoden und Arb-Intervalle.

`verify.py` prüft die sechs eingefrorenen Git-Blobs, das vollständige SHA-256-Manifest, zehn Testgruppen, einen CLI-Lauf und die byteidentische Neuberechnung aller JSON-Eingangsbeispiele und Ergebnisse. Der Bericht kann mit `python build_pdf.py` und einer vollständigen TeX-Live-Installation neu erstellt werden. Eine neu erstellte PDF kann je TeX-Version andere Dateihashes haben; die wissenschaftlichen JSON-Ergebnisse werden separat verglichen.

Quellbasis: `thomasmgfeller/x6-spectral-astrolabium`, Commit `efe19fca88a49d3d59de041652a60c26c180b8eb`. `provenance.json` benennt Pfade und Blob-IDs. `inputs/prior_gluing.py` ist eine eingefrorene Quelle und benötigt im Original weitere Nachbardateien; es ist kein Einstieg dieses Pakets.

Apache-2.0, siehe `LICENSE` und `NOTICE`.
