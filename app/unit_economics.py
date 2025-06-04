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
def show_ride_hailing_sidebar():
    """Справочная информация для ride-hailing"""
    with st.expander("📖 Ride-Hailing метрики"):
        st.markdown("""
        **AOV** - Average Order Value (средний чек поездки)
        **Комиссия с заказа** - комиссия платформы с поездки
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
    **Специфика ride-hailing**: вместо подписок у нас поездки, вместо валовой маржи - комиссия с заказа, 
    ключевая метрика - частота использования.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚗 Параметры поездок")
        
        aov = st.slider("Средний чек поездки (AOV)", 150, 800, 350, 25)
        take_rate = st.slider("Комиссия с заказа (%)", 15, 35, 25, 1)
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
        subplot_titles=('Влияние частоты поездок', 'Влияние комиссии с заказа', 
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
    
    # График 2: Комиссия с заказа
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
        'Параметр': ['Частота поездок', 'Комиссия с заказа', 'Средний чек'],
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
    fig.update_xaxes(title_text="Комиссия с заказа (%)", row=1, col=2)
    fig.update_xaxes(title_text="AOV (руб)", row=2, col=1)
    fig.update_xaxes(title_text="Параметр", row=2, col=2)
    fig.update_yaxes(title_text="LTV (руб)")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Инсайты для ride-hailing
    st.info(f"""
    💡 **Ключевые инсайты для ride-hailing**:
    
    1. **Частота - король**: Увеличение поездок с {frequency} до {frequency*1.5:.1f} в месяц 
       повышает LTV на {((max(ltv_frequency)/min(ltv_frequency) - 1) * 100):.0f}%
    
    2. **Комиссия с заказа имеет пределы**: Повышение комиссии увеличивает LTV, но снижает конкурентоспособность
    
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
