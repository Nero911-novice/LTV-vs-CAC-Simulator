# 🚗 Ride-Hailing LTV/CAC Симулятор

**Специализированная платформа для анализа unit economics в каршеринге и такси**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

https://ltvcacsimulator.streamlit.app/

## 📋 О проекте

Ride-Hailing LTV/CAC Симулятор — это комплексный аналитический инструмент, специально разработанный для анализа unit economics в индустрии ride-hailing. В отличие от универсальных LTV/CAC калькуляторов, этот симулятор учитывает уникальные особенности двухсторонней модели такси и каршеринга.

### 🎯 Зачем нужен специализированный симулятор?

**Ride-hailing ≠ SaaS:**
- **Take rate** вместо валовой маржи (комиссия 20-30% с поездки)
- **Частота поездок** как ключевая метрика retention (не месячный churn)
- **Географическая специфика** — разные города = кардинально разные метрики
- **Промокоды** могут составлять 30-50% от CAC
- **Сезонность** влияет сильнее чем в других бизнесах
- **Supply-demand balance** — нужно привлекать и водителей, и пассажиров

## 🚀 Ключевые возможности

### 📊 **7 основных модулей анализа:**

1. **📈 Unit Economics калькулятор**
   - Расчет LTV/CAC с учетом специфики ride-hailing
   - Анализ чувствительности ключевых метрик
   - Метрика "поездок до окупаемости"
   - Индустриальные бенчмарки

2. **🏙️ Анализ по городам**
   - Сравнение метрик между городами
   - Стадии зрелости рынка
   - Потенциал экспансии
   - City-specific рекомендации

3. **📈 Когортный анализ райдеров**
   - Retention heatmap по месячным когортам
   - Revenue cohort analysis
   - Сезонные эффекты на лояльность
   - Time to second ride анализ

4. **🎪 Сценарное планирование**
   - Конкурентные войны и промо-кампании
   - Экономические кризисы
   - Регулирование и compliance
   - Пандемии и форс-мажоры
   - Развитие общественного транспорта
   - Запуск в новых городах

5. **💰 Оптимизатор промокодов**
   - Привлечение новых пользователей
   - Реактивация неактивных
   - Retention существующих
   - Конкурентная защита
   - Сегментированные промо-кампании

6. **🚀 Стратегия экспансии**
   - Региональные города
   - Международная экспансия
   - Малые города (Tier 2/3)
   - Вертикальная диверсификация

7. **📚 Кейсы из индустрии**
   - Реальные success stories
   - Анализ неудач и провалов
   - Промо-войны и их последствия
   - Нишевые стратегии

## 🛠 Установка и запуск

### Требования
- Python 3.8 или выше
- 2GB RAM
- Современный веб-браузер

### Быстрый старт

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/yourusername/ride-hailing-ltv-cac-simulator.git
cd ride-hailing-ltv-cac-simulator
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Запустите приложение:**
```bash
streamlit run ltv_cac_simulator.py
```

5. **Откройте браузер:**
```
http://localhost:8501
```

### requirements.txt
```txt
streamlit==1.28.2
numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.2
seaborn==0.12.2
plotly==5.17.0
```

## 📊 Основные метрики и KPI

### Ride-Hailing специфические метрики:
- **AOV (Average Order Value)** — средний чек поездки
- **Take Rate** — комиссия платформы с поездки (%)
- **Частота поездок** — поездок на пользователя в месяц
- **Time to 2nd ride** — время до второй поездки (активация)
- **CAC с учетом промокодов** — полная стоимость привлечения
- **LTV через частоту** — не churn rate, а frequency decay
- **Поездок до окупаемости** — сколько поездок нужно для ROI

### Индустриальные бенчмарки:
- **LTV/CAC соотношения:**
  - 🟢 Зрелые рынки: 3-5:1
  - 🟡 Растущие рынки: 2-3:1
  - 🔴 Новые рынки: 1.5-2:1

- **Частота использования:**
  - 🟢 Power users: 8+ поездок/месяц
  - 🟡 Regular users: 3-7 поездок/месяц
  - 🔴 Occasional users: 1-2 поездки/месяц

## 💡 Примеры использования

### 1. Оптимизация промо-бюджета
```python
# Сценарий: У вас 3 млн руб на промокоды
# Вопрос: Как распределить между новыми и retention?

# В модуле "Оптимизатор промокодов":
# - Новые пользователи: 40% скидка = LTV/CAC 2.8:1
# - Retention: 25% скидка = LTV/CAC 4.1:1
# Рекомендация: 70% на retention, 30% на новых
```

### 2. Выбор города для экспансии
```python
# Сценарий: Рассматриваете Казань vs Краснодар
# В модуле "Анализ по городам":

# Казань: население 1.3М, средний доход 45k
# - Потенциал: 195k пользователей
# - LTV/CAC: 3.2:1
# - Окупаемость: 14 месяцев

# Краснодар: население 900k, средний доход 52k
# - Потенциал: 180k пользователей  
# - LTV/CAC: 3.8:1
# - Окупаемость: 11 месяцев

# Рекомендация: Краснодар (лучше unit economics)
```

### 3. Антикризисное планирование
```python
# Сценарий: Экономический кризис, доходы падают на 25%
# В модуле "Сценарное планирование":

# Моделирование:
# - Падение частоты с 4.2 до 3.1 поездок/месяц
# - Рост price sensitivity в 1.8x
# - Снижение AOV с 350 до 280 руб

# Стратегии адаптации:
# 1. Скидки 25% для поддержки спроса
# 2. Фокус на B2B сегмент (менее чувствителен)
# 3. Оптимизация costs на 30%
```

## 🔧 Кастомизация под вашу компанию

### Адаптация метрик:
```python
# В файле ltv_cac_simulator.py найдите секцию:
# "# Базовые метрики для вашего города"

base_aov = 350  # Замените на ваш средний чек
base_take_rate = 25  # Ваша комиссия
base_frequency = 4.5  # Ваша частота поездок
base_cac = 1500  # Ваш CAC
```

### Добавление городов:
```python
# В функции setup_cities_data() добавьте:
"Ваш_Город": {
    "population": 1_000_000,
    "aov": 320,
    "frequency": 3.8,
    "take_rate": 24,
    "cac": 1200,
    "competition": 4,
    "maturity": "Растущий"
}
```

## 📈 Продвинутые возможности

### Когортный анализ с сезонностью
- Автоматический учет сезонных эффектов
- Зимние когорты vs летние
- Влияние праздников на retention

### Географическая сегментация
- Анализ по районам города
- Urban vs suburban patterns
- Транспортная доступность

### Competitive intelligence
- Моделирование конкурентных угроз
- Defensive стратегии
- Market share dynamics

## 🤝 Кейсы применения

### Для Product Managers:
- Приоритизация features на основе impact на LTV
- A/B тестирование промо-механик
- User journey optimization

### Для Growth Teams:
- Channel attribution и CAC optimization
- Referral program design
- Retention strategy development

### Для Finance Teams:
- Unit economics forecasting
- Budget allocation optimization
- Scenario planning для board presentations

### Для Strategy Teams:
- Market entry decisions
- Competitive positioning
- M&A evaluation

## 📚 Документация модулей

### Unit Economics Calculator
Базовые расчеты с учетом специфики ride-hailing:
- LTV через frequency decay (не churn rate)
- CAC с учетом промокодов
- Операционные расходы на пользователя
- Sensitivity analysis по ключевым параметрам

### Promo Optimizer
Оптимизация промо-кампаний:
- ROI по типам промо
- Сегментация аудитории
- Elasticity analysis
- Budget allocation recommendations

### Scenario Planning
Моделирование бизнес-сценариев:
- Financial impact assessment
- Risk mitigation strategies
- Timeline planning
- Resource requirements

## 🚀 Deployment

### Streamlit Cloud (рекомендуется)
1. Загрузите код на GitHub
2. Подключите репозиторий к [Streamlit Cloud](https://streamlit.io/cloud)
3. Автоматический деплой при push

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "ltv_cac_simulator.py"]
```

### Heroku
```bash
# Создайте Procfile:
web: streamlit run ltv_cac_simulator.py --server.port=$PORT --server.address=0.0.0.0
```

## 🔒 Безопасность и конфиденциальность

- **Локальные расчеты**: Все вычисления происходят в браузере
- **Нет сохранения данных**: Данные не передаются на сервер
- **Open source**: Код доступен для аудита
- **Synthetic data**: Используются синтетические данные для демонстрации

## 🐛 Известные ограничения

1. **Simplified model**: Реальный мир сложнее математических моделей
2. **Historical data**: Модель основана на исторических паттернах
3. **Market dynamics**: Не учитывает резкие изменения рынка
4. **Local specifics**: Требует адаптации под местные особенности




