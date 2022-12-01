from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


# создаем еще одну модель, Follow
# в ней должно быть 2 поля:
# кто подписан (user) и на кого подписаны(following)
# для этой модели в документации уже описан эндпоинт /follow/

class Follow(models.Model):
    # поле user будет определено как внешний ключ.
    # оно будет хранить id пользователя, который подписывается
    # т.е. это поле представляет собой отношение к другой таблице/модели - User

    # класс ForeinKey принимает 2 обязательных аргумента
    # 1. модель, с которой происходит связывание - User
    # 2. опция on_delete, которая указывает,
    # что делать при удалении связанного объекта(User)

    # кроме того укажем следующие необязательные аргументы:

    # related_name -
    # имя, используемое для отношения от связанного объекта обратно к нему.

    # verbose_name -
    # понятное для человека имя поля

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    # точно также указываем поле following
    # oно будет определено как внешний ключ.
    # оно будет хранить id пользователя, на которого подписываются
    # т.е. это поле представляет собой отношение к другой таблице/модели - User

    # класс ForeignKey также принимает 2 обязательных аргумента
    # и дополнительно 2 необязательных

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан'
    )

    # добавим в модель класс Meta, так как нам
    # нужно добавить данные о самой модели -
    # укажем в Meta опцию constraints -
    # ограничения, которые мы добавляем в виде списка
    # в нашем списке будет одно ограничение
    # (UniqueConstraint создает уникальное ограничение в БД)
    # пользователь не может подписаться дважды на одного и того же автора
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user', 'following',),
                                    name='unique_follow')
        ]
