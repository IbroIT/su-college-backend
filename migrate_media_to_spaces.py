import os
import sys
import django
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.core.files.storage import default_storage
from django.core.files import File

BASE_DIR = Path(__file__).resolve().parent
MEDIA_ROOT = BASE_DIR / 'media'

print("=" * 60)
print("📦 Миграция медиа файлов в DigitalOcean Spaces")
print("=" * 60)

# Считаем файлы
total_files = 0
uploaded_files = 0
skipped_files = 0
errors = 0

print(f"\n🔍 Сканирование папки: {MEDIA_ROOT}\n")

for root, dirs, files in os.walk(MEDIA_ROOT):
    for filename in files:
        total_files += 1
        local_path = Path(root) / filename
        
        # Получаем относительный путь от media/
        relative_path = local_path.relative_to(MEDIA_ROOT)
        spaces_path = str(relative_path).replace('\\', '/')
        
        try:
            # Проверяем, существует ли уже в Spaces
            if default_storage.exists(spaces_path):
                print(f"⏭️  Пропуск (уже есть): {spaces_path}")
                skipped_files += 1
                continue
            
            # Загружаем файл
            with open(local_path, 'rb') as f:
                django_file = File(f, name=filename)
                saved_name = default_storage.save(spaces_path, django_file)
                print(f"✅ Загружено: {spaces_path}")
                uploaded_files += 1
                
        except Exception as e:
            print(f"❌ Ошибка при загрузке {spaces_path}: {e}")
            errors += 1

print("\n" + "=" * 60)
print("📊 Результаты миграции")
print("=" * 60)
print(f"Всего файлов: {total_files}")
print(f"Загружено: {uploaded_files}")
print(f"Пропущено: {skipped_files}")
print(f"Ошибок: {errors}")
print("=" * 60)
