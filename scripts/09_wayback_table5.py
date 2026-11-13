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
# Section 4.3: Pitchfork vs single comparison source, c. 2012 audience held constant (unflagged)
A2=pd.read_csv('data/analysis_dataset.csv');A2['k']=A2.album.map(norm)
G2=F(M).merge(A2[['k','group','source']],on=['k','group'],how='left')
for s in ['VV','NME']:
    d=G2[(G2.pf==1)|(G2.source==s)]
    print('Pitchfork vs',s,'only (n comparison =',int((d.source==s).sum()),'):',est('ldaily ~ pf + lpre + C(year)',d,'pf'))
# Capture-date sensitivity (added after comments on the submitted draft)
G=F(M).copy(); G['capyr_c']=G.capyr-2012
print('capture dates (main sample):', G.cap.min(), sorted(G.cap)[len(G)//2], G.cap.max(), '; by end 2013:', int((G.capyr<2014).sum()), 'of', len(G))
for t,f in [('pf','ldaily ~ pf + lpre + capyr_c + C(year)'),('any_full','ldaily ~ any_full + lpre + capyr_c + C(year)'),('any_full','ldaily ~ pf + any_full + lpre + capyr_c + C(year)')]:
    print('with capture date:',f,'->',t,est(f,G,t))
print('growth ~ capture date:',est('growth ~ capyr_c + pf + any_full + C(year)',G,'capyr_c'))
print('growth, recognised, with capture date:',est('growth ~ capyr_c + pf + any_full + C(year)',G,'any_full'))
