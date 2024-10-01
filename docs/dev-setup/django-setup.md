## Setup Django


Create a virtual enviroment and install dependencies in the backend folder

```bash
python -m venv venv
pip install -r requierements.txt
```

Create local user for you django

```bash
python manage.py createsuperuser
```

Start backend server by running

```bash
python manage.py makemigrations
python manage.py runserver
```