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

