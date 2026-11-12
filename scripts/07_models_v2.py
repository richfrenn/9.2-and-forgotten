"""9.2 and Forgotten: five fixed models per Amendment 3 (12 Nov 2026)."""
import csv, json, re, unicodedata, numpy as np, pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

D = 'data/'
rng = np.random.default_rng(20261112)

def norm(s):
    s = unicodedata.normalize('NFKD', str(s).lower()).replace('&', 'and')
    return re.sub(r'[^a-z0-9]', '', s)

# ---------- assemble ----------
rec = pd.read_csv(D + 'recognition_scores.csv')
chart = pd.read_csv('data/chart_data.csv'); chart['id'] = chart['row'] - 1
df = rec.merge(chart[['id', 'uk_peak', 'uk_weeks', 'us_peak']], on='id')

pf = pd.read_csv('data/lastfm_summary.csv')
pf = pf[pf.lastfm_url != "https://www.last.fm/music/Ariel+Pink's+Haunted+Graffiti/Before+Today"]
pf['k'] = pf.album.map(norm)
pf = pf.rename(columns={'total_listeners': 'alltime', 'daily_mean_14may_22jul': 'daily', 'daily_mean_sep_oct': 'daily_post'})
pf['flag'] = pf.entry_check.str.startswith('FLAG')
cp = pd.read_csv(D + 'lastfm_summary_comparison.csv')
cp['k'] = cp.album.map(norm)
cp = cp.rename(columns={'alltime_listeners': 'alltime', 'daily_pre_mean': 'daily', 'daily_post_mean': 'daily_post'})
cp['flag'] = cp.flag.notna() & (cp.flag.astype(str).str.len() > 3)
cp['source'] = cp.source_lists.map(lambda s: 'both' if ('NME' in s and 'VV' in s) else ('NME' if 'NME' in s else 'VV'))

df['k'] = df.album.map(norm)
P = df[df.group == 'Pitchfork'].merge(pf[['k', 'rank', 'band', 'alltime', 'daily', 'daily_post', 'flag']], on='k', how='left')
Cm = df[df.group == 'Comparison'].merge(cp[['k', 'source', 'alltime', 'daily', 'daily_post', 'flag']], on='k', how='left')
assert P['rank'].notna().all() and len(P) == 50, P[P['rank'].isna()].album.tolist()
assert Cm['daily'].notna().all() and len(Cm) == 50
P['source'] = 'Pitchfork'; P['weight'] = np.where(P.band == 'top10', 2.32, 8.72)
Cm['rank'] = np.nan; Cm['band'] = ''; Cm['weight'] = 1.0
A = pd.concat([P, Cm], ignore_index=True)
A['pitchfork'] = (A.group == 'Pitchfork').astype(int)
A['any_full'] = (A.main_full_hits > 0).astype(int)
A['any_top100'] = (A.main_top100_hits > 0).astype(int)
A['log_rank'] = np.log(A['rank'])
A['log_daily'] = np.log(A['daily'])
A['log_alltime'] = np.log(A['alltime'])
A['log_ukw'] = np.log1p(A['uk_weeks'].fillna(0))
A.to_csv('data/analysis_dataset.csv', index=False)
P = A[A.group == 'Pitchfork'].copy()

out = []
def say(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)

# ---------- Firth logistic ----------
def firth(y, X, names, maxit=200):
    y = np.asarray(y, float); X = np.column_stack([np.ones(len(y))] + [np.asarray(x, float) for x in X])
    b = np.zeros(X.shape[1])
    def pll(b):
        p = 1 / (1 + np.exp(-X @ b)); W = p * (1 - p)
        I = X.T @ (X * W[:, None])
        return np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)) + 0.5 * np.linalg.slogdet(I)[1]
    for _ in range(maxit):
        p = 1 / (1 + np.exp(-X @ b)); W = p * (1 - p)
        I = X.T @ (X * W[:, None]); Ii = np.linalg.inv(I)
        h = np.einsum('ij,jk,ik->i', X * np.sqrt(W)[:, None], Ii, X * np.sqrt(W)[:, None])
        U = X.T @ (y - p + h * (0.5 - p))
        step = Ii @ U
        while pll(b + step) < pll(b) - 1e-10: step /= 2
        b = b + step
        if np.max(np.abs(step)) < 1e-8: break
    se = np.sqrt(np.diag(Ii)); L = pll(b)
    res = {}
    from scipy.optimize import minimize
    for j in range(1, X.shape[1]):  # profile penalised LR test (full-model penalty, b_j fixed at 0)
        idx = [k for k in range(X.shape[1]) if k != j]
        def negp(bb):
            full = np.zeros(X.shape[1]); full[idx] = bb
            return -pll(full)
        r0 = minimize(negp, b[idx], method='BFGS')
        chi = 2 * (L + r0.fun); pv = stats.chi2.sf(max(chi, 0), 1)
        res[names[j - 1]] = (b[j], se[j], np.exp(b[j]), np.exp(b[j] - 1.96 * se[j]), np.exp(b[j] + 1.96 * se[j]), pv)
    return res

def show_firth(title, res):
    say(title)
    for k, (b, se, OR, lo, hi, p) in res.items():
        say(f'   {k}: b={b:.3f} (SE {se:.3f}), OR={OR:.2f} [{lo:.2f}, {hi:.2f}], penalised LR p={p:.3f}')

def perm_spearman(x, y, n=10000):
    r = stats.spearmanr(x, y).correlation
    null = np.array([stats.spearmanr(x, rng.permutation(y)).correlation for _ in range(n)])
    return r, (np.sum(np.abs(null) >= abs(r)) + 1) / (n + 1)

def ols(formula, data, w=None):
    m = (smf.wls(formula, data, weights=w) if w is not None else smf.ols(formula, data)).fit(cov_type='HC3')
    return m

def show_ols(title, m, terms):
    say(title + f'  (n={int(m.nobs)}, R2={m.rsquared:.2f})')
    for t in terms:
        say(f'   {t}: {m.params[t]:.3f} (HC3 SE {m.bse[t]:.3f}), p={m.pvalues[t]:.3f}, 95% CI [{m.conf_int().loc[t,0]:.3f}, {m.conf_int().loc[t,1]:.3f}]')

say('=== DESCRIPTIVES ===')
for g, G in A.groupby('group'):
    say(f'{g}: any full-list appearance {G.any_full.sum()}/50; appearances {G.main_full_hits.sum()}/300; any top-100 {G.any_top100.sum()}/50')
for s, G in Cm.assign(any_full=(Cm.main_full_hits > 0)).groupby('source'):
    say(f'   comparison source {s}: n={len(G)}, any full-list appearance {G.any_full.sum()}')

say('\n=== MODEL 1 (Pitchfork, n=50): recognition ~ year-end rank ===')
show_firth('Firth logit, any full-list appearance ~ log rank', firth(P.any_full, [P.log_rank], ['log_rank']))
show_firth('  + UK chart weeks (log1p)', firth(P.any_full, [P.log_rank, P.log_ukw], ['log_rank', 'log_ukw']))
show_firth('  + release year', firth(P.any_full, [P.log_rank, P.year - 2006], ['log_rank', 'year']))
r, p = perm_spearman(P.log_rank.values, P.main_full_hits.values)
say(f'Spearman log rank vs number of lists (0-6): rho={r:.3f}, permutation p={p:.4f}')
say('Secondary (top-100 measure):')
show_firth('Firth logit, any top-100 appearance ~ log rank', firth(P.any_top100, [P.log_rank], ['log_rank']))
r, p = perm_spearman(P.log_rank.values, P.main_top100_hits.values)
say(f'Spearman log rank vs number of top-100 appearances: rho={r:.3f}, permutation p={p:.4f}')
say('By band: ' + ', '.join(f'{b}: {G.any_full.sum()}/{len(G)} any, {G.main_full_hits.sum()} appearances' for b, G in P.groupby('band')))

say('\n=== MODEL 2 (Pitchfork): log daily listeners ~ log rank + log all-time listeners + year ===')
for lab, d in [('unflagged (n=44)', P[~P.flag]), ('all 50', P)]:
    show_ols(f'OLS HC3, {lab}', ols('log_daily ~ log_rank + log_alltime + C(year)', d), ['log_rank', 'log_alltime'])
    show_ols(f'WLS design-weighted, {lab}', ols('log_daily ~ log_rank + log_alltime + C(year)', d, d.weight), ['log_rank'])

say('\n=== MODEL 3 (Pitchfork): log daily ~ recognition + log all-time + UK chart weeks ===')
for lab, d in [('unflagged (n=44)', P[~P.flag]), ('all 50', P)]:
    show_ols(f'OLS HC3, any full-list appearance, {lab}', ols('log_daily ~ any_full + log_alltime + log_ukw', d), ['any_full', 'log_alltime', 'log_ukw'])
    show_ols(f'   sensitivity: number of lists, {lab}', ols('log_daily ~ main_full_hits + log_alltime + log_ukw', d), ['main_full_hits'])

say('\n=== MODEL 4 (n=100): recognition ~ on a Pitchfork list ===')
def fisher(a, b):
    t = [[a.sum(), len(a) - a.sum()], [b.sum(), len(b) - b.sum()]]
    o, p = stats.fisher_exact(t); return t, p
Pa = A[A.group == 'Pitchfork'].any_full
for s in ['all', 'NME', 'VV', 'both']:
    Ca = A[(A.group == 'Comparison') & ((A.source == s) | (s == 'all'))].any_full
    t, p = fisher(Pa, Ca)
    say(f'Fisher exact, Pitchfork vs comparison ({s}): {t}, two-sided p={p:.2g}')
t, p = fisher(A[A.group == 'Pitchfork'].any_top100, A[A.group == 'Comparison'].any_top100)
say(f'Secondary, top-100: {t}, p={p:.2g}')
show_firth('Firth logit, any full-list appearance ~ Pitchfork + UK chart weeks (log1p)', firth(A.any_full, [A.pitchfork, A.log_ukw], ['pitchfork', 'log_ukw']))
show_firth('Firth logit, any full-list appearance ~ Pitchfork (alone)', firth(A.any_full, [A.pitchfork], ['pitchfork']))

say('\n=== MODEL 5 (n=100): log daily ~ on a Pitchfork list + log all-time + year ===')
for lab, d in [('unflagged (n=87)', A[~A.flag.astype(bool)]), ('all 100', A)]:
    show_ols(f'OLS HC3, {lab}', ols('log_daily ~ pitchfork + log_alltime + C(year)', d), ['pitchfork', 'log_alltime'])
for s in ['NME', 'VV']:
    d = A[(~A.flag.astype(bool)) & ((A.group == 'Pitchfork') | (A.source == s))]
    show_ols(f'   by source: Pitchfork vs {s} only, unflagged', ols('log_daily ~ pitchfork + log_alltime + C(year)', d), ['pitchfork'])
d = A[~A.flag.astype(bool)]
show_ols('   check: post-break window (Sep-Oct), unflagged', ols('np.log(daily_post) ~ pitchfork + log_alltime + C(year)', d), ['pitchfork'])

say('\n=== DECADE MEASURE (descriptive; 2010-11 albums) ===')
for g, G in A[A.year >= 2010].groupby('group'):
    say(f'{g}: n={len(G)}, any {int((G.decade_hits > 0).sum())}, appearances {int(G.decade_hits.sum())} of {len(G)*11}')

open('data/model_results_v2.txt', 'w').write('\n'.join(out))
