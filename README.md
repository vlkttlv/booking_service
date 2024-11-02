# Веб-сервис для онлайн-бронирования отелей

Этот проект представляет собой веб-приложение, предназначенное для онлайн-бронирования номеров в отелях. Сервис позволяет пользователям искать доступные отели, просматривать информацию о номерах, а также бронировать их на определенные даты.

## Функции сервиса

- **Аутенфикация**: Пользователи могут зарегистрироваться, войти и выйти из аккаунта
- **Поиск отелей**: Пользователи могут фильтровать результаты поиска по различным критериям, таким как местоположение, цена, дата заезды и выезда, услуги в отеле
- **Просмотр комнат в отеле**: Подробная информация о каждой комнате с возможностью бронирования комнаты
- **Бронирование номеров**: Простая процедура бронирования номера
- **Управление бронью**: После завершения бронирования пользователи могут управлять своей бронью через личный кабинет (оплатить или отменить бронь)
- **Добавление отеля/комнаты**: Администратор может добавлять отель или комнату с изображениями в БД
- **Оплата бронирования**: Пользователь может оплатить бронь

## Стек технологий

 **Backend**:
  - Python
  - FastAPI
  - SQLAlchemy
  - Pytest
  - PostgreSQL
  - Redis
  - Celery
  - Stripe
  
 **Frontend**:
  - HTML/CSS
  - JavaScript
  - Bootstrap
  - Jinja

 **Дополнительные инструменты**:
  - Docker
  - Docker compose

## Установка и запуск

### Файл .env:

MODE=DEV <br/>
LOG_LEVEL=INFO <br/>

DB_HOST=  <br/>
DB_PORT= <br/>
DB_USER= <br/>
DB_PASS= <br/>
DB_NAME= <br/>

TEST_DB_HOST= <br/>
TEST_DB_PORT= <br/>
TEST_DB_USER= <br/>
TEST_DB_PASS= <br/>
TEST_DB_NAME= <br/>

SMTP_HOST=smtp.gmail.com <br/>
SMTP_PORT=465 <br/>
SMTP_USER= <br/>
SMTP_PASS= <br/>

REDIS_HOST=localhost <br/>
REDIS_PORT=6379 <br/>

SECRET_KEY= <br/>
ALGORITHM=HS256 <br/>

STRIPE_PUBLISHABLE_KEY= <br/>
STRIPE_SECRET_KEY= <br/>

### Файл .env-for-prod:
MODE=DEV <br/>
LOG_LEVEL=INFO <br/>

DB_HOST=db <br/>
DB_PORT= <br/>
DB_USER= <br/>
DB_PASS= <br/>
DB_NAME=booking_app <br/>

POSTGRES_DB=booking_app <br/>
POSTGRES_USER= <br/>
POSTGRES_PASSWORD= <br/>

SMTP_HOST=smtp.gmail.com <br/>
SMTP_PORT=465 <br/>
SMTP_USER= <br/>
SMTP_PASS= <br/>

REDIS_HOST=redis <br/>
REDIS_PORT=6379 <br/>

SECRET_KEY= <br/>
ALGORITHM=HS256 <br/>

STRIPE_PUBLISHABLE_KEY= <br/>
STRIPE_SECRET_KEY= <br/>

### Миграции alembic
Запуски производятся из командной строки, обязательно находясь в корневой директории проекта
```
alembic upgrade head
```
### Запуск FastAPI
```
uvicorn app.main:app --reload
```
### Запуск celery
```
celery --app=app.tasks.celery:celery worker -l INFO -P solo
```
### Запуск flower
```
celery --app=app.tasks.celery:celery flower
```
### Dockerfile
Для запуска веб-сервера (FastAPI) внутри контейнера необходимо иметь уже запущенный экземпляр PostgreSQL на компьютере. Команда также запускается из корневой директории, в которой лежит файл Dockerfile.
```
docker build .
```  
### Docker compose
Для запуска всех сервисов (БД, Redis, FastAPI, Celery, Flower) необходимо использовать файл docker-compose.yaml и команды
```
docker compose build
docker compose up
```
## Ссылка на приложение
будет позже :) (ссылка на render)

