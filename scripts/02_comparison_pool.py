import os
os.makedirs("output",exist_ok=True)
def src(n):
    return "output/"+n if os.path.exists("output/"+n) else "data/"+n
"""Phase 2 comparison pool: albums on NME or Village Voice Pazz & Jop top-50s, 2006-2011,
that never appeared in any Pitchfork year-end top 50 for 2006-2011."""
import csv, re, unicodedata, sys, difflib
def norm(s):
    s=unicodedata.normalize("NFKD",s).encode("ascii","ignore").decode().lower()
    s=re.sub(r"\[.*?\]|\(.*?\)","",s)
    s=s.replace("&"," and ")
    s=re.sub(r"[^a-z0-9 ]"," ",s)
    w=[x for x in s.split() if x not in ("the","a","an")]
    return " ".join(w)
def key(a,t): return norm(t)
# Pitchfork frame (all 300 entries, including excluded ones)
pf=list(csv.DictReader(open(src("pitchfork_frame_2006_2011.csv"))))
pf_keys={}
for r in pf: pf_keys.setdefault(norm(r["title"]),[]).append(norm(r["artist"]))
def in_pf(a,t):
    na,nt=norm(a),norm(t)
    for k,arts in pf_keys.items():
        a1,b1=k.replace(" ",""),nt.replace(" ","")
        if a1==b1 or (len(b1)>=6 and (a1.startswith(b1) or b1.startswith(a1))) or difflib.SequenceMatcher(None,a1,b1).ratio()>=0.85:
            for pa in arts:
                if pa==na or {w for w in set(pa.split())&set(na.split()) if len(w)>=3}: return True
    return False
pool={}
src=None
for line in open("raw/lists_raw.txt"):
    line=line.strip()
    if line.startswith("#"): src=line[1:]; continue
    if not line: continue
    a,t=line.split("|"); outlet,yr=src.split(); yr=int(yr)
    k=(norm(a),norm(t))
    e=pool.setdefault(k,dict(artist=a,title=t,year=yr,lists=[]))
    e["year"]=min(e["year"],yr); e["lists"].append(f"{outlet}{yr}")
# Non-studio-album exclusions, set before the draw (reason given)
NONALBUM={
 ("Tom Waits","Orphans : brawlers, bawlers and bastards"):"rarities compilation",
 ("Bob Dylan","Tell tale signs (the bootleg series, vol. 8)"):"archival release",
 ("Bruce Springsteen","The promise : the Darkness on the edge of town story"):"archival release",
 ("Beach boys","The Smile sessions"):"archival release",
 ("Lil Wayne","Da drought 3"):"mixtape",
 ("Frank Ocean","Nostalgia, ultra"):"mixtape (not on streaming services)",
 ("Weeknd","House of balloons"):"mixtape",
 ("Das racist","Shut up, dude"):"mixtape",
 ("Death grips","Exmilitary"):"mixtape",
 ("Drums","Summertime! (EP)"):"EP",
 ("Alex Turner","Submarine (soundtrack)"):"soundtrack EP",
 ("Jeffrey Lewis","12 Crass songs"):"covers album",
 ("Robyn","Body talk"):"compilation of the Body Talk EPs",
 ("Lady Gaga","The fame monster"):"reissue/EP of The Fame",
}
rows=[]
for (na,nt),e in pool.items():
    ex=""
    if in_pf(e["artist"],e["title"]): ex="on a Pitchfork top 50 2006-2011"
    elif (e["artist"],e["title"]) in NONALBUM: ex=NONALBUM[(e["artist"],e["title"])]
    rows.append(dict(year=e["year"],artist=e["artist"],title=e["title"],lists=";".join(e["lists"]),n_lists=len(e["lists"]),excluded=ex))
rows.sort(key=lambda r:(r["year"],r["artist"].lower(),r["title"].lower()))
with open("output/comparison_pool.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
el=[r for r in rows if not r["excluded"]]
print("unique",len(rows),"in PF",sum(r["excluded"].startswith("on a P") for r in rows),"nonalbum",sum(1 for r in rows if r["excluded"] and not r["excluded"].startswith("on a P")),"eligible",len(el))
from collections import Counter; print(Counter(r["year"] for r in el))
