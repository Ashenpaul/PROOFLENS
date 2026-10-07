# HNX26PSI08: Proof-Carrying Data Analyst (Agentic GenAI)

[![Hackathon](https://img.shields.io/badge/Hackathon-HACKNEX_Internal_Qualifier-blue.svg)](https://forms.gle/KGjkU5u66Va1MDhu5)
[![Status](https://img.shields.io/badge/Verification-100%25_Reproducible-success.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#)
WEB PAGE LINK:https://ashenpaul.github.io/PROOFLENS/

Presented by: **Division of Computer Science and Engineering, Karunya Institute of Technology and Sciences**  
Domain: **Agentic GenAI · Data Analytics · Code Generation · Verification**

---

## 1. Project Overview

Real-world enterprise data is messy, fragmented across heterogeneous sources (CSVs, relational databases, CRM JSONs, external API dumps), and littered with silent failure modes: conflicting currency denominations, duplicate transaction webhooks, ambiguous date notations, and irreconcilable cross-table contradictions. 

Standard LLM-based data analysts fail catastrophically in these settings:
1. **Hallucinated Math:** They generate authoritative-sounding numbers that do not match the underlying rows.
2. **Untraceable Answers:** They provide conclusions without verifiable calculation paths.
3. **Overconfidence in Ambiguity:** They hallucinate answers to trick questions rather than stating that data is missing or contradictory.

**Proof-Carrying Data Analyst (PCDA)** solves this fundamental challenge. Inspired by Proof-Carrying Code (PCC) principles from formal verification, **every numerical claim emitted by the agent is bundled with self-contained, re-runnable Python proof code**. An independent, sandboxed Verifier executes this code in an isolated subprocess to validate the exact calculation before any answer is certified. Furthermore, an **Ambiguity & Trap Guardrail** detects contradictory datasets, ambiguous dates, and trick premises, refusing to provide false certainty when data integrity is compromised.

---

## 2. Key Architecture & Features

```
                      ┌───────────────────────────────────────┐
                      │             User Query                │
                      └──────────────────┬────────────────────┘
                                         │
                                         ▼
                 ┌─────────────────────────────────────────────────┐
                 │       Data Profiler & Trap Detection Gate       │
                 │   - Primary key duplicate collisions            │
                 │   - Mixed currencies ($ vs € vs £)              │
                 │   - Ambiguous slash-dates (DD/MM vs MM/DD)      │
                 │   - Cross-table accounting contradictions       │
                 │   - Discontinued products & temporal tricks     │
                 └───────────────┬─────────────────┬───────────────┘
                                 │                 │
                [Trap Detected]  │                 │  [Clean / Resolvable]
                                 ▼                 ▼
          ┌────────────────────────────┐    ┌──────────────────────────────────┐
          │ Safe Refusal Protocol      │    │ Autonomous Code Proof Synthesis  │
          │ "I cannot determine this   │    │ - Explicit deduplication         │
          │  due to contradiction..."  │    │ - Exchange rate normalization    │
          │ Emits evidentiary audit    │    │ - Null-safe mathematical logic   │
          └──────────────┬─────────────┘    └────────────────┬─────────────────┘
                         │                                   │
                         │                                   ▼
                         │                  ┌──────────────────────────────────┐
                         │                  │   Independent Sandbox Verifier   │
                         │                  │   - Isolated Subprocess Execution│
                         │                  │   - Strict Timeout & Exit Check  │
                         │                  │   - PROOF_RESULT Token Parser    │
                         │                  │   - Numerical Discrepancy Gate   │
                         │                  └────────────────┬─────────────────┘
                         │                                   │
                         │                                   ▼
                         ▼                  ┌──────────────────────────────────┐
          ┌────────────────────────────┐    │ Signed Proof Certificate (JSON)  │
          │ Refusal Audit Certificate  │    │ - SHA-256 Code Hash              │
          │ - Table & Column citations │    │ - Dataset Fingerprints           │
          │ - Ratio discrepancy metric │    │ - Claimed vs Verified Values     │
          └────────────────────────────┘    │ - Latency & Determinism Log      │
                                            └──────────────────────────────────┘
```

---

## 3. Trap & Adversarial Defense Suite

The PCDA engine specifically counters all 7 traps outlined in the Problem Statement:

| Trap Type | Description & Real-World Manifestation | PCDA Defense Mechanism |
| :--- | :--- | :--- |
| **Units Mismatch ($ / € / £)** | Transactions recorded in EUR and GBP mixed with USD values without explicit conversions. | Ingests `exchange_rates.csv`, joins currency conversion factors, and normalizes all lines to USD base currency. |
| **Ambiguous Dates** | Date entries like `06/07/2023` where day and month are both $\le 12$, making DD/MM vs MM/DD ambiguous. | Flags date ambiguity; refuses queries dependent on ambiguous dates with explicit evidentiary rationale. |
| **Duplicate Rows** | Webhook retries duplicating transaction rows (`TX-1004` appears twice). | Profiler detects key collisions; synthesized proof code explicitly executes `.drop_duplicates(subset=['tx_id'])`. |
| **Table Contradictions** | `regional_summaries.csv` claims APAC 2023 revenue is \$2.5M, while itemized lines in `sales_transactions.csv` sum to \$4.75K. | Detects the 526x conflict; refuses calculation with forensic audit citing both files, row values, and notes. |
| **Missing Data / Nulls** | Missing discount rates, null customer IDs. | Null-safe imputation (`.fillna(0.0)`) and inner join validation. |
| **Trick Premise Questions** | Query asks for 2024 revenue of `PROD-104` (discontinued in 2021). | Cross-checks `product_catalog.csv` status and dates; immediately refuses with invalid premise citation. |
| **Non-Existent Entities** | Query asks for metrics in regions not present in dataset (e.g. Australia). | Validates entity existence before attempting execution; refuses with missing entity notice. |

---

## 4. File Structure

```
proof-carrying-data-analyst/
├── README.md                      # Complete system documentation & evaluation guide
├── requirements.txt               # Dependencies (pandas, numpy)
├── .gitignore                     # Git configuration
├── run_demo.py                    # 1-Click end-to-end demonstration runner
├── data/                          # Benchmark messy multi-table data
│   ├── create_sample_data.py      # Deterministic generator script
│   ├── sales_transactions.csv     # Messy transactions (dupes, mixed currencies, dates)
│   ├── exchange_rates.csv         # Foreign exchange rates
│   ├── product_catalog.csv        # Product catalog with discontinued dates
│   ├── regional_summaries.csv     # Contradictory un-audited regional claims
│   └── customers_crm.json         # CRM customer data
├── pcda/                          # Core engine package
│   ├── __init__.py
│   ├── config.py                  # System constants and paths
│   ├── data_profiler.py           # Deep anomaly & contradiction profiler
│   ├── traps.py                   # Adversarial trap detection & refusal gate
│   ├── agent.py                   # Proof-carrying reasoning agent
│   ├── chatbot.py                 # Conversational AI assistant & evaluator Q&A engine
│   ├── verifier.py                # Subprocess sandbox proof verifier
│   ├── proof_certificate.py       # Cryptographic certificate builder & hasher
│   └── cli.py                     # Rich command-line interface
├── web/                           # Interactive Web Dashboard
│   ├── app.py                     # Zero-dependency Python HTTP server (with /api/chat)
│   └── static/
│       ├── index.html             # Conversational Chatbot & Verifier Dashboard GUI
│       └── app.js                 # Asynchronous client controller
└── tests/                         # Test suites
    └── test_benchmark.py          # 10 Automated benchmark scenarios (100% pass)
```

---

## 5. Getting Started & Setup

### Prerequisites
- Python 3.10+ (Standard Python library + `pandas` and `numpy`)

### 1. Installation
Clone the repository and install the minimal dependencies:
```bash
git clone <your-repo-url>
cd proof-carrying-data-analyst
pip install -r requirements.txt
```

### 2. Generate Benchmark Datasets
The repository includes pre-generated benchmark data. To regenerate or inspect the generation logic:
```bash
python data/create_sample_data.py
```

---

## 6. Running the System

### Option A: 1-Click Full End-to-End Demo
Run the automated demonstration covering all core requirements, messy data hygiene, trap refusals, and sandbox verification:
```bash
python run_demo.py
```

### Option B: Interactive Command-Line Interface (CLI)
Query the analyst, profile datasets, or verify external proof scripts:

```bash
# 1. Profile datasets for traps, collisions, and contradictions
python -m pcda.cli profile

# 2. Ask a valid analytical question (synthesizes proof and verifies)
python -m pcda.cli ask "What is the total net revenue in USD?"

# 3. Test the Contradiction Trap Guardrail (APAC regional revenue mismatch)
python -m pcda.cli ask "What is the total revenue for APAC in 2023?"

# 4. Test the Discontinued Product Trick Guardrail
python -m pcda.cli ask "What was the total revenue for PROD-104 in 2024?"

# 5. Test the Ambiguous Date Guardrail
python -m pcda.cli ask "What was the transaction amount on 06/07/2023?"

# 6. Verify an external Python proof script independently
python -m pcda.cli verify "proof_artifacts/<proof_id>.py" --expected 16674.5
```

### Option C: Interactive Web Dashboard
Launch the zero-dependency browser-based interface:
```bash
python -m web.app
```
Then navigate to **`http://localhost:8080`** in any web browser.

The Web Dashboard provides:
- **Live Anomaly Radar:** Real-time visibility into table schemas, duplicates, and contradictions.
- **Interactive Query Console:** One-click presets to trigger valid queries or adversarial traps.
- **Proof-Carrying Result Viewer:** Formatted code viewer with SHA-256 signatures and execution metrics.
- **Independent Sandbox Verifier:** Paste any arbitrary Python code to execute in an isolated sandbox and re-verify claims.
- **1-Click Benchmark Button:** Automatically runs all 10 benchmark test cases.

---

## 7. Sample Input & Output Demonstration

### Example 1: Valid Calculation with Data Cleansing & Verifier
**User Query:**
```text
What is the total net revenue in USD?
```

**Agent Profiling Action:**
- Detects duplicate `TX-1004` (Webhook retry).
- Detects mixed currencies: USD, EUR (`rate_to_usd: 1.08`), and GBP (`rate_to_usd: 1.27`).
- Detects null discount rates in row `TX-1006` (imputes 0.0).

**Synthesized Executable Proof Script:**
```python
import pandas as pd
import numpy as np

# Load tables
df_tx = pd.read_csv(r"data/sales_transactions.csv")
df_rates = pd.read_csv(r"data/exchange_rates.csv")

# 1. Deduplication: Drop duplicate transaction rows by tx_id
df_tx = df_tx.drop_duplicates(subset=["tx_id"]).copy()

# 2. Join currency exchange rates to normalize all revenues to USD
df_merged = df_tx.merge(df_rates[["currency", "rate_to_usd"]], on="currency", how="left")

# 3. Clean null discounts
df_merged["discount_pct"] = df_merged["discount_pct"].fillna(0.0)

# 4. Compute line item net revenue in USD: quantity * unit_price * (1 - discount_pct) * rate_to_usd
df_merged["net_revenue_usd"] = (
    df_merged["quantity"] * 
    df_merged["unit_price"] * 
    (1.0 - df_merged["discount_pct"]) * 
    df_merged["rate_to_usd"]
)

total_net_revenue = float(df_merged["net_revenue_usd"].sum())
print(f"PROOF_RESULT: {total_net_revenue:.4f}")
```

**Independent Sandbox Verifier Execution:**
- Isolated Subprocess Return Code: `0`
- Extracted `PROOF_RESULT`: `16674.5000`
- Match with Claimed Value: **`MATCH (Within tolerance 1e-4)`**
- Status: **`VERIFIED`**

**Emitted Cryptographic Proof Certificate:**
```json
{
  "proof_id": "proof_5b087159bd7f",
  "status": "VERIFIED",
  "claimed_answer": 16674.5,
  "verified_answer": 16674.5,
  "discrepancy": 0.0,
  "code_sha256": "b94d7ffb748105bbd4801084434f52c4317e33d0941cba105bd7f4728185407e",
  "execution_time_ms": 1047.23
}
```

---

### Example 2: Contradictory Data Trap (Refusal with Evidence)
**User Query:**
```text
What is the total revenue for APAC in 2023?
```

**Agent Evaluation:**
- Scans `regional_summaries.csv` -> APAC reported revenue: **\$2,500,000.00** (Notes: *"UNAUDITED CONFLICT"*).
- Scans `sales_transactions.csv` -> APAC line items sum: **\$4,750.00**.
- Identifies **526.3x contradiction**.

**System Response:**
```text
[STATUS]: REFUSED (Safe Guardrail Active)
[REASON]: I cannot determine the APAC revenue reliably from the data. 
There is a severe cross-table contradiction: 'regional_summaries.csv' reports 
$2,500,000.00 (UNAUDITED CONFLICT: Flash estimates from regional sales lead), 
whereas itemized transactions in 'sales_transactions.csv' sum to $4,750.00 
(a 526.32x mismatch). Answering without an authoritative reconciliation would 
produce a falsified or arbitrary metric.
[TRAP TYPE]: CONTRADICTORY_DATA_SOURCES
```

---

## 8. Benchmark Evaluation & Verification Results

The test suite in [`tests/test_benchmark.py`](file:///C:/Users/ashen/.gemini/antigravity/scratch/proof-carrying-data-analyst/tests/test_benchmark.py) evaluates 10 adversarial and analytical scenarios:

```bash
python -m unittest tests\test_benchmark.py
```

### Benchmark Summary Matrix:
| Test ID | Scenario | Trap Type | Result | Time |
| :---: | :--- | :--- | :---: | :---: |
| **TC01** | Multi-Currency Net Revenue with Deduplication | Clean / Hygiene | **PASS (VERIFIED)** | 1.05s |
| **TC02** | Total Gross Revenue Calculation | Clean / Hygiene | **PASS (VERIFIED)** | 1.02s |
| **TC03** | Product Catalog Join & Category Filtering | Multi-Table Join | **PASS (VERIFIED)** | 1.06s |
| **TC04** | CRM Join & Enterprise Customer Tier Revenue | Multi-Table CRM | **PASS (VERIFIED)** | 1.02s |
| **TC05** | Unique Customer Count Handling Nulls | Dirty Data / Nulls | **PASS (VERIFIED)** | 0.98s |
| **TC06** | Contradictory Regional Sources (APAC) | Contradiction Trap | **PASS (REFUSED)** | 0.05s |
| **TC07** | Discontinued Product Temporal Premise (PROD-104) | Trick Question | **PASS (REFUSED)** | 0.04s |
| **TC08** | Ambiguous Date Notation (`06/07/2023`) | Ambiguous Date | **PASS (REFUSED)** | 0.04s |
| **TC09** | Missing Currency Rate (Bitcoin) | Unit Trap | **PASS (REFUSED)** | 0.04s |
| **TC10** | Non-Existent Entity / Country (Australia) | Missing Entity | **PASS (REFUSED)** | 0.04s |

**Overall Score: 10 / 10 Tests Passed (100% Pass Rate). Zero unverified numbers emitted.**

---

## 9. Scope Note (MVP vs. Stretch Goals)

### Minimum Viable Solution (Implemented & Verified):
- Autonomous Data Profiler detecting primary key duplicate collisions, currency mixtures, ambiguous dates, and accounting discrepancies.
- Ambiguity & Contradiction Refusal Gate adhering to the rule: *"A confident wrong answer is worse than saying 'I cannot determine this from the data.'"*
- Automated Python proof code synthesis with explicit data hygiene (deduplication, FX normalization, null handling).
- Independent Subprocess Sandbox Verifier running in isolated environment with exit-code and tolerance checks.
- Cryptographic Proof Certificates with SHA-256 code hashing and input fingerprints.
- Full CLI and zero-dependency Web Dashboard.

### Stretch Goals Implemented:
- Self-healing code repair loop (`MAX_AGENT_RETRIES`) if generated code encounters syntax or execution anomalies.
- Decoupled Verifier API allowing external evaluators or third-party test runners to paste and execute arbitrary proof code.
- Interactive Web GUI with live code inspection and one-click benchmark trigger.

---

## 10. Declaration of Resources & AI Usage
- **Language & Runtime:** Python 3.10+ (Standard Library: `subprocess`, `hashlib`, `http.server`, `json`, `dataclasses`, `unittest`).
- **Data Analytics:** `pandas` and `numpy`.
- **Pre-trained Models / APIs:** Zero paid external API dependency required for verification execution — the deterministic proof sandbox and profiling engine run entirely local and offline.
- **Datasets:** Synthesized multi-table enterprise benchmark replicating realistic messy ERP, CRM, and foreign exchange environments.

---

## 11. Submission Checklist

- [x] **Working System:** End-to-end operational agent with CLI, Web UI, and verifiable proof output.
- [x] **Source Code:** Structured Git repository with complete source code and reproducible test suite.
- [x] **Data Pipeline:** Transparent multi-table ingestion with automated profiling, hygiene, and join pipelines.
- [x] **Core Model / Reasoning:** Hybrid Agentic reasoning pipeline with trap evaluation gates and code proof synthesis.
- [x] **Evidence & Explanation:** Cryptographic SHA-256 certificates, execution logs, and detailed refusal citations.
- [x] **Sample Input & Output:** Fully documented in README and runnable via `run_demo.py`.
- [x] **Scope Note:** Explicit MVP vs. Stretch goal demarcation.
- [x] **Live Demonstration:** `python run_demo.py` for CLI demo or `python -m web.app` for Web UI.
- [x] **Submission Link:** Ready for submission to [Hacknex Qualifier Form](https://forms.gle/KGjkU5u66Va1MDhu5).
