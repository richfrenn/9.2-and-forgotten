import pandas as pd, numpy as np, io, contextlib
from scipy import stats
with contextlib.redirect_stdout(io.StringIO()):
    from match import A
H=pd.read_csv('census_hits_raw.csv')
drop=[('Lil Wayne','RS 500 (2020)',370),('Franz Ferdinand','RS 250 21st (2024-25)',138),('Jay-Z','Guardian 21st (2019)',30),('Jay-Z','RS 250 21st (2024-25)',12)]
for a,l,r in drop: H=H[~((H.artist==a)&(H.list==l)&(H.list_rank==r))]
add=[]
for nm,ttl,l,r in [('Santogold','Santogold','Paste 250 21st (2025)',220),('Maxwell',"Blacksummers'night",'RS 250 21st (2024-25)',122)]:
    i=A[(A.artist.str.lower()==nm.lower())&(A.title.str.lower()==ttl.lower())].index
    assert len(i)==1,(nm,ttl,len(i)); add.append(dict(i=i[0],list=l,list_rank=r))
H=pd.concat([H,pd.DataFrame(add)],ignore_index=True)
H=H.drop_duplicates(['i','list'])
g=H.groupby('i').agg(n_lists=('list','nunique'),top100=('list_rank',lambda s:(s<=100).sum()),detail=('list',lambda s:'; '.join(s)))
A=A.join(g); A['n_lists']=A.n_lists.fillna(0).astype(int); A['top100']=A.top100.fillna(0).astype(int)
A['any']=(A.n_lists>0).astype(int); A['any100']=(A.top100>0).astype(int)
H.merge(A[['artist','title','group','source','year']],left_on='i',right_index=True).to_csv('census_hits_final.csv',index=False)
A.to_csv('census_scored.csv',index=False)
def fx(a,b,lab):
    t=[[a.sum(),len(a)-a.sum()],[b.sum(),len(b)-b.sum()]]; o,p=stats.fisher_exact(t)
    p1,p2=a.mean(),b.mean(); se=np.sqrt(p1*(1-p1)/len(a)+p2*(1-p2)/len(b)); d=p1-p2
    print(f'{lab:32s} {a.sum()}/{len(a)} ({p1:.0%}) vs {b.sum()}/{len(b)} ({p2:.0%})  diff {d:+.0%} [{d-1.96*se:+.0%},{d+1.96*se:+.0%}]  Fisher p={p:.2g}')
P=A[A.group=='Pitchfork']
for col,lab in [('any','ANY APPEARANCE'),('any100','TOP-100')]:
    print('==',lab)
    for s in ['VV','NME','both']: fx(P[col],A[A.source==s][col],'Pitchfork vs '+s)
    fx(P[col],A[A.group=='Comparison'][col],'Pitchfork vs all comparison')
print('by year Pitchfork vs VV:'); print(A[A.source.isin(['Pitchfork','VV'])].groupby(['year','source'])['any'].agg(['sum','count']).unstack())
