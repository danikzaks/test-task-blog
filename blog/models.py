from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from django.db.models import QuerySet


class SeoMeta(models.Model):
    SEO_ROBOTS_CHOICES = [
        ("index, follow", "Индексировать, следовать"),
        ("noindex, nofollow", "Не индексировать, не следовать"),
        ("noindex, follow", "Не индексировать, следовать"),
        ("index, nofollow", "Индексировать, не следовать"),
    ]

    title = models.CharField(
        max_length=255, verbose_name="Мета-Title", help_text="Мета-заголовок для SEO."
    )
    description = models.TextField(
        verbose_name="Мета-Описание", help_text="Мета-описание для SEO."
    )
    robots = models.CharField(
        max_length=255,
        choices=SEO_ROBOTS_CHOICES,
        default="index, follow",
        verbose_name="Мета-Роботы",
        help_text="Настройки для поисковых роботов (например, 'index, follow').",
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего обновления"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="seo_meta_updates",
        verbose_name="Последний обновивший",
    )

    class Meta:
        verbose_name = "SEO Мета-теги"
        verbose_name_plural = "SEO Мета-теги"
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            models.Index(fields=["updated_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} - {self.robots}"


class Rubric(models.Model):
    name: str = models.CharField(
        max_length=255,
        verbose_name="Название рубрики",
        help_text="Название рубрики, которое будет отображаться на сайте.",
    )
    description: str = models.TextField(
        verbose_name="Описание рубрики",
        help_text="Описание рубрики для SEO.",
        blank=True,
    )
    seo_meta: GenericRelation = GenericRelation(SeoMeta, related_query_name="rubric")
    created_at: Optional[models.DateTimeField] = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    updated_at: Optional[models.DateTimeField] = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего обновления"
    )
    updated_by: Optional[models.ForeignKey] = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rubric_updates",
        verbose_name="Последний обновивший",
    )

    class Meta:
        verbose_name = "Рубрика"
        verbose_name_plural = "Рубрики"
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["updated_at"]),
            models.Index(fields=["updated_by"]),
        ]

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    PUBLISH_STATUS_CHOICES = [
        ("draft", "Черновик"),
        ("published", "Опубликован"),
        ("archived", "Архивирован"),
    ]

    title: str = models.CharField(
        max_length=255, verbose_name="Заголовок поста", help_text="Заголовок поста."
    )
    content: str = models.TextField(
        verbose_name="Контент поста", help_text="Основной текст поста."
    )
    image: Optional[models.ImageField] = models.ImageField(
        upload_to="posts/",
        verbose_name="Изображение",
        help_text="Изображение для поста.",
        null=True,
        blank=True,
    )
    created_at: Optional[models.DateTimeField] = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата, когда пост был создан.",
    )
    updated_at: Optional[models.DateTimeField] = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего обновления",
        help_text="Дата последнего изменения поста.",
    )
    rubric: models.ForeignKey = models.ForeignKey(
        Rubric,
        related_name="posts",
        on_delete=models.CASCADE,
        verbose_name="Рубрика",
        help_text="Рубрика, к которой относится данный пост.",
    )
    seo_meta: GenericRelation = GenericRelation(SeoMeta, related_query_name="post")

    status: str = models.CharField(
        max_length=10,
        choices=PUBLISH_STATUS_CHOICES,
        default="draft",
        verbose_name="Статус публикации",
        help_text="Статус поста: Черновик, Опубликован или Архивирован.",
    )

    updated_by: Optional[models.ForeignKey] = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="post_updates",
        verbose_name="Последний обновивший",
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["rubric"]),
            models.Index(fields=["status"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["updated_by"]),
        ]

    def __str__(self) -> str:
        return self.title
