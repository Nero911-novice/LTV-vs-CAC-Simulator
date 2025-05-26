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
    page_title="💰 LTV vs CAC Симулятор",
    page_icon="💰",
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
</style>
""", unsafe_allow_html=True)

# Инициализация состояния
if 'scenario_results' not in st.session_state:
    st.session_state.scenario_results = []

if 'cohort_data' not in st.session_state:
    st.session_state.cohort_data = {}

# Главная функция
def main():
    st.title("💰 Симулятор LTV vs CAC")
    st.markdown("**Интерактивная платформа для глубокого анализа LTV/CAC метрик**")
    
    # Боковая панель с навигацией
    with st.sidebar:
        st.header("🎯 Режимы анализа")
        mode = st.selectbox(
            "Выберите режим:",
            [
                "📊 Базовый калькулятор",
                "🔄 Когортный анализ", 
                "📈 Анализ по каналам",
                "🎪 Сценарное планирование",
                "🕵️ Детектор ошибок",
                "💡 Оптимизатор бюджета",
                "📚 Обучающие кейсы"
            ]
        )
        
        st.markdown("---")
        show_help_sidebar()
    
    # Роутинг по режимам
    if mode == "📊 Базовый калькулятор":
        basic_calculator_mode()
    elif mode == "🔄 Когортный анализ":
        cohort_analysis_mode()
    elif mode == "📈 Анализ по каналам":
        channel_analysis_mode()
    elif mode == "🎪 Сценарное планирование":
        scenario_planning_mode()
    elif mode == "🕵️ Детектор ошибок":
        error_detector_mode()
    elif mode == "💡 Оптимизатор бюджета":
        budget_optimizer_mode()
    elif mode == "📚 Обучающие кейсы":
        educational_cases_mode()

def show_help_sidebar():
    """Справочная информация"""
    with st.expander("📖 Глоссарий терминов"):
        st.markdown("""
        **LTV** - Lifetime Value (пожизненная ценность клиента)
        **CAC** - Customer Acquisition Cost (стоимость привлечения клиента)
        **ARPPU** - Average Revenue Per Paying User (средний доход с платящего пользователя)
        **Отток** - Процент клиентов, прекращающих пользоваться услугой
        **Удержание** - Процент клиентов, продолжающих пользоваться услугой
        **Период окупаемости** - Время возврата инвестиций в привлечение
        **Когорта** - Группа клиентов, привлеченных в определенный период
        **Валовая маржа** - Доход минус прямые затраты на обслуживание
        """)
    
    with st.expander("🎯 Бенчмарки по индустриям"):
        st.markdown("""
        **SaaS**: LTV/CAC > 3:1 (оптимально 5:1+)
        **Электронная коммерция**: > 2:1 (оптимально 3:1+)
        **Мобильные приложения**: > 1.5:1
        **B2B услуги**: > 5:1
        **Подписочные сервисы**: > 3:1
        """)

def basic_calculator_mode():
    """Базовый калькулятор LTV/CAC"""
    st.header("📊 Базовый калькулятор LTV/CAC")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚙️ Параметры LTV")
        
        # Параметры для расчета LTV
        arpu = st.slider("ARPPU (руб/месяц)", 500, 10000, 2000, 100)
        gross_margin = st.slider("Валовая маржа (%)", 10, 90, 60, 5)
        monthly_churn = st.slider("Месячный отток (%)", 1.0, 20.0, 5.0, 0.5)
        discount_rate = st.slider("Ставка дисконтирования (%)", 0.0, 20.0, 8.0, 1.0)
        
        # Расчет базового LTV
        monthly_profit = arpu * (gross_margin / 100)
        ltv_simple = monthly_profit / (monthly_churn / 100)
        
        # LTV с дисконтированием
        monthly_discount = (discount_rate / 100) / 12
        ltv_discounted = monthly_profit / (monthly_churn / 100 + monthly_discount)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>Базовый LTV: {ltv_simple:,.0f} руб</h3>
            <h3>LTV с дисконтом: {ltv_discounted:,.0f} руб</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("💰 Параметры CAC")
        
        # Параметры CAC
        marketing_spend = st.number_input("Маркетинговые расходы (руб)", 100000, 10000000, 1000000, 50000)
        new_customers = st.number_input("Новых клиентов", 100, 5000, 500, 50)
        sales_costs = st.slider("Доп. затраты на продажи (%)", 0, 50, 20, 5)
        
        # Расчет CAC
        cac_basic = marketing_spend / new_customers
        cac_fully_loaded = cac_basic * (1 + sales_costs / 100)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>Базовый CAC: {cac_basic:,.0f} руб</h3>
            <h3>Полный CAC: {cac_fully_loaded:,.0f} руб</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Анализ соотношений
    st.subheader("📈 Анализ соотношений")
    
    col1, col2, col3 = st.columns(3)
    
    ratio_simple = ltv_simple / cac_fully_loaded
    ratio_discounted = ltv_discounted / cac_fully_loaded
    payback_months = cac_fully_loaded / monthly_profit
    
    with col1:
        color = "success" if ratio_simple >= 3 else "warning" if ratio_simple >= 2 else "error"
        st.markdown(f"""
        <div class="{color}-card">
            <h4>LTV/CAC (простой)</h4>
            <h2>{ratio_simple:.1f}:1</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        color = "success" if ratio_discounted >= 3 else "warning" if ratio_discounted >= 2 else "error"
        st.markdown(f"""
        <div class="{color}-card">
            <h4>LTV/CAC (дисконт)</h4>
            <h2>{ratio_discounted:.1f}:1</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        color = "success" if payback_months <= 12 else "warning" if payback_months <= 18 else "error"
        st.markdown(f"""
        <div class="{color}-card">
            <h4>Период окупаемости</h4>
            <h2>{payback_months:.1f} мес</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Визуализация чувствительности
    create_sensitivity_chart(arpu, gross_margin, monthly_churn, cac_fully_loaded)
    
    # Интерпретация результатов
    show_interpretation(ratio_discounted, payback_months)

def create_sensitivity_chart(arpu: float, gross_margin: float, churn: float, cac: float):
    """Создание графика чувствительности"""
    st.subheader("🎯 Анализ чувствительности")
    
    # Вариации параметров
    churn_range = np.linspace(churn * 0.5, churn * 2, 20)
    arpu_range = np.linspace(arpu * 0.7, arpu * 1.5, 20)
    
    # Расчет LTV для разных значений
    ltv_churn = [(arpu * gross_margin / 100) / (c / 100) for c in churn_range]
    ltv_arpu = [(a * gross_margin / 100) / (churn / 100) for a in arpu_range]
    
    # Создание интерактивного графика
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Влияние оттока на LTV', 'Влияние ARPPU на LTV')
    )
    
    # График влияния оттока
    fig.add_trace(
        go.Scatter(x=churn_range, y=ltv_churn, mode='lines+markers', 
                  name='LTV от оттока', line=dict(color='red', width=3)),
        row=1, col=1
    )
    
    # График влияния ARPPU
    fig.add_trace(
        go.Scatter(x=arpu_range, y=ltv_arpu, mode='lines+markers',
                  name='LTV от ARPPU', line=dict(color='blue', width=3)),
        row=1, col=2
    )
    
    # Добавляем линию CAC для референса
    fig.add_hline(y=cac, line_dash="dash", line_color="orange", 
                  annotation_text=f"CAC = {cac:,.0f} руб")
    
    fig.update_layout(height=400, showlegend=False)
    fig.update_xaxes(title_text="Месячный отток (%)", row=1, col=1)
    fig.update_xaxes(title_text="ARPPU (руб)", row=1, col=2)
    fig.update_yaxes(title_text="LTV (руб)")
    
    st.plotly_chart(fig, use_container_width=True)

def show_interpretation(ratio: float, payback: float):
    """Интерпретация результатов"""
    st.subheader("🧠 Интерпретация результатов")
    
    if ratio >= 5:
        st.success("🎉 **Отличные показатели!** У вас здоровые LTV/CAC метрики. Можно агрессивно масштабировать привлечение.")
    elif ratio >= 3:
        st.info("👍 **Хорошие показатели.** Бизнес устойчив, есть место для роста маркетингового бюджета.")
    elif ratio >= 2:
        st.warning("⚠️ **Осторожно!** Показатели на грани. Нужно либо снижать CAC, либо увеличивать удержание.")
    else:
        st.error("🚨 **Критические показатели!** Текущая модель неустойчива. Срочно пересматривать стратегию.")
    
    if payback <= 6:
        st.success("💰 **Быстрая окупаемость** - отличное движение денежных средств.")
    elif payback <= 12:
        st.info("📈 **Приемлемая окупаемость** для большинства бизнесов.")
    else:
        st.warning("⏳ **Долгая окупаемость** может создать проблемы с движением денежных средств.")

def cohort_analysis_mode():
    """Режим когортного анализа"""
    st.header("🔄 Когортный анализ LTV")
    
    st.markdown("""
    **Зернистость имеет значение!** Разные когорты клиентов имеют кардинально разное поведение.
    Средняя температура по больнице может скрывать критически важные инсайты.
    """)
    
    # Параметры когорт
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚙️ Настройки когорт")
        
        num_cohorts = st.slider("Количество когорт", 6, 24, 12)
        base_arpu = st.slider("Базовый ARPPU", 1000, 5000, 2000, 100)
        seasonality = st.checkbox("Учесть сезонность", True)
        
        # Генерация данных когорт
        cohort_data = generate_cohort_data(num_cohorts, base_arpu, seasonality)
        
    with col2:
        st.subheader("📊 Сводка по когортам")
        
        avg_ltv = np.mean([c['ltv_final'] for c in cohort_data])
        min_ltv = min([c['ltv_final'] for c in cohort_data])
        max_ltv = max([c['ltv_final'] for c in cohort_data])
        
        st.metric("Средний LTV", f"{avg_ltv:,.0f} руб")
        st.metric("Диапазон LTV", f"{min_ltv:,.0f} - {max_ltv:,.0f} руб")
        st.metric("Разброс", f"{(max_ltv/min_ltv):.1f}x")
    
    # Визуализация эволюции когорт
    create_cohort_evolution_chart(cohort_data)
    
    # Таблица когорт
    create_cohort_table(cohort_data)
    
    # Анализ источников привлечения
    analyze_acquisition_sources(cohort_data)

def generate_cohort_data(num_cohorts: int, base_arpu: int, seasonality: bool) -> List[Dict]:
    """Генерация данных для когортного анализа"""
    cohorts = []
    
    for i in range(num_cohorts):
        month = i + 1
        
        # Сезонные эффекты
        seasonal_multiplier = 1.0
        if seasonality:
            # Q4 - высокий СДПО, но выше отток после праздников
            if month in [10, 11, 12]:
                seasonal_multiplier = 1.3
            elif month in [1, 2]:
                seasonal_multiplier = 0.8
        
        # Случайные вариации
        random_factor = np.random.uniform(0.8, 1.2)
        
        arpu = base_arpu * seasonal_multiplier * random_factor
        initial_churn = np.random.uniform(3, 8)  # Первоначальный отток
        mature_churn = initial_churn * 0.7  # Отток стабилизируется
        
        # Источник привлечения влияет на качество
        source = np.random.choice(['Organic', 'Paid Search', 'Social', 'Referral'], 
                                p=[0.3, 0.4, 0.2, 0.1])
        
        source_multipliers = {
            'Organic': {'arpu': 1.2, 'churn': 0.8},
            'Paid Search': {'arpu': 1.0, 'churn': 1.0},
            'Social': {'arpu': 0.8, 'churn': 1.3},
            'Referral': {'arpu': 1.3, 'churn': 0.6}
        }
        
        arpu *= source_multipliers[source]['arpu']
        mature_churn *= source_multipliers[source]['churn']
        
        # Расчет ПЦК эволюции
        ltv_evolution = calculate_ltv_evolution(arpu, initial_churn, mature_churn)
        
        cohorts.append({
            'month': month,
            'source': source,
            'arpu': arpu,
            'initial_churn': initial_churn,
            'mature_churn': mature_churn,
            'ltv_evolution': ltv_evolution,
            'ltv_final': ltv_evolution[-1],
            'customers': np.random.randint(200, 1000)
        })
    
    return cohorts

def calculate_ltv_evolution(arpu: float, initial_churn: float, mature_churn: float) -> List[float]:
    """Расчет эволюции LTV во времени"""
    months = 24
    ltv_values = []
    
    for month in range(1, months + 1):
        # Отток уменьшается со временем (клиенты становятся более лояльными)
        current_churn = initial_churn * np.exp(-month/6) + mature_churn * (1 - np.exp(-month/6))
        
        # LTV с учетом текущего оттока
        ltv = (arpu * 0.6) / (current_churn / 100)  # 60% валовая маржа
        ltv_values.append(ltv)
    
    return ltv_values

def create_cohort_evolution_chart(cohort_data: List[Dict]):
    """График эволюции LTV когорт"""
    st.subheader("📈 Эволюция LTV когорт во времени")
    
    fig = go.Figure()
    
    # Добавляем линии для каждой когорты
    for cohort in cohort_data[:6]:  # Показываем только первые 6 для читаемости
        months = list(range(1, len(cohort['ltv_evolution']) + 1))
        fig.add_trace(go.Scatter(
            x=months,
            y=cohort['ltv_evolution'],
            mode='lines+markers',
            name=f"Месяц {cohort['month']} ({cohort['source']})",
            line=dict(width=2)
        ))
    
    fig.update_layout(
        title="LTV не константа! Зрелые клиенты имеют другое поведение",
        xaxis_title="Возраст когорты (месяцы)",
        yaxis_title="LTV (руб)",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    💡 **Ключевой инсайт**: LTV растет со временем! Клиенты первого месяца могут иметь LTV в 2-3 раза ниже 
    финального значения. Принятие решений на основе раннего LTV = большая ошибка.
    """)

def create_cohort_table(cohort_data: List[Dict]):
    """Таблица сравнения когорт"""
    st.subheader("📋 Детальная таблица когорт")
    
    df = pd.DataFrame([
        {
            'Когорта': f"Месяц {c['month']}",
            'Источник': c['source'],
            'ARPPU': f"{c['arpu']:,.0f}",
            'Отток (начальный)': f"{c['initial_churn']:.1f}%",
            'Отток (зрелый)': f"{c['mature_churn']:.1f}%",
            'LTV (месяц 1)': f"{c['ltv_evolution'][0]:,.0f}",
            'LTV (финальный)': f"{c['ltv_final']:,.0f}",
            'Множитель роста': f"{c['ltv_final']/c['ltv_evolution'][0]:.1f}x",
            'Клиентов': f"{c['customers']:,}"
        }
        for c in cohort_data
    ])
    
    st.dataframe(df, use_container_width=True)

def analyze_acquisition_sources(cohort_data: List[Dict]):
    """Анализ источников привлечения"""
    st.subheader("🎯 Анализ по источникам привлечения")
    
    # Группировка по источникам
    sources_summary = {}
    for cohort in cohort_data:
        source = cohort['source']
        if source not in sources_summary:
            sources_summary[source] = {'ltv': [], 'arpu': [], 'churn': []}
        
        sources_summary[source]['ltv'].append(cohort['ltv_final'])
        sources_summary[source]['arpu'].append(cohort['arpu'])
        sources_summary[source]['churn'].append(cohort['mature_churn'])
    
    # Создание сравнительного графика
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Средний LTV по источникам', 'ARPPU по источникам',
                       'Отток по источникам', 'LTV/CAC потенциал')
    )
    
    sources = list(sources_summary.keys())
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    # Типичные CAC по источникам
    typical_cac = {'Organic': 500, 'Paid Search': 2000, 'Social': 1200, 'Referral': 300}
    
    for i, source in enumerate(sources):
        avg_ltv = np.mean(sources_summary[source]['ltv'])
        avg_arpu = np.mean(sources_summary[source]['arpu'])
        avg_churn = np.mean(sources_summary[source]['churn'])
        cac = typical_cac.get(source, 1500)
        ltv_cac_ratio = avg_ltv / cac
        
        # LTV
        fig.add_trace(go.Bar(x=[source], y=[avg_ltv], marker_color=colors[i], 
                            showlegend=False), row=1, col=1)
        
        # ARPPU
        fig.add_trace(go.Bar(x=[source], y=[avg_arpu], marker_color=colors[i],
                            showlegend=False), row=1, col=2)
        
        # Отток
        fig.add_trace(go.Bar(x=[source], y=[avg_churn], marker_color=colors[i],
                            showlegend=False), row=2, col=1)
        
        # LTV/CAC
        fig.add_trace(go.Bar(x=[source], y=[ltv_cac_ratio], marker_color=colors[i],
                            showlegend=False), row=2, col=2)
    
    fig.update_layout(height=600)
    fig.update_yaxes(title_text="LTV (руб)", row=1, col=1)
    fig.update_yaxes(title_text="ARPPU (руб)", row=1, col=2)
    fig.update_yaxes(title_text="Отток (%)", row=2, col=1)
    fig.update_yaxes(title_text="LTV/CAC", row=2, col=2)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Выводы
    best_source = max(sources, key=lambda s: np.mean(sources_summary[s]['ltv']) / typical_cac.get(s, 1500))
    st.success(f"🏆 **Лучший источник по LTV/CAC**: {best_source}")

def channel_analysis_mode():
    """Анализ по каналам привлечения"""
    st.header("📈 Анализ каналов привлечения")
    
    st.markdown("""
    **Смешанный CAC vs CAC по каналам** - классическая ошибка! Средняя температура по больнице 
    скрывает прибыльные и убыточные каналы.
    """)
    
    # Настройка каналов
    channels_data = setup_channels_analysis()
    
    # Визуализация каналов
    create_channel_comparison_chart(channels_data)
    
    # Анализ временной динамики
    create_channel_dynamics_chart(channels_data)
    
    # Рекомендации по оптимизации
    show_channel_recommendations(channels_data)

def setup_channels_analysis() -> Dict:
    """Настройка анализа каналов"""
    st.subheader("⚙️ Настройка каналов")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Органические каналы**")
        organic_cac = st.slider("Органический CAC", 100, 1000, 300)
        organic_ltv = st.slider("Органический LTV", 5000, 15000, 10000)
        
        seo_cac = st.slider("SEO CAC", 200, 1500, 600)
        seo_ltv = st.slider("SEO LTV", 4000, 12000, 8000)
        
    with col2:
        st.markdown("**Платные каналы**")
        search_cac = st.slider("Поисковая реклама CAC", 1000, 4000, 2000)
        search_ltv = st.slider("Поисковая реклама LTV", 3000, 10000, 6000)
        
        social_cac = st.slider("Социальные сети CAC", 800, 3000, 1500)
        social_ltv = st.slider("Социальные сети LTV", 2000, 8000, 4000)
        
        display_cac = st.slider("Медийная реклама CAC", 1500, 5000, 3000)
        display_ltv = st.slider("Медийная реклама LTV", 2500, 7000, 4500)
    
    return {
        'Органический трафик': {'cac': organic_cac, 'ltv': organic_ltv, 'volume': 1000},
        'SEO': {'cac': seo_cac, 'ltv': seo_ltv, 'volume': 800},
        'Поисковая реклама': {'cac': search_cac, 'ltv': search_ltv, 'volume': 1500},
        'Социальные сети': {'cac': social_cac, 'ltv': social_ltv, 'volume': 1200},
        'Медийная реклама': {'cac': display_cac, 'ltv': display_ltv, 'volume': 600}
    }

def create_channel_comparison_chart(channels_data: Dict):
    """Сравнительный график каналов"""
    st.subheader("📊 Сравнение каналов по LTV/CAC")
    
    fig = go.Figure()
    
    channels = list(channels_data.keys())
    ltv_values = [channels_data[ch]['ltv'] for ch in channels]
    cac_values = [channels_data[ch]['cac'] for ch in channels]
    ratios = [ltv/cac for ltv, cac in zip(ltv_values, cac_values)]
    volumes = [channels_data[ch]['volume'] for ch in channels]
    
    # Bubble chart
    fig.add_trace(go.Scatter(
        x=cac_values,
        y=ltv_values,
        mode='markers+text',
        text=channels,
        textposition="middle center",
        marker=dict(
            size=[v/20 for v in volumes],  # Размер пропорционален объему
            color=ratios,
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="LTV/CAC"),
            line=dict(width=2, color='black')
        ),
        hovertemplate='<b>%{text}</b><br>' +
                      'CAC: %{x:,.0f} руб<br>' +
                      'LTV: %{y:,.0f} руб<br>' +
                      '<extra></extra>'
    ))
    
    # Добавляем диагональные линии для ориентиров
    max_val = max(max(ltv_values), max(cac_values))
    
    # Линия LTV = CAC (1:1)
    fig.add_shape(type="line", x0=0, x1=max_val, y0=0, y1=max_val,
                  line=dict(color="red", width=2, dash="dash"))
    
    # Линия LTV = 3*CAC (3:1)
    fig.add_shape(type="line", x0=0, x1=max_val/3, y0=0, y1=max_val,
                  line=dict(color="orange", width=2, dash="dash"))
    
    fig.update_layout(
        title="Размер пузыря = объем клиентов, цвет = LTV/CAC",
        xaxis_title="CAC (руб)",
        yaxis_title="LTV (руб)",
        height=500
    )
    
    # Добавляем аннотации
    fig.add_annotation(x=max_val*0.8, y=max_val*0.85, text="LTV = CAC (1:1)",
                      showarrow=False, font=dict(color="red"))
    fig.add_annotation(x=max_val*0.25, y=max_val*0.85, text="LTV = 3×CAC (3:1)",
                      showarrow=False, font=dict(color="orange"))
    
    st.plotly_chart(fig, use_container_width=True)

def create_channel_dynamics_chart(channels_data: Dict):
    """График временной динамики каналов"""
    st.subheader("⏰ Временная динамика CAC")
    
    # Симуляция временной динамики
    months = 12
    time_data = {}
    
    for channel in channels_data.keys():
        base_cac = channels_data[channel]['cac']
        
        # Разные паттерны изменения CAC
        if 'Органический' in channel or 'SEO' in channel:
            # Органические каналы - стабильный рост CAC из-за конкуренции
            trend = [base_cac * (1 + 0.02 * month) for month in range(months)]
        elif 'Поисковая' in channel:
            # Поисковая реклама - сезонность + конкуренция
            trend = [base_cac * (1 + 0.03 * month + 0.1 * np.sin(month * np.pi / 6)) 
                    for month in range(months)]
        elif 'Социальные' in channel:
            # Социальные сети - волатильность из-за изменений алгоритмов
            trend = [base_cac * (1 + np.random.normal(0, 0.1)) for _ in range(months)]
        else:
            # Медийная реклама - постепенный рост + креативная усталость
            trend = [base_cac * (1 + 0.04 * month + 0.05 * (month > 6)) 
                    for month in range(months)]
        
        time_data[channel] = trend
    
    # График
    fig = go.Figure()
    
    for channel, values in time_data.items():
        fig.add_trace(go.Scatter(
            x=list(range(1, months + 1)),
            y=values,
            mode='lines+markers',
            name=channel,
            line=dict(width=3)
        ))
    
    fig.update_layout(
        title="CAC не константа! Отслеживайте динамику во времени",
        xaxis_title="Месяц",
        yaxis_title="CAC (руб)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.warning("""
    ⚠️ **Важно**: CAC имеет тенденцию расти со временем из-за:
    - Роста конкуренции на рынке
    - Креативной усталости (падение CTR)
    - Алгоритмических изменений платформ
    - Сезонных факторов
    """)

def show_channel_recommendations(channels_data: Dict):
    """Рекомендации по оптимизации каналов"""
    st.subheader("💡 Рекомендации по оптимизации")
    
    # Расчет метрик
    channel_metrics = {}
    for channel, data in channels_data.items():
        ratio = data['ltv'] / data['cac']
        payback = data['cac'] / (data['ltv'] / 24)  # Предполагаем ПЦК за 24 месяца
        
        channel_metrics[channel] = {
            'ratio': ratio,
            'payback': payback,
            'volume': data['volume'],
            'status': 'profitable' if ratio > 3 else 'marginal' if ratio > 2 else 'unprofitable'
        }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🟢 Каналы для масштабирования")
        for channel, metrics in channel_metrics.items():
            if metrics['status'] == 'profitable':
                st.success(f"**{channel}**: LTV/CAC = {metrics['ratio']:.1f}:1, "
                          f"окупаемость {metrics['payback']:.1f} мес")
    
    with col2:
        st.markdown("#### 🔴 Каналы для оптимизации")
        for channel, metrics in channel_metrics.items():
            if metrics['status'] == 'unprofitable':
                st.error(f"**{channel}**: LTV/CAC = {metrics['ratio']:.1f}:1, "
                        f"окупаемость {metrics['payback']:.1f} мес")
    
    # Общие рекомендации
    best_channel = max(channel_metrics.keys(), key=lambda x: channel_metrics[x]['ratio'])
    worst_channel = min(channel_metrics.keys(), key=lambda x: channel_metrics[x]['ratio'])
    
    st.info(f"""
    📈 **Стратегические рекомендации**:
    
    1. **Масштабировать**: {best_channel} (лучший LTV/CAC = {channel_metrics[best_channel]['ratio']:.1f}:1)
    2. **Оптимизировать**: {worst_channel} (требует улучшения targeting/креативов)
    3. **Диверсифицировать**: Не полагаться только на один канал
    4. **Мониторить**: Отслеживать динамику CAC еженедельно
    """)

def scenario_planning_mode():
    """Режим сценарного планирования"""
    st.header("🎪 Сценарное планирование")
    
    st.markdown("""
    **Что если?** Моделирование различных сценариев для понимания рисков и возможностей.
    Системное мышление - LTV и CAC взаимосвязаны через множество переменных.
    """)
    
    # Выбор типа сценария
    scenario_type = st.selectbox(
        "Выберите тип сценария:",
        [
            "🚀 Сценарий роста", 
            "📉 Кризисный сценарий",
            "🆚 Конкурентное давление",
            "📱 Запуск нового продукта",
            "🌍 Географическое расширение"
        ]
    )
    
    if scenario_type == "🚀 Сценарий роста":
        growth_scenario()
    elif scenario_type == "📉 Кризисный сценарий":
        crisis_scenario()
    elif scenario_type == "🆚 Конкурентное давление":
        competitive_scenario()
    elif scenario_type == "📱 Запуск нового продукта":
        new_product_scenario()
    elif scenario_type == "🌍 Географическое расширение":
        expansion_scenario()

def growth_scenario():
    """Сценарий агрессивного роста"""
    st.subheader("🚀 Сценарий агрессивного роста")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Параметры роста**")
        budget_increase = st.slider("Увеличение бюджета (%)", 50, 500, 200)
        cac_inflation = st.slider("Инфляция СПК (%)", 0, 100, 30)
        volume_efficiency = st.slider("Эффективность масштабирования (%)", 50, 100, 80)
        
    with col2:
        st.markdown("**Базовые метрики**")
        base_budget = st.number_input("Текущий бюджет", 100000, 10000000, 1000000)
        base_cac = st.number_input("Текущий CAC", 500, 5000, 1500)
        base_ltv = st.number_input("Текущий LTV", 2000, 20000, 6000)
    
    # Расчет сценария
    new_budget = base_budget * (1 + budget_increase / 100)
    new_cac = base_cac * (1 + cac_inflation / 100)
    volume_multiplier = (volume_efficiency / 100) * (budget_increase / 100)
    new_customers = (base_budget / base_cac) * (1 + volume_multiplier)
    
    # Результаты
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Новый бюджет", f"{new_budget:,.0f} руб", 
                 f"+{(new_budget - base_budget):,.0f}")
    
    with col2:
        st.metric("Новый CAC", f"{new_cac:,.0f} руб",
                 f"+{(new_cac - base_cac):,.0f}")
    
    with col3:
        st.metric("Новых клиентов", f"{new_customers:,.0f}",
                 f"+{(new_customers - base_budget/base_cac):,.0f}")
    
    # Анализ ROI
    current_roi = (base_ltv - base_cac) / base_cac
    new_roi = (base_ltv - new_cac) / new_cac
    
    st.subheader("📊 Анализ окупаемости")
    
    if new_roi > 0:
        st.success(f"✅ ROI остается положительным: {new_roi:.1%}")
    else:
        st.error(f"❌ ROI становится отрицательным: {new_roi:.1%}")
    
    # Визуализация денежного потока
    create_cashflow_projection(new_budget, new_cac, base_ltv, new_customers)

def crisis_scenario():
    """Кризисный сценарий"""
    st.subheader("📉 Кризисный сценарий")
    
    st.warning("""
    Моделирование влияния экономического кризиса на ключевые метрики.
    Кризис влияет как на привлечение (СПК), так и на удержание (ПЦК).
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Негативные факторы**")
        arpu_decline = st.slider("Падение СДПО (%)", 0, 50, 20)
        churn_increase = st.slider("Рост оттока (%)", 0, 100, 50)
        budget_cut = st.slider("Сокращение бюджета (%)", 0, 70, 30)
        
    with col2:
        st.markdown("**Базовые метрики**")
        base_arpu = st.number_input("Базовый ARPPU", 1000, 10000, 3000)
        base_churn = st.slider("Базовый отток (%)", 1.0, 15.0, 5.0, 0.5)
        base_budget = st.number_input("Базовый бюджет", 100000, 5000000, 1000000)
    
    # Расчет кризисного воздействия
    new_arpu = base_arpu * (1 - arpu_decline / 100)
    new_churn = base_churn * (1 + churn_increase / 100)
    new_budget = base_budget * (1 - budget_cut / 100)
    
    # LTV до и после
    base_ltv = (base_arpu * 0.6) / (base_churn / 100)  # 60% маржа
    new_ltv = (new_arpu * 0.6) / (new_churn / 100)
    
    ltv_change = (new_ltv - base_ltv) / base_ltv
    
    # Результаты
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("ARPPU", f"{new_arpu:,.0f} руб", f"{ltv_change:.1%}")
    
    with col2:
        st.metric("Отток", f"{new_churn:.1f}%", f"+{new_churn - base_churn:.1f}%")
    
    with col3:
        st.metric("LTV", f"{new_ltv:,.0f} руб", f"{(new_ltv - base_ltv):,.0f}")
    
    # Стратегические рекомендации
    if ltv_change < -0.3:
        st.error("🚨 Критическое падение LTV! Необходимы срочные меры по удержанию.")
    elif ltv_change < -0.15:
        st.warning("⚠️ Значительное падение LTV. Пересмотрите стратегию удержания.")
    else:
        st.info("📊 Умеренное влияние. Фокус на эффективности привлечения.")

def create_cashflow_projection(budget: float, cac: float, ltv: float, customers: float):
    """Проекция денежного потока"""
    st.subheader("💰 Проекция денежного потока")
    
    months = 24
    monthly_arpu = ltv / months  # Упрощенное предположение
    
    # Расчет денежного потока
    cashflow = []
    cumulative = 0
    
    for month in range(1, months + 1):
        if month == 1:
            # Первый месяц - расходы на привлечение
            monthly_flow = -budget + (customers * monthly_arpu)
        else:
            # Последующие месяцы - доходы от привлеченных клиентов
            # С учетом оттока 5% в месяц
            active_customers = customers * (0.95 ** (month - 1))
            monthly_flow = active_customers * monthly_arpu
        
        cumulative += monthly_flow
        cashflow.append({'month': month, 'monthly': monthly_flow, 'cumulative': cumulative})
    
    df = pd.DataFrame(cashflow)
    
    # График
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(x=df['month'], y=df['monthly'], name='Месячный поток',
               marker_color=['red' if x < 0 else 'green' for x in df['monthly']]),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=df['month'], y=df['cumulative'], mode='lines+markers',
                  name='Накопительный поток', line=dict(color='blue', width=3)),
        secondary_y=True,
    )
    
    # Линия окупаемости
    fig.add_hline(y=0, line_dash="dash", line_color="black", secondary_y=True)
    
    fig.update_xaxes(title_text="Месяц")
    fig.update_yaxes(title_text="Месячный поток (руб)", secondary_y=False)
    fig.update_yaxes(title_text="Накопительный поток (руб)", secondary_y=True)
    
    fig.update_layout(title="Проекция денежного потока после изменений", height=400)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Период окупаемости
    payback_month = None
    for item in cashflow:
        if item['cumulative'] > 0:
            payback_month = item['month']
            break
    
    if payback_month:
        st.success(f"💰 **Период окупаемости**: {payback_month} месяцев")
    else:
        st.error("❌ **Окупаемость не достигается** в рамках 24 месяцев")

def competitive_scenario():
    """Сценарий конкурентного давления"""
    st.subheader("🆚 Конкурентное давление")
    
    st.info("""
    Новый агрессивный конкурент входит на рынок, влияя на стоимость привлечения 
    и долю рынка. Как это отразится на ваших метриках?
    """)
    
    competitor_aggression = st.slider("Агрессивность конкурента (1-10)", 1, 10, 6)
    
    # Влияние на разные каналы
    channels_impact = {
        'Поисковая реклама': competitor_aggression * 0.15,  # Сильное влияние
        'Социальные сети': competitor_aggression * 0.10,    # Среднее влияние  
        'Медийная реклама': competitor_aggression * 0.20,   # Очень сильное влияние
        'SEO': competitor_aggression * 0.05,                # Слабое влияние
        'Органический': competitor_aggression * 0.02        # Минимальное влияние
    }
    
    st.subheader("📊 Влияние на СПК по каналам")
    
    for channel, impact in channels_impact.items():
        base_cac = 2000  # Базовый СПК
        new_cac = base_cac * (1 + impact)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{channel}**")
        with col2:
            st.metric("СПК", f"{new_cac:,.0f}", f"+{impact:.1%}")

def new_product_scenario():
    """Сценарий запуска нового продукта"""
    st.subheader("📱 Запуск нового продукта")
    
    st.markdown("""
    Новый продукт может иметь совершенно другие метрики ПЦК/СПК. 
    Важно моделировать метрики до запуска.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Характеристики нового продукта**")
        price_premium = st.slider("Премия к цене (%)", -50, 200, 50)
        target_sophistication = st.slider("Сложность таргетинга (1-10)", 1, 10, 7)
        market_size = st.selectbox("Размер рынка", ["Нишевый", "Средний", "Массовый"])
        
    with col2:
        st.markdown("**Базовые метрики**")
        base_price = st.number_input("Базовая цена продукта", 1000, 50000, 5000)
        base_cac = st.number_input("Базовый СПК", 500, 10000, 2000)
        
    # Расчет метрик нового продукта
    new_price = base_price * (1 + price_premium / 100)
    
    # СПК зависит от сложности таргетинга
    cac_multiplier = 1 + (target_sophistication - 5) * 0.2
    new_cac = base_cac * cac_multiplier
    
    # Размер рынка влияет на потенциал масштабирования
    market_multipliers = {"Нишевый": 0.3, "Средний": 1.0, "Массовый": 2.0}
    scale_potential = market_multipliers[market_size]
    
    # Упрощенный ПЦК (предполагаем схожее поведение клиентов)
    new_ltv = new_price * 8  # 8 месяцев средняя жизнь клиента
    
    # Результаты
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Цена продукта", f"{new_price:,.0f} руб", f"{price_premium:+.0f}%")
    
    with col2:
        st.metric("Прогнозный СПК", f"{new_cac:,.0f} руб", f"{(cac_multiplier-1)*100:+.0f}%")
    
    with col3:
        ratio = new_ltv / new_cac
        st.metric("ПЦК/СПК", f"{ratio:.1f}:1", 
                 "Хорошо" if ratio > 3 else "Плохо")
    
    st.info(f"🎯 **Потенциал масштабирования**: {scale_potential:.1f}x от базового рынка")

def expansion_scenario():
    """Сценарий географического расширения"""
    st.subheader("🌍 Географическое расширение")
    
    region = st.selectbox("Целевой регион", 
                         ["СПб и ЛО", "Регионы РФ", "Казахстан", "Беларусь"])
    
    # Региональные коэффициенты (примерные)
    regional_factors = {
        "СПб и ЛО": {"cac_mult": 0.8, "ltv_mult": 0.9, "competition": 8},
        "Регионы РФ": {"cac_mult": 0.6, "ltv_mult": 0.7, "competition": 4}, 
        "Казахстан": {"cac_mult": 0.4, "ltv_mult": 0.5, "competition": 3},
        "Беларусь": {"cac_mult": 0.5, "ltv_mult": 0.6, "competition": 2}
    }
    
    factors = regional_factors[region]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Московские метрики (база)**")
        msk_cac = st.number_input("Московский СПК", 1000, 5000, 2500)
        msk_ltv = st.number_input("Московский ПЦК", 5000, 25000, 12000)
        
    with col2:
        st.markdown(f"**Прогноз для {region}**")
        
        regional_cac = msk_cac * factors["cac_mult"]
        regional_ltv = msk_ltv * factors["ltv_mult"]
        
        st.metric("Региональный СПК", f"{regional_cac:,.0f} руб", 
                 f"{(factors['cac_mult']-1)*100:+.0f}%")
        st.metric("Региональный ПЦК", f"{regional_ltv:,.0f} руб",
                 f"{(factors['ltv_mult']-1)*100:+.0f}%")
        
        regional_ratio = regional_ltv / regional_cac
        msk_ratio = msk_ltv / msk_cac
        
        st.metric("ПЦК/СПК", f"{regional_ratio:.1f}:1",
                 f"{regional_ratio - msk_ratio:+.1f}")
    
    # Анализ привлекательности региона
    st.subheader("📈 Анализ привлекательности")
    
    attractiveness_score = (
        regional_ratio * 2 +  # Доходность
        (10 - factors["competition"]) * 0.5 +  # Низкая конкуренция = плюс
        factors["ltv_mult"] * 5  # Покупательная способность
    )
    
    if attractiveness_score > 8:
        st.success(f"🎯 **Высокая привлекательность** региона {region} (оценка: {attractiveness_score:.1f}/10)")
    elif attractiveness_score > 6:
        st.info(f"📊 **Средняя привлекательность** региона {region} (оценка: {attractiveness_score:.1f}/10)")
    else:
        st.warning(f"⚠️ **Низкая привлекательность** региона {region} (оценка: {attractiveness_score:.1f}/10)")

def error_detector_mode():
    """Режим детектора ошибок"""
    st.header("🕵️ Детектор ошибок в расчетах LTV/CAC")
    
    st.markdown("""
    **В стиле Statistical Detective!** Найдите скрытые ошибки в расчетах LTV/CAC,
    которые могут привести к катастрофическим решениям.
    """)
    
    # Выбор кейса
    error_cases = get_ltv_cac_error_cases()
    
    case_titles = [case['title'] for case in error_cases]
    selected_case = st.selectbox("Выберите кейс для анализа:", case_titles)
    
    current_case = next(case for case in error_cases if case['title'] == selected_case)
    
    # Отображение кейса
    display_error_case(current_case)

def get_ltv_cac_error_cases() -> List[Dict]:
    """База кейсов с ошибками в LTV/CAC"""
    return [
        {
            'title': 'Валовый LTV vs Чистый LTV',
            'description': """
            **Ситуация**: Менеджер по продукту докладывает руководству:
            
            "Наши метрики выглядят отлично! LTV клиента составляет 15,000 руб, 
            CAC только 3,000 руб. Соотношение 5:1 - можем агрессивно масштабироваться!"
            
            **Данные**:
            - Средний чек: 2,500 руб/месяц
            - Средняя продолжительность жизни: 6 месяцев  
            - LTV = 2,500 × 6 = 15,000 руб
            - CAC = 3,000 руб
            
            **Скрытая информация**:
            - Себестоимость товара: 40%
            - Операционные расходы: 25%
            - Стоимость обслуживания клиента: 200 руб/месяц
            """,
            'options': [
                "Расчет корректен, можно масштабироваться",
                "Ошибка: не учтена себестоимость и операционные расходы",
                "Ошибка: слишком короткий период для расчета LTV",
                "Ошибка: нужно учесть дисконтирование"
            ],
            'correct': 1,
            'explanation': """
            **Правильный ответ**: Не учтена себестоимость и операционные расходы.
            
            **Правильный расчет**:
            - Валовая прибыль = 2,500 × (1 - 0.4 - 0.25) = 875 руб/месяц
            - Затраты на обслуживание = 200 руб/месяц  
            - Чистая прибыль = 875 - 200 = 675 руб/месяц
            - Чистый LTV = 675 × 6 = 4,050 руб
            - **Реальное соотношение = 1.35:1** (критически низкое!)
            
            **Урок**: Всегда используйте чистый LTV, не валовый!
            """
        },
        {
            'title': 'Предвзятость выжившего в LTV',
            'description': """
            **Ситуация**: Аналитик рассчитывает LTV на основе существующих клиентов:
            
            "Проанализировал наших клиентов за последний год. Средний LTV составляет 
            12,000 руб при CAC 2,000 руб. Отличное соотношение 6:1!"
            
            **Методология расчета**:
            - Взял всех активных клиентов на текущий момент
            - Рассчитал их суммарную выручку с момента привлечения
            - Разделил на количество клиентов
            
            **Что может быть не так?**
            """,
            'options': [
                "Методология корректна",
                "Предвзятость выжившего: анализируются только активные клиенты", 
                "Нужно учесть более длительный период",
                "Ошибка в расчете среднего значения"
            ],
            'correct': 1,
            'explanation': """
            **Правильный ответ**: Предвзятость выжившего.
            
            **Проблема**: Анализируются только клиенты, которые "выжили" и до сих пор активны.
            Клиенты, которые ушли быстро (и имели низкий LTV), исключены из расчета.
            
            **Правильно**: Когортный анализ всех клиентов, привлеченных в определенный период,
            включая тех, кто уже ушел.
            
            **Реальный LTV может быть в 2-3 раза ниже** расчетного!
            """
        },
        {
            'title': 'Смешанный CAC vs CAC по каналам',
            'description': """
            **Ситуация**: Маркетолог принимает решения на основе общего CAC:
            
            "Наш средний CAC составляет 1,800 руб. Это приемлемо для нашего LTV 7,200 руб.
            Увеличиваем бюджет всех каналов пропорционально."
            
            **Данные по каналам**:
            - Органический трафик: 500 клиентов, CAC 400 руб
            - Google Ads: 300 клиентов, CAC 2,500 руб  
            - Facebook: 200 клиентов, CAC 3,200 руб
            - Средневзвешенный CAC = 1,800 руб
            
            **Вопрос**: В чем ошибка такого подхода?
            """,
            'options': [
                "Ошибки нет, средневзвешенный CAC корректен",
                "Ошибка: каналы имеют разную эффективность и потенциал масштабирования",
                "Ошибка: нужно учесть LTV по каналам отдельно", 
                "Ошибка: Б и В правильные"
            ],
            'correct': 3,
            'explanation': """
            **Правильный ответ**: Б и В правильные.
            
            **Проблемы смешанного CAC**:
            1. Скрывает высокоэффективные каналы (органика: LTV/CAC = 18:1)
            2. Скрывает неэффективные каналы (Facebook: LTV/CAC = 2.25:1)
            3. Неправильные решения по распределению бюджета
            
            **Правильно**: Анализировать LTV/CAC каждого канала отдельно и 
            перераспределять бюджет в пользу эффективных каналов.
            """
        }
    ]

def display_error_case(case: Dict):
    """Отображение кейса с ошибкой"""
    st.subheader(case['title'])
    st.markdown(case['description'])
    
    st.markdown("### 🤔 В чем ошибка?")
    
    answer = st.radio("Выберите правильный ответ:", case['options'], 
                     key=f"error_case_{case['title']}")
    
    if st.button("Проверить ответ", key=f"check_error_{case['title']}"):
        user_choice = case['options'].index(answer)
        
        if user_choice == case['correct']:
            st.success("🎉 Правильно! Отличная детективная работа!")
            st.markdown(case['explanation'])
        else:
            st.error("❌ Неправильно. Попробуйте еще раз!")
            st.info("💡 Подсказка: Подумайте о скрытых факторах и определениях метрик.")

def budget_optimizer_mode():
    """Режим оптимизации бюджета"""
    st.header("💡 Оптимизатор бюджета")
    
    st.markdown("""
    **Практическая часть**: Получите текущий бюджет и оптимизируйте его распределение 
    для максимизации ROI или объема привлечения.
    """)
    
    # Настройка исходных данных
    st.subheader("📊 Текущее распределение бюджета")
    
    col1, col2 = st.columns(2)
    
    with col1:
        total_budget = st.number_input("Общий бюджет (руб)", 500000, 20000000, 2000000)
        optimization_goal = st.selectbox("Цель оптимизации:", 
                                       ["Максимизировать ROI", "Максимизировать объем"])
        
    with col2:
        min_budget_constraint = st.slider("Мин. бюджет на канал (%)", 0, 30, 10)
        max_budget_constraint = st.slider("Макс. бюджет на канал (%)", 40, 80, 60)
    
    # Текущее распределение
    current_allocation = setup_current_allocation(total_budget)
    
    # Расчет оптимального распределения
    optimal_allocation = calculate_optimal_allocation(
        current_allocation, optimization_goal, 
        min_budget_constraint, max_budget_constraint
    )
    
    # Сравнение результатов
    compare_allocations(current_allocation, optimal_allocation)

def setup_current_allocation(total_budget: float) -> Dict:
    """Настройка текущего распределения бюджета"""
    st.subheader("⚙️ Текущие метрики каналов")
    
    channels = {
        'Google Ads': {'budget_pct': 40, 'cac': 2000, 'ltv': 6000, 'max_volume': 1000},
        'Facebook': {'budget_pct': 25, 'cac': 1800, 'ltv': 4500, 'max_volume': 800},
        'Яндекс.Директ': {'budget_pct': 20, 'cac': 2200, 'ltv': 6500, 'max_volume': 600},
        'SEO': {'budget_pct': 10, 'cac': 800, 'ltv': 8000, 'max_volume': 300},
        'Email': {'budget_pct': 5, 'cac': 500, 'ltv': 5000, 'max_volume': 200}
    }
    
    st.markdown("Настройте метрики каналов:")
    
    for channel in channels:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.write(f"**{channel}**")
        with col2:
            channels[channel]['budget_pct'] = st.number_input(
                f"Бюджет %", 0, 100, channels[channel]['budget_pct'], 
                key=f"budget_{channel}")
        with col3:
            channels[channel]['cac'] = st.number_input(
                f"СПК", 100, 5000, channels[channel]['cac'],
                key=f"cac_{channel}")
        with col4:
            channels[channel]['ltv'] = st.number_input(
                f"ПЦК", 1000, 15000, channels[channel]['ltv'],
                key=f"ltv_{channel}")
        with col5:
            channels[channel]['max_volume'] = st.number_input(
                f"Макс. объем", 50, 2000, channels[channel]['max_volume'],
                key=f"volume_{channel}")
    
    # Расчет абсолютных значений
    for channel in channels:
        channels[channel]['budget'] = total_budget * channels[channel]['budget_pct'] / 100
        channels[channel]['customers'] = channels[channel]['budget'] / channels[channel]['cac']
        channels[channel]['roi'] = (channels[channel]['ltv'] - channels[channel]['cac']) / channels[channel]['cac']
    
    return channels

def calculate_optimal_allocation(channels: Dict, goal: str, min_pct: float, max_pct: float) -> Dict:
    """Расчет оптимального распределения бюджета"""
    
    # Простая эвристическая оптимизация
    optimal = {}
    total_budget = sum(ch['budget'] for ch in channels.values())
    
    if goal == "Максимизировать ROI":
        # Сортируем каналы по ROI
        sorted_channels = sorted(channels.items(), key=lambda x: x[1]['roi'], reverse=True)
    else:
        # Сортируем каналы по потенциалу объема (учитывая масштабируемость)
        sorted_channels = sorted(channels.items(), 
                               key=lambda x: x[1]['max_volume'] / x[1]['cac'], reverse=True)
    
    remaining_budget = total_budget
    allocated_budget = {}
    
    # Сначала выделяем минимумы
    for channel_name, channel_data in channels.items():
        min_budget = total_budget * min_pct / 100
        allocated_budget[channel_name] = min_budget
        remaining_budget -= min_budget
    
    # Затем распределяем остаток по эффективности
    for channel_name, channel_data in sorted_channels:
        max_additional = total_budget * max_pct / 100 - allocated_budget[channel_name]
        
        # Ограничение по максимальному объему канала
        max_by_volume = channel_data['max_volume'] * channel_data['cac'] - allocated_budget[channel_name]
        max_additional = min(max_additional, max_by_volume, remaining_budget)
        
        if max_additional > 0:
            allocated_budget[channel_name] += max_additional
            remaining_budget -= max_additional
    
    # Формируем результат
    for channel_name, channel_data in channels.items():
        optimal[channel_name] = channel_data.copy()
        optimal[channel_name]['budget'] = allocated_budget[channel_name]
        optimal[channel_name]['budget_pct'] = (allocated_budget[channel_name] / total_budget) * 100
        optimal[channel_name]['customers'] = min(
            allocated_budget[channel_name] / channel_data['cac'],
            channel_data['max_volume']
        )
        optimal[channel_name]['actual_spend'] = optimal[channel_name]['customers'] * channel_data['cac']
    
    return optimal

def compare_allocations(current: Dict, optimal: Dict):
    """Сравнение текущего и оптимального распределения"""
    st.subheader("📈 Сравнение распределений")
    
    # Создание таблицы сравнения
    comparison_data = []
    
    for channel in current.keys():
        curr = current[channel]
        opt = optimal[channel]
        
        comparison_data.append({
            'Канал': channel,
            'Текущий бюджет': f"{curr['budget']:,.0f}",
            'Оптимальный бюджет': f"{opt['budget']:,.0f}",
            'Изменение': f"{((opt['budget'] - curr['budget']) / curr['budget'] * 100):+.0f}%",
            'Текущий ROI': f"{curr['roi']:.1%}",
            'Текущие клиенты': f"{curr['customers']:.0f}",
            'Оптимальные клиенты': f"{opt['customers']:.0f}"
        })
    
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True)
    
    # Общие метрики
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Текущие результаты")
        curr_customers = sum(ch['customers'] for ch in current.values())
        curr_revenue = sum(ch['customers'] * ch['ltv'] for ch in current.values())
        curr_profit = sum(ch['customers'] * (ch['ltv'] - ch['cac']) for ch in current.values())
        
        st.metric("Общий объем клиентов", f"{curr_customers:.0f}")
        st.metric("Общая выручка", f"{curr_revenue:,.0f} руб")
        st.metric("Общая прибыль", f"{curr_profit:,.0f} руб")
    
    with col2:
        st.markdown("#### 🎯 Оптимальные результаты")
        opt_customers = sum(ch['customers'] for ch in optimal.values())
        opt_revenue = sum(ch['customers'] * ch['ltv'] for ch in optimal.values())
        opt_profit = sum(ch['customers'] * (ch['ltv'] - ch['cac']) for ch in optimal.values())
        
        st.metric("Общий объем клиентов", f"{opt_customers:.0f}",
                 f"{((opt_customers - curr_customers) / curr_customers * 100):+.1f}%")
        st.metric("Общая выручка", f"{opt_revenue:,.0f} руб",
                 f"{((opt_revenue - curr_revenue) / curr_revenue * 100):+.1f}%")
        st.metric("Общая прибыль", f"{opt_profit:,.0f} руб",
                 f"{((opt_profit - curr_profit) / curr_profit * 100):+.1f}%")
    
    # Визуализация изменений
    create_budget_reallocation_chart(current, optimal)

def create_budget_reallocation_chart(current: Dict, optimal: Dict):
    """График перераспределения бюджета"""
    st.subheader("📊 Визуализация перераспределения")
    
    channels = list(current.keys())
    current_budgets = [current[ch]['budget'] for ch in channels]
    optimal_budgets = [optimal[ch]['budget'] for ch in channels]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=channels,
        y=current_budgets,
        name='Текущий бюджет',
        marker_color='lightblue',
        opacity=0.7
    ))
    
    fig.add_trace(go.Bar(
        x=channels,
        y=optimal_budgets,
        name='Оптимальный бюджет',
        marker_color='darkblue',
        opacity=0.9
    ))
    
    fig.update_layout(
        title="Сравнение текущего и оптимального распределения бюджета",
        xaxis_title="Канал",
        yaxis_title="Бюджет (руб)",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def educational_cases_mode():
    """Обучающие кейсы"""
    st.header("📚 Обучающие кейсы")
    
    st.markdown("""
    **Реальные кейсы из практики** для понимания применения ПЦК/СПК метрик 
    в различных бизнес-ситуациях.
    """)
    
    case_type = st.selectbox(
        "Выберите тип кейса:",
        [
            "💰 SaaS стартап",
            "🛍️ Электронная коммерция", 
            "📱 Мобильное приложение",
            "🏢 B2B сервис",
            "📺 Подписочный сервис"
        ]
    )
    
    if case_type == "💰 SaaS стартап":
        saas_case()
    elif case_type == "🛍️ Электронная коммерция":
        ecommerce_case()
    elif case_type == "📱 Мобильное приложение":
        mobile_app_case()
    elif case_type == "🏢 B2B сервис":
        b2b_case()
    elif case_type == "📺 Подписочный сервис":
        subscription_case()

def saas_case():
    """Кейс SaaS стартапа"""
    st.subheader("💰 Кейс: SaaS стартап для автоматизации HR")
    
    st.markdown("""
    **Ситуация**: Стартап разработал SaaS платформу для автоматизации HR процессов.
    Есть 3 тарифных плана, нужно оптимизировать маркетинговую стратегию.
    """)
    
    # Данные по тарифам
    plans_data = {
        "Базовый": {"price": 2000, "churn": 8.0, "conversion": 15, "cac": 3000},
        "Профессиональный": {"price": 5000, "churn": 5.0, "conversion": 8, "cac": 6000}, 
        "Корпоративный": {"price": 15000, "churn": 2.0, "conversion": 3, "cac": 25000}
    }
    
    st.subheader("📊 Данные по тарифным планам")
    
    for plan, data in plans_data.items():
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.write(f"**{plan}**")
        with col2:
            st.metric("Цена/мес", f"{data['price']:,} руб")
        with col3:
            st.metric("Отток/мес", f"{data['churn']:.1f}%")
        with col4:
            st.metric("Конверсия", f"{data['conversion']:.0f}%")
        with col5:
            st.metric("СПК", f"{data['cac']:,} руб")
    
    # Расчет ПЦК для каждого плана
    st.subheader("💡 Анализ ПЦК по планам")
    
    analysis_data = []
    for plan, data in plans_data.items():
        # ПЦК = месячная выручка / месячный отток
        ltv = (data['price'] * 0.8) / (data['churn'] / 100)  # 80% маржа
        ratio = ltv / data['cac']
        payback = data['cac'] / (data['price'] * 0.8)
        
        analysis_data.append({
            'План': plan,
            'ПЦК': f"{ltv:,.0f} руб",
            'ПЦК/СПК': f"{ratio:.1f}:1",
            'Окупаемость': f"{payback:.1f} мес",
            'Статус': '🟢 Хорошо' if ratio > 3 else '🟡 Средне' if ratio > 2 else '🔴 Плохо'
        })
    
    df_analysis = pd.DataFrame(analysis_data)
    st.dataframe(df_analysis, use_container_width=True)
    
    # Рекомендации
    st.subheader("🎯 Стратегические рекомендации")
    
    best_plan = max(plans_data.keys(), 
                   key=lambda p: ((plans_data[p]['price'] * 0.8) / (plans_data[p]['churn'] / 100)) / plans_data[p]['cac'])
    
    st.success(f"""
    **Ключевые инсайты**:
    
    1. **Лучший план для масштабирования**: {best_plan}
    2. **Парадокс SaaS**: Дорогие планы часто имеют лучший ПЦК/СПК из-за низкого оттока
    3. **Стратегия**: Фокус на upsell существующих клиентов в более дорогие планы
    4. **Оптимизация**: Снижение оттока на 1% эквивалентно росту ПЦК на 10-15%
    """)

def ecommerce_case():
    """Кейс электронной коммерции"""
    st.subheader("🛍️ Кейс: Интернет-магазин одежды")
    
    st.markdown("""
    **Вызов**: У интернет-магазина одежды проблемы с unit economics. 
    Нужно понять, какие категории и каналы приносят прибыль.
    """)
    
    # Данные по категориям
    categories = {
        "Женская одежда": {"aov": 3500, "frequency": 2.5, "margin": 60, "cac": 800},
        "Мужская одежда": {"aov": 4200, "frequency": 1.8, "margin": 55, "cac": 1200},
        "Обувь": {"aov": 6000, "frequency": 1.2, "margin": 70, "cac": 1500},
        "Аксессуары": {"aov": 1200, "frequency": 4.0, "margin": 80, "cac": 400}
    }
    
    st.subheader("📊 Метрики по категориям товаров")
    
    category_analysis = []
    for category, data in categories.items():
        # Годовая выручка с клиента
        annual_revenue = data['aov'] * data['frequency']
        # Годовая прибыль
        annual_profit = annual_revenue * (data['margin'] / 100)
        # Простой ПЦК (без учета многолетнего поведения)
        ltv = annual_profit
        ratio = ltv / data['cac']
        
        category_analysis.append({
            'Категория': category,
            'Средний чек': f"{data['aov']:,} руб",
            'Частота/год': f"{data['frequency']:.1f}",
            'Маржа': f"{data['margin']}%",
            'СПК': f"{data['cac']:,} руб",
            'Годовой ПЦК': f"{ltv:,.0f} руб",
            'ПЦК/СПК': f"{ratio:.1f}:1"
        })
    
    df_categories = pd.DataFrame(category_analysis)
    st.dataframe(df_categories, use_container_width=True)
    
    # Сезонный анализ
    st.subheader("📅 Влияние сезонности")
    
    seasonal_impact = st.slider("Сезонный фактор (Q4 vs Q1)", 1.0, 3.0, 2.2, 0.1)
    
    st.info(f"""
    **Сезонный эффект**: В Q4 средний чек увеличивается в {seasonal_impact:.1f} раза,
    но СПК также растет из-за конкуренции на ~40%.
    
    **Стратегия**: Накапливать бюджет для агрессивного масштабирования в высокий сезон.
    """)

def mobile_app_case():
    """Кейс мобильного приложения"""
    st.subheader("📱 Кейс: Мобильное приложение для фитнеса")
    
    st.markdown("""
    **Специфика**: Freemium модель с подпиской. Основная монетизация через 
    конверсию в платную версию и удержание подписчиков.
    """)
    
    # Воронка конверсии
    funnel_data = {
        "Установки": 10000,
        "Регистрации": 6000,  # 60% conversion rate
        "Активные 7 дней": 3000,  # 50% retention 
        "Платные подписки": 300,  # 10% conversion to paid
        "СПК за установку": 25,
        "СПК за подписку": 250
    }
    
    st.subheader("🎯 Воронка конверсии приложения")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Установки", f"{funnel_data['Установки']:,}")
        st.metric("СПК за установку", f"{funnel_data['СПК за установку']} руб")
        
    with col2:
        st.metric("Активные 7 дней", f"{funnel_data['Активные 7 дней']:,}")
        retention_7d = funnel_data['Активные 7 дней'] / funnel_data['Регистрации']
        st.metric("Удержание 7 дней", f"{retention_7d:.1%}")
        
    with col3:
        st.metric("Платные подписки", f"{funnel_data['Платные подписки']:,}")
        st.metric("СПК за подписку", f"{funnel_data['СПК за подписку']} руб")
    
    # Расчет ПЦК
    subscription_price = st.slider("Цена подписки (руб/мес)", 200, 1000, 400)
    monthly_churn = st.slider("Месячный отток подписчиков (%)", 5, 25, 12)
    
    # ПЦК подписчика
    ltv_subscriber = (subscription_price * 0.7) / (monthly_churn / 100)  # 70% после комиссий
    
    # Общий ПЦК с учетом конверсии
    conversion_to_paid = funnel_data['Платные подписки'] / funnel_data['Активные 7 дней']
    ltv_total = ltv_subscriber * conversion_to_paid
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("ПЦК подписчика", f"{ltv_subscriber:,.0f} руб")
        ratio_subscriber = ltv_subscriber / funnel_data['СПК за подписку']
        st.metric("ПЦК/СПК подписчика", f"{ratio_subscriber:.1f}:1")
        
    with col2:
        st.metric("Общий ПЦК с установки", f"{ltv_total:,.0f} руб")
        ratio_total = ltv_total / funnel_data['СПК за установку']
        st.metric("Общий ПЦК/СПК", f"{ratio_total:.1f}:1")
    
    # Рекомендации
    st.subheader("🎯 Рекомендации по оптимизации")
    
    if ratio_subscriber < 3:
        st.error("🚨 Критически низкий ПЦК/СПК подписчиков! Нужно снижать отток или повышать цену.")
    
    if conversion_to_paid < 0.15:
        st.warning("⚠️ Низкая конверсия в платную версию. Улучшайте onboarding и value proposition.")
    
    st.info(f"""
    **Мобильные приложения - специфика**:
    
    1. **Двойная воронка**: Установка → Активация → Монетизация
    2. **Ключевая метрика**: Конверсия в платную версию ({conversion_to_paid:.1%})
    3. **Фокус на retention**: Снижение оттока на 1% = рост ПЦК на ~8%
    4. **Сезонность**: Январь (новогодние обещания) vs лето (пляжный сезон)
    """)

def b2b_case():
    """Кейс B2B сервиса"""
    st.subheader("🏢 Кейс: B2B платформа для управления проектами")
    
    st.markdown("""
    **Специфика B2B**: Длинный цикл продаж, высокие чеки, сложная структура принятия решений.
    Важно учитывать полную стоимость продаж, включая работу менеджеров.
    """)
    
    # Сегменты клиентов
    segments = {
        "SMB (10-50 сотр.)": {
            "deal_size": 15000, "sales_cycle": 2, "close_rate": 25, 
            "churn_annual": 20, "expansion_revenue": 1.2
        },
        "Mid-market (50-200)": {
            "deal_size": 45000, "sales_cycle": 4, "close_rate": 15,
            "churn_annual": 12, "expansion_revenue": 1.5  
        },
        "Enterprise (200+)": {
            "deal_size": 150000, "sales_cycle": 8, "close_rate": 8,
            "churn_annual": 8, "expansion_revenue": 2.0
        }
    }
    
    st.subheader("📊 Сегменты клиентов")
    
    # Затраты на продажи
    sales_costs = {
        "Зарплата менеджера": 120000,  # в месяц
        "Маркетинг (лиды)": 800,      # за лид
        "Демо/презентации": 5000,     # за возможность
        "Поездки/встречи": 15000      # на крупную сделку
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**💰 Настройка затрат на продажи**")
        for cost_type, value in sales_costs.items():
            sales_costs[cost_type] = st.number_input(
                cost_type, value=value, key=f"cost_{cost_type}")
    
    with col2:
        st.markdown("**⚙️ Настройка сегментов**")
        selected_segment = st.selectbox("Выберите сегмент для анализа:", list(segments.keys()))
    
    # Расчет полной стоимости привлечения клиента
    segment_data = segments[selected_segment]
    
    # Количество лидов для закрытия одной сделки
    leads_per_deal = 100 / segment_data['close_rate']
    
    # Стоимость работы менеджера на одну сделку
    manager_cost_per_deal = (sales_costs['Зарплата менеджера'] / 30) * segment_data['sales_cycle'] * 30
    
    # Полный САК
    full_cac = (
        leads_per_deal * sales_costs['Маркетинг (лиды)'] +
        manager_cost_per_deal +
        sales_costs['Демо/презентации'] * (leads_per_deal / 10) +  # 10% доходят до демо
        (sales_costs['Поездки/встречи'] if segment_data['deal_size'] > 50000 else 0)
    )
    
    # Расчет ПЦК с учетом expansion revenue
    annual_revenue = segment_data['deal_size']
    annual_churn = segment_data['churn_annual'] / 100
    years_lifetime = 1 / annual_churn
    
    # С учетом роста выручки (upsell/cross-sell)
    total_ltv = 0
    for year in range(1, min(int(years_lifetime) + 2, 6)):  # До 5 лет
        year_revenue = annual_revenue * (segment_data['expansion_revenue'] ** (year - 1))
        survival_rate = (1 - annual_churn) ** (year - 1)
        total_ltv += year_revenue * survival_rate * 0.8  # 80% маржа
    
    # Результаты анализа
    st.subheader(f"📈 Анализ сегмента: {selected_segment}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Размер сделки", f"{segment_data['deal_size']:,} руб")
        st.metric("Цикл продаж", f"{segment_data['sales_cycle']} мес")
    
    with col2:
        st.metric("Коэффициент закрытия", f"{segment_data['close_rate']}%")
        st.metric("Годовой отток", f"{segment_data['churn_annual']}%")
    
    with col3:
        st.metric("Полный СПК", f"{full_cac:,.0f} руб")
        st.metric("Лидов на сделку", f"{leads_per_deal:.0f}")
    
    with col4:
        st.metric("ПЦК", f"{total_ltv:,.0f} руб")
        ratio = total_ltv / full_cac
        st.metric("ПЦК/СПК", f"{ratio:.1f}:1")
    
    # Детализация СПК
    st.subheader("🔍 Детализация СПК")
    
    cac_breakdown = {
        "Генерация лидов": leads_per_deal * sales_costs['Маркетинг (лиды)'],
        "Работа менеджера": manager_cost_per_deal,
        "Демо и презентации": sales_costs['Демо/презентации'] * (leads_per_deal / 10),
        "Поездки/встречи": sales_costs['Поездки/встречи'] if segment_data['deal_size'] > 50000 else 0
    }
    
    # График структуры СПК
    fig = go.Figure(data=[go.Pie(
        labels=list(cac_breakdown.keys()),
        values=list(cac_breakdown.values()),
        hole=0.3
    )])
    
    fig.update_layout(
        title="Структура полного СПК",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Рекомендации
    st.subheader("💡 Стратегические рекомендации")
    
    if ratio > 5:
        st.success(f"🎉 Отличные показатели для B2B! Можно масштабировать {selected_segment} сегмент.")
    elif ratio > 3:
        st.info(f"👍 Хорошие показатели. Есть потенциал для оптимизации процесса продаж.")
    else:
        st.warning(f"⚠️ Низкие показатели. Нужно пересматривать стратегию для {selected_segment}.")
    
    # Сценарий оптимизации
    st.subheader("🚀 Сценарий оптимизации")
    
    optimization_levers = {
        "Увеличение конверсии на 20%": {"close_rate": 1.2, "effect": "Снижение СПК"},
        "Сокращение цикла продаж на 1 месяц": {"sales_cycle": -1, "effect": "Снижение затрат менеджера"},
        "Повышение retention на 5%": {"churn": -5, "effect": "Увеличение ПЦК"},
        "Рост expansion revenue до 150%": {"expansion": 1.5, "effect": "Увеличение ПЦК"}
    }
    
    selected_optimization = st.selectbox("Выберите рычаг оптимизации:", list(optimization_levers.keys()))
    
    if st.button("Рассчитать эффект"):
        st.success(f"📊 {selected_optimization} может улучшить ПЦК/СПК на 15-30%")

def subscription_case():
    """Кейс подписочного сервиса"""
    st.subheader("📺 Кейс: Подписочный стриминг-сервис")
    
    st.markdown("""
    **Модель**: Netflix-подобный сервис с несколькими тарифами и family sharing.
    Ключевые метрики: время до первого просмотра, engagement, family account usage.
    """)
    
    # Тарифные планы
    subscription_tiers = {
        "Базовый (1 экран)": {"price": 299, "family_size": 1.0, "content_cost": 150},
        "Стандарт (2 экрана)": {"price": 499, "family_size": 1.8, "content_cost": 200},
        "Премиум (4 экрана)": {"price": 899, "family_size": 2.5, "content_cost": 300}
    }
    
    # Метрики engagement
    engagement_metrics = {
        "Время до первого просмотра": 24,  # часов
        "Среднее время просмотра": 2.5,    # часов в день
        "Контентный churn": 15,            # % пользователей без просмотров 30 дней
        "Сезонный фактор": 1.3             # зима vs лето
    }
    
    st.subheader("⚙️ Настройка метрик сервиса")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Engagement метрики**")
        for metric, value in engagement_metrics.items():
            if "время" in metric.lower():
                engagement_metrics[metric] = st.slider(f"{metric}", value*0.5, value*2, value)
            else:
                engagement_metrics[metric] = st.slider(f"{metric}", value*0.5, value*2, value)
    
    with col2:
        st.markdown("**💰 Настройка тарифов**")
        selected_tier = st.selectbox("Анализируемый тариф:", list(subscription_tiers.keys()))
        
        # СПК по каналам для стриминга
        streaming_cac = {
            "Контекстная реклама": 450,
            "Социальные сети": 380,
            "YouTube реклама": 520,
            "TV реклама": 180,
            "Influencer маркетинг": 650
        }
        
        selected_channel = st.selectbox("Канал привлечения:", list(streaming_cac.keys()))
        current_cac = streaming_cac[selected_channel]
    
    # Расчет ПЦК с учетом специфики стриминга
    tier_data = subscription_tiers[selected_tier]
    
    # Базовый месячный доход с учетом family sharing
    effective_revenue = tier_data['price'] / tier_data['family_size']
    net_revenue = effective_revenue - tier_data['content_cost']
    
    # Модель оттока на основе engagement
    base_churn = 8  # базовый месячный отток %
    
    # Engagement влияет на отток
    if engagement_metrics['Время до первого просмотра'] > 48:
        churn_multiplier = 1.5  # долго не начинают смотреть = выше отток
    elif engagement_metrics['Время до первого просмотра'] < 12:
        churn_multiplier = 0.7  # быстро начинают = ниже отток
    else:
        churn_multiplier = 1.0
    
    if engagement_metrics['Среднее время просмотра'] < 1:
        churn_multiplier *= 1.3  # мало смотрят = выше отток
    elif engagement_metrics['Среднее время просмотра'] > 3:
        churn_multiplier *= 0.8  # много смотрят = ниже отток
    
    effective_churn = base_churn * churn_multiplier
    
    # ПЦК с учетом сезонности
    ltv_summer = net_revenue / (effective_churn * 1.2 / 100)  # летом смотрят меньше
    ltv_winter = net_revenue / (effective_churn * 0.8 / 100)  # зимой больше
    
    avg_ltv = (ltv_summer + ltv_winter) / 2
    
    # Результаты
    st.subheader(f"📈 Анализ: {selected_tier} + {selected_channel}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Цена тарифа", f"{tier_data['price']} руб")
        st.metric("Family sharing", f"{tier_data['family_size']:.1f}")
    
    with col2:
        st.metric("Эффективный доход", f"{effective_revenue:.0f} руб")
        st.metric("Чистый доход", f"{net_revenue:.0f} руб")
    
    with col3:
        st.metric("СПК канала", f"{current_cac} руб")
        st.metric("Эффективный отток", f"{effective_churn:.1f}%")
    
    with col4:
        st.metric("Средний ПЦК", f"{avg_ltv:,.0f} руб")
        ratio = avg_ltv / current_cac
        st.metric("ПЦК/СПК", f"{ratio:.1f}:1")
    
    # Сезонная динамика
    st.subheader("📅 Сезонная динамика")
    
    months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 
              'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
    
    # Сезонные коэффициенты (зима выше, лето ниже)
    seasonal_coeffs = [1.3, 1.4, 1.2, 1.0, 0.8, 0.7, 0.6, 0.7, 0.9, 1.1, 1.2, 1.4]
    
    monthly_ltv = [avg_ltv * coeff for coeff in seasonal_coeffs]
    monthly_ratio = [ltv / current_cac for ltv in monthly_ltv]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=monthly_ratio,
        mode='lines+markers',
        name='ПЦК/СПК по месяцам',
        line=dict(color='blue', width=3),
        marker=dict(size=8)
    ))
    
    # Линия минимального порога
    fig.add_hline(y=3, line_dash="dash", line_color="green", 
                  annotation_text="Минимальный порог 3:1")
    fig.add_hline(y=2, line_dash="dash", line_color="red",
                  annotation_text="Критический порог 2:1")
    
    fig.update_layout(
        title="Сезонные колебания ПЦК/СПК",
        xaxis_title="Месяц",
        yaxis_title="ПЦК/СПК",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Специфические рекомендации для стриминга
    st.subheader("🎯 Рекомендации для стриминга")
    
    critical_months = [i for i, ratio in enumerate(monthly_ratio) if ratio < 2]
    
    if critical_months:
        month_names = [months[i] for i in critical_months]
        st.error(f"🚨 Критические месяцы: {', '.join(month_names)}. Рассмотрите снижение СПК или спец.предложения.")
    
    st.info(f"""
    **Стриминг-специфика**:
    
    1. **Family sharing убивает unit economics**: Эффективный доход {effective_revenue:.0f} руб вместо {tier_data['price']} руб
    2. **Content costs растут**: Нужно постоянно инвестировать в контент
    3. **Engagement = retention**: Время до первого просмотра критично
    4. **Сезонность**: Зимой ПЦК выше на 30-40%
    5. **Конкуренция**: Легко переключиться к конкурентам
    
    **Стратегии оптимизации**:
    - Ограничить family sharing (например, геолокация)
    - Персонализация контента для быстрого engagement
    - Сезонные акции в слабые месяцы
    - Эксклюзивный контент для retention
    """)

# Запуск приложения
if __name__ == "__main__":
    main()