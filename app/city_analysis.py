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

