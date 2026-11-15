"""
سابقينك - animated Arabic version of app.py (same models, same logic).
Run:  streamlit run app_v2.py
"""
import json
import math
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from features import PERIODS, clean_alerts, model1_inputs, model2_inputs, risk_level
import v2_ui as ui

BASE = Path(__file__).parent
DATA_FILE = BASE / "SaudiDCD_alerts.csv"
MODELS = BASE / "models"

PERIOD_HOURS = {"Night": "00:00 – 05:59", "Morning": "06:00 – 11:59",
                "Afternoon": "12:00 – 17:59", "Evening": "18:00 – 23:59"}
PERIOD_ICON = {"Night": "🌙", "Morning": "🌅", "Afternoon": "☀️", "Evening": "🌆"}
PERIOD_COLOR = {"Night": "#7B6CF6", "Morning": "#FFC233", "Afternoon": "#FF8A3D", "Evening": "#E8590C"}
PERIOD_MID = {"Night": 3, "Morning": 9, "Afternoon": 15, "Evening": 21}
CLEAR_GAP = 0.05          # the model's period is shown only if it leads the next one by 5+ points
MIN_REGION_ALERTS = 10    # fewer past alerts than this -> use the most common time in all regions

st.set_page_config(page_title="سابقينك", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

# ---------------------------------------------------------------- language

AR_REGION = {"Asir": "عسير", "Najran": "نجران", "Riyadh": "الرياض", "Jazan": "جازان", "Eastern Province": "الشرقية",
             "Makkah": "مكة المكرمة", "Madinah": "المدينة المنورة", "Tabuk": "تبوك"}
AR_PERIOD = {"Night": "الليل", "Morning": "الصباح", "Afternoon": "الظهر والعصر", "Evening": "المساء"}
AR_LEVEL = {"High": "مرتفع", "Medium": "متوسط", "Low": "منخفض"}

T = {
    "badge": ("Built on {n} official Civil Defense alerts", "مبني على {n} إنذار رسمي من الدفاع المدني"),
    "title": ("Sabeqeenak", "سابقينك"),
    "title2": ("Early Warning Risk Predictor", "متنبئ مخاطر الإنذار المبكر"),
    "type1": ("Will my region be alerted tomorrow?", "هل بيجي منطقتي إنذار بكرة؟"),
    "type2": ("At what time of day?", "وفي أي وقت من اليوم؟"),
    "type3": ("And how long until the danger clears?", "وكم ياخذ لين يزول الخطر؟"),
    "s_alerts": ("alerts collected", "إنذار تم جمعه"),
    "s_regions": ("regions", "مناطق"),
    "s_clear": ("usual time to all-clear", "المدة المعتادة للزوال"),
    "s_night": ("of alerts at night (00–06)", "من الإنذارات بالليل (12–6 ص)"),
    "min": ("min", "د"),
    "ph_h": ("Early-warning alert", "إنذار مبكر"),
    "ph_b": ("{r}: stay in a safe place until the all-clear.", "{r}: ابقَ في مكان آمن لين يُعلن زوال الخطر."),
    "ph_eta": ("Usually clears in ~{m} min", "عادةً يزول خلال ~{m} دقيقة"),
    "ph_ok_h": ("All clear", "زال الخطر"),
    "ph_ok_b": ("{r}: the alert is over.", "{r}: انتهى الإنذار."),
    "ph_demo": ("Simulation · not a real alert", "محاكاة · ليس إنذاراً حقيقياً"),
    "live": ("LIVE · latest alerts", "مباشر · آخر الإنذارات"),
    "threat_k": ("Tomorrow's risk level", "مستوى الخطر لبكرة"),
    "threat_p": ("chance of at least one alert", "احتمال إنذار واحد على الأقل"),
    "tab1": ("🎯  Tomorrow in my region", "🎯  بكرة في منطقتي"),
    "tab2": ("🗺️  All regions", "🗺️  كل المناطق"),
    "tab3": ("🛰️  Replay the alerts", "🛰️  إعادة تشغيل الإنذارات"),
    "tab4": ("📘  How it works", "📘  كيف يشتغل"),
    "sb_data": ("Data", "البيانات"),
    "sb_up": ("Updated tweets file (optional)", "ملف تغريدات محدّث (اختياري)"),
    "sb_up_h": ("Same columns as SaudiDCD_alerts.csv. The models stay the same; only the recent activity used as input is updated.",
                "نفس أعمدة SaudiDCD_alerts.csv. الموديلات ما تتغير، يتحدث بس النشاط الأخير اللي يدخل للموديل."),
    "sb_today": ("Data up to (today)", "البيانات لين (اليوم)"),
    "sb_today_h": ("Predictions are for the day after this date.", "التوقعات لليوم اللي بعد هالتاريخ."),
    "sb_loaded": ("{n} alerts loaded · last alert on {d}", "تم تحميل {n} إنذار · آخر إنذار {d}"),
    "sb_trained": ("Models trained on data until {d}", "الموديلات متدربة على بيانات لين {d}"),
    "outlook": ("Risk outlook for <b>{t}</b>, based on @SaudiDCD alerts up to <b>{d}</b>.",
                "توقعات <b>{t}</b>، مبنية على إنذارات @SaudiDCD لين <b>{d}</b>."),
    "warn": ("A student project · it does <b>not</b> replace official warnings. Always follow @SaudiDCD instructions.",
             "مشروع طلابي · <b>لا يغني</b> عن الإنذارات الرسمية. اتبع دائماً تعليمات @SaudiDCD."),
    "region": ("Region", "المنطقة"),
    "school": ("Is school in-person tomorrow in {r}?", "هل الدراسة حضورية بكرة في {r}؟"),
    "school_no": ("No (remote / no school)", "لا (عن بعد / ما فيه دراسة)"),
    "school_yes": ("Yes (in-person)", "نعم (حضوري)"),
    "weekend": ("Tomorrow is {d} (weekend), so there is usually no school.", "بكرة {d} (إجازة نهاية الأسبوع)، فغالباً ما فيه دراسة."),
    "h1": ("Tomorrow's risk", "خطر الغد"),
    "s1": ("Chance of at least one alert in {r}", "احتمال إنذار واحد على الأقل في {r}"),
    "f1": ("{n} alerts in the last 7 days · Random Forest", "{n} إنذار خلال آخر 7 أيام · Random Forest"),
    "h2": ("Most likely time (if an alert happens)", "الوقت الأرجح (لو صار إنذار)"),
    "s2_model": ("{p} · {h} · {c} chance", "{p} · <span dir='ltr'>{h}</span> · احتمال {c}"),
    "f2_model": ("Bars: model for tomorrow · thin: past alerts in {r} ({n})", "الأشرطة: توقع الموديل لبكرة · الرفيعة: إنذارات {r} السابقة ({n})"),
    "h3": ("Usual time until danger clears", "المدة المعتادة لزوال الخطر"),
    "s3": ("Median of past alerts in {r}", "وسيط الإنذارات السابقة في {r}"),
    "f3": ("Statistics from past alerts, no model", "إحصاء من الإنذارات السابقة، بدون موديل"),
    "cl": ("minutes", "دقيقة"),
    "iqr": ("Half of the alerts cleared in <b>{a}–{b}</b> min", "نص الإنذارات زالت خلال <b dir='ltr'>{a}–{b}</b> دقيقة"),
    "close": ("Close to {q} ({b}), so treat it as a hint", "قريب من {q} ({b})، فاعتبره تلميح"),
    "beats": ("{d} points above {q}, the most common time before", "أعلى من {q} (الأشيع سابقاً) بـ {d} نقاط"),
    "s2_hist": ("{p} · {h} · most common in {r} ({s})", "{p} · <span dir='ltr'>{h}</span> · الأشيع في {r} سابقاً ({s})"),
    "no_beat": ("The model's top, {q} ({b}), is only {d} points above it, so we keep the usual time",
                "أعلى توقع للموديل {q} ({b}) يزيد عليه بـ {d} نقاط بس، فنبقى على الوقت المعتاد"),
    "lh1": ("Model's chance for tomorrow", "احتمال الموديل لبكرة"),
    "lh2": ("┄ most common before", "┄ الأشيع سابقاً"),
    "hist_tag": ("most common before", "الأشيع سابقاً"),
    "mode_model": ("Model forecast", "توقع الموديل"),
    "mode_hist": ("Most common before ({s})", "الأشيع سابقاً ({s})"),
    "all_regions": ("All regions", "كل المناطق"),
    "past": ("past alerts: {s}", "سابقاً: {s}"),
    "slogan": ("The punishment is coming, Houthi", "العقاب قادم يا حوثي"),
    "act": ("Alert active", "الإنذار نشط"),
    "ok": ("✅ Usual all-clear", "✅ وقت الزوال المعتاد"),
    "few": ("Only {n} past alert(s) in {r}, so this is the most common time in all regions ({s}).",
            "فيه {n} إنذار بس في {r}، فهذا الوقت الأشيع في كل المناطق ({s})."),
    "tie": ("Most common times in {r}'s past alerts ({a} and {b}).", "الأوقات الأشيع في إنذارات {r} السابقة ({a} و {b})."),
    "usual": ("Most common time in {r}'s past alerts ({s}).", "الوقت الأشيع في إنذارات {r} السابقة ({s})."),
    "noclear": (" The model found no clear time for tomorrow (all periods {a}–{b}).",
                " الموديل ما لقى وقت واضح لبكرة (كل الفترات بين {a} و {b})."),
    "all_ttl": ("Chance of an alert tomorrow · ranked", "احتمال إنذار بكرة · مرتّبة"),
    "all_sub": ("{n} alerts in last 7 days", "{n} إنذار آخر 7 أيام"),
    "lvl_lbl": ("{l} (≥{v})", "{l} (≥{v})"),
    "rp_title": ("Every alert, in time order", "كل الإنذارات بترتيبها الزمني"),
    "rp_sub": ("Each pulse is a real Civil Defense alert from our dataset", "كل نبضة إنذار حقيقي من بياناتنا"),
    "rp_count": ("alerts so far", "إنذار لين الحين"),
    "rp_day": ("Day {d} of {n}", "اليوم {d} من {n}"),
    "rp_rank": ("Alerts by region", "الإنذارات حسب المنطقة"),
    "rp_log": ("Latest alerts", "آخر الإنذارات"),
    "rp_done": ("{n} alerts · {d} days · {r} regions", "{n} إنذار · {d} يوم · {r} مناطق"),
    "rp_hist": ("Alerts per day · click a day to jump", "الإنذارات لكل يوم · اضغط على أي يوم للانتقال"),
}

AR = True   # Arabic-only version (the English strings stay in T in case they are needed later)
DIR = "rtl" if AR else "ltr"
LOC = "ar-u-ca-gregory-nu-latn" if AR else "en-GB"


def t(key, **kw):
    return T[key][1 if AR else 0].format(**kw)


def rname(r):
    return AR_REGION.get(r, r) if AR else r


def pname(p):
    return AR_PERIOD.get(p, p) if AR else p


def lname(level):
    return AR_LEVEL[level] if AR else level


def html(s):
    st.markdown(s, unsafe_allow_html=True)


def fmt_day(d, weekday=False):
    """Date in the chosen language (Gregorian calendar, Latin digits)."""
    if not AR:
        return d.strftime("%A %d %B %Y") if weekday else d.strftime("%d %B %Y")
    months = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
    days = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
    s = f"{d.day} {months[d.month - 1]} {d.year}"
    return f"{days[d.dayofweek]} {s}" if weekday else s


# ---------------------------------------------------------------- page style (dark, glass, RTL aware)
html(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap');
html, body, .stMarkdown, button, input, label, p, span, div {{font-family:'Inter','IBM Plex Sans Arabic',system-ui,sans-serif;}}
.stApp{{background:radial-gradient(1100px 600px at 85% -10%, rgba(232,12,56,.10), transparent 60%),
  radial-gradient(900px 600px at -10% 20%, rgba(220,70,145,.10), transparent 60%), #0C0D11 !important; color:#EBECEF;}}
header[data-testid="stHeader"]{{background:transparent;}}
.block-container{{padding-top:3rem !important; max-width:1260px;}}
iframe{{border-radius:24px;}}
.main .block-container, [data-testid="stMainBlockContainer"]{{direction:{DIR};}}
[data-testid="stWidgetLabel"] p, label p{{color:#EBECEF !important; font-weight:600;}}
.stSelectbox [role="group"], .stSelectbox div[data-baseweb="select"] > div{{background:#17181F !important; border-color:#31333D !important;}}
.stSelectbox input{{color:#EBECEF !important;}}
[role="listbox"], [role="listbox"] [role="option"]{{background:#1C1D25 !important; color:#EBECEF !important;}}
[role="listbox"] [role="option"]:hover, [role="listbox"] [role="option"][data-focused]{{background:#292B35 !important;}}
[data-testid="stButtonGroup"] button{{background:#1C1D25 !important; color:#EBECEF !important; border-color:#31333D !important;}}
[data-testid="stButtonGroup"] button[kind$="Active"], [data-testid="stButtonGroup"] button[aria-checked="true"]{{background:rgba(232,12,56,.18) !important; color:#F88493 !important; border-color:#E80C38 !important;}}
.stTabs [data-baseweb="tab-list"]{{gap:6px; border-bottom:1px solid #2A2D38;}}
.stTabs [role="tab"]{{padding:10px 16px; border-radius:12px 12px 0 0;}}
.stTabs [role="tab"] p{{color:#9FA1AC !important; font-size:1.02rem; font-weight:600;}}
.stTabs [role="tab"][aria-selected="true"] p{{color:#F88493 !important;}}
.stTabs [data-baseweb="tab-highlight"]{{background:#E80C38 !important;}}
section[data-testid="stSidebar"]{{background:#121319 !important; border-inline-end:1px solid #2A2D38;}}
section[data-testid="stSidebar"] *{{color:#EBECEF;}}
[data-testid="stFileUploaderDropzone"]{{background:#17181F !important; border:1px dashed #383B47 !important;}}
[data-testid="stFileUploaderDropzone"] button{{background:#1C1D25 !important; color:#EBECEF !important; border:1px solid #383B47 !important;}}
[data-testid="stDateInput"] *{{background-color:#17181F !important; color:#EBECEF !important; border-color:#31333D !important;}}
div[data-testid="stVerticalBlockBorderWrapper"]{{background:linear-gradient(165deg,#1D1F28,#171920) !important; border-color:#2F313C !important; border-radius:22px !important;}}
.g-line{{direction:{DIR}; display:flex; flex-wrap:wrap; gap:12px; align-items:center; justify-content:space-between; margin:6px 0 12px;}}
.g-out{{font-size:1.02rem; color:#CACCD3;}} .g-out b{{color:#fff;}}
.g-warn{{display:inline-flex; gap:8px; align-items:center; font-size:.86rem; color:#FBACB7; background:rgba(255,51,92,.08);
  border:1px solid rgba(255,51,92,.3); border-radius:999px; padding:6px 14px;}}
.g-info{{direction:{DIR}; font-size:.9rem; color:#C2C8E2; background:rgba(132,142,192,.08); border:1px solid rgba(132,142,192,.3);
  border-radius:14px; padding:8px 14px; margin-top:6px;}}
.g-card{{direction:{DIR}; background:linear-gradient(165deg,#1D1F28,#171920); border:1px solid #2F313C; border-radius:22px; padding:22px 26px; color:#CACCD3; line-height:1.75;}}
.g-card h4{{color:#fff; margin:0 0 6px; font-size:1.05rem;}} .g-card b{{color:#F88493;}}
.g-card .sec{{padding:12px 0; border-bottom:1px solid #2A2D38;}} .g-card .sec:last-child{{border-bottom:none;}}
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;800;900&display=swap');
.stApp:before{{content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:repeating-linear-gradient(0deg, rgba(255,255,255,.018) 0 1px, transparent 1px 4px),
             radial-gradient(1200px 700px at 50% -20%, rgba(255,45,85,.10), transparent 60%);}}
/* tabs -> centered pill navigation */
.stTabs [data-baseweb="tab-list"], .stTabs [role="tablist"]{{gap:4px; border:1px solid #2A2D38 !important; background:#121319; border-radius:14px; padding:6px;
  width:fit-content; margin:8px auto 18px; box-shadow:0 10px 30px rgba(0,0,0,.35);}}
.stTabs [role="tablist"] > div:not([role="tab"]){{display:none !important;}}
.stTabs [data-baseweb="tab-border"], .stTabs [data-baseweb="tab-highlight"]{{display:none !important;}}
.stTabs [role="tab"]{{padding:8px 18px !important; border-radius:10px !important; transition:all .25s;}}
.stTabs [role="tab"] p{{font-family:'Cairo','IBM Plex Sans Arabic',sans-serif !important; font-size:1.02rem !important; font-weight:700 !important;}}
.stTabs [role="tab"][aria-selected="true"]{{background:linear-gradient(180deg,#FF2D55,#C9123A); box-shadow:0 6px 22px rgba(255,45,85,.35);}}
.stTabs [role="tab"][aria-selected="true"] p{{color:#fff !important;}}
.stTabs [role="tab"]:hover p{{color:#fff !important;}}
/* region pills */
[data-testid="stButtonGroup"] button{{border-radius:10px !important; padding:6px 14px !important; font-weight:600 !important;}}
[data-testid="stWidgetLabel"] p{{font-family:'Cairo','IBM Plex Sans Arabic',sans-serif !important; font-size:1rem !important; color:#FF8FA3 !important; letter-spacing:.2px;}}
/* threat banner */
.threat{{direction:{DIR}; position:relative; display:grid; grid-template-columns:auto 1fr auto; gap:26px; align-items:center;
  margin:10px 0 18px; padding:16px 24px; border-radius:14px; overflow:hidden;
  background:linear-gradient(90deg, color-mix(in srgb, var(--lv) 16%, #15161C), #15161C 60%); border:1px solid color-mix(in srgb, var(--lv) 45%, #2A2D38);}}
.threat:before{{content:""; position:absolute; inset-block:0; inset-inline-start:0; width:4px; background:var(--lv); box-shadow:0 0 18px var(--lv);}}
.th-a{{display:flex; gap:14px; align-items:center;}}
.th-dot{{width:14px; height:14px; border-radius:50%; background:var(--lv); box-shadow:0 0 0 0 var(--lv); animation:thp 1.4s infinite;}}
@keyframes thp{{0%{{box-shadow:0 0 0 0 color-mix(in srgb, var(--lv) 70%, transparent)}}70%{{box-shadow:0 0 0 14px transparent}}100%{{box-shadow:0 0 0 0 transparent}}}}
.th-k{{font-size:.82rem; color:#9FA1AC;}} .th-r{{font-family:'Cairo',sans-serif; font-size:1.7rem; font-weight:900; color:#fff; line-height:1.15;}}
.th-m{{display:flex; gap:5px; align-items:flex-end; height:34px; direction:{DIR};}}
.th-m i{{flex:1; height:100%; border-radius:3px; background:#24262F; transform-origin:bottom;}}
.th-m i.on{{background:var(--lv); box-shadow:0 0 10px color-mix(in srgb, var(--lv) 60%, transparent); animation:blk .5s ease-out both;}}
@keyframes blk{{from{{transform:scaleY(.2); opacity:.2}}to{{transform:none; opacity:1}}}}
.th-b{{text-align:end;}} .th-p{{font-family:Inter,sans-serif; font-size:2.6rem; font-weight:900; color:var(--lv); line-height:1; direction:ltr;}}
.th-l{{font-size:.82rem; color:#CACCD3; margin-top:4px;}}
@media (max-width:820px){{.threat{{grid-template-columns:1fr;}} .th-b{{text-align:start;}}}}
</style>""")


# ---------------------------------------------------------------- loading (same as app.py)
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

with st.sidebar:
    st.header(t("sb_data"))
    uploaded = st.file_uploader(t("sb_up"), type="csv", help=t("sb_up_h"))
    alerts = load_alerts(uploaded if uploaded is not None else DATA_FILE)
    last_alert_day = alerts["date"].max().date()
    today = st.date_input(t("sb_today"), value=last_alert_day, min_value=last_alert_day, help=t("sb_today_h"))
    today = pd.Timestamp(today)
    tomorrow = today + pd.Timedelta(days=1)
    st.caption(t("sb_loaded", n=len(alerts), d=fmt_day(pd.Timestamp(last_alert_day))))
    st.caption(t("sb_trained", d=info["trained_until"]))

clear_minutes = alerts.groupby("Region")["duration_min"].median().round(1)

# ---------------------------------------------------------------- hero
night_share = (alerts["period"] == "Night").mean()
hero_cfg = {
    "stats": [{"v": len(alerts), "u": "", "l": t("s_alerts")},
              {"v": alerts["Region"].nunique(), "u": "", "l": t("s_regions")},
              {"v": int(round(alerts["duration_min"].median())), "u": t("min"), "l": t("s_clear")},
              {"v": round(night_share * 100), "u": "%", "l": t("s_night")}],
    "lines": [t("type1"), t("type2"), t("type3")],
    "regions": [{"n": rname(r), "m": f"{clear_minutes[r]:g}"} for r in alerts["Region"].value_counts().index],
    "ph_h": t("ph_h"), "ph_b": t("ph_b", r="{r}"), "ph_eta": t("ph_eta", m="{m}"),
    "ph_ok_h": t("ph_ok_h"), "ph_ok_b": t("ph_ok_b", r="{r}"), "loc": LOC,
    "ticker": [{"r": rname(x.Region), "d": fmt_day(x.datetime).rsplit(" ", 1)[0], "t": f"{x.datetime:%H:%M}",
                "m": (f"{x.duration_min:g} {t('min')}" if pd.notna(x.duration_min) else "–")}
               for x in alerts.sort_values("datetime", ascending=False).head(14).itertuples()],
}
components.html(ui.HERO.replace("__CFG__", json.dumps(hero_cfg, ensure_ascii=False)).replace("__DIR__", DIR)
                .replace("__BADGE__", t("badge", n=len(alerts))).replace("__TITLE__", t("title"))
                .replace("__T2__", t("title2")).replace("__DEMO__", t("ph_demo")).replace("__LIVE__", t("live")), height=550)

html(f'<div class="g-line"><div class="g-out">{t("outlook", t=fmt_day(tomorrow, True), d=fmt_day(today))}</div>'
     f'<div class="g-warn">⚠️ {t("warn")}</div></div>')

# ---------------------------------------------------------------- predictions (same logic as app.py)
x1 = model1_inputs(alerts, regions, today)[info["m1_features"]]
risk = pd.Series(model1.predict_proba(x1)[:, 1], index=regions)

tab1, tab2, tab3, tab4 = st.tabs([t("tab1"), t("tab2"), t("tab3"), t("tab4")])

# ---------------------------------------------------------------- tab 1: one region, three outputs
with tab1:
    c_a, c_b = st.columns([1.7, 1], gap="large")
    with c_a:
        region = st.pills(t("region"), regions, default="Riyadh" if "Riyadh" in regions else regions[0],
                          format_func=rname, key="region") or ("Riyadh" if "Riyadh" in regions else regions[0])
    with c_b:
        school_value = st.segmented_control(t("school", r=rname(region)), [0, 1], default=0,
                                            format_func=lambda v: t("school_yes") if v else t("school_no"))
        school_value = int(school_value or 0)
    if tomorrow.day_name() in info["weekend"] and school_value == 1:
        html(f'<div class="g-info">ℹ️ {t("weekend", d=fmt_day(tomorrow, True).split(" ")[0] if AR else tomorrow.day_name())}</div>')

    x2 = model2_inputs(alerts, [region], today, {region: school_value})[info["m2_features"]]
    period_probs = pd.Series(model2.predict_proba(x2)[0], index=model2.classes_).reindex(PERIODS)
    likely_period = model2.predict(x2)[0]
    past = alerts[alerts["Region"] == region]
    past_share = past["period"].value_counts(normalize=True).reindex(PERIODS, fill_value=0)

    # time-of-day output: start from the region's most common time in past alerts; switch to the model's top
    # period only if the model rates it at least 5 points above that usual time
    if len(past) >= MIN_REGION_ALERTS:
        hist, hist_share = past_share.idxmax(), past_share.max()
    else:
        overall = alerts["period"].value_counts(normalize=True)
        hist, hist_share = overall.idxmax(), overall.max()
    best = period_probs.idxmax()
    lead = period_probs[best] - period_probs[hist]
    if best != hist and lead >= CLEAR_GAP:
        hot = [best]
        sub2 = (t("s2_model", p=f"{PERIOD_ICON[best]} <b>{pname(best)}</b>", h=PERIOD_HOURS[best], c=f"{period_probs[best]:.0%}")
                + "<br><span style='font-size:11px'>" + t("beats", q=pname(hist), d=f"{lead * 100:.0f}") + "</span>")
    else:
        hot = [hist]
        sub2 = (t("s2_hist", p=f"{PERIOD_ICON[hist]} <b>{pname(hist)}</b>", h=PERIOD_HOURS[hist], r=rname(region), s=f"{hist_share:.0%}")
                + "<br><span style='font-size:11px'>" + t("no_beat", q=pname(best), b=f"{period_probs[best]:.0%}",
                                                            d=f"{max(lead, 0) * 100:.0f}") + "</span>")

    level = risk_level(risk[region])
    minutes = clear_minutes.get(region)
    q25, q75 = past["duration_min"].quantile([0.25, 0.75]).round(0) if len(past) else (minutes, minutes)
    out_cfg = {
        "p": float(risk[region]), "level": level, "level_txt": lname(level), "th_med": 0.35, "th_high": 0.50,
        "periods": [{"name": pname(p), "icon": PERIOD_ICON[p], "c": PERIOD_COLOR[p], "m": float(period_probs[p]),
                     "s": float(past_share[p]), "hot": p in hot, "hist": p == hist} for p in PERIODS],
        "hand_h": PERIOD_MID[hot[0]],
        "clear": float(minutes) if pd.notna(minutes) else 7.0, "q25": float(q25), "q75": float(q75),
        "clear_txt": f"{minutes:g}" if pd.notna(minutes) else "–",
        "txt": {"h1": t("h1"), "s1": t("s1", r=rname(region)),
                "f1": t("f1", n=int(x1.loc[region, "region_alerts_last_7d"])),
                "h2": t("h2"), "s2": sub2, "lh1": t("lh1"), "lh2": t("lh2"), "past": t("past", s="{s}"), "hist_tag": t("hist_tag"),
                "h3": t("h3"), "s3": t("s3", r=rname(region), m=f"{minutes:g}" if pd.notna(minutes) else "–"),
                "f3": t("f3"), "cl": t("cl"), "iqr": t("iqr", a=f"{q25:g}", b=f"{q75:g}")},
    }
    lv_color = {"High": "#FF2D55", "Medium": "#FFC233", "Low": "#51CF66"}[level]
    lit = round(risk[region] * 24)
    blocks = "".join(f'<i class="{"on" if k < lit else ""}" style="animation-delay:{k * 0.04:.2f}s"></i>' for k in range(24))
    html(f'''<div class="threat" style="--lv:{lv_color}">
  <div class="th-a"><span class="th-dot"></span><div><div class="th-k">{t("threat_k")}</div><div class="th-r">{rname(region)}</div></div></div>
  <div class="th-m">{blocks}</div>
  <div class="th-b"><div class="th-p">{risk[region]:.0%}</div><div class="th-l">{lname(level)} · {t("threat_p")}</div></div>
</div>''')
    v = hot[0]
    if best != hist and lead >= CLEAR_GAP:
        why = f"<b>{t('mode_model')}</b> · " + t("beats", q=pname(hist), d=f"{lead * 100:.0f}")
    else:
        why = f"<b>{t('mode_hist', s=f'{hist_share:.0%}')}</b> · " + t("no_beat", q=pname(best), b=f"{period_probs[best]:.0%}",
                                                                   d=f"{max(lead, 0) * 100:.0f}")
    national = alerts["duration_min"].median()
    m_txt = f"{minutes:g}" if pd.notna(minutes) else "–"
    out3_cfg = {
        "p": float(risk[region]), "level": level, "level_txt": lname(level), "th_med": 0.35, "th_high": 0.50,
        "periods": [{"name": pname(p), "icon": PERIOD_ICON[p], "c": PERIOD_COLOR[p], "m": float(period_probs[p]),
                     "hot": p == v, "hist": p == hist} for p in PERIODS],
        "hand_h": PERIOD_MID[v],
        "verdict": {"icon": PERIOD_ICON[v], "name": pname(v), "hours": "\u2066" + PERIOD_HOURS[v] + "\u2069"},
        "clear": float(minutes) if pd.notna(minutes) else 7.0, "q25": float(q25), "q75": float(q75),
        "scale": max(20, int(math.ceil((float(q75) + 5) / 10.0) * 10)),
        "txt": {"h1": t("h1"), "h2": t("h2"), "h3": t("h3"), "u3": t("cl"),
                "s1": t("s1", r=rname(region)) + "<br>" + t("f1", n=int(x1.loc[region, "region_alerts_last_7d"])),
                "s2": why,
                "s3": t("iqr", a=f"{q25:g}", b=f"{q75:g}") + "<br>" + f"{rname(region)} <b>{m_txt}</b> {t('min')} · "
                      + f"{t('all_regions')} <b>{national:g}</b> {t('min')}"},
    }
    components.html(ui.OUTLOOK3.replace("__CFG__", json.dumps(out3_cfg, ensure_ascii=False)).replace("__DIR__", DIR),
                    height=520)

# ---------------------------------------------------------------- tab 2: all regions
with tab2:
    items = sorted([{"name": rname(r), "p": float(risk[r]), "lvl": risk_level(risk[r]), "sel": r == region,
                     "sub": t("all_sub", n=int(x1.loc[r, "region_alerts_last_7d"])),
                     "lat": ui.COORDS[r][0], "lon": ui.COORDS[r][1],
                     "side": ui.LABEL_SIDE.get(r, ("r", 0))[0], "dy": ui.LABEL_SIDE.get(r, ("r", 0))[1]}
                    for r in regions], key=lambda x: -x["p"])
    map_cfg = {"items": items, "outline": ui.KSA_OUTLINE,
               "levels": [["High", t("lvl_lbl", l=lname("High"), v="50%")],
                          ["Medium", t("lvl_lbl", l=lname("Medium"), v="35%")],
                          ["Low", lname("Low")]]}
    components.html(ui.RISKMAP.replace("__CFG__", json.dumps(map_cfg, ensure_ascii=False)).replace("__DIR__", DIR)
                    .replace("__TTL__", t("all_ttl")), height=615)

# ---------------------------------------------------------------- tab 3: replay every alert
with tab3:
    a = alerts.dropna(subset=["duration_min"]).sort_values("datetime")
    regs = list(a["Region"].value_counts().index)
    start_day = a["datetime"].min().normalize()
    days = (a["datetime"].max().normalize() - start_day).days + 1
    events = [[int((row.datetime - start_day).total_seconds() // 60), regs.index(row.Region), int(row.duration_min)]
              for row in a.itertuples()]
    rp_cfg = {"events": events, "days": days, "start": start_day.strftime("%Y-%m-%dT00:00:00"),
              "regions": [{"name": rname(x), "lat": ui.COORDS[x][0], "lon": ui.COORDS[x][1],
                           "side": ui.LABEL_SIDE.get(x, ("r", 0))[0], "dy": ui.LABEL_SIDE.get(x, ("r", 0))[1]} for x in regs],
              "outline": ui.KSA_OUTLINE, "loc": LOC, "day": t("rp_day", d="{d}", n="{n}"),
              "done": t("rp_done", n=len(events), d=days, r=len(regs))}
    components.html(ui.REPLAY.replace("__CFG__", json.dumps(rp_cfg, ensure_ascii=False)).replace("__DIR__", DIR)
                    .replace("__T__", t("rp_title")).replace("__S__", t("rp_sub")).replace("__C__", t("rp_count"))
                    .replace("__RK__", t("rp_rank")).replace("__LG__", t("rp_log")).replace("__H__", t("rp_hist")),
                    height=710)

# ---------------------------------------------------------------- tab 4: how it works (same content as app.py)
with tab4:
    if AR:
        body = f"""
<div class="sec"><h4>🎯 خطر الغد</h4>موديل <b>Random Forest</b> متدرب على النشاط الأخير لكل منطقة (إنذارات اليوم، وآخر 3 و 7 أيام،
والأيام من آخر إنذار، ومتوسط مدة الإنذار) وهل بكرة إجازة نهاية أسبوع. في أسابيع الاختبار لقط <b>78%</b> من أيام الهجمات،
تقريباً ضعف القاعدة البسيطة "هجوم اليوم ← هجوم بكرة".<br><b>المستويات:</b> مرتفع ≥ 50% (إنذار الموديل)، متوسط 35–49%، منخفض أقل من 35%.</div>
<div class="sec"><h4>🕐 الوقت الأرجح</h4>موديل <b>Logistic Regression</b> يستخدم المنطقة، والإجازة، وإجابة الدراسة الحضورية، وفترة آخر إنذار في المنطقة
ونشاطها الأخير. هو <b>تلميح مو تأكيد</b>: أصاب 41% في أسابيع الاختبار (4 فترات)، وأغلب قوته من معلومة الدراسة.
نبدأ من <b>الوقت الأشيع</b> في إنذارات المنطقة السابقة (الإطار المنقّط)، والعقرب ما يتحرك لفترة ثانية إلا إذا الموديل أعطاها احتمال أعلى منه بـ <b>5 نقاط أو أكثر</b>. مثال: في الرياض مع الدراسة الحضورية، الموديل يعطي الصباح 32% مقابل الليل 22%، فيروح العقرب للصباح.</div>
<div class="sec"><h4>⏱️ مدة الزوال</h4>وسيط مدة الإنذارات السابقة في المنطقة (إحصاء، بدون موديل).</div>
<div class="sec"><h4>⚠️ القيود</h4>تقريباً 71 يوم بيانات، وتنبيهات زايدة كثيرة، والأنماط تتغير مع الوقت.
الموديلات متدربة على بيانات لين {info['trained_until']}، ورفع ملف تغريدات أحدث يحدّث المدخلات بس، مو الموديلات.</div>"""
    else:
        body = f"""
<div class="sec"><h4>🎯 Tomorrow's risk</h4><b>Random Forest</b> trained on each region's recent activity (alerts today, in the last 3 and 7 days,
days since the last alert, average alert duration) and whether tomorrow is a weekend. On the test weeks it caught <b>78%</b>
of attack days, about twice a simple "attack today → attack tomorrow" rule.<br><b>Levels:</b> High ≥ 50% (the model's alarm), Medium 35–49%, Low below 35%.</div>
<div class="sec"><h4>🕐 Most likely time</h4><b>Logistic Regression</b> using the region, weekend, the school answer you give, the period of the
region's previous alert and its recent activity. It is a <b>hint, not a certainty</b>: it was right 41% of the time on the test weeks
(4 periods), and most of its skill comes from the school information. We start from the region's <b>most common time in past alerts</b> (dashed outline); the hand moves to another period
only if the model rates it at least <b>5 points</b> higher.</div>
<div class="sec"><h4>⏱️ Time until danger clears</h4>Median duration of past alerts in the region (statistics, no model).</div>
<div class="sec"><h4>⚠️ Limits</h4>About 71 days of data; many false alarms; patterns shift over time. The models were trained on data
until {info['trained_until']}; uploading a newer tweets file updates the inputs, not the models.</div>"""
    html(f'<div class="g-card">{body}</div>')

# ---------------------------------------------------------------- footer
html(f'''<div style="direction:{DIR}; display:flex; align-items:center; gap:18px; margin:40px 0 12px;">
  <span style="flex:1; height:1px; background:linear-gradient(90deg,transparent,#FF2D55);"></span>
  <span style="font-family:'Cairo',sans-serif; font-size:1.35rem; font-weight:900; color:#FF2D55; letter-spacing:.5px;
    text-shadow:0 0 18px rgba(255,45,85,.55);">{t("slogan")}</span>
  <span style="flex:1; height:1px; background:linear-gradient(90deg,#FF2D55,transparent);"></span></div>''')
