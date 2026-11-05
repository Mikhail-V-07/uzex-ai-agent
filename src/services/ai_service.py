"""AI Service wrapper bridging Streamlit / legacy callers to the grounded multi-step Agent."""
from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agent import Agent, DB, DB_PATH, validate_sql  # noqa: E402

_agent_instance: Agent | None = None


def get_agent(db_path: str | Path | None = None) -> Agent:
    global _agent_instance
    if _agent_instance is None:
        db = DB(Path(db_path) if db_path else DB_PATH)
        _agent_instance = Agent(db)
    return _agent_instance


def ask_database(question: str, db_path: str | None = None, history: list[dict] | None = None) -> dict:
    ag = get_agent(db_path)
    res = ag.ask(question, history=history)
    sql_list = res.get("sql") or []
    sql_text = "\n\n".join(sql_list) if sql_list else "-- Запрос не потребовался / сущность не найдена"

    # Extract last SQL dataframe for Streamlit compatibility
    df = pd.DataFrame()
    for step in reversed(res.get("steps") or []):
        if step.get("tool") == "run_sql" and not step.get("error"):
            cols = step.get("columns") or []
            rows = step.get("rows") or []
            df = pd.DataFrame(rows, columns=cols)
            break

    return {
        "answer": res["answer"],
        "sql": sql_text,
        "data": df,
        "steps": res.get("steps", []),
        "verified": res.get("verified", True),
        "elapsed": res.get("elapsed", 0.0),
        "model": res.get("model", ""),
        "lang": res.get("lang", "ru"),
    }
