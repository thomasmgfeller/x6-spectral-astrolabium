# X6-QE-Abnahme

**Lokal und GitHub-CI PASS, 15. Oktober 2026.** Geprüfte Implementierung:
`a81e62fb077ef5e8fd7774682a400cbef6ed5aa1`.
Spätere Register-/Evidenzänderungen ändern diese ausführbaren Quellen nicht.

| Prüfung | Ergebnis | Beleg |
| --- | --- | --- |
| X6-QE exakt | 3 Fälle, 4 Graphen, 12 Umbenennungen, 21 Zurückweisungen | [Vollständige Ausgabe](evidence/local-results.json) |
| Sauberer neuer Git-Checkout | PASS; 12 CLI-Schritte, davon 11 erwartete Zurückweisungen | [Abnahme](evidence/fresh-checkout/acceptance.json) samt Logs |
| Gemeinsame Suite | 10 Berichte, 27 übergreifende Kontrollen; zusätzlich 17 Lorentz- und 21 QE-Kontrollen | [Vollständiges Bundle](evidence/fresh-checkout/run/complete.json) |
| Nur entpacktes Release-Paket | PASS_REFERENCE_REPRODUCTION, keine Abweichung | [Reproduktion](../../docs/reference-qe-v0.1/evidence/local-reproduction/REPRODUCTION.json) samt allen Ausgaben |
| Netzwerk-isolierter frischer CI-Checkout | PASS; identischer Bundle-Hash | [CI-Abnahme](evidence/ci/acceptance.json), [Run 38761394407](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/38761394407) |
| Netzwerk-isolierte Paket-Reproduktion | PASS_REFERENCE_REPRODUCTION, keine Abweichung | [CI-Bericht](evidence/ci/REPRODUCTION.json), [Run 38761394210](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/38761394210) |
| Zitiermetadaten | CFF 1.2.0 gegen gepinntes offizielles Schema bestanden | [Validierungsmetadaten](../../docs/reference-qe-v0.1/citation-validation.json) |

Lokal Python 3.12.14 und Node 24.19.0. Netzwerk-Namespace lokal nicht erzwungen
(`network_namespace_isolated=false`); eine lokale Offline-Fähigkeit wird nicht
als abgeschotteter Lauf ausgegeben. Die GitHub-CI erzwingt die Netzwerktrennung.
Der geprüfte PR-Head ist `d81774785916be76e8642ac9909e61ac5f3743e6`; GitHub
prüfte den temporären Merge-Checkout `da38f90c41a61cd25f71d1b0872e187237551a1f`.
CI-Runtime: Python 3.12.15, Node 24.21.0. [Provenienz](evidence/ci/PROVENANCE.json)
nennt Runs, Jobs und Artefakthashes. Die JSON-Belege wurden aus vollständigen
Jobprotokollen übernommen; ausschließlich GitHub-Zeitstempelpräfixe wurden entfernt.

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
