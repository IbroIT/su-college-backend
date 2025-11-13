import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from council_app.models import CouncilMember

print("\n📋 Члены совета и их фото:\n")
members = CouncilMember.objects.all()
for m in members:
    photo_path = m.image.name if m.image else "No photo"
    print(f"  {m.name_ru}: {photo_path}")
    if m.image:
        print(f"    URL: {m.image.url}\n")
