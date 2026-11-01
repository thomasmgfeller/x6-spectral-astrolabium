# Eigenzeit v0.14 · Erster KVF-Kontrollvergleich

Ein masseloses und ein massives freies Skalarfeld werden in derselben flachen Raumzeit mit einer gemeinsamen idealisierten Auslesebeschreibung verglichen. Unter den festgelegten Modell- und Kalibrierannahmen reichen **41.045 unabhängige Messpaare** am ausgewählten Abstand für eine Fehlerschranke von unter **1 % je Entscheidungsrichtung**. [Bericht (PDF)](Eigenzeit_KVF_Kontrollvergleich_v0_14.pdf) · [Vollständiges Prüfpaket (ZIP)](Eigenzeit_KVF_Kontrollvergleich_v0_14_Pruefpaket.zip)

| Ergebnis | Wert |
|---|---:|
| Nominale normierte Korrelation bei Abstand 3, M0 | 0,28549938 |
| Nominale normierte Korrelation bei Abstand 3, M1 | 0,20998236 |
| Vorzeichenregel | M0 bei mehr als 23.645 gleichen Vorzeichen aus 41.045 Paaren, sonst M1 |
| Synthetische Endpunktkontrolle | 18 / 20.000 und 23 / 20.000 Fehlentscheidungen |
| GUM-Auswertung | Drei Korrelationen mit gemeinsamer Kovarianz und Verteilungsfortpflanzung |

Die Fehlerschranke setzt zentrierte gaußförmige Rohdaten, unabhängige Versuche, bekannte Abstände, die vorgegebene Breitenunsicherheit und unabhängig begrenztes Detektorrauschen voraus. Diese Bedingungen sind hier Modellannahmen. Die drei Einstellungsblöcke für den vollständigen Korrelationsvergleich umfassen insgesamt 123.135 Paare je Modell. Die 41.045 Paare beziehen sich auf die primäre Entscheidung bei Abstand 3. [Vertrag](CONTRACT.json) · [Herleitung](DERIVATION.md) · [GUM-Schritte](GUM.md)

Ein Gegenbeispiel erzeugt außerhalb der Kalibriergrenzen durch korreliertes Rauschen exakt dieselben Beobachtungsverteilungen für beide Modelle. Zusätzliche Messungen lösen diese Mehrdeutigkeit nicht auf. [Gegenkontrollen](records/controls.json) · [Primärquellen](SOURCES.md)

**Die Feldanwendung bleibt auf HOLD_FIELD_TRANSFER.** Der Antwortkanal ist ungemessen. Reale Kalibrierung, Quantennachweis gegenüber klassischen Modellen und ein Quantengravitationstest stehen aus. Die C01-Grenze von 2 ppm wird nicht auf die neuen Messgrößen übertragen. [Ergebnisübersicht](records/summary.json) · [Vorgänger v0.13](../kvf_concept_v0_13/README.md)

## Reproduktion

Mit Python 3.12 im Wurzelverzeichnis des Repositorys ausführen:

```sh
python -m pip install -r research/eigenzeit/kvf_control_v0_14/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/eigenzeit/kvf_control_v0_14/publication_check.py --replay
```

Der Prüflauf verifiziert die Originale, alle 42 Archiveinträge, beide dokumentierten Rechenstände und die übernommenen v0.13-Quellen. Anschließend wird das vollständige Archiv in ein temporäres Verzeichnis entpackt und sein Reproduktionsprogramm gestartet. Sieben Ergebnisprotokolle und acht Rohdatendateien werden erneut erzeugt und mit dem Archiv verglichen. Im ursprünglichen Lauf waren alle bytegleich; der plattformübergreifende Zahlenvergleich weist seine engen Toleranzen im Code aus. [Reproduktionsnachweis](records/replay.json) · [Separate Rechenkontrollen](records/check.json)

Die vollständigen Rohdaten und das ursprüngliche Paket-README liegen im ZIP. Die direkt sichtbaren Programme und Protokolle sind unveränderte Auszüge. Der Einstieg für die Reproduktion im Repository ist `publication_check.py`; `reproduce.py` wird innerhalb des vollständigen Archivs ausgeführt.

Die anfängliche Fixierung vor Datenerzeugung und eine nachträgliche ergebnisneutrale Präzisierung der gerichteten Nenner-Rundung sind dokumentiert. Die Daten wurden beibehalten. [Arithmetikprüfung](development/REVIEW.json) · [Veröffentlichungsnachweis](PUBLICATION.json)

## Ausgeführter Antworttest v0.15

[Der kontrollierte KVF-Antwortkanal](../kvf_response_v0_15/README.md) ergänzt eine zeitversetzte Quelle und idealisierte Sonde mit expliziter Rückwirkung, kausalen Nullkontrollen und einem bedingten endlichen Messbudget. Die ursprüngliche Einzelabweichung und der separate GUM-Überdeckungs-Audit bleiben dokumentiert. Die reale Feldanwendung bleibt HOLD_FIELD_TRANSFER.
