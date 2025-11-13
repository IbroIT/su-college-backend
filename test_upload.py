import boto3
import os
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

session = boto3.session.Session()
client = session.client(
    's3',
    region_name=os.getenv('SPACES_REGION'),
    endpoint_url=os.getenv('SPACES_ENDPOINT'),
    aws_access_key_id=os.getenv('SPACES_KEY'),
    aws_secret_access_key=os.getenv('SPACES_SECRET')
)

bucket_name = os.getenv('SPACES_NAME')
test_file_key = 'media/test.txt'
test_content = b'Test file from Django backend'

print(f"🔍 Проверка bucket: {bucket_name}")
print(f"   Region: {os.getenv('SPACES_REGION')}")
print(f"   Endpoint: {os.getenv('SPACES_ENDPOINT')}\n")

# Пробуем загрузить тестовый файл
print(f"📤 Загружаем тестовый файл: {test_file_key}...")
try:
    client.put_object(
        Bucket=bucket_name,
        Key=test_file_key,
        Body=BytesIO(test_content),
        ACL='public-read',
        ContentType='text/plain'
    )
    print("✅ Файл успешно загружен!")
    
    # Формируем URL
    url = f"https://{bucket_name}.{os.getenv('SPACES_REGION')}.digitaloceanspaces.com/{test_file_key}"
    print(f"🌐 URL файла: {url}")
    
    # Проверяем существование файла
    print(f"\n🔍 Проверяем файл...")
    response = client.head_object(Bucket=bucket_name, Key=test_file_key)
    print(f"✅ Файл найден! Размер: {response['ContentLength']} bytes")
    
except client.exceptions.NoSuchBucket:
    print(f"❌ Bucket '{bucket_name}' не существует!")
    print("\n💡 Возможные причины:")
    print("   1. Неправильное имя bucket")
    print("   2. Bucket находится в другом регионе")
    print(f"\n   Проверьте в DigitalOcean, что bucket называется именно '{bucket_name}'")
    print(f"   и находится в регионе '{os.getenv('SPACES_REGION')}'")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
