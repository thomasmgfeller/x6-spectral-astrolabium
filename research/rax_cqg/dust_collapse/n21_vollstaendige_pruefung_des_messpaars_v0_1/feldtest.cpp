// C++17. One row is one labelled order extending the same N19 parent.
#include "intervall.hpp"
#include <array>
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <utility>
using Row=std::array<int,4>;
constexpr int N=21;
constexpr int DUST[]={4,5,6,11,12,13,14};
constexpr int FREE[]={4,5,6,11,12,13,14,15,16,17,18,19,20};
constexpr int LAYER[]={1,-9,16,-8};
struct Edge{int j,c;};
struct Model{
    std::array<int,N> past{},future{};
    std::array<std::vector<Edge>,N> inc,out;
    Model(const std::vector<std::pair<int,int>>& old,Row row){
        auto add=[&](int i,int j){past[j]|=1<<i;future[i]|=1<<j;};
        for(auto [i,j]:old)add(i,j);
        for(int s=0;s<2;++s)for(int i=0;i<19;++i){
            if(row[2*s]&(1<<i))add(i,19+s);
            if(row[2*s+1]&(1<<i))add(19+s,i);
        }
        for(int i=0;i<N;++i)for(int j=0;j<N;++j)if(future[i]&(1<<j)){
            int count=__builtin_popcount(future[i]&past[j]);
            if(count<4){inc[j].push_back({i,LAYER[count]});out[i].push_back({j,LAYER[count]});}
        }
    }
};
struct Fields{std::array<Box,N> y,w;};
struct Failure{const char* law;int node;};
struct Test{
    const Model& m;Fields f;bool changed=false;bool parent=false,reverse=false;
    void bind(Box& v,Box b,const char* eq,int j){
        b=intersect(v,b);
        if(empty(b))throw Failure{eq,j};
        changed |= b.l!=v.l || b.h!=v.h;v=b;
    }
    void chronology(){
        for(int j=0;j<N;++j)for(unsigned a=m.past[j];a;a&=a-1){
            int i=__builtin_ctz(a);Box &l=f.y[i],&r=f.y[j];
            if(l.l>=r.h)throw Failure{"time",j};
            if(l.h>r.h){l.h=r.h;changed=true;}
            if(r.l<l.l){r.l=l.l;changed=true;}
        }
    }
    Box gap(int i,int j)const{
        Box a=f.y[j]-f.y[i];
        if(a.h<=0)throw Failure{"time",j};
        return {std::max<Tick>(0,a.l),a.h};
    }
    void density(int j){
        if(j==15 || j==17 || j==20)return;
        bool device=j==16 || j==18;
        // The smooth device corrections (including J) have magnitude <2e-6.
        // Inertial load L/w^2 is nonnegative and <1e-9 for w>=1e-8.
        constexpr Tick tol=2001;
        Box desired=device?Box{-100000*S,tol}:point(0);
        if(device && f.w[j].l>=10)desired.l=-tol;
        Box residual=point(19*S);
        Box terms[N];int n=0;
        for(auto [i,c]:m.inc[j]){terms[n]=c*sq(gap(i,j));residual=residual+terms[n++];}
        if(empty(intersect(residual,desired)))throw Failure{"D",j};
        if(device && residual.h < -tol)bind(f.w[j],{0,10},"Dweight",j);
        n=0;
        for(auto [i,c]:m.inc[j]){
            Box s=divided(desired-rest(residual,terms[n++]),c);
            if(s.h<0)throw Failure{"Dgap",j};
            Box d=root(s);
            bind(f.y[i],f.y[j]-d,"Dgap",j);
            bind(f.y[j],f.y[i]+d,"Dgap",j);
        }
        // Combine the near-fixed ancestral clocks as a polynomial in one
        // shared clock before isolating any other squared gap.
        Box origin=point((f.y[j].l+f.y[j].h)/2),shift0=f.y[j]-origin;
        Box B0=point(0),C0=point(19*S),loose=point(0);int A0=0;
        for(auto [i,c]:m.inc[j]){
            if(f.y[i].h-f.y[i].l <= S/100){
                Box d=origin-f.y[i];A0+=c;B0=B0+c*d;C0=C0+c*sq(d);
            }else{terms[i]=c*sq(gap(i,j));loose=loose+terms[i];}
        }
        Box poly=A0*sq(shift0)+(2*B0)*shift0+C0;
        Box combined=poly+loose;
        if(empty(intersect(combined,desired)))throw Failure{"Dpoly",j};
        if(device && combined.h < -tol)bind(f.w[j],{0,10},"Dweight",j);
        // Freeze membership before contracting the variables in this loop.
        std::vector<Edge> uncertain;
        for(auto e:m.inc[j])if(f.y[e.j].h-f.y[e.j].l>S/100)uncertain.push_back(e);
        for(auto [i,c]:uncertain){
            Box s=divided(desired-rest(combined,terms[i]),c);
            if(s.h<0)throw Failure{"Dpoly",j};
            Box d=root(s);
            bind(f.y[i],f.y[j]-d,"Dpoly",j);
            bind(f.y[j],f.y[i]+d,"Dpoly",j);
        }
        // Complete the square around a point in the current clock interval.
        // A(shift)^2 + 2B(shift) + C = desired.
        if(device && f.w[j].l<10)return;
        Box center=point((f.y[j].l+f.y[j].h)/2);
        int A=0;Box B=point(0),C=point(19*S)-desired;
        for(auto [i,c]:m.inc[j]){
            Box h=center-f.y[i];A+=c;B=B+c*h;C=C+c*sq(h);
        }
        Box shift=f.y[j]-center;
        if(A==0){
            bind(f.y[j],center+linear(shift,2*B,-C),"Droot",j);
        }else{
            Box disc=sq(B)-A*C;
            if(disc.h<0)throw Failure{"Droot",j};
            Box r=root(disc);
            Box pos=intersect(shift,divided(-B+r,A));
            Box neg=intersect(shift,divided(-B-r,A));
            bind(f.y[j],center+hull(pos,neg),"Droot",j);
        }
    }
    void clock(int j){
        // G=sum_out c*w_k*(Y_k-Y_j) - w_j*sum_in c*(Y_j-Y_i).
        // Device terms only perturb 15..18 among free clocks.
        Box target=(j>=15 && j<=18)?Box{-10,10}:point(0);
        std::array<Box,N> terms{},factors{};
        Box incoming=point(0);
        for(auto [i,c]:m.inc[j])incoming=incoming+c*gap(i,j);
        terms[j]=f.w[j]*(-incoming);Box g=terms[j];
        for(auto [k,c]:m.out[j]){
            factors[k]=c*gap(j,k);terms[k]=f.w[k]*factors[k];g=g+terms[k];
        }
        if(empty(intersect(g,target)))throw Failure{"G",j};
        bind(f.w[j],linear(f.w[j],-incoming,target-rest(g,terms[j])),"Gweight",j);
        for(auto [k,c]:m.out[j])
            bind(f.w[k],linear(f.w[k],factors[k],target-rest(g,terms[k])),"Gweight",j);
        // An affine combination of collar terms reaches its extrema at
        // the endpoints of the shared central clock. Each endpoint uses
        // the whole collar box, so correlations in the inputs remain covered.
        Box left=point(0),right=point(0),other=point(0);
        for(auto [k,c]:m.out[j]){
            if(k>=7 && k<=10){
                left=left+(c*f.w[k])*(f.y[k]-point(f.y[j].l));
                right=right+(c*f.w[k])*(f.y[k]-point(f.y[j].h));
            }else{
                factors[k]=c*gap(j,k);terms[k]=f.w[k]*factors[k];other=other+terms[k];
            }
        }
        int total_c=0;Box offset=point(0);
        for(auto [i,c]:m.inc[j]){total_c+=c;offset=offset+c*f.y[i];}
        Box better=intersect(incoming,total_c*f.y[j]-offset);
        if(empty(better))throw Failure{"Gshared",j};
        Box contribution=(-better)*f.w[j],shared=hull(left,right)+other+contribution;
        if(empty(intersect(shared,target)))throw Failure{"Gshared",j};
        bind(f.w[j],linear(f.w[j],-better,target-rest(shared,contribution)),"Gshared",j);
        for(auto [k,c]:m.out[j])if(k<7 || k>10)
            bind(f.w[k],linear(f.w[k],factors[k],target-rest(shared,terms[k])),"Gshared",j);
        // Second enclosure of the same equation, affine in all clocks.
        // Centre time coordinates to reduce cancellation.
        Box center=point((f.y[j].l+f.y[j].h)/2),slope=point(0),sum=point(0);
        auto add=[&](int k,Box a){factors[k]=a;terms[k]=a*(f.y[k]-center);slope=slope+a;sum=sum+terms[k];};
        for(auto [i,c]:m.inc[j])add(i,c*f.w[j]);
        for(auto [k,c]:m.out[j])add(k,c*f.w[k]);
        Box own=(-slope)*(f.y[j]-center);sum=sum+own;
        if(empty(intersect(sum,target)))throw Failure{"Gaffine",j};
        auto constrain=[&](int k,Box a,Box term){
            Box shift=f.y[k]-center;
            bind(f.y[k],center+linear(shift,a,target-rest(sum,term)),"Gclock",j);
        };
        constrain(j,-slope,own);
        for(auto [i,c]:m.inc[j])constrain(i,factors[i],terms[i]);
        for(auto [k,c]:m.out[j])constrain(k,factors[k],terms[k]);
    }
    void run(int rounds){
        for(int t=0;t<rounds;++t){
            changed=false;chronology();
            if(reverse){
                for(int j:{20,19,18,17,16,15,14,13,12,11,6,5,4})if(!parent || j<19)density(j);
                for(int j:{15,17,18,16,19,20,4,5,6,11,12,13,14})if(!parent || j<19)clock(j);
            }else{
                for(int j:FREE)if(!parent || j<19)density(j);
                for(int j:{20,14,13,12,11,6,5,4,19,17,15,16,18})if(!parent || j<19)clock(j);
            }
            for(int j:FREE)if(j!=15 && j!=17 && j!=20 && (f.w[j].h<=0 || f.w[j].l>=S))
                throw Failure{"positive",j};
            if(!changed)break;
        }
    }
};
struct Audit{
    int leaves=0,boxes=0;
    std::map<std::pair<std::string,int>,int> terminal;
    Fields open{};
};
bool split_search(Test test,int depth,int budget,Audit& audit){
    ++audit.boxes;
    try{test.run(24);}
    catch(Failure e){++audit.leaves;++audit.terminal[{e.law,e.node}];return true;}
    if(depth==0 || audit.boxes>=budget){audit.open=test.f;return false;}
    int axis=-1;Tick cut=0;
    // Separate the inertial small-weight branch before solving for clocks.
    for(int j:{16,18})if(test.f.w[j].l<10 && test.f.w[j].h>10){axis=N+j;cut=10;break;}
    if(axis<0){
        double best=0.0;
        for(int j:FREE){
            for(int field=0;field<2;++field){
                Box x=field?test.f.w[j]:test.f.y[j];
                if(x.h-x.l<2)continue;
                double priority=1.0;
                if(!field && (j==19 || j==20))priority=2.0;
                if(field && (j==16 || j==18))priority=2.0;
                double score=priority*double(x.h-x.l);
                if(score>best){axis=j+N*field;cut=(x.l+x.h)/2;best=score;}
            }
        }
    }
    if(axis<0){audit.open=test.f;return false;}
    for(int side:{0,1}){
        Test child=test;Box& b=axis<N?child.f.y[axis]:child.f.w[axis-N];
        if(side==0)b.h=cut;else b.l=cut;
        if(!split_search(child,depth-1,budget,audit))return false;
    }
    return true;
}
int main(int argc,char** argv){
    int rounds=argc>1?std::stoi(argv[1]):10;
    int depth=argc>2?std::stoi(argv[2]):0,budget=argc>3?std::stoi(argv[3]):20000;
    int n;std::cin>>n;
    std::vector<std::pair<int,int>> order(n);
    for(auto& [a,b]:order)std::cin>>a>>b;
    Fields base;
    base.y.fill({-5*S,2*S});base.w.fill({0,S});
    for(int j:{15,17,20})base.w[j]=point(0);
    for(int a=0;a<8;++a){int j;std::cin>>j;std::cin>>base.y[j].l>>base.y[j].h>>base.w[j].l>>base.w[j].h;}
    std::array<Box,N> native{};
    for(int a=0;a<7;++a){int j;std::cin>>j>>native[j].l>>native[j].h;}
    Box window;std::cin>>window.l>>window.h;base.y[19]=base.y[20]=window;
    std::cin>>n;
    for(int row=0;row<n;++row){
        Row r;for(int& a:r)std::cin>>a;
        Model m(order,r);Test test{m,base};
        test.reverse=argc>4 && std::string(argv[4])=="reverse";
        for(int j:DUST)if(!(m.past[j]&((1<<19)|(1<<20))))test.f.y[j]=native[j];
        try{
            test.run(rounds);
            if(depth){
                Audit audit;
                bool closed=split_search(test,depth,budget,audit);
                std::cout<<(closed?"split":"OPEN")<<' '<<audit.leaves<<' '<<audit.boxes;
                if(closed){
                    assert(audit.boxes==2*audit.leaves-1);
                    for(const auto& [key,count]:audit.terminal)std::cout<<' '<<key.first<<'.'<<key.second<<'='<<count;
                }else{
                    for(int j:{15,16,17,18,19,20})
                        std::cout<<' '<<audit.open.y[j].l<<' '<<audit.open.y[j].h;
                    for(int j:{16,18,19})
                        std::cout<<' '<<audit.open.w[j].l<<' '<<audit.open.w[j].h;
                }
                std::cout<<'\n';
            }else std::cout<<"OPEN -1\n";
        }catch(Failure v){std::cout<<v.law<<' '<<v.node<<'\n';}
    }
    assert(std::cin && std::cout);
    return 0;
}
