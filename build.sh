#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Create superuser automatically if not exists
python manage.py shell << 'EOF'
from accounts.models import User
if not User.objects.filter(email='codertechmind@gmail.com').exists():
    u = User.objects.create_superuser(
        email='codertechmind@gmail.com',
        password='Charan@123',
        first_name='Charan',
        last_name='Thota'
    )
    u.role = 'admin'
    u.save()
    print('Admin created!')
else:
    print('Admin already exists.')
EOF