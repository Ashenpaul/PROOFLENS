# PROOFLENS
# HNX26PSI08: Proof-Carrying Data Analyst (Agentic GenAI)

[![Hackathon](https://img.shields.io/badge/Hackathon-HACKNEX_Internal_Qualifier-blue.svg)](https://forms.gle/KGjkU5u66Va1MDhu5)
[![Verification](https://img.shields.io/badge/Sandbox_Verification-100%25_Deterministic-success.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#)

> **Presented by:** Division of Computer Science and Engineering, Karunya Institute of Technology and Sciences  
> **Domain:** Agentic GenAI · Data Analytics · Code Generation · Verification  
> **Official Submission Form:** [https://forms.gle/KGjkU5u66Va1MDhu5](https://forms.gle/KGjkU5u66Va1MDhu5)

---

## 1. What the Project Does (Executive Summary)

Real-world enterprise data is fragmented across tables and documents, riddled with silent failure modes: conflicting currencies, duplicate rows, ambiguous date notations, and contradictory accounting tables. Standard LLMs fail in these environments because they **hallucinate unverified numbers** and **overconfidently answer trick or unanswerable questions**.

**Proof-Carrying Data Analyst (PCDA)** enforces the principles of Proof-Carrying Code (PCC):
1. **Zero Unverified Numbers (Iron Rule):** Every single numerical claim emitted by the AI is bundled with **self-contained, re-runnable Python proof code**. An independent, sandboxed Verifier executes this code in an isolated subprocess to validate the exact calculation before any answer is certified.
2. **Adversarial Trap Defense ("Know When to Say No"):** A confident wrong answer scores worse than saying *"I cannot determine this from the data"*. The system detects cross-table contradictions, ambiguous dates, and trick questions, refusing them with formal evidentiary justification.
3. **Upload Any Dataset:** Ingests any custom CSV or JSON dataset, dynamically parses schemas, sanitizes dirty rows, and synthesizes verifiable mathematical proofs.

---

## 2. Technologies, Libraries, and Models Used

- **Language & Runtime:** Python 3.10+ (Standard Library: `subprocess`, `hashlib`, `http.server`, `json`, `dataclasses`, `unittest`).
- **Data Engineering & Manipulation:** `pandas` (>= 2.0.0), `numpy` (>= 1.24.0).
- **Core Reasoning Architecture:** Agentic reasoning pipeline with automated code synthesis, dynamic table matching, and self-healing repair loops.
- **Verification Engine:** Isolated subprocess execution sandbox with strict execution timeouts, stdout token parsing (`PROOF_RESULT`), and floating-point tolerance gates ($\le 10^{-4}$).
- **Security & Integrity:** SHA-256 cryptographic proof certificates sealing generated code and raw data fingerprints.
- **User Interface:** Single-page responsive web dashboard and conversational AI chatbot styled with Tailwind CSS (zero external npm/node dependencies required).

---

## 3. Data Pipeline: How Data is Collected, Processed, and Passed
[Uploaded CSV/JSON] ──► [Data Profiler] ──► [Trap & Ambiguity Gate] │ ┌──────────────────────────────────┴──────────────────────────────────┐ │ │ ▼ [Trap / Contradiction / Ambiguity] ▼ [Valid & Cleanable] [Formal Refusal Protocol] [Dynamic Proof Code Synthesizer] - Cites exact conflicting files & rows - Primary key deduplication (.drop_duplicates) - Details discrepancy ratios (e.g. 526x mismatch) - Foreign currency FX normalization ($ / € / £) - Rejects invalid temporal premises - Null-safe imputation (.fillna) │ │ │ ▼ │ [Independent Sandbox Verifier] │ - Isolated subprocess execution │ - Exit code 0 & timeout enforcement │ - PROOF_RESULT numerical extraction │ │ ▼ ▼ [Refusal Audit Certificate] [Signed Cryptographic Certificate] - SHA-256 seal & table citations - SHA-256 code hash & data fingerprint

---
## 4. Trap Defense Matrix (Handling the 7 Traps from Problem 8)
| Trap from PDF | Problem in Real Data | PCDA Defense Mechanism | System Behavior |
| :--- | :--- | :--- | :---: |
| **1. Units don't match ($/€/£)** | Mixed currencies recorded without common denominations. | Ingests `exchange_rates.csv`, joins currency conversion factors, and normalizes all lines into base USD. | **VERIFIED (CLEANED)** |
| **2. Rows are duplicated** | Webhook retries duplicating transaction rows (`TX-1004` recorded twice). | Profiler catches key collisions; synthesized proof code explicitly executes `.drop_duplicates(subset=['tx_id'])`. | **VERIFIED (DEDUPED)** |
| **3. Tables contradict each other** | `regional_summaries.csv` claims APAC revenue is **\$2,500,000**, while itemized lines in `sales_transactions.csv` sum to **\$4,750**. | Detects the **526.3x contradiction**; refuses calculation with forensic audit citing both files, row values, and notes. | **REFUSED (EVIDENCE)** |
| **4. Dates are ambiguous** | Date written as `06/07/2023` where day and month are both $\le 12$ (could be June 7 or July 6). | Flags non-standard locale convention; refuses to calculate an arbitrary assumption without ISO-8601 clarification. | **REFUSED (AMBIGUOUS)** |
| **5. Question designed to trick you** | Query asks for 2024 revenue of `PROD-104` (discontinued in 2021). | Cross-checks `product_catalog.csv` lifecycle dates; immediately refuses because the question premise is invalid. | **REFUSED (TRICK)** |
| **6. Missing data / Nulls** | Missing discount rates (null) or null customer IDs. | Null-safe imputation (`.fillna(0.0)`) and inner join validation. | **VERIFIED (SAFE)** |
| **7. Question has no valid answer** | Query asks for sales in Australia when Australia does not exist in CRM/data. | Validates entity existence before attempting execution; refuses with missing entity notice. | **REFUSED (MISSING)** |
---
## 5. Sample Input and Output
### Sample A: Analytical Query with Messy Data Hygiene
- **User Query:** `"What is the total net revenue in USD?"`
- **Agent Action:** Deduplicates `TX-1004`, converts EUR and GBP into USD via `exchange_rates.csv`, imputes missing discount rates to 0.0.
- **Synthesized Python Proof Script:**
  ```python
  import pandas as pd
  df_tx = pd.read_csv("data/sales_transactions.csv").drop_duplicates(subset=["tx_id"])
  df_rates = pd.read_csv("data/exchange_rates.csv")
  df = df_tx.merge(df_rates[["currency", "rate_to_usd"]], on="currency", how="left")
  df["discount_pct"] = df["discount_pct"].fillna(0.0)
  net_revenue = float((df["quantity"] * df["unit_price"] * (1 - df["discount_pct"]) * df["rate_to_usd"]).sum())
  print(f"PROOF_RESULT: {net_revenue:.4f}")
Independent Sandbox Execution:
Subprocess Exit Code: 0
Extracted Number: 16674.5000
Match with Claim: MATCH (Within tolerance 1e-4)
Cryptographic Certificate Emitted:
json
{
  "proof_id": "proof_5b087159bd7f",
  "status": "VERIFIED",
  "claimed_answer": 16674.5,
  "verified_answer": 16674.5,
  "code_sha256": "b94d7ffb748105bbd4801084434f52c4317e33d0941cba105bd7f4728185407e",
  "execution_time_ms": 1047.23
}
Sample B: Contradictory Data Trap (Refusal with Evidence)
User Query: "What is the total revenue for APAC in 2023?"
System Output:
text
[STATUS]: REFUSED (Safe Guardrail Active)
[REASON]: I cannot determine the APAC revenue reliably from the data. 
There is a severe cross-table contradiction: 'regional_summaries.csv' reports 
$2,500,000.00 (UNAUDITED CONFLICT: Flash estimates from regional sales lead), 
whereas itemized transactions in 'sales_transactions.csv' sum to $4,750.00 
(a 526.32x mismatch). Answering without an authoritative reconciliation would 
produce a falsified or arbitrary metric.
[TRAP TYPE]: CONTRADICTORY_DATA_SOURCES
6. Scope Note (MVP vs. Stretch Goals)
Minimum Viable Solution (MVP - Completed):
Multi-table messy data ingestion and profiling (CSV, JSON).
Detection and safe refusal of ambiguous dates, table contradictions, and trick queries.
Automated Python proof code synthesis with explicit data hygiene (deduplication, FX normalization, null imputation).
Independent Subprocess Sandbox Verifier running in an isolated environment.
Cryptographic SHA-256 Proof Certificates.
Full Command-Line Interface (python -m pcda.cli ask).
Stretch Goals Implemented (Completed):
Universal Dataset Upload: Drag-and-drop or upload ANY arbitrary CSV/JSON dataset with dynamic schema reasoning.
Conversational AI Chatbot: Dual-mode assistant handling both analytical queries and project architecture Q&A.
Single-Page Window Web Dashboard: Streamlined, zero-clutter interface with live execution logs.
Self-Healing Code Repair Loop: Automatically fixes runtime code exceptions up to 3 retries.
Automated 10/10 Benchmark Suite: 100% reproducible test suite verifying all 7 traps and analytical calculations.
7. How to Install Dependencies and Run the System
1. Installation
bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>.git
cd <YOUR_REPO_NAME>
pip install -r requirements.txt
2. Run the Single-Page Web Dashboard & Chatbot (Recommended)
bash
python launch.py

Open http://localhost:8080 in any web browser. You can:

Upload any custom dataset.
Chat with the AI Analyst.
Test adversarial traps.
View cryptographic proof certificates.
3. Run the Automated Terminal Demonstration
bash
python run_demo.py

Executes all 5 core demonstration scenarios end-to-end.

4. Run the Full Test Benchmark Suite (Reproduce Demonstrated Results)
bash
python launch.py test

Or via standard unittest:

bash
python -m unittest tests/test_benchmark.py
8. Benchmark Evaluation Results Matrix (10 / 10 Passed)
Test ID	Evaluation Scenario	Category	Expected	System Status	Result
TC01	Multi-Currency Net Revenue & Deduplication	Clean / Hygiene	$16,674.50	VERIFIED	PASS
TC02	Total Gross Revenue Calculation	Clean / Hygiene	$17,950.00	VERIFIED	PASS
TC03	Product Catalog Join & Category Filtering	Multi-Table	10 Units	VERIFIED	PASS
TC04	CRM Tier Join & Enterprise Revenue	Multi-Table CRM	$9,628.90	VERIFIED	PASS
TC05	Unique Customer Count Handling Nulls	Dirty Data / Nulls	7 Customers	VERIFIED	PASS
TC06	Contradictory Regional Tables (APAC 526x Mismatch)	Contradiction Trap	Refusal	REFUSED	PASS
TC07	Discontinued Product Temporal Premise (PROD-104)	Trick Question	Refusal	REFUSED	PASS
TC08	Ambiguous Date Notation (06/07/2023)	Ambiguous Date	Refusal	REFUSED	PASS
TC09	Missing Currency Exchange Rate (Bitcoin)	Unit Trap	Refusal	REFUSED	PASS
TC10	Non-Existent Entity / Country (Australia)	Missing Entity	Refusal	REFUSED	PASS

Score: 10 / 10 Tests Passed (100% Pass Rate). Zero unverified numbers emitted.

9. Submission Declaration
Problem Statement Chosen: HNX26PSI08: Proof-Carrying Data Analyst (Agentic GenAI)
Institution: Karunya Institute of Technology and Sciences
Public Git Repository: Complete source code, datasets, and tests included.
Evaluation Integrity: Deterministic and reproducible locally offline without reliance on non-deterministic external LLM APIs.
