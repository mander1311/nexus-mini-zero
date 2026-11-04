from pathlib import Path
import os

__version__ = "1.0.0"

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = BASE_DIR / "data" / "nexus.db"
DB_PATH = Path(os.getenv("NEXUS_DB_PATH", str(DEFAULT_DB_PATH)))
