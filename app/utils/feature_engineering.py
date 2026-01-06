import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def engineer_features(df_tx: pd.DataFrame, wallet_address: str) -> pd.DataFrame:
    """
    Create aggregated feature vector for a wallet from transaction-level data.
    For simplicity we aggregate into one row per wallet.
    """
    if df_tx.empty:
        raise ValueError("No transactions found for this wallet.")

    df_tx = df_tx.sort_values("time")
    df_tx["time_diff_sec"] = df_tx["time"].diff().dt.total_seconds().fillna(0)

    features = {
        "wallet": wallet_address,
        "tx_count": len(df_tx),
        "total_volume_btc": df_tx["value_btc"].sum(),
        "avg_tx_value_btc": df_tx["value_btc"].mean(),
        "std_tx_value_btc": df_tx["value_btc"].std(),
        "max_tx_value_btc": df_tx["value_btc"].max(),
        "min_tx_value_btc": df_tx["value_btc"].min(),
        "avg_fee_btc": df_tx["fee_btc"].mean(),
        "avg_time_between_tx_sec": df_tx["time_diff_sec"].replace(0, pd.NA).mean(),
        "burstiness_tx_per_hour": df_tx.set_index("time").resample("1H")["tx_hash"].count().max(),
        "avg_inputs": df_tx["n_inputs"].mean(),
        "avg_outputs": df_tx["n_outputs"].mean()
    }

    df_features = pd.DataFrame([features])
    csv_path = PROCESSED_DIR / f"features_{wallet_address}.csv"
    df_features.to_csv(csv_path, index=False)
    return df_features
