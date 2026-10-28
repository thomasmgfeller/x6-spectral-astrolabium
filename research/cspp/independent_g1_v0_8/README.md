# CSPP v0.8: unabhängige G1-Prüfung vor Dirac

**Vorregistrierung, noch keine neuen Prüfdaten ausgewertet.**

Alle zwölf bisherigen Parameterzellen werden auf einer notwendigen skalaren
G1-Bedingung geprüft: Populations-RMS <=10% für jedes der zehn unveränderten
Operatorfelder. Je64 frische Wolken bei nu=512,1024,2048,4096 ergeben256
unabhängige Wolken; epsilon=1,1/4,1/16 wird innerhalb einer Wolke gepaart.

Die Testfamilie, numerischen Fehlerbudgets, Zufallsströme, Ensemblegröße
und Abbruchregeln stehen in [PROTOCOL.json](PROTOCOL.json).
[METHODS.md](METHODS.md) enthält die vollständige statistische Herleitung,
Fehlerzerlegung und die Grenzen der Aussage. Der Code wird vor dem ersten
neuen RNG-Aufruf öffentlich festgeschrieben.

Die exakte einseitige Binomialregel kontrolliert das gemeinsame Risiko
einer falschen Ablehnung über120 Tests auf höchstens2,5%. Sie liefert
untere RMS-Grenzen ohne eine beschränkte RMS-Verteilung vorauszusetzen.
Nichtverwerfen ist keine Freigabe: G1 kann durch diesen Ablehnungsversuch
allein nicht PASS werden. Kein Dirac-, Flavor- oder Kohärenzlauf ist vorgesehen.

Vor Beginn bestanden unabhängige rationale Zählungen und Gewichte,
direkte Ballsummen, exakte Binomial-/Abdeckungsprüfungen sowie negative
Kontrollen für unsichere Schwellen und zu kleine Erfolgszahlen.
Der Ressourcencheck verwendete ausschließlich eine alte Entwicklungswolke.

Dieser PR baut auf dem noch offenen PR#139 auf. Bisherige Daten und
wissenschaftliche HOLDs bleiben unverändert. Ergebnisse werden nach
der vollständigen festen Auswertung in einem nachfolgenden Commit ergänzt.
