from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    """Позволяет только автору объекта выполнять изменяющие его запросы.
    Разрешает запросы только для чтения для всех пользователей.
    """

    def has_object_permission(self, request, view, obj):
        """Проверяет, является ли пользователь автором объекта."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
