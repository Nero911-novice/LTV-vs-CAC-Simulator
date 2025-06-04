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
def rider_cohort_analysis():
    """Когортный анализ водителей"""
    st.header("📈 Когортный анализ водителей")
    
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
    """Генерация данных когортного анализа для водителей"""
    
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
