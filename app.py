"""
Early Warning Risk Predictor - Streamlit app.
Run:  streamlit run app.py
"""
import json
from pathlib import Path

import altair as alt
import joblib
import pandas as pd
import streamlit as st

from features import PERIODS, clean_alerts, model1_inputs, model2_inputs, risk_level

BASE = Path(__file__).parent
DATA_FILE = BASE / "SaudiDCD_alerts.csv"
MODELS = BASE / "models"

PERIOD_HOURS = {"Night": "00:00 – 05:59", "Morning": "06:00 – 11:59",
                "Afternoon": "12:00 – 17:59", "Evening": "18:00 – 23:59"}
CLEAR_GAP = 0.05   # the model's period is shown only if it leads the next one by 5+ points
LEVEL_COLORS = {"High": "#D9480F", "Medium": "#F2A900", "Low": "#2F9E44"}

MIN_REGION_ALERTS = 10   # fewer past alerts than this -> use the most common time in all regions


def region_usual_time(alerts, region):
    """Most common time of day in the region's past alerts (two periods if they are tied within 5 points)."""
    past = alerts[alerts["Region"] == region]
    if len(past) < MIN_REGION_ALERTS:
        overall = alerts["period"].value_counts(normalize=True)
        return overall.index[0], (f"Only {len(past)} past alert(s) in {region}, so this is the most common time "
                                  f"in all regions ({overall.iloc[0]:.0%}).")
    share = past["period"].value_counts(normalize=True).reindex(PERIODS, fill_value=0).sort_values(ascending=False)
    if share.iloc[0] - share.iloc[1] < CLEAR_GAP:
        return (f"{share.index[0]} / {share.index[1]}",
                f"Most common times in {region}'s past alerts ({share.iloc[0]:.0%} and {share.iloc[1]:.0%}).")
    return share.index[0], f"Most common time in {region}'s past alerts ({share.iloc[0]:.0%})."


st.set_page_config(page_title="Early Warning Risk Predictor", page_icon="🛡️", layout="wide")


# ---------------- loading ----------------
@st.cache_resource
def load_models():
    model1 = joblib.load(MODELS / "model1_attack_tomorrow.joblib")
    model2 = joblib.load(MODELS / "model2_period.joblib")
    info = json.load(open(MODELS / "model_info.json"))
    return model1, model2, info


@st.cache_data
def load_alerts(file):
    return clean_alerts(pd.read_csv(file))


model1, model2, info = load_models()
regions = info["regions"]

# ---------------- sidebar ----------------
with st.sidebar:
    st.header("Data")
    uploaded = st.file_uploader("Updated tweets file (optional)", type="csv",
                                help="Same columns as SaudiDCD_alerts.csv. The models stay the same; "
                                     "only the recent activity used as input is updated.")
    alerts = load_alerts(uploaded if uploaded is not None else DATA_FILE)
    last_alert_day = alerts["date"].max().date()
    today = st.date_input("Data up to (today)", value=last_alert_day, min_value=last_alert_day,
                          help="Predictions are for the day after this date.")
    today = pd.Timestamp(today)
    tomorrow = today + pd.Timedelta(days=1)
    st.caption(f"{len(alerts)} alerts loaded · last alert on {last_alert_day:%d %b %Y}")
    st.caption(f"Models trained on data until {info['trained_until']}")

# ---------------- header ----------------
st.title("🛡️ Early Warning Risk Predictor")
st.markdown(f"Risk outlook for **{tomorrow:%A %d %B %Y}**, based on @SaudiDCD alerts up to "
            f"**{today:%d %B %Y}**.")
st.warning("This tool is a student project and **does not replace official warnings**. "
           "Always follow @SaudiDCD instructions.", icon="⚠️")

# ---------------- user inputs ----------------
col_a, col_b = st.columns(2)
with col_a:
    region = st.selectbox("Region", regions, index=regions.index("Riyadh") if "Riyadh" in regions else 0)
with col_b:
    school = st.radio(f"Is school in-person tomorrow in {region}?", ["No (remote / no school)", "Yes (in-person)"],
                      horizontal=True)
school_value = 1 if school.startswith("Yes") else 0
if tomorrow.day_name() in info["weekend"] and school_value == 1:
    st.info(f"Tomorrow is {tomorrow.day_name()} (weekend), so there is usually no school.")

# ---------------- predictions ----------------
x1 = model1_inputs(alerts, regions, today)[info["m1_features"]]
risk = pd.Series(model1.predict_proba(x1)[:, 1], index=regions)

x2 = model2_inputs(alerts, [region], today, {region: school_value})[info["m2_features"]]
period_probs = pd.Series(model2.predict_proba(x2)[0], index=model2.classes_).reindex(PERIODS)
likely_period = model2.predict(x2)[0]

clear_minutes = alerts.groupby("Region")["duration_min"].median().round(1)

# ---------------- three outputs ----------------
st.subheader(f"{region}: tomorrow")
c1, c2, c3 = st.columns(3)
level = risk_level(risk[region])
with c1:
    st.markdown("**1 · Tomorrow's risk**")
    st.markdown(f"<h1 style='color:{LEVEL_COLORS[level]};margin:0'>{risk[region]:.0%}</h1>",
                unsafe_allow_html=True)
    st.markdown(f"Level: **<span style='color:{LEVEL_COLORS[level]}'>{level}</span>**", unsafe_allow_html=True)
    st.caption(f"{int(x1.loc[region, 'region_alerts_last_7d'])} alerts in the last 7 days")
with c2:
    st.markdown("**2 · Most likely time (if an alert happens)**")
    top_two = period_probs.sort_values(ascending=False)
    if top_two.iloc[0] - top_two.iloc[1] >= CLEAR_GAP:
        st.markdown(f"<h1 style='margin:0'>{likely_period}</h1>", unsafe_allow_html=True)
        st.caption(f"{PERIOD_HOURS[likely_period]} · {top_two.iloc[0]:.0%} chance")
    else:
        # The model has no clear time: fall back to the region's own most common time in past alerts
        label, note = region_usual_time(alerts, region)
        st.markdown(f"<h1 style='margin:0'>{label}</h1>", unsafe_allow_html=True)
        st.caption(f"{note} The model found no clear time for tomorrow "
                   f"(all periods {top_two.min():.0%}–{top_two.max():.0%}).")
with c3:
    st.markdown("**3 · Usual time until danger clears**")
    minutes = clear_minutes.get(region)
    st.markdown(f"<h1 style='margin:0'>{minutes:g} min</h1>" if pd.notna(minutes) else "<h1>–</h1>",
                unsafe_allow_html=True)
    st.caption("Median of past alerts in this region")

past_share = (alerts[alerts["Region"] == region]["period"].value_counts(normalize=True)
              .reindex(PERIODS, fill_value=0))
n_past = int((alerts["Region"] == region).sum())
st.caption(f"Model's chance of each time of day tomorrow, next to the share of past alerts in {region} "
           f"({n_past} alerts) for context.")
probs = pd.concat([
    period_probs.rename("Share").reset_index().rename(columns={"index": "Period"}).assign(Source="Model (tomorrow)"),
    past_share.rename("Share").reset_index().rename(columns={"period": "Period", "index": "Period"}).assign(Source=f"Past alerts in {region}"),
])
st.altair_chart(
    alt.Chart(probs).mark_bar().encode(
        x=alt.X("Period:N", sort=PERIODS, title=None),
        xOffset=alt.XOffset("Source:N"),
        y=alt.Y("Share:Q", axis=alt.Axis(format="%"), title=None),
        color=alt.Color("Source:N", scale=alt.Scale(range=["#1C7ED6", "#CED4DA"]), legend=alt.Legend(orient="top", title=None)),
        tooltip=["Source", "Period", alt.Tooltip("Share:Q", format=".0%")],
    ).properties(height=240),
    use_container_width=True,
)

# ---------------- all regions ----------------
st.subheader("All regions: tomorrow's risk")
overview = pd.DataFrame({
    "Region": regions,
    "Risk": risk.values,
    "Level": [risk_level(p) for p in risk.values],
    "Alerts last 7 days": x1["region_alerts_last_7d"].astype(int).values,
}).sort_values("Risk", ascending=False)
st.altair_chart(
    alt.Chart(overview).mark_bar().encode(
        y=alt.Y("Region:N", sort="-x", title=None),
        x=alt.X("Risk:Q", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 1]), title="Chance of an alert tomorrow"),
        color=alt.Color("Level:N", scale=alt.Scale(domain=list(LEVEL_COLORS), range=list(LEVEL_COLORS.values()))),
        tooltip=["Region", alt.Tooltip("Risk:Q", format=".0%"), "Level", "Alerts last 7 days"],
    ).properties(height=300),
    use_container_width=True,
)

# ---------------- about ----------------
with st.expander("How it works and its limits"):
    st.markdown(f"""
- **Tomorrow's risk:** Random Forest trained on each region's recent activity (alerts today, in the last 3 and 7 days,
  days since the last alert, average alert duration) and whether tomorrow is a weekend.
  On the test weeks it caught **78%** of attack days, about twice a simple "attack today → attack tomorrow" rule.
  **Levels:** High ≥ 50% (the model's alarm), Medium 35–49%, Low below 35%.
- **Most likely time:** Logistic Regression using the region, weekend, the school answer you give, the period of the
  region's previous alert and its recent activity. It is a **hint, not a certainty**: it was right 41% of the time on
  the test weeks (4 periods), and most of its skill comes from the school information. When the model has no clear time
  (its top period leads by less than 5 points, as on most remote-school days), the app shows the region's own **most
  common time in past alerts** and says so (two periods if they are tied; all regions together if the region has
  fewer than 10 past alerts).
- **Time until danger clears:** median duration of past alerts in the region (statistics, no model).
- **Limits:** about 71 days of data; many false alarms; patterns shift over time. The models were trained on data
  until {info['trained_until']}; uploading a newer tweets file updates the inputs, not the models.
""")
