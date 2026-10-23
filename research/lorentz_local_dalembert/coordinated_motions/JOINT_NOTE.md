# Post-screen check of the one surviving candidate

SPDX-License-Identifier: Apache-2.0

The original finite screen produced 166 order/margin rejections, 204 weight gaps
at or below 20%, 49 full-law lower bounds above 1/4, and one HOLD. Those outputs
are retained unchanged. This is a separately frozen follow-up, chosen after the
screening results were known, not part of the original pre-run contract.

Candidate 12 moves node 15 by 12500000000/264451347681 in boosted x and node 5
by -1/20. Its exact symmetric relative weight gap is between
0.21714701801847050529 and 0.21714701801847050530. Its largest of the two tested
single-count event lower bounds is 0.24934433038531550259, which was inconclusive.

Choose X=N(I(2,5)) and Y=N(I(5,1)). Every point in X is in the strict causal past
of node 5; every point in Y is in its strict future. These regions are disjoint
under both exact geometries. Independent increments of the homogeneous Poisson
process give the exact product law for THESE TWO counts. This says nothing
about independence of overlapping intervals elsewhere in the observation.

Their means are approximately (102.21488,1081.16810) at the reference and
(97.88099,1102.16602) at the moved geometry. Freeze E={Y-2X<=891}; the threshold
is the floor of the midpoint of their expected Y-2X values. Its probability is

    P(E) = sum_{j>=0} P(X=j) P(Y<=891+2j).

The inherited directed integer routine bounds this series with both infinite
tails retained, and encloses the geometric means using exact q, square-root and
pi bounds. E is increasing in X and decreasing in Y, so endpoint mean bounds
give probability enclosures. Absolute separation of those event probabilities
lower-bounds TV of the two-count law and hence of the full observation law.

This is one event at one exact point. No threshold optimization, empirical data,
or independent validation cloud is used. The independent audit sums the PMFs
directly at 110 decimal digits to check the implementation; the directed bounds,
not that numerical agreement, provide the certificate. No continuous exclusion
between paired search steps follows.
