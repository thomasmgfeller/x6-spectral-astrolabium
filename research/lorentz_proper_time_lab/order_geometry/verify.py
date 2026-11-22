"""Cross-check the strict-order kernel and the finite calibration fixtures."""
import itertools
import json
import subprocess
from fractions import Fraction

from reference import HERE, analyse, lis_counts, mm_grid


def main():
    rng_cases = []
    # All labelled forward-edge DAGs on four nodes, including transitive inputs.
    possible = list(itertools.combinations(range(4),2))
    for mask in range(1 << len(possible)):
        edges = [e for i,e in enumerate(possible) if mask & (1 << i)]
        rng_cases.append(dict(nodes=[3,1,0,2],edges=edges))
    js = r"""
      const O=require('./order.js'), bank=require('./reference.json'), assert=require('node:assert/strict');
      const graphs=JSON.parse(require('node:fs').readFileSync(0,'utf8'));
      const count=(g,ep=null)=>O.analyse(O.graphOrder(g),ep);
      for (const [kind,r,h,l] of [['n15',93,12,[15,15,15,14]],['minimal',98,12,[16,16,16,15]],
            ['long',101,12,[16,16,16,15]],['all',108,13,[16,16,16,15]]]) {
        const s=count(O.dust(kind));assert.deepEqual([s.pairs,s.height,s.layers],[r,h,l]);
        assert.equal(s.covers.length,s.layers[0]);assert.equal(s.path.length,s.height);
        const restored=count({nodes:s.ids,edges:s.covers.map(e=>e.map(i=>s.ids[i]))});
        assert.deepEqual(restored.matrix,s.matrix);
      }
      const s=count(O.dust('n15'),[3,7]);assert.deepEqual([s.k,s.pairs,s.height,s.layers],[7,9,4,[5,3,1,0]]);
      assert.deepEqual(s.ids,[4,5,6,11,12,13,14]);
      assert.throws(()=>count(O.dust('n15'),[7,3]));
      const invalid=[{nodes:[0,1,2],edges:[[0,1],[1,0]]},{nodes:[1],edges:[[1,1]]},
        {nodes:[1,1],edges:[]},{nodes:[1,2],edges:[[1,3]]},{nodes:[1,2,3],edges:[[1,2],[1,2]]}];
      for(const g of invalid)assert.throws(()=>count(g));
      assert.equal(count({nodes:[],edges:[]}).height,0);
      assert.equal(count({nodes:['x'],edges:[]}).height,1);
      assert.deepEqual(O.infer(s,null,bank).byDimension,[]);
      assert.deepEqual(O.candidates(129,0,bank),null);
      assert.deepEqual(O.candidates(0,0,bank),[2,3,4]);
      for(const [d,r] of [[2,.5],[3,8/35],[4,.1]]) {
        assert.ok(Math.abs(O.mm(r,bank).value-d)<1e-12);
        for(const m of [32,64,128]) {
          let last=0;
          for(const frac of [.01,.1,.3,.5,.9,.99,1]) {
            const v=O.meanHeight(frac,m,d,bank);assert.ok(v>=last);last=v;
            assert.ok(Math.abs(O.chainTime(v,m,d,bank).theta-frac**(1/d))<1e-8);
          }
          assert.equal(O.chainTime(0,m,d,bank).theta,0);
          assert.equal(O.chainTime(m,m,d,bank).upperLimit,true);
        }
      }
      assert.equal(O.mm(0,bank).status,'NO_FINITE_ROOT');assert.equal(O.mm(null,bank).status,'TOO_FEW');
      const P=require('../core.js'), g=O.simulation(P.rng(73),{m:64,d:2,theta:.7}), obs=count(g);
      const a=O.infer(obs,{m:64,T:1},bank), b=O.infer(obs,{m:64,T:5},bank);
      a.byDimension.forEach((v,i)=>assert.ok(Math.abs(b.byDimension[i].chain-5*v.chain)<1e-10));
      assert.deepEqual(a.compatible,b.compatible);
      process.stdout.write(JSON.stringify(graphs.map(g=>count(g))));
    """
    output = json.loads(subprocess.check_output(['node','-e',js], cwd=HERE,
                                               input=json.dumps(rng_cases),text=True))
    for graph,result in zip(rng_cases,output,strict=True):
        audit=analyse(**graph)
        assert audit == {k:result[k] for k in audit}
        assert all(result['matrix'][i][j] for i,j in itertools.pairwise(result['path']))
    bank=json.loads((HERE/'reference.json').read_text())
    assert max(abs(a-b) for a,b in zip(bank['mmGrid'],mm_grid(),strict=True))<1e-13
    c=lis_counts(15)
    assert c == bank['lis15']
    assert Fraction(sum(i*n for i,n in enumerate(c)),sum(c)) == Fraction(96968880223,17435658240)
    for d in (2,3,4):
        rows=bank['conditional'][str(d)]
        assert len(rows)==129
        assert all(a[2]<=b[2] for a,b in itertools.pairwise(rows))
        assert all(0<=lo<=hi<=k*(k-1)//2 for k,(lo,hi,_) in enumerate(rows))
        assert bank['scaling'][str(d)][-1]['k']==16384
    print('PASS: Python/JS on 64 DAGs, N15/N16, open intervals, exact LIS(15), blind calibration.')


if __name__=='__main__':
    main()
