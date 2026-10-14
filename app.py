"""CrimeAI Flask backend.  Run:  python app.py   ->  http://localhost:5000"""
import calendar
import datetime as dt
import os
import zlib

import numpy as np
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

import model
from data import LOCATIONS, RISK_SCORES, AREA_META, MONTHLY_HISTORY, level

app = Flask(__name__)
CORS(app)
clf, reg, INFO = model.load()


def err(msg, code=400):
    return jsonify(error=msg), code


def city():
    return LOCATIONS.get(request.args.get("city", "Bengaluru"))


def area_index(loc, name):
    return loc["areas"].index(name) if name in loc["areas"] else None


# ---------- pages & meta ----------
BASE = os.path.dirname(os.path.abspath(__file__))


@app.get("/")
def home():
    # serves index.html (or Maincode.html) from the same folder as app.py
    files = os.listdir(BASE)
    pages = [f for f in files if f.lower().endswith((".html", ".htm"))]
    pages.sort(key=lambda f: (f.lower() != "index.html", f))   # prefer index.html
    if pages:
        return send_from_directory(BASE, pages[0])
    return err(f"No .html file found in {BASE}. Files seen: {files}", 404)


@app.get("/api/health")
def health():
    return jsonify(status="ok", model=INFO["source"], accuracy=INFO["accuracy"])


@app.get("/api/model-info")
def model_info():
    return jsonify(INFO)


@app.post("/api/retrain")
def retrain():
    global clf, reg, INFO
    clf, reg, INFO = model.train()
    return jsonify(INFO)


# ---------- locations ----------
@app.get("/api/locations")
def locations():
    q = request.args.get("q", "").lower()
    out = [l for l in LOCATIONS.values()
           if not q or q in l["name"].lower() or q in l["state"].lower()
           or any(q in a.lower() for a in l["areas"])]
    return jsonify(out[:10])


# ---------- dashboard ----------
@app.get("/api/dashboard")
def dashboard():
    loc = city()
    if not loc:
        return err("Unknown city", 404)
    per = loc["incidents"] // 8
    rows = []
    for i, a in enumerate(loc["areas"]):
        s = RISK_SCORES[i]
        inc = int(per * (0.6 + s / 200))
        rows.append(dict(area=a, score=s, level=level(s), incidents=inc,
                         top_crime=AREA_META[i]["crime"], peak_time=AREA_META[i]["time"],
                         patrol_units=AREA_META[i]["patrol"], daily_avg=round(inc / 365, 2)))
    counts = {l: sum(r["level"] == l for r in rows) for l in ("CRITICAL", "HIGH", "MEDIUM", "LOW")}
    return jsonify(city=loc["name"], state=loc["state"], total_incidents=loc["incidents"],
                   level_counts=counts, areas=rows)


# ---------- classification ----------
@app.post("/api/classify")
def classify():
    b = request.get_json(silent=True) or {}
    loc = LOCATIONS.get(b.get("city", "Bengaluru"))
    if not loc:
        return err("Unknown city", 404)
    idx = area_index(loc, b.get("zone"))
    if idx is None:
        return err("zone must be one of: " + ", ".join(loc["areas"]))
    x = model.encode(idx, b.get("time"), b.get("day"), b.get("weapon"),
                     b.get("victims"), b.get("density", "Medium"), b.get("weather", "Clear"))
    p = clf.predict_proba(x)[0]
    top = np.argsort(p)[::-1][:4]
    probs = [dict(crime=clf.classes_[i], probability=round(float(p[i]) * 100, 1)) for i in top]
    return jsonify(zone=b["zone"], predicted=probs[0]["crime"],
                   confidence=probs[0]["probability"], probabilities=probs)


# ---------- risk prediction ----------
@app.post("/api/predict")
def predict():
    b = request.get_json(silent=True) or {}
    loc = LOCATIONS.get(b.get("city", "Bengaluru"))
    if not loc:
        return err("Unknown city", 404)
    idx = area_index(loc, b.get("zone"))
    if idx is None:
        return err("zone must be one of: " + ", ".join(loc["areas"]))
    x = model.encode(idx, b.get("time"), b.get("day"), "None", "1",
                     b.get("density"), b.get("weather"))
    trees = np.array([t.predict(x.values)[0] for t in reg.estimators_])
    score = int(round(float(np.clip(trees.mean(), 5, 99))))
    conf = round(float(max(70, 100 - trees.std() * 2)), 1)
    lvl = level(score)
    rec = {"CRITICAL": "Immediate patrol deployment. Coordinate with emergency services.",
           "HIGH": "Increased visibility advised. Alert patrol units.",
           "MEDIUM": "Standard patrol schedule. Monitor for changes.",
           "LOW": "Historically safe under these conditions."}[lvl]
    return jsonify(zone=b["zone"], score=score, level=lvl, confidence=conf, recommendation=rec,
                   factors=[dict(name="Area weight", value=RISK_SCORES[idx]),
                            dict(name="Time", value=int(x["time"][0]) * 25),
                            dict(name="Day type", value=int(x["day"][0]) * 33),
                            dict(name="Density", value=int(x["density"][0]) * 33)])


# ---------- forecast ----------
@app.get("/api/forecast")
def forecast():
    loc = city()
    if not loc:
        return err("Unknown city", 404)
    scale, today = loc["incidents"] / 2847, dt.date.today()
    shares = np.array(RISK_SCORES) / sum(RISK_SCORES)
    y = np.array(MONTHLY_HISTORY, float)                      # 72 real months (2019-2024)
    yearly = y.reshape(6, 12)
    season = (yearly / yearly.mean(axis=1, keepdims=True)).mean(axis=0)  # seasonal index per month
    t = np.arange(72)
    slope, icpt = np.polyfit(t, y / season[t % 12], 1)        # trend on de-seasonalised data
    out = []
    for k in range(1, 7):
        n = today.year * 12 + today.month - 1 + k             # months since year 0
        yr, m = divmod(n, 12)
        total = (icpt + slope * ((yr - 2019) * 12 + m)) * season[m] * scale
        out.append(dict(month=f"{calendar.month_abbr[m + 1]} {yr}", total=round(total),
                        areas={a: round(total * shares[i]) for i, a in enumerate(loc["areas"])}))
    return jsonify(city=loc["name"], method="seasonal index x linear trend, fitted on 72 real months",
                   forecast=out)


# ---------- heatmap (12x12 KDE-style grid) ----------
HOT = [(5, 4, 2.5), (2, 4, 2), (2, 8, 1.8), (9, 2, 2.2), (8, 8, 1.2), (5, 1, 1.5), (2, 1, 1.5), (10, 8, 1)]


@app.get("/api/heatmap")
def heatmap():
    loc = city()
    if not loc:
        return err("Unknown city", 404)
    rng = np.random.default_rng(zlib.crc32(loc["name"].encode()))
    yy, xx = np.mgrid[0:12, 0:12]
    grid = np.full((12, 12), 5.0)
    for (cx, cy, r), s in zip(HOT, RISK_SCORES):
        grid = np.maximum(grid, s * np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * r * r)))
    grid = np.clip(grid + rng.uniform(-4, 4, grid.shape), 2, 99).round().astype(int)
    return jsonify(city=loc["name"], grid=grid.tolist(),
                   areas=[dict(area=a, score=RISK_SCORES[i], level=level(RISK_SCORES[i]))
                          for i, a in enumerate(loc["areas"])])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
