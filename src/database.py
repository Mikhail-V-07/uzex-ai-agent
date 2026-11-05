"""Database initialization module for UZEX AI Agent."""
from pathlib import Path
from build_db import build, DEFAULT_DATA, DB_PATH


def create_database(data_dir: Path = DEFAULT_DATA, db_path: Path = DB_PATH):
    build(data_dir, db_path)


if __name__ == "__main__":
    create_database()
