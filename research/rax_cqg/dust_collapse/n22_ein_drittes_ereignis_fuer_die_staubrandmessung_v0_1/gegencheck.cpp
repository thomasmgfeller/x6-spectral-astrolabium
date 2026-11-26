// Compare C++ layer counts to an independent transitive closure. Also replay
// the field contractor in narrow boxes containing certified off-window roots.
#define main study_entry_point
#include "feldtest.cpp"
#undef main
int main(){
    int edges;
    std::cin>>edges;
    std::vector<std::pair<int,int>> old(edges);
    for(auto& [i,j]:old)std::cin>>i>>j;
    char mode,family,sector;
    while(std::cin>>mode>>family>>sector){
        Row row;for(int& x:row)std::cin>>x;
        Model m(old,row,family=='A',sector=='+');
        if(mode=='C'){
            for(int i=0;i<N;++i){
                std::array<int,N> weights{};
                for(auto [j,v]:m.out[i])weights[j]=v;
                for(int j=0;j<N;++j)std::cout<<weights[j]<<' ';
            }
            std::cout<<'\n';
        }else if(mode=='W'){
            Fields f;
            for(int j=0;j<N;++j)std::cin>>f.y[j].l>>f.y[j].h>>f.w[j].l>>f.w[j].h;
            for(bool rev:{false,true}){
                Test t{m,f};t.reverse=rev;
                try{t.run(32);}catch(Failure err){std::cerr<<err.law<<' '<<err.node<<'\n';return 1;}
            }
            std::cout<<"PASS\n";
        }else return 2;
    }
}
