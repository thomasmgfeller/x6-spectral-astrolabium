OPTIKPLAN v0.1 | 23.10.2026 | Erstellt für Thomas Gfeller

Ziel: technischer Plan für eine Typ-II-ppKTP-Sagnac-Quelle, vierkanalige
Detektion und einen vorab definierten CHSH-Labornachweis.

STATUS: ENTWURF. Sämtliche optischen und elektrischen Hardwareprüfungen
sowie der reale CHSH-Nachweis sind NOT_RUN. Keine Fertigungsfreigabe.

Dateien
Optikplan_v0_1.pdf          Lesefassung des technischen Plans
Optikplan_v0_1.docx         Bearbeitbare Fassung
protocol_v0_1.json         Messparameter und noch auszufüllende Startfelder
schedule.csv              80 vorab erzeugte Messsegmente, 2400 s Nettomesszeit
chsh_check.py              Prüfer nur für die bedingte Zählstatistik
test_chsh_check.py         Mathematische Randfälle und Negativkontrollen
counts_SYNTHETIC.csv       Synthetisches Rechenbeispiel, keine Messdaten
synthetic_result.json      Ergebnis des synthetischen Beispiels
software_test_report.json  Tatsächlicher Ausführungsnachweis der Softwaretests
requirements.txt          Abhängigkeiten der geprüften Auswertung
SHA256SUMS.txt             Hashes der Paketdateien

Ausführung in einer geeigneten Python-Umgebung
  python -m pip install -r requirements.txt
  python -m unittest -v test_chsh_check
  python chsh_check.py counts_SYNTHETIC.csv --data-kind synthetic

Echte Daten werden aus den vollständig archivierten Rohzeitstempeln nach
Abschnitt 8 aggregiert. Die CSV hat genau vier Zeilen, in jeder Zeile vier
rohe, nicht hintergrundbereinigte Zahlen. Reihenfolge: ++, +-, -+, --.
Der Rohdatenadapter und der Paaralgorithmus sind noch zu implementieren.
Der Prüfer zertifiziert keine Hardware, Messannahmen oder Datenintegrität
und vergibt niemals selbst die Gesamtfreigabe PASS_CONDITIONAL_CHSH.

Vor dem Lauf müssen die Nullwerte in freeze_required_before_run ausgefüllt,
alle Hardwaretore dokumentiert und Konfiguration samt Messplan gehasht sein.
Die JSON-Vorlage ist ausdrücklich nicht bereits eingefroren oder lauffreigegeben.

Keine frühe Beendigung oder Verlängerung aufgrund des CHSH-Ergebnisses.
Nur ein primärer Lauf ist vorgesehen. Neue Versuche nach Ergebnisansicht
benötigen eine neue Festlegung des Fehlerbudgets, wenn eine gemeinsame
Fehlerwahrscheinlichkeit für mehrere Tests beansprucht wird.

Geltungsbereich der Statistik
Das einseitige 99-Prozent-Intervall beruht auf vier Bonferroni-kombinierten
Clopper-Pearson-Untergrenzen. Innerhalb jedes Settings wird iid-Bernoulli-
Parität bedingt auf die Paarzahl vorausgesetzt. Fair Sampling einschließlich
Koinzidenzselektion und ein stationäres Messmodell sind zusätzliche Annahmen.
Keine Aussage über einen schlupflochfreien Bell-Test oder Quantenrechenvorteil.
