from app.utils.data_ingestion import fetch_wallet_transactions
from app.utils.feature_engineering import engineer_features
from pathlib import Path
import pandas as pd

WALLET_ADDRESSES = [
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", 
    "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
    "0xf977814e90dA44bFA03b6295A0616a897441aceC",  
    "0xe9f7ecae3a53d2a67105292894676b00d1fab785", 
    "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",  
]

PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    print("=== Starting build_dataset.py ===")
    print("Working directory:", Path().resolve())
    print("Will save combined features to:", PROCESSED_DIR / "all_wallet_features.csv")
    print()

    all_features = []

    for w in WALLET_ADDRESSES:
        print(f"--> Processing wallet: {w}")
        try:
            df_tx = fetch_wallet_transactions(w, limit=150)
            print(f"    Transactions fetched: {len(df_tx)}")

            df_feat = engineer_features(df_tx, w)
            print("    Feature row:")
            print(df_feat)
            print()

            all_features.append(df_feat)
        except Exception as e:
            print(f"    ERROR for {w}: {e}")
            print()

    if all_features:
        df_all = pd.concat(all_features, ignore_index=True)
        out_path = PROCESSED_DIR / "all_wallet_features.csv"
        df_all.to_csv(out_path, index=False)
        print("=== DONE ===")
        print(df_all)
        print(f"\nSaved combined features to: {out_path}")
    else:
        print("=== No features generated – check errors above. ===")
