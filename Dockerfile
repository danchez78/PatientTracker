FROM python:3.11-alpine

USER root

WORKDIR /app

COPY ./requirements.txt .

RUN python3.11 -m pip install -r requirements.txt

COPY . .

CMD ["python3.11", "-u", "src/start.py"]
