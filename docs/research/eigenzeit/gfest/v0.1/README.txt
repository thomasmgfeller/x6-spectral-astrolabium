General Finite Error Stability Theorem - Entwurf 0.1
23. Oktober 2026

Der Entwurf interpretiert infite-error als finite-error.
Das PDF enthält präzise Voraussetzungen, zwei Sätze mit Beweisen, explizite
Konstanten, Grenzen der Aussage und offene Beweispflichten für X6.
Alle Konfigurationspaare werden quantifiziert. Die Anwendung der Voraussetzungen
und eine praktisch nützliche Schranke auf der gewünschten X6-Klasse bleiben offen.
Keine unabhängige Begutachtung, keine formale Verifikation in einem Beweisassistenten.

Inhalt
- PDF und editierbare LaTeX-Quelle
- verify_algebra.py mit exakten rationalen und symbolischen Kontrollen
- validation.json mit ausgeführten Kontrollresultaten und Versionsangaben
- requirements.txt für die Reproduktion der Kontrollen
- source_snapshot.json mit eingefrorenem PR122-Ergebnis und Quellenhashes
- SHA256SUMS für alle übrigen Paketdateien

Reproduktion der Algebra
  python -m pip install -r requirements.txt
  python verify_algebra.py

Reproduktion des Dokuments
  pdflatex -interaction=nonstopmode -halt-on-error General_Finite_Error_Stability_Theorem_v0_1.tex
  pdflatex -interaction=nonstopmode -halt-on-error General_Finite_Error_Stability_Theorem_v0_1.tex

Die Abhängigkeiten wurden mit Python 3.12.14 und TeX Live 2023 geprüft.
Ein neuer Lauf überschreibt validation.json. Gleitkommazahlen können auf anderer
Hardware in letzten Stellen abweichen; sie sind nur Diagnostik, keine uniformen
Intervallzertifikate. Die exakten rationalen Identitäten müssen exakt bestehen.
Die Bibliografie nennt Quellen und begrenzt ihre Rolle. Es wird keine Neuheit beansprucht.
