import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Config must be the FIRST Streamlit command
st.set_page_config(
    page_title="Fraud Risk Analysis",
    page_icon="🛡️",
    layout="wide"
)

# 2. Data Loader
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("paysim_final.csv")
    except Exception:
        np.random.seed(42)
        n_rows = 2000
        df = pd.DataFrame({
            'step': np.random.randint(1, 744, n_rows),
            'type': np.random.choice(['PAYMENT', 'TRANSFER', 'CASH_OUT', 'DEBIT', 'CASH_IN'], n_rows),
            'amount': np.random.exponential(scale=50000, size=n_rows),
            'oldbalanceOrg': np.random.exponential(scale=100000, size=n_rows),
            'newbalanceOrig': np.random.exponential(scale=80000, size=n_rows),
            'nameOrig': [f"C{i}" for i in np.random.randint(100000, 999999, n_rows)],
            'nameDest': [f"M{i}" for i in np.random.randint(100000, 999999, n_rows)],
            'isFraud': np.random.choice([0, 1], n_rows, p=[0.97, 0.03]),
            'isFlaggedFraud': np.random.choice([0, 1], n_rows, p=[0.999, 0.001]),
            'time_period': np.random.choice(['Morning', 'Afternoon', 'Evening', 'Night'], n_rows)
        })
        df['day'] = (df['step'] // 24) + 1
        df['hour'] = df['step'] % 24
        df['errorBalanceOrg'] = df['newbalanceOrig'] + df['amount'] - df['oldbalanceOrg']
        df['large_transaction'] = (df['amount'] > 200000).astype(int)

    def calculate_risk(row):
        if row['isFraud'] == 1:
            return 'High Risk'
        elif row['large_transaction'] == 1 or row['errorBalanceOrg'] != 0:
            return 'Medium Risk'
        return 'Low Risk'

    df['Risk Level'] = df.apply(calculate_risk, axis=1)
    return df

df = load_data()

# 3. Sidebar Navigation
st.sidebar.title("🛡️ FRAUD RISK ANALYSIS")
page = st.sidebar.radio("Navigate:", ["1. Executive Overview", "2. Fraud Analysis", "3. Risk & Account Analysis"])

selected_types = st.sidebar.multiselect("Transaction Type:", options=df['type'].unique(), default=df['type'].unique())
filtered_df = df[df['type'].isin(selected_types)]

# 4. Page Content
if page == "1. Executive Overview":
    st.title("📊 Executive Overview")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Txns", f"{len(filtered_df):,}")
    m2.metric("Total Vol", f"${filtered_df['amount'].sum()/1e6:.2f}M")
    m3.metric("Fraud Txns", f"{filtered_df['isFraud'].sum():,}")
    m4.metric("Fraud Rate", f"{(filtered_df['isFraud'].sum()/len(filtered_df)*100 if len(filtered_df)>0 else 0):.2f}%")
    
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Transactions by Type")
        fig1 = px.pie(filtered_df, names='type', values='amount', hole=0.4, template="plotly_dark")
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        st.subheader("Fraud Rate by Type")
        fr_df = filtered_df.groupby('type')['isFraud'].mean().reset_index()
        fr_df['Fraud Rate (%)'] = fr_df['isFraud'] * 100
        fig2 = px.bar(fr_df, x='type', y='Fraud Rate (%)', template="plotly_dark", color='type')
        st.plotly_chart(fig2, use_container_width=True)

elif page == "2. Fraud Analysis":
    st.title("🚨 Fraud Analysis")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Fraud Incidents by Hour")
        h_df = filtered_df.groupby('hour')['isFraud'].sum().reset_index()
        fig_h = px.line(h_df, x='hour', y='isFraud', markers=True, template="plotly_dark")
        st.plotly_chart(fig_h, use_container_width=True)
    with c2:
        st.subheader("Amount vs Sender Old Balance")
        fig_s = px.scatter(filtered_df, x='oldbalanceOrg', y='amount', color='isFraud', template="plotly_dark")
        st.plotly_chart(fig_s, use_container_width=True)

elif page == "3. Risk & Account Analysis":
    st.title("🎯 Risk & Account Analysis")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Risk Level Breakdown")
        fig_r = px.pie(filtered_df, names='Risk Level', hole=0.4, template="plotly_dark")
        st.plotly_chart(fig_r, use_container_width=True)
    with c2:
        st.subheader("Top Flagged Transactions")
        st.dataframe(filtered_df[filtered_df['Risk Level'] == 'High Risk'][['step', 'type', 'amount', 'nameOrig', 'Risk Level']].head(10), use_container_width=True)