# 9.2 and Forgotten: Analysis plan, Amendment 3

Written 12 November 2026, before full-length lists were collected or scored, and before any model comparing the Pitchfork sample with the comparison group was run.

## What had been seen when this was written

- Top-100 recognition counts for all 100 albums (Amendment 2 measure, scored 11 November): 8 of 50 Pitchfork albums and 0 of 50 comparison albums appear on at least one of the six main lists; 8 of 17 and 2 of 17 on the 2010s lists.
- Within-Pitchfork listening results from the pilot (rank and log daily listeners, with and without historical reach). Model 2 is therefore not a prospective test.
- Comparison-group Last.fm figures (captured 12 November), at the level of parse checks and July-break flags only. No comparison of groups was run.

## Why the plan changes

1. Restricting long lists to their top 100 was set by a website display limit, not by a view of what recognition is. An album at #125 of Rolling Stone's 500 has been recognised by that list.
2. The outcome is sparse (14 appearances in 300 Pitchfork album-list pairs; 0 in the comparison group), so the binomial models in section 3.2 are unstable and model 4 is completely separated.

## Recognition outcome

- Primary: appearance anywhere on the full published list, for the six main lists (Rolling Stone 500, 2020; Consequence 100, 2022; Paste 300, 2024; Guardian 100 of the 21st century, 2019; Rolling Stone 250 of the 21st century, 2025; Paste 250 of the 21st century, 2025).
- Secondary: appearance in a list's top 100 (strong consecration). Already scored and seen.
- If any list cannot be obtained in full, that list is scored on its top 100 and the primary outcome is renamed accordingly in the paper.
- Decade lists are all 101 entries or shorter and are unchanged.

## Models

Model 1 (Pitchfork sample, n = 50). Outcome: any appearance (binary). Firth penalised logistic regression on log year-end rank alone. UK chart weeks and release year are added one at a time as sensitivity checks, not together. Also: Spearman correlation between log rank and number of lists (0 to 6), with a permutation p-value (10,000 permutations).

Model 2 (Pitchfork sample). Log daily listeners on log rank, log all-time listeners and year, OLS with HC3 errors, design-weighted and unweighted. Already seen in the pilot; reported as such.

Model 3 (Pitchfork sample). Log daily listeners on any appearance (binary), log all-time listeners and UK chart weeks, OLS with HC3 errors. Number of lists replaces the binary as a sensitivity check.

Model 4 (both groups, n = 100). Any appearance by group: Fisher's exact test, overall and separately for each comparison source (NME only, Village Voice only, both). Firth logistic regression with group and UK chart weeks as a sensitivity check.

Model 5 (both groups). Log daily listeners on group, log all-time listeners and year, OLS with HC3 errors; also by comparison source.

All listening models are run with and without flagged Last.fm entries (6 Pitchfork, 7 comparison). Everything else is exploratory.
