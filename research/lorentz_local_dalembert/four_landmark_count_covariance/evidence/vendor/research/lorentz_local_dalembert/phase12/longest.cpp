// Original implementation, Apache-2.0. Input is a relation, never coordinates.
#include <cstdint>
#include <vector>
extern "C" void longest_to(const uint8_t* r, const int32_t* order, int n,
                           int target, int reverse, int32_t* out) {
    auto precedes = [&](int a, int b) {return r[reverse ? b*n+a : a*n+b] != 0;};
    std::vector<int> ancestors;
    for (int i=0;i<n;++i) out[i]=-1;
    out[target]=0;
    for (int k=0;k<n;++k) {
        int a=order[reverse ? n-1-k : k];
        if (a==target || precedes(a,target)) ancestors.push_back(a);
    }
    for (int k=int(ancestors.size())-2;k>=0;--k) {
        int a=ancestors[k], best=-1;
        for(int l=k+1;l<int(ancestors.size());++l) {
            int b=ancestors[l];
            if(precedes(a,b) && out[b]>=0 && out[b]+1>best) best=out[b]+1;
        }
        out[a]=best;
    }
}
