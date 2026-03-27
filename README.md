# 🏦 Real-Time Banking Fraud Detection — Microsoft Fabric RTI

A production-ready Proof of Concept for **real-time fraud detection** using [Microsoft Fabric Real-Time Intelligence](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/). This solution ingests banking transactions through EventStreams into an Eventhouse (KQL Database), applies **18 detection functions** and **3 materialized views**, generates alerts in real time, and surfaces insights via a Real-Time Dashboard and an AI-powered Data Agent for natural-language fraud investigation.

> **10,000 transactions · 18 KQL detection functions · 3 materialized views · 15-tile real-time dashboard · AI-powered investigator**

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [📐 Architecture](#-architecture)
- [🚀 Prerequisites](#-prerequisites)
- [📝 Step-by-Step Setup Guide](#-step-by-step-setup-guide)
  - [Step 1: Create Fabric Workspace](#step-1-create-fabric-workspace)
  - [Step 2: Create Eventhouse](#step-2-create-eventhouse)
  - [Step 3: Create Tables](#step-3-create-tables)
  - [Step 4: Generate & Ingest Sample Data](#step-4-generate--ingest-sample-data)
  - [Step 5: Create Detection Functions](#step-5-create-detection-functions)
  - [Step 6: Create Materialized Views](#step-6-create-materialized-views)
  - [Step 7: Configure Policies](#step-7-configure-policies)
  - [Step 8: Create Real-Time Dashboard](#step-8-create-real-time-dashboard)
  - [Step 9: Create KQL Queryset](#step-9-create-kql-queryset)
  - [Step 10: Create Data Agent](#step-10-create-data-agent)
  - [Step 11: Create Ontology](#step-11-create-ontology)
- [📊 KQL Detection Algorithms](#-kql-detection-algorithms)
  - [Core Detection Functions](#core-detection-functions)
  - [Advanced Detection & Risk Profiling](#advanced-detection--risk-profiling)
  - [Dashboard & Investigation Functions](#dashboard--investigation-functions)
- [📓 Using the Notebook](#-using-the-notebook)
- [📁 Repository Structure](#-repository-structure)
- [🔑 Key Performance Indicators](#-key-performance-indicators)
- [🛡️ Data Schema Reference](#️-data-schema-reference)
- [❓ Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🎯 Overview

Traditional fraud detection relies on batch processing with significant latency between a fraudulent transaction and its detection. This POC demonstrates how **Microsoft Fabric Real-Time Intelligence** can close that gap to **near-zero latency** by combining:

| Component | Purpose |
|---|---|
| **EventStreams** | Real-time ingestion of banking transactions |
| **Eventhouse (KQL Database)** | High-performance analytical store with sub-second query times |
| **18 KQL Detection Functions** | Multi-layered fraud scoring, velocity checks, geographic anomalies, and more |
| **3 Materialized Views** | Pre-aggregated hourly, daily, and merchant-level risk summaries |
| **FraudAlerts Table** | Persisted alert records with fraud scores and classification |
| **Real-Time Dashboard** | 15-tile live dashboard with KPIs, trend charts, alert feeds, and geographic analysis |
| **Data Agent (AI)** | Natural-language fraud investigation powered by Fabric AI |
| **Domain Ontology** | Entity-relationship model encoding banking domain knowledge |

### Key Metrics at a Glance

| Metric | Value |
|---|---|
| Total Transactions | 10,000 |
| Detection Functions | 18 (14 custom + 4 entity views) |
| Materialized Views | 3 |
| Dashboard Tiles | 15 |
| Fraud Detection Rules | 6 weighted risk factors |
| Alert Severity Levels | 3 (Critical, High, Medium) |

---

## 📐 Architecture

```
┌─────────────────┐    ┌───────────────────┐    ┌──────────────────────┐
│  Event Source    │───▶│   EventStreams     │───▶│     Eventhouse       │
│  (Bank Txns)    │    │   (Fabric)        │    │   BankingFraudDB     │
└─────────────────┘    └───────────────────┘    └──────────┬───────────┘
                                                           │
                  ┌────────────────────────────────────────┼────────────────────────────┐
                  │                                        │                            │
           ┌──────▼────────┐              ┌───────────────▼──────────┐    ┌────────────▼───────┐
           │  18 KQL        │              │   3 Materialized Views   │    │   FraudAlerts      │
           │  Functions     │              │                          │    │   Table             │
           │  (Detection)   │              │  • Hourly Txn Stats      │    │   (Scored Alerts)   │
           │                │              │  • Customer Daily Risk   │    │                     │
           │  • Fraud Score │              │  • Merchant Risk Profile │    │                     │
           │  • Velocity    │              │                          │    │                     │
           │  • Cross-Border│              └───────────────┬──────────┘    └────────────┬───────┘
           │  • Anomaly     │                              │                            │
           │  • Takeover    │                              │                            │
           │  • Geo Check   │                              │                            │
           └──────┬─────────┘                              │                            │
                  │                                        │                            │
           ┌──────▼────────────────────────────────────────▼────────────────────────────▼───────┐
           │                         Real-Time Dashboard (15 Tiles)                             │
           │                                                                                    │
           │  📊 KPIs  │  📈 Fraud Trend  │  🚨 Alert Feed  │  🌍 Geographic Analysis          │
           │  📉 Charts │  👤 Risk Profile │  🏪 Merchant    │  ⏰ Unusual Time Activity        │
           └────────────────────────────────────────────────────────────────────────────────────┘
           ┌──────────────────────────┐    ┌──────────────────────────┐
           │    Data Agent (AI)       │    │    Domain Ontology       │
           │                          │    │                          │
           │  Natural-language fraud  │    │  Entity relationships:   │
           │  investigation queries   │    │  Customer ─owns─▶ Acct   │
           │                          │    │  Acct ─processes─▶ Txn   │
           │  "Show me suspicious     │    │  Txn ─triggers─▶ Alert   │
           │   transactions today"    │    │  Merchant ─receives─▶Txn │
           └──────────────────────────┘    └──────────────────────────┘
```

### Data Flow

1. **Ingest** — Banking transactions stream into EventStreams from source systems (POS, online banking, ATM, mobile).
2. **Store** — Transactions land in the `Transactions` table inside the `BankingFraudDB` KQL Database (Eventhouse).
3. **Detect** — 18 KQL functions analyze transactions in real time, scoring fraud risk across multiple dimensions.
4. **Alert** — The `FraudAlertTransform` function converts high-risk detections into persisted `FraudAlerts` records.
5. **Aggregate** — 3 materialized views maintain rolling summaries (hourly stats, daily customer risk, merchant profiles).
6. **Visualize** — A 15-tile Real-Time Dashboard renders live KPIs, trend charts, alert feeds, and geographic analysis.
7. **Investigate** — A Data Agent enables natural-language queries for ad-hoc fraud investigation.

---

## 🚀 Prerequisites

| Requirement | Details |
|---|---|
| **Microsoft Fabric** | Capacity **F2 or above** with Real-Time Intelligence workload enabled |
| **Azure Subscription** | With Fabric enabled in the tenant |
| **Python** | 3.9+ (for notebook and data generation) |
| **Azure CLI** | Latest version (for deployment scripts) |
| **Browser** | Edge or Chrome (for Fabric portal at [app.fabric.microsoft.com](https://app.fabric.microsoft.com)) |

### Python Packages

Install dependencies from the included `requirements.txt`:

```bash
pip install -r requirements.txt
```

| Package | Version | Purpose |
|---|---|---|
| `azure-kusto-data` | ≥ 4.0.0 | KQL query execution against Eventhouse |
| `azure-identity` | ≥ 1.15.0 | Azure AD authentication |
| `pandas` | ≥ 2.0.0 | Data manipulation and analysis |
| `matplotlib` | ≥ 3.7.0 | Visualization and charting |
| `seaborn` | ≥ 0.12.0 | Statistical data visualization |
| `faker` | ≥ 19.0.0 | Synthetic data generation |
| `jupyter` | ≥ 1.0.0 | Notebook runtime |

---

## 📝 Step-by-Step Setup Guide

Follow these steps in order to deploy the complete POC from scratch.

---

### Step 1: Create Fabric Workspace

1. Navigate to [app.fabric.microsoft.com](https://app.fabric.microsoft.com).
2. Click **Workspaces** in the left navigation pane.
3. Click **+ New workspace**.
4. Enter the workspace name: **`RTI_IQ_01`** (or your preferred name).
5. Expand **Advanced** and assign your Fabric capacity (F2 or above).
6. Click **Apply**.

> 💡 **Tip:** Enable "Real-Time Intelligence" workload in your capacity settings if not already activated.

---

### Step 2: Create Eventhouse

1. Inside the workspace, click **+ New** → **Real-Time Intelligence** → **Eventhouse**.
2. Name it: **`BankingFraudBD`**
3. Click **Create**.

This automatically provisions a KQL Database named **`BankingFraudDB`** within the Eventhouse.

> ⚠️ **Note:** The Eventhouse name uses "BD" (as in the original POC naming convention). The KQL Database inside it is `BankingFraudDB`.

---

### Step 3: Create Tables

Open a **KQL Queryset** connected to `BankingFraudDB` and run each table creation script **in order**. The scripts are located in `kql/tables/`:

| # | File | Table Created | Columns |
|---|---|---|---|
| 1 | `01_create_customers.kql` | `Customers` | customer_id, customer_name, email, phone, address, city, state, country, postal_code, account_creation_date, customer_risk_score, is_high_risk_customer, entity_type, ingestion_timestamp |
| 2 | `02_create_bankaccounts.kql` | `BankAccounts` | account_id, customer_id, account_type, account_status, opening_date, current_balance, credit_limit, daily_transaction_limit, entity_type, ingestion_timestamp |
| 3 | `03_create_merchants.kql` | `Merchants` | merchant_id, merchant_name, merchant_category, merchant_country, risk_level, entity_type, ingestion_timestamp |
| 4 | `04_create_transactions.kql` | `Transactions` | transaction_id, timestamp, account_id, customer_id, merchant_id, merchant_name, merchant_category, amount, currency, transaction_type, channel, card_present, merchant_country, customer_city, customer_country, customer_risk_score, merchant_risk_level, entity_type, ingestion_timestamp |
| 5 | `05_create_fraudalerts.kql` | `FraudAlerts` | alert_id, transaction_id, timestamp, customer_id, account_id, merchant_id, merchant_name, amount, fraud_score, fraud_type, is_fraudulent, unusual_time, unusual_location, amount_flag, high_risk_merchant, high_risk_customer, card_not_present_risk, channel, merchant_country, customer_country, alert_timestamp, alert_status |

**How to run:**

1. In the workspace, click **+ New** → **KQL Queryset**.
2. Connect it to **BankingFraudDB**.
3. Copy the contents of each `.kql` file and execute sequentially.

```kql
// Example: Create the Customers table
.create-merge table Customers (
    customer_id: string,
    customer_name: string,
    email: string,
    phone: string,
    address: string,
    city: string,
    state: string,
    country: string,
    postal_code: string,
    account_creation_date: datetime,
    customer_risk_score: int,
    is_high_risk_customer: bool,
    entity_type: string,
    ingestion_timestamp: datetime
)
```

> 💡 **Shortcut:** Use `kql/deploy_all.kql` as a reference for the full deployment order, then copy each individual script for execution.

---

### Step 4: Generate & Ingest Sample Data

The `data/` folder contains pre-generated sample datasets in JSON format:

| File | Records | Description |
|---|---|---|
| `sample_customers.json` | ~500 | Customer profiles with risk scores |
| `sample_bankaccounts.json` | ~700 | Bank accounts linked to customers |
| `sample_merchants.json` | ~200 | Merchant profiles with risk levels |
| `sample_transactions.json` | ~10,000 | Transaction records across all channels |

#### Option A: Upload via Fabric Portal (Recommended)

1. Open **BankingFraudDB** in the Fabric portal.
2. Click **Get Data** → **Local file**.
3. Select the JSON file for each table.
4. Map columns to the table schema and complete the ingestion wizard.

#### Option B: Inline Ingestion via KQL

```kql
// Example: Ingest from local JSON (after uploading to blob storage)
.ingest into table Customers
    h'https://yourstorageaccount.blob.core.windows.net/data/sample_customers.json'
    with (format='multijson')
```

#### Option C: Generate Fresh Data with Python

```bash
# Install dependencies
pip install -r requirements.txt

# Generate sample data (if generate_sample_data.py is available)
python data/generate_sample_data.py
```

> 📝 **Note:** The `data/schema_export.json` file contains the full schema definition for all tables, functions, and materialized views — useful for programmatic deployment.

---

### Step 5: Create Detection Functions

Deploy all 14 detection functions from `kql/functions/`. Run each script in the KQL Queryset connected to `BankingFraudDB`.

#### Function Deployment Order & Summary

| # | File | Function Name | Category | Purpose | Key Risk Indicators |
|---|---|---|---|---|---|
| 1 | `01_fraud_detection.kql` | `FraudDetection()` | Core | Multi-factor fraud scoring engine (6 weighted rules) | Amount > $2K, time 2–5 AM, location mismatch, high-risk merchant/customer, card-not-present > $500 |
| 2 | `02_velocity_detection.kql` | `VelocityDetection()` | Core | Rapid-fire transaction detection | Same account, < 5 min apart; critical if < 1 min |
| 3 | `03_cross_border_fraud.kql` | `CrossBorderFraud()` | Core | International transaction risk classification | Country mismatch + amount thresholds → Critical/High/Medium |
| 4 | `04_amount_anomaly_detection.kql` | `AmountAnomalyDetection()` | Core | Spending anomaly vs. customer baseline | Transaction > 5× customer average spend |
| 5 | `05_unusual_time_detection.kql` | `UnusualTimeDetection()` | Core | Off-hours activity detection | Transactions 12 AM–6 AM with amount > $200 |
| 6 | `06_customer_risk_profile.kql` | `CustomerRiskProfile()` | Advanced | Composite customer risk scoring | Weighted: 40% fraud rate, 20% cross-border, 15% high-amount, 25% base risk |
| 7 | `07_account_takeover_detection.kql` | `AccountTakeoverDetection()` | Advanced | Account takeover pattern detection | > 10 txns/hour, > 3 countries/hour, or night + high-value combo |
| 8 | `08_fraud_alert_transform.kql` | `FraudAlertTransform()` | Pipeline | Transforms detections → FraudAlerts records | Auto-generates alert_id, sets status = 'New' |
| 9 | `09_realtime_fraud_dashboard.kql` | `RealTimeFraudDashboard()` | Dashboard | Unified alert feed from all detectors | Union of fraud, velocity, cross-border, amount anomaly, and takeover alerts |
| 10 | `10_multi_channel_switching.kql` | `MultiChannelSwitching()` | Advanced | Channel-hopping detection | ≥ 3 channel switches within 30 min window |
| 11 | `11_merchant_category_anomaly.kql` | `MerchantCategoryAnomaly()` | Advanced | Category spending deviation | Spending > 5× baseline per category; count > 3× baseline |
| 12 | `12_geographic_velocity_check.kql` | `GeographicVelocityCheck()` | Advanced | Impossible travel detection | Different countries < 4 hours apart; critical if < 1 hour |
| 13 | `13_fraud_investigator.kql` | `FraudInvestigator(target_customer_id)` | Investigation | Customer deep-dive investigation | Full profile: customer info, accounts, transactions, fraud flags, risk score |
| 14 | `14_fraud_summary_kpis.kql` | `FraudSummaryKPIs()` | Dashboard | Dashboard KPI summary row | TotalTransactions, FraudCount, FraudRate, FraudAmount, HighRiskCustomers, ActiveAlerts, VelocityAlerts, CriticalCrossBorder |

> ⚠️ **Dependency Order:** Functions 6–14 depend on the core functions (1–5). Always deploy core functions first.

#### Additionally in `schema_export.json`

The schema export includes 4 entity view functions used for filtered access to a unified `AllBankingData` table:

| Function | Purpose |
|---|---|
| `Customers_View()` | Filter `AllBankingData` for `entity_type == "Customer"` |
| `Merchants_View()` | Filter `AllBankingData` for `entity_type == "Merchant"` |
| `BankAccounts_View()` | Filter `AllBankingData` for `entity_type == "BankAccount"` |
| `Transactions_View()` | Filter `AllBankingData` for `entity_type == "Transaction"` |

---

### Step 6: Create Materialized Views

Materialized views provide **continuously updated aggregations** with minimal query cost. Deploy from `kql/materialized-views/`:

| # | File | View Name | Source | Grain | Key Aggregations |
|---|---|---|---|---|---|
| 1 | `01_mv_hourly_transaction_stats.kql` | `mv_HourlyTransactionStats` | `Transactions` | Hourly × TxnType × Channel | TxnCount, TotalAmount, AvgAmount, MaxAmount, CrossBorderCount, HighRiskMerchantCount, CardNotPresentCount |
| 2 | `02_mv_customer_daily_risk.kql` | `mv_CustomerDailyRisk` | `Transactions` | Daily × Customer | DailyTxnCount, DailyAmount, DailyAvg, DailyMax, UniqueCountries, UniqueMerchants, NightTxns, HighAmountTxns, CrossBorderTxns |
| 3 | `03_mv_merchant_risk_profile.kql` | `mv_MerchantRiskProfile` | `Transactions` | Merchant-level | TxnCount, TotalAmount, AvgAmount, UniqueCustomers, HighRiskCustomerTxns, NightTxns, CardNotPresentTxns |

All three views are created with **backfill** enabled to immediately process historical data:

```kql
// Example: Create the hourly stats materialized view
.create-or-alter materialized-view with (backfill=true)
    mv_HourlyTransactionStats on table Transactions
{
    Transactions
    | summarize
        TxnCount = count(),
        TotalAmount = sum(amount),
        AvgAmount = avg(amount),
        MaxAmount = max(amount),
        CrossBorderCount = countif(customer_country != merchant_country),
        HighRiskMerchantCount = countif(merchant_risk_level == "High"),
        CardNotPresentCount = countif(card_present == false)
    by bin(timestamp, 1h), transaction_type, channel
}
```

---

### Step 7: Configure Policies

Apply ingestion and caching policies from `kql/policies/`:

#### 7a. Streaming Ingestion (`01_streaming_ingestion.kql`)

Enable streaming ingestion on the `Transactions` table for near-zero latency:

```kql
.alter table Transactions policy streamingingestion enable
```

> 💡 Streaming ingestion ensures transactions are queryable within seconds of arrival.

#### 7b. Hot Cache (`02_caching.kql`)

Set a 30-day hot cache on `FraudAlerts` for fast query performance on recent alerts:

```kql
.alter table FraudAlerts policy caching hot = 30d
```

> 💡 Hot cache keeps data in SSD/RAM for sub-second query performance. Older data is still accessible but may be slightly slower.

---

### Step 8: Create Real-Time Dashboard

The dashboard provides a live operational view of fraud detection activity.

1. In your workspace, click **+ New** → **Real-Time Dashboard**.
2. Name it: **`Banking Fraud Detection Dashboard`**.
3. Click **+ Add data source** → select **BankingFraudDB**.
4. Create tiles using the queries from `dashboard/dashboard_queries.kql`.

#### Dashboard Tile Reference (15 Tiles)

| # | Tile Name | KQL Source | Visualization |
|---|---|---|---|
| 1 | **Fraud KPIs** | `FraudSummaryKPIs()` | KPI Cards |
| 2 | **Fraud Trend Over Time** | `FraudDetection()` → hourly count | Time Chart 📈 |
| 3 | **Fraud by Type** | `FraudDetection()` → group by fraud_type | Pie Chart 🥧 |
| 4 | **Real-Time Alert Feed** | `RealTimeFraudDashboard()` → take 50 | Table |
| 5 | **Fraud Amount by Channel** | `FraudDetection()` → group by channel, txn_type | Column Chart 📊 |
| 6 | **Top Fraud Customers** | `CustomerRiskProfile()` → top 20 | Table |
| 7 | **Velocity Alerts** | `VelocityDetection()` | Table |
| 8 | **Cross-Border Fraud** | `CrossBorderFraud()` → by country pair | Column Chart 📊 |
| 9 | **Amount Anomalies** | `AmountAnomalyDetection()` → top 20 | Table |
| 10 | **Impossible Travel** | `GeographicVelocityCheck()` | Table |
| 11 | **Multi-Channel Switching** | `MultiChannelSwitching()` | Table |
| 12 | **Unusual Time Activity** | `UnusualTimeDetection()` → by hour, channel | Column Chart 📊 |
| 13 | **Account Takeover Detection** | `AccountTakeoverDetection()` | Table |
| 14 | **Merchant Risk Profile** | `mv_MerchantRiskProfile` → by category | Column Chart 📊 |
| 15 | **Hourly Transaction Volume** | `mv_HourlyTransactionStats` → by timestamp | Time Chart 📈 |

#### Example Dashboard Tile Query

```kql
// Tile 2: Fraud Trend Over Time
FraudDetection()
| where is_fraudulent == true
| summarize FraudCount = count(), FraudAmount = sum(amount) by bin(timestamp, 1h)
| order by timestamp asc
| render timechart
```

> 💡 **Tip:** Set the dashboard auto-refresh interval to **30 seconds** for near-real-time updates.

#### 📸 Dashboard Screenshots

The real-time dashboard is organized into **3 pages** with auto-refresh enabled for live operational monitoring.

---

**Page 1 — Fraud Command Center (KPIs & Overview)**

![Fraud Command Center](images/RTI%20Dashboard%201.png)

The command center provides an at-a-glance operational summary:

| KPI Card | Value | Description |
|---|---|---|
| **Total Transactions** | 10,000 | Total banking transactions monitored |
| **Fraud Count** | 43 | Transactions flagged as fraudulent |
| **Fraud Rate %** | 0.43 | Percentage of fraudulent transactions |
| **Fraud Amount ($)** | 255,601 | Total dollar value of suspicious activity |
| **Active Alerts** | 86 | Open fraud alerts pending investigation |
| **Velocity Alerts** | 4 | Rapid-fire transaction pattern detections |

- 📈 **Fraud Detections Over Time** — Time-series chart tracking FraudCount and TotalAmount trends from Feb 21 to Mar 22, showing daily fluctuations in fraud activity with peaks around Feb 26 (~10K) and periodic dips
- 🥧 **Fraud Types** — Donut chart showing the distribution of fraud types; Amount Anomaly dominates at 100% of classified alerts, indicating most flagged transactions are high-value spending outliers

---

**Page 2 — Detection Details (Alert Feed & Risk Analysis)**

![Detection Details](images/RTI%20Dashboard%202.png)

The detection details page provides real-time operational visibility into active fraud:

- 🔴 **Real-Time Alert Feed** (50 rows) — Live scrolling table of the latest fraud alerts with color-coded severity rows (red = High/Critical). Each row shows timestamp, transaction ID, customer name, amount, detection type (Amount Anomaly, Cross-Border, Fraud Score), severity level, and investigation details. Highest alert: Jason Jones — $9,598.71 Amount Anomaly
- 📊 **Fraud Detection by Channel** — Stacked horizontal funnel chart breaking down fraud detections across ATM, POS, Online, and Mobile channels. ATM leads with 30,715 (89%), followed by POS at 20,172 (58.58%) and Online at 16,834 (48.89%). Each bar shows percentage penetration across detection types
- 👥 **Top Risk Customers** (20 rows) — Ranked table of highest-risk customers with computed risk scores (max 56.17 — Brian Moore), risk category (High/Medium), fraud count, fraud rate %, total fraud amount, cross-border rate, and unique countries. Color-coded rows highlight High-risk customers in red/orange

---

**Page 3 — Investigation (Velocity, Cross-Border & Anomalies)**

![Investigation](images/RTI%20Dashboard%203.png)

Deep-dive investigation tools for fraud analysts:

- ⚡ **Velocity Alerts** (4 rows) — Detects rapid-fire transactions from the same account within minutes. Example: CUST000671 made a $455.48 transaction at Computer Warehouse #55 just 3 minutes after a previous transaction. Shows timestamp, transaction ID, account, customer, amount, time difference (1–4 min), and merchant details
- 🌍 **Cross-Border Fraud** — Bar chart showing international transaction volume by merchant country code. Colombia (CO) leads at ~40K, followed by Ecuador (EC) at ~25K and Tajikistan (TJ) at ~22K. Covers 20+ countries including MU, CI, NI, BT, TT, ME, NP, WS, CF, SO, MV, VU, NG, ZA, SM, UG — each colored by risk category
- 💰 **Amount Anomalies** (20 rows) — Transactions where spending exceeds the customer's historical average by extreme ratios. Top anomaly: Kathryn Dunn spent $8,093.61 at Phone Hub #360 — **15.25x** her average of $530.64. Table shows deviation ratios ranging from 12.72x to 15.25x, all flagging potential card compromise or account takeover

---

**Page 4 — Trends & Analytics (Volume, Night Activity & Takeover)**

![Trends & Analytics](images/RTI%20Dashboard%204.png)

Historical trend analysis and behavioral pattern detection:

- 📈 **Hourly Volume** — High-frequency time-series chart (Feb 20 – Mar 22) showing transaction volume spikes up to 30K per hour with four overlay series: CrossBorder (blue), HighRisk (orange), TotalAmount (dark blue), and TotalTxns (purple). The spiky pattern reveals natural daily transaction cycles with clear daytime peaks and overnight troughs
- 🌙 **Night Activity** (28 rows) — Hourly breakdown of transactions during suspicious hours (12AM–6AM) across all channels. Hour 0 shows: Online (68 txns, $39,650), ATM (66, $44,785), Mobile (64, $57,278), POS (76, $62,239). Useful for identifying unusual after-hours banking patterns that may indicate unauthorized access
- 🔐 **Account Takeover** — Detection panel for accounts showing 10+ transactions/hour or activity from 3+ countries within 1 hour. Currently shows "No Rows To Show" — indicating no active account takeover attempts detected in the monitoring window. This is a good sign for the current data window

> 🔄 **Dashboard pages** — Use the left sidebar to navigate between *Fraud Command Center*, *Detection Details*, and *Trends & Analytics*. The time range filter (top-left: "Last 90 days") applies globally across all pages.

---

### Step 9: Create KQL Queryset

A KQL Queryset provides an interactive query environment for ad-hoc fraud investigation.

1. Click **+ New** → **KQL Queryset**.
2. Name it: **`Fraud Investigation Queries`**.
3. Connect to **BankingFraudDB**.
4. Add commonly used investigation queries:

```kql
// Quick investigation: All fraud indicators for a customer
FraudInvestigator("CUST-001")

// Summary KPIs
FraudSummaryKPIs()

// Recent high-severity alerts
RealTimeFraudDashboard()
| where severity == "Critical"
| order by timestamp desc
| take 20

// Customer risk leaderboard
CustomerRiskProfile()
| where risk_category in ("Critical", "High")
| order by computed_risk_score desc
| take 50
```

---

### Step 10: Create Data Agent

The Data Agent enables **natural-language fraud investigation** using AI.

1. In your workspace, click **+ New** → **Data Agent**.
2. Name it: **`Fraud Investigation Agent`**.
3. Configure the data source: select **BankingFraudDB**.
4. Add the following system instructions:

```
You are a banking fraud investigation assistant. You have access to a KQL database
containing banking transactions, fraud alerts, customer profiles, and detection functions.

Available functions: FraudDetection(), VelocityDetection(), CrossBorderFraud(),
AmountAnomalyDetection(), UnusualTimeDetection(), CustomerRiskProfile(),
AccountTakeoverDetection(), RealTimeFraudDashboard(), GeographicVelocityCheck(),
MultiChannelSwitching(), MerchantCategoryAnomaly(), FraudInvestigator(customer_id),
FraudSummaryKPIs()

When investigating fraud, always check multiple detection dimensions.
Provide specific transaction IDs and amounts in your responses.
```

5. **Test with these sample prompts:**

| Prompt | Expected Behavior |
|---|---|
| `"Show me the top 10 suspicious transactions today"` | Calls `RealTimeFraudDashboard()` with severity filter |
| `"What is the current fraud rate?"` | Calls `FraudSummaryKPIs()` |
| `"Investigate customer CUST-001"` | Calls `FraudInvestigator("CUST-001")` |
| `"Are there any impossible travel alerts?"` | Calls `GeographicVelocityCheck()` |
| `"Which merchants have the highest fraud exposure?"` | Queries `mv_MerchantRiskProfile` |

---

### Step 11: Create Ontology

The ontology defines the **domain knowledge graph** for the banking fraud detection system.

1. In your workspace, click **+ New** → **Ontology**.
2. Name it: **`Banking Fraud Ontology`**.
3. Define the following entities and relationships:

#### Entities

| Entity | Source Table | Key Field | Description |
|---|---|---|---|
| **Customer** | `Customers` | `customer_id` | Bank customer with risk profile |
| **BankAccount** | `BankAccounts` | `account_id` | Financial account with limits |
| **Merchant** | `Merchants` | `merchant_id` | Merchant receiving payments |
| **Transaction** | `Transactions` | `transaction_id` | Individual financial transaction |
| **FraudAlert** | `FraudAlerts` | `alert_id` | Detected fraud event |

#### Relationships

```
Customer ──owns──▶ BankAccount
BankAccount ──processes──▶ Transaction
Transaction ──at──▶ Merchant
Transaction ──triggers──▶ FraudAlert
Customer ──flagged_in──▶ FraudAlert
Merchant ──receives──▶ Transaction
```

> 💡 The ontology powers intelligent navigation in the Data Agent, enabling queries like _"Show me all accounts owned by customers with critical risk scores and their recent transactions."_

---

## 📊 KQL Detection Algorithms

### Core Detection Functions

#### 1. `FraudDetection()` — Multi-Factor Fraud Scoring

The primary fraud scoring engine applies **6 weighted risk factors** to every transaction:

| Rule | Condition | Points | Weight |
|---|---|---|---|
| Unusual Time | Transaction between 2 AM – 5 AM | 15 | Time-based risk |
| Unusual Location | Customer country ≠ Merchant country | 20 | Geographic risk |
| Amount Flag | Transaction amount > $2,000 | 25 | Value-based risk |
| High-Risk Merchant | Merchant risk level = "High" | 10 | Merchant risk |
| High-Risk Customer | Customer risk score > 75 | 15 | Profile-based risk |
| Card-Not-Present | Card not present AND amount > $500 | 20 | Channel risk |

**Scoring:** `fraud_score = sum of triggered rule points` (max 105)

**Classification:** `is_fraudulent = fraud_score > 70`

**Fraud Type Assignment:**

| Priority | Condition | Fraud Type |
|---|---|---|
| 1 | `amount_flag == true` | Amount Anomaly |
| 2 | `unusual_location == true` | Geographic Anomaly |
| 3 | `card_not_present_risk == true` | Card Not Present Fraud |
| 4 | `unusual_time == true` | Unusual Time Activity |
| 5 | `fraud_score > 40` | Multi-Factor Suspicious |
| 6 | Default | Normal |

```kql
// Sample output from FraudDetection()
FraudDetection()
| where is_fraudulent == true
| project transaction_id, timestamp, customer_id, amount,
          fraud_score, fraud_type, unusual_time, unusual_location,
          amount_flag, high_risk_merchant
| order by fraud_score desc
| take 10
```

---

#### 2. `VelocityDetection()` — Rapid-Fire Transaction Detection

Detects abnormally rapid transactions on the same account using `prev()` windowing:

```
┌─ Transaction 1 ─┐    ┌─ Transaction 2 ─┐    ┌─ Transaction 3 ─┐
│ 10:00:00 AM      │───▶│ 10:02:30 AM      │───▶│ 10:03:15 AM      │
│ Account: A-001   │    │ Account: A-001   │    │ Account: A-001   │
│ $500             │    │ $750             │    │ $1,200           │
└──────────────────┘    └──────────────────┘    └──────────────────┘
        2.5 min gap ⚠️           0.75 min gap 🚨
        velocity_flag            high_velocity
```

| Threshold | Flag | Severity |
|---|---|---|
| < 5 minutes | `velocity_flag` | High |
| < 1 minute | `high_velocity` | Critical |

---

#### 3. `CrossBorderFraud()` — International Risk Classification

Flags cross-border transactions where the customer's country differs from the merchant's country:

| Risk Level | Criteria |
|---|---|
| **Critical** | Amount > $1,000 AND merchant risk = "High" |
| **High** | Amount > $500 |
| **Medium** | Amount > $100 (default cross-border) |

---

#### 4. `AmountAnomalyDetection()` — Spending Deviation Analysis

Compares each transaction against the customer's historical average:

```
deviation_ratio = transaction_amount / customer_avg_amount
```

Flags transactions where `deviation_ratio > 5` (i.e., spending 5× above average).

---

#### 5. `UnusualTimeDetection()` — Off-Hours Activity

Flags significant transactions (> $200) occurring during unusual hours (12 AM – 6 AM), enriched with customer contact information and account details for rapid outreach.

---

### Advanced Detection & Risk Profiling

#### 6. `CustomerRiskProfile()` — Composite Risk Scoring

Builds a comprehensive risk profile per customer using a **weighted composite score**:

```
computed_risk_score = (fraud_rate × 0.40)
                    + (cross_border_rate × 0.20)
                    + (high_amount_rate × 0.15)
                    + (base_risk_score × 0.25)
```

| Risk Category | Score Range |
|---|---|
| 🔴 Critical | ≥ 75 |
| 🟠 High | ≥ 50 |
| 🟡 Medium | ≥ 25 |
| 🟢 Low | < 25 |

---

#### 7. `AccountTakeoverDetection()` — Hourly Window Analysis

Analyzes 1-hour time windows per account for takeover patterns:

| Threat Level | Trigger |
|---|---|
| **Critical** | > 3 unique countries AND > 2 high-value transactions in 1 hour |
| **High** | > 15 transactions in 1 hour |
| **Medium** | > 10 transactions OR > 3 countries OR night + high-value combo |

---

#### 8. `FraudAlertTransform()` — Detection-to-Alert Pipeline

Automatically converts fraudulent detections from `FraudDetection()` into persisted alert records:

```
FraudDetection() ──filter(is_fraudulent)──▶ Generate alert_id ──▶ FraudAlerts table
```

Each alert receives:
- `alert_id` = `"ALERT-" + transaction_id`
- `alert_timestamp` = `now()`
- `alert_status` = `"New"`

---

#### 10. `MultiChannelSwitching()` — Channel-Hopping Detection

Detects rapid switching between transaction channels (ATM → Online → Mobile → POS) as an indicator of account compromise:

| Severity | Criteria |
|---|---|
| **Critical** | ≥ 5 channel switches in 1 hour |
| **High** | ≥ 3 channel switches in 1 hour |
| **Medium** | Rapid switches within 30-min window |

---

#### 11. `MerchantCategoryAnomaly()` — Category Spending Deviation

Compares daily spending per merchant category against baseline:

| Severity | Criteria |
|---|---|
| **Critical** | Daily spend > 10× category baseline |
| **High** | Daily spend > 5× category baseline |
| **Medium** | Daily count > 3× category baseline |

---

#### 12. `GeographicVelocityCheck()` — Impossible Travel Detection

Flags transactions from different countries within physically impossible travel times:

| Severity | Time Gap |
|---|---|
| **Critical** | < 1 hour between countries |
| **High** | < 2 hours between countries |
| **Medium** | < 4 hours between countries |

---

### Dashboard & Investigation Functions

#### 9. `RealTimeFraudDashboard()` — Unified Alert Feed

Combines alerts from **5 detection engines** into a single normalized stream:

```kql
union
    fraud_alerts,       // From FraudDetection()
    velocity_alerts,    // From VelocityDetection()
    crossborder_alerts, // From CrossBorderFraud() where Critical
    amount_anomalies,   // From AmountAnomalyDetection()
    account_takeover    // From AccountTakeoverDetection()
| project timestamp, transaction_id, customer_id, amount,
         detection_type, severity, details
| order by timestamp desc
```

---

#### 13. `FraudInvestigator(target_customer_id)` — Customer Deep Dive

The only parameterized function — accepts a `customer_id` and returns a comprehensive investigation profile:

```kql
// Investigate a specific customer
FraudInvestigator("CUST-001")
```

Returns labeled key-value rows covering customer info, risk profile, and fraud indicators.

---

#### 14. `FraudSummaryKPIs()` — Dashboard KPI Cards

Returns a single summary row with all key metrics:

| KPI | Description |
|---|---|
| `TotalTransactions` | Total count across all transactions |
| `FraudCount` | Number of transactions flagged as fraudulent |
| `FraudRate` | Percentage of transactions that are fraudulent |
| `FraudAmount` | Total dollar value of fraudulent transactions |
| `HighRiskCustomers` | Customers with risk score > 75 |
| `ActiveAlerts` | Current alert count in FraudAlerts table |
| `VelocityAlerts` | Count of rapid-fire transaction alerts |
| `CriticalCrossBorder` | Count of critical cross-border alerts |

---

## 📓 Using the Notebook

The `notebooks/` directory is available for Jupyter notebooks that connect to the Eventhouse for interactive analysis.

### Setup

```python
# Install dependencies
pip install -r requirements.txt

# Configure connection
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder

cluster_uri = "https://your-eventhouse-uri.kusto.fabric.microsoft.com"
database = "BankingFraudDB"

kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(cluster_uri)
client = KustoClient(kcsb)
```

### Sample Visualizations

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Fraud Trend Over Time
query = """
FraudDetection()
| where is_fraudulent == true
| summarize Count = count() by bin(timestamp, 1h)
| order by timestamp asc
"""
df = client.execute(database, query).primary_results[0].to_dataframe()
df.plot(x='timestamp', y='Count', kind='line', title='Fraud Trend Over Time')

# 2. Fraud Type Distribution
query = """
FraudDetection()
| where is_fraudulent == true
| summarize Count = count() by fraud_type
"""
df = client.execute(database, query).primary_results[0].to_dataframe()
df.plot(kind='pie', y='Count', labels=df['fraud_type'], title='Fraud by Type')

# 3. Channel Analysis
query = """
Transactions
| summarize TxnCount = count(), TotalAmount = sum(amount) by channel
"""
df = client.execute(database, query).primary_results[0].to_dataframe()
sns.barplot(data=df, x='channel', y='TotalAmount')
plt.title('Transaction Volume by Channel')
plt.show()
```

---

## 📁 Repository Structure

```
FraudDetection/
├── 📄 README.md                                    # This file
├── 📄 requirements.txt                             # Python dependencies
├── 📄 .gitignore                                   # Git ignore rules
├── 📄 LICENSE                                      # MIT License
│
├── 📂 kql/                                         # All KQL scripts
│   ├── 📂 tables/                                  # Table DDL scripts (run first)
│   │   ├── 01_create_customers.kql                 #   Customers table
│   │   ├── 02_create_bankaccounts.kql              #   BankAccounts table
│   │   ├── 03_create_merchants.kql                 #   Merchants table
│   │   ├── 04_create_transactions.kql              #   Transactions table
│   │   └── 05_create_fraudalerts.kql               #   FraudAlerts table
│   │
│   ├── 📂 functions/                               # Detection function scripts (run second)
│   │   ├── 01_fraud_detection.kql                  #   Core fraud scoring
│   │   ├── 02_velocity_detection.kql               #   Rapid-fire detection
│   │   ├── 03_cross_border_fraud.kql               #   International risk
│   │   ├── 04_amount_anomaly_detection.kql         #   Spending anomaly
│   │   ├── 05_unusual_time_detection.kql           #   Off-hours activity
│   │   ├── 06_customer_risk_profile.kql            #   Composite risk scoring
│   │   ├── 07_account_takeover_detection.kql       #   Account takeover
│   │   ├── 08_fraud_alert_transform.kql            #   Detection → Alert pipeline
│   │   ├── 09_realtime_fraud_dashboard.kql         #   Unified alert feed
│   │   ├── 10_multi_channel_switching.kql          #   Channel-hopping detection
│   │   ├── 11_merchant_category_anomaly.kql        #   Category spending deviation
│   │   ├── 12_geographic_velocity_check.kql        #   Impossible travel
│   │   ├── 13_fraud_investigator.kql               #   Customer deep-dive
│   │   └── 14_fraud_summary_kpis.kql               #   Dashboard KPIs
│   │
│   ├── 📂 materialized-views/                      # Materialized view definitions (run third)
│   │   ├── 01_mv_hourly_transaction_stats.kql      #   Hourly rollup
│   │   ├── 02_mv_customer_daily_risk.kql           #   Daily customer risk
│   │   └── 03_mv_merchant_risk_profile.kql         #   Merchant-level risk
│   │
│   ├── 📂 policies/                                # Ingestion & caching policies
│   │   ├── 01_streaming_ingestion.kql              #   Enable streaming on Transactions
│   │   └── 02_caching.kql                          #   30-day hot cache on FraudAlerts
│   │
│   └── 📄 deploy_all.kql                           # Master deployment order reference
│
├── 📂 notebooks/                                   # Jupyter notebooks
│   └── banking_fraud_detection.ipynb               #   Interactive analysis (add manually)
│
├── 📂 data/                                        # Sample data & schemas
│   ├── 📄 schema_export.json                       #   Full schema definition (tables, functions, MVs)
│   ├── 📄 sample_customers.json                    #   Customer sample data
│   ├── 📄 sample_bankaccounts.json                 #   Bank account sample data
│   ├── 📄 sample_merchants.json                    #   Merchant sample data
│   └── 📄 sample_transactions.json                 #   Transaction sample data
│
├── 📂 dashboard/                                   # Dashboard artifacts
│   └── 📄 dashboard_queries.kql                    #   15-tile dashboard KQL queries
│
└── 📂 images/                                      # Dashboard screenshots
    ├── RTI Dashboard 1.png                         #   Fraud Command Center (KPIs)
    ├── RTI Dashboard 2.png                         #   Detection Details & Risk
    ├── RTI Dashboard 3.png                         #   Velocity, Cross-Border, Anomalies
    └── RTI Dashboard 4.png                         #   Trends & Analytics
```

---

## 🔑 Key Performance Indicators

The following KPIs are generated by `FraudSummaryKPIs()` based on the sample dataset:

| KPI | Value | Description |
|---|---|---|
| 📊 **Total Transactions** | 10,000 | Full sample dataset size |
| 🚨 **Fraud Rate** | ~0.43% | Percentage of transactions flagged as fraudulent |
| 💰 **Fraud Amount** | ~$255,600.90 | Total dollar value of suspicious transactions |
| 👤 **High-Risk Customers** | ~232 | Customers with composite risk score > 75 |
| ⚡ **Velocity Alerts** | ~4 | Rapid-fire transaction patterns detected |
| 🌍 **Cross-Border Critical** | ~221 | High-risk international transactions |
| 📋 **Active Alerts** | ~86 | Total fraud alerts in FraudAlerts table |
| 🏪 **Merchant Categories** | 10+ | Categories with risk profiling |

> 📝 **Note:** Values are approximate and depend on sample data generation. Re-run `FraudSummaryKPIs()` after data ingestion for exact figures.

---

## 🛡️ Data Schema Reference

### Entity-Relationship Model

```
┌──────────────┐         ┌───────────────┐         ┌──────────────┐
│   Customers  │────1:N──│  BankAccounts │────1:N──│ Transactions │
│              │         │               │         │              │
│ customer_id  │         │ account_id    │         │ transaction_ │
│ risk_score   │         │ customer_id   │         │ id           │
│ is_high_risk │         │ balance       │         │ amount       │
└──────────────┘         │ credit_limit  │         │ timestamp    │
                         └───────────────┘         │ channel      │
                                                   └──────┬───────┘
┌──────────────┐                                          │
│  Merchants   │──────────────────────────────────────N:1──┘
│              │
│ merchant_id  │         ┌───────────────┐
│ risk_level   │         │  FraudAlerts  │
│ category     │         │               │
└──────────────┘         │ alert_id      │
                         │ fraud_score   │
                         │ fraud_type    │
                         │ is_fraudulent │
                         │ alert_status  │
                         └───────────────┘
```

### Table Record Counts (Sample Data)

| Table | Approximate Records |
|---|---|
| `Customers` | ~500 |
| `BankAccounts` | ~700 |
| `Merchants` | ~200 |
| `Transactions` | ~10,000 |
| `FraudAlerts` | ~86 (generated by detection functions) |

---

## ❓ Troubleshooting

| Issue | Solution |
|---|---|
| **Functions return empty results** | Ensure tables have data. Run `Transactions \| count` to verify. |
| **Materialized views not updating** | Check view status: `.show materialized-views`. Ensure backfill completed. |
| **Streaming ingestion errors** | Verify the policy is enabled: `.show table Transactions policy streamingingestion`. |
| **Dashboard tiles show "No data"** | Confirm the data source is connected to `BankingFraudDB` and functions are deployed. |
| **FraudInvestigator returns no data** | Verify the `target_customer_id` exists: `Customers \| where customer_id == "CUST-001"`. |
| **Data Agent not responding** | Ensure the agent is configured with the correct KQL Database and has access permissions. |
| **Cross-border detection too noisy** | Adjust the amount threshold in `CrossBorderFraud()` (default: > $100). |
| **High-risk customer count seems high** | The risk score threshold is > 75. Adjust in `CustomerRiskProfile()` if needed. |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** this repository.
2. **Create** a feature branch: `git checkout -b feature/my-new-detection`.
3. **Add** your KQL functions to `kql/functions/` following the naming convention (`XX_function_name.kql`).
4. **Test** your functions against the sample dataset.
5. **Update** `kql/deploy_all.kql` with your new function reference.
6. **Submit** a Pull Request with a clear description.

### Contribution Guidelines

- Follow the existing naming conventions for KQL scripts.
- Include a docstring in your function definitions.
- Test all functions before submitting.
- Update this README if adding new features or detection algorithms.
- Keep detection functions idempotent (re-runnable without side effects).

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Banking Fraud Detection POC Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  <b>Built with ❤️ using Microsoft Fabric Real-Time Intelligence</b><br>
  <i>Protecting customers, one transaction at a time.</i>
</p>
