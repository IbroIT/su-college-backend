import boto3
import os
from dotenv import load_dotenv

load_dotenv()

client = boto3.client(
    's3',
    region_name=os.getenv('SPACES_REGION'),
    endpoint_url=os.getenv('SPACES_ENDPOINT'),
    aws_access_key_id=os.getenv('SPACES_KEY'),
    aws_secret_access_key=os.getenv('SPACES_SECRET')
)

bucket_name = os.getenv('SPACES_NAME')

print(f"🔍 Список файлов в bucket '{bucket_name}':\n")

try:
    response = client.list_objects_v2(Bucket=bucket_name)
    
    if 'Contents' in response:
        for obj in response['Contents']:
            size_kb = obj['Size'] / 1024
            print(f"  📄 {obj['Key']} ({size_kb:.2f} KB)")
            
            # Формируем URL
            url = f"https://{bucket_name}.{os.getenv('SPACES_REGION')}.digitaloceanspaces.com/{obj['Key']}"
            print(f"     🌐 {url}\n")
    else:
        print("  Bucket пустой")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
