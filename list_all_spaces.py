import boto3, os
from dotenv import load_dotenv

load_dotenv()
client = boto3.client('s3', region_name=os.getenv('SPACES_REGION'), endpoint_url=os.getenv('SPACES_ENDPOINT'), aws_access_key_id=os.getenv('SPACES_KEY'), aws_secret_access_key=os.getenv('SPACES_SECRET'))

print("\n🔍 ВСЕ файлы в bucket (максимум 100):\n")
response = client.list_objects_v2(Bucket='su-college', MaxKeys=100)

if response.get('Contents'):
    print(f"Всего файлов: {len(response['Contents'])}\n")
    for obj in response.get('Contents', []):
        url = f"https://su-college.blr1.digitaloceanspaces.com/{obj['Key']}"
        size_kb = obj['Size'] / 1024
        print(f"  📄 {obj['Key']} ({size_kb:.2f} KB)")
        print(f"     {url}\n")
else:
    print('  ❌ Bucket пустой или нет доступа')

print(f"\nВсего объектов: {response.get('KeyCount', 0)}")
print(f"IsTruncated: {response.get('IsTruncated', False)}")
