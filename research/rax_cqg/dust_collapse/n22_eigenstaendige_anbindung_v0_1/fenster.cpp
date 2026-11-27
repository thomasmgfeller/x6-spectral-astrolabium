#include "reduktion.hpp"  // Archived field equations, exact interval arithmetic and combined()
#include "endmomente.hpp"

struct Count { int nodes=0, closed=0, open=0, depth=0; };

void cover(Test test, int small, int depth, int budget, Count& stats, bool moments) {
    ++stats.nodes;
    stats.depth=std::max(stats.depth,depth);
    try {
        if (moments) terminal(test);
        else for (int i=0;i<8;++i) {
            test.changed=false;
            test.run(3);
            // Dust fields are interval parameters of the 11 device equations here.
            // Keep the full dust equations in Test::run above.
            combined(test,small);
            if (!test.changed) break;
        }
    } catch (Failure) { ++stats.closed; return; }
    int axis=-1; Tick width=0;
    for (int i=0;i<K;++i) {
        Box b=::axis(test.f,i);
        if (b.h-b.l>width) {axis=i; width=b.h-b.l;}
    }
    if (width<2 || depth>=76 || stats.nodes>=budget) {++stats.open;return;}
    Test child=test;
    Tick cut=middle(::axis(test.f,axis));
    ::axis(child.f,axis).h=cut;
    ::axis(test.f,axis).l=cut;
    cover(child,small,depth+1,budget,stats,moments);
    cover(test,small,depth+1,budget,stats,moments);
}

int main(int argc,char** argv) {
    assert(argc==5);
    const std::string kind=argv[1],mode=argv[4];
    bool positive=kind.back()=='+',before=kind.front()=='A';
    int small=std::stoi(argv[2]),budget=std::stoi(argv[3]),n;
    assert((kind=="A+"||kind=="A0"||kind=="B+"||kind=="B0") && small>=0 && small<4 && budget>=1);
    std::cin>>n;
    std::vector<std::pair<int,int>> edges(n);
    for (auto& [a,b]:edges) std::cin>>a>>b;
    Model m(edges,Row{},before,positive);
    Fields f;
    for (int j=0;j<22;++j) {
        std::cin>>f.y[j].l>>f.y[j].h>>f.w[j].l>>f.w[j].h;
        assert(!empty(f.y[j]) && !empty(f.w[j]));
    }
    assert(std::cin && (positive || (f.w[21].l==0 && f.w[21].h==0)));
    Test t{m,f};
    if (mode=="order") {
        for (int j=0;j<22;++j) for (auto [i,c]:m.inc[j]) std::cout<<i<<' '<<j<<' '<<c<<'\n';
    } else if (mode=="algebra") {
        Vec residual{};Mat jac{};
        equations(m,t.f,t.f,small,residual,jac);
        for (int i=0;i<K;++i) {
            std::cout<<residual[i].l<<' '<<residual[i].h;
            for (Box v:jac[i]) std::cout<<' '<<v.l<<' '<<v.h;
            std::cout<<'\n';
        }
    } else {
        assert(mode=="tree" || mode=="control" || mode=="moments");
        if (mode!="control") {
            for(int k=0;k<2;++k) t.f.w[pos[k]]=(small&(1<<k))?Box{0,10}:Box{10,S};
        }
        Count count;
        cover(t,small,0,budget,count,mode=="moments");
        assert(count.nodes==2*(count.closed+count.open)-1);
        std::cout<<count.nodes<<' '<<count.closed<<' '<<count.open<<' '<<count.depth<<'\n';
    }
}
