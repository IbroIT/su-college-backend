#!/usr/bin/env python
"""
Скрипт для импорта данных из SQLite в PostgreSQL на Heroku
"""
import subprocess
import sys

print("=" * 60)
print("📦 Импорт данных в Heroku PostgreSQL")
print("=" * 60)

# Экспортируем данные
print("\n1️⃣ Экспортируем данные из SQLite...")
result = subprocess.run([
    sys.executable, "manage.py", "dumpdata",
    "teachers", "news_app", "council_app", "projects_app", 
    "resources_app", "vacancies_app", "schedule_app",
    "--natural-foreign", "--natural-primary",
    "--format=json", "--indent=2"
], capture_output=True, text=True, encoding='utf-8')

if result.returncode != 0:
    print(f"❌ Ошибка экспорта: {result.stderr}")
    sys.exit(1)

# Сохраняем с правильной кодировкой
print("2️⃣ Сохраняем данные...")
with open('data_export.json', 'w', encoding='utf-8') as f:
    f.write(result.stdout)

print("✅ Данные экспортированы в data_export.json")
print("\n📋 Следующие шаги:")
print("1. git add data_export.json")
print("2. git commit -m 'Add data export'")
print("3. git push heroku main")
print("4. heroku run python manage.py loaddata data_export.json")
