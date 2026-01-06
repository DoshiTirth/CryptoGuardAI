from app.utils.data_ingestion import fetch_wallet_transactions

if __name__ == "__main__":
    wallet = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    df = fetch_wallet_transactions(wallet, limit=20)
    print(df.head())
    print("Fetched rows:", len(df))
