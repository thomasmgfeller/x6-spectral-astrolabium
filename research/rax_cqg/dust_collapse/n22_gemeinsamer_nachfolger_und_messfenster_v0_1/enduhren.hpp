// Y21 is unbounded if its linear coefficient in the terminal clock equation
// vanishes. Work only with necessary equations that are independent of Y21.
void terminal(Test& t) {
    const auto& m=t.m;
    auto& f=t.f;
    assert(m.occupied && m.future[21]==0);
    std::array<int,N> coeff{};
    int mass=0;
    for (auto [i,c]:m.inc[21]) {coeff[i]=c; mass+=c;}
    assert(mass==0);
    for (int round=0;round<8;++round) {
        t.changed=false;
        t.chronology();
        for (int j:FREE) if (j!=21) {
            t.density(j);
            if (coeff[j]==0) t.clock(j);
        }
        Box linear_moment=point(0), square_moment=point(19*S);
        for (auto [i,c]:m.inc[21]) {
            linear_moment=linear_moment+c*f.y[i];
            square_moment=square_moment+c*sq(f.y[i]);
        }
        if (!contains0(linear_moment) || !contains0(square_moment))
            throw Failure{"terminal moments",21};
        // If a free measurement sees the terminal event, its old gradient
        // must have sign opposite to its nonzero coefficient.
        for (int j:{19,20}) if (coeff[j]) {
            Box old=point(0);
            for (auto [k,c]:m.out[j]) if (k!=21)
                old=old+(c*f.w[k])*(f.y[k]-f.y[j]);
            for (auto [i,c]:m.inc[j])
                old=old-(c*f.w[j])*(f.y[j]-f.y[i]);
            if ((coeff[j]>0 && old.l>=0) || (coeff[j]<0 && old.h<=0))
                throw Failure{"positive terminal gap",j};
        }
        if (!t.changed) break;
    }
}
