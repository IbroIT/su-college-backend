import os, sys, django
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from backend.storage_backends import MediaStorage
from django.core.files.base import ContentFile

storage = MediaStorage()

print("🧪 Прямая загрузка через MediaStorage\n")

test_content = b"Direct upload test"
test_path = "direct_test.txt"

print(f"📤 Загружаем: {test_path}")
saved_name = storage.save(test_path, ContentFile(test_content))
print(f"✅ Сохранено как: {saved_name}")
print(f"✅ URL: {storage.url(saved_name)}")

# Теперь проверим через boto3
import boto3
client = boto3.client(
    's3',
    region_name=os.getenv('SPACES_REGION'),
    endpoint_url=os.getenv('SPACES_ENDPOINT'),
    aws_access_key_id=os.getenv('SPACES_KEY'),
    aws_secret_access_key=os.getenv('SPACES_SECRET')
)

print("\n🔍 Все файлы в bucket:\n")
response = client.list_objects_v2(Bucket='su-college')
for obj in response.get('Contents', []):
    print(f"  ✅ {obj['Key']}")
