import boto3, os
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

client = boto3.client(
    's3',
    region_name=os.getenv('SPACES_REGION'),
    endpoint_url=os.getenv('SPACES_ENDPOINT'),
    aws_access_key_id=os.getenv('SPACES_KEY'),
    aws_secret_access_key=os.getenv('SPACES_SECRET')
)

bucket_name = os.getenv('SPACES_NAME')
test_key = 'test_permissions.txt'
test_content = b'Testing write permissions'

print(f"🧪 Тест прав записи в bucket '{bucket_name}'\n")

try:
    # Пробуем записать
    print(f"📤 Попытка загрузки файла: {test_key}")
    client.put_object(
        Bucket=bucket_name,
        Key=test_key,
        Body=BytesIO(test_content),
        ACL='public-read',
        ContentType='text/plain'
    )
    print(f"✅ Файл загружен успешно!")
    
    # Проверяем
    print(f"\n🔍 Проверяем файл...")
    response = client.head_object(Bucket=bucket_name, Key=test_key)
    print(f"✅ Файл найден! Размер: {response['ContentLength']} bytes")
    
    url = f"https://{bucket_name}.{os.getenv('SPACES_REGION')}.digitaloceanspaces.com/{test_key}"
    print(f"✅ URL: {url}")
    
    print(f"\n✅ API ключ имеет права на ЗАПИСЬ!")
    
except Exception as e:
    print(f"❌ ОШИБКА: {e}")
    print(f"\n⚠️  API ключ НЕ имеет прав на запись!")
    print(f"   Зайдите в DigitalOcean Spaces → Settings → API")
    print(f"   Создайте новый ключ с правами Read & Write")
