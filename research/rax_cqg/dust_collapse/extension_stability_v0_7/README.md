# CST-DUST · Vierte Einfügung und Erweiterungsstabilität bei N15

[Kurzbericht (PDF)](../reports/CST_DUST_N15_Erweiterungsstabilitaet_v0_7.pdf) · [Offline-Prüfpaket (ZIP)](../packages/CST_DUST_N15_Erweiterungsstabilitaet_v0_7_Pruefpaket.zip) · [Rechenweg](Methode.md) · [Zertifikat für den gesamten Träger](full.json)

**Stand 19. November 2026.** Fortsetzung von [PR #311](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/311), Merge-Commit `3bbc8fd2a92879b45fb9444ed77ca4f545b9ad9d`. Die Untersuchung verwendet denselben q₇-Detektor, die Anfangsdichten 1/8 und 1/4 und die Toleranzen der N11-Präparation. λ ist der gemeinsame Anteil des Amplitudengewichts, den jede der zwei N11-Ausgangshistorien auf ihre eigenen erreichbaren Nachkommen überträgt.

| Geprüfte Erweiterung | Gemeinsamer Stabilitätsbefund auf beiden Referenzgittern |
|---|---|
| Alle bisherigen 169 Zustände und alle 23 N15-Typen mit Eliminationsbreite bis drei | Jede Aufteilung besteht bis 5,0210 %. Bei 5,0211 % verletzt der weiterhin zulässige Zeuge aus PR #311 die Niveautoleranz. |
| Alle bisherigen Zustände und alle 1 048 zugelassenen N15-Typen | Jede Aufteilung besteht bis 4,0008 %. Bei genau 5 % sind die Kontrast- und Vorzeichenkriterien für jede Aufteilung gesichert. Das Niveaukriterium bleibt dort offen. |

## Was die Rechnung entscheidet

Auf dem Vollträger steigen die oberen Schranken der relativen Niveauabweichung bei 4,0008 % auf höchstens 9,98208 % und 9,99978 % für die beiden Dichten. Erlaubt sind jeweils 10 %. Die Änderung des vierteiligen Dichtekontrasts beträgt höchstens 18,65911 % des Ausgangskontrasts. Bei 5 % liegen diese drei Schranken bei 12,39730 %, 12,41919 % und 24,14800 %. Die letzte Zahl bleibt unter den erlaubten 25 %. Die Änderung des Gesamterfolgsunterschieds bleibt auch bei 5 % kleiner als sein Ausgangsbetrag. Damit bleibt der Unterschied zwischen hoher und niedriger Dichte negativ.

Beim Übergang von λ = 0,040008 auf 0,040009 überschreitet die verwendete Vollträgerschranke für Dichte 1/4 den zulässigen Wert. Die erste tatsächliche Verletzung auf dem vollen Träger ist weiter zwischen der Garantie bis 4,0008 % und dem bekannten Gegenbeispiel bei 5,0211 % eingeschlossen. Die volle 5,0210-%-Garantie von PR #311 bezog sich auf den N14-Träger. Auf N15 entscheidet die Auslese auf dem grösseren Zustandsraum.

## Inventar der vierten Einfügung

| Zählung | Vor der abschliessenden Skalarprüfung | Danach |
|---|---:|---:|
| Verschiedene N15-Endtypen | 1 652 | 1 048 |
| Verschiedene N14-Eltern-/N15-Tochter-Paare | 5 029 | 4 165 |
| Markierte Vier-Schritt-Pfade aus der Dreierkette | 74 410 | 64 088 |
| Markierte Vier-Schritt-Pfade aus der Ein-Kanten-Ordnung | 107 466 | 92 800 |
| Markierte Pfade beider Eltern zusammen | 181 876 | 156 888 |

Jeder der 139 N14-Elterntypen besitzt mindestens eine zugelassene Tochter. Die Dreierkette erreicht 1 011, die Ein-Kanten-Ordnung 1 047 der 1 048 Typen. Überlappende Typen werden bei der Auslese kohärent zusammengeführt. 257 Typen scheitern nur an einer freien inneren Nullrichtung, 273 nur am gemischten Legendre-Defekt, 74 an beiden Bedingungen. Alle Multiplikitäten sind gegen 284 255 Löschbeziehungen geprüft.

## Nachrechnen

Getestet mit Python 3.12, NumPy 2.3.5, SymPy 1.14.0 und mpmath 1.3.0. Die Einthread-Rechnung benötigt keine Online-Dienste. Das originale v0.6-Eingabearchiv ist im Repository als [Prüfpaket v0.6](../packages/CST_DUST_N14_Volltraeger_v0_6_Pruefpaket.zip) und im Offline-Paket als `input_v06.zip` mit SHA-256 `04b2c22bc8867010ffe3ed0c4a27d52314342b8b724c64492d77e3b8d52b3826` enthalten. Der Prüfer entpackt seine Quellen und Daten lokal.

```sh
python3 -B verify.py
```

Der Standardlauf kontrolliert Prüfsummen, rekonstruiert das N15-Inventar und die Rangklassifikation, prüft die positiven Pilotmatrizen, führt die rationalen Zertifikate für beide Träger erneut aus und kontrolliert die Uhrhüllen an kleinen direkten Summen. Für die numerische Rekonstruktion aller Eingaben in einem temporären Verzeichnis

```sh
python3 -B verify.py --rebuild
```

| Datei | Inhalt |
|---|---|
| `Methode.md` | Zulässigkeit, Uhrhüllen, positive Vervollständigung, Auslese und Fehlerrechnung |
| `catalog.json` | Eltern-Tochter-Multiplizitäten, exakte Ränge, Wurzelpfade und kostenbasierte Auswahl |
| `clocks.json`, `gram.npy`, `certificate.json` | Drei Uhrgitter für 23 N15-Typen, Pilotmatrizen und Stützzertifikat |
| `anchor_rows.json`, `caps.json`, `full.json` | Zwei Elternüberlappungen und Diagonalen je Effekt und N15-Typ, Uhrhüllen und rationale Vollträgerschranke |
| `scalar_checks.json`, `controls.json` | Abel-Gegenrechnung, 604 unabhängige Ausschlussprüfungen und 15 direkte Kontrollen der Waldkontraktion |
| `bottleneck.json` | Extremale Projektionsschranken bei Dichte 1/4 und ihre erreichbaren Endtypen |

Bei der hohen Dichte begrenzen auf beiden Gittern die Endtypen **47037** und **45950** die schwächsten unteren Ankerprojektionen beider Eltern. Ihre individuellen komplexen Uhrantworten wären der nächste gezielte Test des offenen Niveaukriteriums. Beide haben Eliminationsbreite fünf. Die gegenwärtigen Gitterzertifikate setzen numerische Skalar- und Uhrdaten voraus. Kontinuierliche Uhrintegrale, physikalisches Historienmass und Kollapsdynamik bleiben offen.
