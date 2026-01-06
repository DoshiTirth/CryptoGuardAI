import streamlit as st
import pandas as pd

from utils.data_ingestion import fetch_wallet_transactions
from utils.feature_engineering import engineer_features
from utils.risk_scoring import score_wallet
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="CryptoGuard AI", layout="wide")

st.title("CryptoGuard AI – Blockchain Wallet Fraud Detector")

st.write(
    "Enter any **Ethereum wallet address** to analyze its recent transaction "
    "behaviour and get an anomaly-based risk score using IsolationForest."
)

st.sidebar.header("Wallet Analysis")
wallet = st.sidebar.text_input("Ethereum wallet address (0x...)")
n_tx = st.sidebar.slider("Number of recent transactions", 20, 200, 100)

if st.sidebar.button("Analyze Wallet"):
    if not wallet:
        st.error("Please enter a wallet address.")
    else:
        with st.spinner("Fetching data and running ML model..."):
            try:
                df_tx = fetch_wallet_transactions(wallet, limit=n_tx)
                if df_tx.empty:
                    st.warning("No transactions found for this wallet.")
                else:
                    df_features = engineer_features(df_tx, wallet)

                    risk_score, label = score_wallet(df_features)

                    st.success(f"Analysis completed for wallet: `{wallet}`")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Risk Assessment")
                        st.metric("Risk Score (0–100)", f"{risk_score:.1f}")
                        st.write(f"**Risk Category:** {label}")

                        st.subheader("Engineered Features")
                        st.dataframe(df_features.T.rename(columns={0: "value"}))

                    with col2:
                        st.subheader("Transaction Value Over Time (ETH)")
                        st.line_chart(
                            df_tx.set_index("time")["value_btc"],
                        )

                        st.subheader("Transactions Per Hour")
                        hourly = (
                            df_tx.set_index("time")["tx_hash"]
                                 .resample("1H")
                                 .count()
                        )
                        st.bar_chart(hourly)

                    st.subheader("Raw Transactions (latest)")
                    st.dataframe(df_tx)

                    export = df_features.copy()
                    export["risk_score"] = risk_score
                    export["risk_label"] = label

                    st.download_button(
                        "Download Features + Risk Score (CSV)",
                        export.to_csv(index=False),
                        file_name=f"wallet_{wallet}_features_with_risk.csv",
                        mime="text/csv",
                    )

            except Exception as e:
                st.error(f"Error during analysis: {e}")
else:
    st.info("Enter a wallet address in the sidebar and click **Analyze Wallet**.")
