# X6-QE-Abnahme

**Lokal PASS, 15. Oktober 2026.** Geprüfte Implementierung:
`a81e62fb077ef5e8fd7774682a400cbef6ed5aa1`.
Spätere Register-/Evidenzänderungen ändern diese ausführbaren Quellen nicht.

| Prüfung | Ergebnis | Beleg |
| --- | --- | --- |
| X6-QE exakt | 3 Fälle, 4 Graphen, 12 Umbenennungen, 21 Zurückweisungen | [Vollständige Ausgabe](evidence/local-results.json) |
| Sauberer neuer Git-Checkout | PASS; 12 CLI-Schritte, davon 11 erwartete Zurückweisungen | [Abnahme](evidence/fresh-checkout/acceptance.json) samt Logs |
| Gemeinsame Suite | 10 Berichte, 27 übergreifende Kontrollen; zusätzlich 17 Lorentz- und 21 QE-Kontrollen | [Vollständiges Bundle](evidence/fresh-checkout/run/complete.json) |
| Nur entpacktes Release-Paket | PASS_REFERENCE_REPRODUCTION, keine Abweichung | [Reproduktion](../../docs/reference-qe-v0.1/evidence/local-reproduction/REPRODUCTION.json) samt allen Ausgaben |
| Zitiermetadaten | CFF 1.2.0 gegen gepinntes offizielles Schema bestanden | [Validierungsmetadaten](../../docs/reference-qe-v0.1/citation-validation.json) |

Lokal Python 3.12.14 und Node 24.19.0. Netzwerk-Namespace lokal nicht erzwungen
(`network_namespace_isolated=false`); eine lokale Offline-Fähigkeit wird nicht
als abgeschotteter Lauf ausgegeben. Die GitHub-CI erzwingt die Netzwerktrennung.
Ihre beobachtete Abnahme wird vor dem Merge ergänzt.

Die SHA-256 von `complete.json` ist
`a9320d908fb6baf376aea7d43432ba17df469b566a9b115755c3a1116ca46e41`.
Alle acht bestehenden fachlichen Berichte sind gegenüber der ersten
Referenzedition bytegleich; geändert ist nur der zusätzliche Fehlerfall im
Kontrollbericht. `qe-graphs.json` kommt neu hinzu.

Die Referenzquellen sind im Hauptmanifest gebunden. Reproduktion des gespeicherten
Bundles aus der passenden Quellenrevision:

```sh
python3 -S -B x6.py reference verify research/x6_qe/evidence/fresh-checkout/run
```

Ein später geänderter Prüfer erfordert eine neue Evidenzrevision. Historische
Acht-/Neun-Berichte-Bundles werden nicht überschrieben. Externe personelle
Wiederholung: **NOT_PERFORMED**. Billiards, Spider-Herkunft, Transport,
Quantengedächtnis und arithmetische Residuen: **NOT_TESTED**.
