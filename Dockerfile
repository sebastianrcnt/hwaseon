FROM python:3.8-alpine3.13

WORKDIR /usr/bin/app
COPY . /usr/bin/app

RUN apk update
RUN apk add gcc libc-dev
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

EXPOSE 8080

CMD python index.py