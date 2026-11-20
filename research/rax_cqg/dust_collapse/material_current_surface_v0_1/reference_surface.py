"""Spherical Einstein-dust and same-current geometric countercontrols in geometric units."""
from fractions import Fraction as F
from math import isqrt, sqrt
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/"inputs"/"early_areal_radius_two_masses_v0_1"))
from area_mesh import PI, verify_pi
MASSES = (F(1,4), F(4))
X = F(1,2)
TEND2 = F(125,9)
R0 = F(10)

def rational_sqrt(value):
    a,b = isqrt(value.numerator),isqrt(value.denominator)
    assert a*a==value.numerator and b*b==value.denominator
    return F(a,b)

def cube_bounds(cube):
    scale = 10**16
    n = cube.numerator*scale**3//cube.denominator
    lo,hi = 0,1
    while hi**3<=n: hi*=2
    while hi-lo>1:
        mid = (hi+lo)//2
        if mid**3<=n: lo=mid
        else: hi=mid
    out = (F(lo,scale),F(hi,scale))
    assert out[0]**3<=cube<=out[1]**3
    return out

def enclose(value):
    lo,hi = value
    return {"bounds_exact":list(map(str,(lo,hi))),"approx":float((lo+hi)/2)}

def shell_solution(m,total_initial_radius,x):
    # (d(R/R_initial)^(3/2)/dx)^2 is constant for collapsing marginally bound dust.
    speed = rational_sqrt(F(9,4)*TEND2*2*m/total_initial_radius**3)
    z = 1-speed*x
    assert z>0
    return total_initial_radius**3*z*z

def rk_surface(m,n):
    # Independent untransformed first-order evolution in physical proper time.
    dt=float(X)*sqrt(float(TEND2))/n
    r=float(R0)
    def velocity(s): return -sqrt(2*float(m)/s)
    for _ in range(n):
        v1=velocity(r)
        v2=velocity(r+dt*v1/2)
        v3=velocity(r+dt*v2/2)
        v4=velocity(r+dt*v3)
        r += dt*(v1+2*v2+2*v3+v4)/6
    return r

def run():
    verify_pi()
    out, distortions, bases = {},{},{}
    for mass in MASSES:
        field = []
        for n in (8,16,32):
            # Each angular material cone covers a fraction 1/128 of the full solid angle.
            angular = 128
            transfers = [mass*(F(i,n)**3-F(i-1,n)**3)/angular for i in range(1,n+1)]
            m_surface = sum(transfers)*angular
            assert m_surface==mass
            sampled_states = []
            for x in (F(0),F(1,4),X):
                enclosed = F(0)
                surface_cube = shell_solution(m_surface,R0,x)
                last_cube = 0
                for i, packet in enumerate(transfers,1):
                    enclosed += packet*angular
                    u=F(i,n)
                    cube = shell_solution(enclosed,R0*u,x)
                    assert cube==surface_cube*u**3 and cube>last_cube
                    # Positive proper dust in every radial zone; vacuum outside u=1.
                    assert enclosed==mass*u**3
                    last_cube = cube
                assert enclosed==mass and sum(transfers[:n//2])*angular==mass/8
                # Propagate a representative comoving tracer for each mass bin.
                # All angular sectors have the same radial track by spherical symmetry.
                selected = []
                for i in range(n):
                    u_mid = F(2*i+1,2*n)
                    tracer_cube = shell_solution(mass*u_mid**3,R0*u_mid,x)
                    selected.append((tracer_cube<=surface_cube, tracer_cube<=9**3))
                sampled_states.append(selected)
            def crossings(column):
                out_mass = in_mass = F(0)
                for earlier,later in zip(sampled_states,sampled_states[1:]):
                    for i,(a,b) in enumerate(zip(earlier,later)):
                        if a[column] and not b[column]: out_mass += transfers[i]*angular
                        if not a[column] and b[column]: in_mass += transfers[i]*angular
                return out_mass,in_mass
            outgoing,incoming = crossings(0)
            fixed_out,fixed_in = crossings(1)
            assert outgoing==incoming==fixed_out==0 and fixed_in>0
            field.append({"shells":n,"angular_material_sectors":angular,"Q0":str(m_surface),
                          "Q_star":str(enclosed),"material_crossing_out":str(outgoing),"material_crossing_in":str(incoming),
                          "fixed_R9_tracer_crossing_in":str(fixed_in),"fixed_R9_tracer_crossing_out":str(fixed_out)})
        r = cube_bounds(surface_cube)
        # The induced metric on the transported boundary is R^2 times the unit sphere metric.
        # In mu=cos(theta), phi coordinates sqrt(det h)=R^2 (away from chart poles).
        dsq = (r[0]**2,r[1]**2)
        area = (sum(4*PI[0]*dsq[0]/angular for _ in range(angular)),
                sum(4*PI[1]*dsq[1]/angular for _ in range(angular)))
        for steps in (32,64,128):
            independently_evolved = rk_surface(m_surface,steps)
            assert abs(independently_evolved-float(sum(r)/2))<1e-8
        out[str(mass)]={"R_cubed_exact":str(surface_cube),"radius":enclose(r),"area":enclose(area),
                        "initial_mass_and_comoving_surface":field,"rk4_checks_steps":[32,64,128]}
        bases[mass] = r
        h=(8*mass-17)/15
        assert abs(h)==1
        distortion = {}
        for k in (0,1):
            d=1+k*h*X**3
            deformation = (r[0]*d,r[1]*d)
            distortion[str(k)]=enclose(deformation)
            for x in [F(0),F(1,4),X]:
                for u in (F(0),F(1,2),F(1)):
                    s=1+k*h*x**3*u*u
                    assert s>0 and 1+3*k*h*x**3*u*u>0
                    assert (1/s**2)*(u*s)**2==u*u
        distortions[str(mass)] = distortion
    high,low=MASSES[1],MASSES[0]
    delta = (bases[high][0]-bases[low][1],bases[high][1]-bases[low][0])
    delta_area = tuple(F(out[str(high)]["area"]["bounds_exact"][i])-F(out[str(low)]["area"]["bounds_exact"][1-i]) for i in (0,1))
    controls = {}
    for k in (0,1):
        h = list(map(F,distortions["4"][str(k)]["bounds_exact"]))
        l = list(map(F,distortions["1/4"][str(k)]["bounds_exact"]))
        diff=(h[0]-l[1],h[1]-l[0])
        assert diff[1]<0 if k==0 else diff[0]>0
        controls[str(k)] = enclose(diff)
    return {"reference":{"masses":out,"Tstar":"5*sqrt(5)/6","radius_contrast_heavy_minus_light":enclose(delta),
                         "area_contrast_heavy_minus_light":enclose(delta_area)},
            "same_current_metric_controls":{"radii":distortions,"radius_contrast":controls,
                        "qualification":"Auxiliary metrics preserve dust current, all comoving proper volumes and proper time. Only k=0 is asserted to satisfy the specified Einstein-dust evolution."}}
