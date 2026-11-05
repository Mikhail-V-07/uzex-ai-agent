"""FastAPI web service: chat UI + live analytics dashboard + streaming & sync API for the UZEX AI Agent.

Run:  python src/server.py         (http://localhost:8000)
"""
from __future__ import annotations

import json
import logging
import os
import queue
import sys
import threading
import time
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env", override=True)
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Request  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402

from agent import Agent, DB, DB_PATH, _jsonable  # noqa: E402

LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("uzex")

if not DB_PATH.exists():
    from build_db import build, DEFAULT_DATA

    build(DEFAULT_DATA, DB_PATH)

db = DB()
agent = Agent(db)
app = FastAPI(title="UZEX Deals AI Agent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
WEB = ROOT / "web"
WEB.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(WEB)), name="static")
_sem = threading.Semaphore(int(os.getenv("MAX_CONCURRENT", "6")))
_dashboard_cache: dict | None = None


@app.get("/")
def index():
    return FileResponse(str(WEB / "index.html"))


@app.get("/style.css")
def style_css():
    return FileResponse(str(WEB / "style.css"), media_type="text/css")


@app.get("/app.js")
def app_js():
    return FileResponse(str(WEB / "app.js"), media_type="application/javascript")


@app.get("/api/health")
def health():
    return {"ok": True, "models": agent.models, "endpoints": len(agent._endpoints)}


@app.get("/api/stats")
def stats():
    r = db.query("""
        SELECT count(*),
               min(deal_date),
               max(deal_date),
               round(sum(amount_uzs), 2),
               round(sum(amount_uzs) FILTER (WHERE status = 'Исполнен'), 2),
               count(*) FILTER (WHERE status = 'Исполнен'),
               count(DISTINCT product_family)
        FROM deals
    """)[1][0]
    c_cnt = db.query("SELECT count(*) FROM contracts")[1][0][0]
    p_cnt = db.query("SELECT count(*), count(*) FILTER (WHERE role='Продавец'), count(*) FILTER (WHERE role='Покупатель') FROM participants")[1][0]
    b_cnt = db.query("SELECT count(*) FROM brokers")[1][0][0]
    return {
        "deals": r[0],
        "from": str(r[1]),
        "to": str(r[2]),
        "turnover_uzs": float(r[3]),
        "executed_turnover_uzs": float(r[4]),
        "executed_deals": r[5],
        "products": r[6],
        "contracts": c_cnt,
        "participants": p_cnt[0],
        "sellers": p_cnt[1],
        "buyers": p_cnt[2],
        "brokers": b_cnt,
    }


@app.get("/api/dashboard")
def dashboard():
    global _dashboard_cache
    if _dashboard_cache is not None:
        return _dashboard_cache

    def rows_to_dicts(sql: str):
        cols, rows = db.query(sql)
        return [dict(zip(cols, [_jsonable(v) for v in r])) for r in rows]

    _dashboard_cache = {
        "yearly": rows_to_dicts("""
            SELECT year,
                   count(*) AS deals_count,
                   round(sum(amount_uzs), 2) AS turnover_uzs,
                   round(sum(amount_uzs) FILTER (WHERE status = 'Исполнен'), 2) AS executed_uzs,
                   count(*) FILTER (WHERE status = 'Исполнен') AS executed_count
            FROM deals GROUP BY year ORDER BY year
        """),
        "top_products": rows_to_dicts("""
            SELECT product_family,
                   any_value(product_family_uz) AS product_family_uz,
                   any_value(hs_code) AS hs_code,
                   string_agg(DISTINCT unit, '/') AS unit,
                   count(*) AS deals_count,
                   round(sum(amount_uzs), 2) AS turnover_uzs
            FROM deals
            GROUP BY product_family
            ORDER BY turnover_uzs DESC
            LIMIT 12
        """),
        "regions": rows_to_dicts("""
            SELECT region,
                   any_value(region_ru) AS region_ru,
                   count(*) AS deals_count,
                   round(sum(amount_uzs), 2) AS turnover_uzs
            FROM deals
            GROUP BY region
            ORDER BY turnover_uzs DESC
        """),
        "statuses": rows_to_dicts("""
            SELECT status,
                   count(*) AS deals_count,
                   round(sum(amount_uzs), 2) AS turnover_uzs
            FROM deals
            GROUP BY status
            ORDER BY deals_count DESC
        """),
        "top_sellers": rows_to_dicts("""
            SELECT seller_inn AS inn,
                   any_value(seller_name) AS name,
                   any_value(seller_region_ru) AS region_ru,
                   count(*) AS deals_count,
                   round(sum(amount_uzs), 2) AS turnover_uzs
            FROM deals
            GROUP BY seller_inn
            ORDER BY turnover_uzs DESC
            LIMIT 8
        """),
        "top_buyers": rows_to_dicts("""
            SELECT buyer_inn AS inn,
                   any_value(buyer_name) AS name,
                   any_value(buyer_region_ru) AS region_ru,
                   count(*) AS deals_count,
                   round(sum(amount_uzs), 2) AS turnover_uzs
            FROM deals
            GROUP BY buyer_inn
            ORDER BY turnover_uzs DESC
            LIMIT 8
        """),
    }
    return _dashboard_cache


def _log(rec: dict):
    with open(LOG_DIR / "qa.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")


@app.post("/api/ask_sync")
async def ask_sync(request: Request):
    body = await request.json()
    question = (body.get("question") or "").strip()[:2000]
    history = body.get("history") or []
    if not question:
        return JSONResponse({"error": "empty question"}, status_code=400)
    with _sem:
        res = agent.ask(question, history=history)
        _log(
            {
                "ts": time.time(),
                "q": question,
                "answer": res["answer"],
                "sql": res["sql"],
                "verified": res["verified"],
                "elapsed": res["elapsed"],
                "model": res.get("model"),
            }
        )
        return JSONResponse(res)


@app.post("/api/ask")
async def ask(request: Request):
    body = await request.json()
    question = (body.get("question") or "").strip()[:2000]
    history = body.get("history") or []
    if not question:
        return JSONResponse({"error": "empty question"}, status_code=400)
    q: queue.Queue = queue.Queue()

    def worker():
        with _sem:
            try:
                res = agent.ask(question, history=history, on_event=q.put)
                q.put({"type": "done", "result": res, **res})
                q.put({"type": "final", "result": res, **res})
                _log(
                    {
                        "ts": time.time(),
                        "q": question,
                        "answer": res["answer"],
                        "sql": res["sql"],
                        "verified": res["verified"],
                        "elapsed": res["elapsed"],
                        "model": res.get("model"),
                    }
                )
            except Exception as e:  # noqa: BLE001
                log.exception("ask failed")
                q.put({"type": "error", "error": str(e)[:500]})
                _log({"ts": time.time(), "q": question, "error": str(e)})
            finally:
                q.put(None)

    threading.Thread(target=worker, daemon=True).start()

    def stream():
        while True:
            try:
                item = q.get(timeout=5)
            except queue.Empty:
                yield json.dumps({"type": "ping"}) + "\n"
                continue
            if item is None:
                break
            yield json.dumps(item, ensure_ascii=False, default=str) + "\n"

    return StreamingResponse(
        stream(),
        media_type="application/x-ndjson",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
