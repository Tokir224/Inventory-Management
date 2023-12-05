# How to run?
### STEPS:

### Python version 3.10.0

Clone the repository

```bash
git clone https://github.com/Tokir224/Inventory-Management.git
cd Inventory-Management
```

### STEP 01- Create a virtual environment after opening the repository

```bash
python -m venv venv
.\venv\Scripts\activate #window
source venv\bin\activate #linux
```

### STEP 02- install the requirements

```bash
pip install -r requirements.txt
```

### STEP 03- Change email creadential and database creadential

```bash
inventory_management\settings\settings.py
EMAIL_HOST_USER = ''   # Replace your email here
EMAIL_HOST_PASSWORD = '' # Replace your email app password here

inventory_management\settings\development.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '', # Replace your DB name here
        'USER': '', # Replace your DB user here
        'PASSWORD': '', # Replace your DB password here
        'HOST': 'localhost',
        'PORT': '5432', # Replace your DB port here
    }
}
```

### STEP 04- Create table inside database

```bash
python manage.py migrate
```

### STEP 05- Install this tools for celery setup

```bash
https://www.erlang.org/downloads
https://www.rabbitmq.com/install-windows.html#installer
```

### STEP 06- run command for celery tasks

```bash
celery -A inventory_management worker -l info --pool=solo
```

### STEP 07- Create superuser for your shop

```bash
python manage.py createsuperuser2
```

### STEP 08- Run server

```bash
python manage.py runserver
```

### Your project is runnning on this URL
```bash
http://127.0.0.1:8000/
```