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

