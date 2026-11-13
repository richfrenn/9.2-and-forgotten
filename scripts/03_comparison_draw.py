import os
os.makedirs("output",exist_ok=True)
def src(n):
    return "output/"+n if os.path.exists("output/"+n) else "data/"+n
"""Seeded draw of the phase 2 comparison group, matched to the pilot sample's per-year counts.
Full seeded order is kept per year so replacements (no usable Last.fm entry) take the next album."""
import csv, random
SEED=20261111
N={2006:9,2007:8,2008:7,2009:9,2010:8,2011:9}   # pilot sample counts by year
pool=[r for r in csv.DictReader(open(src("comparison_pool.csv"))) if not r["excluded"]]
pool.sort(key=lambda r:(int(r["year"]),r["artist"].lower(),r["title"].lower()))
rng=random.Random(SEED)
out=[]
for y in sorted(N):
    yr=[r for r in pool if int(r["year"])==y]
    order=rng.sample(yr,len(yr))
    for i,r in enumerate(order,1):
        out.append(dict(year=y,draw_order=i,artist=r["artist"],title=r["title"],lists=r["lists"],n_lists=r["n_lists"],
                        selected="yes" if i<=N[y] else ""))
with open("output/comparison_draw_order.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
for r in out:
    if r["selected"]: print(r["year"],r["draw_order"],r["artist"],"|",r["title"],"|",r["lists"])
