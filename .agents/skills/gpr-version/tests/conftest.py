import os
from pathlib import Path

# Ensure a clean, isolated DB for test runs.
TEST_DB = Path(".pytest_opsboard.db")
if TEST_DB.exists():
    TEST_DB.unlink()

os.environ.setdefault("DATABASE_URL", f"sqlite:///./{TEST_DB}")
