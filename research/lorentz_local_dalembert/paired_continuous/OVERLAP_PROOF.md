# A count difference retains the shared-cloud correlation

SPDX-License-Identifier: Apache-2.0

This is a separate follow-up to the frozen continuous screen. It acts only on
its terminal HOLD cells, leaves the original outputs unchanged, and uses no
additional subdivisions or new geometries. The method was chosen after the
initial screen showed persistent unresolved cells on the negative h side.

## 1. The observable and its variance

Take A=I(5,1), B=I(15,1), and the observed integer difference D=N(A)-N(B).
The common points cancel exactly: D=N(A\B)-N(B\A). The two exclusive regions
are disjoint, so Poisson independent increments give

    E[D]=mu_A-mu_B,
    Var(D)=mu_A+mu_B-2*mu_(A intersect B).

The original overlapping interval counts are NOT independent. Replacing their
variance by mu_A+mu_B throws away useful information. Conversely, underestimating
the variance would invalidate the test; we therefore need a rigorous LOWER
bound on the intersection intensity, including all geometric uncertainty.

## 2. A geometric subset of the intersection

Use the same boosted coordinates as the paired ray. Tip 15 is always later than
tip 5 by the constant dt>0. Let r(h) be their spatial distance and define

    delta(h)=max(0,r(h)-dt),
    v(h)=(t_15+delta(h), spatial_position_15(h)).

Then v is in the causal future of both tips (null contact is allowed). Whenever
v precedes tip 1, transitivity gives I(v,1) subset A intersect B, up to null
boundaries of zero Poisson intensity. The virtual tip is a proof device, not a
new observation or new landmark.

Since r^2=dt^2-q_(5,15), the exact cell range of q gives a directed upper bound
delta_U. Put T=t_1-t_15>0, also constant. If delta_U<T, then the expression
-2*T*delta+delta^2 is decreasing on the entire delay range. Therefore

    q_(v,1) >= q_(15,1),lower -2*T*delta_U+delta_U^2 = q_sub,lower.

If this lower bound is positive, the known interval-volume formula yields a
lower intensity C*q_sub,lower^(3/2). If these sufficient positivity conditions
fail, retain lower intensity zero. Combining upper interval means and this
lower intersection bound gives a valid uniform upper variance V on the cell.
There is no numerical integration or unbounded residual volume discarded.

## 3. A distribution-free event bound from the Poisson moments

For a centered variable Z with variance sigma^2, a>0 and t>=0, Markov's
inequality applied to (Z+t)^2 bounds P(Z>=a) by
(sigma^2+t^2)/(a+t)^2. Taking t=sigma^2/a gives the one-sided Cantelli bound
sigma^2/(sigma^2+a^2); the same applies to -Z. It is increasing in sigma^2.

Suppose the lower-mean law has mean at most m_L and variance at most V_L,
and the higher-mean law has mean at least m_H and variance at most V_H.
For the integer event E={D<=k}, provided k+1>m_L and k<m_H,

    P_low(E) >= 1 - V_L/(V_L+(k+1-m_L)^2),
    P_high(E) <= V_H/(V_H+(m_H-k)^2).

The first inequality uses the integer complement D>=k+1. Their difference,
clipped below at zero, is a full-law TV lower bound by projection. A threshold
k is chosen deterministically from the midpoint of the two mean-enclosure
midpoints. Its optimality is neither required nor claimed.

All mean enclosures, virtual-tip delays, overlap lower bounds, variances and
Cantelli fractions are computed with exact rationals or directed square-root
and pi bounds. If the resulting lower bound does not exceed 1/4, the cell stays
HOLD. The argument provides no upper bound on TV and no closeness certificate.

## 4. Scope of a successful overlay

The inherited terminal cells already cover the complete interval. Replacing
HOLD on a cell by a valid whole-cell difference-event exclusion preserves that
coverage. Only when no terminal HOLD remains is the entire declared paired line
excluded. This does not extend the result to the other 58 paired rays or to
arbitrary geometries. The existing conditioning, order and target definitions
are not changed.
