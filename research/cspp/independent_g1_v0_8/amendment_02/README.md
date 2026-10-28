# Amendment02: eindeutiger Audit-Import im Replay

Der erste GitHub-Replay in Job122779960919, Workflow40677627397,
brach am28. Oktober2026 um11:09:19UTC vor der ersten Neuberechnung mit
`AttributeError: module 'audit' has no attribute 'compute'` ab.
Vorregistrierungsnachweis und vollständige Prüfung der gespeicherten
Prüfdaten waren auf GitHub bereits erfolgreich.

Ursache: `support.py` stellt die v0.7-Geometrie über den Python-Suchpfad
bereit. Der bloße Import `audit` im Veröffentlichungsprüfer wählte dadurch
das gleichnamige Vorgängermodul. Dessen API hat keine Funktion `compute`.
Der ursprünglich direkt aufgerufene v0.8-Audit und die Produktion waren
von dieser Importauflösung nicht betroffen.

Die Korrektur betrifft ausschließlich den Replay-Aufrufer:
`publication_checks.py` lädt jetzt `HERE/'audit.py'` unter einem eindeutigen
Modulnamen. Alle ursprünglich vorregistrierten Dateien, der Prüfplan,
sämtliche Zufallsströme und Prüfdaten bleiben bytegleich. Keine Toleranz,
Ensemblegröße oder statistische Entscheidung wird geändert. Der bisherige
Prüfer ist als `original_publication_checks.py` erhalten; seine Prüfsumme
entspricht der in Amendment01 dokumentierten Fassung.

Der korrigierte vollständige Replay wird lokal und erneut in GitHub
ausgeführt. Er benutzt dieselben archivierten Daten und ist keine weitere
unabhängige Stichprobe. Dieser Fehler wird nicht durch Überspringen des
Audits oder durch Abschalten einer Prüfung behoben.
