# Conditional testing and the direction of the bound

SPDX-License-Identifier: Apache-2.0

## Experiment

Condition on the previously selected PR88 witness pair and the A configuration.
Under each geometry, fresh B points follow the stipulated homogeneous Poisson
process. All 90 recorded interval counts are available. Pairwise overlaps and
an optional total physical point count enrich this observation channel. The
fixed integer classifier uses only its 90-count marginal. Each simulated vector
comes from a single shared cloud: arbitrary higher-order overlap dependence is
retained. This is a conditional two-hypothesis diagnostic, not a reconstruction
procedure over the whole geometry class or validation against physical data.

The protocol and implementation were hashed before training, and the trained
model was hashed before validation generation. These are reproducibility seals,
not independently timestamped preregistration. Training has 128 draws per class;
validation has 512 fresh draws per class with distinct pinned seeds. No held-out
threshold or model selection is performed. Conditioning on any trained classifier
leaves the following validation argument unchanged.

## Exact geometry and coupling

The rational Lorentz boost has coefficients 17/8 and 15/8 and determinant one.
Every interval lies within I(3,0). Its physical duration is strictly less than
1.5, so a common Lorentz transformation and translation place it within the
original B sampling diamond. Poisson restriction makes sampling an enclosing
auxiliary box equivalent for these interval counts. Points outside the box or
outside the intervals cannot change the classifier; auxiliary box population
is not an extra observable used by the test.

For endpoints separated by (T,dx,dy), the projected spatial radii of the diamond
are sqrt(T²-dy²)/2 and sqrt(T²-dx²)/2. Directed rational square-root bounds and
outward dyadic rounding enclose this box. With h=2^-30, uniformly chosen cells
and independent uniform positions inside them give uniform box points.
The code conservatively counts a cell only if its entirety is inside both cones,
including the exact endpoint enclosure. All squared comparisons use 128-bit
integers. Coordinate bounds keep these operations within range.

If true point membership differs from inner-cell membership, at least one
endpoint cone satisfies |t-tip_t ± spatial_radius| <= 5h: temporal extrema
change by at most 2h and spatial distance by at most 2 sqrt(2) h. For fixed x,y,
this slab has temporal width at most 10h. There are at most 42 cones, so its
union volume is at most 420h Axy, with Axy the spatial box area. The probability
that any Poisson point meets this union is bounded by its mean population.
Consequently, for each geometry g,

    TV(P_g(counts), Q_g(grid counts)) <= delta_g
    delta_g = rho * scale³ * 420h Axy
              + |rounded Poisson box mean - exact box mean|.

The last term follows by adding/removing an independent Poisson process to
couple the two rates. Delta_0 <= 0.00290694141531251195 and
Delta_1 <= 0.00291117098310259492. This deterministic approximation bound is
separate from validation sampling uncertainty.

## Held-out inference

For the sealed classifier, let r_g be its continuous-model error and e_g its
number of grid-law validation errors. Hoeffding gives, for n=512 and c=12,

    r_g <= min(1, e_g/n + sqrt(c/(2n)) + delta_g)

except on an event of probability at most exp(-c). A union bound over the two
classes costs at most 2 exp(-12), bounded with rational arithmetic by
0.00001228842470665642. There is no independence assumption between interval
counts. Independence is required between validation trials and from training.

For equally likely hypotheses, accuracy is 1-(r_0+r_1)/2. The minimum sum of
errors over all tests equals 1-TV(P_0,P_1); hence any attainable test yields

    TV(full observation laws) >= 1-r_0-r_1.

Projection onto counts cannot increase TV. Thus a test using counts gives a
LOWER bound for the richer observation law, even without simulating optional
additional fields. It cannot give a TV upper bound or a statistical minimax
reconstruction lower bound.

The mathematical confidence statement assumes ideal independent Poisson and
uniform draws. PCG64 with fixed seeds implements a reproducible numerical
experiment, not a proof of ideal randomness. Numerical replay does not remove
this assumption or the conditional, posthoc witness-pair scope.

## What this resolves

The two selected geometries are not statistically indistinguishable under this
model: a fixed test already separates them better than chance with a conservative
finite-sample bound. Their simultaneous membership in the earlier confidence
set and its 7.41% set-wise recovery lower bound remain valid in their stated scope.
Neither result establishes 10% accuracy or a 10% impossibility theorem.
The next identifiability question requires a different, statistically close
pair, or a direct stability theorem using the full joint observation law.
