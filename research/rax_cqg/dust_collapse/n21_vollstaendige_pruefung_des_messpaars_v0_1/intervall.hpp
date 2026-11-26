// Endpoints are integer multiples of 10^-9. All quotients round outwards.
#pragma once
#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
using Tick = std::int64_t;
using Wide = __int128_t;
constexpr Tick S = 1000000000LL;
struct Box { Tick l,h; };
inline Box point(Tick a) { return {a,a}; }
inline Box operator+(Box a,Box b){ return {a.l+b.l,a.h+b.h}; }
inline Box operator-(Box a){ return {-a.h,-a.l}; }
inline Box operator-(Box a,Box b){ return a+(-b); }
inline Box operator*(int k,Box a){ return k>=0?Box{k*a.l,k*a.h}:Box{k*a.h,k*a.l}; }
inline Wide floorq(Wide n,Wide d) { if(d<0){n=-n;d=-d;} return n/d-(n%d<0); }
inline Wide ceilq(Wide n,Wide d) {return -floorq(-n,d);}
inline Tick tick(Wide a){assert(a>=INT64_MIN && a<=INT64_MAX);return static_cast<Tick>(a);}
inline Box operator*(Box a,Box b){
    Wide p=Wide(a.l)*b.l,q=Wide(a.h)*b.l,r=Wide(a.l)*b.h,s=Wide(a.h)*b.h;
    return {tick(floorq(std::min({p,q,r,s}),S)),tick(ceilq(std::max({p,q,r,s}),S))};
}
inline Box sq(Box a){
    Wide p=Wide(a.l)*a.l,q=Wide(a.h)*a.h;
    return {a.l<=0 && a.h>=0?0:tick(floorq(std::min(p,q),S)),tick(ceilq(std::max(p,q),S))};
}
inline Tick isqrt(Wide n){
    assert(n>=0);
    Tick x=static_cast<Tick>(std::sqrt(static_cast<long double>(n)));
    while(Wide(x)*x>n) --x;
    while(Wide(x+1)*(x+1)<=n) ++x;
    return x;
}
inline Box root(Box a){
    assert(a.h>=0);
    Wide hi=Wide(a.h)*S;
    Tick r=isqrt(hi);
    return {isqrt(Wide(std::max<Tick>(0,a.l))*S),r+(Wide(r)*r<hi)};
}
inline Box divided(Box a,int k){
    assert(k!=0);
    if(k<0) return divided(-a,-k);
    return {tick(floorq(a.l,k)),tick(ceilq(a.h,k))};
}
inline bool contains0(Box a){return a.l<=0 && a.h>=0;}
inline Box intersect(Box a,Box b){return {std::max(a.l,b.l),std::min(a.h,b.h)};}
inline bool empty(Box a){return a.l>a.h;}
inline Box hull(Box a,Box b){if(empty(a))return b;if(empty(b))return a;return {std::min(a.l,b.l),std::max(a.h,b.h)};}
// Bound solutions of coeff*x in rhs, restricting x to its current physical box.
// A denominator approaching zero always leaves the full box available.
inline Box linear(Box x,Box coeff,Box rhs){
    if(contains0(coeff))return x;
    Wide n[2]={Wide(rhs.l)*S,Wide(rhs.h)*S};
    Wide lo=floorq(n[0],coeff.l),hi=ceilq(n[0],coeff.l);
    for(Wide a:n) for(Tick b:{coeff.l,coeff.h}){
        lo=std::min(lo,floorq(a,b));hi=std::max(hi,ceilq(a,b));
    }
    if(lo>x.h || hi<x.l)return {1,0};
    return {tick(std::max<Wide>(x.l,lo)),tick(std::min<Wide>(x.h,hi))};
}
inline Box rest(Box sum,Box part){return {sum.l-part.l,sum.h-part.h};}
