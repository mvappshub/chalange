from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

DB_PATH_DEFAULT = Path("opsboard.db")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="backup file path")
    args = ap.parse_args()

    db_path = Path(os.environ.get("OPSBOARD_DB_FILE", str(DB_PATH_DEFAULT)))
    backup = Path(args.file)
    if not backup.exists():
        raise SystemExit(f"backup not found: {backup}")

    shutil.copy2(backup, db_path)
    print(f"restored {backup} -> {db_path}")

if __name__ == "__main__":
    main()
