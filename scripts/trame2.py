import json, datetime as dt
from collections import Counter
sol=json.load(open('milpZ_2_4_4_2.json'))
ND=90; start=dt.date(2027,1,1); days=[start+dt.timedelta(i) for i in range(ND)]
P100=['J','N','R','R','R']; PJ=['J','J','R','R','R']; P50=['J','N']+['R']*8
agents=[]
def add(q,prof,pat,phase):
    L=len(pat); agents.append(dict(q=q,prof=prof,pat=pat,phase=phase,row=[pat[(t-phase)%L] for t in range(ND)]))
for ph in sorted(sol['ph']['100']): add('100%','Rotation J/N',P100,ph)
for pat,w,we in sol['opts']: add('80%','Rotation J/N',list(pat),(3+7*w)%28)
for ph in sorted(sol['ph']['50']): add('50%','Rotation J/N',P50,ph)
for ph in sorted(sol['ph']['J']): add('100%','Jour seul',PJ,ph)
assert len(agents)==60
J=[sum(a['row'][t]=='J' for a in agents) for t in range(ND)]
N=[sum(a['row'][t]=='N' for a in agents) for t in range(ND)]
print('J',min(J),max(J),'N',min(N),max(N))
months=[(0,31),(31,59),(59,90)]
for q,pf in [('100%','Rotation J/N'),('80%','Rotation J/N'),('50%','Rotation J/N'),('100%','Jour seul')]:
    g=[a for a in agents if a['q']==q and a['prof']==pf]
    mx=max(a['row'][x:y].count('N') for a in g for x,y in months)
    we=[sum(1 for t in range(ND) if a['row'][t]!='R' and days[t].weekday()>=5) for a in g]
    sh=[sum(1 for c in a['row'] if c!='R') for a in g]
    print(q,pf,len(g),'nuits max/mois',mx,'postes WE/90j moy',round(sum(we)/len(we),1),'min/max',min(we),max(we),'postes/90j moy',round(sum(sh)/len(sh),1))
# 80%: heures moyennes par semaine
g=[a for a in agents if a['q']=='80%']
print('80% h/sem',sum(sum(1 for c in a['row'] if c!='R') for a in g)/20*12/ (90/7))
json.dump(dict(agents=agents,J=J,N=N),open('trame.json','w'))
