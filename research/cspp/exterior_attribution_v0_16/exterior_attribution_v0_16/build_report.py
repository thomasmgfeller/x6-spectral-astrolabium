"""Build the review report from certified archived outputs."""
import gzip,json,math
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
from flint import arb

HERE=Path(__file__).resolve().parent
OUT=HERE.parent/'output';OUT.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('D','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DB','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DM','/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleD',fontName='DB',fontSize=24,leading=30,textColor=colors.HexColor('#133b50'),spaceAfter=14))
styles.add(ParagraphStyle(name='SubD',fontName='D',fontSize=10,leading=15,textColor=colors.HexColor('#536873'),spaceAfter=14))
styles.add(ParagraphStyle(name='BodyD',fontName='D',fontSize=9.5,leading=14,spaceAfter=8))
styles.add(ParagraphStyle(name='HeadD',fontName='DB',fontSize=14,leading=19,textColor=colors.HexColor('#133b50'),spaceBefore=10,spaceAfter=9))
styles.add(ParagraphStyle(name='SmallD',fontName='D',fontSize=8,leading=11,spaceAfter=7))
styles.add(ParagraphStyle(name='CellD',fontName='D',fontSize=7.8,leading=10.5))
styles.add(ParagraphStyle(name='CodeD',fontName='DM',fontSize=8.1,leading=12,spaceAfter=10,backColor=colors.HexColor('#eef3f6'),borderPadding=8))
def p(s,sty='BodyD'):return Paragraph(s,styles[sty])
def code(s):return p(escape(s).replace('\n','<br/>'),'CodeD')
def head(s):return p(s,'HeadD')
def table(rows,widths):
    cells=[[p(str(x),'CellD') for x in row] for row in rows]
    t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e3edf2')),('VALIGN',(0,0),(-1,-1),'TOP'),
       ('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#afc4d0')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f4f7f9')]),
       ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    return t
def outward(x,upper=False,digits=6):
    z=arb(x[0])*10**digits
    n=int((z.upper().ceil() if upper else z.lower().floor()).unique_fmpz())
    return f'{n/10**digits:.{digits}f}'

def build():
    checks=json.loads((HERE/'results/CHECKS.json').read_text())
    with gzip.open(HERE/'results/ATTRIBUTION_192.json.gz','rt') as f:out=json.load(f)
    doc=SimpleDocTemplate(str(OUT/'Aeussere_Forcierung_v0_16.pdf'),pagesize=(595.276,841.89),
        rightMargin=43,leftMargin=43,topMargin=53,bottomMargin=48,title='CSPP v0.16 - Äussere Forcierung des kompakten Detektors',author='Thomas Gfeller / Forschungsprojekt X6')
    s=[]
    s+=[p('Äussere Forcierung<br/>des kompakten Detektors','TitleD'),p('CSPP v0.16 | 29. Oktober 2026 | Entwicklungsdiagnose auf vorhandenen Daten','SubD')]
    s+=[head('Ergebnis'),p('<b>Die endliche Erweiterung von Ω4 auf Ω5 rettet die bisherige Operatorzelle beim ursprünglichen kompakten Detektor nicht.</b> In allen acht Fällen bleibt die zertifizierte Fehleruntergrenze der vollständigen Ω5-Evolution über dem unveränderten Ziel 0,001. Selbst die kleinste Untergrenze ist grösser als 0,006697.')]
    s+=[p('Auch die getrennte Kontrolle mit vorgeschriebenen äusseren Klein-Gordon-Werten erreicht das Ziel in keinem der acht Fälle. Quelle, Masse, Glättung, Detektorball und beide vollständigen Zeitfenster bleiben unverändert.')]
    s+=[table([['Geprüfter Punkt','Befund'],['Vier vorhandene Gebietspaare, zwei Fenster','8 von 8 endlichen Konfigurationen ausgeschlossen'],['Aktive äussere KG-Referenz','Exakt null bis zum Ende des Detektors'],['Zusätzliche aktive diskrete Aussenwerte','16 von 23 Knoten nachweislich ungleich null; ihr zusätzlicher Detektorbeitrag bleibt unter 0,000010'],['Gesamte fehlende Vergangenheit','Rest jenseits Ω5 weiterhin nicht numerisch zertifiziert']],[185,324])]
    s+=[Spacer(1,12),p('<b>METHOD_HOLD und G1 HOLD bleiben bestehen.</b> Kein verbesserter Operator ist freigegeben, kein frisches Ensemble wurde erzeugt. Die ganze Operatorfamilie wird durch diese Rechnung nicht verworfen.')]
    s+=[head('Was neu geklärt ist'),p('Der Aussenbeitrag wird jetzt am tatsächlichen kompakten Detektor eingeschlossen: direkt sowie über den Transport durch die innere Dynamik. Zusätzlich wird sichtbar, welche Antwort aus vorgeschriebener KG-History und welche aus der diskreten Entwicklung aktiver Aussenpunkte stammt.')]
    s+=[PageBreak(),head('1. Zwei Fortsetzungen sauber auseinanderhalten')]
    s+=[p('Die unveränderte Anfangsfläche liegt bei t = -1. Der kompakte Anfangswert hat Radius 1/2 und Trägerwellenzahl 4, die Anfangsgeschwindigkeit ist null; m = 1, ρ = 3/π und ε = 1/16. Alle Antworten sind durch das ursprüngliche Anfangsmaximum A/e normiert. Das Fehlerziel 0,001 ist in derselben Normierung angegeben.')]
    s+=[p('Für die lokale KG-Referenz gilt endliche Ausbreitung: r ≤ |t+1| + 1/2. Im aktiven Zeitraum -1 &lt; t ≤ 5/4 ergibt sich r ≤ t + 3/2. Die Grenze von Ω4 liegt bei r = 4 - |t|; bis t = 5/4 umfasst sie diesen gesamten Träger. Deshalb ist die aktive äussere KG-Referenz exakt null. Für die frühere History gilt dieser Schluss nicht.')]
    s+=[table([['Fortsetzung','Vorschrift'],['KG-Aussenwerte vorgeschrieben','Äussere History = unveränderte KG-Lösung; aktive Aussenwerte = 0. Innere Gleichungen werden gelöst.'],['Volle diskrete Ω5-Evolution','KG-History auf allen Punkten t ≤ -1. Danach werden alle aktiven Gleichungen gelöst, einschliesslich der Aussenpunkte.']],[175,334])]
    s+=[head('2. Exakter Transport zum Detektor'),p('H bezeichnet innere History, A innere aktive Knoten und E zusätzliche relevante Aussenknoten. Kausale Konvexität erhält die inneren Intervallzahlen und integrierten Detektorkoeffizienten. Mit identischer innerer History gilt:')]
    s+=[code('R_A = (I - K_AA)^(-1)\nL_E = Q_E + Q_A R_A K_AE\nΔA = A5 - A4 = L_E v_E')]
    s+=[p('Die endliche Inverse existiert wegen der streng kausalen Dreiecksstruktur. Q_E v_E ist der direkte Beitrag, Q_A R_A K_AE v_E sein zusätzlicher Transport durch das Innere. Der zweite Term darf nicht weggelassen werden.')]
    s+=[code('ΔA_full = L_EH h_EH + L_EA v_EA,full\nΔA_KG   = L_EH h_EH')]
    s+=[p('Die vollständige diskrete Erweiterung und die KG-Randvorschrift sind deshalb verschiedene kontrollierte Rechnungen. Aus der Differenz der Gebiete allein folgt noch kein reiner intrinsischer Operatorbias.','SmallD')]
    s+=[PageBreak(),head('3. Ergebnisse für beide vollständigen Zeitfenster'),p('W1 = [3/4, 1], W2 = [1, 5/4]. Die Tabelle zeigt konservativ nach aussen gerundete Schranken. Die Fehler sind Beträge komplexer, normierter Raum-Zeit-Mittelwerte, keine Prozentwerte.')]
    rows=[['Archiv / Fenster','|A5 - A4|<br/>untere / obere Schranke','Fehler Ω5<br/>mindestens','Fehler KG-<br/>Randvorschrift<br/>mindestens']]
    for row in out['rows']:
        for wi,w in enumerate(row['windows']):
            q=w['levels'][-1]['quantities']
            rows.append([row['key']+f' / W{wi+1}',outward(q['shell_change']['abs_lower'])+' / '+outward(q['shell_change']['abs_upper'],True),outward(q['extended_error']['abs_lower']),outward(q['KG_prescribed_error']['abs_lower'])])
    s+=[table(rows,[100,161,122,126]),Spacer(1,12)]
    s+=[p('<b>Beide endlichen Vorschriften verfehlen das Ziel 0,001 in allen acht Fällen.</b> Der grösste eingeschlossene Betrag der gesamten Schalenänderung ist kleiner als 0,003801. Der innere Transportterm ist in fünf Fällen nachweislich ungleich null; seine Betragsobergrenze bleibt überall unter 0,000568.')]
    s+=[p('Die zusätzlich erzeugten aktiven Aussenwerte sind klein in ihrer Wirkung auf diesen Detektor: Der entsprechende Antwortbeitrag ist überall kleiner als 0,000010. Diese Zahl erklärt nicht den gesamten verbleibenden Fehler; insbesondere ist sie keine Schranke für die unberechnete Vergangenheit jenseits Ω5.')]
    s+=[head('Numerische Auflösung und Aussagekraft'),p('Nur zwei von acht Schalenänderungen erreichen mit dem festgelegten Gitter die Komponentenradius-Marke 0,001. In sechs Fällen ist die Einschliessung breiter; es wird keine nachträgliche Präzisionsfreigabe behauptet. Der Genauigkeitsausschluss der beiden endlichen Vorschriften bleibt trotzdem gültig, weil bereits ihre konservativen Fehleruntergrenzen deutlich über 0,001 liegen.')]
    s+=[p('Die fortgepflanzte Unsicherheit der KG-Historyquadratur liegt unter 5,6 × 10⁻²³. Der sichtbare Integrationsrest kommt hier vor allem aus den Raumsektoren des Detektors, nicht aus fehlenden Dezimalstellen der Historywerte.','SmallD')]
    s+=[PageBreak(),head('4. Was der Rest jenseits Ω5 leisten müsste'),p('Sei ℓ5 die zertifizierte Untergrenze für |A5 - Aref| und τ = 0,001. Falls eine spätere unendliche Fortsetzung das Ziel überhaupt erreichen soll, muss ihre zusätzliche Antwort R5 mindestens folgende notwendige Reparaturgrösse haben:')]
    s+=[code('|R5| >= max(0, l5 - tau)  [notwendig für Genauigkeit]\n|R5| <= eta  =>  |A_infinity - Aref| >= l5 - eta')]
    rows=[['Archiv','Notwendige spätere Korrektur W1','Notwendige spätere Korrektur W2']]
    for ri,row in enumerate(out['rows']):
        rr=checks['comparisons'][2*ri:2*ri+2]
        rows.append([row['key']]+[outward(r['necessary_beyond5_correction_lower']) for r in rr])
    s+=[table(rows,[111,199,199]),Spacer(1,10)]
    s+=[p('Schon im günstigsten dieser acht Fälle wäre eine spätere Korrektur von mehr als 0,005697 nötig. <b>Das ist keine behauptete Untergrenze des tatsächlichen unbekannten Rests.</b> Es ist eine notwendige Bedingung dafür, dass weitere Vergangenheit die Genauigkeit noch retten könnte.')]
    s+=[head('Eine gültige globale Restgrenze braucht mehr'),p('Für eine deklarierte, konsistente Folge kausal konvexer Erweiterungen sei dₖ = Aₖ₊₁ - Aₖ. Wenn für alle k ≥ 5 bewiesene Schranken bₖ ≥ |dₖ| vorliegen und ihre Summe endlich ist, folgt:')]
    s+=[code('A∞ existiert;  |A∞ - A5| <= Σ(k>=5) b_k')]
    s+=[p('Eine geometrische Majorante C θᵏ⁻⁵ mit 0 ≤ θ &lt; 1 ergäbe C/(1-θ). Eine einzige beobachtete Schale beweist weder C noch θ für die restliche Vergangenheit. Ebenso muss ein gewichteter Aussenfeldansatz die vollständigen Transportkoeffizienten und eine summierbare Feldschranke kontrollieren.')]
    s+=[p('<b>Globale Attribution: NOT_CERTIFIED.</b> Die vorliegende Arbeit schliesst die endliche Ω4→Ω5-Rechnung ab und quantifiziert die Voraussetzung für den nächsten Restnachweis. Sie setzt den unbekannten Rest nicht auf null und ersetzt keinen Existenz- oder Stabilitätsbeweis.')]
    s+=[PageBreak(),head('5. Validierung, Reproduktion und Entscheidung')]
    s+=[table([['Kontrolle','Ergebnis'],['128-/192-Bit-History und lineare Auswertung','2.003 Intervallvergleiche gleicher Zielgrössen überlappen'],['Unabhängige exakte Kausalzählungen','64 Intervalle mit rationaler Fraction-Arithmetik bestätigt'],['Rationaler Kontrollgraph','Explizite Pfadsummen; drei falsche Varianten verworfen; insgesamt sechs algebraische Kontrollen'],['Öffentliche Quelldateien','126 Git-Blob-Identitäten des mitgelieferten Vorgänger-Snapshots bestätigt'],['Raumquadratur','Eine zertifizierte 192-Bit-Integration, gemeinsam verwendet; keine zwei unabhängigen Integrationen']],[214,295])]
    s+=[Spacer(1,10),p('Alle vier vorhandenen Paare bleiben erhalten. Unmögliche Vorfahren des gesamten Detektorbereichs werden durch exakte rationale Geometrie entfernt; die Gleichheit aller verbleibenden Intervallzahlen wird geprüft. Die Gitter 4, 8, 16 und sämtliche Ziele wurden vor der neuen Ergebnisproduktion festgelegt.')]
    s+=[p('Eine dokumentierte algebraische Nachbesserung vermeidet unnötige Intervallaufweitung beim inneren Transportterm. Der erste Code- und Ergebnisstand bleibt in development_initial erhalten. Die Nachbesserung ändert weder die exakten Zielgrössen noch Daten, Gitter oder Fehlerziele. Quellen und Eingaben sind gehasht; Prüfer und Bericht sind nachgelagerte Auswertung.')]
    s+=[code('python3 -m pip install -r exterior_attribution_v0_16/requirements.txt\npython3 -B exterior_attribution_v0_16/exterior.py solve --bits 128\npython3 -B exterior_attribution_v0_16/exterior.py solve --bits 192\npython3 -B exterior_attribution_v0_16/verify.py')]
    s+=[p('Python 3.12.14, NumPy 2.3.5, python-flint 0.8.0; C++17 ohne fast-math und ohne FMA-Kontraktion. Die vollständige Neuberechnung der Detektorkoeffizienten ist im README beschrieben.','SmallD')]
    s+=[p('<b>Anschlussentscheidung:</b> Keine Genauigkeitsfreigabe für die untersuchten endlichen Fortsetzungen. Ein frisches Ensemble bleibt gesperrt. Für eine globale Operatorzuordnung ist jetzt eine bewiesene transportierte Restmajorante nötig; weitere endliche Gebietstabellen allein ersetzen sie nicht.','BodyD')]
    s+=[p('<b>Quellen und Einordnung</b><br/>Projektbasis: PR #147, Commit 61ff6bfae105b14d3dfd69359f11b8f0516872ec; v0.10, v0.12, v0.15.<br/>Aslanbeigi, Saravani, Sorkin (2014): <link href="https://arxiv.org/abs/1403.1622" color="#174d72">arxiv.org/abs/1403.1622</link> - Mittelwertoperatoren und separate Stabilitätsfrage.<br/>Belenchia, Benincasa, Dowker (2016): <link href="https://arxiv.org/abs/1510.04656" color="#174d72">arxiv.org/abs/1510.04656</link> - Mittelwert-Kontinuumsgrenze unter Skalenbedingungen. Beide Arbeiten sind kein externer Beleg der hier berechneten Archivwerte.','SmallD')]
    def footer(c,d):
        c.setFont('D',8);c.setFillColor(colors.HexColor('#536873'))
        c.drawString(43,815,'CSPP | Äussere Forcierung und endliche Fehlerzuordnung')
        c.drawRightString(552,815,'v0.16 | 29.10.2026')
        c.setStrokeColor(colors.HexColor('#c5d5dd'));c.line(43,38,552,38)
        c.drawString(43,25,'Entwicklungsdiagnose | METHOD_HOLD und G1 HOLD bleiben bestehen')
        c.drawRightString(552,25,str(d.page))
    doc.build(s,onFirstPage=footer,onLaterPages=footer)
    print(OUT/'Aeussere_Forcierung_v0_16.pdf')

if __name__=='__main__':build()
