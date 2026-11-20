"""Areal radius of a closed triangulated 2-sphere from intrinsic squared lengths."""
from collections import Counter, defaultdict
from fractions import Fraction as F
from math import isqrt

SCALE = 10**12
# These rational endpoints are also verified below by a Machin-series enclosure.
PI = (F("3.14159265358979323846"), F("3.14159265358979323847"))

def verify_pi():
    def atan_inverse(n):
        terms = [F((-1)**i, (2*i+1)*n**(2*i+1)) for i in range(24)]
        return sum(terms), sum(terms[:-1])
    a,b = atan_inverse(5),atan_inverse(239)
    assert PI[0] <= 16*a[0]-4*b[1] <= 16*a[1]-4*b[0] <= PI[1]

def sqrt_bounds(value):
    if value < 0:
        raise ValueError("Negative squared magnitude")
    low = isqrt(value.numerator*SCALE*SCALE//value.denominator)
    exact = low*low*value.denominator == value.numerator*SCALE*SCALE
    return F(low,SCALE), F(low+(not exact),SCALE)

def connected(adj):
    if not adj:
        return False
    visited = set()
    stack = [next(iter(adj))]
    while stack:
        v = stack.pop()
        if v not in visited:
            visited.add(v)
            stack.extend(adj[v]-visited)
    return len(visited) == len(adj)

def mesh_radius(faces, lengths):
    """Return rational enclosure. lengths maps unordered index pairs to squared lengths."""
    edge_counts = Counter()
    graph = defaultdict(set)
    links = defaultdict(lambda: defaultdict(set))
    seen = set()
    low, high = F(0), F(0)
    for a,b,c in faces:
        face = frozenset((a,b,c))
        if len(face)!=3 or face in seen:
            raise ValueError("Repeated or degenerate face")
        seen.add(face)
        sides = []
        for u,v,w in ((a,b,c),(b,c,a),(c,a,b)):
            edge = tuple(sorted((u,v)))
            if edge not in lengths or lengths[edge]<=0:
                raise ValueError("Missing or nonpositive squared length")
            sides.append(F(lengths[edge]))
            edge_counts[edge] += 1
            graph[u].add(v)
            graph[v].add(u)
            links[w][u].add(v)
            links[w][v].add(u)
        i,j,k = sides
        discriminant = 2*(i*j+j*k+k*i)-i*i-j*j-k*k
        if discriminant<=0:
            raise ValueError("Invalid intrinsic triangle")
        l,h = sqrt_bounds(discriminant)
        low += l/4
        high += h/4
    if (not connected(graph) or set(edge_counts.values())!={2}
            or len(graph)-len(edge_counts)+len(seen)!=2):
        raise ValueError("Cut is not a connected closed triangulated sphere")
    for link in links.values():
        if not connected(link) or any(len(neighbors)!=2 for neighbors in link.values()):
            raise ValueError("Vertex link is not a cycle")
    return sqrt_bounds(low/(4*PI[1]))[0], sqrt_bounds(high/(4*PI[0]))[1]

def quarter(t):
    return (1-t*t)/(1+t*t), 2*t/(1+t*t)

def calibration_mesh(n, radius):
    azimuth = []
    for quadrant in range(4):
        for j in range(n):
            c,s = quarter(F(j,n))
            azimuth.append([(c,s),(-s,c),(-c,-s),(s,-c)][quadrant])
    vertices = [(F(0),F(0),F(radius))]
    rings = []
    for i in range(1,2*n):
        c,s = quarter(F(min(i,2*n-i),n))
        if i>n:
            c = -c
        start = len(vertices)
        vertices.extend((radius*s*u,radius*s*v,radius*c) for u,v in azimuth)
        rings.append(list(range(start,len(vertices))))
    south = len(vertices)
    vertices.append((F(0),F(0),F(-radius)))
    faces = []
    for j in range(len(azimuth)):
        k = (j+1)%len(azimuth)
        faces.extend([(0,rings[0][j],rings[0][k]),(south,rings[-1][k],rings[-1][j])])
        for upper,lower in zip(rings,rings[1:]):
            faces.extend([(upper[j],lower[j],lower[k]),(upper[j],lower[k],upper[k])])
    assert all(sum(x*x for x in p)==radius**2 for p in vertices)
    edges = {tuple(sorted((u,v))) for a,b,c in faces for u,v in [(a,b),(b,c),(c,a)]}
    squared = {(u,v):sum((a-b)**2 for a,b in zip(vertices[u],vertices[v])) for u,v in edges}
    return faces,squared

def calibrate():
    verify_pi()
    records = []
    for radius in (3,7):
        previous_error = F(1)
        for n in (4,8,16):
            faces, lengths = calibration_mesh(n,radius)
            low,high = mesh_radius(faces,lengths)
            assert low<=high<radius and 1-low/radius<previous_error
            previous_error = 1-high/radius
            records.append({"true_radius":radius,"resolution":n,"faces":len(faces),
                            "mesh_radius_bounds":list(map(str,[low,high])),
                            "relative_error_upper":float(1-low/radius)})
        assert previous_error<F(1,100)
    try:
        mesh_radius(faces[1:],lengths)
    except ValueError:
        pass
    else:
        raise AssertionError("Open cut accepted")
    return records
