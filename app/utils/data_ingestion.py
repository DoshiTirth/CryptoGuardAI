import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import os

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")   # <--- your key
ETHERSCAN_BASE_URL = "https://api.etherscan.io/v2/api"

if not ETHERSCAN_API_KEY:
    raise ValueError(
        "Missing ETHERSCAN_API_KEY. Set it as an environment variable or in a local .env file."
    )

RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)



def fetch_wallet_transactions(wallet_address: str, limit: int = 100) -> pd.DataFrame:
    """
    Fetch recent Ethereum transactions for a given wallet address using
    Etherscan API V2 `txlist` endpoint.

    Returns a DataFrame with columns:
    ['tx_hash', 'time', 'value_btc', 'n_inputs', 'n_outputs', 'fee_btc', 'from', 'to', 'is_error']
    (value_btc / fee_btc actually represent ETH amounts).
    """

    # ----- V2 query params -----
    params = {
        "apikey": ETHERSCAN_API_KEY,
        "chainid": 1,              # 1 = Ethereum mainnet
        "module": "account",
        "action": "txlist",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 9999999999,
        "page": 1,
        "offset": limit,           # number of txs to fetch
        "sort": "desc",
    }

    response = requests.get(ETHERSCAN_BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    status = data.get("status")
    if status != "1":
        message = data.get("message", "Unknown error")
        raise ValueError(f"Etherscan API error: status={status}, message={message}")

    txs = data.get("result", [])

    records = []
    for tx in txs:
        ts = int(tx["timeStamp"])
        dt = datetime.fromtimestamp(ts)

        # value in wei -> ETH
        value_eth = int(tx["value"]) / 1e18

        gas_price = int(tx.get("gasPrice", 0))
        gas_used = int(tx.get("gasUsed", 0))
        fee_eth = (gas_price * gas_used) / 1e18

        records.append(
            {
                "tx_hash": tx["hash"],
                "time": dt,
                # for compatibility with rest of project:
                "value_btc": value_eth,   # ETH amount
                "n_inputs": 1,
                "n_outputs": 1,
                "fee_btc": fee_eth,       # ETH fee
                "from": tx["from"],
                "to": tx["to"],
                "is_error": int(tx["isError"]),
            }
        )

    df = pd.DataFrame(records)

    csv_path = RAW_DATA_DIR / f"transactions_{wallet_address}.csv"
    df.to_csv(csv_path, index=False)

    return df
