"use strict";
const {axis}=require("./model.cjs");
function geometry(p,base){const c=JSON.parse(JSON.stringify(base)),get=id=>c.find(x=>x.id===id),b=get("PBS0");get("O04").y_mm=b.y_mm-(p.common_mm-40)+p.lens_shift_mm;get("M1").x_mm=b.x_mm+p.leg_mm;get("M2").y_mm=b.y_mm+p.leg_mm;get("HD").y_mm=b.y_mm+p.leg_mm/2;get("K").x_mm=b.x_mm+p.leg_mm/2-p.crystal_shift_mm/Math.SQRT2;get("K").y_mm=b.y_mm+p.leg_mm/2+p.crystal_shift_mm/Math.SQRT2;return c;}
function buildSVG(p,base){
const c=geometry(p,base),g=id=>c.find(x=>x.id===id),X=x=>40+x,Y=y=>740-y,pt=id=>X(g(id).x_mm)+","+Y(g(id).y_mm);
const esc=s=>String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
let s='<svg xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" viewBox="0 0 1188 840" role="img" aria-labelledby="title desc"><title id="title">X6 Sagnac Layout v0.1 - A2 1:2</title><desc id="desc">800 x 600 mm board, beam height 75 mm, source and four fibers. Design scenario only, not a machining drawing.</desc><defs><marker id="arrowP" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10Z" fill="#6d28d9"/></marker><marker id="arrowR" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10Z" fill="#ba3418"/></marker></defs><rect width="1188" height="840" fill="white"/><g font-family="Arial, sans-serif" fill="#172033"><text x="40" y="45" font-size="26" font-weight="bold">X6 | Gaussian-Worksheet + Sagnac-Layout</text><text x="40" y="74" font-size="15">Entwurf v0.1 | 05.11.2026 | A2 quer, Massstab 1:2 bei 100 % Druck | NOT_RUN / HOLD</text><text x="40" y="102" font-size="13">Strahlzentren massstaeblich. Halter-Konturen sind Platzreservierungen; keine Bohr- oder Montagefreigabe.</text><rect x="40" y="140" width="800" height="600" fill="#fafbfc" stroke="#536273" stroke-width="1"/>';
for(let x=0;x<=800;x+=50)s+='<path d="M'+X(x)+' 140V740" stroke="#e1e5ea" stroke-width=".6"/><text x="'+X(x)+'" y="760" text-anchor="middle" font-size="10">'+x+'</text>';
for(let y=0;y<=600;y+=50)s+='<path d="M40 '+Y(y)+'H840" stroke="#e1e5ea" stroke-width=".6"/><text x="32" y="'+(Y(y)+3)+'" text-anchor="end" font-size="10">'+y+'</text>';
s+='<text x="390" y="786" font-size="13">X / mm</text><text x="10" y="410" font-size="13" transform="rotate(-90 10 410)">Y / mm</text>';
function line(ids,color,arrow){s+='<polyline points="'+ids.map(pt).join(" ")+'" stroke="'+color+'" stroke-width="2" fill="none"'+(arrow?' marker-end="url(#'+arrow+')"':'')+'/>';}
line(["P0","MP1","MP2","O04","DM","PBS0"],"#6d28d9","arrowP");line(["PBS0","M1","K","M2","PBS0"],"#6d28d9",null);
line(["PBS0","DM","L1A","FA","QA","HA","PA","L2A+","FC_A+"],"#ba3418","arrowR");
line(["PA","L2A-","FC_A-"],"#ba3418","arrowR");line(["PBS0","DB","L1B","FB","QB","HB","PB","L2B+","FC_B+"],"#ba3418","arrowR");line(["PB","L2B-","FC_B-"],"#ba3418","arrowR");
line(["DB","BD1"],"#6d28d9","arrowP");line(["ISO","BD0"],"#6d28d9","arrowP");
for(const o of c){
 const x=X(o.x_mm),y=Y(o.y_mm),k=o.kind;
 if(k!=="fiber"){const size=k==="crystal"?40:k==="source"?36:26;s+='<rect x="'+(x-size/2)+'" y="'+(y-size/2)+'" width="'+size+'" height="'+size+'" fill="none" stroke="#9aa5b1" stroke-width=".8" stroke-dasharray="3 3"/>';}
 if(k==="pbs"&&o.id==="PB")s+='<rect x="'+(x-5)+'" y="'+(y-5)+'" width="10" height="10" fill="#dcebf8" stroke="#243649"/><path d="M'+(x-5)+' '+(y-5)+'L'+(x+5)+' '+(y+5)+'" stroke="#243649"/>';
 else if(k==="pbs")s+='<rect x="'+(x-5)+'" y="'+(y-5)+'" width="10" height="10" fill="#dcebf8" stroke="#243649"/><path d="M'+(x-5)+' '+(y+5)+'L'+(x+5)+' '+(y-5)+'" stroke="#243649"/>';
 else if(k==="crystal")s+='<rect x="'+(x-p.crystal_length_mm/2)+'" y="'+(y-1)+'" width="'+p.crystal_length_mm+'" height="2" transform="rotate(45 '+x+' '+y+')" fill="#1f8b7a" stroke="#163f3a"/>';
 else if(k==="mirror"||k==="dichroic"){const t=-(o.surface_normal_azimuth_deg+90)*Math.PI/180,dx=8*Math.cos(t),dy=8*Math.sin(t);s+='<path d="M'+(x-dx)+' '+(y-dy)+'L'+(x+dx)+' '+(y+dy)+'" stroke="#244253" stroke-width="2.5"/>';}
 else if(k==="dump")s+='<circle cx="'+x+'" cy="'+y+'" r="7" fill="#273542"/>';
 else if(k==="fiber")s+='<circle cx="'+x+'" cy="'+y+'" r="2.5" fill="#ba3418"/>';
 else if(k==="lens"||k==="coupler")s+='<ellipse cx="'+x+'" cy="'+y+'" rx="'+(o.nominal_direction_deg===180?2:7)+'" ry="'+(o.nominal_direction_deg===180?7:2)+'" fill="#d6edf0" stroke="#17525e"/>';
 else s+='<circle cx="'+x+'" cy="'+y+'" r="5" fill="#fff" stroke="#33485c"/>';
 const dx=k==="fiber"?-10:16,anchor=k==="fiber"?"end":"start";
 const dy=k==="fiber"?18:-8;
 if(o.id==="PBS0"){s+='<text x="'+(x+30)+'" y="'+(y+60)+'" font-size="10">PBS0</text>';continue;}
 s+='<text x="'+(x+dx)+'" y="'+(y+dy)+'" text-anchor="'+anchor+'" font-size="10">'+esc(o.id)+'</text>';
}
s+='<text x="520" y="322" text-anchor="end" font-size="10">P1=W</text><text x="560" y="323" font-size="10">P2=E</text><text x="532" y="305" text-anchor="end" font-size="10">P3=N</text><text x="532" y="352" text-anchor="end" font-size="10">P4=S</text>';
s+='<path d="M570 330H605" stroke="#6d28d9" stroke-width="1.5" marker-end="url(#arrowP)"/><text x="580" y="348" font-size="10">CCW</text><path d="M540 302V277" stroke="#6d28d9" stroke-width="1.5" marker-end="url(#arrowP)"/><text x="550" y="293" font-size="10">CW</text>';
s+='<rect x="500" y="190" width="180" height="180" fill="none" stroke="#168071" stroke-dasharray="5 4"/><text x="500" y="185" font-size="11">Quellenbereich / Zugang von oben</text>';
s+='<path d="M60 705H160M60 700V710M160 700V710" stroke="#172033" stroke-width="2"/><text x="110" y="695" text-anchor="middle" font-size="12">100 mm real = 50 mm Druck</text>';
const kr=g("K");for(const dir of ["CW","CCW"]){const r=axis(p,"u",dir),d=(dir==="CCW"?1:-1)*r.waist_shift_local_mm;if(Math.abs(r.waist_shift_local_mm)<=p.crystal_length_mm/2){s+='<circle cx="'+X(kr.x_mm-d/Math.SQRT2)+'" cy="'+Y(kr.y_mm+d/Math.SQRT2)+'" r="2" fill="none" stroke="#004d40" stroke-width="1.2"/>';}}s+='<text x="'+(X(kr.x_mm)+18)+'" y="'+(Y(kr.y_mm)+16)+'" font-size="10">K / Fokus u*</text>';let yy=155;const txt=(v,size=12)=>{s+='<text x="875" y="'+yy+'" font-size="'+size+'">'+esc(v)+'</text>';yy+=size+9;};
txt("BEZUG / RICHTUNGEN",15);txt("Draufsicht: Blick von +Z auf Tisch.");txt("+X rechts, +Y oben; Z = 75 mm.");txt("u = Z x k; v = Z (vertikal).");txt("H = u, V = v; lokale Achsen.");yy+=10;
txt("405 nm Pumpweg");txt("Lila Linie; Ruecklauf ueber ISO/BD0.");txt("810 nm Sammelwege");txt("Rote Linie; A+/A-/B+/B- zu Fasern.");yy+=10;
txt("NOMINALE EINSTELLUNG",15);txt("O04: f = "+p.f_mm.toFixed(1)+" mm (Szenario).");txt("D u/v = "+p.axes.u.diameter_mm.toFixed(3)+" / "+p.axes.v.diameter_mm.toFixed(3)+" mm.");txt("M2 u/v = "+p.axes.u.M2.toFixed(2)+" / "+p.axes.v.M2.toFixed(2)+".");txt("K: "+p.crystal_length_mm+" mm, n_p = "+p.n_crystal+".");txt("zR(K,u) = "+axis(p,"u","CW").zR_crystal_mm.toFixed(2)+" mm.");txt("HD: 45 deg, Halbwell bei 405/810.");txt("M1 / M2: AOI jeweils 22.5 deg.");txt("DM / DB: AOI 45 deg.");txt("PBS: aussen 0, intern 45 deg.");yy+=10;
txt("OFFENE FREIGABEN",15);txt("Reale Pumpe / Kaustik / Kovarianz");txt("KTP-Indizes, Schnitt, Polung, Ofen");txt("PBS-/HWP-Phasen und freie Apertur");txt("Dichroika: Plattenversatz / ABCD");txt("810-nm-Relais und Filterdicken");txt("Halter-CAD, Justage / Kollisionen");yy+=10;
txt("Entwurf = keine Messbestaetigung.");txt("* Fokusmarker nur innerhalb K.");txt("Radien / Strahldicken nicht skaliert.");txt("Detektoren extern via vier Fasern.");
s+='<text x="40" y="815" font-size="12">Optische Haupt-/Bezugsebenen, nicht Gehaeusemitten. Druckskalierung mit 100-mm-Balken pruefen. O04 und BOM: HOLD.</text></g></svg>';return s;}

module.exports={geometry,buildSVG};
