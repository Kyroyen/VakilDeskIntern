FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /usr/src/app/

