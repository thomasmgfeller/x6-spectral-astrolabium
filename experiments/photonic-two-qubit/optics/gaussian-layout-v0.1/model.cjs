"use strict";
// Original X6 implementation. Apache-2.0. See ENTWURF.md for physical scope.
function axis(p,axis,direction,overrides={}) {
 const o={...p,...overrides}; const a=o.axes[axis];
 if(!a||![o.lambda_nm,a.diameter_mm,a.M2,a.curvature_per_mm,o.f_mm,o.lens_shift_mm,o.common_mm,o.leg_mm,o.crystal_shift_mm,o.pbs_mm,o.n_pbs,o.crystal_length_mm,o.n_crystal,o.hwp_mm,o.n_hwp].every(v=>typeof v==="number"&&Number.isFinite(v)))throw Error("Missing or nonnumeric physical input");
 const lambda=o.lambda_nm*1e-6,w=a.diameter_mm/2,M=a.M2,k=a.curvature_per_mm;
 if(!(lambda>0&&w>0&&M>=1&&o.f_mm>0&&o.n_crystal>=1&&o.n_pbs>=1&&o.n_hwp>=1&&o.crystal_length_mm>0&&o.leg_mm>0&&o.common_mm-o.lens_shift_mm>0&&o.pbs_mm>=0&&o.hwp_mm>=0))throw Error("Invalid physical input");
 const b=M*lambda/(Math.PI*w*w),den=k*k+b*b;
 let re=k/den,im=b/den;
 re+=o.lens_shift_mm;
 const lensDen=(1-re/o.f_mm)**2+(im/o.f_mm)**2;
 const postRe=(re-(re*re+im*im)/o.f_mm)/lensDen,postIm=im/lensDen;
 const geom=o.common_mm-o.lens_shift_mm+o.leg_mm*(1+Math.SQRT2/2)+(direction==="CCW"?o.crystal_shift_mm:-o.crystal_shift_mm);
 const bp=geom-o.pbs_mm*(1-1/o.n_pbs)-o.crystal_length_mm/2*(1-1/o.n_crystal)-(direction==="CW"?o.hwp_mm*(1-1/o.n_hwp):0);
 const Qre=postRe+bp,delta=-o.n_crystal*Qre;
 const w0=Math.sqrt(M*lambda*postIm/Math.PI);
 const wCenter=w0*Math.sqrt(1+(Qre/postIm)**2);
 const ends=[Qre-o.crystal_length_mm/(2*o.n_crystal),Qre+o.crystal_length_mm/(2*o.n_crystal)];
 return {w0_um:w0*1000,w_center_um:wCenter*1000,waist_shift_local_mm:delta,zR_crystal_mm:o.n_crystal*postIm,zR_air_mm:postIm,air_focus_mm:-postRe,reduced_distance_mm:bp,Q_re_mm:Qre,Q_im_mm:postIm,face_radii_um:ends.map(x=>w0*1000*Math.sqrt(1+(x/postIm)**2))};
}
function evaluate(p){return ["CW","CCW"].flatMap(d=>["u","v"].map(a=>({direction:d,axis:a,...axis(p,a,d)})));}
function tolerances(p){const mods=[
["D_u −5%",{axes:{...p.axes,u:{...p.axes.u,diameter_mm:p.axes.u.diameter_mm*.95}}}],
["D_u +5%",{axes:{...p.axes,u:{...p.axes.u,diameter_mm:p.axes.u.diameter_mm*1.05}}}],
["M²_u −0.1",{axes:{...p.axes,u:{...p.axes.u,M2:p.axes.u.M2-.1}}}],
["M²_u +0.1",{axes:{...p.axes,u:{...p.axes.u,M2:p.axes.u.M2+.1}}}],
["f −1%",{f_mm:p.f_mm*.99}],["f +1%",{f_mm:p.f_mm*1.01}],
["Linse −1 mm",{lens_shift_mm:p.lens_shift_mm-1}],["Linse +1 mm",{lens_shift_mm:p.lens_shift_mm+1}],
["Krümmung −0.001/mm",{axes:{...p.axes,u:{...p.axes.u,curvature_per_mm:p.axes.u.curvature_per_mm-.001}}}],
["Krümmung +0.001/mm",{axes:{...p.axes,u:{...p.axes.u,curvature_per_mm:p.axes.u.curvature_per_mm+.001}}}],
["n_K −0.05",{n_crystal:p.n_crystal-.05}],["n_K +0.05",{n_crystal:p.n_crystal+.05}]
];return mods.map(([name,o])=>({name,...axis(p,"u","CW",o)}));}
function physicalWaistSeparation(p,a="u"){const cw=axis(p,a,"CW"),ccw=axis(p,a,"CCW");return Math.abs(cw.waist_shift_local_mm+ccw.waist_shift_local_mm);}
function cornerBudget(p){const values=[["D",[-.05,.05]],["M",[-.1,.1]],["f",[-.01,.01]],["lens",[-1,1]],["k",[-.0002,.0002]]];let rows=[];for(let i=0;i<32;i++){const v=values.map((x,j)=>x[1][(i>>j)&1]);const q={...p,axes:{...p.axes,u:{...p.axes.u,diameter_mm:p.axes.u.diameter_mm*(1+v[0]),M2:p.axes.u.M2+v[1],curvature_per_mm:p.axes.u.curvature_per_mm+v[4]}},f_mm:p.f_mm*(1+v[2]),lens_shift_mm:p.lens_shift_mm+v[3]};rows.push({corner:i,...axis(q,"u","CW")});}return rows;}
function radiusAtReduced(re,im,M2,lambda_nm){if(!(im>0))throw Error("Invalid Q");return 1000*Math.sqrt(M2*lambda_nm*1e-6/Math.PI*(re*re+im*im)/im);}
function matmul(a,b){return [a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3]];}
function qtransform(Q,M){const [x,y]=Q,[a,b,c,d]=M,den=(c*x+d)**2+(c*y)**2;return [((a*x+b)*(c*x+d)+a*c*y*y)/den,y*(a*d-b*c)/den];}
function relayResult(r){const mag=r.f2_mm/r.f1_mm,wi=r.collection_radius_um*mag,wf=r.fiber_mfd_um/2;return {magnification:mag,image_radius_um:wi,mode_size_only_efficiency:(2*wi*wf/(wi*wi+wf*wf))**2,zR_fiber_mm:Math.PI*(wf*.001)**2/.000810,collimated_radius_mm:.000810*r.f1_mm/(Math.PI*r.collection_radius_um*.001)};}
function measuredReady(v){return v&&v.origin==="MEASURED"&&Array.isArray(v.evidence_refs)&&v.evidence_refs.length>0&&v.uncertainty_covariance!==null;}

module.exports={axis,evaluate,tolerances,cornerBudget,physicalWaistSeparation,matmul,qtransform,radiusAtReduced,relayResult,measuredReady};
