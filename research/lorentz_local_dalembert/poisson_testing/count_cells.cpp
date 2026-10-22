// Exact cell membership for joint Poisson count simulations.
// SPDX-License-Identifier: Apache-2.0
#include <cstdint>
#include <algorithm>
extern "C" int count_cells(const int64_t* cells, int64_t n,
 const int64_t* lo,const int64_t* hi,int nodes,
 const uint64_t* fbits,const uint64_t* pbits,int64_t* counts){
 if(nodes!=21 || n<0)return 1;
 for(int64_t k=0;k<n;k++){
  uint64_t f[2]={0,0},p[2]={0,0};
  const int64_t* v=cells+3*k;
  for(int j=0;j<3;j++)if(v[j]<=-1000000000000LL||v[j]>=1000000000000LL)return 2;
  for(int a=0;a<nodes;a++){
   const int64_t* l=lo+3*a;const int64_t* h=hi+3*a;
   __int128 r2=0;
   for(int j=1;j<3;j++){
    __int128 u=(__int128)v[j]-h[j],w=(__int128)v[j]+1-l[j];
    if(u<0)u=-u;if(w<0)w=-w;__int128 d=std::max(u,w);r2+=d*d;
   }
   __int128 df=(__int128)v[0]-h[0],dp=(__int128)l[0]-v[0]-1;
   if(df>0 && df*df>r2){f[0]|=fbits[2*a];f[1]|=fbits[2*a+1];}
   if(dp>0 && dp*dp>r2){p[0]|=pbits[2*a];p[1]|=pbits[2*a+1];}
  }
  for(int word=0;word<2;word++){
   uint64_t active=f[word]&p[word];
   while(active){int bit=__builtin_ctzll(active);counts[64*word+bit]++;active&=active-1;}
  }
 }
 return 0;
}
