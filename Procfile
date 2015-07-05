web: gunicorn -b 0.0.0.0:5000 manage:app --log-file=-
init: python manage.py db init
upgrade: python manage.py db upgrade
