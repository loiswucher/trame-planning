import json, zipfile, datetime as dt, math
d=json.load(open('trame.json')); ag=d['agents']
data=[]
for i,a in enumerate(ag):
    pat=''.join(a['pat'])
    data.append([f'Agent {i+1:02d}',a['q'],a['prof'],pat,''.join(a['row'])])
html=open('cal_template.html',encoding='utf-8').read().replace('__DATA__',json.dumps(data,ensure_ascii=False))
open('calendrier_agents.html','w',encoding='utf-8').write(html)
# ICS
start=dt.date(2027,1,1)
tz="""BEGIN:VTIMEZONE
TZID:Europe/Paris
BEGIN:STANDARD
DTSTART:19701025T030000
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19700329T020000
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
END:VTIMEZONE
""".replace('\n','\r\n')
import os; os.makedirs('ics',exist_ok=True)
z=zipfile.ZipFile('Calendriers_agents_janv-mars_2027.zip','w',zipfile.ZIP_DEFLATED)
for i,a in enumerate(ag):
    name=f'Agent {i+1:02d}'
    out=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Trame 12h//FR','CALSCALE:GREGORIAN',f'X-WR-CALNAME:Planning {name}']
    s=''.join(['']) 
    body=[]
    for t,c in enumerate(a['row']):
        if c=='R': continue
        day=start+dt.timedelta(t); ds=day.strftime('%Y%m%d')
        if c=='J': s0,e0,lab=f'{ds}T070000',f'{ds}T190000','Jour (7h-19h)'
        else:
            e=day+dt.timedelta(1); s0,e0,lab=f'{ds}T190000',f'{e.strftime("%Y%m%d")}T070000','Nuit (19h-7h)'
        body+=['BEGIN:VEVENT',f'UID:{name.replace(" ","")}-{ds}-{c}@trame12h',f'DTSTAMP:20261120T180000Z',f'DTSTART;TZID=Europe/Paris:{s0}',f'DTEND;TZID=Europe/Paris:{e0}',f'SUMMARY:{lab}','END:VEVENT']
    txt='\r\n'.join(out)+'\r\n'+tz+'\r\n'.join(body)+'\r\nEND:VCALENDAR\r\n'
    z.writestr(f'{name.replace(" ","_")}_{a["q"].replace("%","pct")}.ics',txt)
z.close(); print(len(data))
