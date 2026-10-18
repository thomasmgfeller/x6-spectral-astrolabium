# Prüfpaket für die Varianz- und Bennett-Stufe

Dieses Paket macht die neue Herleitung gezielt prüfbar. Die enthaltenen
Gegenrechnungen sind intern; eine externe Begutachtung oder Replikation
wird nicht behauptet. Die historischen C2- und KL-Referenzen bleiben erhalten.

## 1. Quellen und prüfbare Hauptaussage

Öffentlicher Prüfstand vor Zielbudgetrechnung und neuen Punktwolken:
`b51933763dd414c160b05042fd32e9976d8fa47a`.

Unter bekannter uniformer physischer Volumendichte in der 4D-de-Sitter-Familie,
0≤h≤0,5, N=128 iid Punkten pro Wolke und M unabhängigen gleichartigen Wolken
liefert die neue Rechnung mindestens 95% Überdeckung bei vorher festem M.
Die Zielgrösse ist q=R T²; die Methode identifiziert weder unbekannte Dichte
noch absolute Krümmung ohne unabhängiges T. Die vollständige mathematische
Argumentation steht in [DERIVATION.md](DERIVATION.md).

## 2. Besonders wichtige Prüfpunkte

| Prüffrage | Nachweis oder Gegenprobe | Was den Nachweis widerlegen würde |
| --- | --- | --- |
| Ist die Abhängigkeit richtig gezählt? | Var(U) aus identischen, überlappenden und disjunkten Paaren; exakt gefalteter binärer Paarkern | Falscher Faktor bei den überlappenden Paaren oder stillschweigende Paarunabhängigkeit |
| Stimmen bedingte Intervallvolumina? | Lorentztransformierte Momentpolynome; getrennte Integration von Kugelschnittvolumina | Fehlender Volumenfaktor, falscher Zeitversatz oder falsche physische Dichte |
| Sind Normalisierungen konsistent? | V0=π/24, r=A/Z, w=W/Z³; flacher Referenzwert w(0)=1/50 | Verwechslung von flachem und physischem Volumen |
| Ist der Reihenrest im ganzen Bereich eingeschlossen? | Gemeinsame Zeitspiegelung, absolute Koeffizientenmajorante und geometrische Restschranke | Nicht gerechtfertigte Weglassung ungerader Terme oder zu kleine Majorante |
| Ist die Varianzgrenze wirklich uniform? | Rationale Intervallgrenzen auf 64 vollständigen Zellen, nicht bloss 64 Stichproben | Nicht eingeschlossene Zwischenwerte oder Rundung nach innen |
| Ist die statistische Schranke endlich gültig? | Explizite MGF-/Chernoff-Herleitung für unabhängige ganze Wolken | Nicht unabhängige Wolken, ungesicherter Varianz-Plug-in oder falsche Fehleraufteilung |
| Ist die numerische Entscheidung konservativ? | Rationale untere Bennett-Rate, nach aussen gewählte Abweichung und geometrische Inversion | Verwerfen eines Parameters bei unsicherer numerischer Klassifikation |
| Ist das Budgetversprechen korrekt eingeschränkt? | Hinreichende 2ε-Planung, exakte Grenze und unmittelbarer Vorgänger | Behauptung optimaler Mindestzahlen oder Übertragung auf freie Stoppzeiten |
| Werden zwei Verfahren unzulässig kombiniert? | Separate KL-/Bennett-Ausgaben ohne Schnittbildung oder nachträgliche Auswahl | Schnitt zweier 95%-Intervalle ohne eigenen Verschachtelungsnachweis/Fehlerbudget |

## 3. Nachrechnen

Mit Python 3.12 und vollständiger Repository-Historie:

```sh
python3 -m pip install -r research/lorentz_de_sitter_variance/requirements.txt
python3 -B research/lorentz_de_sitter_variance/verify.py --archive-only
python3 -B research/lorentz_de_sitter_variance/verify.py
```

Der erste Befehl zur Prüfung rekonstruiert Mathematik, Kontrollen, Planungs-
und Gruppenentscheide aus dem Archiv. Der zweite erzeugt zusätzlich sämtliche
Punktwolken erneut und verwendet ein getrenntes Kausalitätsprädikat.
Erwartet: `PASS_ARCHIVE_VARIANCE_AUDIT` bzw. `PASS_FULL_VARIANCE_REPLAY`.

Die unabhängige geometrische Gegenrechnung integriert zeitweise den Schnitt
zweier dreidimensionaler Kugeln. Sie verwendet keine Lorentz-Momentpolynome.
Sie ist eine Gleitkomma-Gegenprobe; der mathematische Nachweis stammt aus
den rationalen Integralen und Restfehlergrenzen. Zwölf symbolische Integrale,
zehn direkte Profilprüfungen und 200-stellige Bennett-Gegenrechnungen prüfen
zusätzliche Normalisierungs- und Rundungsrisiken.

## 4. Grenzen der derzeitigen Evidenz

- Numerische Übereinstimmung allein ist kein Beweis für die allgemeine Aussage.
- Reproduzierter Code ist keine externe wissenschaftliche Bestätigung.
- Verschiedene Gruppengrössen verwenden dieselben Wolken erneut; Quoten werden nicht über diese Gruppen gepoolt.
- Der Rand h=0,5 hilft bei der Präzision. Kleine Krümmungen können trotz verbessertem Budget teuer bleiben.
- Derselbe kausale Datensatz ist mit einem flachen Dichtezwilling vereinbar. Ein enges Intervall unter dem uniformen Modell bestätigt diese Dichteannahme nicht.
- Fehler bei der Dichte oder Zeitskala und frei gewähltes Stoppen sind nicht in der Garantie enthalten.

Für eine externe Prüfung sind insbesondere eine eigenständige Ableitung der
Varianzidentität und der uniformen Restschranke sowie eine separat geschriebene
Implementierung sinnvoll. Es wurden keine externen Personen kontaktiert.
