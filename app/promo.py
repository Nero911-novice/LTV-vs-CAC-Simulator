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

