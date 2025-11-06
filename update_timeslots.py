#!/usr/bin/env python
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from schedule_app.models import TimeSlot
from datetime import time

# Удаляем старые временные слоты
TimeSlot.objects.all().delete()

# Создаем новые временные слоты
timeslots_data = [
    (1, time(9, 0), time(10, 20)),    # 1 пара: 9:00-10:20
    (2, time(10, 30), time(11, 50)),  # 2 пара: 10:30-11:50
    (3, time(12, 0), time(13, 20)),   # 3 пара: 12:00-13:20
    (4, time(14, 0), time(15, 20)),   # 4 пара: 14:00-15:20
    (5, time(15, 30), time(16, 50)),  # 5 пара: 15:30-16:50
    (6, time(17, 0), time(18, 20)),   # 6 пара: 17:00-18:20
]

for number, start_time, end_time in timeslots_data:
    TimeSlot.objects.create(
        number=number,
        start_time=start_time,
        end_time=end_time,
        is_active=True
    )
    print(f"Создан временной слот {number}: {start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}")

print("Временные слоты успешно обновлены!")