from rest_framework import filters, mixins, permissions, viewsets
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
# из приложения posts импортируем все нужные модели
from posts.models import Group, Post
# импортируем кастомный пермишн
from .permissions import IsAuthorOrReadOnly
# из приложения api импортируем все нужные сериализаторы
from .serializers import (CommentSerializer,
                          FollowSerializer,
                          GroupSerializer,
                          PostSerializer)


# для всех вьюсетов берем за базовый класс ModelViewSet
# этот класс может обрабатывать все 6 типичных действий
# создаем вьюсеты с указанием 2-ух обязательных полей
# queryset - выборка объектов модели, с которыми будет работать вьюсет
# serializer_class - сериализатор, который будет применяться для
# валидации и сериализации
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    # добавляем кастомный пермишн
    permission_classes = (IsAuthorOrReadOnly,)

    # переопределяем метод perform_create для того,
    # чтобы поле автора не оставалось пустым
    # (в серилизаторе это поле read_only=True)
    # Нужно, чтобы в это поле попала информация из request.user
    # т.е. информация о пользователе, который сделал запрос
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Важный момент!
#  так как для взаимодействия с моделью Group предусмотрены
# только GET-запросы, то мы наследуем этот вьюсет от следующего класса
# ReadOnlyModelViewSet
# этот базовый класс похож на ModelViewSet, но в отличие от него
# он может только получать данные модели,
# но не может их изменять, редактировать или удалять
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# для модели Comment вьюсет - наследник класса ModelViewSet
class CommentViewSet(viewsets.ModelViewSet):
    # выборка queryset = Comment.objects.all() - здесь будет не актуальна
    # согласно ТЗ в модели Comment мы работаем с комментариями или комментарием
    # к КОНКРЕТНОМУ ПОСТУ. Т.е нам не нужна выборка всех комментариев!
    # нам нужна выборка комментов к конкретному посту
    # для этого нам нужно переопределить метод get_queryset

    # указываем сериализатор, котрый будет применяться для
    # валидации и сериализации
    serializer_class = CommentSerializer
    # добавляем кастомный пермишн
    permission_classes = (IsAuthorOrReadOnly,)

    # далее переопределяем метод
    def get_queryset(self):
        # получаем конкретный пост по его идентификатору (или 404)
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        # затем возвращаем все комменты к этому посту, через related_name
        return post.comments.all()

    # теперь переопределяем метод perform_create
    # чтобы в поле автора комментария попала информация
    # о пользователе из запроса
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


# для модели Follow не подходят готовые базовые классы вьюсетов,
# поэтому мы можем "собрать" свой базовый класс на основе нескольких
# миксинов, с подходящим набором действий и на основе  базового класса
# GenericViewSet
# согласно ТЗ с моделью Follow мы можем проделать следующие действия
# ПОЛУЧИТЬ все подписки пользователя, сделавшего запрос
# выполнить подписку (POST) пользователя, от имени которого сделан запрос
# на пользователя, который указан в запросе

# для модели Follow подходят следующие миксины
# CreateModelMixin — создать объект (для обработки запросов POST) - подписка;
# ListModelMixin — вернуть список объектов (для обработки запросов GET)
# - вернуть список подписок;
# плюс укажем базовый класс GenericViewSet
class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    # выборка queryset = Follow.objects.all() - не подходит
    # нам нужны не все подписки, а подписки КОНКРЕТНОГО пользователя,
    # от имени которого сделан  запрос
    # поэтому в этом вьюсете нам также нужно переопределить метод
    # get_queryset
    serializer_class = FollowSerializer
    # согласно ТЗ доступ к эндпоинту /follow/ составляет исключение.
    # На уровне проекта мы задали уровень доступа IsAuthenticatedOrReadOnly
    # это значит, что у анонимных пользователей есть права только на чтение
    # а аутенцифицированные пользователи имеют доступ ко всем ресурсам API
    # Но для follow должен быть доступ только у аутенцифицированных
    # пользователей
    # поэтому мы добавляем новый аттрибут permission_classes
    # и в нем устанавливаем пермишн
    # уже на уровне представления
    permission_classes = (permissions.IsAuthenticated,)
    # для того, чтобы настроить посик по полям во вьюсете Follow
    # нужно импортировать filters из rest_framework
    # и указать 2 аттрибута -
    # filter_backends - здесь мы указываем фильтрующий бэкенд
    # search_fields -  здесь мы указываем поля модели,
    # по которым необходим поиск
    # для того, чтобы выполнить поиск на ForeignKey или ManyToManyField
    # используем двойную подстановочную аннотацию для того,
    # ссылки на свойство некоторого связанного объекта
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=following__username',)

    def get_queryset(self):
        # нужно получить подписки конкретного пользователя
        # инф-ия о котором хранится в request.user
        # через related_name вытаскиваем всех подписчиков пользователя,
        #  сделавшего запрос
        return self.request.user.follower.all()

    # кроме того переопределим метод perform_create
    # чтобы в поле user попала информация о пользователе из запроса
    # эта информация хранится в (request.user)
    def perform_create(self, serializer):
        user = self.request.user
        # если данные валидны, то сохраняем
        if serializer.is_valid():
            serializer.save(user=user)
