import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Загружаем dotenv ДО импорта Django
from dotenv import load_dotenv
load_dotenv()

print(f"USE_SPACES env: {os.getenv('USE_SPACES')}")

import django
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage

print(f"\nDjango USE_SPACES: {os.getenv('USE_SPACES', 'False') == 'True'}")
print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
print(f"Storage class: {default_storage.__class__.__name__}")
print(f"Storage module: {default_storage.__class__.__module__}")
