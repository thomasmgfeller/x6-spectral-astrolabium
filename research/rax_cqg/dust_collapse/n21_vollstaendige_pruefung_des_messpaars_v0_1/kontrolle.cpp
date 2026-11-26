// Additional entry point for stationary-parent and interval arithmetic controls.
#define main register_main
#include "feldtest.cpp"
#undef main
int main(){
    char mode;
    while(std::cin>>mode){
        if(mode=='P'){
            int n;std::cin>>n;
            std::vector<std::pair<int,int>> order(n);
            for(auto& [a,b]:order)std::cin>>a>>b;
            Fields actual;
            actual.y.fill(point(0));actual.w.fill({0,S});
            for(int j=0;j<19;++j)std::cin>>actual.y[j].l>>actual.y[j].h>>actual.w[j].l>>actual.w[j].h;
            Model m(order,Row{});
            for(bool r:{false,true}){
                Test t{m,actual};t.parent=true;t.reverse=r;
                try{t.run(48);}catch(Failure v){std::cerr<<v.law<<' '<<v.node<<'\n';return 1;}
            }
            std::cout<<"parent accepted\n";
        }else if(mode=='I'){
            Box a,b;std::cin>>a.l>>a.h>>b.l>>b.h;
            auto out=[](Box x){std::cout<<' '<<x.l<<' '<<x.h;};
            out(a*b);out(sq(a));out(divided(a,-9));out(root(sq(a)));
            out(linear({-10*S,10*S},b,a));std::cout<<'\n';
        }else{return 2;}
    }
    return 0;
}
