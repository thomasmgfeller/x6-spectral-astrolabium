/* SPDX-License-Identifier: Apache-2.0
 * Fixed-budget Minkowski proper-time demonstrator. No adaptive stopping.
 * The estimator receives counts, dimension and an external scale, not truth.
 */
(function (root) {
  'use strict';
  const VERSION = 'x6.proper-time-lab/1.1';
  const SAMPLER_POLICY = 'strict-interior-rejection/1';
  const MAX_POINT_ATTEMPTS = 128;
  function rng(seed) {
    if (!Number.isInteger(seed) || seed < 0 || seed > 4294967295) throw Error('Seed muss eine ganze Zahl von 0 bis 4294967295 sein.');
    let state = seed >>> 0;
    return () => {
      state = (state + 0x6D2B79F5) >>> 0;
      let x = Math.imul(state ^ (state >>> 15), 1 | state);
      x ^= x + Math.imul(x ^ (x >>> 7), 61 | x);
      return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
    };
  }
  function normal(random) {
    const u = Math.max(0.5 / 4294967296, random());
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * random());
  }
  function insideDiamond(point,theta=1) {
    return Math.abs(point[0])+Math.hypot(...point.slice(1))<theta/2;
  }
  // Preserve the PRNG and the original transform for every accepted candidate.
  // Reject endpoints/rounded boundary candidates instead of moving their mass
  // to an arbitrary interior point. Finite PRNG independence is not assumed.
  function samplePoint(random, d) {
    if (typeof random !== 'function' || ![2,3,4].includes(d)) throw Error('Ungültige Punktquelle oder Dimension.');
    const unit = () => {
      const u=random();
      if (!Number.isFinite(u) || u<0 || u>=1) throw Error('Zufallswert außerhalb [0,1).');
      return u;
    };
    const rejected={zeroTemporalUniform:0, invalidDirection:0, outsideSupport:0};
    for (let attempt=1; attempt<=MAX_POINT_ATTEMPTS; attempt++) {
      const u=unit();
      if (u===0) {rejected.zeroTemporalUniform++;continue;}
      const A=.5*u**(1/d), t=(unit()<.5 ? -1 : 1)*(.5-A);
      const v=Array.from({length:d-1},()=>normal(unit)), norm=Math.hypot(...v);
      if (!(norm>0) || !Number.isFinite(norm)) {rejected.invalidDirection++;continue;}
      const r=A*unit()**(1/(d-1)), point=[t,...v.map(x=>x*r/norm)];
      if (!point.every(Number.isFinite) || !insideDiamond(point)) {
        rejected.outsideSupport++;continue;
      }
      return {point,attempts:attempt,rejected};
    }
    throw Error('Sampler: nach 128 Versuchen kein strikt innerer Punkt. Keine Ausgabe freigegeben.');
  }
  function check(m, d, alpha = .05, T = 1) {
    if (!Number.isInteger(m) || m < 1 || m > 16384) throw Error('m muss zwischen 1 und 16384 liegen.');
    if (![2, 3, 4].includes(d)) throw Error('Unterstützte Raumzeitdimensionen: 2, 3, 4.');
    if (!(alpha > 0 && alpha < 1) || !Number.isFinite(alpha)) throw Error('Ungültiges Konfidenzniveau.');
    if (!(T > 0 && T <= 1e6) || !Number.isFinite(T)) throw Error('T muss positiv und höchstens 1000000 sein.');
  }
  // Lanczos log-gamma and a continued fraction for the regularized incomplete beta.
  function logGamma(z) {
    const c = [676.5203681218851, -1259.1392167224028, 771.32342877765313,
      -176.61502916214059, 12.507343278686905, -.13857109526572012,
      9.984369578019572e-6, 1.5056327351493116e-7];
    if (z < .5) return Math.log(Math.PI) - Math.log(Math.sin(Math.PI*z)) - logGamma(1-z);
    z -= 1;
    let x = .99999999999980993;
    c.forEach((v, i) => { x += v / (z+i+1); });
    const t = z+7.5;
    return .9189385332046727+(z+.5)*Math.log(t)-t+Math.log(x);
  }
  function betaFraction(a, b, x) {
    const tiny = 1e-300;
    const nonzero = v => Math.abs(v) < tiny ? tiny : v;
    let c = 1, d = 1/nonzero(1-(a+b)*x/(a+1)), h = d;
    for (let j=1; j<=600; j++) {
      let aa = j*(b-j)*x/((a+2*j-1)*(a+2*j));
      d = 1/nonzero(1+aa*d); c = nonzero(1+aa/c); h *= d*c;
      aa = -(a+j)*(a+b+j)*x/((a+2*j)*(a+2*j+1));
      d = 1/nonzero(1+aa*d); c = nonzero(1+aa/c);
      const delta = d*c; h *= delta;
      if (Math.abs(delta-1) < 3e-14) return h;
    }
    throw Error('Beta-Auswertung konvergiert nicht. Keine Ausgabe freigegeben.');
  }
  function betaCDF(x, a, b) {
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    const front = Math.exp(logGamma(a+b)-logGamma(a)-logGamma(b)+a*Math.log(x)+b*Math.log1p(-x));
    return x < (a+1)/(a+b+2) ? front*betaFraction(a,b,x)/a : 1-front*betaFraction(b,a,1-x)/b;
  }
  function betaInverse(p, a, b) {
    let lo=0, hi=1;
    for (let i=0; i<75; i++) {
      const mid=(lo+hi)/2;
      if (betaCDF(mid,a,b) < p) lo=mid; else hi=mid;
    }
    return (lo+hi)/2;
  }
  function infer(k, m, d, alpha=.05, T=1) {
    check(m,d,alpha,T);
    if (!Number.isInteger(k) || k < 0 || k > m) throw Error('K muss eine ganze Zahl zwischen 0 und m sein.');
    const aLow = k===0 ? 0 : (k===m ? Math.exp(Math.log(alpha/2)/m) : betaInverse(alpha/2,k,m-k+1));
    const aHigh = k===m ? 1 : (k===0 ? -Math.expm1(Math.log(alpha/2)/m) : betaInverse(1-alpha/2,k+1,m-k));
    return {k,m,d,alpha,T,thetaHat:(k/m)**(1/d),aLow,aHigh,
      estimate:T*(k/m)**(1/d),lower:T*aLow**(1/d),upper:T*aHigh**(1/d)};
  }
  function cloud({m,d,theta,seed,T=1}) {
    check(m,d,.05,T);
    if (!(theta > 0 && theta < 1)) throw Error('theta muss zwischen 0 und 1 liegen.');
    const random=rng(seed), points=[], inside=[];
    const sampling={policy:SAMPLER_POLICY,maxAttemptsPerPoint:MAX_POINT_ATTEMPTS,
      attempts:0,rejected:{zeroTemporalUniform:0,invalidDirection:0,outsideSupport:0}};
    for (let i=0;i<m;i++) {
      const candidate=samplePoint(random,d),p=candidate.point;
      sampling.attempts+=candidate.attempts;
      for (const key of Object.keys(sampling.rejected)) sampling.rejected[key]+=candidate.rejected[key];
      points.push(p);
      inside.push(insideDiamond(p,theta));
    }
    const k=inside.reduce((s,b)=>s+Number(b),0);
    return {points,inside,sampling,...infer(k,m,d,.05,T)};
  }
  function precedes(a,b) {
    const dt=b[0]-a[0];
    return dt>0 && dt*dt>a.slice(1).reduce((s,x,j)=>s+(b[j+1]-x)**2,0);
  }
  function longestChain(points, inside) {
    const indices=points.map((_,i)=>i).filter(i=>inside[i]).sort((a,b)=>points[a][0]-points[b][0]);
    if (indices.length>256) return {status:'OUTSIDE_DISPLAY_BUDGET',height:null,path:[]};
    const dp=indices.map(()=>1), previous=indices.map(()=>-1);
    for (let j=0;j<indices.length;j++) for (let i=0;i<j;i++) {
      if (precedes(points[indices[i]],points[indices[j]]) && dp[i]+1>dp[j]) {dp[j]=dp[i]+1;previous[j]=i;}
    }
    const height=indices.length ? Math.max(...dp) : 0, path=[];
    let j=dp.indexOf(height);
    while(j>=0) {path.push(indices[j]);j=previous[j];}
    return {status:'COMPUTED',height,path:path.reverse()};
  }
  function binomial(m,p,random) {
    let k=0;
    for(let i=0;i<m;i++) if(random()<p) k++;
    return k;
  }
  function exactMoments(m,d,theta) {
    check(m,d);
    if (!(theta>0 && theta<1)) throw Error('Ungültiges theta.');
    const p=theta**d, mode=Math.floor((m+1)*p), weights=new Float64Array(m+1);
    weights[mode]=1;
    for(let k=mode;k<m;k++) weights[k+1]=weights[k]*(m-k)/(k+1)*p/(1-p);
    for(let k=mode;k>0;k--) weights[k-1]=weights[k]*k/(m-k+1)*(1-p)/p;
    let mass=0,bias=0,mse=0;
    weights.forEach((w,k)=>{const e=(k/m)**(1/d)-theta;mass+=w;bias+=w*e;mse+=w*e*e;});
    return {bias:bias/mass,rmse:Math.sqrt(mse/mass),expectedK:m*p,zeroProbability:Math.exp(m*Math.log1p(-p))};
  }
  const api={VERSION,SAMPLER_POLICY,insideDiamond,samplePoint,rng,infer,cloud,precedes,longestChain,binomial,exactMoments};
  if (typeof module!=='undefined' && module.exports) module.exports=api;
  else root.ProperTime=api;
})(typeof globalThis!=='undefined' ? globalThis : this);
