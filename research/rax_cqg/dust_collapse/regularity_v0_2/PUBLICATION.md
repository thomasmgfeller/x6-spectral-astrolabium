# Singularitätsauflösung separat prüfen · Regularität v0.2

**6. November 2026 · Begrenzte Regularitätsaussagen; CST-Singularitätsauflösung bleibt HOLD.**

Die Prüfung trennt inverse Volumenmomente, die Krümmung einer ausdrücklich angenommenen effektiven Innenmetrik und den Anschluss eines endlichen Staubballs. Ein positives Minimum des mittleren Volumens genügt für keinen dieser weitergehenden Nachweise.

- [Bericht (PDF, acht Seiten)](../reports/CST_Staubball_Regularitaet_Rand_Verfeinerung_v0_2.pdf)
- [Unverändertes Originalpaket (ZIP)](../packages/CST_Staubball_Regularitaet_Rand_Verfeinerung_v0_2_Pruefpaket.zip)
- [Vollständige Ableitungen](DERIVATION.md), [Prüfcode](verify.py), [Ergebnisse](results/verification.json), [Modellvertrag](contract.json) und [Originalanleitung](README.md)

## Drei getrennte Ergebnisse

| Bereich | Ergebnis und Geltungsbereich |
|---|---|
| Reduzierte Dirichlet-Quantisierung | Bei endlicher Energie ist `⟨V⁻¹⟩` zeituniform beschränkt. Die neue kontrahierende Präparation `ψ₀ ∝ q³ exp[−(1−i/2)q²]` hat zunächst `⟨V⁻²⟩ = 16/15`, aber zu jedem späteren Zeitpunkt ein divergentes zweites inverses Moment. Gleichzeitig erreicht `⟨V⟩` bei `t = 35/158` das positive Minimum `77/79`. |
| Effektives homogenes Inneres | Für `V=b+6πGMt²`, `b>0`, sind Dichte und Krümmung bei festen Modellparametern begrenzt. In der bisherigen Skalierung wächst die maximale Krümmung für `ν→0` jedoch wie `ν⁻⁴`. Numerische Gitterverfeinerung und Änderung der physikalischen Modellskala sind verschiedene Prüfungen. |
| Endlicher Ball mit Außenraum | Für ein flaches homogenes Inneres, eine mitbewegte Oberfläche und die üblichen Einstein-Darmois-Israel-Bedingungen ohne Oberflächenschicht ist die innere Misner-Sharp-Masse `m₋=M(1−b/V)` zeitabhängig. Sie kann nicht an eine konstante Schwarzschild-Masse angeschlossen werden. Andere Außenräume oder hergeleitete modifizierte Anschlussgesetze werden dadurch nicht ausgeschlossen. |

Das Quantenbeispiel ist **anfangs bezüglich des zweiten inversen Volumenmoments regulär**. Eine physikalische Dichte- oder Krümmungsregularität des Anfangszustands wird nicht behauptet. Die Masse ist in der Quantenreferenz selbst ein Operator; inverse Volumenmomente werden nicht automatisch mit Dichte oder Kretschmann-Skalar gleichgesetzt.

Ein neues hinreichendes Kriterium verlangt bei physikalisch abgeglichener Verfeinerung `P(Vₙ(t)≤v)≤Cv^(2+δ)` mit gemeinsamen Konstanten und `δ>0`. Es liefert uniforme Integrierbarkeit des zweiten inversen Moments. Dieses Kriterium ist für den dynamischen CST-Staubball **nicht bewiesen**. Ein kompletter Materie-Geometrie-Kern, geeignete Operatoren und die globale kausale Fortsetzung bleiben offen. Keine neue Horizont- oder Schwarzes-Loch-Aussage wird freigegeben.

## Was ausgeführt wurde

Sechs Momentauswertungen, elf untere q-Cutoffs und fünf getrennte Sinusentwicklungen kontrollieren den neuen Zustand. 19 rationale Fälle prüfen die effektiven Massen-, Druck- und Krümmungsidentitäten; 24 rationale Kontrollfälle zeigen, warum ein endliches Mittelvolumen oder bloß beschränkte Einzelmomente unter Verfeinerung nicht genügen. Vier numerische und vier physikalische Skalenstufen sind getrennt dokumentiert.

Die Divergenz und der bedingte Anschlussausschluss folgen aus analytischen Ableitungen. Gleitkommakontrollen sind keine Intervallzertifikate, keine physikalischen Messungen und keine neue CST-Ensemblerechnung. Die alten Bounce-Entscheidungen bleiben unverändert.

**English.** A contracting Dirichlet state starts with a finite second inverse-volume moment and loses it at every later time, despite a positive mean-volume minimum. The effective homogeneous metric is regular at fixed model scale, but its curvature bound is not uniform as the stated volume step tends to zero. The tested flat interior cannot be joined without a surface layer to a constant-mass Schwarzschild exterior under the usual metric junction conditions. Full CST singularity resolution remains unestablished.

## Veröffentlichung und Nachrechnung

ZIP, alle 32 Archivmitglieder und PDF sind unverändert übernommen. Aussagen im Originalmaterial, dass der damalige Analyseschritt keine GitHub-Veröffentlichung enthielt, beschreiben den erhaltenen Ursprungssnapshot. Diese Übersicht dokumentiert die anschließende Veröffentlichung. Hinzugefügt sind nur diese Seite, `publication_check.py`, die numerischen Abhängigkeiten und die CI-Anbindung.

```sh
python3 -m pip install -r research/rax_cqg/dust_collapse/regularity_v0_2/publication-requirements.txt
python3 research/rax_cqg/dust_collapse/regularity_v0_2/publication_check.py --replay
```

Die Veröffentlichungskontrolle prüft Originalbytes, vollständige Prüfsummenabdeckung, PDF-Gleichheit und wissenschaftliche Entscheidungen. Die Nachrechnung läuft in einer temporären Kopie, damit archivierte Ergebnisse unverändert bleiben. Ergebnisstruktur und exakte Werte müssen übereinstimmen; für numerische Vergleiche gelten `atol=1e-8`, `rtol=1e-9`, zusätzlich zu den unveränderten strengeren internen Schranken in `verify.py`. Versionsmetadaten dürfen abweichen. Alle sieben CSV-Dateien werden verglichen.

Projektbeiträge gemäß [Lizenzumfang](../../../../LICENSE_SCOPE.md). Primärliteratur und die Grenzen ihrer Anwendung stehen im Bericht und in [DERIVATION.md](DERIVATION.md).
