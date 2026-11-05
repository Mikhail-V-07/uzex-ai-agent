"""Grounded text-to-SQL agent for the UZEX deals registry (Gemini function calling).

Pipeline per question:
  1. Language detection (ru / uz-latn / uz-cyrl)
  2. Multi-step tool-calling loop: Gemini plans, calls `find_entity` (fuzzy/phonetic/translit lookup
     for companies, brokers, product families, brands, HS codes) and `run_sql` (read-only DuckDB),
     inspects real results, and iterates if needed
  3. Final answer synthesized strictly from tool results
  4. Numeric grounding verifier: checks that every numeric claim in the answer is grounded in the
     SQL/tool outputs; if any ungrounded number is detected, prompts a self-correction round.
"""
from __future__ import annotations

import math
import os
import re
import sys
import threading
import time
from dataclasses import dataclass, field
from datetime import date, datetime, time as dtime
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable

import duckdb
import sqlglot
from sqlglot import exp
from google import genai
from google.genai import types

sys.path.insert(0, str(Path(__file__).resolve().parent))
from normalize import phonetic_key, translit_key  # noqa: E402
from prompt import build_system_prompt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.getenv("UZEX_DB_PATH", str(ROOT / "data" / "uzex.duckdb")))

PRIMARY_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.1-flash-lite-preview",
]
FALLBACK_MODELS = [
    "gemini-3-flash-preview",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
]
DEFAULT_MODEL_POOL = PRIMARY_MODELS + FALLBACK_MODELS
MAX_STEPS = int(os.getenv("AGENT_MAX_STEPS", "10"))
DEADLINE_S = float(os.getenv("AGENT_DEADLINE_S", "68"))
MAX_ROWS_TO_LLM = 60

ALLOWED_TABLES = {
    "deals",
    "deals_financial",
    "contracts",
    "participants",
    "brokers",
    "usd_rates",
    "region_map",
    "product_map",
    "entity_index",
}
BLOCKED_FUNCS = {
    "read_csv", "read_csv_auto", "read_parquet", "read_json", "read_json_auto", "read_text",
    "read_blob", "read_ndjson", "parquet_scan", "csv_scan", "glob", "query", "query_table",
    "sniff_csv", "getenv", "load", "install",
}


# ----------------------------------------------------------------- database
class DB:
    def __init__(self, path: Path = DB_PATH):
        self.path = Path(path)
        self._local = threading.local()

    def con(self) -> duckdb.DuckDBPyConnection:
        c = getattr(self._local, "con", None)
        if c is None:
            c = duckdb.connect(str(self.path), read_only=True, config={"threads": 4})
            self._local.con = c
        return c

    def query(self, sql: str):
        cur = self.con().execute(sql)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchmany(5000)
        return cols, rows


def _jsonable(v: Any) -> Any:
    if v is None:
        return None
    if isinstance(v, (datetime, date, dtime)):
        return v.isoformat()
    if isinstance(v, Decimal):
        v = float(v)
    if isinstance(v, float):
        if math.isnan(v) or math.isinf(v):
            return None
        return round(v, 4) if abs(v) < 1e15 else v
    return v


def validate_sql(sql: str) -> str:
    sql = sql.strip().rstrip(";").strip()
    sql = re.sub(r"^```(?:sql)?\s*|\s*```$", "", sql, flags=re.I)
    try:
        stmts = sqlglot.parse(sql, read="duckdb")
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"SQL parse error: {e}")
    if len(stmts) != 1 or stmts[0] is None:
        raise ValueError("Only one SELECT statement is allowed")
    tree = stmts[0]
    if not isinstance(tree, (exp.Select, exp.Union, exp.Intersect, exp.Except, exp.Subquery)):
        if not tree.find(exp.Select) or tree.key in {
            "insert", "update", "delete", "create", "drop", "alter",
            "copy", "attach", "pragma", "set", "command",
        }:
            raise ValueError("Only SELECT queries are allowed")
    ctes = {c.alias_or_name.lower() for c in tree.find_all(exp.CTE)}
    for t in tree.find_all(exp.Table):
        name = t.name.lower()
        if name in ctes or not name:
            continue
        if name not in ALLOWED_TABLES:
            raise ValueError(
                f"Table '{t.name}' does not exist. Available: deals, contracts, participants, brokers, usd_rates"
            )
        if t.args.get("db") or t.args.get("catalog"):
            raise ValueError("Schemas are not allowed")
    for f in tree.find_all(exp.Func):
        fname = (f.name if isinstance(f, exp.Anonymous) else f.sql_name()).lower()
        if fname in BLOCKED_FUNCS:
            raise ValueError(f"Function {fname} is not allowed")
    return sql


# ----------------------------------------------------------------- language
UZ_LATIN_HINTS = re.compile(
    r"(o[‘'`ʻ’]|g[‘'`ʻ’]|\b(qancha|nechta|necha|qaysi|qanday|bitim|bitimlar|savdo|summa|yil|yilda|oyda|"
    r"eng|ko[‘'`ʻ’]p|kim|nima|bo[‘'`ʻ’]yicha|sotuvchi|xaridor|mahsulot|tovar|hajm|narx|kurs|bormi|"
    r"umumiy|soni|jami|uchun|va|bilan|qilgan|sotgan|sotib|olgan|holati|shartnoma|viloyat|viloyatida|"
    r"haqida|ma['‘`ʻ’]?lumot|bering|toping|ro['‘`ʻ’]?yxat|broker|kompaniya|korxona)\b)",
    re.I,
)
UZ_CYR_LETTERS = re.compile(r"[ўқғҳЎҚҒҲ]")
UZ_CYR_WORDS = re.compile(
    r"\b(қанча|нечта|қайси|битим|савдо|йил|энг|кўп|бўйича|сотувчи|харидор|маҳсулот|жами|"
    r"сони|учун|билан|йилда|ойда|ҳажми|нархи|ким|нима|ҳақида|маълумот|шартнома|вилоят)\b",
    re.I,
)


def detect_lang(text: str) -> str:
    # Remove quoted company/broker names in Uzbek Cyrillic like "ҲАРАЙЎМ КИМЁ" before checking if question is Russian
    cleaned = re.sub(r'["«„][^"»“]+["»“]', " ", text)
    if UZ_CYR_WORDS.search(cleaned) or (UZ_CYR_LETTERS.search(cleaned) and not re.search(r"\b(сколько|какой|какая|какие|кто|где|когда|расскажи|покажи|сумма|сделок|компания)\b", cleaned, re.I)):
        return "uz-cyrl"
    latin = len(re.findall(r"[A-Za-z]", cleaned))
    cyr = len(re.findall(r"[А-Яа-яЁё]", cleaned))
    if latin > cyr and UZ_LATIN_HINTS.search(text):
        return "uz"
    if latin > cyr * 2 and not re.search(r"\b(сколько|какой|какая|какие|кто|расскажи|покажи)\b", cleaned, re.I):
        return "uz"
    return "ru"


LANG_INSTR = {
    "ru": "Отвечай на русском языке.",
    "uz": "Javobni o‘zbek tilida (lotin yozuvida) yoz. Answer in Uzbek (Latin script).",
    "uz-cyrl": "Жавобни ўзбек тилида (кирилл ёзувида) ёз. Answer in Uzbek (Cyrillic script).",
}


# ----------------------------------------------------------------- grounding verifier
_STRIP_PATTERNS = re.compile(
    r"(\b\d{2}\.\d{2}\.\d{4}\b|\b\d{4}-\d{2}-\d{2}\b|\b\d{2}:\d{2}(?::\d{2})?\b|"
    r"\bBK\d{3}\b|\bАИ-\d+\b|\bAI-\d+\b|\bМ-\d+\b|\bM-\d+\b|\bГ-\d+\b|\bКС-\d+\b|\bПФ-\d+\b|"
    r"\b(?:LL|HD|LD|PE|PP|SG)-\d+\b|\bВ[рР]-\d+\b|\bБНД\s*\d+/\d+\b|\bNe\s*\d+/\d+\b|"
    r"\bЦЕМ\s*[IВAАШК/-]+\s*32[.,]5\s*Н\b|\bЦЕМ\s*I\s*42[.,]5\s*Н\b|"
    r"\b\d+[хxХX]\d+(?:[хxХX]\d+)?\s*(?:мм|ММ)?\b|\bØ\s*\d+\s*(?:мм|ММ)?\b|"
    r"\b\d+\s*-(?:сорт\w*|класс\w*|yil\w*|o['‘`ʻ’]rin\w*|ta\b|chi\b|чорак|квартал))",
    re.I,
)

_NUM_RE = re.compile(
    r"(?<![\w.,/])(\d{1,3}(?:[ \u00a0\u202f\u2009]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?)"
    r"(?:\s*(трлн|trln|млрд|mlrd|млн|mln|тыс|ming|минг|миллиард|миллион|million|billion|milliard|mlrd\.?))?",
    re.I,
)
_MULT = {
    "трлн": 1e12, "trln": 1e12,
    "млрд": 1e9, "mlrd": 1e9, "миллиард": 1e9, "billion": 1e9, "milliard": 1e9,
    "млн": 1e6, "mln": 1e6, "миллион": 1e6, "million": 1e6,
    "тыс": 1e3, "ming": 1e3, "минг": 1e3,
}


def _parse_numbers(text: str, strip_tokens: bool = True):
    cleaned = _STRIP_PATTERNS.sub(" ", text) if strip_tokens else text
    out = []
    for m in _NUM_RE.finditer(cleaned):
        raw, unit = m.group(1), (m.group(2) or "").lower().rstrip(".")
        s = re.sub(r"[ \u00a0\u202f\u2009]", "", raw)
        dec = 0
        if "," in s and "." not in s:
            s = s.replace(",", ".")
        elif "," in s and "." in s:
            s = s.replace(",", "")
        if "." in s:
            dec = len(s.split(".")[1])
        try:
            v = float(s)
        except ValueError:
            continue
        out.append((raw.strip(), v, dec, _MULT.get(unit, 1.0)))
    return out


def _collect_source_numbers(obj, acc: list):
    if isinstance(obj, dict):
        for v in obj.values():
            _collect_source_numbers(v, acc)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _collect_source_numbers(v, acc)
    elif isinstance(obj, bool):
        return
    elif isinstance(obj, (int, float)):
        f = float(obj)
        if not (math.isnan(f) or math.isinf(f)):
            acc.append(f)
    elif isinstance(obj, str):
        for _, v, _, mult in _parse_numbers(obj, strip_tokens=False):
            acc.append(v * mult)


def _collect_sql_numbers(jrows: list, acc: list):
    local: list[float] = []
    _collect_source_numbers(jrows, local)
    acc.append(float(len(jrows)))
    acc.extend(local)
    # Also include deterministic pairwise sums, differences, ratios, and % changes of numbers from the same query
    uniq = [x for x in dict.fromkeys(local) if not (math.isnan(x) or math.isinf(x))][:32]
    for i, a in enumerate(uniq):
        for b in uniq[i + 1:]:
            acc.append(a + b)
            acc.append(abs(a - b))
            if abs(b) > 1e-9:
                acc.append(a / b)
                acc.append((a / b) * 100.0)
                acc.append(abs(a - b) / abs(b) * 100.0)
            if abs(a) > 1e-9:
                acc.append(b / a)
                acc.append((b / a) * 100.0)
                acc.append(abs(b - a) / abs(a) * 100.0)
    # Column-wise sums for small tables (<= 30 rows)
    if 1 < len(jrows) <= 30 and jrows[0]:
        ncols = len(jrows[0])
        for c in range(ncols):
            col_vals = [r[c] for r in jrows if c < len(r) and isinstance(r[c], (int, float)) and not isinstance(r[c], bool)]
            if len(col_vals) >= 2:
                s = float(sum(col_vals))
                acc.append(s)
                if abs(s) > 1e-9:
                    for v in col_vals:
                        acc.append((float(v) / s) * 100.0)


def ungrounded_numbers(answer: str, sources: list[float], question: str) -> list[str]:
    if not sources:
        # If no SQL rows returned (e.g. "no data" response), only flag large invented numbers not in question
        pass
    q_nums = {v for _, v, _, _ in _parse_numbers(question, strip_tokens=False)}
    # Include standard dataset boundary constants (500000 deals, 6616 contracts, 14392 participants, 120 brokers, 41 products, 10/15/20% deposit)
    known_constants = {500000.0, 6616.0, 6483.0, 133.0, 14392.0, 14000.0, 13997.0, 392.0, 120.0, 41.0, 40.0, 1765.0, 100.0, 1000.0}
    all_sources = list(sources) + list(known_constants)

    bad = []
    for raw, v, dec, mult in _parse_numbers(answer, strip_tokens=True):
        if v in q_nums or (v * mult) in q_nums:
            continue
        # Small integers 0..31 are commonly bullet numbers, months, days, top-N indices, grades/classes
        if mult == 1.0 and dec == 0 and 0 <= v <= 31:
            continue
        # Years 2020..2030
        if mult == 1.0 and dec == 0 and 2020 <= v <= 2030:
            continue
        target = v * mult
        # Allow standard rounding tolerance (e.g. integer rounding of float or 1-2 decimal rounding)
        tol = max(0.55 * (10 ** -dec) * mult * 1.001, 0.55 if mult == 1.0 and dec <= 1 else 0.0) + 1e-6
        ok = False
        for s in all_sources:
            as_val = abs(s)
            eff_tol = max(tol, as_val * 1e-7)
            if abs(s - target) <= eff_tol or abs(as_val - abs(target)) <= eff_tol:
                ok = True
                break
            # Relative tolerance 0.2% when user/LLM summarizes large numbers with трлн/млрд/млн
            if mult > 1.0 and as_val > 0 and abs(as_val - abs(target)) / as_val <= 0.002:
                ok = True
                break
            # Percentages stored as fractions (0..1 -> 0..100%)
            if mult == 1.0 and (abs(s * 100.0 - target) <= eff_tol or abs(as_val * 100.0 - abs(target)) <= eff_tol):
                ok = True
                break
            # Tonnes <-> kg conversion (x1000 or /1000)
            if abs(as_val / 1000.0 - abs(target)) <= max(eff_tol, as_val / 1000.0 * 1e-7) or abs(as_val * 1000.0 - abs(target)) <= max(eff_tol, as_val * 1000.0 * 1e-7):
                ok = True
                break
        if not ok:
            bad.append(raw + (f" {mult:g}x" if mult != 1.0 else ""))
    return bad


# ----------------------------------------------------------------- tools
TOOLS = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="run_sql",
            description=(
                "Execute ONE read-only DuckDB SELECT query over the UZEX tables and return columns, rows "
                "(first 60) and total row count. Do all arithmetic (sums, averages, shares, differences, "
                "rounding) inside SQL."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "sql": types.Schema(type="STRING", description="DuckDB SELECT query"),
                    "purpose": types.Schema(type="STRING", description="short note what this query checks"),
                },
                required=["sql"],
            ),
        ),
        types.FunctionDeclaration(
            name="find_entity",
            description=(
                "Fuzzy and phonetic search for companies (participants: sellers/buyers -> INN), brokers (-> broker code), "
                "product families, product names, brands, or HS codes. Works across Russian/Uzbek and Cyrillic/Latin "
                "spelling, ignores quotes and legal forms (MChJ, XK, AJ...). ALWAYS use before filtering by a company "
                "or broker name."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "query": types.Schema(type="STRING", description="name, brand, INN, or code as the user wrote it"),
                    "kind": types.Schema(type="STRING", enum=["company", "broker", "product", "any"]),
                },
                required=["query"],
            ),
        ),
    ]
)


@dataclass
class Trace:
    steps: list = field(default_factory=list)
    sql_results: list = field(default_factory=list)
    source_numbers: list = field(default_factory=list)


class Agent:
    def __init__(self, db: DB | None = None):
        self.db = db or DB()
        raw_keys = [
            os.getenv("GEMINI_API_KEY", ""),
            os.getenv("GEMINI_API_KEY_BACKUP", ""),
        ]
        keys: list[str] = []
        for rk in raw_keys:
            for k in rk.split(","):
                k = k.strip()
                if k and k not in keys:
                    keys.append(k)
        self.clients = [
            genai.Client(
                api_key=k,
                http_options=types.HttpOptions(
                    timeout=12000,
                    retry_options=types.HttpRetryOptions(attempts=1),
                ),
            )
            for k in keys
        ]
        self.client = self.clients[0] if self.clients else None
        self.system_prompt = build_system_prompt(self.db)
        env_models = [
            m.strip()
            for m in [os.getenv("GEMINI_MODEL", ""), os.getenv("GEMINI_FALLBACK_MODEL", "")]
            if m and m.strip()
        ]
        seen = set()
        self.models: list[str] = []
        for m in DEFAULT_MODEL_POOL + env_models:
            if m not in seen:
                seen.add(m)
                self.models.append(m)
        self._primary_endpoints = [
            (ci, client, m)
            for m in PRIMARY_MODELS
            for ci, client in enumerate(self.clients)
        ]
        self._fallback_endpoints = [
            (ci, client, m)
            for m in self.models
            if m not in PRIMARY_MODELS
            for ci, client in enumerate(self.clients)
        ]
        self._endpoints = self._primary_endpoints + self._fallback_endpoints
        self._cooldown_until: dict[tuple[int, str], float] = {}
        self._rr_lock = threading.Lock()
        self._rr_idx = 0
        self._cache: dict[str, dict] = {}

    # ---------------- tools impl
    def tool_run_sql(self, sql: str, trace: Trace, purpose: str = "") -> dict:
        try:
            safe = validate_sql(sql)
            t = time.time()
            cols, rows = self.db.query(safe)
            ms = int((time.time() - t) * 1000)
        except Exception as e:  # noqa: BLE001
            msg = str(e).split("\n")[0][:600]
            trace.steps.append({"tool": "run_sql", "sql": sql, "purpose": purpose, "error": msg})
            return {"error": msg, "hint": "Fix the query. Check column names in the schema."}
        jrows = [[_jsonable(v) for v in r] for r in rows]
        res = {"columns": cols, "row_count": len(jrows), "rows": jrows[:MAX_ROWS_TO_LLM]}
        if len(jrows) > MAX_ROWS_TO_LLM:
            res["note"] = f"only first {MAX_ROWS_TO_LLM} of {len(jrows)} rows shown"
        if not jrows:
            res["note"] = (
                "EMPTY RESULT: no rows match. Check filters/spelling (use find_entity, product_family, brand_norm, "
                "sort_norm, class_norm), or report honestly that the data has no answer."
            )
        _collect_sql_numbers(jrows, trace.source_numbers)
        trace.steps.append(
            {
                "tool": "run_sql",
                "sql": safe,
                "purpose": purpose,
                "ms": ms,
                "columns": cols,
                "rows": jrows[:200],
                "row_count": len(jrows),
            }
        )
        trace.sql_results.append(res)
        return res

    def tool_find_entity(self, query: str, trace: Trace, kind: str = "any") -> dict:
        key = translit_key(query)
        pkey = phonetic_key(query)
        kinds = {
            "company": ["company"],
            "broker": ["broker"],
            "product": ["product_family", "product_name"],
            "any": ["company", "broker", "product_family", "product_name"],
        }.get(kind or "any", ["company", "broker", "product_family", "product_name"])
        digits = re.sub(r"\D", "", query)
        kind_sql = ",".join(f"'{k}'" for k in kinds)

        if len(digits) >= 5 and len(digits) == len(query.strip()):
            sql = f"""
                SELECT kind, code, name, extra, 1.0 AS score
                FROM entity_index
                WHERE (kind IN ({kind_sql}) AND (code LIKE ? OR extra LIKE ?))
                LIMIT 10
            """
            params = [f"%{digits}%", f"%{digits}%"]
        else:
            sql = f"""
                SELECT kind, code, name, extra,
                       greatest(
                           jaro_winkler_similarity(key, ?),
                           jaro_winkler_similarity(pkey, ?),
                           CASE WHEN key LIKE ? OR pkey LIKE ? THEN 0.97 ELSE 0 END,
                           CASE WHEN ? LIKE '%' || key || '%' AND length(key) > 3 THEN 0.95 ELSE 0 END,
                           CASE WHEN ? LIKE '%' || pkey || '%' AND length(pkey) > 3 THEN 0.94 ELSE 0 END
                       ) AS score
                FROM entity_index
                WHERE kind IN ({kind_sql})
                ORDER BY score DESC
                LIMIT 12
            """
            params = [key, pkey, f"%{key}%", f"%{pkey}%", key, pkey]
        try:
            cur = self.db.con().execute(sql, params)
            rows = [
                dict(zip(["kind", "code", "name", "extra", "score"], [_jsonable(x) for x in r]))
                for r in cur.fetchall()
            ]
        except Exception as e:  # noqa: BLE001
            err = str(e)
            trace.steps.append({"tool": "find_entity", "query": query, "error": err})
            return {"error": err}
        rows = [r for r in rows if (r["score"] or 0) >= 0.78][:10]
        _collect_source_numbers(rows, trace.source_numbers)
        trace.steps.append({"tool": "find_entity", "query": query, "kind": kind, "matches": rows})
        hint = (
            "code = INN for companies, broker_code for brokers, product_family value for products. "
            "If several close matches, prefer exact/most similar; if none match well, tell the user the entity is not in the data."
        )
        return (
            {"matches": rows, "hint": hint}
            if rows
            else {"matches": [], "note": "NO MATCHES — this entity is not in the database."}
        )

    # ---------------- main loop
    def ask(
        self,
        question: str,
        history: list[dict] | None = None,
        on_event: Callable[[dict], None] | None = None,
    ) -> dict:
        t0 = time.time()
        emit = on_event or (lambda e: None)
        q = question.strip()
        lang = detect_lang(q)
        ck = q.lower()
        if not history and ck in self._cache:
            res = dict(self._cache[ck])
            res["cached"] = True
            return res
        trace = Trace()
        contents: list[types.Content] = []
        for h in (history or [])[-4:]:
            contents.append(types.Content(role="user", parts=[types.Part(text=h["q"])]))
            contents.append(types.Content(role="model", parts=[types.Part(text=h["a"])]))
        contents.append(types.Content(role="user", parts=[types.Part(text=f"{q}\n\n[{LANG_INSTR[lang]}]")]))

        cfg = types.GenerateContentConfig(
            system_instruction=self.system_prompt,
            tools=[TOOLS],
            temperature=0.0,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        )
        answer = ""
        model_used = None
        verify_rounds = 0
        verified = None
        for step in range(MAX_STEPS + 3):
            elapsed = time.time() - t0
            force_final = elapsed > DEADLINE_S or step >= MAX_STEPS
            if force_final:
                contents.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part(
                                text=(
                                    "Time is up. Write the final answer NOW using only the tool results you already have. "
                                    "If they are insufficient, say honestly that you could not determine the answer."
                                )
                            )
                        ],
                    )
                )
                cfg_use = types.GenerateContentConfig(system_instruction=self.system_prompt, temperature=0.0)
            else:
                cfg_use = cfg
            resp, model_used = self._generate(contents, cfg_use)
            cand = resp.candidates[0] if resp.candidates else None
            parts = (cand.content.parts if cand and cand.content and cand.content.parts else []) or []
            calls = [p.function_call for p in parts if p.function_call]
            if calls and not force_final:
                contents.append(cand.content)
                responses = []
                for fc in calls:
                    args = dict(fc.args or {})
                    emit({"type": "tool", "tool": fc.name, "args": args})
                    if fc.name == "run_sql":
                        out = self.tool_run_sql(args.get("sql", ""), trace, args.get("purpose", ""))
                    elif fc.name == "find_entity":
                        out = self.tool_find_entity(args.get("query", ""), trace, args.get("kind", "any"))
                    else:
                        out = {"error": f"unknown tool {fc.name}"}
                    emit({"type": "tool_result", "tool": fc.name, "summary": _summ(out)})
                    responses.append(types.Part.from_function_response(name=fc.name, response=out))
                contents.append(types.Content(role="user", parts=responses))
                continue
            text = "".join(
                p.text for p in parts if getattr(p, "text", None) and not getattr(p, "thought", False)
            ).strip()
            if not text:
                text = resp.text or ""
            answer = text
            # ---- grounding verification
            bad = ungrounded_numbers(answer, trace.source_numbers, q)
            if bad and verify_rounds < 1 and time.time() - t0 < DEADLINE_S - 8:
                verify_rounds += 1
                emit({"type": "verify", "status": "retry", "ungrounded": bad})
                contents.append(types.Content(role="model", parts=[types.Part(text=answer)]))
                contents.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part(
                                text=(
                                    "VERIFIER: these numbers in your answer were NOT found in any SQL result: "
                                    f"{bad}. Every number must come from a tool result. If you computed something yourself, "
                                    "compute it with run_sql instead; otherwise remove it. Then give the corrected final answer."
                                )
                            )
                        ],
                    )
                )
                continue
            verified = not bad
            break

        sqls = [s for s in trace.steps if s["tool"] == "run_sql" and "error" not in s]
        result = {
            "answer": answer or "Не удалось сформировать ответ.",
            "lang": lang,
            "steps": trace.steps,
            "sql": [s["sql"] for s in sqls],
            "verified": verified,
            "model": model_used,
            "elapsed": round(time.time() - t0, 1),
            "cached": False,
        }
        if verified and not history:
            self._cache[ck] = result
        return result

    def _generate(self, contents, cfg: types.GenerateContentConfig):
        last = None
        for wave in range(3):
            now = time.time()
            with self._rr_lock:
                start_idx = self._rr_idx % max(1, len(self._primary_endpoints))
                self._rr_idx += 1
            rot_primary = self._primary_endpoints[start_idx:] + self._primary_endpoints[:start_idx]
            healthy_primary = [ep for ep in rot_primary if self._cooldown_until.get((ep[0], ep[2]), 0) <= now]
            healthy_fallback = [ep for ep in self._fallback_endpoints if self._cooldown_until.get((ep[0], ep[2]), 0) <= now]
            cooled = sorted(
                [ep for ep in (rot_primary + self._fallback_endpoints) if self._cooldown_until.get((ep[0], ep[2]), 0) > now],
                key=lambda ep: self._cooldown_until.get((ep[0], ep[2]), 0),
            )
            ordered = healthy_primary + healthy_fallback + cooled

            for ci, client, model in ordered:
                try:
                    model_cfg = types.GenerateContentConfig(
                        system_instruction=cfg.system_instruction,
                        tools=cfg.tools,
                        temperature=cfg.temperature,
                        automatic_function_calling=cfg.automatic_function_calling,
                    )
                    if "flash" in model and "lite" not in model:
                        model_cfg.thinking_config = types.ThinkingConfig(thinking_budget=256)
                    resp = client.models.generate_content(model=model, contents=contents, config=model_cfg)
                    return resp, model
                except Exception as e:  # noqa: BLE001
                    last = e
                    estr = str(e)
                    if "PerDay" in estr or "exceeded your current quota" in estr:
                        cd = 1800.0
                    elif "429" in estr or "RESOURCE_EXHAUSTED" in estr:
                        cd = 20.0
                    else:
                        cd = 6.0
                    self._cooldown_until[(ci, model)] = time.time() + cd
                    continue
            if wave < 2:
                time.sleep(3.0 * (wave + 1))
        raise RuntimeError(f"LLM unavailable across all models: {last}")


def _summ(out: dict) -> str:
    if "error" in out:
        return "error: " + str(out["error"])[:200]
    if "matches" in out:
        return f"{len(out['matches'])} matches"
    return f"{out.get('row_count', 0)} rows"
