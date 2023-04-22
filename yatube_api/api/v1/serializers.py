import base64
from typing import Tuple

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Переопределяет поведение поля изображения."""

    def to_internal_value(self, data):
        """Преобразует данные внутреннего представления поля.
        Поле должно принимать данные в формате base64."""
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext: str = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для постов."""

    author: serializers.SlugRelatedField = SlugRelatedField(
        slug_field="username", read_only=True
    )
    image: Base64ImageField = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields: Tuple[str] = (
            "id",
            "text",
            "author",
            "pub_date",
            "image",
            "group",
        )
        model: Post = Post


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для сообществ."""

    class Meta:
        model: Group = Group
        fields: Tuple[str] = (
            "id",
            "title",
            "slug",
            "description",
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    author: serializers.SlugRelatedField = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model: Comment = Comment
        fields: Tuple[str] = (
            "id",
            "text",
            "author",
            "post",
            "created",
        )
        read_only_fields: Tuple[str] = ("post",)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""

    user: serializers.SlugRelatedField = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field="username",
    )
    following: serializers.SlugRelatedField = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model: Follow = Follow
        fields: Tuple[str] = "user", "following"
        read_only_fields: Tuple[str] = (
            "id",
            "user",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=("user", "following")
            )
        ]

    def validate_following(self, value):
        if value == self.context["request"].user:
            raise serializers.ValidationError(
                "Нельзя подписываться на самого себя."
            )
        return value
