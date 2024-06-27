# Django setup

## How did I set it up
https://docs.djangoproject.com/en/5.0/intro/tutorial01/

django-admin startproject core
rename the outer folder from core to backend

for testing:
python manage.py startapp polls

You can start the server with
```bash
python manage.py runserver
```

```bash
python manage.py makemigrations
python manage.py migrate
```

## Django Auth