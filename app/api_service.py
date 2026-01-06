from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from utils.data_ingestion import fetch_wallet_transactions
from utils.feature_engineering import engineer_features
from utils.risk_scoring import score_wallet

app = FastAPI(title="CryptoGuard AI API")

class WalletRequest(BaseModel):
    address: str
    limit: int = 100

@app.post("/api/check_wallet")
def check_wallet(req: WalletRequest):
    df_tx = fetch_wallet_transactions(req.address, limit=req.limit)
    df_features = engineer_features(df_tx, req.address)
    risk_score, label = score_wallet(df_features)

    return {
        "address": req.address,
        "risk_score": risk_score,
        "risk_label": label
    }
