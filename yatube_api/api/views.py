from api.permissions import (
    IsAdminOrReadOnlyPermission,
    IsAuthorOrReadOnlyPermission,
    IsOwnerOrNoAccess,
)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from posts.models import Group, Post, Follow
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from . my_viewsets import CreateListViewSet
from . serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с постами.
    Позволяет просматривать, создавать, обновлять и удалять посты.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnlyPermission, permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        """Создает новый пост с автором, равным текущему пользователю."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с сообществами.
    Позволяет просматривать сообщества.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnlyPermission,)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями к постам.
    Позволяет просматривать, создавать, обновлять и удалять комментарии
    к постам.
    """

    serializer_class = CommentSerializer
    # pagination_class = PageNumberPagination
    permission_classes = (IsAuthorOrReadOnlyPermission, permissions.IsAuthenticatedOrReadOnly,)


    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        return post.comments

    def perform_create(self, serializer):
        """Создает новый комментарий к посту."""
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Создает подписку на автора."""
        serializer.save(user=self.request.user)
