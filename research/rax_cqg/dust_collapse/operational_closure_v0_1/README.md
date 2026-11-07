# CST-DUST: Präparation, Rückkehrtest und Fehlerbudget v0.1

Analytischer Fortschritt nach PR 260, ohne n=5-Produktion und ohne bezahlte
Rechenleistung. Dies ist ein bedingter operationaler Abschluss der
Referenzauslese, keine Herleitung eines physikalischen Detektors oder Bounce.
Alle acht physikalischen Gates bleiben **HOLD**.

## Ergebnisse

- Selbst die gesamte klassische Recordverteilung lässt unterschiedliche
  kohärente Zustände und Auslesen zu. Im erklärten n=1-Modell wird dies
  analytisch und an 150 exakt eingeschlossenen Fällen gezeigt.
- Eine bekannte Rang-eins-Rückkehrmessung mit perfekter phasenfreier
  Kalibrierung erzwingt die passende reine Präparation. Bei vorgegebener
  gemeinsamer Recordverteilung folgt die ursprüngliche Referenzsichtbarkeit.
- Maßdarstellung und eine gemeinsam geänderte Wellenfunktionsphase ändern
  diese Vorhersage nicht. Zustand, Effekt und vollständiges Instrument
  müssen konsistent transportiert werden.
- Die kombinierte Fehlergrenze lautet
  `min(1, tau + sqrt(min(1, epsilon+tau)) + 4*delta)`.
  Die Zahlenbeispiele sind Diagnosebudgets, keine Messdaten.

`DERIVATION.md` enthält die vollständigen Beweise. Das PDF ist die kompakte
Lesefassung. `operational_contract.json` trennt mathematische Festlegungen
von den noch fehlenden physikalischen Nachweisen. Der Nulltest allein
qualifiziert keinen Detektor; die Identitätsauslese wäre ein Gegenbeispiel.

## Reproduzieren

ZIP vollständig entpacken, dann im Paketverzeichnis ausführen:

```sh
python3 -B verify_package.py
python3 -B replay.py
```

Die wissenschaftliche Rechnung verwendet nur die Python-Standardbibliothek,
exakte Brüche und ganzzahlige Quadratwurzeleinschließungen. Keine Installation,
Netzwerkverbindung, Cloudkonten oder Zugangsdaten sind erforderlich.
`python3 -B analyze.py` erzeugt die vier wissenschaftlichen Ergebnisdateien.
`replay.py` rechnet sie isoliert nach und verlangt Bytegleichheit.
Das ist keine externe Replikation und keine Beweisassistentenprüfung.

`plan.json` wurde nach dem algebraischen Entwurf und vor den endlichen
Rechnungen eingefroren; keine externe Präregistrierung. Fünf unveränderte
Quellen sind über Git-Blob-Identitäten gepinnt. Die enthaltenen älteren
Herleitungen sind Provenienz, keine neue Auswertung der gesamten CST.

Die 2x2-Matrixmodelle kontrollieren die Algebra und sind keine Quadratur
der kontinuierlichen Historien. Nur die n=1-Momentrechnung wird als
kontinuierlicher Referenzvergleich ausgewiesen.

Der optionale Berichtserzeuger `build_report.py` benötigt ReportLab und
DejaVu-Schriften unter `/usr/share/fonts/truetype/dejavu/`. Der bereits
erzeugte Bericht ist enthalten. `package.py` erstellt Manifest und ZIP mit
festen Archivzeitstempeln. PDF-Metadaten können bei Neurendern variieren;
die Bytegleichheit bezieht sich auf die wissenschaftlichen Ergebnisdateien.

Die vollständige wissenschaftliche nächste Frage ist nun konkret:
Welche zulässige CST-Materie-/Randkopplung liefert die geforderte
Präparation, Recordverteilung und qualifizierte Rückkehrmessung?
Ohne solche Belege bleibt die Sichtbarkeit eine konditionale Referenzobservable.

Lizenz: Apache-2.0, siehe `LICENSE` und `NOTICE`.
