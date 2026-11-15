"""
make_data.py - builds docs/presentation/a/data.js from the project files, so every number in the
presentation comes from the data (nothing typed by hand except the model scores, copied from the notebook).

Run from the repository root:   python docs/presentation/make_data.py
"""
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from features import clean_alerts          # noqa: E402
import v2_ui as ui                          # noqa: E402

AR = {"Asir": "عسير", "Najran": "نجران", "Riyadh": "الرياض", "Jazan": "جازان", "Eastern Province": "الشرقية",
      "Makkah": "مكة المكرمة", "Madinah": "المدينة المنورة", "Tabuk": "تبوك"}

raw = pd.read_csv(ROOT / "SaudiDCD_alerts.csv")
a = clean_alerts(raw)
info = json.load(open(ROOT / "models" / "model_info.json"))
start = pd.Timestamp(info["start_date"])
end = pd.Timestamp(info["trained_until"])
days = (end - start).days + 1

counts = a["Region"].value_counts()
regions = list(counts.index)
med = a.groupby("Region")["duration_min"].median()
daily = a.groupby(a["datetime"].dt.normalize()).size().reindex(pd.date_range(start, end), fill_value=0)
period = a["period"].value_counts(normalize=True)

data = {
    "start": start.strftime("%Y-%m-%d"),
    "days": days,
    "tweets": int(len(raw)),
    "alerts": int((raw["Tweet_Type"].str.strip().str.lower() == "alert").sum()),
    "clears": int((raw["Tweet_Type"].str.strip().str.lower() == "clear").sum()),
    "n_regions": int(a["Region"].nunique()),
    "alert_days": int((daily > 0).sum()),
    "median_all": float(a["duration_min"].median()),
    "period_share": {p: round(float(period.get(p, 0)) * 100, 1) for p in ["Night", "Morning", "Afternoon", "Evening"]},
    "daily": [int(x) for x in daily.values],
    "regions": [{"key": r, "name": AR[r], "count": int(counts[r]), "share": round(counts[r] / len(a) * 100, 1),
                 "median": float(med[r]), "lat": ui.COORDS[r][0], "lon": ui.COORDS[r][1],
                 "side": ui.LABEL_SIDE.get(r, ("r", 0))[0], "dy": ui.LABEL_SIDE.get(r, ("r", 0))[1]} for r in regions],
    "events": [[int((x.datetime - start).total_seconds() // 60), regions.index(x.Region), float(x.duration_min)]
               for x in a.sort_values("datetime").itertuples()],
    "outline": ui.KSA_OUTLINE,
    # model scores on the test weeks (20 Oct - 9 Nov 2026), from the notebook, section 6
    "results": {
        "m1": {"model": "Random Forest", "recall": [0.78, 0.37], "f1": [0.47, 0.37], "auc": [0.65, 0.57], "precision": [0.33, 0.38]},
        "m2": {"model": "Logistic Regression", "acc": [0.41, 0.22], "f1": [0.37, 0.21], "no_school": {"acc": 0.26, "f1": 0.22}},
    },
}
out = Path(__file__).parent / "a" / "data.js"
out.write_text("window.SBQ = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
print("wrote", out, "-", data["alerts"], "alerts,", data["alert_days"], "alert days of", days)
