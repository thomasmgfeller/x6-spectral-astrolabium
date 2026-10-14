# RAX-W1 - exakte Wolfram-Gegenprüfung v0.1

**Ausgeführt: PASS_WITH_SCOPE_LIMITS.** Alle 44 vorab ausgewählten endlichen
U1-Matrixfälle stimmen exakt mit dem veröffentlichten U1-Bericht und beiden
historischen Python-Rechenwegen überein. Zehn Fälle sind stark reduzierbar;
34 zeigen die erwartete Verletzung bei positiver Störstärke.

## Freigegebene Dateien

- [Prüfbericht (PDF, 4 Seiten)](RAX_W1_Exakte_Gegenpruefung_v0_1.pdf)
- [Vollständiges Reproduktionspaket (ZIP)](RAX_W1_Exakte_Gegenpruefung_v0_1_Paket.zip)
- [Veröffentlichungsnachweis und SHA-256-Prüfsummen](PUBLICATION.json)

PDF und ZIP werden bytegleich zur freigegebenen Fassung veröffentlicht. Das
Paket enthält die benötigten historischen U1-Dateien, den Prüfvertrag, sämtliche
Wolfram-Eingaben und -Antworten, den rationalen Abgleich, Gegenkontrollen,
Manipulationsprüfungen und ein vollständiges Dateiinventar.

## Umfang und Ergebnisse

| Prüfung | Ausgeführtes Ergebnis |
| --- | --- |
| Matrix- und Ergebnisabgleich | 44/44 exakte Übereinstimmungen einschliesslich der ursprünglichen Matrix-Hashes |
| Auswahl | 40 Matrizen mit 8 Zuständen; 4 mit 16 Zuständen; beide Familien A/B |
| Starke Reduktion zur vorgegebenen Partition | 10 gültig bei lambda=0; 34 erwartete Verletzungen bei lambda>0 |
| Transportierte Zustandsumbenennung | 44/44 Prüfungen bestanden |
| Mehrschrittidentität | 20/20 Prüfungen für t=2,3 in den Nullstörungsfällen bestanden |
| Verschobene, weiterhin reduzierbare Modelle | 10/10 Kontrollen: der alte Prädiktor hat Fehler 1/10 |
| Ungültige Matrizen | Falsche Zeilensumme und negative Wahrscheinlichkeit trotz Zeilensumme 1 erkannt |
| Symbolische Bedingungen | 7 Boolesche Aussagen bestätigt; konstanter Wechselprädiktor mit Minimax-Fehler 1/20 bei Prognose 2/5 |
| Manipulierte Prüfbelege | 8/8 Negativtests des Abgleichsprogramms bestanden |

Für die spezifizierte endliche Familie und die angegebenen Parametergrenzen
bestätigt Wolfram: starke Reduzierbarkeit genau bei lambda=0, maximale
Blockabweichung delta=2*lambda und maximaler Fehler des unveränderten
Wechselprädiktors gleich lambda. Passende gleichgewichtete Ein-Schritt-Mittelwerte
verdecken die Verletzung in allen 34 gestörten Auswahlfällen; sie beweisen keine
starke Reduktion oder unveränderte Mehrschrittdynamik.

Der Prüfvertrag wurde vor dem ersten Wolfram-Aufruf geschrieben und gehasht;
die veröffentlichten U1-Ergebnisse waren dabei bereits bekannt. Vier Aufrufe
wurden ausgeführt. Die erste gemeinsame Ausgabe der 44 Fälle wurde bei der
Übertragung gekürzt und nicht als vollständiger Nachweis akzeptiert. Die beiden
anschliessenden Ausgaben mit je 22 Fällen waren vollständig und wurden exakt
abgeglichen. Der Vorfall und alle Antworten bleiben im Paket dokumentiert.

## Nachprüfung

ZIP entpacken und im Paketverzeichnis ausführen:

```sh
python3 -B verify_package.py
python3 -B verify.py
python3 -B -m unittest -v test_verify
```

Der Offline-Abgleich benötigt Python 3.12 und nur die Standardbibliothek.
Er prüft die gespeicherten Wolfram-Belege; er führt Wolfram nicht erneut aus.
Die drei eigenständigen WL-Dateien und die Anleitung für einen frischen
Wolfram-Lauf stehen im Paket. Das bestehende `x6.py run rax` reproduziert
weiterhin B1/M1; W1 hat diesen ausdrücklich separaten Einstieg.

Geprüft: Wolfram Language 15.0.1 unter Linux x86-64 und Python 3.12.14.
Das veröffentlichte ZIP wurde frisch entpackt; Inventarprüfung und kompletter
Offline-Abgleich bestanden. Im Auftrag wurden ausschliesslich die bestehende
Wolfram-Anbindung verwendet und keine kostenpflichtigen Dienste neu aktiviert.

## Aussagegrenzen

- Auswahl von 44 der 160 historischen exakten Matrixfälle, keine zufällige
  repräsentative Stichprobe und keine erneute Nachrechnung der 3,2 Millionen
  Übergänge.
- Interne nachträgliche Gegenprüfung mit anderem Rechenkern, keine unabhängige
  personelle oder blinde Begutachtung und keine Begutachtung durch Wolfram Research.
- Keine neue Universalitätsklasse, kein ausgeführtes RAX-U2, keine allgemeine
  geometrische oder Kontinuumsaussage und keine physikalische Validierung.
- U1 bleibt bei 8 gestützt / 16 verworfen / 16 unentschieden; die acht primären
  B1-Vergleiche bleiben unentschieden. Der frühere Archivvorfall bleibt offen.
- Geteilte Modellannahmen können auch bei mehreren Rechenwegen gemeinsame Fehler
  verursachen. Hashes und gespeicherte Ausgaben sind keine Signaturen.

Siehe [U1-Gegenprüfung](../countercheck-v0.1/README.md) und
[gesamtes RAX-Forschungsprogramm](../README.md).

Copyright 2026 Thomas Gfeller. Originale Projektbeiträge unter
[Apache-2.0](../../../../LICENSE), gemäss [Lizenzumfang](../../../../LICENSE_SCOPE.md).
Proprietäre Wolfram-Kernel und Bibliotheken werden nicht mitgeliefert.
