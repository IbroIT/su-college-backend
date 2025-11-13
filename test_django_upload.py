import os
import sys
import django
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings

print("=" * 60)
print("🧪 Тест загрузки файла в DigitalOcean Spaces")
print("=" * 60)

print(f"\n✅ USE_SPACES: {os.getenv('USE_SPACES')}")
print(f"✅ DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
print(f"✅ MEDIA_URL: {settings.MEDIA_URL}")

# Создаем тестовый файл
test_content = b"Test image content from Django"
test_filename = "teachers/test_photo.txt"

print(f"\n📤 Загружаем файл: {test_filename}")

try:
    # Удаляем старый файл если есть
    if default_storage.exists(test_filename):
        print(f"   Удаляем старый файл...")
        default_storage.delete(test_filename)
    
    # Загружаем новый файл
    saved_path = default_storage.save(test_filename, ContentFile(test_content))
    print(f"✅ Файл сохранен как: {saved_path}")
    
    # Получаем URL
    file_url = default_storage.url(saved_path)
    print(f"✅ URL файла: {file_url}")
    
    # Проверяем существование
    if default_storage.exists(saved_path):
        print(f"✅ Файл существует в storage")
        
        # Получаем размер
        size = default_storage.size(saved_path)
        print(f"✅ Размер файла: {size} bytes")
    else:
        print(f"❌ Файл НЕ найден в storage")
    
    print(f"\n🌐 Попробуйте открыть в браузере:")
    print(f"   {file_url}")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
