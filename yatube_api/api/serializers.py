from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


# перед созданием сериализаторов
# нужно импортировать все модели из приложения posts
from posts.models import Comment, Follow, Group, Post, User


# создаем сериализатор для модели Comment
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
        fields = '__all__'
        model = Comment


# создаем сериализатор для модели Group
class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


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
    author = SlugRelatedField(slug_field='username', read_only=True)
    # модель Post связана с моделью Group через поле group
    # по умолчанию это поле также будет иметь тип PrimaryKeyRelatedField
    # т.е мы получим id группы, а не ее название
    # поэтому это поле мы тоже переопределяем
    # в качестве slug_field указываем title из модели Group
    group = SlugRelatedField(
        slug_field='title', queryset=Group.objects.all(), required=False)

    class Meta:
        fields = '__all__'
        model = Post


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
        fields = '__all__'
        model = Follow
