"""ML part: Random Forest classifier (crime type) + Random Forest regressor (risk score).

Uses crime_data.csv if present (columns: area,time,day,weapon,victims,density,weather,crime,risk).
Otherwise trains on synthetic data so the project runs out of the box.
"""
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error
from sklearn.model_selection import train_test_split

from data import RISK_SCORES, AREA_CRIMES

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "crime_data.csv")
PKL = os.path.join(HERE, "models.pkl")

FEATURES = ["area", "time", "day", "weapon", "victims", "density", "weather"]
TIMES = ["Morning", "Afternoon", "Evening", "Night", "Late Night"]
DAYS = ["Weekday", "Weekend", "Holiday", "Festival"]
WEAPONS = ["None", "Blunt Object", "Knife", "Firearm"]
DENSITY = ["Low", "Medium", "High", "Very High"]
WEATHER = ["Clear", "Cloudy", "Rainy", "Heavy Storm"]


def _idx(options, value):
    """'Late Night (00–06h)' -> 4, 'Festival Day' -> 3 (matches by prefix)."""
    for i, o in enumerate(options):
        if str(value).startswith(o):
            return i
    return 0


def encode(area, time="Morning", day="Weekday", weapon="None", victims="1",
           density="Medium", weather="Clear"):
    v = int(str(victims)[0]) if str(victims)[:1].isdigit() else 1
    row = [int(area), _idx(TIMES, time), _idx(DAYS, day), _idx(WEAPONS, weapon),
           v, _idx(DENSITY, density), _idx(WEATHER, weather)]
    return pd.DataFrame([row], columns=FEATURES)


def synthetic(n=8000, seed=42):
    r = np.random.default_rng(seed)
    a, t, d, w = (r.integers(0, 8, n), r.integers(0, 5, n),
                  r.integers(0, 4, n), r.integers(0, 4, n))
    v, de, we = r.integers(1, 5, n), r.integers(0, 4, n), r.integers(0, 4, n)
    risk = (np.array(RISK_SCORES)[a]
            + np.where(t >= 3, 15, np.where(t == 2, 8, 0))
            + np.where(d == 3, 12, np.where(d == 1, 5, 0))
            + de * 3 + (we >= 2) * 5 + r.normal(0, 4, n))
    crime = []
    for i in range(n):
        if w[i] >= 2 and r.random() < 0.7:
            crime.append(r.choice(["Assault", "Robbery"]))
        else:
            crime.append(r.choice(AREA_CRIMES[a[i]], p=[.6, .25, .15]))
    return pd.DataFrame(dict(area=a, time=t, day=d, weapon=w, victims=v,
                             density=de, weather=we, crime=crime,
                             risk=np.clip(risk, 5, 99)))


def train():
    df = pd.read_csv(CSV) if os.path.exists(CSV) else synthetic()
    X_tr, X_te, c_tr, c_te, r_tr, r_te = train_test_split(
        df[FEATURES], df["crime"], df["risk"], test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1).fit(X_tr, c_tr)
    reg = RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1).fit(X_tr, r_tr)
    pred = clf.predict(X_te)
    info = dict(
        source="crime_data.csv" if os.path.exists(CSV) else "synthetic",
        rows=len(df), classes=list(clf.classes_),
        accuracy=round(accuracy_score(c_te, pred), 4),
        f1_weighted=round(f1_score(c_te, pred, average="weighted"), 4),
        risk_mae=round(mean_absolute_error(r_te, reg.predict(X_te)), 2),
        feature_importance=dict(zip(FEATURES, map(lambda x: round(float(x), 4),
                                                  clf.feature_importances_))),
    )
    joblib.dump((clf, reg, info), PKL)
    return clf, reg, info


def load():
    return joblib.load(PKL) if os.path.exists(PKL) else train()
