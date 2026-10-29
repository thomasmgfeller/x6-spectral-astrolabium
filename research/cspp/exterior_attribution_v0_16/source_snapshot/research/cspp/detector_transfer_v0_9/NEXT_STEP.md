# Anschlussentscheidung nach v0.9

**Jetzt:** deterministische Methodenentwicklung. **Noch nicht:** neue
Bestätigungswolken, optomechanischer Hardwareaufbau, Dirac, Astrometrie oder
kosmologische Anpassung.

## 1. Detektorintegration gezielt verbessern

Die aktuelle Boxhülle verliert gemeinsame Abhängigkeiten der kausalen
Indikatoren und Gewichte. Ein nächster Kandidat sollte Teilvolumina von
Lichtkegeln im festen Detektor genauer integrieren oder die Boxen an den
Kausalgrenzen ausrichten. Er muss zunächst dieselben analytischen
Ein-Ereignis-Kontrollen und vorzeichenwechselnden Mehr-Ereignis-Kontrollen
bestehen. Eine veränderte Zellenzahl oder Methode ist eine neue dokumentierte
Entwicklungsversion; v0.9 bleibt unverändert. Eine größere Punktwolke behebt
diesen Quadraturengpass nicht automatisch.

## 2. Anfangsdatenabbildung vor einer Rauschinterpretation prüfen

Auf drei der acht festgelegten Wolken überträgt die kompakte H1-History kein
einziges nichtverschwindendes Quellendatum. Ein neuer Adapter müsste die
unveränderten f,g mit hergeleiteter Fehlerkontrolle auf die tatsächlich
benötigte diskrete Vergangenheit übertragen. Er darf weder die Quelle
verbreitern, Wellenlängen verändern, zusätzliche Punkte unbemerkt einfügen
noch günstige Wolken nachziehen. Orakelhistorie kann als Vergleich dienen,
aber nicht als nachgewiesener Anfangsdatenadapter ausgegeben werden.

## 3. Erst danach unabhängige Transferprüfung festlegen

Erforderlich sind eine vorab berechenbare Mittelwert-/Kovarianzvorhersage,
ein kontrollierter Bereich für etwaige Linearisierung, eine hinreichend
enge kompakte Kontinuumsdetektorreferenz und ein vollständiges Fehlerbudget.
Die bisherige punktweise Paar-Kovarianz muss auf verschiedene
Beobachtungspunkte erweitert oder eine andere begründete Vorhersagemethode
entwickelt werden. Der Detektor und die Quellen bleiben physikalisch fest.

Vor frischen Daten sind Populationsstatistik, Stichprobenumfang/Power,
Konfidenzrisiko, Umgang mit seltenen großen Werten und Ressourcenstopps
öffentlich zu registrieren. Das Modell muss anschließend sowohl seine
stochastischen Vorhersagen treffen als auch die angestrebten
makroskopischen Referenzbedingungen erfüllen. Diese zwei Aufgaben erhalten
getrennte Entscheidungen. Ein plausibles Rauschspektrum allein genügt nicht.

## 4. Weiterführende Anwendungen

Ein lösbares Wellen-/Oszillatormodell kann als unabhängige Methodenkontrolle
helfen. Optomechanik benötigt eine begründete Kopplung an eine mechanische
Observable. Testmassen und astrometrische Winkel verlangen zusätzlich eine
Geometrie-/Krümmungsantwort; Kosmologie benötigt auch Hintergrunddynamik und
Zustandsannahmen. Keine dieser Erweiterungen erhält durch v0.9 eine
physikalische Freigabe.
