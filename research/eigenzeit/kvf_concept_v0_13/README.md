# Eigenzeit v0.13 · Kausaler Vakuum-Feld-Vektor

**Forschungsentwurf · CONCEPT_ONLY · 1. November 2026**

Ziel ist ein metrologischer Teststand für Vakuumkorrelationen und kausale
Feldantwort. Der Arbeitsbegriff **Kausaler Vakuum-Feld-Vektor (KVF)** bezeichnet
einen endlichen Vektor definierter Messgrößen. Die Verbindung zur
Quantengravitation soll über überprüfbare Vorhersagen konkreter Modelle
untersucht werden.

Dieser Stand veröffentlicht Definitionen, einen Aufbauvorschlag und die
Anforderungen an den nächsten Modellvergleich. Es wurden dafür keine
Laborversuche und keine neuen numerischen Modellvergleiche durchgeführt.
Ein gebauter Teststand, eine erreichte 2-ppm-Feldmessung und ein Nachweis
quantengravitativer Effekte werden nicht behauptet.

## Dokumente

- [Messgrößen, Teststand und GUM-Verfahren](DESIGN.md)
- [Primärquellen und ihre Aussagegrenzen](SOURCES.md)
- [Maschinenlesbarer Arbeitsstand](STATUS.json)
- [Vorgänger v0.12: C01-Messdefinition und ausführbare GUM-Bilanz](../c01_gum_v0_12/README.md)

## Erste Ausbaustufe

Für zwei über festgelegte Raumzeitfenster gemittelte Feldobservablen werden
Eigenvarianzen, symmetrisierte Kreuzkorrelation und Kommutatorerwartungswert
als gemeinsame Messgrößen behandelt. Ihr Bezug zu den Detektorsignalen muss
durch ein kalibriertes Messmodell hergestellt werden. Korrelation und
Signalübertragung erhalten getrennte Prüfungen.

Ein elektrooptischer Aufbau mit zwei ultrakurzen Sondenpulsen ist ein
Literatur-gestützter Kandidat. Die in der Literatur verwendete kryogene
Konfiguration ist eine mögliche Forschungsplattform. Für eine frugale,
dezentral nachbaubare Variante sind Empfindlichkeit, thermische Beiträge und
Kosten gesondert zu prüfen; die vorhandene C01-Zählkette allein misst diesen
Feldvektor noch nicht.

## Nächster überprüfbarer Meilenstein

Zwei konkrete Modelle müssen Vorhersagen für dieselben beobachtbaren
Detektorsignale liefern. Danach werden unterscheidende Komponenten, erlaubte
Störparameter, notwendige Messunsicherheit, Fehlentscheidungsrisiken und
Messaufwand festgelegt. Das Ergebnis darf ausdrücklich lauten, dass die
Modelle mit dem verfügbaren Aufbau nicht unterscheidbar sind.

**Aktueller Status:** Modellpaar offen; Detektortransfer offen;
Empfindlichkeitsrechnung nicht ausgeführt; Laborfreigabe HOLD.

Die 2-ppm-Grenze von v0.12 bleibt an die dort definierte C01-Größe gebunden.
Für den KVF sind Einheiten, Bezugsgrößen und absolute Toleranzen erst noch
festzulegen. Veröffentlichung und bestandene Repository-Prüfungen ändern
diesen wissenschaftlichen Status nicht.

## Ausgeführter Kontrollvergleich v0.14

[Der erste KVF-Kontrollvergleich](../kvf_control_v0_14/README.md) rechnet zwei freie Skalarfeldmodelle in derselben flachen Raumzeit mit einer gemeinsamen idealisierten Auslesebeschreibung durch. Er enthält ein bedingtes endliches Messbudget, gemeinsame GUM-Auswertung und ein explizites Rausch-Gegenbeispiel. Der Antwortkanal und die Feldanwendung bleiben offen.
