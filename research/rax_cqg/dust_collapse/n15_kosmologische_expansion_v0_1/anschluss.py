"""Exact marginal dust ball and two Einstein–Straus exteriors (G=c=1)."""
from fractions import Fraction as F
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
def require(x, message):
    if not x:
        raise ArithmeticError(message)

def run(out):
    ref = json.loads((ROOT/'quellen/korrespondenz.json').read_text())['reference']
    M, R0 = F(1), F(ref['R0'])
    require(ref['G']==ref['c']==1 and str(M) in ref['masses'] and R0==10 and
            ref['T_end']=='5*sqrt(5)/3' and 'q=sqrt(M)/4' in ref['analytic'],'Referenz')
    local=[]
    for x in map(F,ref['time_fractions']):
        R3=R0**3*(1-x/4)**2
        # d ln R / d x = -1/[6(1-x/4)] for M=1, T_end²=125/9.
        Hx=-1/(6*(1-x/4))
        require(Hx**2/(F(125,9))==2*M/R3,'lokale marginale Friedmann-Gleichung')
        require(Hx<0 and (2*M)**3<R3<=R0**3,'lokales Fenster')
        local.append(dict(x=x,R_cubed=R3,TE_times_Hlocal=Hx))
    H02=F(1,32000)
    models=[]
    for R,curvature in [(F(40),0),(F(50),-1)]:
        m=2*M/(R**3*H02)
        k=1-m
        epsilon=k*H02*R**2
        # pi*rho0 is rational. Check Misner-Sharp mass and shell equation
        # coefficient by coefficient, for the entire FLRW trajectory a/a0=b.
        pi_rho=3*M/(4*R**3)
        require(F(4,3)*pi_rho*R**3==M and F(8,3)*pi_rho==m*H02,'Masse')
        require(R**2*H02*m==2*M/R and R**2*H02*k==epsilon,'Randbewegung')
        require((curvature==0 and epsilon==0) or (curvature==-1 and epsilon>0),'Krümmung')
        checks=[]
        for b in [F(1),F(100,101),F(9,10)]:
            rb=b*R
            norm=1/b
            H2=H02*(m*norm**3+k*norm**2)
            speed2=rb**2*H2
            f=1-2*M/rb
            require(rb>R0 and f>0,'gemeinsamer Vakuumbereich an der Referenzepoche')
            require(f+speed2==1+epsilon,'Winkelkrümmung')
            Tdot2=(1+epsilon)/f**2
            require(-f*Tdot2+speed2/f==-1,'induzierte Eigenzeit')
            acceleration=-R*H02*m/(2*b**2)
            require(acceleration==-M/rb**2,'radiale Geodäte')
            checks.append(dict(relative_scale=b,matching_radius=rb,radial_speed_squared=speed2))
        models.append(dict(Rb0=R,spatial_curvature_sign=curvature,omega_m=m,omega_k=k,
             pi_rho_background=pi_rho,H0_squared=H02,epsilon=epsilon,
             Eprime_at_zero=1+m/2, E2_at_z_one_percent=m*F(101,100)**3+k*F(101,100)**2,
             V_Vsecond_over_Vprime_squared=F(2,3)-m/6,junction_checks=checks))
    a,b=models
    require(a['Eprime_at_zero']==F(3,2) and b['Eprime_at_zero']==F(157,125),'Steigung')
    require(a['V_Vsecond_over_Vprime_squared']==F(1,2) and
            b['V_Vsecond_over_Vprime_squared']==F(218,375),'Volumendiagnostik')
    # Both exteriors spatially flat in this second control: E is identical,
    # while H0 itself depends on the radius chosen for the exterior matching.
    flat={str(R):2*M/F(R)**3 for R in (40,50)}
    result=dict(local=local,exteriors=models,delta_Eprime=a['Eprime_at_zero']-b['Eprime_at_zero'],
                delta_volume_curvature=b['V_Vsecond_over_Vprime_squared']-a['V_Vsecond_over_Vprime_squared'],
                flat_control_H0_squared=flat)
    (out/'anschluss.json').write_text(json.dumps(result,default=str,indent=2)+'\n')
