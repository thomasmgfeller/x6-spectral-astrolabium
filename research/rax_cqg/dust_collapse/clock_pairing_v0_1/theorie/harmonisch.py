"""Exact endpoint-free diagonal reference, N<=2 and alpha=1."""
from fractions import Fraction as F
from itertools import combinations


def weights(s, beta):
    return [1-beta*s+s*s/2, beta-s, F(1), F(1)]


def birth(d):
    return [[1,d,d*d/4,d*d/4],[0,1,d/2,d/2],[0,0,1,0],[0,0,0,1]]


def transport(a,b,beta):
    left, right = weights(a,beta), weights(b,beta)
    return [[F(v)*right[j]/left[i] for j,v in enumerate(row)]
            for i,row in enumerate(birth(b-a))]


def product(first,second):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*second)]
            for row in first]


def require(condition):
    if not condition:
        raise ValueError('exact check failed')


def replay():
    times = [F(i,8) for i in range(9)]
    result = []
    for beta, expected in [(F(5,4),F(1,2)),(F(4,3),F(11,24))]:
        require(F(1)<beta<F(3,2))
        for t in times:
            require(all(x>0 for x in weights(t,beta)))
        for a,b in combinations(times,2):
            p = transport(a,b,beta)
            require(all(sum(row)==1 and min(row)>=0 for row in p))
            h_a,h_b = weights(a,beta), weights(b,beta)
            require([sum(F(x)*y for x,y in zip(row,h_b)) for row in birth(b-a)]==h_a)
        for a,b,c in combinations(times,3):
            require(product(transport(a,b,beta),transport(b,c,beta))==transport(a,c,beta))
        p0 = transport(F(0),F(1,2),beta)[0][0]
        require(p0==expected)
        result.append(p0)
        print(beta,p0,'36 intervals, 84 triples')
    require(result[0]-result[1]==F(1,24))


if __name__=='__main__':
    replay()
