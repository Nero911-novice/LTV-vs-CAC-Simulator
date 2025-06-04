import streamlit as st

from app.unit_economics import unit_economics_calculator, show_ride_hailing_sidebar
from app.city_analysis import city_analysis_mode
from app.cohorts import rider_cohort_analysis
from app.scenarios import ride_hailing_scenarios
from app.promo import promo_optimizer
from app.expansion import expansion_strategy
from app.cases import industry_cases

st.set_page_config(
    page_title="🚗 Ride-Hailing LTV/CAC Симулятор",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Инициализация состояния
if 'scenario_results' not in st.session_state:
    st.session_state.scenario_results = []

if 'city_data' not in st.session_state:
    st.session_state.city_data = {}


def main():
    st.title("🚗 Ride-Hailing LTV/CAC Симулятор")
    st.markdown("**Специализированная платформа для анализа unit economics в такси**")

    with st.sidebar:
        st.header("🎯 Режимы анализа")
        mode = st.selectbox(
            "Выберите режим:",
            [
                "📊 Unit Economics калькулятор",
                "🏙️ Анализ по городам",
                "📈 Когортный анализ водителей",
                "🎪 Сценарное планирование",
                "💰 Оптимизатор промокодов",
                "🚀 Стратегия экспансии",
                "📚 Кейсы из индустрии"
            ]
        )

        st.markdown("---")
        show_ride_hailing_sidebar()

    if mode == "📊 Unit Economics калькулятор":
        unit_economics_calculator()
    elif mode == "🏙️ Анализ по городам":
        city_analysis_mode()
    elif mode == "📈 Когортный анализ водителей":
        rider_cohort_analysis()
    elif mode == "🎪 Сценарное планирование":
        ride_hailing_scenarios()
    elif mode == "💰 Оптимизатор промокодов":
        promo_optimizer()
    elif mode == "🚀 Стратегия экспансии":
        expansion_strategy()
    elif mode == "📚 Кейсы из индустрии":
        industry_cases()


if __name__ == "__main__":
    main()
