#heroku procfile
#web: gunicorn Rendapp.wsgi:application --log-file - --log-level debug

#railway procfile
web: python manage.py migrate && gunicorn Rendapp.wsgi

