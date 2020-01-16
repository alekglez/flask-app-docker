FROM python:3.7-alpine
LABEL maintainer = "Alejandro Cora Gonzalez <alek.cora.glez@gmail.com>"

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev && \
    rm -rf /var/cache/apk/*

ADD . /flask-app
WORKDIR /flask-app

RUN pip install -r requirements/base.txt
EXPOSE 5000
