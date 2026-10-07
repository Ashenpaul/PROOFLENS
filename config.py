import os
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
ARTIFACTS_DIR = ROOT_DIR / "proof_artifacts"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

# Verification Settings
NUMERICAL_TOLERANCE = 1e-4
SANDBOX_TIMEOUT_SECONDS = 15
MAX_AGENT_RETRIES = 3
PYTHON_EXECUTABLE = "python"
