"""
Comprehensive Benchmark & Evaluation Test Suite for PCDA (HNX26PSI08).
Validates:
1. Correctness of mathematical calculations
2. Re-runnability of synthesized proof code by independent verifier
3. Automated handling of messy data (deduplication, mixed currencies, null rates)
4. Detection and rigorous refusal of traps (ambiguous dates, contradictory sources, discontinued products)
"""

import unittest
from pathlib import Path
from pcda.agent import ProofCarryingDataAnalyst
from pcda.verifier import CodeVerifier
from pcda.config import DATA_DIR, ROOT_DIR

BENCHMARK_CASES = [
    {
        "id": "TC01",
        "name": "Deduplication & Multi-Currency Net Revenue",
        "query": "What is the total net revenue in USD?",
        "expected_status": "VERIFIED",
        "expected_value_range": (16000.0, 17500.0),
        "is_trap": False
    },
    {
        "id": "TC02",
        "name": "Gross Revenue Calculation",
        "query": "What is the total gross revenue in USD?",
        "expected_status": "VERIFIED",
        "expected_value_range": (16500.0, 18500.0),
        "is_trap": False
    },
    {
        "id": "TC03",
        "name": "Multi-Table Product Category Filtering",
        "query": "What is the total quantity of AI products sold?",
        "expected_status": "VERIFIED",
        "expected_value_range": (8.0, 15.0),
        "is_trap": False
    },
    {
        "id": "TC04",
        "name": "CRM Multi-Table Tier Aggregation",
        "query": "What is the total revenue from enterprise tier customers?",
        "expected_status": "VERIFIED",
        "expected_value_range": (7000.0, 12000.0),
        "is_trap": False
    },
    {
        "id": "TC05",
        "name": "Unique Customer Count with Nulls",
        "query": "What is the count of unique customers?",
        "expected_status": "VERIFIED",
        "expected_value_range": (5.0, 10.0),
        "is_trap": False
    },
    {
        "id": "TC06",
        "name": "Trap: Contradictory Regional Sources (APAC)",
        "query": "What is the total revenue for APAC in 2023?",
        "expected_status": "REFUSED",
        "expected_trap_type": "CONTRADICTORY_DATA_SOURCES",
        "is_trap": True
    },
    {
        "id": "TC07",
        "name": "Trap: Discontinued Product Premise (PROD-104)",
        "query": "What was the total revenue for PROD-104 in 2024?",
        "expected_status": "REFUSED",
        "expected_trap_type": "DISCONTINUED_PRODUCT_TRICK",
        "is_trap": True
    },
    {
        "id": "TC08",
        "name": "Trap: Ambiguous Date Notation (06/07/2023)",
        "query": "What was the transaction amount on 06/07/2023?",
        "expected_status": "REFUSED",
        "expected_trap_type": "AMBIGUOUS_DATE_CONVENTION",
        "is_trap": True
    },
    {
        "id": "TC09",
        "name": "Trap: Missing Currency Rate (Bitcoin)",
        "query": "What was the total transaction volume in Bitcoin?",
        "expected_status": "REFUSED",
        "expected_trap_type": "MISSING_EXCHANGE_RATE",
        "is_trap": True
    },
    {
        "id": "TC10",
        "name": "Trap: Non-Existent Entity (Australia)",
        "query": "What was the revenue generated in Australia?",
        "expected_status": "REFUSED",
        "expected_trap_type": "MISSING_DATA_ENTITY",
        "is_trap": True
    }
]

def run_all_benchmarks():
    agent = ProofCarryingDataAnalyst(DATA_DIR)
    verifier = CodeVerifier()
    
    total = len(BENCHMARK_CASES)
    passed = 0
    failed = 0
    details = []

    for case in BENCHMARK_CASES:
        res = agent.answer_query(case["query"])
        status = res["status"]
        test_passed = False
        error_msg = None

        if case["is_trap"]:
            if status == "REFUSED" and res.get("trap_type") == case["expected_trap_type"]:
                test_passed = True
            else:
                error_msg = f"Expected REFUSED with {case['expected_trap_type']}, got status={status}, trap={res.get('trap_type')}"
        else:
            if status == "VERIFIED":
                val = res["answer"]
                min_v, max_v = case["expected_value_range"]
                if min_v <= val <= max_v:
                    # Test independent verifier re-execution
                    match, v_res = verifier.verify_claim(val, res["proof_code"], cwd=str(ROOT_DIR))
                    if match and v_res.success:
                        test_passed = True
                    else:
                        error_msg = f"Independent verifier failed re-check: {v_res.error_message}"
                else:
                    error_msg = f"Value {val} outside expected range [{min_v}, {max_v}]"
            else:
                error_msg = f"Expected VERIFIED, got {status}: {res.get('error') or res.get('refusal_reason')}"

        if test_passed:
            passed += 1
        else:
            failed += 1

        details.append({
            "id": case["id"],
            "name": case["name"],
            "passed": test_passed,
            "status": status,
            "error": error_msg
        })

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "details": details
    }

class TestPCDABenchmark(unittest.TestCase):
    def test_full_benchmark_suite(self):
        results = run_all_benchmarks()
        for d in results["details"]:
            with self.subTest(case=d["name"]):
                self.assertTrue(d["passed"], f"Test {d['id']} failed: {d['error']}")
        self.assertEqual(results["failed"], 0)

if __name__ == "__main__":
    unittest.main()
