import random, itertools, json, numpy as np, datetime as dt
random.seed(7)
NDAY=90; start=dt.date(2027,1,1)
mon=[(start+dt.timedelta(t)) for t in range(NDAY)]
# --- candidats 28 jours (index 0 = lundi)
import sys
NP=int(sys.argv[1]); NL=int(sys.argv[2])
def gen():
    cands=set()
    for _ in range(1200000):
        k=NP
        starts=sorted(random.sample(range(28),k))
        lones=random.sample(range(28),NL)
        shifts=[]  # (day, type)
        for p in starts: shifts+=[(p,'J'),((p+1)%28,'N')]
        shifts+=[(l,'J') for l in lones]
        days=[d for d,_ in shifts]
        if len(set(days))!=len(days): continue
        # espacement cyclique
        ev=sorted(shifts)
        ok=True
        for i,(d,ty) in enumerate(ev):
            nd,nty=ev[(i+1)%len(ev)]; gap=(nd-d)%28 or 28
            # J puis N le lendemain (paire) autorisé
            if ty=='J' and nty=='N' and gap==1: continue
            need=4 if ty=='N' else 2
            if gap<need: ok=False;break
        if not ok: continue
        # un J lone ne doit pas etre suivi d'une paire sans repos: gap>=2 couvre
        pat=['R']*28
        for d,ty in shifts: pat[d]=ty
        we=sum(1 for d,_ in shifts if d%7>=5)
        if we>6: continue
        cands.add((''.join(pat),we))
    return sorted(cands)
C=gen(); print(len(C),'candidats')
json.dump(C,open(f'cands80_{NP}_{NL}.json','w'))
