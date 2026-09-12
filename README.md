# Mobile Apps Market Gap Explorer

An interactive Streamlit project for exploring potential opportunities in the
mobile-app market. It brings Apple App Store and Google Play data into one
consistent analysis and helps users compare demand, satisfaction, engagement,
competition, pricing, and monetization patterns across app categories.

![Mobile Apps Market Gap Explorer](assets/mobile-market-hero.png)

## Overview

The project is designed for exploratory market research. Instead of treating a
large number of installs as proof of an opportunity, it looks at several signals
together:

- **Demand:** rating activity and Android install estimates
- **Satisfaction:** user ratings, including rating-count-weighted summaries
- **Engagement:** review activity relative to installs
- **Competition:** app counts and concentration among leading apps
- **Business model:** free/paid status, advertising, and in-app purchases

The analysis surfaces Food & Drink and Tools as categories worth further
validation, while using Communication as an example of a high-demand market with
stronger network, trust, and switching barriers. These are research hypotheses,
not guarantees of commercial opportunity.

## Features

- Combined exploration of iOS, Android, or both platforms
- Global filters for category, currency, price, and rating
- Interactive histograms, box plots, scatterplots, bar charts, pie charts, and
  sunburst charts
- Demand-versus-satisfaction and competition views
- Sensitivity checks across multiple demand and rating thresholds
- Cross-platform comparisons where fields are comparable
- Light and dark appearance modes
- Filtered-data previews and CSV downloads

## Analysis sections

The app follows a four-part decision framework:

1. **Popularity & Ratings** examines whether visible demand coincides with lower
   satisfaction and shows how much variation category averages can hide.
2. **Reviews & Competition** compares engagement and market concentration to
   distinguish large markets from realistically approachable ones.
3. **Checks & Limitations** tests whether candidate categories remain visible
   under different assumptions and across platforms.
4. **What to Do Next** summarizes the evidence and identifies follow-up research
   such as review-text analysis, competitor research, user interviews, prototype
   testing, and acquisition-cost estimates.

## Data

| File | Description |
| --- | --- |
| `data/ios_apps_clean.csv` | Cleaned Apple App Store records |
| `data/android_apps_clean.csv` | Cleaned Google Play records |
| `data/mobile_apps_unified.csv` | Harmonized cross-platform dataset used by the app |
| `data_quality_summary.json` | Source hashes, transformation details, and validation results |

The unified dataset contains 18,373 app records and includes fields such as
platform, category, price, currency, user rating, rating count, review count,
install estimates, monetization features, developer, and update date. Fields
that are unavailable or not comparable across platforms remain missing rather
than being inferred.

## Run locally

Python 3.10 or newer is recommended.

```bash
git clone https://github.com/BrianIsAwesome111/Mobile-Apps-Market-Gap.git
cd Mobile-Apps-Market-Gap
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit will display a local address, typically
`http://localhost:8501`. Open it in a browser to use the app.

## Repository structure

```text
Mobile-Apps-Market-Gap/
├── app.py                       # Streamlit application and chart logic
├── assets/                      # Interface illustrations
├── data/                        # Cleaned and unified datasets
├── data_quality_summary.json    # Cleaning and validation audit
├── requirements.txt             # Python dependencies
├── Procfile                     # Process declaration for hosting
└── README.md
```

## Interpretation and limitations

- Rating count is a proxy for relative popularity, not a direct count of active
  users, revenue, or unmet demand.
- Android install values are estimates expressed as ranges; equivalent install
  data is not available for iOS in this dataset.
- Android and iOS records may represent different collection periods.
- Price comparisons are only meaningful after accounting for currency.
- Missing ratings, reviews, or install values are retained as missing data.
- Store listings are observational data. Relationships in the charts do not
  establish causation or prove that a market gap exists.

The strongest use of this project is to generate better questions and a focused
shortlist for primary research—not to replace user interviews, competitive
analysis, product testing, or financial validation.
