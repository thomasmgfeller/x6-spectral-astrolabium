# Zwei Pulse im skalaren Direktlink-Modell

**Eigenzeit · Modellrechnung vom 2. November 2026.** Zwei ruhende Quellenereignisse regen ein skalares Direktlink-Feld in derselben vierdimensionalen Poisson-Raumzeit an. Ein endlicher Empfänger registriert für jeden Puls das erste verknüpfte Empfangsereignis. Die Auswertung zählt auch, wie häufig eine Registrierung fehlt.

Im Basisfall lieferten 36 092 von 4 000 000 Versuchen beide Zeitstempel. **Unter dieser Bedingung** beträgt die simulierte Standardabweichung des Abstandsfehlers 0,24818 in Einheiten von $t_0$. Die analytische Schranke reicht von 0,23899 bis 0,25650. Die bedingte Streuung und die Häufigkeit der Doppeltreffer sind zwei getrennte Observablen. [Bericht (PDF)](CST_Zwei_Pulse_Bericht.pdf) · [Originales Prüfpaket mit Protokoll, Code und simulierten Daten (ZIP)](CST_Zwei_Pulse_Pruefpaket.zip)

**English summary.** The first linked reception event defines each timestamp. Only 36,092 of four million baseline trials registered both pulses. The reported timing scatter applies to that selected sample. The direct-link model is a companion to the dust-collapse series through its treatment of finite causal data and readout uncertainty. [Dust-collapse notes and verification](../../rax_cqg/dust_collapse/README.md)

## Reproduktion und Einordnung

Das Archiv entpacken, im Verzeichnis `CST_Zwei_Pulse` mit `sha256sum -c SHA256SUMS` die Dateien prüfen und die Schritte in der enthaltenen `README.md` ausführen. Sie unterscheidet zwischen der Gegenrechnung auf gespeicherten Daten und einem neuen Lauf des C++17-Sprinklers. `protocol.json` hält Geometrie, Startwerte und Vergleichsregel fest. Die Rohdaten enthalten die gemeinsam registrierten Zeitpaare und Trefferzahlen.

Die Direktlink-Regel geht auf Dowker, Henson und Sorkin zurück. Die Studie spezifiziert dafür einen Empfänger mit zwei eingesetzten Emissionen. Das Modell liefert eine synthetische Kontrolle der Ableseregel. [Primärquelle](https://doi.org/10.1103/PhysRevD.82.104048) · [Eigenzeit in 3+1 Dimensionen](../../eigenzeit_4d/README.md)
