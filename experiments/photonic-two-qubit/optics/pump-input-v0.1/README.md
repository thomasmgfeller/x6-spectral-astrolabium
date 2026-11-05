# Pump-Eingangsprofil und messbare Systemziele v0.1

**5. November 2026 · Spezifikation erstellt · Hardwaremessungen NOT_RUN · Beschaffung HOLD**

Das Paket definiert den messbaren Eingang der nächsten Gaussian-Beam-Rechnung für die 405/810-nm-Sagnac-Quelle. Es ergänzt den [Optikplan v0.2](../optikplan-v0.2/README.md) und übernimmt das bedingte CHSH-Protokoll aus [Optikplan v0.1](../optikplan-v0.1/README.md). Es enthält keine Messung einer vorhandenen Pumpquelle und keine freigegebene Bestellstückliste.

## Dateien

- [Spezifikation als ausfüllbares PDF](X6_Pump_Eingangsprofil_Systemziele_v0_1.pdf): acht Seiten, 24 interaktive Felder.
- [Vollständiges Prüfpaket](X6_Pump_Eingangsprofil_v0_1_Pruefpaket.zip): unverändertes Originalarchiv.
- [Pumpen-Datenvorlage](pump_profile.template.json): unbekannte Istwerte sind `null`, Messstatus ist `NOT_RUN`.
- [Systemziele](system_targets.json): 29 Einträge mit Einheit, Herkunft, Prüfregel und Zielart.
- [Messplan](measurement_plan.json): sieben Arbeitsschritte ohne automatische Geräteansteuerung.
- [Ursprüngliche Gebrauchshinweise](README.txt) und [Paketprüfsummen](SHA256.json).

PDF, Archiv und extrahierte Originaldateien werden unverändert veröffentlicht. Die Angaben im ursprünglichen README beschreiben den Stand ihrer Erstellung vor dieser Veröffentlichung. Diese Begleitseite und der Repository-Herkunftsnachweis dokumentieren die Publikation.

## Bezugsebenen

| Ebene | Definition |
|---|---|
| P0 | Nach Laser und festem Kollimator, vor Abschwächer und Polarisationspräparation |
| P1 | Unmittelbar vor Fokuslinse O04, hinter Abschwächer und Pump-HWP/QWP; Ursprung der räumlichen Eingangscharakterisierung |
| PC | Einfallende Leistung an der ersten Kristallfläche je Richtung; Gesamtleistung ist die Summe beider Beiträge |

## Ziele und Grenzen

| Größe | Vorgabe | Einordnung |
|---|---|---|
| Pumpe | Nominal 405 nm, FWHM ≤ 0,10 nm | Tatsächliches Spektrum und Gerät bleiben offen |
| Kristall-Pumpleistung | 0,1 bis 3 mW, im Nachweislauf ±2 % um den eingefrorenen Wert | Beide Übertragungswege kalibrieren |
| Strahlqualität | Bevorzugt M² ≤ 1,3 je Hauptachse | Neues Auslegungsziel; höherer Wert verlangt angepasste Modellierung |
| Polarisationsgrad an P1 | ≥ 0,99 | Neues technisches Ziel; elliptische Sollpolarisation ist zulässig |
| Rohe Sichtbarkeit | H/V und D/A jeweils ≥ 0,90 | Kalibrierziel; keine Hintergrundsubtraktion |
| Mindestdaten | 2000 eindeutige Paare je Setting in jeweils 600 s | Fester CHSH-Messplan, keine nachträgliche Verlängerung |
| Zeitantwort | Optischer Paarpeak FWHM ≤ 1 ns | Primärfenster insgesamt 2 ns |

100–180 µm Pump-Taillenradius und f = 200–300 mm bleiben Suchbereiche. Der nächste Schritt benötigt das tatsächliche Pumpmodell, das gemessene P1-Strahlprofil mit Unsicherheiten und die Glas-/Freiraumwege. Die neue Spezifikation ersetzt die Szenarioparameter des Optikplans v0.2 nicht durch vermeintliche Messwerte. Grenzwerte für spektrale Drift, Strahlwanderung und CW/CCW-Fokusabweichung folgen erst aus dem QPM-, Kopplungs- und Toleranzbudget.

`VERIFIED` bezieht sich auf eine benannte Eigenschaft mit Evidenz. `OPEN` kennzeichnet fehlende Information, `HOLD` eine gesperrte Freigabe. Der unabhängige Ausführungsstatus `NOT_RUN` bleibt erhalten, bis die jeweilige Messung tatsächlich vorliegt. Die JSON-Dateien sind Datenvorlagen, keine Freigabesoftware und kein JSON Schema.

## Integrität prüfen

Im Paketverzeichnis:

```bash
python - <<'PY'
import hashlib, json, zipfile
from pathlib import Path
p = Path('.')
hashes = json.loads((p / 'SHA256.json').read_text())
for name, digest in hashes.items():
    assert hashlib.sha256((p / name).read_bytes()).hexdigest() == digest, name
with zipfile.ZipFile(p / 'X6_Pump_Eingangsprofil_v0_1_Pruefpaket.zip') as z:
    assert z.testzip() is None
    assert set(z.namelist()) == set(hashes) | {'SHA256.json'}
    for name in z.namelist():
        assert z.read(name) == (p / name).read_bytes(), name
profile = json.loads((p / 'pump_profile.template.json').read_text())
assert profile['hardware_status'] == 'NOT_RUN'
assert profile['procurement_status'] == 'HOLD'
assert all(x['value'] is None and x['measurement_status'] == 'NOT_RUN'
           for x in profile['measurements'].values())
print('PASS: Originaldateien, Archividentität und leere Messvorlage')
PY
```

Die Dokumentprüfung umfasst acht gerenderte Seiten, 24 leere interaktive PDF-Felder mit geprüftem Ausfüll-/Speicherrundlauf, 25 leere Messgrößen, eindeutige Ziel-IDs und Archivprüfsummen. Diese Prüfung ist keine optische oder elektrische Qualifikation.

## Öffentliche Quellenzuordnung

Die Dokumentquellen S1 und S2 sind hier öffentlich zugänglich: [S1: Optikplan v0.1](../optikplan-v0.1/README.md) und [S2: Laborbetrieb und Geräteauswahl](../../laborbetrieb-v0.1/README.md). Weitere Quellen sind im PDF und in `system_targets.json` genannt. Es werden keine Herstellerunterlagen oder Fachartikel mitverteilt.

Eigene Projektunterlagen unter [Apache-2.0](../../../../LICENSE), im Umfang von [LICENSE_SCOPE.md](../../../../LICENSE_SCOPE.md). Externe Quellen und ihre Rechte bleiben unverändert.
