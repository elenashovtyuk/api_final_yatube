# TODO:  Напишите свой вариант
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from posts.models import Comment, Follow, Group, Post
from .serializers import CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # переопределяем метод perform_create для того,
    # чтобы поле автора не оставалось пустым
    # Нужно, чтобы в это поле попала информация из request.user
    # т.е. информация о пользователе, который сделал запрос
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    # queryset = Comment.objects.all() - здесь будет не актуальна
    # согласно ТЗ в модели Comment мы работаем с комментариями или комментарием
    # к КОНКРЕТНОМУ ПОСТУ. Т.е нам не нужна выборка всех комментариев!
    # нам нужна выборка комментов к конкретному посту
    # для этого нам нужно переопределить метод get_queryset
    serializer_class = CommentSerializer
    # переопределяем метод
    def get_queryset(self):
        # получаем конкретный пост по его идентификатору
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        # затем возвращаем все комменты к этому посту
        return post.comments.all()

    # теперь переопределяем метод perform_create
    # чтобы в поле автора комментария попала информация
    # о пользователе из запроса
    def perform_create(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
