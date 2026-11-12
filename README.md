# 9.2 and Forgotten? The Afterlife of Pitchfork's Classics: replication materials

Data, scripts and analysis plan for the article. Run every script from this folder with Python 3
(`python3 -m pip install pandas numpy scipy statsmodels`).

## Analysis plan
- `plan/analysis_plan_amendment3_2026-11-12.md` and `.sha256`: Amendment 3 (full-list recognition; Firth, Fisher and permutation tests). Deposited on OSF on 12 November 2026, after the analyses had been run; the OSF record documents the plan, not its timing.
- `plan/analysis_plan_amendment4_2026-11-12.md` and `.sha256`: Amendment 4 (recognition census of all 594 albums).
- `plan/working_plan_extract_2026-11-11.md`: the original protocol and five primary models, with Amendments 1 and 2 (11 November 2026), from the dated working plan.
- Check a hash with `shasum -a 256 plan/<file>.md` and compare with the `.sha256` file.

## Pipeline
| Step | Script | Output |
|---|---|---|
| 1 | scripts/01_frame_and_draw.py | data/pitchfork_frame_2006_2011.csv (frame, exclusions, seeded draw; seed 20261111) |
| 2 | scripts/02_comparison_pool.py | data/comparison_pool.csv (500 albums; 318 eligible) |
| 3 | scripts/03_comparison_draw.py | data/comparison_draw_order.csv |
| 4 | scripts/04_parse_lastfm_mhtml.py | parses saved Last.fm album pages |
| 5 | scripts/05_build_lastfm.py | data/lastfm_daily_listeners.csv, data/lastfm_summary.csv |
| 6 | scripts/06_analysis_pilot.py | pilot models (exploratory) |
| 7 | scripts/07_models_v2.py | data/model_results_v2.txt (the five models under Amendment 3) |
| 8 | scripts/08_wayback_exploratory.py | data/wayback_results.txt (exploratory before-and-after test, section 4.6) |
| 9 | scripts/09_wayback_table5.py | Table 5 rows; data/wayback_all_entries.csv |

Recognition census (Amendment 4): `data/lists_entries.py`, `data/match.py`, `data/score.py` produce `data/census_scored.csv` and `data/census_hits_final.csv` (every hit, checked by hand; manual corrections are listed in `score.py`).

## Exploratory listening analysis (section 4.6, Appendix A)
- `data/wayback_2012_audiences.json`: archived Last.fm listener count and capture date for each sampled album (Internet Archive Wayback Machine).
- `data/wayback_all_entries.csv`: every entry with 2012 count, capture date, 2026 listening, recognition, 2026 flag and exclusion reason.
- Exclusions: only capture after 2018 (3); split or duplicate entry (5); captured within weeks of release (2); no capture (1). Their timing relative to interim estimates is set out in Appendix A of the article.
- The main specification uses unflagged 2026 entries (n = 78). Each row of Table 5 changes one choice.

## Notes
- Last.fm data describe Last.fm users only. Saved Last.fm pages are not redistributed; the parsed values are.
- Retrospective list contents are included only as needed to reproduce matching; see the article's Table 1 for sources.

## Licence
Scripts (`scripts/` and the `.py` files in `data/`): MIT, see `LICENSE`.
Data and analysis plan: CC BY 4.0, see `LICENSE-DATA.md`.
