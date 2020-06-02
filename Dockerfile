FROM python:3.7-alpine3.7

LABEL maintainer="Nolwen Brosson <nolwen.brosson@gmail.com>"
ENV FLASK_APP app.py
ENV MONGODB_URL mongodb://backend_mongo:27017/authentication

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install -r requirements.dev.txt
