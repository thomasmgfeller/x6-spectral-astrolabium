# Fixed full-law testing experiment

SPDX-License-Identifier: Apache-2.0

Condition on the two already selected exact PR88 geometries. The experiment
is a fresh independent B Poisson draw at the original density. The scientific
measurement channel includes all 90 recorded interval counts and their pairwise
overlap counts. A classifier using only the 90 counts is also a valid test of
that richer channel (including optional total physical point count). Hashes
and simulator-coordinate identifiers are provenance, not physical observables.

Generate 128 independent training draws per geometry, form the equal-class
pooled covariance with fixed 10% diagonal shrinkage, and combine it with the
analytic mean difference. Quantize coefficients to integers with maximum
magnitude 4096 and fix the midpoint threshold from analytic mean enclosures.
Seal this model before generating any validation draws. No threshold tuning,
classifier selection, hyperparameter search or re-fit on validation results.

Generate exactly 512 held-out draws per geometry. Every count vector arises
from one shared Poisson cloud and exact whole-cell cone classification; no
Gaussian/covariance-only surrogate. Use dyadic cell size 2^-30 and 128-bit
integer squared-distance arithmetic. Bound continuous-vs-cell-law TV by the
union of 42 cone boundary slabs (width 10h) times the spatial bounding-box area,
plus the exact-to-double Poisson-mean difference. No physical data are added.

For each class, add sqrt(12/(2*512)) to held-out error frequency, then add the
proved grid coupling bound. The two one-sided Hoeffding tails cost 2 exp(-12).
Report achieved accuracy lower bound and full-channel TV lower bound. Do not
reverse the data-processing direction or infer a TV upper bound. Stop after
fixed training/validation, exact classifier audit and replay. Scientific HOLDs
remain; this is a conditional pair diagnostic, not general reconstruction.
