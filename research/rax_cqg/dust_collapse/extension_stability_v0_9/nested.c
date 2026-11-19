/* Reuse the reference density and complex arithmetic. C99, one CPU thread. */
#include "contraction.c"

/* Axes a,b,c,d are clocks 4,5,6,11. The two stored tails carry
   (b,c,t,d) for clock 13 and (a,b,c,d) for clock 14. Integrate
   clock 12 at t with its own density and multiply the clock 14 tail. */
void nested(int n, const double *edge, const Pair *phase, const Pair *weight,
            const Pair *tail13, Pair *tail14) {
    for (int a=0; a<n; ++a) for (int b=0; b<n; ++b) for (int c=0; c<n; ++c) {
        Pair row[n];
        for (int d=0; d<n; ++d) row[d]=(Pair){0,0};
        for (int t=0; t<n; ++t) {
            size_t i=(size_t)t*n+a, j=((size_t)n+t)*n+b, k=((size_t)2*n+t)*n+c;
            double base=1+edge[i]+edge[j]+edge[k];
            Pair initial=mul((Pair){cos(-0.5),sin(-0.5)},mul(mul(phase[i],phase[j]),phase[k]));
            size_t last=((size_t)3*n+t)*n;
            const Pair *other=tail13+(((size_t)b*n+c)*n+t)*n;
            for (int d=0; d<n; ++d) {
                Pair h=density(base+edge[last+d],mul(initial,phase[last+d]));
                Pair z=mul(mul(weight[t],h),other[d]);
                row[d].re+=z.re; row[d].im+=z.im;
            }
        }
        Pair *out=tail14+(((size_t)a*n+b)*n+c)*n;
        for (int d=0; d<n; ++d) out[d]=mul(out[d],row[d]);
    }
}
