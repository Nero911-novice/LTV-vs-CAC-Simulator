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
        timeline = st.slider("Время до окупаемости (месяцев)", 6, 36, 18)
    
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

