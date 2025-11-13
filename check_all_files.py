import boto3, os
from dotenv import load_dotenv

load_dotenv()
client = boto3.client('s3', region_name=os.getenv('SPACES_REGION'), endpoint_url=os.getenv('SPACES_ENDPOINT'), aws_access_key_id=os.getenv('SPACES_KEY'), aws_secret_access_key=os.getenv('SPACES_SECRET'))

print("\n🔍 Все файлы в bucket (включая вложенные):\n")
response = client.list_objects_v2(Bucket='su-college')
if response.get('Contents'):
    for obj in response.get('Contents', []):
        print(f"  ✅ {obj['Key']} ({obj['Size']} bytes)")
else:
    print('  ❌ Нет файлов')
