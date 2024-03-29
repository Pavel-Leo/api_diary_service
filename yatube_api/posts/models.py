from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
TEXT_SYMBOLS: int = 15


class Group(models.Model):
    """Модель группы пользователей."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        """Возвращает строковое представление объекта группы."""
        return self.title[:TEXT_SYMBOLS]


class Post(models.Model):
    """Модель постов."""

    text = models.TextField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="posts",
    )
    image = models.ImageField(upload_to="posts/", null=True, blank=True)

    def __str__(self):
        """Возвращает строковое представление объекта группы."""

        return self.text[:TEXT_SYMBOLS]


class Comment(models.Model):
    """Модель комментариев."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    def __str__(self):
        """Возвращает строковое представление объекта группы."""

        return self.text[:TEXT_SYMBOLS]


class Follow(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    def __str__(self):
        """Возвращает строковое представление объекта группы."""
        return f"{self.user} подписан на {self.following}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"], name="unique_follow"
            )
        ]
