# Early Warning Risk Predictor

An end-to-end machine learning project that gives, **for each Saudi region**, an early-warning outlook for tomorrow based on the official alerts of the Saudi Civil Defense (@SaudiDCD):

1. **Tomorrow's risk**: chance of at least one alert in the region (Random Forest).
2. **Time of risk**: the most likely time of day of an alert: Night, Morning, Afternoon or Evening (Logistic Regression).
3. **Time until danger clears**: median duration of past alerts in the region (statistics).

> ⚠️ This is a student project and **does not replace official warnings**. Always follow @SaudiDCD instructions.

## Data
We collected the data ourselves from [@SaudiDCD](https://x.com/SaudiDCD): every alert tweet and every "danger cleared" tweet from **1 September to 10 November 2026** (190 alerts, 192 clear tweets), linked by `Alert_ID`.

`school_in_person` is a **synthetic feature**, approved by our instructor, used only in the time-of-risk model.

## Results (test weeks: 20 Oct – 9 Nov 2026)
| Task | Model | Score | Simple rule |
|---|---|---|---|
| Tomorrow's risk | Random Forest | Recall 0.78, F1 0.47, ROC-AUC 0.65 | Recall 0.37, F1 0.37, ROC-AUC 0.57 |
| Time of risk | Logistic Regression | Accuracy 0.41, macro F1 0.37 | Accuracy 0.22, macro F1 0.21 |

Without the synthetic school feature, the time-of-risk model scores accuracy 0.26 and macro F1 0.22 (see notebook, section 6.4).

## Project files
| File | Role |
|---|---|
| `Early_Warning_Risk_Predictor.ipynb` | Full workflow: problem, EDA, preprocessing, modeling, evaluation, model selection, deployment |
| `SaudiDCD_alerts.csv` | Collected tweets |
| `features.py` | Cleans tweets and builds model inputs (same logic as the notebook) |
| `app.py` | Streamlit app |
| `models/` | Trained models and `model_info.json` |
| `requirements.txt` | Libraries |

## Run the app
```
pip install -r requirements.txt
streamlit run app.py
```
To publish: push to GitHub, then on [share.streamlit.io](https://share.streamlit.io) choose **New app**, select this repo and `app.py`, and click **Deploy**.

## Limits
About 71 days of data, many false alarms for tomorrow's risk, and attack patterns that shift over time. Collecting more data is the most effective next step.
