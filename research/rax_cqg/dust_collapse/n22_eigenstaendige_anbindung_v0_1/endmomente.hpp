// The unbounded terminal clock can be eliminated exactly when sum(c_i)=0.
void terminal(Test& t) {
    auto& f=t.f;
    const auto& m=t.m;
    assert(m.occupied && m.out[21].empty() && m.past[21]&(1<<20));
    std::array<int,N> coeff{};
    int mass=0;
    for(auto [i,c]:m.inc[21]) {coeff[i]=c; mass+=c;}
    assert(mass==0 && coeff[20]==1);
    for(int round=0;round<8;++round) {
        t.changed=false;
        // Y21 is a placeholder later than every old event. No old equation
        // below reads it, and chronology() can only constrain the old clocks.
        t.chronology();
        for(int j:FREE) if(j!=21) t.density(j);
        for(int j:FREE) if(j!=21 && coeff[j]==0) t.clock(j);
        Box moment=point(0), square=point(19*S);
        std::array<Box,N> first{},second{};
        for(auto [i,c]:m.inc[21]) {
            first[i]=c*f.y[i]; second[i]=c*sq(f.y[i]);
            moment=moment+first[i];square=square+second[i];
        }
        if(!contains0(moment) || !contains0(square)) throw Failure{"moments",21};
        for(auto [i,c]:m.inc[21]) {
            t.bind(f.y[i],divided(-rest(moment,first[i]),c),"moment",i);
            Box v=divided(-rest(square,second[i]),c);
            if(v.h<0) throw Failure{"square",i};
            Box r=root(v);
            t.bind(f.y[i],hull(intersect(f.y[i],r),intersect(f.y[i],-r)),"square",i);
        }
        // G_j^old - c_j G_20^old + c_j w21 (Y20-Yj) = 0.
        // This also holds for free dust clocks. Device corrections at 15..18
        // are enclosed by +/- 10 ticks. G20 has no device correction.
        std::array<Box,N> g{};
        for(int j:FREE) if(j!=21) {
            for(auto [k,c]:m.out[j]) if(k!=21)
                g[j]=g[j]+(c*f.w[k])*(f.y[k]-f.y[j]);
            for(auto [i,c]:m.inc[j]) g[j]=g[j]-(c*f.w[j])*(f.y[j]-f.y[i]);
        }
        if(g[20].l>=0) throw Failure{"positive terminal gap",20};
        for(int j:FREE) if(j!=21 && j!=20 && coeff[j]!=0) {
            Box tol=(j>=15 && j<=18)?Box{-10,10}:point(0);
            Box rhs=tol-g[j]+coeff[j]*g[20];
            Box factor=coeff[j]*(f.y[20]-f.y[j]);
            t.bind(f.w[21],linear(f.w[21],factor,rhs),"projected G",j);
            if(empty(intersect(f.w[21]*factor,rhs))) throw Failure{"projected G",j};
        }
        if(!t.changed) break;
    }
}
