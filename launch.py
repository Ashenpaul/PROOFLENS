"""
One-click unified launcher for PCDA (HNX26PSI08).
Usage:
  python launch.py         -> Starts Web Dashboard and opens browser
  python launch.py demo    -> Runs full terminal demonstration
  python launch.py test    -> Runs benchmark test suite
"""

import sys
import webbrowser
import subprocess
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

def main():
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "web"

    if mode == "demo":
        from run_demo import main as run_demo_main
        run_demo_main()
    elif mode == "test" or mode == "benchmark":
        from tests.test_benchmark import run_all_benchmarks
        results = run_all_benchmarks()
        print(f"\n=======================================================")
        print(f"BENCHMARK RESULTS: {results['passed']}/{results['total']} PASSED ({(results['passed']/results['total'])*100:.1f}%)")
        print(f"=======================================================")
        for d in results["details"]:
            status_symbol = "[PASS]" if d["passed"] else "[FAIL]"
            print(f" {status_symbol} {d['id']}: {d['name']} ({d['status']})")
    else:
        # Launch Web Server & Browser
        print("=" * 60)
        print("Launching Proof-Carrying Data Analyst Web Dashboard...")
        print("URL: http://localhost:8080")
        print("=" * 60)
        try:
            webbrowser.open("http://localhost:8080")
        except Exception:
            pass
        from web.app import run_server
        run_server()

if __name__ == "__main__":
    main()
