import streamlit as st
from dotenv import load_dotenv

from services.analytics_service import AnalyticsService
from services.ai_service import ask_database

load_dotenv()

st.set_page_config(
    page_title="UZEX Spot AI — ИИ-агент биржевых сделок",
    page_icon="📊",
    layout="wide",
)


@st.cache_resource
def get_service():
    return AnalyticsService()


service = get_service()

SAMPLE_QUESTIONS = [
    "Сколько сделок и на какую сумму было заключено в 2024 году?",
    "2025-yilda nechta bitim tuzilgan va ularning umumiy summasi qancha?",
    "Топ-5 товаров по общей сумме сделок за всё время",
    "Qaysi viloyatda 2025-yilda bitimlar summasi eng katta?",
    "Какой объём бензина АИ-92 продали в 2025 году?",
    "Paxta yog‘i bo‘yicha 2024-yildagi o‘rtacha narx qancha?",
    "Сколько сделок совершила компания «Сотото Металл»?",
    "Какова сумма сделок по медному катоду в 2024 году в долларах США и в сумах?",
    "По скольким сделкам была просрочена оплата, а по скольким — поставка?",
    "По скольким контрактам в реестре не было совершено ни одной сделки?",
    "Сколько сделок по золоту было в 2025 году?",
    "2026-yil noyabr oyida nechta bitim tuzilgan?",
]

with st.sidebar:
    st.markdown("### ⚡ UZEX Spot AI")
    st.caption("500 000 сделок · 6 616 контрактов · 14 392 участника · 120 брокеров (2022–2026)")
    if st.button("🗑️ Очистить диалог", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("#### Примеры вопросов (RU / UZ):")
    for idx, sq in enumerate(SAMPLE_QUESTIONS):
        if st.button(sq, key=f"sample_{idx}", use_container_width=True):
            st.session_state.pending_question = sq

st.title("📊 UZEX Spot AI — ИИ-агент реестра биржевых сделок")
st.caption(
    "Точные ответы на русском и узбекском языках (латиница и кириллица) по базе spot.uzex.uz "
    "с автоматической верификацией каждого числа против галлюцинаций."
)

tab_chat, tab_analytics = st.tabs(["💬 ИИ-Агент (Вопрос-ответ)", "📈 Аналитика и Реестр"])

with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                cols_meta = st.columns([2, 2, 3])
                if message.get("verified") is True:
                    cols_meta[0].success("✓ Числа сверены с БД")
                elif message.get("verified") is False:
                    cols_meta[0].warning("! Проверьте таблицу SQL")
                if message.get("elapsed") is not None:
                    cols_meta[1].caption(f"⏱️ Время: {message['elapsed']} с")
                if message.get("model"):
                    cols_meta[2].caption(f"🤖 Модель: {message['model']}")

                if message.get("sql"):
                    with st.expander("Посмотреть SQL-запрос"):
                        st.code(message["sql"], language="sql")

                if message.get("data") is not None and not message["data"].empty:
                    with st.expander("Посмотреть данные из базы"):
                        st.dataframe(message["data"], use_container_width=True)

    typed_question = st.chat_input("Спросите на русском или узбекском (например: Сколько сделок по бензину АИ-92 было в 2024 году?)")
    question = typed_question or st.session_state.pop("pending_question", None)

    if question:
        history_pairs = []
        msgs = st.session_state.messages
        for i in range(0, len(msgs) - 1, 2):
            if msgs[i]["role"] == "user" and msgs[i + 1]["role"] == "assistant":
                history_pairs.append({"q": msgs[i]["content"], "a": msgs[i + 1]["content"]})

        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Анализирую вопрос и выполняю SQL-запросы к DuckDB..."):
                try:
                    result = ask_database(
                        question=question,
                        db_path=str(service.db_path),
                        history=history_pairs[-4:],
                    )
                    answer = result["answer"]
                    sql = result["sql"]
                    data = result["data"]
                    verified = result.get("verified", True)
                    elapsed = result.get("elapsed", 0.0)
                    model_used = result.get("model", "")

                    st.markdown(answer)
                    cols_meta = st.columns([2, 2, 3])
                    if verified:
                        cols_meta[0].success("✓ Числа сверены с БД")
                    else:
                        cols_meta[0].warning("! Проверьте таблицу SQL")
                    cols_meta[1].caption(f"⏱️ Время: {elapsed} с")
                    if model_used:
                        cols_meta[2].caption(f"🤖 Модель: {model_used}")

                    if sql:
                        with st.expander("Посмотреть SQL-запрос"):
                            st.code(sql, language="sql")

                    if data is not None and not data.empty:
                        with st.expander("Посмотреть данные из базы"):
                            st.dataframe(data, use_container_width=True)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sql": sql,
                        "data": data,
                        "verified": verified,
                        "elapsed": elapsed,
                        "model": model_used,
                    })
                except Exception as error:
                    error_message = (
                        "Не удалось обработать вопрос. Проверьте подключение к ИИ и базу данных.\n\n"
                        f"Техническая ошибка: {error}"
                    )
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

with tab_analytics:
    try:
        summary = service.get_summary()
        yearly = service.get_yearly_turnover()
        products = service.get_top_products()
        regions = service.get_region_statistics()
        statuses = service.get_status_statistics()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Всего сделок", f"{int(summary.iloc[0]['deals_count']):,}".replace(",", " "))
        c2.metric("Общий оборот", f"{summary.iloc[0]['turnover_uzs'] / 1e12:.2f} трлн сум")
        c3.metric("Исполненные сделки", f"{int(summary.iloc[0]['executed_deals']):,}".replace(",", " "))
        c4.metric("Категорий товаров", f"{int(summary.iloc[0]['products_count'])}")

        col_l, col_r = st.columns(2)
        with col_l:
            st.subheader("Оборот по годам (сум)")
            st.bar_chart(yearly.set_index("year")["turnover_uzs"])
        with col_r:
            st.subheader("Статистика по статусам сделок")
            st.dataframe(statuses, use_container_width=True)

        col_p, col_reg = st.columns(2)
        with col_p:
            st.subheader("Топ товаров по сумме сделок")
            st.dataframe(products, use_container_width=True)
        with col_reg:
            st.subheader("Регионы по сумме сделок")
            st.dataframe(regions, use_container_width=True)

    except Exception as error:
        st.error(f"Ошибка загрузки аналитики: {error}")
