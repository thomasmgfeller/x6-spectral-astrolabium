# Fixed joint-operator audit

SPDX-License-Identifier: Apache-2.0

Use the same 20 archived packets and PR90's confidence relaxation, unchanged.
No new samples, nonconvex optimization, fitted coordinates, gate thresholds or
physical field constants. Keep the existing fitted reference coordinates and
exact stored pivots. Before evaluation freeze this code and all immediate
source inputs. This is posthoc on known data, not new-data preregistration.

Transform mean-difference constraints through the concave map q=const*mu^(2/3)
using exact extremizers on each pair box. Round outward to 1e-12 q units and
propagate integer difference constraints. Bound linear forms via exact feasible
transport flows, not uncertified optimizer objectives. Use those bounds for
linear design terms, coordinate-linear forms and target terms; retain explicit
quadratic remainders. Use only full-radius evaluation, no artificial local box.

Ablate independent marginal boxes with the same transport procedure versus the
joint graph. Also compare the old symmetric box bound. A greedy flow may be
suboptimal, so combine the smaller valid component bounds from box and joint
runs. Preserve all failed contractions and HOLDs. No changed rule after results.
Stop after all cases, synthetic checks and exact replay. Do not turn a reduced
conservative bound into a reconstruction accuracy or instability claim.
