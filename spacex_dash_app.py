"""
SpaceX Falcon 9 interactive launch dashboard.
Run from repository root: python dashboard/spacex_dash_app.py
Install dependencies from requirements.txt first.
"""
from pathlib import Path
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "spacex_launch_dash.csv"
DATA_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"

if DATA_PATH.exists():
    df = pd.read_csv(DATA_PATH)
else:
    df = pd.read_csv(DATA_URL)
    DATA_PATH.parent.mkdir(exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

# Standardize common course column names if the source file differs slightly.
rename = {}
for col in df.columns:
    norm = col.lower().strip().replace("_", " ")
    if norm in ("launch site", "launchsite"): rename[col] = "Launch Site"
    elif norm in ("payload mass (kg)", "payloadmass", "payload mass"): rename[col] = "Payload Mass (kg)"
    elif norm in ("class", "landing success"): rename[col] = "class"
    elif norm in ("booster version category", "booster version"): rename[col] = "Booster Version Category"
df = df.rename(columns=rename)
required = {"Launch Site", "Payload Mass (kg)", "class"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

df["Payload Mass (kg)"] = pd.to_numeric(df["Payload Mass (kg)"], errors="coerce")
df["class"] = pd.to_numeric(df["class"], errors="coerce")
df = df.dropna(subset=["Launch Site", "Payload Mass (kg)", "class"]).copy()
if "Booster Version Category" not in df.columns:
    df["Booster Version Category"] = "Unknown"

sites = sorted(df["Launch Site"].dropna().unique())
max_payload = max(10000, int(df["Payload Mass (kg)"].max() // 1000 + 1) * 1000)
app = Dash(__name__)
app.title = "SpaceX Falcon 9 Launch Dashboard"
app.layout = html.Div([
    html.H1("SpaceX Falcon 9 Launch Records Dashboard"),
    html.P("Explore landing outcomes by launch site and payload mass."),
    html.Label("Launch site"),
    dcc.Dropdown(
        id="site-dropdown",
        options=[{"label": "All Sites", "value": "ALL"}] +
                [{"label": s, "value": s} for s in sites],
        value="ALL", placeholder="Select a launch site here", searchable=True
    ),
    dcc.Graph(id="success-pie-chart"),
    html.Label("Payload mass range (kg)"),
    dcc.RangeSlider(
        id="payload-slider", min=0, max=max_payload, step=1000,
        marks={i: str(i) for i in range(0, max_payload + 1, max(1000, max_payload // 5))},
        value=[float(df["Payload Mass (kg)"].min()), float(df["Payload Mass (kg)"].max())]
    ),
    dcc.Graph(id="success-payload-scatter-chart"),
], style={"maxWidth": "1200px", "margin": "auto", "padding": "24px"})

@app.callback(Output("success-pie-chart", "figure"), Input("site-dropdown", "value"))
def update_pie(site):
    filtered = df if site == "ALL" else df[df["Launch Site"] == site]
    counts = filtered["class"].map({0: "Unsuccessful", 1: "Successful"}).value_counts()
    title = "Landing outcomes — all launch sites" if site == "ALL" else f"Landing outcomes — {site}"
    return px.pie(values=counts.values, names=counts.index, title=title,
                  color=counts.index, color_discrete_map={"Successful": "#2ca02c", "Unsuccessful": "#d62728"})

@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [Input("site-dropdown", "value"), Input("payload-slider", "value")]
)
def update_scatter(site, payload_range):
    filtered = df[(df["Payload Mass (kg)"] >= payload_range[0]) &
                  (df["Payload Mass (kg)"] <= payload_range[1])]
    if site != "ALL":
        filtered = filtered[filtered["Launch Site"] == site]
    filtered = filtered.copy()
    filtered["Landing outcome"] = filtered["class"].map({0: "Unsuccessful", 1: "Successful"})
    return px.scatter(filtered, x="Payload Mass (kg)", y="class",
                      color="Booster Version Category", symbol="Landing outcome",
                      hover_data=["Launch Site", "Landing outcome"],
                      title="Payload mass vs landing outcome",
                      labels={"class": "Landing outcome (0 = no, 1 = yes)"})

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=8050)
