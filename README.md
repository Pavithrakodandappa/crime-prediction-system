# AI-Based Crime Prediction & Analysis System

A Flask web app that predicts crime type and risk level for city areas, forecasts monthly crime trends, and shows results on a dashboard.

## Features
- Crime type classification (Random Forest)
- Area risk score prediction (Random Forest regressor)
- 6-month forecast (seasonal pattern + linear trend)
- Heatmap and dashboard for 30 Indian cities

## Tech
Python, Flask, Scikit-learn, Pandas, NumPy, HTML, CSS, JavaScript

## Run
1. pip install -r requirements.txt
2. python app.py
3. Open http://127.0.0.1:5000

## Note
The model is trained on synthetic sample data. Add a real crime_data.csv to train on real data.

## Author
Pavithra K – BCA, Christ Academy Institute for Advanced Studies
