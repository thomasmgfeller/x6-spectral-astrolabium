# Primärquellen und Herkunft

Geprüft bzw. im aktuellen Arbeitsgang herangezogen am 11. Oktober 2026.

1. Norland Products, NOA61 Technical Data Sheet:
   https://norlandproducts.com/wp-content/uploads/2025/02/Norland-Products-NOA-61-TDS.pdf
   Bezug: UV-Wellenlängenbereich, Dosis, lampenspezifische Vor-/Endhärtung,
   Alterung und Grenzen der Übertragung von Materialangaben auf eine Baugruppe.
2. Thorlabs, Polaris-Mount-Temperaturprüfung:
   https://www.thorlabs.com/catalogpages/V21/246.pdf
   Bezug: Laser/PSD als Messung der Strahl-/Winkelrückkehr nach Temperaturzyklen.
3. NIST / Christensen et al., Analysis of coincidence-time loopholes in experimental Bell tests:
   https://www.nist.gov/publications/analysis-coincidence-time-loopholes-experimental-bell-tests
   https://arxiv.org/abs/1503.07573
   Bezug: Koinzidenzauswahl kann einen Bell-Wert verzerren; eine klassische Quelle
   kann bei ungeeigneter Auswertung eine scheinbare Verletzung erzeugen.
4. NIST / Knill et al., Bell inequalities for continuously emitting sources:
   https://www.nist.gov/publications/bell-inequalities-continuously-emitting-sources
   Bezug: Bedeutung fester Beobachtungsperioden und zusätzlicher Annahmen.
   Unser Kern implementiert nicht die dortige Distanz-Bell-Statistik.
5. GHDL, offizielle Dokumentation:
   https://ghdl.github.io/ghdl/getting.html
   Bezug: frei verfügbarer Simulator; tatsächliche Version separat protokolliert.
6. Hamamatsu, Physics and operation of the MPPC silicon photomultiplier:
   https://hub.hamamatsu.com/us/en/technical-notes/mppc-sipms/physics-and-operation-of-the-MPPC-silicon-photomultiplier.html
   Bezug: Nachpulse und Grenzen ihrer Identifikation. Keine Übernahme numerischer
   SiPM-Zeitkonstanten auf einen noch nicht ausgewählten Einzelphotonendetektor.

Interne Ausgangsartefakte:
- Photonische_Messkette_v0_1_Digitalkern.zip: H/A/B-Kern mit unsigned64-Zeitstempeln,
  Handshake und Watermark; Mehrfachtreffer werden zu Hit-Flags zusammengefasst.
- Photonische_Messkette_v0_1_Auswertung.zip: vier Herald-Kategorien; alpha=0.05 ist
  ein statistisches Fehlerniveau, kein Störquoten-Limit.

Die neue feste Fensterarchitektur, Zählerzuordnung, Prüfprogramme und der
Hoeffding-basierte Bericht sind eigenständige Entwurfsentscheidungen. Aus den
Quellen wird keine Herstellerfreigabe oder physische Validierung dieses Moduls
abgeleitet.

Die v0.7-Hardware-, UART- und Preisrecherche ist separat in HARDWARE.md mit direkten Hersteller-/Anbieterlinks dokumentiert.
