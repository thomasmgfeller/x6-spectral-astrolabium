# X6-QE v0.1 — Spektrale Unterscheidbarkeit und relationale Struktur

**Exakte endliche Referenzrechnungen, keine neue Quantenphysik.** Vier Graphen
bilden drei bekannte Referenzfälle. Der Beitrag ist die ausführbare Gegenprüfung
und Integration in X6; mathematische Neuheit wird nicht beansprucht.

| Referenz | Festes Ergebnis | Aussagegrenze |
| --- | --- | --- |
| Stern K1,6 | chi_A(t)=t^5(t^2−6), Z(u)^−1=1 | Ein reiner Stern hat keinen nichttrivialen gewöhnlichen Ihara-Zyklusfingerprint. |
| Viererzyklus C4 | chi_A(t)=t^2(t^2−4), Z(u)^−1=(1−u^4)^2 | Ein primitiver Zyklus darf zusammengesetzte Länge haben. Die zwei Orientierungen werden getrennt gezählt. |
| 4×4-Turmgraph / Shrikhande | Beide: Spektrum 6^1, 2^6, (−2)^9; gleiche globale Ihara-Zeta; K4-Anzahlen 8 / 0 | Lokale kombinatorische Information kann gleiche vollständige Spektren und globale Zeta-Funktionen unterscheiden. Keine Aussage über Persistenz, Transport oder Quantengedächtnis. |

## Ausführen

Python **3.12**, nur Standardbibliothek. Aus dem Repository-Hauptverzeichnis:

```sh
python3 -S -B research/x6_qe/verify.py --output /tmp/x6-qe.json
python3 -S -B research/x6_qe/verify.py --verify-report /tmp/x6-qe.json
```

Erwartet: `PASS_WITH_SCOPE_LIMITS`, drei Referenzfälle, vier Graphen, zwölf
Umbenennungen und **21 zurückgewiesene Fehlerfälle**, Exit 0. Der Ausgabeweg muss
neu sein. Fehler ergeben Exit 1; falsche CLI-Argumente Exit 2. Alle Koeffizienten
sind exakte ganze Zahlen; es gibt keine numerische Toleranz, Downloads oder neuen
Wolfram-Aufrufe. Die [gespeicherte Evidenz](evidence/local-results.json) ist durch
den zweiten Befehl mit passender Quellenrevision vollständig nachrechenbar.

Der gemeinsame Einstieg enthält den Bericht `qe-graphs.json`:

```sh
python3 -S -B x6.py reference qualify --output /tmp/x6-reference-evidence
```

Für die ganze Suite wird zusätzlich Node.js 24 benötigt. Ihre zehn Berichte
enthalten weiterhin die bestehenden Lorentz- und Wolfram-Fälle. Siehe
[Offline-Anleitung](../../docs/OFFLINE_REFERENCE.md) und [Abnahme](ACCEPTANCE.md).

## Was die Gegenprüfung unabhängig macht — und was nicht

`core.py` berechnet charakteristische Polynome über Faddeev–LeVerrier. Für die
Ihara-Zeta wird die Matrix der gerichteten, nicht unmittelbar zurücklaufenden
Kantenübergänge vollständig verwendet. `independent.py` importiert diesen Kern
nicht: Sie rekonstruiert die vier Graphen aus ihren Definitionen, prüft die
Polynome durch Bareiss-Determinanten an genügend verschiedenen ganzzahligen
Punkten und gegen geschlossene Referenzformeln. Die gesamte Ihara-Bass-Identität
wird ebenfalls über eine ausreichende Anzahl exakter Auswertungspunkte geprüft.
K4 wird einmal durch Vierermengen, einmal durch Dreiecksspuren in Nachbarschaften
gezählt. Die beiden regulären Graphen erfüllen zusätzlich A²=4I+2J.

Diese Wege sind algebraisch verschieden. Sie teilen Konventionen, Python und
den vertrauenswürdigen Checkout; **externe personelle Wiederholung ist
NOT_PERFORMED**. Drei festgelegte Umbenennungen je Graph sind keine vollständige
Prüfung aller 16! Beschriftungen. Die nichtzurücklaufenden Matrizen werden dabei
auf exakte Permutationskonjugation geprüft.

Der Verifikator rechnet aus den vertrauenswürdigen Quellen neu. Ein Ergebnisordner
liefert keinen ausführbaren Code. Vollständige kanonische JSON-Ausgaben werden
verglichen; `false` ist nicht `0`. Fehlende Graphen, falsche Polynome oder
Motivzahlen, erfundene Quantenclaims und nachgezogene Ergebnisprüfsummen scheitern.
Hashes belegen Quellenbindung, keine Urheberschaft oder externe Begutachtung.

## Forschungsstatus

Der [Vertrag](contract.json) wurde nach Kenntnis dieser Referenzen formuliert;
er ist keine Präregistrierung einer Entdeckung. [Spezifikation](SPECIFICATION.md),
[Quellen](BIBLIOGRAPHY.md) und [weitere Abnahmen](ROADMAP.md) definieren die Grenzen.
Der Ursprung der visuellen Spider-Beobachtung bleibt ungeklärt. Ein Billiard-Solver,
topologisches Gedächtnis und arithmetische Residuen werden hier nicht validiert.
Die Lorentz-Priorität bleibt bestehen; die Verbindung ist methodisch, kein
Nachweis einer physikalischen Gleichsetzung der Operatoren.

Originalcode und Originaldokumentation: Apache-2.0 gemäß Repository-Lizenz.
Graphen werden aus mathematischen Definitionen konstruiert; keine fremde
Graphendatenbank oder fremder Quellcode wird übernommen.
