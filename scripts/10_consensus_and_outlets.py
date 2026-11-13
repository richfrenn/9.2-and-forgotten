"""Robustness checks added after comments on the submitted draft (not planned):
(1) Pitchfork albums also chosen by NME and/or Pazz & Jop vs Pitchfork's own picks;
(2) leave-one-outlet-out (both Rolling Stone lists together; both Paste lists together)."""
import pandas as pd,re,unicodedata
from scipy import stats
n=lambda s:re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',str(s).lower()).replace('&','and'))
cp=pd.read_csv('data/comparison_pool.csv'); c=pd.read_csv('data/census_scored.csv')
ov=cp[cp.excluded.astype(str).str.contains('itchfork',na=False)]
P=c[c.group=='Pitchfork'].copy(); P['ka']=P.artist.map(n); P['kt']=P.title.map(n)
ova=set(); 
for _,r in ov.iterrows():
    kt,ka=n(r.title),n(r.artist)
    hit=P[(P.kt==kt)|((P.ka==ka)&(P.year==r.year))]
    ova|=set(hit.index)
P['also']=P.index.isin(ova)
def pr(lab,a): print(f'{lab}: {int(a.sum())}/{len(a)} ({a.mean():.0%})')
pj=c[c.source=='VV']['any']; both=c[c.source=='both']['any']; nme=c[c.source=='NME']['any']
pr('Pitchfork, also chosen by NME and/or Pazz & Jop',P[P.also]['any']); pr('Pitchfork only',P[~P.also]['any'])
pr('  of which top ten',P[P.also&(P.band=='top10')]['any']); print('top-ten albums also chosen elsewhere:',int((P.also&(P.band=='top10')).sum()),'of',int((P.band=='top10').sum()))
pr('Pazz & Jop only',pj); pr('NME and Pazz & Jop, not Pitchfork',both); pr('NME only',nme)
f=lambda a,b: stats.fisher_exact([[a.sum(),len(a)-a.sum()],[b.sum(),len(b)-b.sum()]])[1]
print('Pitchfork-only vs Pazz & Jop-only p=%.3f'%f(P[~P.also]['any'],pj))
print('Pitchfork+other vs NME&PJ-not-Pitchfork p=%.4f'%f(P[P.also]['any'],both))
def rec(d,drop): return d.detail.fillna('').apply(lambda s: any(x and not any(x.startswith(p) for p in drop) for x in s.split('; ')))
PJ=c[c.source=='VV']
for drop in [['RS 500','RS 250'],['Paste 300','Paste 250']]:
    a=rec(P,drop);b=rec(PJ,drop); print('drop',drop,f'Pitchfork {int(a.sum())}/{len(a)} vs Pazz & Jop {int(b.sum())}/{len(b)}, p=%.4f'%f(a,b))
