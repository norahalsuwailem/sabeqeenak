"""
features.py - turns the raw @SaudiDCD tweets into the inputs our two models expect.
The logic is the same as in the notebook (sections 2.3, 4.1 and 4.3), so the app
predicts exactly like the evaluated models.
"""
import numpy as np
import pandas as pd

START_DATE = "2026-09-01"            # first day of data collection
WEEKEND = ["Friday", "Saturday"]     # Saudi weekend
PERIODS = ["Night", "Morning", "Afternoon", "Evening"]


def period_of(hour):
    if hour < 6:
        return "Night"        # 00:00-05:59
    elif hour < 12:
        return "Morning"      # 06:00-11:59
    elif hour < 18:
        return "Afternoon"    # 12:00-17:59
    else:
        return "Evening"      # 18:00-23:59


def clean_alerts(raw):
    """Raw tweets -> one row per alert, paired with its 'clear' tweet."""
    raw = raw.copy()
    raw["datetime"] = pd.to_datetime(raw["Date"] + " " + raw["Time"])
    raw = raw.dropna(subset=["Alert_ID"])                      # clear tweets with no matching alert
    alerts = raw[raw["Tweet_Type"] == "Alert"].copy()
    clears = (raw[raw["Tweet_Type"] == "Clear"][["Alert_ID", "datetime"]]
              .rename(columns={"datetime": "clear_datetime"}))
    alerts = alerts.merge(clears, on="Alert_ID", how="left")
    alerts["duration_min"] = (alerts["clear_datetime"] - alerts["datetime"]).dt.total_seconds() / 60
    alerts["date"] = alerts["datetime"].dt.normalize()
    alerts["hour"] = alerts["datetime"].dt.hour
    alerts["period"] = alerts["hour"].apply(period_of)
    return alerts.sort_values("datetime").reset_index(drop=True)


def model1_inputs(alerts, regions, today):
    """Model 1 features for every region on `today` (they predict the risk for the next day)."""
    today = pd.Timestamp(today).normalize()
    tomorrow = today + pd.Timedelta(days=1)
    past = alerts[alerts["date"] <= today]
    rows = []
    for region in regions:
        r = past[past["Region"] == region]
        last_3d = r[r["date"] > today - pd.Timedelta(days=3)]
        last_7d = r[r["date"] > today - pd.Timedelta(days=7)]
        if len(r):
            days_since = (today - r["date"].max()).days
        else:
            days_since = (today - pd.Timestamp(START_DATE)).days + 1
        rows.append({
            "region_alerts_today": int((r["date"] == today).sum()),
            "region_alerts_last_3d": len(last_3d),
            "region_alerts_last_7d": len(last_7d),
            "region_days_since_last": days_since,
            "region_avg_duration_7d": round(last_7d["duration_min"].mean(), 1) if len(last_7d) else 0.0,
            "tomorrow_is_weekend": int(tomorrow.day_name() in WEEKEND),
            "Region": region,
        })
    return pd.DataFrame(rows, index=regions)


def model2_inputs(alerts, regions, today, school_in_person):
    """Model 2 features for the alerts of the next day. Only days up to `today` are used.
    school_in_person: dict {region: 0 or 1}, given by the user."""
    today = pd.Timestamp(today).normalize()
    tomorrow = today + pd.Timedelta(days=1)
    rows = []
    for region in regions:
        earlier = alerts[(alerts["Region"] == region) & (alerts["date"] <= today)]
        if len(earlier):
            last = earlier.iloc[-1]
            prev_period, days_since = last["period"], (tomorrow - last["date"]).days
        else:
            prev_period, days_since = "First", (tomorrow - pd.Timestamp(START_DATE)).days
        rows.append({
            "Region": region,
            "is_weekend": int(tomorrow.day_name() in WEEKEND),
            "school_in_person": int(school_in_person.get(region, 0)),
            "prev_period_region": prev_period,
            "region_days_since_prev": days_since,
            "region_alerts_prev_7d": int((earlier["date"] >= tomorrow - pd.Timedelta(days=7)).sum()),
        })
    return pd.DataFrame(rows, index=regions)


def risk_level(prob):
    """Probability of an attack tomorrow -> level shown in the app.
    High = the model's own alarm (>= 50%)."""
    if prob >= 0.50:
        return "High"
    elif prob >= 0.35:
        return "Medium"
    return "Low"
