import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed")
output_file = PROCESSED_DIR / "all_wallet_features.csv"

feature_files = list(PROCESSED_DIR.glob("features_*.csv"))

if not feature_files:
    print("No feature files found in data/processed/")
    exit()

all_rows = []

for file in feature_files:
    print(f"Loading: {file.name}")
    df = pd.read_csv(file)

    wallet = file.stem.replace("features_", "")
    df["wallet"] = wallet

    all_rows.append(df)

df_all = pd.concat(all_rows, ignore_index=True)
cols = ["wallet"] + [c for c in df_all.columns if c != "wallet"]
df_all = df_all[cols]

df_all.to_csv(output_file, index=False)

print("\nMerged feature file saved as:")
print(output_file)
print(f"Total wallets combined: {len(df_all)}")
