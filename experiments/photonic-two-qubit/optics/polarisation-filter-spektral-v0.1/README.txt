X6 Polarisationstransfer, Filterbudget und spektrale Prüfmatrix v0.1
5. November 2026. Basis: main f97307cd93070d1a57a62cb2e1c1d4dc232fb45e.

Die ideale Port-/Polarisationszuordnung, die Rechenvorschriften und der Prüfvertrag sind ausgearbeitet. Physische Phase, Serienfilterkurven, Spektren und elektrische Detektorketten-Abnahme fehlen. Hardware NOT_RUN, BOM HOLD. Neue Budgetzuteilungen sind als solche markiert; sie ersetzen keine bestehenden CHSH-Gates.

Inhalt: PDF-Bericht, bearbeitbares XLSX mit Filterrechnung und 23 Prüfzeilen, Spezifikation.json, Rechenergebnisse.json, zwei Messdatentemplates, technische Filter-Datenanfrage, analysis.py und test_analysis.py. Vorlagen sind absichtlich leer. Keine Messwerte wurden erzeugt oder als Laborwerte ausgegeben.

Reproduktion (Python >=3.10, nur Standardbibliothek):
  python analysis.py
  python -m unittest -v test_analysis
  python analysis.py --spectral ausgefuellte_Spektraldaten.json

Spektraldaten beziehen sich auf dieselben Laborports A/B nach der installierten Filter-/Sammelkette und vor der Polarisationsanalyse. Zwei Intensitätsmatrizen allein liefern nur eine obere Schranke für den kohärenten Überlapp. Die Phase muss unabhängig bestimmt werden. Das Programm zertifiziert keine Messunsicherheit und erteilt keine Hardwarefreigabe. Eine Vorlage mit leeren Achsen wird mit Fehlermeldung abgewiesen.

Die Berechnung von gamma aus sqrt(J) und einer Phase je Rasterzelle setzt kohärente komplexe Amplituden voraus. Bei gemischten Zuständen, Pumprauschen oder unaufgelösten inkohärenten Moden ist ein gegenseitiges Kohärenz-/Dichtematrixmodell erforderlich. Die integrierte Polarisationsmessung prüft die tatsächlich erhaltene Kohärenz; eine Phase allein zertifiziert das Amplitudenmodell nicht.

T_H/T_V-Kurven und komplexe spektrale Phase sind verschiedene Eingaben. Reflektions-/Beschichtungsphasen, Basiswechsel und die mittlere HWP-Phase gehören in die Gesamtübertragung. Eine physische HD-Achse a=(X+Z)/sqrt(2) ergibt +45 Grad für k=-Y und -45 Grad für k=+Y in u=Z cross k,v=Z. Motorwinkel sind keine Achsenmessung.

Die XLSX-Formeln rechnen Szenario und ein getrenntes leeres Messwertfeld. Alle Messwerte müssen obere/untere konservative Grenzen gemäß Bericht enthalten. Ein numerisch erfülltes Filterbudget ist keine Gesamtfreigabe. Desktop-Excel wurde nicht ausgeführt. Bibliotheks-Rechen- und Renderprüfung sind in Validierung.json dokumentiert.

Veröffentlichte Quelldokumente bleiben unverändert. Dies ist ein ergänzendes Arbeitspaket; Lieferanten wurden nicht kontaktiert.
