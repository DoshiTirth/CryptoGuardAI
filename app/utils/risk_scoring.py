
import numpy as np
import pandas as pd
import joblib
from pathlib import Path

MODEL_PATH = Path("app/model/isolation_forest_model.pkl")

def load_model():
    model, feature_cols = joblib.load(MODEL_PATH)
    return model, feature_cols


def score_wallet(df_features: pd.DataFrame):
    """
    Takes a 1-row features DataFrame for a wallet and
    returns (risk_score_0_to_100, risk_label_str).
    """
    model, feature_cols = load_model()

    X = df_features.reindex(columns=feature_cols, fill_value=0)

    raw_score = model.decision_function(X)[0]

    risk_score = float(np.clip((1 - raw_score) * 50, 0, 100))

    if risk_score < 40:
        label = "Low Risk"
    elif risk_score < 70:
        label = "Medium Risk"
    else:
        label = "High Risk"

    return risk_score, label
