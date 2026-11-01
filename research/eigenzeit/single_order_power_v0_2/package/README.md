# X6 Eigenzeit · Trennleistung einer Einzelordnung v0.2

**Entscheidung.** Für flach gegen de Sitter h=1/2 genügt eine einzige Ordnung mit 30.000 Ereignissen im deklarierten Modell. Der vollständige Paaranteil sichert in beiden Richtungen mindestens 80 % Trennleistung bei höchstens 5 % Fehlalarm. Die notwendige Ereigniszahl für jeden Test steigt von 8.999 auf 9.857. Die genaue optimale Größe ist offen.

## Inhalt

Bericht.pdf und BEWEIS.md geben die Aussage, Voraussetzungen und Nachweise an. design.json und FREEZE.sha256 dokumentieren die lokale Festlegung vor den vier Implementierungsbeispielen. certificate.json enthält nach außen gerundete Risikogrenzen, checks.json die unabhängigen numerischen und algebraischen Kontrollen. examples.json sichert Zählungen und Datenfingerabdrücke aller vier Fälle. source/ enthält die benutzten veröffentlichten Vorwärtsrechnungen, den Affinitätscode aus v0.1 und die Lizenz. Die vier Beispielwolken sind aus ihren getrennten Seed-Namen reproduzierbar. Ihre großen Matrizen werden vorübergehend angelegt.

## Wiederholen

Python 3, NumPy, SciPy und für die vollständigen Beispiele ein C++17-Compiler auf einer Little-Endian-Plattform. Referenzversionen stehen in environment.json. Die wissenschaftliche Zertifizierung selbst verwendet rationale Zahlen und ganze Zahlen. In dieser Version importieren die eingebundenen Referenzmodule auch die numerischen Bibliotheken. Führe die Prüfungen ohne Python-Optimierungsoptionen aus, damit die Gegenkontrollen mit assert aktiv bleiben.

```sh
sha256sum -c MANIFEST.sha256
sha256sum -c FREEZE.sha256
python -B certificate.py > /tmp/x6-single-power-certificate.json
cmp certificate.json /tmp/x6-single-power-certificate.json
python -B audit.py certificate.json > /tmp/x6-single-power-checks.json
cmp checks.json /tmp/x6-single-power-checks.json
python -B examples.py > /tmp/x6-single-power-examples.json
cmp examples.json /tmp/x6-single-power-examples.json
```

Für die Beispielsimulation benötigt der vollständige Relationstest vorübergehend 112,5 MB pro 30.000er-Ordnung. Die separate Kontrolle des Abfrageinterfaces nutzt eine etwa 1,15 GB große Sparse-Datei mit wenigen tatsächlich belegten Seiten. Plattformunterschiede bei Simulationen können sich in den Koordinatenhashes niederschlagen. Das mathematische Zertifikat setzt die Modellgesetze voraus.

## Anwendung auf eine Beobachtung

Für eine vorliegende vollständige strikte Ordnung wird jede Zeile der booleschen Relation mit kleinster Bitposition zuerst gespeichert. Es folgen direkt N Zeilen mit je ceil(N/8) Bytes, ohne Dateiheader. Ein gesetztes Bit bedeutet „Zeilenereignis liegt vor Spaltenereignis“. Die Diagonale ist null. Die Vollständigkeit und Transitivität der gelieferten Ordnung sind Eingabevoraussetzungen. Die Zufallspaarung benötigt nur ihre Vergleichbarkeitsabfragen. Werden die beiden gerichteten Matrixeinträge gelesen, müssen beide Richtungen vorab wohldefiniert sein.

```sh
python apply_order.py full_order eine_30000er_ordnung.bin
python apply_order.py matching eine_96000er_ordnung.bin
python decision.py full_order 30000 44887925
```

Für eine vorab unabhängig festgelegte Wiederholung der Paarung kann bei matching ein Seed mit --seed angegeben werden. Ein erneutes Auswürfeln derselben Ordnung bis zum gewünschten Ergebnis fällt außerhalb des Zertifikats. Kalibrier- oder Testwolken gehen bei der Anwendung nicht in die Entscheidung ein.
