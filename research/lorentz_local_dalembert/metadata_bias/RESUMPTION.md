# Fortsetzung des unterbrochenen, unveränderten Experiments

Vor Berechnung der fünf fehlenden Wolken festgelegt, 20. Oktober 2026.
Der ursprüngliche mathematische Freeze bleibt
`3f6109f4bfb9424352893406e0ba92ddfe6ef858`; der unveränderte Zwischenstand ist
`b22344e17b8d64c7399f4fd705ad21de24603a7b`.

- Ausschließlich Seeds 70210027 bis 70210031 werden ergänzt. Alle 27 alten
  Rohdatensätze einschließlich der drei Ausfälle bleiben byteidentisch.
- `resume_run.py` ruft dieselben eingefrorenen Funktionen auf. Modelle, Felder,
  Rauschrealisierungen, Guards, Gewichte, Testkriterien und Bootstrap bleiben
  unverändert. Neue Ausgaben liegen in separaten Fortsetzungsordnern.
- Vor jeder Wolke wird der Seed, danach die Laufzeit und der Speicherhöchststand
  atomar protokolliert. Bestehende Fortsetzungsordner werden nicht überschrieben.
  Auch die Fortsetzung ersetzt keine ausgefallenen Seeds und ändert keine Auswahl.
- Die ursprünglichen Ausführungsprotokolle bleiben unverändert auf RUNNING:
  beim Prozessabbruch liefen ihre Finalizer nicht mehr. Laufzeit und Peak-RSS
  dieser beiden Prozesse sind nicht vollständig bekannt. Die ursprünglichen
  Ausführungs-/Budget-Gates bleiben deshalb **nicht nachgewiesen**, selbst wenn
  alle 32 Datensätze vorliegen. Ein numerischer Replay ersetzt diese Messlücke nicht.
- Für die Auswertung werden die beiden Archive in einem temporären Verzeichnis
  zusammengeführt. Die dortigen Ausführungsübersichten heißen RESUMED_COMPLETE.
  Ihre numerischen Zeit-/Speicherfelder dienen nur der Kompatibilität mit dem
  unveränderten Analyzer und enthalten ausdrücklich Untergrenzen aus vorhandenen
  Aufzeichnungen. Der Adapter gibt diese Felder im veröffentlichten Bericht als
  unbekannt (`null`) aus und setzt die Ressourcen-Gates auf nicht bestanden.
  Alle statistischen Kennzahlen/Gates kommen unverändert aus `mb_analyze.py`.
  Keine unbekannte Ressourcenmessung wird als PASS ausgegeben.

## Passive numerische Diagnose

Die Diagnose liest ausschließlich gespeicherte Geometrie, Gewichte und
Solverausgaben. Sie ist kein neues Akzeptanzkriterium und beeinflusst weder
Fortsetzung noch Auswertung. Ausgegeben werden:

1. Singulärwerte, Zeilenrang, erwartete Nullität und Kondition der normierten
   Momentmatrix D vor/nach der vorhandenen Relationsprojektion. Der bestehende
   Konditionsguard 1e5 bleibt unverändert; Rangdiagnose relativ zu sigma_max mit
   1e-12. Der absichtliche Gewichtsnullraum ist kein Rekonstruktionsfehler.
2. Singulärwerte von D H^(-1/2), H=I+11ᵀ: Kondition des Momentproblems mit dem
   bekannten Root-Feldrauschterm, **keine Einbettungs-Jacobi-Matrix**.
3. Momentresiduen aller sechs Gewichtsvektoren, Solverstatus, kleinste
   Constraint-Slack und Spektrum/Rang der nahezu aktiven Constraint-Jacobi-Matrix
   (Slack <=1e-7, Rangschwelle 1e-10 relativ). Redundante aktive Constraints sind
   möglich und werden nicht automatisch als Versagen bewertet.

Eine rauschgewichtete Mess-Jacobi-Matrix einer vollständigen Einbettungsschätzung
ist weiterhin nicht definiert. Weder diese Diagnose noch eine SVD liefert die
noch fehlende validierte Einbettungskovarianz. Keine Online-/Krümmungsfreigabe.
