# 9.2 and Forgotten? Working analysis plan (extract), November 2026

This file reproduces, word for word, the recognition protocol and the analysis plan as recorded in the
project's dated working document, including Amendments 1 and 2 (both 11 November 2026, before any album
was scored). Paragraphs reporting data collected after these dates have been left out. The working
document's revision history holds the timestamps; it was not an external registration and should not be
read as preregistration. Amendments 3 and 4 are in the hashed files in this folder.

Note: the first amendment is headed "Amendment" in the working document; it is Amendment 1 in the article.

---

3.1 Recognition protocol
Protocol approved and frozen 11 November 2026, before any list was checked against any album. Genre source: Discogs (master release genre and style tags).
Without this measure the study is only asking whether Pitchfork rankings predict Last.fm activity. It is the priority, and the rules below are fixed before any list is checked against any album.
List set. Retrospective album lists by outlets other than Pitchfork, published 2018 to 2026, drawn from a published index of critics' lists (Acclaimed Music's source list, cross-checked against muzieklijstjes.nl) rather than found by searching for the albums. The candidate outlets and the index snapshot date are recorded before collection. Pitchfork's own later lists are recorded separately as institutional persistence and never enter the main measure.
Amendment, 11 November 2026 (before any album was scored). Acclaimed Music could not be reached (it returns a bot check), so the list set is built outlets-first instead. The outlet frame is the publications Metacritic tracks, the same universe of reviewers Schmutz and van Venrooij (2021) draw on: 92 outlets taken from the Metacritic publication listing pages that could be retrieved on 11 November 2026, plus NME, Uncut and Stereogum, which Metacritic tracks but which sat on listing pages that could not be retrieved, making 95 in all (outlet_frame.csv). Pitchfork is excluded as the institution under study, and Amazon as a retailer. Each outlet in the frame is then searched for ranked album lists published 2018 to 2026 (all-time, century, decade or genre), by outlet name and list type only, never by album. Outlets that published no such list simply contribute none. muzieklijstjes.nl is used as a cross-check for lists the search misses.
Amendment 2, 11 November 2026 (before any album was scored). Outlet websites mostly block automated reading, so list contents are taken from BestEverAlbums, which archives critics' lists by publication. Its public pages show at most the first 100 entries of any list. Recognition is therefore defined as appearing in the top 100 of a list (or anywhere on a list of 100 or fewer). This also puts lists of different lengths (100, 250, 500) on the same footing. For each outlet in the frame, its lists are found from BestEverAlbums' page for that publication and checked against a web search by outlet and list type, still never by album.

Eligibility, per album and list. A list counts in an album's denominator only if the album could have appeared on it:
Period. The album's release year falls inside the list's period. A best-of-the-2010s list can recognise only the 2010 and 2011 albums; a best-of-the-2000s list only 2006 to 2009.

Genre. A genre-restricted list (best indie, best hip-hop) counts only for albums in that genre. Each album's genre is coded from Discogs (the master release's genre and style tags) before list collection, blind to listening data.

Geography. A list restricted by nationality (best British albums) counts only for acts from that country.

Format. Album lists only; song and mixed lists are excluded.

Scores. Numerator (lists the album appears on) and denominator (lists it was eligible for) are kept separately and both distributions reported, because a share alone hides breadth: 1 of 4 and 8 of 40 are different kinds of recognition. The main model treats appearances as a binomial outcome out of eligible lists (beta-binomial if the data are overdispersed), so the denominator carries its own information. Two checks on outlet dependence: counting at outlet level (an album counts once per outlet, however many of its lists include it), and dropping one outlet at a time. A rank-weighted score, normalised by list length, is secondary.
Fixing the window problem. Decade lists for the 2000s mostly appeared in 2009, outside the window, so 2006 to 2009 albums have fewer eligible lists than 2010 and 2011 albums. The main measure therefore uses only list types open to every album in the sample: all-time and 21st-century lists. 2010s decade lists are analysed separately, for the 2010 and 2011 albums only, and genre lists are reported as a further breakdown.
Same rules for both groups. The Pitchfork sample and the comparison group are scored identically, against the same list set.

3.2 Analysis plan (specified during pilot development; amended 12 November)
The five primary models below were specified during pilot development, on 11 November 2026, before any list contents were scored. That order is recorded in this working document's revision history, not in an external registration, so it should not be read as preregistration. Two further qualifications: the within-Pitchfork listening results (model 2) had already been seen in the pilot (section 4.3), so model 2 is not a prospective test; and the author of the plan knew in general which sample albums are widely canonised. Each model carries at most three covariates. Everything else (Pitchfork review score, Metacritic rating and review count, US chart peak, genre, country of the act, label type) is exploratory and reported as such.
Within Pitchfork (50 albums; the rank analysis).
Recognition ~ log year-end rank + UK chart weeks (log) + year.

Current listening (log daily listeners) ~ log rank + log historical reach + year.

Current listening ~ recognition + log historical reach + UK chart weeks.

Pitchfork against the comparison group (100 albums; the institutional contrast).
Recognition ~ on a Pitchfork list + UK chart weeks (log) + year.

Current listening ~ on a Pitchfork list + log historical reach + year.

The two analyses stay separate: rank exists only inside Pitchfork's lists, and the comparison asks a different question. Models 4 and 5 are reported pooled and separately for NME-only and Village Voice comparison albums, and the pooled result is described as a comparison of configurations of recognition, not a clean institutional contrast. All models are run with and without flagged Last.fm entries, and models 2, 3 and 5 on both the pre-break and post-break windows (section 4.3).
