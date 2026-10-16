# Computational specification before new target generation

This implements the unchanged PR #42 contract. Its historical design status
remains unchanged in contract.json; execution status belongs to RESULTS.json.
No target draw is used for development or timing. Only deterministic examples
and six m=4 draws under a different namespace precede the source freeze.

- Python 3.12, NumPy 2.3.5, one numerical-library thread. Per phase: 1,800 seconds,
  2 GiB address space. Fresh output directories; failure retains INCONCLUSIVE.json.
- Marks are positions 0 and 1; background positions start at 2. Endpoint and
  background generation order, floating-point comparisons and collision handling
  follow the contract. Matrices are archived as lossless binary strings.
- Public inference accepts exactly N, marks and relation_rows; negative indices,
  duplicate marks, nonbinary/nontransitive relations and extra fields fail.
  Calibration accepts exactly split, packet and theta, and only calibration rows.
  Supervised calibration labels are permitted; test labels never enter fitting.
- V/L/C0 use only intrinsic statistics computed from that packet. D uses the six
  fixed unstandardized polynomial columns. No tuning, alternative fit or correction.
  Model size, coefficients, singular values, rank and normal-equation residual remain
  archived. An independent least-squares path uses numpy.linalg.lstsq with rcond=1e-12.
- All 6,912 generated orders are retained. Matching is written before model fitting
  and loss evaluation. The matching function reads only family, split, draw, id, m,
  R and H, and uses the prescribed priorities. No selected cohort replaces primary.
- Each unselected bootstrap uses the exact specified stream, 5,000 rows of n
  indices, generated replicate-major and position-minor with below(n). The same
  indices serve every method and loss. Matched bootstraps draw complete pairs;
  each pair supplies one uniform and one jittered observation. Transfer differences
  are jittered minus uniform MSE and are descriptive.
- Report MSE, RMSE, MAE and signed bias, with percentile intervals. Also report
  squared-time bias/MSE and zero-K counts. The ideal analytic squared-time MSE
  is printed as a reference, never a forced numerical equality gate. No unplanned
  hypothesis test is added to that diagnostic.
- Independent validation regenerates the stream with a separate implementation,
  checks every raw draw, obtains relations from t,x, and resolves near-null floating
  boundaries with exact rational representations of the stored floats. Chain
  heights use sorted-coordinate longest nondecreasing subsequences. Every full
  order is reversed in labels with transported marks and sent through inference.
- The checker separately reconstructs matching, calibrates by least squares,
  calculates losses, uses a separate stream replay and scalar percentile formula
  for all bootstraps, and verifies the primary gates. Numeric agreement uses
  atol=1e-10 and rtol=1e-9, coefficients additionally atol=rtol=1e-8; exact fields,
  selections and decisions must agree exactly. The two linear algebra paths use
  the same installed library, so this is not a person-independent replication.
- All raw predictions and signed individual errors are archived. Inconclusive
  runs are never promoted by the comparison tool. Time and memory observations
  are not compared bitwise across machines or described as speed superiority.

The computational source freeze includes this file, the unchanged design,
all executed project sources, requirements and the new workflow. Publication of
that source commit must precede the first target invocation. Later interpretation
belongs in RESULTS.md; it may not silently change this specification or the code.
