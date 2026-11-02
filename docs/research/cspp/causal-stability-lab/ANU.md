# ANU-Zufallszahlen im Stabilitätslab

Die Australian National University in Canberra gewinnt Zufallszahlen aus optisch gemessenen Vakuumfluktuationen. Die AQN-API liefert fertige Zahlenblöcke. Der gespeicherte UTC-Zeitstempel bezeichnet deren Empfang durch X6. Der Zeitpunkt der optischen Messung und eine analoge Detektorspur sind in diesem Produkt nicht enthalten. [ANU-Messverfahren](https://physics.anu.edu.au/research/qst/qoptics/random_numbers.php) · [API-Dokumentation](https://quantumnumbers.anu.edu.au/documentation)

## Abschluss am 2. November 2026

Die ANU-Abrufe sind eingestellt. Zum Abschluss lag im Datenzweig eine Reservierung, aber kein erfolgreich archivierter Zahlenblock vor. Für diese Kontrolle gibt es daher keinen Messbefund. Das Labor greift beim Öffnen ausschliesslich auf das GitHub-Archiv zu. Die technischen und vertraglichen Bedingungen des früheren Probebetriebs stehen in der [historischen Betriebsanleitung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a2390096227065579c3ddb9b8b82389f694e4c02/docs/research/cspp/causal-stability-lab/ANU.md).

## Daten und Nutzungsrechte

Die Nutzungs-FAQ der ANU erlaubt die freie Verwendung der **über die API erhaltenen Zahlen** für Forschung und weitere Zwecke. Das Archiv enthält die 1 024 empfangenen Bytes in Hex-Darstellung, Abrufzeit, Quelle, Verweis auf die ANU-Bedingungen, Datum der letzten Tarifprüfung und SHA-256 der Bytes. X6 beschreibt die ANU-Nutzungszusage separat von der Projektlizenz für eigenen Code. Der Adapter verwendet keine Texte, Abbildungen oder Logos der ANU als Archivmaterial. Konto, Schlüssel und HTTP-Header sind nicht Teil des Datenformats. [ANU-Nutzungs-FAQ](https://quantumnumbers.anu.edu.au/faq)

Jeder erfolgreich gespeicherte Block erhält auf dem Datenzweig eine Datei mit dem UTC-Reservierungsdatum im Namen. `latest.json` verweist inhaltlich auf den zuletzt erfolgreichen Block. Der Browser prüft die Integrität der Bytes und berechnet das Ergebnis auf Anforderung neu. SHA-256 ist ein Integritätsvergleich, kein unabhängiger Herkunftsnachweis. [Stabilitätslab](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/causal-stability/#anu)

## Was der Vergleich misst

Fest eingestellt sind der vorhandene CSPP-v0.25-Kontrollgraph mit fünf aktiven Knoten, drei History-Eingängen, θ = 21 und Störamplitude η = 1. Bit 0, 1 und 2 jedes Bytes liefern in dieser Reihenfolge die drei Vorzeichen (0 ergibt −1, 1 ergibt +1). Ein Block liefert 1 024 Modellantworten. Für die endliche Transferzeile t und die Vorzeichen s ist die Antwort A = t·s. Unter unabhängigen, gleich wahrscheinlichen Vorzeichen gilt E[A²] = Σᵢ tᵢ². Das Lab zeigt die beobachtete RMS-Amplitude √(Σⱼ Aⱼ² / 1 024) und die Populationsreferenz √E[A²]. Die Referenz ist keine Behauptung über den Erwartungswert des endlichen RMS-Schätzers.

Die Gegenprobe nutzt das bekannte Verhalten des endlichen Modells. Die Stichprobenstreuung lässt Abweichungen vom Referenzwert erwarten. Es gibt für einzelne Blöcke keine Bestehensgrenze und daraus keinen Nachweis der Quantenherkunft, der Stabilität bei wachsender Dichte oder eines Raumzeitsignals. Ein erneuter API-Abruf erzeugt andere Eingaben. Für eine exakte Wiederholung wird derselbe archivierte Block verwendet.
