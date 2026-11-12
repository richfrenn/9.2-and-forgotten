import pandas as pd,numpy as np,statsmodels.formula.api as smf,json,re,unicodedata
from scipy import stats
exec(open('scripts/08_wayback_exploratory.py').read().split("out=[]")[0])
F=lambda d:d[~d.flag.astype(bool)]
M=D[D.excl=='']
OLD=D[(D.capyr<2018)&(~D.album.isin(['BlaQKout','Bon Iver, Bon Iver','Velociraptor!','Love vs. Money','Take Care']))]
specs=[('Main: unflagged entries',F(M)),('Flagged 2026 entries restored',M),('Captures to 2013 only',F(M[M.capyr<2014])),
       ('Split and early entries restored',F(D[D.capyr<2018])),('Exclusion list before consistency check',F(OLD)),('Releases 2006 to 2008 only',F(M[M.year<=2008]))]
def est(f,d,t):
    m=smf.ols(f,d).fit(cov_type='HC3');ci=m.conf_int().loc[t];return m.params[t],ci[0],ci[1],m.pvalues[t],int(m.nobs)
rows=[]
for lab,d in specs:
    a=est('ldaily ~ pf + lpre + C(year)',d,'pf');b=est('ldaily ~ any_full + lpre + C(year)',d,'any_full');c=est('ldaily ~ pf + any_full + lpre + C(year)',d,'any_full')
    rows.append((lab,a[4],a,b,c))
    print(lab,a[4],'pf %+.2f [%+.2f,%+.2f] p=%.3f'%a[:4],'| rec %+.2f [%+.2f,%+.2f] p=%.3f'%b[:4],'| both %+.2f [%+.2f,%+.2f] p=%.3f'%c[:4])
P=F(M)[F(M).pf==1];print('within Pf',est('ldaily ~ any_full + lpre + C(year)',P,'any_full'))
G=F(M);print('n',G.groupby('group').size().to_dict(),'rec',G.groupby(['group','any_full']).size().to_dict())
print('pre med',G.groupby('group').pre.median().to_dict(),stats.mannwhitneyu(G[G.pf==1].pre,G[G.pf==0].pre).pvalue)
print('growth med',G.groupby('group').growth.median().round(2).to_dict(),stats.mannwhitneyu(G[G.pf==1].growth,G[G.pf==0].growth).pvalue)
print('rec pre',G.groupby('any_full').pre.median().to_dict(),stats.mannwhitneyu(G[G.any_full==1].pre,G[G.any_full==0].pre).pvalue)
print('lpre',est('ldaily ~ pf + lpre + C(year)',G,'lpre'))
print('growth model',est('growth ~ pf + any_full + C(year)',G,'any_full'))
print('captures',(G.capyr<2014).sum(),G.cap.max(),G.cap.min(),G.cap.median() if False else sorted(G.cap)[len(G)//2])
D[['album','group','year','pre','cap','alltime','daily','any_full','flag','excl']].to_csv('data/wayback_all_entries.csv',index=False)
