# CST-DUST · Die Staubuhr 5 als Dichtezeiger

**23. November 2026 · N15-Typ 2097151 · Markierte Dosis 1**

Die veröffentlichte Wirkung prägt der vorhandenen inneren Staubuhr 5 eine von der Dichte am Ereignis 11 abhängige Phase auf. Dazu genügen zwei kleine, echte Uhrpakete im ursprünglichen Fenster. Ihre Uhren laufen auf jedem Wirkungspaar mit ihrem jeweiligen Wert weiter. Der Konstruktion liegt die gewöhnliche Wirkung ohne künstliche Verschiebung einer nur einmal benutzten Uhrkopie zugrunde. Die gewählte kohärente Paketpräparation und ihr äusserer Vergleich sind Annahmen dieses Versuchs.

Der Puls an der rechten Kopie von Uhr 6 verschiebt das Zeigerargument der Uhr 5 nicht. Hinter 12 ist Uhr 5 noch als Randkoordinate vorhanden. Hinter 13 ist sie bereits integriert. Für einen gemeinsamen bedingten Staubausgang erhält man auch dort einen kleinen Interferenzkontrast zwischen zwei Dichtepräparationen.

| Prüfung | Befund |
|---|---|
| Phase aus dem ursprünglichen Paar 5→11 | Bei mittlerer Uhr 11 ist der Betrag der relativen Phase genau x/304, x = w₁₁/D. Über ihr ganzes Uhrfenster liegt der Faktor zwischen 15/16 und 17/16 dieses Werts. |
| Alternative mit dem vor 11 gespeicherten Uhrpaar 5/6 | Bei festem gewichteten Mittelpunkt, gemeinsamer Dauer, identischer späterer Uhr 12 und gemeinsam zulässiger Dichte erreicht der reine Abstandsanteil höchstens 26,259 % des Vergleichswerts. |
| Gewöhnlicher Ausgang hinter 13 | Für die angegebenen schmalen Pakete und den pulsfreien Lauf liegt der Vieramplituden-Phasenkontrast in [−3,2173379; −3,2173378] × 10⁻⁶ rad. |
| Vergleich zweier Präparationsphasen | Die Änderung der normierten Intensitätsbalance liegt im selben Lauf in [−3,2173253; −3,2173252] × 10⁻⁶. |
| Physisches P3-Register | 60 × NOT_RUN. Ein früh auslesbarer Einzelspeicher, die physische Randpaarung für die Messung und die unabhängige positive Masseneichung sind offen. |

## Nachrechnen

Im entpackten Verzeichnis prüfen die ersten drei Python-Befehle Quellen, Wirkungsidentitäten, Träger und den strikten Interferenzausschlag allein mit der Standardbibliothek von Python ab Version 3.10. Die letzten drei Rechnungen verwenden zusätzlich NumPy.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
python3 -B uhr5.py
python3 -B zertifikat.py
OPENBLAS_NUM_THREADS=1 python3 -B schnitt.py
OPENBLAS_NUM_THREADS=1 python3 -B ausgang.py
OPENBLAS_NUM_THREADS=1 python3 -B kontrollen.py
```

HERLEITUNG.md beschreibt beide Kandidaten, die Präparation, die bedingten Enddaten und den Fehlerbeweis. Die JSON-Dateien enthalten Einzelwerte und Intervallschranken. quellen/herkunft.json nennt die bytegleichen Quellen auf GitHub. Die vier gehashten lokalen Prüfpläne dokumentieren den Hauptversuch und seine Ergänzungen. Es gab keinen externen Blindtest oder unabhängigen Zeitstempel.

[Veröffentlichte Verklebung und offenes Dichtefenster](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/360) · [Äussere Dichtequelle und zwei Pulsregeln](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/361)
