# CST-DUST · Sondengeometrie und Vakuumkontrolle

Auf der veröffentlichten N22-Grundordnung wurde für eine eigens leere Randpräparation ein exakter Nullzeuge der Staubgleichungen gefunden. Bei identisch beibehaltenen positiven späten Randgewichten scheitert ein vollständig leeres Inneres. Ein positiver unabhängiger Masseneichwert für die schwere oder leichte Präparation ist offen.

Im flachen Kontrollmodell trennt ein einzelnes Seitenbit auf der Bahn 5→11 zwischen den beiden bekannten Kugeln über [31/64,17/32]. Ein neues Paar mit Radien 1 und 1,785 zeigt dagegen auf allen drei vorgeschlagenen Bahnen über das ganze ursprüngliche Fenster identische Seiten. Die verbleibenden besten maximalen relativen Fehler auf diesem Paar liegen bei rund 28,19 % für den Radius (exakt 157/557) und rund 52,22 % für die Fläche (87449/167449). Die konstruktive Sehnenmessung mit sechs verschiedenen Richtungen ist auf 30 synthetischen Bedingungen je Auflösung geprüft. Acht Halbierungen genügen für vollständig eingeschlossene Intervalle in der 5-%-Toleranz. Die Eingaben für eine solche Messung umfassen unabhängige Orte, Massstab, gemeinsamen Schnitt und Seiteninformation.

Am Halbschnitt wurde auch die physische Modellvoraussetzung einer freien, quellenfreien Fenstersonde überprüft. Ausgangspunkt sind die drei geometrisch unterscheidenden Bahnen und ihre beiden verschiedenen induzierten N23-Ordnungen. Gleichzeitige Kombinationen der drei Abtastungen, beliebig viele leere Nachfolger bei unverändertem altem Zukunftskragen sowie die vollständige N24-Familie mit genau einem neuen positiven Nachfolger sind unter ihren jeweiligen ausgewiesenen Voraussetzungen ausgeschlossen. Andere Netze, Messorte und Kopplungen erfordern separate Prüfungen.

## Offline reproduzieren

Nach Entpacken im Hauptverzeichnis mit Python ab 3.10 und Standardbibliothek ausführen.

    python3 -B pruefen.py

Der Hauptprüfer kontrolliert vor den Rechnungen die SHA-256-Liste, die bytegleichen Originaldaten und den Prüffreigabestand. Er berechnet alle registrierten Aussagen erneut. Die rationalen Widerspruchsnachweise für den Zusatzsensor werden ohne Optimierer geprüft. Hinweise zu unabhängig rekonstruierten Schritten und gemeinsam genutzten Basisfunktionen stehen in den Teilverzeichnissen.

| Teil | Beweis bzw. Kontrolle |
|---|---|
| messfenster | Geometrische Nullstellen und robuste Seitentrennung im Zeitfenster |
| schalen | Neues Gegenpaar mit identischen Seiten und Messung eines unbekannten Radius mit drei Sehnen |
| leere_sonden | Gemeinsame Sensoren und Hindernis für beliebige endliche leere Zukunftsnetze |
| positive_probe_next | Gesamtdurchlauf mit einem positiven inneren Helfer am Halbzeitschnitt |
| helper_audit_next | Unabhängige Antikettenzählung, Vorzeichen und Ausschluss der positiven Halbsonde |
| geom_terminal_next | Zweites rationales Widerspruchszertifikat für jede der zwölf letzten terminalen Anbindungen |
| massenkontrolle | Genaues N22-Staubvakuum, Widerspruch bei positivem späten Kragen, Skalierung der Ladung |
| eingaben | Gepinnte Ereignisorte, Randpräparationen und physischer P3-Freigabestand |

Die Lage der physischen Oberfläche und der physische Anfangsmassenstandard bleiben offen. Die acht Pilotplätze sind Teil der 60 physischen P3-Punkte, alle auf NOT_RUN. Das Paket enthält keine physischen P3-Messwerte. Quellen in Herkunft.md, mathematische Einzelheiten und Geltungsbereiche in den jeweiligen README-Dateien.
