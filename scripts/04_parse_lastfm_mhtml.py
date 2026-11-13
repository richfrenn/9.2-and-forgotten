import os
os.makedirs("output",exist_ok=True)
def src(n):
    return "output/"+n if os.path.exists("output/"+n) else "data/"+n
import sys, email, glob, re, csv, datetime as dt
from email import policy
from bs4 import BeautifulSoup
res=[]
for p in sorted(glob.glob(sys.argv[1])):
    msg=email.message_from_binary_file(open(p,'rb'),policy=policy.default)
    html=None; loc=None
    for part in msg.walk():
        if part.get_content_type()=='text/html':
            html=part.get_content(); loc=part.get('Content-Location'); break
    s=BeautifulSoup(html,'html.parser')
    title=s.title.get_text(strip=True) if s.title else ''
    ab=[a.get('title') for a in s.find_all('abbr')][:2]
    rows=[]; seen=set()
    for tr in s.find_all('tr'):
        c=[td.get_text(strip=True) for td in tr.find_all(['td','th'])]
        if len(c)==2 and re.search(r'20\d\d$',c[0]) and c[0] not in seen:
            seen.add(c[0]); rows.append(c)
    res.append(dict(file=p.split('/')[-1],url=loc,title=title,L=ab[0] if ab else None,S=ab[1] if len(ab)>1 else None,n=len(rows),first=rows[0][0] if rows else None,last=rows[-1][0] if rows else None,rows=rows))
import json; json.dump(res,open('output/mhtml_parsed.json','w'))
for r in res: print(r['title'],'|',r['url'],'|',r['L'],r['S'],r['n'],r['first'],'->',r['last'])
