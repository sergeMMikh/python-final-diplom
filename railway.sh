#!/bin/bash
gunicorn commercial_net_service.wsgi:application --daemon
celery -A commercial_net_service worker --beat