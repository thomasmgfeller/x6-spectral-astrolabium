# A finite-sample joint region for the 20 observed chain counts

Scope: flat 3+1 Minkowski space, seven externally fixed labelled events in a
strict timelike chain, five affinely independent anchors, known intensity.
The random background excludes the inserted chain events. No intrinsic
selection, arbitrary-poset or operator claim is made.

## Observable independent counts

Use the v0.2 disjoint atoms Y(i,j), i<j, in I(e0,e6), with e5=p, e6=q.
The observed mask contains all 21 interval counts except N(5,6). Mobius
inversion of the full mask would give

    Y(i,j)=N(i,j)-N(i+1,j)-N(i,j-1)+N(i+1,j-1).

Only Y(4,6) and Y(5,6) require the withheld count. Their sum is observed:

    Z=Y(4,6)+Y(5,6)=N(4,6)-N(4,5).

The other 19 atoms and Z are 20 independent Poisson counts on disjoint sets.
Write their count vector as y and its mean as lambda. The observed interval
vector is n=C y for a square 0/1 matrix C. The code verifies an exact integer
inverse C^-1. This is an invertible change of the existing observations,
not access to the withheld N(p,q) or to latent atom counts.

## Uniform joint concentration

For a Poisson count X of mean lambda, let

    Z(X,lambda)=X log(X/lambda)-X+lambda,

with 0 log 0=0 and the natural degenerate convention at lambda=0. Exponential
Markov applied to E exp(tX)=exp(lambda(exp(t)-1)), and optimized separately
on each side of lambda, gives P(Z>=u)<=min(1,2 exp(-u)). For 0<s<1, integrating
this tail yields

    E exp(sZ) <= 1+s int_0^infinity exp(su) min(1,2exp(-u)) du
               = 2^s/(1-s).

Independence of the 20 observable cells and s=1/2 imply

    P(sum_i Z(y_i,lambda_i)>48) <= 2^30 exp(-24) < 0.05.

The last strict inequality is also checked by a finite rational lower sum
for exp(24). This is a conservative nonasymptotic region, not Wilks' theorem,
a fitted chi-square cutoff or a simulation-calibrated threshold. Its
noncoverage bound is approximately 0.04054; coverage is above 95.94%.

## An enclosing ellipsoid

Convexity gives, for y,lambda>=0,

    Z(y,lambda) >= (y-lambda)^2/[2 max(y,lambda)].

For y>=lambda this follows by integrating the second derivative 1/u of
h(u)=u log u-u+1 on [1,y/lambda]; the minimum there is lambda/y.
For y<=lambda, integrate on [y/lambda,1], where 1/u>=1. The zero cases follow
by continuity. On sum Z<=K=48, each coordinate satisfies

    lambda_i <= U_i = y_i+K+ceil_sqrt(K^2+2K y_i),
    sum_i (lambda_i-y_i)^2/U_i <= 2K=96.

The square-root ceiling is computed exactly on integers. This data-dependent
ellipsoid contains the likelihood region and retains the joint shape.

## Correlation-preserving error propagation

Scale signed squared distances by their common positive factor so that
s_j=-sqrt(m_j), where m=C lambda and the observed center is n=C y. The
common scale cancels in relative error. Set delta=lambda-y and r^2=96.
For each observed interval let v_j=sum_b C_jb^2 U_b and
L_j=n_j-ceil_sqrt(96 v_j). If any L_j<=0, issue no certificate. Otherwise

    s_j-s_hat_j = a_j (C delta)_j + R_j,
    a_j=-1/(2sqrt(n_j)),
    |R_j| <= 96 v_j/[8 L_j^(3/2)] = r_j.

This is Taylor's theorem with a second derivative bound for -sqrt(m).
The count center gives G_hat and d_hat as in v0.2. Let w=G_hat^-1 d_hat,
q_hat=-d_hat^T G_hat^-1 d_hat. An LDL decomposition with the sign pattern
(-,+,+,+) gives a whitening W with W^T G_hat W=J=diag(-1,1,1,1).

G_j and d_j denote the exact constant derivatives with respect to s_j. Define

    B_j=W^T G_j W,
    h_j=W^T(d_j-G_j w),
    l_j=w^T G_j w-2w^T d_j,
    B'_b=sum_j B_j a_j C_jb,
    h'_b=sum_j h_j a_j C_jb,
    l'_b=sum_j l_j a_j C_jb.

Weighted Cauchy-Schwarz on the ellipsoid gives the deterministic bounds

    epsilon = sqrt(96 sum_b U_b ||B'_b||_F^2) + sum_j r_j ||B_j||_F,
    H       = sqrt(96 sum_b U_b ||h'_b||_2^2) + sum_j r_j ||h_j||_2,
    A       = sqrt(96 sum_b U_b (l'_b)^2)     + sum_j r_j |l_j|.

These bounds sum correlated linear contributions before taking norms. They
do not turn each interval's fluctuation into a separately adversarial error.
Frobenius norms upper-bound the required operator norms.

For actual changes DeltaG,Deltad, let h=Deltad-DeltaG w. The following
identity is exact, with no small-noise truncation:

    q-q_hat = w^T DeltaG w-2w^T Deltad-h^T(G_hat+DeltaG)^-1 h.

If epsilon<1, the inverse in whitened coordinates has norm <=1/(1-epsilon).
Consequently, on the entire joint region,

    |q-q_hat| <= A+H^2/(1-epsilon) = B.

The resulting interval [max(0,q_hat-B),q_hat+B] for the squared proper time
can be square-rooted. No certificate is issued if the sufficient guards fail.

## Outward numerical evaluation and statistical interpretation

All issued certificates are re-evaluated using Decimal intervals with floor
and ceiling rounding on elementary arithmetic. Correctly rounded square
roots are expanded to neighboring representable values. The lower and upper
endpoints and the inverse-radius condition are therefore checked as
enclosures, not ordinary floating estimates. Precision is 60 significant
digits; selected results are independently repeated at 90 digits. This is
validated interval arithmetic under the documented Decimal implementation,
not proof-assistant verification or independent peer review.

Let [qhat_lo,qhat_hi] enclose the exact point estimate and [qlo,qhi] its
joint-region enclosure. The issue rule is checked with directed rounding:

    qlo>0,
    121 qlo >= 100 qhat_hi,
     81 qhi <= 100 qhat_lo.

It ensures at most 10% relative error in proper time whenever the true mean
is in the joint region. For each fixed model parameter, the unconditional
probability of issuing a wrong certificate is at most 2^30 exp(-24).
This is NOT a claim of the same error probability conditional on selecting
only certified observations. Uncertified observations retain HOLD.

## Sources for standard ingredients

- Poisson process and disjoint counts: Last and Penrose,
  https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf
- Exponential Poisson tail argument: Harchol-Balter, chapter 18,
  https://www.cs.cmu.edu/~harchol/Probability/chapters/chpt18.pdf
- Decimal rounding and neighboring values:
  https://docs.python.org/3.12/library/decimal.html

The observable-cell reduction and the propagation written here are derived
for this experiment. No novelty or external validation is asserted.
