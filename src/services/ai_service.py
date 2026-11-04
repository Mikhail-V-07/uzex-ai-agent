import os
import re

import duckdb
import sqlglot
from sqlglot import exp
from google import genai
from google.genai import types


MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

ALLOWED_TABLES = {
    "deals_financial",
    "deals",
    "contracts",
    "participants",
    "brokers",
    "usd_rates",
}

SYSTEM_PROMPT = """
Ты — аналитический AI-агент биржи UZEX.
Ты отвечаешь на русском и узбекском языках.

Твоя задача — преобразовать вопрос пользователя в SQL-запрос DuckDB.

Доступные таблицы:

1. deals_financial:
   - содержит сделки и финансовые данные;
   - "Номер сделки"
   - "Дата сделки"
   - "Наименование товара"
   - "Количество"
   - "Сумма сделки"
   - "Стартовая цена"
   - "Номер контракта"
   - "Состояние сделки"
   - "ИНН продавца"
   - "ИНН покупателя"
   - amount
   - start_price
   - amount_uzs — сумма сделки, приведённая к узбекским сумам.

2. contracts:
   - "Номер контракта"
   - "Наименование продукта"
   - "Марка товара"
   - "Размер товара"
   - "Сорт товара"
   - "Тип товара"
   - "Класс товара"
   - "Код ТН ВЭД"
   - "Группа товара"
   - "Категория товара"
   - "Отрасль промышленности"
   - "Единица измерения"
   - "Регион"
   - "ИНН продавца"

3. participants:
   - "ИНН"
   - "Наименование"
   - "Регион"
   - "Вид деятельности"
   - "Роль"

4. brokers:
   - "Код брокера"
   - "Наименование"
   - "ИНН"
   - "Регион"

5. usd_rates:
   - "Дата"
   - "Курс"

Правила:
- Используй только перечисленные таблицы.
- Создавай только один SELECT-запрос.
- Не используй INSERT, UPDATE, DELETE, DROP, CREATE,
  ALTER, ATTACH, COPY и другие изменяющие команды.
- Не используй внешние файлы и функции чтения файлов.
- Всегда добавляй LIMIT не более 100.
- Для финансовых итогов используй amount_uzs,
  а не сумму исходных значений в разных валютах.
- Если вопрос про исполненные сделки, фильтруй
  "Состояние сделки" = 'Исполнен'.
- Не смешивай физические единицы измерения.
- Не придумывай названия колонок.
- Если вопрос непонятен, верни простой запрос,
  который поможет уточнить данные.

Верни только SQL-код. Без объяснений и Markdown.
"""


def _get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Не найден GEMINI_API_KEY. Проверь файл .env"
        )

    return genai.Client(api_key=api_key)

def generate_content_with_fallback(contents, config=None):
    client = _get_client()

    models = [
        os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
        os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.1-flash-lite"),
    ]

    errors = []

    for model in models:
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )

            return response

        except Exception as error:
            errors.append(f"{model}: {error}")

    raise RuntimeError(
        "Все модели Gemini недоступны:\n" + "\n".join(errors)
    )

def generate_sql(question: str) -> str:
    client = _get_client()

    response = generate_content_with_fallback(
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.1,
            max_output_tokens=1200,
    
)
)

    if not response.text:
        raise RuntimeError("ИИ не вернул SQL-запрос.")

    sql = response.text.strip()

    # Убираем Markdown-обрамление, если модель его добавила.
    sql = re.sub(r"^```(?:sql)?\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\s*```$", "", sql)

    
            
    return sql.strip().rstrip(";")


def validate_sql(sql: str) -> str:
    try:
        statements = sqlglot.parse(sql, read="duckdb")
    except Exception as error:
        raise ValueError(f"Не удалось разобрать SQL: {error}")

    if len(statements) != 1 or statements[0] is None:
        raise ValueError("Разрешён только один SQL-запрос.")

    tree = statements[0]

    if not isinstance(tree, exp.Select):
        raise ValueError("Разрешены только SELECT-запросы.")

    tables = list(tree.find_all(exp.Table))

    if not tables:
        raise ValueError("Запрос должен обращаться к таблицам базы.")

    for table in tables:
        table_name = table.name.lower()

        if table_name not in ALLOWED_TABLES:
            raise ValueError(
                f"Таблица {table_name} не разрешена."
            )

        if table.db or table.catalog:
            raise ValueError("Обращение к внешним схемам запрещено.")

    # Ограничиваем объём возвращаемых строк.
    limit = tree.args.get("limit")

    if limit is None:
        tree = tree.limit(100)
    else:
        limit_value = limit.expression

        if not isinstance(limit_value, exp.Literal) or limit_value.is_string:
            raise ValueError("LIMIT должен быть целым числом.")

        if int(limit_value.this) > 100:
            raise ValueError("Максимальный LIMIT — 100.")


    blocked_functions = {
            "read_csv",
            "read_csv_auto",
            "read_parquet",
            "read_json",
            "read_text",
            "read_blob",
            "read_ndjson",
            "parquet_scan",
            "csv_scan",
            "glob",
        }
    
    for function in tree.find_all(exp.Anonymous):
            if function.name.lower() in blocked_functions:
                raise ValueError("Эта SQL-функция запрещена.")
    

    return tree.sql(dialect="duckdb")


def execute_sql(sql: str, db_path: str):
    connection = duckdb.connect(db_path, read_only=True)

    try:
        return connection.execute(sql).fetchdf()
    finally:
        connection.close()


def explain_result(question: str, sql: str, dataframe) -> str:
    client = _get_client()

    # Передаём модели только ограниченную выборку результата.
    records = dataframe.head(30).to_json(
        orient="records",
        force_ascii=False,
        date_format="iso",
    )

    prompt = f"""
Вопрос пользователя:
{question}

Выполненный SQL:
{sql}

Результат запроса из базы данных:
{records}

Объясни результат пользователю на языке его вопроса.

Правила:
- Используй только данные из результата запроса.
- Не придумывай цифры, названия и причины.
- Если результат пустой, прямо скажи об этом.
- Если результат содержит несколько строк, выдели главное.
- Если данных недостаточно, сообщи об ограничении.
- Не называй зарегистрированный оборот фактически исполненным.
"""

    response = generate_content_with_fallback(
    contents=prompt,
    config=types.GenerateContentConfig(
        temperature=0.1,
        max_output_tokens=1200,
    ),
)

    return response.text or "Не удалось сформировать текстовый ответ."


def ask_database(question: str, db_path: str):
    sql = generate_sql(question)
    safe_sql = validate_sql(sql)

    dataframe = execute_sql(safe_sql, db_path)
    answer = explain_result(question, safe_sql, dataframe)

    return {
        "answer": answer,
        "sql": safe_sql,
        "data": dataframe,
    }