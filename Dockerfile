FROM python:3.10.4-alpine
WORKDIR /code

RUN python3 -m pip install --upgrade pip

COPY ./requirements.txt /src/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /src/requirements.txt

run ls

RUN python3 manage.py migrate
RUN celery -A commercial_net_service worker -d --beat

COPY . /code/

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]