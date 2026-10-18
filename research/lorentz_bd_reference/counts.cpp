// SPDX-License-Identifier: Apache-2.0
// Strict causal predicate, sorted conformal coordinates; no fast-math.
extern "C" void future_counts(const double* x, int n, long long* out) {
  for (int i=0; i<n; ++i) {
    out[i]=0;
    for (int j=i+1; j<n; ++j) {
      double dt=x[4*j]-x[4*i];
      double a=x[4*j+1]-x[4*i+1];
      double b=x[4*j+2]-x[4*i+2];
      double c=x[4*j+3]-x[4*i+3];
      if (dt>0 && dt*dt>a*a+b*b+c*c) ++out[i];
    }
  }
}
