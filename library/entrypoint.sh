#!/bin/sh

python manage.py makemigrations
python manage.py migrate

python manage.py loaddata events_fixture.json

echo "from django.contrib.auth.models import User; User.objects.create_superuser('eroma', 'admin@example.com', 'Hjvfy0809')" | python manage.py shell


python manage.py runserver 0.0.0.0:8000
