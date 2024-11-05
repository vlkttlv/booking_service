# создаем образ приложения фастапи

FROM python:3.12.6

RUN mkdir /booking

WORKDIR /booking

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


