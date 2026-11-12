"""9.2 and Forgotten: exploratory before-and-after test (not pre-registered).
c.2012 Last.fm audiences from Wayback captures vs 2026 daily listeners."""
import json,re,unicodedata,numpy as np,pandas as pd,statsmodels.formula.api as smf
from scipy import stats
def norm(s):
    s=unicodedata.normalize('NFKD',str(s).lower()).replace('&','and');return re.sub(r'[^a-z0-9]','',s)
raw=json.load(open('data/wayback_2012_audiences.json'))
W=pd.DataFrame([dict(album=v[0],group=v[2],year=v[3],pre=v[4]['number'],cap=v[5]['date']) for v in raw.values()])
W['k']=W.album.map(norm)
A=pd.read_csv('data/analysis_dataset.csv');A['k']=A.album.map(norm)
D=W.merge(A[['k','group','alltime','daily','any_full','flag']],on=['k','group'])
c=pd.to_datetime(D.cap);D['capyr']=c.dt.year+c.dt.dayofyear/365
D['growth']=np.log(D.alltime/D.pre)/(2026.85-D.capyr)*100
D['lpre']=np.log(D.pre);D['ldaily']=np.log(D.daily);D['pf']=(D.group=='Pitchfork').astype(int)
SPLIT=['Bon Iver, Bon Iver','Take Care','Love vs. Money','Inside In / Inside Out','Pick a Bigger Weapon']  # split entry or captured within weeks of release
EARLY=['Velociraptor!','BlaQKout']
D['excl']=np.select([D.capyr>=2018,D.album.isin(SPLIT+EARLY)],['capture after lists began','split entry / capture too soon after release'],'')
out=[]
def say(*a):
    s=' '.join(map(str,a));print(s);out.append(s)
say('collected:',len(W),'matched:',len(D)); say(D[D.excl!=''][['album','group','excl']].to_string())
M=D[D.excl=='']
say('\nMAIN n:',M.groupby('group').size().to_dict(),' 2026-flagged in main:',int(M.flag.astype(bool).sum()))
say('median c.2012 listeners:',M.groupby('group').pre.median().to_dict(),' MW p=%.3f'%stats.mannwhitneyu(M[M.pf==1].pre,M[M.pf==0].pre).pvalue)
say('median capture date:',M.groupby('group').cap.median().to_dict() if False else M.groupby('group').capyr.median().round(2).to_dict())
g=M.groupby('group').growth
say('growth %/yr median:',g.median().round(2).to_dict(),'IQR:',g.quantile([.25,.75]).round(2).to_dict(),' MW p=%.3f'%stats.mannwhitneyu(M[M.pf==1].growth,M[M.pf==0].growth).pvalue)
say('recognised vs not: n',M.groupby('any_full').size().to_dict(),'pre median',M.groupby('any_full').pre.median().to_dict(),
    'MW p=%.3f'%stats.mannwhitneyu(M[M.any_full==1].pre,M[M.any_full==0].pre).pvalue,
    'growth median',M.groupby('any_full').growth.median().round(2).to_dict(),'MW p=%.3f'%stats.mannwhitneyu(M[M.any_full==1].growth,M[M.any_full==0].growth).pvalue)
def show(lab,f,d,terms):
    m=smf.ols(f,d).fit(cov_type='HC3');ci=m.conf_int()
    say(f'{lab} (n={int(m.nobs)}, R2={m.rsquared:.2f}): '+'; '.join(f'{t} {m.params[t]:+.2f} [{ci.loc[t,0]:+.2f}, {ci.loc[t,1]:+.2f}] p={m.pvalues[t]:.3f}' for t in terms))
for lab,d in [('MAIN unflagged',M[~M.flag.astype(bool)]),('MAIN',M),('captures to 2013',M[M.capyr<2014]),('excl 2026-flagged',M[~M.flag.astype(bool)]),('incl split/early',D[D.capyr<2018]),('release 2006-08',M[M.year<=2008])]:
    say('\n--',lab)
    show(' A pf','ldaily ~ pf + lpre + C(year)',d,['pf','lpre'])
    show(' B rec','ldaily ~ any_full + lpre + C(year)',d,['any_full'])
    show(' C both','ldaily ~ pf + any_full + lpre + C(year)',d,['pf','any_full'])
    show(' D growth ~ pf + rec','growth ~ pf + any_full + C(year)',d,['pf','any_full'])
P=M[M.pf==1]
say('\n-- within Pitchfork');show(' rec','ldaily ~ any_full + lpre + C(year)',P,['any_full'])
open('data/wayback_results.txt','w').write('\n'.join(out))
M.to_csv('data/wayback_dataset.csv',index=False)
