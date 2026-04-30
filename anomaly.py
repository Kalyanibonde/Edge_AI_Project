import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(data):
    model = IsolationForest(contamination=0.05)
    preds = model.fit_predict(data)

    # Convert: -1 → anomaly (1), 1 → normal (0)
    return [1 if x == -1 else 0 for x in preds]