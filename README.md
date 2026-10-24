# IBM Applied Data Science Capstone — SpaceX Falcon 9

**Owner repository:** https://github.com/eunicewellis/IBM-SpaceX-Capstones

This project investigates whether historical Falcon 9 launch characteristics can help classify first-stage landing outcomes. It is an educational retrospective analysis, not an operational launch-safety tool.

## Project contents

| File | Purpose |
|---|---|
| `notebooks/01_data_collection_api.ipynb` | Collect raw launch records from the public SpaceX API |
| `notebooks/02_web_scraping.ipynb` | Inspect and archive tables from the Wikipedia launch history page |
| `notebooks/03_data_wrangling.ipynb` | Inspect data quality and prepare course datasets |
| `notebooks/04_eda_sql.ipynb` | SQL exploratory queries using SQLite / IPython SQL |
| `notebooks/05_eda_visualization.ipynb` | EDA plots and feature preparation |
| `notebooks/06_folium_launch_site_location.ipynb` | Launch site map and outcome markers |
| `notebooks/08_machine_learning_prediction.ipynb` | Compare classification models |
| `dashboard/spacex_dash_app.py` | Interactive Plotly Dash app |
| `data/` | Generated data outputs; course datasets may be downloaded by notebooks |
| `reports/` | Capstone report draft |

## Run locally

1. Create a virtual environment and install requirements:
   `python -m venv .venv`
   `source .venv/bin/activate` (macOS/Linux)
   `pip install -r requirements.txt`
2. Open notebooks in Jupyter and run each from top to bottom. Some original IBM notebooks use browser-only `js.fetch` and `piplite`; use the IBM Skills Network environment for those cells, or replace the fetch step with `pandas.read_csv(URL)` for local Jupyter.
3. Run the dashboard from repository root: `python dashboard/spacex_dash_app.py`. The dashboard downloads the course CSV if `data/spacex_launch_dash.csv` is not present.
4. Save generated charts, map HTML, dashboard screenshots, and model outputs into `reports/` before final submission.

## Important reproducibility notes

- The course datasets are fixed historical snapshots; the live SpaceX API and Wikipedia page can change.
- Do not merge datasets unless the key, join logic, and row counts are documented.
- `Class` is the course target label. Follow the course's landing outcome definitions consistently.
- Compare Logistic Regression, SVM, Decision Tree, and KNN. Report metrics only after running the notebook; do not treat results copied from another repository as your own measured output.
- Folium proximity calculations need sourced reference coordinates. Do not report coast/rail/highway distances unless actually calculated from documented coordinates.
- Some notebook cells may require adjustment if IBM changes source column names or runtime libraries.

## Submission checklist

- [ ] Run notebooks top-to-bottom and resolve errors.
- [ ] Add executed outputs and charts.
- [ ] Verify all source/data files and citations.
- [ ] Capture a dashboard screenshot and save the Folium map HTML.
- [ ] Update the report with actual measured results and this repository URL.
- [ ] Confirm this repository is public and the uploaded files are visible.
