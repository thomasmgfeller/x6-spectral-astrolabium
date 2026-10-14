# RAX-U1 Gegenprüfung v0.1

**Interne Gegenprüfung eines synthetischen Kontrollversuchs. Keine externe oder
verblindete Begutachtung, kein RAX-U2-Entdeckungslauf und keine physische Evidenz.**

## Freigegebene Dateien

- [Prüfbericht als PDF, 4 Seiten](RAX_U1_Gegenpruefung_v0_1.pdf)
- [Vollständiges Reproduktionspaket als ZIP, ca. 5,4 MB](RAX_U1_Gegenpruefung_v0_1_Paket.zip)
- [Publikationsnachweis mit Dateigrössen und SHA-256](PUBLICATION.json)

PDF und ZIP werden unverändert veröffentlicht. Das Paket enthält 50 Dateien,
darunter die U1-Quellen, den eingefrorenen Vertrag, das rekonstruierte vollständige
Roharchiv, die erhaltene beschädigte Kopie, den neuen Gegenprüfer, Fehlerproben
und maschinenlesbare Ergebnisse. Nach dem Entpacken stehen die Befehle in
`research/rax_u1_countercheck/README.md` und im PDF. Der Lauf aus dem gepackten
Archiv wurde ausgeführt und mit dem Ergebnisbericht verglichen.

## Ergebnis und Grenzen

| Gegenstand | Befund |
| --- | --- |
| 160 vollständige Übergangsmatrizen | Bestätigt; 32 stark lumpbar, 128 nicht stark lumpbar |
| 3.200.000 Übergänge | Vollständiges Replay und unabhängige Neuzählung stimmen überein |
| 40 Entscheidungen | 8 gestützt, 16 verworfen, 16 unentschieden; unverändert |
| Alte Ressourcenprüfung im Referenzprüfer | Lücke für Laufzeit- und Speicherangaben reproduziert; neue zusätzliche Prüfung erkennt sie |
| Präparationsmittelwerte ausserhalb U1 | Explizites Gegenbeispiel zeigt Grenzen der Verallgemeinerung |
| Verhältnis der statistischen Kriterien | Bei den gewählten Toleranzen redundant; keine doppelte unabhängige Bestätigung |
| Archivverlust von 720.000 Bytes | Bytegleiche Rekonstruktion bestätigt; Ursache weiterhin UNKNOWN |
| Dauerhafte unbeaufsichtigte Erfassung | Noch nicht uneingeschränkt qualifiziert |

Die Originaldaten halten die Ressourcenbudgets ein. Die Prüflücke verändert
die 40 ursprünglichen Entscheidungen nicht. Der zusätzliche Prüfer importiert
weder den ursprünglichen Rechenkern noch seinen Referenzprüfer; der separate
Fehlerproben-Harness importiert beide ausdrücklich für den Verhaltensvergleich.
Die ursprünglichen Quellen und die Evidenz bleiben unverändert.

Das konstruierte Gegenbeispiel liegt ausserhalb der eingefrorenen U1-Familie.
Es widerlegt keine Aussage über diese Familie, begrenzt aber den Schluss von
vier passenden Präparationsmittelwerten auf beliebige mikroskopische Fehler.
U2 benötigt reichhaltigere Gegenversuche und einen eigenen Prüfvertrag.

## Historischer Stand im unveränderten Bericht

Der PDF-Bericht und das ZIP wurden vor dieser Veröffentlichung fertiggestellt.
Ihre Aussage, dass sie keinen GitHub-Upload belegen, beschreibt diesen damaligen
Stand. Diese Veröffentlichung stellt nun genau diese freigegebenen Artefakte
bereit; ihre enthaltenen lokalen Commit-IDs bleiben als Herkunftsangaben erhalten.
Die Veröffentlichung selbst ist keine externe wissenschaftliche Begutachtung.

## Herkunft und Lizenz

Prüfdatum und Freigabe: 14. Oktober 2026. Der vollständige wissenschaftliche
Umfang, Reproduktionsbefehle, Quellen und offenen Abnahmebedingungen stehen im
PDF und im Paket. Die Prüfsummen dienen dem Inhaltsvergleich, nicht als Signatur
oder wissenschaftlicher Nachweis.

Copyright 2026 Thomas Gfeller. Originale Projektbeiträge unter
[Apache-2.0](../../../../LICENSE), gemäss
[Lizenzumfang](../../../../LICENSE_SCOPE.md). Fachliteratur und benannte
Abhängigkeiten behalten ihre jeweiligen Rechte und Lizenzen.
