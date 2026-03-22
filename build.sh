#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

python manage.py shell << 'EOF'
from accounts.models import User

# Create admin if not exists, or promote existing user
email = 'codertechmind@gmail.com'

if User.objects.filter(email=email).exists():
    u = User.objects.get(email=email)
    u.is_staff = True
    u.is_superuser = True
    u.role = 'admin'
    u.set_password('Charan@123')
    u.save()
    print(f'User {email} promoted to admin!')
else:
    u = User.objects.create_superuser(
        email=email,
        password='Charan@123',
        first_name='Charan',
        last_name='Thota'
    )
    u.role = 'admin'
    u.save()
    print(f'Admin {email} created!')
EOF