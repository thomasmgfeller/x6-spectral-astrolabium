// Adapted from PR 257: n<=5 and disjoint mixed-radix index ranges.
// Outward fixed-point intervals; checked integer operations, no floating-point math.
#include <algorithm>
#include <array>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using Z=__int128_t;
const Z S=Z(1)<<60;
void need(bool b,const char* s){if(!b)throw std::runtime_error(s);}
Z add(Z a,Z b){Z c;need(!__builtin_add_overflow(a,b,&c),"integer add overflow");return c;}
Z sub(Z a,Z b){Z c;need(!__builtin_sub_overflow(a,b,&c),"integer subtract overflow");return c;}
Z mul(Z a,Z b){Z c;need(!__builtin_mul_overflow(a,b,&c),"integer multiply overflow");return c;}
Z fl(Z a,Z b){need(b>0,"positive divisor");Z q=a/b;return a<0&&a%b?sub(q,1):q;}
Z ce(Z a,Z b){need(b>0,"positive divisor");Z q=a/b;return a>0&&a%b?add(q,1):q;}
Z absz(Z x){return x<0?sub(0,x):x;}
Z parse(const std::string& s){Z n=0;bool minus=s[0]=='-';for(size_t i=minus;i<s.size();++i){need(s[i]>='0'&&s[i]<='9',"integer syntax");n=add(mul(n,10),s[i]-'0');}return minus?sub(0,n):n;}
Z readz(){std::string s;need(bool(std::cin>>s),"integer input");return parse(s);}
std::string str(Z x){bool minus=x<0;if(minus)x=sub(0,x);std::string s;do{s.push_back(char('0'+x%10));x/=10;}while(x);if(minus)s.push_back('-');std::reverse(s.begin(),s.end());return s;}
struct I{Z l,h;I(Z a=0,Z b=0):l(a),h(b){need(a<=b,"ordered interval");}};
const I zero(0,0),one(S,S);
I readi(){Z l=readz(),h=readz();return I(l,h);}
void printi(I a){std::cout<<str(a.l)<<' '<<str(a.h)<<' ';}
I operator+(I a,I b){return I(add(a.l,b.l),add(a.h,b.h));}
I operator-(I a){return I(sub(0,a.h),sub(0,a.l));}
I operator-(I a,I b){return a+-b;}
I operator*(I a,I b){
 Z low,high;
 if(a.l>=0&&b.l>=0){low=mul(a.l,b.l);high=mul(a.h,b.h);}
 else{std::array<Z,4> v={mul(a.l,b.l),mul(a.l,b.h),mul(a.h,b.l),mul(a.h,b.h)};low=*std::min_element(v.begin(),v.end());high=*std::max_element(v.begin(),v.end());}
 return I(fl(low,S),ce(high,S));
}
I times(I a,Z k){return k<0?times(-a,sub(0,k)):I(mul(a.l,k),mul(a.h,k));}
I divide(I a,Z k){need(k!=0,"nonzero divisor");return k<0?divide(-a,sub(0,k)):I(fl(a.l,k),ce(a.h,k));}
I operator/(I a,I b){
 need(b.l>0||b.h<0,"interval divisor excludes zero");if(b.h<0)return (-a)/(-b);
 std::array<Z,4> ns={mul(a.l,S),mul(a.l,S),mul(a.h,S),mul(a.h,S)};
 std::array<Z,4> ds={b.l,b.h,b.l,b.h};Z low=fl(ns[0],ds[0]),high=ce(ns[0],ds[0]);
 for(int i=1;i<4;++i){low=std::min(low,fl(ns[i],ds[i]));high=std::max(high,ce(ns[i],ds[i]));}return I(low,high);
}
I powi(I a,int n){I out=one;for(int j=0;j<n;++j)out=out*a;return out;}
I widen(I a){return I(sub(a.l,1),add(a.h,1));}
struct C{I re,im;};
const C cone{one,zero},czero{zero,zero};
C operator+(C a,C b){return C{a.re+b.re,a.im+b.im};}
C operator*(C a,C b){return C{a.re*b.re-a.im*b.im,a.re*b.im+a.im*b.re};}
C scale(C a,I x){return C{a.re*x,a.im*x};}
I pi;
C cis(I t){
 Z num=mul(2,add(t.l,t.h)),den=add(pi.l,pi.h);
 Z kval=fl(add(mul(2,num),den),mul(2,den));need(absz(kval)<10000,"range reduction integer");int k=int(kval);
 I x=t-divide(times(pi,k),2);need(std::max(absz(x.l),absz(x.h))<=S,"reduced phase <=1");
 I x2=x*x,c=one,s=x,tc=one,ts=x;
 for(int j=1;j<=16;++j){tc=divide(-(tc*x2),(2*j-1)*(2*j));ts=divide(-(ts*x2),(2*j)*(2*j+1));c=c+tc;s=s+ts;}
 // 2^60/34! and 2^60/35! are positive and less than one.
 c=widen(c);s=widen(s);int quadrant=(k%4+4)%4;
 if(quadrant==0)return C{c,s};
 if(quadrant==1)return C{-s,c};
 if(quadrant==2)return C{-c,-s};
 return C{s,-c};
}
C chi(I t){
 if(std::max(absz(t.l),absz(t.h))<=S){
  I re=one,im=zero,term=one;
  for(int k=1;k<=36;++k){term=divide(term*t,k+1);if(k%4==0)re=re+term;else if(k%4==1)im=im-term;else if(k%4==2)re=re-term;else im=im+term;}
  // 2^60/(2*38!) < 1; retain one outward unit.
  return C{widen(divide(one+re,2)),widen(divide(im,2))};
 }
 C z=cis(t);return C{divide(one+z.im/t,2),-divide((one-z.re)/t,2)};
}
struct Term{int key;I c;};
int main(){try{
 std::string mode;need(bool(std::cin>>mode),"mode input");
 if(mode=="overflow"){mul(Z(1)<<126,2);throw std::runtime_error("overflow was not rejected");}
 pi=readi();
 if(mode=="ops"){
  int n;std::cin>>n;for(int j=0;j<n;++j){I a=readi(),b=readi();printi(a+b);printi(a-b);printi(a*b);printi(a/b);std::cout<<'\n';}return 0;
 }
 if(mode=="points"){
  int n;std::cin>>n;for(int j=0;j<n;++j){I a=readi();C c=cis(a),d=chi(a);printi(c.re);printi(c.im);printi(d.re);printi(d.im);std::cout<<'\n';}return 0;
 }
 need(mode=="integrate","known operation");
 int n,ng,np,nm,nc;std::cin>>n>>ng>>np>>nm>>nc;need(n>=1&&n<=5&&ng>=1&&ng<=357,"input dimensions");
 need(np>=1&&np<=1785&&nm>=1&&nm<=243&&nc>=1&&nc<=1785,"bounded circuit dimensions");
 long long begin,end;std::cin>>begin>>end;
 std::vector<int> q(n),idx(n,0);long long count=1;
 for(int &x:q){std::cin>>x;need(x>=1&&x<=128,"quadrature order");count*=x;}
 need(begin>=0&&begin<end&&end<=count&&end-begin<=65536,"bounded index range");
 long long offset=begin;for(int j=n-1;j>=0;--j){idx[j]=int(offset%q[j]);offset/=q[j];}
 std::vector<std::vector<I>> nodes(n),weights(n);
 for(int j=0;j<n;++j)for(int k=0;k<q[j];++k){nodes[j].push_back(readi());weights[j].push_back(readi());}
 std::vector<std::vector<int>> keys(nm,std::vector<int>(n));for(auto &key:keys)for(int &x:key){std::cin>>x;need(x>=0&&x<=2,"monomial degree");}
 std::vector<std::vector<Term>> polys(np);
 for(auto &poly:polys){int count;std::cin>>count;for(int k=0;k<count;++k){int key;std::cin>>key;need(key>=0&&key<nm,"monomial index");poly.push_back(Term{key,readi()});}}
 std::vector<std::pair<int,int>> circuit(nc);
 for(int k=0;k<nc;++k){auto &x=circuit[k];std::cin>>x.first>>x.second;need(x.first>=0&&x.first<=k&&x.second>=0&&x.second<np,"circuit ordering");}
 std::vector<int> leaves(ng);for(int &x:leaves){std::cin>>x;need(x>=1&&x<=nc,"leaf index");}
 need(bool(std::cin),"complete integral input");
 std::vector<C> sums(ng,czero),chars(np),values(nc+1);values[0]=cone;
 std::vector<I> monomials(nm);I norm=zero;int factorial=1;for(int j=2;j<=n;++j)factorial*=j;
 for(long long it=begin;it<end;++it){
  std::vector<std::array<I,3>> powers(n);I weight=times(one,factorial);
  for(int j=0;j<n;++j){I u=nodes[j][idx[j]];powers[j]={one,u,u*u};weight=weight*weights[j][idx[j]]*powi(u,j);}
  for(int k=0;k<nm;++k){I value=one;for(int j=0;j<n;++j)value=value*powers[j][keys[k][j]];monomials[k]=value;}
  for(int k=0;k<np;++k){I t=zero;for(const auto &term:polys[k])t=t+monomials[term.key]*term.c;chars[k]=chi(t);}
  for(int k=0;k<nc;++k)values[k+1]=values[circuit[k].first]*chars[circuit[k].second];
  norm=norm+weight;for(int k=0;k<ng;++k)sums[k]=sums[k]+scale(values[leaves[k]],weight);
  for(int j=n-1;j>=0;--j){if(++idx[j]<q[j])break;idx[j]=0;}
 }
 printi(norm);std::cout<<end-begin<<'\n';for(C c:sums){printi(c.re);printi(c.im);std::cout<<'\n';}
 return 0;
 }catch(const std::exception &e){std::cerr<<e.what()<<'\n';return 2;}}

