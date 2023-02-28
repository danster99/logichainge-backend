FROM python:3.9-slim-buster

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc git

RUN ls

RUN pip install --upgrade pip && pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip 

COPY . /app/
#CMD alembic upgrade head
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]


CMD uvicorn app.main:app --host 0.0.0.0 --port 8080

