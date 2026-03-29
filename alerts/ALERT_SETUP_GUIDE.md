# 🔔 Fraud Alert Notifications Setup Guide

## Overview

This guide configures **real-time fraud alert notifications** via **Email** and **Microsoft Teams** using **Fabric Activator (Reflex)**. When the system detects an anomalous or fraudulent transaction, alerts are automatically triggered.

## Architecture

```
┌──────────────────┐     ┌─────────────────────┐     ┌──────────────────┐
│  BankingFraudDB  │────▶│  Fabric Activator    │────▶│  📧 Email Alert  │
│  (KQL Database)  │     │  (BankingFraud       │     │  📱 Teams Alert  │
│                  │     │   AlertNotifier)      │     │                  │
│  • Transactions  │     │                      │     │  Recipients:     │
│  • FraudAlerts   │     │  8 Alert Rules:      │     │  • Fraud Ops Team│
│  • Detection     │     │  • High-Value Fraud  │     │  • Risk Manager  │
│    Functions     │     │  • Velocity Attack   │     │  • Compliance    │
│                  │     │  • Account Takeover  │     │                  │
└──────────────────┘     │  • Impossible Travel │     └──────────────────┘
                         │  • Amount Anomaly    │
                         │  • Night Activity    │
                         │  • Channel Switching │
                         │  • Cross-Border      │
                         └─────────────────────┘
```

## Alert Rules Summary

| # | Alert Name | KQL File | Trigger Condition | Severity | Frequency | Notification |
|---|---|---|---|---|---|---|
| 1 | **High-Value Fraud** | `01_high_value_fraud_alert.kql` | Fraud flagged + Amount > $2,000 | 🔴 Critical / 🟠 High | Every 5 min | Email + Teams |
| 2 | **Velocity Attack** | `02_velocity_attack_alert.kql` | Multiple txns < 5 min apart | 🔴 Critical | Every 2 min | Email + Teams |
| 3 | **Account Takeover** | `03_account_takeover_alert.kql` | 10+ txns/hr OR 3+ countries/hr | 🔴 Critical | Every 5 min | Email + Teams |
| 4 | **Impossible Travel** | `04_impossible_travel_alert.kql` | Country change < 4 hours | 🔴 Critical / 🟠 High | Every 10 min | Email + Teams |
| 5 | **Amount Anomaly** | `05_amount_anomaly_alert.kql` | Spending > 5x customer average | 🟠 High / 🟡 Medium | Every 5 min | Email + Teams |
| 6 | **Night Activity** | `06_night_activity_alert.kql` | Transactions 12AM–5AM | 🟠 High / 🟡 Medium | Every 30 min | Email (digest) |
| 7 | **Channel Switching** | `07_multi_channel_switch_alert.kql` | 3+ channel switches in 30 min | 🟠 High / 🟡 Medium | Every 10 min | Email + Teams |
| 8 | **Cross-Border Critical** | `08_cross_border_critical_alert.kql` | International + Critical risk | 🔴 Critical | Every 5 min | Email + Teams |

---

## Step-by-Step Setup

### Method 1: From Real-Time Dashboard (Recommended)

This is the easiest way — set alerts directly from dashboard tiles.

#### Step 1: Open the Fraud Dashboard
1. Go to **RTI_IQ_01** workspace
2. Open **"RealTime Fraud Detection Dashboard"** or **"Banking Fraud Command Center"**

#### Step 2: Set Alert on a Dashboard Tile
1. Hover over any tile (e.g., "Real-Time Alert Feed")
2. Click the **⋯ (More options)** menu → **"Set alert"**
3. This opens the Activator alert builder

#### Step 3: Configure the Alert Rule
1. **Condition**: Select the measure column (e.g., `fraud_score`)
2. **Operator**: "Is greater than" → Value: `3`
3. **Action**: 
   - ✅ **Send me an email** — enters your email
   - ✅ **Send a Teams message** — select channel/chat
4. **Check every**: `5 minutes`
5. Click **Create**

#### Step 4: Repeat for Each Alert Type
Create separate alerts for:
- **Fraud Score > 4** → CRITICAL alert (Email + Teams)
- **Fraud Score > 3** → HIGH alert (Email only)
- **Amount > $5,000** on fraud transactions → CRITICAL
- **Velocity Alerts count > 0** → CRITICAL (Email + Teams)

---

### Method 2: From Fabric Activator (Reflex) Item

For more advanced alert configurations with custom KQL.

#### Step 1: Open the Activator
1. In **RTI_IQ_01** workspace, find **"BankingFraudAlertNotifier"** (Reflex item)
2. Or navigate to: Workspace → + New → Reflex

#### Step 2: Add Data Source
1. Click **"Select a data source"**
2. Choose **"KQL Database"** → Select **"BankingFraudDB"**
3. In the KQL query box, paste the alert query from the `.kql` files

#### Step 3: Configure Alert 1 — High-Value Fraud
1. Paste the query from `01_high_value_fraud_alert.kql`
2. Set **Object**: `CustomerID` (the entity being monitored)
3. Set **Trigger**:
   - Property: `FraudScore`
   - Condition: `Becomes greater than` → `3`
4. Set **Action**:
   - **Email**: Add fraud team distribution list
   - **Teams**: Select the Fraud Operations channel
5. Set **Evaluation frequency**: `Every 5 minutes`

#### Step 4: Configure Alert 2 — Velocity Attack
1. Add new trigger → Paste `02_velocity_attack_alert.kql`
2. **Object**: `AccountID`
3. **Trigger**: `TimeDiffMinutes` becomes less than `5`
4. **Action**: Email + Teams (URGENT priority)
5. **Frequency**: `Every 2 minutes`

#### Step 5: Configure Alert 3 — Account Takeover
1. Add new trigger → Paste `03_account_takeover_alert.kql`
2. **Object**: `CustomerID`
3. **Trigger**: `TransactionsPerHour` becomes greater than `10`
4. **Action**: Email + Teams (CRITICAL)
5. **Frequency**: `Every 5 minutes`

#### Step 6: Configure Remaining Alerts
Repeat for alerts 4–8 using the corresponding `.kql` files.

#### Step 7: Start the Activator
1. Click **"Start"** to activate all alert rules
2. Monitor the **"Alert History"** tab for triggered alerts

---

### Method 3: From KQL Queryset (Manual Query + Alert)

#### Step 1: Open FraudInvestigator_IQ
1. Open the KQL Queryset in the workspace
2. Run any alert query to verify results

#### Step 2: Pin to Dashboard + Set Alert
1. After running a query, click **"Pin to dashboard"**
2. On the pinned tile, use **"Set alert"** to configure notifications

---

## Teams Channel Configuration

### Option A: Teams Webhook (Recommended for Teams Channels)

1. In Microsoft Teams, go to the target channel
2. Click **⋯** → **Connectors** → **Incoming Webhook**
3. Name it: **"Fabric Fraud Alerts"**
4. Copy the webhook URL
5. In Fabric Activator, choose **"Teams"** action and paste the webhook URL

### Option B: Direct Teams Notification

1. In Activator alert action, select **"Post to Teams"**
2. Choose the team and channel
3. The alert message will appear as an Adaptive Card with:
   - Alert severity badge (🔴🟠🟡🟢)
   - Transaction details
   - Quick action buttons (Investigate / Dismiss / Escalate)

---

## Email Notification Configuration

### Alert Email Format

```
Subject: 🔴 [CRITICAL] Banking Fraud Alert — $9,598.71 Amount Anomaly

Body:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ FRAUD ALERT — Amount Anomaly Detected
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Severity:     🔴 CRITICAL
Alert Time:   2026-03-29 10:35:00 UTC
Customer:     CUST000595 (Jason Jones)
Amount:       $9,598.71
Merchant:     Phone Hub #360
Channel:      Online
Deviation:    15.25x above average ($629.42)

🔗 Investigate in Dashboard:
   [Open Dashboard] [View Customer Profile] [Block Account]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Distribution Lists

| Severity | Recipients | Frequency |
|---|---|---|
| 🔴 Critical | fraud-critical@bank.com, Teams #fraud-war-room | Immediate |
| 🟠 High | fraud-ops@bank.com, Teams #fraud-alerts | Every 5 min |
| 🟡 Medium | fraud-review@bank.com | Hourly digest |
| 🟢 Low | fraud-log@bank.com | Daily summary |

---

## Monitoring & Maintenance

### Check Alert Health
```kql
// Verify alert queries return expected results
FraudDetection()
| where is_fraudulent == true
| summarize Count = count() by bin(timestamp, 1h)
| where Count > 0
| order by timestamp desc
| take 5
```

### Alert Volume Monitoring
```kql
// Track daily alert volume to detect alert fatigue
FraudAlerts
| summarize 
    TotalAlerts = count(),
    CriticalAlerts = countif(fraud_score > 4),
    HighAlerts = countif(fraud_score > 3 and fraud_score <= 4),
    MediumAlerts = countif(fraud_score > 2 and fraud_score <= 3)
    by bin(timestamp, 1d)
| order by timestamp desc
```

---

## Fabric Activator Item Created

| Property | Value |
|---|---|
| **Name** | BankingFraudAlertNotifier |
| **Type** | Reflex (Activator) |
| **ID** | `34320c26-9ebf-4a22-8a25-b3186078bf85` |
| **Workspace** | RTI_IQ_01 |
| **Data Source** | BankingFraudDB (KQL Database) |
| **Alert Rules** | 8 (High-Value, Velocity, Takeover, Travel, Anomaly, Night, Channel, Cross-Border) |
