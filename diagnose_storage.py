import os, sys, django
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.core.files.storage import default_storage
from django.core.files import File
from django.conf import settings

print("=" * 60)
print("🔍 Диагностика Django Storage")
print("=" * 60)

print(f"\nUse Spaces: {os.getenv('USE_SPACES')}")
if hasattr(settings, 'STORAGES'):
    print(f"Storage Backend: {settings.STORAGES.get('default', {}).get('BACKEND', 'N/A')}")
elif hasattr(settings, 'DEFAULT_FILE_STORAGE'):
    print(f"Storage Backend: {settings.DEFAULT_FILE_STORAGE}")
print(f"Media URL: {settings.MEDIA_URL}")

print(f"\nStorage class: {default_storage.__class__.__name__}")
print(f"Storage location: {getattr(default_storage, 'location', 'N/A')}")
if hasattr(default_storage, 'bucket_name'):
    print(f"Bucket name: {default_storage.bucket_name}")
if hasattr(default_storage, 'endpoint_url'):
    print(f"Endpoint: {default_storage.endpoint_url}")

# Пробуем загрузить один файл
BASE_DIR = Path(__file__).resolve().parent
test_file = BASE_DIR / 'media' / 'council' / 'members' / 'president.jpg'

if test_file.exists():
    print(f"\n{'=' * 60}")
    print(f"🧪 Тест загрузки файла")
    print(f"{'=' * 60}")
    print(f"\nФайл: {test_file}")
    print(f"Размер: {test_file.stat().st_size} bytes")
    
    try:
        with open(test_file, 'rb') as f:
            django_file = File(f, name='president.jpg')
            spaces_path = 'council/members/president.jpg'
            
            print(f"\n📤 Загружаем как: {spaces_path}")
            
            # Удаляем если есть
            if default_storage.exists(spaces_path):
                print(f"   Удаляем старый файл...")
                default_storage.delete(spaces_path)
            
            saved_name = default_storage.save(spaces_path, django_file)
            print(f"✅ Сохранено как: {saved_name}")
            
            url = default_storage.url(saved_name)
            print(f"✅ URL: {url}")
            
            # Проверяем через boto3
            import boto3
            client = boto3.client(
                's3',
                region_name=os.getenv('SPACES_REGION'),
                endpoint_url=os.getenv('SPACES_ENDPOINT'),
                aws_access_key_id=os.getenv('SPACES_KEY'),
                aws_secret_access_key=os.getenv('SPACES_SECRET')
            )
            
            try:
                response = client.head_object(Bucket='su-college', Key=saved_name)
                print(f"✅ ФАЙЛ РЕАЛЬНО ЕСТЬ В SPACES! Размер: {response['ContentLength']} bytes")
            except:
                print(f"❌ ФАЙЛА НЕТ В SPACES!")
                
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"\n❌ Тестовый файл не найден: {test_file}")
