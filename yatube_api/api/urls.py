from django.urls import include, path
# т.к нам нужно получить коллекцию ссылок на все ресурсы API, то
# нам понадобится стандартный роутер DefaultRouter
# он в отличие от второго базового класса SimpleRouter
# генерирует корневой эндпоинт /,
# GET-запрос к которому вернёт список ссылок на все ресурсы, доcтупные в API.
from rest_framework.routers import DefaultRouter

# импортируем все вьюсеты из нашего приложения api
from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet


# для всех вьюсетов нужно создать свои роутер
# с помощью роутеров для заданных вьюсетов создаются эндпоинты по маске адреса

# 1. импортируем класс DefaultRouter и
# создаем в файле urls экземпляр этого класса
router = DefaultRouter()

# 2. для того, чтобы роутер создал необходимый набор эндпоинтов
# для наших вьюсетов необходимо вызвать метод register,
# зарегистрировать эндпоинты
# для этого в качестве аргументов метода register укажем следующие аргументы
# URL-префикс(маска) и название вьюсета,
# для которого создается набор эндпоинтов
router.register(r'posts', PostViewSet, basename='posts')
router.register(
    'posts/(?P<post_id>\\d+)/comments', CommentViewSet, basename='comments')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'follow', FollowViewSet, basename='follow')

# после регистрации эндпоинтов надо включить новые зарегистрированные эндпоинты
# перечень эндпоинтов будет доступен в routers.urls
# включим их в основной urls
urlpatterns = [
    path('v1/', include(router.urls)),
    # Djoser создаст набор необходимых эндпоинтов.
    # базовые - для управления пользователями в Django
    path('v1/', include('djoser.urls')),
    # JWT-эндпоинты для управления JWT-токенами
    path('v1/', include('djoser.urls.jwt')),
]

# ПОСЛЕДОВАТЕЛЬНОСТЬ ДЕЙСТВИЙ ПО ПОДКЛЮЧЕНИЮ И НАСТРОЙКЕ JWT-аутентификации

# 1. Установим и подключим две библиотеки - Djoser, Simple JWT
# 2. Обновим файл settings.py:
# подключим библиотеку к нашему проекту -
# добавим в INSTALLED_APPS приложение djoser (обязательно после
# django.contrib.auth  и rest_framework)
# 3.добавим 'DEFAULT_PERMISSION_CLASSES' и 'DEFAULT_AUTHENTICATION_CLASSES'
# Изменим файл роутинга urls.py

# после проделанных действий становятся доступны следующие эндпоинты в API
# api/v1/jwt/create/
# api/v1/jwt/refresh/
# api/v1/jwt/verify/

# т.е djoser сгенерировал эндпоинты,
# которые управляют токенами и пользователями через API
