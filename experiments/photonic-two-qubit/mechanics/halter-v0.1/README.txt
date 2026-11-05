X6 Halterzeichnungen v0.1 - 5. November 2026

INHALT UND GRENZEN
Bemasste Konstruktionszeichnungen und sechs echte CAD-Volumenkoerper:
H01 Sockel, H02 Stativ, H03A Linsen-/Filterfassung, H03B Deckring,
H04 Moduladapter, H05 Faserkoppleradapter. Alle Teile: DESIGN_HOLD.
Diese Teile sind eigene Entwuerfe. Sie sind keine Herstellerzeichnungen
und keine vollstaendige, einbaufertige Mechanik des Bell-Aufbaus.

PDF: neun A3-Blaetter, Einzelteilansichten 1:1 bei 100 % Druck.
DXF: neun Zeichnungsblaetter in Millimetern mit Ansichten und Bemasstexten.
Sie sind keine direkt verwendbaren CNC-Konturen: Rahmen, Text, Mittellinien
und mehrere Ansichten befinden sich ebenfalls im Modellbereich.
STEP: sechs einzelne Bauteile in Millimetern. Gewinde sind als Kernloecher
modelliert, nicht als Schraubenflaechen. Gewinde, Bohrspitzen, Kantenbruch
und Oberflaechenfinish nach Zeichnung herstellen; zuerst fachlich freigeben.

GRUNDLAGEN
800 x 600 mm Planflaeche und 75 mm Strahlhoehe stammen aus dem optischen
Szenariolayout. Die neuen mechanischen Masse sind Entwurfsentscheidungen.
D25.4 fuer H03 ist ein Szenario, kein bestaetigtes Liefermass.
H01 + H02 + H03A ergibt nominal 12 + 41 + 22 = 75 mm ohne Zwischenlagen.
Die +/-0.15-mm-Hoehenkette beruecksichtigt nur diese drei Laengen; optische
Zentrierung, Tischform, Klemmung und Temperatur sind darin nicht enthalten.
Sie ist keine zugesicherte optische Justagegenauigkeit.

BAUGRUPPEN
- MNT-03/MNT-04: H03 nur bei passenden Linsen-/Filtermassen, Randdicken,
  Kruemmungen und ausreichender freier Apertur; Zwischenlagen/Distanzring
  sind noch nicht ausgelegt. Keine unkontrollierte Kraft auf Glas ausueben.
- MNT-01: kinematische Spiegelhalter bleiben separate Bauteile.
- MNT-02: PBS-Klemmung und benoetigte Ports bleiben offen. Der 12.7-mm-
  PBS-Kandidat ersetzt die 10-mm-Annahme nicht ohne optische Neurechnung.
- Wellenplatten: benoetigen Rotationshalter; Analysator-HWP zudem Motor-
  und Referenzierungsfunktion. H03 ersetzt diese Funktionen nicht.
- OVEN-01: H04 ist lediglich ein Moduladapter; keine direkte Kristallfassung,
  kein ausgelegter Waermekontakt, keine TEC-/Sensor- oder Temperaturregelung.
- COUP-MNT: H05 ist lediglich ein Adapter; das Fuenfachsmodul bleibt separat.
- Z-STAGE: kein fertiger Linsen-Verstelltisch enthalten.

BEFESTIGUNGEN
H01 nimmt einen Schraubenkopf bis D10.5 x 6.0 mm auf. Bei Schraubenlaenge
12 mm ab Kopfauflage ergibt sich geometrisch 6.5 mm Eingriff in H02.
Kopfgeometrie, Gewindeauslauf, Vorspannung und Lastfall sind zu pruefen.
H02 besitzt M4 oben, M6 unten und ist ausschliesslich fuer H03 gezeichnet.
H04/H05 benoetigen einen anderen Stativabschluss mit M6 oben und eine
neu bestimmte Laenge. Kein Einbau mit dem gezeichneten H02 zugesichert.
M4-Verbindung H02/H03: Einschraubtiefe im Korpus maximal 5 mm. Drehmoment,
Sicherung und verbleibende Wanddicke sind in der Fertigungspruefung offen.

KOLLISION
H01 unter O04 und DM, jeweils auf der optischen Achse und parallel zum
globalen Raster angenommen: 35 mm Sockeltiefe bei 32.212 mm Achsabstand
ergibt 2.788 mm Ueberlapp, bei +10 mm O04-Hub 12.788 mm. Diese Anordnung
ist abgelehnt. Seitlicher Versatz oder gemeinsamer Traeger ist auszulegen.
Das ist eine konkrete bedingte Bauraumpruefung, keine globale Kollisions-
freigabe. Tatsachliche Modulkoerper, Schrauben, Kabel und Justierhuellen fehlen.
Optische Zentren sind keine Befestigungskoordinaten. Kein Grundplattenbohrplan.

FUER DIE FERTIGUNGSREVISION ERFORDERLICH
1. Exakte Bestellcodes mit Hersteller-CAD und Revisionsstand aller Module.
2. Linsendurchmesser, Rand-/Mittendicken, Kruemmungen und freie Aperturen.
3. Spiegel-/PBS-Groessen, Portzugang, Klemmflaechen und Achshoehen.
4. Ofenabmessungen, Montageflaechen, Temperaturbereich und Kabelwege.
5. Faserkoppler-/Rotationshalter-/Verstelltisch-Lochbilder und Stellwege.
6. Grundplattenmaterial, Dicke, Befestigungsraster und Last-/Driftbudget.
7. Kollisionsfreier Gesamtaufbau und Pruefung der Glasklemmung/Justage.
Fehlende Angaben bleiben OPEN, die Fertigungsfreigabe HOLD.

QUELLEN
https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/eb6022d19179e32e1e652502cdb5556911a4483e/experiments/photonic-two-qubit/optics/gaussian-layout-v0.1
https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/eb6022d19179e32e1e652502cdb5556911a4483e/experiments/photonic-two-qubit/optics/rfq-bom-v0.1/BOM_und_RFQ_Daten.json
Layout_Quelle.json und koordinaten_Quelle.csv sichern die verwendeten Daten.
Keine neuen Messwerte, Lieferzusagen oder Beschaffungsfreigaben.

REPRODUKTION UND PRUEFUNG
build.py erzeugt Zeichnungen und CAD-Dateien; Pfad P am Anfang anpassen.
Abhaengigkeiten: CadQuery 2.7.0, ezdxf 1.4.4, ReportLab und DejaVu-Schriften.
Die Parameter stehen im Quellcode; Bauteile.json dokumentiert die Ausgabe,
ist aber keine automatisch eingelesene Parameterdatei.
Geprueft: gueltige zusammenhaengende Volumenkoerper, STEP-Reimport und
Volumengleichheit, Bauteilaussenmasse, DXF-Audit/Einheiten, neun PDF-Blaetter
und visuelle Darstellung. Kein Prototyp gefertigt oder physisch geprueft.
SHA256SUMS.txt dokumentiert die urspruenglichen Paketdateien.
