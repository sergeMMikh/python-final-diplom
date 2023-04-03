release: python manage.py migrate
web: gunicorn commercial_net_service.wsgi:application
worker: celery -A commercial_net_service worker --beat