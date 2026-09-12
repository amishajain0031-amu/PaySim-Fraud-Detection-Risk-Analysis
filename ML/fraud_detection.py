import streamlit as st

st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="💳",
    layout="centered"
)

st.title("💳 Fraud Detection System")
st.write("Enter transaction details to check for fraud.")

# -----------------------------
# USER INPUT
# -----------------------------

transaction_type = st.selectbox(
    "Transaction Type",
    ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT", "CASH_IN"]
)

amount = st.number_input(
    "Transaction Amount",
    min_value=0.0,
    value=1000.0
)

oldbalanceOrg = st.number_input(
    "Old Balance (Sender)",
    min_value=0.0,
    value=1000.0
)

newbalanceOrig = st.number_input(
    "New Balance (Sender)",
    min_value=0.0,
    value=0.0
)

oldbalanceDest = st.number_input(
    "Old Balance (Receiver)",
    min_value=0.0,
    value=0.0
)

newbalanceDest = st.number_input(
    "New Balance (Receiver)",
    min_value=0.0,
    value=0.0
)

# -----------------------------
# PREDICTION
# -----------------------------

if st.button("Predict"):

    fraud_score = 0
    reasons = []

    # Rule 1: Very large transaction
    if amount >= 50000:
        fraud_score += 30
        reasons.append("Large transaction amount")

    # Rule 2: Transfer with almost entire sender balance
    if transaction_type == "TRANSFER":
        if oldbalanceOrg > 0 and amount >= oldbalanceOrg * 0.8:
            fraud_score += 30
            reasons.append("Large portion of sender balance transferred")

    # Rule 3: Cash out with large amount
    if transaction_type == "CASH_OUT":
        if oldbalanceOrg > 0 and amount >= oldbalanceOrg * 0.8:
            fraud_score += 30
            reasons.append("Large cash-out relative to sender balance")

    # Rule 4: Sender balance inconsistency
    expected_sender_balance = oldbalanceOrg - amount

    if abs(newbalanceOrig - expected_sender_balance) > 1:
        fraud_score += 20
        reasons.append("Sender balance change is unusual")

    # Rule 5: Receiver balance inconsistency
    if transaction_type in ["TRANSFER", "CASH_IN"]:
        expected_receiver_balance = oldbalanceDest + amount

        if abs(newbalanceDest - expected_receiver_balance) > 1:
            fraud_score += 20
            reasons.append("Receiver balance change is unusual")

    # Keep score between 0 and 100
    fraud_score = min(fraud_score, 100)

    # -----------------------------
    # RESULT
    # -----------------------------

    st.subheader("Prediction Result")

    if fraud_score >= 50:

        st.error("🚨 FRAUDULENT TRANSACTION")

        st.metric(
            "Fraud Risk",
            f"{fraud_score}%"
        )

        if reasons:
            st.write("### Why was it flagged?")
            for reason in reasons:
                st.write("⚠️", reason)

    else:

        st.success("✅ SAFE / LEGITIMATE TRANSACTION")

        st.metric(
            "Fraud Risk",
            f"{fraud_score}%"
        )

        if reasons:
            st.write("### Minor risk indicators")
            for reason in reasons:
                st.write("ℹ️", reason)
        else:
            st.write("No suspicious indicators detected.")