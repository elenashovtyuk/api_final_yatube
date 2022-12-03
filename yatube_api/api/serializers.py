from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
# from rest_framework.relations import SlugRelatedField


# перед созданием сериализаторов
# нужно импортировать все модели из приложения posts
from posts.models import Comment, Follow, Group, Post, User


# создаем сериализатор для модели Comment
# он отвечает за преобразование объектов модели comment в формат JSON и обратно
class CommentSerializer(serializers.ModelSerializer):
    # модель Comment связана с моделью User через поле author
    # по умолчанию у этого поля в сериализаторе
    # будет тип PrimaryKeyRelatedField
    # то есть, мы получим в ответе просто id автора, это не информативно
    # нужно переопределить это поле в сериализаторе
    # укажем 2 аттрибута у этого поля:
    # read_only=True (только для чтения)
    # slug_field='username' - из модели User
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    # также переопределим поле post,
    # через которое модель Comment связана с моделью Post
    post = serializers.PrimaryKeyRelatedField(
        read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


# создаем сериализатор для модели Group
class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


# создаем сериализатор для модели Post
class PostSerializer(serializers.ModelSerializer):
    # модель Post связана с моделью User через поле author
    # если ничего не менять, то по умолчанию это связанное поле
    # будет иметь тип PrimaryKeyRelatedField
    # (т.е мы получим id, а не строковое представление этого поля,
    # а это не информативно)
    # поэтому нужно переопределить это поле в сериализаторе
    # то, что мы передаем в аттрибуте slug_field
    # преобразуется в slug при ответе
    # также указываем аттрибут только для чтения,
    # так как автора публикации нельзя поменять
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    # модель Post связана с моделью Group через поле group
    # по умолчанию это поле также будет иметь тип PrimaryKeyRelatedField
    # т.е мы получим id группы, а не ее название
    # поэтому это поле мы тоже переопределяем
    # в качестве slug_field указываем title из модели Group
    group = serializers.SlugRelatedField(
        slug_field='title', queryset=Group.objects.all(), required=False)

    class Meta:
        model = Post
        fields = '__all__'


# создаем сериализатор для модели Follow
class FollowSerializer(serializers.ModelSerializer):
    # модель Follow связана с моделью User через 2 поля
    # user, following
    # по умолчанию мы будем получать только id подписчика
    #  и того, на кого подписаны
    # это не информативно - надо переопределить эти поля
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),)
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = '__all__'
        # добавляем валидатор UniqueTogetherValidator в класс Meta
        # этот валидатор может использоваться для наложения ограничений
        # unique_together
        # у этого валидатора есть два обязательных аргумента
        # queryset - это набор запросов(выборка подписок), для которых
        # должна быть применена уникальность
        # fields - список или кортеж имен полей, которые должны составлять
        # уникальный набор (поля сериализатора)
        # в нашем случае такой уникальный набор должны составлять оба поля
        # сериализатора FollowSerializer
        # т.е. пользователь не может дважды подписаться на другого пользователя
        # и третий необязательный аргумент - сообщение об ошибке,
        # которое будет выдано в случае сбоя валидации
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=["user", "following"],
                message="Уже подписаны",
            )
        ]

    # этот метод принимает один аргумент - словарь значений полей модели,
    # для которых нам и ттребуется осуществить проверку
    # в данном случае нам нужно проверить,
    # что два поля модели Follow - это не одно и то же,
    # т.е., что тот, на кого подписываются
    # не является сам же подписчиком(на самого себя)

    def validate(self, data):
        # eсли пользователь, выполнивший запрос = тот, на кого подписываются
        # то выбросить исключение SerializerError с сообщением о том, что
        # нельзя подписаться на самого себя
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя!')
        return data
