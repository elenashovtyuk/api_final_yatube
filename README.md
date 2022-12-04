# Yatube API (api_final_yatube)

gfcyfcyvyfvyvy

## Клонируем проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:elenashovtyuk/api_final_yatube.git
```

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
