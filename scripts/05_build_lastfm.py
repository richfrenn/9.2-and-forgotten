import os
os.makedirs("output",exist_ok=True)
def src(n):
    return "output/"+n if os.path.exists("output/"+n) else "data/"+n
import csv, datetime as dt
frame={ (r['artist'],r['title']):r for r in csv.DictReader(open(src('pitchfork_frame_2006_2011.csv')))}
alias={("Ariel Pink","Before Today"):("Ariel Pink's Haunted Graffiti","Before Today"),("Micachu and the Shapes","Jewellery"):("Micachu and the Shapes","Jewellery")}
start=dt.date(2026,5,13)
daily=open('output/lastfm_daily_listeners.csv','w',newline=''); dw=csv.writer(daily); dw.writerow(['artist','album','lastfm_url','date','daily_listeners'])
summ=[]
for line in open('raw/raw.tsv'):
    a,t,url,L,S,first,last,pre,preN,post,postN,ser=line.rstrip('\n').split('\t')
    vals=[int(x) for x in ser.split()]
    assert len(vals)==181,(a,len(vals))
    for i,v in enumerate(vals): dw.writerow([a,t,'https://www.last.fm'+url,(start+dt.timedelta(i)).isoformat(),v])
    f=frame.get(alias.get((a,t),(a,t)))
    L=int(L.replace(',','')); pre=float(pre); post=float(post)
    br=post/pre if pre else None
    summ.append(dict(artist=a,album=t,year=f['year'] if f else '',rank=f['rank'] if f else '',band=f['band'] if f else '',lastfm_url='https://www.last.fm'+url,total_listeners=L,total_scrobbles=int(S.replace(',','')),daily_mean_14may_22jul=pre,daily_mean_sep_oct=post,post_over_pre=round(br,2),current_activity_ratio_pct=round(100*pre/L,4),entry_check='OK' if br<0.75 else 'FLAG: little or no July break; resolve by identity check only'))
daily.close()
summ.sort(key=lambda r:-r['current_activity_ratio_pct'])
with open('output/lastfm_summary.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(summ[0].keys())); w.writeheader(); w.writerows(summ)
for r in summ: print(r['year'],r['rank'],r['artist'],'|',r['album'],r['daily_mean_14may_22jul'],r['current_activity_ratio_pct'],r['post_over_pre'],r['entry_check'][:7])
