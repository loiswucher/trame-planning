import json, sys, numpy as np, datetime as dt
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
WCAP=int(sys.argv[1]); MAXN=int(sys.argv[2]); TAG=sys.argv[3]
ND=90; C=json.load(open(f'cands80_{TAG}.json')); months=[(0,31),(31,59),(59,90)]
def vec80(pat,w): return ''.join(pat[(t-3-7*w)%28] for t in range(ND))
def vc(pat,ph): return ''.join(pat[(t-ph)%len(pat)] for t in range(ND))
opts=[]
for pat,we in C:
    if we>WCAP: continue
    for w in range(4):
        r=vec80(pat,w)
        if all(r[a:b].count('N')<=MAXN for a,b in months): opts.append((pat,w,we,r))
groups=[('100',34,[vc(['J','N','R','R','R'],p) for p in range(5)]),('J',4,[vc(['J','J','R','R','R'],p) for p in range(5)]),
        ('50',2,[vc(['J','N']+['R']*8,p) for p in range(10)])]
cols=[]  # (rows)
for o in opts: cols.append(('80',o))
for g,n,rows in groups:
    for p,r in enumerate(rows): cols.append((g,(p,r)))
nv=len(cols)
A=lil_matrix((2*ND,nv+1))
for j,(g,o) in enumerate(cols):
    r=o[3] if g=='80' else o[1]
    for t,c in enumerate(r):
        if c=='J': A[t,j]=1
        if c=='N': A[ND+t,j]=1
lb=np.array([10]*ND+[7]*ND,float)
A2=A.tocsr().copy().tolil()
for t in range(2*ND): A2[t,nv]=-1
ub=np.array([10]*ND+[7]*ND,float)
# totaux par groupe
G=lil_matrix((4,nv+1)); gl=[]
idx80=[j for j,(g,_) in enumerate(cols) if g=='80']
for j in idx80: G[0,j]=1
for k,(g,n,_) in enumerate(groups):
    for j,(gg,_) in enumerate(cols):
        if gg==g: G[k+1,j]=1
tot=np.array([20,34,4,2],float)
cost=np.array([ (o[2] if g=='80' else 0) for g,o in cols]+[500],float)
res=milp(cost,constraints=[LinearConstraint(A.tocsr(),lb,np.inf),LinearConstraint(A2.tocsr(),-np.inf,ub),LinearConstraint(G.tocsr(),tot,tot)],
         integrality=np.array([1]*nv+[0]),bounds=Bounds(0,np.append(np.where(np.array([g=='80' for g,_ in cols]),20,np.where(np.array([g=='100' for g,_ in cols]),34,4)),30)),
         options={'time_limit':400,'disp':False})
print(TAG,WCAP,MAXN,res.status,res.message[:60], res.fun if res.x is not None else None)
if res.x is not None:
    print('Z',res.x[nv]); x=np.round(res.x[:nv]).astype(int); sol=[(cols[j],int(x[j])) for j in range(nv) if x[j]>0]
    out=dict(opts=[],ph={})
    for (g,o),n in sol:
        if g=='80': out['opts']+=[[o[0],o[1],o[2]]]*n
        else: out['ph'].setdefault(g,[]).extend([o[0]]*n)
    json.dump(out,open(f'milpZ_{WCAP}_{MAXN}_{TAG}.json','w'))
    print('weekend shifts total 80%',res.fun,'moyenne/agent',(res.fun-500*res.x[nv])/20, out['ph'])
