#!/usr/bin/env python
import os
import django
import sqlite3

# Подключаемся напрямую к SQLite базе
db_path = r'C:\Users\Ибро\Desktop\Projects\college\backend\db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print('=== Current rooms ===')
cursor.execute("SELECT id, number, building FROM schedule_app_room")
rooms = cursor.fetchall()

for room_id, number, building in rooms:
    print(f'{room_id}: {building}-{number}')

print('\n=== Updating room numbers to be unique ===')
# Обновляем номера аудиторий, включив корпус в номер
for room_id, number, building in rooms:
    new_number = f'{building}-{number}'
    cursor.execute("UPDATE schedule_app_room SET number = ? WHERE id = ?", (new_number, room_id))
    print(f'Updated room {room_id}: {number} -> {new_number}')

conn.commit()
conn.close()
print('Rooms updated successfully!')