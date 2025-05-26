import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple, Optional

# Конфигурация
st.set_page_config(
    page_title="🚗 Ride-Hailing LTV/CAC Симулятор",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Стили
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .warning-card {
        background: #ff6b6b;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .success-card {
        background: #51cf66;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .city-card {
        background: #f8f9fa;
        border: 2px solid #e1e5e9;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Инициализация состояния
if 'scenario_results' not in st.session_state:
    st.session_state.scenario_results = []

if 'city_data' not in st.session_state:
    st.session_state.city_data = {}

# Главная функция
def main():
    st.title("🚗 Ride-Hailing LTV/CAC Симулятор")
    st.markdown("**Специализированная платформа для анализа unit economics в каршеринге и такси**")
    
    # Боковая панель
    with st.sidebar:
        st.header("🎯 Режимы анализа")
        mode = st.selectbox(
            "Выберите режим:",
            [
                "📊 Unit Economics калькулятор",
                "🏙️ Анализ по городам", 
                "📈 Когортный анализ райдеров",
                "🎪 Сценарное планирование",
                "💰 Оптимизатор промокодов",
                "🚀 Стратегия экспансии",
                "📚 Кейсы из индустрии"
            ]
        )
        
        st.markdown("---")
        show_ride_hailing_sidebar()
    
    # Роутинг
    if mode == "📊 Unit Economics калькулятор":
        unit_economics_calculator()
    elif mode == "🏙️ Анализ по городам":
        city_analysis_mode()
    elif mode == "📈 Когортный анализ райдеров":
        rider_cohort_analysis()
    elif mode == "🎪 Сценарное планирование":
        ride_hailing_scenarios()
    elif mode == "💰 Оптимизатор промокодов":
        promo_optimizer()
    elif mode == "🚀 Стратегия экспансии":
        expansion_strategy()
    elif mode == "📚 Кейсы из индустрии":
        industry_cases()

def show_ride_hailing_sidebar():
    """Справочная информация для ride-hailing"""
    with st.expander("📖 Ride-Hailing метрики"):
        st.markdown("""
        **AOV** - Average Order Value (средний чек поездки)
        **Take Rate** - комиссия платформы с поездки
        **Частота** - поездок на пользователя в месяц
        **Time to 2nd ride** - время до второй поездки
        **Monthly Active Users** - активные пользователи в месяц
        **Supply/Demand balance** - баланс водителей и пассажиров
        **Surge pricing** - динамическое ценообразование
        **Промокоды** - субсидии для привлечения пользователей
        """)
    
    with st.expander("🎯 Особенности индустрии"):
        st.markdown("""
        **Двухсторонняя модель**: водители + пассажиры
        **Сетевые эффекты**: больше водителей → больше пассажиров
        **Плотность**: концентрация в крупных городах
        **Пиковые часы**: rush hours, выходные, праздники
        **Конкуренция**: агрессивные промокампании
        **Регулирование**: лицензии, налоги, ограничения
        """)

def unit_economics_calculator():
    """Калькулятор Unit Economics для ride-hailing"""
    st.header("📊 Unit Economics для Ride-Hailing")
    
    st.markdown("""
    **Специфика ride-hailing**: вместо подписок у нас поездки, вместо валовой маржи - take rate, 
    ключевая метрика - частота использования.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚗 Параметры поездок")
        
        aov = st.slider("Средний чек поездки (AOV)", 150, 800, 350, 25)
        take_rate = st.slider("Take rate (%)", 15, 35, 25, 1)
        monthly_frequency = st.slider("Поездок в месяц на пользователя", 1, 20, 4, 1)
        monthly_churn = st.slider("Месячный отток пользователей (%)", 5, 25, 12, 1)
        
        # Операционные расходы на пользователя
        ops_costs = st.slider("Операционные расходы на пользователя/месяц", 10, 100, 30, 5)
        
        # Расчет LTV
        monthly_revenue = aov * (take_rate / 100) * monthly_frequency
        monthly_profit = monthly_revenue - ops_costs
        ltv = monthly_profit / (monthly_churn / 100)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>LTV пассажира: {ltv:,.0f} руб</h3>
            <p>Месячная прибыль: {monthly_profit:,.0f} руб</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("💰 Стоимость привлечения")
        
        # CAC с учетом промокодов
        marketing_spend = st.number_input("Маркетинговый бюджет (руб)", 500000, 20000000, 2000000, 100000)
        promo_budget = st.number_input("Бюджет на промокоды (руб)", 200000, 10000000, 1000000, 100000)
        new_users = st.number_input("Новых пользователей", 500, 10000, 2000, 100)
        
        # Расчет полного CAC
        total_acquisition_cost = marketing_spend + promo_budget
        cac_total = total_acquisition_cost / new_users
        cac_marketing = marketing_spend / new_users
        cac_promo = promo_budget / new_users
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>Полный CAC: {cac_total:,.0f} руб</h3>
            <p>Маркетинг: {cac_marketing:,.0f} | Промо: {cac_promo:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Анализ соотношений
    st.subheader("📈 Анализ Unit Economics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    ltv_cac_ratio = ltv / cac_total
    payback_months = cac_total / monthly_profit if monthly_profit > 0 else float('inf')
    
    # Специфические метрики для ride-hailing
    revenue_per_ride = aov * (take_rate / 100)
    rides_to_payback = cac_total / revenue_per_ride if revenue_per_ride > 0 else float('inf')
    
    with col1:
        color = "success" if ltv_cac_ratio >= 3 else "warning" if ltv_cac_ratio >= 2 else "error"
        st.markdown(f"""
        <div class="{color}-card">
            <h4>LTV/CAC</h4>
            <h2>{ltv_cac_ratio:.1f}:1</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        color = "success" if payback_months <= 6 else "warning" if payback_months <= 12 else "error"
        st.markdown(f"""
        <div class="{color}-card">
            <h4>Окупаемость</h4>
            <h2>{payback_months:.1f} мес</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Доход с поездки</h4>
            <h2>{revenue_per_ride:.0f} руб</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        color = "success" if rides_to_payback <= 20 else "warning" if rides_to_payback <= 40 else "error"
        st.markdown(f"""
        <div class="{color}-card">
            <h4>Поездок до окупаемости</h4>
            <h2>{rides_to_payback:.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Анализ чувствительности для ride-hailing
    create_ride_hailing_sensitivity_chart(aov, take_rate, monthly_frequency, monthly_churn, cac_total)
    
    # Интерпретация
    show_ride_hailing_interpretation(ltv_cac_ratio, payback_months, rides_to_payback, monthly_frequency)

def create_ride_hailing_sensitivity_chart(aov: float, take_rate: float, frequency: float, churn: float, cac: float):
    """График чувствительности для ride-hailing метрик"""
    st.subheader("🎯 Анализ чувствительности ride-hailing метрик")
    
    # Вариации ключевых параметров
    frequency_range = np.linspace(frequency * 0.5, frequency * 2, 20)
    take_rate_range = np.linspace(take_rate * 0.7, take_rate * 1.4, 20)
    aov_range = np.linspace(aov * 0.8, aov * 1.3, 20)
    
    # Расчет LTV для разных сценариев
    ltv_frequency = [(aov * (take_rate / 100) * f - 30) / (churn / 100) for f in frequency_range]
    ltv_take_rate = [(aov * (tr / 100) * frequency - 30) / (churn / 100) for tr in take_rate_range]
    ltv_aov = [(a * (take_rate / 100) * frequency - 30) / (churn / 100) for a in aov_range]
    
    # График с тремя subplot'ами
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Влияние частоты поездок', 'Влияние take rate', 
                       'Влияние среднего чека', 'Сравнение факторов'),
        specs=[[{"colspan": 1}, {"colspan": 1}], 
               [{"colspan": 1}, {"colspan": 1}]]
    )
    
    # График 1: Частота поездок
    fig.add_trace(
        go.Scatter(x=frequency_range, y=ltv_frequency, mode='lines+markers',
                  name='LTV от частоты', line=dict(color='blue', width=3)),
        row=1, col=1
    )
    
    # График 2: Take rate
    fig.add_trace(
        go.Scatter(x=take_rate_range, y=ltv_take_rate, mode='lines+markers',
                  name='LTV от take rate', line=dict(color='green', width=3)),
        row=1, col=2
    )
    
    # График 3: AOV
    fig.add_trace(
        go.Scatter(x=aov_range, y=ltv_aov, mode='lines+markers',
                  name='LTV от AOV', line=dict(color='orange', width=3)),
        row=2, col=1
    )
    
    # График 4: Сравнение эластичности
    elasticity_data = {
        'Параметр': ['Частота поездок', 'Take Rate', 'Средний чек'],
        'Эластичность': [
            (max(ltv_frequency) - min(ltv_frequency)) / min(ltv_frequency),
            (max(ltv_take_rate) - min(ltv_take_rate)) / min(ltv_take_rate),
            (max(ltv_aov) - min(ltv_aov)) / min(ltv_aov)
        ]
    }
    
    fig.add_trace(
        go.Bar(x=elasticity_data['Параметр'], y=elasticity_data['Эластичность'],
               marker_color=['blue', 'green', 'orange']),
        row=2, col=2
    )
    
    # Добавляем линию CAC
    for i in range(1, 4):
        row = 1 if i <= 2 else 2
        col = i if i <= 2 else i - 2
        fig.add_hline(y=cac, line_dash="dash", line_color="red", 
                     annotation_text=f"CAC = {cac:,.0f}", row=row, col=col)
    
    fig.update_layout(height=600, showlegend=False)
    fig.update_xaxes(title_text="Поездок/месяц", row=1, col=1)
    fig.update_xaxes(title_text="Take Rate (%)", row=1, col=2)
    fig.update_xaxes(title_text="AOV (руб)", row=2, col=1)
    fig.update_xaxes(title_text="Параметр", row=2, col=2)
    fig.update_yaxes(title_text="LTV (руб)")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Инсайты для ride-hailing
    st.info(f"""
    💡 **Ключевые инсайты для ride-hailing**:
    
    1. **Частота - король**: Увеличение поездок с {frequency} до {frequency*1.5:.1f} в месяц 
       повышает LTV на {((max(ltv_frequency)/min(ltv_frequency) - 1) * 100):.0f}%
    
    2. **Take rate имеет пределы**: Повышение комиссии увеличивает LTV, но снижает конкурентоспособность
    
    3. **AOV зависит от продукта**: Премиум-сегмент vs эконом влияет на средний чек
    
    4. **Фокус на habit forming**: Превратить occasional users в power users критически важно
    """)

def show_ride_hailing_interpretation(ltv_cac_ratio: float, payback_months: float, 
                                   rides_to_payback: float, frequency: float):
    """Интерпретация результатов для ride-hailing"""
    st.subheader("🧠 Интерпретация для ride-hailing бизнеса")
    
    if ltv_cac_ratio >= 4:
        st.success("🎉 **Отличные показатели!** Unit economics здоровые, можно агрессивно масштабироваться.")
    elif ltv_cac_ratio >= 2.5:
        st.info("👍 **Приемлемые показатели.** Есть место для оптимизации частоты использования.")
    elif ltv_cac_ratio >= 1.5:
        st.warning("⚠️ **На грани рентабельности.** Критически важно увеличить retention и частоту.")
    else:
        st.error("🚨 **Убыточная модель!** Пересматривайте стратегию промокодов и операционную эффективность.")
    
    # Специфические рекомендации для ride-hailing
    if frequency < 3:
        st.warning("📊 **Низкая частота использования.** Рассмотрите loyalty программы и push-уведомления.")
    
    if rides_to_payback > 30:
        st.error("🚨 **Слишком много поездок до окупаемости.** Снижайте промокоды или улучшайте retention.")
    elif rides_to_payback <= 15:
        st.success("💰 **Быстрая окупаемость в поездках** - отличная модель для масштабирования.")
    
    # Индустриальные бенчмарки
    st.markdown("""
    ### 📊 Бенчмарки ride-hailing индустрии:
    
    **LTV/CAC соотношения:**
    - 🟢 Mature markets: 3-5:1
    - 🟡 Growing markets: 2-3:1  
    - 🔴 New markets: 1.5-2:1 (допустимо при быстром росте)
    
    **Поездок до окупаемости:**
    - 🟢 10-20 поездок (отлично)
    - 🟡 20-30 поездок (приемлемо)
    - 🔴 30+ поездок (проблема)
    
    **Частота использования:**
    - 🟢 Power users: 8+ поездок/месяц
    - 🟡 Regular users: 3-7 поездок/месяц
    - 🔴 Occasional users: 1-2 поездки/месяц
    """)

def city_analysis_mode():
    """Анализ по городам"""
    st.header("🏙️ Анализ по городам")
    
    st.markdown("""
    **Городская специфика**: разные города имеют кардинально разные метрики из-за плотности, 
    конкуренции, покупательной способности и транспортной инфраструктуры.
    """)
    
    # Настройка городов
    cities_data = setup_cities_data()
    
    # Визуализация сравнения городов
    create_cities_comparison_chart(cities_data)
    
    # Анализ по стадиям развития
    analyze_city_maturity(cities_data)
    
    # Рекомендации по городам
    show_city_recommendations(cities_data)

def setup_cities_data() -> Dict:
    """Настройка данных по городам"""
    st.subheader("⚙️ Настройка метрик по городам")
    
    # Предустановленные данные для российских городов
    default_cities = {
        "Москва": {
            "population": 12_500_000, "aov": 420, "frequency": 6.2, "take_rate": 28,
            "cac": 1800, "competition": 9, "maturity": "Зрелый"
        },
        "СПб": {
            "population": 5_400_000, "aov": 380, "frequency": 4.8, "take_rate": 26,
            "cac": 1400, "competition": 8, "maturity": "Зрелый"
        },
        "Новосибирск": {
            "population": 1_600_000, "aov": 280, "frequency": 3.2, "take_rate": 24,
            "cac": 900, "competition": 5, "maturity": "Растущий"
        },
        "Екатеринбург": {
            "population": 1_500_000, "aov": 310, "frequency": 3.8, "take_rate": 25,
            "cac": 1100, "competition": 6, "maturity": "Растущий"
        },
        "Казань": {
            "population": 1_300_000, "aov": 260, "frequency": 2.9, "take_rate": 23,
            "cac": 800, "competition": 4, "maturity": "Развивающийся"
        },
        "Краснодар": {
            "population": 900_000, "aov": 240, "frequency": 2.1, "take_rate": 22,
            "cac": 650, "competition": 3, "maturity": "Развивающийся"
        }
    }
    
    selected_cities = st.multiselect(
        "Выберите города для анализа:",
        list(default_cities.keys()),
        default=["Москва", "СПб", "Новосибирск", "Казань"]
    )
    
    if not selected_cities:
        selected_cities = ["Москва", "СПб"]
    
    # Расширенные метрики
    cities_analysis = {}
    for city in selected_cities:
        data = default_cities[city].copy()
        
        # Расчет LTV и других метрик
        monthly_revenue = data['aov'] * data['take_rate'] / 100 * data['frequency']
        ops_cost = 25  # Фиксированная операционная стоимость
        monthly_profit = monthly_revenue - ops_cost
        
        # Churn зависит от зрелости рынка
        churn_rates = {"Зрелый": 10, "Растущий": 12, "Развивающийся": 15}
        churn = churn_rates[data['maturity']]
        
        ltv = monthly_profit / (churn / 100)
        ltv_cac_ratio = ltv / data['cac']
        
        cities_analysis[city] = {
            **data,
            'monthly_revenue': monthly_revenue,
            'monthly_profit': monthly_profit,
            'churn': churn,
            'ltv': ltv,
            'ltv_cac_ratio': ltv_cac_ratio,
            'market_potential': data['population'] * 0.15 * data['frequency']  # 15% penetration
        }
    
    return cities_analysis

def create_cities_comparison_chart(cities_data: Dict):
    """Сравнительный анализ городов"""
    st.subheader("📊 Сравнение городов")
    
    # Подготовка данных для графика
    cities = list(cities_data.keys())
    ltv_values = [cities_data[city]['ltv'] for city in cities]
    cac_values = [cities_data[city]['cac'] for city in cities]
    populations = [cities_data[city]['population'] for city in cities]
    frequencies = [cities_data[city]['frequency'] for city in cities]
    
    # Bubble chart
    fig = go.Figure()
    
    # Цветовая карта по стадии зрелости
    maturity_colors = {"Зрелый": "green", "Растущий": "orange", "Развивающийся": "red"}
    colors = [maturity_colors[cities_data[city]['maturity']] for city in cities]
    
    fig.add_trace(go.Scatter(
        x=cac_values,
        y=ltv_values,
        mode='markers+text',
        text=cities,
        textposition="middle center",
        marker=dict(
            size=[p/100000 for p in populations],  # Размер = население
            color=colors,
            line=dict(width=2, color='black'),
            sizemode='diameter',
            sizeref=2.*max([p/100000 for p in populations])/(40.**2),
            sizemin=10
        ),
        hovertemplate='<b>%{text}</b><br>' +
                      'CAC: %{x:,.0f} руб<br>' +
                      'LTV: %{y:,.0f} руб<br>' +
                      '<extra></extra>'
    ))
    
    # Добавляем линии-ориентиры
    max_val = max(max(ltv_values), max(cac_values))
    
    # Линия LTV = CAC (1:1)
    fig.add_shape(type="line", x0=0, x1=max_val, y0=0, y1=max_val,
                  line=dict(color="red", width=2, dash="dash"))
    
    # Линия LTV = 3*CAC (3:1)
    fig.add_shape(type="line", x0=0, x1=max_val/3, y0=0, y1=max_val,
                  line=dict(color="green", width=2, dash="dash"))
    
    fig.update_layout(
        title="Размер пузыря = население, цвет = стадия развития рынка",
        xaxis_title="CAC (руб)",
        yaxis_title="LTV (руб)",
        height=500
    )
    
    # Добавляем аннотации
    fig.add_annotation(x=max_val*0.8, y=max_val*0.85, text="LTV = CAC (1:1)",
                      showarrow=False, font=dict(color="red"))
    fig.add_annotation(x=max_val*0.25, y=max_val*0.85, text="LTV = 3×CAC (3:1)",
                      showarrow=False, font=dict(color="green"))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Таблица детального сравнения
    st.subheader("📋 Детальное сравнение городов")
    
    comparison_df = pd.DataFrame([
        {
            'Город': city,
            'Население': f"{data['population']:,}",
            'AOV': f"{data['aov']} руб",
            'Частота': f"{data['frequency']:.1f}",
            'Take Rate': f"{data['take_rate']}%",
            'CAC': f"{data['cac']:,} руб",
            'LTV': f"{data['ltv']:,.0f} руб",
            'LTV/CAC': f"{data['ltv_cac_ratio']:.1f}:1",
            'Стадия': data['maturity'],
            'Потенциал рынка': f"{data['market_potential']:,.0f}"
        }
        for city, data in cities_data.items()
    ])
    
    st.dataframe(comparison_df, use_container_width=True)

def analyze_city_maturity(cities_data: Dict):
    """Анализ по стадиям зрелости рынка"""
    st.subheader("📈 Анализ по стадиям развития рынка")
    
    # Группировка по стадиям
    maturity_groups = {}
    for city, data in cities_data.items():
        stage = data['maturity']
        if stage not in maturity_groups:
            maturity_groups[stage] = []
        maturity_groups[stage].append(data)
    
    # Средние показатели по стадиям
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Средний LTV/CAC по стадиям', 'Средний CAC',
                       'Частота использования', 'Take Rate'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    stages = list(maturity_groups.keys())
    colors = ['red', 'orange', 'green']
    
    for i, stage in enumerate(stages):
        stage_data = maturity_groups[stage]
        avg_ltv_cac = np.mean([d['ltv_cac_ratio'] for d in stage_data])
        avg_cac = np.mean([d['cac'] for d in stage_data])
        avg_frequency = np.mean([d['frequency'] for d in stage_data])
        avg_take_rate = np.mean([d['take_rate'] for d in stage_data])
        
        fig.add_trace(go.Bar(x=[stage], y=[avg_ltv_cac], 
                            marker_color=colors[i % len(colors)], showlegend=False), 
                     row=1, col=1)
        fig.add_trace(go.Bar(x=[stage], y=[avg_cac], 
                            marker_color=colors[i % len(colors)], showlegend=False), 
                     row=1, col=2)
        fig.add_trace(go.Bar(x=[stage], y=[avg_frequency], 
                            marker_color=colors[i % len(colors)], showlegend=False), 
                     row=2, col=1)
        fig.add_trace(go.Bar(x=[stage], y=[avg_take_rate], 
                            marker_color=colors[i % len(colors)], showlegend=False), 
                     row=2, col=2)
    
    fig.update_layout(height=600)
    fig.update_yaxes(title_text="LTV/CAC", row=1, col=1)
    fig.update_yaxes(title_text="CAC (руб)", row=1, col=2)
    fig.update_yaxes(title_text="Поездок/месяц", row=2, col=1)
    fig.update_yaxes(title_text="Take Rate (%)", row=2, col=2)
    
    st.plotly_chart(fig, use_container_width=True)

def show_city_recommendations(cities_data: Dict):
    """Рекомендации по городам"""
    st.subheader("💡 Стратегические рекомендации")
    
    # Анализ лучших и худших городов
    best_city = max(cities_data.keys(), key=lambda x: cities_data[x]['ltv_cac_ratio'])
    worst_city = min(cities_data.keys(), key=lambda x: cities_data[x]['ltv_cac_ratio'])
    
    highest_potential = max(cities_data.keys(), key=lambda x: cities_data[x]['market_potential'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🟢 Лучшие показатели")
        best_data = cities_data[best_city]
        st.success(f"""
        **{best_city}**: LTV/CAC = {best_data['ltv_cac_ratio']:.1f}:1
        
        • Частота: {best_data['frequency']:.1f} поездок/месяц
        • AOV: {best_data['aov']} руб
        • Зрелость рынка: {best_data['maturity']}
        
        **Стратегия**: Максимальное масштабирование
        """)
        
        st.markdown("#### 🚀 Наибольший потенциал")
        potential_data = cities_data[highest_potential]
        st.info(f"""
        **{highest_potential}**: Потенциал {potential_data['market_potential']:,.0f}
        
        • Население: {potential_data['population']:,}
        • Текущий CAC: {potential_data['cac']:,} руб
        • Конкуренция: {potential_data['competition']}/10
        """)
    
    with col2:
        st.markdown("#### 🔴 Требуют внимания")
        worst_data = cities_data[worst_city]
        st.warning(f"""
        **{worst_city}**: LTV/CAC = {worst_data['ltv_cac_ratio']:.1f}:1
        
        • Частота: {worst_data['frequency']:.1f} поездок/месяц
        • CAC: {worst_data['cac']:,} руб
        • Churn: {worst_data['churn']}%
        
        **Стратегия**: Оптимизация retention и частоты
        """)
        
        # Общие рекомендации по типам городов
        st.markdown("#### 📊 По типам городов")
        
        for maturity in ["Зрелый", "Растущий", "Развивающийся"]:
            cities_in_stage = [city for city, data in cities_data.items() 
                             if data['maturity'] == maturity]
            if cities_in_stage:
                stage_recommendations = {
                    "Зрелый": "Оптимизация операций, премиум продукты",
                    "Растущий": "Агрессивное масштабирование, захват доли",
                    "Развивающийся": "Образование рынка, низкие цены"
                }
                st.write(f"**{maturity}** ({', '.join(cities_in_stage)}): {stage_recommendations[maturity]}")

def rider_cohort_analysis():
    """Когортный анализ райдеров"""
    st.header("📈 Когортный анализ райдеров")
    
    st.markdown("""
    **Особенности ride-hailing**: первая поездка ≠ активация. Ключевая метрика - 
    time to second ride и частота использования в первые 30 дней.
    """)
    
    # Параметры анализа
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚙️ Параметры когорт")
        
        num_cohorts = st.slider("Количество месячных когорт", 6, 18, 12)
        base_cohort_size = st.slider("Размер базовой когорты", 1000, 10000, 3000)
        seasonal_effect = st.checkbox("Учесть сезонные эффекты", True)
        
    with col2:
        st.subheader("🎯 Метрики активации")
        
        time_to_second_ride = st.slider("Среднее время до 2-й поездки (дни)", 3, 21, 7)
        first_month_frequency = st.slider("Поездок в первый месяц (активные)", 2, 8, 4)
        activation_rate = st.slider("Доля активированных пользователей (%)", 30, 80, 55)
    
    # Генерация когортных данных
    cohort_data = generate_rider_cohort_data(
        num_cohorts, base_cohort_size, seasonal_effect, 
        time_to_second_ride, first_month_frequency, activation_rate
    )
    
    # Визуализация когортной таблицы
    create_rider_cohort_table(cohort_data)
    
    # Анализ retention кривых
    create_retention_curves(cohort_data)
    
    # Анализ revenue cohorts
    create_revenue_cohort_analysis(cohort_data)

def generate_rider_cohort_data(num_cohorts: int, base_size: int, seasonal: bool,
                              time_to_second: int, first_frequency: int, activation_rate: int) -> List[Dict]:
    """Генерация данных когортного анализа для райдеров"""
    
    cohorts = []
    
    for i in range(num_cohorts):
        month = i + 1
        
        # Сезонные эффекты для ride-hailing
        seasonal_multiplier = 1.0
        if seasonal:
            # Зима (дек-фев) - больше поездок из-за погоды
            if month in [12, 1, 2]:
                seasonal_multiplier = 1.4
            # Лето (июн-авг) - меньше поездок, больше пешком/велосипед
            elif month in [6, 7, 8]:
                seasonal_multiplier = 0.8
            # Дождливые месяцы (окт-ноя, мар-апр)
            elif month in [10, 11, 3, 4]:
                seasonal_multiplier = 1.2
        
        cohort_size = int(base_size * seasonal_multiplier * np.random.uniform(0.9, 1.1))
        
        # Расчет метрик когорты
        activated_users = int(cohort_size * (activation_rate / 100))
        
        # Retention pattern для ride-hailing (более крутое падение в начале)
        monthly_retention = []
        for month_num in range(1, 13):
            if month_num == 1:
                retention = 1.0  # 100% в первый месяц
            elif month_num == 2:
                retention = activation_rate / 100  # Активация во второй месяц
            else:
                # Экспоненциальное снижение с выходом на плато
                base_retention = 0.25 + (activation_rate / 100 - 0.25) * np.exp(-(month_num - 2) / 4)
                retention = max(base_retention, 0.15)  # Минимум 15% долгосрочный retention
            
            monthly_retention.append(retention)
        
        # Расчет помесячной выручки
        aov = 350 * seasonal_multiplier  # AOV зависит от сезона
        take_rate = 0.25
        
        monthly_revenue = []
        for month_num, retention in enumerate(monthly_retention):
            active_users = cohort_size * retention
            
            # Частота зависит от стадии жизненного цикла
            if month_num == 0:
                frequency = first_frequency * 0.6  # Первый месяц - частичный
            elif month_num <= 2:
                frequency = first_frequency  # Начальная активность
            else:
                # Стабилизация частоты для retained users
                frequency = first_frequency * 1.2
            
            revenue = active_users * aov * take_rate * frequency
            monthly_revenue.append(revenue)
        
        # Расчет LTV когорты
        total_revenue = sum(monthly_revenue)
        ltv_per_user = total_revenue / cohort_size
        
        cohorts.append({
            'month': month,
            'cohort_size': cohort_size,
            'activated_users': activated_users,
            'activation_rate': activation_rate / 100,
            'monthly_retention': monthly_retention,
            'monthly_revenue': monthly_revenue,
            'ltv_per_user': ltv_per_user,
            'seasonal_factor': seasonal_multiplier,
            'time_to_second_ride': time_to_second + np.random.normal(0, 2)
        })
    
    return cohorts

def create_rider_cohort_table(cohort_data: List[Dict]):
    """Создание когортной таблицы retention"""
    st.subheader("📊 Когортная таблица retention (в %)")
    
    # Подготовка данных для heatmap
    cohort_months = len(cohort_data)
    max_periods = 12
    
    retention_matrix = np.zeros((cohort_months, max_periods))
    
    for i, cohort in enumerate(cohort_data):
        for j in range(min(len(cohort['monthly_retention']), max_periods)):
            retention_matrix[i, j] = cohort['monthly_retention'][j] * 100
    
    # Создание интерактивной heatmap
    fig = go.Figure(data=go.Heatmap(
        z=retention_matrix,
        x=[f"M{i+1}" for i in range(max_periods)],
        y=[f"Когорта {i+1}" for i in range(cohort_months)],
        colorscale='RdYlGn',
        zmin=0,
        zmax=100,
        text=[[f"{val:.1f}%" for val in row] for row in retention_matrix],
        texttemplate="%{text}",
        textfont={"size":10},
        colorbar=dict(title="Retention %")
    ))
    
    fig.update_layout(
        title="Retention Rate по когортам (чем зеленее, тем лучше)",
        xaxis_title="Месяц с момента привлечения",
        yaxis_title="Когорта",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Средние показатели
    st.subheader("📈 Средние показатели retention")
    
    avg_retention = np.mean(retention_matrix, axis=0)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("1-й месяц", f"{avg_retention[0]:.1f}%")
    with col2:
        st.metric("2-й месяц (активация)", f"{avg_retention[1]:.1f}%")
    with col3:
        st.metric("6-й месяц", f"{avg_retention[5]:.1f}%")
    with col4:
        st.metric("12-й месяц", f"{avg_retention[11]:.1f}%")

def create_retention_curves(cohort_data: List[Dict]):
    """Кривые retention для разных когорт"""
    st.subheader("📉 Кривые retention по когортам")
    
    fig = go.Figure()
    
    # Показываем несколько репрезентативных когорт
    selected_cohorts = [0, len(cohort_data)//4, len(cohort_data)//2, len(cohort_data)-1]
    colors = ['blue', 'green', 'orange', 'red']
    
    for i, cohort_idx in enumerate(selected_cohorts):
        if cohort_idx < len(cohort_data):
            cohort = cohort_data[cohort_idx]
            months = list(range(1, len(cohort['monthly_retention']) + 1))
            retention_pct = [r * 100 for r in cohort['monthly_retention']]
            
            fig.add_trace(go.Scatter(
                x=months,
                y=retention_pct,
                mode='lines+markers',
                name=f"Когорта {cohort['month']} (сезон {cohort['seasonal_factor']:.1f}x)",
                line=dict(color=colors[i], width=3),
                marker=dict(size=6)
            ))
    
    # Средняя кривая
    avg_retention = []
    for month_idx in range(12):
        month_retentions = [c['monthly_retention'][month_idx] * 100 
                          for c in cohort_data if month_idx < len(c['monthly_retention'])]
        avg_retention.append(np.mean(month_retentions))
    
    fig.add_trace(go.Scatter(
        x=list(range(1, 13)),
        y=avg_retention,
        mode='lines+markers',
        name="Средняя retention",
        line=dict(color='black', width=4, dash='dash'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Retention curves: влияние сезонности на лояльность",
        xaxis_title="Месяц с момента привлечения",
        yaxis_title="Retention (%)",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Инсайты
    st.info("""
    💡 **Ключевые паттерны ride-hailing retention**:
    
    1. **Крутое падение после 1-го месяца** - критичность быстрой активации
    2. **Стабилизация на 3-4 месяце** - формирование привычки
    3. **Сезонные различия** - зимние когорты часто имеют лучший retention
    4. **Долгосрочное плато 15-25%** - база лояльных пользователей
    """)

def create_revenue_cohort_analysis(cohort_data: List[Dict]):
    """Анализ выручки по когортам"""
    st.subheader("💰 Revenue Cohort Analysis")
    
    # Подготовка данных
    cohort_months = len(cohort_data)
    max_periods = 12
    
    revenue_matrix = np.zeros((cohort_months, max_periods))
    
    for i, cohort in enumerate(cohort_data):
        for j in range(min(len(cohort['monthly_revenue']), max_periods)):
            revenue_matrix[i, j] = cohort['monthly_revenue'][j] / 1000  # В тысячах рублей
    
    # Cumulative revenue
    cumulative_revenue = np.cumsum(revenue_matrix, axis=1)
    
    # График cumulative revenue
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Месячная выручка по когортам', 'Накопительная выручка')
    )
    
    # Monthly revenue heatmap
    fig.add_trace(
        go.Heatmap(
            z=revenue_matrix,
            x=[f"M{i+1}" for i in range(max_periods)],
            y=[f"Когорта {i+1}" for i in range(cohort_months)],
            colorscale='Blues',
            name="Monthly Revenue",
            showscale=False
        ),
        row=1, col=1
    )
    
    # Cumulative revenue heatmap
    fig.add_trace(
        go.Heatmap(
            z=cumulative_revenue,
            x=[f"M{i+1}" for i in range(max_periods)],
            y=[f"Когорта {i+1}" for i in range(cohort_months)],
            colorscale='Greens',
            name="Cumulative Revenue",
            colorbar=dict(title="Выручка (тыс. руб)")
        ),
        row=1, col=2
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # LTV анализ
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 LTV по когортам")
        ltv_data = pd.DataFrame([
            {
                'Когорта': f"Когорта {c['month']}",
                'Размер': c['cohort_size'],
                'LTV на пользователя': f"{c['ltv_per_user']:,.0f} руб",
                'Сезонный фактор': f"{c['seasonal_factor']:.1f}x",
                'Активация': f"{c['activation_rate']:.1%}"
            }
            for c in cohort_data
        ])
        st.dataframe(ltv_data, use_container_width=True)
    
    with col2:
        st.markdown("#### 💡 Выводы")
        
        avg_ltv = np.mean([c['ltv_per_user'] for c in cohort_data])
        max_ltv_cohort = max(cohort_data, key=lambda x: x['ltv_per_user'])
        min_ltv_cohort = min(cohort_data, key=lambda x: x['ltv_per_user'])
        
        st.metric("Средний LTV", f"{avg_ltv:,.0f} руб")
        st.success(f"Лучшая когорта: {max_ltv_cohort['month']} ({max_ltv_cohort['ltv_per_user']:,.0f} руб)")
        st.warning(f"Худшая когорта: {min_ltv_cohort['month']} ({min_ltv_cohort['ltv_per_user']:,.0f} руб)")
        
        ltv_variance = (max_ltv_cohort['ltv_per_user'] - min_ltv_cohort['ltv_per_user']) / avg_ltv
        st.info(f"Разброс LTV: {ltv_variance:.1%}")

def ride_hailing_scenarios():
    """Сценарное планирование для ride-hailing"""
    st.header("🎪 Сценарное планирование для Ride-Hailing")
    
    st.markdown("""
    **Специфические сценарии для ride-hailing**: конкурентные войны, регулирование, 
    пандемии, изменения в городской мобильности.
    """)
    
    scenario_type = st.selectbox(
        "Выберите сценарий:",
        [
            "🆚 Конкурентная война (агрессивные промокоды)",
            "📉 Экономический кризис (снижение спроса)",
            "🚫 Усиление регулирования",
            "🦠 Пандемия/форс-мажор",
            "🚇 Развитие общественного транспорта",
            "🚗 Запуск в новом городе"
        ]
    )
    
    if scenario_type == "🆚 Конкурентная война (агрессивные промокоды)":
        competitive_war_scenario()
    elif scenario_type == "📉 Экономический кризис (снижение спроса)":
        economic_crisis_scenario()
    elif scenario_type == "🚫 Усиление регулирования":
        regulation_scenario()
    elif scenario_type == "🦠 Пандемия/форс-мажор":
        pandemic_scenario()
    elif scenario_type == "🚇 Развитие общественного транспорта":
        public_transport_scenario()
    elif scenario_type == "🚗 Запуск в новом городе":
        new_city_launch_scenario()

def competitive_war_scenario():
    """Сценарий конкурентной войны"""
    st.subheader("🆚 Конкурентная война с промокодами")
    
    st.warning("""
    **Ситуация**: Крупный конкурент запустил агрессивную промокампанию с скидками 50% и 
    cashback'ом. Ваша доля рынка падает, пользователи уходят к конкурентам.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**⚙️ Параметры ответной реакции**")
        
        promo_intensity = st.slider("Интенсивность промокодов (% от выручки)", 10, 60, 30)
        market_share_loss = st.slider("Потеря доли рынка без реакции (%)", 10, 50, 25)
        cac_inflation = st.slider("Рост CAC из-за конкуренции (%)", 20, 100, 50)
        
        # Базовые метрики
        base_aov = 350
        base_frequency = 4.5
        base_take_rate = 25
        base_cac = 1500
        base_users = 100000
        
    with col2:
        st.markdown("**📊 Базовые показатели**")
        st.metric("Базовый AOV", f"{base_aov} руб")
        st.metric("Частота", f"{base_frequency} поездок/месяц")
        st.metric("Take Rate", f"{base_take_rate}%")
        st.metric("Базовый CAC", f"{base_cac:,} руб")
    
    # Расчет сценариев
    
    # Сценарий 1: Не реагируем на конкуренцию
    scenario_1_users = base_users * (1 - market_share_loss / 100)
    scenario_1_revenue = scenario_1_users * base_aov * (base_take_rate / 100) * base_frequency
    scenario_1_cac = base_cac  # CAC не меняется, но пользователей меньше
    
    # Сценарий 2: Агрессивная промореакция
    scenario_2_users = base_users * 0.95  # Небольшая потеря все равно есть
    effective_take_rate = base_take_rate - promo_intensity  # Промокоды едят маржу
    scenario_2_revenue = scenario_2_users * base_aov * (effective_take_rate / 100) * base_frequency
    scenario_2_cac = base_cac * (1 + cac_inflation / 100)
    
    # Сценарий 3: Фокус на retention без промокодов
    scenario_3_users = base_users * (1 - market_share_loss / 100 * 0.6)  # Меньшие потери
    scenario_3_frequency = base_frequency * 1.2  # Повышение лояльности существующих
    scenario_3_revenue = scenario_3_users * base_aov * (base_take_rate / 100) * scenario_3_frequency
    scenario_3_cac = base_cac * 1.1  # Небольшой рост CAC
    
    # Результаты сравнения
    st.subheader("📈 Сравнение сценариев")
    
    scenarios_df = pd.DataFrame([
        {
            'Сценарий': 'Не реагируем',
            'Пользователи': f"{scenario_1_users:,.0f}",
            'Месячная выручка': f"{scenario_1_revenue:,.0f} руб",
            'Эффективный CAC': f"{scenario_1_cac:,} руб",
            'Take Rate': f"{base_take_rate}%",
            'Риски': 'Потеря доли рынка'
        },
        {
            'Сценарий': 'Промовойна',
            'Пользователи': f"{scenario_2_users:,.0f}",
            'Месячная выручка': f"{scenario_2_revenue:,.0f} руб",
            'Эффективный CAC': f"{scenario_2_cac:,} руб",
            'Take Rate': f"{effective_take_rate:.1f}%",
            'Риски': 'Низкая маржинальность'
        },
        {
            'Сценарий': 'Фокус на retention',
            'Пользователи': f"{scenario_3_users:,.0f}",
            'Месячная выручка': f"{scenario_3_revenue:,.0f} руб",
            'Эффективный CAC': f"{scenario_3_cac:,} руб",
            'Take Rate': f"{base_take_rate}%",
            'Риски': 'Медленная реакция'
        }
    ])
    
    st.dataframe(scenarios_df, use_container_width=True)
    
    # Рекомендации
    best_revenue_scenario = max([scenario_1_revenue, scenario_2_revenue, scenario_3_revenue])
    
    if best_revenue_scenario == scenario_3_revenue:
        st.success("🎯 **Рекомендация**: Фокус на retention и частоте использования может быть эффективнее промовойны.")
    elif best_revenue_scenario == scenario_1_revenue:
        st.info("📊 **Рекомендация**: Возможно, стоит переждать конкурентную волну, сосредоточившись на операционной эффективности.")
    else:
        st.warning("⚠️ **Рекомендация**: Промовойна оправдана, но контролируйте unit economics.")
    
    st.markdown("""
    ### 💡 Альтернативные стратегии конкуренции:
    
    1. **Дифференциация сервиса**: премиум опции, лучший UX
    2. **Вертикальная интеграция**: доставка еды, грузоперевозки  
    3. **B2B focus**: корпоративные клиенты, менее чувствительные к цене
    4. **Geographic moats**: фокус на пригородах, где конкуренция слабее
    5. **Supply-side**: переманивание лучших водителей
    """)

def economic_crisis_scenario():
    """Сценарий экономического кризиса"""
    st.subheader("📉 Экономический кризис и снижение спроса")
    
    st.error("""
    **Ситуация**: Экономический кризис снижает располагаемые доходы. Пользователи переходят 
    на общественный транспорт, снижается частота поездок, растет price sensitivity.
    """)
    
    # Параметры кризиса
    col1, col2 = st.columns(2)
    
    with col1:
        demand_drop = st.slider("Снижение общего спроса (%)", 20, 60, 35)
        price_sensitivity = st.slider("Рост price sensitivity (эластичность)", 1.2, 2.5, 1.8)
        income_effect = st.slider("Снижение доходов населения (%)", 10, 30, 20)
        
    with col2:
        # Реакция бизнеса
        price_cut = st.slider("Снижение цен для поддержки спроса (%)", 0, 30, 15)
        cost_optimization = st.slider("Оптимизация операционных расходов (%)", 10, 40, 25)
        
    # Базовые метрики
    base_volume = 1000000  # поездок в месяц
    base_aov = 350
    base_take_rate = 25
    base_ops_cost = 50  # на пользователя в месяц
    
    # Расчет влияния кризиса
    new_volume = base_volume * (1 - demand_drop / 100)
    new_aov = base_aov * (1 - price_cut / 100)
    
    # Price elasticity effect
    additional_volume_from_price_cut = base_volume * (price_cut / 100) * price_sensitivity
    final_volume = min(new_volume + additional_volume_from_price_cut, base_volume * 0.9)
    
    new_ops_cost = base_ops_cost * (1 - cost_optimization / 100)
    
    # Финансовые результаты
    base_revenue = base_volume * base_aov * (base_take_rate / 100)
    new_revenue = final_volume * new_aov * (base_take_rate / 100)
    
    base_profit = base_revenue - (base_volume / 4.5) * base_ops_cost  # Assuming 4.5 rides per user per month
    new_profit = new_revenue - (final_volume / 4.5) * new_ops_cost
    
    # Результаты
    st.subheader("📊 Влияние кризиса на бизнес")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Объем поездок", f"{final_volume:,.0f}", 
                 f"{((final_volume - base_volume) / base_volume * 100):+.1f}%")
    
    with col2:
        st.metric("Средний чек", f"{new_aov:.0f} руб", 
                 f"{((new_aov - base_aov) / base_aov * 100):+.1f}%")
    
    with col3:
        st.metric("Месячная выручка", f"{new_revenue:,.0f} руб", 
                 f"{((new_revenue - base_revenue) / base_revenue * 100):+.1f}%")
    
    with col4:
        st.metric("Прибыль", f"{new_profit:,.0f} руб", 
                 f"{((new_profit - base_profit) / base_profit * 100):+.1f}%")
    
    # Стратегические рекомендации для кризиса
    profit_impact = (new_profit - base_profit) / base_profit
    
    if profit_impact < -0.5:
        st.error("🚨 **Критическое влияние на прибыльность!** Необходимы экстренные меры.")
        recommendations = [
            "Радикальное сокращение операционных расходов",
            "Фокус на наиболее прибыльных сегментах",
            "Временное закрытие убыточных городов",
            "Переговоры с водителями о снижении комиссии"
        ]
    elif profit_impact < -0.2:
        st.warning("⚠️ **Серьезное влияние.** Нужна антикризисная стратегия.")
        recommendations = [
            "Сегментированные цены (эконом vs премиум)",
            "Loyalty программы для удержания пользователей",
            "Расширение в B2B сегмент",
            "Партнерства с работодателями"
        ]
    else:
        st.info("📊 **Умеренное влияние.** Возможность для укрепления позиций.")
        recommendations = [
            "Захват доли рынка от ослабленных конкурентов",
            "Инвестиции в технологии для снижения costs",
            "Подготовка к восстановлению экономики"
        ]
    
    st.markdown("### 💡 Рекомендуемые действия:")
    for rec in recommendations:
        st.write(f"• {rec}")

def regulation_scenario():
    """Сценарий усиления регулирования"""
    st.subheader("🚫 Усиление государственного регулирования")
    
    st.info("""
    **Ситуация**: Государство вводит новые требования для ride-hailing: лицензирование водителей,
    ограничения на surge pricing, обязательное страхование, налоги на цифровые услуги.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📋 Новые требования**")
        
        licensing_cost = st.slider("Стоимость лицензирования водителя (руб)", 5000, 50000, 15000)
        driver_retention_impact = st.slider("Отток водителей из-за лицензий (%)", 10, 40, 25)
        surge_limitation = st.slider("Ограничение surge pricing (макс. множитель)", 1.5, 3.0, 2.0)
        digital_tax = st.slider("Налог на цифровые услуги (%)", 0, 10, 5)
        
    with col2:
        st.markdown("**📊 Базовые показатели**")
        
        base_drivers = 50000
        base_surge_revenue_share = 15  # % от выручки приходится на surge
        base_avg_surge = 2.5
        base_monthly_revenue = 500_000_000
    
    # Расчет влияния регулирования
    
    # Влияние на водителей
    remaining_drivers = base_drivers * (1 - driver_retention_impact / 100)
    supply_shortage = (base_drivers - remaining_drivers) / base_drivers
    
    # Влияние на surge pricing
    surge_revenue_loss = 0
    if surge_limitation < base_avg_surge:
        surge_revenue_loss = (base_surge_revenue_share / 100) * base_monthly_revenue * \
                           ((base_avg_surge - surge_limitation) / base_avg_surge)
    
    # Влияние дефицита водителей на спрос
    demand_impact = supply_shortage * 0.8  # 80% эластичность спроса к доступности
    demand_loss = base_monthly_revenue * demand_impact
    
    # Налоговое влияние
    tax_cost = base_monthly_revenue * (digital_tax / 100)
    
    # Licensing costs
    monthly_licensing_cost = (base_drivers * licensing_cost) / 12  # Амортизация на год
    
    # Итоговое влияние
    total_revenue_impact = surge_revenue_loss + demand_loss
    total_cost_impact = tax_cost + monthly_licensing_cost
    net_impact = total_revenue_impact + total_cost_impact
    
    # Результаты
    st.subheader("💰 Финансовое влияние регулирования")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Потеря водителей", f"{base_drivers - remaining_drivers:,.0f}", 
                 f"-{driver_retention_impact}%")
    
    with col2:
        st.metric("Потеря от surge", f"{surge_revenue_loss:,.0f} руб", 
                 f"-{(surge_revenue_loss/base_monthly_revenue*100):.1f}%")
    
    with col3:
        st.metric("Потеря от дефицита", f"{demand_loss:,.0f} руб", 
                 f"-{(demand_loss/base_monthly_revenue*100):.1f}%")
    
    with col4:
        st.metric("Доп. расходы", f"{total_cost_impact:,.0f} руб", 
                 f"+{(total_cost_impact/base_monthly_revenue*100):.1f}%")
    
    # Общее влияние
    total_impact_pct = (net_impact / base_monthly_revenue) * 100
    
    if total_impact_pct > 15:
        st.error(f"🚨 **Критическое влияние**: {total_impact_pct:.1f}% от выручки!")
    elif total_impact_pct > 8:
        st.warning(f"⚠️ **Серьезное влияние**: {total_impact_pct:.1f}% от выручки")
    else:
        st.info(f"📊 **Умеренное влияние**: {total_impact_pct:.1f}% от выручки")
    
    # Стратегии адаптации
    st.subheader("🔧 Стратегии адаптации к регулированию")
    
    strategies = [
        {
            "Стратегия": "Помощь водителям с лицензированием",
            "Описание": "Subsidize licensing costs, обучающие программы",
            "Эффект": "Снижение оттока водителей на 50-70%",
            "Стоимость": f"{monthly_licensing_cost * 0.8:,.0f} руб/месяц"
        },
        {
            "Стратегия": "Технологическая оптимизация",
            "Описание": "AI для предсказания спроса, динамическое ценообразование в рамках лимитов",
            "Эффект": "Компенсация 30-40% потерь от surge ограничений",
            "Стоимость": "Инвестиции в R&D"
        },
        {
            "Стратегия": "Диверсификация сервисов",
            "Описание": "Доставка, грузоперевозки, subscription модели",
            "Эффект": "Новые источники дохода, снижение зависимости от регулирования",
            "Стоимость": "Значительные капиталовложения"
        },
        {
            "Стратегия": "Лоббирование и партнерства",
            "Описание": "Работа с регуляторами, отраслевые ассоциации",
            "Эффект": "Смягчение будущих регуляторных требований",
            "Стоимость": "Политические и юридические расходы"
        }
    ]
    
    strategies_df = pd.DataFrame(strategies)
    st.dataframe(strategies_df, use_container_width=True)

def pandemic_scenario():
    """Сценарий пандемии"""
    st.subheader("🦠 Пандемия / Форс-мажорные обстоятельства")
    
    st.error("""
    **Ситуация**: Пандемия или другие форс-мажорные обстоятельства кардинально меняют 
    паттерны мобильности. Lockdown, удаленная работа, страх перед общественным транспортом.
    """)
    
    # Фазы пандемии
    pandemic_phase = st.selectbox(
        "Фаза пандемии:",
        ["🔒 Lockdown (полная изоляция)", "📉 Partial restrictions", "📈 Recovery phase", "🆕 New normal"]
    )
    
    col1, col2 = st.columns(2)
    
    # Параметры в зависимости от фазы
    if pandemic_phase == "🔒 Lockdown (полная изоляция)":
        default_demand = -80
        default_essential = 20
        default_safety = 80
    elif pandemic_phase == "📉 Partial restrictions":
        default_demand = -50
        default_essential = 40
        default_safety = 60
    elif pandemic_phase == "📈 Recovery phase":
        default_demand = -20
        default_essential = 70
        default_safety = 30
    else:  # New normal
        default_demand = 10
        default_essential = 90
        default_safety = 10
    
    with col1:
        st.markdown(f"**📊 Параметры: {pandemic_phase}**")
        
        demand_change = st.slider("Изменение общего спроса (%)", -90, 50, default_demand)
        essential_trips_share = st.slider("Доля критически важных поездок (%)", 10, 90, default_essential)
        safety_premium = st.slider("Премия за безопасность vs общ.транспорт (%)", 0, 100, default_safety)
        
    with col2:
        st.markdown("**🚗 Адаптация сервиса**")
        
        safety_measures_cost = st.slider("Затраты на safety меры (% от выручки)", 0, 15, 8)
        delivery_expansion = st.slider("Expansion в доставку (% доп. выручки)", 0, 50, 25)
        pricing_adjustment = st.slider("Корректировка цен (%)", -30, 30, 0)
    
    # Базовые метрики
    base_monthly_volume = 2_000_000
    base_aov = 350
    base_take_rate = 25
    
    # Расчет влияния пандемии
    
    # Изменение спроса с учетом структуры поездок
    new_volume = base_monthly_volume * (1 + demand_change / 100)
    
    # Safety premium effect - люди предпочитают такси общественному транспорту
    safety_boost = base_monthly_volume * 0.1 * (safety_premium / 100)  # 10% базы могут переключиться
    final_volume = new_volume + safety_boost
    
    # Влияние на AOV
    new_aov = base_aov * (1 + pricing_adjustment / 100)
    
    # Диверсификация в доставку
    delivery_revenue = base_monthly_volume * base_aov * (base_take_rate / 100) * (delivery_expansion / 100)
    
    # Затраты на безопасность
    base_revenue = final_volume * new_aov * (base_take_rate / 100)
    safety_costs = base_revenue * (safety_measures_cost / 100)
    
    total_revenue = base_revenue + delivery_revenue
    net_revenue = total_revenue - safety_costs
    
    # Сравнение с базовым сценарием
    base_total_revenue = base_monthly_volume * base_aov * (base_take_rate / 100)
    
    # Результаты
    st.subheader("📈 Влияние на бизнес-показатели")
    
    col1, col2, col3, col4 = st.columns(4)
    
    volume_change = ((final_volume - base_monthly_volume) / base_monthly_volume) * 100
    revenue_change = ((total_revenue - base_total_revenue) / base_total_revenue) * 100
    
    with col1:
        st.metric("Объем поездок", f"{final_volume:,.0f}", f"{volume_change:+.1f}%")
    
    with col2:
        st.metric("AOV", f"{new_aov:.0f} руб", f"{pricing_adjustment:+.0f}%")
    
    with col3:
        st.metric("Общая выручка", f"{total_revenue:,.0f} руб", f"{revenue_change:+.1f}%")
    
    with col4:
        st.metric("Чистая выручка", f"{net_revenue:,.0f} руб", 
                 f"{((net_revenue - base_total_revenue) / base_total_revenue * 100):+.1f}%")
    
    # Breakdown по источникам выручки
    if delivery_revenue > 0:
        st.subheader("🍕 Структура выручки")
        
        fig = go.Figure(data=[go.Pie(
            labels=['Ride-hailing', 'Delivery'],
            values=[base_revenue, delivery_revenue],
            hole=0.3
        )])
        
        fig.update_layout(title="Диверсификация в условиях пандемии", height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Стратегические инсайты
    st.subheader("💡 Стратегические инсайты")
    
    if revenue_change > 0:
        st.success(f"""
        🎯 **Возможность в кризисе**: Выручка выросла на {revenue_change:.1f}%
        
        **Факторы успеха**:
        • Safety premium: +{safety_boost:,.0f} поездок
        • Диверсификация: +{delivery_revenue:,.0f} руб выручки
        • Адаптивная стратегия ценообразования
        """)
    else:
        st.warning(f"""
        ⚠️ **Сложный период**: Выручка снизилась на {abs(revenue_change):.1f}%
        
        **Факторы снижения**:
        • Общее падение спроса: {demand_change}%
        • Затраты на безопасность: {safety_costs:,.0f} руб
        • Ограничения мобильности
        """)
    
    # Рекомендации по фазам
    phase_recommendations = {
        "🔒 Lockdown (полная изоляция)": [
            "Полный pivot в доставку еды и товаров",
            "Минимизация операционных расходов",
            "Поддержка водителей (финансовая помощь)",
            "Подготовка к recovery phase"
        ],
        "📉 Partial restrictions": [
            "Hybrid модель: rides + delivery",
            "Максимальные safety меры",
            "Маркетинг safety преимуществ",
            "Flexible pricing для поддержки спроса"
        ],
        "📈 Recovery phase": [
            "Агрессивный возврат пользователей",
            "Постепенное увеличение цен",
            "Expansion supply side",
            "Подготовка к new normal"
        ],
        "🆕 New normal": [
            "Закрепление новых user behavior",
            "Инвестиции в technology (contactless)",
            "Expansion в смежные сервисы",
            "Подготовка к следующим кризисам"
        ]
    }
    
    st.markdown(f"### 🎯 Рекомендации для фазы '{pandemic_phase}':")
    for rec in phase_recommendations[pandemic_phase]:
        st.write(f"• {rec}")

def public_transport_scenario():
    """Развитие общественного транспорта"""
    st.subheader("🚇 Развитие общественного транспорта")
    
    st.info("""
    **Ситуация**: Город инвестирует в развитие общественного транспорта - новые линии метро, 
    BRT, улучшение автобусной сети. Растет конкуренция с более дешевой альтернативой.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🚇 Развитие транспорта**")
        
        metro_expansion = st.slider("Расширение метро (новых станций)", 0, 20, 8)
        bus_improvement = st.slider("Улучшение автобусной сети (%)", 0, 50, 25)
        public_transport_price = st.slider("Цена поездки в общ.транспорте (руб)", 20, 80, 45)
        
        # Влияние на ride-hailing
        coverage_impact = st.slider("Покрытие маршрутов ride-hailing (%)", 30, 80, 55)
        
    with col2:
        st.markdown("**🚗 Текущие показатели**")
        
        current_aov = 350
        current_frequency = 4.2
        current_users = 150000
        price_elasticity = 2.1  # Чувствительность к цене
        
        st.metric("Средний чек ride-hailing", f"{current_aov} руб")
        st.metric("Цена общ.транспорта", f"{public_transport_price} руб")
        st.metric("Соотношение цен", f"{current_aov/public_transport_price:.1f}x")
    
    # Расчет влияния
    
    # Price advantage общественного транспорта
    price_ratio = current_aov / public_transport_price
    
    # Оценка переключения пользователей
    # Эластичность спроса: чем больше разница в цене, тем больше переключаются
    demand_elasticity_effect = min(0.4, (price_ratio - 3) * 0.1)  # Максимум 40% могут переключиться
    
    # Влияние покрытия маршрутов
    coverage_effect = (coverage_impact / 100) * 0.3  # До 30% дополнительного влияния
    
    total_demand_loss = (demand_elasticity_effect + coverage_effect) * 100
    
    # Качественные улучшения общ.транспорта
    quality_multiplier = 1 + (bus_improvement / 100) * 0.5
    metro_effect = metro_expansion * 0.02  # Каждая станция = 2% дополнительного влияния
    
    final_demand_loss = min(60, total_demand_loss * quality_multiplier + metro_effect * 100)
    
    # Влияние на сегменты
    # Больше всего страдают короткие поездки в центре
    short_trips_loss = final_demand_loss * 1.5
    long_trips_loss = final_demand_loss * 0.6
    premium_trips_loss = final_demand_loss * 0.3  # Премиум сегмент менее чувствителен
    
    # Новые показатели
    new_users = current_users * (1 - final_demand_loss / 100)
    new_frequency = current_frequency * 0.95  # Небольшое снижение частоты
    
    # Адаптационные стратегии
    st.subheader("📊 Сегментированное влияние")
    
    segments_data = {
        'Сегмент': ['Короткие поездки (<3 км)', 'Средние поездки (3-10 км)', 
                   'Длинные поездки (>10 км)', 'Премиум сегмент'],
        'Потеря спроса': [f"{short_trips_loss:.1f}%", f"{final_demand_loss:.1f}%", 
                         f"{long_trips_loss:.1f}%", f"{premium_trips_loss:.1f}%"],
        'Причина': ['Прямая конкуренция с метро/автобусом', 'Улучшение связности', 
                   'Ограниченное влияние', 'Низкая price sensitivity']
    }
    
    st.table(segments_data)
    
    # Финансовое влияние
    col1, col2, col3 = st.columns(3)
    
    revenue_impact = ((new_users * new_frequency) - (current_users * current_frequency)) / (current_users * current_frequency) * 100
    
    with col1:
        st.metric("Потеря пользователей", f"{current_users - new_users:,.0f}", 
                 f"{((new_users - current_users) / current_users * 100):+.1f}%")
    
    with col2:
        st.metric("Влияние на частоту", f"{new_frequency:.1f}", 
                 f"{((new_frequency - current_frequency) / current_frequency * 100):+.1f}%")
    
    with col3:
        st.metric("Общее влияние на выручку", f"{revenue_impact:+.1f}%", 
                 "Critical" if revenue_impact < -20 else "Moderate")
    
    # Стратегии адаптации
    st.subheader("🎯 Стратегии адаптации")
    
    if revenue_impact < -25:
        st.error("🚨 **Критическое влияние** - необходима кардинальная перестройка стратегии")
        strategies = [
            "**First/Last mile solution**: Интеграция с общественным транспортом",
            "**Premium positioning**: Фокус на комфорт и скорость vs цену",
            "**Suburban expansion**: Районы со слабым покрытием общ.транспорта",
            "**Multi-modal app**: Добавить общественный транспорт в приложение"
        ]
    elif revenue_impact < -15:
        st.warning("⚠️ **Серьезное влияние** - нужна адаптация value proposition")
        strategies = [
            "**Time advantage**: Акцент на экономии времени",
            "**Weather positioning**: Преимущества в плохую погоду",
            "**Group rides**: Снижение cost per person",
            "**Corporate segment**: B2B решения"
        ]
    else:
        st.info("📊 **Умеренное влияние** - возможности для сотрудничества")
        strategies = [
            "**Partnership opportunities**: Совместные решения с городом",
            "**Complementary service**: Ride-hailing + общ.транспорт",
            "**Quality differentiation**: Улучшение user experience",
            "**New use cases**: Поездки в rush hour, ночное время"
        ]
    
    for strategy in strategies:
        st.write(f"• {strategy}")
    
    # Возможности
    st.markdown("""
    ### 💡 Скрытые возможности:
    
    1. **Intermodal integration**: Стать частью городской транспортной экосистемы
    2. **Peak hour advantage**: Когда общ.транспорт переполнен
    3. **Accessibility**: Для людей с ограниченными возможностями
    4. **Cargo/delivery**: Использование транспортной инфраструктуры
    5. **Data partnership**: Аналитика мобильности для города
    """)

def new_city_launch_scenario():
    """Запуск в новом городе"""
    st.subheader("🚗 Запуск в новом городе")
    
    st.success("""
    **Ситуация**: Планируете launch в новом городе. Нужно спрогнозировать unit economics, 
    определить стратегию проникновения и timeline до breakeven.
    """)
    
    # Параметры города
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🏙️ Характеристики города**")
        
        city_population = st.number_input("Население города", 300000, 5000000, 1200000, 50000)
        car_penetration = st.slider("Автомобилизация (авто на 1000 жителей)", 200, 600, 350)
        avg_income = st.number_input("Средний доход (руб/месяц)", 30000, 150000, 55000, 5000)
        public_transport_quality = st.slider("Качество общ.транспорта (1-10)", 1, 10, 5)
        
    with col2:
        st.markdown("**🎯 Стратегия запуска**")
        
        launch_strategy = st.selectbox("Стратегия запуска:", 
                                     ["Aggressive (быстрый захват)", "Moderate (постепенный рост)", 
                                      "Conservative (осторожный вход)"])
        
        initial_promo_budget = st.number_input("Промо-бюджет на launch (руб)", 1000000, 50000000, 8000000, 500000)
        target_market_share = st.slider("Целевая доля рынка через год (%)", 5, 40, 20)
        
        # Конкуренция
        existing_competitors = st.slider("Количество конкурентов", 0, 5, 2)
    
    # Расчет потенциала рынка
    
    # Addressable market
    # Предполагаем, что 15-25% населения потенциально может использовать ride-hailing
    market_penetration_potential = 0.15 + (avg_income - 30000) / 120000 * 0.1  # Higher income = higher penetration
    market_penetration_potential = min(0.25, max(0.10, market_penetration_potential))
    
    # Корректировки на качество общ.транспорта (плохой транспорт = больше потенциал)
    transport_multiplier = 1.5 - (public_transport_quality / 10) * 0.5
    
    # Конкуренция снижает потенциал
    competition_factor = 1 / (1 + existing_competitors * 0.2)
    
    total_addressable_market = city_population * market_penetration_potential * transport_multiplier * competition_factor
    
    # Прогноз метрик
    estimated_frequency = 2.5 + (avg_income - 30000) / 60000  # Больше доходы = больше поездок
    estimated_frequency = min(5.0, max(1.5, estimated_frequency))
    
    estimated_aov = 200 + (avg_income - 30000) / 1000  # Зависимость от доходов
    estimated_aov = min(500, max(150, estimated_aov))
    
    # CAC зависит от стратегии и конкуренции
    strategy_multipliers = {"Aggressive (быстрый захват)": 2.0, "Moderate (постепенный рост)": 1.3, "Conservative (осторожный вход)": 1.0}
    base_cac = 800 + existing_competitors * 300
    estimated_cac = base_cac * strategy_multipliers[launch_strategy]
    
    # Timeline запуска по месяцам
    months_to_target = 12 if launch_strategy.startswith("Aggressive") else 18 if launch_strategy.startswith("Moderate") else 24
    
    # Расчет пользователей по месяцам
    target_users = total_addressable_market * (target_market_share / 100)
    
    # Результаты анализа
    st.subheader("📊 Потенциал рынка")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Потенциал рынка", f"{total_addressable_market:,.0f}")
    
    with col2:
        st.metric("Целевые пользователи", f"{target_users:,.0f}")
    
    with col3:
        st.metric("Прогноз AOV", f"{estimated_aov:.0f} руб")
    
    with col4:
        st.metric("Прогноз CAC", f"{estimated_cac:,.0f} руб")
    
    # Финансовая модель запуска
    create_launch_financial_model(target_users, estimated_aov, estimated_frequency, estimated_cac, 
                                 initial_promo_budget, months_to_target, launch_strategy)
    
    # Рекомендации по запуску
    show_launch_recommendations(city_population, avg_income, public_transport_quality, 
                               existing_competitors, launch_strategy)

def create_launch_financial_model(target_users: float, aov: float, frequency: float, cac: float,
                                 promo_budget: int, months_to_target: int, strategy: str):
    """Финансовая модель запуска в новом городе"""
    
    st.subheader("💰 Финансовая модель запуска")
    
    # Кривая роста пользователей
    months = list(range(1, months_to_target + 1))
    
    # S-образная кривая роста
    if strategy.startswith("Aggressive"):
        # Быстрый рост в начале, потом замедление
        users_curve = [target_users * (1 - np.exp(-3 * m / months_to_target)) for m in months]
    elif strategy.startswith("Moderate"):
        # Линейный рост
        users_curve = [target_users * m / months_to_target for m in months]
    else:
        # Медленный старт, потом ускорение
        users_curve = [target_users * (m / months_to_target) ** 1.5 for m in months]
    
    # Расчет помесячных показателей
    monthly_data = []
    cumulative_cac_spend = 0
    cumulative_revenue = 0
    
    for i, month in enumerate(months):
        current_users = users_curve[i]
        new_users = current_users if i == 0 else current_users - users_curve[i-1]
        
        # CAC spend
        monthly_cac_spend = new_users * cac
        cumulative_cac_spend += monthly_cac_spend
        
        # Промо расходы (больше в начале)
        promo_weight = 2 - (month / months_to_target)  # От 2 до 1
        monthly_promo = (promo_budget / months_to_target) * promo_weight
        
        # Revenue (с учетом ramp-up новых пользователей)
        # Новые пользователи в первый месяц делают только 50% от полной частоты
        active_users = current_users * 0.85  # 85% активны каждый месяц
        monthly_revenue = active_users * aov * frequency * 0.25  # 25% take rate
        cumulative_revenue += monthly_revenue
        
        # Прибыльность
        monthly_costs = monthly_cac_spend + monthly_promo + (current_users * 15)  # 15 руб ops cost на пользователя
        monthly_profit = monthly_revenue - monthly_costs
        
        monthly_data.append({
            'month': month,
            'users': current_users,
            'new_users': new_users,
            'revenue': monthly_revenue,
            'cac_spend': monthly_cac_spend,
            'promo_spend': monthly_promo,
            'profit': monthly_profit,
            'cumulative_revenue': cumulative_revenue,
            'cumulative_cac': cumulative_cac_spend
        })
    
    # График финансовой модели
    df = pd.DataFrame(monthly_data)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Рост пользователей', 'Месячная выручка vs расходы',
                       'Накопительная прибыльность', 'Breakeven анализ'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # График 1: Рост пользователей
    fig.add_trace(
        go.Scatter(x=df['month'], y=df['users'], mode='lines+markers',
                  name='Пользователи', line=dict(color='blue', width=3)),
        row=1, col=1
    )
    
    # График 2: Выручка vs расходы
    fig.add_trace(
        go.Bar(x=df['month'], y=df['revenue'], name='Выручка', marker_color='green'),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(x=df['month'], y=df['cac_spend'] + df['promo_spend'], name='Расходы', marker_color='red'),
        row=1, col=2
    )
    
    # График 3: Накопительная прибыльность
    cumulative_profit = np.cumsum(df['profit'])
    fig.add_trace(
        go.Scatter(x=df['month'], y=cumulative_profit, mode='lines+markers',
                  name='Накопительная прибыль', line=dict(color='purple', width=3)),
        row=2, col=1
    )
    fig.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=1)
    
    # График 4: ROI
    cumulative_spend = df['cumulative_cac'] + np.cumsum(df['promo_spend'])
    roi = (df['cumulative_revenue'] - cumulative_spend) / cumulative_spend * 100
    fig.add_trace(
        go.Scatter(x=df['month'], y=roi, mode='lines+markers',
                  name='ROI (%)', line=dict(color='orange', width=3)),
        row=2, col=2
    )
    fig.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)
    
    fig.update_layout(height=600, showlegend=False)
    fig.update_xaxes(title_text="Месяц")
    fig.update_yaxes(title_text="Пользователи", row=1, col=1)
    fig.update_yaxes(title_text="Руб", row=1, col=2)
    fig.update_yaxes(title_text="Руб", row=2, col=1)
    fig.update_yaxes(title_text="ROI (%)", row=2, col=2)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Ключевые метрики
    col1, col2, col3 = st.columns(3)
    
    breakeven_month = None
    for i, profit in enumerate(cumulative_profit):
        if profit > 0:
            breakeven_month = i + 1
            break
    
    total_investment = cumulative_spend[-1]
    final_revenue = df['cumulative_revenue'].iloc[-1]
    final_roi = roi.iloc[-1]
    
    with col1:
        if breakeven_month:
            st.metric("Breakeven", f"{breakeven_month} месяц")
        else:
            st.metric("Breakeven", "Не достигнут")
    
    with col2:
        st.metric("Общие инвестиции", f"{total_investment:,.0f} руб")
    
    with col3:
        color = "success" if final_roi > 50 else "warning" if final_roi > 0 else "error"
        st.markdown(f"""
        <div class="{color}-card">
            <h4>ROI через {months_to_target} мес</h4>
            <h2>{final_roi:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)

def show_launch_recommendations(population: int, income: int, transport_quality: int,
                               competitors: int, strategy: str):
    """Рекомендации по запуску"""
    
    st.subheader("🎯 Рекомендации по запуску")
    
    # Оценка привлекательности рынка
    attractiveness_score = 0
    
    # Размер рынка
    if population > 1_500_000:
        attractiveness_score += 3
    elif population > 800_000:
        attractiveness_score += 2
    else:
        attractiveness_score += 1
    
    # Доходы
    if income > 80_000:
        attractiveness_score += 3
    elif income > 50_000:
        attractiveness_score += 2
    else:
        attractiveness_score += 1
    
    # Общественный транспорт (чем хуже, тем лучше для нас)
    if transport_quality < 4:
        attractiveness_score += 3
    elif transport_quality < 7:
        attractiveness_score += 2
    else:
        attractiveness_score += 1
    
    # Конкуренция (чем меньше, тем лучше)
    if competitors == 0:
        attractiveness_score += 3
    elif competitors <= 2:
        attractiveness_score += 2
    else:
        attractiveness_score += 1
    
    # Интерпретация
    if attractiveness_score >= 10:
        st.success("🎯 **Высокоприоритетный рынок** - отличные условия для запуска")
        priority = "Высокий"
    elif attractiveness_score >= 7:
        st.info("📊 **Перспективный рынок** - хорошие возможности при правильной стратегии")
        priority = "Средний"
    else:
        st.warning("⚠️ **Сложный рынок** - требует осторожного подхода и больших инвестиций")
        priority = "Низкий"
    
    # Специфические рекомендации
    recommendations = []
    
    if income < 50_000:
        recommendations.append("🎯 **Price-sensitive market**: Фокус на низкие цены и промокоды")
    
    if transport_quality > 7:
        recommendations.append("🚇 **Strong public transport**: Позиционирование как premium alternative")
    
    if competitors >= 3:
        recommendations.append("🆚 **High competition**: Необходима уникальная value proposition")
    
    if population < 500_000:
        recommendations.append("🏘️ **Small market**: Рассмотреть региональную стратегию")
    
    # Стратегические рекомендации по фазам
    phase_recommendations = {
        "Aggressive (быстрый захват)": [
            "Массивные промокампании в первые 3 месяца",
            "Aggressive driver onboarding с бонусами",
            "PR и маркетинг для создания buzz'а",
            "Быстрое расширение зоны покрытия"
        ],
        "Moderate (постепенный рост)": [
            "Постепенное расширение по районам",
            "Фокус на качество сервиса с самого начала",
            "Partnerships с местными бизнесами",
            "Organic growth через word-of-mouth"
        ],
        "Conservative (осторожный вход)": [
            "Pilot в одном районе города",
            "Глубокое изучение local preferences",
            "Минимальные промокоды, фокус на retention",
            "Постепенное масштабирование при положительных метриках"
        ]
    }
    
    st.markdown(f"### 📋 Рекомендации для стратегии '{strategy}':")
    for rec in phase_recommendations[strategy]:
        st.write(f"• {rec}")
    
    if recommendations:
        st.markdown("### 🎯 Специфические рекомендации:")
        for rec in recommendations:
            st.write(f"• {rec}")

def promo_optimizer():
    """Оптимизатор промокодов"""
    st.header("💰 Оптимизатор промокодов")
    
    st.markdown("""
    **Промокоды в ride-hailing**: мощный инструмент привлечения, но съедающий маржу. 
    Ключ - найти оптимальный баланс между объемом привлечения и unit economics.
    """)
    
    # Типы промокодов
    promo_type = st.selectbox(
        "Тип промокампании:",
        [
            "🆕 Привлечение новых пользователей",
            "🔄 Реактивация неактивных",
            "💎 Retention существующих",
            "🆚 Конкурентная защита",
            "🎯 Sегментированные промо"
        ]
    )
    
    if promo_type == "🆕 Привлечение новых пользователей":
        new_user_promo_optimization()
    elif promo_type == "🔄 Реактивация неактивных":
        reactivation_promo_optimization()
    elif promo_type == "💎 Retention существующих":
        retention_promo_optimization()
    elif promo_type == "🆚 Конкурентная защита":
        competitive_defense_promo()
    elif promo_type == "🎯 Sегментированные промо":
        segmented_promo_optimization()

def new_user_promo_optimization():
    """Оптимизация промокодов для новых пользователей"""
    st.subheader("🆕 Промокоды для новых пользователей")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**⚙️ Параметры промокампании**")
        
        promo_discount = st.slider("Размер скидки (%)", 20, 80, 50)
        max_rides_promo = st.slider("Максимум поездок по промо", 1, 10, 3)
        promo_budget = st.number_input("Бюджет на промокоды (руб)", 500000, 20000000, 3000000)
        
        # Базовые метрики
        base_aov = 350
        base_conversion_rate = 5  # % от показов промо конвертируются в первую поездку
        
    with col2:
        st.markdown("**📊 Поведенческие параметры**")
        
        promo_elasticity = st.slider("Эластичность к размеру скидки", 0.5, 2.0, 1.2)
        activation_rate = st.slider("Доля делающих 2+ поездки (%)", 30, 80, 55)
        organic_frequency = st.slider("Частота после промо", 2.0, 6.0, 3.8)
        
    # Расчет эффективности промокампании
    
    # Влияние размера скидки на конверсию
    boosted_conversion = base_conversion_rate * (1 + (promo_discount / 100) * promo_elasticity)
    
    # Количество пользователей, которых можем привлечь
    promo_aov = base_aov * (1 - promo_discount / 100)
    cost_per_promo_ride = base_aov - promo_aov
    
    # Максимальное количество новых пользователей при данном бюджете
    max_new_users = promo_budget / (cost_per_promo_ride * max_rides_promo)
    
    # Фактическое количество с учетом конверсии
    actual_new_users = max_new_users * (boosted_conversion / 100) if boosted_conversion <= 100 else max_new_users
    
    # LTV анализ
    # Промо-пользователи: первые max_rides_promo по скидке, потом organic
    promo_revenue = actual_new_users * max_rides_promo * promo_aov * 0.25  # 25% take rate
    
    # Активированные пользователи продолжают использовать сервис
    activated_users = actual_new_users * (activation_rate / 100)
    organic_ltv_per_user = (base_aov * 0.25 * organic_frequency) / 0.12  # 12% месячный churn
    total_organic_revenue = activated_users * organic_ltv_per_user
    
    total_revenue = promo_revenue + total_organic_revenue
    effective_cac = promo_budget / actual_new_users if actual_new_users > 0 else float('inf')
    ltv_per_user = total_revenue / actual_new_users if actual_new_users > 0 else 0
    
    # Результаты
    st.subheader("📈 Результаты промокампании")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Привлеченных пользователей", f"{actual_new_users:,.0f}")
    
    with col2:
        st.metric("Эффективный CAC", f"{effective_cac:,.0f} руб")
    
    with col3:
        st.metric("LTV на пользователя", f"{ltv_per_user:,.0f} руб")
    
    with col4:
        ltv_cac_ratio = ltv_per_user / effective_cac if effective_cac != float('inf') else 0
        color = "success" if ltv_cac_ratio >= 3 else "warning" if ltv_cac_ratio >= 2 else "error"
        st.markdown(f"""
        <div class="{color}-card">
            <h4>LTV/CAC</h4>
            <h2>{ltv_cac_ratio:.1f}:1</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Оптимизация промо-параметров
    create_promo_optimization_chart(promo_budget, base_aov, base_conversion_rate, 
                                   activation_rate, organic_frequency, promo_elasticity)
    
    # Рекомендации
    show_promo_recommendations(ltv_cac_ratio, promo_discount, activation_rate)

def create_promo_optimization_chart(budget: int, aov: float, base_conv: float,
                                   activation: float, frequency: float, elasticity: float):
    """График оптимизации промопараметров"""
    
    st.subheader("🎯 Оптимизация промопараметров")
    
    # Сценарии с разными размерами скидок
    discount_range = np.arange(20, 81, 10)
    scenarios = []
    
    for discount in discount_range:
        # Расчет для каждого уровня скидки
        boosted_conv = base_conv * (1 + (discount / 100) * elasticity)
        promo_aov = aov * (1 - discount / 100)
        cost_per_ride = aov - promo_aov
        
        max_users = budget / (cost_per_ride * 3)  # 3 промо-поездки
        actual_users = max_users * min(boosted_conv / 100, 1.0)
        
        # LTV расчет
        promo_revenue = actual_users * 3 * promo_aov * 0.25
        activated = actual_users * (activation / 100)
        organic_ltv = (aov * 0.25 * frequency) / 0.12
        total_revenue = promo_revenue + activated * organic_ltv
        
        cac = budget / actual_users if actual_users > 0 else 0
        ltv = total_revenue / actual_users if actual_users > 0 else 0
        roi = (total_revenue - budget) / budget * 100 if budget > 0 else 0
        
        scenarios.append({
            'discount': discount,
            'users': actual_users,
            'cac': cac,
            'ltv': ltv,
            'roi': roi,
            'ltv_cac_ratio': ltv / cac if cac > 0 else 0
        })
    
    df_scenarios = pd.DataFrame(scenarios)
    
    # График сравнения сценариев
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Привлеченные пользователи', 'LTV/CAC соотношение',
                       'ROI кампании', 'CAC vs LTV'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "scatter"}]]
    )
    
    # График 1: Пользователи
    fig.add_trace(
        go.Bar(x=df_scenarios['discount'], y=df_scenarios['users'],
               marker_color='blue', showlegend=False),
        row=1, col=1
    )
    
    # График 2: LTV/CAC
    fig.add_trace(
        go.Bar(x=df_scenarios['discount'], y=df_scenarios['ltv_cac_ratio'],
               marker_color='green', showlegend=False),
        row=1, col=2
    )
    
    # График 3: ROI
    colors = ['green' if roi > 0 else 'red' for roi in df_scenarios['roi']]
    fig.add_trace(
        go.Bar(x=df_scenarios['discount'], y=df_scenarios['roi'],
               marker_color=colors, showlegend=False),
        row=2, col=1
    )
    
    # График 4: CAC vs LTV scatter
    fig.add_trace(
        go.Scatter(x=df_scenarios['cac'], y=df_scenarios['ltv'],
                  mode='markers+text', text=[f"{d}%" for d in df_scenarios['discount']],
                  textposition="top center", marker=dict(size=10, color='purple'),
                  showlegend=False),
        row=2, col=2
    )
    
    fig.update_layout(height=600)
    fig.update_xaxes(title_text="Размер скидки (%)", row=1, col=1)
    fig.update_xaxes(title_text="Размер скидки (%)", row=1, col=2)
    fig.update_xaxes(title_text="Размер скидки (%)", row=2, col=1)
    fig.update_xaxes(title_text="CAC (руб)", row=2, col=2)
    fig.update_yaxes(title_text="Пользователи", row=1, col=1)
    fig.update_yaxes(title_text="LTV/CAC", row=1, col=2)
    fig.update_yaxes(title_text="ROI (%)", row=2, col=1)
    fig.update_yaxes(title_text="LTV (руб)", row=2, col=2)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Оптимальная скидка
    optimal_scenario = max(scenarios, key=lambda x: x['roi'])
    st.success(f"""
    🎯 **Оптимальный размер скидки**: {optimal_scenario['discount']}%
    
    • Привлеченных пользователей: {optimal_scenario['users']:,.0f}
    • LTV/CAC: {optimal_scenario['ltv_cac_ratio']:.1f}:1
    • ROI кампании: {optimal_scenario['roi']:.1f}%
    """)

def show_promo_recommendations(ltv_cac_ratio: float, discount: int, activation: int):
    """Рекомендации по промокодам"""
    
    st.subheader("💡 Рекомендации по промостратегии")
    
    if ltv_cac_ratio >= 3:
        st.success("✅ **Эффективная промостратегия** - можно масштабировать")
        recs = [
            "Увеличить бюджет на промокоды при сохранении параметров",
            "Тестировать увеличение количества промо-поездок",
            "Расширить каналы привлечения с текущими промо"
        ]
    elif ltv_cac_ratio >= 2:
        st.warning("⚠️ **Промостратегия на грани** - нужна оптимизация")
        recs = [
            "Снизить размер скидки и компенсировать targeting'ом",
            "Фокус на улучшение activation rate через onboarding",
            "A/B тест разных промо-механик (cashback vs скидка)"
        ]
    else:
        st.error("🚨 **Неэффективные промокоды** - срочно пересматривать")
        recs = [
            "Кардинально снизить размер скидки",
            "Перейти с blanket промо на targeted",
            "Сфокусироваться на organic каналах"
        ]
    
    for rec in recs:
        st.write(f"• {rec}")
    
    # Дополнительные инсайты
    if discount > 60:
        st.warning("💸 **Слишком высокие скидки** могут привлекать не целевую аудиторию")
    
    if activation < 40:
        st.error("📉 **Низкий activation rate** - проблема в product experience, не в промо")
    
    st.markdown("""
    ### 🧠 Психология промокодов в ride-hailing:
    
    1. **FOMO эффект**: Ограниченное время действия увеличивает конверсию
    2. **Якорный эффект**: Показ полной цены со скидкой vs просто низкой цены
    3. **Frequency illusion**: После первой поездки пользователь чаще замечает бренд
    4. **Habit formation**: 3-4 поездки обычно достаточно для формирования привычки
    5. **Price anchoring**: Промопользователи могут стать price-sensitive в долгосроке
    """)

def reactivation_promo_optimization():
    """Оптимизация промокодов для реактивации"""
    st.subheader("🔄 Реактивация неактивных пользователей")
    
    st.info("""
    **Особенности реактивации**: пользователи уже знают продукт, поэтому нужны другие стимулы.
    Часто эффективнее небольшие скидки + персонализация.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**👥 Сегменты неактивных**")
        
        recent_inactive = st.number_input("Неактивны 1-3 месяца", 10000, 500000, 150000, 10000)
        long_inactive = st.number_input("Неактивны 3-6 месяцев", 5000, 300000, 80000, 5000)
        dormant = st.number_input("Неактивны >6 месяцев", 20000, 1000000, 200000, 10000)
        
    with col2:
        st.markdown("**💰 Промопараметры**")
        
        reactivation_budget = st.number_input("Бюджет реактивации", 500000, 10000000, 2000000)
        promo_size = st.slider("Размер скидки (%)", 15, 50, 25)
        personalization_lift = st.slider("Лифт от персонализации (%)", 10, 100, 40)
    
    # Базовые показатели реактивации по сегментам
    base_reactivation_rates = {
        'recent': 12,  # % реактивируются без промо
        'long': 6,
        'dormant': 2
    }
    
    # Эффект промокодов и персонализации
    promo_lift = promo_size / 20  # Каждые 20% скидки = 1x лифт
    total_lift = promo_lift * (1 + personalization_lift / 100)
    
    # Расчет по сегментам
    segments_analysis = {}
    total_reactivated = 0
    total_cost = 0
    
    for segment, count in [('recent', recent_inactive), ('long', long_inactive), ('dormant', dormant)]:
        base_rate = base_reactivation_rates[segment.split('_')[0] if '_' in segment else segment]
        boosted_rate = min(base_rate * (1 + total_lift), 50)  # Максимум 50% реактивация
        
        reactivated = count * (boosted_rate / 100)
        cost_per_reactivation = 350 * (promo_size / 100) * 2  # 2 промо-поездки
        segment_cost = reactivated * cost_per_reactivation
        
        segments_analysis[segment] = {
            'count': count,
            'base_rate': base_rate,
            'boosted_rate': boosted_rate,
            'reactivated': reactivated,
            'cost': segment_cost,
            'cac': cost_per_reactivation
        }
        
        total_reactivated += reactivated
        total_cost += segment_cost
    
    # Результаты
    st.subheader("📊 Результаты реактивации")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        for segment, data in segments_analysis.items():
            segment_name = {"recent": "Недавние", "long": "Давние", "dormant": "Спящие"}[segment]
            st.metric(f"{segment_name} ({data['boosted_rate']:.1f}%)", 
                     f"{data['reactivated']:,.0f}")
    
    with col2:
        st.metric("Общая реактивация", f"{total_reactivated:,.0f}")
        st.metric("Общие затраты", f"{total_cost:,.0f} руб")
    
    with col3:
        avg_cac = total_cost / total_reactivated if total_reactivated > 0 else 0
        st.metric("Средний CAC реактивации", f"{avg_cac:,.0f} руб")
        
        # LTV реактивированных (обычно ниже новых пользователей)
        reactivated_ltv = 4200  # Примерная оценка
        ltv_cac = reactivated_ltv / avg_cac if avg_cac > 0 else 0
        
        color = "success" if ltv_cac >= 3 else "warning" if ltv_cac >= 2 else "error"
        st.markdown(f"""
        <div class="{color}-card">
            <h4>LTV/CAC</h4>
            <h2>{ltv_cac:.1f}:1</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Сравнение эффективности по сегментам
    fig = go.Figure()
    
    segments = list(segments_analysis.keys())
    segment_names = ["Недавние", "Давние", "Спящие"]
    rates = [segments_analysis[s]['boosted_rate'] for s in segments]
    costs = [segments_analysis[s]['cac'] for s in segments]
    
    fig.add_trace(go.Bar(
        x=segment_names,
        y=rates,
        name='Реактивация (%)',
        marker_color='green',
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=segment_names,
        y=costs,
        mode='lines+markers',
        name='CAC (руб)',
        line=dict(color='red', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Эффективность реактивации по сегментам",
        xaxis_title="Сегмент неактивных",
        yaxis=dict(title="Реактивация (%)", side="left"),
        yaxis2=dict(title="CAC (руб)", side="right", overlaying="y"),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Рекомендации по реактивации
    st.markdown("""
    ### 💡 Рекомендации по реактивации:
    
    1. **Таргетинг недавних**: Лучшее соотношение эффективности к стоимости
    2. **Персонализация сообщений**: "Мы скучали по вам" + любимый маршрут
    3. **Timing важен**: Не сразу после ухода, но и не слишком поздно
    4. **Причинный анализ**: Понять, почему ушли (цена, качество, конкурент)
    5. **Градуированные промо**: Начать с малого, эскалировать при необходимости
    """)

def retention_promo_optimization():
    """Промокоды для удержания"""
    st.subheader("💎 Retention промокоды")
    
    st.success("""
    **Философия retention промо**: лучше дать небольшую скидку лояльному клиенту, 
    чем потерять его и тратить в 5 раз больше на привлечение нового.
    """)
    
    # Риск-сегментация пользователей
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**⚠️ Риск-сегменты**")
        
        high_risk_users = st.number_input("Высокий риск оттока", 5000, 100000, 25000)
        medium_risk_users = st.number_input("Средний риск", 10000, 200000, 50000)
        low_risk_users = st.number_input("Низкий риск", 50000, 500000, 150000)
        
    with col2:
        st.markdown("**🎯 Retention стратегия**")
        
        intervention_timing = st.selectbox("Timing вмешательства:", 
                                         ["Predictive (до оттока)", "Reactive (после снижения активности)"])
        
        retention_budget = st.number_input("Бюджет на retention", 500000, 5000000, 1500000)
        
        # Типы retention промо
        promo_strategy = st.selectbox("Тип промо:", 
                                    ["Скидки на поездки", "Cashback программа", "Loyalty points", "Premium features"])
    
    # Модель риска оттока и эффективности intervention
    risk_segments = {
        'high': {
            'count': high_risk_users,
            'churn_probability': 80,  # % вероятность ухода без intervention
            'intervention_effectiveness': 60,  # % снижения риска при intervention
            'cost_per_intervention': 150
        },
        'medium': {
            'count': medium_risk_users,
            'churn_probability': 40,
            'intervention_effectiveness': 45,
            'cost_per_intervention': 80
        },
        'low': {
            'count': low_risk_users,
            'churn_probability': 15,
            'intervention_effectiveness': 30,
            'cost_per_intervention': 40
        }
    }
    
    # Расчет ROI от retention программы
    total_saved_users = 0
    total_program_cost = 0
    
    retention_results = {}
    
    for segment, data in risk_segments.items():
        # Пользователи, которых потеряли бы без программы
        would_churn = data['count'] * (data['churn_probability'] / 100)
        
        # Пользователи, которых сохранили благодаря программе
        saved_users = would_churn * (data['intervention_effectiveness'] / 100)
        
        # Стоимость программы для сегмента
        segment_cost = data['count'] * data['cost_per_intervention']
        
        retention_results[segment] = {
            'would_churn': would_churn,
            'saved': saved_users,
            'cost': segment_cost,
            'roi_per_saved': segment_cost / saved_users if saved_users > 0 else 0
        }
        
        total_saved_users += saved_users
        total_program_cost += segment_cost
    
    # LTV анализ сохраненных пользователей
    avg_ltv_remaining = 3500  # LTV пользователя, который остался благодаря retention программе
    total_ltv_saved = total_saved_users * avg_ltv_remaining
    program_roi = (total_ltv_saved - total_program_cost) / total_program_cost * 100
    
    # Результаты
    st.subheader("📈 Эффективность retention программы")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Сохраненных пользователей", f"{total_saved_users:,.0f}")
    
    with col2:
        st.metric("Затраты на программу", f"{total_program_cost:,.0f} руб")
    
    with col3:
        st.metric("LTV сохраненных", f"{total_ltv_saved:,.0f} руб")
    
    with col4:
        color = "success" if program_roi > 200 else "warning" if program_roi > 100 else "error"
        st.markdown(f"""
        <div class="{color}-card">
            <h4>ROI программы</h4>
            <h2>{program_roi:.0f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Breakdown по сегментам
    st.subheader("📊 Эффективность по сегментам")
    
    segments_df = pd.DataFrame([
        {
            'Сегмент': {'high': 'Высокий риск', 'medium': 'Средний риск', 'low': 'Низкий риск'}[seg],
            'Пользователей': data['count'],
            'Ушли бы': f"{retention_results[seg]['would_churn']:.0f}",
            'Сохранили': f"{retention_results[seg]['saved']:.0f}",
            'Затраты': f"{retention_results[seg]['cost']:,.0f} руб",
            'Cost per save': f"{retention_results[seg]['roi_per_saved']:.0f} руб"
        }
        for seg, data in risk_segments.items()
    ])
    
    st.dataframe(segments_df, use_container_width=True)
    
    # Recommendations
    st.markdown("""
    ### 💡 Retention стратегии по типам промо:
    
    **🎫 Скидки на поездки**:
    • Плюсы: Простота, прямое снижение cost of service
    • Минусы: Временный эффект, может снизить perceived value
    • Лучше для: High-risk сегмента как экстренная мера
    
    **💰 Cashback программа**:
    • Плюсы: Создает лояльность, стимулирует частоту
    • Минусы: Сложность в учете, может создать gaming behavior
    • Лучше для: Medium-risk пользователей
    
    **⭐ Loyalty points**:
    • Плюсы: Долгосрочная привязка, возможность partner rewards
    • Минусы: Сложность в управлении, operational overhead
    • Лучше для: Low-risk пользователей для профилактики
    
    **👑 Premium features**:
    • Плюсы: Увеличивает perceived value, может увеличить frequency
    • Минусы: Требует product development, может создать entitlement
    • Лучше для: High-value пользователей всех сегментов
    """)

def competitive_defense_promo():
    """Конкурентная защита через промокоды"""
    st.subheader("🆚 Конкурентная защита")
    
    st.warning("""
    **Ситуация**: Конкурент запускает агрессивную кампанию по переманиванию ваших пользователей.
    Нужна быстрая defensive стратегия для защиты user base.
    """)
    
    # Threat assessment
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**⚠️ Оценка угрозы**")
        
        competitor_discount = st.slider("Скидка конкурента (%)", 30, 80, 50)
        threat_duration = st.slider("Ожидаемая длительность атаки (недели)", 2, 12, 6)
        at_risk_users = st.number_input("Пользователей под угрозой", 10000, 200000, 75000)
        
        # Historical churn data
        organic_churn = st.slider("Органический месячный churn (%)", 8, 20, 12)
        
    with col2:
        st.markdown("**🛡️ Defensive стратегия**")
        
        defense_strategy = st.selectbox("Тип защиты:", 
                                      ["Matching (аналогичная скидка)", "Premium positioning", 
                                       "Loyalty surge", "Targeted retention"])
        
        defense_budget = st.number_input("Бюджет на защиту", 1000000, 20000000, 5000000)
        
        # Response timing
        response_speed = st.selectbox("Скорость реакции:", 
                                    ["Immediate (в течение дня)", "Fast (в течение недели)", "Measured (2-3 недели)"])
    
    # Modeling competitive threat
    base_weekly_churn = organic_churn / 4  # Базовый недельный churn
    
    # Threat multiplier based on competitor offer
    threat_multiplier = 1 + (competitor_discount / 50)  # Каждые 50% скидки = 2x threat
    
    # Time decay of competitive effect
    weeks = list(range(1, threat_duration + 1))
    competitive_churn_rates = []
    
    for week in weeks:
        # Эффект конкурента затухает со временем
        decay_factor = np.exp(-week / 4)  # Exponential decay
        weekly_threat = base_weekly_churn * threat_multiplier * decay_factor
        competitive_churn_rates.append(weekly_threat)
    
    # Users lost without defense
    users_lost_without_defense = []
    remaining_users = at_risk_users
    
    for weekly_churn in competitive_churn_rates:
        lost_this_week = remaining_users * (weekly_churn / 100)
        users_lost_without_defense.append(lost_this_week)
        remaining_users -= lost_this_week
    
    total_lost_without_defense = sum(users_lost_without_defense)
    
    # Defense effectiveness
    defense_effectiveness = {
        "Matching (аналогичная скидка)": 70,  # % снижения потерь
        "Premium positioning": 40,
        "Loyalty surge": 55,
        "Targeted retention": 65
    }
    
    response_delay_penalty = {
        "Immediate (в течение дня)": 1.0,
        "Fast (в течение недели)": 0.8,
        "Measured (2-3 недели)": 0.6
    }
    
    effectiveness = defense_effectiveness[defense_strategy] * response_delay_penalty[response_speed]
    users_saved = total_lost_without_defense * (effectiveness / 100)
    
    # Cost analysis
    if defense_strategy == "Matching (аналогичная скидка)":
        cost_per_user = competitor_discount / 100 * 350 * 3  # 3 поездки с защитной скидкой
    elif defense_strategy == "Premium positioning":
        cost_per_user = 200  # Маркетинг премиум позиционирования
    elif defense_strategy == "Loyalty surge":
        cost_per_user = 120  # Loyalty бонусы
    else:  # Targeted retention
        cost_per_user = 150  # Персонализированные retention offers
    
    total_defense_cost = at_risk_users * cost_per_user
    
    # LTV impact
    avg_ltv_at_risk = 4500  # LTV пользователей под угрозой
    ltv_saved = users_saved * avg_ltv_at_risk
    defense_roi = (ltv_saved - total_defense_cost) / total_defense_cost * 100
    
    # Results
    st.subheader("⚔️ Результаты защитной кампании")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Потери без защиты", f"{total_lost_without_defense:,.0f}")
    
    with col2:
        st.metric("Сохраненных пользователей", f"{users_saved:,.0f}")
    
    with col3:
        st.metric("Затраты на защиту", f"{total_defense_cost:,.0f} руб")
    
    with col4:
        color = "success" if defense_roi > 100 else "warning" if defense_roi > 0 else "error"
        st.markdown(f"""
        <div class="{color}-card">
            <h4>ROI защиты</h4>
            <h2>{defense_roi:.0f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Timeline visualization
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=weeks,
        y=users_lost_without_defense,
        mode='lines+markers',
        name='Потери без защиты',
        line=dict(color='red', width=3)
    ))
    
    users_lost_with_defense = [loss * (1 - effectiveness/100) for loss in users_lost_without_defense]
    fig.add_trace(go.Scatter(
        x=weeks,
        y=users_lost_with_defense,
        mode='lines+markers',
        name='Потери с защитой',
        line=dict(color='green', width=3)
    ))
    
    fig.update_layout(
        title="Временная динамика конкурентной угрозы",
        xaxis_title="Неделя",
        yaxis_title="Потеря пользователей",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Strategic recommendations
    if defense_roi > 200:
        st.success("🛡️ **Defensive кампания высокоэффективна** - рекомендуется к реализации")
    elif defense_roi > 50:
        st.info("📊 **Умеренная эффективность** - рассмотреть альтернативные стратегии")
    else:
        st.warning("⚠️ **Низкая эффективность** - возможно, лучше принять потери и сфокусироваться на привлечении")
    
    st.markdown(f"""
    ### 🎯 Стратегические рекомендации для "{defense_strategy}":
    """)
    
    strategy_recommendations = {
        "Matching (аналогичная скидка)": [
            "Быстрая реакция критична - каждый день промедления = +10% потерь",
            "Коммуницировать 'мы всегда предлагаем лучшие цены'",
            "Подготовить exit strategy когда конкурент прекратит кампанию",
            "Избегать race to the bottom - установить минимальные границы"
        ],
        "Premium positioning": [
            "Акцент на quality, safety, reliability vs цену",
            "Testimonials и case studies довольных клиентов",
            "Premium features как differentiator",
            "Меньше direct mentions конкурента"
        ],
        "Loyalty surge": [
            "Reward existing loyalty вместо привлечения новых",
            "Exclusive perks для долгосрочных пользователей",
            "Community building и insider access",
            "Gradual rollout для maximum impact"
        ],
        "Targeted retention": [
            "Персонализированные offers на основе usage patterns",
            "Proactive outreach к high-value пользователям",
            "Address specific pain points каждого сегмента",
            "Measure effectiveness по сегментам"
        ]
    }
    
    for rec in strategy_recommendations[defense_strategy]:
        st.write(f"• {rec}")

def segmented_promo_optimization():
    """Сегментированные промокоды"""
    st.subheader("🎯 Сегментированные промокампании")
    
    st.success("""
    **Персонализация промо**: Вместо one-size-fits-all подхода, создаем targeted offers 
    для разных сегментов пользователей на основе их поведения и характеристик.
    """)
    
    # Segmentation criteria
    segmentation_approach = st.selectbox(
        "Принцип сегментации:",
        ["Behavioral (частота поездок)", "Geographic (районы города)", 
         "Temporal (время использования)", "Value-based (потрачено денег)"]
    )
    
    if segmentation_approach == "Behavioral (частота поездок)":
        behavioral_segmentation()
    elif segmentation_approach == "Geographic (районы города)":
        geographic_segmentation()
    elif segmentation_approach == "Temporal (время использования)":
        temporal_segmentation()
    elif segmentation_approach == "Value-based (потрачено денег)":
        value_based_segmentation()

def behavioral_segmentation():
    """Сегментация по поведению"""
    st.markdown("### 📊 Поведенческая сегментация")
    
    # Определение сегментов
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**👥 Сегменты пользователей**")
        
        power_users = st.number_input("Power users (8+ поездок/мес)", 5000, 100000, 25000)
        regular_users = st.number_input("Regular users (3-7 поездок/мес)", 20000, 300000, 85000)
        occasional_users = st.number_input("Occasional users (1-2 поездки/мес)", 50000, 500000, 150000)
        
    with col2:
        st.markdown("**🎯 Промо по сегментам**")
        
        power_promo = st.slider("Power users скидка (%)", 0, 30, 10)
        regular_promo = st.slider("Regular users скидка (%)", 15, 50, 25)
        occasional_promo = st.slider("Occasional users скидка (%)", 30, 70, 45)
    
    # Behavioral insights для каждого сегмента
    segments_data = {
        'Power Users': {
            'count': power_users,
            'avg_frequency': 12,
            'avg_aov': 380,
            'churn_risk': 'Low',
            'promo_sensitivity': 'Low',
            'promo_discount': power_promo,
            'strategy': 'Loyalty & Premium'
        },
        'Regular Users': {
            'count': regular_users,
            'avg_frequency': 5,
            'avg_aov': 350,
            'churn_risk': 'Medium',
            'promo_sensitivity': 'Medium',
            'promo_discount': regular_promo,
            'strategy': 'Frequency increase'
        },
        'Occasional Users': {
            'count': occasional_users,
            'avg_frequency': 1.5,
            'avg_aov': 320,
            'churn_risk': 'High',
            'promo_sensitivity': 'High',
            'promo_discount': occasional_promo,
            'strategy': 'Activation & Habit'
        }
    }
    
    # Расчет эффективности по сегментам
    total_campaign_cost = 0
    total_incremental_revenue = 0
    
    results_data = []
    
    for segment, data in segments_data.items():
        # Baseline revenue без промо
        baseline_revenue = data['count'] * data['avg_frequency'] * data['avg_aov'] * 0.25
        
        # Эффект промо на frequency (обратная зависимость от baseline frequency)
        frequency_lift = (data['promo_discount'] / 100) * (10 / data['avg_frequency'])  # Higher discount + lower baseline = higher lift
        new_frequency = data['avg_frequency'] * (1 + frequency_lift)
        
        # Промо стоимость
        promo_cost_per_ride = data['avg_aov'] * (data['promo_discount'] / 100)
        total_promo_rides = data['count'] * new_frequency
        segment_promo_cost = total_promo_rides * promo_cost_per_ride
        
        # Новая выручка
        new_revenue = data['count'] * new_frequency * data['avg_aov'] * 0.25
        incremental_revenue = new_revenue - baseline_revenue
        
        # ROI сегмента
        segment_roi = (incremental_revenue - segment_promo_cost) / segment_promo_cost * 100 if segment_promo_cost > 0 else 0
        
        results_data.append({
            'Сегмент': segment,
            'Пользователей': f"{data['count']:,}",
            'Baseline частота': f"{data['avg_frequency']:.1f}",
            'Новая частота': f"{new_frequency:.1f}",
            'Скидка': f"{data['promo_discount']}%",
            'Затраты на промо': f"{segment_promo_cost:,.0f}",
            'Доп. выручка': f"{incremental_revenue:,.0f}",
            'ROI': f"{segment_roi:.0f}%"
        })
        
        total_campaign_cost += segment_promo_cost
        total_incremental_revenue += incremental_revenue
    
    # Результаты
    st.subheader("📈 Результаты сегментированной кампании")
    
    results_df = pd.DataFrame(results_data)
    st.dataframe(results_df, use_container_width=True)
    
    # Общий ROI
    overall_roi = (total_incremental_revenue - total_campaign_cost) / total_campaign_cost * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Общие затраты", f"{total_campaign_cost:,.0f} руб")
    
    with col2:
        st.metric("Доп. выручка", f"{total_incremental_revenue:,.0f} руб")
    
    with col3:
        color = "success" if overall_roi > 100 else "warning" if overall_roi > 0 else "error"
        st.markdown(f"""
        <div class="{color}-card">
            <h4>Общий ROI</h4>
            <h2>{overall_roi:.0f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Insights по сегментам
    st.markdown("""
    ### 💡 Инсайты поведенческой сегментации:
    
    **🚀 Power Users**:
    • Низкая чувствительность к скидкам - фокус на exclusive perks
    • Высокая frequency уже достигнута - сложно увеличить
    • Лучший сегмент для premium services и loyalty программ
    
    **⚖️ Regular Users**:
    • Оптимальный баланс volume vs sensitivity
    • Потенциал для growth в power users при правильном nudging
    • Средние скидки могут стимулировать frequency
    
    **📈 Occasional Users**:
    • Высокий потенциал роста, но нужны большие стимулы
    • Риск привлечения только discount-hunting behavior
    • Фокус на habit formation, а не только на deals
    """)

def geographic_segmentation():
    """Географическая сегментация"""
    st.markdown("### 🗺️ Географическая сегментация")
    
    st.info("""
    **Географическая специфика**: Разные районы города имеют разную плотность спроса,
    покупательную способность и конкуренцию с общественным транспортом.
    """)
    
    # Зоны города
    zones_data = {
        'Центр': {
            'population': 500000,
            'avg_income': 80000,
            'competition': 9,
            'public_transport': 8,
            'current_penetration': 15
        },
        'Бизнес-районы': {
            'population': 300000,
            'avg_income': 120000,
            'competition': 7,
            'public_transport': 7,
            'current_penetration': 25
        },
        'Спальные районы': {
            'population': 800000,
            'avg_income': 50000,
            'competition': 4,
            'public_transport': 5,
            'current_penetration': 8
        },
        'Пригороды': {
            'population': 400000,
            'avg_income': 45000,
            'competition': 2,
            'public_transport': 3,
            'current_penetration': 12
        }
    }
    
    # Расчет потенциала и стратегии по зонам
    for zone, data in zones_data.items():
        # Потенциал роста
        market_potential = data['population'] * 0.2  # 20% максимальная penetration
        growth_potential = market_potential - (data['population'] * data['current_penetration'] / 100)
        
        # Стратегия промо на основе характеристик зоны
        if data['avg_income'] > 80000 and data['competition'] > 6:
            promo_strategy = "Premium positioning, небольшие скидки"
            recommended_discount = 15
        elif data['public_transport'] < 5:
            promo_strategy = "Convenience focus, средние скидки"
            recommended_discount = 25
        elif data['current_penetration'] < 10:
            promo_strategy = "Market education, высокие скидки"
            recommended_discount = 40
        else:
            promo_strategy = "Balanced approach"
            recommended_discount = 30
        
        zones_data[zone].update({
            'growth_potential': growth_potential,
            'promo_strategy': promo_strategy,
            'recommended_discount': recommended_discount
        })
    
    # Визуализация
    col1, col2 = st.columns(2)
    
    with col1:
        # Таблица по зонам
        zones_df = pd.DataFrame([
            {
                'Зона': zone,
                'Население': f"{data['population']:,}",
                'Средний доход': f"{data['avg_income']:,}",
                'Текущая penetration': f"{data['current_penetration']}%",
                'Потенциал роста': f"{data['growth_potential']:,.0f}",
                'Рекомендуемая скидка': f"{data['recommended_discount']}%"
            }
            for zone, data in zones_data.items()
        ])
        st.dataframe(zones_df, use_container_width=True)
    
    with col2:
        # График потенциала vs текущей penetration
        fig = go.Figure()
        
        zones = list(zones_data.keys())
        current_users = [zones_data[z]['population'] * zones_data[z]['current_penetration'] / 100 for z in zones]
        potential_users = [zones_data[z]['growth_potential'] for z in zones]
        
        fig.add_trace(go.Bar(
            x=zones,
            y=current_users,
            name='Текущие пользователи',
            marker_color='blue'
        ))
        
        fig.add_trace(go.Bar(
            x=zones,
            y=potential_users,
            name='Потенциал роста',
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title="Текущие пользователи vs потенциал роста",
            barmode='stack',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Стратегические рекомендации
    st.markdown("""
    ### 🎯 Географические стратегии:
    
    **🏢 Центр города**:
    • Высокая конкуренция → фокус на differentiation
    • Хороший общ.транспорт → позиционирование как time-saver
    • Высокие доходы → меньшая price sensitivity
    
    **💼 Бизнес-районы**:
    • B2B partnerships с компаниями
    • Rush hour surge pricing acceptance
    • Corporate accounts и bulk payments
    
    **🏠 Спальные районы**:
    • Price-sensitive segment → высокие промо
    • Слабый общ.транспорт → удобство как value prop
    • Family accounts и shared rides
    
    **🌳 Пригороды**:
    • Last mile connectivity с транспортными узлами
    • Scheduled rides для commuting
    • Lower competition → focus на market education
    """)

def temporal_segmentation():
    """Временная сегментация"""
    st.markdown("### ⏰ Временная сегментация")
    
    st.success("""
    **Time-based промо**: Разное время использования = разные потребности и готовность платить.
    Surge pricing vs off-peak discounts.
    """)
    
    # Временные сегменты
    time_segments = {
        'Rush hour (7-9, 17-19)': {
            'demand_level': 'High',
            'price_sensitivity': 'Low',
            'current_surge': 1.8,
            'recommended_strategy': 'Premium pricing, minimal discounts'
        },
        'Business hours (9-17)': {
            'demand_level': 'Medium',
            'price_sensitivity': 'Medium', 
            'current_surge': 1.2,
            'recommended_strategy': 'Moderate promotions for B2B'
        },
        'Evening leisure (19-23)': {
            'demand_level': 'Medium-High',
            'price_sensitivity': 'Medium',
            'current_surge': 1.4,
            'recommended_strategy': 'Entertainment partnerships'
        },
        'Night hours (23-6)': {
            'demand_level': 'Low',
            'price_sensitivity': 'Low',
            'current_surge': 1.6,
            'recommended_strategy': 'Safety premium, night differential'
        },
        'Weekend days': {
            'demand_level': 'Medium',
            'price_sensitivity': 'High',
            'current_surge': 1.1,
            'recommended_strategy': 'Leisure promotions, family discounts'
        },
        'Off-peak (10-16)': {
            'demand_level': 'Low',
            'price_sensitivity': 'High',
            'current_surge': 0.9,
            'recommended_strategy': 'Aggressive promotions for demand stimulation'
        }
    }
    
    # Выбор стратегии
    selected_segment = st.selectbox("Выберите временной сегмент:", list(time_segments.keys()))
    
    segment_data = time_segments[selected_segment]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**📊 Характеристики: {selected_segment}**")
        st.write(f"• Уровень спроса: {segment_data['demand_level']}")
        st.write(f"• Price sensitivity: {segment_data['price_sensitivity']}")
        st.write(f"• Текущий surge: {segment_data['current_surge']}x")
        st.write(f"• Стратегия: {segment_data['recommended_strategy']}")
        
    with col2:
        st.markdown("**⚙️ Промо параметры**")
        
        promo_type = st.selectbox("Тип промо:", 
                                ["Скидка от базовой цены", "Фиксированная цена", 
                                 "Cashback", "Bundle offers"])
        
        if segment_data['price_sensitivity'] == 'High':
            default_discount = 35
        elif segment_data['price_sensitivity'] == 'Medium':
            default_discount = 20
        else:
            default_discount = 10
            
        promo_size = st.slider("Размер промо (%)", 5, 50, default_discount)
    
    # Simulation промо эффекта
    base_demand = 10000  # Базовый спрос в сегменте
    base_aov = 350
    
    # Demand elasticity к промо
    elasticity_map = {'High': 2.5, 'Medium': 1.5, 'Low': 0.8}
    elasticity = elasticity_map[segment_data['price_sensitivity']]
    
    # Новый спрос после промо
    demand_lift = (promo_size / 100) * elasticity
    new_demand = base_demand * (1 + demand_lift)
    
    # Revenue impact
    new_aov = base_aov * (1 - promo_size / 100) if promo_type == "Скидка от базовой цены" else base_aov
    
    base_revenue = base_demand * base_aov * 0.25
    new_revenue = new_demand * new_aov * 0.25
    promo_cost = new_demand * base_aov * (promo_size / 100)
    net_revenue = new_revenue - promo_cost
    
    # Results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Рост спроса", f"{new_demand:,.0f}", f"+{demand_lift:.1%}")
    
    with col2:
        st.metric("Выручка с промо", f"{new_revenue:,.0f} руб", 
                 f"{((new_revenue - base_revenue) / base_revenue * 100):+.1f}%")
    
    with col3:
        st.metric("Чистая выручка", f"{net_revenue:,.0f} руб",
                 f"{((net_revenue - base_revenue) / base_revenue * 100):+.1f}%")
    
    # Визуализация по всем временным сегментам
    st.subheader("📊 Сравнение всех временных сегментов")
    
    all_segments_data = []
    for segment, data in time_segments.items():
        elasticity = elasticity_map[data['price_sensitivity']]
        optimal_discount = 30 if data['price_sensitivity'] == 'High' else 20 if data['price_sensitivity'] == 'Medium' else 10
        
        demand_lift = (optimal_discount / 100) * elasticity
        revenue_lift = demand_lift * (1 - optimal_discount / 100)  # Упрощенный расчет
        
        all_segments_data.append({
            'Сегмент': segment,
            'Спрос': data['demand_level'],
            'Price Sensitivity': data['price_sensitivity'],
            'Surge': f"{data['current_surge']}x",
            'Оптимальная скидка': f"{optimal_discount}%",
            'Ожидаемый лифт': f"{revenue_lift:.1%}"
        })
    
    segments_df = pd.DataFrame(all_segments_data)
    st.dataframe(segments_df, use_container_width=True)

def value_based_segmentation():
    """Сегментация по потраченной сумме"""
    st.markdown("### 💎 Value-based сегментация")
    
    st.info("""
    **RFM подход для ride-hailing**: Recency (последняя поездка), Frequency (количество поездок), 
    Monetary (потраченная сумма). Разные value segments требуют разного подхода к промо.
    """)
    
    # RFM сегменты
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**💰 Value сегменты**")
        
        vip_users = st.number_input("VIP (>10k руб/мес)", 1000, 50000, 8000)
        high_value = st.number_input("High value (5-10k руб/мес)", 5000, 100000, 25000)
        medium_value = st.number_input("Medium value (2-5k руб/мес)", 20000, 200000, 75000)
        low_value = st.number_input("Low value (<2k руб/мес)", 50000, 500000, 150000)
        
    with col2:
        st.markdown("**🎯 Промо стратегии**")
        
        vip_strategy = st.selectbox("VIP стратегия:", 
                                  ["Exclusive perks", "Concierge service", "Priority support", "No promotions needed"])
        
        high_value_strategy = st.selectbox("High value стратегия:",
                                         ["Loyalty rewards", "Upgrade incentives", "Volume discounts"])
        
        medium_value_strategy = st.selectbox("Medium value стратегия:",
                                           ["Frequency bonuses", "Referral rewards", "Modest discounts"])
        
        low_value_strategy = st.selectbox("Low value стратегия:",
                                        ["Activation campaigns", "High discounts", "Habit formation"])
    
    # Расчет ROI для каждого сегмента
    value_segments = {
        'VIP': {
            'count': vip_users,
            'avg_monthly_spend': 12000,
            'frequency': 15,
            'churn_risk': 5,
            'promo_budget_per_user': 200 if vip_strategy != "No promotions needed" else 0
        },
        'High Value': {
            'count': high_value,
            'avg_monthly_spend': 7500,
            'frequency': 9,
            'churn_risk': 8,
            'promo_budget_per_user': 150
        },
        'Medium Value': {
            'count': medium_value,
            'avg_monthly_spend': 3500,
            'frequency': 5,
            'churn_risk': 12,
            'promo_budget_per_user': 80
        },
        'Low Value': {
            'count': low_value,
            'avg_monthly_spend': 1200,
            'frequency': 2,
            'churn_risk': 20,
            'promo_budget_per_user': 120
        }
    }
    
    # Анализ эффективности промо по сегментам
    total_promo_budget = 0
    total_incremental_revenue = 0
    
    segment_results = []
    
    for segment, data in value_segments.items():
        # Базовая выручка (take rate 25%)
        base_monthly_revenue = data['count'] * data['avg_monthly_spend'] * 0.25
        
        # Эффект промо зависит от сегмента
        if segment == 'VIP':
            revenue_lift = 0.05  # VIP мало реагируют на промо, но ценят attention
        elif segment == 'High Value':
            revenue_lift = 0.15  # Умеренная реакция
        elif segment == 'Medium Value':
            revenue_lift = 0.25  # Хорошая реакция
        else:  # Low Value
            revenue_lift = 0.40  # Высокая реакция на промо
        
        incremental_revenue = base_monthly_revenue * revenue_lift
        promo_cost = data['count'] * data['promo_budget_per_user']
        
        segment_roi = (incremental_revenue - promo_cost) / promo_cost * 100 if promo_cost > 0 else 0
        
        segment_results.append({
            'Сегмент': segment,
            'Пользователей': f"{data['count']:,}",
            'Средний spend': f"{data['avg_monthly_spend']:,} руб",
            'Частота': f"{data['frequency']} поездок",
            'Churn risk': f"{data['churn_risk']}%",
            'Промо бюджет': f"{promo_cost:,.0f} руб",
            'Доп. выручка': f"{incremental_revenue:,.0f} руб",
            'ROI': f"{segment_roi:.0f}%"
        })
        
        total_promo_budget += promo_cost
        total_incremental_revenue += incremental_revenue
    
    # Результаты
    st.subheader("📈 ROI по value сегментам")
    
    results_df = pd.DataFrame(segment_results)
    st.dataframe(results_df, use_container_width=True)
    
    # Общий ROI и рекомендации
    overall_roi = (total_incremental_revenue - total_promo_budget) / total_promo_budget * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Общий промо бюджет", f"{total_promo_budget:,.0f} руб")
    
    with col2:
        st.metric("Дополнительная выручка", f"{total_incremental_revenue:,.0f} руб")
    
    with col3:
        color = "success" if overall_roi > 150 else "warning" if overall_roi > 75 else "error"
        st.markdown(f"""
        <div class="{color}-card">
            <h4>Общий ROI</h4>
            <h2>{overall_roi:.0f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Value-based инсайты
    st.markdown("""
    ### 💡 Value-based промо инсайты:
    
    **💎 VIP сегмент**:
    • Промо могут обесценить brand perception
    • Фокус на exclusive access и premium service
    • Personal relationship management важнее скидок
    
    **💰 High Value**:
    • Loyalty программы с accumulated benefits
    • Early access к новым features
    • Volume-based rewards
    
    **⚖️ Medium Value**:
    • Оптимальный сегмент для most промо кампаний
    • Potential для upgrade в high value при правильном nurturing
    • Referral программы work well
    
    **📈 Low Value**:
    • Высокий потенциал роста при правильном подходе
    • Risk привлечения только deal-seekers
    • Focus на habit formation over pure discounting
    """)

def expansion_strategy():
    """Стратегия экспансии"""
    st.header("🚀 Стратегия географической экспансии")
    
    st.markdown("""
    **Expansion в ride-hailing**: не просто копирование модели, а адаптация под локальные условия.
    Успех зависит от выбора города, timing'а входа и локализации value proposition.
    """)
    
    expansion_type = st.selectbox(
        "Тип экспансии:",
        [
            "🏙️ Новый город в том же регионе",
            "🌍 Новый регион/страна", 
            "🏘️ Малые города (Tier 2/3)",
            "🚁 Vertical expansion (грузоперевозки, доставка)"
        ]
    )
    
    if expansion_type == "🏙️ Новый город в том же регионе":
        regional_city_expansion()
    elif expansion_type == "🌍 Новый регион/страна":
        international_expansion()
    elif expansion_type == "🏘️ Малые города (Tier 2/3)":
        small_cities_expansion()
    elif expansion_type == "🚁 Vertical expansion (грузоперевозки, доставка)":
        vertical_expansion()

def regional_city_expansion():
    """Экспансия в региональный город"""
    st.subheader("🏙️ Expansion в региональный город")
    
    # Анализ целевого города
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎯 Характеристики города**")
        
        target_city = st.text_input("Название города", "Новосибирск")
        population = st.number_input("Население", 500000, 3000000, 1600000)
        avg_income = st.number_input("Средний доход (руб)", 35000, 100000, 55000)
        existing_competitors = st.slider("Конкурентов на рынке", 0, 5, 2)
        transport_quality = st.slider("Качество общ.транспорта (1-10)", 1, 10, 6)
        
    with col2:
        st.markdown("**📊 Текущее присутствие**")
        
        current_cities = st.number_input("Городов в портфеле", 1, 20, 3)
        operational_experience = st.slider("Опыт работы (лет)", 1, 10, 4)
        brand_recognition = st.slider("Узнаваемость бренда в регионе (%)", 10, 80, 35)
        
        # Ресурсы для экспансии
        expansion_budget = st.number_input("Бюджет на запуск (млн руб)", 5, 200, 50)
        timeline = st.slider("Timeline до breakeven (месяцев)", 6, 36, 18)
    
    # Market sizing
    addressable_market = population * 0.15  # 15% penetration potential в региональном городе
    income_adjustment = min(1.2, avg_income / 60000)  # Adjustment для покупательной способности
    adjusted_market = addressable_market * income_adjustment
    
    # Competitive landscape
    market_share_potential = max(0.15, 0.5 / (existing_competitors + 1))  # С учетом конкуренции
    target_users_year_1 = adjusted_market * market_share_potential
    
    # Financial projections
    estimated_aov = 200 + (avg_income - 35000) / 500  # Зависимость от доходов
    estimated_frequency = 2.5 + (avg_income - 35000) / 25000  # Больше доходы = больше поездок
    
    monthly_revenue_potential = target_users_year_1 * estimated_frequency * estimated_aov * 0.25 / 12
    
    # Costs
    launch_costs = {
        'Маркетинг и промо': expansion_budget * 0.4,
        'Операционная инфраструктура': expansion_budget * 0.3,
        'Regulatory и legal': expansion_budget * 0.1,
        'Local team': expansion_budget * 0.15,
        'Резерв': expansion_budget * 0.05
    }
    
    monthly_operational_costs = target_users_year_1 * 25 / 12  # 25 руб на пользователя в месяц
    
    # Результаты анализа
    st.subheader(f"📊 Анализ экспансии в {target_city}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Потенциал рынка", f"{adjusted_market:,.0f}")
    
    with col2:
        st.metric("Целевые пользователи (год 1)", f"{target_users_year_1:,.0f}")
    
    with col3:
        st.metric("Месячная выручка (зрелость)", f"{monthly_revenue_potential:,.0f} руб")
    
    with col4:
        payback_months = expansion_budget * 1000000 / (monthly_revenue_potential - monthly_operational_costs)
        st.metric("Прогноз окупаемости", f"{payback_months:.1f} мес")
    
    # Breakdown costs
    st.subheader("💰 Структура инвестиций")
    
    costs_df = pd.DataFrame([
        {'Категория': category, 'Сумма': f"{cost:,.0f} млн руб", 'Доля': f"{cost/expansion_budget:.1%}"}
        for category, cost in launch_costs.items()
    ])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(costs_df, use_container_width=True)
    
    with col2:
        fig = go.Figure(data=[go.Pie(
            labels=list(launch_costs.keys()),
            values=list(launch_costs.values()),
            hole=0.3
        )])
        fig.update_layout(title="Распределение инвестиций", height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Risk assessment
    st.subheader("⚠️ Оценка рисков")
    
    risk_factors = []
    risk_score = 0
    
    if existing_competitors >= 3:
        risk_factors.append("🔴 Высокая конкуренция")
        risk_score += 3
    elif existing_competitors >= 1:
        risk_factors.append("🟡 Умеренная конкуренция")
        risk_score += 1
    
    if avg_income < 45000:
        risk_factors.append("🔴 Низкая покупательная способность")
        risk_score += 3
    elif avg_income < 60000:
        risk_factors.append("🟡 Ограниченная покупательная способность")
        risk_score += 1
    
    if transport_quality > 7:
        risk_factors.append("🟡 Сильный общественный транспорт")
        risk_score += 2
    
    if brand_recognition < 25:
        risk_factors.append("🟡 Низкая узнаваемость бренда")
        risk_score += 1
    
    if population < 800000:
        risk_factors.append("🟡 Ограниченный размер рынка")
        risk_score += 1
    
    # Интерпретация рисков
    if risk_score <= 3:
        st.success("🟢 **Низкий риск** - благоприятные условия для экспансии")
        recommendation = "Рекомендуется к запуску"
    elif risk_score <= 6:
        st.warning("🟡 **Умеренный риск** - требуется детальное планирование")
        recommendation = "Рекомендуется с осторожностью"
    else:
        st.error("🔴 **Высокий риск** - требуется пересмотр стратегии")
        recommendation = "Не рекомендуется без значительных изменений"
    
    for risk in risk_factors:
        st.write(f"• {risk}")
    
    st.info(f"**Общая рекомендация**: {recommendation}")
    
    # Success factors
    st.subheader("🎯 Ключевые факторы успеха")
    
    success_factors = [
        "**Local partnerships**: Договоренности с местными таксопарками",
        "**Regulatory compliance**: Работа с местными властями заранее",
        "**Localized marketing**: Адаптация под местные особенности",
        "**Supply-side focus**: Быстрое привлечение водителей",
        "**Gradual rollout**: Поэтапный запуск по районам",
        "**Price positioning**: Правильное позиционирование относительно местных цен"
    ]
    
    for factor in success_factors:
        st.write(f"• {factor}")

def international_expansion():
    """Международная экспансия"""
    st.subheader("🌍 Международная экспансия")
    
    st.warning("""
    **International expansion**: самый сложный тип экспансии. Требует понимания локального
    регулирования, культуры, конкуренции и адаптации бизнес-модели.

"""
    st.warning("""
    **International expansion**: самый сложный тип экспансии. Требует понимания локального
    регулирования, культуры, конкуренции и адаптации бизнес-модели.
    """)
    
    # Выбор целевой страны/региона
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🌍 Целевой рынок**")
        
        target_country = st.selectbox("Целевая страна:", 
                                    ["Казахстан", "Беларусь", "Узбекистан", 
                                     "Грузия", "Армения", "Другая"])
        
        market_maturity = st.selectbox("Зрелость рынка:", 
                                     ["Emerging (нет ride-hailing)", 
                                      "Early stage (есть 1-2 игрока)",
                                      "Competitive (3+ игроков)"])
        
        regulatory_risk = st.slider("Регуляторный риск (1-10)", 1, 10, 5)
        cultural_distance = st.slider("Культурная дистанция (1-10)", 1, 10, 3)
        
    with col2:
        st.markdown("**💰 Инвестиционные параметры**")
        
        market_size_usd = st.number_input("Размер рынка (млн USD)", 10, 1000, 150)
        investment_budget_usd = st.number_input("Инвестиционный бюджет (млн USD)", 5, 200, 25)
        local_partnership = st.checkbox("Локальное партнерство", True)
        
        # Mode входа
        entry_mode = st.selectbox("Режим входа:",
                                ["Organic expansion", "Acquisition", 
                                 "Joint venture", "Franchise"])
    
    # Risk scoring
    risk_factors = {}
    total_risk_score = 0
    
    # Regulatory risk
    if regulatory_risk >= 8:
        risk_factors["Regulatory"] = {"score": 3, "desc": "Высокий регуляторный риск"}
        total_risk_score += 3
    elif regulatory_risk >= 5:
        risk_factors["Regulatory"] = {"score": 2, "desc": "Умеренный регуляторный риск"}
        total_risk_score += 2
    else:
        risk_factors["Regulatory"] = {"score": 1, "desc": "Низкий регуляторный риск"}
        total_risk_score += 1
    
    # Market competition
    competition_scores = {"Emerging": 1, "Early stage": 2, "Competitive": 4}
    comp_score = competition_scores[market_maturity.split(" ")[0]]
    risk_factors["Competition"] = {"score": comp_score, "desc": f"Конкуренция: {market_maturity}"}
    total_risk_score += comp_score
    
    # Cultural risk
    if cultural_distance >= 7:
        risk_factors["Cultural"] = {"score": 3, "desc": "Высокие культурные барьеры"}
        total_risk_score += 3
    elif cultural_distance >= 4:
        risk_factors["Cultural"] = {"score": 2, "desc": "Умеренные культурные барьеры"}
        total_risk_score += 2
    else:
        risk_factors["Cultural"] = {"score": 1, "desc": "Низкие культурные барьеры"}
        total_risk_score += 1
    
    # Investment requirements по entry mode
    investment_multipliers = {
        "Organic expansion": 1.0,
        "Acquisition": 2.5,
        "Joint venture": 1.3,
        "Franchise": 0.6
    }
    
    required_investment = investment_budget_usd * investment_multipliers[entry_mode]
    
    # Timeline to profitability
    base_timeline = 24  # месяцев
    timeline_adjustments = {
        "Emerging": -6,  # Быстрее в новых рынках
        "Early stage": 0,
        "Competitive": +12  # Дольше при высокой конкуренции
    }
    
    risk_timeline_penalty = (total_risk_score - 5) * 2  # Каждый пункт риска = +2 месяца
    estimated_timeline = base_timeline + timeline_adjustments[market_maturity.split(" ")[0]] + risk_timeline_penalty
    
    if local_partnership:
        estimated_timeline -= 6  # Партнерство ускоряет
        required_investment *= 0.8  # И снижает расходы
    
    # Results
    st.subheader("📊 Анализ международной экспансии")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        risk_color = "error" if total_risk_score >= 9 else "warning" if total_risk_score >= 6 else "success"
        st.markdown(f"""
        <div class="{risk_color}-card">
            <h4>Общий риск</h4>
            <h2>{total_risk_score}/12</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Требуется инвестиций", f"${required_investment:.1f}M")
    
    with col3:
        st.metric("Timeline до прибыльности", f"{estimated_timeline} мес")
    
    with col4:
        market_attractiveness = market_size_usd / required_investment
        st.metric("Market attractiveness", f"{market_attractiveness:.1f}x")
    
    # Risk breakdown
    st.subheader("⚠️ Детализация рисков")
    
    risk_df = pd.DataFrame([
        {"Категория риска": category, "Балл": data["score"], "Описание": data["desc"]}
        for category, data in risk_factors.items()
    ])
    st.dataframe(risk_df, use_container_width=True)
    
    # Entry mode analysis
    st.subheader(f"🎯 Анализ стратегии '{entry_mode}'")
    
    entry_analysis = {
        "Organic expansion": {
            "pros": ["Полный контроль", "Низкие изначальные инвестиции", "Сохранение brand identity"],
            "cons": ["Медленное проникновение", "Высокие regulatory риски", "Отсутствие local expertise"],
            "best_for": "Зрелые рынки с низкими барьерами"
        },
        "Acquisition": {
            "pros": ["Быстрый market entry", "Готовая клиентская база", "Local expertise"],
            "cons": ["Высокие инвестиции", "Integration challenges", "Cultural misalignment"],
            "best_for": "Конкурентные рынки с качественными targets"
        },
        "Joint venture": {
            "pros": ["Разделение рисков", "Local partnerships", "Regulatory support"],
            "cons": ["Ограниченный контроль", "Потенциальные конфликты", "Sharing profits"],
            "best_for": "Высокорисковые рынки с strong local players"
        },
        "Franchise": {
            "pros": ["Низкие инвестиции", "Быстрое масштабирование", "Local ownership"],
            "cons": ["Ограниченный контроль качества", "Зависимость от franchisees", "Brand risks"],
            "best_for": "Множественные малые рынки"
        }
    }
    
    analysis = entry_analysis[entry_mode]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**✅ Преимущества:**")
        for pro in analysis["pros"]:
            st.write(f"• {pro}")
        
        st.markdown("**❌ Недостатки:**")
        for con in analysis["cons"]:
            st.write(f"• {con}")
    
    with col2:
        st.info(f"**Лучше всего для**: {analysis['best_for']}")
        
        # Рекомендация
        if total_risk_score <= 4:
            st.success("🟢 **Рекомендация**: Благоприятные условия для экспансии")
        elif total_risk_score <= 7:
            st.warning("🟡 **Рекомендация**: Экспансия возможна при тщательном планировании")
        else:
            st.error("🔴 **Рекомендация**: Высокорисковая экспансия, рассмотреть альтернативы")

def small_cities_expansion():
    """Экспансия в малые города"""
    st.subheader("🏘️ Экспансия в малые города (Tier 2/3)")
    
    st.info("""
    **Особенности малых городов**: Меньше конкуренции, но и меньше покупательная способность.
    Требуется адаптация ценовой модели и operational approach.
    """)
    
    # Параметры малого города
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🏘️ Характеристики города**")
        
        small_city_population = st.slider("Население", 100000, 800000, 300000)
        economic_activity = st.selectbox("Экономическая активность:",
                                       ["Промышленный центр", "Административный центр",
                                        "Туристический", "Сельскохозяйственный"])
        
        distance_from_major = st.slider("Расстояние от крупного города (км)", 50, 500, 150)
        avg_income_small = st.slider("Средний доход (% от московского)", 40, 80, 55)
        
    with col2:
        st.markdown("**🚗 Транспортная ситуация**")
        
        taxi_penetration = st.slider("Проникновение такси (%)", 5, 40, 15)
        car_ownership = st.slider("Автомобилизация (авто/1000 жителей)", 200, 450, 320)
        public_transport = st.slider("Качество общ.транспорта (1-10)", 2, 8, 4)
        
        # Адаптация модели
        pricing_strategy = st.selectbox("Ценовая стратегия:",
                                      ["Московские цены", "Скидка 20%", "Скидка 40%", "Локальные цены"])
    
    # Market analysis
    moscow_aov = 350
    moscow_income = 100000
    
    # Adjustment для малого города
    income_ratio = avg_income_small / 100
    adjusted_aov = moscow_aov * income_ratio
    
    # Pricing strategy impact
    pricing_adjustments = {
        "Московские цены": 1.0,
        "Скидка 20%": 0.8,
        "Скидка 40%": 0.6,
        "Локальные цены": income_ratio
    }
    
    final_aov = adjusted_aov * pricing_adjustments[pricing_strategy]
    
    # Market potential
    # В малых городах меньше проникновение ride-hailing
    max_penetration = 0.10  # Максимум 10% vs 20% в больших городах
    addressable_market = small_city_population * max_penetration
    
    # Competition factor (обычно меньше конкуренции)
    competition_factor = 0.8 if small_city_population > 400000 else 0.5
    realistic_market = addressable_market * competition_factor
    
    # Operational considerations
    driver_density = car_ownership / 1000 * 0.05  # 5% готовы работать водителями
    required_drivers = realistic_market / 20  # 1 водитель на 20 пользователей
    driver_gap = max(0, required_drivers - small_city_population * driver_density)
    
    # Financial model
    frequency_small_city = 2.0  # Меньше частота чем в мегаполисах
    monthly_revenue_per_user = final_aov * frequency_small_city * 0.25
    
    # Costs в малых городах
    operational_cost_per_user = 15  # Ниже чем в больших городах
    cac_small_city = 800  # Меньше конкуренция = меньше CAC
    
    # Break-even analysis
    monthly_profit_per_user = monthly_revenue_per_user - operational_cost_per_user
    ltv_small_city = monthly_profit_per_user / 0.08  # 8% churn в малых городах
    ltv_cac_ratio = ltv_small_city / cac_small_city
    
    # Results
    st.subheader("📊 Анализ потенциала малого города")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Потенциал рынка", f"{realistic_market:,.0f}")
    
    with col2:
        st.metric("AOV адаптированный", f"{final_aov:.0f} руб")
    
    with col3:
        st.metric("LTV пользователя", f"{ltv_small_city:,.0f} руб")
    
    with col4:
        color = "success" if ltv_cac_ratio >= 3 else "warning" if ltv_cac_ratio >= 2 else "error"
        st.markdown(f"""
        <div class="{color}-card">
            <h4>LTV/CAC</h4>
            <h2>{ltv_cac_ratio:.1f}:1</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Supply-side challenges
    st.subheader("🚗 Анализ предложения (водители)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Потенциальных водителей", f"{small_city_population * driver_density:,.0f}")
        st.metric("Требуется водителей", f"{required_drivers:,.0f}")
        
        if driver_gap > 0:
            st.error(f"Дефицит водителей: {driver_gap:,.0f}")
        else:
            st.success("Достаточно водителей")
    
    with col2:
        # График supply/demand balance
        fig = go.Figure()
        
        categories = ['Потенциальные водители', 'Требуется водителей']
        values = [small_city_population * driver_density, required_drivers]
        colors = ['blue', 'red' if driver_gap > 0 else 'green']
        
        fig.add_trace(go.Bar(x=categories, y=values, marker_color=colors))
        fig.update_layout(title="Баланс спроса и предложения водителей", height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Strategies for small cities
    st.subheader("🎯 Стратегии для малых городов")
    
    strategies = {
        "Промышленный центр": [
            "Фокус на B2B сегмент (заводы, офисы)",
            "Корпоративные контракты на развоз сотрудников",
            "Timing на смены (3 смены = 3 пика спроса)"
        ],
        "Административный центр": [
            "Partnerships с госучреждениями",
            "Фокус на деловые поездки",
            "Premium позиционирование для чиновников"
        ],
        "Туристический": [
            "Сезонная модель работы",
            "Partnerships с отелями и достопримечательностями",
            "Tour packages и экскурсионные маршруты"
        ],
        "Сельскохозяйственный": [
            "Агро-логистика и грузоперевозки",
            "Межгородские маршруты в райцентры",
            "Специализация на rural mobility"
        ]
    }
    
    for strategy in strategies[economic_activity]:
        st.write(f"• {strategy}")
    
    # Risks and mitigation
    st.markdown("""
    ### ⚠️ Риски малых городов:
    
    **🔴 Основные риски:**
    • Ограниченный размер рынка
    • Низкая покупательная способность
    • Сложности с привлечением водителей
    • Seasonal fluctuations
    • Медленное изменение привычек
    
    **✅ Стратегии митигации:**
    • Multi-city approach (кластер малых городов)
    • Адаптация ценовой модели
    • Фокус на underserved segments
    • Partnerships с местными бизнесами
    • Flexible operational model
    """)

def vertical_expansion():
    """Вертикальная экспансия"""
    st.subheader("🚁 Vertical Expansion: Новые сервисы")
    
    st.success("""
    **Leverage existing assets**: Используем платформу, водителей и пользователей для запуска
    смежных сервисов. Диверсификация revenue streams и повышение lifetime value.
    """)
    
    # Выбор вертикали
    vertical_type = st.selectbox(
        "Тип вертикальной экспансии:",
        ["🍕 Доставка еды", "📦 Курьерские услуги", "🚚 Грузоперевозки", 
         "🏪 Grocery delivery", "💊 Медицинские услуги", "🎓 B2B корпоративные решения"]
    )
    
    if vertical_type == "🍕 Доставка еды":
        food_delivery_vertical()
    elif vertical_type == "📦 Курьерские услуги":
        courier_vertical()
    elif vertical_type == "🚚 Грузоперевозки":
        cargo_vertical()
    elif vertical_type == "🏪 Grocery delivery":
        grocery_vertical()
    elif vertical_type == "💊 Медицинские услуги":
        medical_vertical()
    elif vertical_type == "🎓 B2B корпоративные решения":
        b2b_vertical()

def food_delivery_vertical():
    """Доставка еды"""
    st.markdown("### 🍕 Доставка еды")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Текущие активы ride-hailing**")
        
        current_drivers = st.number_input("Активных водителей", 5000, 100000, 25000)
        current_users = st.number_input("Активных пользователей", 50000, 1000000, 200000)
        brand_recognition = st.slider("Узнаваемость бренда (%)", 20, 90, 65)
        
    with col2:
        st.markdown("**🍕 Параметры food delivery**")
        
        restaurant_partnerships = st.number_input("Потенциальных ресторанов", 500, 10000, 2500)
        delivery_fee = st.slider("Комиссия доставки (руб)", 50, 200, 120)
        restaurant_commission = st.slider("Комиссия с ресторана (%)", 15, 35, 25)
        avg_order_value = st.slider("Средний чек заказа (руб)", 600, 2000, 1200)
    
    # Market analysis
    food_delivery_market_size = current_users * 0.4  # 40% ride-hailing пользователей заказывают еду
    monthly_orders_per_user = 3.5  # Частота заказов
    
    # Revenue calculation
    delivery_revenue = food_delivery_market_size * monthly_orders_per_user * delivery_fee
    commission_revenue = food_delivery_market_size * monthly_orders_per_user * avg_order_value * (restaurant_commission / 100)
    total_monthly_revenue = delivery_revenue + commission_revenue
    
    # Costs
    driver_costs = food_delivery_market_size * monthly_orders_per_user * 80  # Оплата курьерам
    operational_costs = total_monthly_revenue * 0.15  # 15% на operations
    
    monthly_profit = total_monthly_revenue - driver_costs - operational_costs
    
    # Investment requirements
    initial_investment = restaurant_partnerships * 15000  # 15k на привлечение ресторана
    tech_development = 8000000  # Разработка delivery платформы
    marketing_launch = 12000000  # Launch кампания
    
    total_investment = initial_investment + tech_development + marketing_launch
    payback_months = total_investment / monthly_profit if monthly_profit > 0 else float('inf')
    
    # Results
    st.subheader("📈 Финансовая модель доставки еды")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Потенциальных пользователей", f"{food_delivery_market_size:,.0f}")
    
    with col2:
        st.metric("Месячная выручка", f"{total_monthly_revenue:,.0f} руб")
    
    with col3:
        st.metric("Месячная прибыль", f"{monthly_profit:,.0f} руб")
    
    with col4:
        st.metric("Окупаемость", f"{payback_months:.1f} мес" if payback_months != float('inf') else "Не окупается")
    
    # Revenue breakdown
    fig = go.Figure(data=[go.Pie(
        labels=['Комиссия доставки', 'Комиссия с ресторанов'],
        values=[delivery_revenue, commission_revenue],
        hole=0.3
    )])
    fig.update_layout(title="Структура выручки food delivery", height=300)
    st.plotly_chart(fig, use_container_width=True)

def courier_vertical():
    """Курьерские услуги"""
    st.markdown("### 📦 Курьерские услуги")
    
    # Similar structure for other verticals...
    st.info("B2B и C2C курьерские услуги, логистика последней мили")
    
    # Simplified implementation for brevity
    st.write("• Leverage existing driver network")
    st.write("• Focus on B2B segment (e-commerce, pharmacies)")
    st.write("• Same-day delivery premium")
    st.write("• Integration with marketplace platforms")

def cargo_vertical():
    """Грузоперевозки"""
    st.markdown("### 🚚 Грузоперевозки")
    st.info("Малотоннажные грузоперевозки для частных лиц и малого бизнеса")

def grocery_vertical():
    """Grocery delivery"""
    st.markdown("### 🏪 Grocery Delivery")
    st.info("Доставка продуктов и товаров повседневного спроса")

def medical_vertical():
    """Медицинские услуги"""
    st.markdown("### 💊 Медицинские услуги")
    st.info("Доставка лекарств, медицинский транспорт, телемедицина")

def b2b_vertical():
    """B2B корпоративные решения"""
    st.markdown("### 🎓 B2B корпоративные решения")
    st.info("Корпоративные аккаунты, employee transportation, business travel")

def industry_cases():
    """Кейсы из индустрии"""
    st.header("📚 Кейсы из ride-hailing индустрии")
    
    st.markdown("""
    **Реальные кейсы**: Адаптированные примеры успешных и неуспешных стратегий 
    в ride-hailing с фокусом на unit economics и growth strategies.
    """)
    
    case_type = st.selectbox(
        "Выберите тип кейса:",
        [
            "🚀 Успешные стратегии роста",
            "💸 Промо-войны и их последствия", 
            "🌍 Международная экспансия",
            "🔄 Pivot и диверсификация",
            "💔 Неудачные запуски",
            "🎯 Нишевые стратегии"
        ]
    )
    
    if case_type == "🚀 Успешные стратегии роста":
        growth_success_cases()
    elif case_type == "💸 Промо-войны и их последствия":
        promo_wars_cases()
    elif case_type == "🌍 Международная экспансия":
        international_cases()
    elif case_type == "🔄 Pivot и диверсификация":
        pivot_cases()
    elif case_type == "💔 Неудачные запуски":
        failure_cases()
    elif case_type == "🎯 Нишевые стратегии":
        niche_strategy_cases()

def growth_success_cases():
    """Успешные стратегии роста"""
    st.subheader("🚀 Кейсы успешного роста")
    
    # Кейс 1: Supply-side first strategy
    with st.expander("📈 Кейс 1: Driver-first стратегия в новом городе"):
        st.markdown("""
        **Ситуация**: Запуск в городе-миллионнике с существующей конкуренцией.
        
        **Стратегия**: Вместо традиционного одновременного привлечения водителей и пассажиров,
        фокус на driver acquisition в первые 3 месяца.
        
        **Тактики**:
        • Guaranteed earnings для первых 1000 водителей
        • Бонусы за привлечение других водителей
        • Premium payout rates (выше конкурентов на 15%)
        • Zero commission первый месяц
        
        **Результаты**:
        • Supply density: 1 водитель на 80 потенциальных пользователей
        • Wait time: 3-4 минуты vs 8-10 у конкурентов
        • Organic demand growth благодаря word-of-mouth
        • LTV/CAC 4.2:1 vs обычных 2.8:1
        
        **Почему сработало**: Решили главную проблему ride-hailing - availability
        """)
    
    # Кейс 2: B2B focus
    with st.expander("💼 Кейс 2: B2B-first стратегия"):
        st.markdown("""
        **Ситуация**: Запуск в городе с низкой покупательной способностью.
        
        **Стратегия**: Фокус на корпоративных клиентах вместо B2C.
        
        **Тактики**:
        • Корпоративные аккаунты с ежемесячной оплатой
        • Dedicated fleet для крупных клиентов
        • Integration с HR системами
        • Bulk pricing со скидками
        
        **Результаты**:
        • 60% выручки от B2B vs обычных 20%
        • Predictable cash flow
        • Lower CAC (sales vs marketing)
        • Higher retention (корпоративные контракты)
        
        **Unit Economics**:
        • B2B CAC: 3,500 руб vs B2C: 1,800 руб
        • B2B LTV: 28,000 руб vs B2C: 6,200 руб
        • B2B LTV/CAC: 8:1 vs B2C: 3.4:1
        """)
    
    # Кейс 3: Loyalty program
    with st.expander("⭐ Кейс 3: Loyalty как growth driver"):
        st.markdown("""
        **Ситуация**: Зрелый рынок с высокой конкуренцией, падающий retention.
        
        **Стратегия**: Запуск comprehensive loyalty программы.
        
        **Механика**:
        • Points за каждую поездку (1 руб = 1 point)
        • Tier system (Bronze/Silver/Gold/Platinum)
        • Exclusive perks для высоких tiers
        • Referral bonuses в points
        
        **Результаты через 6 месяцев**:
        • Retention +35% для участников программы
        • Frequency +28% (стимул тратить points)
        • AOV +15% (upgrade behavior)
        • Referral rate +120%
        
        **Финансовое влияние**:
        • Программа cost: 8% от выручки
        • LTV increase: +42%
        • Net ROI: 380%
        """)

def promo_wars_cases():
    """Кейсы промо-войн"""
    st.subheader("💸 Промо-войны: победители и побежденные")
    
    with st.expander("⚔️ Кейс 1: Агрессивная оборонительная кампания"):
        st.markdown("""
        **Trigger**: Новый конкурент запустил 70% скидки на первые 10 поездок.
        
        **Defensive response**:
        • Matching offer в течение 24 часов
        • Дополнительный cashback для existing users
        • Surge pricing reduction в peak hours
        • PR кампания "Мы всегда предлагаем лучшие цены"
        
        **Timeline и затраты**:
        • Неделя 1-2: 50М руб на промо (2x обычного)
        • Неделя 3-4: 35М руб 
        • Неделя 5-8: Постепенное снижение
        
        **Результаты**:
        • User retention: 92% vs прогнозируемых 75%
        • Market share loss: 3% vs прогнозируемых 15%
        • Total cost: 180М руб
        • Estimated LTV saved: 750М руб
        • ROI defensive campaign: 317%
        
        **Lesson learned**: Быстрая реакция критически важна
        """)
    
    with st.expander("📉 Кейс 2: Промо-война до взаимного истощения"):
        st.markdown("""
        **Ситуация**: Два игрока на рынке начали эскалацию промо.
        
        **Эскалация**:
        • Месяц 1: Игрок A - 50% скидка, Игрок B - matching
        • Месяц 2: A - 60% + cashback, B - 65% скидка
        • Месяц 3: A - 70% + free rides, B - 75% + referral bonuses
        • Месяц 4-6: Взаимное истощение
        
        **Итог через 6 месяцев**:
        • Оба игрока: Unit economics разрушены
        • LTV/CAC упало с 3.2:1 до 0.8:1
        • Привлеченные пользователи: 90% churn после окончания промо
        • Итог: Merge или exit одного из игроков
        
        **Lessons**:
        • Set clear boundaries для промо-войн
        • Focus на value proposition, не только цену
        • Sustainable competitive advantages важнее промо
        """)

def international_cases():
    """Кейсы международной экспансии"""
    st.subheader("🌍 Международная экспансия: успехи и провалы")
    
    with st.expander("✅ Кейс 1: Успешная региональная экспансия"):
        st.markdown("""
        **Маршрут**: Россия → Казахстан → Узбекистан
        
        **Success factors**:
        • Cultural proximity
        • Similar regulatory environment  
        • Existing Russian-speaking user base
        • Local partnerships в каждой стране
        
        **Адаптации**:
        • Казахстан: Фокус на Алматы и Нур-Султан
        • Узбекистан: Cash payments integration
        • Local pricing (40-60% от российских цен)
        • Multilingual support
        
        **Результаты через 2 года**:
        • 3 страны, 8 городов
        • Combined revenue: 15% от total
        • Payback period: 14 месяцев average
        • Regional brand recognition: 45%
        """)
    
    with st.expander("❌ Кейс 2: Неудачная экспансия в Европу"):
        st.markdown("""
        **Attempt**: Россия → Польша
        
        **Challenges encountered**:
        • Strict EU regulations (GDPR, licensing)
        • Established competition (Uber, Bolt)
        • Different user behavior patterns
        • Higher operational costs
        • Currency volatility
        
        **Timeline провала**:
        • Месяц 1-6: Регуляторные препятствия
        • Месяц 7-12: Медленный user acquisition  
        • Месяц 13-18: CAC в 3x выше прогноза
        • Месяц 19-24: Exit decision
        
        **Total losses**: $8M
        
        **Lessons learned**:
        • Regulatory due diligence критически важен
        • Market timing matters
        • Local adaptation vs global brand balance
        • Have clear exit criteria
        """)

def pivot_cases():
    """Кейсы pivot и диверсификации"""
    st.subheader("🔄 Pivot стратегии и диверсификация")
    
    with st.expander("🍕 Кейс 1: Pivot в food delivery во время пандемии"):
        st.markdown("""
        **Trigger**: COVID-19 lockdown, падение ride-hailing на 80%
        
        **Pivot timeline**:
        • Неделя 1-2: Emergency planning
        • Неделя 3-4: Partnership с ресторанами
        • Неделя 5-8: Platform adaptation
        • Неделя 9-12: Full food delivery launch
        
        **Resource reallocation**:
        • 70% drivers switched to delivery
        • Tech team focused on delivery features
        • Customer base partially migrated
        
        **Results через 6 месяцев**:
        • Food delivery: 40% от pre-COVID ride revenue  
        • Combined business sustained 65% revenue
        • Retained 80% driver network
        • Post-COVID: Dual service offering
        
        **Long-term impact**:
        • Diversified revenue streams
        • Higher user engagement (multiple services)
        • Improved LTV through cross-selling
        """)

def failure_cases():
    """Кейсы неудач"""
    st.subheader("💔 Неудачные запуски: lessons learned")
    
    with st.expander("💸 Кейс 1: Overpriced premium positioning"):
        st.markdown("""
        **Strategy**: Запуск premium-only сервиса в среднем городе
        
        **Positioning**:
        • Только luxury cars
        • Premium pricing (2x local taxi)
        • "Exclusive experience" messaging
        
        **Результат через 6 месяцев**:
        • User base: 2,000 (прогноз 25,000)
        • Monthly rides: 3,500 (прогноз 45,000)  
        • CAC: $85 (прогноз $25)
        • LTV/CAC: 0.8:1
        
        **Root causes**:
        • Market research показал готовность платить, но behavior отличался
        • Insufficient volume для operational efficiency
        • Word-of-mouth negative (too expensive)
        
        **Pivot attempt**: Добавили economy tier, но brand damage уже сделан
        **Final outcome**: Exit через 10 месяцев
        """)

def niche_strategy_cases():
    """Нишевые стратегии"""
    st.subheader("🎯 Нишевые стратегии: focus на сегменты")
    
    with st.expander("🚗 Кейс 1: Women-only ride service"):
        st.markdown("""
        **Niche**: Безопасность для женщин
        
        **Service features**:
        • Только водители-женщины
        • Panic button с прямой связью с службой безопасности
        • Family sharing (tracking для родственников)
        • Verified driver profiles
        
        **Market response**:
        • Target audience: 40% female population
        • Adoption rate: 25% среди женщин 18-45
        • Premium pricing: +30% accepted
        • Word-of-mouth: 4.2x higher than regular service
        
        **Unit Economics**:
        • CAC: $18 (lower due to word-of-mouth)
        • LTV: $95 (higher retention due to safety value)
        • LTV/CAC: 5.3:1
        
        **Challenges**:
        • Limited driver pool
        • Higher operational complexity
        • Seasonal fluctuations (safety concerns vary)
        """)

if __name__ == "__main__":
    main()
