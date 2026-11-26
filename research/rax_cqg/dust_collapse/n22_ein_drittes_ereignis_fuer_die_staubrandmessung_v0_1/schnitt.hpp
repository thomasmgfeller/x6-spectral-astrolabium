// Sums of free clock equations across cuts of the order. Terms internal
// to each cut cancel before interval evaluation. No threshold for w21.
void cut(unsigned subset){
    std::array<Box,N> coeff{},terms{},center_clock{};
    std::array<int,N> incoming{};
    int noisy=__builtin_popcount(subset & ((1u<<15)|(1u<<16)|(1u<<17)|(1u<<18)));
    Box target={-10*noisy,10*noisy},total=point(0);
    for(int j=0;j<N;++j){
        Box part=point(0),offset=point(0);
        int aj=(subset>>j)&1;
        for(auto [i,c]:m.inc[j]){
            int v=c*(int((subset>>i)&1)-aj);
            if(!v)continue;
            incoming[j]+=v;
            offset=offset+v*f.y[i];part=part+v*gap(i,j);
        }
        coeff[j]=intersect(part,incoming[j]*f.y[j]-offset);
        if(empty(coeff[j]))throw Failure{"cut",j};
        terms[j]=coeff[j]*f.w[j];total=total+terms[j];
    }
    if(empty(intersect(total,target)))throw Failure{"cut",static_cast<int>(subset)};
    for(int j=0;j<N;++j){
        if(f.w[j].l<f.w[j].h)bind(f.w[j],linear(f.w[j],coeff[j],target-rest(total,terms[j])),"cutW",j);
        center_clock[j]=incoming[j]*f.w[j];
    }
    for(int j=0;j<N;++j){
        int aj=(subset>>j)&1;
        for(auto [i,c]:m.inc[j]){
            int v=c*(int((subset>>i)&1)-aj);
            if(v)center_clock[i]=center_clock[i]-v*f.w[j];
        }
    }
    // Evaluate the mixed bilinear expression at y midpoint, keeping w
    // as interval variables; the exact first derivatives in y handle offsets.
    Box centered=point(0);
    std::array<Box,N> mid{},errors{};
    for(int j=0;j<N;++j)mid[j]=point((f.y[j].l+f.y[j].h)/2);
    for(int j=0;j<N;++j){
        int aj=(subset>>j)&1;Box v=point(0);
        for(auto [i,c]:m.inc[j]){
            int s=c*(int((subset>>i)&1)-aj);
            if(s)v=v+s*(mid[j]-mid[i]);
        }
        errors[j]=center_clock[j]*(f.y[j]-mid[j]);
        centered=centered+v*f.w[j]+errors[j];
    }
    if(empty(intersect(centered,target)))throw Failure{"cutY",static_cast<int>(subset)};
    for(int j:FREE)
        bind(f.y[j],mid[j]+linear(f.y[j]-mid[j],center_clock[j],target-rest(centered,errors[j])),"cutY",j);
}
void joint(){
    constexpr unsigned pair=(1u<<19)|(1u<<20)|(1u<<21);
    constexpr unsigned device=(1u<<15)|(1u<<16)|(1u<<17)|(1u<<18);
    constexpr unsigned dust=(1u<<4)|(1u<<5)|(1u<<6)|(1u<<11)|(1u<<12)|(1u<<13)|(1u<<14);
    for(unsigned group:{(1u<<20)|(1u<<21),(1u<<19)|(1u<<21),
                        (1u<<17)|(1u<<18),device,device|pair,dust|device|pair})
        cut(group);
}
