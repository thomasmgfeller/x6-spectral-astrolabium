# Wolfram-Gegenprüfung: Polaritätsumkehr (Referenzfall 2)

**Ausgeführt: PASS_WITH_SCOPE_LIMITS.** Wolfram und der veröffentlichte
X6-Kern bestätigen den festgelegten synthetischen Gegenbeispielfall.
Das invertierte Signal wird von X6 korrekt als `FAIL` zurückgewiesen;
die Gegenprüfung dieses Verhaltens ist bestanden.

## Freigegebene Dateien

- [Prüfbericht](PRUEFBERICHT_DE.txt)
- [Vollständiges Reproduktionspaket](X6_Wolfram_Fall2_v0_1.zip)
- [Veröffentlichungsnachweis und Prüfsummen](PUBLICATION.json)

Das ZIP wird bytegleich zur freigegebenen Fassung veröffentlicht.
SHA-256: `20781540c209de9f9c85835b02737c8e0b29961791279f543ac53ebf08393951`.
Der separat lesbare Bericht ist bytegleich aus diesem Paket übernommen.

## Eingabe und Ergebnis

Referenz: `x[n] = cos(2*pi*n/128)`, `n=0,...,127`, Abtastrate 128 Hz.
Der Hauptfall ist `y=-x`; zusätzliche Kontrollen sind `y=x` und `y=0`.
Kein Rauschen und keine Zufallsstichprobe.

| Kennzahl für y=-x | Sollwert | Wolfram | X6 |
| --- | ---: | ---: | ---: |
| Relativer Welch-PSD-Fehler | 0 | 0 | 0 |
| Betragsquadratische Kohärenz | 1 | 1 | 1 |
| Gewichteter RMS-Phasenfehler | 180 Grad | 180 Grad | 180 Grad |
| Normierter Rekonstruktionsfehler | 2 | 2 | 2 |

Vier symbolische Identitäten und zwölf numerische Sollwertprüfungen wurden
bestätigt. Der separate X6-Abgleich umfasst zwölf Kennzahlvergleiche und
die vollständigen Hauptfall-Spektren samt Auswertbarkeitsmasken.
Die maximale absolute PSD/CSD-Abweichung beträgt
`9.540979117872439e-18`, die Kohärenzabweichung
`4.440892098500626e-16`. Alle liegen innerhalb der festgehaltenen Toleranzen.

Die Identitätskontrolle wird in dieser Konfiguration als `PASS` bewertet;
die Nullausgabe wird als `FAIL` bewertet und erhält ausdrücklich
undefinierte Kohärenz und Phase.

## Methodik und dokumentierte Korrektur

Wolfram Language 15.0.1 unter Linux x86-64, nominelle Arbeitspräzision
80 Stellen; Node.js v24.19.0 mit unveränderter X6-Quelle aus Commit
`90b74509f2b65de08a77de8a7057204834951fc2`.
Welch: drei überlappende Segmente mit je 64 Werten, Schrittweite 32,
periodisches Hann-Fenster und Mittelwertabzug pro Segment.

Der erste Wolfram-Lauf bestätigte den Hauptfall, scheiterte aber an der
strengen Präzisionstoleranz der zusätzlichen Nullkontrolle: Wolfram
transformierte den exakten ganzzahligen Nullvektor mit Maschinenpräzision.
Der Prüfadapter bildet diesen Sonderfall in der zweiten Fassung exakt ab.
Eingaben, Sollwerte, Toleranzen und X6-Quelle blieben unverändert.
Beide Programme, Rohantworten und die Korrektur sind im Paket erhalten.
Die Anpassung erfolgte nach Einsicht in den ersten Lauf; sie ist keine
blinde Prüfung.

## Nachprüfung

Nach dem Entpacken in das Verzeichnis `X6_Wolfram_Fall2_v0_1` wechseln:

```sh
python verify.py
python verify.py --rerun
```

Der erste Befehl prüft gespeicherte Belege und Dateiintegrität.
Der zweite führt zusätzlich X6 mit Node.js neu aus.
**Keiner der beiden Befehle führt Wolfram erneut aus.**
Für eine neue Wolfram-Auswertung ist `wolfram_check_v0_1_1.wl` vorgesehen.
Python benötigt nur die Standardbibliothek; der frische X6-Lauf zusätzlich Node.js.

## Aussage und Grenzen

Identische Leistungsspektren und Kohärenz 1 garantieren keine vorzeichen-
und phasentreue Rekonstruktion. Der Test bestätigt diese konkrete
Recheneigenschaft und ihre korrekte Behandlung im ausgewählten X6-Stand.
Er belegt keine allgemeine Filterüberlegenheit oder reale Geräteleistung.

Die Welch-Segmente sind keine unabhängigen Versuche. Es werden weder
Kohärenz-Konfidenzintervalle noch Quantenkohärenz oder Hardwareabnahmen
abgeleitet. Die getrennte Implementierung verwendet einen anderen
Rechenkern; Testentwurf und Auswertung stammen von derselben Assistenz.
Keine externe personelle Begutachtung oder Zertifizierung durch Wolfram Research.

Die Sollwerte und bestehende X6-Tests waren vor dem Auftrag bekannt.
Der festgehaltene Prüfvertrag ist keine Vorregistrierung einer neuen Entdeckung.
Prüfsummen belegen Inhaltsintegrität; lokale Zeitprotokolle sind keine
extern beglaubigten Zeitstempel.

Siehe [Signal Validation Lab](../../SIGNAL_VALIDATION_LAB.md).
Originale Projektbeiträge unter [Apache-2.0](../../../LICENSE), gemäss
[Lizenzumfang](../../../LICENSE_SCOPE.md). Das ZIP enthält die übernommenen
X6-Lizenzhinweise und keine Wolfram-Software.
