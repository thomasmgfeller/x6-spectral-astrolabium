/* Six-by-six local interpolation on two summed phase coefficients. */
#include <math.h>
#include <stddef.h>
typedef struct {double re,im;} Pair;
static int weights(double u,int count,double w[6]){
    int begin=(int)floor(u)-2;
    if(begin<0)begin=0;
    if(begin>count-6)begin=count-6;
    double t=u-begin;
    for(int j=0;j<6;j++){
        double v=1.0;
        for(int k=0;k<6;k++) if(k!=j)v*=(t-k)/(j-k);
        w[j]=v;
    }
    return begin;
}
void reduce(int na,int nb,int nc,int nd,int nu,int nv,double u0,double v0,double du,double dv,
    const double *xa,const double *xb,const double *xc,const double *xd,const Pair *table,const Pair *prefix,const Pair *cond,Pair *out){
    double re=0.0,im=0.0;
    for(int a=0;a<na;a++)for(int b=0;b<nb;b++)for(int c=0;c<nc;c++){
        double u=-8*xa[a]*xa[a]+16*xb[b]*xb[b]-9*xc[c]*xc[c];
        double v=-8*xa[a]+16*xb[b]-9*xc[c];
        size_t abc=((size_t)a*nb+b)*nc+c;
        double zr=0.0,zi=0.0;
        for(int k=0;k<nd;k++){
            double wu[6],wv[6];
            int i=weights((u+xd[k]*xd[k]-u0)/du,nu,wu);
            int j=weights((v+xd[k]-v0)/dv,nv,wv);
            double tr=0.0,ti=0.0;
            for(int l=0;l<6;l++){
                const Pair *row=table+(size_t)(i+l)*nv+j;
                double br=0,bi=0;
                for(int m=0;m<6;m++){br+=wv[m]*row[m].re;bi+=wv[m]*row[m].im;}
                tr+=wu[l]*br;ti+=wu[l]*bi;
            }
            Pair f=cond[abc*nd+k];
            zr+=f.re*tr-f.im*ti;zi+=f.re*ti+f.im*tr;
        }
        Pair p=prefix[abc];
        re+=p.re*zr-p.im*zi;im+=p.re*zi+p.im*zr;
    }
    out[0]=(Pair){re,im};
}
