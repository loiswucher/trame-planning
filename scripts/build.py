import json, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter as L
d=json.load(open('trame.json')); agents=d['agents']
F=lambda **k: Font(name='Arial',**k)
fill=lambda c: PatternFill('solid',start_color=c,end_color=c)
thin=Side(style='thin',color='BFBFBF'); box=Border(left=thin,right=thin,top=thin,bottom=thin)
wb=Workbook(); S=wb.active; S.title='Synthèse'; T=wb.create_sheet('Trame')
NA=60; N=90; R0=6; R1=R0+NA-1; C0=10; C1=C0+N-1
# ---------- Trame
T['A1']='Trame de planning 12h – janvier à mars 2027 (10 postes de jour / 7 postes de nuit)'; T['A1'].font=F(bold=True,size=14)
T['A2']='J = jour 7h-19h · N = nuit 19h-7h · R = repos. Les codes se calculent à partir du cycle (col. E) et de la position au 1er jour (col. G) : modifiez ces deux cellules pour décaler un agent.'; T['A2'].font=F(italic=True,size=9)
hdr=['N°','Agent','Quotité','Profil','Cycle','Durée cycle (j)','Position au 1er jour','Roulement complet (j)','Roulement complet terminé le']
for i,h in enumerate(hdr,1):
    c=T.cell(5,i,h); c.font=F(bold=True,color='FFFFFF',size=9); c.fill=fill('1F3864'); c.alignment=Alignment(wrap_text=True,horizontal='center',vertical='center'); c.border=box
T.row_dimensions[5].height=48
for j in range(N):
    col=C0+j
    c=T.cell(5,col)
    c.value="=Synthèse!$B$4" if j==0 else f"={L(col-1)}5+1"
    c.number_format='dd/mm'; c.font=F(bold=True,size=8,color='FFFFFF'); c.fill=fill('1F3864'); c.alignment=Alignment(horizontal='center',vertical='center',text_rotation=90); c.border=box
    w=T.cell(4,col,f'=CHOOSE(WEEKDAY({L(col)}5,2),"L","M","M","J","V","S","D")')
    w.font=F(bold=True,size=8); w.alignment=Alignment(horizontal='center')
    w.fill=fill('F8CBAD') if False else PatternFill()
tc=[C1+1,C1+2,C1+3,C1+4,C1+5,C1+6,C1+7,C1+8]
for col,h in zip(tc,['Nb jours (J)','Nb nuits (N)','Heures','Nuits janv.','Nuits févr.','Nuits mars','Nuits max / mois','Postes sam./dim.']):
    c=T.cell(5,col,h); c.font=F(bold=True,color='FFFFFF',size=9); c.fill=fill('1F3864'); c.alignment=Alignment(wrap_text=True,horizontal='center',vertical='center'); c.border=box
for i,a in enumerate(agents):
    r=R0+i; pat=''.join(a['pat']); Lc=len(pat)
    pos=(-a['phase'])%Lc+1
    cyc={'JNRRR':'JNRRR','JJRRR':'JJRRR'}.get(pat,pat)
    vals=[i+1,f'Agent {i+1:02d}',a['q'],a['prof'],pat,f'=LEN(E{r})',pos,f'=F{r}*7/GCD(F{r},7)',f'=$J$5+H{r}-1']
    for k,v in enumerate(vals,1):
        c=T.cell(r,k,v); c.font=F(size=9,color='0000FF' if k in (2,5,7) else '000000'); c.border=box
        c.alignment=Alignment(horizontal='center' if k!=2 and k!=4 else 'left',shrink_to_fit=(k==5))
    T.cell(r,9).number_format='dd/mm/yyyy'
    for j in range(N):
        col=C0+j
        c=T.cell(r,col,f'=MID($E{r},MOD($G{r}-1+{L(col)}$5-$J$5,$F{r})+1,1)')
        c.font=F(size=8,bold=True); c.alignment=Alignment(horizontal='center'); c.border=box
    rng=f'{L(C0)}{r}:{L(C1)}{r}'
    T.cell(r,tc[0],f'=COUNTIF({rng},"J")'); T.cell(r,tc[1],f'=COUNTIF({rng},"N")'); T.cell(r,tc[2],f'=({L(tc[0])}{r}+{L(tc[1])}{r})*Synthèse!$B$7')
    ms=[(C0,C0+30),(C0+31,C0+58),(C0+59,C1)]
    for k,(x,y) in enumerate(ms): T.cell(r,tc[3+k],f'=COUNTIF({L(x)}{r}:{L(y)}{r},"N")')
    T.cell(r,tc[6],f'=MAX({L(tc[3])}{r}:{L(tc[5])}{r})')
    T.cell(r,tc[7],f'=SUMPRODUCT((({L(C0)}$4:{L(C1)}$4="S")+({L(C0)}$4:{L(C1)}$4="D"))*({L(C0)}{r}:{L(C1)}{r}<>"R"))')
    for col in tc: T.cell(r,col).font=F(size=9); T.cell(r,col).alignment=Alignment(horizontal='center'); T.cell(r,col).border=box
# coverage rows
rows=[('J présents',lambda c:f'=COUNTIF({c}{R0}:{c}{R1},"J")'),('N présents',lambda c:f'=COUNTIF({c}{R0}:{c}{R1},"N")'),
      ('Objectif J',lambda c:'=Synthèse!$B$5'),('Objectif N',lambda c:'=Synthèse!$B$6'),
      ('Marge J',lambda c:f'={c}67-{c}69'),('Marge N',lambda c:f'={c}68-{c}70')]
for k,(lab,fn) in enumerate(rows):
    r=67+k
    T.cell(r,1,lab).font=F(bold=True,size=9)
    for j in range(N):
        col=C0+j; c=T.cell(r,col,fn(L(col))); c.font=F(size=8,bold=(k<2)); c.alignment=Alignment(horizontal='center'); c.border=box
T['A74']='Marge = effectif présent dans la trame – postes à tenir : elle sert à absorber CA, RTT, arrêts maladie et formations.'; T['A74'].font=F(italic=True,size=9)
cr=f'{L(C0)}{R0}:{L(C1)}{R1}'
T.conditional_formatting.add(cr,CellIsRule(operator='equal',formula=['"J"'],fill=fill('FFE699')))
T.conditional_formatting.add(cr,CellIsRule(operator='equal',formula=['"N"'],fill=fill('2F5597'),font=Font(name='Arial',color='FFFFFF',bold=True)))
T.conditional_formatting.add(cr,CellIsRule(operator='equal',formula=['"R"'],font=Font(name='Arial',color='BFBFBF')))
T.conditional_formatting.add(f'{L(C0)}71:{L(C1)}72',CellIsRule(operator='lessThan',formula=['0'],fill=fill('FF9999')))
T.conditional_formatting.add(f'{L(C0)}4:{L(C1)}4',FormulaRule(formula=[f'OR({L(C0)}4="S",{L(C0)}4="D")'],fill=fill('F8CBAD')))
T.conditional_formatting.add(f'{L(C0)}5:{L(C1)}5',FormulaRule(formula=[f'OR({L(C0)}$4="S",{L(C0)}$4="D")'],fill=fill('C55A11')))
for col,w in zip(range(1,10),[4,10,8,13,9,8,9,10,13]): T.column_dimensions[L(col)].width=w
for col in range(C0,C1+1): T.column_dimensions[L(col)].width=3.6
for col in tc: T.column_dimensions[L(col)].width=9
T.freeze_panes=T.cell(R0,C0)
# ---------- Synthèse
S['A1']='Synthèse de la trame – janvier à mars 2027'; S['A1'].font=F(bold=True,size=14)
S['A3']='Paramètres'; S['A3'].font=F(bold=True,size=11)
par=[('Date de début de la trame',dt.date(2027,1,1),'dd/mm/yyyy'),('Postes de jour à tenir par jour',10,'0'),('Postes de nuit à tenir par jour',7,'0'),('Durée d’un poste (h)',12,'0')]
for i,(a,b,f) in enumerate(par):
    S.cell(4+i,1,a).font=F(size=10); c=S.cell(4+i,2,b); c.font=F(size=10,color='0000FF'); c.number_format=f; c.alignment=Alignment(horizontal='center')
S['A9']='Roulement complet par profil'; S['A9'].font=F(bold=True,size=11)
h=['Profil','Cycle','Durée du cycle (j)','Agents','Roulement complet (j)','Roulement complet terminé le','Nouveau roulement identique dès le','Nuits max sur un mois','Postes sam./dim. (moy. sur 90 j)','Heures / semaine (moy.)']
for i,t in enumerate(h,1):
    c=S.cell(10,i,t); c.font=F(bold=True,color='FFFFFF',size=10); c.fill=fill('1F3864'); c.alignment=Alignment(wrap_text=True,horizontal='center',vertical='center'); c.border=box
S.row_dimensions[10].height=45
prof=[('100 % – rotation','JNRRR','100%','Rotation J/N',None),('80 % – rotation','4 × JNRRR + 2 J','80%','Rotation J/N',28),('50 % – rotation','JNRRRRRRRR','50%','Rotation J/N',None),('100 % – jour seul','JJRRR','100%','Jour seul',None)]
for i,(n,p,q,pf,ln) in enumerate(prof):
    r=11+i
    crit=f'Trame!$C${R0}:$C${R1},"{q}",Trame!$D${R0}:$D${R1},"{pf}"'
    vals=[n,p,ln if ln else f'=LEN(B{r})',f'=COUNTIFS({crit})',f'=C{r}*7/GCD(C{r},7)',f'=$B$4+E{r}-1',f'=$B$4+E{r}',f'=_xlfn.MAXIFS(Trame!${L(tc[6])}${R0}:${L(tc[6])}${R1},{crit})',f'=AVERAGEIFS(Trame!${L(tc[7])}${R0}:${L(tc[7])}${R1},{crit})',f'=AVERAGEIFS(Trame!${L(tc[2])}${R0}:${L(tc[2])}${R1},{crit})/(90/7)']
    for k,v in enumerate(vals,1):
        c=S.cell(r,k,v); c.font=F(size=10); c.border=box; c.alignment=Alignment(horizontal='left' if k==1 else 'center')
    S.cell(r,6).number_format='dd/mm/yyyy'; S.cell(r,7).number_format='dd/mm/yyyy'; S.cell(r,9).number_format='0.0'; S.cell(r,10).number_format='0.0'
S['A15']='Total agents'; S['A15'].font=F(bold=True,size=10); S['D15']='=SUM(D11:D14)'; S['D15'].font=F(bold=True,size=10); S['D15'].alignment=Alignment(horizontal='center')
S['A17']='Couverture (effectif présent dans la trame, 90 jours)'; S['A17'].font=F(bold=True,size=11)
cov=[('Jour : minimum / moyenne / maximum',f'=MIN(Trame!{L(C0)}67:{L(C1)}67)',f'=AVERAGE(Trame!{L(C0)}67:{L(C1)}67)',f'=MAX(Trame!{L(C0)}67:{L(C1)}67)'),
     ('Nuit : minimum / moyenne / maximum',f'=MIN(Trame!{L(C0)}68:{L(C1)}68)',f'=AVERAGE(Trame!{L(C0)}68:{L(C1)}68)',f'=MAX(Trame!{L(C0)}68:{L(C1)}68)')]
for i,(a,x,y,z) in enumerate(cov):
    r=18+i; S.cell(r,1,a).font=F(size=10)
    for k,v in enumerate([x,y,z],2):
        c=S.cell(r,k,v); c.font=F(size=10); c.alignment=Alignment(horizontal='center'); c.number_format='0.0' if k==3 else '0'
S['A20']='Jours sous l’objectif (jour + nuit)'; S['A20'].font=F(size=10)
S['B20']=f'=COUNTIF(Trame!{L(C0)}71:{L(C1)}72,"<0")'; S['B20'].font=F(bold=True,size=10); S['B20'].alignment=Alignment(horizontal='center')
S['A22']='Hypothèses retenues'; S['A22'].font=F(bold=True,size=11)
hyp=['Période : 1er janvier au 31 mars 2027 (90 jours). La trame se répète à l’identique, la date de début est modifiable (B4).',
'60 agents : 38 à 100 %, 20 à 80 %, 2 à 50 %. 4 agents à 100 % sont « jour seul » (cycle JJRRR) ; les 56 autres tournent jour/nuit.',
'100 % : 1 jour, 1 nuit, 3 repos (5 jours). 80 % : 1 jour, 1 nuit, 4 repos (6 jours). 50 % : 1 jour, 1 nuit, 8 repos (10 jours).',
'Roulement complet = l’agent repasse par chaque position du cycle sur chaque jour de la semaine (week-ends compris) : PPCM(cycle ; 7) = 35 / 42 / 70 jours.',
'Les agents sont décalés dans le cycle pour répartir les équipes : colonnes E (cycle) et G (position au 1er jour) de l’onglet Trame.',
'La trame présente plus de monde que les postes à tenir : cette marge absorbe congés, RTT, arrêts et formations. Elle est plus large la nuit que le jour.',
'Noms d’agents fictifs (Agent 01…) à remplacer ; ne tient pas compte des jours fériés ni des congés posés.']
for i,t in enumerate(hyp):
    c=S.cell(23+i,1,'• '+t); c.font=F(size=10)
S.column_dimensions['A'].width=38
for col,w in zip('BCDEFGHIJ',[18,16,10,16,20,22,14,18,14]): S.column_dimensions[col].width=w
wb.save('Trame_planning_12h_janv-mars_2027.xlsx')
