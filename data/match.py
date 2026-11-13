import sys,re,unicodedata,pandas as pd
sys.path.insert(0,'.'); import lists_entries as L
def n(s): s=unicodedata.normalize('NFKD',str(s).lower()); s=re.sub(r'[̀-ͯ]','',s).replace('&',' and '); s=re.sub(r'\(.*?\)|\[.*?\]','',s); s=re.sub(r'[^a-z0-9 ]',' ',s); s=re.sub(r'\b(the|a|an)\b',' ',s); return re.sub(r'\s+',' ',s).strip()
def tok(s): return set(t for t in n(s).split() if len(t)>=3)|({n(s)} if n(s) else set())
paste21=[]
for f in ['paste21_101_250.txt','data/lists/paste_21st_2025_top100.txt']:
    for l in open(f):
        r,a,b=l.rstrip('\n').split('|'); paste21.append((int(r),a,b))
LISTS={'RS 500 (2020)':L.RS500,'Consequence 100 (2022)':L.CON100,'Paste 300 (2024)':L.PASTE300,'Guardian 21st (2019)':[(int(r),a,b) for r,a,b in L.GUARDIAN],'RS 250 21st (2024-25)':L.RS250,'Paste 250 21st (2025)':paste21}
pf=pd.read_csv('data/pitchfork_frame_2006_2011.csv'); pf=pf[pf.excluded.isna()].copy()
pf['group']='Pitchfork'; pf['source']='Pitchfork'
po=pd.read_csv('data/comparison_pool.csv'); po=po[po.excluded.isna()].copy()
po['group']='Comparison'; po['source']=po.lists.map(lambda s:'both' if ('NME' in s and 'VV' in s) else ('NME' if 'NME' in s else 'VV')); po['rank']=None; po['band']=None
A=pd.concat([pf[['year','rank','artist','title','band','group','source']],po[['year','rank','artist','title','band','group','source']]],ignore_index=True)
hits=[];near=[]
for i,r in A.iterrows():
    na=n(r.title)
    for ln,ent in LISTS.items():
        for rk,ar,al in ent:
            nb=n(al)
            albok = na==nb or (len(nb)>=6 and len(na)>=6 and (na in nb or nb in na))
            if not albok: continue
            artok = bool(tok(r.artist)&tok(ar))
            (hits if artok else near).append((i,r.group,r.source,r.year,r.artist,r.title,ln,rk,ar,al))
H=pd.DataFrame(hits,columns=['i','group','source','year','artist','title','list','list_rank','l_artist','l_album'])
N=pd.DataFrame(near,columns=H.columns)
A.to_csv('census_frame.csv'); H.to_csv('census_hits_raw.csv',index=False); N.to_csv('census_near.csv',index=False)
pd.set_option('display.width',250); pd.set_option('display.max_rows',300)
print(H[['group','source','year','artist','title','list','list_rank','l_artist','l_album']].to_string())
print('NEAR'); print(N[['group','artist','title','list','list_rank','l_artist','l_album']].to_string())
print(len(A), A.groupby('source').size().to_dict())
