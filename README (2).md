# 🛡️ PaySim Fraud Detection & Risk Analysis

## 📌 Project Overview

This project is a **Fraud Detection and Risk Analysis System** built using the **PaySim transaction dataset**.

The project has two main parts:

1. **Fraud Risk Analysis Dashboard** – provides an interactive view of transaction volume, fraud transactions, fraud rate, fraud patterns, and risk levels.
2. **Fraud Detection Application** – allows a user to enter transaction details and receive a fraud/legitimate result based on the current rule-based risk logic.

The dashboard is built with **Streamlit, Pandas, NumPy, and Plotly**. The dashboard loads `paysim_final.csv` when it is available. It also contains a fallback sample-data generator so the dashboard can still run when the CSV is not found.

## 🎯 Main Goal

The main goal of this project is to analyze financial transactions and identify transactions that may represent fraudulent activity.

The system is designed to help:

- identify suspicious transactions
- understand fraud patterns
- analyze fraud by transaction type and hour
- categorize transactions into risk levels
- provide an interactive interface for fraud checking
- support faster fraud investigation

## 💼 Business Problem

Digital payment systems process a large number of transactions. Checking every transaction manually is difficult and time-consuming.

Fraudulent transactions can cause:

- financial losses
- customer trust issues
- increased investigation workload
- security risks

An automated fraud-analysis system can help organizations identify suspicious transactions and prioritize them for further investigation.

## 📊 Dataset

The project uses the **PaySim** transaction dataset.

The application works with fields such as:

- `step` – simulation time step
- `type` – transaction type
- `amount` – transaction amount
- `oldbalanceOrg` – sender balance before transaction
- `newbalanceOrig` – sender balance after transaction
- `oldbalanceDest` – receiver balance before transaction
- `newbalanceDest` – receiver balance after transaction
- `nameOrig` – sender account identifier
- `nameDest` – receiver account identifier
- `isFraud` – fraud indicator
- `isFlaggedFraud` – flagged-fraud indicator

The dashboard also creates/uses derived fields such as `day`, `hour`, `errorBalanceOrg`, `large_transaction`, and `Risk Level`.

## 🔄 Project Workflow

```text
PaySim Dataset
      ↓
Data Loading
      ↓
Data Preparation / Feature Creation
      ↓
Fraud & Risk Analysis
      ↓
Interactive Streamlit Dashboard
      ↓
Transaction Input
      ↓
Fraud Detection Rules
      ↓
SAFE / FRAUD result
```

## 📈 Dashboard Features

### 1. Executive Overview

The dashboard displays:

- Total Transactions
- Total Transaction Volume
- Fraud Transactions
- Fraud Rate
- Transactions by Type
- Fraud Rate by Transaction Type

The dashboard allows users to filter transactions by transaction type.

### 2. Fraud Analysis

The dashboard provides:

- Fraud Incidents by Hour
- Amount vs Sender Old Balance analysis

These visualizations help understand when fraud occurs and how transaction amount relates to sender balance.

### 3. Risk & Account Analysis

The dashboard provides:

- Risk Level Breakdown
- Top Flagged Transactions

Risk levels are currently categorized as:

- **High Risk** – transaction is marked as fraud
- **Medium Risk** – large transaction or sender balance inconsistency
- **Low Risk** – no detected risk indicator

## 🔍 Fraud Detection Application

The separate Streamlit fraud detection application accepts:

- Transaction Type
- Transaction Amount
- Old Sender Balance
- New Sender Balance
- Old Receiver Balance
- New Receiver Balance

The application then applies rule-based checks.

### Current Rules

#### Rule 1 – Large Transaction

If:

```text
amount >= 50,000
```

the system adds 30 risk points.

#### Rule 2 – Large Transfer

For a `TRANSFER`, if the transaction is at least 80% of the sender's old balance, 30 points are added.

#### Rule 3 – Large Cash Out

For a `CASH_OUT`, if the transaction is at least 80% of the sender's old balance, 30 points are added.

#### Rule 4 – Sender Balance Inconsistency

The application calculates:

```text
Expected Sender Balance = Old Sender Balance - Amount
```

If the entered new balance differs from the expected value by more than 1, 20 points are added.

#### Rule 5 – Receiver Balance Inconsistency

For `TRANSFER` and `CASH_IN` transactions:

```text
Expected Receiver Balance = Old Receiver Balance + Amount
```

If the entered new balance differs from the expected value by more than 1, 20 points are added.

### Final Decision

```text
Risk Score >= 50  →  FRAUDULENT TRANSACTION
Risk Score < 50   →  SAFE / LEGITIMATE TRANSACTION
```

> **Important:** The current fraud detection screen uses manually defined rules and a risk score. The displayed score is not a machine-learning probability of fraud.

## 🛠️ Technologies Used

- **Python**
- **Pandas** – data manipulation
- **NumPy** – numerical operations
- **Plotly Express** – interactive charts
- **Streamlit** – web application and dashboard
- **Jupyter Notebook** – analysis and experimentation
- **Pickle (`.pkl`)** – stored project pipeline/model artifact

## 📁 Project Structure

```text
project/
│
├── app.py
├── fraud_detection.py
├── fraud_detection_pipeline.pkl
├── ML.ipynb
├── Data_Profiling.ipynb
├── paysim_final.csv
└── README.md
```

> File names can be adjusted to match your local project folder.

## ▶️ How to Run the Project

### 1. Install Python

Check that Python is installed:

```bash
python --version
```

### 2. Install Required Libraries

```bash
pip install streamlit pandas numpy plotly
```

If `pip` does not work:

```bash
python -m pip install streamlit pandas numpy plotly
```

### 3. Run the Risk Analysis Dashboard

Open the project folder in Command Prompt/Terminal and run:

```bash
streamlit run app.py
```

The dashboard should open in your browser.

### 4. Run the Fraud Detection Application

Run:

```bash
streamlit run fraud_detection.py
```

The application provides transaction input fields and a **Predict** button.

## 🧪 Example

Example transaction:

```text
Transaction Type: TRANSFER
Amount: 80,000
Old Sender Balance: 80,000
New Sender Balance: 0
Old Receiver Balance: 1,000
New Receiver Balance: 1,000
```

The rule-based system identifies multiple suspicious indicators and can classify the transaction as:

```text
🚨 FRAUDULENT TRANSACTION
```

A normal transaction with consistent balances and no major risk indicators can produce:

```text
✅ SAFE / LEGITIMATE TRANSACTION
```

## ⚠️ Current Limitations

The current Streamlit fraud detection screen is **rule-based**, not a complete live machine-learning prediction interface.

Therefore:

- the risk score should not be interpreted as a true fraud probability
- manually selected thresholds may not generalize to all transactions
- the current UI does not use the stored `.pkl` pipeline for its displayed prediction
- the production version should use the same preprocessing and trained model used during model development

## 🚀 Future Improvements

Possible improvements include:

- connect the Streamlit prediction page directly to the trained ML pipeline
- use `model.predict()` for the final fraud classification
- use `model.predict_proba()` where supported for probability estimates
- apply the exact preprocessing used during model training
- evaluate the model using precision, recall, F1-score, ROC-AUC and PR-AUC
- handle the strong class imbalance in fraud data
- add model explainability
- add real-time transaction monitoring
- add downloadable fraud reports
- improve account-level risk analysis
- deploy the application online

## 👩‍💻 Project Purpose

This project demonstrates how transaction data can be analyzed and presented through an interactive fraud-risk application.

It combines:

**Data Analysis + Visualization + Fraud Risk Rules + Streamlit Application**

to create a practical fraud detection and risk analysis prototype.

## 📜 Note

This project is intended for **educational and analytical purposes**. The current rule-based fraud score should not be treated as a real-world financial fraud probability or production fraud decision system.
