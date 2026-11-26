"""Action at a down-set, exact layer matrix and exhaustive free-clock tests."""
from fractions import Fraction as F
from itertools import permutations
from math import prod


def ideals(nodes, order):
    past = {j:{i for i,k in order if k==j} for j in nodes}
    result = [frozenset()]
    for j in sorted(nodes, key=lambda i:(len(past[i]),i)):
        result += [s|{j} for s in result if past[j]<=s]
    return result


def determinant(rows):
    return sum((-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
               * prod(row[col] for row,col in zip(rows,p)) for p in permutations(range(len(rows))))


def cut_force(i, selected, y, w, edges, box):
    assert w[i].lo == w[i].hi == 0
    return sum((c*w[j]*(y[j]-y[i]) for (k,j),c in edges.items()
                if k==i and j in selected and c),box(0))


def run():
    from quelle import DATA, box
    y,w,order,edges,_,windows = DATA
    z,r,u,h = 16,18,15,17
    nodes = set(y)
    prefix = {i for i,j in order if j==z}
    assert prefix == {0,1,2,u}
    groups = {'prefix':[], 'complement':[], 'cross':[]}
    for (i,j),c in sorted(edges.items()):
        if not c:
            continue
        assert not (j in prefix and i not in prefix)
        kind = 'prefix' if j in prefix else 'cross' if i in prefix else 'complement'
        groups[kind].append([i,j,c])
    cols = [3,4,11,z]
    minor = [[edges.get((i,j),0) for j in cols] for i in sorted(prefix)]
    assert determinant(minor)==-1472
    support = {i:{j:c for (k,j),c in edges.items() if k==i and c and w[j].lo>0}
               for i in (u,h)}
    assert support == {u:{z:1,r:-9,7:16,8:-8},h:{r:1,7:-9,8:16,9:-8}}
    assert w[u].lo == w[u].hi == w[h].lo == w[h].hi == 0
    known = {}
    for i,row in support.items():
        C = sum((c*w[j] for j,c in row.items()),box(0))
        L = sum((c*w[j]*y[j] for j,c in row.items()),box(0))
        assert not C.contains_zero()
        assert (y[i]-L/C).contains_zero()
        known[str(i)] = {'weights':{str(j):row[j] for j in sorted(row)},
                         'quadratic_coefficient':C.data(),'clock_from_exterior':(L/C).data()}

    sections = ideals(nodes,order)
    summaries = {}
    closing = []
    for cut in sections:
        if z not in cut:
            category = 'before_z'
        elif r not in cut:
            category = 'with_z_without_r'
            assert set(support[u]) & cut == {z}
            assert cut_force(u,cut,y,w,edges,box).lo>0
        elif 7 not in cut:
            category = 'with_r_without_7'
            assert set(support[h]) & cut == {r}
            assert cut_force(h,cut,y,w,edges,box).lo>0
        else:
            category = 'with_7'
        summaries[category] = summaries.get(category,0)+1
        if r not in cut:
            continue
        # A complete outgoing support gives exact zero by the original
        # stationary equation. Every incomplete admissible case excludes zero.
        both = True
        for i in (u,h):
            force = cut_force(i,cut,y,w,edges,box)
            full = set(support[i]) <= cut
            assert force.contains_zero() == full
            both &= full
        if both:
            closing.append(cut)
    minimal = [sorted(d) for d in closing if not any(s<d for s in closing)]
    assert minimal == [sorted({9} | {i for i,j in order if j==9})]
    stages = []
    future_order = (7,8,9)
    for n in range(4):
        cut = set(prefix)|{z,r,h,*future_order[:n]}
        # Currents only depend on these listed successors. Complete to an ideal.
        cut |= {i for i,j in order if j in cut}
        stages.append({'through':(r,*future_order)[n],
                       'G15_inside':cut_force(u,cut,y,w,edges,box).data(),
                       'G17_inside':cut_force(h,cut,y,w,edges,box).data()})
    assert set(support[u]) & prefix == set()
    assert [(i,edges[i,z]) for i in sorted(prefix)] == [(0,-8),(1,16),(2,-9),(15,1)]
    prefix_examples = []
    for clock in (F('-2.4675380'), F('-2.4675379')):
        s = (clock*clock-6)/(2*(clock+3))
        assert -3<clock<s and windows[0][0]<(s+F(11,6))/F(23,6)<windows[0][1]
        prefix_examples.append({'Y15':str(clock),'Y16_from_density_only':str(s)})
    return {'D':sorted(prefix), 'action_edges':groups, 'cross_rank':4,'minor':minor,
            'minor_columns':cols,'minor_determinant':determinant(minor),'vacuum':known,
            'ideal_count':len(sections),'ideal_groups':summaries, 'both_closed_with_receiver':len(closing),
            'least_ideal_with_receiver_and_both_closed':minimal[0],'successive_forces':stages,
            'partial_prefix_examples':prefix_examples}
