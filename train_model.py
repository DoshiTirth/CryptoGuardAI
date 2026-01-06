# train_model.py
from pathlib import Path
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

PROCESSED_DIR = Path("data/processed")
MODEL_DIR = Path("app/model")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    csv_path = PROCESSED_DIR / "all_wallet_features.csv"
    print("Loading:", csv_path)
    df = pd.read_csv(csv_path)

    # All columns except 'wallet' are features
    feature_cols = [c for c in df.columns if c not in ["wallet"]]
    X = df[feature_cols].fillna(0)

    print("Training IsolationForest on", X.shape[0], "wallets and",
          X.shape[1], "features...")

    model = IsolationForest(
        n_estimators=200,
        contamination=0.2,      # assume ~20% wallets are “anomalies”
        random_state=42,
    )
    model.fit(X)

    model_path = MODEL_DIR / "isolation_forest_model.pkl"
    joblib.dump((model, feature_cols), model_path)

    print("Model saved to:", model_path)
