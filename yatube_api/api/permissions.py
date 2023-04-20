from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True
        elif not request.user.is_staff:
            raise MethodNotAllowed("Создание группы запрещено.")


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsOwnerOrNoAccess(permissions.BasePermission):
    """
    Проверка, является ли пользователь владельцем аккаунта, для которого
    запрошен список подписок.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user
