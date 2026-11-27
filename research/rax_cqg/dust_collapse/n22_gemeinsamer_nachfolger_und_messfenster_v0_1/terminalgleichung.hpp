// G21 / w21 for a positive terminal receiver. The linear row has the same
// zero set as G21 on this sector and stays informative for tiny weights.
void equations(const Model& m, const Fields& at, const Fields& half, int small, Vec& r, Mat& jac) {
    original_residuals(m,at,half,small,r,jac);
    if (!m.occupied || m.future[21]) return;
    Box linear_sum=point(0);
    jac[10]={};
    for (auto [i,c]:m.inc[21]) {
        linear_sum=linear_sum+c*(at.y[i]-at.y[21]);
        if (i>=15) jac[10][i-15]=jac[10][i-15]+point(c*S);
        jac[10][6]=jac[10][6]-point(c*S);
    }
    r[10]=linear_sum;
}

void twins(Test& t) {
    Fields& f=t.f;
    Box scale=-9*f.w[7]+16*f.w[8]-8*f.w[9]+f.w[18]+f.w[21];
    Box gap=f.y[17]-f.y[20], tol{-10,10};
    if (empty(intersect(scale*gap,tol))) throw Failure{"twin clocks",17};
    gap=linear(gap,scale,tol);
    t.bind(f.y[17],f.y[20]+gap,"twin clocks",17);
    t.bind(f.y[20],f.y[17]-gap,"twin clocks",20);
    if (f.w[18].l<10) return;
    Box slope=18*(f.y[15]-f.y[2])-2*(f.y[16]-f.y[2])-point(16*S);
    Box shift=f.y[18]-f.y[19];
    Box corr{-2001,2001};
    Box left=sq(f.y[18]-f.y[17]),right=sq(f.y[18]-f.y[20]);
    if (empty(intersect(slope*shift+left+right,corr))) throw Failure{"paired density",18};
    shift=linear(shift,slope,corr-left-right);
    t.bind(f.y[18],f.y[19]+shift,"paired density",18);
    t.bind(f.y[19],f.y[18]-shift,"paired density",19);
}
