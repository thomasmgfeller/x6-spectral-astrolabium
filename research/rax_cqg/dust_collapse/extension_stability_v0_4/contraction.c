/* C99 contractions of fixed Gauss grids. All storage belongs to the caller. */
#include <stddef.h>
#include <math.h>

typedef struct { double re, im; } Pair;

static inline Pair mul(Pair a, Pair b) {
    return (Pair){a.re*b.re - a.im*b.im, a.re*b.im + a.im*b.re};
}

/* z = exp(-i*c/2). The analytic series removes cancellation at c = 0. */
static inline Pair density(double c, Pair z) {
    if (fabs(c) < 0.125) {
        double u=c*c;
        return (Pair){1.0+u*(-1.0/48+u*(1.0/3840+u*(-1.0/645120+u/185794560))),
                      c*(-1.0/8+u*(1.0/384+u*(-1.0/46080+u/10321920)))};
    }
    double inv=1.0/c;
    return (Pair){0.5-z.im*inv, (z.re-1.0)*inv};
}

/* Pack the conditional sum over the fifth clock. Edges have axes
   (parent number, fifth index, corresponding parent index). */
void tail(int n, int parents, const double *base, const Pair *phase,
          const Pair *weight, const double *edge, const Pair *ephase, Pair *out) {
    if (parents == 0) {
        Pair total={0,0};
        for (int t=0;t<n;++t) {
            Pair v=mul(weight[t],density(base[t],phase[t]));
            total.re+=v.re; total.im+=v.im;
        }
        out[0]=total;
        return;
    }
    size_t blocks=1;
    for (int j=0;j<parents-1;++j) blocks*=n;
    for (size_t b=0;b<blocks;++b) {
        int ids[4]={0}; size_t id=b;
        for (int j=parents-2;j>=0;--j) { ids[j]=id%n; id/=n; }
        Pair *row=out+b*n;
        for (int k=0;k<n;++k) row[k]=(Pair){0,0};
        for (int t=0;t<n;++t) {
            double c=base[t]; Pair z=phase[t];
            for (int j=0;j<parents-1;++j) {
                size_t offset=((size_t)j*n+t)*n+ids[j];
                c+=edge[offset]; z=mul(z,ephase[offset]);
            }
            size_t last=((size_t)(parents-1)*n+t)*n;
            for (int k=0;k<n;++k) {
                Pair d=density(c+edge[last+k],mul(z,ephase[last+k]));
                Pair val=mul(weight[t],d);
                row[k].re+=val.re; row[k].im+=val.im;
            }
        }
    }
}

/* Contract the remaining four clocks. Prefix is the product of the first
   three density/weight factors. Stride zero broadcasts a missing tail edge. */
void finish(int n, const Pair *prefix, const double *base, const Pair *phase,
            const Pair *weight, const double *edge, const Pair *ephase,
            const Pair *conditional, const long long *stride, Pair *out) {
    Pair total={0,0};
    for (int a=0;a<n;++a) for (int b=0;b<n;++b) {
        double cab[n]; Pair zab[n];
        for (int t=0;t<n;++t) {
            size_t i=(size_t)a*n+t, j=((size_t)n+b)*n+t;
            cab[t]=base[t]+edge[i]+edge[j];
            zab[t]=mul(mul(phase[t],ephase[i]),ephase[j]);
        }
        for (int c=0;c<n;++c) {
            size_t pos=((size_t)a*n+b)*n+c, edgepos=((size_t)2*n+c)*n;
            size_t q=a*stride[0]+b*stride[1]+c*stride[2];
            Pair row={0,0};
            for (int t=0;t<n;++t) {
                Pair v=mul(weight[t],density(cab[t]+edge[edgepos+t],mul(zab[t],ephase[edgepos+t])));
                Pair term=mul(v,conditional[q+t*stride[3]]);
                row.re+=term.re; row.im+=term.im;
            }
            Pair term=mul(prefix[pos],row);
            total.re+=term.re; total.im+=term.im;
        }
    }
    *out=total;
}
