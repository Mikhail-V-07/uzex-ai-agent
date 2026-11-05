"""Telegram Bot interface for UZEX Spot AI Agent (aiogram 3.x).

Run with:
    python src/bot.py

Requires TELEGRAM_BOT_TOKEN in .env (along with GEMINI_API_KEY).
"""
from __future__ import annotations

import asyncio
import html
import os
import sys
from collections import defaultdict
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
load_dotenv(ROOT / ".env", override=False)

from agent import Agent, DB  # noqa: E402
from build_db import build as build_db  # noqa: E402

DB_PATH = Path(os.getenv("UZEX_DB_PATH", str(ROOT / "data" / "uzex.duckdb")))
if not DB_PATH.exists():
    build_db()

db = DB(DB_PATH)
agent = Agent(db)

USER_HISTORY: dict[int, list[dict]] = defaultdict(list)
LAST_SQL: dict[int, list[str]] = {}

SAMPLE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Сделки за 2024 год (RU)", callback_data="q:2024_ru"),
            InlineKeyboardButton(text="📊 2025-yil bitimlari (UZ)", callback_data="q:2025_uz"),
        ],
        [
            InlineKeyboardButton(text="⛽ Бензин АИ-92 в 2025 (RU)", callback_data="q:ai92_ru"),
            InlineKeyboardButton(text="🌻 Paxta yog‘i narxi (UZ)", callback_data="q:oil_uz"),
        ],
        [
            InlineKeyboardButton(text="🏢 «Сотото Металл» (RU)", callback_data="q:sototo"),
            InlineKeyboardButton(text="🛡️ Золото в 2025 (Тест)", callback_data="q:gold"),
        ],
    ]
)

QUICK_MAP = {
    "q:2024_ru": "Сколько сделок и на какую сумму было заключено в 2024 году?",
    "q:2025_uz": "2025-yilda nechta bitim tuzilgan va ularning umumiy summasi qancha?",
    "q:ai92_ru": "Какой объём бензина АИ-92 продали в 2025 году?",
    "q:oil_uz": "Paxta yog‘i bo‘yicha 2024-yildagi o‘rtacha narx qancha?",
    "q:sototo": "Сколько сделок совершила компания «Сотото Металл»?",
    "q:gold": "Сколько сделок по золоту было в 2025 году?",
}


def format_tg_message(res: dict) -> str:
    ans = html.escape(res.get("answer", ""))
    verified = res.get("verified", False)
    elapsed = res.get("elapsed", 0.0)
    sql_cnt = len(res.get("sql") or [])
    badge = "✅ Числа сверены с БД" if verified else "⚠️ Проверьте SQL"
    footer = f"\n\n<code>{badge} · SQL: {sql_cnt} · {elapsed}s</code>"
    if len(ans) + len(footer) > 4000:
        ans = ans[: 4000 - len(footer) - 10] + "…"
    return ans + footer


async def handle_question(message: Message, question: str, uid: int):
    wait_msg = await message.answer("⏳ <i>Анализирую вопрос и выполняю SQL-запросы к DuckDB…</i>")
    loop = asyncio.get_running_loop()
    hist = USER_HISTORY[uid][-4:]
    try:
        res = await loop.run_in_executor(None, lambda: agent.ask(question, history=hist))
        USER_HISTORY[uid].append({"q": question, "a": res.get("answer", "")})
        LAST_SQL[uid] = res.get("sql") or []
        kb = None
        if LAST_SQL[uid]:
            kb = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="🔍 Показать SQL-запрос", callback_data="show_sql")]]
            )
        await wait_msg.edit_text(format_tg_message(res), reply_markup=kb)
    except Exception as e:  # noqa: BLE001
        await wait_msg.edit_text(f"❌ Ошибка при обработке запроса: <code>{html.escape(str(e)[:400])}</code>")


async def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        print("TELEGRAM_BOT_TOKEN is not set in .env. Set it to run the Telegram bot.")
        return

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def cmd_start(message: Message):
        USER_HISTORY[message.from_user.id].clear()
        await message.answer(
            "<b>📊 UZEX Spot AI — ИИ-агент реестра биржевых сделок (2022–2026)</b>\n\n"
            "Задайте любой вопрос на <b>русском</b> или <b>узбекском</b> языке (латиница/кириллица) "
            "о 500 000 сделках, 6 616 контрактах, 14 392 участниках, 120 брокерах и курсах валют.\n\n"
            "Выберите пример ниже или напишите свой вопрос:",
            reply_markup=SAMPLE_KEYBOARD,
        )

    @dp.message(Command("clear"))
    async def cmd_clear(message: Message):
        USER_HISTORY[message.from_user.id].clear()
        await message.answer("🗑️ История диалога очищена.")

    @dp.callback_query(F.data.startswith("q:"))
    async def cb_sample(cb: CallbackQuery):
        q = QUICK_MAP.get(cb.data)
        await cb.answer()
        if q and cb.message:
            await cb.message.answer(f"❓ <b>{html.escape(q)}</b>")
            await handle_question(cb.message, q, cb.from_user.id)

    @dp.callback_query(F.data == "show_sql")
    async def cb_sql(cb: CallbackQuery):
        await cb.answer()
        sqls = LAST_SQL.get(cb.from_user.id) or []
        if not sqls:
            await cb.message.answer("SQL-запросы для последнего ответа отсутствуют.")
            return
        txt = "\n\n".join(f"<pre>{html.escape(s)}</pre>" for s in sqls)
        await cb.message.answer(f"<b>Выполненные SQL-запросы (DuckDB):</b>\n{txt[:3900]}")

    @dp.message(F.text)
    async def on_text(message: Message):
        q = (message.text or "").strip()
        if not q:
            return
        await handle_question(message, q, message.from_user.id)

    print("UZEX Spot AI Telegram Bot started polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
