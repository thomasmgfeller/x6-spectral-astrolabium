"""Polarization state and scalar erasure are separate physical operations."""
import math
import numpy as np
from .config import number

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1., -1.]).astype(complex)
SINGLET = np.array([0, 1, -1, 0], complex)/np.sqrt(2)
C_M_PER_S = 299_792_458.0


def rotation(y, z):
    """U=Rz(z) Ry(y); angles are Bloch rotations, not waveplate angles."""
    return ((math.cos(z/2)*I-1j*math.sin(z/2)*Z) @
            (math.cos(y/2)*I-1j*math.sin(y/2)*Y))


def density(visibility, ua, ub, dephase_a=0.0, dephase_b=0.0):
    number(visibility, "visibility", 0, 1)
    for u in (ua,ub):
        u = np.asarray(u)
        if u.shape != (2,2) or not np.isfinite(u).all() or not np.allclose(u.conj().T@u,I,atol=1e-12,rtol=0):
            raise ValueError("Finite unitary 2x2 polarization operators required")
    rho = visibility*np.outer(SINGLET, SINGLET.conj())+(1-visibility)*np.eye(4)/4
    u = np.kron(ua, ub)
    rho = u@rho@u.conj().T
    for p, op in ((dephase_a, np.kron(Z, I)), (dephase_b, np.kron(I, Z))):
        number(p, "dephasing", 0, 1)
        rho = (1-p/2)*rho+(p/2)*(op@rho@op)
    validate_density(rho)
    return rho


def validate_density(rho):
    rho = np.asarray(rho)
    if (rho.shape != (4, 4) or not np.isfinite(rho).all() or
        np.max(np.abs(rho-rho.conj().T)) > 1e-10 or
        abs(np.trace(rho)-1) > 1e-10 or np.linalg.eigvalsh(rho).min() < -1e-10):
        raise ValueError("Invalid two-qubit density matrix; no state repair")


def negativity(rho):
    validate_density(rho)
    # Transpose B's indices in rho[a,b,c,d].
    pt = rho.reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4)
    return float(-np.minimum(np.linalg.eigvalsh(pt), 0).sum())


def probabilities(rho, angle_a_deg, angle_b_deg):
    validate_density(rho)
    projectors = []
    for angle in (angle_a_deg, angle_b_deg):
        theta = math.radians(2*angle)
        op = math.sin(theta)*X+math.cos(theta)*Z
        projectors.append(((I+op)/2, (I-op)/2))
    p = np.array([np.trace(rho@np.kron(a,b)).real
                  for a in projectors[0] for b in projectors[1]])
    if p.min() < -1e-12 or abs(p.sum()-1) > 1e-10:
        raise ValueError("Invalid Born probabilities")
    # Remove only floating point roundoff after explicit domain checks.
    p = np.maximum(p, 0)
    return p/p.sum()  # order ++,+-,-+,--


def efficiency(arm, environment):
    loss_db = (arm.attenuation_db_per_km*arm.length_km +
               arm.insertion_loss_db + arm.loss_db_per_environment*environment)
    if np.any(np.asarray(loss_db) < 0):
        raise ValueError("Realized loss would imply gain; revise the environmental model")
    return arm.coupling*arm.detector_efficiency*10.0**(-np.asarray(loss_db)/10)


def delay(arm, environment):
    value = (arm.group_index*arm.length_km*1000/C_M_PER_S +
             arm.electronics_delay_s + arm.delay_s_per_environment*environment)
    if np.any(np.asarray(value) < 0):
        raise ValueError("Negative realized propagation/electronics delay")
    return value


def stationary_ou(rng, n, dt, tau, sigma):
    """Exact discrete transition for a stationary scalar OU process."""
    out = np.zeros(n)
    out[0] = rng.normal(0, sigma)
    a = math.exp(-dt/tau)
    sd = sigma*math.sqrt(-math.expm1(-2*dt/tau))
    for k in range(1, n):
        out[k] = a*out[k-1]+rng.normal(0, sd)
    return out


def fixed_bin_retention(width_s, delta_s, sigma_s):
    """E[(1-|D|/W)+], D~N(delta,sigma²), uniform bin phase.

    Isolated pairs, no dead time, quantization or edge effects. This differs
    from the acceptance of a sliding +/-W/2 coincidence gate.
    """
    number(width_s, "width_s", 1e-18)
    number(delta_s, "delta_s")
    number(sigma_s, "sigma_s", 0)
    w, mu, s = width_s, abs(delta_s), sigma_s
    if s == 0:
        return max(0., 1-mu/w)
    if s > 10*w:
        # Avoid subtraction of nearly equal normal CDFs for very narrow bins.
        x, weights = np.polynomial.legendre.leggauss(24)
        z = (x+1)/2
        def integrand(v):
            return (1-np.abs(v))*np.exp(-.5*((w*v-mu)/s)**2)
        return float(w/s/math.sqrt(2*math.pi)*np.sum(weights*(integrand(z)+integrand(-z)))/2)
    phi = lambda x: math.exp(-x*x/2)/math.sqrt(2*math.pi)
    cdf = lambda x: .5*math.erfc(-x/math.sqrt(2))
    a, b, c = (-w-mu)/s, -mu/s, (w-mu)/s
    left = cdf(b)-cdf(a)
    right = cdf(c)-cdf(b)
    mleft = mu*left+s*(phi(a)-phi(b))
    mright = mu*right+s*(phi(b)-phi(c))
    value = left+right+(mleft-mright)/w
    if not -1e-12 <= value <= 1+1e-12:
        raise ArithmeticError("Unstable retention integral")
    return min(1., max(0., value))
