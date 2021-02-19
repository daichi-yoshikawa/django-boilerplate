FROM python:3.8.6-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /root/django-app

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends less procps

CMD /bin/bash
