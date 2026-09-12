# Mobile Apps Exploratory Assignment

This folder contains the completed AI-assisted portion of the assignment: an improved data-cleaning checklist, cleaned Apple App Store and Android datasets, a unified cross-platform table, a data-quality report, and a Streamlit app for exploratory graphs. The project investigates possible gaps in the mobile-app market by comparing demand signals with ratings, review activity, categories, and competition. Its Analysis section closes with a directional prioritization of Food & Drink and Tools while explaining the higher entry barriers in Communication.

## What the assignment is asking you to do

1. Review your original cleaning checklist, improve it, and preview the Markdown file in VS Code with **Command+Shift+V**.
2. Apply the checklist to the Apple App Store and Google Play datasets.
3. Build a Streamlit app with menu choices adapted to mobile-app data.
4. Include exploratory histograms, a box plot, scatterplot, pie chart, and sunburst chart. The categorical histogram includes a count/percent choice.
5. If time permits, add relevant visuals or Streamlit features. This app includes optional Android app-icon samples and CSV downloads.
6. Use the formal analysis section to interpret the evidence, state a directional conclusion, and distinguish measured signals from strategic judgment.

## Deliverables

- `DATA_CLEANING_CHECKLIST.md`: corrected and expanded checklist plus the cleaning results.
- `data/ios_apps_clean.csv`: cleaned iOS data.
- `data/android_apps_clean.csv`: cleaned Android data.
- `data/mobile_apps_unified.csv`: compact table used by the app.
- `data_quality_summary.json`: reproducible source hashes, transformations, and validation checks.
- `app.py`: Streamlit exploratory app with light/dark appearance controls, dataset selectors, images, filters, downloads, and chart builders.
- `assets/`: original hero and opportunity illustrations used by the polished interface.
- `requirements.txt`: Python dependencies.
- Navigation uses `streamlit-option-menu` for the sidebar sections and exploratory chart pages.

## Run the app

### Simplest method on a Mac

Double-click `Start Mobile App.command`. It creates a private Python environment, installs the required packages, and starts the app automatically. Keep the Terminal window open while using the app. Press **Control+C** in that Terminal window when you want to stop it.

If macOS blocks the launcher the first time, Control-click it, choose **Open**, and then choose **Open** again.

### VS Code or Terminal method

Open this folder in VS Code, then run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local address, usually `http://localhost:8501`. Open that address in a browser.

## Suggested submission workflow

1. Preview `DATA_CLEANING_CHECKLIST.md` in VS Code.
2. Run the Streamlit app and click through every menu option.
3. Try both iOS and Android, then the combined dataset.
4. Save screenshots only if your teacher asks for them.
5. Submit the project folder or the specific files requested by your teacher.

## Analysis structure

The analysis tests the thesis that a promising mobile-app opportunity may combine visible demand, weaker satisfaction, meaningful engagement, and a realistic path to entry. It is split into separate option-menu sections so each argument has room for its evidence and interpretation.

### Option-menu structure

The website uses plain-language navigation: Home, About the Study, How Data Was Prepared, View the Data, and Explore the Data. These are followed by four focused sections:

1. **Popularity & Ratings**
   - Validate rating count as a demand proxy with the existing rating-count-versus-installs scatterplot.
   - Add a demand–satisfaction quadrant scatterplot.
   - Compare category rating activity with weighted satisfaction.
   - Use box plots to show variation within Food & Drink, Tools, and Communication.

2. **Reviews & Competition**
   - Compare installs with reviews per 1,000 installs.
   - Compare category app counts with total rating activity.
   - Show whether demand is spread across many competitors or concentrated in a few leading apps.
   - Explain why Communication may have a higher entry barrier despite strong demand.

3. **Checks & Limitations**
   - Test whether the same candidate categories remain visible under different rating and demand thresholds.
   - Compare patterns across iOS and Android where comparable fields exist.
   - Add business-model context such as free-app share, advertising, and in-app purchases if useful.
   - Explain that rating count is a popularity proxy, not a direct measure of users, revenue, or unmet need.

4. **What to Do Next**
   - Present the Food & Drink and Tools recommendation briefly.
   - Compare them directly with Communication.
   - Distinguish measured evidence from strategic judgment.
   - End with next-stage validation: review-text analysis, competitor research, user interviews, prototype testing, and acquisition-cost estimates.

### Graphs to add or strengthen

| Analysis argument | Recommended graph | What it should show |
| --- | --- | --- |
| Demand–satisfaction mismatch | Log-scale scatterplot of estimated installs versus user rating, colored by category | High-demand apps or categories with weaker satisfaction |
| App-level opportunity | Quadrant scatterplot with demand on the x-axis and rating on the y-axis | High-demand/low-satisfaction candidates versus attractive, crowded, or weak markets |
| Low review activity | Scatterplot of maximum installs versus reviews per 1,000 installs | Adoption with comparatively weak observable engagement |
| Focused workflows in Food & Drink and Tools | Category bubble chart with rating activity versus weighted rating; bubble size = number of apps | Categories with meaningful demand and room for improvement |
| Communication’s entry barrier | Bar chart of app counts, rating concentration, or leading-app share by category | Whether demand is controlled by a small number of established competitors |
| Competition versus demand | Bubble chart of number of apps versus total rating count; bubble size = average rating | Large markets versus crowded or more approachable markets |
| Hidden variation within categories | Box plot of ratings by category | Whether category averages hide poorly performing subgroups or niches |
| Robustness of the recommendation | Sensitivity line or dot chart using multiple rating and demand thresholds | Whether Food & Drink and Tools remain candidates under reasonable assumptions |
| Cross-platform consistency | Grouped bar chart or dot plot comparing categories across iOS and Android | Whether a pattern is platform-specific or appears across ecosystems |
| Monetization context | Stacked bar chart of free/paid, advertising, and in-app-purchase shares | Business-model conditions surrounding the opportunity |
| Limits of the demand proxy | Existing rating-count-versus-installs graph with raw, log-scale, and rank correlations | Why rating count supports relative popularity comparisons but is not a user count |

The highest-priority chart is the demand–satisfaction quadrant scatterplot. It directly visualizes the thesis by separating high-demand/low-satisfaction candidates from high-demand/high-satisfaction markets. It uses a logarithmic demand axis, labels only selected candidates, and explains that the plot identifies hypotheses for validation rather than proving an unmet need.

Related graphs are grouped into the three analytical sections above, with the final section reserved for the concise recommendation. This gives the reader a clear progression: **Do users want it? Are they satisfied and engaged? Is the opportunity realistically enterable? What should be prioritized?**

## Important limitations

- The Android dataset includes scrape timestamps; the iOS dataset does not include a collection date. Cross-platform comparisons may therefore involve different collection periods.
- Android has genuine missing rating and install values. They remain missing rather than being replaced with invented values.
- Cross-platform price comparisons should use the currency filter.
- App-store records are observational data. The charts can show patterns but do not establish causation.
