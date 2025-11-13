import os, sys, django
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

print("=" * 60)
print("🧪 Тест загрузки изображения")
print("=" * 60)

# Создаем тестовое изображение
img = Image.new('RGB', (100, 100), color='red')
img_io = BytesIO()
img.save(img_io, format='JPEG')
img_io.seek(0)

test_filename = "teachers/test_photo.jpg"

print(f"\n📤 Загружаем: {test_filename}")

try:
    # Удаляем если существует
    if default_storage.exists(test_filename):
        print(f"   Удаляем старый файл...")
        default_storage.delete(test_filename)
    
    # Загружаем
    saved_path = default_storage.save(test_filename, ContentFile(img_io.read()))
    print(f"✅ Сохранено как: {saved_path}")
    
    # Получаем URL
    url = default_storage.url(saved_path)
    print(f"✅ URL: {url}")
    
    print(f"\n🌐 Откройте в браузере:")
    print(f"   {url}")
    print(f"\n   Должно показать красное изображение 100x100px")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()

# Показываем все файлы
print("\n" + "=" * 60)
print("📁 Все файлы в bucket:")
print("=" * 60)

import boto3
client = boto3.client(
    's3',
    region_name=os.getenv('SPACES_REGION'),
    endpoint_url=os.getenv('SPACES_ENDPOINT'),
    aws_access_key_id=os.getenv('SPACES_KEY'),
    aws_secret_access_key=os.getenv('SPACES_SECRET')
)

response = client.list_objects_v2(Bucket='su-college')
for obj in response.get('Contents', []):
    url = f"https://su-college.blr1.digitaloceanspaces.com/{obj['Key']}"
    print(f"\n  📄 {obj['Key']}")
    print(f"     🌐 {url}")
