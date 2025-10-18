import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iproject.settings')
django.setup()
from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser admin/admin created.')
else:
    print('Superuser admin already exists.')
