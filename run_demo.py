"""
End-to-End Live Demonstration Script for HNX26PSI08: Proof-Carrying Data Analyst.
Run this script to observe the entire system in action across all key scenarios:
1. Data Profiling & Trap Detection
2. Verifiable Calculation with Auto-Generated Proof Code
3. Sandbox Verification and Certificate Issuance
4. Rejection of Contradictory Data Traps
5. Rejection of Discontinued Product Trick Queries
6. Rejection of Ambiguous Date Queries
7. Independent Proof Verification
"""

import sys
import time
import json
from pathlib import Path

from pcda.config import DATA_DIR, ROOT_DIR
from pcda.data_profiler import DataProfiler
from pcda.agent import ProofCarryingDataAnalyst
from pcda.verifier import CodeVerifier

def print_separator(title=""):
    print("\n" + "=" * 70)
    if title:
        print(f" >>> {title.upper()}")
        print("=" * 70)

def main():
    print("""
######################################################################
#  HNX26PSI08: PROOF-CARRYING DATA ANALYST (AGENTIC GENAI) DEMO     #
#  Karunya Institute of Technology and Sciences - Hacknex Internal   #
######################################################################
    """)
    time.sleep(0.5)

    # 1. Dataset Profiling
    print_separator("Step 1: Ingesting & Profiling Messy Multi-Table Data")
    profiler = DataProfiler(DATA_DIR)
    profile = profiler.profile_all()
    print(f"Loaded {len(profile['tables'])} tables from '{DATA_DIR.name}/'")
    for name, info in profile['tables'].items():
        print(f"  * {name:<25}: {info['row_count']} rows, {info['duplicate_rows']} exact duplicates")
    
    print("\nActive Traps & Anomalies Identified by Profiler:")
    for d in profile['duplicate_warnings']:
        print(f"  [!] DUPLICATE KEY: {d['table']}.{d['column']} has {d['duplicate_count']} colliding records")
    for c in profile['currency_inconsistencies']:
        print(f"  [!] MIXED CURRENCIES: {c['table']}.{c['column']} -> {c['currencies_found']}")
    for a in profile['date_ambiguities']:
        print(f"  [!] AMBIGUOUS DATES: {a['table']}.{a['column']} -> {a['ambiguous_samples']}")
    for con in profile['cross_table_contradictions']:
        print(f"  [!] DATA CONTRADICTION: {con['reason']}")

    time.sleep(1)

    # Initialize Agent
    agent = ProofCarryingDataAnalyst(DATA_DIR)

    # 2. Answering Clean Query with Proof
    print_separator("Scenario 1: Analytical Query with Messy Data Hygiene")
    q1 = "What is the total net revenue in USD?"
    print(f"User Question: '{q1}'")
    print("Agent Action: Sanitizing duplicates, matching FX rates, synthesizing proof...")
    res1 = agent.answer_query(q1)

    print(f"\n[Status]: {res1['status']}")
    print(f"[Verified Answer]: ${res1['answer']:,.2f} USD")
    print(f"[Sandbox Execution Time]: {res1['verification_result']['execution_time_ms']:.2f} ms")
    print("\n[Synthesized Python Proof Script]:")
    print("-" * 50)
    print(res1['proof_code'].strip())
    print("-" * 50)
    print(f"[Cryptographic Proof ID]: {res1['certificate']['proof_id']}")
    print(f"[Code SHA-256]: {res1['certificate']['code_sha256']}")

    time.sleep(1)

    # 3. Contradiction Trap
    print_separator("Scenario 2: Trap - Cross-Table Contradiction")
    q2 = "What is the total revenue for APAC in 2023?"
    print(f"User Question: '{q2}'")
    print("Agent Action: Evaluating regional sources for consistency...")
    res2 = agent.answer_query(q2)

    print(f"\n[Status]: {res2['status']} (Safely Refused)")
    print(f"[Refusal Justification]:\n  {res2['refusal_reason']}")
    print(f"[Trap Classification]: {res2['trap_type']}")

    time.sleep(1)

    # 4. Discontinued Trick Question
    print_separator("Scenario 3: Trap - Discontinued Product Trick Question")
    q3 = "What was the total revenue for PROD-104 in 2024?"
    print(f"User Question: '{q3}'")
    print("Agent Action: Validating temporal status of products in catalog...")
    res3 = agent.answer_query(q3)

    print(f"\n[Status]: {res3['status']} (Safely Refused)")
    print(f"[Refusal Justification]:\n  {res3['refusal_reason']}")
    print(f"[Trap Classification]: {res3['trap_type']}")

    time.sleep(1)

    # 5. Ambiguous Date Trap
    print_separator("Scenario 4: Trap - Ambiguous Date Convention")
    q4 = "What was the transaction amount on 06/07/2023?"
    print(f"User Question: '{q4}'")
    print("Agent Action: Inspecting date locale clarity...")
    res4 = agent.answer_query(q4)

    print(f"\n[Status]: {res4['status']} (Safely Refused)")
    print(f"[Refusal Justification]:\n  {res4['refusal_reason']}")
    print(f"[Trap Classification]: {res4['trap_type']}")

    time.sleep(1)

    # 6. External Independent Verifier
    print_separator("Scenario 5: External Independent Verifier Execution")
    print("Demonstrating how an external evaluator runs the generated proof code in isolation:")
    verifier = CodeVerifier()
    matched, v_res = verifier.verify_claim(res1['answer'], res1['proof_code'], cwd=str(ROOT_DIR))
    print(f"Independent Subprocess Exit Code: {v_res.exit_code}")
    print(f"Independent Value Extracted: {v_res.verified_value}")
    print(f"Does it match the Agent's Claim? {'YES (VERIFIED)' if matched else 'NO'}")
    print(f"Stdout:\n  {v_res.stdout.strip()}")

    print_separator("Demonstration Complete")
    print("To launch the interactive Web Dashboard:")
    print("  python -m web.app")
    print("Then open: http://localhost:8080 in your browser.")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
