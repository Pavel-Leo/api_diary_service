from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """Позволяет только администраторам выполнять запросы на создание объекта.
    Разрешает запросы только для чтения для всех пользователей."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True
        elif not request.user.is_staff:
            raise MethodNotAllowed("Создание группы запрещено.")


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    """Позволяет только автору объекта выполнять изменяющие его запросы.
    Разрешает запросы только для чтения для всех пользователей.
    """

    def has_object_permission(self, request, view, obj):
        """Проверяет, является ли пользователь автором объекта."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
