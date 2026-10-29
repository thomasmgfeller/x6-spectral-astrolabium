#include <vector>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <limits>
#include <cfenv>

// Coordinates are the exact dyadic values represented by finite binary64.
// Outward one-ULP intervals enclose every elementary operation. Compile without
// fast-math or contraction. Ambiguous signs use exact integer arithmetic.
static double down(double x){return std::nextafter(x,-INFINITY);}
static double up(double x){return std::nextafter(x,INFINITY);}
struct I { double l,h; };
static I sub(double b,double a){double d=b-a;return {down(d),up(d)};}
static I square(I x){
    double l=x.l<=0&&x.h>=0?0:down(std::min(x.l*x.l,x.h*x.h));
    return {std::max(0.,l),up(std::max(x.l*x.l,x.h*x.h))};
}
static int (*exact_sign)(const double*,const double*)=nullptr;
extern "C" void set_exact_sign(int (*callback)(const double*,const double*)){exact_sign=callback;}
static bool precedes(const double* a,const double* b,int64_t* stats){
    stats[0]++;if(!(b[0]>a[0]))return false;
    I s=square(sub(b[0],a[0]));
    for(int k=1;k<4;k++){I q=square(sub(b[k],a[k]));s={down(s.l-q.h),up(s.h-q.l)};}
    if(s.l>0)return true;if(s.h<0)return false;
    stats[1]++;int sign=exact_sign(a,b);if(!sign)stats[2]++;
    return sign>0; // Exact null is excluded by the declared strict-order rule.
}
extern "C" int causal_inventory(const double* x,int n,const double* p,int m,
 int32_t* counts,int32_t* pc,uint64_t* past,uint64_t* ppast,int64_t* stats){
    volatile double tiny=std::numeric_limits<double>::denorm_min();
    volatile double twice=tiny+tiny;
    if(!std::numeric_limits<double>::is_iec559 || std::fegetround()!=FE_TONEAREST || !(tiny>0 && twice>tiny))return 1;
    const int w=(n+63)/64;
    std::fill(past,past+(size_t)n*w,0);std::fill(ppast,ppast+(size_t)m*w,0);
    std::vector<uint64_t> future((size_t)n*w,0);
    for(int i=0;i<n;i++)for(int j=0;j<i;j++)if(precedes(x+4*j,x+4*i,stats)){
        past[(size_t)i*w+j/64]|=uint64_t(1)<<(j%64);
        future[(size_t)j*w+i/64]|=uint64_t(1)<<(i%64);
    }
    for(int i=0;i<m;i++)for(int j=0;j<n;j++)if(precedes(x+4*j,p+4*i,stats))
        ppast[(size_t)i*w+j/64]|=uint64_t(1)<<(j%64);
    if(counts)for(int i=0;i<n;i++)for(int j=0;j<n;j++){
        int v=-1;if((past[(size_t)i*w+j/64]>>(j%64))&1){
            v=0;for(int k=0;k<w;k++)v+=__builtin_popcountll(past[(size_t)i*w+k]&future[(size_t)j*w+k]);
        }counts[(size_t)i*n+j]=v;
    }
    if(pc)for(int i=0;i<m;i++)for(int j=0;j<n;j++){
        int v=-1;if((ppast[(size_t)i*w+j/64]>>(j%64))&1){
            v=0;for(int k=0;k<w;k++)v+=__builtin_popcountll(ppast[(size_t)i*w+k]&future[(size_t)j*w+k]);
        }pc[(size_t)i*n+j]=v;
    }
    return 0;
}
extern "C" int relation(const double* a,const double* b,int64_t* stats){return precedes(a,b,stats)?1:0;}
extern "C" void region_membership(const double* x,int n,double h,uint8_t* out,int64_t* stats){
    const double lo[4]={-h,0,0,0},hi[4]={h,0,0,0};
    for(int i=0;i<n;i++){
        bool a=precedes(lo,x+4*i,stats),b=precedes(x+4*i,hi,stats);out[i]=a&&b;
    }
}
