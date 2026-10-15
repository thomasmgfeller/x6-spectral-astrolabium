# Wolfram-Gegenprüfung: Null Fehler und Scheinreplikation (Referenzfall 4)

**Ausgeführt: PASS_WITH_SCOPE_LIMITS.** Der abschließende Wolfram-Lauf
besteht zwölf Prüfaussagen ohne Meldungen. Eine getrennte Python-Rechnung
bestätigt sieben Ergebnisgrößen innerhalb der absoluten Toleranz `1e-60`.
Geprüft werden konstruierte statistische Modelle; reale Projektdaten und
X6-Produktionsläufe wurden nicht untersucht.

## Freigegebene Dateien

- [Vollständiger Prüfbericht](PRUEFBERICHT_DE.txt)
- [Unverändertes Reproduktionspaket](X6_Wolfram_Fall4_v0_1.zip)
- [Veröffentlichungsnachweis und Prüfsummen](PUBLICATION.json)

SHA-256 des ZIP:
`7f4df01f65dec25a2165beea1dfe0b7e2a77b80effb28db14ed428df40eca4d7`.
Der separat lesbare Bericht ist bytegleich aus dem freigegebenen Paket übernommen.

## Ergebnis und Voraussetzungen

Bei null beobachteten Fehlern ist die exakte einseitige obere
95-%-Konfidenzgrenze für die Fehlerwahrscheinlichkeit
`u_n = 1 - (1/20)^(1/n)`.

| Modell | Gespeicherte Einträge | Unabhängige Versuche | Obere Grenze |
| --- | ---: | ---: | ---: |
| Unabhängige Bernoulli-Versuche mit gemeinsamem festem p | 20 | 20 | 13,91083406682652... % |
| Bekannte Kopien einer einzigen Bernoulli-Ziehung | 20 | 1 | 95 % |

Vorausgesetzt sind eine vorab festgelegte Stichprobengröße und
Fehlerdefinition sowie die vollständige Erfassung der Versuche.
Das Konfidenzniveau beschreibt die Deckungseigenschaft des Verfahrens;
es ist keine Posteriorwahrscheinlichkeit für den festen Parameter.

Die Negativkontrolle setzt den wahren Wert auf `p=1/5`. Im Kopiermodell
liefert eine fehlerfreie Ziehung mit Wahrscheinlichkeit `4/5` zwanzig
fehlerfreie Einträge. Wer daraus fälschlich zwanzig unabhängige Versuche
macht, schließt den wahren Wert aus. Nur bei der fehlerhaften Ziehung
(Wahrscheinlichkeit `1/5`) deckt sein Intervall den wahren Wert.
Die tatsächliche Deckung des falsch angewendeten Verfahrens beträgt
hier **20 %**. Das korrekt auf einen Versuch angewendete Verfahren deckt
bei diesem konkreten Parameter in 100 % der Fälle; dies ist keine
universelle 100-%-Deckungsgarantie.

## Reproduktion

ZIP vollständig entpacken und im Verzeichnis `X6_Wolfram_Fall4_v0_1` ausführen:

```sh
python3 verify.py
```

Das Skript benötigt nur die Python-Standardbibliothek. Es rechnet mit
`Decimal` bei Präzision 100 und mit exakten Brüchen, prüft die gespeicherten
Wolfram-Belege, beide Freeze-Dateien und das vollständige Dateimanifest.
**Es führt Wolfram nicht erneut aus und benötigt keinen Netzwerkzugriff.**
Für einen frischen Wolfram-Lauf liegt `wolfram_check_v0_1_1.wl` bei.

Der verwendete Wolfram-Kernel meldet Version 15.0.1 für Linux x86-64,
die angeforderte Dezimalpräzision beträgt 80. Zusätzlich zum
Zahlenvergleich beweist eine exakte rationale Einschließung die
entscheidende Wurzel in einem Intervall der Breite `1e-60`.

## Dokumentierte Korrektur

Der erste Wolfram-Lauf gab trotz wahrer Boolescher Prüfwerte eine
`N::meprec`-Warnung beim Vergleich von Beta-Quantil und Radikal aus.
Gemäß Prüfvertrag bleibt er **INCONCLUSIVE** und ist vollständig erhalten.
Im zweiten Lauf vergleicht `SameQ[RootReduce[a], RootReduce[b]]` die
exakten algebraischen Darstellungen. Modell, Sollwerte, zwölf Prüf-IDs,
Präzision und Toleranz blieben unverändert. Der zweite Lauf ist meldungsfrei.

Die Korrektur erfolgte nach Einsicht in den ersten Lauf.
Sollwerte und lokale Vorrechnung waren vor der Fixierung bekannt.
Die Freeze-Dateien sind keine Vorregistrierung einer Entdeckung und
keine extern beglaubigten Zeitstempel.

## Aussage und Grenzen

Kopieren erzeugt keine zusätzlichen unabhängigen Versuche.
Gleiche beobachtete Werte allein beweisen jedoch keine Abhängigkeit.
Dieser Referenzfall unterstellt ausdrücklich einen bekannten
Kopiermechanismus; er behauptet nicht, dass vorhandene Projektdaten Kopien sind.

Die Gegenrechnung verwendet einen anderen Rechenkern. Testentwurf und
Auswertung stammen von derselben Assistenz. Es liegen keine externe
personelle Begutachtung, Zertifizierung durch Wolfram Research oder
physikalische Validierung vor. Hashes prüfen Inhaltsintegrität.

Methodische Referenz:
[NIST: Exact Binomial](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbino.htm).
Weitere Funktionsreferenzen stehen im Prüfbericht.

Siehe [Signal Validation Lab](../../SIGNAL_VALIDATION_LAB.md).
Originale Projektbeiträge unter [Apache-2.0](../../../LICENSE), gemäß
[Lizenzumfang](../../../LICENSE_SCOPE.md). Externe Dokumentation und
Drittmaterial behalten ihre eigenen Rechte. Das Paket enthält keine
Wolfram-Software.

