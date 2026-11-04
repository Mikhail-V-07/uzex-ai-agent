import streamlit as st
from dotenv import load_dotenv

from services.analytics_service import AnalyticsService
from services.ai_service import ask_database

load_dotenv()

st.set_page_config(
    page_title="UZEX AI Agent",
    page_icon="📊",
    layout="wide",
)

@st.cache_resource
def get_service():
    return AnalyticsService()


service = get_service()

st.title("UZEX AI Agent")
st.caption("Интеллектуальная аналитика биржевых сделок")

# -------------------------------
# AI CHAT
# -------------------------------

st.header("Задайте вопрос о биржевых данных")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Показываем предыдущие сообщения.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("sql"):
            with st.expander("Посмотреть SQL-запрос"):
                st.code(message["sql"], language="sql")

        if message.get("data") is not None:
            with st.expander("Посмотреть данные из базы"):
                st.dataframe(
                    message["data"],
                    use_container_width=True,
                )

question = st.chat_input(
    "Например: Сколько хлопка продали в 2025 году?"
)

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Анализирую вопрос и обращаюсь к базе..."):
            try:
                result = ask_database(
                    question=question,
                    db_path=str(service.db_path),
                )

                answer = result["answer"]
                sql = result["sql"]
                data = result["data"]

                st.markdown(answer)

                with st.expander("Посмотреть SQL-запрос"):
                    st.code(sql, language="sql")

                with st.expander("Посмотреть данные из базы"):
                    st.dataframe(
                        data,
                        use_container_width=True,
                    )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sql": sql,
                    "data": data,
                })

            except Exception as error:
                error_message = (
                    "Не удалось обработать вопрос. "
                    "Проверь подключение к ИИ и базу данных.\n\n"
                    f"Техническая ошибка: {error}"
                )

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message,
                })


st.divider()

# -------------------------------
# ANALYTICS DASHBOARD
# -------------------------------

st.header("Общая аналитика")

try:
    summary = service.get_summary()
    yearly = service.get_yearly_turnover()
    products = service.get_top_products()
    statuses = service.get_status_statistics()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Всего сделок",
            f"{int(summary.iloc[0]['deals_count']):,}".replace(",", " "),
        )

    with col2:
        turnover = summary.iloc[0]["turnover_uzs"] / 1_000_000_000_000

        st.metric(
            "Зарегистрированный оборот",
            f"{turnover:.2f} трлн UZS",
        )

    st.caption(
        "Оборот рассчитан по всем состояниям сделок, "
        "а не только по исполненным."
    )

    st.subheader("Оборот по годам")

    yearly_chart = yearly.set_index("year")["turnover_uzs"]
    st.bar_chart(yearly_chart)

    st.subheader("Топ товаров")

    st.dataframe(
        products,
        use_container_width=True,
    )

    st.subheader("Статистика по состояниям сделок")

    st.dataframe(
        statuses,
        use_container_width=True,
    )

except Exception as error:
    st.error(f"Ошибка загрузки аналитики: {error}")