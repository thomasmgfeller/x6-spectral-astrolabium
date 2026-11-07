"""Exact finite control of an explicit pointer-plus-filter measurement."""
from fractions import Fraction as F


def eye(n):return [[F(int(i==j)) for j in range(n)] for i in range(n)]
def zero(n):return [[F(0) for _ in range(n)] for _ in range(n)]
def transpose(a):return list(map(list,zip(*a)))
def product(a,b):return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]
def add(a,b):return [[x+y for x,y in zip(row,col)] for row,col in zip(a,b)]
def require(ok,message):
    if not ok:raise RuntimeError(message)


def audit():
    projectors=[zero(4) for _ in range(4)]
    projectors[0][0][0]=projectors[1][1][1]=F(1)
    for i in [2,3]:
        for j in [2,3]:
            projectors[2][i][j]=F(1,2)
            projectors[3][i][j]=F(1 if i==j else -1,2)
    require(sum_matrices(projectors)==eye(4),'Complete orthogonal effects')
    orth=0
    for i,a in enumerate(projectors):
        for j,b in enumerate(projectors):
            require(product(a,b)==(a if i==j else zero(4)),'Orthogonal projectors');orth+=1
    U=zero(16)
    for label,a in enumerate(projectors):
        for i in range(4):
            for j in range(4):
                for pointer in range(4):U[4*i+(pointer+label)%4][4*j+pointer]+=a[i][j]
    require(product(transpose(U),U)==product(U,transpose(U))==eye(16),'Pointer coupling is unitary')
    kraus=[]
    for label in range(4):
        k=[[U[4*i+label][4*j] for j in range(4)] for i in range(4)]
        require(k==projectors[label],'Measured pointer gives prescribed Kraus operator');kraus.append(k)
    count_two=add(projectors[2],projectors[3])
    phases=[(F(1),F(1)),(F(1),F(-1))]
    counts=[];success=[]
    for x,y in phases:
        # psi=(x,y)/sqrt(2) in the final two-record sector; all factors rational.
        vector=[[F(0)],[F(0)],[x],[y]]
        counts.append(product(transpose(vector),product(count_two,vector))[0][0]/2)
        success.append(product(transpose(vector),product(projectors[2],vector))[0][0]/2)
    require(counts==[F(1),F(1)] and success==[F(1),F(0)],'Counting cannot replace coherent filtering')
    rho=zero(4);rho[2][2]=F(1)
    after=sum_matrices([product(k,product(rho,transpose(k))) for k in kraus])
    require([after[i][i] for i in range(4)]==[F(0),F(0),F(1,2),F(1,2)],
            'Ignoring readout can disturb geometry records')
    return {'basis_dimension':4,'pointer_dimension':4,'unitary_dimension':16,
            'orthogonal_projector_products':orth,'unitarity':'EXACT_PASS','kraus_completeness':'EXACT_PASS',
            'projectors':projectors,'count_only_probabilities':counts,'coherent_success_probabilities':success,
            'nonselective_record_disturbance':{'before':['0','0','1','0'],
                                            'after':[after[i][i] for i in range(4)]},
            'physical_detector_selected':False,'full_history_coherent_access':'ASSUMED',
            'fixed_number_alpha_dependence':'NONE; alpha changes preparation weights across numbers'}


def sum_matrices(matrices):
    out=zero(len(matrices[0]))
    for x in matrices:out=add(out,x)
    return out
