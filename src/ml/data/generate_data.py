import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()


n_samples = 1000
data = []

for _ in range(n_samples):
    # Дата (за последние 30 дней)
    date = fake.date_between(start_date='-30d', end_date='today')

    # День недели (0=Пн, 6=Вс)
    day_of_week = pd.to_datetime(date).dayofweek

    # Выполнена ли привычка сегодня (бинарно)
    habit_today = np.random.choice([0, 1], p=[0.3, 0.7])

    # Серия дней (зависит от предыдущих дней)
    streak = np.random.randint(0, 15) if habit_today else 0

    # Количество заметок (0-5)
    notes = np.random.randint(0, 8)

    # Целевая переменная (мотивация: 0-1)
    motivation = (
        0.4 * (streak / 15)
        + 0.3 * habit_today
        + 0.2 * (notes / 5)
        + 0.1 * np.random.rand()
    )
    motivation = np.clip(motivation, 0, 1)

    data.append([date, day_of_week, habit_today, streak, notes, motivation])

df = pd.DataFrame(
    data,
    columns=[
        'date',
        'day_of_week',
        'habit_today',
        'streak_days',
        'notes',
        'motivation',
    ],
)

# Сохраняем в CSV
df.to_csv('habits_data.csv', index=False)
