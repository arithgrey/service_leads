#!/bin/sh
# Ejecuta las migraciones si es necesario
echo "Microservice stock"
echo "Running makemigrations and migrate..."
echo "Running makemigrations and migrate..."
echo "Running makemigrations and migrate..."
echo "Running makemigrations and migrate..."

python manage.py makemigrations
python manage.py makemigrations lead_type lead lead_search lead_metrics expose
python manage.py migrate
# Inicia el servidor con watchmedo
echo "Starting the server with watchmedo..."
watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- gunicorn -b 0.0.0.0:8080 app.wsgi:application
