# RAX-W1: exakte Wolfram-Gegenprüfung

Registerstand: 2026-10-17. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: ced51c97b03525acc5d9ff907e175afce740974a

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ced51c97b03525acc5d9ff907e175afce740974a/docs/research/rax/wolfram-check-v0.1/README.md)

## Dokumentierte Aussage

44 ausgewählte U1-Matrizen, zehn gültige Reduktionen und 34 beabsichtigte Verletzungen werden exakt abgeglichen.

- [docs/research/rax/wolfram-check-v0.1/RAX_W1_Exakte_Gegenpruefung_v0_1_Paket.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ced51c97b03525acc5d9ff907e175afce740974a/docs/research/rax/wolfram-check-v0.1/RAX_W1_Exakte_Gegenpruefung_v0_1_Paket.zip): Gespeicherte Wolfram-Antworten und unabhängiger Python-Prüfer; interne Post-hoc-Prüfung.

## Reproduzieren

Python 3.12/Standardbibliothek. Offline-Prüfung startet keinen Wolfram-Kernel.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-rax-w1
cd x6-rax-w1
git checkout --detach ced51c97b03525acc5d9ff907e175afce740974a
python3 -m zipfile -e docs/research/rax/wolfram-check-v0.1/RAX_W1_Exakte_Gegenpruefung_v0_1_Paket.zip /tmp/x6-hub-rax-w1
cd /tmp/x6-hub-rax-w1/RAX_W1_Exakte_Gegenpruefung_v0_1
python3 -B verify_package.py
python3 -B verify.py
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Externe Reproduktion bzw. neuer Wolfram-Lauf mit eigener Umgebung; Aussagebereich nicht auf U2 ausdehnen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
