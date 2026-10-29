#include <vector>
#include <cmath>
#include <cstdint>
#include <limits>

// Strict endpoint-excluded Alexandrov counts. Noncausal sentinel is -1.
// Floating-point near-null relations are re-evaluated in long double;
// unresolved relations are reported to the caller, never resampled.
static bool precedes(const double* a, const double* b, int64_t& unresolved) {
    double dt=b[0]-a[0];
    if (!(dt>0)) return false;
    double s=dt*dt, scale=s;
    for(int k=1;k<4;k++){double d=b[k]-a[k];s-=d*d;scale+=d*d;}
    if(std::abs(s)>64*std::numeric_limits<double>::epsilon()*scale) return s>0;
    long double t=(long double)b[0]-a[0], z=t*t, q=z;
    for(int k=1;k<4;k++){long double d=(long double)b[k]-a[k];z-=d*d;q+=d*d;}
    if(std::abs(z)<=64*std::numeric_limits<long double>::epsilon()*q) ++unresolved;
    return z>0;
}
extern "C" int64_t interval_counts(const double* x, int n, const double* p, int m,
                                    int32_t* out, int32_t* probes) {
    int w=(n+63)/64; int64_t unresolved=0;
    std::vector<uint64_t> past((size_t)n*w),future((size_t)n*w),pp(w);
    for(int i=0;i<n;i++)for(int j=0;j<i;j++)if(precedes(x+4*j,x+4*i,unresolved)){
        past[(size_t)i*w+j/64]|=uint64_t(1)<<(j%64);
        future[(size_t)j*w+i/64]|=uint64_t(1)<<(i%64);
    }
    if(out)for(int i=0;i<n;i++)for(int j=0;j<n;j++){
        int v=-1;
        if((past[(size_t)i*w+j/64]>>(j%64))&1){
            v=0;for(int k=0;k<w;k++)v+=__builtin_popcountll(past[(size_t)i*w+k]&future[(size_t)j*w+k]);
        }
        out[(size_t)i*n+j]=v;
    }
    for(int i=0;i<m;i++){
        std::fill(pp.begin(),pp.end(),0);
        for(int j=0;j<n;j++)if(precedes(x+4*j,p+4*i,unresolved))pp[j/64]|=uint64_t(1)<<(j%64);
        for(int j=0;j<n;j++){
            int v=-1;
            if((pp[j/64]>>(j%64))&1){
                v=0;for(int k=0;k<w;k++)v+=__builtin_popcountll(pp[k]&future[(size_t)j*w+k]);
            }
            probes[(size_t)i*n+j]=v;
        }
    }
    return unresolved;
}
