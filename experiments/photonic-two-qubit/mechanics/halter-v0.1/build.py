from pathlib import Path
import json, math, hashlib, shutil, zipfile
import cadquery as cq
import ezdxf
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

P=Path(__file__).resolve().parent; P.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont('DejaVu','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuBold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
C=canvas.Canvas(str(P/'X6_Halterzeichnungen_v0_1.pdf'),pagesize=(420*mm,297*mm))
parts=[]; validations=[];doc=None;msp=None
def cylinder(radius,length,pos,direction):return cq.Solid.makeCylinder(radius,length,cq.Vector(*pos),cq.Vector(*direction))
def plate(w,d,h):return cq.Workplane('XY').box(w,d,h,centered=(True,True,False)).val()
def slotcut(shape,x,y,r,travel,h):
 s=cq.Workplane('XY').center(x,y).slot2D(2*r+travel,2*r,90).extrude(h).val()
 return shape.cut(s)
def savepart(code,title,s,dim,threads):
 assert s.isValid() and len(s.Solids())==1 and s.Volume()>0
 path=P/(code+'.step');cq.exporters.export(s,str(path))
 back=cq.importers.importStep(str(path)).val();assert back.isValid()
 assert abs(back.Volume()-s.Volume())<1e-5
 parts.append(dict(id=code,title=title,dimensions_mm=dim,threads=threads,status='DESIGN_HOLD',material='Aluminium EN AW-6082 T6 (Entwurf)' if code!='H02' else 'Nichtrostender Stahl (Sorte OPEN)',volume_mm3=s.Volume()))
 validations.append(dict(id=code,solid_valid=True,solids=1,step_roundtrip_volume_error_mm3=abs(back.Volume()-s.Volume())))

# Exact design solids. Threads represented by tap-drill cylinders, never as finished bores.
s=plate(50,35,12)
for x in [-18,18]:s=slotcut(s,x,0,3.3,12,12)
s=s.cut(cylinder(3.3,12,(0,0,0),(0,0,1))).cut(cylinder(5.5,6.5,(0,0,0),(0,0,1)))
savepart('H01','Sockel mit Langloechern',s,[50,35,12],[])
s=cylinder(6,41,(0,0,0),(0,0,1)).cut(cylinder(2.5,8,(0,0,0),(0,0,1))).cut(cylinder(1.65,8,(0,0,41),(0,0,-1)))
savepart('H02','Stativ fuer H03',s,[12,12,41],[{'face':'unten','thread':'M6x1','effective_depth':6.5,'pilot_depth':8},{'face':'oben','thread':'M4x0.7','effective_depth':6,'pilot_depth':8}])
s=plate(44,10,44).cut(cylinder(11,10,(0,-5,22),(0,1,0))).cut(cylinder(12.8,8,(0,-5,22),(0,1,0)))
for x in [-17,17]:
 for z in [5,39]:s=s.cut(cylinder(1.25,6,(x,-5,z),(0,1,0)))
s=s.cut(cylinder(1.65,6.8,(0,0,0),(0,0,1)))
savepart('H03A','Fassungskorpus D25.4 - Szenario',s,[44,10,44],[{'face':'vorn 4x','thread':'M3x0.5','effective_depth':4.5,'pilot_depth':6},{'face':'unten','thread':'M4x0.7','effective_depth':5,'pilot_depth':6.8}])
s=plate(44,3,44).cut(cylinder(11,3,(0,-1.5,22),(0,1,0)))
for x in [-17,17]:
 for z in [5,39]:s=s.cut(cylinder(1.7,3,(x,-1.5,z),(0,1,0)))
savepart('H03B','Deckring fuer H03A',s,[44,3,44],[])
for code,w,d,xc in [('H04',60,40,20),('H05',70,40,25)]:
 s=plate(w,d,8)
 for x in [-xc,xc]:
  for y in [-10,10]:s=slotcut(s,x,y,2.25,6,8)
 s=s.cut(cylinder(2.5,8,(0,0,0),(0,0,1)))
 savepart(code,'Modul-Adapter' if code=='H04' else 'Faserkoppler-Adapter',s,[w,d,8],[{'face':'unten','thread':'M6x1','effective_depth':5,'pilot_depth':8}])

def txt(x,y,t,size=3,bold=False):
 C.setFont('DejaVuBold' if bold else 'DejaVu',size);C.drawString(x,y,t)
 if msp is not None:msp.add_text(t,dxfattribs={'height':size,'insert':(x,y),'layer':'TEXT'})
def line(x1,y1,x2,y2,dash=False):
 C.setDash([2,1] if dash else []);C.line(x1,y1,x2,y2);C.setDash([])
 if msp is not None:msp.add_line((x1,y1),(x2,y2),dxfattribs={'layer':'CENTER' if dash else 'GEOMETRY'})
def rect(x,y,w,h):
 for a,b,c,d in [(x,y,x+w,y),(x+w,y,x+w,y+h),(x+w,y+h,x,y+h),(x,y+h,x,y)]:line(a,b,c,d)
def circle(x,y,r):
 C.circle(x,y,r,stroke=1,fill=0)
 if msp is not None:msp.add_circle((x,y),r,dxfattribs={'layer':'GEOMETRY'})
def slot(x,y,r,t):
 C.line(x-r,y-t/2,x-r,y+t/2);C.line(x+r,y-t/2,x+r,y+t/2)
 C.arc(x-r,y+t/2-r,x+r,y+t/2+r,0,180);C.arc(x-r,y-t/2-r,x+r,y-t/2+r,180,180)
 if msp is not None:
  msp.add_line((x-r,y-t/2),(x-r,y+t/2));msp.add_line((x+r,y-t/2),(x+r,y+t/2))
  msp.add_arc((x,y+t/2),r,0,180);msp.add_arc((x,y-t/2),r,180,360)
def dh(x1,x2,y,label):
 line(x1,y,x2,y);line(x1,y-2,x1,y+2);line(x2,y-2,x2,y+2);txt((x1+x2)/2-5,y+2,label,2.6)
def dv(x,y1,y2,label):
 line(x,y1,x,y2);line(x-2,y1,x+2,y1);line(x-2,y2,x+2,y2);txt(x+2,(y1+y2)/2,label,2.6)
def notes(items):
 y=239
 for t in items:
  for ln in t.split('\n'):txt(282,y,ln,3);y-=5
  y-=4
def begin(code,title,page):
 global doc,msp
 doc=ezdxf.new('R2010');doc.units=4;msp=doc.modelspace()
 for layer,col in [('GEOMETRY',7),('CENTER',4),('TEXT',7)]:doc.layers.new(layer,dxfattribs={'color':col})
 C.saveState();C.scale(mm,mm);C.setLineWidth(.22);C.setStrokeColorRGB(.13,.19,.25);C.setFillColorRGB(.13,.19,.25)
 rect(10,10,400,277);txt(18,274,title,6,True)
 txt(18,263,'KONSTRUKTIONSENTWURF / HOLD - NICHT ZUR FERTIGUNG FREIGEGEBEN',3.5,True)
 line(275,53,275,252);line(10,49,410,49);line(10,25,410,25)
 txt(17,39,f'X6 PHOTONIK | {code} | Revision 0.1 | 05.11.2026',3.5,True)
 txt(17,31,'Einheiten: mm | Einzelteilansichten 1:1 bei Druck 100 % auf A3 | Gewinde symbolisch',3)
 txt(17,17,'Abnahme: offen | Auslegung / Schnittstellen: siehe Hinweise | Keine Hardwaremessung',3)
 txt(375,17,f'Blatt {page}/9',3)
def end(code):
 doc.saveas(P/(code+'.dxf'));C.restoreState();C.showPage()

begin('00','Halter und Adapter - Konstruktionssatz',1)
for i,(k,t) in enumerate([('H01','Sockel 50 x 35 x 12; zwei M6-Langloecher'),('H02','Stativ D12 x 41; M6 unten / M4 oben'),('H03A','Linsen-/Filterfassung fuer D25.4-Szenario'),('H03B','Deckring D22; passend zum Fassungskorpus'),('H04','Adapter 60 x 40 x 8 fuer Modulanschluss'),('H05','Adapter 70 x 40 x 8 fuer Faserkoppelmodul')]):txt(23,238-i*15,k+'   '+t,4)
txt(23,132,'75 mm Strahlhoehe = 12 + 41 + 22 mm',5,True)
txt(23,118,'Gueltig nur fuer H01 + H02 + H03A ohne Zwischenlage.',3.5)
txt(23,108,'Optische Zentren bleiben Layout-Sollwerte, keine Bohrkoordinaten.',3.5)
txt(23,93,'Nicht einzeln tolerierte Masse: +/-0.10 mm (Entwurfsvorschlag).',3.5)
txt(23,83,'Werkstoff, Finish, Passungen und Gewindeklasse vor Fertigung bestaetigen.',3)
notes(['Basis: Layout 800 x 600, Strahlhoehe 75.', 'Eigene mechanische Entwurfsmasse;\nkeine Hersteller-Anschlusszeichnung.', 'H03 ist eine starre Fassung.\nKeine Kipp-/XY-Feinjustage integriert.', 'Spiegel, Wellenplatten, PBS und\nFaserkoppler brauchen weiterhin\npassende Justier-/Rotationsmodule.', 'H04/H05 sind Adapter, keine\nfertigen Kristall-/PBS-/Faserhalter.', 'Vor Fertigung: Teilemasse, CAD-Kollision,\nKlemmung, Toleranzen und Werkstoff\nmit Lieferanten schliessen.'])
end('00_Uebersicht')
begin('H01','H01 - Sockelplatte',2)
rect(55,170,50,35)
for x in [62,98]:slot(x,187.5,3.3,12)
circle(80,187.5,3.3);circle(80,187.5,5.5);line(80,164,80,211,True)
dh(55,105,217,'50');dv(115,170,205,'35');dh(62,98,157,'36');txt(51,232,'Draufsicht (+Z)',3.5,True)
rect(55,99,50,12);line(76.7,99,76.7,111,True);line(83.3,99,83.3,111,True);dv(115,99,111,'12')
txt(51,126,'Vorderansicht',3.5,True)
notes(['Platte: 50 x 35 x 12.', '2x Langloch durch:\nBreite 6.6, Endradius 3.3;\nMittenhub 12, Gesamtlaenge 18.6.', 'Langlochmitten X = +/-18, Y = 0.\nUrsprung: Plattenmitte unten.', 'Mitte: D6.6 durch; von unten\nD11 x 6.5 tief als Kopfsenkung.', 'Vorgesehener Schraubenkopf:\nD <= 10.5, Hoehe <= 6.0.', 'Ober-/Unterseite plan; Entwurf:\nDicke +/-0.05; Ebenheit 0.05.\nKanten 0.3 brechen.', 'Grundplatten-Bohrbild OPEN.\nLangloecher sind kein Feinjustiertisch.'])
end('H01_Zeichnung')
begin('H02','H02 - Stativ fuer 75-mm-Strahlhoehe',3)
rect(64,151,12,41);dh(64,76,204,'D12');dv(88,151,192,'41')
line(70,144,70,198,True)
for x in [67.5,72.5]:line(x,151,x,159,True)
for x in [68.35,71.65]:line(x,184,x,192,True)
circle(70,115,6);circle(70,115,1.65);txt(50,99,'Draufsicht',3.5)
notes(['Laenge 41.00 +/-0.05.', 'Unten: M6 x 1, tragend >=6.5;\nKernloch D5 x 8 tief.', 'Oben: M4 x 0.7, tragend >=6;\nKernloch D3.3 x 8 tief.', 'STEP zeigt Kernloechercylinder;\nGewinde und Bohrspitzen sind\nFertigungsmerkmale, nicht modelliert.', 'Stirnflaechen parallel 0.03.\nHoehenkette ohne Unterlegscheiben.', 'M4-Verbindung zu H03A:\nEinschraubtiefe im Korpus max. 5.\nGewindestiftlaenge abstimmen.', 'Andere Module: L = 75 - 12 - h.\nh: gesamte Hoehe ab Stativauflage\nbis optischer Achse, real messen.'])
end('H02_Zeichnung')
for page,code,depth in [(4,'H03A',10),(5,'H03B',3)]:
 begin(code,code+' - '+('Fassungskorpus' if code=='H03A' else 'Deckring'),page)
 rect(48,161,44,44);circle(70,183,11)
 if code=='H03A':circle(70,183,12.8)
 for x in [53,87]:
  for z in [166,200]:circle(x,z,1.25 if code=='H03A' else 1.7)
 line(70,155,70,211,True);line(42,183,98,183,True)
 dh(48,92,221,'44');dv(108,161,205,'44');dh(53,87,148,'34')
 txt(44,236,'Vorderansicht (-Y)',3.5,True)
 # Actual section through optical centre, Y horizontal and Z vertical.
 
 if code=='H03A':
  for q in [(155,161,158.35,161),(161.65,161,165,161),(155,161,155,170.2),(165,161,165,170.2),(155,170.2,165,170.2),(158.35,161,158.35,167.8),(161.65,161,161.65,167.8),(158.35,167.8,161.65,167.8)]:line(*q)
 else:rect(155,161,depth,11)
 rect(155,195.8 if code=='H03A' else 194,depth,9.2 if code=='H03A' else 11)
 if code=='H03A':
  rect(163,170.2,2,1.8);rect(163,194,2,1.8)
  line(160,157,160,212,True)
 dh(155,155+depth,221,str(depth));txt(143,236,'Mittelschnitt',3.5,True)
 if code=='H03A':notes(['Aussen 44 x 10 x 44.\nAchse Z=22.00 +/-0.05.', 'Sitz D25.60 +0.05/0, Tiefe 8.00.\nDurchlass D22, Schulterdicke 2.', '4x M3 x 0.5 von vorn, tragend 4.5;\nKernloch D2.5 x 6 tief.\nX=+/-17, Z=5/39.', 'Unten mittig M4 x 0.7, tragend 5;\nKernloch D3.3 x 6.8 tief.\nBohrspitze darf Sitz nicht erreichen.', 'D25.4 und Sitzgeometrie sind\nANNAHMEN; reale Randdicke,\nWoe lbung und freie Apertur OPEN.'.replace('Woe lbung','Woelbung'), 'Keine blanke Metallklemmung am Glas.\nWeiche Zwischenlagen, Distanzring\nund Klemmkraft erst nach Glasdaten.', 'Sitzmass gilt nach Oberflaechenfinish.\nKeine Linsenlage/Fokuslage zugesichert.'])
 else:notes(['Aussen 44 x 3 x 44.', 'Zentraler Durchlass D22 durch.', '4x D3.4 durch; X=+/-17, Z=5/39.\nKopfschrauben von vorn,\nKorpusgewinde M3.', 'Deckring nur mit passendem\nDistanz-/Zwischenlagenpaket montieren.\nNicht bis zum Glas festziehen.', 'Bei kleinen Randdicken:\naxiale Distanz = 8 - t_Rand -\nSumme_Zwischenlagen (Entwurf).\nNegative Distanz: unpassend.', 'Gekruemmte Flaechen, Keil,\nBauhoehe und Spannungsfreiheit\nseparat pruefen.', 'D22 kann Nutzapertur begrenzen;\nVignettierung vor Freigabe rechnen.'])
 end(code+'_Zeichnung')
for page,code,w,xc in [(6,'H04',60,20),(7,'H05',70,25)]:
 begin(code,code+' - '+('Modul-Adapterplatte' if code=='H04' else 'Faserkoppler-Adapterplatte'),page)
 rect(45,165,w,40)
 for x in [45+w/2-xc,45+w/2+xc]:
  for y in [175,195]:slot(x,y,2.25,6)
 circle(45+w/2,185,2.5);dh(45,45+w,219,str(w));dv(45+w+10,165,205,'40')
 rect(45,107,w,8);dv(45+w+10,107,115,'8')
 notes([f'Aussen {w} x 40 x 8.', '4x Langloch parallel Y, durch:\nBreite 4.5, Endradius 2.25,\nMittenhub 6, Gesamtlaenge 10.5.', f'Langlochmitten X=+/-{xc}, Y=+/-10.\nUrsprung: Plattenmitte unten.', 'Mittig M6 x 1 DURCH;\nKernloch D5 durch.\nSchraubeneingriff max. 5.', 'Ein-Stativ-Anschluss: Verdrehung /\nKippmoment unter Kabellast pruefen.\nBei Bedarf Zweipunktstuetze neu auslegen.', 'Modul-Lochbild ist NICHT bestaetigt.\nKein universeller Anschluss zugesichert.', 'h = 8 + Modul-Achshoehe +\nZwischenlagen / Zusatzstufen.\nPassende Stativlaenge neu berechnen.', 'Kein thermisch ausgelegter Ofenhalter.' if code=='H04' else 'Keine integrierte XY/Z/Kipp-Verstellung;\nFuenfachsmodul bleibt separates Kaufteil.'])
 end(code+'_Zeichnung')

begin('07','Montageprinzip und Baugruppenabgrenzung',8)
rect(65,75,50,12);rect(84,87,12,41);rect(68,128,44,44);circle(90,150,12.8);circle(90,150,11)
line(40,150,150,150,True);dv(35,75,150,'75');txt(145,79,'H01',4);txt(145,108,'H02',4);txt(145,148,'H03A + H03B',4)
txt(45,206,'Vorderansicht des Montageprinzips (1:1)',4,True)
txt(24,225,'75 +/-0.15 mm: arithmetische Hoehenkette bei je +/-0.05.',3.5)
txt(24,195,'Klemmversatz, Glaszentrierung und Tischform noch nicht enthalten.',3)
notes(['MNT-03: H03 fuer O04/L1A/L1B\nnur bei passenden Glasdaten.', 'MNT-04: H03 fuer vier Filter\nnur nach Dicke/Apertur/Freigabe.', 'MNT-01: kinematische Spiegelhalter\nweiter separat; kein starrer Ersatz.', 'MNT-02: PBS-Modul / Klemmung OPEN.\nAlle benoetigten Ports freihalten.', 'Wellenplatten: Rotations-/Motorhalter\nweiter separat. H03 ist dafuer\nkeine funktionale Loesung.', 'OVEN-01: H04 nur Anschlusskonzept;\nKristallklemmung/TEC/Sensor OPEN.', 'COUP-MNT: H05 nur Anschlusskonzept.\nZ-STAGE: O04-Bauraum weiterhin HOLD.'])
end('07_Montage')

# Conservative base-plate interference in the pump corner, assuming base centred on optic.
layout=json.loads((P/'Layout_Quelle.json').read_text());coords={x['id']:x for x in layout['components']}
gap=coords['DM']['y_mm']-coords['O04']['y_mm']
collision={'origin':'DESIGN_ENVELOPE_SCREEN','assumptions':'H01 centred under both optical axes, axes aligned to global X/Y; no offset posts; full +/-10 mm lens motion','O04_DM_nominal_distance_mm':gap,'H01_along_Y_mm':35,'nominal_overlap_mm':35-gap,'worst_case_overlap_mm':45-gap,'status':'FAIL_FOR_THIS_MOUNTING_SCENARIO','global_collision_check':'OPEN','actual_hardware':'NOT_RUN'}
(P/'Kollisionspruefung.json').write_text(json.dumps(collision,indent=2)+'\n')
begin('08','Einbaupruefung - Engstelle O04 / DM',9)
rect(72,117,50,35);rect(72,117+gap,50,35);line(97,105,97,202,True)
txt(132,130,'O04-Sockel',3.5);txt(132,170,'DM-Sockel: nur Szenario',3.5)
dv(60,134.5,134.5+gap,f'{gap:.3f}')
txt(24,230,f'Sockel ueberlappen im Nennstand um {35-gap:.3f} mm.',4,True)
txt(24,219,f'Bei +10 mm Linsenhub: rechnerisch {45-gap:.3f} mm Ueberlapp.',3.5)
txt(24,204,'Draufsicht 1:1; optische Zentren als Sockelmitten angenommen.',3)
notes(['Diese Anordnung ist NICHT einbaubar.', 'Abhilfe entwerfen: seitlich versetzte\nSockel/Stative oder kompakte\ngemeinsame Traegerbaugruppe.', 'Kein automatisches Verschieben\nder optischen Sollkoordinaten: erst\nABCD-/Fokusrechnung aktualisieren.', 'Die Pruefung betrifft nur H01 bei\nO04/DM unter den genannten Annahmen.\nKomplettes 3D-CAD, Verkabelung,\nSchraubenzugaenge und Justierhuellen\nsind weiterhin OPEN.', 'Quelle: gaussian-layout-v0.1\nkoordinaten.csv / eingaben.json\nCommit eb6022d19179e32e1e652502\ncdb5556911a4483e.', 'Fertigungsfreigabe aller Teile: HOLD.\nGlas-/Modulmasse und Anschluss-CAD\nsind als naechstes erforderlich.'])
end('08_Kollision')
C.save()
(P/'Bauteile.json').write_text(json.dumps(parts,indent=2,ensure_ascii=False)+'\n')
(P/'Validierung.json').write_text(json.dumps({'cad':validations,'nominal_height_mm':12+41+22,'drawing_scale':'1:1 A3 100%','pdf_visual_review':'PENDING','hardware_status':'NOT_RUN','manufacturing_release':'HOLD'},indent=2)+'\n')
for f in P.glob('*.dxf'):
 d=ezdxf.readfile(f);assert not d.audit().has_errors;assert d.units==4
print('Created six STEP solids, nine DXF drawing sheets, nine-page PDF; CAD roundtrip PASS.')
