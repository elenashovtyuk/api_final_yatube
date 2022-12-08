# Yatube API (api_final_yatube)

## Описание

Проект Yatube API представляет собой REST API для блог-платформы Yatube.
Позволяет просматривать и отправлять посты, просматривать группы, просматривать подписки и подписываться на авторов.

## Используемые технологии

 - Django Rest Framework (библиотека для преобразования Django-приложения в REST API)
 - Postman (графическая программа для тестирования API)

## Ключевые моменты

1. Применены вьюсеты
2. Для аутентификации использованы JWT-токены
3. Аутентифицированным пользователям разрешено изменение и удаление своего контента. В остальных случаях доступ предоставляется только для чтения.
4. Работа с JWT-токенами организована при помощи библиотеки Djoser

# Установка

## Клонируем проект

Клонировать репозиторий и перейти в него в командной строке:

git clone git@github.com:elenashovtyuk/api_final_yatube.git

```
cd api_final_yatube
```

## Разворачиваем проект и окружение

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

 ## Установим зависимости

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

 ## Выполним миграции

```
python3 manage.py migrate
```

 ## Запускаем проект

```
python3 manage.py runserver
```
# Примеры запросов к API

Для доступа к API необходимо получить токен:
Для этого нужно выполнить POST-запрос по указанному эндпоинту с использованием "username" и "password":
```
http://127.0.0.1:8000/api/v1/jwt/create/
```
```
{
    "username": "eshovtyuk",
    "password": "paradox_1"
}
```
API вернет JWT-токен в следующем формате
```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MDMyNDk0MCwianRpIjoiNGE2OGFlZjFjNTU0NDY3YTg4MTljZmM1ZmQ2ZDkzZGEiLCJ1c2VyX2lkIjoxfQ.W_Hbq-okTanriDwBIlSFpR6G2nWBxcAaaJM_DMln41Q",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcwMzI0OTQwLCJqdGkiOiI1NDQzMjUyNmUxZTI0MDQxOWQ3ODlhZThjYzM1Y2I2MyIsInVzZXJfaWQiOjF9.xDYiUYNfzJbKztMSn-EL-0Q_I4dy5roShIxHlP44yq8"
}
```

Этот токен также надо будет передавать в заголовке каждого запроса, в поле Authorization: Bearer <токен>

После это можно обращаться к различным ресурсам API:

```
/api/v1/posts/ (GET, POST)

/api/v1/posts/{id}/ (GET, PUT, PATCH, DELETE)

/api/v1/posts/{post_id}/comments/ (GET, POST)

/api/v1/posts/{post_id}/comments/{id}/ (GET, PUT, PATCH, DELETE)

/api/v1/groups/ (GET)

/api/v1/follow/ (GET, POST)
```

Также можно обновить или проверить JWT-токен

```

/api/v1/jwt/refresh/

/api/v1/jwt/verify/
```

## Автор
Шовтюк Е.
