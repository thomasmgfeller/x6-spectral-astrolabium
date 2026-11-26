// The archived implementation supplies the order, layer coefficients and integer arithmetic.
#define main archived_n22_main
#include "feldtest.cpp"
#undef main

constexpr int K=11, axis_id[K]={15,16,17,18,19,20,21,16,18,19,21};
constexpr int pos[4]={16,18,19,21};
using Vec=std::array<Box,K>;
using Mat=std::array<Vec,K>;
struct Results {long nodes=0,closed=0,open=0; int depth=0;};
Box& axis(Fields& f,int k){return k<7?f.y[axis_id[k]]:f.w[axis_id[k]];}
Tick middle(Box x){return (x.l+x.h)/2;}
Box halfsegment(Box x,Box m){return divided(x+m,2);}
// These are the four density and seven clock residuals, in this order.
// The collar is an interval parameter, fixed along each segment in the free fields.
void equations(const Model& model, const Fields& at, const Fields& half,
               int small, Vec& r, Mat& jac){
    for(int p=0;p<4;++p){
        int j=pos[p];
        if(p<2 && (small & (1<<p))){
            r[p]=at.w[j]-Box{0,10};jac[p][7+p]=point(S);continue;
        }
        r[p]=point(19*S)-(p<2?Box{-2001,2001}:point(0));
        for(auto [i,c]:model.inc[j]){
            r[p]=r[p]+c*sq(at.y[j]-at.y[i]);
            Box d=(2*c)*(half.y[j]-half.y[i]);
            jac[p][j-15]=jac[p][j-15]+d;
            if(i>=15)jac[p][i-15]=jac[p][i-15]-d;
        }
    }
    for(int j=15;j<=21;++j){
        const int row=j-15+4;
        r[row]=j<=18?Box{-10,10}:point(0);
        auto edge=[&](int a,int b,int c){
            r[row]=r[row]+(c*at.w[b])*(at.y[b]-at.y[a]);
            Box v=c*half.w[b];
            if(b>=15)jac[row][b-15]=jac[row][b-15]+v;
            if(a>=15)jac[row][a-15]=jac[row][a-15]-v;
            for(int k=0;k<4;++k)if(b==pos[k])
                jac[row][7+k]=jac[row][7+k]+c*(half.y[b]-half.y[a]);
        };
        for(auto [i,c]:model.inc[j])edge(i,j,-c);
        for(auto [b,c]:model.out[j])edge(j,b,c);
    }
}
void combined(Test& t,int small){
    Fields at=t.f, half=t.f;
    for(int k=0;k<K;++k){
        Box b=axis(t.f,k);axis(at,k)=point(middle(b));axis(half,k)=halfsegment(b,axis(at,k));
    }
    Vec r{};Mat jac{};
    // All residuals have degree at most two in the free fields. The derivative
    // at the segment midpoint is the exact secant slope along that segment.
    equations(t.m,at,half,small,r,jac);
    // Approximate inverse chooses rational row combinations only.
    double a[K][2*K]{};
    for(int i=0;i<K;++i)for(int j=0;j<K;++j){a[i][j]=double(middle(jac[i][j]))/S;a[i][K+j]=(i==j);}
    for(int j=0;j<K;++j){
        int h=j;for(int i=j+1;i<K;++i)if(std::abs(a[i][j])>std::abs(a[h][j]))h=i;
        if(std::abs(a[h][j])<1e-12)return;
        for(int k=0;k<2*K;++k)std::swap(a[h][k],a[j][k]);
        double d=a[j][j];for(double& v:a[j])v/=d;
        for(int i=0;i<K;++i)if(i!=j){d=a[i][j];for(int k=0;k<2*K;++k)a[i][k]-=d*a[j][k];}
    }
    for(int i=0;i<K;++i){
        double norm=0;for(int k=0;k<K;++k)norm=std::max(norm,std::abs(a[i][K+k]));
        Vec g{};Box f{};
        for(int k=0;k<K;++k){
            int lambda=std::lround(32768*a[i][K+k]/norm);
            if(!lambda)continue;
            f=f+lambda*r[k];
            for(int j=0;j<K;++j)g[j]=g[j]+lambda*jac[k][j];
        }
        f=divided(f,32768);
        for(int j=0;j<K;++j){
            g[j]=divided(g[j],32768);
            if(j!=i)f=f+g[j]*(axis(t.f,j)-axis(at,j));
        }
        t.bind(axis(t.f,i),axis(at,i)+linear(axis(t.f,i)-axis(at,i),g[i],-f),"linear",i);
        if(!contains0(f+g[i]*(axis(t.f,i)-axis(at,i))))throw Failure{"residual",i};
    }
}
void search(Test t,int small,Results& s,int depth,int maxdepth,int budget){
    ++s.nodes;s.depth=std::max(s.depth,depth);
    try{
        for(int it=0;it<15;++it){
            t.changed=false;t.chronology();
            for(int j:pos)t.density(j);
            for(int j:{20,21,19,17,15,16,18})t.clock(j);
            if(it==1 || it==4 || it==9 || !t.changed)combined(t,small);
            if(!t.changed)break;
        }
    }catch(Failure){++s.closed;return;}
    int best=-1;double score=0;
    for(int k=0;k<K;++k){
        Box b=axis(t.f,k);double v=double(b.h-b.l);
        if(b.h-b.l>=2 && v>score){best=k;score=v;}
    }
    if(depth>=maxdepth || best<0 || s.nodes>=budget){
        if(s.open==0){
            std::cerr<<"first open";
            for(int k=0;k<K;++k){Box v=axis(t.f,k);std::cerr<<" "<<v.l<<":"<<v.h;}
            std::cerr<<"\n";
        }
        ++s.open;return;
    }
    Tick mid=middle(axis(t.f,best));Test child=t;
    axis(child.f,best).h=mid;axis(t.f,best).l=mid;
    search(child,small,s,depth+1,maxdepth,budget);
    search(t,small,s,depth+1,maxdepth,budget);
}
int main(int argc,char** argv){
    assert(argc==4 || argc==5);bool control=argc==5;int depth=std::stoi(argv[1]),budget=std::stoi(argv[2]),sector=std::stoi(argv[3]);
    assert(depth>=0 && budget>0 && sector>=0 && sector<=3);
    int n;std::cin>>n;std::vector<std::pair<int,int>> order(n);
    for(auto& [a,b]:order)std::cin>>a>>b;
    Fields base;base.y.fill({-5*S,2*S});base.w.fill({0,S});
    for(int j:{15,17,20})base.w[j]=point(0);
    for(int a=0;a<8;++a){int j;std::cin>>j;std::cin>>base.y[j].l>>base.y[j].h>>base.w[j].l>>base.w[j].h;}
    for(int a=0;a<7;++a){int j;Box dummy;std::cin>>j>>dummy.l>>dummy.h;}
    Box W;std::cin>>W.l>>W.h;base.y[19]=base.y[20]=W;
    std::cin>>n;
    for(int i=0;i<n;++i){
        Row r;for(int& a:r)std::cin>>a;
        Model m(order,r,false,true);Test t{m,base};
        for(int j:{15,16,17,18,19,20,21}){
            assert((m.past[j]&1) && (m.future[j]&(1<<7)));
            for(auto e:m.inc[j])assert(e.j>=15 || e.j<=3);
            for(auto e:m.out[j])assert(e.j>=15 || (e.j>=7 && e.j<=10));
        }
        for(int p=0;p<2;++p)t.f.w[pos[p]]=(sector&(1<<p))?Box{0,10}:Box{10,S};
        if(control)for(int k=0;k<K;++k){Box v;std::cin>>v.l>>v.h;axis(t.f,k)=v;}
        if(control && std::string(argv[4])=="algebra"){
            Vec values{};Mat jac{};
            equations(m,t.f,t.f,sector,values,jac);
            for(int i=0;i<K;++i){
                std::cout<<values[i].l<<' '<<values[i].h;
                for(Box b:jac[i])std::cout<<' '<<b.l<<' '<<b.h;
                std::cout<<'\n';
            }
            continue;
        }
        Results s;search(t,sector,s,0,depth,budget);
        assert(s.nodes==2*(s.closed+s.open)-1);
        std::cout<<r[1]<<' '<<sector<<' '<<s.nodes<<' '<<s.closed<<' '<<s.open<<' '<<s.depth<<std::endl;
    }
    assert(std::cin && std::cout);
}
