"""Database initialization module for UZEX AI Agent."""
from pathlib import Path
from build_db import build, DEFAULT_DATA, DB_PATH


def create_database(data_dir: Path = DEFAULT_DATA, db_path: Path = DB_PATH):
    db_path = Path(db_path)
    gz_path = Path(str(db_path) + ".gz")
    if not db_path.exists() and gz_path.exists():
        import gzip
        import shutil

        db_path.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(gz_path, "rb") as f_in, open(db_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        return
    build(data_dir, db_path)


if __name__ == "__main__":
    create_database()
