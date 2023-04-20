web: python manage.py migrate  && \
    python manage.py collectstatic --noinput && \
    gunicorn --bind=0.0.0.0:8000 'commercial_net_service.wsgi'