import os
os.makedirs("output",exist_ok=True)
def src(n):
    return "output/"+n if os.path.exists("output/"+n) else "data/"+n
"""Exploratory pilot models (Pitchfork sample, entries passing identity check).
Primary outcome: log mean daily unique listeners, 14 May-22 Jul 2026.
Secondary: current activity ratio (exploratory normalisation).
Historical reach (log all-time Last.fm listeners) enters as a predictor, not a denominator.
Design weights: top-10 band 58 eligible/25 sampled, 11-50 band 218/25."""
import csv, numpy as np, statsmodels.formula.api as smf, pandas as pd
from scipy.stats import spearmanr
d=pd.DataFrame(list(csv.DictReader(open(src("lastfm_summary.csv")))))
for c in ["rank","total_listeners","daily_mean_14may_22jul","current_activity_ratio_pct","year"]: d[c]=pd.to_numeric(d[c])
d["log_daily"]=np.log(d.daily_mean_14may_22jul); d["log_reach"]=np.log(d.total_listeners)
d["log_rank"]=np.log(d["rank"]); d["top10"]=(d.band=="top10").astype(int)
d["w"]=np.where(d.top10==1,58/25,218/25)
def run(sub,label):
    print(f"\n=== {label}  n={len(sub)}")
    print("Spearman rank~daily", spearmanr(sub["rank"],sub.daily_mean_14may_22jul))
    print("Spearman rank~ratio", spearmanr(sub["rank"],sub.current_activity_ratio_pct))
    print("Spearman rank~reach", spearmanr(sub["rank"],sub.total_listeners))
    for f in ["log_daily ~ log_rank","log_daily ~ log_rank + log_reach","log_daily ~ log_rank + log_reach + C(year)"]:
        m=smf.ols(f,sub).fit(cov_type="HC3")
        print(f, "| " + "; ".join(f"{k}={m.params[k]:.3f} (p={m.pvalues[k]:.3f})" for k in m.params.index if k!="Intercept" and not k.startswith("C(")), f"| R2={m.rsquared:.2f}")
    m=smf.wls("log_daily ~ log_rank + log_reach",sub,weights=sub.w).fit(cov_type="HC3")
    print("WEIGHTED log_daily ~ log_rank + log_reach |", "; ".join(f"{k}={m.params[k]:.3f} (p={m.pvalues[k]:.3f})" for k in ["log_rank","log_reach"]))
ok=d[d.entry_check=="OK"]
run(ok,"entries passing identity check (44, incl. main Before Today entry)")
allp=d[~((d.album=="Before Today")&(d.entry_check!="OK"))]
run(allp,"all 50 sampled albums incl. flagged")
