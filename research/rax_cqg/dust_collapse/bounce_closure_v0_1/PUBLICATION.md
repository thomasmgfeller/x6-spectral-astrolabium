# Abschluss des bisherigen Bounce-Kandidaten v0.1

**5. November 2026 · `CLOSED_REJECTED_FOR_DOMINANT_BOUNCE`**

Bei gleichen Historien-Amplitudenbeträgen und erhaltenen orthogonalen Endvolumenkanälen gilt für die 27 Entwicklungs- und die 17 disjunkten Prüfpfade `q_B ≤ 1/2`. Ein beliebiger normierter passiver Zusatzzeiger kann die geforderte Dominanz von 80 % damit nicht erreichen. Der Abschluss konsolidiert den bereits bekannten Ausschlusssatz und zertifiziert seine Voraussetzungen auf beiden Familien.

- [Abschlussbericht (PDF, sechs Seiten)](../reports/CST_Staubball_Bounce_Kandidat_Abschluss_v0_1.pdf)
- [Unverändertes vollständiges Prüfpaket](../packages/CST_Staubball_Bounce_Kandidat_Abschluss_v0_1_Pruefpaket.zip)
- [Lesbarer Prüfer](verify_closure.py), [maschinenlesbare Entscheidung](results/closure_result.json), [Kandidatensnapshot](candidate_snapshot.json), [Quellenbindung](source_snapshot.json)
- [Originale Methodik und Wiederholung](README.md)

Die drei Originalarchive und alle 15 Dateien des gelieferten Abschlussarchivs sind hier bytegleich zugänglich. `PUBLICATION.md` und `publication_check.py` sind zusätzliche Veröffentlichungshilfen. Der im Originalbericht beschriebene Quellenstand bleibt `5f7994400869c921dec5b335f04a384a713e5e64`; er wird nicht nachträglich auf diesen Publikationscommit umgeschrieben.

## Abgrenzung der Entscheidung

Die analytische Schranke schliesst PASS für den dominanten Bounce aus. Sie ersetzt kein historisches HOLD durch ein FAIL: HOLD bei unzureichender Interferenzkontrolle bleibt erhalten. Auf den 17 Prüfpfaden ergibt sich für Gesamt- und geteilte Dichtespur über das ganze vereinbarte Kopplungsband `[32/45, 162/95]` FAIL, bei einem diagonalen Bounce-Anteil unter 6,82 %. Bei ausgeschalteter Dichtespur ergibt sich weiterhin HOLD. Die numerisch offenen Übergangsbereiche der Entwicklungsfamilie bleiben dokumentiert.

N bedeutet nur, dass die festgelegte Umkehrfolge im festgelegten Zeitfenster nicht erfüllt ist. Die Befunde widerlegen weder alle möglichen Bounces noch die CST. Ein allgemeiner dynamischer CST-Bounce und Singularitätsauflösung bleiben **HOLD**. Es wurden Modellrechnungen wiederholt, keine physischen Messungen ausgeführt.

Die Suche nach dem 80-%-Ziel durch reine Optimierung passiver Messkopplungen wird für diesen Kandidaten abgeschlossen. Eine neue Kandidaten-ID verlangt eine unabhängig begründete Änderung ausschlussrelevanter Voraussetzungen und vorab festgelegte klassische und dynamische Referenzprüfungen. Bereits ausgewertete Pfade werden nicht zu frischen Prüfdaten umdeklariert.

## Prüfung im Repository

Python ab 3.10 mit Standardbibliothek; nicht mit `-O` ausführen:

```sh
python3 research/rax_cqg/dust_collapse/bounce_closure_v0_1/publication_check.py --replay
```

Die Veröffentlichungskontrolle prüft das unveränderte ZIP, alle 15 Mitglieder, die Berichtskopie und die Übereinstimmung der drei Quellenarchive mit den bereits veröffentlichten Paketen. Anschliessend wird der Originalprüfer in einer temporären Arbeitskopie ausgeführt. Er kontrolliert 51 Originalprüfsummen, beide Träger und isolierten Endkanäle, die Intervallsumme, 120 direkte Zahlenvergleiche und acht Ergebnisdateien. Die in diesem Abschluss erneut erzeugten acht Dateien waren bytegleich zu den archivierten Originalen.

Die vollständige Neuerzeugung der Kausalordnungen, 18 ursprüngliche explizite Nachzählungen und 70 inverse Momentquadraturen werden dabei nicht erneut ausgeführt. Lokale Plan-Hashes sind Integritätssiegel und keine externe Präregistrierung. Die Abschlussbewertung ist retrospektiv.

Projektbeiträge gemäss [Lizenzumfang](../../../../LICENSE_SCOPE.md); bestehende Quellen und Nachweise bleiben erhalten.
