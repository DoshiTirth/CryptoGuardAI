# CryptoGuard AI  
Blockchain Wallet Fraud & Anomaly Detection Platform

## Overview
CryptoGuard AI is a machine-learning powered blockchain analytics tool that analyzes Ethereum wallet activity.  
It fetches recent transactions from the Etherscan API (V2), engineers behavioral features, and uses an IsolationForest model to assign a fraud risk score to each wallet.

**The project includes:**
- Real-time data ingestion from Ethereum
- Feature engineering for wallet behavior
- Anomaly detection with IsolationForest
- Streamlit web application
- CSV export for Power BI dashboards

---

## Features

- **Live blockchain data** from Etherscan API V2  
- **IsolationForest anomaly detection** for suspicious wallets  
- **Risk score (0–100)** with Low / Medium / High risk labels  
- **Streamlit dashboard** with charts and tables  
- **CSV export** for further analysis (e.g., Power BI)  
- Modular Python codebase for easy extension  

---

## Tech Stack

**Languages & Libraries**
- Python 3.10+
- pandas
- numpy
- scikit-learn
- joblib
- requests
- streamlit

**API**
- Etherscan API V2

**Tools**
- Conda
- VS Code
- Power BI Desktop

---

## Project Structure

```text
CryptoGuardAI/
│
├── app/
│   ├── streamlit_app.py          # Streamlit web application
│   ├── api_service.py            # (optional) FastAPI service
│   ├── model/
│   │   └── isolation_forest_model.pkl
│   └── utils/
│       ├── data_ingestion.py     # Etherscan API integration
│       ├── feature_engineering.py
│       └── risk_scoring.py
│
├── data/
│   ├── raw/                      # Raw transaction CSVs
│   └── processed/                # Feature CSVs
│       ├── features_<wallet>.csv
│       └── all_wallet_features.csv
│
├── dashboards/
│   └── PowerBI_CryptoGuard.pbix  # Power BI dashboard (optional)
│
├── notebooks/
│   └── 01_train_model.ipynb      # Optional training notebook
│
├── build_dataset.py              # Build feature dataset
├── train_model.py                # Train IsolationForest model
├── test_ingestion.py             # Test Etherscan connectivity
│
├── requirements.txt
└── README.md
```

## Installation

### 1. Create and activate Conda environment
```bash
conda create -n cryptoguard python=3.10 -y
conda activate cryptoguard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Configuration

### Add your Etherscan API key

Edit: app/utils/data_ingestion.py

**Replace:**
```python
ETHERSCAN_API_KEY = "YOUR_API_KEY_HERE"
```

---

## Building the Dataset

**Generate wallet features:**
```bash
python build_dataset.py
```

**Outputs:**
- data/processed/features_<wallet>.csv
- data/processed/all_wallet_features.csv

---

## Training the Model

**Train the IsolationForest model:**
```bash
python train_model.py
```

**Creates:**
```bash
app/model/isolation_forest_model.pkl
```
---

## Running the Streamlit App

Start the app:
```bash
streamlit run app/streamlit_app.py
```
**Then open:**
```bash
http://localhost:8501
```
**App features:**
- Risk score & label
- Raw transactions
- Feature table
- Line chart
- Hourly activity bar chart
- CSV export

---

## Testing API / Ingestion

Run test:
```bash
python test_ingestion.py
```

**You should see:**
- A DataFrame of transactions
- “Fetched rows: X”

---

## Power BI Dashboard (Optional)

1. Export CSV from Streamlit  
2. Import into Power BI  
3. Suggested visuals:
   - Risk distribution  
   - Total volume vs risk  
   - Transaction count per wallet  
   - Feature comparison  

Save as:
```bash
dashboards/PowerBI_CryptoGuard.pbix
```

---

## Risk Scoring Logic

IsolationForest anomaly score → scaled to 0–100.

Risk levels:
- 0–40 → Low Risk  
- 40–70 → Medium Risk  
- 70–100 → High Risk  

Higher scores = more unusual behavior.  

---

## Future Enhancements

- Multi-chain support (BTC, BSC, Polygon)  
- Discord/Telegram alert bot  
- Cloud deployment  
- Advanced ML models (Autoencoders, LSTM)  
- REST API for developers  
- Real-time monitoring engine  

---

## License
 
Not for commercial use.  

