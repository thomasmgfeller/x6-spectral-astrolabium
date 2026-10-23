# Optikplan v0.1

**Entwurf · 23.10.2026 · Hardware und realer CHSH-Nachweis: NOT_RUN**

[PDF lesen](Optikplan_v0_1.pdf) · [DOCX bearbeiten](Optikplan_v0_1.docx) · [Vollständiges Prüfpaket herunterladen](../../downloads/Optikplan_v0_1_Pruefpaket.zip)

Der 13-seitige Plan spezifiziert eine 405-nm-Pumpe, eine Typ-II-ppKTP-Sagnac-Quelle für Photonenpaare um 810 nm, zwei lokale Polarisationsanalysatoren und vier Detektorkanäle. Er enthält Bauteilanforderungen, die elektrische Schnittstelle zur Messkette und ein vorab definiertes CHSH-Abnahmeprotokoll. Beschaffung, maßstäblicher Aufbau, elektrische Qualifikation und optische Abnahme stehen noch aus.

## Umfang und Schnittstelle

| Teil | Festlegung |
|---|---|
| Quelle | CW-Pumpe bei 405 nm, 10-mm-Typ-II-ppKTP im Sagnac-Interferometer; Zielzustand Ψ− |
| Analyse | Je Arm Halbwellenplatte und Polarisationsstrahlteiler; vier Si-Einzelphotonendetektoren |
| Kanäle | 0 = A+, 1 = A−, 2 = B+, 3 = B−; gemeinsame Zeitbasis |
| Referenzsignale | Positive TTL-Impulse der spezifizierten SPCM-Option; genau ein 50-Ω-Abschluss gegen Masse am Empfänger. Der CML-Entwicklungspfad benötigt einen eigenen Empfänger und eine andere Terminierung. |
| Ereignisformat | 24 Byte je Ereignis; bei insgesamt 400 kcps 9,6 MB/s. Der bisherige UART-Pfad ist dafür nicht ausreichend. |
| Messplan | 20 Zyklen × 4 Einstellungen × 30 s = 2400 s Nettomesszeit, zuzüglich Positionierung und Einschwingen |
| Koinzidenz | Festes 2-ns-Fenster; eindeutige zeitbasierte Paare nach der im PDF definierten Auswahlregel |
| Primärstatistik | Vorzeichenfestes T = −E00 − E01 − E10 + E11; keine Untergrundsubtraktion |
| Statistische Schwelle | Mindestens 2000 Paare pro Einstellung und einseitige, Bonferroni-kombinierte 99-%-Untergrenze für T > 2 |

Die Gesamtfreigabe setzt zusätzlich alle technischen Tore und die ausdrücklich akzeptierten Modellannahmen voraus: iid-Bernoulli-Parität innerhalb jeder Einstellung, bedingt auf die Paarzahl; stationärer Zustand und Messabbildung; Fair Sampling einschließlich Koinzidenzselektion. Das ist ein bedingter Labornachweis. Ein schlupflochfreier Bell-Test, geräteunabhängige Sicherheit oder Quantenrechenvorteil werden nicht behauptet.

## Dateien

| Datei | Zweck |
|---|---|
| [Optikplan_v0_1.pdf](Optikplan_v0_1.pdf) / [DOCX](Optikplan_v0_1.docx) | Vollständige Spezifikation, Abnahmetore und Quellen |
| [protocol_v0_1.json](protocol_v0_1.json) | Parameter und vor Messbeginn auszufüllende Felder |
| [schedule.csv](schedule.csv) | 80 vorab erzeugte Messsegmente |
| [chsh_check.py](chsh_check.py) | Bedingte Statistik aus vier Zähltabellen |
| [test_chsh_check.py](test_chsh_check.py) | 11 Softwaretests, einschließlich Vorzeichen- und Negativkontrollen |
| [counts_SYNTHETIC.csv](counts_SYNTHETIC.csv) / [Ergebnis](synthetic_result.json) | Ausschließlich synthetisches Rechenbeispiel |
| [software_test_report.json](software_test_report.json) | Ursprünglicher Ausführungsnachweis |
| [requirements.txt](requirements.txt) / [SHA256SUMS.txt](SHA256SUMS.txt) | Abhängigkeiten und Identität der Originaldateien |
| [README.txt](README.txt) | Unveränderte Anleitung aus dem Prüfpaket |

## Softwareprüfung reproduzieren

Getestet mit Python 3.12. Eine virtuelle Umgebung wird empfohlen.

```bash
cd experiments/photonic-two-qubit/optics/optikplan-v0.1
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
sha256sum -c SHA256SUMS.txt
python -m unittest -v test_chsh_check
python chsh_check.py counts_SYNTHETIC.csv --data-kind synthetic
```

Das synthetische Beispiel ergibt T = 2,8288 und die 99-%-Untergrenze 2,7474337305888685. Der Prüfer bewertet ausschließlich die Zählstatistik. Er lässt Hardware, Rohdatenintegrität, Modellannahmen und Gesamtfreigabe ausdrücklich auf `NOT_ASSESSED`.

GitHub Actions führt die Prüfsummenprüfung, die 11 Tests und das synthetische Beispiel im Job `optikplan-statistics` des Workflows [Photonic Reference](../../../../.github/workflows/photonic-reference.yml) erneut aus. Frische CI-Ergebnisse werden als Workflow-Artefakt gespeichert; der ursprüngliche Testbericht bleibt unverändert.

## Vor einer echten Messung

Die Nullfelder unter `freeze_required_before_run` müssen ausgefüllt, Kalibrierungen und Hardwaretore dokumentiert und Konfiguration samt Messplan gehasht werden. Die Vorlage ist noch nicht als ausführbarer Messlauf eingefroren. Der Rohdatenadapter und der im Plan definierte Paaralgorithmus sind noch zu implementieren und zu prüfen.

Vorgesehen ist ein primärer Lauf ohne ergebnisabhängige Verlängerung oder frühe Beendigung. Negative Kontrolle, Ausfallregeln und Abnahmetore stehen im PDF. Wiederholte Versuche nach Ergebnisansicht benötigen einen neuen Plan für das gemeinsame Fehlerbudget.

## Einordnung und Herkunft

Dieses Paket ergänzt den [optischen Funktionsentwurf](../../OPTICAL_DESIGN.md) und das [Laborprotokoll](../../LAB_PROTOCOL.md). Die ältere [v0.7-Digitalreferenz](../../reference/sagnac_v0_7/README.md) bleibt eine separate Entwicklungsstufe: Ihre UART-Übertragung und Ereignisdefinition sind nicht automatisch eine Umsetzung des neuen Rohdatenprotokolls. Auch die Kaskoden-Frontend-Entwürfe sind noch keine qualifizierten Vierkanal-Detektoren.

Alle zwölf Originaldateien sind byteidentisch mit dem bereitgestellten Prüfpaket. Dieses README und die Repository-Verlinkung wurden für die Veröffentlichung ergänzt. Der SHA-256-Wert des ZIP lautet:

```text
08846b1759c4ddc62b1f904756d04d156ce7706f25b5699e010e98dc8cd8d366
```

Für die ursprünglichen Projektbeiträge gilt der [Lizenzumfang des Repositorys](../../../../LICENSE_SCOPE.md); zitierte Herstellerunterlagen und Veröffentlichungen behalten ihre jeweiligen Rechte. Quellen werden im PDF angegeben und nicht als Volltexte mitgeliefert.
