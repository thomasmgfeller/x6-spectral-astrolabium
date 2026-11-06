#!/usr/bin/env python3
"""One source for the readable Markdown contract and the paginated PDF."""
from pathlib import Path
import html,json,re
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parent
C=json.loads((ROOT/'contract.json').read_text())
V=json.loads((ROOT/'results/verification.json').read_text())
F='/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('D',F+'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DB',F+'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('D',normal='D',bold='DB',italic='D',boldItalic='DB')
INK=colors.HexColor('#173747');TEAL=colors.HexColor('#087C80');PALE=colors.HexColor('#ECF3F5')
styles={
 'body':ParagraphStyle('body',fontName='D',fontSize=10,leading=14.4,textColor=INK,spaceAfter=8),
 'small':ParagraphStyle('small',fontName='D',fontSize=8.7,leading=12.2,textColor=INK,spaceAfter=6),
 'title':ParagraphStyle('title',fontName='DB',fontSize=24,leading=29,textColor=INK,spaceAfter=17),
 'head':ParagraphStyle('head',fontName='DB',fontSize=11.7,leading=16,textColor=TEAL,spaceBefore=9,spaceAfter=7),
 'kick':ParagraphStyle('kick',fontName='DB',fontSize=8.5,leading=12,textColor=TEAL,spaceAfter=10),
 'eq':ParagraphStyle('eq',fontName='D',fontSize=10.1,leading=15.5,textColor=INK,spaceBefore=5,spaceAfter=10,leftIndent=10)
}
story=[];md=[];page_count=0
def plain(s):
 s=re.sub(r'<br\s*/?>','\n',s)
 s=re.sub(r'<b>(.*?)</b>',r'**\1**',s)
 s=re.sub(r'<link href="([^"]+)">(.*?)</link>',r'[\2](\1)',s)
 return html.unescape(re.sub(r'<[^>]+>','',s))
def start(title):
 global page_count
 if story:story.append(PageBreak())
 page_count+=1
 story.append(Paragraph(f'CST-DUST · MODEL CONTRACT v0.1 · 6. NOVEMBER 2026 · {page_count:02}',styles['kick']))
 story.append(Paragraph(title,styles['title']));md.extend(['',f'## {page_count}. {plain(title)}',''])
def p(s,small=False):
 story.append(Paragraph(s,styles['small' if small else 'body']));md.extend([plain(s),''])
def h(s):story.append(Paragraph(s,styles['head']));md.extend(['### '+plain(s),''])
def eq(s):story.append(Paragraph(s,styles['eq']));md.extend(['```text',plain(s),'```',''])
def table(head,rows,widths):
 arr=[[Paragraph('<b>'+str(t)+'</b>',styles['small']) for t in head]]+[[Paragraph(str(t),styles['small']) for t in row] for row in rows]
 t=Table(arr,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),
 ('LINEBELOW',(0,0),(-1,0),.8,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#CDDCE1')),
 ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
 story.append(t);story.append(Spacer(1,9))
 md.append('| '+' | '.join(map(plain,head))+' |');md.append('| '+' | '.join(['---']*len(head))+' |')
 md.extend('| '+' | '.join(plain(str(v)).replace('\n',' ') for v in row)+' |' for row in rows);md.append('')

start('CST-DUST<br/>Model Contract')
p('<b>CST-DUST-MC-001 · Version 0.1.0</b><br/>Ein verbindlich versionierbarer Prüfvertrag für einen endlichen Staubball auf Kausalsets.')
p('<b>Protokoll: spezifiziert. Physikalischer CST-Modellschluss: HOLD.</b> Der Vertrag legt Annahmen, Referenz, Messgrößen, Prüfentscheidungen und Sperrgründe fest. Er enthält noch keinen vollständig definierten und validierten vierdimensionalen Materie-Geometrie-Kern.')
table(['Entscheidung','Regel'],[
 ('Korrespondenz','Klassische Staubbewegung und Rückwirkung im vorab festgelegten regulären Fenster prüfen.'),
 ('Bounce','Mehrzeitiges Umkehrereignis und seine zulässige Wahrscheinlichkeit separat bewerten.'),
 ('Regularität','An jedem Prüfpunkt eine eigene Entscheidung über definierte Dichte-/Krümmungsmomente und Verfeinerung ausgeben.'),
 ('Randanschluss','Endliches Inneres, materielle Oberfläche und Außenraum als zusammengehöriges Problem behandeln.'),
 ('Trapping / Fortsetzung','Lokale Lichtfronten und kausale Fortsetzbarkeit erhalten eigene Nachweise.')],[117,380])
h('Fester Grundsatz')
p('Ein positives Minimum von ⟨V⟩ verändert die Regularitätsentscheidung nicht. Ebenso begründet ein PASS auf einer klassischen Referenz kein PASS für die CST-Dynamik. Jeder Befund nennt Modell, Observable, Raumgebiet, Zeitintervall, Verfeinerung und Evidenzart.')
p('Vorhandene Ergebnisse dienen als ausdrücklich retrospektive Eingaben. Neue Auswahlregeln sind prospektiv für künftige Daten. Diese lokale Festlegung ist keine externe Präregistrierung.',small=True)

start('Modellklasse und offener Modellschluss')
p('<b>Zielkandidat CST-DUST-C1:</b> vierdimensionaler Kontinuumsbezug, Signatur (-+++), c=1, Λ=0; positiver, irrotationaler, druckloser Staub. Der erste makroskopische Vergleich ist sphärisch und innen homogen. Einzelne diskrete Historien müssen nicht exakt kugelsymmetrisch sein. Staubzeit gilt zunächst nur dort, wo ein regulärer Staubfluss existiert.')
h('Gekoppelte Kontinuumsreferenz')
eq('S = (16πG)⁻¹ ∫ √(-g) R d⁴x + S<sub>∂</sub><br/>     - ½ ∫ √(-g) ρ (g<super>ab</super> ∂<sub>a</sub>T ∂<sub>b</sub>T + 1) d⁴x')
p('Variation vor dem Einsetzen der Zwangsbedingung liefert für u<sub>a</sub>=-∂<sub>a</sub>T: u·u=-1, ∇<sub>a</sub>(ρu<super>a</super>)=0, geodätischen Transport und G<sub>ab</sub>=8πGρu<sub>a</sub>u<sub>b</sub>. Diese bereits gravitative Referenz ist kein Emergenznachweis aus CST [P2, L1]. Nach Kaustiken benötigt druckloser Ein-Strom-Staub eine neue Beschreibung.')
table(['Offener Pflichtschluss','Vor einem dynamischen CST-Test erforderlich'],[
 ('D1: Historienträger','Markierte Kausalsets, zulässige Randdaten, 4D-Auswahl und vollständige bzw. kontrolliert abgeschnittene Summe.'),
 ('D2-D3: Wirkung / Maß','Explizite Staubdiskretisierung, BDG-Koeffizienten, Materiemaß, Sektorengewichte ζ<sub>N</sub>, Rand-/Eckterme und Regulatoren.'),
 ('D4: Quantenzustand','Anfangspräparation, inneres Produkt, Normierung und Komposition bzw. konsistentes Dekohärenzfunktional.'),
 ('D5-D7: Auswertung','Relationale Observablen, Gewichte der Vergröberungsfasern, Außenraum sowie vollständiger Laufplan.')],[132,365])
p('Formal kann eine Amplitude als Summe über (C, Materiemarken) mit μ(C, Materie) exp(iS/ℏ) geschrieben werden. Solange die Pflichtschlüsse fehlen, ist dies eine Strukturvorgabe. Ein Faktor 1/|Aut| folgt nur aus dem tatsächlich gewählten Beschriftungsmaß [P3]. Ein Volumenpfad darf nicht ohne Nachweis als geschlossene Markov-Dynamik behandelt werden.',small=True)

start('Endlicher Ball und Außenraum')
p('<b>Referenz REF-DUST-FB-01:</b> marginal gebundener, homogener Einstein-Staubball mit flachem FRW-Inneren und mitbewegter Oberfläche. Außerhalb liegt Schwarzschild mit derselben konstanten Masse M. Der Anfangsradius ist R₀=10 in Referenzeinheiten, G=1. Damit ist der endliche Ball von Anfang an Teil der Prüfung.')
eq('T<sub>s</sub>(M) = (2/3) √(R₀³/(2GM)),     a(T) = (1-T/T<sub>s</sub>)<super>2/3</super><br/>R<sub>b</sub>(T) = R₀a(T),     V(T) = 4πR<sub>b</sub>³/3,     ρ(T) = M/V(T)<br/>Ṙ<sub>b</sub>(0) = -√(2GM/R₀),     m<sub>MS</sub>(R<sub>b</sub>) = M')
p('Ohne Oberflächenschicht gelten im klassischen Modell [h<sub>ab</sub>]=[K<sub>ab</sub>]=0. Der Staubdruck verschwindet auch an der Oberfläche. Ein endlicher Dichtesprung zum Vakuum ist dabei zulässig; ein Delta-Stress oder eine quadrierte Delta-Krümmung darf nicht stillschweigend eingeführt werden.')
h('Drei verschiedene Grenzen')
table(['Grenze','Vertragliche Behandlung'],[
 ('Materieoberfläche','Zeitartige Weltfläche innerhalb der Raumzeit. Kausale Intervalle und Wirkungsbeiträge über die Oberfläche bleiben erhalten.'),
 ('Rechengebiet','Äußere und zeitliche Abschneidung gesondert dokumentieren. Nichtlokale Restbeiträge durch Vergrößerung oder begründete Schranken kontrollieren.'),
 ('q=0 der reduzierten Zelle','Konfigurationsraumrand eines anderen Referenzmodells; keine räumliche Staubballoberfläche.')],[132,365])
h('Bekannter Ausschluss bleibt wirksam')
p('Für das frühere effektive Innere V=b+6πGMt², b&gt;0, ergibt sich m₋=M(1-b/V). Bei mitbewegter Oberfläche und üblichen Einstein-Anschlussbedingungen ohne Schicht ist damit kein Anschluss an konstante Schwarzschild-Masse auf einem offenen Zeitintervall möglich [P1]. Ein anderer Außenraum oder ein modifiziertes Anschlussgesetz muss aus derselben Kandidatentheorie folgen.')
p('Im Vakuum gibt es keinen materiellen Staubzeitgeber. Eine äußere Zeitfoliation wird über die Oberfläche fortgesetzt und eigens spezifiziert. Der hier deklarierte endliche Testbereich liefert keine globale Aussage über Unendlich.',small=True)

start('Messgrößen und Verfeinerung')
table(['Größe','Definition und notwendige Kontrolle'],[
 ('Staubstrom J<super>a</super>','Kontinuumsziel J<super>a</super>=ρu<super>a</super>. Diskret zuerst orientierte Massenflüsse durch relationale Schnitte definieren; Vektorkomponenten erst nach begründetem geometrischem Wörterbuch.'),
 ('Masse / räumliches Volumen','M<sub>Σ</sub>=-∫<sub>Σ</sub>J·n dΣ für zukunftsgerichtetes n. N/λ schätzt Vierervolumen, keine räumliche Scheibe. Schichtbreite ist kein kalibriertes V(T).'),
 ('Dichte / Krümmung','Physikalische Observable mit Maß, Ordnung und Domäne. ⟨M̂⟩⟨V̂⁻¹⟩ ist bei nichtkommutierenden Operatoren kein hergeleiteter Dichteerwartungswert. V⁻² ist kein Krümmungsoperator.'),
 ('Expansionen','Staubexpansion θ=∇·u getrennt von θ±=A⁻¹ dA/dλ±. Nullrichtungen zukunftsgerichtet, Orientierung und Normierung festlegen.'),
 ('Trapping','θ+&lt;0 und θ-&lt;0: künftig gefangene Fläche. θ+=0, θ-&lt;0: künftig marginale Fläche. Ein Horizonttyp benötigt zusätzliche geometrische Bedingungen [L4].')],[126,371])
h('Vier getrennte Änderungen')
p('<b>Numerisch:</b> Gitter, Zeitschritt oder Cutoff bei festem Modell. <b>Statistisch:</b> Anzahl unabhängiger Realisierungen. <b>CST-Verfeinerung:</b> Zähldichte λ in L⁻⁴ und ℓ=λ⁻¹/⁴ bei physikalisch abgeglichenem Gebiet, Zustand und Kopplungen. <b>Physikalische Skalenfamilie:</b> Änderung einer postulierten Naturkonstanten wie ν ist eine eigene Fragestellung.')
p('Nichtlokalitätsskala L<sub>k</sub> und Mittelungsskala L<sub>cg</sub> werden im Laufplan getrennt von ℓ fixiert. Ein späterer L<sub>cg</sub>→0-Grenzgang ist kein Bestandteil eines Tests bei fester Messauflösung. Dichte λ und Materiedichte ρ haben verschiedene Dimensionen.')
p('Der bekannte BD-Operator nähert im Mittel unter Voraussetzungen □-R/2 an [L2]. Eine diskrete Produktidentität oder eine vollständige Krümmungskontrolle folgt daraus nicht. Insbesondere misst der Ricci-Skalar allein keine Schwarzschild-Weylkrümmung.',small=True)

start('Erster Korrespondenztest')
p('<b>PST-FB-01:</b> festgelegter endlicher Screening-Test, derzeit NOT_RUN und wegen D1-D7 nicht für einen CST-Dynamiknachweis zulässig. Die analytische Referenz ist sofort berechenbar. Eine Vorhersage aus dem neuen Kandidaten muss ohne Nachanpassung an die Prüfdaten entstehen.')
table(['Festlegung','Wert / Regel'],[
 ('Massen / Anfangsradius','M=1/4, 1, 4; jeweils R₀=10 und G=1. Anfangsgeschwindigkeit für jede Masse aus dem Zwang bestimmen.'),
 ('Gemeinsames Zeitfenster',f'0 ≤ T ≤ ½ min T<sub>s</sub> = {V["reference_controls"]["T_end"]:.9f}. Fünf Marken bei 0, ¼, ½, ¾, 1 dieses Endwerts.'),
 ('Primäre Messgrößen','R<sub>b</sub>, ρ, H=ȧ/a und ä/a: jeweils 5 % relative Gesamttoleranz an allen Marken und Massen.'),
 ('Erhaltung / Massenantwort','Massenfehler und normalisierter Flussbilanzrest höchstens 2 % von M; initiales Verhältnis |Ṙ(M₂)|/|Ṙ(M₁)|=√(M₂/M₁) mit 5 % Toleranz.'),
 ('Auflösungen','λ₀, 2λ₀, 4λ₀, 8λ₀; absolute λ₀ und physikalischer Abgleich vor Laufstart. Beide feinsten Stufen bestehen; ihr Unterschied höchstens 2,5 % der jeweiligen Referenzgröße.'),
 ('Statistik','Gemeinsame 95-%-Unsicherheitsaussage über alle primären Vergleiche, einschließlich Massenantwort und Stufenvergleich. Methode, Stichprobengröße und Teststärke vor neuen Daten fixieren.')],[133,364])
p('<b>Entscheidung:</b> PASS nur, wenn jedes vollständige Unsicherheitsintervall im vorab gesetzten Toleranzband liegt. Ein davon disjunktes Intervall bedeutet FAIL für den betroffenen Test; Überschneidung bedeutet HOLD. Systematische Fehler werden zusätzlich begrenzt und nicht als unabhängige Zufallsfehler ausgegeben.')
p('Die Zahlen sind gewählte erste Leistungsanforderungen, keine Naturkonstanten. Sie gelten für den endlichen Test; vier Stufen beweisen keinen Kontinuumsgrenzwert. Absolute Dichten, Ensemblegröße, Zustandsbreiten, Randpuffer und statistisches Verfahren bleiben explizite Zulassungsvoraussetzungen. Ein unerreichbares Budget führt zu HOLD, nicht zur nachträglichen Lockerung.',small=True)

start('Regularität als eigene Entscheidung')
p('<b>REGULARITY wird an jedem Prüfpunkt neu bewertet.</b> Die Standardaussage dieser Version betrifft begrenzte und konvergierende physikalische Momente auf einem deklarierten Raumgebiet und Zeitintervall. Eine stärkere Aussage wie punktweise Krümmungsbeschränktheit oder Singularitätsauflösung benötigt zusätzliche Nachweise.')
eq('sup<sub>n,T∈I,ξ∈D</sub> E[(ρ<sub>n</sub>(T,ξ)/ρ*)²] ≤ C<sub>ρ</sub> &lt; ∞<br/>sup<sub>n,T∈I,ξ∈D</sub> E[|K<sub>n</sub>(T,ξ)|/K*] ≤ C<sub>K</sub> &lt; ∞')
p('ξ bezeichnet relationale Messzellen im behaupteten Gebiet D, zunächst bei fester physikalischer Mittelungsskala L<sub>cg</sub>. Lokale Dichtekontrolle kann nicht durch M/V für den gesamten Ball ersetzt werden. An der Oberfläche sind einseitige Grenzen oder ein begründetes aufgelöstes Übergangsprofil nötig.',small=True)
p('ρ*=M/V₀ und K*=(GM/R₀³)² bleiben bei Verfeinerung fest. K bezeichnet nur nach begründetem geometrischem Bezug den Kretschmann-Skalar. Für Quantenobservablen sind Spektralmaße oder ein Messinstrument, geeignete Domänen und die Bedeutung des Betrags anzugeben. Hier wird keine gemeinsame klassische Mehrzeitverteilung vorausgesetzt.',small=True)
table(['Pflicht','Anforderung für PASS im deklarierten Umfang'],[
 ('R1: Definition','Physikalische Dichte-/Krümmungsobservable und Erhaltung der benötigten Domänen belegen.'),
 ('R2: Schranken','Gemeinsame Konstanten aus dem Modell herleiten. Beobachtete Stichprobenmaxima sind keine universellen Schranken.'),
 ('R3: Seltene Beiträge','Uniforme Integrierbarkeit der betroffenen Größen kontrollieren. Null beobachtete Extremereignisse genügt nicht.'),
 ('R4: Verfeinerung','Physikalischen Abgleich und Konvergenz begründen. Begrenzte Momente allein sichern keine Konvergenz ihrer Werte.'),
 ('R5: Zeit / Raum','Intervall und Raumgebiet vollständig abdecken; endlich viele Prüfmarken nur mit kontrollierten Zwischenräumen auf ein Intervall übertragen.')],[123,374])
p('Für eine positive Volumenobservable ist P(V<sub>n</sub>(T)≤v)≤Cv<super>2+δ</super> für 0&lt;v≤v₀ mit gemeinsamen C,v₀,δ&gt;0 ein hinreichender Tail-Nachweis: E[V⁻²]≤v₀⁻²+2Cv₀<super>δ</super>/δ. Erst ein separat bewiesener Operator-/Formvergleich überträgt ihn auf Dichte oder Krümmung [P1]. Das Scheitern dieses hinreichenden Kriteriums allein ist kein Gegenbeweis physikalischer Regularität.',small=True)

start('Prüfpunkte und Entscheidungslogik')
table(['Prüfpunkt','Auslöser und verpflichtender Eintrag'],[
 ('P0: Ausgangsstand','Vertrag, Referenz und Herkunft fixieren. Alle acht CST-Entscheidungen ausgeben; Regularität derzeit HOLD.'),
 ('P1: Modellschluss','Wirkung, Maß, Zustand, Operatoren und Randdaten. Regularität der Präparation separat prüfen.'),
 ('P2: Messkalibrierung','Strom, räumliches Volumen, Dichte und Krümmung. Bias/Varianz und unbekannte Tails getrennt behandeln.'),
 ('P3: Korrespondenz','Für jede Masse, jedes Zeitfenster und jede Auflösung einen Record führen; danach eine gesonderte Gesamtauswertung.'),
 ('P4: Umkehr / Trapping','Am Ereignis und im umgebenden Intervall alle Entscheidungen einschließlich Regularität neu ausgeben.'),
 ('P5: Vollständiges Gebiet','Innen-/Rand-/Außenraum und kausale Fortsetzung prüfen; keine Übertragung eines Innenraum-PASS auf den Außenraum.')],[126,371])
p('<b>PASS:</b> alle Anforderungen der konkreten Aussage belegt. <b>FAIL:</b> eine gültige, im Geltungsbereich liegende Verletzung nachgewiesen. <b>HOLD:</b> Definition, Evidenz oder Kontrolle fehlt. NOT_RUN, RUN und INHERITED sind Ausführungszustände und ersetzen keine dieser Entscheidungen.')
p('Ein gültiger Gegenbeweis kann FAIL begründen, obwohl andere Voraussetzungen ungeklärt sind. Ein Gegenbeispiel aus einer anderen Modellklasse darf dagegen nicht übertragen werden. Bei widersprüchlicher oder noch nicht geprüfter Evidenz bleibt die betreffende Anforderung UNRESOLVED.')
h('Keine automatische Gesamtfreigabe')
p('Die maschinenlesbaren Entscheidungen heißen MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION. Ihre getrennte Ausgabe ist verpflichtend. Das Prüfskript bewertet die Vollständigkeit deklarierter, geprüfter Evidenz; es verifiziert weder mathematische Beweise noch die Wahrheit eines Literaturverweises.')
p('Selbst ein Momenten-PASS ersetzt keine Kontrolle relevanter Gezeitenkomponenten, keine kausale Fortsetzung und keine globale Vollständigkeit. Ein Ereignishorizont erfordert zusätzliche globale Information. Es gibt deshalb keine automatische Ausgabe „Singularität aufgelöst“.',small=True)

start('Übernommene Befunde und Sperren')
table(['Vorhandene Evidenz','Zulässige Verwendung'],[
 ('Reduzierte Einstein-Staub-Referenz [P2]','Klassische Bewegung und semiklassische Kontrollen als Methodenreferenz. Kein Nachweis aus der vollen CST-Summe.'),
 ('Historiengewichtung [P3]','Maß dq=dV/(2√V) für die festgelegte reduzierte Quantisierung. Die volle Materie-/Geometriegewichtung bleibt offen.'),
 ('Dirichlet-Gegenbeispiel [P1]','Anfangs endliches ⟨V⁻²⟩ kann trotz positivem mittlerem Minimum sofort divergieren. FAIL der Momentenerhaltung dieses Modells; keine automatische physikalische Krümmungsaussage.'),
 ('Effektive Innenmetrik [P1]','Bei fester ν bedingt regulär; K<sub>max</sub> wächst in der geprüften ν→0-Familie wie ν⁻⁴. Keine uniforme Grenze in dieser Skalierung.'),
 ('Schwarzschild-Anschluss [P1]','Die geprüfte Bounce-/Rand-/Außenraum-Kombination ist ausgeschlossen. Andere hergeleitete Außenräume bleiben prüfbar.')],[151,346])
h('Pflichtkontrollen für spätere Implementierungen')
p('Labelpermutation darf die Physik nicht ändern. Falsche Volumeneinheiten und die Verwechslung von N/λ mit räumlichem Volumen müssen auffallen. Eine massenblinde Geometrie muss die Rückwirkungsprüfung verfehlen. Künstliches Abschneiden an der Stauboberfläche muss als geändertes Gebiet erkannt werden. Ein Bounce-PASS bei fehlender Tail-Kontrolle muss Regularität auf HOLD lassen.')
p('Für eine spätere Trapping-Prüfung werden bekannte Staubgeometrie und Minkowski-Negativkontrolle verwendet. Ihre bestandene Messkalibrierung ist anschließend von einer dynamischen Entstehung gefangener Flächen zu trennen. Das frühere dominante Bounce-Modell bleibt verworfen; der neue Vertrag setzt diese Entscheidung nicht zurück.')
h('Aktueller Status von CST-DUST-C1')
p('<b>Alle acht physikalischen Entscheidungen: HOLD.</b> Grund sind der offene Modellschluss und fehlende passende dynamische Evidenz. Das bedeutet keine Widerlegung von CST. Es bezeichnet präzise, welche Aussage dieser Kandidat derzeit noch nicht trägt.')

start('Arbeitsfolge und Versionsregeln')
table(['Nächster Baustein','Konkretes Abnahmeergebnis'],[
 ('1. Mikroskopischer Modellschluss','D1-D4 als berechenbare Definitionen schließen; mindestens einen vollständig nachrechenbaren kleinen Fall mit Normierungs-/Symmetriekontrollen liefern.'),
 ('2. Strom und Messgrößen','D5 schließen; Flüsse, Dichte und räumliche Volumina auf der endlichen Referenz kalibrieren, Außenraumfehler bilanzieren.'),
 ('3. Laufmanifest','D6-D7 einschließlich tatsächlicher Skalen, Zustände, Unsicherheitsverfahren, Seeds und erreichbarem Budget fixieren.'),
 ('4. PST-FB-01','Unabhängige Vorhersagen gegen die festgelegten Toleranzen prüfen. An jedem P3-Punkt Regularität separat ausweisen.'),
 ('5. Weiterführende Aussagen','Trapping/Bounce nur mit passender Ereignisdefinition; vollständigen Randanschluss und Fortsetzung separat schließen.')],[131,366])
p('Definitionen von 1 und 2 können parallel vorbereitet werden. Kostenpflichtige Läufe und neue große Ensembles sind für diesen Vertragsschritt nicht vorgesehen. Solange Zulassung oder Teststärke fehlen, bleibt der dynamische Test HOLD / NOT_RUN.')
h('Änderungen sind sichtbar und überprüfbar')
p('Jeder Entscheidungsrecord enthält Vertragsversion und SHA-256, Laufmanifest-Hash, Modellkennung, Raumgebiet, Zeitintervall, Verfeinerung, Evidenzverweise und die einzelnen Entscheidungen. Physikalische und numerische Parameter dürfen nicht unter demselben Namen ausgetauscht werden.')
p('Eine Änderung an Wirkung, Maß, Anfangszustand, Randgesetz, Operator, Toleranz oder Abbruchregel erzeugt vor neuen Prüfdaten eine neue Vertragsversion. Nach Einsicht in Prüfdaten vorgenommene Anpassungen werden als explorativ gekennzeichnet; bestätigende Aussagen benötigen neue unabhängige Daten. Betroffene alte Entscheidungen werden erneut bewertet, nicht überschrieben.')
p('Die alten 27 Entwicklungs- und 17 Prüfpfade sowie frühere Quantenreferenzzustände sind bekannte Daten. Sie dürfen nicht als frische unabhängige Validierung dieses Vertrags etikettiert werden. Ein nachträglich ausgesuchtes Zeitfenster oder ein günstiger Randanschluss zählt als Modelländerung.')

start('Nachrechnung und Quellen')
p(f'<b>Ausgeführt:</b> {V["reference_controls"]["cases"]} klassische Referenzfälle mit je fünf algebraischen Kontrollen und {V["decision_control_cases"]} Kontrollen der Entscheidungslogik. Keine neuen CST-Historien. Größter relativer Identitätsrest: {V["reference_controls"]["max_relative_residual"]:.2e}. Das sind Gleitkommakontrollen, keine Intervallzertifikate.')
eq('python3 verify.py<br/>python3 gate.py examples/checkpoint_P0.json')
p('contract.json ist die maschinenlesbare Festlegung; CONTRACT.md und dieser Bericht beschreiben denselben Stand. gate.py hält fehlende Regularität, fehlende Tails und unpassende Evidenz zurück. results/ enthält Referenzwerte, Kontrollen und den Ausgangsrecord. Reproduktion der PDF: Python mit ReportLab und DejaVu Sans, danach python3 make_report.py.',small=True)
h('Projektquellen, unveränderter veröffentlichter Stand')
base='https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/feebbeed17d83b3cb058ffecc2debd9af1000375/research/rax_cqg/dust_collapse/'
for label,folder,title in [('P1','regularity_v0_2','Regularität, Rand und Verfeinerung v0.2'),('P2','classical_backreaction_v0_1','Klassische Staubbewegung und Rückwirkung v0.1'),('P3','history_weighting_v0_1','Historiengewichtung v0.1')]:
 p(f'[{label}] Projektbericht: <link href="{base}{folder}/PUBLICATION.md">{title}</link>. Die Veröffentlichungsübersicht ist im Paket archiviert; Beweise und Prüfdaten sind dort verlinkt.',small=True)
h('Primärliteratur und Reichweite')
for s in [
 '[L1] Brown, Kuchař (1995), <link href="https://arxiv.org/abs/gr-qc/9409001">Dust as a Standard of Space and Time in Canonical Quantum Gravity</link>. Motivation der gekoppelten Staubreferenz; kein CST-Modellschluss.',
 '[L2] Belenchia, Benincasa, Dowker (2016), <link href="https://arxiv.org/abs/1510.04656">The continuum limit of a 4-dimensional causal set scalar d’Alembertian</link>. Grenzwert des Mittelwerts unter Voraussetzungen; kein Beweis beschränkter Krümmungsfluktuationen.',
 '[L3] Dowker, Liu, Lloyd-Jones (2025), <link href="https://arxiv.org/abs/2501.00139">Timelike boundary and corner terms in the causal set action</link>. Analytische/numerische Evidenz für zeitartige Randbeiträge in Minkowski-Teilgebieten; kein Anschlussgesetz für gekrümmten Staub.',
 '[L4] Hayward (1994), <link href="https://arxiv.org/abs/gr-qc/9303006">General Laws of Black-Hole Dynamics</link>. Lokale marginale Flächen und Trapping-Horizonte; keine Übertragung ihrer klassischen Gesetze ohne Voraussetzungen auf einen Quantenzustand.'
 ]:p(s,small=True)
p('Quellenabruf: 6. November 2026. Dateien und Prüfsummen: inputs/provenance.json und SHA256SUMS. Der Vertrag schafft prüfbare Zuständigkeiten für die Nachweise; er behauptet keine neue Singularitätsauflösung.',small=True)

def footer(canvas,doc):
 canvas.setStrokeColor(TEAL);canvas.setLineWidth(.6);canvas.line(49,42,546,42)
 canvas.setFont('D',8);canvas.setFillColor(INK)
 canvas.drawString(49,29,'X6 Astrolabium · CST-DUST-MC-001 · v0.1.0')
 canvas.drawRightString(546,29,f'{doc.page} / {page_count}')

pdf=ROOT/'CST_DUST_Model_Contract_v0_1.pdf'
doc=SimpleDocTemplate(str(pdf),pagesize=(595.276,841.89),leftMargin=49,rightMargin=49,
 topMargin=43,bottomMargin=56,title='CST-DUST Model Contract v0.1',author='X6 Astrolabium - Arbeitsdokument',pageCompression=1)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
(ROOT/'CONTRACT.md').write_text('# CST-DUST Model Contract v0.1\n\n'+ '\n'.join(md))
print(pdf)
