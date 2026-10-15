# Wolfram-Gegenprüfung: Spektren und gerichtete Kausalordnung (Referenzfall 5)

**Ausgeführt: PASS_WITH_SCOPE_LIMITS.** Wolfram bestätigt im korrigierten
Lauf 16 von 16 Prüfaussagen. Eine getrennte Python-Implementierung stimmt
bei allen Matrizen, sechs charakteristischen Polynomen, Extremalmengen
und sechs Permutationsdatensätzen exakt überein.

## Freigegebene Dateien

- [Vollständiger Prüfbericht](PRUEFBERICHT_DE.txt)
- [Unverändertes Reproduktionspaket](X6_Wolfram_Fall5_v0_1.zip)
- [Veröffentlichungsnachweis und Prüfsummen](PUBLICATION.json)

SHA-256 des freigegebenen ZIP:
`7992c9a6ad1622cd338785a11ddccd46d3a0d4839db0333719f239c2d3fef868`.
Der separat lesbare Bericht ist bytegleich aus diesem Paket übernommen.

## Exaktes Gegenbeispiel

Die strikte Ordnung `C=[[0,1,1],[0,0,0],[0,0,0]]` beschreibt ein
minimales Ereignis vor zwei unvergleichbaren maximalen Ereignissen.
Die duale Ordnung ist `D=Transpose[C]`. Es gilt `C[i,j]=1`, wenn
Ereignis i strikt vor Ereignis j liegt.

Mit `S=C+C^T`, `A=C-C^T` und `K=SA-AS` liefern beide Ordnungen
dieselben charakteristischen Polynome in der Konvention `det(z I-M)`:

| Operator | Polynom für beide Ordnungen |
| --- | --- |
| S | z(z²−2) |
| A | z(z²+2) |
| K | z(z²−16) |

Die Anzahl minimaler/maximaler Elemente ist jedoch **(1,2)** für C und
**(2,1)** für D. Diese Anzahlen bleiben unter ordnungserhaltenden
Bijektionen erhalten. Alle sechs möglichen Umbenennungen bestätigen,
dass kein ordnungserhaltender Isomorphismus existiert.

Die Positivkontrollen finden jeweils zwei Automorphismen und zwei
ordnungsumkehrende Abbildungen. Die Spektren bleiben unter jeder
Umbenennung unverändert. Aus den vollständigen Matrizen S und A in
derselben Basis lässt sich hingegen `C=(S+A)/2` rekonstruieren.

## Reproduktion

ZIP vollständig entpacken und im Verzeichnis `X6_Wolfram_Fall5_v0_1` ausführen:

```sh
python3 verify_release.py
```

Erwartet: `PASS_WITH_SCOPE_LIMITS`. Der Prüfer rekonstruiert die
mathematischen Ergebnisse, prüft die gespeicherten Wolfram-Antworten,
beide Freeze-Dateien, die dokumentierte Korrektur und das Dateimanifest.
Er benötigt nur die Python-Standardbibliothek und keinen Netzwerkzugriff.
**Wolfram wird dabei nicht erneut ausgeführt.** Für eine frische
Wolfram-Auswertung ist `wolfram_check_v0_1_1.wl` vorgesehen.

Python verwendet ganzzahlige Polynommultiplikation und die
Leibniz-Determinantenformel; Wolfram die eingebaute
`CharacteristicPolynomial`-Funktion mit expliziter Konventionsanpassung.
Es gibt keine numerische Näherung; die Vergleichstoleranz ist null.

## Dokumentierter Erstfehler

Der erste Kernel-Lauf bestand 15/16 Aussagen. Der Adapter berücksichtigte
nicht, dass Wolfram `CharacteristicPolynomial[M,z]=det(M-z I)` verwendet.
Für drei Dimensionen unterscheiden sich die Koeffizienten daher um ein
globales Minuszeichen. Der Erstlauf bleibt **FAIL_SIGN_CONVENTION**.

Der korrigierte Adapter multipliziert mit `(-1)^n`. Modelle, Sollwerte,
16 Prüf-IDs und Nulltoleranz bleiben unverändert. Der zweite Lauf besteht
16/16 Aussagen ohne Meldungen. Beide Programme und Rohantworten sind
erhalten. Der vorausgehende fehlgeschlagene Kontextabruf ist separat
dokumentiert; er war kein mathematischer Rechenlauf.

Die Änderung erfolgte nach Einsicht in den ersten Lauf. Sollwerte und
Python-Vorrechnung waren vor der Fixierung bekannt. Das ist keine
blinde Prüfung oder Vorregistrierung einer Entdeckung.

## Wissenschaftliche Aussage und Grenzen

Das Beispiel widerlegt die allgemeine eindeutige Rekonstruktion einer
gerichteten Ordnung aus **genau diesem Tripel von Spektren**.
Ein darauf beschränktes Verfahren muss Mehrdeutigkeit zulassen oder
zusätzliche Information verlangen. Extremalanzahlen unterscheiden
dieses Paar; ihre allgemeine Vollständigkeit wird nicht behauptet.

Wenn Ordnungsumkehr als Äquivalenz zugelassen wird, gehören diese beiden
Ordnungen zusammen. Der Gegenbeweis betrifft ordnungserhaltende Isomorphie.
A ist reell schiefsymmetrisch und in dieser Definition kein hermitescher
Observable-Operator; sein Spektrum enthält komplexe Eigenwerte.

Keine allgemeine Unmöglichkeit spektraler Rekonstruktion, kein
Lorentzscher Kontinuumsnachweis und keine physikalische
Quantengravitations-Validierung werden behauptet. Reale Projektdaten
und X6-Produktionsläufe wurden nicht auditiert. Testentwurf und
Auswertung stammen von derselben Assistenz; es liegt keine externe
personelle Begutachtung oder Zertifizierung durch Wolfram Research vor.
Hashes belegen Inhaltskonsistenz, keine Urheberschaft oder extern
beglaubigten Zeitstempel.

Softwarekonvention:
[Wolfram: CharacteristicPolynomial](https://reference.wolfram.com/language/ref/CharacteristicPolynomial.html).
Siehe auch [wissenschaftlicher Projektumfang](../../../SCIENTIFIC_SCOPE.md).

Originale Projektbeiträge unter [Apache-2.0](../../../../LICENSE), gemäß
[Lizenzumfang](../../../../LICENSE_SCOPE.md). Drittmaterial behält
seine eigenen Rechte. Das Paket enthält keine Wolfram-Software.

