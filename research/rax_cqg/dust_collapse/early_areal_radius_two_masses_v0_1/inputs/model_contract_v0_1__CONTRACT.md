# CST-DUST Model Contract v0.1


## 1. CST-DUST
Model Contract

**CST-DUST-MC-001 · Version 0.1.0**
Ein verbindlich versionierbarer Prüfvertrag für einen endlichen Staubball auf Kausalsets.

**Protokoll: spezifiziert. Physikalischer CST-Modellschluss: HOLD.** Der Vertrag legt Annahmen, Referenz, Messgrößen, Prüfentscheidungen und Sperrgründe fest. Er enthält noch keinen vollständig definierten und validierten vierdimensionalen Materie-Geometrie-Kern.

| Entscheidung | Regel |
| --- | --- |
| Korrespondenz | Klassische Staubbewegung und Rückwirkung im vorab festgelegten regulären Fenster prüfen. |
| Bounce | Mehrzeitiges Umkehrereignis und seine zulässige Wahrscheinlichkeit separat bewerten. |
| Regularität | An jedem Prüfpunkt eine eigene Entscheidung über definierte Dichte-/Krümmungsmomente und Verfeinerung ausgeben. |
| Randanschluss | Endliches Inneres, materielle Oberfläche und Außenraum als zusammengehöriges Problem behandeln. |
| Trapping / Fortsetzung | Lokale Lichtfronten und kausale Fortsetzbarkeit erhalten eigene Nachweise. |

### Fester Grundsatz

Ein positives Minimum von ⟨V⟩ verändert die Regularitätsentscheidung nicht. Ebenso begründet ein PASS auf einer klassischen Referenz kein PASS für die CST-Dynamik. Jeder Befund nennt Modell, Observable, Raumgebiet, Zeitintervall, Verfeinerung und Evidenzart.

Vorhandene Ergebnisse dienen als ausdrücklich retrospektive Eingaben. Neue Auswahlregeln sind prospektiv für künftige Daten. Diese lokale Festlegung ist keine externe Präregistrierung.


## 2. Modellklasse und offener Modellschluss

**Zielkandidat CST-DUST-C1:** vierdimensionaler Kontinuumsbezug, Signatur (-+++), c=1, Λ=0; positiver, irrotationaler, druckloser Staub. Der erste makroskopische Vergleich ist sphärisch und innen homogen. Einzelne diskrete Historien müssen nicht exakt kugelsymmetrisch sein. Staubzeit gilt zunächst nur dort, wo ein regulärer Staubfluss existiert.

### Gekoppelte Kontinuumsreferenz

```text
S = (16πG)⁻¹ ∫ √(-g) R d⁴x + S∂
     - ½ ∫ √(-g) ρ (gab ∂aT ∂bT + 1) d⁴x
```

Variation vor dem Einsetzen der Zwangsbedingung liefert für ua=-∂aT: u·u=-1, ∇a(ρua)=0, geodätischen Transport und Gab=8πGρuaub. Diese bereits gravitative Referenz ist kein Emergenznachweis aus CST [P2, L1]. Nach Kaustiken benötigt druckloser Ein-Strom-Staub eine neue Beschreibung.

| Offener Pflichtschluss | Vor einem dynamischen CST-Test erforderlich |
| --- | --- |
| D1: Historienträger | Markierte Kausalsets, zulässige Randdaten, 4D-Auswahl und vollständige bzw. kontrolliert abgeschnittene Summe. |
| D2-D3: Wirkung / Maß | Explizite Staubdiskretisierung, BDG-Koeffizienten, Materiemaß, Sektorengewichte ζN, Rand-/Eckterme und Regulatoren. |
| D4: Quantenzustand | Anfangspräparation, inneres Produkt, Normierung und Komposition bzw. konsistentes Dekohärenzfunktional. |
| D5-D7: Auswertung | Relationale Observablen, Gewichte der Vergröberungsfasern, Außenraum sowie vollständiger Laufplan. |

Formal kann eine Amplitude als Summe über (C, Materiemarken) mit μ(C, Materie) exp(iS/ℏ) geschrieben werden. Solange die Pflichtschlüsse fehlen, ist dies eine Strukturvorgabe. Ein Faktor 1/|Aut| folgt nur aus dem tatsächlich gewählten Beschriftungsmaß [P3]. Ein Volumenpfad darf nicht ohne Nachweis als geschlossene Markov-Dynamik behandelt werden.


## 3. Endlicher Ball und Außenraum

**Referenz REF-DUST-FB-01:** marginal gebundener, homogener Einstein-Staubball mit flachem FRW-Inneren und mitbewegter Oberfläche. Außerhalb liegt Schwarzschild mit derselben konstanten Masse M. Der Anfangsradius ist R₀=10 in Referenzeinheiten, G=1. Damit ist der endliche Ball von Anfang an Teil der Prüfung.

```text
Ts(M) = (2/3) √(R₀³/(2GM)),     a(T) = (1-T/Ts)2/3
Rb(T) = R₀a(T),     V(T) = 4πRb³/3,     ρ(T) = M/V(T)
Ṙb(0) = -√(2GM/R₀),     mMS(Rb) = M
```

Ohne Oberflächenschicht gelten im klassischen Modell [hab]=[Kab]=0. Der Staubdruck verschwindet auch an der Oberfläche. Ein endlicher Dichtesprung zum Vakuum ist dabei zulässig; ein Delta-Stress oder eine quadrierte Delta-Krümmung darf nicht stillschweigend eingeführt werden.

### Drei verschiedene Grenzen

| Grenze | Vertragliche Behandlung |
| --- | --- |
| Materieoberfläche | Zeitartige Weltfläche innerhalb der Raumzeit. Kausale Intervalle und Wirkungsbeiträge über die Oberfläche bleiben erhalten. |
| Rechengebiet | Äußere und zeitliche Abschneidung gesondert dokumentieren. Nichtlokale Restbeiträge durch Vergrößerung oder begründete Schranken kontrollieren. |
| q=0 der reduzierten Zelle | Konfigurationsraumrand eines anderen Referenzmodells; keine räumliche Staubballoberfläche. |

### Bekannter Ausschluss bleibt wirksam

Für das frühere effektive Innere V=b+6πGMt², b>0, ergibt sich m₋=M(1-b/V). Bei mitbewegter Oberfläche und üblichen Einstein-Anschlussbedingungen ohne Schicht ist damit kein Anschluss an konstante Schwarzschild-Masse auf einem offenen Zeitintervall möglich [P1]. Ein anderer Außenraum oder ein modifiziertes Anschlussgesetz muss aus derselben Kandidatentheorie folgen.

Im Vakuum gibt es keinen materiellen Staubzeitgeber. Eine äußere Zeitfoliation wird über die Oberfläche fortgesetzt und eigens spezifiziert. Der hier deklarierte endliche Testbereich liefert keine globale Aussage über Unendlich.


## 4. Messgrößen und Verfeinerung

| Größe | Definition und notwendige Kontrolle |
| --- | --- |
| Staubstrom Ja | Kontinuumsziel Ja=ρua. Diskret zuerst orientierte Massenflüsse durch relationale Schnitte definieren; Vektorkomponenten erst nach begründetem geometrischem Wörterbuch. |
| Masse / räumliches Volumen | MΣ=-∫ΣJ·n dΣ für zukunftsgerichtetes n. N/λ schätzt Vierervolumen, keine räumliche Scheibe. Schichtbreite ist kein kalibriertes V(T). |
| Dichte / Krümmung | Physikalische Observable mit Maß, Ordnung und Domäne. ⟨M̂⟩⟨V̂⁻¹⟩ ist bei nichtkommutierenden Operatoren kein hergeleiteter Dichteerwartungswert. V⁻² ist kein Krümmungsoperator. |
| Expansionen | Staubexpansion θ=∇·u getrennt von θ±=A⁻¹ dA/dλ±. Nullrichtungen zukunftsgerichtet, Orientierung und Normierung festlegen. |
| Trapping | θ+<0 und θ-<0: künftig gefangene Fläche. θ+=0, θ-<0: künftig marginale Fläche. Ein Horizonttyp benötigt zusätzliche geometrische Bedingungen [L4]. |

### Vier getrennte Änderungen

**Numerisch:** Gitter, Zeitschritt oder Cutoff bei festem Modell. **Statistisch:** Anzahl unabhängiger Realisierungen. **CST-Verfeinerung:** Zähldichte λ in L⁻⁴ und ℓ=λ⁻¹/⁴ bei physikalisch abgeglichenem Gebiet, Zustand und Kopplungen. **Physikalische Skalenfamilie:** Änderung einer postulierten Naturkonstanten wie ν ist eine eigene Fragestellung.

Nichtlokalitätsskala Lk und Mittelungsskala Lcg werden im Laufplan getrennt von ℓ fixiert. Ein späterer Lcg→0-Grenzgang ist kein Bestandteil eines Tests bei fester Messauflösung. Dichte λ und Materiedichte ρ haben verschiedene Dimensionen.

Der bekannte BD-Operator nähert im Mittel unter Voraussetzungen □-R/2 an [L2]. Eine diskrete Produktidentität oder eine vollständige Krümmungskontrolle folgt daraus nicht. Insbesondere misst der Ricci-Skalar allein keine Schwarzschild-Weylkrümmung.


## 5. Erster Korrespondenztest

**PST-FB-01:** festgelegter endlicher Screening-Test, derzeit NOT_RUN und wegen D1-D7 nicht für einen CST-Dynamiknachweis zulässig. Die analytische Referenz ist sofort berechenbar. Eine Vorhersage aus dem neuen Kandidaten muss ohne Nachanpassung an die Prüfdaten entstehen.

| Festlegung | Wert / Regel |
| --- | --- |
| Massen / Anfangsradius | M=1/4, 1, 4; jeweils R₀=10 und G=1. Anfangsgeschwindigkeit für jede Masse aus dem Zwang bestimmen. |
| Gemeinsames Zeitfenster | 0 ≤ T ≤ ½ min Ts = 3.726779962. Fünf Marken bei 0, ¼, ½, ¾, 1 dieses Endwerts. |
| Primäre Messgrößen | Rb, ρ, H=ȧ/a und ä/a: jeweils 5 % relative Gesamttoleranz an allen Marken und Massen. |
| Erhaltung / Massenantwort | Massenfehler und normalisierter Flussbilanzrest höchstens 2 % von M; initiales Verhältnis |Ṙ(M₂)|/|Ṙ(M₁)|=√(M₂/M₁) mit 5 % Toleranz. |
| Auflösungen | λ₀, 2λ₀, 4λ₀, 8λ₀; absolute λ₀ und physikalischer Abgleich vor Laufstart. Beide feinsten Stufen bestehen; ihr Unterschied höchstens 2,5 % der jeweiligen Referenzgröße. |
| Statistik | Gemeinsame 95-%-Unsicherheitsaussage über alle primären Vergleiche, einschließlich Massenantwort und Stufenvergleich. Methode, Stichprobengröße und Teststärke vor neuen Daten fixieren. |

**Entscheidung:** PASS nur, wenn jedes vollständige Unsicherheitsintervall im vorab gesetzten Toleranzband liegt. Ein davon disjunktes Intervall bedeutet FAIL für den betroffenen Test; Überschneidung bedeutet HOLD. Systematische Fehler werden zusätzlich begrenzt und nicht als unabhängige Zufallsfehler ausgegeben.

Die Zahlen sind gewählte erste Leistungsanforderungen, keine Naturkonstanten. Sie gelten für den endlichen Test; vier Stufen beweisen keinen Kontinuumsgrenzwert. Absolute Dichten, Ensemblegröße, Zustandsbreiten, Randpuffer und statistisches Verfahren bleiben explizite Zulassungsvoraussetzungen. Ein unerreichbares Budget führt zu HOLD, nicht zur nachträglichen Lockerung.


## 6. Regularität als eigene Entscheidung

**REGULARITY wird an jedem Prüfpunkt neu bewertet.** Die Standardaussage dieser Version betrifft begrenzte und konvergierende physikalische Momente auf einem deklarierten Raumgebiet und Zeitintervall. Eine stärkere Aussage wie punktweise Krümmungsbeschränktheit oder Singularitätsauflösung benötigt zusätzliche Nachweise.

```text
supn,T∈I,ξ∈D E[(ρn(T,ξ)/ρ*)²] ≤ Cρ < ∞
supn,T∈I,ξ∈D E[|Kn(T,ξ)|/K*] ≤ CK < ∞
```

ξ bezeichnet relationale Messzellen im behaupteten Gebiet D, zunächst bei fester physikalischer Mittelungsskala Lcg. Lokale Dichtekontrolle kann nicht durch M/V für den gesamten Ball ersetzt werden. An der Oberfläche sind einseitige Grenzen oder ein begründetes aufgelöstes Übergangsprofil nötig.

ρ*=M/V₀ und K*=(GM/R₀³)² bleiben bei Verfeinerung fest. K bezeichnet nur nach begründetem geometrischem Bezug den Kretschmann-Skalar. Für Quantenobservablen sind Spektralmaße oder ein Messinstrument, geeignete Domänen und die Bedeutung des Betrags anzugeben. Hier wird keine gemeinsame klassische Mehrzeitverteilung vorausgesetzt.

| Pflicht | Anforderung für PASS im deklarierten Umfang |
| --- | --- |
| R1: Definition | Physikalische Dichte-/Krümmungsobservable und Erhaltung der benötigten Domänen belegen. |
| R2: Schranken | Gemeinsame Konstanten aus dem Modell herleiten. Beobachtete Stichprobenmaxima sind keine universellen Schranken. |
| R3: Seltene Beiträge | Uniforme Integrierbarkeit der betroffenen Größen kontrollieren. Null beobachtete Extremereignisse genügt nicht. |
| R4: Verfeinerung | Physikalischen Abgleich und Konvergenz begründen. Begrenzte Momente allein sichern keine Konvergenz ihrer Werte. |
| R5: Zeit / Raum | Intervall und Raumgebiet vollständig abdecken; endlich viele Prüfmarken nur mit kontrollierten Zwischenräumen auf ein Intervall übertragen. |

Für eine positive Volumenobservable ist P(Vn(T)≤v)≤Cv2+δ für 0<v≤v₀ mit gemeinsamen C,v₀,δ>0 ein hinreichender Tail-Nachweis: E[V⁻²]≤v₀⁻²+2Cv₀δ/δ. Erst ein separat bewiesener Operator-/Formvergleich überträgt ihn auf Dichte oder Krümmung [P1]. Das Scheitern dieses hinreichenden Kriteriums allein ist kein Gegenbeweis physikalischer Regularität.


## 7. Prüfpunkte und Entscheidungslogik

| Prüfpunkt | Auslöser und verpflichtender Eintrag |
| --- | --- |
| P0: Ausgangsstand | Vertrag, Referenz und Herkunft fixieren. Alle acht CST-Entscheidungen ausgeben; Regularität derzeit HOLD. |
| P1: Modellschluss | Wirkung, Maß, Zustand, Operatoren und Randdaten. Regularität der Präparation separat prüfen. |
| P2: Messkalibrierung | Strom, räumliches Volumen, Dichte und Krümmung. Bias/Varianz und unbekannte Tails getrennt behandeln. |
| P3: Korrespondenz | Für jede Masse, jedes Zeitfenster und jede Auflösung einen Record führen; danach eine gesonderte Gesamtauswertung. |
| P4: Umkehr / Trapping | Am Ereignis und im umgebenden Intervall alle Entscheidungen einschließlich Regularität neu ausgeben. |
| P5: Vollständiges Gebiet | Innen-/Rand-/Außenraum und kausale Fortsetzung prüfen; keine Übertragung eines Innenraum-PASS auf den Außenraum. |

**PASS:** alle Anforderungen der konkreten Aussage belegt. **FAIL:** eine gültige, im Geltungsbereich liegende Verletzung nachgewiesen. **HOLD:** Definition, Evidenz oder Kontrolle fehlt. NOT_RUN, RUN und INHERITED sind Ausführungszustände und ersetzen keine dieser Entscheidungen.

Ein gültiger Gegenbeweis kann FAIL begründen, obwohl andere Voraussetzungen ungeklärt sind. Ein Gegenbeispiel aus einer anderen Modellklasse darf dagegen nicht übertragen werden. Bei widersprüchlicher oder noch nicht geprüfter Evidenz bleibt die betreffende Anforderung UNRESOLVED.

### Keine automatische Gesamtfreigabe

Die maschinenlesbaren Entscheidungen heißen MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION. Ihre getrennte Ausgabe ist verpflichtend. Das Prüfskript bewertet die Vollständigkeit deklarierter, geprüfter Evidenz; es verifiziert weder mathematische Beweise noch die Wahrheit eines Literaturverweises.

Selbst ein Momenten-PASS ersetzt keine Kontrolle relevanter Gezeitenkomponenten, keine kausale Fortsetzung und keine globale Vollständigkeit. Ein Ereignishorizont erfordert zusätzliche globale Information. Es gibt deshalb keine automatische Ausgabe „Singularität aufgelöst“.


## 8. Übernommene Befunde und Sperren

| Vorhandene Evidenz | Zulässige Verwendung |
| --- | --- |
| Reduzierte Einstein-Staub-Referenz [P2] | Klassische Bewegung und semiklassische Kontrollen als Methodenreferenz. Kein Nachweis aus der vollen CST-Summe. |
| Historiengewichtung [P3] | Maß dq=dV/(2√V) für die festgelegte reduzierte Quantisierung. Die volle Materie-/Geometriegewichtung bleibt offen. |
| Dirichlet-Gegenbeispiel [P1] | Anfangs endliches ⟨V⁻²⟩ kann trotz positivem mittlerem Minimum sofort divergieren. FAIL der Momentenerhaltung dieses Modells; keine automatische physikalische Krümmungsaussage. |
| Effektive Innenmetrik [P1] | Bei fester ν bedingt regulär; Kmax wächst in der geprüften ν→0-Familie wie ν⁻⁴. Keine uniforme Grenze in dieser Skalierung. |
| Schwarzschild-Anschluss [P1] | Die geprüfte Bounce-/Rand-/Außenraum-Kombination ist ausgeschlossen. Andere hergeleitete Außenräume bleiben prüfbar. |

### Pflichtkontrollen für spätere Implementierungen

Labelpermutation darf die Physik nicht ändern. Falsche Volumeneinheiten und die Verwechslung von N/λ mit räumlichem Volumen müssen auffallen. Eine massenblinde Geometrie muss die Rückwirkungsprüfung verfehlen. Künstliches Abschneiden an der Stauboberfläche muss als geändertes Gebiet erkannt werden. Ein Bounce-PASS bei fehlender Tail-Kontrolle muss Regularität auf HOLD lassen.

Für eine spätere Trapping-Prüfung werden bekannte Staubgeometrie und Minkowski-Negativkontrolle verwendet. Ihre bestandene Messkalibrierung ist anschließend von einer dynamischen Entstehung gefangener Flächen zu trennen. Das frühere dominante Bounce-Modell bleibt verworfen; der neue Vertrag setzt diese Entscheidung nicht zurück.

### Aktueller Status von CST-DUST-C1

**Alle acht physikalischen Entscheidungen: HOLD.** Grund sind der offene Modellschluss und fehlende passende dynamische Evidenz. Das bedeutet keine Widerlegung von CST. Es bezeichnet präzise, welche Aussage dieser Kandidat derzeit noch nicht trägt.


## 9. Arbeitsfolge und Versionsregeln

| Nächster Baustein | Konkretes Abnahmeergebnis |
| --- | --- |
| 1. Mikroskopischer Modellschluss | D1-D4 als berechenbare Definitionen schließen; mindestens einen vollständig nachrechenbaren kleinen Fall mit Normierungs-/Symmetriekontrollen liefern. |
| 2. Strom und Messgrößen | D5 schließen; Flüsse, Dichte und räumliche Volumina auf der endlichen Referenz kalibrieren, Außenraumfehler bilanzieren. |
| 3. Laufmanifest | D6-D7 einschließlich tatsächlicher Skalen, Zustände, Unsicherheitsverfahren, Seeds und erreichbarem Budget fixieren. |
| 4. PST-FB-01 | Unabhängige Vorhersagen gegen die festgelegten Toleranzen prüfen. An jedem P3-Punkt Regularität separat ausweisen. |
| 5. Weiterführende Aussagen | Trapping/Bounce nur mit passender Ereignisdefinition; vollständigen Randanschluss und Fortsetzung separat schließen. |

Definitionen von 1 und 2 können parallel vorbereitet werden. Kostenpflichtige Läufe und neue große Ensembles sind für diesen Vertragsschritt nicht vorgesehen. Solange Zulassung oder Teststärke fehlen, bleibt der dynamische Test HOLD / NOT_RUN.

### Änderungen sind sichtbar und überprüfbar

Jeder Entscheidungsrecord enthält Vertragsversion und SHA-256, Laufmanifest-Hash, Modellkennung, Raumgebiet, Zeitintervall, Verfeinerung, Evidenzverweise und die einzelnen Entscheidungen. Physikalische und numerische Parameter dürfen nicht unter demselben Namen ausgetauscht werden.

Eine Änderung an Wirkung, Maß, Anfangszustand, Randgesetz, Operator, Toleranz oder Abbruchregel erzeugt vor neuen Prüfdaten eine neue Vertragsversion. Nach Einsicht in Prüfdaten vorgenommene Anpassungen werden als explorativ gekennzeichnet; bestätigende Aussagen benötigen neue unabhängige Daten. Betroffene alte Entscheidungen werden erneut bewertet, nicht überschrieben.

Die alten 27 Entwicklungs- und 17 Prüfpfade sowie frühere Quantenreferenzzustände sind bekannte Daten. Sie dürfen nicht als frische unabhängige Validierung dieses Vertrags etikettiert werden. Ein nachträglich ausgesuchtes Zeitfenster oder ein günstiger Randanschluss zählt als Modelländerung.


## 10. Nachrechnung und Quellen

**Ausgeführt:** 15 klassische Referenzfälle mit je fünf algebraischen Kontrollen und 17 Kontrollen der Entscheidungslogik. Keine neuen CST-Historien. Größter relativer Identitätsrest: 1.11e-15. Das sind Gleitkommakontrollen, keine Intervallzertifikate.

```text
python3 verify.py
python3 gate.py examples/checkpoint_P0.json
```

contract.json ist die maschinenlesbare Festlegung; CONTRACT.md und dieser Bericht beschreiben denselben Stand. gate.py hält fehlende Regularität, fehlende Tails und unpassende Evidenz zurück. results/ enthält Referenzwerte, Kontrollen und den Ausgangsrecord. Reproduktion der PDF: Python mit ReportLab und DejaVu Sans, danach python3 make_report.py.

### Projektquellen, unveränderter veröffentlichter Stand

[P1] Projektbericht: [Regularität, Rand und Verfeinerung v0.2](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/feebbeed17d83b3cb058ffecc2debd9af1000375/research/rax_cqg/dust_collapse/regularity_v0_2/PUBLICATION.md). Die Veröffentlichungsübersicht ist im Paket archiviert; Beweise und Prüfdaten sind dort verlinkt.

[P2] Projektbericht: [Klassische Staubbewegung und Rückwirkung v0.1](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/feebbeed17d83b3cb058ffecc2debd9af1000375/research/rax_cqg/dust_collapse/classical_backreaction_v0_1/PUBLICATION.md). Die Veröffentlichungsübersicht ist im Paket archiviert; Beweise und Prüfdaten sind dort verlinkt.

[P3] Projektbericht: [Historiengewichtung v0.1](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/feebbeed17d83b3cb058ffecc2debd9af1000375/research/rax_cqg/dust_collapse/history_weighting_v0_1/PUBLICATION.md). Die Veröffentlichungsübersicht ist im Paket archiviert; Beweise und Prüfdaten sind dort verlinkt.

### Primärliteratur und Reichweite

[L1] Brown, Kuchař (1995), [Dust as a Standard of Space and Time in Canonical Quantum Gravity](https://arxiv.org/abs/gr-qc/9409001). Motivation der gekoppelten Staubreferenz; kein CST-Modellschluss.

[L2] Belenchia, Benincasa, Dowker (2016), [The continuum limit of a 4-dimensional causal set scalar d’Alembertian](https://arxiv.org/abs/1510.04656). Grenzwert des Mittelwerts unter Voraussetzungen; kein Beweis beschränkter Krümmungsfluktuationen.

[L3] Dowker, Liu, Lloyd-Jones (2025), [Timelike boundary and corner terms in the causal set action](https://arxiv.org/abs/2501.00139). Analytische/numerische Evidenz für zeitartige Randbeiträge in Minkowski-Teilgebieten; kein Anschlussgesetz für gekrümmten Staub.

[L4] Hayward (1994), [General Laws of Black-Hole Dynamics](https://arxiv.org/abs/gr-qc/9303006). Lokale marginale Flächen und Trapping-Horizonte; keine Übertragung ihrer klassischen Gesetze ohne Voraussetzungen auf einen Quantenzustand.

Quellenabruf: 6. November 2026. Dateien und Prüfsummen: inputs/provenance.json und SHA256SUMS. Der Vertrag schafft prüfbare Zuständigkeiten für die Nachweise; er behauptet keine neue Singularitätsauflösung.
