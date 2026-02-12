from __future__ import annotations

import os
import shutil
from datetime import datetime
from pathlib import Path

DB_PATH_DEFAULT = Path("opsboard.db")

def main():
    db_path = Path(os.environ.get("OPSBOARD_DB_FILE", str(DB_PATH_DEFAULT)))
    if not db_path.exists():
        raise SystemExit(f"DB file not found: {db_path}")

    backups = Path("backups")
    backups.mkdir(exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out = backups / f"opsboard_{ts}.db"
    shutil.copy2(db_path, out)
    print(f"backup created: {out}")

if __name__ == "__main__":
    main()
