# Nachträgliche GitHub-Veröffentlichung

Der Nutzer erteilte am **16. Oktober 2026 um 14:41 Uhr Europe/Zurich** ausdrücklich
die Freigabe zur öffentlichen Veröffentlichung des zuvor geprüften Pakets.

Der frühere automatische Freigabeblock ist damit für diese Veröffentlichung
aufgelöst. Er bleibt Teil der tatsächlichen Entstehungsgeschichte:
Vertrag und Quellcode wurden **vor dem Ziellauf lokal**, aber **erst nach dem
Ziellauf öffentlich** bereitgestellt. Eine öffentliche Vorregistrierung wird
auch nach der Publikation nicht behauptet.

Der lokale Git-Transport besaß keine Push-Zugangsdaten. Die verbundene GitHub-App
veröffentlicht daher die geprüften Dateien über die Git-Daten-API. Diese erzeugt
neue öffentliche Commit-IDs und ersetzt keine historischen lokalen Zeitstempel.

## Erhaltene lokale Historie

`local-history.bundle` ist die unveränderte, bereits im freigegebenen Prüfpaket
enthaltene Git-Historie:

- Basis: `faeb2e003ff91cd3cc90b18db9617d725bebcb2f`
- Vertragscommit: `9da649b34adca8bb249b9ff80647bf5e682b8f98`
- Quellfreeze: `4680e959a40d4e8fa9ff2193eaf8c10f2d85299d`
- Lokaler Ergebniscommit: `ef64e9174d882ac5c5b7cd43e5d004da2e66b162`

Die ursprünglichen Verträge, Quellfreeze-Dateien und Rechenergebnisse bleiben
unverändert. `publication.json` beschreibt weiterhin den ursprünglichen lokalen
Freeze-Zustand, nicht den aktuellen GitHub-Veröffentlichungsstatus.

Die CI und die dokumentierten Reproduktionsbefehle laden diese Objekte aus dem
Bundle in eine separate lokale Archiv-Referenz. Dadurch kann der unveränderte
Runner die ursprünglichen Quellcommit-IDs weiterhin exakt prüfen. Die aktualisierte
Dateiinventur bindet auch das Bundle per SHA-256.

Die Veröffentlichung umfasst Bericht, alle 352 Erzeugungen, 207 Repräsentanten,
sämtliche exakten Werte und Restklassen, getrennte Gegenprüfung, nachträglich
markierte Zeitumkehrdiagnose und den Reproduktionsworkflow. Sie erweitert keine
wissenschaftliche Aussage und ändert keine Ergebnisse.
