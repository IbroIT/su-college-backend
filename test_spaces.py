import os
import sys
import django
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

print("=" * 60)
print("🔍 Проверка настроек DigitalOcean Spaces")
print("=" * 60)

print(f"\n✅ USE_SPACES: {os.getenv('USE_SPACES')}")
print(f"✅ SPACES_NAME: {os.getenv('SPACES_NAME')}")
print(f"✅ SPACES_REGION: {os.getenv('SPACES_REGION')}")
print(f"✅ SPACES_ENDPOINT: {os.getenv('SPACES_ENDPOINT')}")
print(f"✅ SPACES_KEY: {os.getenv('SPACES_KEY')[:10]}...")

print("\n" + "=" * 60)
print("🔍 Django Settings")
print("=" * 60)

if hasattr(settings, 'AWS_ACCESS_KEY_ID'):
    print(f"✅ AWS_ACCESS_KEY_ID: {settings.AWS_ACCESS_KEY_ID[:10]}...")
    print(f"✅ AWS_STORAGE_BUCKET_NAME: {settings.AWS_STORAGE_BUCKET_NAME}")
    print(f"✅ AWS_S3_REGION_NAME: {settings.AWS_S3_REGION_NAME}")
    print(f"✅ AWS_S3_ENDPOINT_URL: {settings.AWS_S3_ENDPOINT_URL}")
    print(f"✅ AWS_S3_CUSTOM_DOMAIN: {settings.AWS_S3_CUSTOM_DOMAIN}")
    print(f"✅ MEDIA_URL: {settings.MEDIA_URL}")
    print(f"✅ DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
else:
    print("❌ DigitalOcean Spaces НЕ активирован!")
    print(f"   USE_SPACES = {os.getenv('USE_SPACES')}")

print("\n" + "=" * 60)
print("🧪 Тестирование подключения")
print("=" * 60)

try:
    storage = S3Boto3Storage()
    print("✅ Storage инициализирован успешно!")
    
    # Попробуем получить список файлов
    try:
        # Проверяем доступ к bucket
        connection = storage.connection
        bucket = connection.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        print(f"✅ Подключение к bucket '{settings.AWS_STORAGE_BUCKET_NAME}' успешно!")
        
        # Получаем первые 5 файлов
        files = list(bucket.objects.limit(5))
        print(f"✅ В bucket найдено файлов: {len(files)}")
        if files:
            print("\nПервые файлы:")
            for obj in files:
                print(f"  - {obj.key}")
        
    except Exception as e:
        print(f"⚠️  Ошибка при доступе к bucket: {e}")
        
except Exception as e:
    print(f"❌ Ошибка при инициализации Storage: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
