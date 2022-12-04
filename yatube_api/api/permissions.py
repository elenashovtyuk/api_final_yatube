from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    # в методе has_permission проверяем - если метод запроса безопасный
    # или пользователь аутентифицирован, то запрос разрешен
    # но в этом методе инфо об объекте нет
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated)

    # здесь мы проверяем -
    # если метод запроса безопасный
    # или аутентифицированный пользователь из запроса
    # является автором(поста или коммента), то доступ к объекту разрешен
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
    # после создания кастомного пермишн,
    # добавляем его в аттрибут permission_classes
    # в соответствующие представления - PostViewSet, CommentViewSet
